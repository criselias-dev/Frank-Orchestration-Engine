import os
import requests

PIPEFY_API_URL = "https://api.pipefy.com/graphql"
PIPEFY_TOKEN = os.getenv("PIPEFY_TOKEN")

if not PIPEFY_TOKEN:
    raise Exception("PIPEFY_TOKEN não encontrada. Defina variável de ambiente.")

headers = {
    "Authorization": f"Bearer {PIPEFY_TOKEN}",
    "Content-Type": "application/json"
}

def get_address_from_cep(cep):
    """Consulta ViaCEP e retorna dados de endereço."""
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    data = response.json()

    if "erro" in data:
        raise Exception("CEP não encontrado.")

    return {
        "rua": data.get("logradouro", ""),
        "bairro": data.get("bairro", ""),
        "cidade": data.get("localidade", ""),
        "uf": data.get("uf", ""),
        "complemento": data.get("complemento", "")
    }

def update_pipe_card(card_id, address):
    mutation = """
    mutation UpdateFields($input: UpdateFieldsValuesInput!) {
      updateFieldsValues(input: $input) {
        clientMutationId
      }
    }
    """

    variables = {
        "input": {
            "nodeId": card_id,
            "values": [
                {"fieldId": "rua", "value": address["rua"]},
                {"fieldId": "bairro", "value": address["bairro"]},
                {"fieldId": "cidade", "value": address["cidade"]},
                {"fieldId": "uf", "value": address["uf"]},
                {"fieldId": "complemento", "value": address["complemento"]}
    ]
        }
    }

    response = requests.post(
        PIPEFY_API_URL,
        headers=headers,
        json={"query": mutation, "variables": variables}
    )

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        return response.json()
    except ValueError:
        return {"error": "Resposta não é JSON válido", "raw": response.text}
def main():
    cep = input("Digite o CEP: ")
    card_id = input("Digite o ID do card: ")

    address = get_address_from_cep(cep)
    print("Dados do CEP:", address)  # <--- ADICIONE ISSO

    result = update_pipe_card(card_id, address)
    print("Resultado da mutation:", result)  # <--- mantenha

if __name__ == "__main__":
    main()