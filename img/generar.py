"""Genera las imágenes del perfil (todas guardadas en el repo, para que carguen
siempre, también en la app de GitHub del celular):

  img/banner.gif   encabezado con el texto que se escribe solo
  img/codigo.png   tarjeta de código «class WualterS»
  img/umapyoi.png  tarjeta del proyecto Umapyoi AutoReroll
  img/stack.png    tecnologías por grupo
  img/btn-*.png    botones (en vez de badges externos, que a veces no cargan)

Uso: pip install playwright pillow && python img/generar.py
"""

import base64
import io
import pathlib
import urllib.request

from PIL import Image
from playwright.sync_api import sync_playwright

IMG = pathlib.Path(__file__).resolve().parent
FUENTES = {
    "Manrope": "https://fonts.gstatic.com/s/manrope/v20/xn7gYHE41ni1AdIRggexSg.woff2",
    "Mono": "https://fonts.gstatic.com/s/jetbrainsmono/v24/tDbY2o-flEEny0FZhsfKu5WU4zr3E_BX0PnT8RD8-qxjPQ.ttf",
}
FRASES = [
    "⚽ Modelos estadísticos de fútbol",
    "🐍 Python + Flask en producción",
    "📊 Datos que se validan contra el mercado",
    "🔁 Un modelo que se mejora solo",
    "🤖 Automatización y bots",
]


def _fuentes():
    css = ""
    for nombre, url in FUENTES.items():
        datos = base64.b64encode(urllib.request.urlopen(url).read()).decode()
        fmt = "woff2" if url.endswith("woff2") else "truetype"
        css += (f"@font-face{{font-family:{nombre};font-weight:200 800;"
                f"src:url(data:font/{fmt};base64,{datos}) format('{fmt}')}}\n")
    return css


BASE = """
*{margin:0;box-sizing:border-box}
body{font-family:Manrope;background:#0B0F17;color:#E6EAF2;overflow:hidden;position:relative}
.g1{position:absolute;width:900px;height:900px;border-radius:50%;left:-260px;top:-430px;
    background:radial-gradient(circle,rgba(255,90,31,.42),transparent 65%)}
.g2{position:absolute;width:900px;height:900px;border-radius:50%;right:-300px;bottom:-540px;
    background:radial-gradient(circle,rgba(198,244,50,.26),transparent 65%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:40px 40px}
.grad{background:linear-gradient(90deg,#FF5A1F,#FFB36B 55%,#C6F432);-webkit-background-clip:text;color:transparent}
.chip{font-weight:700;padding:10px 20px;border-radius:999px;background:rgba(255,255,255,.06);
      border:1.5px solid rgba(255,255,255,.14)}
"""

BANNER = """<div class=g1></div><div class=g2></div><div class=grid></div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center">
  <div style="font-size:26px;font-weight:600;color:#FF8A5B;letter-spacing:6px">HOLA, SOY</div>
  <div class=grad style="font-size:136px;font-weight:800;letter-spacing:-5px;line-height:1.05">WualterS</div>
  <div style="font-size:30px;font-weight:600;margin-top:4px">Desarrollador Python · Cusco, Perú 🇵🇪</div>
  <div style="margin-top:30px;height:56px;display:flex;align-items:center;font-family:Mono;font-size:34px;color:#fff">
    <span id=t></span><span style="display:inline-block;width:16px;height:40px;background:#C6F432;margin-left:6px"></span>
  </div>
</div>"""

CODIGO = """<div class=g1 style="left:-420px;top:-560px"></div><div class=grid></div>
<div style="position:absolute;inset:34px;border-radius:22px;background:rgba(15,20,32,.92);
            border:1.5px solid rgba(255,255,255,.12);box-shadow:0 20px 60px rgba(0,0,0,.5);overflow:hidden">
  <div style="height:54px;display:flex;align-items:center;gap:10px;padding:0 22px;background:rgba(255,255,255,.04);
              border-bottom:1.5px solid rgba(255,255,255,.08)">
    <i style="width:15px;height:15px;border-radius:50%;background:#FF5F57"></i>
    <i style="width:15px;height:15px;border-radius:50%;background:#FEBC2E"></i>
    <i style="width:15px;height:15px;border-radius:50%;background:#28C840"></i>
    <span style="margin-left:14px;font-family:Mono;font-size:20px;color:#8593AD">wualters.py</span>
  </div>
  <pre style="font-family:Mono;font-size:25px;line-height:1.62;padding:24px 34px;color:#E6EAF2">\
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
.k{color:#FF8A5B}.c{color:#C6F432}.f{color:#7FD4FF}.a{color:#E6EAF2}s{color:#FFD08A}u{color:#5E6A82}</style>"""

UMAPYOI = """<div class=g1 style="background:radial-gradient(circle,rgba(124,92,255,.42),transparent 65%)"></div>
<div class=g2 style="background:radial-gradient(circle,rgba(88,101,242,.30),transparent 65%)"></div><div class=grid></div>
<div style="position:absolute;inset:0;display:flex;align-items:center;gap:56px;padding:0 70px">
  <div style="font-size:150px;filter:drop-shadow(0 10px 30px rgba(124,92,255,.5))">🏇</div>
  <div>
    <div style="font-size:22px;font-weight:700;letter-spacing:5px;color:#A89BFF">AUTOMATIZACIÓN · VISIÓN POR COMPUTADORA</div>
    <div style="font-size:72px;font-weight:800;letter-spacing:-2px;line-height:1.1;margin-top:6px">Umapyoi AutoReroll</div>
    <div style="font-size:28px;font-weight:500;color:#B9C2D6;margin-top:12px;max-width:900px;line-height:1.4">
      Bot de escritorio para Umamusume Global: hace el reroll solo y detecta las cartas SSR objetivo.</div>
    <div style="display:flex;gap:12px;margin-top:26px;font-size:22px">
      <span class=chip>OpenCV</span><span class=chip>Tesseract OCR</span><span class=chip>Tkinter</span>
      <span class=chip>Webhooks de Discord</span><span class=chip>ES / EN</span></div>
  </div>
</div>"""

# nombre, texto, fondo, color del texto
BOTONES = [
    ("proyectos", "🧭 Proyectos", "#FF5A1F", "#0B0F17"),
    ("stack", "🛠️ Stack", "#232B3D", "#E6EAF2"),
    ("contacto", "📬 Contacto", "#C6F432", "#0B0F17"),
    ("english", "🇺🇸 English", "#232B3D", "#E6EAF2"),
    ("probar", "▶ Probar la app", "#FF5A1F", "#0B0F17"),
    ("aciertos", "✅ Aciertos públicos", "#C6F432", "#0B0F17"),
    ("correo", "✉️ wualters.dev@gmail.com", "#FF5A1F", "#0B0F17"),
    ("web", "🌐 instrumentoapp.com", "#232B3D", "#E6EAF2"),
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
        f'<div style="width:250px;font-size:19px;font-weight:700;letter-spacing:3px;color:#FF8A5B">{t}</div>'
        f'<div style="display:flex;flex-wrap:wrap;gap:10px;font-size:21px">'
        + "".join(f"<span class=chip>{c}</span>" for c in chips) + "</div></div>"
        for t, chips in GRUPOS)
    return (f'<div class=g1 style="left:-420px;top:-560px"></div><div class=g2></div><div class=grid></div>'
            f'<div style="position:absolute;inset:0;padding:40px 60px">{filas}</div>')


def botones(b, css):
    pg = b.new_page(viewport={"width": 900, "height": 120}, device_scale_factor=2)
    for nombre, texto, fondo, color in BOTONES:
        pg.set_content(f"<html><head><meta charset=utf-8><style>{css}*{{margin:0}}body{{background:transparent}}"
                       f"b{{display:inline-block;font:800 19px Manrope;letter-spacing:1px;padding:13px 24px;"
                       f"border-radius:999px;background:{fondo};color:{color}}}</style></head>"
                       f"<body><b id=b>{texto}</b></body></html>")
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(150)
        pg.locator("#b").screenshot(path=str(IMG / f"btn-{nombre}.png"), omit_background=True)
    pg.close()


def _pagina(b, css, cuerpo, ancho, alto):
    pg = b.new_page(viewport={"width": ancho, "height": alto})
    pg.set_content(f"<html><head><meta charset=utf-8><style>{css}{BASE}</style></head><body>{cuerpo}</body></html>")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(300)
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
        poner(frase, 1800)
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
                                            ("stack", stack_html(), 1280, 410)):
            pg = _pagina(b, css, cuerpo, ancho, alto)
            pg.screenshot(path=str(IMG / f"{nombre}.png"))
            pg.close()
        b.close()


if __name__ == "__main__":
    main()
