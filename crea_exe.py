"""Compila il programma Python in EXE con PyInstaller. Lo usa il workflow «Build EXE».
Le scelte (nome, versione, file di avvio, console…) stanno in exe.json. Generato da Pubblica · by Lollo ®2026"""
import hashlib, json, os, re, shutil, sys
import PyInstaller.__main__

os.chdir(os.path.dirname(os.path.abspath(__file__)))
c = json.load(open("exe.json", encoding="utf-8"))
nome = c["nome"]
versione = str(c.get("versione", "1.0"))
cartella = os.path.abspath("progetto")
avvio = os.path.abspath(c["avvio"])
if not os.path.isfile(avvio):
    sys.exit("File di avvio non trovato: " + c["avvio"])


def file_versione(percorso):
    """Proprietà del file in Windows (tasto destro → Proprietà → Dettagli): nome, versione, autore."""
    n = [int(x) for x in re.findall(r"\d+", versione)][:4]
    n += [0] * (4 - len(n))
    t = tuple(n)
    testo = f"""VSVersionInfo(
  ffi=FixedFileInfo(filevers={t}, prodvers={t}, mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[
    StringFileInfo([StringTable('041004B0', [
      StringStruct('CompanyName', 'by Lollo'),
      StringStruct('FileDescription', {nome!r}),
      StringStruct('FileVersion', {versione!r}),
      StringStruct('InternalName', {nome!r}),
      StringStruct('LegalCopyright', 'by Lollo ®2026'),
      StringStruct('OriginalFilename', {nome + '.exe'!r}),
      StringStruct('ProductName', {nome!r}),
      StringStruct('ProductVersion', {versione!r})])]),
    VarFileInfo([VarStruct('Translation', [0x0410, 1200])])
  ]
)
"""
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    with open(percorso, "w", encoding="utf-8") as f:
        f.write(testo)
    return percorso


arg = [avvio, "--name", nome, "--noconfirm", "--clean",
       "--distpath", "dist", "--workpath", "build", "--specpath", "build",
       "--paths", os.path.dirname(avvio), "--paths", cartella]
arg.append("--onefile" if c.get("unFile", True) else "--onedir")
arg.append("--console" if c.get("console", True) else "--windowed")
icona = c.get("icona")
if icona and os.path.isfile(icona):
    arg += ["--icon", os.path.abspath(icona)]   # PNG: PyInstaller lo converte in .ico grazie a Pillow
if os.name == "nt":                              # le proprietà del file esistono solo su Windows
    arg += ["--version-file", os.path.abspath(file_versione(os.path.join("build", "versione.txt")))]
prefisso = c.get("cartellaDati", "")            # app HTML: i file vanno nella cartella «app» dentro l'EXE
for f in c.get("dati", []):                     # immagini, json, testi del progetto: dentro l'EXE, stesse cartelle
    if os.path.isfile(f):
        dest = os.path.normpath(os.path.join(prefisso, os.path.relpath(os.path.dirname(os.path.abspath(f)), cartella)))
        arg += ["--add-data", os.path.abspath(f) + os.pathsep + dest]
for m in c.get("nascosti", []):
    arg += ["--hidden-import", m]
print("PyInstaller " + " ".join(arg), flush=True)
PyInstaller.__main__.run(arg)

os.makedirs("uscita", exist_ok=True)
est = ".exe" if os.name == "nt" else ""
if c.get("unFile", True):
    finale = os.path.join("uscita", nome + "-" + versione + est)
    shutil.copy2(os.path.join("dist", nome + est), finale)
else:
    finale = shutil.make_archive(os.path.join("uscita", nome + "-" + versione + "-windows"), "zip", os.path.join("dist", nome))

# impronta SHA-256: chi scarica può controllare che il file sia proprio questo
h = hashlib.sha256()
with open(finale, "rb") as f:
    for blocco in iter(lambda: f.read(1 << 20), b""):
        h.update(blocco)
with open(finale + ".sha256", "w", encoding="utf-8") as f:
    f.write(h.hexdigest() + "  " + os.path.basename(finale) + "\n")
print("Pronto: " + finale + " (" + str(os.path.getsize(finale)) + " byte)")
print("SHA-256: " + h.hexdigest())
