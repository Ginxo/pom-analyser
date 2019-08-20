from emingora.pom.analyser.entity import GAV
from emingora.pom.analyser.entity.Pom import Pom


class PomBuilder:

    def __init__(self, gav: GAV):
        self.__gav = gav
        self.__dependencies = []
        self.__dependencies_management = []

    def add_dependency(self, gav: GAV):
        self.__dependencies.append(gav)
        return self

    def add_dependencies_management(self, gav: GAV):
        self.__dependencies_management.append(gav)
        return self

    def build(self) -> Pom:
        return Pom(self.__gav, self.__dependencies, self.__dependencies_management)
