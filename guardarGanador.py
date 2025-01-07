import customtkinter as ctk

import funciones as func
from preguntaFinal import pregunta, guardarEnCSV

class guardarGanador(ctk.CTk):
    """Muestra un mensaje de victoria."""

    def __init__(self, tiempo: int, intentos: int):
        super().__init__()
        self.title("Victoria")  # Título
        self.after(201, lambda: self.iconbitmap('cardsIcons.ico'))
        # Centra la pantalla con las medidas pasadas
        func.centrarPantalla(self, 500, 230)
        # Ajusta el peso de la cuadrícula
        func.configure_grid(self, 3, 3)
        # Label victoria
        self.victory_label = ctk.CTkLabel(self, text="¡Felicidades! ¡Ganaste!", font=("Arial", 25))
        self.victory_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="nsew")

        # Label info
        self.guardarInfo = ctk.CTkLabel(self, text="¿Quieres guardar los datos de la partida?", font=("Arial", 20))
        self.guardarInfo.grid(row=1, column=0, columnspan=3, pady=10, sticky="nsew")

        # Si guardar info
        btnSi = ctk.CTkButton(self, text="Si", width=200, height=50, fg_color="green", hover_color="darkgreen",
                              command=lambda: pregunta(tiempo, intentos).mainloop()
                              , font=("Arial", 20))
        btnSi.grid(row=2, column=0, pady=20, padx=10, sticky="nsew")

        # No guardar info
        btnNo = ctk.CTkButton(self, text="No", width=200, height=50, fg_color="red", hover_color="darkred",
                              command=lambda: guardarEnCSV(tiempo, "", intentos), font=("Arial", 20))
        btnNo.grid(row=2, column=2, pady=20, padx=10, sticky="nsew")

        self.mainloop()
