import unittest

from emingora.pom.analyser.tools.RepeatedGAVS import RepeatedGAVS
from emingora.pom.analyser.utils.PomReaderUtil import PomReaderUtil


class CheckRepeatedGAVTest(unittest.TestCase):
    def test_true(self):
        # Arrange
        pom = PomReaderUtil.read('resources/noRepeatedDependency_pom.xml')

        # Act
        result = RepeatedGAVS.get_repeated_gavs(pom)

        # Assert
        self.assertEqual(0, len(result))

    def test_false(self):
        # Arrange
        pom = PomReaderUtil.read('resources/withRepeatedDependency_pom.xml')

        # Act
        result = RepeatedGAVS.get_repeated_gavs(pom)

        # Assert
        self.assertEqual(1, len(result))
        self.assertEqual("org.springframework", result[0].group_id)
        self.assertEqual("spring-web", result[0].artifact_id)
        self.assertEqual("1", result[0].version)
        self.assertEqual(None, result[0].classifier)
