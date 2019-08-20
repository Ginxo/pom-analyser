import unittest

from emingora.pom.analyser.tools.GAVDeclaredAndDefine import GAVDeclaredAndDefine
from emingora.pom.analyser.utils.PomReaderUtil import PomReaderUtil


class GAVDeclaredAndDefineTest(unittest.TestCase):
    def test_simple(self):
        # Arrange
        pom = PomReaderUtil.read('resources/dep_management/pom.xml')

        # Act
        result = GAVDeclaredAndDefine.get_repeated_gavs(pom)

        # Assert
        self.assertEqual(2, len(result))

        result_project1 = result[list(result.keys())[0]]
        result_project2 = result[list(result.keys())[1]]
        self.assertEqual(3, len(result_project1))
        self.assertEqual(1, len(result_project2))

        GAVDeclaredAndDefineTest.check_dep(self, result_project1, "group1:artifact1:1:None", "org.drools:drools-bom:0.0.1-SNAPSHOT:None", 1, 0, 0)
        GAVDeclaredAndDefineTest.check_dep(self, result_project1, "group3:artifact3:3:None", "org.drools:drools-bom:0.0.1-SNAPSHOT:None", 1, 1, 0)
        GAVDeclaredAndDefineTest.check_dep(self, result_project1, "group8:artifact8:8:None", "org.test:test-parent:0.0.1-SNAPSHOT:None", 1, 2, 0)

        GAVDeclaredAndDefineTest.check_dep(self, result_project2, "group2:artifact2:2:None", "org.test:test-parent:0.0.1-SNAPSHOT:None", 1, 0, 0)

    def test_true(self):
        # Arrange
        pom = PomReaderUtil.read('resources/kie/pom.xml')

        # Act
        result = GAVDeclaredAndDefine.get_repeated_gavs(pom)

        # Assert
        self.assertTrue(True)

    @staticmethod
    def check_dep(self, project, expected_dep_id, expected_belonging_id, expected_dep_len, dep_index, dep2_index):
        project_dep = project[list(project.keys())[dep_index]]
        self.assertEqual(expected_dep_len, len(project_dep))
        self.assertEqual(expected_dep_id, project_dep[dep2_index].get_id())
        self.assertEqual(expected_belonging_id, project_dep[dep2_index].belonging_pom.get_id())
