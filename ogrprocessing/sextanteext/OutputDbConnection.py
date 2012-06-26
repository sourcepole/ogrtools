from sextante.outputs.Output import Output

class OutputDbConnection(Output):

    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.value = None
        self.hidden = True
