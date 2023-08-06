import json

import humps


class LiveSourceLocation(object):
    def __init__(self, source, line):
        self.source = source
        self.line = line
        self.commitId = None
        self.fileChecksum = None

    def __eq__(self, other):
        if isinstance(other, LiveSourceLocation):
            return self.source == other.source \
                   and self.line == other.line \
                   and self.commitId == other.commitId \
                   and self.fileChecksum == other.fileChecksum
        return False

    def to_json(self):
        return json.dumps(self, default=lambda o: humps.camelize(o.__dict__))

    @classmethod
    def from_json(cls, json_str):
        json_dict = humps.decamelize(json.loads(json_str))
        return LiveSourceLocation(json_dict["source"], json_dict["line"])
