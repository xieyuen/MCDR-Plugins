import os
import sys
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# 修复导入路径
from src.MCDRpost.mcdrpost.utils.version import SemanticVersion


class TestSemanticVersion(unittest.TestCase):
    def test_init_and_properties(self):
        """测试 SemanticVersion 初始化和属性"""
        v = SemanticVersion("1.2.3")
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)
        self.assertIsNone(v.pre_release)
        self.assertIsNone(v.build_metadata)

    def test_version_parsing_with_pre_release(self):
        """测试带预发布版本的版本解析"""
        v = SemanticVersion("1.2.3-alpha.1")
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)
        self.assertIsNotNone(v.pre_release)

    def test_version_parsing_with_build_metadata(self):
        """测试带构建元数据的版本解析"""
        v = SemanticVersion("1.2.3+build.123")
        self.assertEqual(v.major, 1)
        self.assertEqual(v.minor, 2)
        self.assertEqual(v.patch, 3)
        self.assertIsNotNone(v.build_metadata)

    def test_equality(self):
        """测试版本相等性比较"""
        v1 = SemanticVersion("1.2.3")
        v2 = SemanticVersion("1.2.3")
        v3 = SemanticVersion("1.2.4")
        self.assertTrue(v1 == v2)
        self.assertFalse(v1 == v3)
        # 测试与字符串比较
        self.assertTrue(v1 == "1.2.3")
        self.assertFalse(v1 == "1.2.4")

    def test_less_than(self):
        """测试版本小于比较"""
        v1 = SemanticVersion("1.2.3")
        v2 = SemanticVersion("1.2.4")
        v3 = SemanticVersion("1.3.0")
        v4 = SemanticVersion("2.0.0")
        self.assertTrue(v1 < v2)
        self.assertTrue(v2 < v3)
        self.assertTrue(v3 < v4)
        # 测试与字符串比较
        self.assertTrue(v1 < "1.2.4")
        self.assertFalse(v2 < "1.2.3")

    def test_string_representation(self):
        """测试字符串表示"""
        v = SemanticVersion("1.2.3-alpha+build.123")
        self.assertEqual(str(v), "1.2.3a0+build.123")
        self.assertEqual(repr(v), "SemanticVersion('1.2.3a0+build.123')")


if __name__ == '__main__':
    unittest.main()
