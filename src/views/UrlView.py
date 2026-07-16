import customtkinter as ctk
from components import Alerts as alerts

class UrlView(ctk.CTkFrame):
    def __init__(self, parent, main):
        super().__init__(parent, fg_color="transparent")
        self.main = main
        
        # Estructuras de control internas para la vista
        # Ahora mapeamos los botones usando "categoria::alias" para evitar colisiones de nombres idénticos
        self.botonesRutas = {}
        # Guarda tuplas de (categoria, alias) para saber exactamente qué lanzar en modo múltiple
        self.listaRutasSeleccionadas = []
        
        # Guardamos la categoría que se está mostrando actualmente (por defecto "Sin Categoría")
        self.categoriaActiva = self.main.logic.categoriaPorDefecto
        
        # Construir la interfaz de inmediato (esto se ejecuta cada vez que entras a la pestaña)
        self.createWidgets()

    def createWidgets(self):
        # Título principal de la vista
        self.tituloUrls = ctk.CTkLabel(self, text="⚔️ ELIGE TU DESTINO ⚔️", font=("Arial", 24, "bold"))
        self.tituloUrls.pack(pady=(20, 10), side="top")

        # --- CONTENEDOR HORIZONTAL PARA FILTROS (Desplegable + Buscador) ---
        self.contenedorFiltros = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedorFiltros.pack(pady=10, fill="x")

        # Menú desplegable de Categorías (Lado Izquierdo)
        listaCategorias = self.main.logic.obtenerCategorias()
        self.desplegableCategorias = ctk.CTkOptionMenu(
            self.contenedorFiltros,
            values=listaCategorias,
            command=self.cambiarCategoria,
            fg_color="#b58d3d",
            button_color="#9c752d",
            button_hover_color="#805d21",
            font=("Arial", 14, "bold"),
            dropdown_font=("Arial", 12)
        )
        self.desplegableCategorias.pack(side="left", padx=(10, 5), expand=True, fill="x")
        self.desplegableCategorias.set(self.categoriaActiva)

        # Barra de Búsqueda Global (Lado Derecho)
        self.entradaBusqueda = ctk.CTkEntry(
            self.contenedorFiltros,
            placeholder_text="🔍 Buscar enlace globalmente...",
            font=("Arial", 12),
            width=250
        )
        self.entradaBusqueda.pack(side="right", padx=(5, 10), expand=True, fill="x")
        # Vinculamos la barra al evento de soltar una tecla para filtrar en tiempo real
        self.entradaBusqueda.bind("<KeyRelease>", self.ejecutarBusqueda)

        # --- SCROLL DE CONTENIDO (Botones de URLs) ---
        self.scrollUrls = ctk.CTkScrollableFrame(
            self, 
            width=500, 
            height=250
        )
        self.scrollUrls.pack(pady=10, fill="both", expand=True)

        # Renderizamos los botones correspondientes a la categoría seleccionada por defecto
        self.cargarUrlsPorCategoria(self.categoriaActiva)
        
        # --- CONTROLES DE SELECCIÓN MÚLTIPLE (Banda inferior) ---
        self.contenedorOculto = ctk.CTkFrame(
            self,
            height=60,
            fg_color="transparent"
        )
        self.contenedorOculto.pack(side="bottom", fill="x", pady=5)
        self.contenedorOculto.pack_propagate(False)

        self.scrollHorizontalUrl = ctk.CTkScrollableFrame(
            self.contenedorOculto, 
            orientation="horizontal",
            fg_color="#2b2b2b"
        )

        self.contenedorControles = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedorControles.pack(side="bottom", fill="x", pady=10)

        self.switchMultipleUrl = ctk.CTkSwitch(
            self.contenedorControles, 
            text="Seleccion multiple",
            font=("Arial", 14),
            progress_color="#b58d3d",
            command=self.alternarModoMultiple
        )
        self.switchMultipleUrl.pack(side="left", padx=10)

        self.btnLanzarMultiple = ctk.CTkButton(
            self.contenedorControles, 
            text="Lanzar rutas seleccionadas 🚀",
            font=("Arial", 14, "bold"),
            fg_color="#2c6e49",
            hover_color="#4f9a69",
            command=self.lanzarUrlsMultiples
        )

    # --- LÓGICA DE CATEGORÍAS Y RENDERIZADO DINÁMICO ---

    def cargarUrlsPorCategoria(self, categoria):
        # Limpiamos cualquier widget que exista dentro del scroll de URLs
        for widget in self.scrollUrls.winfo_children():
            widget.destroy()
            
        # Reseteamos el diccionario temporal de botones en pantalla
        self.botonesRutas.clear()
        
        # Obtenemos las URLs que pertenecen únicamente a la categoría seleccionada
        enlacesDeCategoria = self.main.logic.diccionario.get(categoria, {})
        
        if len(enlacesDeCategoria) == 0:
            self.noHayNadaUrls = ctk.CTkLabel(
                self.scrollUrls, 
                text="⚔️ ¡No tienes ninguna Url guardada aquí! ⚔️", 
                font=("Arial", 12, "bold")
            )
            self.noHayNadaUrls.pack(pady=20)
            return

        # Dibujamos los botones de esta categoría en específico
        for alias, url in enlacesDeCategoria.items():
            # Creamos la clave de mapeo único
            identificador = f"{categoria}::{alias}"
            
            # Verificación inteligente de color: si ya estaba seleccionado en el modo múltiple, se dibuja dorado
            colorBoton = "#b58d3d" if (categoria, alias) in self.listaRutasSeleccionadas else ctk.ThemeManager.theme["CTkButton"]["fg_color"]
            
            btn = ctk.CTkButton(
                self.scrollUrls, 
                text=alias, 
                command=lambda c=categoria, a=alias: self.clickBoton(c, a), 
                width=400,
                fg_color=colorBoton
            )
            btn.pack(pady=10, padx=15, fill="x")
            self.botonesRutas[identificador] = btn

    def cambiarCategoria(self, nuevaCategoria):
        # Actualizamos la categoría activa interna
        self.categoriaActiva = nuevaCategoria
        
        # Limpiamos la barra de búsqueda por consistencia
        self.entradaBusqueda.delete(0, "end")
        
        # Apagamos el modo de selección múltiple por seguridad al cambiar de pestaña (Regla Opción A)
        self.switchMultipleUrl.deselect()
        self.alternarModoMultiple()
        
        # Volvemos a renderizar los botones de la nueva categoría elegida
        self.cargarUrlsPorCategoria(nuevaCategoria)

    # --- NUEVO MÉTODO: MOTOR DE BÚSQUEDA GLOBAL ---

    def ejecutarBusqueda(self, event=None):
        # Capturamos el texto en minúsculas para comparar de manera insensible
        textoBuscado = self.entradaBusqueda.get().strip().lower()
        
        # Si el buscador está vacío, salimos del Modo Búsqueda
        if not textoBuscado:
            # Re-habilitamos el desplegable de categorías
            self.desplegableCategorias.configure(state="normal")
            # Volvemos a pintar las URLs de la pestaña en la que estábamos parados
            self.cargarUrlsPorCategoria(self.categoriaActiva)
            return
            
        # Si hay texto, entramos en Modo Búsqueda Global
        # Deshabilitamos el desplegable de categorías para guiar visualmente al usuario
        self.desplegableCategorias.configure(state="disabled")
        
        # Limpiamos los botones en pantalla
        for widget in self.scrollUrls.winfo_children():
            widget.destroy()
        self.botonesRutas.clear()
        
        # Buscamos coincidencias de alias o categorías en toda la base de datos (JSON)
        resultados = []
        for categoria, enlaces in self.main.logic.diccionario.items():
            for alias, url in enlaces.items():
                # Busca si la palabra coincide en el alias o en el nombre de la categoría
                if textoBuscado in alias.lower() or textoBuscado in categoria.lower():
                    resultados.append((categoria, alias))
                    
        # Si no encontramos nada en todo el JSON
        if not resultados:
            self.noHayCoincidencias = ctk.CTkLabel(
                self.scrollUrls, 
                text="⚔️ No se encontraron enlaces que coincidan ⚔️", 
                font=("Arial", 12, "bold")
            )
            self.noHayCoincidencias.pack(pady=20)
            return
            
        # Dibujamos las coincidencias encontradas
        for categoria, alias in resultados:
            identificador = f"{categoria}::{alias}"
            
            # Mantenemos el color dorado si ya estaba seleccionado antes de buscar
            colorBoton = "#b58d3d" if (categoria, alias) in self.listaRutasSeleccionadas else ctk.ThemeManager.theme["CTkButton"]["fg_color"]
            
            # En búsqueda global, le mostramos la categoría entre corchetes para guiar al usuario
            textoBoton = f"[{categoria}] {alias}"
            
            btn = ctk.CTkButton(
                self.scrollUrls,
                text=textoBoton,
                command=lambda c=categoria, a=alias: self.clickBoton(c, a),
                width=400,
                fg_color=colorBoton
            )
            btn.pack(pady=10, padx=15, fill="x")
            self.botonesRutas[identificador] = btn

    # ---------- GESTIÓN DE EVENTOS Y CLICS -------------------------------------------

    def clickBoton(self, categoria, nombre):
        identificador = f"{categoria}::{nombre}"
        
        # Si el modo de selección múltiple está activo
        if self.switchMultipleUrl.get() == 1:
            # Añadimos la tupla única a nuestra lista
            self.listaRutasSeleccionadas.append((categoria, nombre))
            
            # Cambiamos el color del botón mapeando su identificador único
            self.botonesRutas[identificador].configure(fg_color="#b58d3d")
            
            # Creamos la insignia de selección incluyendo el nombre de la categoría para evitar dudas
            btnBadge = ctk.CTkButton(
                self.scrollHorizontalUrl,
                text=f" 🔗 [{categoria}] {nombre}  ✕ ",
                font=("Arial", 12, "bold"),
                fg_color="#3a3a3a",
                hover_color="#551a1a",
                width=80,
                height=25,
                corner_radius=6
            )
            btnBadge.configure(command=lambda b=btnBadge, c=categoria, a=nombre: self.quitarRutaEspecifica(b, c, a))
            btnBadge.pack(side="left", padx=5, pady=10)
        else:
            # Abrimos la URL mandando su categoría y nombre correspondientes de forma limpia
            self.main.logic.abrirUrl(categoria, nombre)

    def alternarModoMultiple(self):
        # Si el switch de selección múltiple se activa
        if self.switchMultipleUrl.get() == 1:
            self.scrollHorizontalUrl.pack(fill="both", expand=True)
            self.btnLanzarMultiple.pack(side="left", padx=20)
        else:
            # Si se desactiva, limpiamos e invalidamos insignias
            self.scrollHorizontalUrl.pack_forget()
            self.btnLanzarMultiple.pack_forget()
            
            for widget in self.scrollHorizontalUrl.winfo_children():
                widget.destroy()

            self.listaRutasSeleccionadas.clear()
            
            # Devolvemos todos los botones en pantalla (independientemente de si son de categoría o búsqueda) a su color normal
            for btn in self.botonesRutas.values():
                btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

    def lanzarUrlsMultiples(self):
        # Si la lista está vacía, mostramos alerta
        if not self.listaRutasSeleccionadas:
            alerts.mostrarUrlMultipleNo()
            return
        
        # Iteramos las tuplas seleccionadas para abrir cada enlace en su categoría correcta
        for categoria, alias in self.listaRutasSeleccionadas:
            self.main.logic.abrirUrl(categoria, alias)
            
        # Apagamos el modo múltiple automáticamente al finalizar
        self.switchMultipleUrl.deselect()
        self.alternarModoMultiple()

    def quitarRutaEspecifica(self, botonBadge, categoria, alias):
        identificador = f"{categoria}::{alias}"
        tuplaAEliminar = (categoria, alias)
        
        # Removemos la tupla de nuestra lista de lanzamiento
        if tuplaAEliminar in self.listaRutasSeleccionadas:
            self.listaRutasSeleccionadas.remove(tuplaAEliminar)
            
        # Destruimos la insignia física de la pantalla
        botonBadge.destroy()
        
        # Si el botón sigue renderizado en pantalla, le devolvemos su color por defecto
        if tuplaAEliminar not in self.listaRutasSeleccionadas and identificador in self.botonesRutas:
            self.botonesRutas[identificador].configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

if __name__ == "__main__":
    pass