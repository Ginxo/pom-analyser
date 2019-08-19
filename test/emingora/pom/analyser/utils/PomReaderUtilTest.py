import unittest

from emingora.pom.analyser.GAV import GAV
from emingora.pom.analyser.utils.PomReaderUtil import PomReaderUtil


class PomReaderUtilTest(unittest.TestCase):
    def test_read_simple(self):
        # Act
        pom = PomReaderUtil.read('resources/simple_pom.xml')

        # Assert
        PomReaderUtilTest.check_gav(self, pom.gav, GAV, "io.missus.message-service", "api", "0.0.1-SNAPSHOT")
        self.assertEqual(None, pom.parent)

        self.assertEqual(3, len(pom.dependencies))
        PomReaderUtilTest.check_gav(self, pom.dependencies[0], GAV, "org.springframework", "spring-web")
        PomReaderUtilTest.check_gav(self, pom.dependencies[1], GAV, "io.projectreactor", "reactor-core")
        PomReaderUtilTest.check_gav(self, pom.dependencies[2], GAV, "org.projectlombok", "lombok")

        self.assertEqual(3, len(pom.dependencies_management))
        PomReaderUtilTest.check_gav(self, pom.dependencies_management[0], GAV, "org.springframework", "spring-web", "1")
        PomReaderUtilTest.check_gav(self, pom.dependencies_management[1], GAV, "io.projectreactor", "reactor-core", "2")
        PomReaderUtilTest.check_gav(self, pom.dependencies_management[2], GAV, "org.projectlombok", "lombok", "3",
                                    "sources")

        self.assertEqual(None, pom.children)

    def test_read_children1(self):
        # Act
        pom = PomReaderUtil.read('resources/children1_pom.xml')

        # Assert
        PomReaderUtilTest.check_gav(self, pom.gav, GAV, "io.missus.message-service", "api", "0.0.1-SNAPSHOT")
        PomReaderUtilTest.check_gav(self, pom.parent, GAV, "io.missus.message-service", "parent", "0.0.1-SNAPSHOT")

        self.assertEqual(3, len(pom.dependencies))
        PomReaderUtilTest.check_gav(self, pom.dependencies[0], GAV, "org.springframework", "spring-web")
        PomReaderUtilTest.check_gav(self, pom.dependencies[1], GAV, "io.projectreactor", "reactor-core")
        PomReaderUtilTest.check_gav(self, pom.dependencies[2], GAV, "org.projectlombok", "lombok")

        self.assertEqual(3, len(pom.dependencies_management))
        PomReaderUtilTest.check_gav(self, pom.dependencies_management[0], GAV, "org.springframework", "spring-web", "1")
        PomReaderUtilTest.check_gav(self, pom.dependencies_management[1], GAV, "io.projectreactor", "reactor-core", "2")
        PomReaderUtilTest.check_gav(self, pom.dependencies_management[2], GAV, "org.projectlombok", "lombok", "3",
                                    "sources")

        self.assertEqual(None, pom.children)

    def test_read_parent1(self):
        # Act
        pom = PomReaderUtil.read('resources/parent1_pom.xml')

        # Assert
        PomReaderUtilTest.check_gav(self, pom.gav, GAV, "io.missus.message-service", "parent", "0.0.1-SNAPSHOT")
        PomReaderUtilTest.check_gav(self, pom.parent, GAV, "org.springframework.boot", "spring-boot-starter-parent",
                                    "2.1.2.RELEASE")

        self.assertEqual(None, pom.dependencies)
        self.assertEqual(None, pom.dependencies_management)

        self.assertEqual(2, len(pom.children))

        # Check children 0
        PomReaderUtilTest.check_gav(self, pom.children[0].gav, GAV, "io.missus.message-service", "core", "0.0.1-SNAPSHOT")
        PomReaderUtilTest.check_gav(self, pom.children[0].parent, GAV, "io.missus.message-service", "parent", "0.0.1-SNAPSHOT")

        self.assertEqual(None, pom.children[0].dependencies)
        self.assertEqual(None, pom.children[0].dependencies_management)
        self.assertEqual(2, len(pom.children[0].children))

        # Check Children 0 - 0
        print(pom.children[0].children[0])
        PomReaderUtilTest.check_gav(self, pom.children[0].children[0].gav, GAV, "io.missus.message-service", "core-core", "0.0.1-SNAPSHOT")
        PomReaderUtilTest.check_gav(self, pom.children[0].children[0].parent, GAV, "io.missus.message-service", "core", "0.0.1-SNAPSHOT")

        self.assertEqual(15, len(pom.children[0].children[0].dependencies))
        self.assertEqual(None, pom.children[0].children[0].dependencies_management)
        self.assertEqual(None, pom.children[0].children[0].children)

        # Check Children 0 - 1
        print(pom.children[0].children[1])
        PomReaderUtilTest.check_gav(self, pom.children[0].children[1].gav, GAV, "io.missus.message-service", "core-api", "0.0.1-SNAPSHOT")
        PomReaderUtilTest.check_gav(self, pom.children[0].children[1].parent, GAV, "io.missus.message-service", "core", "0.0.1-SNAPSHOT")

        self.assertEqual(3, len(pom.children[0].children[1].dependencies))
        self.assertEqual(None, pom.children[0].children[1].dependencies_management)
        self.assertEqual(None, pom.children[0].children[1].children)


        # Check children 1
        PomReaderUtilTest.check_gav(self, pom.children[1].gav, GAV, "io.missus.message-service", "api", "0.0.1-SNAPSHOT")
        PomReaderUtilTest.check_gav(self, pom.children[1].parent, GAV, "io.missus.message-service", "parent", "0.0.1-SNAPSHOT")

        self.assertEqual(3, len(pom.children[1].dependencies))
        PomReaderUtilTest.check_gav(self, pom.children[1].dependencies[0], GAV, "org.springframework", "spring-web")
        PomReaderUtilTest.check_gav(self, pom.children[1].dependencies[1], GAV, "io.projectreactor", "reactor-core")
        PomReaderUtilTest.check_gav(self, pom.children[1].dependencies[2], GAV, "org.projectlombok", "lombok")
        self.assertEqual(None, pom.children[1].dependencies_management)
        self.assertEqual(None, pom.children[1].children)


    @staticmethod
    def check_gav(self, gav: GAV, instance_type, group_id: str, artifact_id: str, version: str = None,
                  classifier: str = None):
        self.assertTrue(isinstance(gav, instance_type))
        self.assertEqual(gav.group_id, group_id,
                         "expected group_id {0}, value {1}. {2}".format(gav.group_id, group_id, gav))
        self.assertEqual(gav.artifact_id, artifact_id,
                         "expected artifact_id {0}, value {1}. {2}".format(gav.artifact_id, artifact_id, gav))
        self.assertEqual(gav.version, version, "expected version {0}, value {1}. {2}".format(gav.version, version, gav))
        self.assertEqual(gav.classifier, classifier,
                         "expected classifier {0}, value {1}. {2}".format(gav.classifier, classifier, gav))
