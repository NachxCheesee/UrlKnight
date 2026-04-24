# Copyright 2026 Ignacio Catalán
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# importamos la libreria de la interfaz grafica
import customtkinter as ctk
# el archivo .py de logic en el cual esta la logica para el guardado local
import logic
# libreria para dar mensajes profesionales
from CTkMessagebox import CTkMessagebox
# Utilizado para obtener rutas temporales
import sys
import os

# Necesario para encontrar la ruta de los assets
def rutaRecurso(relative_path):
    # Obtiene la ruta absoluta del recurso
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si no estamos en un .exe, usamos la ruta normal
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# URLKnight hereda todo de ctk.CTk
class URLKnight(ctk.CTk):
    def __init__(self):
        super().__init__() # Esto activa las funciones internas de CustomTkinter

        # Obtenemos el ancho y alto real de TU pantalla actual (Asi aseguramos que la ventana aparezca siempre con un tamaño especifico independiente de la pantalla )
        monitor_ancho = self.winfo_screenwidth()
        monitor_alto = self.winfo_screenheight()

        # Calculamos 
        ancho_app = int(monitor_ancho * 0.50)
        alto_app = int(monitor_alto * 0.50)
        
        # 2. Calculamos la posición para que quede centrada
        x = int((self.winfo_screenwidth() / 2) - (ancho_app / 2))
        y = int((self.winfo_screenheight() / 2) - (alto_app / 2))

        # Para que la ventana aparezca un poco más arriba
        y = y - 80

        # --- CONFIGURACION DE VENTANA ---
        self.title("URL Knight")
        # Forzamos que la app este en modo oscuro 
        ctk.set_appearance_mode("dark")
        # ancho_minimo y alto_minimo de la ventana
        self.minsize(640,360)
        # Definimos el tamaño: "ANCHO x ALTO"
        self.geometry(f"{ancho_app}x{alto_app}+{x}+{y}")
        # Imagen de icono
        ruta_icono = rutaRecurso("assets/UrlKnight.ico")
        self.iconbitmap(ruta_icono)

        # ESTRUCTURA DE CELDAS (Grid)
        # Columna 0 (Menú) - No se estira
        self.grid_columnconfigure(0, weight=0)
        # Columna 1 (Contenido) - Se estira todo lo que pueda
        self.grid_columnconfigure(1, weight=1)
        # Fila 0 - Se estira hacia abajo
        self.grid_rowconfigure(0, weight=1)

        # CREACIÓN DE LOS CONTENEDORES
        self.contenedores()
        self.configuracionMenu()
        self.mostrarPantallaUrls()

    # --- CONFIGURACION CONTENEDORES --- 

    def contenedores(self):
        # Frame del Menú Lateral
        self.menu_lateral = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        # Frame de Contenido
        self.contenido = ctk.CTkFrame(self, fg_color="transparent")
        self.contenido.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def limpiarContenido(self):
        # Buscamos cada objeto en el frame contenido y lo sacamos
        for widget in self.contenido.winfo_children():
            widget.destroy()

    # --- CONFIGURACION MENU ---

    def configuracionMenu(self):

        # padx lado a lado 
        # pady arriba y abajo
        self.tituloMenu = ctk.CTkLabel(self.menu_lateral, text="URL KNIGHT", font=("Arial", 20, "bold"))
        self.tituloMenu.pack(pady=30, padx=10)

        # Botón 1:
        self.btnUrlMenu = ctk.CTkButton(
            self.menu_lateral, 
            text="Mis rutas", 
            command=self.mostrarPantallaUrls
        )
        self.btnUrlMenu.pack(pady=10, padx=20, fill="x")

        # Botón 2: 
        self.btnAgregarMenu = ctk.CTkButton(
            self.menu_lateral, 
            text="Añadir Url", 
            command=self.mostrarPantallaAgregarUrl
        )
        self.btnAgregarMenu.pack(pady=10, padx=20, fill="x")

        # Botón 3: 
        self.btnEliminarMenu = ctk.CTkButton(
            self.menu_lateral, 
            text="Eliminar Url", 
            command=self.mostrarPantallaEliminarUrl
        )
        self.btnEliminarMenu.pack(pady=10, padx=20, fill="x")

        self.btnPortabilidadMenu = ctk.CTkButton(
            self.menu_lateral, 
            text="Guia de Portabilidad", 
            command=self.mostrarPantallaGuiaPortabilidad
        )
        self.btnPortabilidadMenu.pack(pady=10, padx=20, fill="x")

    # --- CONFIGURACION PANTALLAS EN CONTENIDO ---

    def mostrarPantallaUrls(self):

        self.limpiarContenido() # Borramos lo que haya
        
        # Dibujamos la pantalla
        self.tituloUrls = ctk.CTkLabel(self.contenido, text="⚔️ ELIGE TU DESTINO ⚔️", font=("Arial", 24, "bold"))
        self.tituloUrls.pack(pady=20)

        # Creamos la caja con scroll
        # Le damos un ancho y un alto relativo al contenedor
        self.scrollUrls = ctk.CTkScrollableFrame(
            self.contenido, 
            width=500, 
            height=300
        )
        self.scrollUrls.pack(pady=10, fill="both", expand=True)

        # Revisamos al informacion del json y la agregamos como botones al scroll
        for alias, url in logic.diccionario.items():
            btn = ctk.CTkButton(self.scrollUrls, text=alias, command=lambda n=alias: self.clickBoton(n), width=400)
            btn.pack(pady=10, padx=15, fill = "x")

        # Si el usuario no tiene nada guardado mostramos el siguiente mensaje
        if len(logic.diccionario) == 0:
            self.noHayNadaUrls = ctk.CTkLabel(self.scrollUrls, text="⚔️ ¡No tienes ninguna Url guardada! ⚔️", font=("Arial", 12, "bold"))
            self.noHayNadaUrls.pack(pady=20)

    def mostrarPantallaAgregarUrl(self):
        self.limpiarContenido() # Borramos lo que haya
        
        self.tituloAgregar = ctk.CTkLabel(self.contenido, text="📜 AÑADIR URL 🛡️", font=("Arial", 24, "bold"))
        self.tituloAgregar.pack(pady=20)


        self.entradaAliasAgregar = ctk.CTkEntry(self.contenido, placeholder_text="Ingresa tu alias aqui...", width=400)
        self.entradaAliasAgregar.pack(pady=10)

        self.entradaUrlAgregar = ctk.CTkEntry(self.contenido, placeholder_text="Ingresa tu url aqui...", width=400)
        self.entradaUrlAgregar.pack(pady=10)

        self.btnAgregarUrlAgregar = ctk.CTkButton(
            self.contenido, 
            text="Agregar Url",
            width=200,
            command=self.agregarUrl
        )
        self.btnAgregarUrlAgregar.pack(pady=10, padx=20)

    def mostrarPantallaEliminarUrl(self):
        self.limpiarContenido() # Borramos lo que haya
        
        self.tituloEliminar = ctk.CTkLabel(self.contenido, text="❌ ELIMINAR URL ❌", font=("Arial", 24, "bold"))
        self.tituloEliminar.pack(pady=20)


        self.entradaAliasEliminar = ctk.CTkEntry(self.contenido, placeholder_text="Ingresa tu alias aqui...", width=400)
        self.entradaAliasEliminar.pack(pady=10)

        self.btnEliminarUrlEliminar = ctk.CTkButton(
            self.contenido, 
            text="Eliminar Url",
            width=200,
            command=self.eliminarUrl
        )
        self.btnEliminarUrlEliminar.pack(pady=10, padx=20)

    def mostrarPantallaGuiaPortabilidad(self):
        self.limpiarContenido() # Borramos lo que haya
        
        self.tituloGuia = ctk.CTkLabel(self.contenido, text="📜 GUIA DE PORTABILIDAD 📜", font=("Arial", 24, "bold"))
        self.tituloGuia.pack(pady=20)

        # 1. Creamos el CTkTextbox
        # wrap="word" es para que el texto no se corte a la mitad de una palabra
        self.textoGuia = ctk.CTkTextbox(
            self.contenido, 
            font=("Segoe UI", 14),
            wrap="word",
            border_width=2,
            fg_color="#2b2b2b",
            text_color="#dce4ee"
        )
        
        # 'fill="both"' y 'expand=True' hacen que el cuadro crezca con la ventana
        self.textoGuia.pack(padx=10, pady=10, fill="both", expand=True)

        # 2. El contenido de tu guía
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

        # 3. Insertamos el texto
        self.textoGuia.insert("0.0", contenidoGuia)

        # 4. IMPORTANTE: Hacemos que sea de solo lectura para el usuario
        self.textoGuia.configure(state="disabled")

    # --- FUNCIONES DE LOS BOTONES ---

    def clickBoton(self, nombre):
        
        logic.abrirUrl(nombre)

    def agregarUrl(self):
        alias = self.entradaAliasAgregar.get()
        url = self.entradaUrlAgregar.get()
        
        # Realizamos las verificaciones antes de llamar a logic
        if not alias.strip() or not url.strip():
            self.mostrarCamposObligatorios()
        elif alias in logic.diccionario:
            self.mostrarAliasExiste()
        elif alias.startswith(("http://", "https://")):
            self.mostrarAliasInvalido()
        elif not url.startswith(("http://", "https://")):
            self.mostrarUrlInvalida()
        else:
            self.mostrarGuardadoExitoso()
            logic.agregarUrl(alias, url)
        
        # Limpiamos los campos de texto
        self.entradaAliasAgregar.delete(0, 'end')
        self.entradaUrlAgregar.delete(0, 'end')


    def eliminarUrl(self):
        alias = self.entradaAliasEliminar.get()

        # Realizamos las verificaciones antes de llamar a logic
        if not alias.strip():
            self.mostrarCamposObligatorios()
        elif alias in logic.diccionario:
            logic.eliminarUrl(alias)
            self.mostrarBorradoExitoso()
        else:
            self.mostrarAliasNotFound()


        self.entradaAliasEliminar.delete(0, 'end')

    # --- MENSAJES DE WINDOWS ---

    def mostrarAliasInvalido(self):
        CTkMessagebox(title="Error", message="¡Alias invalido! Asegúrate de que NO empiece con http:// o https://", icon="cancel")

    def mostrarGuardadoExitoso(self):
        CTkMessagebox(title="Éxito", message="¡URL guardada correctamente!", icon="check")

    def mostrarUrlInvalida(self):
        CTkMessagebox(title="Error", message="¡Url invalido! Asegúrate de que empiece con http:// o https://", icon="cancel")
    
    def mostrarBorradoExitoso(self):
        CTkMessagebox(title="Éxito", message="¡URL borrada correctamente!", icon="check")

    def mostrarCamposObligatorios(self):

        CTkMessagebox(title="Error", message="¡Todos los campos son obligatorios!", icon="cancel")

    def mostrarAliasNotFound(self):
        CTkMessagebox(title="Error", message="¡Alias no encontrado!", icon="cancel")
    
    def mostrarAliasExiste(self):
        CTkMessagebox(title="Error", message="¡Ya existe un Alias con ese nombre!", icon="cancel")


if __name__ == "__main__":

    logic.inicio() # llamamos a logic para que cree el archivo de guardado json

    # 🛡️ Cierre de la Splash Screen
    try:
        import pyi_splash # type: ignore
        pyi_splash.close()
    except ImportError:
        pass

    app = URLKnight() # Creamos la instancia de nuestra clase
    app.mainloop()    # Iniciamos el corazón de la app
