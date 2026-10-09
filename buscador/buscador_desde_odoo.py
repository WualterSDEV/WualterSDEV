"""Genera un buscador de recetas a partir de una exportación de Odoo (listas de materiales).

Uso:
  python buscador_desde_odoo.py MAESTRO_RECETAS_VALLE.xlsx "Valle" [salida.html]

Las cantidades en KILOS/LITROS se pasan a GRAMOS/MILILITROS. El Excel que descarga el buscador
sale en el mismo formato de Odoo.
Requiere: pip install openpyxl
"""
import sys, os, re, json, unicodedata, openpyxl
HERE = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) < 3: sys.exit(__doc__)
SRC, SEDE = sys.argv[1], sys.argv[2]
OUT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, '..', f'Buscador_Recetas_{SEDE.upper()}.html')

def key(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().upper()
    return ' '.join(re.sub(r'[^A-Z0-9]', ' ', s).split())
def a_gramos(cant, unidad):
    u = (unidad or '').strip().upper()
    if u in ('KILOS', 'KILO', 'KG') and isinstance(cant, (int, float)): return round(cant * 1000, 4), 'GRAMOS'
    if u in ('LITROS', 'LITRO', 'LT') and isinstance(cant, (int, float)): return round(cant * 1000, 4), 'MILILITROS'
    return cant, unidad
def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None

POSTRE = re.compile(r'BROWN|CAKE|CHEESCAKE|CHEESECAKE|TORTA|PIE |ALFAJOR|GUARGUERO|FLAN|MAZAMORRA|TRES LECHES|PIONONO|BUDIN|'
                    r'VOLTEADA|SUSPIRO|PANNA|TARTA|HELADO|POSTRE|KEKE|MUFFIN|PICARON|GALLETA|ARROZ CON LECHE|MOUSSE|TIRAMISU|'
                    r'CREPE|PUDIN|GELATINA|ENCANELADO|CHOCOTEJA|COCADA|TURRON|BESO DE MOZA|SUSPIRITO|MANJAR|FRUTAS DE ESTACION')
def categoria(n):
    k = key(n)
    if k.startswith('RB '): return 'Receta base'
    if 'BOX LUNCH' in k: return 'Box Lunch'
    if 'MENU' in k.split(): return 'Menú'
    if 'BUFFET' in k or 'PAX' in k: return 'Buffet'
    return 'Otros'

recs, cur = [], None
for r in openpyxl.load_workbook(SRC, read_only=True).active.iter_rows(min_row=2, values_only=True):
    if r[0] or r[1]:
        cur = dict(oid=r[0], n=str(r[1]).strip(), q=num(r[3]), it=[]); recs.append(cur)
    if cur and r[6]:
        cant, u = a_gramos(r[7], r[4])
        cur['it'].append([str(r[6]).strip(), u, cant, r[5]])
byname = {}
for i, rc in enumerate(recs): byname.setdefault(key(rc['n']), 'O%d' % i)
out = []
for i, rc in enumerate(recs):
    items = []
    for nombre, u, cant, ref in rc['it']:
        sub = byname.get(key(nombre))
        if sub == 'O%d' % i: sub = None
        items.append([nombre, 'Receta' if sub or key(nombre).startswith('RB ') else 'Producto', cant, u, None, None, sub, ref])
    q = rc['q'] if rc['q'] is not None else 1
    q = int(q) if q == int(q) else q
    cat = categoria(rc['n'])
    out.append(dict(id='O%d' % i, cod=rc['oid'] or '', n=rc['n'], t='Base' if cat == 'Receta base' else 'Venta', cat=cat, area='',
                    pv=None, costo=None, f=q, up='', q=q, qu='', it=items, oid=rc['oid'], carta=None,
                    postre=bool(POSTRE.search(key(rc['n']) + ' ')) and 'PALTA' not in key(rc['n'])))
data = json.dumps(out, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
lib = open(os.path.join(HERE, 'xlsx.full.min.js'), encoding='utf-8').read()
html = open(os.path.join(HERE, 'plantilla.html'), encoding='utf-8').read()
html = html.replace('/*XLSX*/', lib, 1).replace('/*DATA*/', data, 1).replace('/*FUENTE*/', f'Odoo · Sede {SEDE}', 1)
html = html.replace('<title>Buscador de Recetas</title>', f'<title>Recetas {SEDE}</title>', 1)
open(OUT, 'w', encoding='utf-8').write(html)
print(f'{len(out)} recetas ({sum(o["t"] == "Base" for o in out)} base, {sum(o["postre"] for o in out)} postres) -> {OUT}')
