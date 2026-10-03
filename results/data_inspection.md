# Data Inspection Report

**Error**: `data/raw/multitude_v3_clean.csv` does not exist. Data inspection cannot be performed until the data is uploaded.

## 8. Split Design Proposal


### Grouping & Leakage
Since there is **no explicit original article/headline ID** in this dataset (`source` just identifies the dataset origin like 'multitude'), we cannot group strictly by article ID. 
To carve a validation set from `train` without leakage, we must group by **`norm_hash` (normalized text hash)**. 
**Limits:** Grouping by `norm_hash` only prevents identical or nearly-identical texts from crossing the train/val split. If a human article was rewritten by two different generators, they will have different hashes and might end up in different splits. This is an unavoidable limitation of not having article IDs. We must strictly ensure that `norm_hash` intersection between train and val is zero. Furthermore, any train texts that share a `norm_hash` with the fixed `test` set must be completely purged to eliminate test leakage.

### Duplicates
- **Test-in-Train Leakage**: All train rows that have a `norm_hash` present in `test` MUST BE DROPPED.
- **Within-Train Duplicates**: Retaining near-duplicates (e.g. same text generated multiple times or slight variations) within the same split (train or val) is generally safe, but deduplicating exact/near exact texts in train can prevent overfitting on common templates. We propose removing all within-train near-duplicates (`keep='first'`).

### Class Weighting
Class balance varies significantly per cluster (e.g., human vs AI classes, and between different generators). 
Because the loss is calculated over imbalanced classes, **Class Weighting** inside the CrossEntropyLoss is highly recommended, or at least a balanced sampler during training, to prevent the majority classes (often Human or a specific generator) from dominating the gradients.
