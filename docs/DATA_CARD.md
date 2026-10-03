# MULTITuDE V3 Clean - Data Card

## Dataset Facts
- **Source**: `data/raw/multitude_v3_clean.csv`
- **Total Rows**: 206,330
- **Task**: 8-class AI text attribution (1 human class, 7 AI generator classes)
- **SHA-256 (Raw)**: 1e08f9c6980ed9cae11bc831d8ce54d13125ea9a52dfef387b0b4ebd0909647c
- **SHA-256 (Splits File)**: 922da64859257236e5d06a38ee3c39aa54819972996edc120a1ac1f71ae1e707

## Languages
- **Included (18 Base-Paper Languages)**: ar, bg, cs, de, el, en, es, hr, hu, nl, pl, pt, ro, ru, sk, sl, uk, zh
- **Excluded Set**: ca, ga, gd (These 3 languages were removed from the training, validation, and test splits and are kept strictly for zero-shot testing).

## Splits Method and Limitations
The dataset was split into train, val, and test partitions using **story grouping**. Machine-generated texts were attached to the group of their single best-matching human text via TF-IDF cosine similarity within each language and outlet bucket to prevent story leakage. 
- **Validation Leakage**: In 14 out of 18 languages, the `val->train` similarity is higher than the `test->train` similarity, meaning the validation set is leakier than the test set.
- **Exceptions (hu, pl, ro)**: For Hungarian (hu), Polish (pl), and Romanian (ro), the validation split is actually more similar to the train split than a purely random control, indicating the grouped split leaked more in these languages.
- **Giant Groups**: Over-merging was preferred to under-linking, but this resulted in massive groups in some languages (e.g., the largest group is an `el` group with 821 rows, and there are several groups > 200 rows). The original test split rows (which were not regrouped) were assigned a placeholder group ID of `-1`. 

## Flag Definitions
- `flag_junk`: 
  - For Latin, Cyrillic, Greek, and Arabic clusters: True if the text contains fewer than 20 letter characters.
  - For the Hanzi cluster: True if the text contains fewer than 5 CJK ideographs or Kana characters.
- `flag_script_mismatch`: True if the text contains mostly out-of-cluster characters for its language's designated script cluster.
- `flag_prompt_echo`: True if the text contains one of the known prompt-leakage regex patterns (e.g. `(?i)\b(task write|task translate...)\b`).
- `story_disjoint`: True if the row's maximum cosine similarity to any train row of a different label in the same language is strictly less than 0.7 (`max_sim_train_other < 0.7`).

## Story Disjointness
The `max_sim_train_other` column measures the maximum TF-IDF cosine similarity of a val or test row to any train row of a different label in the same language. The `story_disjoint` flag is True if this similarity is strictly less than 0.7. These columns measure the "cleanliness" of the test and validation sets against story leakage from the train set (i.e. ensuring a machine-generated text in the test set does not have its original human anchor story in the train set). 

Share of `story_disjoint` rows per language:

**VAL**:
- ar: 99.5% disjoint
- bg: 99.3% disjoint
- cs: 100.0% disjoint
- de: 99.6% disjoint
- el: 100.0% disjoint
- en: 94.7% disjoint
- es: 98.1% disjoint
- hr: 99.6% disjoint
- hu: 95.2% disjoint
- nl: 98.9% disjoint
- pl: 96.3% disjoint
- pt: 98.9% disjoint
- ro: 94.1% disjoint
- ru: 96.5% disjoint
- sk: 99.4% disjoint
- sl: 99.9% disjoint
- uk: 99.3% disjoint
- zh: 95.3% disjoint

**TEST**:
- ar: 97.8% disjoint
- bg: 97.4% disjoint
- cs: 97.8% disjoint
- de: 99.2% disjoint
- el: 97.7% disjoint
- en: 97.8% disjoint
- es: 98.4% disjoint
- hr: 98.6% disjoint
- hu: 98.8% disjoint
- nl: 98.8% disjoint
- pl: 99.3% disjoint
- pt: 97.3% disjoint
- ro: 99.5% disjoint
- ru: 97.6% disjoint
- sk: 97.8% disjoint
- sl: 98.9% disjoint
- uk: 98.0% disjoint
- zh: 94.7% disjoint

## Final Counts per Cluster x Split x Class
| Cluster | Split | Max/Min Ratio | Counts |
|---|---|---|---|
| cyrillic | train | 1.03 | v5-Eagle-7B-HF: 2717, aya-101: 2716, Mistral-7B-Instruct-v0.2: 2703, human: 2696, gpt-3.5-turbo-0125: 2695, vicuna-13b: 2695, opt-iml-max-30b: 2667, Llama-2-70b-chat-hf: 2642 |
| cyrillic | val | 1.16 | gpt-3.5-turbo-0125: 304, human: 300, vicuna-13b: 297, Mistral-7B-Instruct-v0.2: 296, opt-iml-max-30b: 291, aya-101: 284, v5-Eagle-7B-HF: 274, Llama-2-70b-chat-hf: 261 |
| cyrillic | test | 1.03 | aya-101: 900, gpt-3.5-turbo-0125: 900, Mistral-7B-Instruct-v0.2: 899, vicuna-13b: 899, human: 898, v5-Eagle-7B-HF: 896, opt-iml-max-30b: 890, Llama-2-70b-chat-hf: 871 |
| latin | train | 1.04 | Mistral-7B-Instruct-v0.2: 10911, gpt-3.5-turbo-0125: 10889, aya-101: 10882, v5-Eagle-7B-HF: 10820, human: 10798, vicuna-13b: 10714, opt-iml-max-30b: 10698, Llama-2-70b-chat-hf: 10503 |
| latin | val | 1.19 | vicuna-13b: 1270, human: 1200, Llama-2-70b-chat-hf: 1163, v5-Eagle-7B-HF: 1161, aya-101: 1112, gpt-3.5-turbo-0125: 1109, Mistral-7B-Instruct-v0.2: 1082, opt-iml-max-30b: 1071 |
| latin | test | 1.03 | gpt-3.5-turbo-0125: 3600, Mistral-7B-Instruct-v0.2: 3600, human: 3599, aya-101: 3598, v5-Eagle-7B-HF: 3592, vicuna-13b: 3591, opt-iml-max-30b: 3550, Llama-2-70b-chat-hf: 3501 |
| greek | train | 1.06 | human: 899, aya-101: 861, Mistral-7B-Instruct-v0.2: 860, vicuna-13b: 856, opt-iml-max-30b: 854, v5-Eagle-7B-HF: 854, Llama-2-70b-chat-hf: 850, gpt-3.5-turbo-0125: 846 |
| greek | val | 1.55 | gpt-3.5-turbo-0125: 153, v5-Eagle-7B-HF: 143, aya-101: 139, Mistral-7B-Instruct-v0.2: 138, vicuna-13b: 137, opt-iml-max-30b: 130, Llama-2-70b-chat-hf: 124, human: 99 |
| greek | test | 1.02 | aya-101: 300, human: 300, gpt-3.5-turbo-0125: 300, v5-Eagle-7B-HF: 299, Mistral-7B-Instruct-v0.2: 299, Llama-2-70b-chat-hf: 296, vicuna-13b: 295, opt-iml-max-30b: 295 |
| hanzi | train | 1.03 | opt-iml-max-30b: 916, aya-101: 915, vicuna-13b: 914, Mistral-7B-Instruct-v0.2: 913, human: 900, gpt-3.5-turbo-0125: 899, v5-Eagle-7B-HF: 899, Llama-2-70b-chat-hf: 888 |
| hanzi | val | 1.35 | human: 100, v5-Eagle-7B-HF: 98, gpt-3.5-turbo-0125: 88, Mistral-7B-Instruct-v0.2: 86, aya-101: 85, opt-iml-max-30b: 76, vicuna-13b: 75, Llama-2-70b-chat-hf: 74 |
| hanzi | test | 1.02 | human: 300, Mistral-7B-Instruct-v0.2: 300, aya-101: 300, v5-Eagle-7B-HF: 299, opt-iml-max-30b: 297, Llama-2-70b-chat-hf: 296, vicuna-13b: 296, gpt-3.5-turbo-0125: 295 |
| arabic | train | 1.06 | Mistral-7B-Instruct-v0.2: 946, v5-Eagle-7B-HF: 930, vicuna-13b: 930, aya-101: 929, gpt-3.5-turbo-0125: 921, opt-iml-max-30b: 916, human: 902, Llama-2-70b-chat-hf: 893 |
| arabic | val | 1.85 | human: 98, Llama-2-70b-chat-hf: 94, gpt-3.5-turbo-0125: 79, opt-iml-max-30b: 76, aya-101: 71, v5-Eagle-7B-HF: 69, vicuna-13b: 68, Mistral-7B-Instruct-v0.2: 53 |
| arabic | test | 1.02 | Mistral-7B-Instruct-v0.2: 300, aya-101: 300, human: 300, gpt-3.5-turbo-0125: 300, v5-Eagle-7B-HF: 300, vicuna-13b: 299, opt-iml-max-30b: 298, Llama-2-70b-chat-hf: 295 |

## Shortcut Baselines

Macro-F1 (chance ~ 0.125) on val and test sets using simple shortcut features.

| Cluster | Model | Val F1 | Test F1 | Test F1 (Clean Subset) |
|---|---|---|---|---|
| cyrillic | (a) Length Features | 0.301 | 0.292 | 0.290 |
| cyrillic | (b) First 3 Words TF-IDF | 0.307 | 0.308 | 0.303 |
| cyrillic | (c) Flags Only | 0.051 | 0.059 | 0.029 |
| cyrillic | (d) All Combined | 0.344 | 0.337 | 0.317 |
| latin | (a) Length Features | 0.240 | 0.231 | 0.231 |
| latin | (b) First 3 Words TF-IDF | 0.308 | 0.302 | 0.294 |
| latin | (c) Flags Only | 0.047 | 0.050 | 0.028 |
| latin | (d) All Combined | 0.281 | 0.274 | 0.266 |
| greek | (a) Length Features | 0.345 | 0.324 | 0.317 |
| greek | (b) First 3 Words TF-IDF | 0.361 | 0.373 | 0.364 |
| greek | (c) Flags Only | 0.033 | 0.070 | 0.029 |
| greek | (d) All Combined | 0.453 | 0.457 | 0.431 |
| hanzi | (a) Length Features | 0.153 | 0.166 | 0.156 |
| hanzi | (b) First 3 Words TF-IDF | 0.384 | 0.386 | 0.331 |
| hanzi | (c) Flags Only | 0.131 | 0.128 | 0.031 |
| hanzi | (d) All Combined | 0.327 | 0.320 | 0.268 |
| arabic | (a) Length Features | 0.331 | 0.321 | 0.320 |
| arabic | (b) First 3 Words TF-IDF | 0.458 | 0.425 | 0.424 |
| arabic | (c) Flags Only | 0.040 | 0.051 | 0.029 |
| arabic | (d) All Combined | 0.415 | 0.433 | 0.431 |

## Regeneration Commands
To regenerate these splits and evaluate the baselines:

```bash
# 1. Rebuild the dataset splits and initial story groups
python scripts/build_splits.py

# 2. Add script-aware junk flags and story-disjoint similarity flags
python scripts/add_flags_and_similarity.py

# 3. Verify leakage assumptions and run cross-split similarity
python scripts/check_leakage.py
python scripts/cross_split_similarity.py

# 4. Generate story group statistics
python scripts/report_stats.py

# 5. Run shortcut baselines
python scripts/shortcut_baselines.py
```
