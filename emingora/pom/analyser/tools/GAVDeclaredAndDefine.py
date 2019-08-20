from emingora.pom.analyser.entity.GAV import GAV
from emingora.pom.analyser.entity.Pom import Pom
from emingora.pom.analyser.utils.GAVUtils import GAVUtils


class GAVDeclaredAndDefine:

    @staticmethod
    def get_repeated_gavs(pom: Pom, found_dict: {} = {}, inherited_dep_management: [] = None) -> {}:
        dependencies_management = (pom.dependencies_management if pom.dependencies_management is not None else []) + \
                                  (inherited_dep_management if inherited_dep_management is not None else [])

        for dependency in dependencies_management:
            GAVDeclaredAndDefine.__check(dependency, pom.dependencies, found_dict)
            GAVDeclaredAndDefine.__check_children(pom, dependency, dependencies_management, found_dict)

        GAVDeclaredAndDefine.__check_parents(pom.dependencies_management, pom.parent, found_dict)
        return found_dict

    @staticmethod
    def __check(dependency: GAV, dependencies: [], found_dict: {}):
        for dep in dependencies if dependencies is not None else []:
            if GAVUtils.is_gav_equal_not_none_version(dependency, dep):
                GAVDeclaredAndDefine.__fill_found_dict(dependency, dep, found_dict)

    @staticmethod
    def __check_children(pom: Pom, dependency: GAV, dependencies_management: [], found_dict: {}):
        if pom.children is not None:
            for children in pom.children:
                GAVDeclaredAndDefine.__check(dependency, children.dependencies, found_dict)
                GAVDeclaredAndDefine.__check(dependency, children.dependencies_management, found_dict)
            for child in pom.children:
                GAVDeclaredAndDefine.get_repeated_gavs(child, found_dict, dependencies_management)

    @staticmethod
    def __check_parents(dependencies_management: [], parent_pom: Pom, found_dict: {}):
        if parent_pom is not None:
            for dependency_management in dependencies_management if dependencies_management is not None and parent_pom.dependencies is not None else []:
                GAVDeclaredAndDefine.__check(dependency_management, parent_pom.dependencies, found_dict)
            if parent_pom.parent is not None:
                GAVDeclaredAndDefine.__check_parents(dependencies_management, parent_pom.parent, found_dict)

    @staticmethod
    def __fill_found_dict(dependency1: GAV, dependency2: GAV, found_dict: {}):
        if found_dict.get(dependency1.belonging_pom.get_id()) is None:
            found_dict[dependency1.belonging_pom.get_id()] = {}

        project_key = found_dict.get(dependency1.belonging_pom.get_id())
        if project_key.get(dependency1.get_id()) is None:
            project_key[dependency1.get_id()] = []

        if dependency2 not in project_key.get(dependency1.get_id()):
            project_key.get(dependency1.get_id()).append(dependency2)
