
class Task:
    def __init__(self):
        self.description = ""
        self.sub_tasks: list[Task] = []

    def do_task(self): ...
