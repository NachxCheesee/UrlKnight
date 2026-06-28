# Propuesta de mejoras — UrlKnight ⚔️

Este documento detalla los cambios sugeridos tras analizar el código fuente. Están organizados por prioridad e impacto.

---

## 🐛 Grupo 1 — Bugs y problemas reales (prioridad alta)

### 1.1 KeyError en `logic.abrirUrl()` — `src/logic.py:55`

**Problema:** Si se invoca `abrirUrl(alias)` con un alias que no existe en el diccionario, Python lanza `KeyError` y la app crashea.

**Solución propuesta:** Capturar `KeyError` y mostrar un mensaje al usuario (o ignorar silenciosamente según el contexto).

```python
def abrirUrl(self, alias: str) -> None:
    try:
        webbrowser.open(self.diccionario[alias])
    except KeyError:
        # Opción 1: loguear + ignorar
        # Opción 2: mostrar alerta al usuario
        pass
```

---

### 1.2 Estado global en `logic.py` — `src/logic.py:21-22`

**Problema:** `RUTA_DATOS` y `diccionario` son variables globales a nivel de módulo. Cualquier import comparte el mismo estado, lo que impide tener múltiples instancias,测试ar en aislamiento o reiniciar estado limpio sin recargar el módulo.

**Solución propuesta:** Convertir `logic.py` en una clase `GestorDatos`.

```python
class GestorDatos:
    def __init__(self, ruta_archivo: str | None = None):
        self.ruta_datos = ruta_archivo or self._obtener_ruta_archivo()
        self.diccionario: dict[str, str] = {}
        self._iniciar()

    def _obtener_ruta_archivo(self) -> str: ...
    def _iniciar(self) -> None: ...
    def abrirUrl(self, alias: str) -> None: ...
    def agregarUrl(self, alias: str, url: str) -> None: ...
    def eliminarUrl(self, alias: str) -> None: ...
```

**Impacto en el resto del código:** Mínimo. `main.py` cambia de `self.logic = logic` a `self.logic = GestorDatos()`. Las vistas acceden con `self.main.logic.diccionario`, `self.main.logic.abrirUrl()`, etc., que siguen funcionando igual.

---

### 1.3 `webbrowser.open` falla silenciosamente — `src/logic.py:55`

**Problema:** Si la URL almacenada es inválida o no hay navegador por defecto, `webbrowser.open` retorna `False` pero el valor se ignora. El usuario cree que se abrió la URL pero no pasó nada.

**Solución propuesta:** Verificar el valor de retorno y mostrar alerta si falla.

```python
def abrirUrl(self, alias: str) -> None:
    try:
        url = self.diccionario[alias]
        if not webbrowser.open(url):
            # mostrar alerta: "No se pudo abrir la URL"
    except KeyError:
        # mostrar alerta: "Alias no encontrado"
```

---

### 1.4 Encoding roto en `requirements.txt`

**Problema:** La línea `# Dependencias cr�ticas (Internas de CustomTkinter)` tiene la `ñ` corrupta. En algunos contextos (CI, pip) puede generar warnings.

**Solución propuesta:** Reemplazar `cr�ticas` por `críticas` o mejor aún, escribir en inglés para evitar problemas de encoding.

---

### 1.5 Falta `.gitignore` para artefactos de build

**Problema:** PyInstaller genera `dist/`, `build/` y `*.spec`. Si alguien build localmente y hace git add, esos archivos se suben al repo.

**Solución propuesta:** Añadir al `.gitignore`:

```
# PyInstaller
dist/
build/
*.spec
```

---

## 🎯 Grupo 2 — Mejoras de calidad de vida (prioridad media)

### 2.1 Type hints en todo el código

**Problema:** Python 3.13 permite tipado completo. El proyecto no tiene ni un solo type hint.

**Solución propuesta:** Añadir type hints a todas las funciones y métodos.

---

### 2.2 Validación real de URLs con `requests`

**Problema:** `requests==2.32.4` está en `requirements.txt` pero nunca se importa. La validación actual solo verifica el prefijo `http://` o `https://`, no si la URL es realmente accesible.

**Solución propuesta:** Al agregar una URL, hacer un HEAD request para verificar que el dominio responde.

---

### 2.3 Confirmación antes de eliminar

**Problema:** `DeleteView.eliminarUrl()` borra directamente sin pedir confirmación.

**Solución propuesta:** Mostrar un `CTkMessagebox` de confirmación (yes/no) antes de eliminar.

---

### 2.4 Editar alias/URL

**Problema:** No hay forma de modificar un alias o URL existente. Hay que borrar y volver a crear.

**Solución propuesta:** Nueva vista `EditView` o botón de edición en `UrlView`.

---

### 2.5 Búsqueda/filtro de URLs

**Problema:** Si hay muchas URLs, no hay forma de buscar una por nombre.

**Solución propuesta:** Añadir `CTkEntry` como filtro encima de la lista en `UrlView`.

---

### 2.6 Atajos de teclado

**Problema:** No hay shortcuts (Enter para guardar, Escape para salir, etc.).

**Solución propuesta:** Bindear teclas en las vistas.

---

## 💡 Grupo 3 — A futuro (nice to have)

| Ítem | Descripción |
|---|---|
| Tests unitarios | Al menos para `logic.py` con `unittest` o `pytest` |
| Categorías/carpetas | Organizar URLs por grupos |
| Export/Import | JSON externo para compartir URLs |
| Dark/Light toggle | Actualmente hardcodeado a `dark` |
| Splash mejorado | El actual solo cierra `pyi_splash` sin progreso |
| CI/CD | GitHub Actions para build automático con PyInstaller |
| Icono en las URLs | Mostrar favicon de cada sitio |

---

## 📐 Principio de cambio mínimo

Todos los cambios propuestos siguen la regla de **mínima intervención**: mantener compatibilidad hacia atrás, no romper la API existente entre módulos, y preservar la portabilidad (ruta relativa al `.exe`).
