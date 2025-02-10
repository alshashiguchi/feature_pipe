import pytest
from unittest.mock import patch, mock_open
import json
import requests
import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.process_feature import processar_arquivo

@patch("builtins.open", new_callable=mock_open)
@patch("requests.post")
def test_processar_arquivo_sucesso(mock_post, mock_file):
    # Mock dos arquivos de configuração e dados
    mock_file.side_effect = [
        mock_open(read_data=json.dumps({"url": "http://mockapi.com", "endpoint": "test"})).return_value,
        mock_open(read_data=json.dumps({"key": "value"})).return_value
    ]

    # Mock da resposta da API
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Chamada da função
    processar_arquivo("dados.json", "config.json")
    
    # Verificações
    mock_post.assert_called_once_with("http://mockapi.com/test", json={"key": "value"}, headers={"Content-Type": "application/json"})

@patch("builtins.open", new_callable=mock_open)
@patch("requests.post")
def test_processar_arquivo_falha(mock_post, mock_file):
    # Mock dos arquivos de configuração e dados
    mock_file.side_effect = [
        mock_open(read_data=json.dumps({"url": "http://mockapi.com", "endpoint": "test"})).return_value,
        mock_open(read_data=json.dumps({"key": "value"})).return_value
    ]

    # Mock da resposta da API com erro
    mock_response = requests.Response()
    mock_response.status_code = 400
    mock_response._content = b"Bad Request"
    mock_post.return_value = mock_response

    with pytest.raises(SystemExit) as cm:
        processar_arquivo("dados.json", "config.json")

    assert cm.value.code == 1
    mock_post.assert_called_once_with("http://mockapi.com/test", json={"key": "value"}, headers={"Content-Type": "application/json"})
