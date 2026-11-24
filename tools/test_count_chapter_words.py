import tempfile
import unittest
from pathlib import Path
from count_chapter_words import audit, count_text


class CountTests(unittest.TestCase):
    def test_titles_spaces_and_punctuation(self):
        self.assertEqual(count_text('# 第一章 标题\n\n你好，世 界！123A\n'), (4, 10))

    def test_extension_a(self):
        self.assertEqual(count_text('㐀渡\n'), (2, 2))

    def test_missing_duplicate_and_prologue(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '楔子.md').write_text('楔子不算章节')
            (root / '第001章_甲.md').write_text('# 标题\n正文')
            (root / '第002章_乙.md').write_text('乙')
            (root / '第002章_重复.md').write_text('另稿')
            rows, errors = audit(root, 1, 3)
            self.assertEqual([(r['chapter'], r['han']) for r in rows], [(1, 2)])
            self.assertEqual(errors, ['第002章：重复文件', '第003章：缺失'])


if __name__ == '__main__':
    unittest.main()
