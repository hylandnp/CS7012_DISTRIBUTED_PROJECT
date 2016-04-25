
class Mapper(object):

    def __init__(self, map_function, map_input):
        self.map_function = map_function
        self.map_input = map_input

    def run(self):
        return map(self.map_function, self.map_input)
