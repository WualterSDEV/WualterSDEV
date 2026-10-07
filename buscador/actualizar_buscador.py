"""Genera Buscador_Recetas.html a partir de los reportes de Inforest.

Uso:
  python actualizar_buscador.py recetas_base.xls recetas_venta.xls [cruce_carta.xlsx] [salida.html]

cruce_carta.xlsx (opcional) es el Excel con la hoja 'Cruce Carta'; marca qué recetas están en la carta.
Requiere: pip install xlrd openpyxl
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from parse import parse; from norm import norm
if len(sys.argv) < 3: sys.exit(__doc__)
b = parse(sys.argv[1], 'base'); v = parse(sys.argv[2], 'venta')
CRUCE = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, '..', 'RECETAS_INFOREST_CARTA_Y_POSTRES.xlsx')
OUT = sys.argv[4] if len(sys.argv) > 4 else os.path.join(HERE, '..', 'Buscador_Recetas.html')
for rr in b+v:
    for it in rr['items']:
        if it['ucosto']=='KILOS' and it['factor']==1000.0: it['ucosto']='GRAMOS'
for r in b:
    if not r['nombre']: r['nombre'] = 'RB MASA HAMBURGUESA P' if r['codigo'] == '00171' else '(sin nombre) ' + r['codigo']
carta = {}
if os.path.exists(CRUCE):
    import openpyxl
    x = openpyxl.load_workbook(CRUCE, data_only=True)['Cruce Carta']
    for row in x.iter_rows(min_row=2, values_only=True):
        if row[3]: carta.setdefault(row[3], (row[0], row[1], row[2]))
bidx = {}
for r in b: bidx.setdefault(norm(r['nombre']), 'B'+r['codigo'])
def rnd(x): return round(x, 4) if isinstance(x, float) else x
out = []
for kind, recs in (('V', v), ('B', b)):
    for r in recs:
        items = []
        for it in r['items']:
            ref = bidx.get(norm(it['insumo'])) if it['tipo']=='Receta' else None
            if ref == kind+r['codigo']: ref = None
            items.append([it['insumo'], it['tipo'], it['cant'] and rnd(it['cant']), it['ucosto'], rnd(it['precio']), rnd(it['subtotal']), ref])
        c = carta.get(r['codigo']) if kind=='V' else None
        out.append(dict(id=kind+r['codigo'], cod=r['codigo'], n=r['nombre'], t='Venta' if kind=='V' else 'Base',
            cat=r['categoria'] or '', area=r['area'] or '', pv=rnd(r['venta']) if kind=='V' and (r['venta'] or 0) >= 1 else None,
            costo=rnd(r['costo']), up=r.get('unidad'), f=r.get('factor'), it=items,
            carta=[c[0], c[1], c[2]] if c else None, postre=(r['area']=='PASTELERIA')))
data = json.dumps(out, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
lib = open(os.path.join(HERE, 'xlsx.full.min.js'), encoding='utf-8').read()
html = open(os.path.join(HERE, 'plantilla.html'), encoding='utf-8').read()
html = html.replace('/*XLSX*/', lib, 1).replace('/*DATA*/', data, 1)
open(OUT, 'w', encoding='utf-8').write(html)
print(f'{len(out)} recetas ({sum(1 for o in out if o["carta"])} en carta, {sum(1 for o in out if o["postre"])} de pastelería) -> {OUT}')
