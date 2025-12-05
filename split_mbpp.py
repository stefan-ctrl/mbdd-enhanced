import json
import os
import re
from pathlib import Path


def sanitize_filename(name: str) -> str:
    # Keep alphanumerics, dash, underscore; replace others with underscore
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(name)).strip()


def main():
    repo_root = Path(__file__).parent
    input_path = repo_root / "sanitized-mbpp.json"

    prompt_dir = repo_root / "sanitized" / "prompt"
    code_dir = repo_root / "sanitized" / "code"
    tests_dir = repo_root / "sanitized" / "tests"

    for d in (prompt_dir, code_dir, tests_dir):
        d.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}")

    if not isinstance(data, list):
        raise ValueError("Expected a JSON array at top level.")

    total = len(data)
    written_prompt = written_code = written_tests = 0

    for idx, entry in enumerate(data, start=1):
        if not isinstance(entry, dict):
            continue

        task_id = entry.get("task_id")
        if task_id is None:
            # Fallback to index if task_id missing
            task_id = f"item_{idx}"

        fname = sanitize_filename(task_id)

        prompt = entry.get("prompt")
        code = entry.get("code")
        tests = entry.get("tests")
        test_list = entry.get("test_list")
        test_imports = entry.get("test_imports")  # optional list of import statements

        if prompt is not None:
            (prompt_dir / f"{fname}.txt").write_text(str(prompt), encoding="utf-8")
            written_prompt += 1

        if code is not None:
            code_str = str(code)
            # If the string contains literal escape sequences like "\n" rather than real newlines,
            # convert them to actual characters without over-decoding.
            # Only replace if real newlines aren't already present.
            if "\\n" in code_str and "\n" not in code_str:
                code_str = code_str.replace("\\n", "\n")
            if "\\t" in code_str and "\t" not in code_str:
                code_str = code_str.replace("\\t", "\t")
            # Handle escaped quotes minimally (common in embedded JSON strings)
            code_str = code_str.replace('\\"', '"').replace("\\'", "'")

            (code_dir / f"{fname}.py").write_text(code_str, encoding="utf-8")
            written_code += 1

        # Prefer test_list if present; otherwise use tests
        if test_list is not None:
            # Expecting a list of assertions; join into one file
            if isinstance(test_list, list):
                # Ensure each entry is a string and decode basic escapes
                lines = []
                for t in test_list:
                    t_str = str(t)
                    if "\\n" in t_str and "\n" not in t_str:
                        t_str = t_str.replace("\\n", "\n")
                    if "\\t" in t_str and "\t" not in t_str:
                        t_str = t_str.replace("\\t", "\t")
                    t_str = t_str.replace('\\"', '"').replace("\\'", "'")
                    lines.append(t_str)
                assertions_content = "\n".join(lines) + "\n"

                # Prepend optional test imports
                import_lines = []
                if isinstance(test_imports, list):
                    for imp in test_imports:
                        imp_str = str(imp)
                        if "\\n" in imp_str and "\n" not in imp_str:
                            imp_str = imp_str.replace("\\n", "\n")
                        if "\\t" in imp_str and "\t" not in imp_str:
                            imp_str = imp_str.replace("\\t", "\t")
                        imp_str = imp_str.replace('\\"', '"').replace("\\'", "'")
                        import_lines.append(imp_str)
                imports_block = ("\n".join(import_lines) + ("\n" if import_lines else ""))

                content = imports_block + assertions_content
                (tests_dir / f"{fname}.py").write_text(content, encoding="utf-8")
                written_tests += 1
        elif tests is not None:
            tests_str = str(tests)
            if "\\n" in tests_str and "\n" not in tests_str:
                tests_str = tests_str.replace("\\n", "\n")
            if "\\t" in tests_str and "\t" not in tests_str:
                tests_str = tests_str.replace("\\t", "\t")
            tests_str = tests_str.replace('\\"', '"').replace("\\'", "'")
            import_lines = []
            if isinstance(test_imports, list):
                for imp in test_imports:
                    imp_str = str(imp)
                    if "\\n" in imp_str and "\n" not in imp_str:
                        imp_str = imp_str.replace("\\n", "\n")
                    if "\\t" in imp_str and "\t" not in imp_str:
                        imp_str = imp_str.replace("\\t", "\t")
                    imp_str = imp_str.replace('\\"', '"').replace("\\'", "'")
                    import_lines.append(imp_str)
            imports_block = ("\n".join(import_lines) + ("\n" if import_lines else ""))
            content = imports_block + tests_str
            (tests_dir / f"{fname}.py").write_text(content, encoding="utf-8")
            written_tests += 1

    print(
        json.dumps(
            {
                "total_entries": total,
                "written": {
                    "prompt": written_prompt,
                    "code": written_code,
                    "tests": written_tests,
                },
                "output_dirs": {
                    "prompt": str(prompt_dir),
                    "code": str(code_dir),
                    "tests": str(tests_dir),
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
