from random import randrange

import customtkinter as ctk
import pandas as pd
import datetime

import funciones as func


# Clase pregunta final
class pregunta(ctk.CTk):
    """Ventana para preguntar datos adicionales."""

    def __init__(self, tiempo: int, intentos: int):

        super().__init__()
        self.after(201, lambda: self.iconbitmap('imagenes/cardsIcons.ico'))
        self.title("Guardar nombre")
        func.centrarPantalla(self, 475, 205)
        func.configure_grid(self, 3, 1)
        # Etiqueta
        self.label_nombre = ctk.CTkLabel(self, text="Introduce tu nombre:", font=("Arial", 20))
        self.label_nombre.grid(row=0, column=0, pady=10)
        # Entrada
        self.entry_nombre = ctk.CTkEntry(self, placeholder_text="Nombre", font=("Arial", 20))
        self.entry_nombre.grid(row=1, column=0, padx=20, pady=10)
        self.entry_nombre.bind("<Return>", lambda event: self.guardarNombre(tiempo, intentos))  # Vincula Enter
        # Botón
        self.btn_confirmar = ctk.CTkButton(self, text="Confirmar", command=lambda: self.guardarNombre(tiempo, intentos),
                                           font=("Arial", 20))
        self.btn_confirmar.grid(row=2, column=0, pady=20)

    def guardarNombre(self, tiempo, intentos):
        """Metodo para guardar el nombre introducido."""
        nombre = self.entry_nombre.get()  # aqui agarra el texto
        if nombre.strip():  # Mira que no este vacio
            guardarEnCSV(tiempo+1, nombre, intentos)
            quit()
        else:
            print("El nombre no puede estar vacío.")


def guardarEnCSV(tiempo, nombre, intentos):
    """Metodo para guardar el nombre introducido."""
    if not nombre.strip():  # Si el nombre está vacío
        rndm = randrange(1000)  # Genera un número aleatorio
        nombre = f"Anonimo{rndm}"  # Asigna un nombre anónimo

    # Obtiene la fecha y hora actuales
    fecha = datetime.datetime.now()
    s = f"{tiempo}s"
    # Datos a guardar
    data = {
        "Nombre": [nombre],
        "Tiempo": [s],
        "Intentos": [intentos],
        "Fecha": [fecha.strftime("%d/%m/%Y")],
        "Hora": [fecha.strftime("%H:%M:%S")],
    }

    # Crear un DataFrame con los datos
    df = pd.DataFrame(data)

    try:
        # Intenta cargar el archivo existente
        dfCsv = pd.read_csv("partidasGuardadas.csv")

        # Combina los DataFrames y guarda el archivo
        df_combined = pd.concat([dfCsv, df], ignore_index=True)
        df_combined.to_csv("partidasGuardadas.csv", index=False)

        print("Archivo actualizado:")
        print(df_combined)

        if nombre.startswith("A"):
            quit()
    except FileNotFoundError:
        # Si el archivo no existe, crea uno nuevo con los datos actuales
        df.to_csv("partidasGuardadas.csv", index=False)
        print("Archivo creado:")
        print(df)
