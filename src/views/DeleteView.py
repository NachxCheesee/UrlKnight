import customtkinter as ctk
from components import Alerts as alerts

class DeleteView(ctk.CTkFrame):
    def __init__(self, parent, main):
        super().__init__(parent, fg_color="transparent")
        self.main = main
        
        # Construir la interfaz de inmediato
        self.createWidgets()

    def createWidgets(self):
        # Todo se monta directo en 'self'
        self.tituloEliminar = ctk.CTkLabel(self, text="❌ ELIMINAR URL ❌", font=("Arial", 24, "bold"))
        self.tituloEliminar.pack(pady=20)

        self.entradaAliasEliminar = ctk.CTkEntry(self, placeholder_text="Ingresa tu alias aqui...", width=400)
        self.entradaAliasEliminar.pack(pady=10)

        self.btnEliminarUrlEliminar = ctk.CTkButton(
            self, 
            text="Eliminar Url",
            width=200,
            command=self.eliminarUrl
        )
        self.btnEliminarUrlEliminar.pack(pady=10, padx=20)
    

    # --- BOTONES ---

    def eliminarUrl(self):
        # Tomamos el texto escrito
        alias = self.entradaAliasEliminar.get()

        # Verificaciones usando el archivo 'alerts' importado
        # Diccionario consultado desde 'self.main.logic'
        if not alias.strip():
            alerts.mostrarCamposObligatorios()
        elif alias in self.main.logic.diccionario:
            self.main.logic.eliminarUrl(alias)
            alerts.mostrarBorradoExitoso()
        else:
            alerts.mostrarAliasNotFound()

        # Limpiamos el campo de texto
        self.entradaAliasEliminar.delete(0, 'end')

if __name__ == "__main__":
    pass