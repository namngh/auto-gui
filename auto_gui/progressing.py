from auto_gui import command, error


class Progressing(object):
    def __init__(self):
        self.pipes = []

    def pipeline(self, cmd, *params):
        self.pipes.append(command.Command(command=cmd, params=params))

        return self

    def run(self):
        if len(self.pipes) == 0:
            raise Exception(error.MISSING_PIPELINE)

        for pipe in self.pipes:
            pipe.exec()
