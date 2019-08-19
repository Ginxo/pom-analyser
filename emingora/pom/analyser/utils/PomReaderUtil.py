#
# parsing maven pom.xml
# artifactId & version
#
import os
from xml.etree import ElementTree

from emingora.pom.analyser.GAV import GAV
from emingora.pom.analyser.Pom import Pom


class PomReaderUtil:
    namespaces = {'xmlns': 'http://maven.apache.org/POM/4.0.0'}

    @staticmethod
    def read(pom_file_path: str) -> Pom:
        print("Reading pom file [{0}]".format(pom_file_path))
        tree = ElementTree.parse(pom_file_path)
        root = tree.getroot()
        parent = PomReaderUtil.__read_parent_gav(root)
        gav = PomReaderUtil.__read_gav(root, parent)
        dependencies = PomReaderUtil.__read_dependencies(root)
        dependency_management = PomReaderUtil.__read_dependency_management(root)
        children = PomReaderUtil.__read_children(root, os.path.dirname(pom_file_path))
        return Pom(gav, dependencies, dependency_management, parent, children)

    @staticmethod
    def __read_parent_gav(root) -> GAV:
        return PomReaderUtil.__read_gav(root.find("xmlns:parent", namespaces=PomReaderUtil.namespaces), None) \
            if root.find("xmlns:parent", namespaces=PomReaderUtil.namespaces) is not None else None

    @staticmethod
    def __read_gav(root, parent) -> GAV:
        group_id = root.find("xmlns:groupId", namespaces=PomReaderUtil.namespaces).text \
            if root.find("xmlns:groupId", namespaces=PomReaderUtil.namespaces) is not None \
            else parent.group_id if parent is not None else None
        artifact_id = root.find("xmlns:artifactId", namespaces=PomReaderUtil.namespaces).text

        version = root.find("xmlns:version", namespaces=PomReaderUtil.namespaces).text \
            if root.find("xmlns:version", namespaces=PomReaderUtil.namespaces) is not None \
            else parent.version if parent is not None else None
        return GAV(group_id, artifact_id, version)

    @staticmethod
    def __read_dependency_management(root) -> []:
        return PomReaderUtil.__read_dependencies(
            root.find(".//xmlns:dependencyManagement", namespaces=PomReaderUtil.namespaces)
        ) if root.find(".//xmlns:dependencyManagement", namespaces=PomReaderUtil.namespaces) is not None else None

    @staticmethod
    def __read_dependencies(root) -> []:
        return PomReaderUtil.__read_dependency(
            list(root.find("xmlns:dependencies", namespaces=PomReaderUtil.namespaces))
        ) if root.find("xmlns:dependencies", namespaces=PomReaderUtil.namespaces) is not None else None

    @staticmethod
    def __read_dependency(dependency_tree) -> []:
        dependencies = []
        for d in dependency_tree:
            group_id = d.find("xmlns:groupId", namespaces=PomReaderUtil.namespaces).text
            artifact_id = d.find("xmlns:artifactId", namespaces=PomReaderUtil.namespaces).text
            version = d.find("xmlns:version", namespaces=PomReaderUtil.namespaces).text \
                if d.find("xmlns:version", namespaces=PomReaderUtil.namespaces) is not None else None
            classifier = d.find("xmlns:classifier", namespaces=PomReaderUtil.namespaces).text \
                if d.find("xmlns:classifier", namespaces=PomReaderUtil.namespaces) is not None else None
            dependencies.append(GAV(group_id, artifact_id, version, classifier))
        return dependencies

    @staticmethod
    def __read_children(root, base_dir) -> []:
        if root.find("xmlns:modules", namespaces=PomReaderUtil.namespaces) is not None:
            children = []
            modules = root.find("xmlns:modules", namespaces=PomReaderUtil.namespaces)
            for module in modules:
                children.append(PomReaderUtil.read("{0}/{1}/{2}".format(base_dir, module.text, "pom.xml")))
            return children
        else:
            return None
