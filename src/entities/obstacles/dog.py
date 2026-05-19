from import obstacles import Obstacles  

class Dog(Obstacles):
    def __init__(self, name):
        super().__init__(name)

    def describe(self):
        return f"Dog: {self.name}"

    