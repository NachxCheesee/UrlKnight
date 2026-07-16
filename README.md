# UrlKnight ⚔️
Un administrador de URLs ligero, portable y diseñado para la productividad sin instalaciones.
---
<p align="left">
  <img src="https://img.shields.io/badge/Python-3.13.2-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
  <img src="https://img.shields.io/badge/Storage-JSON-000000?style=for-the-badge&logo=json&logoColor=white" />
</p>

---

## 📝 Descripción

**UrlKnight** es una aplicación de escritorio portátil de alto rendimiento diseñada para centralizar, organizar y proteger tus accesos directos de forma eficiente. A diferencia de los marcadores tradicionales, este caballero está pensado para la **movilidad y la privacidad**: puedes llevarlo en un pendrive y usarlo en cualquier estación de trabajo sin dejar rastro, manteniendo tus datos seguros de miradas indiscretas gracias a su motor de encriptación local.

Desarrollada con **CustomTkinter** y estructurada bajo arquitectura modular, garantiza una interfaz moderna con organización por categorías, búsqueda global inteligente y persistencia cifrada.

---

<img src="assets/Captura.png" width="700">

---

## 🚀 Características Principales

* **🛡️ Portabilidad y Privacidad (Base64):** Tus enlaces ya no se guardan en texto plano. La app ofusca automáticamente la base de datos local utilizando Base64 para proteger tu privacidad sin añadir dependencias pesadas.
* **📁 Organización por Categorías:** Clasifica tus enlaces de forma jerárquica. Crea, elimina y organiza marcadores de manera ordenada en carpetas lógicas.
* **🔍 Búsqueda Global en Tiempo Real:** Filtra al instante tus enlaces escribiendo en su barra de búsqueda. El radar analiza todo el archivo de manera global sin importar la categoría activa.
* **⚙️ Editor de Destinos Inteligente:** Modifica fácilmente el alias, la dirección URL o traslada un enlace de una categoría a otra de forma segura y sin dejar enlaces huérfanos.
* **💾 Persistencia con Migración Automática:** Si tienes una base de datos antigua (V2), el Knight la detecta en el primer inicio, la estructura en categorías y la encripta automáticamente sin perder un solo enlace.
* **🛸 Interfaz Refinada (UX):** Ventanas emergentes de confirmación que se calculan dinámicamente para aparecer centradas sobre la app y optimización de memoria mediante la destrucción y construcción dinámica de vistas.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** [Python 3.13.2](https://www.python.org/)
* **GUI:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Interfaz moderna y responsive).
* **Gestión de Datos:** Librería `json` para persistencia local.
* **Seguridad:** Librería estándar `base64` para la ofuscación de datos en disco.
* **Arquitectura de Rutas:** `sys` y `os` para garantizar la independencia de la unidad de almacenamiento.
* **Navegación:** `webbrowser` para integración directa con el navegador predeterminado.
* **Distribución:** `PyInstaller` para empaquetado en un ejecutable único.

--- 

## 🛡️ Guía de Portabilidad

Para que tus datos estén siempre seguros, recuerda estas reglas:
1. **La Bóveda:** El archivo `UrlKnightData.json` es la memoria encriptada de la app. Debe estar siempre en la **misma carpeta** que `UrlKnight.exe`.
2. **El Viaje:** Si cambias de PC, mueve la **carpeta completa**.
3. **Respaldo:** Puedes copiar el archivo `.json` a tu nube favorita para tener un backup instantáneo de todos tus enlaces.

---

## 📦 Descarga y Ejecución

¿No tienes Python? No lo necesitas.
1. Ve a la sección de **[Releases]** de este repositorio.
2. Descarga el archivo `.zip` con la última versión.
3. Descomprime y ejecuta `UrlKnight.exe`. ¡Eso es todo!

---

### ⚠️ Nota sobre Windows SmartScreen

Al ser un software de código abierto y no tener una firma digital pagada, Windows puede mostrar un aviso de **"Editor desconocido"**. 

**Para ejecutarlo:** 1. Haz clic en **"Más información"**.
2. Luego selecciona **"Ejecutar de todas formas"**. 

Puedes revisar el código fuente en este repositorio si te genera cualquier duda.
