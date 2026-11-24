"""验证发布状态、稿件指纹、审读与回填门禁；只使用临时合成项目。"""
import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import novel_harness as h
import check_reader_pull as rp
from count_chapter_words import audit


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.cfg = json.loads((h.ROOT / 'harness/project.json').read_text())
        for name in self.cfg['required'] + self.cfg['ledgers']:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('# 测试资料\n')
        h.save_json(self.root / 'harness/project.json', self.cfg)
        h.save_json(self.root / 'harness/layout.json', json.loads((h.ROOT / 'harness/layout.json').read_text()))
        (self.root / '异星录/06_执行计划').mkdir(parents=True, exist_ok=True)
        for v in self.cfg['volumes']:
            for file in ['卷纲.md', '十章篇章卡.md', '逐章卡.md']:
                path = self.root / v['plan'] / file
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('# 合成规划\n')
        evidence = self.root / 'harness/initial.md'
        evidence.write_text('测试初态证据')
        h.save_json(self.root / 'harness/status.json', dict(
            schema_version=1, last_published_chapter=0, next_chapter=1,
            last_story_day='D0', next_batch='A00', evidence={'harness/initial.md': h.digest(evidence)}))
        (self.root / '异星录/正文').mkdir(parents=True)

    def artifact(self, name):
        p = self.root / f'异星录/06_执行计划/审读记录/第一卷/{name}.md'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('# 合成验收记录\n仅用于测试，不是真实小说审读。\n')
        return dict(path=p.relative_to(self.root).as_posix(), sha256=h.digest(p))

    def save(self, b):
        h.save_json(h.batch_path(self.root, b['id']), b)

    def reader_report(self, b):
        """Synthetic evidence exercises gates only; it makes no claim about real prose."""
        rows = [{k: x[k] for k in ('chapter', 'path', 'sha256')}
                for x in b['checkpoints']['final']['chapters']]
        opening = b['start'] <= 3
        if opening:
            for n in sorted({1, 2, 3} - {x['chapter'] for x in rows}):
                old = list((self.root / self.cfg['volumes'][0]['prose']).glob(f'第{n:03}章_*.md'))
                p = old[0] if old else self.root / f'异星录/06_执行计划/工作区/context/第{n:03}章_合成上下文.md'
                p.parent.mkdir(parents=True, exist_ok=True)
                if not p.exists():
                    p.write_text('# 合成上下文\n' + '文' * 2200)
                rows.append(dict(chapter=n, path=p.relative_to(self.root).as_posix(), sha256=h.digest(p)))
        rows.sort(key=lambda x: x['chapter'])
        quotes = {x['chapter']: ('旧' if '旧文' in x['path'] else '文') for x in rows}
        checks = [dict(criterion=c, chapter=x['chapter'], quote=quotes[x['chapter']],
                       reason='临时合成测试证据，不是真实小说审读', verdict='pass')
                  for x in rows for c in rp.CHAPTER_CHECKS]
        checks += [dict(criterion=c, chapter=rows[0]['chapter'], quote=quotes[rows[0]['chapter']],
                        reason='临时合成测试', verdict='pass')
                   for c in rp.BATCH_CHECKS + (rp.OPENING_CHECKS if opening else ())]
        report = dict(schema_version=1, kind='review', independent=True, body_first=True,
                      writer=b['writer'], reviewer='reader-fixture', profile='opening' if opening else 'serial',
                      manuscripts=rows, source_digest=rp.digest_rows(rows), checks=checks, verdict='pass')
        p = self.root / 'harness/reader-reviews/A00.json'
        h.save_json(p, report)
        return dict(path=p.relative_to(self.root).as_posix(), sha256=h.digest(p))

    def change_reader_report(self, b, change):
        p = self.root / b['reader_review']['path']
        report = h.read_json(p)
        change(report)
        h.save_json(p, report)
        b['reader_review']['sha256'] = h.digest(p)
        self.save(b)

    def complete(self, start=1, end=2):
        if start > 1:
            s = h.status(self.root)
            s.update(last_published_chapter=start - 1, next_chapter=start)
            h.save_json(self.root / 'harness/status.json', s)
            for n in range(1, start):
                p = self.root / self.cfg['volumes'][(n - 1) // 100]['prose'] / f'第{n:03}章_旧文.md'
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('# 旧章题\n' + '旧' * 2200)
        b = h.prepare(self.root, 'A00', start, end)
        b['writer'] = 'writer-fixture'
        b['reader_contract'] = dict(expectation='合成期待', payoff='合成兑现', cost='合成代价', next_expectation='合成新期待')
        b['context']['read_files'] = list(b['input_hashes'])
        b['context']['chapter_cards'] = self.cfg['volumes'][(start - 1) // 100]['plan'] + '/逐章卡.md'
        for n in range(start, end + 1):
            p = self.root / '异星录/06_执行计划/工作区/A00' / f'第{n:03}章_合成.md'
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f'# 第{n}章 标题不计字\n' + '文' * 2200 + '！123')
            b['chapters'].append(dict(chapter=n, path=p.relative_to(self.root).as_posix()))
        self.save(b)
        h.seal(self.root, 'A00', 'draft')
        h.seal(self.root, 'A00', 'final')
        b = h.load_batch(self.root, 'A00')
        b['reader_review'] = self.reader_report(b)
        for label, phase in [('initial', 'draft'), ('final', 'final')]:
            b['reviews'][label] = dict(**self.artifact(label), reviewer='reader-fixture',
                independent=True, body_first=True, input_digest=b['checkpoints'][phase]['digest'], verdict='pass')
        for name in self.cfg['ledgers'] + [b['context']['chapter_cards']]:
            b['writebacks'].append(dict(path=name, sha256=h.digest(self.root / name), status='unchanged', note='合成测试，确认无变化'))
        b['continuity_report'] = self.artifact('continuity')
        self.save(b)
        return b

    def test_structure_and_no_future_prose_required(self):
        self.assertEqual(h.check(self.root)['errors'], [])

    def test_reject_path_escape_and_symlink(self):
        for name in ['/tmp/outside', '../../outside']:
            with self.assertRaises(ValueError):
                h.safe(self.root, name)
        (self.root / 'escape').symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaises(ValueError):
            h.safe(self.root, 'escape/outside')

    def test_reject_changed_scale_or_threshold(self):
        for key, value in [('planned_chapters', 10), ('minimum_han', 1200)]:
            cfg = copy.deepcopy(self.cfg)
            cfg[key] = value
            h.save_json(self.root / 'harness/project.json', cfg)
            with self.assertRaises(ValueError):
                h.config(self.root)

    def test_broken_critical_link_and_status_evidence(self):
        (self.root / 'AGENTS.md').write_text('[丢失](missing.md)')
        (self.root / 'harness/initial.md').write_text('已变')
        errors = h.check(self.root, True)['errors']
        self.assertTrue(any('断链' in e for e in errors))
        self.assertTrue(any('状态证据' in e for e in errors))

    def test_prepare_rejects_out_of_order_and_never_overwrites(self):
        with self.assertRaises(ValueError):
            h.prepare(self.root, 'A00', 2, 3)
        h.prepare(self.root, 'A00', 1, 2)
        with self.assertRaises(ValueError):
            h.prepare(self.root, 'A00', 1, 2)
        self.assertFalse((self.root / '异星录/06_执行计划/工作区/A00').exists())

    def test_empty_batch_cannot_pass(self):
        h.prepare(self.root, 'A00', 1, 2)
        with self.assertRaises(ValueError):
            h.gate(self.root, 'A00')

    def test_happy_gate_and_counts(self):
        self.complete()
        result = h.gate(self.root, 'A00')
        self.assertEqual(result['errors'], [])
        self.assertEqual([r['han'] for r in result['rows']], [2200, 2200])

    def test_changed_manuscript_requires_rereview(self):
        b = self.complete()
        p = self.root / b['chapters'][0]['path']
        p.write_text(p.read_text() + '变')
        self.assertTrue(any('封稿后变化' in e for e in h.gate(self.root, 'A00')['errors']))
        h.seal(self.root, 'A00', 'final')
        self.assertNotIn('final', h.load_batch(self.root, 'A00')['reviews'])
        self.assertIsNone(h.load_batch(self.root, 'A00')['reader_review'])
        self.assertTrue(h.gate(self.root, 'A00')['errors'])

    def test_stale_report_and_wrong_digest_are_blocked(self):
        b = self.complete()
        (self.root / b['reviews']['initial']['path']).write_text('变化')
        b['reviews']['final']['input_digest'] = '0' * 64
        self.save(b)
        errors = h.gate(self.root, 'A00')['errors']
        self.assertTrue(any('指纹过期' in e for e in errors))
        self.assertTrue(any('未绑定' in e for e in errors))

    def test_writer_self_review_is_blocked(self):
        b = self.complete()
        b['reviews']['final']['reviewer'] = b['writer']
        self.save(b)
        self.assertTrue(any('独立读者' in e for e in h.gate(self.root, 'A00')['errors']))

    def test_unresolved_issue_or_conflict_is_blocked(self):
        b = self.complete()
        b['issues'] = [dict(id='I1', chapter=1, severity='严重', status='open')]
        b['conflicts'] = [dict(id='C1', status='pending')]
        self.save(b)
        errors = h.gate(self.root, 'A00')['errors']
        self.assertTrue(any('问题未关闭' in e for e in errors))
        self.assertTrue(any('未解决设定冲突' in e for e in errors))

    def test_missing_writeback_and_changed_input_are_blocked(self):
        b = self.complete()
        b['writebacks'].pop()
        (self.root / 'AGENTS.md').write_text('新规则')
        self.save(b)
        errors = h.gate(self.root, 'A00')['errors']
        self.assertTrue(any('未完整覆盖' in e for e in errors))
        self.assertTrue(any('输入变化未解释' in e for e in errors))

    def test_old_prose_cannot_be_waived_by_context_explanation(self):
        b = self.complete(3, 4)
        name = next(iter(b['protected_prose']))
        (self.root / name).write_text('变动旧文')
        b['context_changes'][name] = '不能豁免'
        self.save(b)
        self.assertTrue(any('旧已发布正文变化' in e for e in h.gate(self.root, 'A00')['errors']))

    def test_fifty_and_volume_audits_required_at_boundary(self):
        b = self.complete(99, 100)
        errors = h.gate(self.root, 'A00')['errors']
        for label in ['50章审计', '100章审计', '收官状态快照']:
            self.assertTrue(any(label in e for e in errors))
        for label in ['fifty', 'volume', 'snapshot']:
            b['periodic_audits'][label] = self.artifact(label)
        self.save(b)
        self.assertEqual(h.gate(self.root, 'A00')['errors'], [])

    def test_close_requires_exact_published_bytes_and_is_idempotent(self):
        b = self.complete()
        before = h.digest(self.root / 'harness/status.json')
        self.assertTrue(h.close(self.root, 'A00', 'D2', 'A01')['errors'])
        self.assertEqual(h.digest(self.root / 'harness/status.json'), before)
        target_dir = self.root / self.cfg['volumes'][0]['prose']
        target_dir.mkdir(parents=True, exist_ok=True)
        for row in b['chapters']:
            shutil.copyfile(self.root / row['path'], target_dir / Path(row['path']).name)
        (target_dir / '目录.md').write_text('目录是元数据，不是旧章节正文')
        (self.root / '异星录/正文/README.md').write_text('正文导航元数据可同步更新')
        self.assertEqual(h.close(self.root, 'A00', 'D2', 'A01')['errors'], [])
        self.assertEqual(h.status(self.root)['last_published_chapter'], 2)
        for item in b['chapters']:
            (self.root / item['path']).unlink()
        self.assertEqual(h.close(self.root, 'A00', 'D2', 'A01')['errors'], [])
        self.assertEqual(h.load_batch(self.root, 'A00')['state'], 'published')
        self.assertEqual(h.prepare(self.root, 'A01', 3, 4)['base_published'], 2)

    def test_close_last_chapter_has_no_continuation(self):
        batch = self.complete(800, 800)
        batch['periodic_audits'] = {
            key: self.artifact(key) for key in ('fifty', 'volume', 'snapshot')
        }
        self.save(batch)
        target_dir = self.root / self.cfg['volumes'][-1]['prose']
        for row in batch['chapters']:
            shutil.copyfile(self.root / row['path'], target_dir / Path(row['path']).name)

        with self.assertRaisesRegex(ValueError, '不接受下一批次'):
            h.close(self.root, 'A00', 'D947', 'A01')
        self.assertEqual(h.close(self.root, 'A00', 'D947')['errors'], [])
        state = h.status(self.root)
        self.assertEqual(state['last_published_chapter'], 800)
        self.assertIsNone(state['next_chapter'])
        self.assertIsNone(state['next_batch'])
        with self.assertRaisesRegex(ValueError, '全书已完结'):
            h.prepare(self.root, 'A01', 801, 801)
        for row in batch['chapters']:
            (self.root / row['path']).unlink()
        self.assertEqual(h.close(self.root, 'A00', 'D947')['errors'], [])

    def test_partial_publication_and_duplicate_prose_are_detected(self):
        self.complete()
        p = self.root / self.cfg['volumes'][0]['prose'] / '第001章_错误.md'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('不一致')
        self.assertTrue(h.gate(self.root, 'A00', True)['errors'])

    def test_inventory_detects_missing_duplicate_wrong_volume(self):
        self.complete(3, 4)
        old = self.root / self.cfg['volumes'][0]['prose']
        (old / '第001章_重复.md').write_text('文')
        wrong = self.root / self.cfg['volumes'][1]['prose']
        wrong.mkdir(parents=True)
        (wrong / '第002章_错误卷.md').write_text('文')
        (old / '第002章_旧文.md').unlink()
        _, errors = h.inventory(self.root, self.cfg, 2)
        self.assertTrue(any('重复' in e for e in errors))
        self.assertTrue(any('放错卷' in e for e in errors))
        (wrong / '第002章_错误卷.md').unlink()
        _, errors = h.inventory(self.root, self.cfg, 2)
        self.assertTrue(any('缺失' in e for e in errors))

    def test_recursive_word_audit_catches_cross_volume_duplicate(self):
        p = self.root / '异星录/正文/甲/第001章_甲.md'
        p.parent.mkdir(parents=True)
        p.write_text('# 题\n文')
        q = self.root / '异星录/正文/乙/第001章_乙.md'
        q.parent.mkdir(parents=True)
        q.write_text('文')
        rows, errors = audit(self.root / '异星录/正文', 1, 1, recursive=True)
        self.assertEqual(rows, [])
        self.assertIn('重复', errors[0])


    def repair_record(self):
        batch = self.complete()
        target_dir = self.root / self.cfg['volumes'][0]['prose']
        target_dir.mkdir(parents=True, exist_ok=True)
        rows = []
        for item in batch['chapters']:
            dest = target_dir / Path(item['path']).name
            shutil.copyfile(self.root / item['path'], dest)
            rows.append(dict(chapter=item['chapter'], path=dest.relative_to(self.root).as_posix(),
                             before_sha256='a' * 64, after_sha256=h.digest(dest)))
        state = h.status(self.root)
        state.update(last_published_chapter=2, next_chapter=3)
        h.save_json(self.root / 'harness/status.json', state)
        digest = h.rows_digest([dict(chapter=x['chapter'], path=x['path'], sha256=x['after_sha256']) for x in rows])
        reviews = copy.deepcopy(batch['reviews'])
        for item in reviews.values():
            item['input_digest'] = digest
        record = dict(schema_version=1, kind='existing-prose-repair', authorization='合成测试授权',
                      reader_policy_version=1, reader_review=batch['reader_review'],
                      writer=batch['writer'], chapters=rows, protected_prose={},
                      groups=[dict(chapters=[1, 2], initial_digest=digest, initial=reviews['initial'], final=reviews['final'])],
                      chapter_cards=[batch['context']['chapter_cards']], writebacks=batch['writebacks'], issues=[],
                      story_state={k: state[k] for k in ['last_published_chapter', 'last_story_day', 'next_chapter', 'next_batch']})
        h.save_json(self.root / 'harness/repair.json', record)
        return record

    def test_old_chapter_repair_keeps_story_state(self):
        self.repair_record()
        self.assertEqual(h.verify_repair(self.root, 'harness/repair.json')['errors'], [])
        self.assertEqual(h.status(self.root)['last_published_chapter'], 2)

    def test_repair_rejects_changed_final_prose(self):
        record = self.repair_record()
        (self.root / record['chapters'][0]['path']).write_text('损坏')
        self.assertTrue(h.verify_repair(self.root, 'harness/repair.json')['errors'])

    def test_repair_rejects_self_review_and_incomplete_coverage(self):
        record = self.repair_record()
        record['groups'][0]['final']['reviewer'] = record['writer']
        record['groups'][0]['chapters'] = [1]
        h.save_json(self.root / 'harness/repair.json', record)
        errors = h.verify_repair(self.root, 'harness/repair.json')['errors']
        self.assertTrue(any('独立' in e for e in errors))
        self.assertTrue(any('完整且唯一覆盖' in e for e in errors))

    def test_repair_cannot_advance_current_chapter(self):
        self.repair_record()
        state = h.status(self.root)
        state.update(last_published_chapter=3, next_chapter=4)
        h.save_json(self.root / 'harness/status.json', state)
        self.assertTrue(any('不应推进' in e for e in h.verify_repair(self.root, 'harness/repair.json')['errors']))

    def test_layout_detects_retired_script_and_unclassified_cache(self):
        (self.root / '_expand_old.py').write_text('print(1)')
        (self.root / '异星录/06_执行计划/old-cache.json').write_text('{}')
        errors = h.check_layout(self.root)
        self.assertTrue(any('一次性旧脚本' in e for e in errors))
        self.assertTrue(any('执行文件未分类' in e for e in errors))

    def test_missing_reader_review_and_contract_block_gate(self):
        b = self.complete()
        b['reader_review'] = None
        b['reader_contract']['payoff'] = ''
        self.save(b)
        errors = h.gate(self.root, 'A00')['errors']
        self.assertTrue(any('独立吸引力审读' in e for e in errors))
        self.assertTrue(any('写前缺读者期待' in e for e in errors))

    def test_removing_new_reader_policy_cannot_bypass_gate(self):
        b = self.complete()
        del b['reader_policy_version']
        self.save(b)
        self.assertTrue(any('不能跳过' in e for e in h.gate(self.root, 'A00')['errors']))

    def test_reader_quote_must_exist_and_each_chapter_must_be_covered(self):
        b = self.complete()
        def mutate(report):
            report['checks'][0]['quote'] = '正文里完全不存在的引文'
            report['checks'].pop(5)
        self.change_reader_report(b, mutate)
        errors = h.gate(self.root, 'A00')['errors']
        self.assertTrue(any('缺实际正文原句' in e for e in errors))
        self.assertTrue(any('覆盖不完整' in e for e in errors))

    def test_author_diagnostic_never_counts_as_pass(self):
        b = self.complete()
        self.change_reader_report(b, lambda r: r.update(kind='diagnostic', independent=False, reviewer=r['writer']))
        self.assertTrue(any('作者诊断' in e for e in h.gate(self.root, 'A00')['errors']))
        state = h.status(self.root)
        state.update(last_published_chapter=2, next_chapter=3)
        h.save_json(self.root / 'harness/status.json', state)
        self.assertEqual(rp.coverage(self.root)['unreviewed_or_not_passed_count'], 2)

    def test_failed_reader_item_and_wrong_writer_are_blocked(self):
        b = self.complete()
        def mutate(report):
            report['writer'] = 'other-writer'
            report['checks'][0].update(verdict='needs_revision', action='合成修订方向')
        self.change_reader_report(b, mutate)
        errors = h.gate(self.root, 'A00')['errors']
        self.assertTrue(any('主笔' in e for e in errors))
        self.assertTrue(any('未通过的开篇/追读' in e for e in errors))

    def test_opening_cannot_skip_actual_prologue(self):
        self.complete()
        p = self.root / self.cfg['volumes'][0]['prose'] / '楔子_合成.md'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('# 楔子\n开头只有说明。')
        errors = h.gate(self.root, 'A00')['errors']
        self.assertTrue(any('真实阅读入口楔子' in e for e in errors))
        self.assertTrue(any('真实入口前100' in e for e in errors))

    def test_first_page_evidence_cannot_be_later_climax(self):
        b = self.complete()
        def mutate(report):
            next(x for x in report['checks'] if x['criterion'] == 'first_page_hook')['quote'] = '123'
        self.change_reader_report(b, mutate)
        errors = h.gate(self.root, 'A00')['errors']
        self.assertTrue(any('真实入口前100' in e for e in errors))

    def test_review_context_change_invalidates_reader_coverage(self):
        b = self.complete()
        state = h.status(self.root)
        state.update(last_published_chapter=2, next_chapter=3)
        h.save_json(self.root / 'harness/status.json', state)
        self.assertEqual(rp.coverage(self.root)['passed_count'], 2)
        r = h.read_json(self.root / b['reader_review']['path'])
        context = next(x for x in r['manuscripts'] if x['chapter'] == 3)
        p = self.root / context['path']
        p.write_text(p.read_text() + '变化')
        self.assertEqual(rp.coverage(self.root)['passed_count'], 0)

    def test_new_repair_requires_reader_review(self):
        record = self.repair_record()
        record.pop('reader_policy_version')
        h.save_json(self.root / 'harness/repair.json', record)
        self.assertTrue(any('不能跳过' in e for e in h.verify_repair(self.root, 'harness/repair.json')['errors']))

    def test_pinned_legacy_record_is_honest_and_cannot_be_reused_after_change(self):
        record = self.repair_record()
        record.pop('reader_policy_version')
        p = self.root / 'harness/repair.json'
        h.save_json(p, record)
        cfg = h.read_json(self.root / 'harness/project.json')
        cfg['legacy_reader_records'] = {'harness/repair.json': h.digest(p)}
        h.save_json(self.root / 'harness/project.json', cfg)
        result = h.verify_repair(self.root, 'harness/repair.json')
        self.assertEqual(result['errors'], [])
        self.assertTrue(any('未按H002' in e for e in result['warnings']))
        record['note'] = '新内容不能借用旧签名'
        h.save_json(p, record)
        self.assertTrue(any('不能跳过' in e for e in h.verify_repair(self.root, 'harness/repair.json')['errors']))

    def test_opening_repair_can_include_real_prologue_without_chapter_length_rule(self):
        record = self.repair_record()
        p = self.root / self.cfg['volumes'][0]['prose'] / '楔子_合成.md'
        p.write_text('# 合成楔子\n入口有具体冲突。')
        row = dict(chapter=0, path=p.relative_to(self.root).as_posix(), before_sha256='b' * 64, after_sha256=h.digest(p))
        record['chapters'].insert(0, row)
        group = record['groups'][0]
        group['chapters'].insert(0, 0)
        digest = h.rows_digest([dict(chapter=x['chapter'], path=x['path'], sha256=x['after_sha256']) for x in record['chapters']])
        group['initial_digest'] = digest
        for phase in ('initial', 'final'):
            group[phase]['input_digest'] = digest
        report_path = self.root / record['reader_review']['path']
        report = h.read_json(report_path)
        report['manuscripts'].insert(0, dict(chapter=0, path=row['path'], sha256=row['after_sha256']))
        report['source_digest'] = rp.digest_rows(report['manuscripts'])
        next(x for x in report['checks'] if x['criterion'] == 'first_page_hook').update(chapter=0, quote='入口有具体冲突。')
        h.save_json(report_path, report)
        record['reader_review']['sha256'] = h.digest(report_path)
        h.save_json(self.root / 'harness/repair.json', record)
        self.assertEqual(h.verify_repair(self.root, 'harness/repair.json')['errors'], [])


if __name__ == '__main__':
    unittest.main()
