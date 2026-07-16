import customtkinter as ctk
from components import Alerts as alerts

class DeleteView(ctk.CTkFrame):
    def __init__(self, parent, main):
        super().__init__(parent, fg_color="transparent")
        self.main = main
        
        # Guardamos la referencia de la ventana emergente de confirmación para que no se duplique
        self.ventanaConfirmacion = None
        
        # Construir la interfaz de inmediato al cambiar a esta pestaña
        self.createWidgets()

    def createWidgets(self):
        # Limpiamos cualquier widget residual (útil al reconstruir la vista tras borrar)
        for widget in self.winfo_children():
            widget.destroy()

        # Título principal de la vista
        self.tituloEliminar = ctk.CTkLabel(self, text="❌ ELIMINAR URL ❌", font=("Arial", 24, "bold"))
        self.tituloEliminar.pack(pady=20)

        # Obtenemos la lista actual de categorías registradas en logic
        listaCategorias = self.main.logic.obtenerCategorias()

        # --- SELECCIÓN DE CATEGORÍA ---
        self.labelCategoria = ctk.CTkLabel(self, text="Selecciona la categoría:", font=("Arial", 12, "bold"))
        self.labelCategoria.pack(pady=(10, 2))

        self.desplegableCategorias = ctk.CTkOptionMenu(
            self,
            values=listaCategorias,
            command=self.cambiarCategoria, # Al cambiar de categoría, actualizamos los alias de abajo
            fg_color="#b58d3d",
            button_color="#9c752d",
            button_hover_color="#805d21",
            font=("Arial", 14, "bold"),
            dropdown_font=("Arial", 12)
        )
        self.desplegableCategorias.pack(pady=(0, 15))

        # --- SELECCIÓN DE URL (ALIAS) ---
        self.labelUrl = ctk.CTkLabel(self, text="Selecciona la URL que deseas eliminar:", font=("Arial", 12, "bold"))
        self.labelUrl.pack(pady=(5, 2))

        # El desplegable se inicia vacío y se configura en el método cambiarCategoria
        self.desplegableUrls = ctk.CTkOptionMenu(
            self,
            values=[],
            fg_color="#b58d3d",
            button_color="#9c752d",
            button_hover_color="#805d21",
            font=("Arial", 14, "bold"),
            dropdown_font=("Arial", 12)
        )
        self.desplegableUrls.pack(pady=(0, 20))

        # --- BOTÓN DE ACCIÓN ---
        self.btnEliminarUrlEliminar = ctk.CTkButton(
            self, 
            text="Eliminar Url",
            width=200,
            fg_color="#8b0000",
            hover_color="#b22222",
            command=self.confirmarEliminacion
        )
        self.btnEliminarUrlEliminar.pack(pady=10, padx=20)

        # Forzamos la primera actualización para sincronizar las URLs de la categoría inicial activa
        if listaCategorias:
            self.cambiarCategoria(self.desplegableCategorias.get())

    # --- ACCIONES Y SINCRONIZACIÓN ---

    # Sincroniza dinámicamente el segundo menú en función de la categoría que elijas
    def cambiarCategoria(self, nuevaCategoria):
        # Buscamos el diccionario de enlaces pertenecientes a la categoría seleccionada
        enlacesDeCategoria = self.main.logic.diccionario.get(nuevaCategoria, {})
        # Obtenemos solo las llaves (los nombres o alias de las webs)
        listaUrls = list(enlacesDeCategoria.keys())

        # Si la categoría seleccionada tiene enlaces guardados
        if listaUrls:
            # Actualizamos los valores del desplegable, lo habilitamos y seleccionamos el primero
            self.desplegableUrls.configure(values=listaUrls, state="normal")
            self.desplegableUrls.set(listaUrls[0])
            # Habilitamos el botón de eliminar
            self.btnEliminarUrlEliminar.configure(state="normal")
        else:
            # Si está vacía, deshabilitamos el desplegable para evitar clicks y bloqueamos el botón de eliminar
            self.desplegableUrls.configure(values=["Sin enlaces"], state="disabled")
            self.desplegableUrls.set("Sin enlaces")
            self.btnEliminarUrlEliminar.configure(state="disabled")

    # Diseña y centra la ventana de confirmación antes de proceder a borrar del JSON
    def confirmarEliminacion(self):
        # Controlamos que no se abran ventanas flotantes duplicadas en pantalla
        if self.ventanaConfirmacion is not None and self.ventanaConfirmacion.winfo_exists():
            self.ventanaConfirmacion.focus()
            return

        # Capturamos la selección de ambos desplegables
        categoriaSeleccionada = self.desplegableCategorias.get()
        aliasSeleccionado = self.desplegableUrls.get()

        # Creamos el popup de alerta
        self.ventanaConfirmacion = ctk.CTkToplevel(self)
        self.ventanaConfirmacion.title("Confirmar Borrado")
        self.ventanaConfirmacion.resizable(False, False)
        # Forzamos la jerarquía visual para que aparezca siempre flotando sobre el resto
        self.ventanaConfirmacion.attributes("-topmost", True)

        # --- CÁLCULO DE CENTRADO DINÁMICO ---
        anchoAlerta = 400
        altoAlerta = 200

        # Capturamos las medidas actualizadas de tu pantalla y tu ventana de CustomTkinter
        self.main.update_idletasks()
        anchoPrincipal = self.main.winfo_width()
        altoPrincipal = self.main.winfo_height()
        posicionXPrincipal = self.main.winfo_x()
        posicionYPrincipal = self.main.winfo_y()

        # Ejecutamos el cálculo matemático para posicionar la ventana flotante en el centro exacto
        posicionX = posicionXPrincipal + (anchoPrincipal // 2) - (anchoAlerta // 2)
        posicionY = posicionYPrincipal + (altoPrincipal // 2) - (altoAlerta // 2)

        # Aplicamos el centrado
        self.ventanaConfirmacion.geometry(f"{anchoAlerta}x{altoAlerta}+{posicionX}+{posicionY}")

        # Mensaje del popup
        labelMensaje = ctk.CTkLabel(
            self.ventanaConfirmacion,
            text=f"¿Estás seguro de que quieres eliminar la URL:\n'{aliasSeleccionado}'\nde la categoría '{categoriaSeleccionada}'?\n\nEsta acción es irreversible.",
            font=("Arial", 12, "bold"),
            pady=20
        )
        labelMensaje.pack()

        # Contenedor de botones para centrar el diseño
        contenedorBotones = ctk.CTkFrame(self.ventanaConfirmacion, fg_color="transparent")
        contenedorBotones.pack(pady=10)

        # Botón para cerrar la alerta sin cambios
        btnCancelar = ctk.CTkButton(
            contenedorBotones,
            text="Cancelar",
            fg_color="#555555",
            hover_color="#777777",
            width=120,
            command=self.ventanaConfirmacion.destroy
        )
        btnCancelar.pack(side="left", padx=10)

        # Botón destructivo para mandar a eliminar de forma definitiva
        btnConfirmar = ctk.CTkButton(
            contenedorBotones,
            text="Sí, eliminar",
            fg_color="#8b0000",
            hover_color="#b22222",
            width=120,
            command=lambda: self.ejecutarEliminacion(categoriaSeleccionada, aliasSeleccionado)
        )
        btnConfirmar.pack(side="right", padx=10)

    # Llama a logic.py para borrar definitivamente la URL seleccionada
    def ejecutarEliminacion(self, categoria, alias):
        # Destruimos el popup de advertencia
        if self.ventanaConfirmacion is not None:
            self.ventanaConfirmacion.destroy()
            self.ventanaConfirmacion = None

        # Mandamos las variables limpias al motor logic para reescribir el JSON
        self.main.logic.eliminarUrl(categoria, alias)
        
        # Mostramos la alerta de proceso exitoso
        alerts.mostrarBorradoExitoso()

        # Reconstruimos la interfaz completa de esta pestaña para que cargue los desplegables limpios
        self.createWidgets()

if __name__ == "__main__":
    pass