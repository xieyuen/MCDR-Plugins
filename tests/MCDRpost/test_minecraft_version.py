from mcdrpost.utils.version import MinecraftVersion, SemanticVersion


import unittest

class TestMinecraftVersion(unittest.TestCase):
    latestMinecraftVersion = MinecraftVersion('26.1-snapshot-1')

    def test_initialize(self):
        ver = MinecraftVersion('1.19.4')
        self.assertEqual(ver.major, 1)
        self.assertEqual(ver.minor, 19)
        self.assertEqual(ver.patch, 4)
        self.assertEqual(ver.pre_release, None)
        self.assertEqual(ver.build_metadata, None)
        self.assertEqual(ver.version, SemanticVersion('1.19.4'))

        ver = self.latestMinecraftVersion

        self.assertEqual(ver.major, 26)
        self.assertEqual(ver.minor, 1)
        self.assertEqual(ver.patch, 1)
        self.assertEqual(ver.pre_release, 'snapshot-1')
        self.assertEqual(ver.build_metadata, None)


    def test_compare(self):
        self.assertLess(MinecraftVersion('1.19.4'), MinecraftVersion('1.19.5'))
        self.assertLess(MinecraftVersion('1.19.4'), SemanticVersion('1.19.5'))
        self.assertLess(MinecraftVersion('1.19.4'), MinecraftVersion('1.19.5-prerelease'))
        self.assertGreater(MinecraftVersion('1.19.5'), MinecraftVersion('1.19.5-prerelease'))
        self.assertGreater(MinecraftVersion('1.19.5'), (1,19,5, "prerelease", "build.info"))
        self.assertGreater(MinecraftVersion('1.19.5'), (1,19,5, "prerelease"))
        self.assertGreater(MinecraftVersion('1.19.5'), "1.19.5-prerelease+build")

        # test new version naming system
        self.assertGreater(MinecraftVersion('26.1-prerelease-1'), MinecraftVersion('1.19.0'))

if __name__ == '__main__':
    unittest.main()
