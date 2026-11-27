"""Avvia l'app HTML come programma Windows: una finestra con il motore di Edge (WebView2).
I file dell'app sono dentro l'EXE; un piccolo server locale li serve su http://127.0.0.1,
così fetch, moduli JavaScript e salvataggi (localStorage) funzionano come online.
Generato da Pubblica · by Lollo ®2026"""
import functools, http.server, os, socket, socketserver, sys, threading, time, webbrowser, zlib

TITOLO = "Pubblica"
APP_ID = "Pubblica"                 # nome fisso dell'app: da qui dipendono porta e cartella dei dati
PAGINA = "index.html"
LARGHEZZA, ALTEZZA = 1200, 800
SCHERMO_INTERO = False

BASE = os.path.join(getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))), "app")
# I dati dell'app (localStorage, IndexedDB) restano qui tra un avvio e l'altro
DATI = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "by Lollo", APP_ID)
# Porta sempre uguale per questa app: i salvataggi del browser sono legati all'indirizzo
PORTA = 20000 + zlib.crc32(APP_ID.encode("utf-8")) % 20000
TIPI = {".js": "text/javascript", ".mjs": "text/javascript", ".css": "text/css", ".json": "application/json",
        ".svg": "image/svg+xml", ".wasm": "application/wasm", ".webmanifest": "application/manifest+json",
        ".html": "text/html", ".htm": "text/html", ".png": "image/png", ".jpg": "image/jpeg", ".ico": "image/x-icon"}


class Gestore(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, **TIPI}  # su Windows il registro può sbagliare i tipi

    def log_message(self, *a):            # senza console non c'è dove scrivere
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = False


def avvia_server():
    gestore = functools.partial(Gestore, directory=BASE)
    for porta in [PORTA] + list(range(PORTA + 1, PORTA + 20)):
        try:
            srv = Server(("127.0.0.1", porta), gestore)
            threading.Thread(target=srv.serve_forever, daemon=True).start()
            return srv, f"http://127.0.0.1:{porta}/{PAGINA}"
        except OSError:
            continue                       # porta occupata: provo la successiva
    raise SystemExit("Nessuna porta libera per avviare l'app.")


def edge_disponibile():
    """True se c'è WebView2 (Windows 10/11 aggiornati). Senza, pywebview userebbe il vecchio Internet Explorer."""
    try:
        from webview.platforms import winforms
        return winforms.renderer == "edgechromium"
    except Exception:
        return False


def apri_nel_browser(url):
    """Ripiego: l'app si apre nel browser predefinito e questa finestrella la tiene accesa."""
    webbrowser.open(url)
    try:
        import tkinter as tk
        f = tk.Tk()
        f.title(TITOLO)
        f.geometry("420x150")
        tk.Label(f, text=f"{TITOLO} è aperta nel browser.\n\nChiudi questa finestra per spegnerla.\n"
                        "(Per aprirla in una finestra sua installa «Microsoft Edge WebView2 Runtime».)",
                 justify="center", padx=16, pady=16).pack(expand=True)
        tk.Button(f, text="Riapri nel browser", command=lambda: webbrowser.open(url)).pack(pady=(0, 12))
        f.mainloop()
    except Exception:
        while True:
            time.sleep(3600)


def main():
    if not os.path.isfile(os.path.join(BASE, PAGINA)):
        raise SystemExit("Pagina non trovata nell'EXE: " + PAGINA)
    srv, url = avvia_server()
    if os.environ.get("PUBBLICA_PROVA"):   # prova automatica senza finestra
        print(url, flush=True)
        time.sleep(float(os.environ["PUBBLICA_PROVA"]))
        return
    if sys.platform == "win32" and not edge_disponibile():
        apri_nel_browser(url)
        return
    import webview
    try:
        webview.settings["ALLOW_DOWNLOADS"] = True              # esporta/scarica file dall'app
        webview.settings["OPEN_EXTERNAL_LINKS_IN_BROWSER"] = True
    except Exception:
        pass
    os.makedirs(DATI, exist_ok=True)
    webview.create_window(TITOLO, url, width=LARGHEZZA, height=ALTEZZA, min_size=(360, 480),
                          fullscreen=SCHERMO_INTERO, text_select=True)
    try:
        webview.start(private_mode=False, storage_path=DATI)
    except Exception:
        apri_nel_browser(url)


if __name__ == "__main__":
    main()
