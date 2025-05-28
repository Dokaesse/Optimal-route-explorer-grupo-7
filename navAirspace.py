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