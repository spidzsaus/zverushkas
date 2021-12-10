class Category:
    def __init__(self, default=None):
        self.default = default
    
    def __getattr__(self, value):
        return self.default
    
    def __str__(self):
        output = ''
        for key, value in self.__dict__.items():
            output += f'| {key}: \t {value}' '\n'
        return output
    
    def copy(self):
        c = Category()
        for key, value in self.__dict__.items():
            c.__setattr__(key, value)
        return c

class Enum:
    def __init__(self, *modes):
        self.indexes = []
        for mode in modes:
            obj = object()
            self.__setattr__(mode, obj)
            self.indexes.append(obj)

    def __getitem__(self, value):
        return self.indexes[value]