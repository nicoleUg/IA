import argparse
import http.client
import http.server
import platform
import socketserver
import threading
import time
import urllib.parse
import webbrowser


HOST = "127.0.0.1"
PORT = 8000
PAGE = "index.html"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  
        return


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True


def start_server(host: str, port: int) -> socketserver.TCPServer:
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadingTCPServer((host, port), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def wait_for_server(url: str, timeout_s: float = 8.0) -> bool:
    parts = urllib.parse.urlsplit(url)
    host = parts.hostname or "127.0.0.1"
    port = parts.port or (443 if parts.scheme == "https" else 80)
    path = parts.path or "/"
    if parts.query:
        path += f"?{parts.query}"

    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            conn = http.client.HTTPConnection(host, port, timeout=1.0)
            conn.request("GET", path)
            resp = conn.getresponse()
            if 200 <= resp.status < 500:
                conn.close()
                return True
            conn.close()
        except Exception:
            pass
        time.sleep(0.15)
    return False


def open_in_webview(url: str) -> None:
    import webview  

    webview.create_window(
        "Teachable Machine Pose (Local)",
        url,
        width=900,
        height=800,
    )
    webview.start()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Teachable Machine Pose model locally")
    parser.add_argument(
        "--browser",
        action="store_true",
        help="Force open in your default browser",
    )
    parser.add_argument(
        "--webview",
        action="store_true",
        help="Force open in embedded WebView window",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=PORT,
        help="Port for the local HTTP server (default: 8000)",
    )
    parser.add_argument(
        "--backend",
        choices=["webgl", "cpu"],
        default="webgl",
        help="TensorFlow.js backend. Use cpu if webgl freezes (default: webgl)",
    )
    args = parser.parse_args()

    server = start_server(HOST, args.port)

    url = f"http://{HOST}:{args.port}/{PAGE}?backend={args.backend}"

    if not wait_for_server(url):
        print(f"Aviso: no se pudo verificar el servidor a tiempo en {url}. Se intentará abrir igual.")

    print("Servidor local listo:", url)

    is_windows = platform.system().lower().startswith("win")
    open_browser = args.browser or (is_windows and not args.webview)

    try:
        if open_browser:
            webbrowser.open(url)
            print("Se abrió en el navegador. Para cerrar: Ctrl+C en esta terminal.")
            while True:
                time.sleep(1)

        try:
            open_in_webview(url)
        except Exception as exc:
            print("No se pudo abrir la ventana WebView.")
            print("Motivo:", repr(exc))
            print("Abriendo en navegador como alternativa...")
            webbrowser.open(url)
            print("Para cerrar: Ctrl+C en esta terminal.")
            while True:
                time.sleep(1)
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCerrado por usuario.")
