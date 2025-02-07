import json
import requests
import sys
import os

def processar_arquivo(dados_path, config_path):
    # Ler o arquivo de configuração
    with open(config_path, 'r', encoding='utf-8') as conf_file:
        config = json.load(conf_file)
    
    api_url = f"{config['url']}/{config['endpoint']}"
    
    # Ler os dados do produto
    with open(dados_path, 'r', encoding='utf-8') as dados_file:
        dados = json.load(dados_file)
    
    # Enviar a requisição para a API
    response = requests.post(api_url, json=dados, headers={"Content-Type": "application/json"})
    
    # Verificar resposta
    if response.status_code == 200 or response.status_code == 201:
        print(f"Sucesso ao enviar {dados_path} para {api_url}")
    else:
        print(f"Erro ao enviar {dados_path}: {response.status_code} - {response.text}")
        sys.exit(1)  # Falha no pipeline se a requisição falhar

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python processa_json.py <caminho_dados.json> <caminho_config.json>")
        sys.exit(1)

    dados_json = sys.argv[1]
    config_json = sys.argv[2]

    if not os.path.exists(dados_json) or not os.path.exists(config_json):
        print("Erro: Arquivo(s) JSON não encontrado(s).")
        sys.exit(1)

    processar_arquivo(dados_json, config_json)
  