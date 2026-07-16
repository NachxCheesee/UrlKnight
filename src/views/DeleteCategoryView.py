import customtkinter as ctk
from components import Alerts as alerts

class DeleteCategoryView(ctk.CTkFrame):
    def __init__(self, parent, main):
        super().__init__(parent, fg_color="transparent")
        self.main = main
        
        # Guardamos la referencia de la ventana emergente de confirmación para controlar que no se abra más de una
        self.ventanaConfirmacion = None
        
        # Construir la interfaz de inmediato al cambiar a esta pestaña
        self.createWidgets()

    def createWidgets(self):
        # Título principal de la vista
        self.tituloEliminar = ctk.CTkLabel(self, text="🗑️ ELIMINAR CATEGORÍA 🗑️", font=("Arial", 24, "bold"))
        self.tituloEliminar.pack(pady=20)

        # Obtenemos todas las categorías registradas en la app
        listaCategoriasCompleta = self.main.logic.obtenerCategorias()
        
        # Filtramos la lista para quitar "Sin Categoría" de las opciones eliminables por seguridad extrema
        self.listaCategoriasEliminables = []
        for cat in listaCategoriasCompleta:
            if cat != self.main.logic.categoriaPorDefecto:
                self.listaCategoriasEliminables.append(cat)

        # Si no hay categorías creadas por el usuario todavía
        if len(self.listaCategoriasEliminables) == 0:
            # Mostramos un mensaje explicativo en la pantalla
            self.labelSinCategorias = ctk.CTkLabel(
                self, 
                text="🛡️ No tienes categorías personalizadas para eliminar 🛡️\nLa categoría 'Sin Categoría' es permanente.", 
                font=("Arial", 14, "italic")
            )
            self.labelSinCategorias.pack(pady=40)
        else:
            # Label informativo para guiar al usuario
            self.labelSeleccion = ctk.CTkLabel(
                self, 
                text="Selecciona la categoría que deseas borrar permanentemente:", 
                font=("Arial", 12, "bold")
            )
            self.labelSeleccion.pack(pady=(10, 5))

            # Menú desplegable cargado únicamente con las categorías que sí se pueden borrar
            self.desplegableCategorias = ctk.CTkOptionMenu(
                self,
                values=self.listaCategoriasEliminables,
                fg_color="#b58d3d",
                button_color="#9c752d",
                button_hover_color="#805d21",
                font=("Arial", 14, "bold"),
                dropdown_font=("Arial", 12)
            )
            self.desplegableCategorias.pack(pady=(0, 20))
            # Seleccionamos la primera opción disponible de la lista filtrada
            self.desplegableCategorias.set(self.listaCategoriasEliminables[0])

            # Mensaje de advertencia sobre la pérdida de datos
            self.labelAdvertencia = ctk.CTkLabel(
                self,
                text="⚠️ ¡Atención! Al eliminar la categoría se borrarán\ntodas las URLs que estén guardadas dentro de ella.",
                font=("Arial", 12, "bold"),
                text_color="#cc3333"
            )
            self.labelAdvertencia.pack(pady=15)

            # Botón para iniciar el proceso de eliminación (abrirá la confirmación)
            self.btnEliminarCategoria = ctk.CTkButton(
                self, 
                text="Eliminar Categoría",
                width=200,
                fg_color="#8b0000",
                hover_color="#b22222",
                command=self.confirmarEliminacion
            )
            self.btnEliminarCategoria.pack(pady=10, padx=20)

    # --- ACCIONES ---

    # Abre la ventana flotante de confirmación de seguridad y la centra en la app
    def confirmarEliminacion(self):
        # Si ya hay una ventana de confirmación abierta, la traemos al frente y no creamos otra
        if self.ventanaConfirmacion is not None and self.ventanaConfirmacion.winfo_exists():
            self.ventanaConfirmacion.focus()
            return

        # Capturamos la categoría seleccionada en el desplegable
        categoriaSeleccionada = self.desplegableCategorias.get()

        # Creamos la ventana emergente de CustomTkinter
        self.ventanaConfirmacion = ctk.CTkToplevel(self)
        self.ventanaConfirmacion.title("Confirmar Eliminación")
        
        # Evitamos que el usuario cambie el tamaño de la alerta
        self.ventanaConfirmacion.resizable(False, False)
        # Forzamos que la ventana aparezca por encima de la app principal
        self.ventanaConfirmacion.attributes("-topmost", True)

        # --- LÓGICA DE CENTRADO DINÁMICO ---
        # Definimos las dimensiones de la alerta emergente
        anchoAlerta = 400
        altoAlerta = 200

        # Actualizamos las tareas en espera del sistema para asegurarnos de capturar las medidas reales
        self.main.update_idletasks()
        
        # Obtenemos las dimensiones y posición actual de tu ventana principal (main.py)
        anchoPrincipal = self.main.winfo_width()
        altoPrincipal = self.main.winfo_height()
        posicionXPrincipal = self.main.winfo_x()
        posicionYPrincipal = self.main.winfo_y()

        # Calculamos el punto central horizontal y vertical relativo a la app principal
        posicionX = posicionXPrincipal + (anchoPrincipal // 2) - (anchoAlerta // 2)
        posicionY = posicionYPrincipal + (altoPrincipal // 2) - (altoAlerta // 2)

        # Aplicamos la geometría con la posición exacta calculada en píxeles
        self.ventanaConfirmacion.geometry(f"{anchoAlerta}x{altoAlerta}+{posicionX}+{posicionY}")

        # Mensaje de confirmación detallado
        labelMensaje = ctk.CTkLabel(
            self.ventanaConfirmacion,
            text=f"¿Estás seguro de que quieres eliminar\nla categoría '{categoriaSeleccionada}'?\n\nEsta acción no se puede deshacer.",
            font=("Arial", 13, "bold"),
            pady=20
        )
        labelMensaje.pack()

        # Contenedor para los botones de acción
        contenedorBotones = ctk.CTkFrame(self.ventanaConfirmacion, fg_color="transparent")
        contenedorBotones.pack(pady=10)

        # Botón para cancelar y cerrar la advertencia sin hacer nada
        btnCancelar = ctk.CTkButton(
            contenedorBotones,
            text="Cancelar",
            fg_color="#555555",
            hover_color="#777777",
            width=120,
            command=self.ventanaConfirmacion.destroy
        )
        btnCancelar.pack(side="left", padx=10)

        # Botón destructivo para confirmar la eliminación definitiva
        btnConfirmar = ctk.CTkButton(
            contenedorBotones,
            text="Sí, eliminar",
            fg_color="#8b0000",
            hover_color="#b22222",
            width=120,
            command=lambda: self.ejecutarEliminacion(categoriaSeleccionada)
        )
        btnConfirmar.pack(side="right", padx=10)

    # Ejecuta el borrado final en el logic una vez aceptado por el usuario
    def ejecutarEliminacion(self, categoriaAEliminar):
        # Cerramos la ventana de confirmación inmediatamente
        if self.ventanaConfirmacion is not None:
            self.ventanaConfirmacion.destroy()
            self.ventanaConfirmacion = None

        # Llamamos al motor logic para borrar la categoría y sus URLs del JSON
        exito = self.main.logic.eliminarCategoria(categoriaAEliminar)

        if exito:
            # Alerta visual de éxito al usuario
            alerts.mostrarEliminadoExitosoCategoria()
            
            # Reconstruimos los widgets de esta misma pestaña para actualizar el desplegable
            for widget in self.winfo_children():
                widget.destroy()
            self.createWidgets()
        else:
            # Alerta en caso de error interno inesperado
            alerts.mostrarErrorProceso()

if __name__ == "__main__":
    pass