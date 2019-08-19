class GAV:
    def __init__(self, group_id: str, artifact_id: str, version: str, classifier: str = None):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.classifier = classifier

    def __repr__(self):
        return "{0}:{1}:{2}:{3}".format(self.group_id, self.artifact_id, self.version, self.classifier)
