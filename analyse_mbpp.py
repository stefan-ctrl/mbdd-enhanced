from pathlib import Path
import json
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


_tiktoken_encoding = None


def _get_encoding():
    global _tiktoken_encoding
    if _tiktoken_encoding is None:
        import tiktoken
        _tiktoken_encoding = tiktoken.get_encoding("cl100k_base")
    return _tiktoken_encoding


def count_tokens(text: str) -> int:
    if not text:
        return 0
    return len(_get_encoding().encode(text))


def count_sentences(text: str) -> int:
    # Split on ., !, ? considering consecutive punctuation as one separator
    if not text:
        return 0
    parts = re.split(r"[.!?]+", text)
    # Count non-empty segments
    return sum(1 for seg in parts if seg.strip())


def describe(values: list[int]) -> dict:
    if not values:
        return {"avg": 0, "median": 0, "min": 0, "max": 0, "count": 0,
                "std": 0, "q1": 0, "q3": 0, "iqr": 0,
                "whisker_low": 0, "whisker_high": 0, "outliers": []}
    avg = round(sum(values) / len(values), 2)
    med = statistics.median(values)
    std = round(statistics.stdev(values), 2) if len(values) > 1 else 0
    q1, q2, q3 = statistics.quantiles(values, n=4, method="inclusive") if len(values) >= 2 else (med, med, med)
    iqr = round(q3 - q1, 2)
    whisker_low = q1 - 1.5 * iqr
    whisker_high = q3 + 1.5 * iqr
    # Clamp whiskers to actual data range
    actual_low = min(v for v in values if v >= whisker_low) if any(v >= whisker_low for v in values) else min(values)
    actual_high = max(v for v in values if v <= whisker_high) if any(v <= whisker_high for v in values) else max(values)
    outliers = sorted(v for v in values if v < whisker_low or v > whisker_high)
    return {
        "avg": avg,
        "median": med,
        "min": min(values),
        "max": max(values),
        "count": len(values),
        "std": std,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "whisker_low": actual_low,
        "whisker_high": actual_high,
        "outliers": outliers,
    }


def analyse_dataset(label: str, root: Path):
    code_files = list_files(root, "code", "py")
    prompt_files = list_files(root, "prompt", "txt")

    code_texts = [read_text(p) for p in code_files]
    code_line_counts = [count_lines(t) for t in code_texts]
    code_char_counts = [len(t) for t in code_texts]
    code_token_counts = [count_tokens(t) for t in code_texts]
    code_chars_per_line = []
    for t in code_texts:
        lines = t.rstrip("\n").split("\n") if t else []
        code_chars_per_line.extend([len(line) for line in lines])

    prompt_texts = [read_text(p) for p in prompt_files]
    prompt_char_counts = [len(t) for t in prompt_texts]
    prompt_word_counts = [count_tokens(t) for t in prompt_texts]
    prompt_sentence_counts = [count_sentences(t) for t in prompt_texts]

    # Raw output
    print(f"Dataset: {label}")
    print("- Code lines:", describe(code_line_counts))
    print("- Code characters:", describe(code_char_counts))
    print("- Code tokens:", describe(code_token_counts))
    print("- Code characters per line:", describe(code_chars_per_line))
    print("- Prompt characters:", describe(prompt_char_counts))
    print("- Prompt tokens:", describe(prompt_word_counts))
    print("- Prompt sentences:", describe(prompt_sentence_counts))
    print()

    # Markdown table output
    code_line_stats = describe(code_line_counts)
    code_char_stats = describe(code_char_counts)
    code_token_stats = describe(code_token_counts)
    code_cpl_stats = describe(code_chars_per_line)
    char_stats = describe(prompt_char_counts)
    word_stats = describe(prompt_word_counts)
    sent_stats = describe(prompt_sentence_counts)

    print(f"## {label} Summary (Markdown Table)")
    print("| Metric | Count | Min | Median | Average | Max |")
    print("|---|---:|---:|---:|---:|---:|")
    print(
        f"| Code lines | {code_line_stats['count']} | {code_line_stats['min']} | {code_line_stats['median']} | {code_line_stats['avg']} | {code_line_stats['max']} |"
    )
    print(
        f"| Code characters | {code_char_stats['count']} | {code_char_stats['min']} | {code_char_stats['median']} | {code_char_stats['avg']} | {code_char_stats['max']} |"
    )
    print(
        f"| Code tokens | {code_token_stats['count']} | {code_token_stats['min']} | {code_token_stats['median']} | {code_token_stats['avg']} | {code_token_stats['max']} |"
    )
    print(
        f"| Code chars/line | {code_cpl_stats['count']} | {code_cpl_stats['min']} | {code_cpl_stats['median']} | {code_cpl_stats['avg']} | {code_cpl_stats['max']} |"
    )
    print(
        f"| Prompt characters | {char_stats['count']} | {char_stats['min']} | {char_stats['median']} | {char_stats['avg']} | {char_stats['max']} |"
    )
    print(
        f"| Prompt tokens | {word_stats['count']} | {word_stats['min']} | {word_stats['median']} | {word_stats['avg']} | {word_stats['max']} |"
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
    print(f"| Q1 | {stats_left['q1']} | {stats_right['q1']} |")
    print(f"| Median | {stats_left['median']} | {stats_right['median']} |")
    print(f"| Average | {stats_left['avg']} | {stats_right['avg']} |")
    print(f"| Q3 | {stats_left['q3']} | {stats_right['q3']} |")
    print(f"| Max | {stats_left['max']} | {stats_right['max']} |")
    print(f"| Std | {stats_left['std']} | {stats_right['std']} |")
    print(f"| IQR | {stats_left['iqr']} | {stats_right['iqr']} |")
    print(f"| Whisker Low | {stats_left['whisker_low']} | {stats_right['whisker_low']} |")
    print(f"| Whisker High | {stats_left['whisker_high']} | {stats_right['whisker_high']} |")
    print(f"| Outliers | {len(stats_left['outliers'])} | {len(stats_right['outliers'])} |")
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


def export_json(data: dict, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main():
    base = Path(__file__).parent
    sanitized = base / "sanitized"
    original = base / "original"

    # Collect stats for both datasets
    def collect(root: Path):
        code_files = list_files(root, "code", "py")
        prompt_files = list_files(root, "prompt", "txt")
        code_texts = [read_text(p) for p in code_files]
        code_line_counts = [count_lines(t) for t in code_texts]
        code_char_counts = [len(t) for t in code_texts]
        code_token_counts = [count_tokens(t) for t in code_texts]
        code_chars_per_line = []
        for t in code_texts:
            lines = t.rstrip("\n").split("\n") if t else []
            code_chars_per_line.extend([len(line) for line in lines])
        prompt_texts = [read_text(p) for p in prompt_files]
        char_counts = [len(t) for t in prompt_texts]
        word_counts = [count_tokens(t) for t in prompt_texts]
        sent_counts = [count_sentences(t) for t in prompt_texts]
        return {
            "code_lines": describe(code_line_counts),
            "code_chars": describe(code_char_counts),
            "code_tokens": describe(code_token_counts),
            "code_cpl": describe(code_chars_per_line),
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
        compare_stats("original", orig_stats["code_lines"], "sanitized", sani_stats["code_lines"], "Code lines")
        compare_stats("original", orig_stats["code_chars"], "sanitized", sani_stats["code_chars"], "Code characters")
        compare_stats("original", orig_stats["code_tokens"], "sanitized", sani_stats["code_tokens"], "Code tokens")
        compare_stats("original", orig_stats["code_cpl"], "sanitized", sani_stats["code_cpl"], "Code characters per line")
        compare_stats("original", orig_stats["chars"], "sanitized", sani_stats["chars"], "Prompt characters")
        compare_stats("original", orig_stats["words"], "sanitized", sani_stats["words"], "Prompt tokens")
        compare_stats("original", orig_stats["sents"], "sanitized", sani_stats["sents"], "Prompt sentences")

    # Plots for both datasets (if present)
    if sanitized.exists():
        # Recompute raw values for histograms
        code_files = list_files(sanitized, "code", "py")
        prompt_files = list_files(sanitized, "prompt", "txt")
        code_line_counts = [count_lines(read_text(p)) for p in code_files]
        prompt_texts = [read_text(p) for p in prompt_files]
        char_counts = [len(t) for t in prompt_texts]
        word_counts = [count_tokens(t) for t in prompt_texts]
        sent_counts = [count_sentences(t) for t in prompt_texts]

        plots_dir = Path(__file__).parent / "plots"
        ensure_dir(plots_dir)

        if sani_stats is None:
            code_texts = [read_text(p) for p in code_files]
            code_char_counts = [len(t) for t in code_texts]
            code_token_counts = [count_tokens(t) for t in code_texts]
            code_chars_per_line = []
            for t in code_texts:
                lines = t.rstrip("\n").split("\n") if t else []
                code_chars_per_line.extend([len(line) for line in lines])
            sani_stats = {
                "code_lines": describe(code_line_counts),
                "code_chars": describe(code_char_counts),
                "code_tokens": describe(code_token_counts),
                "code_cpl": describe(code_chars_per_line),
                "chars": describe(char_counts),
                "words": describe(word_counts),
                "sents": describe(sent_counts),
            }

        # Bar charts of stats (titles omit dataset label; filenames indicate sanitized)
        plot_stat_bars("Code Lines (Stats)", sani_stats["code_lines"], plots_dir / "sanitized_code_lines_stats.png")
        plot_stat_bars("Prompt Characters (Stats)", sani_stats["chars"], plots_dir / "sanitized_prompt_characters_stats.png")
        plot_stat_bars("Prompt Tokens (Stats)", sani_stats["words"], plots_dir / "sanitized_prompt_tokens_stats.png")
        plot_stat_bars("Prompt Sentences (Stats)", sani_stats["sents"], plots_dir / "sanitized_prompt_sentences_stats.png")

        # Histograms of distributions (titles omit dataset label)
        plot_hist("Code Lines (Histogram)", code_line_counts, plots_dir / "sanitized_code_lines_hist.png", xlabel="Lines per file", show_percentiles=True)
        plot_hist("Prompt Characters (Histogram)", char_counts, plots_dir / "sanitized_prompt_characters_hist.png", xlabel="Characters per prompt", show_percentiles=True)
        plot_hist("Prompt Tokens (Histogram)", word_counts, plots_dir / "sanitized_prompt_tokens_hist.png", xlabel="Tokens per prompt")
        plot_hist("Prompt Sentences (Histogram)", sent_counts, plots_dir / "sanitized_prompt_sentences_hist.png", xlabel="Sentences per prompt")
        # Characters per code
        code_files = list_files(sanitized, "code", "py")
        code_texts = [read_text(p) for p in code_files]
        code_char_counts = [len(t) for t in code_texts]
        plot_hist("Characters per Code (Histogram)", code_char_counts, plots_dir / "sanitized_characters_per_code_hist.png", xlabel="Characters per code file")
        # Characters per line in code
        code_chars_per_line = []
        for text in code_texts:
            lines = text.rstrip("\n").split("\n") if text else []
            code_chars_per_line.extend([len(line) for line in lines])
        plot_hist("Characters per Line (Histogram)", code_chars_per_line, plots_dir / "sanitized_characters_per_line_hist.png", xlabel="Characters per line")

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
        word_counts_o = [count_tokens(t) for t in prompt_texts_o]
        sent_counts_o = [count_sentences(t) for t in prompt_texts_o]

        plots_dir = Path(__file__).parent / "plots"
        ensure_dir(plots_dir)

        if orig_stats is None:
            code_texts_o = [read_text(p) for p in code_files_o]
            code_char_counts_o = [len(t) for t in code_texts_o]
            code_token_counts_o = [count_tokens(t) for t in code_texts_o]
            code_chars_per_line_o = []
            for t in code_texts_o:
                lines = t.rstrip("\n").split("\n") if t else []
                code_chars_per_line_o.extend([len(line) for line in lines])
            orig_stats = {
                "code_lines": describe(code_line_counts_o),
                "code_chars": describe(code_char_counts_o),
                "code_tokens": describe(code_token_counts_o),
                "code_cpl": describe(code_chars_per_line_o),
                "chars": describe(char_counts_o),
                "words": describe(word_counts_o),
                "sents": describe(sent_counts_o),
            }

        # Bar charts of stats (titles omit dataset label; filenames indicate original)
        plot_stat_bars("Code Lines (Stats)", orig_stats["code_lines"], plots_dir / "original_code_lines_stats.png")
        plot_stat_bars("Prompt Characters (Stats)", orig_stats["chars"], plots_dir / "original_prompt_characters_stats.png")
        plot_stat_bars("Prompt Tokens (Stats)", orig_stats["words"], plots_dir / "original_prompt_tokens_stats.png")
        plot_stat_bars("Prompt Sentences (Stats)", orig_stats["sents"], plots_dir / "original_prompt_sentences_stats.png")

        # Histograms of distributions (titles omit dataset label)
        plot_hist("Code Lines (Histogram)", code_line_counts_o, plots_dir / "original_code_lines_hist.png", xlabel="Lines per file", show_percentiles=True)
        plot_hist("Prompt Characters (Histogram)", char_counts_o, plots_dir / "original_prompt_characters_hist.png", xlabel="Characters per prompt", show_percentiles=True)
        plot_hist("Prompt Tokens (Histogram)", word_counts_o, plots_dir / "original_prompt_tokens_hist.png", xlabel="Tokens per prompt")
        plot_hist("Prompt Sentences (Histogram)", sent_counts_o, plots_dir / "original_prompt_sentences_hist.png", xlabel="Sentences per prompt")
        # Characters per code
        code_files_o = list_files(original, "code", "py")
        code_texts_o = [read_text(p) for p in code_files_o]
        code_char_counts_o = [len(t) for t in code_texts_o]
        plot_hist("Characters per Code (Histogram)", code_char_counts_o, plots_dir / "original_characters_per_code_hist.png", xlabel="Characters per code file")
        # Characters per line in code
        code_chars_per_line_o = []
        for text in code_texts_o:
            lines = text.rstrip("\n").split("\n") if text else []
            code_chars_per_line_o.extend([len(line) for line in lines])
        plot_hist("Characters per Line (Histogram)", code_chars_per_line_o, plots_dir / "original_characters_per_line_hist.png", xlabel="Characters per line")

        if plt is None:
            print("matplotlib not installed; skipped plot generation.")
        else:
            print(f"Saved plots to {plots_dir}")


    # Collect raw per-file values for JSON export
    def collect_raw(root: Path):
        code_files = list_files(root, "code", "py")
        prompt_files = list_files(root, "prompt", "txt")
        code_texts = [read_text(p) for p in code_files]
        prompt_texts = [read_text(p) for p in prompt_files]
        code_line_counts = [count_lines(t) for t in code_texts]
        code_char_counts = [len(t) for t in code_texts]
        code_token_counts = [count_tokens(t) for t in code_texts]
        code_chars_per_line = []
        code_chars_per_line_files = []
        for p, t in zip(code_files, code_texts):
            lines = t.rstrip("\n").split("\n") if t else []
            code_chars_per_line.extend([len(l) for l in lines])
            code_chars_per_line_files.extend([p.stem for _ in lines])
        char_counts = [len(t) for t in prompt_texts]
        token_counts = [count_tokens(t) for t in prompt_texts]
        sent_counts = [count_sentences(t) for t in prompt_texts]

        code_names = [p.stem for p in code_files]
        prompt_names = [p.stem for p in prompt_files]

        raw = {
            "code_lines": code_line_counts,
            "code_characters": code_char_counts,
            "code_tokens": code_token_counts,
            "code_characters_per_line": code_chars_per_line,
            "prompt_characters": char_counts,
            "prompt_tokens": token_counts,
            "prompt_sentences": sent_counts,
        }
        files = {
            "code_lines": code_names,
            "code_characters": code_names,
            "code_tokens": code_names,
            "code_characters_per_line": code_chars_per_line_files,
            "prompt_characters": prompt_names,
            "prompt_tokens": prompt_names,
            "prompt_sentences": prompt_names,
        }
        return raw, files

    def describe_with_files(values, file_names):
        """Like describe() but enriches outliers with file names."""
        stats = describe(values)
        if not values or not file_names or len(values) < 2:
            stats["outliers"] = []
            return stats
        q1 = stats["q1"]
        q3 = stats["q3"]
        iqr = stats["iqr"]
        low_thresh = q1 - 1.5 * iqr
        high_thresh = q3 + 1.5 * iqr
        outlier_details = []
        for v, f in zip(values, file_names):
            if v < low_thresh or v > high_thresh:
                outlier_details.append({"file": f, "value": v})
        stats["outliers"] = sorted(outlier_details, key=lambda x: x["value"])
        return stats

    # Export JSON
    plots_dir = Path(__file__).parent / "plots"
    ensure_dir(plots_dir)

    json_output = {
        "tokenization": {
            "method": "tiktoken",
            "encoding": "cl100k_base",
        },
    }
    if original.exists():
        raw_orig, files_orig = collect_raw(original)
        json_output["original"] = {
            "raw": raw_orig,
            "stats": {k: describe_with_files(v, files_orig[k]) for k, v in raw_orig.items()},
        }
    if sanitized.exists():
        raw_sani, files_sani = collect_raw(sanitized)
        json_output["sanitized"] = {
            "raw": raw_sani,
            "stats": {k: describe_with_files(v, files_sani[k]) for k, v in raw_sani.items()},
        }

    json_path = plots_dir / "analysis.json"
    export_json(json_output, json_path)
    print(f"Exported JSON to {json_path}")


if __name__ == "__main__":
    main()
