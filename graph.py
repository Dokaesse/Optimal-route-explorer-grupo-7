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
        plt.grid(True)

        for node in self.nodes:
            list_nodes.append(node) #metemos todos los nodos en una lista
            if node.name == name:
                found_node, found = node, True
                ax.scatter(found_node.lon, found_node.lat, color='blue') #el nodo que queremos información lo ponemos en azul
                ax.text(found_node.lon + 0.03, found_node.lat + 0.03, found_node.name, color='black', size=7)
                list_nodes.remove(node) #borramos el nodo principal de la lista
        if found: #En caso de que el nodo que queremos información exista haremos el plot
            for nei_node in found_node.vecinos:
                #print(nei_node.name)
                ax.scatter(nei_node.lon,nei_node.lat, color='green') #los nodos vecinos del principal en verde
                ax.text(nei_node.lon + 0.03, nei_node.lat + 0.03, nei_node.name, color='black', size=7)
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
                ax.text(node.lon+0.03,node.lat+0.03, node.name, color='black', size=7)
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

    def show_reachability(self, origin_name, test=None):
        origin_node = None
        for node in self.nodes:
            if node.name == origin_name:
                origin_node = node
                break
        if not origin_node:
            print(f"❌ Nodo {origin_name} no encontrado.")
            return

        # BFS sin deque: usamos una lista como cola
        visited = set()
        queue = [origin_node]
        visited.add(origin_node.name)

        while queue:
            current = queue.pop(0)  # Sacamos el primer elemento (FIFO)
            for seg in self.segments:
                if seg.origin.name == current.name and seg.dest.name not in visited:
                    visited.add(seg.dest.name)
                    queue.append(seg.dest)

        # Dibujamos los nodos
        fig, ax = plt.subplots(figsize=(16, 8))
        for node in self.nodes:
            color = 'red' if node.name == origin_name else ('green' if node.name in visited else 'gray')
            ax.plot(node.lon, node.lat, 'o', color=color)
            if color == 'red':
                ax.text(node.lon, node.lat, f' {node.name}', fontsize=10, color=color)
            else:
                ax.text(node.lon, node.lat, f' {node.name}', fontsize=8)

        # Dibujamos los segmentos
        for seg in self.segments:
            x_org, x_dest = seg.origin.lon, seg.dest.lon
            y_org, y_dest = seg.origin.lat, seg.dest.lat
            if seg.origin.name in visited and seg.dest.name in visited:
                ax.annotate('', xy=(x_dest, y_dest), xytext=(x_org, y_org),
                        arrowprops=dict(arrowstyle='->', color='blue', lw=1))  # hacemos los segmentos que los unen
            else:
                ax.plot([x_org, x_dest], [y_org, y_dest], color='gray', linestyle='--', lw=1)

        ax.set_title(f'Nodos alcanzables desde {origin_name}')
        plt.xlabel('Longitud')
        plt.ylabel('Latitud')
        plt.grid(True)
        if test:
            plt.show()
        else:
            return fig, ax

    def find_shortest_path(self, origin, destination, test=False):
        origin_node, destination_node = None, None
        self.paths.clear()
        # Buscar los nodos de inicio y destino
        if not self.airports:
            for point in self.nodes:
                if point.name == origin:
                    origin_node = point
                elif point.name == destination:
                    destination_node = point
                if origin_node and destination_node:
                    break
        else:
            for point in self.airports:
                if point.name == origin:
                    origin_node = point.sid
                elif point.name == destination:
                    destination_node = point.star
                if origin_node and destination_node:
                    break

        if not origin_node or not destination_node:
            print("❌ Origen o destino no encontrado.")
            return 'error', 'error'

        print(f"🔍 Ejecutando busqueda desde {origin_node.name} a {destination_node.name}")

        open_list = [{
            'node': origin_node,
            'path': [origin_node],
            'g': 0,  # coste desde el inicio
            'f': distance(origin_node, destination_node)  # estimación total f = g + h
        }]

        visited = set()

        while open_list:
            # Ordenar la lista abierta según menor f (g + h)
            open_list.sort(key=lambda item: item['f'])
            current = open_list.pop(0)
            current_node = current['node']
            current_path = current['path']
            current_g = current['g']

            if current_node == destination_node:
                print("✅ Camino encontrado")
                total_path = Path(None, destination_node, current_g, current_path)
                fig, ax = total_path.path_plot(self, origin, destination)
                self.paths.append(total_path)
                if test:
                    ax.show()
                return fig, ax

            if current_node in visited:
                continue
            visited.add(current_node)

            # Expandir vecinos
            for neighbor in current_node.vecinos:
                if neighbor not in visited:
                    g_new = current_g + distance(current_node, neighbor)
                    h = distance(neighbor, destination_node)
                    f_new = g_new + h
                    open_list.append({
                        'node': neighbor,
                        'path': current_path + [neighbor],
                        'g': g_new,
                        'f': f_new
                    })

        print("❌ No se encontró camino.")
        return 'error', 'error'

    def register_kml_file(self):
        import os
        f = open('data/google_earth/showplot.kml', 'w')
        f.write('<kml xmlns="http://www.opengis.net/kml/2.2"><Document>')
        for node in self.nodes:
            f.write(f'<Placemark><name>{node.name}</name><Point><coordinates>{node.lon},{node.lat}</coordinates></Point></Placemark>')
        for segment in self.segments:
            f.write(f'<Placemark><name>{segment.name}</name><LineString><extrude>1</extrude><tesellate>1</tesellate><altitudeMode>absolute</altitudeMode><coordinates>{segment.origin.lon},{segment.origin.lat},4000\n{segment.dest.lon},{segment.dest.lat},2000</coordinates></LineString></Placemark>')
        f.write('</Document></kml>')
        f.close()

        show_plot = "data/google_earth/showplot.kml"
        plot_absoluto = os.path.abspath(show_plot)
        if os.path.exists(plot_absoluto) :
            os.startfile(plot_absoluto)
        else:
            print("❌ El archivo no se encuentra en esa ruta.")

    def show_shortest_path_on_google_earth_animation(self):
        import os
        # Creamos un diccionario para acceder rápido a los segmentos
        segment_dict = {(seg.origin.name, seg.dest.name): seg for seg in self.segments}
        path = self.paths[0].camino
        kml_path = 'data/google_earth/shortest_path_animation.kml'

        with open(kml_path, 'w', encoding='utf-8') as f:
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
            <kml xmlns="http://www.opengis.net/kml/2.2"
                xmlns:gx="http://www.google.com/kml/ext/2.2">
            <Document>
                ''')

            # Estilo de línea y polígonos
            f.write('''
                <Style id="lineStyle">
                    <LineStyle>
                        <color>7f00ffff</color>
                        <width>4</width>
                    </LineStyle>
                    <PolyStyle>
                        <color>7f00ff00</color>
                    </PolyStyle>
                </Style>
                <Style id="planeIcon">
                    <IconStyle>
                        <scale>1.2</scale>
                        <Icon>
                            <href>http://maps.google.com/mapfiles/kml/shapes/airports.png</href>
                        </Icon>
                    </IconStyle>
                </Style>
                ''')

            # Añadimos los puntos
            for point in path:
                f.write(f'''
                    <Placemark>
                        <name>{point.name}</name>
                        <Point>
                            <coordinates>{point.lon},{point.lat}</coordinates>
                        </Point>
                    </Placemark>
                    ''')

            h_max = 10000  # altura máxima
            n = len(path)
            velocidad_kmh = 800
            escala_tiempo = 60

            altitudes = [
                int(h_max * (1 - ((2 * i / (n - 1)) - 1) ** 2))
                for i in range(n)
            ]

            # Líneas entre puntos
            for i in range(len(path) - 1):
                seg = segment_dict.get((path[i].name, path[i + 1].name))
                if seg:
                    alt1 = altitudes[i]
                    alt2 = altitudes[i + 1]
                    f.write(f'''
                        <Placemark>
                            <name>{seg.name}</name>
                            <styleUrl>#lineStyle</styleUrl>
                            <LineString>
                                <extrude>1</extrude>
                                <tessellate>1</tessellate>
                                <altitudeMode>absolute</altitudeMode>
                                <coordinates>
                                    {seg.origin.lon},{seg.origin.lat},{alt1}
                                    {seg.dest.lon},{seg.dest.lat},{alt2}
                                </coordinates>
                            </LineString>
                        </Placemark>
                        ''')

            # Avión (icono inicial)
            f.write(f'''
                <Placemark id="airplane">
                    <name>Avión</name>
                    <styleUrl>#planeIcon</styleUrl>
                    <Point>
                        <coordinates>{path[0].lon},{path[0].lat},{altitudes[0]}</coordinates>
                    </Point>
                </Placemark>
                ''')

            # Animación
            f.write('''
                <gx:Tour>
                    <name>Vuelo animado</name>
                    <gx:Playlist>
                ''')

            for i in range(len(path) - 1):
                p1, p2 = path[i], path[i + 1]
                alt1, alt2 = altitudes[i], altitudes[i + 1]
                d_km = distance(p1, p2)
                dur_seg = (d_km / velocidad_kmh) * 3600 / escala_tiempo

                f.write(f'''
                <gx:FlyTo>
                    <gx:duration>{dur_seg:.2f}</gx:duration>
                    <gx:flyToMode>smooth</gx:flyToMode>
                    <LookAt>
                        <longitude>{p2.lon}</longitude>
                        <latitude>{p2.lat}</latitude>
                        <altitude>{alt2}</altitude>
                        <heading>0</heading>
                        <tilt>60</tilt>
                        <range>1000</range>
                        <altitudeMode>absolute</altitudeMode>
                    </LookAt>
                </gx:FlyTo>
        ''')
            f.write('''
                    </gx:Playlist>
                </gx:Tour>
                ''')
            f.write('</Document></kml>')

        # Abrimos el archivo en Google Earth si existe
        kml_abs_path = os.path.abspath(kml_path)
        if os.path.exists(kml_abs_path):
            os.startfile(kml_abs_path)
        else:
            print("❌ El archivo no se encuentra en esa ruta.")


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

