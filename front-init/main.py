import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
from datetime import datetime
import socket
import threading


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        self.handle_socket(data_dict)
        self.send_response(302)
        self.send_header("Location", "/")
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "text/plain")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())

    def handle_socket(self, data_dict):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(json.dumps({timestamp: data_dict}).encode(), ("localhost", 5000))


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("0.0.0.0", 3000)
    http = server_class(server_address, handler_class)
    try:
        http_thread = threading.Thread(target=http.serve_forever)
        http_thread.start()
        print(f"HTTP Server running on port {server_address[1]}")

        socket_thread = threading.Thread(target=run_socket_server)
        socket_thread.start()
        print("Socket Server running on port 5000")

        http_thread.join()
        socket_thread.join()

    except KeyboardInterrupt:
        http.shutdown()
        print("HTTP Server shutting down")


def run_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("localhost", 5000))
        print("Socket Server listening on port 5000")

        while True:
            data, addr = s.recvfrom(1024)
            data_dict = json.loads(data)
            timestamp = list(data_dict.keys())[0]

            with open("storage/data.json", "a") as file:
                json.dump({timestamp: data_dict[timestamp]}, file)
                file.write("\n")


if __name__ == "__main__":
    run()
