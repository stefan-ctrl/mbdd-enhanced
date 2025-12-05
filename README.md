# Mostly Basic Python Problems (MBPP) — Enhancements

This repo makes a small, practical tweak to the original MBPP dataset and workflow from Google Research:
https://github.com/google-research/google-research/tree/master/mbpp

Intent: keep the dataset intact while making it easier to browse prompts, edit code, and run tests locally with pytest.

What’s added:
- `split_mbpp.py`: splits each entry in `sanitized-mbpp.json` into files under `prompt/`, `code/`, and `tests/`, named by `task_id`.
- `test_splitted_mbpp.py`: a pytest test module that imports `code/<task_id>.py` and executes assertions from `test_list` or `tests`.

# Quick start
- Generate files: `python3 split_mbpp.py`
- Run tests: `pytest -q`
- With coverage:
     ```bash
     pytest --cov=original/code --cov=sanitized/code \
                     --cov-report=term-missing \
                     --cov-report=xml:reports/coverage.xml \
                     --cov-report=html:reports/htmlcov
     ```


# Analysis
Based on `analyse_mbpp.py`:

## Original Summary
| Metric | Count | Min | Median | Average | Max |
|---|---:|---:|---:|---:|---:|
| Code lines | 974 | 2 | 5.0 | 6.7 | 50 |
| Prompt characters | 974 | 37 | 77.0 | 78.62 | 249 |
| Prompt words | 974 | 7 | 14.0 | 14.61 | 44 |
| Prompt sentences | 974 | 1 | 1.0 | 1.02 | 7 |


## Sanitized Summary
| Metric | Count | Min | Median | Average | Max |
|---|---:|---:|---:|---:|---:|
| Code lines | 427 | 2 | 4 | 5.85 | 26 |
| Prompt characters | 427 | 39 | 82 | 92.63 | 410 |
| Prompt words | 427 | 7 | 16 | 17.26 | 81 |
| Prompt sentences | 427 | 1 | 1 | 1.24 | 5 |

## Code lines (Comparison)
| Metric | original | sanitized |
|---|---|---|
| Count | 974 | 427 |
| Min | 2 | 2 |
| Median | 5.0 | 4 |
| Average | 6.7 | 5.85 |
| Max | 50 | 26 |

## Prompt characters (Comparison)
| Metric | original | sanitized |
|---|---|---|
| Count | 974 | 427 |
| Min | 37 | 39 |
| Median | 77.0 | 82 |
| Average | 78.62 | 92.63 |
| Max | 249 | 410 |

## Prompt words (Comparison)
| Metric | original | sanitized |
|---|---|---|
| Count | 974 | 427 |
| Min | 7 | 7 |
| Median | 14.0 | 16 |
| Average | 14.61 | 17.26 |
| Max | 44 | 81 |

## Prompt sentences (Comparison)
| Metric | original | sanitized |
|---|---|---|
| Count | 974 | 427 |
| Min | 1 | 1 |
| Median | 1.0 | 1 |
| Average | 1.02 | 1.24 |
| Max | 7 | 5 |

## Raw
```
Dataset: original
- Code lines: {'avg': 6.7, 'median': 5.0, 'min': 2, 'max': 50, 'count': 974}
- Prompt characters: {'avg': 78.62, 'median': 77.0, 'min': 37, 'max': 249, 'count': 974}
- Prompt words: {'avg': 14.61, 'median': 14.0, 'min': 7, 'max': 44, 'count': 974}
- Prompt sentences: {'avg': 1.02, 'median': 1.0, 'min': 1, 'max': 7, 'count': 974}

Dataset: sanitized
- Code lines: {'avg': 5.85, 'median': 4, 'min': 2, 'max': 26, 'count': 427}
- Prompt characters: {'avg': 92.63, 'median': 82, 'min': 39, 'max': 410, 'count': 427}
- Prompt words: {'avg': 17.26, 'median': 16, 'min': 7, 'max': 81, 'count': 427}
- Prompt sentences: {'avg': 1.24, 'median': 1, 'min': 1, 'max': 5, 'count': 427}
```

