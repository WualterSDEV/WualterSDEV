"""Capturas de Instrumento para el perfil, en alta resolución (2x) y con una
cuenta de usuario normal. Es una prueba de Playwright del repo de la app: usa
su Simulador (datos de ejemplo, no de producción).

Uso, desde el repo de la app:
    cp ../WualterSDEV/scripts/capturas_app.py tests/ui/test_perfil_tmp.py
    CAPTURAS=/ruta/salida python -m pytest -q -p no:logging tests/ui/test_perfil_tmp.py
    rm tests/ui/test_perfil_tmp.py
Después: CAPTURAS=/ruta/salida python img/generar.py (en este repo).
"""
import os

from simulacion import MOVIL, PC
from test_capturas_docs import COMBI, VIVO_DET, _picks, _ruta_json, _servidor_real
from test_hoy import _con_picks
from test_pantallas import crear_usuario, en_app, entrar, ir_a

DIR = os.environ.get("CAPTURAS", "capturas")


def foto(p, nombre):
    p.wait_for_timeout(500)
    p.evaluate("document.querySelectorAll('.consejo, .toast, #toast')"
               ".forEach(e => e.style.setProperty('display', 'none', 'important'))")
    os.makedirs(DIR, exist_ok=True)
    p.screenshot(path=os.path.join(DIR, nombre + ".png"))


def test_perfil(abrir, simulador, navegador, monkeypatch):
    original = navegador.new_context
    monkeypatch.setattr(navegador, "new_context", lambda **kw: original(device_scale_factor=2, **kw))
    crear_usuario("lucia")
    _picks("lucia")
    _con_picks(simulador)

    h = abrir(MOVIL, inicio="hoy")
    entrar(h, "lucia")
    h.wait_for_selector(".hoy-pick")
    foto(h, "m-hoy")

    p = abrir(MOVIL)
    _servidor_real(p, simulador)
    entrar(p, "lucia")
    en_app(p)
    foto(p, "m-partidos")
    p.locator("[data-partido=p1]").first.click()
    p.wait_for_selector(".sugerida-total")
    foto(p, "m-analisis")
    simulador.partidos[0]["vivo"]["fixture_id"] = 77
    simulador.vivo = [{"id": "77", "minuto": 22, "liga": "Liga 1", "local": "Alianza Lima",
                       "visitante": "Universitario", "marcador": "1 — 1", "goles_local": 1,
                       "goles_visitante": 1, "logo_local": None, "logo_visitante": None}]
    _ruta_json(p, "**/api/vivo/77**", VIVO_DET)
    ir_a(p, "vivo")
    p.wait_for_selector("[data-vivo]")
    p.locator("[data-vivo]").first.click()
    p.wait_for_selector(".presion-svg, .vivo-predicho")
    foto(p, "m-vivo")

    c = abrir(MOVIL)
    _servidor_real(c, simulador)
    entrar(c, "lucia")
    en_app(c)
    c.evaluate(COMBI)
    ir_a(c, "combinar")
    c.wait_for_selector(".combi-mejor")
    foto(c, "m-combinar")
    ir_a(c, "registro")
    c.wait_for_selector(".reg-pick")
    foto(c, "m-registro")

    a = abrir(PC)
    _servidor_real(a, simulador)
    entrar(a, "lucia")
    en_app(a)
    a.locator("[data-partido=p1]").first.click()
    a.wait_for_selector(".sugerida-total")
    foto(a, "pc-partidos")
