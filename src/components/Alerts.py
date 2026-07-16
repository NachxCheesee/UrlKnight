# ==============================================================================
# MÓDULO: Gestión de Alertas (alertas.py)
# Propósito: Centralizar y gestionar todas las ventanas emergentes (mayoritariamente en caso de validaciones)
#            de la aplicación para mantener el código de la UI limpio y modular.
# ==============================================================================

# libreria para dar mensajes profesionales
from CTkMessagebox import CTkMessagebox

def mostrarAliasInvalido():
    CTkMessagebox(title="Error", message="¡Alias invalido! Asegúrate de que NO empiece con http:// o https://", icon="cancel")

def mostrarGuardadoExitoso():
    CTkMessagebox(title="Éxito", message="¡URL guardada correctamente!", icon="check")

def mostrarUrlInvalida():
    CTkMessagebox(title="Error", message="¡Url invalido! Asegúrate de que empiece con http:// o https://", icon="cancel")
    
def mostrarBorradoExitoso():
    CTkMessagebox(title="Éxito", message="¡URL borrada correctamente!", icon="check")

def mostrarCamposObligatorios():
    CTkMessagebox(title="Error", message="¡Todos los campos son obligatorios!", icon="cancel")

def mostrarAliasNotFound():
    CTkMessagebox(title="Error", message="¡Alias no encontrado!", icon="cancel")
    
def mostrarAliasExiste():
    CTkMessagebox(title="Error", message="¡Ya existe un Alias con ese nombre!", icon="cancel")

def mostrarUrlMultipleNo():
    CTkMessagebox(title="Aviso", message="¡No has seleccionado ninguna ruta, caballero!", icon="warning")

def mostrarCategoriaExiste():
    CTkMessagebox(title="Error", message="¡Esta categoria ya existe!", icon="cancel")

def mostrarCategoriaCreada():
    CTkMessagebox(title="Éxito", message="¡Categoria creada con exito!", icon="check")

def mostrarEliminadoExitosoCategoria():
    CTkMessagebox(title="Éxito", message="¡Categoria eliminada con exito!", icon="check")

def mostrarErrorProceso():
    # Añadida para dar soporte a fallos lógicos inesperados en el backend
    CTkMessagebox(title="Error", message="¡Ha ocurrido un error inesperado al procesar la solicitud!", icon="cancel")


if __name__ == "__main__":
    pass