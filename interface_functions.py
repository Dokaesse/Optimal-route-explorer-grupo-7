import tkinter as tk
from tkinter import messagebox
from test_graph import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import MouseEvent

def load_flight_plan_display(plot_display):
    popup = tk.Toplevel()
    popup.title('Cargar fichero')
    label = tk.Label(popup, text='Introduce el nombre del fichero donde está tu plot guardado: ')
    label.pack(pady=5, padx=5)
    name = tk.Entry(popup)
    name.pack(pady=5, padx=5)
    cargar_button = tk.Button(popup, text='cargar', command=lambda: load_flight(name, plot_display, popup))
    cargar_button.pack(pady=5)

def load_flight(name, plot_display, popup):
    fig, ax = g.load_flight_plan(name.get(), popup)
    if fig == 'error':
        messagebox.showerror("Error", "No existe ningun archivo con ese nombre")
        popup.destroy()
    else:
        canvas = FigureCanvasTkAgg(fig, master=plot_display)
        canvas.draw()
        canvas_picture = canvas.get_tk_widget()
        canvas_picture.config(width=600, height=700)
        canvas_picture.grid(row=0, column=0, padx=5, pady=5, sticky= tk.N + tk.E + tk.S +tk.W)
        fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, plot_display))
        popup.destroy()

def save_flight_plan_button():
    popup = tk.Toplevel()
    popup.title('Guardar plan de vuelo')
    label = tk.Label(popup, text='Introduce un nombre de un fichero para guardarlo (si no existe lo creará): ')
    label.pack(pady=5, padx=5)
    nombre_fichero = tk.Entry(popup)
    nombre_fichero.pack(padx=5, pady=5)
    save_button = tk.Button(popup, text='guardar', command=lambda: (g.save_flight_plan(nombre_fichero.get()), popup.destroy()))
    save_button.pack(pady=5, padx=5)

def clean_flight_plan(plot_display, actualizar_listas):
    g.nodes.clear()
    g.segments.clear()
    show_initial_plot(plot_display,actualizar_listas)


def crear_punto(nombre, x, y, plot_display, popup, actualizar_listas=None):
    found = any(node.name == nombre for node in g.nodes)

    if not found:
        g.add_node(Node(nombre, x, y))
        popup.destroy()
        actualizar_listas()
        show_initial_plot(plot_display, actualizar_listas)

    else:
        messagebox.showerror("Error", "El nombre del punto ya existe. Intente con otro nombre.")
        popup.destroy()


def on_click(event: MouseEvent, plot_display, actualizar_listas=None):
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
    ##messagebox.showinfo('Cordenaadas del click', f'Has clickado en {x:.2f} y {y:.2f}')


def show_initial_plot(plot_display, actualizar_listas=None):
    fig, ax = g.plot()
    canvas = FigureCanvasTkAgg(fig, master=plot_display)
    canvas.draw()

    canvas_picture = canvas.get_tk_widget()
    canvas_picture.config(width=600, height=700)
    canvas_picture.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.S + tk.W)

    # Conectamos el click con la función y le pasamos actualizar_listas
    fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, plot_display, actualizar_listas))


def segment_creator(origin_name, destination_name, plot_display, actualizar_listas):
    found = False
    if origin_name == destination_name:
        found = True
        print('duplicado')
    if not found:
        g.add_segment(f'{origin_name}{destination_name}', origin_name, destination_name)
        for segment in g.segments:
            print(segment.name)
        show_initial_plot(plot_display, actualizar_listas)

def show_plot_node(sa_nodo, plot_display):
    print(sa_nodo)
    if g.plot_node(sa_nodo):
        fig, ax = g.plot_node(sa_nodo)
        canvas = FigureCanvasTkAgg(fig, master=plot_display)
        canvas.draw()
        print('si')
        canvas_picture = canvas.get_tk_widget()
        canvas_picture.config(width=600, height=700)
        canvas_picture.grid(row=0, column=0, padx=5, pady=5, sticky= tk.N + tk.E + tk.S +tk.W)
    else:
        print('Ha habido un error') ## hacerlo como error que salga ventana

def borrar_punto_segmento(actualizar_listas, plot_display, nodo_name, segment_name): #cambiarlo de archivo
    found_nodo = False
    print('si')
    if nodo_name != 'puntos':
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
    if segment_name != 'segmentos':
        for segment in g.segments:
            if segment.name == segment_name:
                origin_node = segment.or_node
                dest_node = segment.dest_node
                origin_node.nodes.remove(dest_node)
                g.segments.remove(segment)
                found_segment = True
                break
    if found_nodo or found_segment:
        print('juan')
        show_initial_plot(plot_display, actualizar_listas)