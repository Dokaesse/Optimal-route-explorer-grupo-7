from segment import *
import matplotlib.pyplot as plt

class Graph:
    def __init__(self): #Inicializamos la clase
        self.nodes = []
        self.segments = []

    def add_node(self, n): #Añadimos nodos a nuestra lista de nodos
        i=0
        fin = False
        while i<len(self.nodes) and not fin:
            if self.nodes[i].name == n.name or (self.nodes[i].x == n.x and self.nodes[i].y == n.y):
                fin = True
            i+=1
        if not fin:
            self.nodes.append(n)
            print(n.name)
            return True
        else: return False

    def add_segment(self, name, name_origin, name_dest): #Añadimos los segmentos a la lista de segmentos
        i, org_position, dest_position = 0,0,0
        org_bolean, dest_bolean = False, False
        fin = False
        for node in self.nodes:
            if node.name == name_origin:
                org_position, org_bolean = i, True
            elif node.name == name_dest:
                dest_position, dest_bolean = i, True
            if org_bolean and dest_bolean:
                #print(org_position,  dest_position)
                fin = True
                break
            i+=1
        if fin:
            #print(f'entro como {name}')
            found = False
            for k in self.segments: #Filtramos si ya existe un segmento con el mismo nombre o si el segmento tiene los mismos nodos que otro segmento
                if k.name == name or (k.or_node.name == name_origin and k.dest_node.name == name_dest):
                    found = True
                    #print(f'Encontrado un segmento duplicado o que no deberia ya tiene otros elementos {k.name, k.or_node.name, k.dest_node.name}')
                    break
            if not found: #Si no se cumple alguna de las dos condiciones, entonces creamos el segmento y lo añadimos en la lista de segmentos al igual que a los nodos los hacemos vecinos
                origin = self.nodes[org_position]  # Con la posición encotramos el nodo en la lista de nodos
                destination = self.nodes[dest_position]
                existe = False
                for neight in origin.nodes:
                    if neight == destination:
                        existe = True
                        break
                if not existe:
                    origin.add_neighbor(destination)
                self.segments.append(Segment(name, origin, destination))
                #print(f'segmento {name} registrado')
                #print(len(self.segments))
                return True
        else:
            return False

    def info_nodo(self, name):
        for node in self.nodes:
            if node.name == name:
                print(f'Informacion del nodo: \n nombre: {node.name} posicion: {node.x}, {node.y} \n vecinos: {[neight.name for neight in node.nodes]}')
    def info_segmentos(self):
        for k in self.segments:
            print(k.name)
        print(len(self.segments))

    def plot(self, test=False):
        #print(len(self.nodes))
        #print(len(self.segments))
        fig, ax = plt.subplots()
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 25)
        ax.set_title('Gráfico con nodos y segmentos')
        for k in self.nodes:
            ax.scatter(k.x, k.y, color='red')
            ax.text(k.x+0.3,k.y+0.3, k.name, color='green', size=12)

        for segment in self.segments:
            #print(self.segments[segment].__dict__)
            #print(segment.name)
            x_org, y_org  = segment.or_node.x, segment.or_node.y
            x_dest,y_dest  = segment.dest_node.x, segment.dest_node.y
            vx,vy  = [x_org, x_dest], [y_org, y_dest]
            x_mid,y_mid  = (x_org + x_dest) / 2, (y_org + y_dest) / 2

            plt.plot(vx,vy,color='blue', marker='>', markersize=4)
            ax.text(x_mid, y_mid, round(segment.cost, 2), color='black', fontsize=10, ha='center', va='center')
        if test:
            plt.show()
        else:
            return fig, ax

    def get_closest(self, x , y):
        closest = 1000
        for node in self.nodes:
            distance = ((x - node.x)**2 + (y - node.y)**2)**1/2
            if distance<closest:
                closest, clo_node = distance, node
        print(f'El nodo mas cercano es {clo_node.name}')

    def plot_node(self, name, test=False):
        found, nodes, list_nodes = False, self.nodes, []
        fig, ax = plt.subplots()
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 25)
        for node in self.nodes:
            list_nodes.append(node)
            if node.name == name:
                found_node, found = node, True
                ax.scatter(found_node.x, found_node.y, color='blue')
                ax.text(found_node.x + 0.3, found_node.y + 0.3, found_node.name, color='black', size=12)
                list_nodes.remove(node)
        if found:
            for nei_node in found_node.nodes:
                print(nei_node.name)
                ax.scatter(nei_node.x,nei_node.y, color='green')
                ax.text(nei_node.x + 0.3, nei_node.y + 0.3, nei_node.name, color='black', size=12)
                list_nodes.remove(nei_node)
            print('-------------------------')
            for segment in self.segments:
                if segment.or_node.name == name:
                    print(name)
                    x_org, y_org = segment.or_node.x, segment.or_node.y
                    x_dest, y_dest = segment.dest_node.x, segment.dest_node.y
                    vx, vy = [x_org, x_dest], [y_org, y_dest]
                    x_mid, y_mid = (x_org + x_dest) / 2, (y_org + y_dest) / 2

                    ax.plot(vx, vy, color='red')
                    ax.text(x_mid, y_mid, round(segment.cost, 2), color='black', fontsize=10, ha='center', va='center')
            for node in list_nodes:
                ax.scatter(node.x, node.y, color='gray')
                ax.text(node.x+0.3,node.y+0.3, node.name, color='black', size=12)

            #plt.show()
            if test:
                plt.show()
            else:
                return fig, ax
        else:
            print('No he encontrado ese punto!!!')
            return False

    def save_flight_plan(self, file_name):
        f = open(file_name, 'w')
        f.write(f'Plan\n')
        for node in self.nodes:
            f.write(f'{node.name},{node.x},{node.y},{[neight.name for neight in node.nodes]}\n')
        print('acabado el guardado!')
        f.close()

    def load_flight_plan(self, file_name, popup):
        #fig, ax = plt.subplots()
        #ax.set_title('Gráfico con nodos y segmentos')
        try:
            f = open(file_name, 'r')
            lineas = f.readlines()
            f.close()
            nodos = []
            i = 1
            self.segments.clear()
            self.nodes.clear()
            for k in lineas[1:]:
                value = k.strip('\n').split(',', 3)
                neighbors_str = value[3].strip()[1:-1]  # Eliminar los corchetes '[' y ']'
                neighbors = [n.strip().strip("'") for n in neighbors_str.split(',')] if neighbors_str else []
                node = Node(value[0], float(value[1]), float(value[2]))
                node.nodes = neighbors
                self.add_node(node)
            for node in self.nodes:
                #print(node.name)
                #print(node.nodes)
                for i in range(len(node.nodes) -1, -1, -1):
                    #print(i)
                    self.add_segment(f'{node.name}{node.nodes[i]}', node.name, node.nodes[i])
                    node.nodes.remove(node.nodes[i])
                    #print(node.nodes)
            #print(self.nodes[1].nodes)
            self.info_nodo('A')
            self.info_segmentos()
            fig, ax = self.plot()
            return fig, ax
            #print(nodos)
            #plt.show()
            #return fig, ax
        except:
            return 'error', 'error'