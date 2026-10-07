import xlrd
def lab(vals, key, off=1):
    # value after label (skip blanks)
    for i,v in enumerate(vals):
        if isinstance(v,str) and v.strip()==key:
            for w in vals[i+1:]:
                if isinstance(w,str) and w.strip().endswith(':'): return None
                if w!='' : return w
    return None
def parse(path, kind):
    s = xlrd.open_workbook(path).sheet_by_index(0)
    recs=[]; cat=None; cur=None
    for i in range(s.nrows):
        raw = s.row_values(i); vals=[v for v in raw if v!='']
        if not vals: continue
        if vals[0]=='Codigo :':
            name = lab(raw,'Receta Base :' if kind=='base' else 'Receta Venta:')
            if kind=='base' and name in ('Usuario :',): name=''
            cur=dict(codigo=vals[1], nombre=(name or '').strip(), area=lab(raw,'Area de Producción :'),
                     categoria=cat, unidad=lab(raw,'Unidad de Produc.:'), ucosto=lab(raw,'Unidad de Costo :'), factor=lab(raw,'Factor :'),
                     items=[], costo=None, venta=None)
            recs.append(cur)
        elif len(vals)==1 and isinstance(vals[0],str):
            cat=vals[0].strip()
        elif cur and isinstance(vals[0],str) and vals[0].isdigit() and len(vals)>=8:
            it=dict(item=vals[0],insumo=str(vals[1]).strip(),ucompra=vals[2],factor=vals[3],ucosto=vals[4],cant=vals[5],precio=vals[6],subtotal=vals[7])
            it['tipo']= vals[9] if kind=='base' and len(vals)>9 else ('Receta' if it['ucompra']=='RECETA' or str(it['insumo']).startswith('RB ') else 'Producto')
            cur['items'].append(it)
        elif cur and vals[0]=='Total Costo :':
            cur['costo']=vals[1]
        elif cur and kind=='venta' and vals[0]=='En el local':
            cur['costo']=lab(raw,'Total Costo :'); cur['venta']=lab(raw,'Venta :')
    return recs
