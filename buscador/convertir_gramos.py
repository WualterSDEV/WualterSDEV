import sys, openpyxl
wb = openpyxl.load_workbook(sys.argv[1]); ws = wb.active
CONV = {'KILOS': 'GRAMOS', 'KILO': 'GRAMOS', 'KG': 'GRAMOS', 'LITROS': 'MILILITROS', 'LITRO': 'MILILITROS', 'LT': 'MILILITROS'}
n = 0
for row in ws.iter_rows(min_row=2):
    u = (row[4].value or '').strip().upper()
    if u in CONV and isinstance(row[7].value, (int, float)):
        v = round(row[7].value * 1000, 4)
        row[7].value = int(v) if v == int(v) else v
        row[4].value = CONV[u]; n += 1
wb.save(sys.argv[2]); print(n, 'líneas convertidas')
