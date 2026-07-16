# ==============================================================================
# MÓDULO: Lógica de Negocio y Persistencia de Datos (logic.py)
# Propósito: Gestionar el almacenamiento de enlaces (URLs) en un archivo JSON,
#            controlar el ciclo de vida de los datos y manejar la apertura
#            de links en el navegador web predeterminado.
# Características: Soporte nativo para portabilidad (.exe / PyInstaller).
# ==============================================================================


# Importamos las diferentes librerias
# Para abrir el navegador preferido
import webbrowser
# Para interactuar con el sistema operativo
import os
# Para interactuar con el archivo JSON
import json
# Necesario para detectar la ruta del .exe
import sys 
# Librería estándar para ofuscar/encriptar el JSON sin aumentar peso al .exe
import base64


# Ruta donde se guardará físicamente el archivo JSON
rutaDatos = ""
# Diccionario global donde cargaremos en memoria todos los datos de la app
diccionario = {}
# Nombre de la categoría que se creará por defecto y que no se puede borrar
categoriaPorDefecto = "Sin Categoría"

# Función para averiguar dónde está parada la app y definir la ruta del JSON
def obtenerRutaArchivo():
    # Detectamos si el código corre compilado como ejecutable .exe (PyInstaller)
    if getattr(sys, "frozen", False):
        # Si es el ejecutable, la carpeta base es donde está el archivo .exe
        rutaBase = os.path.dirname(sys.executable)
    else:
        # Si estamos en desarrollo, la carpeta base es donde está el script .py
        rutaBase = os.path.dirname(os.path.abspath(__file__))
    
    # Unimos la ruta de la carpeta con el nombre del archivo de datos
    return os.path.join(rutaBase, "UrlKnightData.json")

# Función que lee el archivo del disco, lo desencripta y migra la estructura si es vieja
def cargarDatos(ruta):
    # Si el archivo no existe en la carpeta, devolvemos el diccionario base con "Sin Categoría" de antemano
    if not os.path.exists(ruta):
        return {categoriaPorDefecto: {}}
    try:
        # Abrimos el archivo en modo lectura ('r') con codificación UTF-8
        with open(ruta, "r", encoding="utf-8") as f:
            # Leemos todo el texto y eliminamos espacios en blanco al inicio/final
            contenido = f.read().strip()
            
        # DESENCRIPTACIÓN
        # Intentamos decodificar el texto que leímos asumiendo que está en Base64
        try:
            # Decodificamos de Base64 a bytes, y luego de bytes a texto legible
            contenidoDecodificado = base64.b64decode(contenido).decode("utf-8")
            # Convertimos el texto JSON decodificado en un diccionario de Python
            datos = json.loads(contenidoDecodificado)
        except Exception:
            # Si falla, significa que el archivo estaba en texto plano (versión antigua)
            # Lo cargamos directamente como texto plano para no perder nada
            datos = json.loads(contenido)
            
        # MIGRACIÓN
        # Vamos a revisar si el archivo que acabamos de cargar tiene el formato viejo (plano)
        # Para esto, revisamos si algún valor del diccionario es un texto (una URL) en lugar de un diccionario
        esFormatoAntiguo = False
        for clave, valor in datos.items():
            if isinstance(valor, str):
                # Si encontramos que el valor es un texto plano, confirmamos que es el formato antiguo
                esFormatoAntiguo = True
                break
                
        # Si detectamos que es el formato antiguo lo migración 
        if esFormatoAntiguo:
            # Creamos la nueva estructura con la categoría por defecto vacía
            datosMigrados = {categoriaPorDefecto: {}}
            
            # Recorremos todos los enlaces viejos y los metemos dentro de "Sin Categoría"
            for alias, url in datos.items():
                datosMigrados[categoriaPorDefecto][alias] = url
                
            # Guardamos inmediatamente en el disco con el nuevo formato y ya encriptado
            guardarDatos(ruta, datosMigrados)
            
            # Retornamos la base de datos ya estructurada para que la app trabaje feliz
            return datosMigrados
            
        # Si ya tenía el formato nuevo de categorías, simplemente retornamos los datos cargados
        return datos
        
    except Exception:
        # Si ocurre cualquier otro error crítico, devolvemos el diccionario base para no romper la app
        return {categoriaPorDefecto: {}}

# Función que encripta el diccionario y lo escribe físicamente en el disco
def guardarDatos(ruta, datos):
    # Convertimos el diccionario a una cadena de texto en formato JSON
    # indent=4 hace que el JSON se estructure bonito (aunque al encriptar no se note en el archivo físico)
    jsonPlano = json.dumps(datos, indent=4, ensure_ascii=False)
    
    # Convertimos el texto plano a Base64 para ocultarlo de miradas curiosas
    # Primero pasamos el texto a bytes (.encode), lo codificamos, y lo volvemos a texto (.decode)
    jsonOfuscado = base64.b64encode(jsonPlano.encode("utf-8")).decode("utf-8")
    
    # Abrimos el archivo en modo escritura ('w') para reemplazar su contenido con el texto oculto
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(jsonOfuscado)
    
# --- FUNCIONES LLAMADAS DESDE LAS VISTAS (INTERFACE) ---

# Abre la URL correspondiente en el navegador web
def abrirUrl(categoria, alias):
    # Verificamos que la categoría exista en nuestro diccionario y que el alias también
    if categoria in diccionario and alias in diccionario[categoria]:
        # La librería webbrowser abre la URL en el navegador por defecto del sistema
        webbrowser.open(diccionario[categoria][alias])
        
# Agrega una nueva URL dentro de una categoría específica
def agregarUrl(categoria, alias, url):
    # Si por algún motivo la categoría no existe en el diccionario, la creamos vacía
    if categoria not in diccionario:
        diccionario[categoria] = {}
        
    # Guardamos el par Clave-Valor (Nombre de la Web: URL) dentro de esa categoría
    diccionario[categoria][alias] = url
    # Guardamos los cambios de inmediato en el archivo físico
    guardarDatos(rutaDatos, diccionario)

# Elimina una URL de una categoría específica
def eliminarUrl(categoria, aliasEliminar):
    # Verificamos que la categoría exista y que la URL esté guardada en ella
    if categoria in diccionario and aliasEliminar in diccionario[categoria]:
        # Eliminamos el registro usando "del"
        del diccionario[categoria][aliasEliminar]
        # Guardamos los cambios actualizados en el archivo físico
        guardarDatos(rutaDatos, diccionario)

# --- NUEVAS FUNCIONES PARA GESTIÓN DE CATEGORÍAS ---

# Retorna una lista con todas las categorías que existen actualmente en la app
def obtenerCategorias():
    global diccionario
    # Convertimos las llaves del diccionario (que son los nombres de las categorías) en una lista
    return list(diccionario.keys())

# Crea una nueva categoría vacía
def agregarCategoria(nuevaCategoria):
    # Quitamos los espacios en blanco innecesarios al inicio y al final
    nuevaCategoriaClean = nuevaCategoria.strip()
    # Si el nombre no está vacío y la categoría no existe previamente
    if nuevaCategoriaClean and nuevaCategoriaClean not in diccionario:
        # Creamos la categoría asociándole un diccionario interno vacío {}
        diccionario[nuevaCategoriaClean] = {}
        # Guardamos la base de datos actualizada
        guardarDatos(rutaDatos, diccionario)
        # Retornamos True para avisarle a la interfaz que se creó con éxito
        return True
    # Retornamos False si la categoría ya existía o el nombre era inválido
    return False

# Elimina una categoría por completo junto con todas sus URLs
def eliminarCategoria(categoriaEliminar):
    # Regla de seguridad: "Sin Categoría" jamás puede ser eliminada
    if categoriaEliminar == categoriaPorDefecto:
        return False
        
    # Si la categoría existe en nuestro diccionario
    if categoriaEliminar in diccionario:
        # La eliminamos por completo del diccionario
        del diccionario[categoriaEliminar]
        # Guardamos los cambios en el archivo físico
        guardarDatos(rutaDatos, diccionario)
        # Retornamos True indicando que la eliminación fue exitosa
        return True
    return False

# Modifica los datos de una URL y permite cambiarla de categoría si es necesario
def modificarUrl(categoriaOrigen, aliasOriginal, nuevoAlias, nuevaUrl, categoriaDestino):
    # 1. Eliminamos el registro antiguo de la categoría donde estaba originalmente
    if categoriaOrigen in diccionario and aliasOriginal in diccionario[categoriaOrigen]:
        del diccionario[categoriaOrigen][aliasOriginal]
    
    # 2. Nos aseguramos de que la nueva categoría de destino exista (por seguridad)
    if categoriaDestino not in diccionario:
        diccionario[categoriaDestino] = {}
        
    # 3. Insertamos los nuevos datos en la categoría de destino
    diccionario[categoriaDestino][nuevoAlias] = nuevaUrl
    # 4. Guardamos todos los cambios actualizados en el JSON
    guardarDatos(rutaDatos, diccionario)

# --- INICIALIZACIÓN AUTOMÁTICA AL ABRIR LA APP ---

def inicio():
    global rutaDatos, diccionario
    # Obtenemos la ruta física donde se guardará nuestro archivo JSON
    rutaDatos = obtenerRutaArchivo()
    
    # Si el archivo JSON no existe en la carpeta (primera vez que se abre la app)
    if not os.path.exists(rutaDatos):
        # Lo creamos con la estructura básica inicial de antemano: {"Sin Categoría": {}}
        guardarDatos(rutaDatos, {categoriaPorDefecto: {}})
        
    # Cargamos el contenido del archivo en nuestra variable global 'diccionario'
    diccionario = cargarDatos(rutaDatos)
    
    # Doble verificación: si por alguna razón el archivo estaba vacío, forzamos que exista "Sin Categoría"
    if categoriaPorDefecto not in diccionario:
        diccionario[categoriaPorDefecto] = {}
        # Guardamos para asegurar la persistencia
        guardarDatos(rutaDatos, diccionario)

# Evitamos que se ejecute código suelto si importamos este módulo desde otro lado
if __name__ == "__main__":
    pass