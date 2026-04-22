import argparse
import http.server
import socketserver
import threading
import time
import webbrowser


HOST = "127.0.0.1"
PORT = 8000
PAGE = "index.html"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  
        return


def start_server(host: str, port: int) -> socketserver.TCPServer:
    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer((host, port), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


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
        help="Open in your default browser (recommended if WebView is blank)",
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
    time.sleep(0.2)

    url = f"http://{HOST}:{args.port}/{PAGE}?backend={args.backend}"
    print("Servidor local listo:", url)

    try:
        if args.browser:
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
    main()
