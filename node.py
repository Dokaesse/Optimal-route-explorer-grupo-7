import math
class Node:
    def __init__(self, name,  x, y): #Inicializamos la clase
        self.name = name
        self.lon = x
        self.lat = y
        self.vecinos = []

    def add_neight(self, n_node): #Añadimos vecinos al nodo y filtramos si ya el vecino que queremos poner(Inservible ya que se hace la comprovación en graph.py)
        self.vecinos.append(n_node)
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
    """
    Calcula la distancia Haversine entre dos puntos con atributos .lat y .lon
    """
    R = 6371  # Radio de la Tierra en kilómetros

    lat1, lon1 = math.radians(n1.lat), math.radians(n1.lon)
    lat2, lon2 = math.radians(n2.lat), math.radians(n2.lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Resultado en kilómetros

