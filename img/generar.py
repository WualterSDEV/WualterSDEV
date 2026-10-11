"""Genera las imágenes del perfil. Todas se guardan en el repo para que carguen
siempre, también en la app de GitHub del celular (los badges externos a veces
fallan). Colores y letras del estilo «Marcador» de Instrumento: fondo casi
negro, lima solo en lo importante y títulos en Barlow Condensed.

  img/banner.png       encabezado
  img/hero.jpg         Instrumento en PC y en el celular
  img/pantallas.jpg    seis pantallas de la app (3 x 2, legible en el celular)
  img/btn-*.png        botones

Las capturas salen de scripts/capturas_app.py (ver ahí cómo correrlo en el
repo de la app). Uso:

  pip install playwright pillow
  CAPTURAS=/ruta/capturas python img/generar.py
"""

import base64
import io
import os
import pathlib
import urllib.request

from PIL import Image
from playwright.sync_api import sync_playwright

IMG = pathlib.Path(__file__).resolve().parent
CAPTURAS = pathlib.Path(os.environ.get("CAPTURAS") or IMG.parent / "capturas")
FUENTES = [
    ("Manrope", "200 800", "https://fonts.gstatic.com/s/manrope/v20/xn7gYHE41ni1AdIRggexSg.woff2"),
    ("Barlow", "700", "https://fonts.gstatic.com/s/barlowcondensed/v13/HTxwL3I-JCGChYJ8VI-L6OO_au7B46r2_3E.ttf"),
    ("Barlow", "800", "https://fonts.gstatic.com/s/barlowcondensed/v13/HTxwL3I-JCGChYJ8VI-L6OO_au7B47b1_3E.ttf"),
]


def _fuentes():
    css = ""
    for nombre, peso, url in FUENTES:
        datos = base64.b64encode(urllib.request.urlopen(url).read()).decode()
        fmt = "woff2" if url.endswith("woff2") else "truetype"
        css += (f"@font-face{{font-family:{nombre};font-weight:{peso};"
                f"src:url(data:font/{fmt};base64,{datos}) format('{fmt}')}}\n")
    return css


def _uri(ruta):
    return "data:image/png;base64," + base64.b64encode(ruta.read_bytes()).decode()


# los mismos colores de static/estilo.css de Instrumento
BASE = """
:root{--bg:#0B0D0C;--card:#131614;--line:#242925;--line2:#303631;
      --tx:#ECEFEA;--tx2:#C4C9C3;--mut:#979E98;--hi:#C6F432}
*{margin:0;box-sizing:border-box}
body{font-family:Manrope;background:var(--bg);color:var(--tx);overflow:hidden;position:relative}
.d{font-family:Barlow;text-transform:uppercase}
.glow{position:absolute;width:1100px;height:1100px;border-radius:50%;right:-420px;top:-600px;
      background:radial-gradient(circle,rgba(198,244,50,.14),transparent 62%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);background-size:44px 44px;
    -webkit-mask-image:linear-gradient(180deg,#000,transparent 95%)}
"""

BANNER = """<div class=glow></div><div class=grid></div>
<div style="position:absolute;inset:0;padding:0 90px;display:flex;flex-direction:column;justify-content:center">
  <div style="display:flex;align-items:center;gap:14px;font-size:26px;font-weight:700;color:var(--mut);letter-spacing:5px">
    <i style="width:12px;height:12px;border-radius:50%;background:var(--hi)"></i>DESARROLLADOR PYTHON</div>
  <div class=d style="font-size:190px;font-weight:800;letter-spacing:2px;line-height:.9;margin-top:14px">
    Wualter<span style="color:var(--hi)">S</span></div>
  <div style="font-size:40px;font-weight:700;color:var(--tx2);margin-top:22px">
    Modelos estadísticos llevados a producción · Cusco, Perú</div>
</div>"""

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
    return f"""<div class=glow style="right:-300px;top:-500px"></div><div class=grid></div>
<div style="position:absolute;left:70px;top:60px;width:1260px;border-radius:22px;background:#000;padding:12px;
            box-shadow:0 40px 100px rgba(0,0,0,.7),0 0 0 2px var(--line2)">
  <div style="border-radius:12px;overflow:hidden"><img src="{_uri(CAPTURAS / 'pc-partidos.png')}" style="width:100%;display:block"></div>
</div>
<div style="position:absolute;right:60px;top:150px">{_marco_tel(CAPTURAS / 'm-hoy.png', 330)}</div>"""


PANTALLAS = [("m-hoy", "Hoy"), ("m-partidos", "Partidos"), ("m-analisis", "Análisis"),
             ("m-vivo", "En vivo"), ("m-combinar", "Combinar"), ("m-registro", "Registro")]


def pantallas_html():
    celdas = "".join(f'<div style="display:flex;flex-direction:column;align-items:center">'
                     f'{_marco_tel(CAPTURAS / f"{a}.png", 400)}'
                     f'<div class=d style="margin-top:26px;font-weight:700;font-size:64px;color:var(--tx)">{e}</div></div>'
                     for a, e in PANTALLAS)
    return (f'<div class=glow></div><div class=grid></div>'
            f'<div style="position:absolute;inset:0;display:grid;grid-template-columns:repeat(3,400px);'
            f'justify-content:center;column-gap:90px;row-gap:70px;padding-top:60px">{celdas}</div>')


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


def _foto(b, css, cuerpo, ancho, alto):
    pg = b.new_page(viewport={"width": ancho, "height": alto})
    pg.set_content(f"<html><head><meta charset=utf-8><style>{css}{BASE}</style></head><body>{cuerpo}</body></html>")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(500)
    img = Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
    pg.close()
    return img


def main():
    css = _fuentes()
    with sync_playwright() as p:
        b = p.chromium.launch()
        botones(b, css)
        _foto(b, css, BANNER, 1600, 520).save(IMG / "banner.png", optimize=True)
        # JPEG: son capturas, en PNG pesan tres veces más
        _foto(b, css, hero_html(), 1700, 930).save(IMG / "hero.jpg", quality=86, optimize=True, progressive=True)
        _foto(b, css, pantallas_html(), 1620, 2200).save(IMG / "pantallas.jpg", quality=84, optimize=True,
                                                         progressive=True)
        b.close()


if __name__ == "__main__":
    main()
