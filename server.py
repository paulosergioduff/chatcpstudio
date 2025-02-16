from http.server import SimpleHTTPRequestHandler, HTTPServer

host = "localhost"
port = 8000

server = HTTPServer((host, port), SimpleHTTPRequestHandler)

print(f"Servidor rodando em http://{host}:{port}/")

server.serve_forever()
