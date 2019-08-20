from emingora.pom.analyser.entity.Pom import Pom
from emingora.pom.analyser.utils.GAVUtils import GAVUtils


class RepeatedGAVS:
    @staticmethod
    def get_repeated_gavs(pom: Pom) -> []:
        gavs = []
        for i in range(len(pom.dependencies)):
            for dependency_j in pom.dependencies[(i + 1):]:
                if GAVUtils.check_gav(pom.dependencies[i], dependency_j):
                    gavs.append(dependency_j)
                    break
        return gavs
