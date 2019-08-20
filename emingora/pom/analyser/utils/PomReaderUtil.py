#
# parsing maven pom.xml
# artifactId & version
#
import os
from xml.etree import ElementTree

from emingora.pom.analyser.entity.GAV import GAV
from emingora.pom.analyser.entity.Pom import Pom

XMLNS = 'xmlns'
POM_XMLNS = 'http://maven.apache.org/POM/4.0.0'
XMLNS_DEPENDENCY_MANAGEMENT = ".//" + XMLNS + ":dependencyManagement"
XMLNS_DEPENDENCIES = XMLNS + ":dependencies"
XMLNS_PARENT = XMLNS + ":parent"
XMLNS_MODULES = XMLNS + ":modules"
XMLNS_GROUP_ID = XMLNS + ":groupId"
XMLNS_ARTIFACT_ID = XMLNS + ":artifactId"
XMLNS_VERSION = XMLNS + ":version"
XMLNS_CLASSIFIER = XMLNS + ":classifier"
NAMESPACES = {XMLNS: POM_XMLNS}


class PomReaderUtil:

    @staticmethod
    def read(pom_file_path: str, parent_pom: Pom = None) -> Pom:
        print("Reading pom file [{0}]".format(pom_file_path))
        tree = ElementTree.parse(pom_file_path)
        root = tree.getroot()

        parent = PomReaderUtil.__read_parent_gav(root) if parent_pom is None else parent_pom
        pom_gav = PomReaderUtil.__read_pom_gav(root, parent)
        dependencies = PomReaderUtil.__read_dependencies(root, pom_gav)
        dependency_management = PomReaderUtil.__read_dependency_management(root, pom_gav)

        pom = Pom(pom_gav, dependencies, dependency_management, parent)
        pom.children = PomReaderUtil.__read_children(root, os.path.dirname(pom_file_path), pom)
        return pom

    @staticmethod
    def __read_parent_gav(root) -> Pom:
        pom_gav = PomReaderUtil.__read_pom_gav(root.find(XMLNS_PARENT, namespaces=NAMESPACES), None) \
            if root.find(XMLNS_PARENT, namespaces=NAMESPACES) is not None else None
        return Pom(pom_gav, None, None) if pom_gav is not None else None

    @staticmethod
    def __read_pom_gav(root, parent) -> GAV:
        group_id = root.find(XMLNS_GROUP_ID, namespaces=NAMESPACES).text \
            if root.find(XMLNS_GROUP_ID, namespaces=NAMESPACES) is not None \
            else parent.gav.group_id if parent is not None else None
        artifact_id = root.find(XMLNS_ARTIFACT_ID, namespaces=NAMESPACES).text

        version = root.find(XMLNS_VERSION, namespaces=NAMESPACES).text \
            if root.find(XMLNS_VERSION, namespaces=NAMESPACES) is not None \
            else parent.gav.version if parent is not None else None
        return GAV(group_id, artifact_id, version)

    @staticmethod
    def __read_dependency_management(root, belonging_pom: GAV) -> []:
        return PomReaderUtil.__read_dependencies(
            root.find(XMLNS_DEPENDENCY_MANAGEMENT, namespaces=NAMESPACES), belonging_pom
        ) if root.find(XMLNS_DEPENDENCY_MANAGEMENT, namespaces=NAMESPACES) is not None else None

    @staticmethod
    def __read_dependencies(root, belonging_pom: GAV) -> []:
        return PomReaderUtil.__read_dependency(
            list(root.find(XMLNS_DEPENDENCIES, namespaces=NAMESPACES)), belonging_pom
        ) if root.find(XMLNS_DEPENDENCIES, namespaces=NAMESPACES) is not None else None

    @staticmethod
    def __read_dependency(dependency_tree, belonging_pom: GAV) -> []:
        dependencies = []
        for d in dependency_tree:
            group_id = d.find(XMLNS_GROUP_ID, namespaces=NAMESPACES).text
            artifact_id = d.find(XMLNS_ARTIFACT_ID, namespaces=NAMESPACES).text
            version = d.find(XMLNS_VERSION, namespaces=NAMESPACES).text \
                if d.find(XMLNS_VERSION, namespaces=NAMESPACES) is not None else None
            classifier = d.find(XMLNS_CLASSIFIER, namespaces=NAMESPACES).text \
                if d.find(XMLNS_CLASSIFIER, namespaces=NAMESPACES) is not None else None
            dependencies.append(GAV(group_id, artifact_id, version, classifier, belonging_pom))
        return dependencies

    @staticmethod
    def __read_children(root, base_dir, parent_pom: Pom) -> []:
        if root.find(XMLNS_MODULES, namespaces=NAMESPACES) is not None:
            children = []
            modules = root.find(XMLNS_MODULES, namespaces=NAMESPACES)
            for module in modules:
                children.append(PomReaderUtil.read("{0}/{1}/{2}".format(base_dir, module.text, "pom.xml"), parent_pom))
            return children
        else:
            return None
