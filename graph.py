from segment import *
from node import distance
from path import *
import matplotlib.pyplot as plt
#Todas las funciónes que creamos no serán funciones, sino métodos de la clase Graph
class Graph:
    def __init__(self): #Inicializamos la clase
        self.nodes = []
        self.segments = []
        self.paths = []

    def add_node(self, n): #Añadimos nodos a nuestra lista de nodos
        i=0
        fin = False
        while i<len(self.nodes) and not fin:
            if self.nodes[i].name == n.name or (self.nodes[i].x == n.x and self.nodes[i].y == n.y):
                fin = True
            i+=1
        if not fin:
            self.nodes.append(n)
            #print(n.name)
            return True
        else: return False

    def add_segment(self, name, name_origin, name_dest): #Añadimos los segmentos a la lista de segmentos
        i, org_position, dest_position = 0,0,0
        org_bolean, dest_bolean = False, False
        fin = False
        for node in self.nodes: #Filtramos que existan tanto nodo de origen como destino
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
                    #print(f'Encontrado un segmento duplicado o que no debería ya tiene otros elementos {k.name, k.or_node.name, k.dest_node.name}')
                    break
            if not found: #Si no se cumple alguna de las dos condiciones, entonces creamos el segmento y lo añadimos en la lista de segmentos al igual que a los nodos los hacemos vecinos
                origin = self.nodes[org_position]  # Con la posición encontramos el nodo en la lista de nodos
                destination = self.nodes[dest_position]
                origin.add_neighbor(destination)
                self.segments.append(Segment(name, origin, destination))
                #print(f'segmento {name} registrado')
                #print(len(self.segments))
                return True
        else:
            return False

    def info_nodo(self, name): #función para pruebas
        for node in self.nodes:
            if node.name == name:
                print(f'Información del nodo: \n nombre: {node.name} posicion: {node.x}, {node.y} \n vecinos: {[neight.name for neight in node.nodes]}')
    def info_segmentos(self): ##función para pruebas
        for k in self.segments:
            print(k.name)
        print(len(self.segments))

    def plot(self, test=False): #Metodo para crear nuestros plots(el argumento test está por default en False)
        #print(len(self.nodes))
        #print(len(self.segments))
        fig, ax = plt.subplots() #Creamos subplot, lo necesitaremos para la interfaz
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 25)
        ax.set_title('Gráfico con nodos y segmentos')
        for k in self.nodes: #ponemos los nodos como puntos
            ax.scatter(k.x, k.y, color='red')
            ax.text(k.x+0.3,k.y+0.3, k.name, color='green', size=12)

        for segment in self.segments: # hacemos los segmentos de la lista de segmentos
            #print(self.segments[segment].__dict__)
            #print(segment.name)
            x_org, y_org  = segment.or_node.x, segment.or_node.y
            x_dest,y_dest  = segment.dest_node.x, segment.dest_node.y
            vx,vy  = [x_org, x_dest], [y_org, y_dest]
            x_mid,y_mid  = (x_org + x_dest) / 2, (y_org + y_dest) / 2
            ax.annotate('', xy=(x_dest, y_dest), xytext=(x_org, y_org), arrowprops=dict(arrowstyle='->', color='blue', lw=2))#con el marker le hacemos las flechas de dirección
            ax.text(x_mid, y_mid, round(segment.cost, 2), color='black', fontsize=10, ha='center', va='center') #Añadimos la distancia entre segmentos
        if test: #si test es True
            plt.show()
        else: #caso contrario
            return fig, ax

    def get_closest(self, x , y): #Nos da el punto de mas cercanía a un nodo
        closest = 1000
        for node in self.nodes:
            distance = ((x - node.x)**2 + (y - node.y)**2)**1/2
            if distance<closest:
                closest, clo_node = distance, node
        print(f'El nodo mas cercano es {clo_node.name}')

    def plot_node(self, name, test=False): #Metodo para mostrar información del nodo seleccionado
        found, nodes, list_nodes = False, self.nodes, []
        fig, ax = plt.subplots()
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 25)
        for node in self.nodes:
            list_nodes.append(node) #metemos todos los nodos en una lista
            if node.name == name:
                found_node, found = node, True
                ax.scatter(found_node.x, found_node.y, color='blue') #el nodo que queremos información lo ponemos en azul
                ax.text(found_node.x + 0.3, found_node.y + 0.3, found_node.name, color='black', size=12)
                list_nodes.remove(node) #borramos el nodo principal de la lista
        if found: #En caso de que el nodo que queremos información exista haremos el plot
            for nei_node in found_node.nodes:
                #print(nei_node.name)
                ax.scatter(nei_node.x,nei_node.y, color='green') #los nodos vecinos del principal en verde
                ax.text(nei_node.x + 0.3, nei_node.y + 0.3, nei_node.name, color='black', size=12)
                list_nodes.remove(nei_node) # los borramos de la lista
            #print('-------------------------')
            for segment in self.segments:
                if segment.or_node.name == name:
                    print(name)
                    x_org, y_org = segment.or_node.x, segment.or_node.y
                    x_dest, y_dest = segment.dest_node.x, segment.dest_node.y
                    vx, vy = [x_org, x_dest], [y_org, y_dest]
                    x_mid, y_mid = (x_org + x_dest) / 2, (y_org + y_dest) / 2
                    ax.annotate('', xy=(x_dest, y_dest), xytext=(x_org, y_org), arrowprops=dict(arrowstyle='->', color='red', lw=2)) #hacemos los segmentos que los unen
                    ax.text(x_mid, y_mid, round(segment.cost, 2), color='black', fontsize=10, ha='center', va='center')
            for node in list_nodes: #finalmente los nodos restantes en la lista son los que no son ni el principal ni los vecinos por tanto los ponemos en gris
                ax.scatter(node.x, node.y, color='gray')
                ax.text(node.x+0.3,node.y+0.3, node.name, color='black', size=12)
            if test: #en caso de que sea un test el argumento será true, por default es False
                plt.show()
            else:
                return fig, ax #nos devuelve lo necesario para mostrarlo en la interfaz
        else:
            return False

    def save_flight_plan(self, file_name): #Función para guardar nuestro plan de vuelo en un archivo
        f = open(file_name, 'w') #buscamos el archivo(si no existe lo creará)
        f.write(f'Plan\n')
        for node in self.nodes: # por cada punto escribimos la información necesaria: nombre, posicion(x e y) y nodos vecinos(necesarios para hacer los segmentos)
            f.write(f'{node.name},{node.x},{node.y},{[neight.name for neight in node.nodes]}\n')
        print('acabado el guardado!')
        f.close()

    def load_flight_plan(self, file_name): #Cargamos el plan de vuelo
        try: #intentamos encontrar el archivo
            f = open(file_name, 'r')
            lineas = f.readlines()
            f.close()
            self.segments.clear()
            self.nodes.clear()
            for k in lineas[1:]: #leeremos cada línea del archivo para configurar el plot
                value = k.strip('\n').split(',', 3)
                neighbors_str = value[3].strip()[1:-1]  # Eliminar los corchetes '[' y ']'
                neighbors = [n.strip().strip("'") for n in neighbors_str.split(',')] if neighbors_str else []
                node = Node(value[0], float(value[1]), float(value[2]))
                node.nodes = neighbors
                self.add_node(node) # añadimos los nodos y una lista de vecinos(estos serán ahora mismo el nombre del nodo no el objeto+
            for node in self.nodes:
                #print(node.name)
                #print(node.nodes)
                for i in range(len(node.nodes) -1, -1, -1):
                    #print(i)
                    self.add_segment(f'{node.name}{node.nodes[i]}', node.name, node.nodes[i]) #con este código iremos uno a uno en cada nodo a sus vecinos y substituiremos el nombre del nodo vecino por el nodo en sí, llamando a la función de añadir segmento que se encarga de ello
                    node.nodes.remove(node.nodes[i])
            self.info_nodo('A')
            self.info_segmentos()
            fig, ax = self.plot()
            return fig, ax
        except: #En caso de error devolveremos 'error' y 'error', normalmente el error está en que no existe el archivo que queremos leer
            return 'error', 'error'

    def find_shortest_path(self, origin, destination):
        origin_node, destination_node, fin, previous_node = '', '', False, None

        for node in self.nodes:
            if node.name == origin:
                origin_node = node
            elif node.name == destination:
                destination_node = node
            if origin_node and destination_node:
                fin = True
                break
        if not fin:
            print("Origen o destino no encontrado.")
            return

        final_path = False
        last_node = origin_node
        path_follower = []

        while not final_path:
            for neight in last_node.nodes:
                if neight != previous_node:
                    if not path_follower:
                        current_path = [origin_node, neight]
                    else:
                        current_path = path_follower.copy()
                        current_path.append(neight)
                    distancia = 0
                    for i in range(len(current_path) - 1):
                        distancia += distance(current_path[i], current_path[i + 1])
                    p = Path(last_node, neight, distancia, current_path)
                    self.paths.append(p)

            if not self.paths:
                print("No hay camino disponible hacia el destino.")
                return 'error', 'error'

            # Ordenamos los caminos por la distancia estimada total al destino
            self.paths.sort(key=lambda path: path.distance + distance(path.destino, destination_node))

            # Seleccionamos el mejor camino (ya es el primero)
            last_path = self.paths[0]
            last_node = last_path.destino

            for path in self.paths:
                camino_array = [node.name for node in path.camino]
                print(camino_array, path.distance, path.distance + distance(path.destino, destination_node))
            print('-------------------------')

            if last_node.name == destination_node.name:
                final_path = True
            else:
                self.paths.pop(0)  # Quitamos el primero porque ya lo usamos
                previous_node = last_path.inicio
                path_follower = last_path.camino

        print("Camino encontrado:")
        fig, ax = last_path.path_plot(self)
        self.paths.clear()  #Borramos todos los elementos de paths para la busqueda del siguente camino
        return fig, ax
