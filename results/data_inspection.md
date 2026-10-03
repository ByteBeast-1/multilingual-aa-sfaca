# Data Inspection Report

## 1. Dataset Overview

- **Row count**: 206330
- **Columns**: ['Unnamed: 0', 'text', 'label', 'multi_label', 'split', 'language', 'length', 'source']
- **Dtypes**:
  - Unnamed: 0: int64
  - text: object
  - label: int64
  - multi_label: object
  - split: object
  - language: object
  - length: int64
  - source: object

### Counts
**Per Split:**
- train: 156240
- test: 50090
**Per Cluster:**
- latin: 144335
- cyrillic: 30991
- arabic: 10367
- greek: 10328
- hanzi: 10309
**Per Language:**
- ar: 10367
- cs: 10351
- hu: 10349
- nl: 10344
- pt: 10344
- bg: 10340
- de: 10339
- en: 10338
- hr: 10335
- ro: 10335
- es: 10334
- sl: 10333
- sk: 10331
- pl: 10329
- el: 10328
- ru: 10327
- uk: 10324
- zh: 10309
- gd: 10276
- ca: 5283
- ga: 4714
**Per Label (multi_label):**
- aya-101: 25948
- human: 25945
- Mistral-7B-Instruct-v0.2: 25937
- gpt-3.5-turbo-0125: 25935
- v5-Eagle-7B-HF: 25892
- vicuna-13b: 25876
- opt-iml-max-30b: 25568
- Llama-2-70b-chat-hf: 25229

**Cross-tab of cluster x label x split:**

| Cluster | Label | Split | Count |
|---|---|---|---|
| arabic | Llama-2-70b-chat-hf | test | 295 |
| arabic | Llama-2-70b-chat-hf | train | 987 |
| arabic | Mistral-7B-Instruct-v0.2 | test | 300 |
| arabic | Mistral-7B-Instruct-v0.2 | train | 999 |
| arabic | aya-101 | test | 300 |
| arabic | aya-101 | train | 1000 |
| arabic | gpt-3.5-turbo-0125 | test | 300 |
| arabic | gpt-3.5-turbo-0125 | train | 1000 |
| arabic | human | test | 300 |
| arabic | human | train | 1000 |
| arabic | opt-iml-max-30b | test | 298 |
| arabic | opt-iml-max-30b | train | 992 |
| arabic | v5-Eagle-7B-HF | test | 300 |
| arabic | v5-Eagle-7B-HF | train | 999 |
| arabic | vicuna-13b | test | 299 |
| arabic | vicuna-13b | train | 998 |
| cyrillic | Llama-2-70b-chat-hf | test | 871 |
| cyrillic | Llama-2-70b-chat-hf | train | 2903 |
| cyrillic | Mistral-7B-Instruct-v0.2 | test | 899 |
| cyrillic | Mistral-7B-Instruct-v0.2 | train | 2999 |
| cyrillic | aya-101 | test | 900 |
| cyrillic | aya-101 | train | 3000 |
| cyrillic | gpt-3.5-turbo-0125 | test | 900 |
| cyrillic | gpt-3.5-turbo-0125 | train | 2999 |
| cyrillic | human | test | 898 |
| cyrillic | human | train | 2996 |
| cyrillic | opt-iml-max-30b | test | 890 |
| cyrillic | opt-iml-max-30b | train | 2958 |
| cyrillic | v5-Eagle-7B-HF | test | 896 |
| cyrillic | v5-Eagle-7B-HF | train | 2991 |
| cyrillic | vicuna-13b | test | 899 |
| cyrillic | vicuna-13b | train | 2992 |
| greek | Llama-2-70b-chat-hf | test | 296 |
| greek | Llama-2-70b-chat-hf | train | 974 |
| greek | Mistral-7B-Instruct-v0.2 | test | 299 |
| greek | Mistral-7B-Instruct-v0.2 | train | 998 |
| greek | aya-101 | test | 300 |
| greek | aya-101 | train | 1000 |
| greek | gpt-3.5-turbo-0125 | test | 300 |
| greek | gpt-3.5-turbo-0125 | train | 999 |
| greek | human | test | 300 |
| greek | human | train | 998 |
| greek | opt-iml-max-30b | test | 295 |
| greek | opt-iml-max-30b | train | 985 |
| greek | v5-Eagle-7B-HF | test | 299 |
| greek | v5-Eagle-7B-HF | train | 997 |
| greek | vicuna-13b | test | 295 |
| greek | vicuna-13b | train | 993 |
| hanzi | Llama-2-70b-chat-hf | test | 296 |
| hanzi | Llama-2-70b-chat-hf | train | 962 |
| hanzi | Mistral-7B-Instruct-v0.2 | test | 300 |
| hanzi | Mistral-7B-Instruct-v0.2 | train | 999 |
| hanzi | aya-101 | test | 300 |
| hanzi | aya-101 | train | 1000 |
| hanzi | gpt-3.5-turbo-0125 | test | 295 |
| hanzi | gpt-3.5-turbo-0125 | train | 987 |
| hanzi | human | test | 300 |
| hanzi | human | train | 1000 |
| hanzi | opt-iml-max-30b | test | 297 |
| hanzi | opt-iml-max-30b | train | 992 |
| hanzi | v5-Eagle-7B-HF | test | 299 |
| hanzi | v5-Eagle-7B-HF | train | 997 |
| hanzi | vicuna-13b | test | 296 |
| hanzi | vicuna-13b | train | 989 |
| latin | Llama-2-70b-chat-hf | test | 4374 |
| latin | Llama-2-70b-chat-hf | train | 13271 |
| latin | Mistral-7B-Instruct-v0.2 | test | 4500 |
| latin | Mistral-7B-Instruct-v0.2 | train | 13644 |
| latin | aya-101 | test | 4498 |
| latin | aya-101 | train | 13650 |
| latin | gpt-3.5-turbo-0125 | test | 4500 |
| latin | gpt-3.5-turbo-0125 | train | 13655 |
| latin | human | test | 4499 |
| latin | human | train | 13654 |
| latin | opt-iml-max-30b | test | 4430 |
| latin | opt-iml-max-30b | train | 13431 |
| latin | v5-Eagle-7B-HF | test | 4488 |
| latin | v5-Eagle-7B-HF | train | 13626 |
| latin | vicuna-13b | test | 4489 |
| latin | vicuna-13b | train | 13626 |


## 2. Text Length Statistics

| Cluster | Mean Chars | Mean Tokens | % > 128 tokens |
|---|---|---|---|
| cyrillic | 744.4 | 182.1 | 69.9% |
| latin | 937.5 | 231.1 | 81.1% |
| hanzi | 165.2 | 92.1 | 26.4% |
| greek | 490.1 | 134.1 | 44.0% |
| arabic | 509.0 | 140.5 | 53.2% |

## 3. Source Column Analysis

**Unique values and counts:**
- MULTITuDE_MassiveSumm_dw: 20306
- MULTITuDE_MassiveSumm_dnevnik: 15002
- MULTITuDE_MassiveSumm_globalvoices: 14335
- MULTITuDE_MassiveSumm_bbc: 13942
- MULTITuDE_MassiveSumm_voanews: 12181
- MULTITuDE_MassiveSumm_rfi: 9300
- MULTITuDE_MassiveSumm_denik: 9051
- MULTITuDE_MassiveSumm_sme: 9031
- MULTITuDE_MassiveSumm_dziennik: 6079
- MULTITuDE_MassiveSumm_24: 4827
- MULTITuDE_MassiveSumm_welt: 4554
- MULTITuDE_MassiveSumm_20minutos: 4327
- MULTITuDE_MassiveSumm_index: 4222
- MULTITuDE_MassiveSumm_rt: 4161
- MULTITuDE_MassiveSumm_rte: 4121
- MULTITuDE_MassiveSumm_eleftherostypos: 3629
- MassiveSumm_dw: 2921
- MULTITuDE_MassiveSumm_rp: 2853
- MULTITuDE_MassiveSumm_unian: 2761
- MULTITuDE_MassiveSumm_voaportugues: 2559
- MULTITuDE_MassiveSumm_gazeta: 2452
- MULTITuDE_MassiveSumm_ria: 2423
- MassiveSumm_dnevnik: 2157
- MULTITuDE_MassiveSumm_eremnews: 2129
- MassiveSumm_globalvoices: 2059
- MassiveSumm_bbc: 2013
- MassiveSumm_voanews: 1752
- MULTITuDE_MassiveSumm_delo: 1717
- MULTITuDE_MassiveSumm_acorianooriental: 1610
- MULTITuDE_MassiveSumm_kathimerini: 1516
- MULTITuDE_MassiveSumm_spiegel: 1454
- MassiveSumm_rfi: 1343
- MassiveSumm_sme: 1300
- MassiveSumm_denik: 1300
- MULTITuDE_MassiveSumm_tass: 1248
- MULTITuDE_MassiveSumm_dnes: 1236
- MULTITuDE_MassiveSumm_alwafd: 1230
- MULTITuDE_MassiveSumm_aljazeera: 1218
- MULTITuDE_MassiveSumm_mk: 1188
- MULTITuDE_MassiveSumm_elpais: 1157
- MULTITuDE_MassiveSumm_meinbezirk: 1156
- MULTITuDE_MassiveSumm_vesti: 1089
- MULTITuDE_MassiveSumm_aawsat: 1048
- MULTITuDE_MassiveSumm_voachinese: 956
- MULTITuDE_MassiveSumm_interfax: 925
- MULTITuDE_MassiveSumm_tanea: 887
- MassiveSumm_dziennik: 877
- MULTITuDE_MassiveSumm_rbc: 873
- MULTITuDE_MassiveSumm_publico: 859
- MULTITuDE_MassiveSumm_pravda: 846
- MULTITuDE_MassiveSumm_n-tv: 839
- MULTITuDE_MassiveSumm_faz: 750
- MassiveSumm_24: 693
- MassiveSumm_welt: 656
- MassiveSumm_20minutos: 623
- MassiveSumm_index: 607
- MULTITuDE_MassiveSumm_rtve: 600
- MassiveSumm_rt: 597
- MassiveSumm_rte: 593
- MULTITuDE_MassiveSumm_kyiv: 591
- MassiveSumm_eleftherostypos: 522
- MULTITuDE_MassiveSumm_ren: 450
- MassiveSumm_rp: 409
- MassiveSumm_unian: 395
- MassiveSumm_voaportugues: 367
- MassiveSumm_gazeta: 351
- MassiveSumm_ria: 349
- MassiveSumm_eremnews: 306
- MULTITuDE_MassiveSumm_tovima: 299
- MassiveSumm_delo: 247
- MassiveSumm_acorianooriental: 231
- MassiveSumm_kathimerini: 218
- MassiveSumm_spiegel: 209
- MassiveSumm_tass: 179
- MassiveSumm_dnes: 178
- MassiveSumm_alwafd: 176
- MassiveSumm_aljazeera: 175
- MassiveSumm_mk: 171
- MULTITuDE_MassiveSumm_golosameriki: 167
- MassiveSumm_meinbezirk: 166
- MassiveSumm_elpais: 166
- MassiveSumm_vesti: 157
- MassiveSumm_aawsat: 150
- MULTITuDE_MassiveSumm_golem: 140
- MassiveSumm_voachinese: 137
- MassiveSumm_interfax: 133
- MassiveSumm_tanea: 127
- MassiveSumm_rbc: 126
- MassiveSumm_publico: 123
- MassiveSumm_pravda: 122
- MassiveSumm_n-tv: 120
- MassiveSumm_faz: 108
- MassiveSumm_rtve: 87
- MassiveSumm_kyiv: 85
- MassiveSumm_ren: 65
- MULTITuDE_MassiveSumm_mos: 49
- MassiveSumm_tovima: 42
- MassiveSumm_golosameriki: 24
- MassiveSumm_golem: 20
- MULTITuDE_MassiveSumm_amerikaninsesi: 14
- MULTITuDE_MassiveSumm_prin: 7
- MULTITuDE_MassiveSumm_avgi: 7
- MassiveSumm_mos: 7
- MULTITuDE_MassiveSumm_voacantonese: 7
- MULTITuDE_MassiveSumm_stoxos: 7
- MassiveSumm_amerikaninsesi: 2
- MassiveSumm_stoxos: 1
- MassiveSumm_voacantonese: 1
- MassiveSumm_prin: 1
- MassiveSumm_avgi: 1

**Is there ANY column that identifies the original article or headline?**
**NO.** There is no explicit identifier column.

## 4. Duplicate Analysis

- Exact duplicate rows: 0
- Near-duplicate rows (normalized): 74
- Test texts that also occur in train (leakage): 17 rows (2 unique hashes)

## 5. Gemini/Claude Rows

No Gemini/Claude rows found in label or source. Verified clean.

## 6. Class Balance and KAGGLE_RUN_FACTS Comparison

| Cluster | Split | Found | Kaggle Fact | Mismatch |
|---|---|---|---|---|
| latin | train | 108557 | 95431 | 13126 |
| latin | test | 35778 | 28631 | 7147 |
| cyrillic | train | 23838 | 23838 | Match |
| cyrillic | test | 7153 | 7153 | Match |
| greek | train | 7944 | 7944 | Match |
| greek | test | 2384 | 2384 | Match |
| arabic | train | 7975 | 7975 | Match |
| arabic | test | 2392 | 2392 | Match |
| hanzi | train | 7926 | 7926 | Match |
| hanzi | test | 2383 | 2383 | Match |

## 7. `src/data_loader.py` Filters

Looking at `src/data_loader.py`, the following filters apply when `load_multitude_csv(path, restrict_to_base_paper_18=True)` is called:
1. **Language Filter**: Drops 3 languages (`ca`, `ga`, `gd`) because they are not part of the base paper's 18 core languages.
2. **Label Verification**: Maps `multi_label` using `LABEL2ID`. Any row with an unrecognized `multi_label` raises a `ValueError` rather than silently dropping or mislabeling it.

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
