import unittest

from emingora.pom.analyser.GAV import GAV
from emingora.pom.analyser.utils.GAVUtils import GAVUtils


class GAVUtilsTest(unittest.TestCase):

    def test_simple_equal(self):
        # Arrange
        gav1 = GAV("g1", "a1", "1", "c1")
        gav2 = GAV("g1", "a1", "2", "c1")

        # Act
        result = GAVUtils.is_gav_equal_not_none_version(gav1, gav2)

        # Assert
        self.assertTrue(result)

    def test_none_version_equal(self):
        # Arrange
        gav1 = GAV("g1", "a1", None, "c1")
        gav2 = GAV("g1", "a1", "2", "c1")

        # Act
        result = GAVUtils.is_gav_equal_not_none_version(gav1, gav2)

        # Assert
        self.assertFalse(result)

    def test_both_none_version_equal(self):
        # Arrange
        gav1 = GAV("g1", "a1", None, "c1")
        gav2 = GAV("g1", "a1", None, "c1")

        # Act
        result = GAVUtils.is_gav_equal_not_none_version(gav1, gav2)

        # Assert
        self.assertFalse(result)

    def test_not_equal(self):
        # Arrange
        gav1 = GAV("g1", "a1", "1", "c1")
        gav2 = GAV("g2", "a1", "1", "c1")

        # Act
        result = GAVUtils.is_gav_equal_not_none_version(gav1, gav2)

        # Assert
        self.assertFalse(result)
