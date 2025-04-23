import tkinter as tk
from tkinter import messagebox
from test_graph import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import MouseEvent
#archivo para las funciones de la interfaz

def load_flight_plan_display(plot_display, actualizar_listas): #función para recoger datos sobre el archivo que queremos cargar
    popup = tk.Toplevel()
    popup.title('Cargar fichero')
    label = tk.Label(popup, text='Introduce el nombre del fichero donde está tu plot guardado: ')
    label.pack(pady=5, padx=5)
    name = tk.Entry(popup)
    name.pack(pady=5, padx=5)
    cargar_button = tk.Button(popup, text='cargar', command=lambda: load_flight(name, plot_display, popup, actualizar_listas))
    cargar_button.pack(pady=5)

def load_flight(name, plot_display, popup, actualizar_listas): #función para cargar nuestro archivo
    fig, ax = g.load_flight_plan(name.get()) #función en graph.py que nos devuelve nuestro plot o, por el contrario, devuelve error si no existe el archivo que cargamos
    if fig == 'error': #Mensaje de error si no existe el archivo
        messagebox.showerror("Error", "No existe ningún archivo con ese nombre")
        popup.destroy()
    else:
        canvas = FigureCanvasTkAgg(fig, master=plot_display)
        canvas.draw()
        canvas_picture = canvas.get_tk_widget()
        canvas_picture.config(width=600, height=700)
        canvas_picture.grid(row=0, column=0, padx=5, pady=5, sticky= tk.N + tk.E + tk.S +tk.W)
        fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, plot_display, actualizar_listas))
        popup.destroy()

def save_flight_plan_button(): #Función para recoger datos sobre donde queremos guardar nuestro plot
    popup = tk.Toplevel()
    popup.title('Guardar plan de vuelo')
    label = tk.Label(popup, text='Introduce un nombre de un fichero para guardarlo (si no existe lo creará): ')
    label.pack(pady=5, padx=5)
    nombre_fichero = tk.Entry(popup)
    nombre_fichero.pack(padx=5, pady=5)
    save_button = tk.Button(popup, text='guardar', command=lambda: (g.save_flight_plan(nombre_fichero.get()), popup.destroy())) #llamamos a la función de guardado del plan de vuelo de graph.py
    save_button.pack(pady=5, padx=5)

def clean_flight_plan(plot_display, actualizar_listas): #funcion para limpiar el gráfico
    g.nodes.clear()
    g.segments.clear()
    show_initial_plot(plot_display,actualizar_listas)


def crear_punto(nombre, x, y, plot_display, popup, actualizar_listas=None): #Función para crear nuevos puntos en nuestro plot
    found = any(node.name == nombre for node in g.nodes)
    if not found: #buscamos si el nombre del punto que queremos registrar ya existe(esto ya lo hace g.add_node, pero lo hacemos para poder mostrar un mensaje de error)
        g.add_node(Node(nombre, x, y))
        popup.destroy()
        actualizar_listas()
        show_initial_plot(plot_display, actualizar_listas)
    else: #En caso de existir nos muestra un mensaje de error
        messagebox.showerror("Error", "El nombre del punto ya existe. Intente con otro nombre.")
        popup.destroy()


def on_click(event: MouseEvent, plot_display, actualizar_listas=None): #Función que nos permite registrar el evento de hacer clic en nuestra gráfica, útil para registrar puntos.
    if event.inaxes:
        x, y = round(event.xdata, 2), round(event.ydata, 2)
        popup = tk.Toplevel()
        popup.title('Introduce un nombre: ')
        label = tk.Label(popup, text=f"Ingrese un dato para las coordenadas ({x}, {y}):")
        label.pack(pady=5)

        input_text = tk.Entry(popup)
        input_text.pack(pady=5)

        def continuar():
            crear_punto(input_text.get(), x, y, plot_display, popup, actualizar_listas)

        save_button = tk.Button(popup, text='Continuar', command=continuar)
        save_button.pack(pady=5)
    ##messagebox.showinfo('Coordenadas del clic', f'Has clicado en {x:.2f} y {y:.2f}')


def show_initial_plot(plot_display, actualizar_listas=None): #Función para mostrar inicialmente el plot en la interfaz, pero también la llamaremos en otras funciones para mostrar el gráfico actualizado
    fig, ax = g.plot()
    canvas = FigureCanvasTkAgg(fig, master=plot_display)
    canvas.draw()

    canvas_picture = canvas.get_tk_widget()
    canvas_picture.config(width=600, height=700)
    canvas_picture.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.S + tk.W)

    # Conectamos el clic con la función y le pasamos actualizar_listas
    fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, plot_display, actualizar_listas))


def segment_creator(origin_name, destination_name, plot_display, actualizar_listas): #función para crear segmentos
    found = False
    if origin_name == destination_name: #verificamos que no se pueda poner mismo origen y final
        found = True
        print('duplicado')
    if not found:
        g.add_segment(f'{origin_name}{destination_name}', origin_name, destination_name) #si se cumplen las condiciones se crea el segmento con el metodo add_segment
        for segment in g.segments:
            print(segment.name)
        show_initial_plot(plot_display, actualizar_listas) #actualizamos el plot de la interfaz

def show_plot_node(sa_nodo, plot_display): #Con esta función mostraremos la información del punto que seleccionemos
    print(sa_nodo)
    if g.plot_node(sa_nodo):
        fig, ax = g.plot_node(sa_nodo) #esta función nos devuelve los valores de fig y ax necesarios para crear nuestro plot
        canvas = FigureCanvasTkAgg(fig, master=plot_display)
        canvas.draw()
        canvas_picture = canvas.get_tk_widget()
        canvas_picture.config(width=600, height=700)
        canvas_picture.grid(row=0, column=0, padx=5, pady=5, sticky= tk.N + tk.E + tk.S +tk.W) #dibujamos la figura y hacemos el canvas para poder verlo en la interfaz
    elif sa_nodo != 'Punto':
        messagebox.showerror('ERROR🛑', 'No se ha podido mostrar información del punto!!')

def show_shortest_path(nodes_origin_path_menu, nodes_dest_path_menu, plot_display):
    if nodes_origin_path_menu != 'Origen' and nodes_dest_path_menu != 'Destino':
        fig, ax = g.find_shortest_path(nodes_origin_path_menu, nodes_dest_path_menu)
        if fig == 'error':
            messagebox.showerror('ERROR🛑', f'No hay manera de llegar a {nodes_dest_path_menu} desde {nodes_origin_path_menu}')
        else:
            canvas = FigureCanvasTkAgg(fig, master=plot_display)
            canvas.draw()
            canvas_picture = canvas.get_tk_widget()
            canvas_picture.config(width=600, height=700)
            canvas_picture.grid(row=0, column=0, padx=5, pady=5,
                                sticky=tk.N + tk.E + tk.S + tk.W)  # dibujamos la figura y hacemos el canvas para poder verlo en la interfaz

def borrar_punto_segmento(actualizar_listas, plot_display, nodo_name, segment_name): #Función que nos permite borrar tanto puntos como segmentos del plot
    found_nodo = False
    if nodo_name != 'Punto': #comprobamos que no tenga el valor inicial del menú, ya que este no es un punto y, por lo tanto, no se puede borrar
        for i in range(len(g.segments) -1, -1, -1):
            origin_node = g.segments[i].or_node
            dest_node = g.segments[i].dest_node
            if origin_node.name == nodo_name or dest_node.name == nodo_name:
                origin_node.nodes.remove(dest_node)
                g.segments.remove(g.segments[i])
                print('borrando')
                #del g.segments[i]
        for node in g.nodes:
            if node.name == nodo_name:
                print('pepe')
                print(node.nodes)
                g.nodes.remove(node)
                #del node
                found_nodo = True
                break
    found_segment = False
    if segment_name != 'Segmentos': #commprobamos al igual que con el punto que este no sea el valor inicial del menú, qeu nno existe en nuestra lista de segmentos
        for segment in g.segments:
            if segment.name == segment_name: #buscamos el segmento que tenga el mismo nombre y lo borramos de la lista
                origin_node = segment.or_node
                dest_node = segment.dest_node
                origin_node.nodes.remove(dest_node) #le borramos también al punto de origen su vecino que seria el destinatario de su ruta
                g.segments.remove(segment)
                found_segment = True
                break
    if found_nodo or found_segment: #si se cumple alguna de las condiciones antes dichas entonces actualizaremos nuestro plot en la interfaz
        #print('juan')
        show_initial_plot(plot_display, actualizar_listas)