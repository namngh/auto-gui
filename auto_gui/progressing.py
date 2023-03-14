from .command import Command
from .error import MISSING_PIPELINE


class Progressing(object):
    def __init__(self):
        self.pipes = []

    def pipeline(self, cmd, *params):
        self.pipes.append(Command(command=cmd, params=params))

        return self

    def run(self):
        if len(self.pipes) == 0:
            raise Exception(MISSING_PIPELINE)

        for pipe in self.pipes:
            pipe.exec()
