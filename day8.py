import sys

# Read in values from provided file
values = [int(x) for x in open(sys.argv[1]).read().strip().split()]

# Class to represent a node in the tree, including its metadata
# Has a method to recursively compute the node's value, for Part 2
class Node:
    def __init__(self, num_children, num_metadata):
        self.num_children = num_children
        self.num_metadata = num_metadata
        self.children = []
        self.metadata = []
    def get_value(self):
        if self.num_children == 0:
            return sum(self.metadata)
        else:
            value = 0
            for d in self.metadata:
                if 1 <= d <= self.num_children:
                    value += self.children[d-1].get_value()
            return value

# Receives a list of values and parses the next node
# The children are parsed recursively.
def parseNode(values):
    global k
    num_children = values[k]
    num_metadata = values[k+1]
    k += 2
    node = Node(num_children, num_metadata)
    for i in range(num_children):
        child = parseNode(values)
        node.children.append(child)
    for i in range(num_metadata):
        data = values[k]
        node.metadata.append(data)
        k += 1
    nodes.append(node)
    return node

# k is a global index indicating position so far in the values array
k = 0
nodes = []

root = parseNode(values)

sum_metadata = 0
for node in nodes:
    sum_metadata += sum(node.metadata)

print("Part 1:", sum_metadata)

print("Part 2:", root.get_value())
