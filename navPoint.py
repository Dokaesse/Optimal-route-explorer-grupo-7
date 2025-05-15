class navPoint:
    def __init__(self, ident, name, lat, lon):
        self.ident = ident
        self.name = name
        self.lat = lat
        self.lon = lon
        self.vecinos = []

    def add_neight(self, point):
        self.vecinos.append(point)