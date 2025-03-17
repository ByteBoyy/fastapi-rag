class AppResource:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"AppResource(name={self.name})"