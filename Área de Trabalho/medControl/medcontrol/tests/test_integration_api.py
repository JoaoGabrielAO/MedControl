import requests
import pytest

def test_viacep_integration():
    """Valida se a API do ViaCEP está online e retornando dados corretos"""
    cep = "01001000"
    url = f"https://viacep.com.br/ws/{cep}/json/"
    
    response = requests.get(url)
    
    # Verifica se a conexão foi bem sucedida (Código 200)
    assert response.status_code == 200
    
    dados = response.json()
    
    # Verifica se o dado retornado é o esperado para aquele CEP
    assert dados["logradouro"] == "Praça da Sé"
    assert dados["localidade"] == "São Paulo"