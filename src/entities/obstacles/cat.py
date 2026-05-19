from obstacles import Obstacles

class Cat(Obstacles):
    def __init__(self, name):
        super().__init__(name)

    def describe(self):
        return f"Cat: {self.name}"