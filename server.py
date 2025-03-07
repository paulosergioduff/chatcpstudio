from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
from datetime import datetime

# Criar uma lista para armazenar o histórico do chat (simulação)
chatHistory = []

# Criar a pasta 'memories/Temporal_Lobe' se não existir
if not os.path.exists("memories/Temporal_Lobe"):
    os.makedirs("memories/Temporal_Lobe")

class RequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/sendChat':  # Verifica se a rota é /sendChat
            content_length = int(self.headers['Content-Length'])  # Tamanho dos dados
            post_data = self.rfile.read(content_length)  # Lê os dados POST
            
            try:
                chat_data = json.loads(post_data)  # Converte os dados para JSON
                chatHistory.extend(chat_data)  # Adiciona ao histórico do chat
                print("Chat recebido:", chat_data)
                
                # Gerar o nome do arquivo com timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                file_path = os.path.join("memories", "Temporal_Lobe", f"{timestamp}.json")  # Caminho atualizado
                
                # Salvar os dados no arquivo
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(chat_data, f, ensure_ascii=False, indent=4)
                
                # Responde ao cliente
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "sucesso"}).encode())
            except json.JSONDecodeError:
                self.send_response(400)  # Resposta de erro se não for um JSON válido
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Dados inválidos"}).encode())
        else:
            # Caso a rota não seja reconhecida
            self.send_response(404)
            self.end_headers()

# Configuração do servidor
host = "localhost"
port = 8000

def run():
    server = HTTPServer((host, port), RequestHandler)
    print(f"Servidor rodando em http://{host}:{port}/")
    server.serve_forever()

if __name__ == '__main__':
    run()