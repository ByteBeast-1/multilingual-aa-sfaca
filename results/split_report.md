# Split Design Report

- **Raw CSV SHA-256**: 1e08f9c6980ed9cae11bc831d8ce54d13125ea9a52dfef387b0b4ebd0909647c
- **Splits CSV SHA-256**: 64ee154bb1ca8c3f4fa3aa473c6b05da686d882014244b60dbf2bd2cb4257318

## Story Grouping Diagnostics
- **Total groups**: 17992
- **Singleton rate**: 14.73% (2651 / 17992)
- **Groups with exactly 1 human**: 17992 (117.28% of non-singletons)

## Group Size Histogram
- Size 1: 2651 groups
- Size 2: 1767 groups
- Size 3: 1568 groups
- Size 4: 1423 groups
- Size 5: 1501 groups
- Size 6: 1486 groups
- Size 7: 1494 groups
- Size 8: 1248 groups
- Size 9: 900 groups
- Size 10: 613 groups
- Size 15: 211 groups
- Size 20: 94 groups
- Size 25: 35 groups
- Size 30: 42 groups
- Size 35: 16 groups
- Size 40: 10 groups
- Size 45: 12 groups
- Size 50: 7 groups
- Size 55: 9 groups
- Size 60: 4 groups
- Size 65: 3 groups
- Size 70: 3 groups
- Size 75: 5 groups
- Size 85: 1 groups
- Size 100: 2 groups
- Size 105: 1 groups
- Size 115: 1 groups
- Size 170: 1 groups
- Size 180: 1 groups
- Size 195: 1 groups
- Size 235: 1 groups

## Flag Distributions
| Cluster | Split | Generator | Junk | Script Mismatch | Prompt Echo |
|---|---|---|---|---|---|
| cyrillic | train | opt-iml-max-30b | 1 | 30 | 23 |
| cyrillic | train | Mistral-7B-Instruct-v0.2 | 0 | 42 | 0 |
| cyrillic | train | human | 2 | 4 | 0 |
| cyrillic | train | v5-Eagle-7B-HF | 0 | 156 | 17 |
| cyrillic | train | vicuna-13b | 0 | 376 | 39 |
| cyrillic | train | Llama-2-70b-chat-hf | 0 | 319 | 104 |
| cyrillic | val | v5-Eagle-7B-HF | 0 | 6 | 1 |
| cyrillic | val | Llama-2-70b-chat-hf | 0 | 28 | 5 |
| cyrillic | val | Mistral-7B-Instruct-v0.2 | 0 | 2 | 0 |
| cyrillic | val | vicuna-13b | 0 | 25 | 3 |
| cyrillic | val | opt-iml-max-30b | 1 | 0 | 1 |
| cyrillic | test | Mistral-7B-Instruct-v0.2 | 0 | 20 | 0 |
| cyrillic | test | v5-Eagle-7B-HF | 0 | 45 | 3 |
| cyrillic | test | vicuna-13b | 0 | 124 | 14 |
| cyrillic | test | human | 0 | 3 | 0 |
| cyrillic | test | opt-iml-max-30b | 1 | 5 | 3 |
| cyrillic | test | Llama-2-70b-chat-hf | 0 | 92 | 24 |
| latin | train | Llama-2-70b-chat-hf | 0 | 2 | 972 |
| latin | train | human | 14 | 0 | 0 |
| latin | train | vicuna-13b | 1 | 5 | 74 |
| latin | train | opt-iml-max-30b | 19 | 18 | 83 |
| latin | train | v5-Eagle-7B-HF | 1 | 10 | 159 |
| latin | val | vicuna-13b | 0 | 1 | 6 |
| latin | val | human | 4 | 0 | 0 |
| latin | val | v5-Eagle-7B-HF | 0 | 0 | 14 |
| latin | val | opt-iml-max-30b | 2 | 0 | 17 |
| latin | val | Llama-2-70b-chat-hf | 0 | 0 | 101 |
| latin | test | human | 5 | 0 | 0 |
| latin | test | v5-Eagle-7B-HF | 0 | 2 | 40 |
| latin | test | gpt-3.5-turbo-0125 | 0 | 0 | 1 |
| latin | test | vicuna-13b | 0 | 0 | 18 |
| latin | test | opt-iml-max-30b | 25 | 23 | 27 |
| latin | test | Llama-2-70b-chat-hf | 0 | 0 | 305 |
| latin | test | aya-101 | 0 | 0 | 1 |
| latin | test | Mistral-7B-Instruct-v0.2 | 1 | 0 | 1 |
| greek | train | Mistral-7B-Instruct-v0.2 | 0 | 41 | 0 |
| greek | train | aya-101 | 0 | 1 | 0 |
| greek | train | opt-iml-max-30b | 1 | 7 | 4 |
| greek | train | human | 0 | 4 | 0 |
| greek | train | Llama-2-70b-chat-hf | 0 | 52 | 23 |
| greek | train | v5-Eagle-7B-HF | 0 | 29 | 4 |
| greek | train | vicuna-13b | 0 | 185 | 15 |
| greek | val | v5-Eagle-7B-HF | 0 | 1 | 0 |
| greek | val | vicuna-13b | 0 | 1 | 0 |
| greek | val | human | 0 | 1 | 0 |
| greek | test | v5-Eagle-7B-HF | 0 | 8 | 2 |
| greek | test | Llama-2-70b-chat-hf | 0 | 15 | 5 |
| greek | test | vicuna-13b | 0 | 64 | 7 |
| greek | test | human | 0 | 1 | 0 |
| greek | test | Mistral-7B-Instruct-v0.2 | 0 | 15 | 0 |
| greek | test | opt-iml-max-30b | 0 | 2 | 1 |
| hanzi | train | gpt-3.5-turbo-0125 | 38 | 1 | 0 |
| hanzi | train | aya-101 | 41 | 2 | 0 |
| hanzi | train | Llama-2-70b-chat-hf | 25 | 177 | 11 |
| hanzi | train | human | 426 | 50 | 0 |
| hanzi | train | vicuna-13b | 51 | 80 | 7 |
| hanzi | train | Mistral-7B-Instruct-v0.2 | 36 | 152 | 0 |
| hanzi | train | v5-Eagle-7B-HF | 38 | 26 | 1 |
| hanzi | train | opt-iml-max-30b | 49 | 18 | 2 |
| hanzi | val | human | 49 | 3 | 0 |
| hanzi | val | opt-iml-max-30b | 2 | 0 | 0 |
| hanzi | val | Mistral-7B-Instruct-v0.2 | 8 | 7 | 0 |
| hanzi | val | aya-101 | 2 | 0 | 0 |
| hanzi | val | v5-Eagle-7B-HF | 3 | 1 | 0 |
| hanzi | val | gpt-3.5-turbo-0125 | 1 | 0 | 0 |
| hanzi | val | Llama-2-70b-chat-hf | 3 | 11 | 1 |
| hanzi | val | vicuna-13b | 4 | 4 | 0 |
| hanzi | test | opt-iml-max-30b | 12 | 5 | 1 |
| hanzi | test | Llama-2-70b-chat-hf | 9 | 49 | 4 |
| hanzi | test | human | 144 | 23 | 0 |
| hanzi | test | Mistral-7B-Instruct-v0.2 | 11 | 44 | 0 |
| hanzi | test | vicuna-13b | 16 | 28 | 3 |
| hanzi | test | v5-Eagle-7B-HF | 10 | 12 | 2 |
| hanzi | test | aya-101 | 5 | 2 | 0 |
| hanzi | test | gpt-3.5-turbo-0125 | 6 | 0 | 0 |
| arabic | train | Mistral-7B-Instruct-v0.2 | 0 | 108 | 1 |
| arabic | train | v5-Eagle-7B-HF | 0 | 33 | 3 |
| arabic | train | Llama-2-70b-chat-hf | 1 | 91 | 26 |
| arabic | train | human | 4 | 0 | 0 |
| arabic | train | opt-iml-max-30b | 1 | 2 | 15 |
| arabic | train | vicuna-13b | 1 | 75 | 5 |
| arabic | val | Mistral-7B-Instruct-v0.2 | 0 | 1 | 0 |
| arabic | val | opt-iml-max-30b | 0 | 1 | 3 |
| arabic | val | v5-Eagle-7B-HF | 0 | 0 | 1 |
| arabic | val | vicuna-13b | 0 | 1 | 0 |
| arabic | val | human | 1 | 0 | 0 |
| arabic | val | Llama-2-70b-chat-hf | 0 | 1 | 1 |
| arabic | test | Llama-2-70b-chat-hf | 0 | 30 | 5 |
| arabic | test | Mistral-7B-Instruct-v0.2 | 0 | 26 | 1 |
| arabic | test | vicuna-13b | 0 | 29 | 5 |
| arabic | test | opt-iml-max-30b | 0 | 0 | 2 |
| arabic | test | v5-Eagle-7B-HF | 0 | 9 | 1 |

## Class Balance (Counts & Min/Max Ratio)
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

### Prompt patterns flagged
`(?i)\b(task write|task translate|leave out the|return just the|you are a|your article in|a news article in|the article in|text of the|here is a|title:)\b`