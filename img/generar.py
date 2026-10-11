"""Genera las imágenes del perfil. Todas se guardan en el repo para que carguen
siempre, también en la app de GitHub del celular (los badges externos a veces
fallan). Identidad propia del perfil: fondo tinta, violeta y cian de acento,
títulos en Space Grotesk y texto en Inter. Cada app conserva su color dentro de su tarjeta.

Las tarjetas con texto se diseñan a 820 px de ancho y se guardan al doble: en
un celular se ven a ~45% y la letra sigue legible.

  img/banner.png      encabezado: quién soy y qué hago
  img/hero.jpg        Instrumento en PC y en el celular
  img/funciones.png   qué hace la app (6 tarjetas)
  img/proyectos.png   mis proyectos (Instrumento y Umapyoi)
  img/habilidades.png lo que sé resolver, cada habilidad con su prueba
  img/flujo.png       cómo funciona por dentro (línea de pasos)
  img/pantallas.jpg   seis pantallas de la app (3 x 2)
  img/stack.png       tecnologías con sus logos
  img/app-*.png       encabezado de la sección de cada app, con su color
  img/btn-*.png       botones (con el color de su app)

Recursos en img/recursos/: íconos Phosphor (MIT) y logos de Simple Icons (CC0).
Las capturas salen de scripts/capturas_app.py. Uso:

  pip install playwright pillow
  CAPTURAS=/ruta/capturas python img/generar.py
"""

import base64
import io
import json
import os
import pathlib
import urllib.request

from PIL import Image
from playwright.sync_api import sync_playwright

IMG = pathlib.Path(__file__).resolve().parent
REC = IMG / "recursos"
CAPTURAS = pathlib.Path(os.environ.get("CAPTURAS") or IMG.parent / "capturas")
FUENTES = [
    ("Texto", "100 900", "https://fonts.gstatic.com/s/inter/v20/UcC73FwrK3iLTeHuS_nVMrMxCp50SjIa1ZL7.woff2"),
    ("Display", "300 700", "https://fonts.gstatic.com/s/spacegrotesk/v22/V8mDoQDjQSkFtoMM3T6r8E7mPbF4Cw.woff2"),
    ("Mono", "200 800", "https://fonts.gstatic.com/s/jetbrainsmono/v24/tDbY2o-flEEny0FZhsfKu5WU4zr3E_BX0PnT8RD8-qxjPQ.ttf"),
]


def _b64(datos):
    return base64.b64encode(datos).decode()


def _fuentes():
    css = ""
    for nombre, peso, url in FUENTES:
        fmt = "woff2" if url.endswith("woff2") else "truetype"
        css += (f"@font-face{{font-family:{nombre};font-weight:{peso};"
                f"src:url(data:font/{fmt};base64,{_b64(urllib.request.urlopen(url).read())}) format('{fmt}')}}\n")
    fosforo = (REC / "style.css").read_text().replace(
        'url("./Phosphor.woff2")', f'url(data:font/woff2;base64,{_b64((REC / "Phosphor.woff2").read_bytes())})')
    return css + fosforo


def _uri(ruta):
    return "data:image/png;base64," + _b64(ruta.read_bytes())


def _marca(nombre, alto=34):
    """Logo de Simple Icons con su color (blanco si el color se pierde en el fondo oscuro)."""
    color = json.loads((REC / "marcas" / "colores.json").read_text())[nombre]
    r, g, b = (int(color[i:i + 2], 16) for i in (0, 2, 4))
    if 0.2126 * r + 0.7152 * g + 0.0722 * b < 70:
        color = "ECEFEA"
    svg = (REC / "marcas" / f"{nombre}.svg").read_text().replace("<svg ", f'<svg fill="#{color}" ', 1)
    return f'<img src="data:image/svg+xml;base64,{_b64(svg.encode())}" style="height:{alto}px;width:{alto}px">'


# paleta propia del perfil; --vivo marca lo que está en producción
BASE = """
:root{--bg:#0A0B14;--card:#121427;--soft:#1A1D35;--line:#242845;--line2:#323759;
      --tx:#EEF0FF;--tx2:#C4C8E4;--mut:#8F95BA;--hi:#9D8CFF;--cian:#3DD9EB;--vivo:#3DD68C;--neg:#FF8076;
      --grad:linear-gradient(100deg,#9D8CFF,#3DD9EB)}
*{margin:0;box-sizing:border-box}
body{font-family:Texto;background:var(--bg);color:var(--tx);position:relative}
.d{font-family:Display;letter-spacing:-.02em}
.g{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.glow{position:absolute;width:900px;height:900px;border-radius:50%;right:-380px;top:-520px;pointer-events:none;
      background:radial-gradient(circle,rgba(157,140,255,.16),transparent 62%)}
.grid{position:absolute;inset:0;pointer-events:none;
    background-image:linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);background-size:36px 36px;
    -webkit-mask-image:linear-gradient(180deg,#000,transparent 90%)}
.marco{position:relative;padding:40px 36px;overflow:hidden}
.kicker{display:flex;align-items:center;gap:10px;font-size:15px;font-weight:800;letter-spacing:3px;color:var(--mut)}
.kicker i.punto{width:9px;height:9px;border-radius:50%;background:var(--hi)}
.titulo{font-family:Display;font-weight:700;letter-spacing:-.03em;font-size:52px;line-height:1;margin-top:10px}
.titulo b{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.card{background:var(--card);border:1.5px solid var(--line);border-radius:20px}
.ico{width:54px;height:54px;border-radius:14px;display:grid;place-items:center;font-size:30px;flex:none;
     background:rgba(157,140,255,.12);color:var(--hi);border:1.5px solid rgba(157,140,255,.32)}
.chip{display:inline-flex;align-items:center;gap:9px;font-weight:700;font-size:18px;padding:9px 15px;
      border-radius:999px;background:var(--card);border:1.5px solid var(--line2)}
"""


def _pagina(contenido):
    return f'<div class=marco><div class=glow></div><div class=grid></div><div style="position:relative">{contenido}</div></div>'


AREAS = [("chart-line-up", "Modelos de datos"), ("devices", "Apps web"), ("robot", "Automatización")]


def banner_html():
    areas = "".join(f'<div class=card style="padding:12px 14px;border-radius:14px;display:flex;align-items:center;gap:10px">'
                    f'<i class="ph ph-{i}" style="font-size:24px;color:var(--hi)"></i>'
                    f'<span style="font-size:15px;font-weight:800">{t}</span></div>' for i, t in AREAS)
    k, s, f, c = ("color:#C792EA", "color:#7EE0F0", "color:#82AAFF", "color:#6B7194")
    codigo = f"""<span style="{k}">class</span> <span style="{f}">Wualter</span>:
    base  = <span style="{s}">"Cusco, Perú"</span>
    hace  = [<span style="{s}">"datos"</span>, <span style="{s}">"web"</span>, <span style="{s}">"bots"</span>]
    stack = [<span style="{s}">"Python"</span>, <span style="{s}">"SQL"</span>, <span style="{s}">"JS"</span>]
    <span style="{k}">def</span> <span style="{f}">ahora</span>(self):
        <span style="{k}">return</span> <span style="{s}">"Instrumento"</span>"""
    return f"""<div class=marco style="padding:46px 44px 44px;height:470px">
<div class=glow style="right:-300px;top:-460px"></div><div class=grid></div>
<div style="position:relative">
  <div class=kicker><i class=punto></i>DESARROLLADOR PYTHON · CUSCO, PERÚ</div>
  <div class=d style="font-size:100px;font-weight:700;letter-spacing:-.04em;line-height:.95;margin-top:14px">Wualter<span class=g>S</span></div>
  <div style="font-size:24px;font-weight:700;color:var(--tx2);margin-top:14px;max-width:440px;line-height:1.3">
    Construyo productos de datos de punta a punta</div>
  <div style="display:flex;gap:10px;margin-top:30px">{areas}</div>
</div>
<div class=card style="position:absolute;right:40px;top:40px;width:290px;transform:rotate(2.5deg);overflow:hidden;
     box-shadow:0 30px 60px rgba(0,0,0,.55)">
  <div style="display:flex;align-items:center;gap:6px;padding:11px 14px;border-bottom:1.5px solid var(--line);background:var(--soft)">
    <i style="width:10px;height:10px;border-radius:50%;background:#FF8076"></i>
    <i style="width:10px;height:10px;border-radius:50%;background:#F2C94C"></i>
    <i style="width:10px;height:10px;border-radius:50%;background:#3DD68C"></i>
    <span style="font-family:Mono;font-size:12px;color:var(--mut);margin-left:8px">wualter.py</span></div>
  <pre style="font-family:Mono;font-size:12.5px;line-height:1.6;padding:14px 16px;color:var(--tx);white-space:pre">{codigo}</pre>
</div>
<div class=card style="position:absolute;right:66px;top:368px;width:240px;padding:12px 16px;transform:rotate(-2deg);
     box-shadow:0 30px 60px rgba(0,0,0,.55);display:flex;align-items:center;gap:10px">
  <i style="flex:none;width:10px;height:10px;border-radius:50%;background:var(--vivo);box-shadow:0 0 12px var(--vivo)"></i>
  <div><div style="font-size:11px;font-weight:800;letter-spacing:2px;color:var(--mut)">EN PRODUCCIÓN</div>
  <div style="font-size:15px;font-weight:800;margin-top:2px">instrumentoapp.com</div></div>
</div>
</div>"""


FUNCIONES = [
    ("calendar-check", "Hoy", "Los picks más seguros del día, cada uno con su probabilidad y el respaldo de datos."),
    ("magnifying-glass", "Análisis", "Quién gana, goles, córners, tarjetas y tiros, con una combinada sugerida."),
    ("broadcast", "En vivo", "Gráfico de presión durante el partido y avisos push con goles y picks."),
    ("stack", "Combinar", "La probabilidad de que salgan todas las líneas, calculada en conjunto."),
    ("list-checks", "Registro", "Tus picks, acierto, ganancia y «¿Cuánto meter?» según tu bank."),
    ("arrows-clockwise", "Se mejora solo", "Reentrena cada día y cada semana prueba ajustes contra partidos jugados."),
]


def funciones_html():
    tarjetas = "".join(
        f'<div class=card style="padding:22px"><div class=ico><i class="ph ph-{i}"></i></div>'
        f'<div style="font-size:24px;font-weight:800;margin-top:16px">{t}</div>'
        f'<div style="font-size:18px;font-weight:600;color:var(--tx2);margin-top:6px;line-height:1.4">{d}</div></div>'
        for i, t, d in FUNCIONES)
    return _pagina(f"""<div class=kicker><i class=punto></i>INSTRUMENTO</div>
<div class=titulo>Qué hace <b>la app</b></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:26px">{tarjetas}</div>""")


# ícono, habilidad, prueba concreta, proyecto
HABILIDADES = [
    ("chart-line-up", "Modelos estadísticos", "Dixon-Coles y Binomial Negativa. Todos los mercados salen de una sola matriz de marcadores, así nunca se contradicen.", "Instrumento"),
    ("shield-check", "Validación honesta", "Backtest walk-forward: un ajuste entra solo si gana. Cada pick se guarda antes del partido y no se toca más.", "Instrumento"),
    ("cpu", "Servidores estables", "Las tareas pesadas corren en un proceso hijo para no pasar el límite de memoria; el sistema la recupera entera.", "Instrumento"),
    ("lock-key", "Criptografía aplicada", "Cifrado de Web Push (RFC 8291) y firma VAPID (RFC 8292) implementados a mano con cryptography.", "Instrumento"),
    ("eye", "Visión por computadora", "OpenCV y Tesseract leen la pantalla del juego y detectan las cartas SSR objetivo.", "Umapyoi"),
    ("heartbeat", "Automatización vigilada", "Tareas de fondo diarias que reportan su latido y avisan por Telegram si una se cae.", "Instrumento"),
]


def habilidades_html():
    def etiqueta(p):
        color, fondo = COLOR[p], _rgba(COLOR[p], .12)
        return (f'<span style="font-size:11px;font-weight:800;letter-spacing:1.5px;color:{color};background:{fondo};'
                f'padding:4px 9px;border-radius:999px">{p.upper()}</span>')
    tarjetas = "".join(
        f'<div class=card style="padding:22px"><div style="display:flex;justify-content:space-between;align-items:flex-start">'
        f'<div class=ico><i class="ph ph-{i}"></i></div>{etiqueta(pr)}</div>'
        f'<div style="font-size:23px;font-weight:800;margin-top:16px">{t}</div>'
        f'<div style="font-size:17px;font-weight:600;color:var(--tx2);margin-top:6px;line-height:1.45">{d}</div></div>'
        for i, t, d, pr in HABILIDADES)
    return _pagina(f"""<div class=kicker><i class=punto></i>HABILIDADES CON PRUEBA</div>
<div class=titulo>Lo que sé <b>resolver</b></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:26px">{tarjetas}</div>""")


FLUJO = [
    ("database", "Datos", "API-Football: partidos, estadísticas y alineaciones de 28 competiciones."),
    ("soccer-ball", "Goles", "Dixon-Coles con xG, altitud, lesiones y descanso: una sola matriz de marcadores."),
    ("chart-bar", "Estadísticas", "Binomial Negativa para córners, tarjetas, tiros y faltas; cópula para combinadas."),
    ("shield-check", "Validación", "Backtest walk-forward, calibración y control de falsos descubrimientos."),
    ("target", "Medición", "Pick guardado antes del partido, cerrado con el resultado y CLV contra el cierre."),
    ("arrows-clockwise", "Mejora", "Cada semana compite contra 7 ajustes: solo entra el que gana."),
]


def flujo_html():
    pasos = "".join(f"""<div style="display:flex;gap:20px;position:relative;padding-bottom:{0 if n == len(FLUJO) else 22}px">
  {'' if n == len(FLUJO) else '<div style="position:absolute;left:26px;top:58px;bottom:0;width:2px;background:linear-gradient(var(--hi),var(--cian))"></div>'}
  <div class=ico style="position:relative"><i class="ph ph-{i}"></i></div>
  <div style="padding-top:4px"><div style="display:flex;align-items:baseline;gap:10px">
      <span class=d style="font-size:16px;font-weight:700;color:var(--mut)">0{n}</span>
      <span style="font-size:24px;font-weight:800">{t}</span></div>
    <div style="font-size:18px;font-weight:600;color:var(--tx2);margin-top:4px;line-height:1.45">{d}</div></div>
</div>""" for n, (i, t, d) in enumerate(FLUJO, 1))
    return _pagina(f"""<div class=kicker><i class=punto></i>POR DENTRO</div>
<div class=titulo>Cómo <b>funciona</b></div>
<div class=card style="padding:28px 26px;margin-top:26px">{pasos}</div>""")


STACK = [
    ("Lenguajes", [("python", "Python"), ("javascript", "JavaScript"), ("html5", "HTML"), ("css3", "CSS"), (None, "SQL")]),
    ("Backend y datos", [("flask", "Flask"), ("postgresql", "PostgreSQL"), ("sqlite", "SQLite"), ("pandas", "pandas"),
                         ("numpy", "NumPy"), ("scipy", "SciPy")]),
    ("Automatización", [("opencv", "OpenCV"), (None, "Tesseract OCR"), ("selenium", "Selenium"), ("discord", "Discord")]),
    ("Calidad y despliegue", [("pytest", "pytest"), (None, "Playwright"), ("ruff", "ruff"), ("githubactions", "GitHub Actions"),
                              ("render", "Render"), ("pwa", "PWA"), ("git", "Git")]),
]


def stack_html():
    grupos = "".join(
        f'<div style="margin-top:22px"><div style="font-size:14px;font-weight:800;letter-spacing:2.5px;color:var(--cian)">'
        f'{g.upper()}</div><div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:12px">'
        + "".join(f'<span class=chip>{_marca(m, 22) if m else ""}{t}</span>' for m, t in items) + "</div></div>"
        for g, items in STACK)
    return _pagina(f"""<div class=kicker><i class=punto></i>HERRAMIENTAS</div>
<div class=titulo>Mi <b>stack</b></div>{grupos}""")


def _chips(lista, alto=18):
    return "".join(f'<span class=chip style="font-size:15px;padding:7px 12px;gap:7px">'
                   f'{_marca(m, alto) if m else ""}{t}</span>' for m, t in lista)


# Cada app conserva su propio color (el de su marca) dentro del marco neutro del perfil.
# Para sumar una app nueva: agregar un diccionario aquí (clave = nombre de archivo),
# sus botones en BOTONES y correr este script. Los pasos completos están en docs/agregar-app.md.
PROYECTOS = [
    dict(clave="instrumento", nombre="Instrumento", color="#C6F432", icono="ph:soccer-ball", seccion=True,
         tipo="DESTACADO · APP WEB", lema="Pronósticos de fútbol con un modelo real",
         texto="Pronósticos de fútbol con un modelo estadístico real. Gratis, en PC y celular, y publica cuánto acierta.",
         cifras=[("300+", "PRs en<br>6 semanas"), ("~770", "pruebas por<br>cambio"), ("28", "ligas y<br>copas")],
         chips=[("python", "Python"), ("flask", "Flask"), ("postgresql", "PostgreSQL"), ("scipy", "SciPy"), ("javascript", "JS")],
         pie='<span style="color:var(--vivo)">●</span> En producción · instrumentoapp.com'),
    dict(clave="umapyoi", nombre="Umapyoi AutoReroll", color="#FF8FB8", icono="🏇",
         tipo="AUTOMATIZACIÓN · ESCRITORIO", lema="El reroll de Umamusume Global, en automático",
         texto="Bot que hace solo el reroll de Umamusume Global: crea el perfil, reclama recompensas, tira el gacha "
               "y detecta las cartas SSR con visión por computadora. Avisa por Discord.",
         cifras=[],
         chips=[("python", "Python"), ("opencv", "OpenCV"), (None, "Tesseract OCR"), (None, "Tkinter"), ("discord", "Discord")],
         pie='<i class="ph ph-lock-key"></i> Repositorio privado'),
]
COLOR = {p["nombre"].split()[0]: p["color"] for p in PROYECTOS}     # «Instrumento», «Umapyoi»


def _rgba(color, a):
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r},{g},{b},{a})"


def _icono(p, tam):
    i = p["icono"]
    return f'<i class="ph ph-{i[3:]}"></i>' if i.startswith("ph:") else i


def _sello(p, lado=62, radio=18, letra=34):
    c = p["color"]
    return (f'<div style="width:{lado}px;height:{lado}px;border-radius:{radio}px;display:grid;place-items:center;'
            f'font-size:{letra}px;flex:none;color:{c};background:{_rgba(c, .12)};border:1.5px solid {_rgba(c, .4)}">'
            f'{_icono(p, letra)}</div>')


def _tarjeta(p):
    c = p["color"]
    cifras = "".join(f'<div style="flex:1;background:var(--soft);border-radius:12px;padding:10px 12px">'
                     f'<div class=d style="font-size:30px;font-weight:700;line-height:1;color:{c}">{n}</div>'
                     f'<div style="font-size:12px;font-weight:700;color:var(--mut);margin-top:4px;line-height:1.3">{t}</div></div>'
                     for n, t in p["cifras"])
    cifras = f'<div style="display:flex;gap:8px;margin-top:16px">{cifras}</div>' if cifras else ""
    return f"""<div class=card style="padding:24px;display:flex;flex-direction:column;position:relative;overflow:hidden;
     border-top:3px solid {c}">
  <div style="position:absolute;width:320px;height:320px;right:-160px;top:-180px;border-radius:50%;
       background:radial-gradient(circle,{_rgba(c, .16)},transparent 65%)"></div>
  <div style="display:flex;align-items:center;gap:14px;position:relative">{_sello(p)}
    <div><div style="font-size:11px;font-weight:800;letter-spacing:2px;color:{c}">{p["tipo"]}</div>
      <div class=d style="font-size:32px;font-weight:700;line-height:1;margin-top:4px">{p["nombre"]}</div></div></div>
  <div style="font-size:16.5px;font-weight:600;color:var(--tx2);margin-top:16px;line-height:1.45">{p["texto"]}</div>
  {cifras}
  <div style="display:flex;flex-wrap:wrap;gap:7px;margin-top:16px">{_chips(p["chips"])}</div>
  <div style="margin-top:auto;padding-top:18px;font-size:14px;font-weight:700;color:var(--mut)">{p["pie"]}</div>
</div>"""


def proyectos_html():
    return _pagina(f"""<div class=kicker><i class=punto></i>PORTAFOLIO</div>
<div class=titulo>Mis <b>proyectos</b></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:26px">{"".join(map(_tarjeta, PROYECTOS))}</div>""")


def cabecera_html(p):
    """Encabezado de la sección de cada app en el README, con su color."""
    c = p["color"]
    return f"""<div class=marco style="padding:26px 36px">
<div style="position:absolute;width:700px;height:700px;right:-300px;top:-420px;border-radius:50%;
     background:radial-gradient(circle,{_rgba(c, .16)},transparent 62%)"></div><div class=grid></div>
<div style="position:relative;display:flex;align-items:center;gap:20px;padding-left:18px;border-left:4px solid {c}">
  {_sello(p, 74, 20, 40)}
  <div><div style="font-size:13px;font-weight:800;letter-spacing:2.5px;color:{c}">{p["tipo"]}</div>
    <div class=d style="font-size:46px;font-weight:700;line-height:1;margin-top:4px">{p["nombre"]}</div>
    <div style="font-size:18px;font-weight:600;color:var(--tx2);margin-top:6px">{p["lema"]}</div></div>
</div></div>"""


# archivo, texto, app (su color) y si es el botón principal
BOTONES = [
    ("app", "Abrir la app", "instrumento", True),
    ("aciertos", "Aciertos públicos", "instrumento", False),
    ("como", "Cómo funciona", "instrumento", False),
]


def _marco_tel(img, ancho, extra=""):
    borde = round(ancho * .03)
    alto = round((ancho - 2 * borde) * 844 / 390) + 2 * borde      # proporción de la captura (390 x 844)
    return (f'<div style="width:{ancho}px;height:{alto}px;border-radius:{ancho * .16:.0f}px;background:#000;'
            f'padding:{borde}px;box-shadow:0 30px 80px rgba(0,0,0,.6),0 0 0 2px var(--line2);flex:none;{extra}">'
            f'<div style="width:100%;height:100%;border-radius:{ancho * .13:.0f}px;overflow:hidden;background:var(--bg)">'
            f'<img src="{_uri(img)}" style="width:100%;display:block"></div></div>')


def hero_html():
    return f"""<div style="position:relative;width:1700px;height:930px;overflow:hidden">
<div class=glow style="right:-300px;top:-500px;width:1100px;height:1100px;background:radial-gradient(circle,{_rgba(PROYECTOS[0]["color"], .14)},transparent 62%)"></div><div class=grid></div>
<div style="position:absolute;left:70px;top:60px;width:1260px;border-radius:22px;background:#000;padding:12px;
            box-shadow:0 40px 100px rgba(0,0,0,.7),0 0 0 2px var(--line2)">
  <div style="border-radius:12px;overflow:hidden"><img src="{_uri(CAPTURAS / 'pc-partidos.png')}" style="width:100%;display:block"></div>
</div>
<div style="position:absolute;right:60px;top:150px">{_marco_tel(CAPTURAS / 'm-hoy.png', 330)}</div></div>"""


PANTALLAS = [("m-hoy", "Hoy"), ("m-partidos", "Partidos"), ("m-analisis", "Análisis"),
             ("m-vivo", "En vivo"), ("m-combinar", "Combinar"), ("m-registro", "Registro")]


def pantallas_html():
    celdas = "".join(f'<div style="display:flex;flex-direction:column;align-items:center">'
                     f'{_marco_tel(CAPTURAS / f"{a}.png", 400)}'
                     f'<div class=d style="margin-top:26px;font-weight:700;font-size:64px;color:var(--tx)">{e}</div></div>'
                     for a, e in PANTALLAS)
    return (f'<div style="position:relative;width:1620px;height:2200px;overflow:hidden">'
            f'<div class=glow style="width:1100px;height:1100px;background:radial-gradient(circle,{_rgba(PROYECTOS[0]["color"], .14)},transparent 62%)"></div><div class=grid></div>'
            f'<div style="position:absolute;inset:0;display:grid;grid-template-columns:repeat(3,400px);'
            f'justify-content:center;column-gap:90px;row-gap:70px;padding-top:60px">{celdas}</div></div>')


def botones(b, css):
    pg = b.new_page(viewport={"width": 900, "height": 120}, device_scale_factor=2)
    color = {p["clave"]: p["color"] for p in PROYECTOS}
    for nombre, texto, app, principal in BOTONES:
        estilo = (f"background:{color[app]};color:#0A0B14" if principal else
                  f"background:#121427;color:#EEF0FF;box-shadow:inset 0 0 0 2px {_rgba(color[app], .45)}")
        pg.set_content(f"<html><head><meta charset=utf-8><style>{css}*{{margin:0}}body{{background:transparent}}"
                       f"b{{display:inline-block;font:700 19px Texto;letter-spacing:.3px;padding:13px 26px;"
                       f"border-radius:999px;{estilo}}}</style></head>"
                       f"<body><b id=b>{texto}</b></body></html>")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(150)
        pg.locator("#b").screenshot(path=str(IMG / f"btn-{nombre}.png"), omit_background=True)
    pg.close()


def _foto(b, css, cuerpo, ancho, escala=2):
    """Foto del cuerpo completo (el alto sale del contenido)."""
    pg = b.new_page(viewport={"width": ancho, "height": 400}, device_scale_factor=escala)
    pg.set_content(f"<html><head><meta charset=utf-8><style>{css}{BASE}</style></head>"
                   f"<body><div id=r style='width:{ancho}px'>{cuerpo}</div></body></html>")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(600)
    img = Image.open(io.BytesIO(pg.locator("#r").screenshot())).convert("RGB")
    pg.close()
    return img


def _png(img, nombre):
    # las tarjetas son de colores planos: con 256 colores pesan mucho menos y no se nota
    img.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(IMG / nombre, optimize=True)


def main():
    css = _fuentes()
    with sync_playwright() as p:
        b = p.chromium.launch()
        botones(b, css)
        for nombre, html in (("banner.png", banner_html()), ("funciones.png", funciones_html()),
                             ("habilidades.png", habilidades_html()), ("flujo.png", flujo_html()),
                             ("stack.png", stack_html()), ("proyectos.png", proyectos_html())):
            _png(_foto(b, css, html, 820), nombre)
        for p in (p for p in PROYECTOS if p.get("seccion")):   # solo las apps con sección propia
            _png(_foto(b, css, cabecera_html(p), 820), f"app-{p['clave']}.png")
        # JPEG: son capturas, en PNG pesan tres veces más
        _foto(b, css, hero_html(), 1700, 1).save(IMG / "hero.jpg", quality=86, optimize=True, progressive=True)
        _foto(b, css, pantallas_html(), 1620, 1).save(IMG / "pantallas.jpg", quality=84, optimize=True, progressive=True)
        b.close()


if __name__ == "__main__":
    main()
