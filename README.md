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