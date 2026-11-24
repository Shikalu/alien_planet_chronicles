#!/usr/bin/env python3
"""《异星录》本地批次记录与可复跑门禁；不改写/复制正文。仅依赖标准库。"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

from count_chapter_words import count_text
import check_reader_pull as reader_pull

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = re.compile(r'^第(\d+)章_')
BATCH_ID = re.compile(r'^[A-Za-z][A-Za-z0-9_-]{0,39}$')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe(root: Path, name: str) -> Path:
    if not isinstance(name, str) or not name or Path(name).is_absolute():
        raise ValueError(f'必须使用项目相对路径：{name!r}')
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'路径越出项目：{name}')
    return path


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(value, dict):
        raise ValueError(f'JSON根节点必须是对象：{path.name}')
    return value


def save_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temp, path)


def config(root: Path) -> dict:
    cfg = read_json(root / 'harness/project.json')
    if cfg.get('schema_version') != 1 or cfg.get('planned_chapters') != 800:
        raise ValueError('配置版本或800章规模错误')
    volumes = cfg.get('volumes', [])
    if len(volumes) != 8 or [(v['number'], v['start'], v['end']) for v in volumes] != [
            (i + 1, i * 100 + 1, (i + 1) * 100) for i in range(8)]:
        raise ValueError('八卷范围必须连续覆盖1—800，不能改变既有规划')
    if (cfg.get('minimum_han'), cfg.get('maximum_han')) != (2200, 3200):
        raise ValueError('字数阈值与根规则不一致')
    return cfg


def status(root: Path) -> dict:
    value = read_json(root / 'harness/status.json')
    last = value.get('last_published_chapter')
    if value.get('schema_version') != 1 or type(last) is not int or not 0 <= last <= 800:
        raise ValueError('状态版本/已发布章号无效')
    if last == 800:
        if value.get('next_chapter') is not None or value.get('next_batch') is not None:
            raise ValueError('全书完结后不得登记下一章或批次')
    elif value.get('next_chapter') != last + 1:
        raise ValueError('状态中的下一章未连续')
    if not value.get('last_story_day') or not value.get('evidence'):
        raise ValueError('状态缺故事时间/来源证据')
    return value


def all_hashes(root: Path, base: str) -> dict[str, str]:
    root = root.resolve()
    return {p.relative_to(root).as_posix(): digest(p)
            for p in sorted(safe(root, base).rglob('*.md')) if p.is_file() and p.name not in {'目录.md', 'README.md'}}


def markdown_links(root: Path, files: list[str]) -> list[str]:
    errors = []
    for name in files:
        path = safe(root, name)
        if path.suffix != '.md' or not path.exists():
            continue
        text = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
        for target in re.findall(r'\]\(([^\n)]+)\)', text):
            target = target.strip().strip('<>')
            if re.match(r'^[a-zA-Z][\w+.-]*:', target) or target.startswith('#'):
                continue
            target = target.split('#', 1)[0]
            resolved = (path.parent / target).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(f'断链：{name} -> {target}')
    return errors


def inventory(root: Path, cfg: dict, last: int) -> tuple[list[dict], list[str]]:
    root = root.resolve()
    found: dict[int, list[Path]] = {}
    errors = []
    base = root / '异星录/正文'
    for path in sorted(base.rglob('*.md')):
        match = CHAPTER.match(path.name)
        if not match:
            continue
        n = int(match[1])
        found.setdefault(n, []).append(path)
        if not 1 <= n <= 800:
            errors.append(f'正文章号越界：{path.relative_to(root)}')
        elif path.parent != safe(root, cfg['volumes'][(n - 1) // 100]['prose']):
            errors.append(f'正文放错卷：第{n:03}章 {path.relative_to(root)}')
        if n > last:
            errors.append(f'正文已出现但状态未登记：第{n:03}章；先核批次发布恢复')
    rows = []
    for n in range(1, last + 1):
        paths = found.get(n, [])
        if len(paths) != 1:
            errors.append(f'第{n:03}章：' + ('缺失' if not paths else '重复文件'))
            continue
        p = paths[0]
        han, nonspace = count_text(p.read_text(encoding='utf-8'))
        rows.append(dict(chapter=n, path=p.relative_to(root).as_posix(), han=han,
                         nonspace=nonspace, sha256=digest(p)))
    return rows, errors


def check(root: Path, structure_only: bool = False) -> dict:
    cfg, current = config(root), status(root)
    errors, warnings = [], []
    for name in cfg['required'] + cfg['ledgers']:
        if not safe(root, name).is_file():
            errors.append(f'缺权威文件：{name}')
    for v in cfg['volumes']:
        plan = safe(root, v['plan'])
        expected = ['逐章卡.md'] if v['number'] == 1 else ['卷纲.md', '十章篇章卡.md']
        for name in expected:
            if not (plan / name).is_file():
                errors.append(f'缺规划：{v["plan"]}/{name}')
    for name, sha in current['evidence'].items():
        p = safe(root, name)
        if not p.is_file() or digest(p) != sha:
            errors.append(f'状态证据缺失或变化：{name}')
    link_files = list(dict.fromkeys(cfg['required'] + [
        p.relative_to(root).as_posix() for p in (root / 'skills/alien-serial-harness').rglob('*.md')]))
    errors.extend(markdown_links(root, link_files))
    if (root / 'harness/layout.json').is_file():
        errors.extend(check_layout(root))
    rows = []
    if not structure_only:
        rows, more = inventory(root, cfg, current['last_published_chapter'])
        errors.extend(more)
        for row in rows:
            if row['han'] < cfg['minimum_han']:
                errors.append(f'第{row["chapter"]:03}章纯汉字不足：{row["han"]} < 2200')
            if row['han'] > cfg['maximum_han']:
                warnings.append(f'第{row["chapter"]:03}章超过建议上限：{row["han"]} > 3200，需人工检查')
    reader_coverage = reader_pull.coverage(root)
    return dict(scope='structure' if structure_only else 'published-inventory-and-structure',
                last_published_chapter=current['last_published_chapter'],
                chapters=len(rows), total_han=sum(r['han'] for r in rows),
                reader_review_coverage=reader_coverage, errors=errors, warnings=warnings, rows=rows)


def batch_path(root: Path, batch_id: str) -> Path:
    if not BATCH_ID.fullmatch(batch_id):
        raise ValueError('批次ID只允许字母起始及字母数字、短横线、下划线')
    return root / 'harness/batches' / f'{batch_id}.json'


def prepare(root: Path, batch_id: str, start: int, end: int) -> dict:
    root = root.resolve()
    cfg, current = config(root), status(root)
    if current['last_published_chapter'] == cfg['planned_chapters']:
        raise ValueError('全书已完结，无续写批次')
    if not 1 <= start <= end <= 800 or end - start >= 10 or (start - 1) // 100 != (end - 1) // 100:
        raise ValueError('每批1—10章且不跨卷；不足10章仍须审读')
    if start != current['next_chapter'] or batch_id != current['next_batch']:
        raise ValueError('批次必须承接当前状态记录的下一章与下一批次')
    path = batch_path(root, batch_id)
    if path.exists():
        raise ValueError('批次已存在；核对并恢复原检查点，不覆盖')
    structural = check(root, True)
    _, inv_errors = inventory(root, cfg, current['last_published_chapter'])
    if structural['errors'] or inv_errors:
        raise ValueError('写前结构/已发布清单异常：' + '; '.join(structural['errors'] + inv_errors))
    sources = ['AGENTS.md', '异星录/00_项目总览/项目总纲.md',
               '异星录/00_项目总览/资料索引与阅读地图.md',
               '异星录/00_项目总览/后七卷设定决策与执行约束.md',
               '异星录/03_剧情架构/分卷总纲.md', '异星录/03_剧情架构/README.md']
    for folder in ['01_世界设定', '02_角色档案', '05_写作规范']:
        sources.extend(p.relative_to(root).as_posix() for p in sorted((root / '异星录' / folder).glob('*.md')))
    sources.extend(cfg['ledgers'])
    sources.extend(current['evidence'])
    plan = safe(root, cfg['volumes'][(start - 1) // 100]['plan'])
    sources.extend(p.relative_to(root).as_posix() for p in sorted(plan.glob('*.md')))
    inputs = {name: digest(safe(root, name)) for name in dict.fromkeys(sources)}
    value = dict(schema_version=1, id=batch_id, start=start, end=end, state='prepared',
                 base_published=current['last_published_chapter'], base_status_sha256=digest(root / 'harness/status.json'),
                 writer='', context={'read_files': [], 'chapter_cards': ''}, input_hashes=inputs,
                 protected_prose=all_hashes(root, '异星录/正文'), chapters=[], checkpoints={}, reviews={},
                 issues=[], conflicts=[], writebacks=[], context_changes={},
                 continuity_report=None, periodic_audits={}, reader_policy_version=1, reader_review=None,
                 reader_contract=dict(expectation='', payoff='', cost='', next_expectation=''))
    save_json(path, value)
    return value


def load_batch(root: Path, batch_id: str) -> dict:
    value = read_json(batch_path(root, batch_id))
    if value.get('schema_version') != 1 or value.get('id') != batch_id:
        raise ValueError('批次版本或ID不一致')
    a, b = value['start'], value['end']
    if type(a) is not int or type(b) is not int or not 1 <= a <= b <= 800 or b - a >= 10:
        raise ValueError('批次章号无效')
    if (a - 1) // 100 != (b - 1) // 100 or value['base_published'] != a - 1:
        raise ValueError('批次范围/写前起点不一致')
    return value


def draft_rows(root: Path, batch: dict) -> list[dict]:
    root = root.resolve()
    rows = []
    chapters = batch['chapters']
    expected = list(range(batch['start'], batch['end'] + 1))
    if [c['chapter'] for c in chapters] != expected:
        raise ValueError('稿件清单必须按章连续、完整且唯一')
    for chapter in chapters:
        p = safe(root, chapter['path'])
        work = safe(root, config(root).get('workspace', '异星录/06_执行计划/工作区'))
        if not p.is_relative_to(work) or p.suffix != '.md':
            raise ValueError('封稿必须是执行计划/工作区内的Markdown工作稿')
        match = CHAPTER.match(p.name)
        if not match or int(match[1]) != chapter['chapter']:
            raise ValueError('稿件文件名与章号不一致')
        han, nonspace = count_text(p.read_text(encoding='utf-8'))
        rows.append(dict(chapter=chapter['chapter'], path=chapter['path'], sha256=digest(p), han=han, nonspace=nonspace))
    return rows


def rows_digest(rows: list[dict]) -> str:
    return hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()


def seal(root: Path, batch_id: str, phase: str) -> dict:
    batch = load_batch(root, batch_id)
    if batch['state'] == 'published':
        raise ValueError('已发布批次不能重新封稿')
    rows = draft_rows(root, batch)
    batch['checkpoints'][phase] = dict(digest=rows_digest(rows), chapters=rows)
    batch['reviews'].pop('initial' if phase == 'draft' else 'final', None)
    batch['reader_review'] = None
    if phase == 'draft':
        batch['checkpoints'].pop('final', None)
        batch['reviews'].pop('final', None)
    batch['state'] = 'draft-sealed' if phase == 'draft' else 'final-sealed'
    save_json(batch_path(root, batch_id), batch)
    return batch['checkpoints'][phase]


def artifact(root: Path, item: dict | None, label: str, errors: list[str], forbidden: set[str] | None = None) -> None:
    if not isinstance(item, dict) or not item.get('path') or not item.get('sha256'):
        errors.append(f'缺{label}路径/指纹')
        return
    name = item['path']
    path = safe(root, name)
    if not path.is_file() or digest(path) != item['sha256']:
        errors.append(f'{label}文件缺失或指纹过期：{name}')
    elif path.stat().st_size == 0:
        errors.append(f'{label}文件为空：{name}')
    if forbidden and name in forbidden:
        errors.append(f'{label}不能用正文文件充当报告')


def reader_gate(root: Path, record: dict, record_name: str, rows: list[dict], errors: list[str], warnings: list[str]) -> None:
    """Require evidence for current work; grandfather only explicitly pinned historical records."""
    if record.get('reader_policy_version') != 1:
        legacy = config(root).get('legacy_reader_records', {})
        p = safe(root, record_name)
        if record_name in legacy and p.is_file() and digest(p) == legacy[record_name]:
            warnings.append('历史记录未按H002开篇/追读标准审读，不计入吸引力通过覆盖')
        else:
            errors.append('缺有效reader_policy_version=1；新工作不能跳过吸引力验收')
        return
    item = record.get('reader_review')
    artifact(root, item, '独立吸引力审读', errors, {r['path'] for r in rows})
    if not isinstance(item, dict) or not item.get('path'):
        return
    path = safe(root, item['path'])
    if not path.is_file():
        return
    if path.parent != root.resolve() / 'harness/reader-reviews' or path.suffix != '.json':
        errors.append('吸引力报告须放harness/reader-reviews目录中的JSON')
        return
    report = read_json(path)
    if report.get('writer') != record.get('writer'):
        errors.append('吸引力报告的主笔与任务记录不一致')
    result = reader_pull.validate(root, report, expected_rows=rows)
    errors.extend(result['errors'])


def gate(root: Path, batch_id: str, published: bool = False) -> dict:
    root = root.resolve()
    cfg, current, batch = config(root), status(root), load_batch(root, batch_id)
    errors, warnings = [], []
    closing_again = current['last_published_chapter'] == batch['end'] and current.get('last_batch') == batch_id
    if not closing_again and (current['last_published_chapter'] != batch['base_published'] or
                              digest(root / 'harness/status.json') != batch['base_status_sha256']):
        errors.append('当前发布状态已变化，不可沿用旧批次起点')
    if not batch.get('writer'):
        errors.append('缺真实主笔标识')
    for phase in ['draft', 'final']:
        snap = batch['checkpoints'].get(phase)
        if not snap or rows_digest(snap['chapters']) != snap['digest']:
            errors.append(f'缺{phase}封稿或封稿摘要损坏')
    final = batch['checkpoints'].get('final', {})
    # A closed batch retains reviewed fingerprints; completed work copies may be removed.
    if batch.get('state') == 'published':
        rows = final.get('chapters', [])
        if [row['chapter'] for row in rows] != list(range(batch['start'], batch['end'] + 1)):
            errors.append('已发布封稿清单不完整')
    else:
        rows = draft_rows(root, batch)
    if rows_digest(rows) != final.get('digest'):
        errors.append('终稿在封稿后变化，须重新封稿并独立复核')
    forbidden = {r['path'] for r in rows}
    for row in rows:
        if row['han'] < cfg['minimum_han']:
            errors.append(f'第{row["chapter"]:03}章不足2200纯汉字：{row["han"]}')
        if row['han'] > cfg['maximum_han']:
            warnings.append(f'第{row["chapter"]:03}章超过3200建议上限：{row["han"]}')
    contract = batch.get('reader_contract', {})
    if not all(isinstance(contract.get(k), str) and contract[k].strip()
               for k in ('expectation', 'payoff', 'cost', 'next_expectation')):
        errors.append('写前缺读者期待/局部兑现/实际代价/下一批期待')
    reader_gate(root, batch, batch_path(root, batch_id).relative_to(root).as_posix(), rows, errors, warnings)
    for label, phase in [('initial', 'draft'), ('final', 'final')]:
        review = batch['reviews'].get(label)
        artifact(root, review, f'{label}独立审读报告', errors, forbidden)
        if not isinstance(review, dict):
            continue
        if not review.get('reviewer') or review['reviewer'] == batch.get('writer') or review.get('independent') is not True or review.get('body_first') is not True:
            errors.append(f'{label}缺独立读者/先正文后资料的真实记录')
        if review.get('input_digest') != batch['checkpoints'].get(phase, {}).get('digest'):
            errors.append(f'{label}审读未绑定对应封稿')
        allowed = ['pass', 'issues'] if label == 'initial' else ['pass']
        if review.get('verdict') not in allowed:
            errors.append(f'{label}审读结论无效/终审未通过')
    initial, final_review = batch['reviews'].get('initial'), batch['reviews'].get('final')
    if isinstance(initial, dict) and isinstance(final_review, dict) and initial.get('path') == final_review.get('path'):
        errors.append('初审与复核应保留各自报告，不覆盖历史审读')
    for issue in batch['issues']:
        if issue.get('severity') not in ['严重', '中等', '轻微'] or not batch['start'] <= issue.get('chapter', 0) <= batch['end']:
            errors.append('问题记录缺有效章号/严重程度')
        if issue.get('status') != 'closed':
            (warnings if issue.get('severity') == '轻微' else errors).append(f'问题未关闭：{issue.get("id")}')
        elif not issue.get('resolution'):
            errors.append(f'问题关闭缺证据：{issue.get("id")}')
    for conflict in batch['conflicts']:
        if conflict.get('status') != 'resolved' or not conflict.get('resolution'):
            errors.append(f'存在未解决设定冲突：{conflict.get("id")}')
    context = batch['context']
    if not set(batch['input_hashes']) <= set(context.get('read_files', [])):
        errors.append('写前必读来源未登记完整（登记不能替代实际阅读）')
    cards = context.get('chapter_cards')
    expected_cards = cfg['volumes'][(batch['start'] - 1) // 100]['plan'] + '/逐章卡.md'
    if cards != expected_cards or not safe(root, cards).is_file():
        errors.append('缺当前批次实际逐章卡路径')
    required = set(cfg['ledgers']) | ({cards} if cards else set())
    writebacks = batch['writebacks']
    names = [w['path'] for w in writebacks]
    if len(names) != len(set(names)):
        errors.append('回填清单重复路径')
    if not required <= set(names):
        errors.append('连续性/术语/章卡回填未完整覆盖：' + ', '.join(sorted(required - set(names))))
    for w in writebacks:
        artifact(root, w, '回填', errors)
        if w.get('status') not in ['updated', 'unchanged'] or not w.get('note'):
            errors.append(f'回填缺实际变更/不变说明：{w.get("path")}')
    for name, sha in batch['input_hashes'].items():
        p = safe(root, name)
        if not p.is_file():
            errors.append(f'写前输入被删除：{name}')
        elif digest(p) != sha and not batch['context_changes'].get(name):
            errors.append(f'写前输入变化未解释：{name}')
    for name, sha in batch['protected_prose'].items():
        p = safe(root, name)
        if not p.is_file() or digest(p) != sha:
            errors.append(f'旧已发布正文变化：{name}')
    artifact(root, batch.get('continuity_report'), '连续性报告', errors, forbidden)
    for divisor, key in [(50, 'fifty'), (100, 'volume')]:
        if any(n % divisor == 0 for n in range(batch['start'], batch['end'] + 1)):
            artifact(root, batch['periodic_audits'].get(key), f'{divisor}章审计', errors, forbidden)
    if any(n % 100 == 0 for n in range(batch['start'], batch['end'] + 1)):
        artifact(root, batch['periodic_audits'].get('snapshot'), '收官状态快照', errors, forbidden)
    # Only this batch may be added during publication; old files and prologue remain protected.
    current_prose = all_hashes(root, '异星录/正文')
    allowed_new = set()
    for row in rows:
        target = cfg['volumes'][(row['chapter'] - 1) // 100]['prose'] + '/' + Path(row['path']).name
        allowed_new.add(target)
        if published and current_prose.get(target) != row['sha256']:
            errors.append(f'发布稿与独立复核终稿不一致/缺失：{target}')
        elif target in current_prose and current_prose[target] != row['sha256']:
            errors.append(f'正文目录存在非当前终稿：{target}')
    extra = set(current_prose) - set(batch['protected_prose']) - allowed_new
    if extra:
        errors.append('正文目录存在批次外新增文件：' + ', '.join(sorted(extra)))
    return dict(id=batch_id, scope='post-publication' if published else 'pre-publication', errors=errors, warnings=warnings, rows=rows)


def close(root: Path, batch_id: str, story_day: str, next_batch: str | None = None) -> dict:
    batch = load_batch(root, batch_id)
    completed = batch['end'] == config(root)['planned_chapters']
    if not story_day.strip():
        raise ValueError('需实际故事时间')
    if completed:
        if next_batch is not None:
            raise ValueError('全书收官不接受下一批次ID')
    elif not next_batch or not BATCH_ID.fullmatch(next_batch) or next_batch == batch_id:
        raise ValueError('未完结批次需有效的下一批次ID')
    # A persistent lock records an interrupted close; do not remove another process's lock.
    lock = root / 'harness/.close.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError('发布登记锁已存在；先核是否有正在执行/中断的登记，再人工处理锁') from None
    try:
        os.close(fd)
        result = gate(root, batch_id, True)
        if result['errors']:
            return result
        batch = load_batch(root, batch_id)
        current = status(root)
        if current.get('last_batch') == batch_id:
            if current['last_story_day'] != story_day or current['next_batch'] != next_batch:
                raise ValueError('重复close参数与已提交状态不同')
        else:
            evidence = {item['path']: item['sha256'] for item in [batch['reviews']['final'], batch['continuity_report']]}
            if batch.get('reader_review'):
                evidence[batch['reader_review']['path']] = batch['reader_review']['sha256']
            evidence.update({item['path']: item['sha256'] for item in batch['periodic_audits'].values()})
            current = dict(schema_version=1, last_published_chapter=batch['end'], last_story_day=story_day,
                           next_chapter=None if completed else batch['end'] + 1,
                           next_batch=next_batch, last_batch=batch_id,
                           provenance='batch-gate', evidence=evidence)
            save_json(root / 'harness/status.json', current)
        batch['state'] = 'published'
        save_json(batch_path(root, batch_id), batch)
        return result
    finally:
        lock.unlink()



def check_layout(root: Path) -> list[str]:
    layout = read_json(root / 'harness/layout.json')
    errors = []
    for pattern in layout.get('retire_root_patterns', []):
        for p in root.glob(pattern):
            if p.is_file():
                errors.append(f'一次性旧脚本仍在项目根：{p.name}')
    base = root / '异星录/06_执行计划'
    allowed_dirs = set(layout.get('execution_groups', []))
    for p in base.iterdir():
        if p.name in {'.DS_Store', '__pycache__'}:
            continue
        if p.is_dir() and p.name not in allowed_dirs:
            errors.append(f'执行目录未分类：{p.name}')
        elif p.is_file() and p.name not in {'README.md', '详细执行计划.md'}:
            errors.append(f'执行文件未分类：{p.name}')
    return errors


def verify_repair(root: Path, record_name: str) -> dict:
    """Validate an authorized repair of existing prose without advancing story state."""
    root = root.resolve()
    cfg, current = config(root), status(root)
    record = read_json(safe(root, record_name))
    errors, warnings = [], []
    if record.get('schema_version') != 1 or record.get('kind') != 'existing-prose-repair':
        raise ValueError('返修记录版本/种类错误')
    if not record.get('authorization') or not record.get('writer'):
        errors.append('缺返修授权/真实主笔标识')
    rows = record.get('chapters', [])
    numbers = [row['chapter'] for row in rows]
    if not numbers or len(numbers) != len(set(numbers)):
        errors.append('返修章号为空或重复')
    targets = set()
    for row in rows:
        n = row['chapter']
        if type(n) is not int or not 0 <= n <= current['last_published_chapter']:
            errors.append(f'返修不能包含未发布章号：{n}')
            continue
        p = safe(root, row['path'])
        match = CHAPTER.match(p.name)
        prologue = n == 0 and p.name.startswith('楔子') and p.suffix == '.md'
        volume = cfg['volumes'][0 if n == 0 else (n - 1) // 100]['prose']
        if p.parent != safe(root, volume) or not (prologue if n == 0 else match and int(match[1]) == n):
            errors.append(f'返修正文路径/卷号不符：{row["path"]}')
        targets.add(row['path'])
        if not p.is_file() or digest(p) != row['after_sha256']:
            errors.append(f'返修终稿与记录不符：{row["path"]}')
            continue
        han, _ = count_text(p.read_text(encoding='utf-8'))
        if n > 0 and han < cfg['minimum_han']:
            errors.append(f'返修第{n}章不足2200纯汉字')
        if n > 0 and han > cfg['maximum_han']:
            warnings.append(f'返修第{n}章超过3200建议上限')
        if not re.fullmatch(r'[a-f0-9]{64}', row.get('before_sha256', '')):
            errors.append(f'返修第{n}章缺修改前指纹')
    preserved = record.get('protected_prose', {})
    for name, sha in preserved.items():
        p = safe(root, name)
        if not p.is_file() or digest(p) != sha:
            errors.append(f'返修范围外正文变化：{name}')
    current_files = set(all_hashes(root, '异星录/正文'))
    # README and volume indexes are metadata, not chapter bodies.
    actual_prose = {name for name in current_files if CHAPTER.match(Path(name).name) or Path(name).name.startswith('楔子')}
    if actual_prose != targets | set(preserved):
        errors.append('返修目标和保护清单未完整覆盖现行正文/楔子')
    groups = record.get('groups', [])
    covered = []
    for group in groups:
        group_numbers = group['chapters']
        covered.extend(group_numbers)
        final_rows = [dict(chapter=x['chapter'], path=x['path'], sha256=x['after_sha256'])
                      for x in rows if x['chapter'] in group_numbers]
        final_digest = rows_digest(final_rows)
        for phase in ['initial', 'final']:
            review = group.get(phase)
            artifact(root, review, f'返修{phase}审读', errors, targets)
            if not isinstance(review, dict):
                continue
            if not review.get('reviewer') or review.get('reviewer') == record['writer'] or review.get('independent') is not True or review.get('body_first') is not True:
                errors.append(f'返修{phase}缺真实独立首读/复核记录')
            expected = group.get('initial_digest') if phase == 'initial' else final_digest
            if review.get('input_digest') != expected:
                errors.append(f'返修{phase}报告未绑定实际稿件摘要')
            if review.get('verdict') not in (['pass', 'issues'] if phase == 'initial' else ['pass']):
                errors.append(f'返修{phase}未通过')
    if sorted(covered) != sorted(numbers):
        errors.append('独立审读分组未完整且唯一覆盖返修章节')
    required = set(cfg['ledgers']) | set(record.get('chapter_cards', []))
    names = {item['path'] for item in record.get('writebacks', [])}
    if not required <= names or not record.get('chapter_cards'):
        errors.append('返修六份台账/章卡回填证据不完整')
    for item in record.get('writebacks', []):
        artifact(root, item, '返修回填', errors)
        if item.get('status') not in {'updated', 'unchanged'} or not item.get('note'):
            errors.append('返修回填缺变化/继承说明')
    for issue in record.get('issues', []):
        if issue.get('status') != 'closed' or not issue.get('resolution'):
            errors.append(f'返修问题未关闭：{issue.get("id")}')
    for field in ['last_published_chapter', 'last_story_day', 'next_chapter', 'next_batch']:
        if current.get(field) != record.get('story_state', {}).get(field):
            errors.append(f'旧章返修不应推进连载状态：{field}')
    reader_rows = [dict(chapter=x['chapter'], path=x['path'], sha256=x['after_sha256']) for x in rows]
    reader_gate(root, record, record_name, reader_rows, errors, warnings)
    return dict(scope='existing-prose-repair', chapters=len(rows), protected=len(preserved), errors=errors, warnings=warnings)


def preservation(root: Path) -> dict:
    baseline = read_json(safe(root, config(root)['preservation_baseline']))
    errors = []
    for name, sha in baseline['files'].items():
        p = safe(root, name)
        if not p.is_file() or digest(p) != sha:
            errors.append(f'保护文件变化：{name}')
    return dict(scope='harness-change-preservation-only', files=len(baseline['files']), errors=errors, warnings=[])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    cmd = sub.add_parser('check')
    cmd.add_argument('--structure-only', action='store_true')
    cmd.add_argument('--json', action='store_true')
    cmd = sub.add_parser('verify-preservation')
    cmd = sub.add_parser('verify-repair')
    cmd.add_argument('--record', required=True)
    for name in ['prepare', 'seal', 'gate', 'close']:
        cmd = sub.add_parser(name)
        cmd.add_argument('--id', required=True)
        if name == 'prepare':
            cmd.add_argument('--start', type=int, required=True)
            cmd.add_argument('--end', type=int, required=True)
        if name == 'seal':
            cmd.add_argument('--phase', choices=['draft', 'final'], required=True)
        if name == 'gate':
            cmd.add_argument('--published', action='store_true')
        if name == 'close':
            cmd.add_argument('--story-day', required=True)
            cmd.add_argument('--next-batch', help='未完结时必填，末章收官时省略')
    args = parser.parse_args()
    try:
        if args.command == 'check':
            result = check(ROOT, args.structure_only)
        elif args.command == 'verify-preservation':
            result = preservation(ROOT)
        elif args.command == 'verify-repair':
            result = verify_repair(ROOT, args.record)
        elif args.command == 'prepare':
            result = prepare(ROOT, args.id, args.start, args.end)
        elif args.command == 'seal':
            result = seal(ROOT, args.id, args.phase)
        elif args.command == 'gate':
            result = gate(ROOT, args.id, args.published)
        else:
            result = close(ROOT, args.id, args.story_day, args.next_batch)
        if args.command == 'check' and not args.json:
            print(f'范围 {result["scope"]}；正文 {result["chapters"]}章 / {result["total_han"]}汉字')
            coverage = result['reader_review_coverage']
            print(f'独立开篇/追读审读通过 {coverage["passed_count"]}/{coverage["published"]}章；'
                  f'未审或未通过 {coverage["unreviewed_or_not_passed_count"]}章；自动检查不代表吸引力通过')
            for item in result['errors']:
                print('ERROR ' + item)
            for item in result['warnings']:
                print('WARN ' + item)
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get('errors') else 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(f'ERROR 数据或参数无效：{exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
