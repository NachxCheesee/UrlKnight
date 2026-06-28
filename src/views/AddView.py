import customtkinter as ctk
from components import Alerts as alerts

class AddView(ctk.CTkFrame):
    def __init__(self, parent, main):
        super().__init__(parent, fg_color="transparent")
        self.main = main
        
        # Construir la interfaz de inmediato
        self.createWidgets()

    def createWidgets(self):
        # Todo se empaqueta en 'self' (este mismo frame)
        self.tituloAgregar = ctk.CTkLabel(self, text="📜 AÑADIR URL 🛡️", font=("Arial", 24, "bold"))
        self.tituloAgregar.pack(pady=20)

        self.entradaAliasAgregar = ctk.CTkEntry(self, placeholder_text="Ingresa tu alias aqui...", width=400)
        self.entradaAliasAgregar.pack(pady=10)

        self.entradaUrlAgregar = ctk.CTkEntry(self, placeholder_text="Ingresa tu url aqui...", width=400)
        self.entradaUrlAgregar.pack(pady=10)

        self.btnAgregarUrlAgregar = ctk.CTkButton(
            self, 
            text="Agregar Url",
            width=200,
            command=self.agregarUrl
        )
        self.btnAgregarUrlAgregar.pack(pady=10, padx=20)

    # --- BOTONES ---

    def agregarUrl(self):
            alias = self.entradaAliasAgregar.get()
            url = self.entradaUrlAgregar.get()
            
            # Validaciones
            if not alias.strip() or not url.strip():
                alerts.mostrarCamposObligatorios()
            elif alias in self.main.logic.diccionario:
                alerts.mostrarAliasExiste()
            elif alias.startswith(("http://", "https://")):
                alerts.mostrarAliasInvalido()
            elif not url.startswith(("http://", "https://")):
                alerts.mostrarUrlInvalida()
            else:
                alerts.mostrarGuardadoExitoso()
                self.main.logic.agregarUrl(alias, url)
            
            # --- LIMPIEZA ---
            self.entradaAliasAgregar.delete(0, 'end')
            self.entradaUrlAgregar.delete(0, 'end')

if __name__ == "__main__":
    pass