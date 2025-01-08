from PIL import Image
import customtkinter as ctk

class SimpleImageButtonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Botón con Imagen")
        self.geometry("200x200")

        # Cargar la imagen
        self.image = self.load_image("imagenes/1.png")

        # Crear el botón con el texto "?" inicialmente
        self.button = ctk.CTkButton(self, text="?", width=80, height=80,command=self.show_image,
                                    font=("Arial", 20), text_color="black")
        self.button.pack(pady=60)

    def load_image(self, path):
        """Carga una imagen desde la ruta especificada y la convierte a CTkImage."""
        img = Image.open(path)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(80, 80))
        return ctk_img

    def show_image(self):
        """Muestra la imagen en el botón."""
        self.button.configure(image=self.image, text="")
        # Deshabilitar el botón para que no se pueda hacer clic nuevamente
        self.button.configure(state="disabled")

if __name__ == "__main__":
    app = SimpleImageButtonApp()
    app.mainloop()