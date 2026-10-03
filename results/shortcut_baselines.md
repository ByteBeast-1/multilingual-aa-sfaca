# Shortcut Baselines Report

Macro-F1 (chance ≈ 0.125) on val and test sets using simple shortcut features.

| Cluster | Model | Val F1 | Test F1 | Test F1 (Clean Subset) |
|---|---|---|---|---|
| cyrillic | (a) Length Features | 0.291 | 0.292 | 0.293 |
| cyrillic | (b) First 3 Words TF-IDF | 0.322 | 0.313 | 0.308 |
| cyrillic | (c) Flags Only | 0.067 | 0.059 | 0.029 |
| cyrillic | (d) All Combined | 0.343 | 0.332 | 0.315 |
| latin | (a) Length Features | 0.223 | 0.220 | 0.220 |
| latin | (b) First 3 Words TF-IDF | 0.309 | 0.303 | 0.295 |
| latin | (c) Flags Only | 0.051 | 0.050 | 0.028 |
| latin | (d) All Combined | 0.264 | 0.257 | 0.250 |
| greek | (a) Length Features | 0.318 | 0.325 | 0.324 |
| greek | (b) First 3 Words TF-IDF | 0.335 | 0.377 | 0.370 |
| greek | (c) Flags Only | 0.070 | 0.070 | 0.029 |
| greek | (d) All Combined | 0.436 | 0.423 | 0.395 |
| hanzi | (a) Length Features | 0.175 | 0.177 | 0.154 |
| hanzi | (b) First 3 Words TF-IDF | 0.394 | 0.383 | 0.365 |
| hanzi | (c) Flags Only | 0.086 | 0.073 | 0.030 |
| hanzi | (d) All Combined | 0.353 | 0.339 | 0.323 |
| arabic | (a) Length Features | 0.299 | 0.325 | 0.324 |
| arabic | (b) First 3 Words TF-IDF | 0.422 | 0.430 | 0.430 |
| arabic | (c) Flags Only | 0.057 | 0.051 | 0.029 |
| arabic | (d) All Combined | 0.401 | 0.420 | 0.419 |