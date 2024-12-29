import requests

def true_random_number(api_key, num=1, min_val=0, max_val=100):
    """
    Gera números verdadeiramente aleatórios usando a API Random.org.
    
    :param api_key: Chave da API da Random.org
    :param num: Quantidade de números aleatórios a serem gerados
    :param min_val: Valor mínimo (inclusivo)
    :param max_val: Valor máximo (inclusivo)
    :return: Lista de números aleatórios
    """
    url = "https://api.random.org/json-rpc/4/invoke"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": api_key,
            "n": num,
            "min": min_val,
            "max": max_val,
            "replacement": True
        },
        "id": 42
    }
    
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    
    if "result" in data:
        return data["result"]["random"]["data"]
    else:
        raise Exception(f"Erro ao obter número aleatório: {data.get('error', 'Desconhecido')}")


if __name__ == "__main__":
    # Exemplo de uso
    api_key = API_KEY
    i = 0
    while i < 2:
        i += 1
        try:
            random_numbers = true_random_number(api_key, num=6, min_val=1, max_val=60)
            random_numbers = sorted(random_numbers)
            print("Números verdadeiramente aleatórios:", random_numbers)
        except Exception as e:
            print("Erro:", e)
