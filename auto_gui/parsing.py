from auto_gui import progressing, error

class Parsing(object):
    def __init__(self, **data):
        self.script_path = data.get("script_path")
        self.script = data.get("script")

        if self.script == None:
            if self.script_path == None:
                raise Exception(error.MISSING_SCRIPT)
            
            self.read_script()

        self.parse()

    def read_script(self):
        with open(self.script_path, 'r') as f:
            self.script = f.readlines()

    def parse(self):
        progress = progressing.Progressing()
        for line in self.script:
            line.strip()

            part = line.split(" ")
            command = part[0]
            part.pop(0)
            progress = progress.pipeline(command, *part)

        self.progress = progress

        return self

    def run(self):
        self.progress.run()