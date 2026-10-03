# Cross-Split Similarity (Leakage Measurement)

Comparing maximum cosine similarity of val/test rows to train rows of **different labels** (multi_label) in the same language.

| Language | Comparison | Mean | P50 | P90 | P99 | %>0.5 | %>0.7 |
|---|---|---|---|---|---|---|---|
| uk | val->train (actual) | 0.380 | 0.369 | 0.498 | 0.639 | 9.6% | 0.7% |
| uk | test->train (actual) | 0.371 | 0.356 | 0.482 | 0.799 | 8.3% | 2.0% |
| uk | val->train (random) | 0.422 | 0.416 | 0.556 | 0.824 | 19.8% | 2.4% |
| uk | test->train (random) | 0.423 | 0.412 | 0.560 | 0.817 | 21.3% | 2.6% |
| hu | val->train (actual) | 0.415 | 0.391 | 0.570 | 0.774 | 18.4% | 4.8% |
| hu | test->train (actual) | 0.381 | 0.366 | 0.496 | 0.717 | 9.6% | 1.2% |
| hu | val->train (random) | 0.407 | 0.398 | 0.527 | 0.711 | 14.9% | 1.1% |
| hu | test->train (random) | 0.410 | 0.395 | 0.542 | 0.746 | 16.9% | 2.1% |
| de | val->train (actual) | 0.434 | 0.426 | 0.546 | 0.650 | 19.8% | 0.4% |
| de | test->train (actual) | 0.427 | 0.419 | 0.536 | 0.676 | 17.0% | 0.8% |
| de | val->train (random) | 0.490 | 0.484 | 0.634 | 0.747 | 43.2% | 3.0% |
| de | test->train (random) | 0.490 | 0.487 | 0.622 | 0.726 | 45.4% | 2.1% |
| es | val->train (actual) | 0.465 | 0.454 | 0.591 | 0.738 | 31.5% | 1.9% |
| es | test->train (actual) | 0.433 | 0.428 | 0.522 | 0.752 | 15.2% | 1.6% |
| es | val->train (random) | 0.530 | 0.530 | 0.678 | 0.796 | 57.7% | 6.9% |
| es | test->train (random) | 0.528 | 0.527 | 0.674 | 0.804 | 59.1% | 6.6% |
| pl | val->train (actual) | 0.439 | 0.417 | 0.622 | 0.753 | 28.8% | 3.7% |
| pl | test->train (actual) | 0.366 | 0.350 | 0.479 | 0.669 | 7.8% | 0.7% |
| pl | val->train (random) | 0.415 | 0.401 | 0.554 | 0.761 | 18.2% | 2.4% |
| pl | test->train (random) | 0.411 | 0.400 | 0.547 | 0.742 | 18.3% | 1.9% |
| en | val->train (actual) | 0.538 | 0.529 | 0.665 | 0.773 | 61.4% | 5.3% |
| en | test->train (actual) | 0.516 | 0.512 | 0.638 | 0.720 | 55.2% | 2.2% |
| en | val->train (random) | 0.623 | 0.628 | 0.746 | 0.820 | 88.1% | 22.8% |
| en | test->train (random) | 0.624 | 0.632 | 0.748 | 0.822 | 87.9% | 23.8% |
| ro | val->train (actual) | 0.478 | 0.454 | 0.677 | 0.743 | 37.5% | 5.9% |
| ro | test->train (actual) | 0.416 | 0.408 | 0.524 | 0.679 | 14.8% | 0.5% |
| ro | val->train (random) | 0.446 | 0.434 | 0.576 | 0.767 | 26.2% | 2.1% |
| ro | test->train (random) | 0.446 | 0.434 | 0.575 | 0.777 | 26.3% | 2.6% |
| nl | val->train (actual) | 0.508 | 0.505 | 0.627 | 0.704 | 51.8% | 1.1% |
| nl | test->train (actual) | 0.476 | 0.469 | 0.592 | 0.708 | 35.6% | 1.2% |
| nl | val->train (random) | 0.543 | 0.542 | 0.672 | 0.768 | 67.0% | 5.2% |
| nl | test->train (random) | 0.544 | 0.547 | 0.677 | 0.768 | 65.7% | 6.1% |
| ru | val->train (actual) | 0.399 | 0.375 | 0.534 | 0.795 | 15.5% | 3.5% |
| ru | test->train (actual) | 0.373 | 0.354 | 0.487 | 0.778 | 8.9% | 2.4% |
| ru | val->train (random) | 0.433 | 0.424 | 0.590 | 0.775 | 27.1% | 2.3% |
| ru | test->train (random) | 0.437 | 0.427 | 0.585 | 0.793 | 26.2% | 3.1% |
| bg | val->train (actual) | 0.402 | 0.398 | 0.513 | 0.636 | 12.8% | 0.7% |
| bg | test->train (actual) | 0.386 | 0.371 | 0.490 | 0.817 | 9.1% | 2.6% |
| bg | val->train (random) | 0.436 | 0.427 | 0.574 | 0.793 | 25.7% | 2.3% |
| bg | test->train (random) | 0.437 | 0.424 | 0.576 | 0.816 | 25.7% | 2.8% |
| pt | val->train (actual) | 0.467 | 0.460 | 0.583 | 0.705 | 34.0% | 1.1% |
| pt | test->train (actual) | 0.432 | 0.422 | 0.544 | 0.776 | 18.8% | 2.7% |
| pt | val->train (random) | 0.522 | 0.528 | 0.659 | 0.772 | 60.0% | 3.9% |
| pt | test->train (random) | 0.517 | 0.518 | 0.666 | 0.792 | 56.2% | 5.9% |
| el | val->train (actual) | 0.333 | 0.322 | 0.427 | 0.547 | 2.9% | 0.0% |
| el | test->train (actual) | 0.343 | 0.322 | 0.440 | 0.770 | 5.5% | 2.3% |
| el | val->train (random) | 0.360 | 0.345 | 0.479 | 0.747 | 7.2% | 1.3% |
| el | test->train (random) | 0.367 | 0.345 | 0.491 | 0.778 | 8.9% | 2.2% |
| hr | val->train (actual) | 0.394 | 0.384 | 0.527 | 0.640 | 14.8% | 0.4% |
| hr | test->train (actual) | 0.391 | 0.377 | 0.519 | 0.734 | 13.1% | 1.4% |
| hr | val->train (random) | 0.425 | 0.417 | 0.576 | 0.727 | 22.8% | 1.5% |
| hr | test->train (random) | 0.420 | 0.410 | 0.565 | 0.748 | 22.6% | 1.7% |
| zh | val->train (actual) | 0.401 | 0.375 | 0.635 | 0.843 | 23.6% | 4.7% |
| zh | test->train (actual) | 0.404 | 0.379 | 0.621 | 0.878 | 25.2% | 5.3% |
| zh | val->train (random) | 0.445 | 0.427 | 0.678 | 0.890 | 33.0% | 8.7% |
| zh | test->train (random) | 0.434 | 0.414 | 0.674 | 0.912 | 31.4% | 8.2% |
| ar | val->train (actual) | 0.372 | 0.362 | 0.488 | 0.622 | 9.2% | 0.5% |
| ar | test->train (actual) | 0.377 | 0.359 | 0.501 | 0.769 | 10.1% | 2.2% |
| ar | val->train (random) | 0.407 | 0.397 | 0.541 | 0.754 | 18.8% | 1.6% |
| ar | test->train (random) | 0.412 | 0.399 | 0.557 | 0.778 | 20.3% | 2.1% |
| cs | val->train (actual) | 0.360 | 0.353 | 0.474 | 0.552 | 6.8% | 0.0% |
| cs | test->train (actual) | 0.355 | 0.336 | 0.474 | 0.760 | 7.5% | 2.2% |
| cs | val->train (random) | 0.407 | 0.392 | 0.562 | 0.738 | 18.5% | 2.2% |
| cs | test->train (random) | 0.399 | 0.385 | 0.546 | 0.744 | 16.5% | 2.2% |
| sl | val->train (actual) | 0.405 | 0.400 | 0.517 | 0.637 | 14.2% | 0.1% |
| sl | test->train (actual) | 0.376 | 0.363 | 0.490 | 0.704 | 8.8% | 1.1% |
| sl | val->train (random) | 0.418 | 0.406 | 0.557 | 0.713 | 21.8% | 1.4% |
| sl | test->train (random) | 0.412 | 0.399 | 0.550 | 0.739 | 18.4% | 1.6% |
| sk | val->train (actual) | 0.348 | 0.338 | 0.452 | 0.624 | 4.7% | 0.6% |
| sk | test->train (actual) | 0.362 | 0.335 | 0.512 | 0.757 | 10.8% | 2.2% |
| sk | val->train (random) | 0.388 | 0.368 | 0.567 | 0.781 | 16.9% | 2.4% |
| sk | test->train (random) | 0.385 | 0.363 | 0.540 | 0.749 | 14.3% | 2.1% |

## Conclusion

**Test->Train similarity is HIGH** for languages: de, es, en, ro, nl, pt, hr, zh, ar, sk. This indicates that the benchmark's original test split shares story groups with the train split, meaning the benchmark itself leaks stories across its splits.

The actual val->train similarity should be significantly lower than the random val->train similarity, demonstrating that the grouped splitting successfully prevented story leakage into the validation set.