# Copyright 2026 Ignacio Catalán
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# Importamos las diferentes librerias
# Para abrir el navegador preferido
import webbrowser
# Para interactuar con el sistema operativo
import os
# Para interactuar con el archivo JSON
import json
# Necesario para detectar la ruta del .exe
import sys 

RUTA_DATOS = ""
diccionario = {}

def obtenerRutaArchivo():
    # Detectamos si el código corre como .exe (PyInstaller) o como .py
    if getattr(sys, 'frozen', False):
        # Si es el ejecutable, la carpeta base es donde está el .exe
        ruta_base = os.path.dirname(sys.executable)
    else:
        # Si es desarrollo, la carpeta base es donde está el script
        ruta_base = os.path.dirname(os.path.abspath(__file__))
    
    # Retornamos la ruta del JSON al lado del ejecutable
    return os.path.join(ruta_base, 'UrlKnightData.json')

def cargarDatos(ruta):
    # Si aun no existe el archivo JSON damos un diccionario vacio para empezar de cero
    if not os.path.exists(ruta):
        return {}
    try:
        # Abrimos el archivo con permiso de lectura en donde transformamos la informacion en un diccionario que python pueda leer 
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # Si falla retornamos un diccionario vacio para empezar 
        return {}

def guardarDatos(ruta, datos):
    with open(ruta, 'w', encoding='utf-8') as f:
        # Abrimos el archivo con permiso de escritura
        json.dump(datos, f, indent=4, ensure_ascii=False)
    
# --- FUNCIONES LLAMADAS DESDE MAIN ---

def abrirUrl(alias):
     webbrowser.open(diccionario[alias])
        
def agregarUrl(alias, url):
    diccionario[alias] = url
    guardarDatos(RUTA_DATOS, diccionario)

def eliminarUrl(aliasEliminar):

    del diccionario[aliasEliminar]

    guardarDatos(RUTA_DATOS, diccionario)

# Al momento de abrir la app se ejecuta el siguiente codigo automaticamente
def inicio():
    # Tomamos las rutas globales del archivo
    global RUTA_DATOS, diccionario
    # Obtenemos la ruta del archivo
    RUTA_DATOS = obtenerRutaArchivo()
    # Si no existe creamos el archivo automaticamente sin nada {}
    if not os.path.exists(RUTA_DATOS):
        guardarDatos(RUTA_DATOS, {})
    # Cargamos los datos
    diccionario = cargarDatos(RUTA_DATOS)


if __name__ == "__main__":
    pass
