import customtkinter as ctk

import preguntaFinal as prg
import guardarGanador as gdrGndr
from MemoryGame import MemoryGame

# Inicializa CustomTkinter
ctk.set_appearance_mode("System")  # Cambia entre "Dark", "Light", "System"
ctk.set_default_color_theme("blue")  # Tema de color


# Inicia el juego
if __name__ == "__main__":
    app = MemoryGame()
    app.mainloop()
    # app = gdrGndr.guardarGanador(59, 8)