import argparse
import pandas as pd
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw_path', default='data/raw/multitude_v3_clean.csv')
    parser.add_argument('--splits_path', default='data/processed/splits_8class.csv')
    args = parser.parse_args()

    splits = pd.read_csv(args.splits_path)
    raw = pd.read_csv(args.raw_path)
    if 'Unnamed: 0' in raw.columns:
        raw = raw.rename(columns={'Unnamed: 0': 'row_id'})
    else:
        raw['row_id'] = raw.index

    df = splits[splits['group_id'] != -1].merge(raw[['row_id', 'source']], on='row_id', how='left')

    num_groups = df['group_id'].nunique()
    print(f"Number of groups (excl -1): {num_groups}")

    num_human = df[df['multi_label'] == 'human']['row_id'].nunique()
    print(f"Number of human anchors: {num_human}")

    group_counts = df.groupby('group_id')['multi_label'].value_counts().unstack(fill_value=0)
    if 'human' not in group_counts.columns:
        group_counts['human'] = 0
    group_counts['machine'] = group_counts.sum(axis=1) - group_counts['human']
    humans_no_machine = (group_counts['human'] > 0) & (group_counts['machine'] == 0)
    print(f"Humans with no attached machine text: {humans_no_machine.sum()}")

    group_sizes = df.groupby('group_id').size()
    print(f"Group size min: {group_sizes.min()}")
    print(f"Group size median: {group_sizes.median()}")
    print(f"Group size p90: {np.percentile(group_sizes, 90)}")
    print(f"Group size max: {group_sizes.max()}")

    print("Top 10 largest groups:")
    largest = group_sizes.nlargest(10)
    for g_id, size in largest.items():
        g_df = df[df['group_id'] == g_id]
        lang = g_df['language'].iloc[0]
        outlet = g_df['source'].iloc[0]
        print(f"- Group {g_id}: size {size}, {lang}, {outlet}")

if __name__ == '__main__':
    main()
