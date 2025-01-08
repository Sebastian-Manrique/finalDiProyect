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

    def generate_symbols(self):
        """Genera una lista de pares de símbolos aleatorios."""
        # Generar la base de símbolos: letras y emojis
        base_symbols = [chr(i) for i in range(65, 65 + self.pairs - 2)]  # Letras A, B, C...
        base_symbols += ["🍎", "🍇"]  # Añadir los emojis como símbolos únicos

        # Ajustar para tener exactamente 10 pares
        symbols = base_symbols[:self.pairs] * 2  # Recorta a 10 pares y duplica
        random.shuffle(symbols)  # Baraja los símbolos

        # DEBUG: Imprime los símbolos en formato de tablero
        print("\nTablero generado:")
        for i in range(self.rows):
            row = symbols[i * self.columns:(i + 1) * self.columns]  # Slice para obtener cada fila
            print("[" + "][".join(row) + "]")  # Formato de fila con corchetes

        return symbols

    def create_board(self):
        """Crea los botones en el tablero."""
        for row in range(self.rows):
            for col in range(self.columns):
                btn = ctk.CTkButton(self, text="?", width=80, height=80,
                                    command=lambda r=row, c=col: self.reveal_tile(r, c), font=("Arial", 20),
                                    text_color="black")
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                self.buttons[(row, col)] = btn

    def reveal_tile(self, row, col):
        """Revela el símbolo en la celda seleccionada."""
        if (row, col) in self.revealed or len(self.revealed) == 2:
            return  # No se puede revelar más de dos a la vez

        idx = row * self.columns + col  # Índice en la lista de símbolos
        symbol = self.symbols[idx]  # Obtiene el símbolo para esa celda
        self.buttons[(row, col)].configure(text=symbol, state="disabled", text_color="black")  # Muestra el símbolo
        self.revealed.append((row, col))

        if len(self.revealed) == 2:  # Si hay dos revelados, comprueba coincidencia
            self.after(1000, self.check_match)  # Espera 1 segundo para comprobar

    def check_match(self):
        """Comprueba si las celdas reveladas coinciden."""
        (r1, c1), (r2, c2) = self.revealed
        idx1 = r1 * self.columns + c1
        idx2 = r2 * self.columns + c2

        if self.symbols[idx1] == self.symbols[idx2]:  # Si coinciden
            self.matched_pairs += 1
            self.buttons[(r1, c1)].configure(text="✔", fg_color="green")
            self.buttons[(r2, c2)].configure(text="✔", fg_color="green")
        else:  # Si no coinciden
            self.buttons[(r1, c1)].configure(text="?", state="normal")
            self.buttons[(r2, c2)].configure(text="?", state="normal")

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
