import customtkinter as ctk
from components import Alerts as alerts

class AddCategoryView(ctk.CTkFrame):
    def __init__(self, parent, main):
        super().__init__(parent, fg_color="transparent")
        self.main = main
        
        # Construir la interfaz de inmediato al cambiar a esta pestaña
        self.createWidgets()

    def createWidgets(self):
        # Título principal de la vista
        self.tituloCategoria = ctk.CTkLabel(self, text="📁 AÑADIR CATEGORÍA 🛡️", font=("Arial", 24, "bold"))
        self.tituloCategoria.pack(pady=20)

        # Campo de texto para ingresar el nombre de la nueva categoría
        self.entradaNuevaCategoria = ctk.CTkEntry(
            self, 
            placeholder_text="Ingresa el nombre de la categoría...", 
            width=400
        )
        self.entradaNuevaCategoria.pack(pady=15)

        # Botón para ejecutar la acción de agregar la categoría
        self.btnAgregarCategoria = ctk.CTkButton(
            self, 
            text="Agregar Categoría",
            width=200,
            command=self.agregarCategoria
        )
        self.btnAgregarCategoria.pack(pady=10, padx=20)

    # --- ACCIONES ---

    def agregarCategoria(self):
        # Capturamos el nombre ingresado y eliminamos espacios vacíos en los extremos
        nombreCategoria = self.entradaNuevaCategoria.get().strip()
        
        # Obtenemos la lista actual de categorías directamente desde logic
        categoriasExistentes = self.main.logic.obtenerCategorias()
        
        # Creamos una lista temporal en minúsculas para comparar sin importar si usan mayúsculas
        categoriasExistentesMinusc = [cat.lower() for cat in categoriasExistentes]
        
        # --- BLOQUE DE VERIFICACIONES DESDE LA VISTA ---
        
        # 1. Validación: El campo está vacío o solo contiene espacios
        if not nombreCategoria:
            alerts.mostrarCamposObligatorios()
            
        # 2. Validación: Evitar duplicados exactos o variaciones de mayúsculas (ej: evitar "Estudios" y "estudios")
        elif nombreCategoria.lower() in categoriasExistentesMinusc:
            # Alerta personalizada para avisar que el nombre ya está registrado
            alerts.mostrarCategoriaExiste()
            
        # 3. Todo correcto: Intentamos registrar la categoría a través de logic
        else:
            # Enviamos la categoría limpia a la lógica de negocio
            self.main.logic.agregarCategoria(nombreCategoria)
            # Alerta de éxito al guardar
            alerts.mostrarCategoriaCreada()
            # Limpiamos el campo de texto ÚNICAMENTE si la operación fue un éxito total
            self.entradaNuevaCategoria.delete(0, "end")


if __name__ == "__main__":
    pass