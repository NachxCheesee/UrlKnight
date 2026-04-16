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
def ruta_recurso(relative_path):
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

        # Obtenemos el ancho y alto real de TU pantalla actual
        monitor_ancho = self.winfo_screenwidth()
        monitor_alto = self.winfo_screenheight()

        # Calculamos 
        ancho_app = int(monitor_ancho * 0.50)
        alto_app = int(monitor_alto * 0.50)
        
        # 2. Calculamos la posición para que quede centrada
        x = int((self.winfo_screenwidth() / 2) - (ancho_app / 2))
        y = int((self.winfo_screenheight() / 2) - (alto_app / 2))

        # Para que aparezca un poco más arriba
        y = y - 80

        #Configuracion de ventana
        self.title("URL Knight")
        # Forzamos que la app este en modo oscuro 
        ctk.set_appearance_mode("dark")
        # self.minsize(ancho_minimo, alto_minimo)
        self.minsize(640,360)
        # Definimos el tamaño: "ANCHO x ALTO"
        self.geometry(f"{ancho_app}x{alto_app}+{x}+{y}")
        # Imagen de icono
        ruta_icono = ruta_recurso("assets/UrlKnight.ico")
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
        self.setup_menu_widgets()
        self.mostrar_pantalla_URLS()

    # --- CONFIGURACION CONTENEDORES --- 

    def contenedores(self):
        # Frame del Menú Lateral
        self.menu_lateral = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        # Frame de Contenido
        self.contenido = ctk.CTkFrame(self, fg_color="transparent")
        self.contenido.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def limpiar_contenido(self):
        # Buscamos cada objeto en el frame contenido y lo sacamos
        for widget in self.contenido.winfo_children():
            widget.destroy()

    # --- CONFIGURACION MENU ---

    def setup_menu_widgets(self):

        # padx lado a lado 
        # pady arriba y abajo
        self.titulo = ctk.CTkLabel(self.menu_lateral, text="URL KNIGHT", font=("Arial", 20, "bold"))
        self.titulo.pack(pady=30, padx=10)

        # Botón 1:
        self.btn_URLS = ctk.CTkButton(
            self.menu_lateral, 
            text="Mostrar Urls", 
            command=self.mostrar_pantalla_URLS
        )
        self.btn_URLS.pack(pady=10, padx=20, fill="x")

        # Botón 2: 
        self.btn_agregar_Url = ctk.CTkButton(
            self.menu_lateral, 
            text="Agregar Url", 
            command=self.mostrar_pantalla_agregar_url
        )
        self.btn_agregar_Url.pack(pady=10, padx=20, fill="x")

        # Botón 3: 
        self.btn_eliminar_Url = ctk.CTkButton(
            self.menu_lateral, 
            text="Eliminar Url", 
            command=self.mostrar_pantalla_eliminar_url
        )
        self.btn_eliminar_Url.pack(pady=10, padx=20, fill="x")


    # --- CONFIGURACION PANTALLAS ---

    def mostrar_pantalla_URLS(self):

        self.limpiar_contenido() # Borramos lo que haya
        
        # Dibujamos la pantalla
        self.label_titulo = ctk.CTkLabel(self.contenido, text="⚔️ ELIGE TU DESTINO", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=20)

        # Creamos la caja con scroll
        # Le damos un ancho y un alto relativo al contenedor
        self.scroll = ctk.CTkScrollableFrame(
            self.contenido, 
            width=500, 
            height=300, 
            label_text=" "
        )
        self.scroll.pack(pady=10, fill="both", expand=True)

        for alias, url in logic.diccionario.items():
            btn = ctk.CTkButton(self.scroll, text=alias, command=lambda n=alias: self.click_boton(n), width=400)
            btn.pack(pady=10, padx=15, fill = "x")

    def mostrar_pantalla_agregar_url(self):
        self.limpiar_contenido() # Borramos lo que haya
        
        self.label_titulo = ctk.CTkLabel(self.contenido, text="📜 AGREGAR URL", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=20)


        self.entrada_alias = ctk.CTkEntry(self.contenido, placeholder_text="Ingresa tu alias aqui...", width=400)
        self.entrada_alias.pack(pady=10)

        self.entrada_url = ctk.CTkEntry(self.contenido, placeholder_text="Ingresa tu url aqui...", width=400)
        self.entrada_url.pack(pady=10)

        self.btn_agregar_Url = ctk.CTkButton(
            self.contenido, 
            text="Agregar Url",
            width=200,
            command=self.agregar_url
        )
        self.btn_agregar_Url.pack(pady=10, padx=20)

    def mostrar_pantalla_eliminar_url(self):
        self.limpiar_contenido() # Borramos lo que haya
        
        self.label_titulo = ctk.CTkLabel(self.contenido, text="📜 ELIMINAR URL", font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=20)


        self.entrada_alias = ctk.CTkEntry(self.contenido, placeholder_text="Ingresa tu alias aqui...", width=400)
        self.entrada_alias.pack(pady=10)

        self.btn_eliminar_Url = ctk.CTkButton(
            self.contenido, 
            text="Eliminar Url",
            width=200,
            command=self.eliminar_url
        )
        self.btn_eliminar_Url.pack(pady=10, padx=20)

    # --- FUNCIONES DE LOS BOTONES ---

    def click_boton(self, nombre):
        
        logic.abrirUrl(nombre)

    def agregar_url(self):
        alias = self.entrada_alias.get()
        url = self.entrada_url.get()

        if not alias.strip() or not url.strip():
            self.mostrar_campos_obligatorios()
        elif alias in logic.diccionario:
            self.mostrar_alias_existe()
        elif not url.startswith(("http://", "https://")):
            self.mostrar_url_invalida()
        else:
            self.mostrar_guardado_exitoso()
            logic.añadirUrl(alias, url)
        
        self.entrada_alias.delete(0, 'end')
        self.entrada_url.delete(0, 'end')


    def eliminar_url(self):
        alias = self.entrada_alias.get()

        if not alias.strip():
            self.mostrar_campos_obligatorios()
        else:
            if alias in logic.diccionario:
                logic.eliminarUrl(alias)
                self.mostrar_borrado_exitoso()

            else:
                self.mostrar_alias_not_Found()


        self.entrada_alias.delete(0, 'end')

    # --- MENSAJES DE WINDOWS ---

    def mostrar_guardado_exitoso(self):
        CTkMessagebox(title="Éxito", message="¡URL guardada correctamente!", icon="check")

    def mostrar_url_invalida(self):
        CTkMessagebox(title="Error", message="¡Url invalida! Asegúrate de que empiece con http:// o https://", icon="cancel")
    
    def mostrar_borrado_exitoso(self):
        CTkMessagebox(title="Éxito", message="¡URL borrada correctamente!", icon="check")

    def mostrar_campos_obligatorios(self):

        CTkMessagebox(title="Atención", message="¡Todos los campos son obligatorios!", icon="warning")

    def mostrar_alias_not_Found(self):
        CTkMessagebox(title="Error", message="¡Alias no encontrado!", icon="cancel")
    
    def mostrar_alias_existe(self):
        CTkMessagebox(title="Error", message="¡Ya existe un Alias con ese nombre!", icon="cancel")


if __name__ == "__main__":
    logic.inicio()
    app = URLKnight() # Creamos la instancia de nuestra clase
    app.mainloop()    # Iniciamos el corazón de la app