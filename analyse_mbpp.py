from pathlib import Path
import re
import statistics


def list_files(base: Path, subdir: str, ext: str):
    d = base / subdir
    if not d.exists():
        return []
    return sorted(d.glob(f"*.{ext}"))


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return ""


def count_lines(text: str) -> int:
    if not text:
        return 0
    return text.rstrip("\n").count("\n") + 1


def tokenize_words(text: str) -> list[str]:
    # Split on word boundaries; include alphanumerics and underscore
    return re.findall(r"[A-Za-z0-9_]+", text)


def count_sentences(text: str) -> int:
    # Split on ., !, ? considering consecutive punctuation as one separator
    if not text:
        return 0
    parts = re.split(r"[.!?]+", text)
    # Count non-empty segments
    return sum(1 for seg in parts if seg.strip())


def describe(values: list[int]) -> dict:
    if not values:
        return {"avg": 0, "median": 0, "min": 0, "max": 0, "count": 0}
    return {
        "avg": round(sum(values) / len(values), 2),
        "median": statistics.median(values),
        "min": min(values),
        "max": max(values),
        "count": len(values),
    }


def analyse_dataset(label: str, root: Path):
    code_files = list_files(root, "code", "py")
    prompt_files = list_files(root, "prompt", "txt")

    code_line_counts = [count_lines(read_text(p)) for p in code_files]

    prompt_texts = [read_text(p) for p in prompt_files]
    prompt_char_counts = [len(t) for t in prompt_texts]
    prompt_word_counts = [len(tokenize_words(t)) for t in prompt_texts]
    prompt_sentence_counts = [count_sentences(t) for t in prompt_texts]

    # Raw output
    print(f"Dataset: {label}")
    print("- Code lines:", describe(code_line_counts))
    print("- Prompt characters:", describe(prompt_char_counts))
    print("- Prompt words:", describe(prompt_word_counts))
    print("- Prompt sentences:", describe(prompt_sentence_counts))
    print()

    # Markdown table output
    code_stats = describe(code_line_counts)
    char_stats = describe(prompt_char_counts)
    word_stats = describe(prompt_word_counts)
    sent_stats = describe(prompt_sentence_counts)

    print(f"## {label} Summary (Markdown Table)")
    print("| Metric | Count | Min | Median | Average | Max |")
    print("|---|---:|---:|---:|---:|---:|")
    print(
        f"| Code lines | {code_stats['count']} | {code_stats['min']} | {code_stats['median']} | {code_stats['avg']} | {code_stats['max']} |"
    )
    print(
        f"| Prompt characters | {char_stats['count']} | {char_stats['min']} | {char_stats['median']} | {char_stats['avg']} | {char_stats['max']} |"
    )
    print(
        f"| Prompt words | {word_stats['count']} | {word_stats['min']} | {word_stats['median']} | {word_stats['avg']} | {word_stats['max']} |"
    )
    print(
        f"| Prompt sentences | {sent_stats['count']} | {sent_stats['min']} | {sent_stats['median']} | {sent_stats['avg']} | {sent_stats['max']} |"
    )
    print()


def compare_stats(label_left: str, stats_left: dict, label_right: str, stats_right: dict, metric_name: str):
    print(f"## {metric_name} (Comparison)")
    print(f"| Metric | {label_left} | {label_right} |")
    print("|---|---|---|")
    print(f"| Count | {stats_left['count']} | {stats_right['count']} |")
    print(f"| Min | {stats_left['min']} | {stats_right['min']} |")
    print(f"| Median | {stats_left['median']} | {stats_right['median']} |")
    print(f"| Average | {stats_left['avg']} | {stats_right['avg']} |")
    print(f"| Max | {stats_left['max']} | {stats_right['max']} |")
    print()


def main():
    base = Path(__file__).parent
    sanitized = base / "sanitized"
    original = base / "original"

    # Collect stats for both datasets
    def collect(root: Path):
        code_files = list_files(root, "code", "py")
        prompt_files = list_files(root, "prompt", "txt")
        code_line_counts = [count_lines(read_text(p)) for p in code_files]
        prompt_texts = [read_text(p) for p in prompt_files]
        char_counts = [len(t) for t in prompt_texts]
        word_counts = [len(tokenize_words(t)) for t in prompt_texts]
        sent_counts = [count_sentences(t) for t in prompt_texts]
        return {
            "code": describe(code_line_counts),
            "chars": describe(char_counts),
            "words": describe(word_counts),
            "sents": describe(sent_counts),
        }

    orig_stats = collect(original) if original.exists() else None
    sani_stats = collect(sanitized) if sanitized.exists() else None

    # Raw + per-dataset tables (retain previous outputs if present)
    if orig_stats is not None:
        analyse_dataset("original", original)
    else:
        print("Dataset: original (missing)\n")
    if sani_stats is not None:
        analyse_dataset("sanitized", sanitized)
    else:
        print("Dataset: sanitized (missing)\n")

    # Comparison tables: four tables for code lines, prompt chars, words, sentences
    if orig_stats is not None and sani_stats is not None:
        compare_stats("original", orig_stats["code"], "sanitized", sani_stats["code"], "Code lines")
        compare_stats("original", orig_stats["chars"], "sanitized", sani_stats["chars"], "Prompt characters")
        compare_stats("original", orig_stats["words"], "sanitized", sani_stats["words"], "Prompt words")
        compare_stats("original", orig_stats["sents"], "sanitized", sani_stats["sents"], "Prompt sentences")


if __name__ == "__main__":
    main()
