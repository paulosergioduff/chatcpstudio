import os
import json
from datetime import datetime
import pyperclip  # Para copiar para a área de transferência

# Configurações
MEMORIES_DIR = "memories/Temporal_Lobe"
DATE_FORMAT = "%Y-%m-%d-%H-%M-%S"

# Função para carregar conversas dentro de um intervalo de datas
def load_conversations(start_date, end_date):
    conversations = []
    try:
        # Verifica se a pasta existe
        if not os.path.exists(MEMORIES_DIR):
            print(f"Erro: A pasta '{MEMORIES_DIR}' não foi encontrada.")
            return conversations
        
        # Lista os arquivos na pasta
        for filename in os.listdir(MEMORIES_DIR):
            if filename.endswith(".json"):
                try:
                    # Extrai a data do nome do arquivo
                    file_date_str = filename.split(".")[0]
                    file_date = datetime.strptime(file_date_str, DATE_FORMAT)
                    
                    # Verifica se a data está dentro do intervalo
                    if start_date <= file_date <= end_date:
                        file_path = os.path.join(MEMORIES_DIR, filename)
                        with open(file_path, "r") as file:
                            data = json.load(file)  # Carrega o array completo
                            conversations.extend(data)  # Adiciona todas as mensagens
                except ValueError:
                    print(f"Erro: O arquivo '{filename}' não segue o formato de data esperado.")
                except Exception as e:
                    print(f"Erro ao processar o arquivo '{filename}': {str(e)}")
    except Exception as e:
        print(f"Erro ao acessar a pasta '{MEMORIES_DIR}': {str(e)}")
    
    return conversations

# Função para formatar as conversas em um texto claro
def format_conversations(conversations):
    formatted_text = ""
    for message in conversations:
        if message["sender"] == "user":
            formatted_text += f"Usuário: {message['content']}\n"
        elif message["sender"] == "ai":
            formatted_text += f"IA: {message['content']}\n"
    return formatted_text

# Função para gerar o prompt
def generate_prompt(formatted_text):
    prompt = (
        "Abaixo estão algumas conversas que tive com um usuário. "
        "Com base nessas conversas, responda:\n"
        "1. Quais foram os principais tópicos discutidos?\n"
        "2. Quais insights ou aprendizados podem ser extraídos?\n"
        "3. Há alguma tendência ou padrão recorrente nas conversas?\n\n"
        f"{formatted_text}"
    )
    return prompt

# Função principal do módulo Sleep
def sleep_module(start_date_str, end_date_str):
    try:
        start_date = datetime.strptime(start_date_str, DATE_FORMAT)
        end_date = datetime.strptime(end_date_str, DATE_FORMAT)
    except ValueError:
        return "Erro: O formato da data deve ser 'YYYY-MM-DD-HH-MM-SS'."
    
    conversations = load_conversations(start_date, end_date)
    
    if not conversations:
        return "Nenhuma conversa encontrada no intervalo especificado."
    
    formatted_text = format_conversations(conversations)
    prompt = generate_prompt(formatted_text)
    
    # Copia o prompt para a área de transferência
    try:
        pyperclip.copy(prompt)
        print("Prompt copiado para a área de transferência!")
    except Exception as e:
        print(f"Erro ao copiar para a área de transferência: {str(e)}")
        print("Salvando o prompt em um arquivo temporário...")
        with open("temp_prompt.txt", "w") as file:
            file.write(prompt)
        print("Prompt salvo em 'temp_prompt.txt'.")
    
    return prompt

# Exemplo de uso:
if __name__ == "__main__":
    prompt = sleep_module("2025-02-16-00-00-00", "2025-02-24-23-59-59")
    print("\nPrompt gerado:\n")
    print(prompt)