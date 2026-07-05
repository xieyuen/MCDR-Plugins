import sys
import unittest

from typing import Any

sys.path.append('./src/MCDRpost')

from mcdrpost.utils.version import MCVersion


class TestMCVersion(unittest.TestCase):

    def __run_init_test(self, versions, expected_vers):
        for v, e in zip(versions, expected_vers):
            self.assertEqual(e,
                             (v.major, v.minor, v.patch, v.prerelease, v.build),
                             )

    def test_init(self):
        old_versions = [
            MCVersion("1.2"),
            MCVersion("1.2.3"),
            MCVersion("1.2-pre.1-1"),
            MCVersion("1.2.3-pre.1-1"),
        ]

        old_expected = [
            (1, 2, 0, "", ""),
            (1, 2, 3, "", ""),
            (1, 2, 0, "pre.1-1", ""),
            (1, 2, 3, "pre.1-1", ""),
        ]

        self.__run_init_test(old_versions, old_expected)

        new_versions = [
            MCVersion("26.1"),
            MCVersion("26.1-snapshot-1"),
            MCVersion("26.1.2"),
            MCVersion("26.1.2-snapshot-1"),
        ]

        new_expected = [
            (26, 1, 0, "", ""),
            (26, 1, 0, "snapshot-1", ""),
            (26, 1, 2, "", ""),
            (26, 1, 2, "snapshot-1", ""),
        ]

        self.__run_init_test(new_versions, new_expected)

    def test_init_err(self):
        value_error_cases: list[Any] = [
            "",
            "1",
            "1.",
            "1..",
            "1!.132.",

        ]

        for c in value_error_cases:
            with self.assertRaises(ValueError):
                MCVersion(c)

        type_error_cases: list[Any] = [
            124, 7654.2453, (134, 7), [], {}, set(),(None, None),None
        ]
        for c in type_error_cases:
            with self.assertRaises(TypeError):
                MCVersion(c)

    def test_comparison(self):
        v_old_1 = MCVersion("1.2")
        v_old_2 = MCVersion("1.2.3")
        v_old_3 = MCVersion("1.2.4")
        v_old_4 = MCVersion("1.2.4-pre")
        v_old_5 = MCVersion("1.2-pre")
        v_old_6 = MCVersion("1.2.4-pre+b")

        self.assertLess(v_old_1, v_old_2)
        self.assertLess(v_old_1, v_old_3)
        self.assertLess(v_old_5, v_old_1)
        self.assertLess(v_old_4, v_old_3)
        self.assertEqual(v_old_4, v_old_6)

        v_new_1 = MCVersion("26.2-snapshot-1")
        v_new_2 = MCVersion("26.2")

        self.assertGreater(v_new_1, v_old_1)
        self.assertGreater(v_new_1, v_old_2)
        self.assertGreater(v_new_1, v_old_3)
        self.assertGreater(v_new_1, v_old_4)
        self.assertGreater(v_new_2, v_old_1)
        self.assertGreater(v_new_2, v_old_2)
        self.assertGreater(v_new_2, v_old_3)
        self.assertGreater(v_new_2, v_old_4)
        self.assertGreater(v_new_2, v_new_1)

    def test_diff_type_comparison(self):
        ver = MCVersion("1.2")
        cases: list[tuple[Any, bool]] = [
            ("1.2.3", True),
            ("1.2.3-pre", True),
            ("1.1.3-pre", False),
            ("1.1.3", False),
            ("1.1", False),
            ("1.3", True),
            ("26.3", True),
            ("26.3-snapshot-1", True),
            ((1,2,3), True),
            ((1,1), False),
            ((1,1,12309), False),
            ((1,1,12309, "234"), False),
        ]

        for case, expected in cases:
            self.assertEqual(ver < case, expected)


if __name__ == '__main__':
    unittest.main()
