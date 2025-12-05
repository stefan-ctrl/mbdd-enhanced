from pathlib import Path
import re
import statistics
from typing import Optional, Tuple

# Optional plotting support
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:  # matplotlib not installed or headless issues
    plt = None  # type: ignore


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
    # Count natural language words (letters only, keep simple contractions like don't)
    # This avoids counting numbers/underscores and aligns better with word metrics.
    return re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", text)


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


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def plot_stat_bars(title: str, stats: dict, out_path: Path):
    if plt is None:
        return
    labels = ["Min", "Median", "Average", "Max"]
    values = [stats["min"], stats["median"], stats["avg"], stats["max"]]
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, values, color="white", edgecolor="black")
    # Apply distinct hatch patterns for monochrome clarity
    hatches = ["///", "\\\\\\", "xxx", "---"]
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    ax.set_title(title)
    ax.set_ylabel("Value")
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_hist(title: str, values: list[int], out_path: Path, xlabel: str, show_percentiles: bool = False):
    if plt is None or not values:
        return
    fig, ax = plt.subplots(figsize=(6, 4))
    n, bins, patches = ax.hist(
        values, bins=30, color="0.85", edgecolor="0.25", alpha=1.0
    )

    # Compute statistics
    avg = sum(values) / len(values)
    med = statistics.median(values)
    p75 = statistics.quantiles(values, n=4, method="inclusive")[2] if len(values) > 0 else 0

    # Ensure headroom for markers and top annotations
    y_max = float(max(n)) if len(n) else 1.0
    ax.set_ylim(0, y_max * 1.2)

    # Highlight average and median as monochrome markers with distinct styles
    ax.axvline(avg, color="black", linestyle="--", linewidth=1, alpha=0.7)
    ax.axvline(med, color="black", linestyle=":", linewidth=1, alpha=0.7)
    ax.scatter([avg], [y_max * 1.05], s=50, zorder=3,
               marker="o", facecolors="white", edgecolors="black", linewidths=1.5,
               label=f"Avg {avg:.2f}")
    ax.scatter([med], [y_max * 1.1], s=50, zorder=3,
               marker="D", facecolors="black", edgecolors="black",
               label=f"Median {med}")

    # Optional percentile markers and percentage annotations
    if show_percentiles:
        for x in [p75]:
            ax.axvline(x, color="black", linestyle="-.", linewidth=1, alpha=0.7)
        # Percent of values less-or-equal than each percentile value (read left-to-right)
        def pct_le(th: float) -> float:
            if not values:
                return 0.0
            return round(100.0 * sum(1 for v in values if v <= th) / len(values), 1)
        # Place small text labels slightly above histogram
        ax.text(p75, y_max * 1.14, f"<=P75: {pct_le(p75)}%", ha="center", va="bottom", fontsize=8)

    ax.set_title(title)
    ax.set_ylabel("Frequency")
    ax.set_xlabel(xlabel)
    ax.grid(axis="y", linestyle=":", alpha=0.5)
    ax.legend(frameon=False, loc="upper right")
    # Add extra top buffer
    fig.tight_layout()
    fig.subplots_adjust(top=0.88)
    fig.savefig(out_path)
    plt.close(fig)


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

    # Plots for both datasets (if present)
    if sanitized.exists():
        # Recompute raw values for histograms
        code_files = list_files(sanitized, "code", "py")
        prompt_files = list_files(sanitized, "prompt", "txt")
        code_line_counts = [count_lines(read_text(p)) for p in code_files]
        prompt_texts = [read_text(p) for p in prompt_files]
        char_counts = [len(t) for t in prompt_texts]
        word_counts = [len(tokenize_words(t)) for t in prompt_texts]
        sent_counts = [count_sentences(t) for t in prompt_texts]

        plots_dir = Path(__file__).parent / "plots"
        ensure_dir(plots_dir)

        if sani_stats is None:
            sani_stats = {
                "code": describe(code_line_counts),
                "chars": describe(char_counts),
                "words": describe(word_counts),
                "sents": describe(sent_counts),
            }

        # Bar charts of stats (titles omit dataset label; filenames indicate sanitized)
        plot_stat_bars("Code Lines (Stats)", sani_stats["code"], plots_dir / "sanitized_code_lines_stats.png")
        plot_stat_bars("Prompt Characters (Stats)", sani_stats["chars"], plots_dir / "sanitized_prompt_characters_stats.png")
        plot_stat_bars("Prompt Words (Stats)", sani_stats["words"], plots_dir / "sanitized_prompt_words_stats.png")
        plot_stat_bars("Prompt Sentences (Stats)", sani_stats["sents"], plots_dir / "sanitized_prompt_sentences_stats.png")

        # Histograms of distributions (titles omit dataset label)
        plot_hist("Code Lines (Histogram)", code_line_counts, plots_dir / "sanitized_code_lines_hist.png", xlabel="Lines per file", show_percentiles=True)
        plot_hist("Prompt Characters (Histogram)", char_counts, plots_dir / "sanitized_prompt_characters_hist.png", xlabel="Characters per prompt", show_percentiles=True)
        plot_hist("Prompt Words (Histogram)", word_counts, plots_dir / "sanitized_prompt_words_hist.png", xlabel="Words per prompt")
        plot_hist("Prompt Sentences (Histogram)", sent_counts, plots_dir / "sanitized_prompt_sentences_hist.png", xlabel="Sentences per prompt")
        # Characters per code
        code_files = list_files(sanitized, "code", "py")
        code_texts = [read_text(p) for p in code_files]
        code_char_counts = [len(t) for t in code_texts]
        plot_hist("Characters per Code (Histogram)", code_char_counts, plots_dir / "sanitized_characters_per_code_hist.png", xlabel="Characters per code file")

        if plt is None:
            print("matplotlib not installed; skipped plot generation.")
        else:
            print(f"Saved plots to {plots_dir}")

    if original.exists():
        # Recompute raw values for histograms (original)
        code_files_o = list_files(original, "code", "py")
        prompt_files_o = list_files(original, "prompt", "txt")
        code_line_counts_o = [count_lines(read_text(p)) for p in code_files_o]
        prompt_texts_o = [read_text(p) for p in prompt_files_o]
        char_counts_o = [len(t) for t in prompt_texts_o]
        word_counts_o = [len(tokenize_words(t)) for t in prompt_texts_o]
        sent_counts_o = [count_sentences(t) for t in prompt_texts_o]

        plots_dir = Path(__file__).parent / "plots"
        ensure_dir(plots_dir)

        if orig_stats is None:
            orig_stats = {
                "code": describe(code_line_counts_o),
                "chars": describe(char_counts_o),
                "words": describe(word_counts_o),
                "sents": describe(sent_counts_o),
            }

        # Bar charts of stats (titles omit dataset label; filenames indicate original)
        plot_stat_bars("Code Lines (Stats)", orig_stats["code"], plots_dir / "original_code_lines_stats.png")
        plot_stat_bars("Prompt Characters (Stats)", orig_stats["chars"], plots_dir / "original_prompt_characters_stats.png")
        plot_stat_bars("Prompt Words (Stats)", orig_stats["words"], plots_dir / "original_prompt_words_stats.png")
        plot_stat_bars("Prompt Sentences (Stats)", orig_stats["sents"], plots_dir / "original_prompt_sentences_stats.png")

        # Histograms of distributions (titles omit dataset label)
        plot_hist("Code Lines (Histogram)", code_line_counts_o, plots_dir / "original_code_lines_hist.png", xlabel="Lines per file", show_percentiles=True)
        plot_hist("Prompt Characters (Histogram)", char_counts_o, plots_dir / "original_prompt_characters_hist.png", xlabel="Characters per prompt", show_percentiles=True)
        plot_hist("Prompt Words (Histogram)", word_counts_o, plots_dir / "original_prompt_words_hist.png", xlabel="Words per prompt")
        plot_hist("Prompt Sentences (Histogram)", sent_counts_o, plots_dir / "original_prompt_sentences_hist.png", xlabel="Sentences per prompt")
        # Characters per code
        code_files_o = list_files(original, "code", "py")
        code_texts_o = [read_text(p) for p in code_files_o]
        code_char_counts_o = [len(t) for t in code_texts_o]
        plot_hist("Characters per Code (Histogram)", code_char_counts_o, plots_dir / "original_characters_per_code_hist.png", xlabel="Characters per code file")

        if plt is None:
            print("matplotlib not installed; skipped plot generation.")
        else:
            print(f"Saved plots to {plots_dir}")


if __name__ == "__main__":
    main()
