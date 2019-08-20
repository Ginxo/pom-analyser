from emingora.pom.analyser.entity.GAV import GAV


class GAVUtils:

    @staticmethod
    def check_gav(gav1: GAV, gav2: GAV) -> bool:
        return gav1.group_id == gav2.group_id and gav1.artifact_id == gav2.artifact_id \
               and gav1.version == gav2.version and gav1.classifier == gav2.classifier

    @staticmethod
    def is_gav_equal_not_none_version(gav1: GAV, gav2: GAV) -> bool:
        return gav1.group_id == gav2.group_id and gav1.artifact_id == gav2.artifact_id \
               and gav1.version is not None and gav2.version is not None and gav1.classifier == gav2.classifier
