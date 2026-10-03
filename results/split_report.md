# Split Design Report

- **Raw CSV SHA-256**: 1e08f9c6980ed9cae11bc831d8ce54d13125ea9a52dfef387b0b4ebd0909647c
- **Splits CSV SHA-256**: 59f3e7c0a8027bc6447bbfbe358561c0e12dc4b9a6f794017dccdc224a562598
- **Grouping strategy**: one-to-one per (language, outlet, generator) via `linear_sum_assignment`

## Story Grouping Diagnostics
- **Total groups**: 17992
- **Singletons**: 0 (0.00%)
- **Groups with exactly 1 human**: 17992
- **Groups > 8 rows**: 30
- **Group sizes** — min: 2, median: 8.0, p90: 8.0, max: 11

### Val rows in groups > 8, per cluster
- arabic: 0/797 val rows in groups > 8 (0.0% )
- cyrillic: 0/2380 val rows in groups > 8 (0.0% )
- greek: 0/784 val rows in groups > 8 (0.0% )
- hanzi: 0/800 val rows in groups > 8 (0.0% )
- latin: 0/9544 val rows in groups > 8 (0.0% )

### Leftover machine texts (|machine|>|human| in a bucket)
| language | outlet | generator | n_leftover |
|----------|--------|-----------|------------|
| uk | MassiveSumm_unian | gpt-3.5-turbo-0125 | 3 |
| uk | MassiveSumm_unian | Mistral-7B-Instruct-v0.2 | 3 |
| uk | MassiveSumm_unian | aya-101 | 3 |
| uk | MassiveSumm_unian | v5-Eagle-7B-HF | 3 |
| uk | MassiveSumm_unian | vicuna-13b | 2 |
| el | MassiveSumm_tanea | aya-101 | 1 |
| el | MassiveSumm_tanea | gpt-3.5-turbo-0125 | 1 |
| el | MassiveSumm_tovima | vicuna-13b | 1 |
| el | MassiveSumm_tovima | gpt-3.5-turbo-0125 | 1 |
| el | MassiveSumm_tovima | aya-101 | 1 |
| el | MassiveSumm_tovima | Mistral-7B-Instruct-v0.2 | 1 |
| el | MassiveSumm_tovima | v5-Eagle-7B-HF | 1 |
| el | MassiveSumm_tovima | opt-iml-max-30b | 1 |
| nl | MassiveSumm_globalvoices | Mistral-7B-Instruct-v0.2 | 1 |
| nl | MassiveSumm_globalvoices | aya-101 | 1 |
| nl | MassiveSumm_globalvoices | gpt-3.5-turbo-0125 | 1 |
| pt | MassiveSumm_voaportugues | vicuna-13b | 1 |
| pt | MassiveSumm_voaportugues | gpt-3.5-turbo-0125 | 1 |
| pt | MassiveSumm_voaportugues | Mistral-7B-Instruct-v0.2 | 1 |
| pt | MassiveSumm_voaportugues | v5-Eagle-7B-HF | 1 |
| uk | MassiveSumm_gazeta | gpt-3.5-turbo-0125 | 1 |
| uk | MassiveSumm_gazeta | Mistral-7B-Instruct-v0.2 | 1 |
| uk | MassiveSumm_gazeta | aya-101 | 1 |

## Group Size Histogram
- Size 2: 1 groups
- Size 3: 2 groups
- Size 4: 10 groups
- Size 5: 14 groups
- Size 6: 118 groups
- Size 7: 569 groups
- Size 8: 17248 groups
- Size 9: 29 groups
- Size 11: 1 groups

## Class Balance (Counts & Min/Max Ratio)
| Cluster | Split | Max/Min Ratio | Counts |
|---------|-------|---------------|--------|
| arabic | train | 1.01 | gpt-3.5-turbo-0125: 900, human: 900, aya-101: 900, Mistral-7B-Instruct-v0.2: 899, v5-Eagle-7B-HF: 899, vicuna-13b: 898, opt-iml-max-30b: 894, Llama-2-70b-chat-hf: 888 |
| arabic | val | 1.02 | aya-101: 100, v5-Eagle-7B-HF: 100, gpt-3.5-turbo-0125: 100, Mistral-7B-Instruct-v0.2: 100, vicuna-13b: 100, human: 100, Llama-2-70b-chat-hf: 99, opt-iml-max-30b: 98 |
| arabic | test | 1.02 | Mistral-7B-Instruct-v0.2: 300, aya-101: 300, human: 300, gpt-3.5-turbo-0125: 300, v5-Eagle-7B-HF: 300, vicuna-13b: 299, opt-iml-max-30b: 298, Llama-2-70b-chat-hf: 295 |
| cyrillic | train | 1.03 | aya-101: 2700, Mistral-7B-Instruct-v0.2: 2699, gpt-3.5-turbo-0125: 2699, human: 2696, vicuna-13b: 2693, v5-Eagle-7B-HF: 2692, opt-iml-max-30b: 2664, Llama-2-70b-chat-hf: 2615 |
| cyrillic | val | 1.04 | Mistral-7B-Instruct-v0.2: 300, gpt-3.5-turbo-0125: 300, human: 300, aya-101: 300, vicuna-13b: 299, v5-Eagle-7B-HF: 299, opt-iml-max-30b: 294, Llama-2-70b-chat-hf: 288 |
| cyrillic | test | 1.03 | aya-101: 900, gpt-3.5-turbo-0125: 900, Mistral-7B-Instruct-v0.2: 899, vicuna-13b: 899, human: 898, v5-Eagle-7B-HF: 896, opt-iml-max-30b: 890, Llama-2-70b-chat-hf: 871 |
| greek | train | 1.03 | aya-101: 901, gpt-3.5-turbo-0125: 900, Mistral-7B-Instruct-v0.2: 899, human: 899, v5-Eagle-7B-HF: 899, vicuna-13b: 895, opt-iml-max-30b: 888, Llama-2-70b-chat-hf: 878 |
| greek | val | 1.03 | human: 99, aya-101: 99, gpt-3.5-turbo-0125: 99, Mistral-7B-Instruct-v0.2: 99, v5-Eagle-7B-HF: 98, vicuna-13b: 98, Llama-2-70b-chat-hf: 96, opt-iml-max-30b: 96 |
| greek | test | 1.02 | aya-101: 300, human: 300, gpt-3.5-turbo-0125: 300, v5-Eagle-7B-HF: 299, Mistral-7B-Instruct-v0.2: 299, Llama-2-70b-chat-hf: 296, vicuna-13b: 295, opt-iml-max-30b: 295 |
| hanzi | train | 1.04 | human: 899, aya-101: 899, Mistral-7B-Instruct-v0.2: 898, v5-Eagle-7B-HF: 896, opt-iml-max-30b: 892, vicuna-13b: 889, gpt-3.5-turbo-0125: 888, Llama-2-70b-chat-hf: 865 |
| hanzi | val | 1.04 | Mistral-7B-Instruct-v0.2: 101, aya-101: 101, human: 101, v5-Eagle-7B-HF: 101, vicuna-13b: 100, opt-iml-max-30b: 100, gpt-3.5-turbo-0125: 99, Llama-2-70b-chat-hf: 97 |
| hanzi | test | 1.02 | human: 300, Mistral-7B-Instruct-v0.2: 300, aya-101: 300, v5-Eagle-7B-HF: 299, opt-iml-max-30b: 297, Llama-2-70b-chat-hf: 296, vicuna-13b: 296, gpt-3.5-turbo-0125: 295 |
| latin | train | 1.03 | gpt-3.5-turbo-0125: 10799, human: 10798, Mistral-7B-Instruct-v0.2: 10795, aya-101: 10794, vicuna-13b: 10784, v5-Eagle-7B-HF: 10784, opt-iml-max-30b: 10585, Llama-2-70b-chat-hf: 10500 |
| latin | val | 1.03 | human: 1200, aya-101: 1200, vicuna-13b: 1200, gpt-3.5-turbo-0125: 1199, Mistral-7B-Instruct-v0.2: 1198, v5-Eagle-7B-HF: 1197, opt-iml-max-30b: 1184, Llama-2-70b-chat-hf: 1166 |
| latin | test | 1.03 | gpt-3.5-turbo-0125: 3600, Mistral-7B-Instruct-v0.2: 3600, human: 3599, aya-101: 3598, v5-Eagle-7B-HF: 3592, vicuna-13b: 3591, opt-iml-max-30b: 3550, Llama-2-70b-chat-hf: 3501 |

### Prompt patterns flagged
`(?i)\b(task write|task translate|leave out the|return just the|you are a|your article in|a news article in|the article in|text of the|here is a|title:)\b`