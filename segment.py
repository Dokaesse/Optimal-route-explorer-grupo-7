from node import *
class Segment:
    def __init__(self, name, or_node, dest_node):
        self.name = name
        self.origin = or_node
        self.dest = dest_node
        self.distance = distance(or_node, dest_node)


