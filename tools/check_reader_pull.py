#!/usr/bin/env python3
"""核验吸引力审读的覆盖、正文证据及版本；不自动判断作品是否吸引人。"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_CHECKS = ('opening_pressure', 'protagonist_choice', 'visible_change', 'emotional_payoff', 'next_question')
BATCH_CHECKS = ('promise_payoff', 'progressive_stakes')
OPENING_CHECKS = ('first_page_hook', 'protagonist_stakes', 'three_chapter_promise', 'exposition_cost')


def first_page(text):
    """Return the actual body through its first 100 Han characters, ignoring headings."""
    body = '\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('#')).strip()
    matches = list(re.finditer(r'[\u3400-\u4dbf\u4e00-\u9fff]', body))
    return body[:matches[99].end()] if len(matches) >= 100 else body


def digest_rows(rows):
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def within(root, name):
    if not isinstance(name, str) or not name or Path(name).is_absolute():
        raise ValueError('审读路径必须是项目相对路径')
    p = (root / name).resolve()
    if not p.is_relative_to(root.resolve()):
        raise ValueError('审读路径越出项目')
    return p


def validate(root, record, expected_rows=None, require_pass=True):
    root = root.resolve()
    errors, notes, rows, texts = [], [], [], {}
    if record.get('schema_version') != 1 or record.get('kind') not in ('review', 'diagnostic'):
        raise ValueError('吸引力审读记录版本/类型无效')
    cfg = json.loads((root / 'harness/project.json').read_text())
    prologues = sorted((root / cfg['volumes'][0]['prose']).glob('楔子*.md'))
    if len(prologues) > 1:
        errors.append('存在多个楔子入口，须先确定真实阅读顺序')
    for item in record.get('manuscripts', []):
        n, name = item['chapter'], item['path']
        if type(n) is not int or not 0 <= n <= 800 or n in texts:
            errors.append('正文编号无效或重复（0代表真实前置楔子）')
            continue
        p = within(root, name)
        match = re.match(r'^第(\d+)章_', p.name)
        if n and (not match or int(match[1]) != n):
            errors.append(f'审读章号与正文文件名不符：{name}')
        if n == 0 and p not in [x.resolve() for x in prologues]:
            errors.append('楔子必须指向实际发布的阅读入口')
        # Closed batches can remove work copies; the published identical bytes remain evidence.
        if not p.is_file() and n:
            p = within(root, cfg['volumes'][(n - 1) // 100]['prose']) / Path(name).name
        if not p.is_file():
            errors.append(f'审读正文缺失：{name}')
            continue
        sha = hashlib.sha256(p.read_bytes()).hexdigest()
        if sha != item['sha256']:
            errors.append(f'审读正文已变化：{name}')
        rows.append(dict(chapter=n, path=name, sha256=sha))
        texts[n] = p.read_text(encoding='utf-8')
    if not rows or record.get('source_digest') != digest_rows(rows):
        errors.append('吸引力审读未绑定完整实际稿件摘要')
    if expected_rows is not None:
        actual = {(x['chapter'], x['sha256']) for x in rows}
        if not {(x['chapter'], x['sha256']) for x in expected_rows} <= actual:
            errors.append('吸引力审读未完整覆盖本次终稿')
    seen = set()
    for check in record.get('checks', []):
        criterion, n = check.get('criterion'), check.get('chapter')
        key = criterion, n
        if key in seen:
            errors.append(f'吸引力检查项重复：{criterion}/{n}')
        seen.add(key)
        if criterion not in CHAPTER_CHECKS + BATCH_CHECKS + OPENING_CHECKS:
            errors.append(f'未知吸引力检查项：{criterion}')
        if n not in texts or not check.get('quote') or check['quote'] not in texts.get(n, ''):
            errors.append(f'吸引力判断缺实际正文原句：{criterion}/{n}')
        if not check.get('reason') or check.get('verdict') not in ('pass', 'needs_revision'):
            errors.append(f'吸引力判断缺理由或结论：{criterion}/{n}')
        if check.get('verdict') == 'needs_revision' and not check.get('action'):
            errors.append(f'未通过项缺修改方向：{criterion}/{n}')
    required = {(c, n) for n in texts if n > 0 for c in CHAPTER_CHECKS}
    # Batch checks cite a concrete chapter but need only one check per criterion.
    missing = [f'{c}/{n}' for c, n in sorted(required - seen)]
    missing += [c for c in BATCH_CHECKS if not any(x[0] == c for x in seen)]
    if record.get('profile') not in ('opening', 'serial'):
        errors.append('吸引力审读范围须为opening或serial')
    if record.get('profile') == 'opening' or any(0 <= n <= 3 for n in texts):
        missing += [c for c in OPENING_CHECKS if not any(x[0] == c for x in seen)]
        if prologues and 0 not in texts:
            missing.append('真实阅读入口楔子')
        if not {1, 2, 3} <= set(texts):
            missing.append('黄金前三章完整正文')
        entry = 0 if prologues else 1
        for item in record.get('checks', []):
            if item.get('criterion') == 'first_page_hook' and (item.get('chapter') != entry
                    or not item.get('quote') or item['quote'] not in first_page(texts.get(entry, ''))):
                errors.append('第一页抓手必须引用真实入口前100纯汉字，不能用后段高潮替代')
    eligible = (record.get('kind') == 'review' and record.get('independent') is True
                and record.get('body_first') is True and record.get('reviewer')
                and record.get('reviewer') != record.get('writer') and record.get('writer'))
    if require_pass:
        if missing:
            errors.append('吸引力审读覆盖不完整：' + ', '.join(missing))
        if not eligible:
            errors.append('吸引力验收缺真实独立首读记录；作者诊断不能自签通过')
        if record.get('verdict') != 'pass' or any(x.get('verdict') != 'pass' for x in record.get('checks', [])):
            errors.append('存在未通过的开篇/追读审读项')
    else:
        notes.extend(missing)
    passed = not errors and not missing and eligible and record.get('verdict') == 'pass' and all(x.get('verdict') == 'pass' for x in record.get('checks', []))
    return dict(errors=errors, incomplete_checks=notes, reader_review_passed=bool(passed),
                verdict=record.get('verdict'), chapters=[n for n in texts if n > 0],
                includes_prologue=0 in texts, profile=record.get('profile'))


def coverage(root):
    passed, records, pending = set(), [], []
    for p in sorted((root / 'harness/reader-reviews').glob('*.json')):
        item = json.loads(p.read_text())
        if item.get('kind') not in ('review', 'diagnostic'):
            continue
        result = validate(root, item, require_pass=True)
        if result['reader_review_passed']:
            passed.update(result['chapters'])
            records.append(p.relative_to(root).as_posix())
        else:
            pending.append(p.relative_to(root).as_posix())
    last = json.loads((root / 'harness/status.json').read_text())['last_published_chapter']
    actual = sorted(n for n in passed if n <= last)
    return dict(published=last, reader_review_passed_chapters=actual, passed_count=len(actual),
                unreviewed_or_not_passed_count=last-len(actual), passed_records=records,
                diagnostic_or_not_passed_records=pending)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--record')
    ap.add_argument('--coverage', action='store_true')
    ap.add_argument('--require-complete', action='store_true')
    args = ap.parse_args()
    try:
        if args.coverage:
            result = coverage(ROOT)
            failed = args.require_complete and result['unreviewed_or_not_passed_count'] > 0
        elif args.record:
            item = json.loads(within(ROOT, args.record).read_text())
            result = validate(ROOT, item, require_pass=item.get('kind') != 'diagnostic')
            failed = not result['reader_review_passed']
        else:
            ap.error('指定--record或--coverage')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if failed else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'ERROR {exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
