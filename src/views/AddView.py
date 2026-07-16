import customtkinter as ctk
from components import Alerts as alerts

class AddView(ctk.CTkFrame):
    def __init__(self, parent, main):
        super().__init__(parent, fg_color="transparent")
        self.main = main
        
        # Construir la interfaz de inmediato al cambiar a esta pestaña
        self.createWidgets()

    def createWidgets(self):
        # Título principal de la vista
        self.tituloAgregar = ctk.CTkLabel(self, text="📜 AÑADIR URL 🛡️", font=("Arial", 24, "bold"))
        self.tituloAgregar.pack(pady=20)

        # --- NUEVO DESPLEGABLE PARA SELECCIONAR CATEGORÍA ---
        # Consultamos dinámicamente las categorías disponibles en la base de datos
        listaCategorias = self.main.logic.obtenerCategorias()

        # Label informativo para guiar al usuario
        self.labelCategoria = ctk.CTkLabel(self, text="Selecciona una categoría:", font=("Arial", 12, "bold"))
        self.labelCategoria.pack(pady=(5, 2))

        # Menú desplegable con las categorías existentes
        self.desplegableCategorias = ctk.CTkOptionMenu(
            self,
            values=listaCategorias,
            fg_color="#b58d3d",
            button_color="#9c752d",
            button_hover_color="#805d21",
            font=("Arial", 14, "bold"),
            dropdown_font=("Arial", 12)
        )
        self.desplegableCategorias.pack(pady=(0, 15))
        # Seleccionamos por defecto la categoría principal de la app
        self.desplegableCategorias.set(self.main.logic.categoriaPorDefecto)

        # Campo de texto para el alias (nombre de la web)
        self.entradaAliasAgregar = ctk.CTkEntry(self, placeholder_text="Ingresa tu alias aqui...", width=400)
        self.entradaAliasAgregar.pack(pady=10)

        # Campo de texto para la URL
        self.entradaUrlAgregar = ctk.CTkEntry(self, placeholder_text="Ingresa tu url aqui...", width=400)
        self.entradaUrlAgregar.pack(pady=10)

        # Botón para ejecutar la acción de agregar
        self.btnAgregarUrlAgregar = ctk.CTkButton(
            self, 
            text="Agregar Url",
            width=200,
            command=self.agregarUrl
        )
        self.btnAgregarUrlAgregar.pack(pady=10, padx=20)

    # --- ACCIONES ---

    def agregarUrl(self):
        # Capturamos los datos ingresados por el usuario
        categoriaSeleccionada = self.desplegableCategorias.get()
        alias = self.entradaAliasAgregar.get().strip()
        url = self.entradaUrlAgregar.get().strip()
        
        # Obtenemos las URLs que pertenecen únicamente a la categoría seleccionada
        enlacesDeCategoria = self.main.logic.diccionario.get(categoriaSeleccionada, {})
        
        # --- BLOQUE DE VERIFICACIONES Y VALIDACIONES DESDE LA VISTA ---
        
        # 1. Validación: Campos obligatorios vacíos
        if not alias or not url:
            alerts.mostrarCamposObligatorios()
            
        # 2. Validación: Verificar duplicados pero únicamente dentro de la categoría seleccionada
        elif alias in enlacesDeCategoria:
            alerts.mostrarAliasExiste()
            
        # 3. Validación: Evitar que el alias sea una URL para que la interfaz no se rompa visualmente
        elif alias.startswith(("http://", "https://")):
            alerts.mostrarAliasInvalido()
            
        # 4. Validación: Que el enlace ingresado sea una URL válida
        elif not url.startswith(("http://", "https://")):
            alerts.mostrarUrlInvalida()
            
        # 5. Todo correcto: Procedemos a guardar la URL en la base de datos
        else:
            alerts.mostrarGuardadoExitoso()
            # Llamamos a logic pasándole ahora la categoría seleccionada, el alias y la url
            self.main.logic.agregarUrl(categoriaSeleccionada, alias, url)
            
            # --- LIMPIEZA DE FORMULARIO ---
            self.entradaAliasAgregar.delete(0, "end")
            self.entradaUrlAgregar.delete(0, "end")
            # Devolvemos el desplegable a su opción por defecto
            self.desplegableCategorias.set(self.main.logic.categoriaPorDefecto)

if __name__ == "__main__":
    pass