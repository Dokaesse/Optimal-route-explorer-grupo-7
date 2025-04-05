##Configuracion de la interfaz
import tkinter as tk
from interface_functions import *

def actualizar_listas(): #función que utilizaremos para poder actualizar las listas de la interfaz siempre que cambiemos algún punto o segmento
    print('actualizando listas...')
    # Obtener las nuevas listas de nombres
    nombres_nodos = [node.name for node in g.nodes]
    nombres_segmentos = [segment.name for segment in g.segments]
    # === Lista: sa_nodo ===
    sa_nodo.set('punto')  # valor fijo que no está en la lista
    menu = nodes_menu['menu']
    menu.delete(0, 'end')
    for nombre in nombres_nodos:
        menu.add_command(label=nombre, command=lambda value=nombre: sa_nodo.set(value))

    # === Lista: sa_nodo_origen ===
    sa_nodo_origen.set('inicio')  # valor fijo que no está en la lista
    menu = nodes_origin_menu['menu']
    menu.delete(0, 'end')
    for nombre in nombres_nodos:
        menu.add_command(label=nombre, command=lambda value=nombre: sa_nodo_origen.set(value))

    # === Lista: sa_nodo_destino ===
    sa_nodo_destino.set('destino')  # valor fijo que no está en la lista
    menu = nodes_dest_menu['menu']
    menu.delete(0, 'end')
    for nombre in nombres_nodos:
        menu.add_command(label=nombre, command=lambda value=nombre: sa_nodo_destino.set(value))

    # === Lista: sa_nodo_borrar ===
    sa_nodo_borrar.set('punto')  # valor fijo que no está en la lista
    menu = nodes_options_menu['menu']
    menu.delete(0, 'end')
    for nombre in nombres_nodos:
        menu.add_command(label=nombre, command=lambda value=nombre: sa_nodo_borrar.set(value))

    # === Lista: sa_segmento_borrar ===
    sa_segmento_borrar.set('segmentos')  # valor fijo que no está en la lista
    menu = segments_option_menu['menu']
    menu.delete(0, 'end')
    for nombre in nombres_segmentos:
        menu.add_command(label=nombre, command=lambda value=nombre: sa_segmento_borrar.set(value))

#configuracion de la ventana
root = tk.Tk()
root.geometry('850x480')
root.title('Version 1 finalizada')
root.columnconfigure(0, weight=1)
root.columnconfigure(0, weight=10)
root.rowconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


#Configuracion del display del plot
plot_display = tk.LabelFrame(root, text='Plot')
plot_display.grid(row=0, column=1, rowspan=3, pady=5, padx=5, sticky='nsew')
plot_display.columnconfigure(0, weight=1)
plot_display.rowconfigure(0, weight=1)

#Conjunto para botones de guardar/cargar/limpiar
button_save_run_fileplot = tk.LabelFrame(root, text='Cargar y guardar plot')
button_save_run_fileplot.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
button_save_run_fileplot.columnconfigure(0, weight=1)
button_save_run_fileplot.rowconfigure(0, weight=1)
button_save_run_fileplot.rowconfigure(1, weight=1)
button_save_run_fileplot.rowconfigure(2, weight=1)

#Botones de guardado/cargar y limpiar (las funciones asociadas en interface_functions.py)
run_button = tk.Button(button_save_run_fileplot, text='Cargar archivo', command=lambda: (load_flight_plan_display(plot_display, actualizar_listas), actualizar_listas())) ##En toda función que cambiemos nodos y segmentos llamaremos a actualizar_lista(), también lo pasaremos como argumento(explicación en línea 143)
run_button.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.S + tk.W)

save_button = tk.Button(button_save_run_fileplot, text='Guardar archivo', command=lambda: save_flight_plan_button()) #Todas las funciones de los botones las llamamos utilizando lambda que hace que la función solo se ejecute una vez y solo cuando se llama
save_button.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.S + tk.W)

clean_button = tk.Button(button_save_run_fileplot, text='Limpiar el plot', command=lambda: (clean_flight_plan(plot_display, actualizar_listas), actualizar_listas())) #Pasamos el argumento actualizar_listas(explicación en línea 143)
clean_button.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.S + tk.W)

#Menu y botón para desplegar información de un punto(las funciones asociadas en interface_functions.py)
plot_node_display = tk.LabelFrame(root, text='Información de un punto')
plot_node_display.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
plot_node_display.columnconfigure(0, weight=1)
plot_node_display.columnconfigure(1, weight=1)
plot_node_display.rowconfigure(0, weight=1)
plot_node_display.rowconfigure(1, weight=1)

sa_nodo = tk.StringVar(value='punto')
nodes_menu = tk.OptionMenu(plot_node_display, sa_nodo, *[node.name for node in g.nodes])
nodes_menu.grid(row=0, column=0, columnspan=2, padx=5, pady=5,sticky='ew')

mostrar_button = tk.Button(plot_node_display, text='Mostrar', command=lambda: show_plot_node(sa_nodo.get(), plot_display))
mostrar_button.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

back_button = tk.Button(plot_node_display, text='Volver al plot', command=lambda: show_initial_plot(plot_display))
back_button.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

#Botones y menu desplegable para crear segmentos(las funciones asociadas en interface_functions.py)
segment_creator_display = tk.LabelFrame(root, text='Crear segmentos')
segment_creator_display.grid(row=2, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
segment_creator_display.columnconfigure(0, weight=1)
segment_creator_display.columnconfigure(1, weight=1)
segment_creator_display.rowconfigure(0, weight=1)
segment_creator_display.rowconfigure(1, weight=1)
segment_creator_display.rowconfigure(2, weight=1)

sa_nodo_origen = tk.StringVar(value='inicio')
sa_nodo_destino = tk.StringVar(value='destino')

nodes_origin_menu = tk.OptionMenu(segment_creator_display, sa_nodo_origen, *[node.name for node in g.nodes])
nodes_origin_menu.grid(row=0, column=0, padx=5, pady=5,sticky='ew')

nodes_dest_menu = tk.OptionMenu(segment_creator_display, sa_nodo_destino, *[node.name for node in g.nodes])
nodes_dest_menu.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

create_button = tk.Button(segment_creator_display, text='Crear', command=lambda: (segment_creator(sa_nodo_origen.get(), sa_nodo_destino.get(), plot_display, actualizar_listas), actualizar_listas())) #Pasamos el argumento actualizar_listas(explicación en línea 143)
create_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

#Conjunto para botones de borrar puntos y segmentos
nodes_segments_deleter_display = tk.LabelFrame(root, text='Borrar elementos')
nodes_segments_deleter_display.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N + tk.E + tk.W + tk.S)
nodes_segments_deleter_display.columnconfigure(0, weight=1)
nodes_segments_deleter_display.columnconfigure(1, weight=1)
nodes_segments_deleter_display.rowconfigure(0, weight=1)
nodes_segments_deleter_display.rowconfigure(1, weight=1)
nodes_segments_deleter_display.rowconfigure(2, weight=1)

#Botones y menu desplegable para borrar nodos y segmentos(las funciones asociadas en interface_functions.py)
sa_nodo_borrar = tk.StringVar(value='puntos')
sa_segmento_borrar = tk.StringVar(value='segmentos')

nodes_options_menu = tk.OptionMenu(nodes_segments_deleter_display, sa_nodo_borrar, *[node.name for node in g.nodes])
nodes_options_menu.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

segments_option_menu = tk.OptionMenu(nodes_segments_deleter_display, sa_segmento_borrar, *[nodes.name for nodes in g.segments])
segments_option_menu.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

delete_button = tk.Button(nodes_segments_deleter_display, text='Borrar', command=lambda: (borrar_punto_segmento(actualizar_listas, plot_display, sa_nodo_borrar.get(), sa_segmento_borrar.get()), actualizar_listas())) #Pasamos el argumento actualizar_listas(explicación en línea 143)
delete_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

show_initial_plot(plot_display, actualizar_listas) #Esto nos permitirá mostrar nuestro plot inicialmente en la interfaz, tenemos que pasarle actualizar_listas porque esa función la requerimos para el evento de clic que nos crea puntos, lo que hará que al crear se actualicen las listas

root.mainloop() #Encendemos la aplicación