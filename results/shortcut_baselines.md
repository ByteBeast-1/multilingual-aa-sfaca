# Shortcut Baselines Report

Macro-F1 (chance ≈ 0.125) on val and test sets using simple shortcut features.

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