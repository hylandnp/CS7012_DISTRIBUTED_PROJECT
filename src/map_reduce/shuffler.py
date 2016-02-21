
class Shuffler(object):

    def __init__(self, group_function, group_input):
        self.group_function = group_function
        self.group_input = group_input

    def run(self):
        return self.group_function(self.group_input)
