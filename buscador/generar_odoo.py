"""Recetas de Inforest (carta + postres + sus recetas base) en formato de importación de Odoo, en gramos.

Uso:
  python generar_odoo.py recetas_base.xls recetas_venta.xls recetas_odoo.xlsx cruce_carta.xlsx salida.xlsx
"""
import sys, os, re, unicodedata, openpyxl
from copy import copy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from parse import parse; from norm import norm
if len(sys.argv) < 6: sys.exit(__doc__)
BASE, VENTA, ODOO, CRUCE, OUT = sys.argv[1:6]

def a_gramos(cant, unidad, factor=None):
    if unidad in ('KILOS', 'LITROS'):
        return (cant if factor == 1000.0 else (cant or 0) * 1000), ('GRAMOS' if unidad == 'KILOS' else 'MILILITROS')
    return cant, unidad
def key(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().upper()
    return ' '.join(re.sub(r'[^A-Z0-9()/ ]', ' ', s).split())

b = parse(BASE, 'base'); v = parse(VENTA, 'venta')
for rr in b + v:
    for it in rr['items']:
        it['cant'], it['ucosto'] = a_gramos(it['cant'], it['ucosto'], it['factor'])
for r in b:
    if not r['nombre']: r['nombre'] = 'RB MASA HAMBURGUESA P' if r['codigo'] == '00171' else '(sin nombre) ' + r['codigo']
    f = r['factor'] if isinstance(r['factor'], (int, float)) else None
    r['rinde'], r['urinde'] = a_gramos(f, r['ucosto'], f) if f is not None else (None, None)

ws = openpyxl.load_workbook(ODOO).active
hdr = [c for c in ws[1]]
ref, loose = {}, {}
for r in ws.iter_rows(min_row=2, values_only=True):
    if r[0] and r[1]: ref.setdefault(key(r[1]), r[0])
    if r[5] and r[6]: ref.setdefault(key(r[6]), r[5])
for k, c in ref.items(): loose.setdefault((norm(k), k.startswith('RB '), k.startswith('(M')), set()).add(c)
def odoo_ref(name):
    k = key(name)
    if k in ref: return ref[k]
    s = loose.get((norm(k), k.startswith('RB '), k.startswith('(M')))
    return next(iter(s)) if s and len(s) == 1 else None

carta = {row[3] for row in openpyxl.load_workbook(CRUCE, data_only=True)['Cruce Carta'].iter_rows(min_row=2, values_only=True) if row[3]}
vsel = [r for r in v if r['codigo'] in carta or r['area'] == 'PASTELERIA']
bidx = {}
for r in b: bidx.setdefault(norm(r['nombre']), r)
order, seen = [], set()
def visit(r):
    for it in r['items']:
        s = bidx.get(norm(it['insumo'])) if it['tipo'] == 'Receta' else None
        if s and s is not r and s['codigo'] not in seen:
            seen.add(s['codigo']); visit(s); order.append(s)
for r in [r for r in b if r['area'] == 'PASTELERIA'] + vsel: visit(r)
for r in b:
    if r['area'] == 'PASTELERIA' and r['codigo'] not in seen: seen.add(r['codigo']); order.append(r)

out = openpyxl.Workbook(); o = out.active; o.title = ws.title
for j, h in enumerate(hdr, 1):
    c = o.cell(1, j, h.value); c.font = copy(h.font); c.fill = copy(h.fill); c.alignment = copy(h.alignment); c.border = copy(h.border)
for col, dim in ws.column_dimensions.items(): o.column_dimensions[col].width = dim.width
row = 2
for r, t in [(r, 'Base') for r in order] + [(r, 'Venta') for r in vsel]:
    # Fila de la receta: rinde y su unidad (ej. 72 PORCION); los insumos van en las filas de abajo
    head = [odoo_ref(r['nombre']), r['nombre'], 'Fabricar este producto', 1 if t == 'Venta' else (r['rinde'] or 1),
            'UNIDAD' if t == 'Venta' else (r['urinde'] or 'UNIDAD'), None, None, None]
    lines = [head] + [[None] * 4 + [it['ucosto'], odoo_ref(it['insumo']), it['insumo'], it['cant']] for it in r['items']]
    for line in lines:
        for j, val in enumerate(line, 1):
            if isinstance(val, float) and val == int(val): val = int(val)
            o.cell(row, j, round(val, 4) if isinstance(val, float) else val)
        row += 1
o.freeze_panes = 'A2'
out.save(OUT)
print(f'{len(order) + len(vsel)} recetas ({len(order)} base, {len(vsel)} venta), {row - 2} filas -> {OUT}')
