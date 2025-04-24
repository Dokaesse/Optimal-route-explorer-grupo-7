from path import *
from test_graph import *
p = Path('A', 'D', )
#No funciona
p.add_node_path('A',g)
p.add_node_path('B',g)
p.add_node_path('C',g)
p.add_node_path('D',g)
p.add_node_path('D',g)
if p.contains_node('D'):
    print('Está')
else: print('no está')

p.path_plot(g)