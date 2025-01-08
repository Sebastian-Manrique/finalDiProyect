import random
import time
from PIL import Image, ImageTk

import customtkinter as ctk

import funciones as func
from guardarGanador import guardarGanador


class MemoryGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.after(201, lambda: self.iconbitmap('imagenes/cardsIcons.ico'))
        self.title("Juego de memoria")
        func.centrarPantalla(self, 750, 750)
        self.rows = 5
        self.columns = 4
        self.pairs = (self.rows * self.columns) // 2  # Numero de pares
        self.images = self.load_images()  # Cargar imágenes
        self.symbols = self.generate_symbols()
        self.buttons = {}  # Diccionario para guardar los botones
        self.revealed = []  # Lista para celdas reveladas

        self.attempts = 0  # Contador de intentos
        self.matched_pairs = 0  # Pares encontrados

        # Configuración principal
        func.configure_grid(self, self.rows + 2, self.columns)  # Configura la cuadrícula
        self.create_board()  # Crea el tablero

        # Etiqueta de Intentos
        self.label_attempts = ctk.CTkLabel(self, text=f"Intentos: {self.attempts}", font=("Arial", 20))
        self.label_attempts.grid(row=self.rows, column=0, columnspan=self.columns, pady=10)

        self.start_time = time.time()  # Tiempo inicial
        self.timer_label = ctk.CTkLabel(self, text="Tiempo: 0s", font=("Arial", 20))
        self.timer_label.grid(row=self.rows + 1, column=0, columnspan=self.columns)
        self.update_timer()

    def create_board(self):
        """Crea los botones en el tablero."""
        for row in range(self.rows):
            for col in range(self.columns):
                btn = ctk.CTkButton(self, text="?", width=80, height=80,
                                    command=lambda r=row, c=col: self.reveal_tile(r, c),
                                    font=("Arial", 20), text_color="black")
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                self.buttons[(row, col)] = btn

    def reveal_tile(self, row, col):
        """Revela la imagen en la celda seleccionada."""
        if (row, col) in self.revealed or len(self.revealed) == 2:
            return  # No se puede revelar más de dos a la vez

        idx = row * self.columns + col  # Índice de la imagen
        image = self.symbols[idx]  # Obtiene la imagen para esa celda
        self.buttons[(row, col)].configure(image=image["image"], text="")
        self.revealed.append((row, col))

        if len(self.revealed) == 2:  # Si hay dos revelados, comprueba coincidencia
            self.after(1000, self.check_match)  # Espera 1 segundo para comprobar

    def check_match(self):
        """Comprueba si las celdas reveladas coinciden."""
        (r1, c1), (r2, c2) = self.revealed
        idx1 = r1 * self.columns + c1
        idx2 = r2 * self.columns + c2

        if self.symbols[idx1]["image"] == self.symbols[idx2]["image"]:  # Si coinciden
            self.matched_pairs += 1
            self.buttons[(r1, c1)].configure(state="disabled")
            self.buttons[(r2, c2)].configure(state="disabled")
        else:  # Si no coinciden
            self.buttons[(r1, c1)].configure(image=None, text="?")
            self.buttons[(r2, c2)].configure(image=None, text="?")

        self.revealed = []  # Reinicia las celdas reveladas
        self.attempts += 1  # Incrementa los intentos
        self.label_attempts.configure(text=f"Intentos: {self.attempts}", font=("Arial", 20))

        if self.matched_pairs == self.pairs:  # Si todos los pares están encontrados
            elapsed_time = int(time.time() - self.start_time)
            guardarGanador(elapsed_time, self.attempts).mainloop()

    def update_timer(self):
        """Actualiza el temporizador cada segundo."""
        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.configure(text=f"Tiempo: {elapsed_time}s")
        if self.matched_pairs < self.pairs:  # Sigue actualizando si el juego no ha terminado
            self.after(1000, self.update_timer)

    def load_images(self):
        """Carga las imágenes y sus nombres, y las convierte a CTkImage."""
        images = []
        for i in range(1, self.pairs + 1):  # Asume que las imágenes están numeradas de 1 a 10
            img = Image.open(f"imagenes/{i}.png")  # Carga la imagen
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))  # Convierte a CTkImage
            images.append({"image": ctk_img, "name": f"{i}"})  # Asocia la imagen con su nombre
        return images

    def generate_symbols(self):
        """Genera una lista de pares de imágenes aleatorios."""
        symbols = self.images * 2  # Crear pares de cada imagen
        random.shuffle(symbols)  # Barajar los símbolos
        return symbols

    def get_image_name(self, idx):
        """Obtiene el nombre de la imagen en un índice específico."""
        return self.symbols[idx]["name"]
