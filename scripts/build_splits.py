import pandas as pd
import numpy as np
import hashlib
import string
import re
import os
import sys
import json
import regex
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import StratifiedGroupKFold
import networkx as nx

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.clusters import get_cluster, BASE_PAPER_18_LANGUAGES, LANG_TO_CLUSTER
from transformers import AutoTokenizer

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

def detect_dominant_script(text):
    script_counts = {
        'latin': len(regex.findall(r'\p{IsLatin}', text)),
        'cyrillic': len(regex.findall(r'\p{IsCyrillic}', text)),
        'greek': len(regex.findall(r'\p{IsGreek}', text)),
        'arabic': len(regex.findall(r'\p{IsArabic}', text)),
        'hanzi': len(regex.findall(r'\p{IsHan}', text))
    }
    total = sum(script_counts.values())
    if total == 0:
        return 'unknown'
    return max(script_counts, key=script_counts.get)

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
    print("Loading data...")
    df = pd.read_csv(raw_path)
    
    if 'Unnamed: 0' in df.columns:
        df = df.rename(columns={'Unnamed: 0': 'row_id'})
    else:
        df['row_id'] = df.index

    df['text'] = df['text'].fillna('')
    df['norm_hash'] = df['text'].apply(lambda x: hash_text(normalize_text(x)))

    # Flags calculation
    print("Calculating flags...")
    # 1. Junk
    df['flag_junk'] = df['text'].apply(lambda x: len(regex.findall(r'\p{L}', x)) < 20)
    
    # 2. Script mismatch
    df['cluster'] = df['language'].apply(lambda x: get_cluster(x) if x in LANG_TO_CLUSTER else 'unknown')
    df['dominant_script'] = df['text'].apply(detect_dominant_script)
    df['flag_script_mismatch'] = df['dominant_script'] != df['cluster']
    
    # 3. Prompt echo
    # Patterns specified in the prompt: "task write", "task translate", "leave out the", "return just the", "you are a", "your article in", "a news article in", "the article in", "text of the", "here is a", "title:"
    prompt_patterns = r'(?i)\b(task write|task translate|leave out the|return just the|you are a|your article in|a news article in|the article in|text of the|here is a|title:)\b'
    prompt_regex = re.compile(prompt_patterns)
    df['flag_prompt_echo'] = df['text'].apply(lambda x: bool(prompt_regex.search(x[:200])))
    
    # 4. Length tokens
    print("Tokenizing for lengths...")
    tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-large")
    df['length_tokens'] = df['text'].apply(lambda x: len(tokenizer.encode(x, add_special_tokens=True, max_length=512, truncation=True)))
    
    empty_hash = hash_text("")

    # Drop ca, ga, gd
    ca_ga_gd = df[df['language'].isin(['ca', 'ga', 'gd'])]
    ca_ga_gd[['row_id']].to_csv('results/ca_ga_gd_ids.csv', index=False)
    df = df[df['language'].isin(BASE_PAPER_18_LANGUAGES)].copy()
    
    # Drop Gemini/Claude entirely from train and test paths
    df = df[~df['multi_label'].astype(str).str.contains('Gemini|Claude', case=False, na=False)]
    
    test_df = df[df['split'] == 'test'].copy()
    train_df = df[df['split'] == 'train'].copy()
    
    # Test-in-train purge excluding empty hash
    test_hashes = set(test_df[test_df['norm_hash'] != empty_hash]['norm_hash'])
    train_df = train_df[~((train_df['norm_hash'].isin(test_hashes)) & (train_df['norm_hash'] != empty_hash))].copy()
    
    # Within-train deduplication
    train_df = train_df.drop_duplicates(subset=['norm_hash'], keep='first').copy()
    
    train_df['outlet'] = train_df['source'].apply(lambda x: str(x).replace('MULTITuDE_', ''))
    
    print("Building story groups using new linking strategy...")
    group_id_counter = 0
    train_df['group_id'] = -1
    
    total_groups = 0
    singletons = 0
    groups_exactly_1_human = 0
    
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
        
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4), max_features=5000)
        try:
            tfidf = vectorizer.fit_transform(group_df['text'].fillna(''))
        except ValueError:
            for idx in group_df.index:
                train_df.at[idx, 'group_id'] = group_id_counter
                group_id_counter += 1
            continue
            
        sim_matrix = cosine_similarity(tfidf)
        
        # We attach each machine text to the single best matching human text
        human_indices = np.where(group_df['label'].values == 0)[0]
        machine_indices = np.where(group_df['label'].values == 1)[0]
        
        # Each human starts its own group
        local_groups = {h: [h] for h in human_indices}
        
        for m_idx in machine_indices:
            sims = sim_matrix[m_idx, human_indices]
            best_h = human_indices[np.argmax(sims)]
            local_groups[best_h].append(m_idx)
            
        # Assign group ids
        for h, members in local_groups.items():
            for m in members:
                df_idx = group_df.index[m]
                train_df.at[df_idx, 'group_id'] = group_id_counter
            group_id_counter += 1

    print("Extracting grouping diagnostics...")
    group_sizes = []
    
    for g_id, g_df in train_df.groupby('group_id'):
        total_groups += 1
        size = len(g_df)
        group_sizes.append(size)
        if size == 1:
            singletons += 1
        
        if sum(g_df['label'] == 0) == 1:
            groups_exactly_1_human += 1
            
    print("StratifiedGroupKFold Validation Splitting...")
    train_df['final_split'] = 'train'
    val_indices = []
    
    # 10 folds, seed 42
    for cluster in train_df['cluster'].unique():
        c_df = train_df[train_df['cluster'] == cluster]
        if len(c_df) < 10:
            continue
            
        # Grouped by group_id, stratified by multi_label
        sgkf = StratifiedGroupKFold(n_splits=10, shuffle=True, random_state=42)
        try:
            # next(sgkf.split(X, y, groups))
            # returns train_idx, test_idx (which is our val)
            train_idx, val_idx = next(sgkf.split(c_df, c_df['multi_label'], c_df['group_id']))
            val_indices.extend(c_df.iloc[val_idx].index)
        except ValueError:
            pass # Too few groups or classes to split
            
    train_df.loc[val_indices, 'final_split'] = 'val'
    test_df['group_id'] = -1
    test_df['final_split'] = 'test'
    
    final_cols = ['row_id', 'cluster', 'language', 'multi_label', 'final_split', 'group_id', 'flag_junk', 'flag_script_mismatch', 'flag_prompt_echo', 'length_tokens']
    final_df = pd.concat([train_df[final_cols], test_df[final_cols]])
    final_df = final_df.rename(columns={'final_split': 'split'})
    
    final_df.to_csv(out_path, index=False)
    out_sha256 = get_file_hash(out_path)
    
    print("Writing report...")
    report = ["# Split Design Report\n"]
    report.append(f"- **Raw CSV SHA-256**: {raw_sha256}")
    report.append(f"- **Splits CSV SHA-256**: {out_sha256}")
    
    report.append("\n## Story Grouping Diagnostics")
    report.append(f"- **Total groups**: {total_groups}")
    report.append(f"- **Singleton rate**: {singletons / total_groups:.2%} ({singletons} / {total_groups})")
    non_singletons = total_groups - singletons
    if non_singletons > 0:
        report.append(f"- **Groups with exactly 1 human**: {groups_exactly_1_human} ({(groups_exactly_1_human/non_singletons):.2%} of non-singletons)")
    else:
        report.append(f"- **Groups with exactly 1 human**: {groups_exactly_1_human} (0% of non-singletons)")
        
    report.append("\n## Group Size Histogram")
    size_counts = pd.Series(group_sizes).value_counts().sort_index()
    for s, c in size_counts.items():
        if s <= 10 or s % 5 == 0:
            report.append(f"- Size {s}: {c} groups")
            
    report.append("\n## Flag Distributions")
    report.append("| Cluster | Split | Generator | Junk | Script Mismatch | Prompt Echo |")
    report.append("|---|---|---|---|---|---|")
    
    for cluster in final_df['cluster'].unique():
        for split in ['train', 'val', 'test']:
            c_df = final_df[(final_df['cluster'] == cluster) & (final_df['split'] == split)]
            for gen in c_df['multi_label'].unique():
                g_df = c_df[c_df['multi_label'] == gen]
                n_junk = g_df['flag_junk'].sum()
                n_script = g_df['flag_script_mismatch'].sum()
                n_prompt = g_df['flag_prompt_echo'].sum()
                if n_junk + n_script + n_prompt > 0:
                    report.append(f"| {cluster} | {split} | {gen} | {n_junk} | {n_script} | {n_prompt} |")
                    
    report.append("\n## Class Balance (Counts & Min/Max Ratio)")
    report.append("| Cluster | Split | Max/Min Ratio | Counts |")
    report.append("|---|---|---|---|")
    for cluster in final_df['cluster'].unique():
        for split in ['train', 'val', 'test']:
            c_df = final_df[(final_df['cluster'] == cluster) & (final_df['split'] == split)]
            if len(c_df) == 0: continue
            counts = c_df['multi_label'].value_counts()
            ratio = counts.max() / counts.min() if counts.min() > 0 else float('inf')
            counts_str = ", ".join([f"{k}: {v}" for k, v in counts.items()])
            report.append(f"| {cluster} | {split} | {ratio:.2f} | {counts_str} |")
            
    report.append("\n### Prompt patterns flagged")
    report.append(f"`{prompt_patterns}`")

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
        
    print(f"Done. Splits written to {out_path}, report to {report_path}")

if __name__ == '__main__':
    build_splits()
