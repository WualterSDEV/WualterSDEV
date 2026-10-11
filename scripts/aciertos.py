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

    # 1200 x 520 con letra grande: en el celular la tarjeta se ve a ~30% de su tamaño
    partes = [f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 520" width="1200" height="520"
 font-family="{FUENTE}" role="img" aria-label="Aciertos de Instrumento">
<defs>
  <radialGradient id="g1" gradientUnits="userSpaceOnUse" cx="0" cy="0" r="1" gradientTransform="translate(1150 0) scale(700)">
    <stop offset="0" stop-color="#C6F432" stop-opacity=".14"/><stop offset="1" stop-color="#C6F432" stop-opacity="0"/></radialGradient>
  <clipPath id="c"><rect width="1200" height="520" rx="28"/></clipPath>
</defs>
<g clip-path="url(#c)">
<rect width="1200" height="520" fill="#0A0B14"/><rect width="1200" height="520" fill="url(#g1)"/>
<rect x="1" y="1" width="1198" height="518" rx="27" fill="none" stroke="#323759" stroke-width="2"/>
<circle cx="64" cy="66" r="8" fill="#C6F432"/>
<text x="86" y="76" font-size="28" font-weight="700" letter-spacing="3" fill="#EEF0FF">ACIERTOS EN VIVO</text>
<text x="1140" y="76" font-size="24" fill="#8F95BA" text-anchor="end">{escape(fecha)}</text>
"""]
    if medido:
        sub = f"{ok} de {n} picks" + (f" · {dias} días" if dias else "")
        partes.append(f"""<text x="52" y="260" font-size="190" font-weight="800" letter-spacing="-8" fill="#C6F432">{pct}%</text>
<text x="58" y="320" font-size="36" font-weight="700" fill="#EEF0FF">de acierto en los picks</text>
<text x="58" y="364" font-size="28" fill="#8F95BA">{escape(sub)}</text>
<rect x="58" y="392" width="440" height="14" rx="7" fill="#FFFFFF" fill-opacity=".08"/>
<rect x="58" y="392" width="{round(440 * pct / 100)}" height="14" rx="7" fill="#C6F432"/>
""")
    else:
        partes.append(f"""<text x="58" y="230" font-size="84" font-weight="800" fill="#C6F432">Midiendo…</text>
<text x="58" y="290" font-size="34" font-weight="700" fill="#EEF0FF">{n} picks medidos</text>
<text x="58" y="336" font-size="26" fill="#8F95BA">el % aparece con {PICKS_MINIMOS}: con pocos casos engaña</text>
""")
    partes.append('<text x="58" y="476" font-size="23" fill="#8F95BA">Cada pick se guarda antes del partido · cuentan también los que fallaron</text>\n')

    # los últimos partidos con pick, con ✓ / ✗
    recientes = [r for r in datos.get("recientes") or [] if r.get("pick")][:3]
    for i, r in enumerate(recientes):
        y = 120 + i * 104
        bien = r["pick"].get("ok")
        color, signo = ("#C6F432", "✓") if bien else ("#FF8076", "✗")
        partido = f"{corto(r.get('local'), 14)} {r.get('marcador', '')} {corto(r.get('visitante'), 14)}"
        partes.append(f"""<rect x="560" y="{y}" width="580" height="90" rx="16" fill="#121427" stroke="#242845" stroke-width="2"/>
<circle cx="604" cy="{y + 45}" r="22" fill="{color}" fill-opacity=".16"/>
<text x="604" y="{y + 55}" font-size="28" font-weight="800" fill="{color}" text-anchor="middle">{signo}</text>
<text x="642" y="{y + 40}" font-size="26" font-weight="700" fill="#EEF0FF">{escape(partido)}</text>
<text x="642" y="{y + 72}" font-size="22" fill="#C4C8E4">{escape(corto(r['pick'].get('texto'), 34))}</text>
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
