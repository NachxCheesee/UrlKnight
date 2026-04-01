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

# Creamos esta excepción artificial para que asi pueda ser llamada desde donde sea 
# Esto con el fin de que el usuario pueda volver al menu independiente de donde este 
class VolverMenu(Exception):
    pass

# Este es el input a utilizar 
# Cada que se llame se verifica si el usuario ingreso la letra 'b' si es el caso llamamos a la excepción de VolverMenu si no retornamos el mensaje original
def inputKnight():
    respuesta = input()
    if respuesta.lower() == 'b':
        raise VolverMenu() 
    return respuesta

def introduccion():
    # Limpieza de la consola
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nBienvenido al administrador de URL\n")
    print("Guía: Escribe 'b' o 'B' en cualquier momento para volver al Menu.\n")

def listarUrl():
    try:
        print("")
        claves = list(diccionario.keys())

        if len(claves) == 0:
            print("Aun no has guardado ninguna Url!\n")
            return
        
        numero = 0
        print("Ingresa el numero de la URL preferida")
        for i in claves:
            numero += 1
            print(f"{numero}- {i}")
            
        print("")
        
        while True:
            try:
                
                eleccion = inputKnight()

                eleccion = (int(eleccion)) -1
                
                
                if 0 <= eleccion < len(claves):
                    webbrowser.open(diccionario[claves[eleccion]])
                    break
                else:
                    print("Error Ingrese una opcion visible")
                    continue

                
            except ValueError:
                print("Error ingrese un numero valido")
    except VolverMenu:
        raise
    except Exception as e:
        print(f"Error inesperado: {e}")
        
def añadirUrl():
    print("Ingrese el Alias de la nueva Url")
    Alias = inputKnight()
    print("Ingrese la Url (Puedes pegar la que ya tengas con el click derecho)")
    Url = inputKnight().strip()
    diccionario[Alias] = Url

    guardar_datos(RUTA_DATOS, diccionario)
    
    print("Dato ingresado con exito\n")
    
def eliminarUrl():
    print("Ingresa el Alias de la Url a eliminar")
    aliasEliminar = inputKnight()
    if aliasEliminar in diccionario:
        del diccionario[aliasEliminar]

        guardar_datos(RUTA_DATOS, diccionario)

        print("Url eliminada\n")
    else:
        print("El Alias no existe\n")

def menu():

        while(True):
            # Encerramos la funcion dentro de la excepción VolverMenu asi se puede volver al menu desde cualquier lugar 
            try:
                print("1- Seleccionar URL")
                print("2- Añadir URL")
                print("3- Eliminar URL")
                print("4- Salir")
                eleccion = inputKnight()
                
                if eleccion == "1":
                    listarUrl()
                elif eleccion == "2":
                    añadirUrl()
                elif eleccion == "3":
                    eliminarUrl()    
                elif eleccion == "4":
                    break
                else:
                    print("Opcion invalida\n")
            except VolverMenu:
                print("\nMENU\n")

if __name__ == "__main__":
    RUTA_DATOS = obtener_ruta_archivo()
    diccionario = cargar_datos(RUTA_DATOS)
    introduccion()
    menu()
