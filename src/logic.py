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

RUTA_DATOS = {}
diccionario = {}

def obtener_ruta_archivo():

    # guardamos en una variable en donde el usuario guarda sus registros de apps
    appdata = os.getenv('APPDATA')
    # vemos con la ruta de appdata en donde esta la carpeta de la app
    carpeta = os.path.join(appdata, 'UrlKnight')
    # si no existe esta carpeta la creamos
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    # creamos la ruta final de archivos y la retornamos    
    return os.path.join(carpeta, 'urls.json')

def cargar_datos(ruta):
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

def guardar_datos(ruta, datos):
    with open(ruta, 'w', encoding='utf-8') as f:
        # Abrimos el archivo con permiso de escritura
        json.dump(datos, f, indent=4, ensure_ascii=False)
    
def abrirUrl(alias):
     webbrowser.open(diccionario[alias])
        
def añadirUrl(Alias, url):
    diccionario[Alias] = url
    guardar_datos(RUTA_DATOS, diccionario)

def eliminarUrl(aliasEliminar):

    del diccionario[aliasEliminar]

    guardar_datos(RUTA_DATOS, diccionario)

def inicio():
    global RUTA_DATOS, diccionario
    
    RUTA_DATOS = obtener_ruta_archivo()
    diccionario = cargar_datos(RUTA_DATOS)

if __name__ == "__main__":
    pass
