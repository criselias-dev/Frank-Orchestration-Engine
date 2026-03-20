from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

PIPEFY_API_URL = "https://api.pipefy.com/graphql"
PIPEFY_TOKEN = os.getenv("PIPEFY_TOKEN")

if not PIPEFY_TOKEN:
    raise Exception("PIPEFY_TOKEN não encontrada. Defina a variável de ambiente.")

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

def get_phase_fields():
    query = """
    query {
      phase(id: 342168944) {
        fields {
          id
          label
        }
      }
    }
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

def processar_card(card_id):

    card_data = get_card(card_id)
    fields = card_data["data"]["card"]["fields"]

    cep = None

    for f in fields:
        if f["field"]["label"] == "CEP":
            cep = f["value"]

    if not cep:
        print("CEP não encontrado no start form.")
        return

    endereco = buscar_endereco_por_cep(cep)

    if "erro" in endereco:
        print("CEP inválido.")
        return

    phase_fields_data = get_phase_fields()
    phase_fields = phase_fields_data["data"]["phase"]["fields"]

    # mapeia label -> id da fase (Application Received)
    phase_map = {pf["label"]: pf["id"] for pf in phase_fields}

    updates = {}

    if "Rua" in phase_map:
        updates[phase_map["Rua"]] = endereco.get("logradouro")

    if "Bairro" in phase_map:
        updates[phase_map["Bairro"]] = endereco.get("bairro")

    if "Cidade" in phase_map:
        updates[phase_map["Cidade"]] = endereco.get("localidade")

    if updates:
        update_fields_batch(card_id, updates)
        print("Endereço atualizado com sucesso.")
    else:
        print("Nada para atualizar.")

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json or {}

    card_id = payload.get("card_id") or payload.get("data", {}).get("card", {}).get("id")

    print("Card recebido:", card_id)

    if not card_id:
        return '', 200

    processar_card(card_id)

    return '', 200

if __name__ == '__main__':
    app.run(port=5000)