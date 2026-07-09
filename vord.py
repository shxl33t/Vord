#!/usr/bin/env python3
# vord — detector de troca de tela do device. Captura screenshot automatico
# quando a tela muda, grava em screens/ + vord-log.tsv com timestamp.
# Roda em terminal proprio (background). Os timestamps do log permitem
# correlacionar cada tela com o trafego de um proxy (Burp, mitmproxy) depois.
#
# Uso: python3 vord.py [serial]    (sem serial = usa o device conectado)
import sys, os, time, subprocess, io, datetime
from PIL import Image

SERIAL = sys.argv[1] if len(sys.argv) > 1 else None
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "screens")
os.makedirs(SHOTS, exist_ok=True)
LOG = os.path.join(SHOTS, "vord-log.tsv")

POLL = 2.5          # segundos entre capturas
DIST_NEW = 12       # hamming > isto = tela candidata a nova
DIST_SETTLE = 4     # candidata estavel se proxima captura difere < isto

def adb(*args):
    return ["adb"] + (["-s", SERIAL] if SERIAL else []) + list(args)

def screencap():
    p = subprocess.run(adb("exec-out","screencap","-p"),
                       capture_output=True, timeout=15)
    return p.stdout or b""

def dhash(png_bytes, size=8):
    img = Image.open(io.BytesIO(png_bytes)).convert("L").resize((size+1,size), Image.LANCZOS)
    px = list(img.tobytes())
    bits = 0; i = 0
    for row in range(size):
        for col in range(size):
            left = px[row*(size+1)+col]; right = px[row*(size+1)+col+1]
            bits = (bits<<1) | (1 if left>right else 0); i+=1
    return bits

def ham(a,b): return bin(a^b).count("1")

def focused():
    try:
        out = subprocess.run(adb("shell",
              "dumpsys window 2>/dev/null | grep -E 'mCurrentFocus|mFocusedApp' | head -2"),
              capture_output=True, timeout=8, text=True).stdout
        out = " ".join(out.split())
        return out or "?"
    except Exception:
        return "?"

def log(epoch, secure, h, path, nbytes, foc):
    new = not os.path.exists(LOG)
    with open(LOG,"a") as f:
        if new: f.write("epoch\tiso\tsecure\tdhash\tpng\tbytes\tfocus\n")
        iso = datetime.datetime.fromtimestamp(epoch).isoformat(timespec="seconds")
        f.write(f"{int(epoch)}\t{iso}\t{secure}\t{h:016x}\t{path}\t{nbytes}\t{foc}\n")

def main():
    print(f"[*] vord ativo (serial={SERIAL or 'auto'}). Ctrl-C pra sair.")
    print(f"[*] screenshots -> {SHOTS}/auto-*.png   log -> {LOG}")
    last_saved = None       # dhash da ultima tela SALVA
    last_secure = False
    cand = None             # (dhash, png_bytes)
    while True:
        try:
            data = screencap()
            ts = time.time()
            if len(data) < 1000:   # FLAG_SECURE ou captura falhou
                if not last_secure:
                    foc = focused()
                    log(ts, 1, 0, "", 0, foc)
                    print(f"[{datetime.datetime.now():%H:%M:%S}] tela SECURE (sem captura)  {foc}")
                    last_secure = True; last_saved = None; cand = None
                time.sleep(POLL); continue
            last_secure = False
            h = dhash(data)
            if last_saved is None or ham(h, last_saved) > DIST_NEW:
                # candidata a nova tela — confirma estabilidade
                if cand is not None and ham(h, cand[0]) <= DIST_SETTLE:
                    foc = focused()
                    name = f"auto-{datetime.datetime.fromtimestamp(ts):%H%M%S}.png"
                    path = os.path.join(SHOTS, name)
                    with open(path,"wb") as f: f.write(data)
                    log(ts, 0, h, path, len(data), foc)
                    print(f"[{datetime.datetime.now():%H:%M:%S}] NOVA TELA -> {name}  {foc}")
                    last_saved = h; cand = None
                else:
                    cand = (h, data)   # primeira deteccao; espera proxima pra confirmar
            else:
                cand = None
            time.sleep(POLL)
        except KeyboardInterrupt:
            print("\n[*] encerrado."); break
        except Exception as e:
            print(f"[!] {e}"); time.sleep(POLL)

if __name__ == "__main__":
    main()
