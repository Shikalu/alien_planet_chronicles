#!/usr/bin/env python3
"""Audit prose-style risks in the manuscript without changing source text.

The metrics are deliberately diagnostic rather than prescriptive. A high score
identifies chapters that deserve a close read; it is not proof that prose is bad.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DIR = ROOT / "异星录/正文/第一卷_热海坠城"
HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")

PATTERNS = {
    "simile": r"(?:像|仿佛|似乎)",
    "sudden": r"(?:突然|骤然|猛地)",
    "negation_explanation": r"不是[^。！？\n]{1,30}而是",
    "silence": r"(?:沉默|没有说话|没有回答|没有回应)",
    "generic_action": r"(?:点了点头|摇了摇头|皱了皱眉|咬了咬牙|深吸了一口气)",
    "gaze": r"(?:眼睛|目光|眼神)",
    "abstract_emotion": r"(?:感到|意识到|明白了|有些害怕|十分紧张|非常愤怒|心情沉重)",
}


def count_text(text: str) -> dict[str, int]:
    body = "\n".join(
        line for line in text.splitlines() if line.strip() and not line.lstrip().startswith("#")
    )
    paragraphs = [line.strip() for line in body.splitlines() if line.strip()]
    sentences = [s for s in re.split(r"(?<=[。！？])", body) if s.strip()]
    clean = re.sub(r"\s", "", body)
    counts = {name: len(re.findall(rx, body)) for name, rx in PATTERNS.items()}
    dialogue_marks = len(re.findall(r"[“”]", body)) // 2
    avg_sentence = round(len(HAN.findall(body)) / max(1, len(sentences)), 1)
    avg_paragraph = round(len(HAN.findall(body)) / max(1, len(paragraphs)), 1)
    return {
        "han": len(HAN.findall(body)),
        "nonspace": len(clean),
        "paragraphs": len(paragraphs),
        "sentences": len(sentences),
        "dialogue_lines": dialogue_marks,
        "dialogue_ratio": round(dialogue_marks / max(1, len(paragraphs)), 3),
        "avg_sentence_han": avg_sentence,
        "avg_paragraph_han": avg_paragraph,
        **counts,
    }


def risk_score(metrics: dict[str, int | float]) -> float:
    return round(
        metrics["simile"]
        + metrics["sudden"] * 1.2
        + metrics["negation_explanation"] * 1.5
        + metrics["silence"] * 1.2
        + metrics["generic_action"] * 1.2
        + metrics["gaze"] * 0.5
        + metrics["abstract_emotion"] * 1.3,
        1,
    )


def audit(directory: Path) -> list[dict[str, int | float | str]]:
    rows = []
    for path in sorted(directory.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        metrics = count_text(text)
        rows.append({"file": path.name, **metrics, "risk_score": risk_score(metrics)})
    return rows


def print_report(rows: list[dict[str, int | float | str]]) -> None:
    print(
        "文件\t汉字\t段数\t对白段比\t均句长\t均段长\t比喻\t突然\t不是而是\t沉默\t通用动作\t抽象情绪\t风险分"
    )
    for row in rows:
        print(
            f"{row['file']}\t{row['han']}\t{row['paragraphs']}\t{row['dialogue_ratio']}\t"
            f"{row['avg_sentence_han']}\t{row['avg_paragraph_han']}\t{row['simile']}\t"
            f"{row['sudden']}\t{row['negation_explanation']}\t{row['silence']}\t"
            f"{row['generic_action']}\t{row['abstract_emotion']}\t{row['risk_score']}"
        )

    print("\n高风险章节")
    for row in sorted(rows, key=lambda item: float(item["risk_score"]), reverse=True)[:15]:
        print(f"{row['risk_score']:>5}  {row['file']}")

    print("\n对白占比最低")
    for row in sorted(rows, key=lambda item: float(item["dialogue_ratio"]))[:10]:
        print(f"{row['dialogue_ratio']:>5}  {row['file']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--json", type=Path, help="write full metrics as JSON")
    args = parser.parse_args()
    rows = audit(args.directory)
    print_report(rows)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
