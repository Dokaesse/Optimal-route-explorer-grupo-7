from navPoint import *
from navAirport import *
from navSegments import *
from navAirspace import *
from graph import *
s = navSpace()
def load_data_file(points, aero, segments):
    try:
        space.segments.clear()
        space.nodes.clear()
        space.airports.clear()
        #points, aero, segments = 'nav.txt', 'aer.txt', 'seg.txt'
        f = open(points)
        lineas = f.readline().strip()

        while lineas != '':
            value = lineas.strip('\n').split(' ')
            # print(value)
            point = navPoint(value[0], value[1], float(value[2]), float(value[3]))
            s.add_point(point)
            lineas = f.readline()
        f.close()

        f = open(aero)
        ##s.add_airport(f)
        lineas = f.readline().strip()
        last_airport, dep, arr = '', '', ''
        while lineas != '':
            value = lineas.strip('\n')
            if value[-2] == '.':
                if value[-1] == 'D':
                    dep = value
                elif value[-1] == 'A':
                    arr = value
            else:
                s.add_airport(last_airport, dep, arr)
                last_airport, dep, arr = value, '', ''
            lineas = f.readline()
        s.add_airport(last_airport, dep, arr)
        f.close()
        for i in s.airports:
            print(i.__dict__)

        f = open(segments)
        lineas = f.readline().strip()
        while lineas != '':
            value = lineas.strip('\n').split(' ')
            s.add_segment(value)
            lineas = f.readline()
        f.close()
    except:
        return False
    # space.plot_node('GIR.D', True)
    # space.find_shortest_path('LEBL', 'LEZG')
    # space.plot(True)
load_data_file('data/catalunya/nav.txt', 'data/catalunya/aer.txt', 'data/catalunya/seg.txt')