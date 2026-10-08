# Genera img/banner.png: python img/generar_banner.py img/banner.png (requiere playwright).
import base64, urllib.request, sys
from playwright.sync_api import sync_playwright
f = base64.b64encode(urllib.request.urlopen("https://fonts.gstatic.com/s/manrope/v20/xn7gYHE41ni1AdIRggexSg.woff2").read()).decode()
html = """<html><head><style>
@font-face{font-family:Manrope;font-weight:200 800;src:url(data:font/woff2;base64,%s) format('woff2')}
*{margin:0;box-sizing:border-box}
body{width:1600px;height:520px;font-family:Manrope;background:#0B0F17;overflow:hidden;position:relative;color:#fff}
.g1{position:absolute;width:900px;height:900px;border-radius:50%%;left:-250px;top:-420px;background:radial-gradient(circle,rgba(255,90,31,.45),transparent 65%%)}
.g2{position:absolute;width:900px;height:900px;border-radius:50%%;right:-300px;bottom:-520px;background:radial-gradient(circle,rgba(198,244,50,.28),transparent 65%%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:40px 40px}
.c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.hola{font-size:30px;font-weight:600;color:#FF8A5B;letter-spacing:6px;text-transform:uppercase}
h1{font-size:150px;font-weight:800;letter-spacing:-5px;line-height:1.05;background:linear-gradient(90deg,#FF5A1F,#FFB36B 55%%,#C6F432);-webkit-background-clip:text;color:transparent}
.sub{font-size:36px;font-weight:600;color:#E6EAF2;margin-top:6px}
.chips{display:flex;gap:16px;margin-top:34px}
.chip{font-size:24px;font-weight:700;padding:12px 24px;border-radius:999px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.14);color:#E6EAF2}
</style></head><body><div class=g1></div><div class=g2></div><div class=grid></div>
<div class=c><div class=hola>Hola, soy</div><h1>WualterS</h1>
<div class=sub>Desarrollador Python · Cusco, Perú 🇵🇪</div>
<div class=chips><span class=chip>⚽ Modelos de fútbol</span><span class=chip>🐍 Python + Flask en producción</span><span class=chip>📊 Validado contra el mercado</span><span class=chip>🤖 Bots</span></div></div>
</body></html>""" % f
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1600,"height":520})
    pg.set_content(html); pg.wait_for_timeout(500)
    pg.evaluate("document.fonts.ready"); pg.screenshot(path=sys.argv[1]); b.close()
