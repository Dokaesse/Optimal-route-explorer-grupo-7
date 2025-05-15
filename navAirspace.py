from navPoint import *
from navAirport import *
from navSegments import *
from path import *
from graph import *
import matplotlib.pyplot as plt
space = Graph()
class navSpace:
    def __init__(self):
        self.points = []
        self.segments = []
        self.airports = []
        self.paths = []

    def add_point(self, point):
        space.nodes.append(point)

    def add_segment(self, segment):
        origin, dest, fin = None, None, False
        for point in space.nodes:
            if point.ident == segment[0]:
                origin = point
            elif point.ident == segment[1]:
                dest = point
            if origin and dest:
                fin = True
                break
        if fin:
            name = f'{origin.name}-{dest.name}'
            space.segments.append(navSegment(name,origin, dest, float(segment[2])))
            origin.add_neight(dest)
        else:
            print('No se ha encontrado o origen o inicio')

    def add_airport(self, last_airport, dep, arr):
        for point in space.nodes:
            if point.name == dep:
                dep = point
            elif point.name == arr:
                arr = point
        if last_airport != '':
            space.airports.append(
                navAirport(last_airport, dep if dep != '' else False, arr if arr != '' else False))


    def find_shortest_path(self, origin, destination):
        origin_node, destination_node, fin, previous_node = '', '', False, None
        for point in self.airports:
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
        # Inicializamos variables para la búsqueda del camino
        final_path = False  # Flag para indicar si encontramos el camino
        last_node = origin_node  # Empezamos desde el nodo de origen
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
            for path in self.paths:
                camino_array = [node.name for node in path.camino]
                print(camino_array, path.distance, path.distance + distance(path.destino, destination_node))
            print('-------------------------')

            # Si llegamos al nodo destino, terminamos
            if last_node.name == destination_node.name:
                final_path = True
            else:
                self.paths.pop(0)  # Eliminamos el camino usado
                previous_node = last_path.inicio  # Actualizamos el nodo previo
                path_follower = last_path.camino  # Actualizamos el camino seguido

        # Mostramos que encontramos el camino
        print("Camino encontrado:")
        fig, ax = last_path.path_plot_space(self)  # Graficamos el camino encontrado
        self.paths.clear()  # Limpiamos la lista de caminos para futuras búsquedas
        # Devolvemos la figura y los ejes de la gráfica
        return fig, ax

import math

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