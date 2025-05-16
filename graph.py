from segment import *
from navSegments import *
#from node import distance
from path import *
import matplotlib.pyplot as plt
import math
#Todas las funciónes que creamos no serán funciones, sino métodos de la clase Graph
class Graph:
    def __init__(self): #Inicializamos la clase
        self.nodes = []
        self.segments = []
        self.airports = []
        self.paths = []

    def add_node(self, n): #Añadimos nodos a nuestra lista de nodos
        i=0
        fin = False
        while i<len(self.nodes) and not fin:
            if self.nodes[i].name == n.name or (self.nodes[i].lon == n.lon and self.nodes[i].lat == n.lat):
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
                if k.name == name or (k.origin.name == name_origin and k.dest.name == name_dest):
                    found = True
                    #print(f'Encontrado un segmento duplicado o que no debería ya tiene otros elementos {k.name, k.or_node.name, k.dest_node.name}')
                    break
            if not found: #Si no se cumple alguna de las dos condiciones, entonces creamos el segmento lat lo añadimos en la lista de segmentos al igual que a los nodos los hacemos vecinos
                origin = self.nodes[org_position]  # Con la posición encontramos el nodo en la lista de nodos
                destination = self.nodes[dest_position]
                origin.add_neight(destination)
                self.segments.append(navSegment(name, origin, destination, distance(origin, destination)))
                #print(f'segmento {name} registrado')
                #print(len(self.segments))
                return True
        else:
            return False

    def info_nodo(self, name): #función para pruebas
        for node in self.nodes:
            if node.name == name:
                print(f'Información del nodo: \n nombre: {node.name} posicion: {node.lon}, {node.lat} \n vecinos: {[neight.name for neight in node.vecinos]}')
    def info_segmentos(self): ##función para pruebas
        for k in self.segments:
            print(k.name)
        print(len(self.segments))

    def plot(self, test=False): #Metodo para crear nuestros plots(el argumento test está por default en False)
        fig, ax = plt.subplots(figsize=(16, 8))  # Ventana más grande
        ax.set_title('Gráfico con nodos y segmentos')

        for k in self.nodes:  # Nodos
            ax.scatter(k.lon, k.lat, color='red')  # lon en X, lat en Y
            ax.text(k.lon + 0.05, k.lat + 0.05, k.name, color='green', size=7)

        for segment in self.segments:  # Segmentos con flechas y distancias
            x_org, y_org = segment.origin.lon, segment.origin.lat
            x_dest, y_dest = segment.dest.lon, segment.dest.lat
            ax.annotate('', xy=(x_dest, y_dest), xytext=(x_org, y_org),
                        arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))
            x_mid, y_mid = (x_org + x_dest) / 2, (y_org + y_dest) / 2
            ax.text(x_mid, y_mid, round(segment.distance, 2), color='black', fontsize=7, ha='center', va='center')

        plt.xlabel('Longitud')
        plt.ylabel('Latitud')
        plt.grid(True)
        plt.tight_layout()
        if test: #si test es True
            plt.show()
        else: #caso contrario
            return fig, ax

    def get_closest(self, lon , lat): #Nos da el punto de mas cercanía a un nodo
        closest = 1000
        for node in self.nodes:
            distance = ((lon - node.lon)**2 + (lat - node.lat)**2)**1/2
            if distance<closest:
                closest, clo_node = distance, node
        print(f'El nodo mas cercano es {clo_node.name}')

    def plot_node(self, name, test=False): #Metodo para mostrar información del nodo seleccionado
        found, nodes, list_nodes = False, self.nodes, []
        fig, ax = plt.subplots(figsize=(16, 8))  # Ventana más grande
        ax.set_title(f'Información de {name}')

        for node in self.nodes:
            list_nodes.append(node) #metemos todos los nodos en una lista
            if node.name == name:
                found_node, found = node, True
                ax.scatter(found_node.lon, found_node.lat, color='blue') #el nodo que queremos información lo ponemos en azul
                ax.text(found_node.lon + 0.3, found_node.lat + 0.3, found_node.name, color='black', size=7)
                list_nodes.remove(node) #borramos el nodo principal de la lista
        if found: #En caso de que el nodo que queremos información exista haremos el plot
            for nei_node in found_node.vecinos:
                #print(nei_node.name)
                ax.scatter(nei_node.lon,nei_node.lat, color='green') #los nodos vecinos del principal en verde
                ax.text(nei_node.lon + 0.3, nei_node.lat + 0.3, nei_node.name, color='black', size=7)
                list_nodes.remove(nei_node) # los borramos de la lista
            #print('-------------------------')
            for segment in self.segments:
                if segment.origin.name == name:
                    print(name)
                    x_org, y_org = segment.origin.lon, segment.origin.lat
                    x_dest, y_dest = segment.dest.lon, segment.dest.lat
                    vx, vy = [x_org, x_dest], [y_org, y_dest]
                    x_mid, y_mid = (x_org + x_dest) / 2, (y_org + y_dest) / 2
                    ax.annotate('', xy=(x_dest, y_dest), xytext=(x_org, y_org), arrowprops=dict(arrowstyle='->', color='red', lw=2)) #hacemos los segmentos que los unen
                    ax.text(x_mid, y_mid, round(segment.distance, 2), color='black', fontsize=10, ha='center', va='center')
            for node in list_nodes: #finalmente los nodos restantes en la lista son los que no son ni el principal ni los vecinos por tanto los ponemos en gris
                ax.scatter(node.lon, node.lat, color='gray')
                ax.text(node.lon+0.3,node.lat+0.3, node.name, color='black', size=7)
            if test: #en caso de que sea un test el argumento será true, por default es False
                plt.show()
            else:
                return fig, ax #nos devuelve lo necesario para mostrarlo en la interfaz
        else:
            return False

    def save_flight_plan(self, file_name): #Función para guardar nuestro plan de vuelo en un archivo
        f = open(file_name, 'w') #buscamos el archivo(si no existe lo creará)
        f.write(f'Plan\n')
        for node in self.nodes: # por cada punto escribimos la información necesaria: nombre, posicion(lon e lat) y nodos vecinos(necesarios para hacer los segmentos)
            f.write(f'{node.name},{node.lon},{node.lat},{[neight.name for neight in node.vecinos]}\n')
        print('acabado el guardado!')
        f.close()

    def load_flight_plan(self, file_name): #Cargamos el plan de vuelo
        #intentamos encontrar el archivo
        try:
            print('hola')
            f = open(file_name, 'r')
            lineas = f.readlines()
            f.close()
            self.segments.clear()
            self.nodes.clear()
            self.airports.clear()
            for k in lineas[1:]: #leeremos cada línea del archivo para configurar el plot
                value = k.strip('\n').split(',', 3)
                neighbors_str = value[3].strip()[1:-1]  # Eliminar los corchetes '[' y ']'
                neighbors = [n.strip().strip("'") for n in neighbors_str.split(',')] if neighbors_str else []
                node = Node(value[0], float(value[1]), float(value[2]))
                node.vecinos = neighbors
                self.add_node(node) # añadimos los nodos y una lista de vecinos(estos serán ahora mismo el nombre del nodo no el objeto+
            for node in self.nodes:
                #print(node.name)
                #print(node.nodes)
                for i in range(len(node.vecinos) -1, -1, -1):
                    #print(i)
                    self.add_segment(f'{node.name}{node.vecinos[i]}', node.name, node.vecinos[i]) #con este código iremos uno a uno en cada nodo a sus vecinos y substituiremos el nombre del nodo vecino por el nodo en sí, llamando a la función de añadir segmento que se encarga de ello
                    node.vecinos.remove(node.vecinos[i])
            self.info_nodo('A')
            self.info_segmentos()
            fig, ax = self.plot()
            return fig, ax
        except:
            return 'error', 'error'


    def find_shortest_path(self, origin, destination, test=False):
        origin_node, destination_node, fin, previous_node = '', '', False, None
        for point in self.airports:
            print(point.name, point.sid.name, point.star.name)
            if point.name == origin:
                origin_node = point.sid
            elif point.name == destination:
                destination_node = point.star
            if origin_node and destination_node:
                fin = True
                break
        if not fin:
            print("Origen o destino no encontrado.dddd")
            return
        print(origin_node.name, destination_node.name)
        # Inicializamos variables para la búsqueda del camino
        final_path = False  # Flag para indicar si encontramos el camino
        last_node = origin_node  # Empezamos desde el nodo de origen
        print(origin_node)
        path_follower = []  # Lista para seguir el camino actual
        while not final_path:
            # Exploramos los nodos vecinos del nodo actual
            for neight in last_node.vecinos:
                if neight != previous_node:  # Evitamos retroceder al nodo anterior
                    if not path_follower:
                        current_path = [origin_node, neight]  # Si es el primer movimiento
                    else:
                        current_path = path_follower.copy()  # Continuamos desde el camino actual
                        current_path.append(neight)

                    # Calculamos la distancia total del camino actual
                    distancia = 0
                    for i in range(len(current_path) - 1):
                        distancia += distance(current_path[i], current_path[i + 1])

                    # Creamos un objeto Path y lo agregamos a la lista de caminos posibles
                    p = Path(last_node, neight, distancia, current_path)
                    self.paths.append(p)

            # Si no hay caminos posibles, devolvemos error
            if not self.paths:
                print("No hay camino disponible hacia el destino.")
                return 'error', 'error'

            # Ordenamos los caminos posibles sumando su distancia más la distancia estimada al destino
            self.paths.sort(key=lambda path: path.distance + distance(path.destino, destination_node))

            # Seleccionamos el mejor camino (el primero de la lista ordenada)
            last_path = self.paths[0]
            last_node = last_path.destino  # Avanzamos al siguiente nodo

            # (Opcional) Mostramos en consola los caminos posibles para depuración
            '''
            for path in self.paths:
                camino_array = [node.name for node in path.camino]
                print(camino_array, path.distance, path.distance + distance(path.destino, destination_node))
            print('-------------------------')
            '''
            # Si llegamos al nodo destino, terminamos
            if last_node.name == destination_node.name:
                final_path = True
            else:
                self.paths.pop(0)  # Eliminamos el camino usado
                previous_node = last_path.inicio  # Actualizamos el nodo previo
                path_follower = last_path.camino  # Actualizamos el camino seguido

        # Mostramos que encontramos el camino
        print("Camino encontrado:")
        fig, ax = last_path.path_plot(self, origin, destination)  # Graficamos el camino encontrado
        self.paths.clear()  # Limpiamos la lista de caminos para futuras búsquedas
        # Devolvemos la figura y los ejes de la gráfica
        if test:
            ax.show()
        else:
            return fig, ax

def distance(point1, point2):
    """
    Calcula la distancia Haversine entre dos puntos con atributos .lat y .lon
    """
    R = 6371  # Radio de la Tierra en kilómetros

    lat1, lon1 = math.radians(point1.lat), math.radians(point1.lon)
    lat2, lon2 = math.radians(point2.lat), math.radians(point2.lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Resultado en kilómetros
