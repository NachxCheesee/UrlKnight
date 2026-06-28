import customtkinter as ctk
from components import Alerts as alerts

class UrlView(ctk.CTkFrame):
    def __init__(self, parent, main):
        super().__init__(parent, fg_color="transparent")
        self.main = main
        
        # Estructuras de control internas para la vista
        self.botonesRutas = {}
        self.listaRutasSeleccionadas = []
        
        # Construir la interfaz de inmediato
        self.createWidgets()

    def createWidgets(self):
        self.tituloUrls = ctk.CTkLabel(self, text="⚔️ ELIGE TU DESTINO ⚔️", font=("Arial", 24, "bold"))
        self.tituloUrls.pack(pady=20, side="top")

        self.scrollUrls = ctk.CTkScrollableFrame(
            self, 
            width=500, 
            height=250
        )

        # Usamos el diccionario cargado en el main (main.py)
        for alias, url in self.main.logic.diccionario.items():
            btn = ctk.CTkButton(self.scrollUrls, text=alias, command=lambda n=alias: self.clickBoton(n), width=400)
            btn.pack(pady=10, padx=15, fill="x")
            self.botonesRutas[alias] = btn

        # Si el JSON esta vacio mostramos el siguiete mensaje en la pantalla
        if len(self.main.logic.diccionario) == 0:
            self.noHayNadaUrls = ctk.CTkLabel(self.scrollUrls, text="⚔️ ¡No tienes ninguna Url guardada! ⚔️", font=("Arial", 12, "bold"))
            self.noHayNadaUrls.pack(pady=10)

        
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

        self.scrollUrls.pack(pady=10, fill="both", expand=True)

    # ---------- BOTONES -------------------------------------------

    # AL MOMENTO DE SELECCIONAR UNA URL
    def clickBoton(self, nombre):
        # SI el modo de seleccion multiple esta acivo
        if self.switchMultipleUrl.get() == 1:
            # LOGICA: Permite duplicados agregando directo a la lista
            self.listaRutasSeleccionadas.append(nombre)
            
            # DISEÑO: Cambia el botón a color dorado de selección
            self.botonesRutas[nombre].configure(fg_color="#b58d3d")
            
            # DINÁMICO: Crea la insignia en el scroll horizontal
            btn_badge = ctk.CTkButton(
                self.scrollHorizontalUrl,
                text=f" 🔗 {nombre}  ✕ ",
                font=("Arial", 12, "bold"),
                fg_color="#3a3a3a",
                hover_color="#551a1a",
                width=80,
                height=25,
                corner_radius=6
            )
            btn_badge.configure(command=lambda b=btn_badge, a=nombre: self.quitarRutaEspecifica(b, a))
            btn_badge.pack(side="left", padx=5, pady=10)
        else:
            # Abrimos la Url de manera normal
            self.main.logic.abrirUrl(nombre)

    def alternarModoMultiple(self):
        if self.switchMultipleUrl.get() == 1:
            self.scrollHorizontalUrl.pack(fill="both", expand=True)
            
            self.btnLanzarMultiple.pack(side="left", padx=20)
        else:
            self.scrollHorizontalUrl.pack_forget()
            self.btnLanzarMultiple.pack_forget()
            
            for widget in self.scrollHorizontalUrl.winfo_children():
                widget.destroy()

            self.listaRutasSeleccionadas.clear()
            for btn in self.botonesRutas.values():
                btn.configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])

    def lanzarUrlsMultiples(self):
        if not self.listaRutasSeleccionadas:
            alerts.mostrarUrlMultipleNo()
            return
        
        # Abre todas las URLs seleccionadas en un bucle
        for alias in self.listaRutasSeleccionadas:
            self.main.logic.abrirUrl(alias)
            
        # Apaga el modo automáticamente al terminar el lanzamiento
        self.switchMultipleUrl.deselect()
        self.alternarModoMultiple()

    # PARA QUITAR UNA URL EN EL MODO DE SELECCION MULTIPLE
    def quitarRutaEspecifica(self, boton_badge, alias):
        # LOGICA: Sacamos solo UNA instancia de ese alias de la lista
        if alias in self.listaRutasSeleccionadas:
            self.listaRutasSeleccionadas.remove(alias)
            
        # DINÁMICO: Destruimos físicamente ese botón de la barra horizontal
        boton_badge.destroy()
        
        # DISEÑO: Si ya no quedan más copias de ese alias en la lista, devolvemos el botón de arriba a su color normal
        if alias not in self.listaRutasSeleccionadas:
            self.botonesRutas[alias].configure(fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"])


if __name__ == "__main__":
    pass