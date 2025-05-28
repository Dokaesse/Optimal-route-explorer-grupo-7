import matplotlib.pyplot as plt
class Path:
    def __init__(self, inicio, destino, distancia=None, camino=None):
        self.inicio = inicio
        self.destino = destino
        self.distance = distancia
        if camino is None:
            self.camino = []
        else:
            self.camino = camino

    def add_node_path(self, node_name, g):
        fin_1, fin_2 = False, False
        for node in self.camino:
            if node.name == node_name:
                fin_1 = True
        if not fin_1:
            for node in g.nodes:
                if node.name == node_name:
                    self.camino.append(node)
                    fin_2 = True
                    break
            if not fin_2:
                print('No he encontrado ese punto')
        else:
            print('Ese punto ya está en el path')

    def contains_node(self, node_name):
        fin = False
        for node in self.camino:
            if node.name == node_name:
                fin = True
                break
        return fin

    def path_plot(self, g, origen, destination):
        fig, ax = plt.subplots(figsize=(16, 8))  # Ventana más grande
        ax.set_title(f'Distancia {round(self.distance, 2)}km entre {origen} a {destination}')

        list_nodes = []
        print(self.camino)
        fin = True
        for node in g.nodes:
            list_nodes.append(node)
            for path_node in self.camino:
                if node.name == path_node.name:
                    ax.scatter(node.lon, node.lat, color='blue')
                    ax.text(node.lon + 0.03, node.lat + 0.03, node.name, color='black', size=7)
                    list_nodes.remove(node)
        i, fin = 0, False
        '''
        while i<len(self.camino)-1 and not fin:
            fin = True
            for node in self.camino[i].nodes:
                print(node.name, self.camino[i+1].name, self.camino[i].name)
                if node.name == self.camino[i+1].name:
                    fin = False
                    break
            i+=1
        i=0
        '''
        while i < len(self.camino) - 1 and not fin:
            for segment in g.segments:
                if segment.origin.name == self.camino[i].name and segment.dest.name == self.camino[i + 1].name:
                    x_org, y_org = segment.origin.lon, segment.origin.lat
                    x_dest, y_dest = segment.dest.lon, segment.dest.lat
                    vx, vy = [x_org, x_dest], [y_org, y_dest]
                    x_mid, y_mid = (x_org + x_dest) / 2, (y_org + y_dest) / 2
                    ax.annotate('', xy=(x_dest, y_dest), xytext=(x_org, y_org),
                                arrowprops=dict(arrowstyle='->', color='red',
                                                lw=2))  # hacemos los segmentos que los unen
                    ax.text(x_mid, y_mid, round(segment.distance, 2), color='black', fontsize=7, ha='center', va='center')
            i += 1
        for node in list_nodes:
            ax.scatter(node.lon, node.lat, color='grey')
            ax.text(node.lon + 0.03, node.lat + 0.03, node.name, color='black', size=7)

        return fig, ax
'''        
    def path_plot(self,g, test=False):
        fig, ax = plt.subplots()
        list_nodes = []
        print(self.camino)
        fin = True
        if test:
            for node in self.camino:
                print('sasa')
                ax.scatter(node.x, node.y, color='blue')
                ax.text(node.x + 0.3, node.y + 0.3, node.name, color='black', size=12)

                # Dibujamos las flechas entre nodos si hay segmento entre ellos
            for i in range(len(self.camino) - 1):
                or_node = self.camino[i]
                dest_node = self.camino[i + 1]
                for segment in g.segments:
                    if segment.or_node.name == or_node.name and segment.dest_node.name == dest_node.name:
                        x_org, y_org = or_node.x, or_node.y
                        x_dest, y_dest = dest_node.x, dest_node.y
                        x_mid, y_mid = (x_org + x_dest) / 2, (y_org + y_dest) / 2

                        ax.annotate('', xy=(x_dest, y_dest), xytext=(x_org, y_org),
                                    arrowprops=dict(arrowstyle='->', color='red', lw=2))
                        ax.text(x_mid, y_mid, round(segment.cost, 2), color='black', fontsize=10, ha='center',
                                va='center')
                        break  # Salimos porque ya encontramos el segmento correspondiente

            plt.show()
        else:
            for node in g.nodes:
                list_nodes.append(node)
                for path_node in self.camino:
                    if node.name == path_node.name:
                        ax.scatter(node.x, node.y, color='blue')
                        ax.text(node.x + 0.3, node.y + 0.3, node.name, color='black', size=12)
                        list_nodes.remove(node)
            for node in g.nodes:
                list_nodes.append(node)
            for path_node in self.camino:
                ax.scatter(path_node.x, path_node.y, color='blue')
                ax.text(path_node.x + 0.3, path_node.y + 0.3, path_node.name, color='black', size=12)
                list_nodes.remove(path_node)
            i, fin = 0, False

            ###
            while i<len(self.camino)-1 and not fin:
                fin = True
                for node in self.camino[i].nodes:
                    print(node.name, self.camino[i+1].name, self.camino[i].name)
                    if node.name == self.camino[i+1].name:
                        fin = False
                        break
                i+=1
            i=0
            ###
            
            while i<len(self.camino)-1 and not fin:
                for segment in g.segments:
                    if segment.or_node.name == self.camino[i].name and segment.dest_node.name == self.camino[i+1].name:
                        x_org, y_org = segment.or_node.x, segment.or_node.y
                        x_dest, y_dest = segment.dest_node.x, segment.dest_node.y
                        vx, vy = [x_org, x_dest], [y_org, y_dest]
                        x_mid, y_mid = (x_org + x_dest) / 2, (y_org + y_dest) / 2
                        ax.annotate('', xy=(x_dest, y_dest), xytext=(x_org, y_org),
                                    arrowprops=dict(arrowstyle='->', color='red',
                                                    lw=2))  # hacemos los segmentos que los unen
                        ax.text(x_mid, y_mid, round(segment.cost, 2), color='black', fontsize=10, ha='center', va='center')
                i+=1
            for node in list_nodes:
                ax.scatter(node.x, node.y, color='grey')
                ax.text(node.x + 0.3, node.y + 0.3, node.name, color='black', size=12)
            #plt.show()
            return fig, ax
'''
