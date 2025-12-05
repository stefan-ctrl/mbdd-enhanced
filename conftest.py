import json
from pathlib import Path


def pytest_configure(config):
    # Ensure reports directory exists; also ensure parent directory for junitxml
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    junitxml = getattr(config.option, "junitxml", None)
    if junitxml:
        Path(junitxml).parent.mkdir(parents=True, exist_ok=True)


def pytest_terminal_summary(terminalreporter, exitstatus):
    """Write a machine-readable summary JSON and a concise text report."""
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    outcomes = [
        "passed",
        "failed",
        "error",
        "skipped",
        "xfailed",
        "xpassed",
    ]

    stats = {}
    for outcome in outcomes:
        items = terminalreporter.stats.get(outcome, []) or []
        stats[outcome] = {
            "count": len(items),
            "items": [getattr(r, "nodeid", str(r)) for r in items],
        }

    total = sum(v["count"] for v in stats.values())

    summary = {
        "exitstatus": exitstatus,
        "total": total,
        "stats": stats,
    }

    (reports_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    lines = [f"Exit status: {exitstatus}", f"Total: {total}"]
    for outcome in outcomes:
        lines.append(f"{outcome}: {stats[outcome]['count']}")
    (reports_dir / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
