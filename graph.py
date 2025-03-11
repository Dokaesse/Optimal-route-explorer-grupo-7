import math

from segment import *
import matplotlib.pyplot as plt

class Graph:
    def __init__(self): #Inicializamos la clase
        self.nodes = []
        self.segments = []
    def add_node(self, n): #Añadimos nodos a nuestra lista de nodos
        if not n in self.nodes: #Si ya existe el nodo en la lista no lo duplicamos
            self.nodes.append(n)
        '''
        i=0
        fin = False
        while i<len(self.nodes) and not fin:
            if self.nodes[i] == n:
                fin = True
            i+=1
        if not fin:
            self.nodes.append(n)
            return True
        else: return False
        '''
    def add_segment(self, name, name_origin, name_dest): #Añadimos los segmentos a la lista de segmentos
        i, org_position, dest_position = 0,0,0
        org_bolean, dest_bolean = False, False
        fin = False
        if name_dest<name_origin: #ordenamos alfabeticamente los nodos de destino y origen para poder despúes filtrar
            name_dest, name_origin = name_origin, name_dest
        while i<len(self.nodes) and not fin: # Buscador para encontrar con los nombres proporcionados, la posición del nodo inicial y final.
            if self.nodes[i].name == name_origin:
                org_position = i
                org_bolean = True
            elif self.nodes[i].name == name_dest:
                dest_position = i
                dest_bolean = True
            if org_bolean and dest_bolean:
                fin = True
                print(org_position,  dest_position)
            i+=1
        if fin:
            found = False
            for k in self.segments: #Filtramos si ya existe un segmento con el mismo nombre o si el segmento tiene los mismos nodos que otro segmento
                if k.name == name or (k.or_node.name == name_origin and k.dest_node.name == name_dest):
                    found = True
                    break
            if not found: #Si no se cumple alguna de las dos condiciones, entonces creamos el segmento y lo añadimos en la lista de segmentos al igual que a los nodos los hacemos vecinos
                origin = self.nodes[org_position]  # Con la posición encotramos el nodo en la lista de nodos
                destination = self.nodes[dest_position]
                origin.add_neighbor(destination)
                destination.add_neighbor(origin)
                self.segments.append(Segment(name, origin, destination))
                return True
        else:
            return False
    def plot(self):
        print(len(self.nodes))
        print(len(self.segments))
        fig, ax = plt.subplots()
        ax.set_title('Gráfico con nodos y segmentos')
        for k in self.nodes:
            ax.scatter(k.x, k.y, color='red')
            ax.text(k.x+0.3,k.y+0.3, k.name, color='green', size=12)

        for segment in self.segments:
            #print(self.segments[segment].__dict__)
            x_org, y_org  = segment.or_node.x, segment.or_node.y
            x_dest,y_dest  = segment.dest_node.x, segment.dest_node.y
            vx,vy  = [x_org, x_dest], [y_org, y_dest]
            x_mid,y_mid  = (x_org + x_dest) / 2, (y_org + y_dest) / 2

            plt.plot(vx,vy,color='blue')
            ax.text(x_mid, y_mid, round(segment.cost, 2), color='black', fontsize=10, ha='center', va='center')
        plt.show()
