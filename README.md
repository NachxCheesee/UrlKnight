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

**UrlKnight** es una aplicación de escritorio diseñada para centralizar tus accesos directos de forma eficiente. A diferencia de los marcadores tradicionales, este caballero está pensado para la **movilidad**: puedes llevarlo en un pendrive y usarlo en cualquier estación de trabajo (universidad, oficina o casa) sin dejar rastro en el sistema operativo local.

Desarrollada con **CustomTkinter**, garantiza una interfaz moderna y una persistencia de datos inteligente que acompaña siempre al ejecutable.

---

<img src="assets/Captura.png" width="700">

---

## 🚀 Características Principales

* **🛡️ Portabilidad Total:** Olvídate de carpetas ocultas en `%AppData%`. El Knight guarda sus datos exactamente donde tú lo pongas.
* **💾 Persistencia Automática:** Gestión de archivos JSON dinámica mediante `sys.executable`, asegurando que tus links viajen contigo.
* **⚡ Experiencia Profesional:** Splash Screen de carga y mensajes de sistema estilizados con `CTkMessagebox`.
* **📖 Guía Integrada:** Incluye un manual de usuario dentro de la app para asegurar el correcto manejo de la "Bóveda de Datos".

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** [Python 3.13.2](https://www.python.org/)
* **GUI:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Interfaz moderna y responsive).
* **Gestión de Datos:** Librería `json` para persistencia local.
* **Arquitectura de Rutas:** `sys` y `os` para garantizar la independencia de la unidad de almacenamiento.
* **Navegación:** `webbrowser` para integración directa con el navegador predeterminado.
* **Distribución:** `PyInstaller` para empaquetado en un ejecutable único.

--- 

## 🛡️ Guía de Portabilidad

Para que tus datos estén siempre seguros, recuerda estas reglas:
1. **La Bóveda:** El archivo `UrlKnightData.json` es la memoria de la app. Debe estar siempre en la **misma carpeta** que `UrlKnight.exe`.
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
