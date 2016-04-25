
class Reducer(object):

    def __init__(self, reduce_function, reduce_input):
        self.reduce_function = reduce_function
        self.reduce_input = reduce_input

    def run(self):
        return [self.reduce_function(w, s) for w, s in self.reduce_input]
