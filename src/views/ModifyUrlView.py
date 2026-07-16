import customtkinter as ctk
from components import Alerts as alerts

class ModifyUrlView(ctk.CTkFrame):
    def __init__(self, parent, main):
        super().__init__(parent, fg_color="transparent")
        self.main = main
        
        # Variable para controlar el popup de confirmación centrado
        self.ventanaConfirmacion = None
        
        # Construir la interfaz de inmediato al cambiar a esta pestaña
        self.createWidgets()

    def createWidgets(self):
        # Limpiamos cualquier widget residual
        for widget in self.winfo_children():
            widget.destroy()

        # Título principal de la vista
        self.tituloModificar = ctk.CTkLabel(self, text="📝 MODIFICAR URL 🛡️", font=("Arial", 24, "bold"))
        self.tituloModificar.pack(pady=15)

        # Obtenemos las categorías para alimentar los desplegables
        listaCategorias = self.main.logic.obtenerCategorias()

        # --- SECCIÓN 1: SELECCIÓN DEL ENLACE ACTUAL ---
        self.contenedorSeleccion = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedorSeleccion.pack(pady=5, fill="x")

        # Desplegable para la Categoría de Origen
        self.labelOrigen = ctk.CTkLabel(self.contenedorSeleccion, text="Categoría de origen:", font=("Arial", 12, "bold"))
        self.labelOrigen.pack(pady=(5, 2))

        self.desplegableCategoriaOrigen = ctk.CTkOptionMenu(
            self.contenedorSeleccion,
            values=listaCategorias,
            command=self.cambiarCategoriaOrigen, # Sincroniza las URLs al cambiar de origen
            fg_color="#b58d3d",
            button_color="#9c752d",
            button_hover_color="#805d21",
            font=("Arial", 13, "bold")
        )
        self.desplegableCategoriaOrigen.pack(pady=(0, 10))

        # Desplegable para seleccionar el Link de esa categoría
        self.labelLink = ctk.CTkLabel(self.contenedorSeleccion, text="Enlace a modificar:", font=("Arial", 12, "bold"))
        self.labelLink.pack(pady=(5, 2))

        self.desplegableUrls = ctk.CTkOptionMenu(
            self.contenedorSeleccion,
            values=[],
            command=self.cargarDatosUrl, # Rellena los inputs de abajo al cambiar de link
            fg_color="#b58d3d",
            button_color="#9c752d",
            button_hover_color="#805d21",
            font=("Arial", 13, "bold")
        )
        self.desplegableUrls.pack(pady=(0, 10))

        # --- SECCIÓN 2: FORMULARIO DE EDICIÓN ---
        self.contenedorEdicion = ctk.CTkFrame(self, fg_color="transparent")
        self.contenedorEdicion.pack(pady=10, fill="x")

        # Entrada para modificar el nombre (Alias)
        self.labelNuevoAlias = ctk.CTkLabel(self.contenedorEdicion, text="Nuevo Nombre / Alias:", font=("Arial", 12, "bold"))
        self.labelNuevoAlias.pack(pady=(5, 2))

        self.entradaNuevoAlias = ctk.CTkEntry(self.contenedorEdicion, placeholder_text="Nombre del link...", width=400)
        self.entradaNuevoAlias.pack(pady=(0, 10))

        # Entrada para modificar la URL física
        self.labelNuevaUrl = ctk.CTkLabel(self.contenedorEdicion, text="Nueva dirección URL:", font=("Arial", 12, "bold"))
        self.labelNuevaUrl.pack(pady=(5, 2))

        self.entradaNuevaUrl = ctk.CTkEntry(self.contenedorEdicion, placeholder_text="https://...", width=400)
        self.entradaNuevaUrl.pack(pady=(0, 10))

        # Desplegable para seleccionar la Categoría de Destino (para mover el link de carpeta)
        self.labelDestino = ctk.CTkLabel(self.contenedorEdicion, text="Mover a categoría:", font=("Arial", 12, "bold"))
        self.labelDestino.pack(pady=(5, 2))

        self.desplegableCategoriaDestino = ctk.CTkOptionMenu(
            self.contenedorEdicion,
            values=listaCategorias,
            fg_color="#b58d3d",
            button_color="#9c752d",
            button_hover_color="#805d21",
            font=("Arial", 13, "bold")
        )
        self.desplegableCategoriaDestino.pack(pady=(0, 15))

        # --- BOTÓN PRINCIPAL PARA GUARDAR ---
        self.btnGuardarCambios = ctk.CTkButton(
            self,
            text="Guardar Cambios",
            width=200,
            fg_color="#2c6e49",
            hover_color="#4f9a69",
            command=self.confirmarModificacion
        )
        self.btnGuardarCambios.pack(pady=10)

        # Inicialización del estado dinámico de los componentes
        if listaCategorias:
            self.cambiarCategoriaOrigen(self.desplegableCategoriaOrigen.get())

    # --- CONTROL DE FLUJO Y SINCRONIZACIÓN ---

    # Al cambiar la categoría de origen, actualizamos la lista de enlaces de ese cajón
    def cambiarCategoriaOrigen(self, nuevaCategoria):
        enlacesDeCategoria = self.main.logic.diccionario.get(nuevaCategoria, {})
        listaUrls = list(enlacesDeCategoria.keys())

        if listaUrls:
            # Seteamos las URLs de esa categoría y habilitamos componentes de edición
            self.desplegableUrls.configure(values=listaUrls, state="normal")
            self.desplegableUrls.set(listaUrls[0])
            
            self.entradaNuevoAlias.configure(state="normal")
            self.entradaNuevaUrl.configure(state="normal")
            self.desplegableCategoriaDestino.configure(state="normal")
            self.btnGuardarCambios.configure(state="normal")
            
            # Forzamos la carga del primer link de la nueva lista
            self.cargarDatosUrl(listaUrls[0])
        else:
            # Si no hay enlaces en esa categoría, congelamos el formulario de edición
            self.desplegableUrls.configure(values=["Sin enlaces"], state="disabled")
            self.desplegableUrls.set("Sin enlaces")
            
            self.entradaNuevoAlias.delete(0, "end")
            self.entradaNuevoAlias.configure(state="disabled")
            
            self.entradaNuevaUrl.delete(0, "end")
            self.entradaNuevaUrl.configure(state="disabled")
            
            self.desplegableCategoriaDestino.configure(state="disabled")
            self.btnGuardarCambios.configure(state="disabled")

    # Autocompleta los campos del formulario con los datos actuales del link seleccionado
    def cargarDatosUrl(self, aliasSeleccionado):
        categoriaOrigen = self.desplegableCategoriaOrigen.get()
        
        # Obtenemos la URL del diccionario en logic
        urlActual = self.main.logic.diccionario.get(categoriaOrigen, {}).get(aliasSeleccionado, "")

        # Escribimos el nombre actual en la entrada de texto
        self.entradaNuevoAlias.delete(0, "end")
        self.entradaNuevoAlias.insert(0, aliasSeleccionado)

        # Escribimos la dirección URL en la entrada de texto
        self.entradaNuevaUrl.delete(0, "end")
        self.entradaNuevaUrl.insert(0, urlActual)

        # Por defecto, marcamos el destino idéntico a su origen
        self.desplegableCategoriaDestino.set(categoriaOrigen)

    # --- VERIFICACIONES Y POPUP DE CONFIRMACIÓN ---

    # Ejecuta el análisis de errores e inicia el popup si todo está correcto
    def confirmarModificacion(self):
        # Evitamos la duplicación de alertas en pantalla
        if self.ventanaConfirmacion is not None and self.ventanaConfirmacion.winfo_exists():
            self.ventanaConfirmacion.focus()
            return

        # Capturamos todos los datos del formulario de origen y destino
        categoriaOrigen = self.desplegableCategoriaOrigen.get()
        aliasOriginal = self.desplegableUrls.get()
        
        nuevoAlias = self.entradaNuevoAlias.get().strip()
        nuevaUrl = self.entradaNuevaUrl.get().strip()
        categoriaDestino = self.desplegableCategoriaDestino.get()

        # Cargamos los enlaces que ya existen en la categoría de destino para validar duplicados
        enlacesDestino = self.main.logic.diccionario.get(categoriaDestino, {})

        # --- BLOQUE DE VERIFICACIONES DESDE LA VISTA ---

        # 1. Validación: Campos de edición obligatorios vacíos
        if not nuevoAlias or not nuevaUrl:
            alerts.mostrarCamposObligatorios()
            return

        # 2. Validación: Si el alias ya existe en la categoría de destino
        # Excepción: Se permite guardar si el nombre y destino no han cambiado (solo edita la dirección URL)
        elif nuevoAlias in enlacesDestino and (nuevoAlias != aliasOriginal or categoriaDestino != categoriaOrigen):
            alerts.mostrarAliasExiste()
            return

        # 3. Validación: Evitar que el alias sea una URL
        elif nuevoAlias.startswith(("http://", "https://")):
            alerts.mostrarAliasInvalido()
            return

        # 4. Validación: Que la dirección URL sea válida
        elif not nuevaUrl.startswith(("http://", "https://")):
            alerts.mostrarUrlInvalida()
            return

        # --- CREACIÓN DEL POPUP CENTRADO ---
        self.ventanaConfirmacion = ctk.CTkToplevel(self)
        self.ventanaConfirmacion.title("Guardar Cambios")
        self.ventanaConfirmacion.resizable(False, False)
        self.ventanaConfirmacion.attributes("-topmost", True)

        # Medidas fijas de la ventana emergente
        anchoAlerta = 420
        altoAlerta = 220

        # Capturamos la posición real del main para ubicar la alerta encima
        self.main.update_idletasks()
        anchoPrincipal = self.main.winfo_width()
        altoPrincipal = self.main.winfo_height()
        posicionXPrincipal = self.main.winfo_x()
        posicionYPrincipal = self.main.winfo_y()

        # Cálculo matemático del centro geométrico
        posicionX = posicionXPrincipal + (anchoPrincipal // 2) - (anchoAlerta // 2)
        posicionY = posicionYPrincipal + (altoPrincipal // 2) - (altoAlerta // 2)

        # Aplicamos coordenadas
        self.ventanaConfirmacion.geometry(f"{anchoAlerta}x{altoAlerta}+{posicionX}+{posicionY}")

        # Mensaje informativo para confirmar cambios de categoría
        textoCambio = f"¿Confirmas los cambios para '{aliasOriginal}'?\n"
        if categoriaOrigen != categoriaDestino:
            textoCambio += f"\n📁 Se moverá de '{categoriaOrigen}' a '{categoriaDestino}'"
        if aliasOriginal != nuevoAlias:
            textoCambio += f"\n🏷️ Cambiará su nombre a '{nuevoAlias}'"

        labelMensaje = ctk.CTkLabel(
            self.ventanaConfirmacion,
            text=f"{textoCambio}\n\n¿Deseas aplicar esta configuración?",
            font=("Arial", 12, "bold"),
            pady=15
        )
        labelMensaje.pack()

        # Contenedor para alinear los botones de acción
        contenedorBotones = ctk.CTkFrame(self.ventanaConfirmacion, fg_color="transparent")
        contenedorBotones.pack(pady=10)

        # Botón para anular el proceso
        btnCancelar = ctk.CTkButton(
            contenedorBotones,
            text="Cancelar",
            fg_color="#555555",
            hover_color="#777777",
            width=120,
            command=self.ventanaConfirmacion.destroy
        )
        btnCancelar.pack(side="left", padx=10)

        # Botón de confirmación definitiva
        btnConfirmar = ctk.CTkButton(
            contenedorBotones,
            text="Confirmar",
            fg_color="#2c6e49",
            hover_color="#4f9a69",
            width=120,
            command=lambda: self.ejecutarModificacion(categoriaOrigen, aliasOriginal, nuevoAlias, nuevaUrl, categoriaDestino)
        )
        btnConfirmar.pack(side="right", padx=10)

    # Llama al motor lógico para actualizar los datos encriptados del JSON
    def ejecutarModificacion(self, catOrigen, aliasOrig, nuevoAlias, nuevaUrl, catDestino):
        # Destruimos la ventana de confirmación de inmediato
        if self.ventanaConfirmacion is not None:
            self.ventanaConfirmacion.destroy()
            self.ventanaConfirmacion = None

        # Registramos las modificaciones en el JSON
        self.main.logic.modificarUrl(catOrigen, aliasOrig, nuevoAlias, nuevaUrl, catDestino)
        
        # Alerta informativa de éxito
        alerts.mostrarGuardadoExitoso()

        # Reconstruimos completamente la pestaña para limpiar y sincronizar los desplegables con el nuevo JSON
        self.createWidgets()

if __name__ == "__main__":
    pass