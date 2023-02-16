
class Task:
    def __init__(self):
        self.description = ""
        self.embeddings: list = []

    def do_task(self): ...
