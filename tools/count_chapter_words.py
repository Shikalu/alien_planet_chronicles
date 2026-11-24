#!/usr/bin/env python3
"""统计小说正文：不计 Markdown 标题，分别统计汉字与含标点非空字符。"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_DIR = ROOT / '异星录/正文/第一卷_热海坠城'
REPORT_DIR = ROOT / 'harness/reports/word-counts'
HAN = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff]')
CHAPTER = re.compile(r'^第(\d+)章_')


def count_text(text: str) -> tuple[int, int]:
    body = '\n'.join(line for line in text.splitlines()
                     if not re.match(r'^\s*#{1,6}\s', line))
    return len(HAN.findall(body)), len(re.sub(r'\s', '', body))


def audit(directory: Path, start: int, end: int, recursive: bool = False) -> tuple[list[dict], list[str]]:
    found: dict[int, list[Path]] = {}
    for path in (directory.rglob('*.md') if recursive else directory.glob('*.md')):
        match = CHAPTER.match(path.name)
        if match and start <= int(match[1]) <= end:
            found.setdefault(int(match[1]), []).append(path)
    rows, errors = [], []
    for n in range(start, end + 1):
        paths = found.get(n, [])
        if len(paths) != 1:
            errors.append(f'第{n:03}章：' + ('缺失' if not paths else '重复文件'))
            continue
        path = paths[0]
        han, nonspace = count_text(path.read_text(encoding='utf-8'))
        try:
            name = str(path.relative_to(ROOT))
        except ValueError:
            name = str(path)
        rows.append(dict(chapter=n, path=name, han=han, nonspace=nonspace))
    return rows, errors


def write_report(rows: list[dict], errors: list[str], args: argparse.Namespace) -> None:
    baseline_path = REPORT_DIR / '初始字数基线.json'
    baseline = {r['chapter']: r for r in json.loads(baseline_path.read_text())} if baseline_path.exists() else {}
    selected_before = [baseline[r['chapter']] for r in rows if r['chapter'] in baseline]
    short = [r for r in rows if r['han'] < args.minimum]
    long = [r for r in rows if r['han'] > args.maximum]
    total = sum(r['han'] for r in rows)
    before = sum(r['han'] for r in selected_before)
    passed = not errors and not short and not long
    lines = [f'# 第{args.start:03}—{args.end:03}章字数核查', '',
             '## 统计口径', '',
             '- 去掉 Markdown 标题、空白；“正文汉字”另去掉标点、数字与拉丁字母，只计 CJK 扩展A及基本区汉字。',
             '- “含标点非空字符”保留标点、数字等，供与不同平台口径对照。',
             f'- 本轮保守验收区间：每章正文汉字 {args.minimum}—{args.maximum}；不以标点凑满最低长度。',
             '- 字数达标不等于剧情质量验收；读者审读与连续性报告另见本目录。', '',
             '## 结果', '',
             f'- 字数检查：**{"通过" if passed else "未通过"}**。找到唯一正文文件 {len(rows)} 章。',
             f'- 正文汉字合计：**{total:,}**；含标点非空字符合计：**{sum(r["nonspace"] for r in rows):,}**。',
             f'- 区间内 {len(rows)-len(short)-len(long)} 章；不足 {len(short)} 章；超出建议上限 {len(long)} 章。']
    if selected_before:
        lines += [f'- 已有基线覆盖 {len(selected_before)} 章：修订前 {before:,} 汉字，净增 {total-before:,} 汉字。',
                  f'- 修订前不足下限：{sum(r["han"] < args.minimum for r in selected_before)} 章（汉字口径）；'
                  f'{sum(r["nonspace"] < args.minimum for r in selected_before)} 章（含标点口径）。']
    if rows:
        lines += [f'- 最短 {min(r["han"] for r in rows):,} 汉字，最长 {max(r["han"] for r in rows):,} 汉字。']
    lines += [''] + [f'- 错误：{error}' for error in errors]
    lines += ['## 逐章对照', '', '| 章号 | 标题 | 修订前汉字 | 当前汉字 | 净增 | 当前含标点字符 | 字数结果 |',
              '|---:|---|---:|---:|---:|---:|---|']
    for row in rows:
        n = row['chapter']
        old = baseline.get(n, {}).get('han')
        status = '不足' if row['han'] < args.minimum else ('超上限' if row['han'] > args.maximum else '达标')
        title = Path(row['path']).stem.split('_', 1)[1]
        lines.append(f'| {n:03} | {title} | {old if old is not None else "—"} | {row["han"]} | '
                     f'{row["han"]-old if old is not None else "—"} | {row["nonspace"]} | {status} |')
    lines += ['', '## 复跑', '', '```sh',
              f'python3 tools/count_chapter_words.py --start {args.start} --end {args.end} '
              f'--minimum {args.minimum} --maximum {args.maximum} '
              + ('--all-volumes ' if args.all_volumes else '')
              + (f'--directory {str(args.directory)!r} ' if args.directory else '')
              + '--write-report', '```', '',
              '初始基线文件只读保留；复跑仅更新当前字数快照与本报告。', '']
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    prefix = '前100章' if (args.start, args.end) == (1, 100) else f'第{args.start:03}-{args.end:03}章'
    if args.all_volumes:
        prefix = '跨卷_' + prefix
    (REPORT_DIR / f'{prefix}字数验收.md').write_text('\n'.join(lines), encoding='utf-8')
    (REPORT_DIR / f'{prefix}当前字数.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=100)
    parser.add_argument('--minimum', type=int, default=2200)
    parser.add_argument('--maximum', type=int, default=3200)
    parser.add_argument('--write-report', action='store_true')
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--all-volumes', action='store_true', help='递归检查全部已发布卷')
    scope.add_argument('--directory', type=Path, help='明确指定正文目录；默认仍为第一卷')
    args = parser.parse_args()
    if not 1 <= args.start <= args.end or not 0 < args.minimum <= args.maximum:
        parser.error('章号范围和字数区间无效')
    directory = ROOT / '异星录/正文' if args.all_volumes else (args.directory or TEXT_DIR)
    if not directory.is_dir():
        parser.error(f'正文目录不存在：{directory}')
    rows, errors = audit(directory, args.start, args.end, recursive=args.all_volumes)
    short = [r for r in rows if r['han'] < args.minimum]
    long = [r for r in rows if r['han'] > args.maximum]
    print(f'章节 {len(rows)}；汉字 {sum(r["han"] for r in rows):,}；'
          f'达标 {len(rows)-len(short)-len(long)}；不足 {len(short)}；超上限 {len(long)}')
    for row in short + long:
        print(f'  第{row["chapter"]:03}章 {row["han"]} 汉字')
    for error in errors:
        print(error)
    if args.write_report:
        write_report(rows, errors, args)
    return 2 if errors else (1 if short or long else 0)


if __name__ == '__main__':
    raise SystemExit(main())
