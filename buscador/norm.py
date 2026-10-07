import re, unicodedata
STOP={'DE','LA','EL','CON','Y','A','AL','DEL','LOS','LAS','EN','RB','M','B','P'}
def norm(s):
    s=unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode().upper()
    s=re.sub(r'\(.*?\)',' ',s) if not re.fullmatch(r'\s*\(.*\)\s*',s) else s
    s=re.sub(r'[^A-Z0-9 ]',' ',s)
    s=s.replace('RISSOTO','RISOTTO').replace('OZOBUCO','OSOBUCO').replace('CARRILERA','CARRILLERA').replace('SPAGUETTI','SPAGHETTI').replace('RIGATTONI','RIGATONI').replace('CEVICHE','CEBICHE')
    return ' '.join(w for w in s.split() if w not in STOP)
