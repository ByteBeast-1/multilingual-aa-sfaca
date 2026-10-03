# Data Card Metrics

## Groups (Train + Val)
- Test rows have group_id -1 and are not counted here.
- Number of human anchors: 17992
- Humans with no attached machine text: 2651 (14.7%)
- Group sizes: min=1, median=6.0, p90=15.0, max=821

### Top 10 Largest Groups
- Group 4766: size 821, lang el, outlet MULTITuDE_MassiveSumm_voanews, splits {'train': 821}
- Group 729: size 793, lang ar, outlet MULTITuDE_MassiveSumm_rt, splits {'train': 793}
- Group 14888: size 566, lang sk, outlet MULTITuDE_MassiveSumm_sme, splits {'train': 566}
- Group 2533: size 467, lang cs, outlet MULTITuDE_MassiveSumm_denik, splits {'train': 467}
- Group 8508: size 436, lang hu, outlet MULTITuDE_MassiveSumm_24, splits {'train': 436}
- Group 9032: size 252, lang nl, outlet MULTITuDE_MassiveSumm_globalvoices, splits {'train': 252}
- Group 11658: size 241, lang pt, outlet MULTITuDE_MassiveSumm_rfi, splits {'train': 241}
- Group 6294: size 238, lang es, outlet MULTITuDE_MassiveSumm_20minutos, splits {'train': 238}
- Group 12144: size 235, lang ro, outlet MULTITuDE_MassiveSumm_dw, splits {'val': 235}
- Group 4148: size 213, lang el, outlet MULTITuDE_MassiveSumm_eleftherostypos, splits {'val': 213}

## Junk Counts (New Script-Aware)
- arabic / train / Llama-2-70b-chat-hf: 1
- arabic / train / human: 4
- arabic / train / opt-iml-max-30b: 1
- arabic / train / vicuna-13b: 1
- arabic / val / human: 1
- cyrillic / test / opt-iml-max-30b: 1
- cyrillic / train / human: 2
- cyrillic / train / opt-iml-max-30b: 1
- cyrillic / val / opt-iml-max-30b: 1
- greek / train / opt-iml-max-30b: 1
- hanzi / test / Llama-2-70b-chat-hf: 26
- hanzi / test / Mistral-7B-Instruct-v0.2: 6
- hanzi / test / v5-Eagle-7B-HF: 4
- hanzi / test / vicuna-13b: 7
- hanzi / train / Llama-2-70b-chat-hf: 86
- hanzi / train / Mistral-7B-Instruct-v0.2: 12
- hanzi / train / opt-iml-max-30b: 2
- hanzi / train / v5-Eagle-7B-HF: 12
- hanzi / train / vicuna-13b: 22
- hanzi / val / Llama-2-70b-chat-hf: 6
- hanzi / val / Mistral-7B-Instruct-v0.2: 2
- hanzi / val / v5-Eagle-7B-HF: 1
- latin / test / Mistral-7B-Instruct-v0.2: 1
- latin / test / human: 5
- latin / test / opt-iml-max-30b: 25
- latin / train / human: 14
- latin / train / opt-iml-max-30b: 19
- latin / train / v5-Eagle-7B-HF: 1
- latin / train / vicuna-13b: 1
- latin / val / human: 4
- latin / val / opt-iml-max-30b: 2

## Story Disjointness

### VAL
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

### TEST
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
