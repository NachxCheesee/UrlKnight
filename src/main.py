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
# Utilizado para obtener rutas temporales
import sys
import os
# Las diferentes ventanas que se muestran en CONTENIDO
from views.UrlView import UrlView
from views.AddView import AddView
from views.DeleteView import DeleteView
from views.GuideView import GuideView

# Necesario para encontrar la ruta de los assets
def rutaRecurso(relative_path):
    # Obtiene la ruta absoluta del recurso
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Si no estamos en un .exe (Pruebas de codigo etc), usamos la ruta normal
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# URLKnight hereda todo de ctk.CTk
class URLKnight(ctk.CTk):
    def __init__(self):
        super().__init__() # Esto activa las funciones internas de CustomTkinter

        # Obtenemos el ancho y alto real de TU pantalla actual (Asi aseguramos que la ventana aparezca siempre con un tamaño especifico independiente de la pantalla del monitor)
        monitor_ancho = self.winfo_screenwidth()
        monitor_alto = self.winfo_screenheight()

        # Calculamos 
        ancho_app = int(monitor_ancho * 0.50)
        alto_app = int(monitor_alto * 0.50)
        
        # Calculamos la posición para que quede centrada
        x = int((self.winfo_screenwidth() / 2) - (ancho_app / 2))
        y = int((self.winfo_screenheight() / 2) - (alto_app / 2))

        # Para que la ventana aparezca un poco más arriba
        y = y - 80

        # --- CONFIGURACION DE VENTANA ---
        self.title("URL Knight")
        # Forzamos que la app este en modo oscuro 
        ctk.set_appearance_mode("dark")
        # ancho_minimo y alto_minimo de la ventana
        self.minsize(640,450)
        # Definimos el tamaño: "ANCHO x ALTO"
        self.geometry(f"{ancho_app}x{alto_app}+{x}+{y}")
        # Imagen de icono
        ruta_icono = rutaRecurso("assets/UrlKnight.ico")
        self.iconbitmap(ruta_icono)

        # Lo declaramos (necesario para las Views de CONTENIDO)
        self.logic = logic
        
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
        # Llamamos en seguida a la pantalla de Urls
        self.mostrarPantallaUrls()

    # --- CONFIGURACION CONTENEDORES --- 

    def contenedores(self):
        # Frame del Menú Lateral
        self.menu_lateral = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        # Frame de Contenido
        self.contenido = ctk.CTkFrame(self, fg_color="transparent")
        self.contenido.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)


    # --- FUNCION GLOBAL --- 

    def limpiarContenido(self):
        # Buscamos cada objeto en el frame CONTENIDO y lo BORRAMOS
        for widget in self.contenido.winfo_children():
            widget.destroy()

    # --- CONFIGURACION MENU ---

    def configuracionMenu(self):

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
        # BORRAMOS el contenedor central como siempre
        self.limpiarContenido()
        # Instanciamos tu nueva clase externa pasándole self (este archivo main)
        pantalla = UrlView(self.contenido, self)
        # La empaquetamos para que ocupe todo el espacio central responsivo
        pantalla.pack(fill="both", expand=True)

    def mostrarPantallaAgregarUrl(self):
        self.limpiarContenido() 
        pantalla = AddView(self.contenido, self)
        pantalla.pack(fill="both", expand=True)

    def mostrarPantallaEliminarUrl(self):
        self.limpiarContenido() # Borramos lo que haya
        pantalla = DeleteView(self.contenido, self)
        pantalla.pack(fill="both", expand=True)

    def mostrarPantallaGuiaPortabilidad(self):
        self.limpiarContenido() # Borramos lo que haya
        pantalla = GuideView(self.contenido, self)
        pantalla.pack(fill="both", expand=True)

if __name__ == "__main__":
    # Apenas se inicie la app

    logic.inicio() # llamamos a logic para que cree el archivo de guardado json

    # Cierre de la Splash Screen
    try:
        import pyi_splash # type: ignore
        pyi_splash.close()
    except ImportError:
        pass

    app = URLKnight() # Creamos la instancia de nuestra clase
    app.mainloop()    # Iniciamos el bucle de la app
