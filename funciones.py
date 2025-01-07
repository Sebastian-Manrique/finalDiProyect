#Funciones

def configure_grid(ventana, filas, columnas):
    """Configura una cuadrícula para ser responsiva."""
    for i in range(filas):
        ventana.grid_rowconfigure(i, weight=1)
    for j in range(columnas):
        ventana.grid_columnconfigure(j, weight=1)


def centrarPantalla(ventana, ancho_ventana, alto_ventana):
    """Centrar la ventana en la pantalla."""  # No está en una clase ni en otra porque ambas la usan.
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    pos_x = (ancho_pantalla // 2) - (ancho_ventana // 2)
    pos_y = (alto_pantalla // 2) - (alto_ventana // 2)
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")