# Data Card Metrics

## Groups (Train + Val)
- Test rows have group_id -1 and are not counted here.
- Number of human anchors: 17992
- Humans with no attached machine text: 0 (0.0%)
- Group sizes: min=2, median=8.0, p90=8.0, max=11

### Top 10 Largest Groups
- Group 4692: size 11, lang el, outlet MULTITuDE_MassiveSumm_tovima, splits {'train': 11}
- Group 4583: size 9, lang el, outlet MULTITuDE_MassiveSumm_tanea, splits {'train': 9}
- Group 4621: size 9, lang el, outlet MULTITuDE_MassiveSumm_tanea, splits {'train': 9}
- Group 4670: size 9, lang el, outlet MassiveSumm_tovima, splits {'train': 9}
- Group 4685: size 9, lang el, outlet MULTITuDE_MassiveSumm_tovima, splits {'train': 9}
- Group 4687: size 9, lang el, outlet MULTITuDE_MassiveSumm_tovima, splits {'train': 9}
- Group 9204: size 9, lang nl, outlet MULTITuDE_MassiveSumm_globalvoices, splits {'train': 9}
- Group 9526: size 9, lang nl, outlet MULTITuDE_MassiveSumm_globalvoices, splits {'train': 9}
- Group 9590: size 9, lang nl, outlet MULTITuDE_MassiveSumm_globalvoices, splits {'train': 9}
- Group 11816: size 9, lang pt, outlet MassiveSumm_voaportugues, splits {'train': 9}

## Junk Counts (New Script-Aware)
- arabic / train / Llama-2-70b-chat-hf: 1
- arabic / train / human: 5
- arabic / train / opt-iml-max-30b: 1
- arabic / train / vicuna-13b: 1
- cyrillic / test / opt-iml-max-30b: 1
- cyrillic / train / human: 2
- cyrillic / train / opt-iml-max-30b: 2
- greek / train / opt-iml-max-30b: 1
- hanzi / test / Llama-2-70b-chat-hf: 26
- hanzi / test / Mistral-7B-Instruct-v0.2: 6
- hanzi / test / v5-Eagle-7B-HF: 4
- hanzi / test / vicuna-13b: 7
- hanzi / train / Llama-2-70b-chat-hf: 78
- hanzi / train / Mistral-7B-Instruct-v0.2: 12
- hanzi / train / opt-iml-max-30b: 2
- hanzi / train / v5-Eagle-7B-HF: 12
- hanzi / train / vicuna-13b: 19
- hanzi / val / Llama-2-70b-chat-hf: 14
- hanzi / val / Mistral-7B-Instruct-v0.2: 2
- hanzi / val / v5-Eagle-7B-HF: 1
- hanzi / val / vicuna-13b: 3
- latin / test / Mistral-7B-Instruct-v0.2: 1
- latin / test / human: 5
- latin / test / opt-iml-max-30b: 25
- latin / train / human: 16
- latin / train / opt-iml-max-30b: 15
- latin / train / vicuna-13b: 1
- latin / val / human: 2
- latin / val / opt-iml-max-30b: 6
- latin / val / v5-Eagle-7B-HF: 1

## Story Disjointness

### VAL
- ar: 97.9% disjoint
- bg: 98.0% disjoint
- cs: 98.2% disjoint
- de: 98.6% disjoint
- el: 97.8% disjoint
- en: 94.8% disjoint
- es: 97.7% disjoint
- hr: 99.1% disjoint
- hu: 98.7% disjoint
- nl: 98.1% disjoint
- pl: 98.2% disjoint
- pt: 97.3% disjoint
- ro: 98.5% disjoint
- ru: 96.6% disjoint
- sk: 97.4% disjoint
- sl: 98.8% disjoint
- uk: 96.6% disjoint
- zh: 91.4% disjoint

### TEST
- ar: 97.8% disjoint
- bg: 97.4% disjoint
- cs: 97.8% disjoint
- de: 99.4% disjoint
- el: 97.7% disjoint
- en: 97.3% disjoint
- es: 98.5% disjoint
- hr: 98.6% disjoint
- hu: 98.7% disjoint
- nl: 99.0% disjoint
- pl: 98.3% disjoint
- pt: 97.4% disjoint
- ro: 98.1% disjoint
- ru: 97.6% disjoint
- sk: 97.8% disjoint
- sl: 99.1% disjoint
- uk: 98.0% disjoint
- zh: 95.3% disjoint
