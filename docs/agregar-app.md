# Cómo agregar una app nueva al perfil

El perfil es un marco neutro (fondo tinta, violeta y cian). Cada app conserva
su propio color dentro de su tarjeta, su encabezado y sus botones, así todas
combinan sin perder su identidad.

## 1. Datos de la app

En `img/generar.py`, agrega un diccionario a `PROYECTOS`:

```python
dict(clave="miapp", nombre="Mi App", color="#FF9F43", icono="ph:rocket", seccion=True,
     tipo="APP WEB", lema="Una línea que diga qué resuelve",
     texto="Dos o tres líneas sobre qué hace y para quién.",
     cifras=[("1.2k", "usuarios<br>activos")],          # solo números reales; [] si aún no hay
     chips=[("python", "Python"), (None, "Otra herramienta")],
     pie='<span style="color:var(--vivo)">●</span> En producción · miapp.com'),
```

- `color`: el color principal de la marca de la app.
- `icono`: un ícono de Phosphor (`ph:nombre`) o un emoji.
- `chips`: el logo sale de `img/recursos/marcas/<nombre>.svg` (Simple Icons); `None` = sin logo.
- `seccion=True` si la app tendrá su propio bloque en el README (encabezado `img/app-<clave>.png`).

Si la app tiene botones, agrégalos a `BOTONES` con su `clave`: toman el color de la app.
Si alguna habilidad viene de la app, en `HABILIDADES` usa la primera palabra de su nombre.

## 2. Generar las imágenes

```bash
pip install playwright pillow
CAPTURAS=/ruta/capturas python img/generar.py
```

## 3. Bloque en el README

Debajo de la sección de la última app:

```html
<img src="img/app-miapp.png" alt="Mi App · lema" width="100%"/>

Qué hace la app en una o dos líneas.

<a href="https://miapp.com"><img src="img/hero-miapp.jpg" alt="Mi App en PC y en el celular" width="100%"/></a>

<p>
  <a href="https://miapp.com"><img src="img/btn-miapp.png" height="40" alt="Abrir la app"/></a>
</p>
```

Reglas: sin badges externos ni enlaces internos `#` (fallan en la app de GitHub del
celular), sin Mermaid y sin cifras inventadas.
