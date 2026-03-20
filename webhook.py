from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

PIPEFY_API_URL = "https://api.pipefy.com/graphql"
PIPEFY_TOKEN = os.getenv("PIPEFY_TOKEN")

headers = {
    "Authorization": f"Bearer {PIPEFY_TOKEN}",
    "Content-Type": "application/json"
}

def graphql(query):
    response = requests.post(
        PIPEFY_API_URL,
        headers=headers,
        json={"query": query}
    )
    return response.json()

def get_card(card_id):
    query = f"""
    query {{
      card(id: "{card_id}") {{
        fields {{
          field {{ id label }}
          value
        }}
      }}
    }}
    """
    return graphql(query)

def update_fields_batch(card_id, updates):

    values = ",\n".join(
        [f'{{ fieldId: "{fid}", value: {json.dumps(val)} }}'
         for fid, val in updates.items()]
    )

    mutation = f"""
    mutation {{
      updateFieldsValues(input: {{
        nodeId: "{card_id}",
        values: [
          {values}
        ]
      }}) {{
        clientMutationId
      }}
    }}
    """

    return graphql(mutation)

def buscar_endereco_por_cep(cep):
    cep = cep.replace("-", "").strip()
    url = f"https://viacep.com.br/ws/{cep}/json/"
    return requests.get(url).json()

@app.route('/webhook', methods=['POST'])
def webhook():

    payload = request.json or {}

    # pegar ID corretamente
    card_id = payload.get("data", {}).get("card", {}).get("id")

    print("Card recebido:", card_id)

    if not card_id:
        return '', 200

    card_data = get_card(card_id)
    fields = card_data["data"]["card"]["fields"]

    cep = None
    phase_map = {}

    for f in fields:
        phase_map[f["field"]["label"]] = f["field"]["id"]
        if f["field"]["label"] == "CEP":
            cep = f["value"]

    updates = {}

    if cep:
        endereco = buscar_endereco_por_cep(cep)

        if "erro" not in endereco:
            updates[phase_map["Rua"]] = endereco.get("logradouro")
            updates[phase_map["Bairro"]] = endereco.get("bairro")
            updates[phase_map["Cidade"]] = endereco.get("localidade")

    if updates:
        update_fields_batch(card_id, updates)
        print("Endereço atualizado.")

    return '', 200


if __name__ == '__main__':
    app.run(port=5000)