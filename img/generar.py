"""Genera las imágenes del perfil. Todas se guardan en el repo para que carguen
siempre, también en la app de GitHub del celular (los badges externos a veces
fallan). Estilo «Marcador» de Instrumento: fondo casi negro, lima solo en lo
importante y títulos en Barlow Condensed.

Las tarjetas con texto se diseñan a 820 px de ancho y se guardan al doble: en
un celular se ven a ~45% y la letra sigue legible.

  img/banner.png      encabezado con los números de Instrumento
  img/hero.jpg        Instrumento en PC y en el celular
  img/funciones.png   qué hace la app (6 tarjetas)
  img/retos.png       retos técnicos resueltos (problema → solución)
  img/flujo.png       cómo funciona por dentro (línea de pasos)
  img/pantallas.jpg   seis pantallas de la app (3 x 2)
  img/stack.png       tecnologías con sus logos
  img/umapyoi.png     tarjeta de Umapyoi AutoReroll
  img/btn-*.png       botones

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
    ("Manrope", "200 800", "https://fonts.gstatic.com/s/manrope/v20/xn7gYHE41ni1AdIRggexSg.woff2"),
    ("Barlow", "700", "https://fonts.gstatic.com/s/barlowcondensed/v13/HTxwL3I-JCGChYJ8VI-L6OO_au7B46r2_3E.ttf"),
    ("Barlow", "800", "https://fonts.gstatic.com/s/barlowcondensed/v13/HTxwL3I-JCGChYJ8VI-L6OO_au7B47b1_3E.ttf"),
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


# los mismos colores de static/estilo.css de Instrumento
BASE = """
:root{--bg:#0B0D0C;--card:#131614;--soft:#1A1E1B;--line:#242925;--line2:#303631;
      --tx:#ECEFEA;--tx2:#C4C9C3;--mut:#979E98;--hi:#C6F432;--onhi:#0B1400;--visita:#8E9CF0;--neg:#FF8076}
*{margin:0;box-sizing:border-box}
body{font-family:Manrope;background:var(--bg);color:var(--tx);position:relative}
.d{font-family:Barlow;text-transform:uppercase}
.glow{position:absolute;width:900px;height:900px;border-radius:50%;right:-380px;top:-520px;pointer-events:none;
      background:radial-gradient(circle,rgba(198,244,50,.13),transparent 62%)}
.grid{position:absolute;inset:0;pointer-events:none;
    background-image:linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);background-size:36px 36px;
    -webkit-mask-image:linear-gradient(180deg,#000,transparent 90%)}
.marco{position:relative;padding:40px 36px;overflow:hidden}
.kicker{display:flex;align-items:center;gap:10px;font-size:15px;font-weight:800;letter-spacing:3px;color:var(--mut)}
.kicker i.punto{width:9px;height:9px;border-radius:50%;background:var(--hi)}
.titulo{font-family:Barlow;font-weight:800;text-transform:uppercase;font-size:56px;line-height:.95;margin-top:10px}
.titulo b{color:var(--hi)}
.card{background:var(--card);border:1.5px solid var(--line);border-radius:20px}
.ico{width:54px;height:54px;border-radius:14px;display:grid;place-items:center;font-size:30px;flex:none;
     background:rgba(198,244,50,.10);color:var(--hi);border:1.5px solid rgba(198,244,50,.28)}
.chip{display:inline-flex;align-items:center;gap:9px;font-weight:700;font-size:18px;padding:9px 15px;
      border-radius:999px;background:var(--card);border:1.5px solid var(--line2)}
"""


def _pagina(contenido):
    return f'<div class=marco><div class=glow></div><div class=grid></div><div style="position:relative">{contenido}</div></div>'


def banner_html():
    stats = [("300+", "pull requests<br>en 6 semanas"), ("~770", "pruebas en<br>cada cambio"), ("28", "competiciones<br>con datos")]
    barras = [("52%", "Local", True), ("27%", "Empate", False), ("21%", "Visita", False)]
    return f"""<div class=marco style="padding:46px 44px 44px;height:470px">
<div class=glow style="right:-300px;top:-460px"></div><div class=grid></div>
<div style="position:relative">
  <div class=kicker><i class=punto></i>DESARROLLADOR PYTHON · CUSCO, PERÚ</div>
  <div class=d style="font-size:108px;font-weight:800;letter-spacing:1px;line-height:.9;margin-top:16px">Wualter<span style="color:var(--hi)">S</span></div>
  <div style="font-size:25px;font-weight:700;color:var(--tx2);margin-top:14px;max-width:470px;line-height:1.3">
    Modelos estadísticos llevados a producción</div>
  <div style="display:flex;gap:12px;margin-top:30px">
    {"".join(f'<div class=card style="padding:14px 18px;border-radius:16px;min-width:150px"><div class=d style="font-size:44px;font-weight:800;line-height:1;color:var(--hi)">{n}</div><div style="font-size:14px;font-weight:700;color:var(--mut);margin-top:6px;line-height:1.3">{t}</div></div>' for n, t in stats)}
  </div>
</div>
<div class=card style="position:absolute;right:44px;top:66px;width:250px;padding:20px;transform:rotate(3deg);
     box-shadow:0 30px 60px rgba(0,0,0,.55)">
  <div style="display:flex;justify-content:space-between;font-size:12px;font-weight:700;color:var(--mut)">
    <span>Liga 1 · 18:03</span><span style="color:var(--hi)">● Datos sólidos</span></div>
  <div style="display:flex;justify-content:space-between;align-items:center;margin:18px 4px 16px">
    <div style="text-align:center"><div style="width:46px;height:46px;border-radius:50%;background:var(--soft);
      border:1.5px solid var(--line2);display:grid;place-items:center;font-weight:800;font-size:14px;margin:auto">CI</div>
      <div style="font-size:12px;font-weight:700;margin-top:6px">Cienciano</div></div>
    <div style="font-size:11px;font-weight:800;color:var(--mut)">VS</div>
    <div style="text-align:center"><div style="width:46px;height:46px;border-radius:50%;background:var(--soft);
      border:1.5px solid var(--line2);display:grid;place-items:center;font-weight:800;font-size:14px;margin:auto">ME</div>
      <div style="font-size:12px;font-weight:700;margin-top:6px">Melgar</div></div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px">
    {"".join(f'<div style="border-radius:10px;padding:8px 0;text-align:center;border:1.5px solid {"var(--hi)" if on else "var(--line)"};background:{"rgba(198,244,50,.12)" if on else "var(--soft)"}"><div style="font-size:20px;font-weight:800;color:{"var(--hi)" if on else "var(--tx)"}">{p}</div><div style="font-size:10px;font-weight:700;color:var(--mut)">{t}</div></div>' for p, t, on in barras)}
  </div>
  <div style="margin-top:14px;padding:10px 12px;border-radius:10px;background:var(--soft);font-size:12px;font-weight:700">
    <span style="color:var(--hi)">✓</span> Menos de 2.5 goles <span style="float:right;color:var(--hi)">78%</span></div>
</div>
<div class=card style="position:absolute;right:58px;top:372px;width:230px;padding:12px 16px;transform:rotate(-2deg);
     box-shadow:0 30px 60px rgba(0,0,0,.55);display:flex;align-items:center;gap:10px">
  <i style="flex:none;width:10px;height:10px;border-radius:50%;background:var(--hi);box-shadow:0 0 12px var(--hi)"></i>
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


RETOS = [
    ("Un servidor que se caía sin avisar",
     "Reentrenar dentro del proceso web pasaba los 512 MB del servidor y la instancia moría sin error ni log.",
     "Las tareas pesadas corren en un proceso hijo: al terminar, el sistema operativo recupera toda su memoria."),
    ("Mercados que nunca se contradicen",
     "«Gana Nice» y «Strasbourg o empate» llegaron a mostrarse a la vez: cada mercado se calculaba por su lado.",
     "Todos salen de una sola matriz de marcadores, y cada ajuste reparte la matriz entera."),
    ("Push sin dependencias frágiles",
     "La librería habitual de Web Push no compilaba en todos los entornos.",
     "Cifrado RFC 8291 y firma VAPID (RFC 8292) implementados a mano con cryptography."),
    ("Un historial que no se puede maquillar",
     "Recalcular partidos jugados con el modelo de hoy inflaría los aciertos: ya vio el resultado.",
     "Cada pick se guarda antes del partido y no se toca más. Sin % hasta tener 20 picks."),
    ("Un modelo que se mejora sin romperse",
     "Cambiar el modelo a ojo puede empeorarlo sin que nadie lo note.",
     "Cada semana los ajustes compiten en walk-forward con el modelo en uso; solo entra el que gana claro."),
]


def retos_html():
    filas = "".join(f"""<div class=card style="padding:24px 24px 22px;display:flex;gap:20px">
  <div class=d style="font-size:54px;font-weight:800;color:var(--hi);line-height:.9;width:62px;flex:none">{n:02d}</div>
  <div><div style="font-size:25px;font-weight:800">{t}</div>
    <div style="display:flex;gap:12px;margin-top:12px;font-size:18px;line-height:1.45;color:var(--tx2)">
      <span style="flex:none;font-size:12px;font-weight:800;letter-spacing:1.5px;color:var(--neg);padding-top:4px;width:84px">PROBLEMA</span><span>{p}</span></div>
    <div style="display:flex;gap:12px;margin-top:8px;font-size:18px;line-height:1.45;color:var(--tx)">
      <span style="flex:none;font-size:12px;font-weight:800;letter-spacing:1.5px;color:var(--hi);padding-top:4px;width:84px">SOLUCIÓN</span><span>{s}</span></div>
  </div></div>""" for n, (t, p, s) in enumerate(RETOS, 1))
    return _pagina(f"""<div class=kicker><i class=punto></i>INGENIERÍA</div>
<div class=titulo>Retos técnicos <b>que resolví</b></div>
<div style="display:flex;flex-direction:column;gap:14px;margin-top:26px">{filas}</div>""")


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
  {'' if n == len(FLUJO) else '<div style="position:absolute;left:26px;top:58px;bottom:0;width:2px;background:linear-gradient(var(--hi),var(--line2))"></div>'}
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
        f'<div style="margin-top:22px"><div style="font-size:14px;font-weight:800;letter-spacing:2.5px;color:var(--hi)">'
        f'{g.upper()}</div><div style="display:flex;flex-wrap:wrap;gap:10px;margin-top:12px">'
        + "".join(f'<span class=chip>{_marca(m, 22) if m else ""}{t}</span>' for m, t in items) + "</div></div>"
        for g, items in STACK)
    return _pagina(f"""<div class=kicker><i class=punto></i>HERRAMIENTAS</div>
<div class=titulo>Mi <b>stack</b></div>{grupos}""")


def umapyoi_html():
    chips = "".join(f"<span class=chip>{_marca(m, 20) if m else ''}{t}</span>" for m, t in
                    [("python", "Python"), ("opencv", "OpenCV"), (None, "Tesseract OCR"), (None, "Tkinter"),
                     ("discord", "Webhooks de Discord")])
    return _pagina(f"""<div class=kicker><i class=punto style="background:var(--visita)"></i>OTRO PROYECTO · AUTOMATIZACIÓN</div>
<div class=card style="padding:26px;margin-top:18px;display:flex;gap:22px;align-items:flex-start">
  <div style="width:96px;height:96px;border-radius:24px;display:grid;place-items:center;font-size:58px;flex:none;
       background:rgba(142,156,240,.12);border:1.5px solid rgba(142,156,240,.35)">🏇</div>
  <div><div class=d style="font-size:46px;font-weight:800;line-height:.95">Umapyoi AutoReroll</div>
    <div style="font-size:18px;font-weight:600;color:var(--tx2);margin-top:10px;line-height:1.45">
      Bot de escritorio para Umamusume Global: acepta términos, crea el perfil, reclama recompensas, tira el gacha
      y detecta las cartas SSR objetivo con visión por computadora. Avisa por Discord, en español e inglés.</div>
    <div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:16px">{chips}</div>
    <div style="margin-top:14px;font-size:14px;font-weight:700;color:var(--mut)"><i class="ph ph-lock-key"></i> Repositorio privado</div>
  </div>
</div>""")


# nombre, texto, principal (lima) o no
BOTONES = [
    ("app", "Abrir la app", True),
    ("aciertos", "Aciertos públicos", False),
    ("como", "Cómo funciona", False),
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
<div class=glow style="right:-300px;top:-500px;width:1100px;height:1100px"></div><div class=grid></div>
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
            f'<div class=glow style="width:1100px;height:1100px"></div><div class=grid></div>'
            f'<div style="position:absolute;inset:0;display:grid;grid-template-columns:repeat(3,400px);'
            f'justify-content:center;column-gap:90px;row-gap:70px;padding-top:60px">{celdas}</div></div>')


def botones(b, css):
    pg = b.new_page(viewport={"width": 900, "height": 120}, device_scale_factor=2)
    for nombre, texto, principal in BOTONES:
        estilo = ("background:#C6F432;color:#0B1400" if principal else
                  "background:#131614;color:#ECEFEA;box-shadow:inset 0 0 0 2px #303631")
        pg.set_content(f"<html><head><meta charset=utf-8><style>{css}*{{margin:0}}body{{background:transparent}}"
                       f"b{{display:inline-block;font:800 19px Manrope;letter-spacing:.3px;padding:13px 26px;"
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
                             ("retos.png", retos_html()), ("flujo.png", flujo_html()),
                             ("stack.png", stack_html()), ("umapyoi.png", umapyoi_html())):
            _png(_foto(b, css, html, 820), nombre)
        # JPEG: son capturas, en PNG pesan tres veces más
        _foto(b, css, hero_html(), 1700, 1).save(IMG / "hero.jpg", quality=86, optimize=True, progressive=True)
        _foto(b, css, pantallas_html(), 1620, 1).save(IMG / "pantallas.jpg", quality=84, optimize=True, progressive=True)
        b.close()


if __name__ == "__main__":
    main()
