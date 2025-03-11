from node import *
class Segment:
    def __init__(self, name, or_node, dest_node):
        self.name = name
        self.or_node = or_node
        self.dest_node = dest_node
        self.cost = distance(or_node, dest_node)


