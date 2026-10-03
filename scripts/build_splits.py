import pandas as pd
import numpy as np
import hashlib
import string
import re
import os
import sys
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import GroupShuffleSplit
import networkx as nx

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.clusters import get_cluster, BASE_PAPER_18_LANGUAGES
import hashlib

def normalize_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)
    return text.strip()

def hash_text(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def get_file_hash(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for block in iter(lambda: f.read(65536), b''):
            sha256.update(block)
    return sha256.hexdigest()

def build_splits():
    raw_path = 'data/raw/multitude_v3_clean.csv'
    out_path = 'data/processed/splits_8class.csv'
    report_path = 'results/split_report.md'
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('results', exist_ok=True)

    if not os.path.exists(raw_path):
        print(f"Error: {raw_path} not found.")
        sys.exit(1)
    
    raw_sha256 = get_file_hash(raw_path)
    
    df = pd.read_csv(raw_path)
    
    # Check id column
    if 'Unnamed: 0' in df.columns:
        df = df.rename(columns={'Unnamed: 0': 'row_id'})
    else:
        df['row_id'] = df.index

    # 1. Scope (drop ca, ga, gd)
    ca_ga_gd = df[df['language'].isin(['ca', 'ga', 'gd'])]
    ca_ga_gd[['row_id']].to_csv('results/ca_ga_gd_ids.csv', index=False)
    
    df = df[df['language'].isin(BASE_PAPER_18_LANGUAGES)].copy()
    
    # Calculate norm hash for deduplication/leakage
    df['norm_hash'] = df['text'].apply(lambda x: hash_text(normalize_text(x)))
    
    # 2. Test split
    test_df = df[df['split'] == 'test'].copy()
    train_df = df[df['split'] == 'train'].copy()
    
    test_hashes = set(test_df['norm_hash'])
    train_df = train_df[~train_df['norm_hash'].isin(test_hashes)].copy()
    
    # Drop within-train near-duplicates
    train_df = train_df.drop_duplicates(subset=['norm_hash'], keep='first').copy()
    
    # 3. Story grouping
    train_df['outlet'] = train_df['source'].apply(lambda x: str(x).replace('MULTITuDE_', ''))
    
    # Pre-cluster assignment
    from src.clusters import LANG_TO_CLUSTER
    train_df['cluster'] = train_df['language'].apply(lambda x: get_cluster(x) if x in LANG_TO_CLUSTER else 'unknown')
    test_df['cluster'] = test_df['language'].apply(lambda x: get_cluster(x) if x in LANG_TO_CLUSTER else 'unknown')
    
    print("Building story groups using TF-IDF cosine similarity...")
    group_id_counter = 0
    train_df['group_id'] = -1
    
    # To store diagnostics
    group_sizes = []
    groups_exactly_1_human = 0
    groups_at_most_1_per_gen = 0
    total_groups = 0
    singletons = 0
    random_groups_samples = []

    for (lang, outlet), group_df in train_df.groupby(['language', 'outlet']):
        if len(group_df) <= 1:
            for idx in group_df.index:
                train_df.at[idx, 'group_id'] = group_id_counter
                group_id_counter += 1
            continue
            
        humans = group_df[group_df['label'] == 0]
        machines = group_df[group_df['label'] == 1]
        
        if len(humans) == 0 or len(machines) == 0:
            for idx in group_df.index:
                train_df.at[idx, 'group_id'] = group_id_counter
                group_id_counter += 1
            continue
        
        # TF-IDF on char n-grams and word n-grams
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), max_features=5000)
        try:
            tfidf = vectorizer.fit_transform(group_df['text'].fillna(''))
        except ValueError: # Empty vocab
            for idx in group_df.index:
                train_df.at[idx, 'group_id'] = group_id_counter
                group_id_counter += 1
            continue
            
        sim_matrix = cosine_similarity(tfidf)
        
        G = nx.Graph()
        G.add_nodes_from(range(len(group_df)))
        
        # Link machines to most similar human
        human_indices = np.where(group_df['label'].values == 0)[0]
        machine_indices = np.where(group_df['label'].values == 1)[0]
        
        for m_idx in machine_indices:
            sims = sim_matrix[m_idx, human_indices]
            best_h = human_indices[np.argmax(sims)]
            # Threshold could be 0.2
            if sims.max() > 0.15:
                G.add_edge(m_idx, best_h)
        
        components = list(nx.connected_components(G))
        for comp in components:
            comp_indices = list(comp)
            df_indices = group_df.iloc[comp_indices].index
            for idx in df_indices:
                train_df.at[idx, 'group_id'] = group_id_counter
            group_id_counter += 1

    print("Grouping done. Extracting diagnostics...")
    grouped = train_df.groupby('group_id')
    for g_id, g_df in grouped:
        total_groups += 1
        size = len(g_df)
        group_sizes.append(size)
        if size == 1:
            singletons += 1
        
        if sum(g_df['label'] == 0) == 1:
            groups_exactly_1_human += 1
        
        # Check if at most one text per generator (multi_label)
        machine_counts = g_df[g_df['label'] == 1]['multi_label'].value_counts()
        if len(machine_counts) == 0 or machine_counts.max() <= 1:
            groups_at_most_1_per_gen += 1
            
        if total_groups % max(1, (len(train_df)//500)) == 0 and len(random_groups_samples) < 20 and size > 1:
            random_groups_samples.append(g_df)

    # 4. Validation Split (GroupShuffleSplit, ~10% groups per cluster)
    train_df['final_split'] = 'train'
    val_indices = []
    
    print("Carving validation set...")
    for cluster in train_df['cluster'].unique():
        cluster_df = train_df[train_df['cluster'] == cluster]
        gss = GroupShuffleSplit(n_splits=1, test_size=0.10, random_state=42)
        try:
            train_idx, val_idx = next(gss.split(cluster_df, groups=cluster_df['group_id']))
            val_indices.extend(cluster_df.iloc[val_idx].index)
        except ValueError:
            pass # Not enough groups
    
    train_df.loc[val_indices, 'final_split'] = 'val'
    
    # Also we must ensure Gemini/Claude are dropped entirely from everywhere (Phase B instructions)
    # The instructions say: "no Gemini/Claude labels".
    train_df = train_df[~train_df['multi_label'].astype(str).str.contains('Gemini|Claude', case=False, na=False)]
    test_df = test_df[~test_df['multi_label'].astype(str).str.contains('Gemini|Claude', case=False, na=False)]
    
    test_df['group_id'] = -1
    test_df['final_split'] = 'test'
    
    # 5. Output
    final_df = pd.concat([
        train_df[['row_id', 'cluster', 'language', 'multi_label', 'final_split', 'group_id']],
        test_df[['row_id', 'cluster', 'language', 'multi_label', 'final_split', 'group_id']]
    ])
    final_df = final_df.rename(columns={'final_split': 'split'})
    
    final_df.to_csv(out_path, index=False)
    out_sha256 = get_file_hash(out_path)
    
    print("Writing report...")
    report = ["# Split Design Report\n"]
    report.append(f"- **Raw CSV SHA-256**: {raw_sha256}")
    report.append(f"- **Splits CSV SHA-256**: {out_sha256}")
    
    report.append("\n## Story Grouping Diagnostics")
    report.append(f"- **Total groups**: {total_groups}")
    report.append(f"- **Singleton rate**: {singletons / total_groups:.2%}")
    report.append(f"- **Groups with exactly 1 human**: {groups_exactly_1_human} ({(groups_exactly_1_human/max(1, total_groups-singletons)):.2%} of non-singletons)")
    report.append(f"- **Groups with <= 1 text per generator**: {groups_at_most_1_per_gen} ({(groups_at_most_1_per_gen/total_groups):.2%} of all groups)")
    
    well_formed_rate = groups_at_most_1_per_gen / total_groups
    if well_formed_rate < 0.70:
        report.append("\n**WARNING**: Grouping looks poor (well-formed rate < 70%). Fallback to purely random grouping might be necessary, though current groups are used for val splitting.")
    else:
        report.append("\nGrouping looks acceptable (>= 70% well-formed).")
        
    report.append("\n### 20 Random Groups Sample")
    for idx, grp in enumerate(random_groups_samples[:20]):
        report.append(f"\n**Group {idx+1} (Size: {len(grp)}):**")
        for _, row in grp.iterrows():
            lbl = row['multi_label']
            text_snippet = str(row['text'])[:150].replace('\n', ' ')
            report.append(f"- `{lbl}`: {text_snippet}...")
            
    report.append("\n## Class Balance (Counts & Min/Max Ratio)")
    stats = []
    for cluster in final_df['cluster'].unique():
        for split in ['train', 'val', 'test']:
            c_df = final_df[(final_df['cluster'] == cluster) & (final_df['split'] == split)]
            if len(c_df) == 0:
                continue
            counts = c_df['multi_label'].value_counts()
            ratio = counts.max() / counts.min() if counts.min() > 0 else float('inf')
            counts_str = ", ".join([f"{k}: {v}" for k, v in counts.items()])
            stats.append(f"| {cluster} | {split} | {ratio:.2f} | {counts_str} |")
            
    report.append("| Cluster | Split | Max/Min Ratio | Counts |")
    report.append("|---|---|---|---|")
    report.extend(stats)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    print(f"Done. Splits written to {out_path}, report to {report_path}")

if __name__ == '__main__':
    build_splits()
