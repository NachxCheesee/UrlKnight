import customtkinter as ctk


class GuideView(ctk.CTkFrame):
    def __init__(self, parent, main):
        super().__init__(parent, fg_color="transparent")
        self.main = main
        
        # Construir la interfaz de inmediato
        self.createWidgets()

    def createWidgets(self): # <-- ¡Corregido: faltaba el (self)!
        # Todo se monta directo en 'self'
        self.tituloGuia = ctk.CTkLabel(self, text="📜 GUIA DE PORTABILIDAD 📜", font=("Arial", 24, "bold"))
        self.tituloGuia.pack(pady=20)

        # Creamos el CTkTextbox
        # wrap="word" es para que el texto no se corte a la mitad de una palabra
        self.textoGuia = ctk.CTkTextbox(
            self, 
            font=("Segoe UI", 14),
            wrap="word",
            border_width=2,
            fg_color="#2b2b2b",
            text_color="#dce4ee"
        )
        
        # 'fill="both"' y 'expand=True' hacen que el cuadro crezca con la ventana
        self.textoGuia.pack(padx=10, pady=10, fill="both", expand=True)

        # El contenido de tu guía
        contenidoGuia = (
            "Guía del Caballero Nómada: Cómo llevar tu información a todos lados\n\n"
            "¡Felicidades! Tienes en tus manos una herramienta diseñada para la libertad. "
            "UrlKnight no necesita instalación, pero para que tus datos viajen seguros contigo, "
            "sigue estas reglas de honor:\n\n"
            "1. EL COFRE DEL TESORO (LA CARPETA)\n"
            "Aunque el programa es un solo archivo .exe, este genera su propia \"bóveda\" "
            "de datos llamada UrlKnightData.json. Regla de Oro: Mantén siempre el archivo .exe "
            "y el .json en la misma carpeta.\n\n"
            "2. CÓMO MOVER TUS DATOS A UN PENDRIVE \n"
            "Si vas a usar el Knight en la universidad o en el trabajo:\n"
            "- Copia la carpeta completa de UrlKnight a tu pendrive.\n"
            "- Al llegar al otro PC, abre la carpeta y ejecuta el UrlKnight.exe.\n"
            "- ¡Listo! Verás todos tus links tal cual los dejaste en casa.\n\n"
            "3. PREGUNTAS FRECUENTES DEL VIAJERO \n\n"
            "* ¿Puedo crear un acceso directo?\n"
            "Sí, pero hazlo desde el pendrive. No muevas el .exe solo al escritorio del otro PC "
            "o no encontrará tus links.\n\n"
            "* ¿Perdí mis links?\n"
            "Revisa que el archivo UrlKnightData.json esté al lado del programa. Si lo borras, "
            "el Knight empezará de cero.\n\n"
            "* ¿Cómo hago un respaldo?\n"
            "Solo haz una copia del archivo UrlKnightData.json en tu correo o nube. "
            "¡Ahí está toda tu configuración!"
        )

        # Insertamos el texto
        self.textoGuia.insert("0.0", contenidoGuia)

        # Hacemos que sea de solo lectura para el usuario
        self.textoGuia.configure(state="disabled")

if __name__ == "__main__":
    pass