"""Dibuja la tarjeta «Aciertos en vivo» de Instrumento (SVG) con los datos
públicos de la app: /api/publico/portada, lo mismo que muestra /aciertos.

Uso: python scripts/aciertos.py SALIDA.svg
Si la app no responde, sale con error y no escribe nada: el workflow deja la
tarjeta anterior. Con menos de 20 picks medidos no muestra el % (con pocos
casos engaña), igual que la app.
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from xml.sax.saxutils import escape

URLS = [os.environ.get("URL_PORTADA") or "https://instrumentoapp.com/api/publico/portada",
        "https://app-z8g3.onrender.com/api/publico/portada"]
PICKS_MINIMOS = 20
MESES = "ene feb mar abr may jun jul ago sep oct nov dic".split()
FUENTE = "'Segoe UI',Manrope,Inter,Helvetica,Arial,sans-serif"


def traer():
    ultimo = None
    for url in URLS:
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": "perfil-wualters/1.0"})
            with urllib.request.urlopen(pedido, timeout=60) as r:
                return json.load(r)
        except Exception as e:          # el siguiente link, y si no, error
            ultimo = e
    raise SystemExit(f"No se pudo leer la portada: {ultimo}")


def corto(t, n):
    t = str(t or "")
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def svg(datos, ahora):
    a = datos.get("aciertos") or {}
    pick = a.get("pick") or {}
    n, ok, pct = pick.get("n") or 0, pick.get("ok") or 0, pick.get("pct")
    dias = a.get("dias")
    medido = pct is not None and n >= PICKS_MINIMOS
    lima = ahora - timedelta(hours=5)
    fecha = f"{lima.day} {MESES[lima.month - 1]} {lima.year}"

    partes = [f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 420" width="1200" height="420"
 font-family="{FUENTE}" role="img" aria-label="Aciertos de Instrumento">
<defs>
  <radialGradient id="g1" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1" gradientTransform="translate(120 20) scale(620)">
    <stop offset="0" stop-color="#FF5A1F" stop-opacity=".40"/><stop offset="1" stop-color="#FF5A1F" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1" gradientTransform="translate(1160 430) scale(560)">
    <stop offset="0" stop-color="#C6F432" stop-opacity=".22"/><stop offset="1" stop-color="#C6F432" stop-opacity="0"/></radialGradient>
  <linearGradient id="tx" x1="0" x2="1"><stop offset="0" stop-color="#FF5A1F"/>
    <stop offset=".55" stop-color="#FFB36B"/><stop offset="1" stop-color="#C6F432"/></linearGradient>
  <clipPath id="c"><rect width="1200" height="420" rx="26"/></clipPath>
</defs>
<g clip-path="url(#c)">
<rect width="1200" height="420" fill="#0B0F17"/><rect width="1200" height="420" fill="url(#g1)"/>
<rect width="1200" height="420" fill="url(#g2)"/>
<rect x="1" y="1" width="1198" height="418" rx="25" fill="none" stroke="#FFFFFF" stroke-opacity=".12" stroke-width="2"/>
<circle cx="62" cy="58" r="7" fill="#C6F432"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="80" y="66" font-size="22" font-weight="700" letter-spacing="4" fill="#FF8A5B">INSTRUMENTO · ACIERTOS EN VIVO</text>
<text x="1148" y="66" font-size="19" fill="#8593AD" text-anchor="end">actualizado {escape(fecha)}</text>
"""]
    if medido:
        sub = f"{ok} de {n} picks" + (f" · últimos {dias} días" if dias else "")
        partes.append(f"""<text x="54" y="220" font-size="150" font-weight="800" letter-spacing="-6" fill="url(#tx)">{pct}%</text>
<text x="58" y="268" font-size="28" font-weight="700" fill="#E6EAF2">de acierto en los picks</text>
<text x="58" y="304" font-size="22" fill="#8593AD">{escape(sub)}</text>
<rect x="58" y="330" width="420" height="12" rx="6" fill="#FFFFFF" fill-opacity=".08"/>
<rect x="58" y="330" width="{round(420 * pct / 100)}" height="12" rx="6" fill="url(#tx)"/>
""")
    else:
        partes.append(f"""<text x="58" y="200" font-size="64" font-weight="800" fill="url(#tx)">Midiendo…</text>
<text x="58" y="250" font-size="26" font-weight="700" fill="#E6EAF2">{n} picks medidos</text>
<text x="58" y="288" font-size="21" fill="#8593AD">el % aparece con {PICKS_MINIMOS}: con pocos casos engaña</text>
""")
    partes.append('<text x="58" y="394" font-size="18" fill="#5E6A82">Guardado antes de cada partido · incluye los que fallaron · instrumentoapp.com/aciertos</text>\n')

    # los últimos partidos con pick, con ✓ / ✗
    recientes = [r for r in datos.get("recientes") or [] if r.get("pick")][:4]
    if recientes:
        partes.append('<text x="560" y="114" font-size="18" font-weight="700" letter-spacing="3" fill="#8593AD">ÚLTIMOS PICKS</text>\n')
    for i, r in enumerate(recientes):
        y = 132 + i * 56
        bien = r["pick"].get("ok")
        color, signo = ("#C6F432", "✓") if bien else ("#FF5F57", "✗")
        partido = f"{corto(r.get('local'), 18)} {r.get('marcador', '')} {corto(r.get('visitante'), 18)}"
        partes.append(f"""<rect x="560" y="{y}" width="588" height="48" rx="12" fill="#FFFFFF" fill-opacity=".045"/>
<circle cx="588" cy="{y + 24}" r="14" fill="{color}" fill-opacity=".16"/>
<text x="588" y="{y + 31}" font-size="20" font-weight="800" fill="{color}" text-anchor="middle">{signo}</text>
<text x="616" y="{y + 21}" font-size="17" font-weight="700" fill="#E6EAF2">{escape(partido)}</text>
<text x="616" y="{y + 40}" font-size="15" fill="#B9C2D6">{escape(corto(r['pick'].get('texto'), 48))}</text>
""")
    partes.append("</g></svg>\n")
    return "".join(partes)


if __name__ == "__main__":
    salida = sys.argv[1] if len(sys.argv) > 1 else "aciertos.svg"
    contenido = svg(traer(), datetime.now(timezone.utc))
    os.makedirs(os.path.dirname(salida) or ".", exist_ok=True)
    with open(salida, "w", encoding="utf-8") as f:
        f.write(contenido)
    print("Listo:", salida)
