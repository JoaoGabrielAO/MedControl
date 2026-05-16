import requests

print("--- Teste de API ViaCEP ---")
cep_digitado = "01001000" 

url = f"https://viacep.com.br/ws/{cep_digitado}/json/"
resposta = requests.get(url)

if resposta.status_code == 200:
    
    dados = resposta.json()
    print("Sucesso! O garçom trouxe os seguintes dados:")
    print(dados)
    print(f"\nA rua encontrada foi: {dados['logradouro']}")
else:
    print("Erro ao buscar o CEP.")