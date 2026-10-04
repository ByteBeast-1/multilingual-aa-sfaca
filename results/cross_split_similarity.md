# Cross-Split Similarity (Leakage Measurement)

Comparing maximum cosine similarity of val/test rows to train rows of **different labels** (multi_label) in the same language.

| Language | Comparison | Mean | P50 | P90 | P99 | %>0.5 | %>0.7 |
|---|---|---|---|---|---|---|---|
| uk | val->train (actual) | 0.390 | 0.370 | 0.523 | 0.841 | 12.4% | 3.4% |
| uk | test->train (actual) | 0.371 | 0.356 | 0.486 | 0.808 | 8.4% | 2.0% |
| uk | val->train (random) | 0.418 | 0.404 | 0.559 | 0.764 | 20.0% | 2.2% |
| uk | test->train (random) | 0.421 | 0.409 | 0.566 | 0.818 | 21.0% | 2.4% |
| hu | val->train (actual) | 0.388 | 0.376 | 0.508 | 0.744 | 11.0% | 1.3% |
| hu | test->train (actual) | 0.380 | 0.365 | 0.496 | 0.725 | 9.7% | 1.3% |
| hu | val->train (random) | 0.403 | 0.391 | 0.528 | 0.748 | 15.7% | 1.8% |
| hu | test->train (random) | 0.412 | 0.400 | 0.543 | 0.741 | 17.4% | 1.6% |
| de | val->train (actual) | 0.438 | 0.427 | 0.558 | 0.707 | 21.0% | 1.4% |
| de | test->train (actual) | 0.428 | 0.420 | 0.537 | 0.673 | 17.8% | 0.6% |
| de | val->train (random) | 0.488 | 0.481 | 0.614 | 0.744 | 42.7% | 2.0% |
| de | test->train (random) | 0.491 | 0.489 | 0.623 | 0.726 | 45.3% | 2.1% |
| es | val->train (actual) | 0.449 | 0.441 | 0.561 | 0.808 | 23.0% | 2.3% |
| es | test->train (actual) | 0.432 | 0.429 | 0.519 | 0.741 | 14.8% | 1.5% |
| es | val->train (random) | 0.526 | 0.526 | 0.665 | 0.825 | 57.5% | 6.5% |
| es | test->train (random) | 0.532 | 0.530 | 0.675 | 0.798 | 60.4% | 6.7% |
| pl | val->train (actual) | 0.394 | 0.377 | 0.519 | 0.740 | 12.1% | 1.8% |
| pl | test->train (actual) | 0.370 | 0.351 | 0.483 | 0.751 | 8.6% | 1.7% |
| pl | val->train (random) | 0.421 | 0.407 | 0.567 | 0.789 | 22.0% | 2.2% |
| pl | test->train (random) | 0.412 | 0.398 | 0.547 | 0.775 | 17.8% | 2.3% |
| en | val->train (actual) | 0.524 | 0.523 | 0.650 | 0.765 | 59.2% | 5.2% |
| en | test->train (actual) | 0.516 | 0.511 | 0.639 | 0.731 | 54.7% | 2.7% |
| en | val->train (random) | 0.615 | 0.622 | 0.745 | 0.824 | 85.9% | 20.3% |
| en | test->train (random) | 0.619 | 0.627 | 0.740 | 0.824 | 88.0% | 22.1% |
| ro | val->train (actual) | 0.434 | 0.425 | 0.555 | 0.734 | 23.4% | 1.5% |
| ro | test->train (actual) | 0.418 | 0.408 | 0.524 | 0.764 | 14.6% | 1.9% |
| ro | val->train (random) | 0.443 | 0.433 | 0.566 | 0.764 | 25.6% | 1.8% |
| ro | test->train (random) | 0.451 | 0.441 | 0.581 | 0.775 | 28.2% | 2.5% |
| nl | val->train (actual) | 0.500 | 0.498 | 0.620 | 0.723 | 49.1% | 1.9% |
| nl | test->train (actual) | 0.475 | 0.469 | 0.590 | 0.701 | 35.0% | 1.0% |
| nl | val->train (random) | 0.539 | 0.540 | 0.679 | 0.767 | 63.5% | 6.2% |
| nl | test->train (random) | 0.541 | 0.545 | 0.670 | 0.761 | 64.8% | 5.0% |
| ru | val->train (actual) | 0.387 | 0.369 | 0.522 | 0.768 | 12.9% | 3.4% |
| ru | test->train (actual) | 0.373 | 0.355 | 0.490 | 0.778 | 9.1% | 2.4% |
| ru | val->train (random) | 0.434 | 0.424 | 0.582 | 0.770 | 26.9% | 2.9% |
| ru | test->train (random) | 0.435 | 0.428 | 0.582 | 0.784 | 26.2% | 3.1% |
| bg | val->train (actual) | 0.394 | 0.380 | 0.517 | 0.789 | 11.8% | 2.0% |
| bg | test->train (actual) | 0.387 | 0.371 | 0.491 | 0.815 | 9.2% | 2.6% |
| bg | val->train (random) | 0.434 | 0.426 | 0.575 | 0.779 | 25.1% | 2.1% |
| bg | test->train (random) | 0.441 | 0.428 | 0.582 | 0.802 | 26.6% | 3.2% |
| pt | val->train (actual) | 0.451 | 0.437 | 0.572 | 0.785 | 25.7% | 2.7% |
| pt | test->train (actual) | 0.431 | 0.422 | 0.545 | 0.770 | 18.9% | 2.6% |
| pt | val->train (random) | 0.519 | 0.520 | 0.657 | 0.792 | 57.9% | 4.9% |
| pt | test->train (random) | 0.518 | 0.519 | 0.665 | 0.788 | 56.7% | 5.6% |
| el | val->train (actual) | 0.353 | 0.331 | 0.465 | 0.785 | 7.3% | 2.2% |
| el | test->train (actual) | 0.344 | 0.324 | 0.442 | 0.770 | 5.5% | 2.3% |
| el | val->train (random) | 0.370 | 0.344 | 0.503 | 0.807 | 10.5% | 2.2% |
| el | test->train (random) | 0.373 | 0.352 | 0.495 | 0.779 | 9.5% | 2.4% |
| hr | val->train (actual) | 0.418 | 0.410 | 0.553 | 0.688 | 20.8% | 0.9% |
| hr | test->train (actual) | 0.390 | 0.377 | 0.517 | 0.730 | 12.8% | 1.4% |
| hr | val->train (random) | 0.426 | 0.415 | 0.572 | 0.748 | 24.7% | 2.0% |
| hr | test->train (random) | 0.423 | 0.412 | 0.574 | 0.764 | 23.0% | 2.1% |
| zh | val->train (actual) | 0.429 | 0.408 | 0.679 | 0.913 | 31.4% | 8.6% |
| zh | test->train (actual) | 0.401 | 0.380 | 0.614 | 0.874 | 24.0% | 4.7% |
| zh | val->train (random) | 0.443 | 0.409 | 0.706 | 0.991 | 32.8% | 10.2% |
| zh | test->train (random) | 0.433 | 0.414 | 0.676 | 0.899 | 31.4% | 8.3% |
| ar | val->train (actual) | 0.375 | 0.358 | 0.503 | 0.780 | 10.3% | 2.1% |
| ar | test->train (actual) | 0.377 | 0.359 | 0.501 | 0.767 | 10.1% | 2.2% |
| ar | val->train (random) | 0.407 | 0.393 | 0.552 | 0.786 | 17.8% | 2.1% |
| ar | test->train (random) | 0.414 | 0.398 | 0.562 | 0.783 | 21.4% | 2.6% |
| cs | val->train (actual) | 0.377 | 0.360 | 0.509 | 0.774 | 11.2% | 1.8% |
| cs | test->train (actual) | 0.355 | 0.336 | 0.475 | 0.760 | 7.5% | 2.2% |
| cs | val->train (random) | 0.401 | 0.384 | 0.539 | 0.766 | 15.6% | 2.7% |
| cs | test->train (random) | 0.399 | 0.385 | 0.545 | 0.739 | 16.3% | 2.1% |
| sl | val->train (actual) | 0.392 | 0.381 | 0.512 | 0.722 | 11.9% | 1.2% |
| sl | test->train (actual) | 0.375 | 0.362 | 0.488 | 0.693 | 8.7% | 0.9% |
| sl | val->train (random) | 0.409 | 0.398 | 0.544 | 0.732 | 16.6% | 1.6% |
| sl | test->train (random) | 0.412 | 0.399 | 0.552 | 0.743 | 18.9% | 1.6% |
| sk | val->train (actual) | 0.374 | 0.350 | 0.538 | 0.806 | 12.8% | 2.6% |
| sk | test->train (actual) | 0.362 | 0.335 | 0.511 | 0.752 | 10.7% | 2.2% |
| sk | val->train (random) | 0.391 | 0.364 | 0.564 | 0.797 | 15.8% | 2.9% |
| sk | test->train (random) | 0.386 | 0.365 | 0.543 | 0.750 | 14.6% | 2.2% |

## Conclusion

- **Val actual < Random control**: 18 out of 18 languages.
- **Test actual < Random control**: 18 out of 18 languages.
- **Val->train > Test->train similarity**: 17 out of 18 languages.

### Per-language share of test rows with similarity above 0.7:
- uk: 2.0%
- hu: 1.3%
- de: 0.6%
- es: 1.5%
- pl: 1.7%
- en: 2.7%
- ro: 1.9%
- nl: 1.0%
- ru: 2.4%
- bg: 2.6%
- pt: 2.6%
- el: 2.3%
- hr: 1.4%
- zh: 4.7%
- ar: 2.2%
- cs: 2.2%
- sl: 0.9%
- sk: 2.2%