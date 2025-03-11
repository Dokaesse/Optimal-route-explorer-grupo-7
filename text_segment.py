from segment import *

n1 = Node('aaa', 2, 2)
n2 = Node('bbb', 3, 3)
n3 = Node('ccc', 4, 4)

s1 = Segment('n1 to n2', n1, n2)
s2 = Segment('n2 to n3', n2, n3)

print(n1.__dict__)
print(n2.__dict__)
print(n3.__dict__)
print(s1.__dict__)
print(s2.__dict__)


