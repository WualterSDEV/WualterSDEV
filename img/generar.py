"""Genera las imágenes del perfil (todas guardadas en el repo, para que carguen
siempre, también en la app de GitHub del celular). Colores y letras del estilo
«Marcador» de Instrumento: fondo casi negro, lima solo en lo importante y
títulos en Barlow Condensed.

  img/banner.gif     encabezado con el texto que se escribe solo
  img/codigo.png     tarjeta de código «class WualterS»
  img/umapyoi.png    tarjeta del proyecto Umapyoi AutoReroll
  img/stack.png      tecnologías por grupo
  img/btn-*.png      botones (en vez de badges externos, que a veces no cargan)
  img/hero.png       Instrumento en PC y celular
  img/pantallas.png  seis pantallas de la app

Las capturas de la app salen de docs/pantallas/ del repo de Instrumento
(regenerarlas allá primero). Uso:

  pip install playwright pillow
  APP=../APP python img/generar.py
"""

import base64
import io
import os
import pathlib
import urllib.request

from PIL import Image
from playwright.sync_api import sync_playwright

IMG = pathlib.Path(__file__).resolve().parent
APP = pathlib.Path(os.environ.get("APP") or IMG.parent.parent / "APP")
FUENTES = [
    ("Manrope", "200 800", "https://fonts.gstatic.com/s/manrope/v20/xn7gYHE41ni1AdIRggexSg.woff2"),
    ("Mono", "200 800", "https://fonts.gstatic.com/s/jetbrainsmono/v24/tDbY2o-flEEny0FZhsfKu5WU4zr3E_BX0PnT8RD8-qxjPQ.ttf"),
    ("Barlow", "700", "https://fonts.gstatic.com/s/barlowcondensed/v13/HTxwL3I-JCGChYJ8VI-L6OO_au7B46r2_3E.ttf"),
    ("Barlow", "800", "https://fonts.gstatic.com/s/barlowcondensed/v13/HTxwL3I-JCGChYJ8VI-L6OO_au7B47b1_3E.ttf"),
]
FRASES = [
    "⚽ Modelos estadísticos de fútbol",
    "🐍 Python + Flask en producción",
    "📊 Validado contra el mercado",
    "🔁 Un modelo que se mejora solo",
    "🤖 Automatización y bots",
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
    tipo = {".svg": "svg+xml", ".png": "png"}.get(ruta.suffix, "jpeg")
    return f"data:image/{tipo};base64," + base64.b64encode(ruta.read_bytes()).decode()


# los mismos colores de static/estilo.css de Instrumento
BASE = """
:root{--bg:#0B0D0C;--card:#131614;--soft:#1A1E1B;--line:#242925;--line2:#303631;
      --tx:#ECEFEA;--tx2:#C4C9C3;--mut:#979E98;--mut2:#6D746E;--hi:#C6F432;--onhi:#0B1400;--acc:#BFE35A}
*{margin:0;box-sizing:border-box}
body{font-family:Manrope;background:var(--bg);color:var(--tx);overflow:hidden;position:relative}
.d{font-family:Barlow;text-transform:uppercase}
.glow{position:absolute;width:1000px;height:1000px;border-radius:50%;right:-380px;top:-520px;
      background:radial-gradient(circle,rgba(198,244,50,.16),transparent 62%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.028) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.028) 1px,transparent 1px);background-size:44px 44px;
    -webkit-mask-image:linear-gradient(180deg,#000,transparent 92%)}
.chip{font-weight:700;padding:10px 20px;border-radius:999px;background:var(--card);border:1.5px solid var(--line2)}
.chip.hi{background:rgba(198,244,50,.10);border-color:rgba(198,244,50,.45);color:var(--hi)}
"""

BANNER = """<div class=glow></div><div class=grid></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">
  <div style="display:flex;align-items:center;gap:12px;font-size:22px;font-weight:700;color:var(--mut);letter-spacing:5px">
    <i style="width:10px;height:10px;border-radius:50%;background:var(--hi)"></i>HOLA, SOY</div>
  <div class=d style="font-size:168px;font-weight:800;letter-spacing:2px;line-height:.95;margin-top:10px">
    Wualter<span style="color:var(--hi)">S</span></div>
  <div style="font-size:28px;font-weight:600;color:var(--tx2);margin-top:12px">Desarrollador Python · Cusco, Perú 🇵🇪</div>
  <div style="margin-top:28px;height:58px;display:flex;align-items:center;padding:0 24px;border-radius:14px;
              background:var(--card);border:1.5px solid var(--line);font-family:Mono;font-size:28px;color:var(--tx)">
    <span style="color:var(--hi);margin-right:14px">›</span><span id=t></span>
    <span style="display:inline-block;width:13px;height:32px;background:var(--hi);margin-left:6px"></span>
  </div>
</div>"""

CODIGO = """<div class=glow style="right:auto;left:-520px"></div><div class=grid></div>
<div style="position:absolute;inset:34px;border-radius:22px;background:var(--card);
            border:1.5px solid var(--line2);box-shadow:0 20px 60px rgba(0,0,0,.5);overflow:hidden">
  <div style="height:54px;display:flex;align-items:center;gap:10px;padding:0 22px;background:var(--soft);
              border-bottom:1.5px solid var(--line)">
    <i style="width:14px;height:14px;border-radius:50%;background:#3A403B"></i>
    <i style="width:14px;height:14px;border-radius:50%;background:#3A403B"></i>
    <i style="width:14px;height:14px;border-radius:50%;background:var(--hi)"></i>
    <span style="margin-left:14px;font-family:Mono;font-size:20px;color:var(--mut)">wualters.py</span>
  </div>
  <pre style="font-family:Mono;font-size:25px;line-height:1.62;padding:24px 34px;color:var(--tx)">\
<b class=k>class</b> <b class=c>WualterS</b>(<b class=c>Desarrollador</b>):
    <i class=a>ubicacion</i>    = <s>"Cusco, Perú 🇵🇪"</s>
    <i class=a>stack</i>        = [<s>"Python"</s>, <s>"Flask"</s>, <s>"pandas"</s>, <s>"SciPy"</s>, <s>"Postgres"</s>]
    <i class=a>construyendo</i> = <s>"Instrumento ⚽ → instrumentoapp.com"</s>
    <i class=a>aprendiendo</i>  = [<s>"xG"</s>, <s>"CLV"</s>, <s>"bajas"</s>, <s>"calibración por liga"</s>]
    <i class=a>contacto</i>     = <s>"wualters.dev@gmail.com"</s>

    <b class=k>def</b> <b class=f>filosofia</b>(<i class=a>self</i>):
        <b class=k>return</b> <s>"Medir antes de creer."</s>  <u># sin humo</u></pre>
</div>
<style>pre b,pre i,pre s,pre u{font-style:normal;text-decoration:none;font-weight:500}
.k{color:var(--hi)}.c{color:#FFFFFF;font-weight:700!important}.f{color:#8E9CF0}.a{color:var(--tx2)}
s{color:#E8D9A8}u{color:var(--mut2)}</style>"""

UMAPYOI = """<div class=glow style="background:radial-gradient(circle,rgba(142,156,240,.20),transparent 62%)"></div>
<div class=grid></div>
<div style="position:absolute;inset:0;display:flex;align-items:center;gap:56px;padding:0 70px">
  <div style="font-size:140px;width:220px;height:220px;border-radius:44px;display:grid;place-items:center;
              background:var(--card);border:1.5px solid var(--line2)">🏇</div>
  <div>
    <div style="font-size:21px;font-weight:700;letter-spacing:5px;color:#8E9CF0">AUTOMATIZACIÓN · VISIÓN POR COMPUTADORA</div>
    <div class=d style="font-size:96px;font-weight:800;line-height:1;margin-top:8px">Umapyoi AutoReroll</div>
    <div style="font-size:27px;font-weight:500;color:var(--tx2);margin-top:12px;max-width:960px;line-height:1.4">
      Bot de escritorio para Umamusume Global: hace el reroll solo y detecta las cartas SSR objetivo.</div>
    <div style="display:flex;gap:12px;margin-top:26px;font-size:21px">
      <span class=chip>OpenCV</span><span class=chip>Tesseract OCR</span><span class=chip>Tkinter</span>
      <span class=chip>Webhooks de Discord</span><span class=chip>ES / EN</span></div>
  </div>
</div>"""

# nombre, texto, principal (lima) o no
BOTONES = [
    ("proyectos", "🧭 Proyectos", True),
    ("stack", "🛠️ Stack", False),
    ("contacto", "📬 Contacto", False),
    ("english", "🇺🇸 English", False),
    ("probar", "▶ Probar la app gratis", True),
    ("aciertos", "✅ Aciertos públicos", False),
    ("correo", "✉️ wualters.dev@gmail.com", True),
    ("web", "🌐 instrumentoapp.com", False),
]

GRUPOS = [
    ("LENGUAJES", ["🐍 Python", "JavaScript", "HTML / CSS", "SQL"]),
    ("BACKEND Y DATOS", ["Flask", "PostgreSQL (Neon)", "SQLite", "pandas", "NumPy", "SciPy"]),
    ("MODELOS", ["Dixon-Coles", "Binomial Negativa", "Cópula gaussiana", "Kelly fraccionado"]),
    ("AUTOMATIZACIÓN", ["OpenCV", "Tesseract OCR", "Selenium", "Discord"]),
    ("DEPLOY Y CALIDAD", ["Render", "GitHub Actions", "pytest", "Playwright", "ruff", "PWA"]),
]


def stack_html():
    filas = "".join(
        f'<div style="display:flex;align-items:center;gap:22px;margin:14px 0">'
        f'<div class=d style="width:250px;font-size:27px;font-weight:700;letter-spacing:1px;color:var(--hi)">{t}</div>'
        f'<div style="display:flex;flex-wrap:wrap;gap:10px;font-size:21px">'
        + "".join(f"<span class=chip>{c}</span>" for c in chips) + "</div></div>"
        for t, chips in GRUPOS)
    return (f'<div class=glow></div><div class=grid></div>'
            f'<div style="position:absolute;inset:0;padding:40px 60px">{filas}</div>')


def _tel(img, ancho=300, extra=""):
    return (f'<div style="width:{ancho}px;height:{ancho * 2.06:.0f}px;border-radius:{ancho * .15:.0f}px;background:#000;'
            f'padding:10px;box-shadow:0 30px 80px rgba(0,0,0,.6),0 0 0 2px var(--line2);flex:none;{extra}">'
            f'<div style="width:100%;height:100%;border-radius:{ancho * .115:.0f}px;overflow:hidden;background:var(--bg)">'
            f'<img src="{_uri(img)}" style="width:100%;display:block"></div></div>')


def hero_html():
    p = APP / "docs" / "pantallas"
    return f"""<div class=glow style="right:-200px;top:-300px"></div><div class=grid></div>
<div style="position:absolute;left:90px;top:120px;width:560px">
  <img src="{_uri(APP / 'static' / 'favicon.svg')}" style="width:96px;height:96px;border-radius:24px">
  <div class=d style="font-size:104px;font-weight:800;line-height:.95;margin-top:28px">Instrumento</div>
  <div style="font-size:28px;font-weight:800;color:var(--hi);margin-top:12px">Pronósticos de fútbol con un modelo real</div>
  <div style="font-size:22px;line-height:1.5;color:var(--tx2);margin-top:18px;font-weight:600">
    Probabilidades calculadas con los datos de cada equipo y medidas contra lo que pasó. Gratis, en PC y en el celular.</div>
  <div style="display:flex;gap:12px;margin-top:30px;flex-wrap:wrap;font-size:19px">
    <span class="chip hi">🆓 Gratis</span><span class=chip>💻 PC</span><span class=chip>📱 Android / iPhone</span>
    <span class=chip>🔁 Se mejora solo</span></div>
</div>
<div style="position:absolute;left:720px;top:90px;width:820px;border-radius:18px;background:#000;padding:10px;
            box-shadow:0 30px 80px rgba(0,0,0,.6),0 0 0 2px var(--line2)">
  <div style="border-radius:10px;overflow:hidden;height:512px"><img src="{_uri(p / '60-pc-partidos.jpg')}" style="width:100%;display:block"></div>
</div>
<div style="position:absolute;left:1110px;top:250px">{_tel(p / '05-hoy.jpg', 250)}</div>"""


PANTALLAS = [("05-hoy", "Hoy"), ("10-partidos", "Partidos"), ("12-analisis", "Análisis"),
             ("21-en-vivo-detalle", "En vivo"), ("31-combinar-boleto", "Combinar"), ("40-registro-picks", "Registro")]


def pantallas_html():
    fila = "".join(f'<div>{_tel(APP / "docs" / "pantallas" / f"{a}.jpg")}'
                   f'<div class=d style="margin-top:18px;text-align:center;font-weight:700;font-size:34px;color:var(--tx2)">'
                   f'{e}</div></div>' for a, e in PANTALLAS)
    return (f'<div class=glow></div><div class=grid></div>'
            f'<div style="position:absolute;inset:0;display:flex;gap:56px;justify-content:center;padding-top:50px">{fila}</div>')


def botones(b, css):
    pg = b.new_page(viewport={"width": 900, "height": 120}, device_scale_factor=2)
    for nombre, texto, principal in BOTONES:
        estilo = ("background:#C6F432;color:#0B1400" if principal else
                  "background:#131614;color:#ECEFEA;box-shadow:inset 0 0 0 2px #303631")
        pg.set_content(f"<html><head><meta charset=utf-8><style>{css}*{{margin:0}}body{{background:transparent}}"
                       f"b{{display:inline-block;font:800 19px Manrope;letter-spacing:.5px;padding:13px 24px;"
                       f"border-radius:999px;{estilo}}}</style></head>"
                       f"<body><b id=b>{texto}</b></body></html>")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(150)
        pg.locator("#b").screenshot(path=str(IMG / f"btn-{nombre}.png"), omit_background=True)
    pg.close()


def _pagina(b, css, cuerpo, ancho, alto):
    pg = b.new_page(viewport={"width": ancho, "height": alto})
    pg.set_content(f"<html><head><meta charset=utf-8><style>{css}{BASE}</style></head><body>{cuerpo}</body></html>")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(400)
    return pg


def _foto(pg):
    return Image.open(io.BytesIO(pg.screenshot())).convert("RGB")


def banner(b, css):
    pg = _pagina(b, css, BANNER, 1280, 420)
    cuadros = []                                   # (imagen, milisegundos)

    def poner(texto, ms):
        pg.evaluate("t => document.getElementById('t').textContent = t", texto)
        cuadros.append((_foto(pg), ms))

    for frase in FRASES:
        letras = list(frase)
        for i in range(2, len(letras) + 1, 2):
            poner("".join(letras[:i]), 55)
        poner(frase, 2200)
        for i in range(len(letras) - 4, 0, -5):
            poner("".join(letras[:i]), 35)
        poner("", 250)
    pg.close()
    paleta = cuadros[len(FRASES[0]) // 2][0].quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    imgs = [c.quantize(palette=paleta, dither=Image.Dither.NONE) for c, _ in cuadros]
    imgs[0].save(IMG / "banner.gif", save_all=True, append_images=imgs[1:],
                 duration=[ms for _, ms in cuadros], loop=0, optimize=True, disposal=1)


def main():
    css = _fuentes()
    with sync_playwright() as p:
        b = p.chromium.launch()
        banner(b, css)
        botones(b, css)
        for nombre, cuerpo, ancho, alto in (("codigo", CODIGO, 1280, 540), ("umapyoi", UMAPYOI, 1600, 420),
                                            ("stack", stack_html(), 1280, 410), ("hero", hero_html(), 1600, 800),
                                            ("pantallas", pantallas_html(), 2160, 760)):
            pg = _pagina(b, css, cuerpo, ancho, alto)
            pg.screenshot(path=str(IMG / f"{nombre}.png"))
            pg.close()
        b.close()


if __name__ == "__main__":
    main()
