from emingora.pom.analyser import GAV


class Pom:

    def __init__(self, gav: GAV, dependencies: [], dependencies_management: [], parent=None, children: [] = None):
        self.gav = gav
        self.dependencies = dependencies
        self.dependencies_management = dependencies_management
        self.parent = parent
        self.children = children

    def __repr__(self):
        return "GAV:{0}\nDEPENDENCIES:{1}\nDEPENDENCY_MANAGEMENT:{2}\nPARENT:{3}\nCHILDREN:{4}\n".format(self.gav, self.dependencies, self.dependencies_management, self.parent, self.children)
