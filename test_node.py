from node import *
n1 = Node ('aaa', 0, 0)
n2 = Node ('bbb', 3, 4)
print (n1.distance(n2))
print (n1.add_neighbor(n2))
print (n1.add_neighbor(n2))
print (n1.__dict__)
for n in n1.nodes:
    print ( n.__dict__)