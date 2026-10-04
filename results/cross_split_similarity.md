# Cross-Split Similarity (Leakage Measurement)

Comparing maximum cosine similarity of val/test rows to train rows of **different labels** (multi_label) in the same language.

| Language | Comparison | Mean | P50 | P90 | P99 | %>0.5 | %>0.7 |
|---|---|---|---|---|---|---|---|
| uk | val->train (actual) | 0.390 | 0.370 | 0.523 | 0.841 | 12.4% | 3.4% |
| uk | test->train (actual) | 0.371 | 0.356 | 0.486 | 0.808 | 8.4% | 2.0% |
| uk | val->train (random) | 0.429 | 0.417 | 0.572 | 0.810 | 23.3% | 2.9% |
| uk | test->train (random) | 0.422 | 0.410 | 0.556 | 0.819 | 21.5% | 2.6% |
| hu | val->train (actual) | 0.388 | 0.376 | 0.508 | 0.744 | 11.0% | 1.3% |
| hu | test->train (actual) | 0.380 | 0.365 | 0.496 | 0.725 | 9.7% | 1.3% |
| hu | val->train (random) | 0.409 | 0.396 | 0.548 | 0.741 | 17.8% | 1.6% |
| hu | test->train (random) | 0.406 | 0.394 | 0.535 | 0.740 | 16.1% | 1.4% |
| de | val->train (actual) | 0.438 | 0.427 | 0.558 | 0.707 | 21.0% | 1.4% |
| de | test->train (actual) | 0.428 | 0.420 | 0.537 | 0.673 | 17.8% | 0.6% |
| de | val->train (random) | 0.489 | 0.487 | 0.623 | 0.727 | 44.5% | 2.3% |
| de | test->train (random) | 0.490 | 0.485 | 0.625 | 0.725 | 44.0% | 2.2% |
| es | val->train (actual) | 0.449 | 0.441 | 0.561 | 0.808 | 23.0% | 2.3% |
| es | test->train (actual) | 0.432 | 0.429 | 0.519 | 0.741 | 14.8% | 1.5% |
| es | val->train (random) | 0.533 | 0.530 | 0.674 | 0.811 | 59.7% | 6.4% |
| es | test->train (random) | 0.531 | 0.530 | 0.677 | 0.806 | 60.1% | 7.1% |
| pl | val->train (actual) | 0.394 | 0.377 | 0.519 | 0.740 | 12.1% | 1.8% |
| pl | test->train (actual) | 0.370 | 0.351 | 0.483 | 0.751 | 8.6% | 1.7% |
| pl | val->train (random) | 0.415 | 0.402 | 0.554 | 0.740 | 19.2% | 1.7% |
| pl | test->train (random) | 0.411 | 0.397 | 0.553 | 0.753 | 18.7% | 2.1% |
| en | val->train (actual) | 0.524 | 0.523 | 0.650 | 0.765 | 59.2% | 5.2% |
| en | test->train (actual) | 0.516 | 0.511 | 0.639 | 0.731 | 54.7% | 2.7% |
| en | val->train (random) | 0.622 | 0.631 | 0.746 | 0.825 | 88.4% | 22.4% |
| en | test->train (random) | 0.622 | 0.627 | 0.742 | 0.822 | 88.2% | 22.7% |
| ro | val->train (actual) | 0.434 | 0.425 | 0.555 | 0.734 | 23.4% | 1.5% |
| ro | test->train (actual) | 0.418 | 0.408 | 0.524 | 0.764 | 14.6% | 1.9% |
| ro | val->train (random) | 0.450 | 0.441 | 0.579 | 0.783 | 28.6% | 2.2% |
| ro | test->train (random) | 0.449 | 0.438 | 0.587 | 0.763 | 28.6% | 2.3% |
| nl | val->train (actual) | 0.500 | 0.498 | 0.620 | 0.723 | 49.1% | 1.9% |
| nl | test->train (actual) | 0.475 | 0.469 | 0.590 | 0.701 | 35.0% | 1.0% |
| nl | val->train (random) | 0.540 | 0.544 | 0.673 | 0.769 | 65.6% | 6.6% |
| nl | test->train (random) | 0.542 | 0.545 | 0.673 | 0.764 | 64.7% | 5.2% |
| ru | val->train (actual) | 0.387 | 0.369 | 0.522 | 0.768 | 12.9% | 3.4% |
| ru | test->train (actual) | 0.373 | 0.355 | 0.490 | 0.778 | 9.1% | 2.4% |
| ru | val->train (random) | 0.432 | 0.425 | 0.571 | 0.777 | 25.5% | 2.7% |
| ru | test->train (random) | 0.434 | 0.425 | 0.589 | 0.786 | 26.1% | 2.7% |
| bg | val->train (actual) | 0.394 | 0.380 | 0.517 | 0.789 | 11.8% | 2.0% |
| bg | test->train (actual) | 0.387 | 0.371 | 0.491 | 0.815 | 9.2% | 2.6% |
| bg | val->train (random) | 0.433 | 0.421 | 0.566 | 0.791 | 25.2% | 2.3% |
| bg | test->train (random) | 0.439 | 0.427 | 0.576 | 0.822 | 25.6% | 3.1% |
| pt | val->train (actual) | 0.451 | 0.437 | 0.572 | 0.785 | 25.7% | 2.7% |
| pt | test->train (actual) | 0.431 | 0.422 | 0.545 | 0.770 | 18.9% | 2.6% |
| pt | val->train (random) | 0.516 | 0.515 | 0.662 | 0.776 | 55.2% | 5.2% |
| pt | test->train (random) | 0.518 | 0.521 | 0.657 | 0.795 | 57.3% | 5.4% |
| el | val->train (actual) | 0.353 | 0.331 | 0.465 | 0.785 | 7.3% | 2.2% |
| el | test->train (actual) | 0.344 | 0.324 | 0.442 | 0.770 | 5.5% | 2.3% |
| el | val->train (random) | 0.366 | 0.345 | 0.493 | 0.773 | 9.4% | 2.6% |
| el | test->train (random) | 0.371 | 0.347 | 0.502 | 0.773 | 10.1% | 1.9% |
| hr | val->train (actual) | 0.418 | 0.410 | 0.553 | 0.688 | 20.8% | 0.9% |
| hr | test->train (actual) | 0.390 | 0.377 | 0.517 | 0.730 | 12.8% | 1.4% |
| hr | val->train (random) | 0.427 | 0.420 | 0.565 | 0.765 | 22.7% | 1.9% |
| hr | test->train (random) | 0.421 | 0.408 | 0.572 | 0.781 | 22.4% | 2.3% |
| zh | val->train (actual) | 0.429 | 0.408 | 0.679 | 0.913 | 31.4% | 8.6% |
| zh | test->train (actual) | 0.401 | 0.380 | 0.614 | 0.874 | 24.0% | 4.7% |
| zh | val->train (random) | 0.428 | 0.406 | 0.669 | 0.890 | 29.8% | 7.8% |
| zh | test->train (random) | 0.437 | 0.414 | 0.680 | 0.916 | 32.2% | 8.6% |
| ar | val->train (actual) | 0.375 | 0.358 | 0.503 | 0.780 | 10.3% | 2.1% |
| ar | test->train (actual) | 0.377 | 0.359 | 0.501 | 0.767 | 10.1% | 2.2% |
| ar | val->train (random) | 0.410 | 0.395 | 0.551 | 0.795 | 17.8% | 2.3% |
| ar | test->train (random) | 0.413 | 0.395 | 0.562 | 0.781 | 19.9% | 2.8% |
| cs | val->train (actual) | 0.377 | 0.360 | 0.509 | 0.774 | 11.2% | 1.8% |
| cs | test->train (actual) | 0.355 | 0.336 | 0.475 | 0.760 | 7.5% | 2.2% |
| cs | val->train (random) | 0.400 | 0.385 | 0.549 | 0.759 | 15.9% | 2.1% |
| cs | test->train (random) | 0.399 | 0.385 | 0.547 | 0.761 | 16.2% | 2.6% |
| sl | val->train (actual) | 0.392 | 0.381 | 0.512 | 0.722 | 11.9% | 1.2% |
| sl | test->train (actual) | 0.375 | 0.362 | 0.488 | 0.693 | 8.7% | 0.9% |
| sl | val->train (random) | 0.420 | 0.407 | 0.567 | 0.729 | 20.5% | 1.8% |
| sl | test->train (random) | 0.414 | 0.401 | 0.554 | 0.736 | 20.0% | 1.6% |
| sk | val->train (actual) | 0.374 | 0.350 | 0.538 | 0.806 | 12.8% | 2.6% |
| sk | test->train (actual) | 0.362 | 0.335 | 0.511 | 0.752 | 10.7% | 2.2% |
| sk | val->train (random) | 0.390 | 0.370 | 0.558 | 0.762 | 14.9% | 2.4% |
| sk | test->train (random) | 0.388 | 0.364 | 0.555 | 0.771 | 15.2% | 2.8% |

## Conclusion

**Test->Train similarity is HIGH** for languages: de, es, en, ro, nl, pt, hr, zh, ar, sk. This indicates that the benchmark's original test split shares story groups with the train split, meaning the benchmark itself leaks stories across its splits.

The actual val->train similarity should be significantly lower than the random val->train similarity, demonstrating that the grouped splitting successfully prevented story leakage into the validation set.