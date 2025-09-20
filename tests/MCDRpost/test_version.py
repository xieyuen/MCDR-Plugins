import sys
import os
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# 修复导入路径
from src.MCDRpost.mcdrpost.utils.version import MinecraftVersion, SemanticVersion


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


class TestMinecraftVersion(unittest.TestCase):
    def test_regular_version(self):
        """测试正常的Minecraft版本"""
        v = MinecraftVersion("1.19.3")
        self.assertFalse(v.is_snapshot)
        self.assertEqual(str(v), "1.19.3")

    def test_snapshot_version_parsing(self):
        """测试快照版本解析"""
        v = MinecraftVersion("22w24a")
        self.assertTrue(v.is_snapshot)
        self.assertEqual(str(v), "22w24a")
        self.assertEqual(repr(v), "MinecraftVersion('22w24a')")

    def test_snapshot_version_mapping(self):
        """测试快照版本映射到正式版本"""
        v = MinecraftVersion("22w24a")
        # 22w24a 应该映射到 1.19.4 (根据映射表)
        # 这里我们验证映射版本存在
        self.assertIsNotNone(v.mapped_version)

    def test_snapshot_version_comparison(self):
        """测试快照版本比较"""
        v1 = MinecraftVersion("22w24a")
        v2 = MinecraftVersion("22w25a")
        self.assertTrue(v1 < v2)

    def test_mixed_version_comparison(self):
        """测试快照版本与正式版本比较"""
        # 根据映射表，22w24a 映射到 1.19.4
        snapshot = MinecraftVersion("22w24a")
        mapped_release = MinecraftVersion("1.19.4")
        older_release = MinecraftVersion("1.19.3")
        newer_release = MinecraftVersion("1.19.5")

        # 快照版本应该等于其映射的正式版本（根据__eq__方法）
        self.assertTrue(snapshot == mapped_release)
        # 快照版本应该大于旧版本
        self.assertTrue(snapshot > older_release)
        # 快照版本应该小于新版本
        self.assertTrue(snapshot < newer_release)

    def test_regular_version_comparison(self):
        """测试正常版本比较"""
        v1 = MinecraftVersion("1.19.2")
        v2 = MinecraftVersion("1.19.3")
        self.assertTrue(v1 < v2)
        self.assertTrue(v2 > v1)
        self.assertTrue(v1 == MinecraftVersion("1.19.2"))

    def test_version_equality_with_string(self):
        """测试版本与字符串的相等性比较"""
        v = MinecraftVersion("1.19.3")
        self.assertTrue(v == "1.19.3")

    def test_snapshot_version_equality_with_string(self):
        """测试快照版本与字符串的相等性比较"""
        v = MinecraftVersion("22w24a")
        self.assertTrue(v == "22w24a")


if __name__ == '__main__':
    unittest.main()
