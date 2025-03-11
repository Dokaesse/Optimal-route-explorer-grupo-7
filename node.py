class Node:
    def __init__(self, name,  x, y): #Inicializamos la clase
        self.name = name
        self.x = x
        self.y = y
        self.nodes = []

    def add_neighbor(self, n_node): #Añadimos vecinos al nodo y filtramos si ya el vecino que queremos poner(Inservible ya que se hace la comprovación en graph.py)
        self.nodes.append(n_node)
        '''
        i=0
        fin = False
        while i<(len(self.nodes)) and not fin:
            if self.nodes[i] == n_node:
                fin = True
            i+=1
        if not fin:
            self.nodes.append(n_node)
            return True
        else:
            #print('Ya existe este punto!!')
            return False
        '''
    def distance(self, n_node):
        dist = ((n_node.x - self.x)**2 + (n_node.y - self.y)**2)**0.5
        return dist

def distance(n1,n2):
    dist = ((n2.x - n1.x) ** 2 + (n2.y - n1.y) ** 2) ** 0.5
    return dist

