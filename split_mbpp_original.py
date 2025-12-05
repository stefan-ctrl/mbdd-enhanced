import json
import re
from pathlib import Path


def sanitize_filename(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", str(name)).strip()


EXCEPTION_KEEP_LITERAL_NEWLINE = (
    "Forces of the \\ndarkness*are coming into the play.",
    "Mi Box runs on the \\n Latest android*which has google assistance and chromecast.",
    "Certain services\\nare subjected to change*over the seperate subscriptions.",
)


def decode_minimal(s: str) -> str:
    # Minimal decoding for common escapes
    # Handle exception: keep literal "\\n" for specific phrase(s)
    keep_literal_newline = any(p in s for p in EXCEPTION_KEEP_LITERAL_NEWLINE)

    if "\\n" in s and "\n" not in s and not keep_literal_newline:
        s = s.replace("\\n", "\n")
    if "\\t" in s and "\t" not in s:
        s = s.replace("\\t", "\t")
    s = s.replace('\\"', '"').replace("\\'", "'")
    return s


def main():
    repo_root = Path(__file__).parent
    input_path = repo_root / "mbpp.jsonl"

    prompt_dir = repo_root / "original" / "prompt"
    code_dir = repo_root / "original" / "code"
    tests_dir = repo_root / "original" / "tests"

    for d in (prompt_dir, code_dir, tests_dir):
        d.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    total = 0
    written_prompt = written_code = written_tests = 0

    with input_path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError as e:
                # Skip invalid lines, but count them
                continue

            total += 1

            if not isinstance(entry, dict):
                continue

            task_id = entry.get("task_id")
            if task_id is None:
                task_id = f"item_{idx}"
            fname = sanitize_filename(task_id)

            # Original MBPP uses `text` for prompt
            prompt = entry.get("prompt", entry.get("text"))
            code = entry.get("code")
            tests = entry.get("tests")
            test_list = entry.get("test_list")
            test_imports = entry.get("test_imports")
            test_setup_code = entry.get("test_setup_code")

            if prompt is not None:
                prompt_str = decode_minimal(str(prompt))
                (prompt_dir / f"{fname}.txt").write_text(prompt_str, encoding="utf-8")
                written_prompt += 1

            if code is not None:
                code_str = decode_minimal(str(code))
                (code_dir / f"{fname}.py").write_text(code_str, encoding="utf-8")
                written_code += 1

            # Build tests content with optional imports and setup code
            imports_block = ""
            if isinstance(test_imports, list) and test_imports:
                import_lines = [decode_minimal(str(imp)) for imp in test_imports]
                imports_block = "\n".join(import_lines) + "\n"

            setup_block = ""
            if isinstance(test_setup_code, str) and test_setup_code.strip():
                setup_block = decode_minimal(test_setup_code)
                if not setup_block.endswith("\n"):
                    setup_block += "\n"

            if isinstance(test_list, list) and test_list:
                lines = [decode_minimal(str(t)) for t in test_list]
                assertions_content = "\n".join(lines) + "\n"
                content = imports_block + setup_block + assertions_content
                (tests_dir / f"{fname}.py").write_text(content, encoding="utf-8")
                written_tests += 1
            elif tests is not None:
                tests_str = decode_minimal(str(tests))
                content = imports_block + setup_block + tests_str
                (tests_dir / f"{fname}.py").write_text(content, encoding="utf-8")
                written_tests += 1

    summary = {
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
    }

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
