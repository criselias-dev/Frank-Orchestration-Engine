import os
import requests
import json

PIPEFY_API_URL = "https://api.pipefy.com/graphql"
PIPEFY_TOKEN = os.getenv("PIPEFY_TOKEN")
APPLICATION_RECEIVED_PHASE_ID = 342168944

if not PIPEFY_TOKEN:
    raise Exception("PIPEFY_TOKEN não encontrada.")

headers = {
    "Authorization": f"Bearer {PIPEFY_TOKEN}",
    "Content-Type": "application/json"
}

# ----------------------------------------
# GraphQL genérica
# ----------------------------------------
def graphql(query):
    response = requests.post(
        PIPEFY_API_URL,
        headers=headers,
        json={"query": query}
    )
    return response.json()

# ----------------------------------------
# Buscar último card
# ----------------------------------------
def get_latest_card_from_phase():
    query = f"""
    query {{
      phase(id: {APPLICATION_RECEIVED_PHASE_ID}) {{
        cards {{
          edges {{
            node {{ id }}
          }}
        }}
      }}
    }}
    """
    data = graphql(query)
    edges = data["data"]["phase"]["cards"]["edges"]
    return edges[-1]["node"]["id"]

# ----------------------------------------
# Buscar card completo
# ----------------------------------------
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

# ----------------------------------------
# Buscar fields da fase
# ----------------------------------------
def get_phase_fields():
    query = f"""
    query {{
      phase(id: {APPLICATION_RECEIVED_PHASE_ID}) {{
        fields {{
          id
          label
        }}
      }}
    }}
    """
    return graphql(query)

# ----------------------------------------
# Update em lote seguro
# ----------------------------------------
def update_fields_batch(card_id, updates):

    formatted_values = []

    for fid, val in updates.items():

        if isinstance(val, list):
            value_part = json.dumps(val)
        else:
            value_part = json.dumps(val)

        formatted_values.append(
            f'{{ fieldId: "{fid}", value: {value_part} }}'
        )

    values_string = ",\n".join(formatted_values)

    mutation = f"""
    mutation {{
      updateFieldsValues(input: {{
        nodeId: "{card_id}",
        values: [
          {values_string}
        ]
      }}) {{
        clientMutationId
      }}
    }}
    """

    return graphql(mutation)

# ----------------------------------------
# ViaCEP
# ----------------------------------------
def buscar_endereco_por_cep(cep):
    cep = cep.replace("-", "").strip()
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    return response.json()

# ==================================================
# EXECUÇÃO PRINCIPAL
# ==================================================
if __name__ == "__main__":

    print("\n🔎 Buscando último card...\n")
    card_id = get_latest_card_from_phase()
    print("Card:", card_id)

    card_data = get_card(card_id)
    phase_fields_data = get_phase_fields()

    card_fields = card_data["data"]["card"]["fields"]
    phase_fields = phase_fields_data["data"]["phase"]["fields"]

    # ----------------------------------------
    # Mapear valores atuais do card
    # ----------------------------------------
    current_values = {}
    for f in card_fields:
        current_values[f["field"]["label"]] = f["value"]

    # ----------------------------------------
    # Mapear Start Form (convertendo JSON quando necessário)
    # ----------------------------------------
    start_form_map = {}
    for f in card_fields:
        if not f["value"]:
            continue

        value = f["value"]

        try:
            parsed = json.loads(value)
            start_form_map[f["field"]["label"]] = parsed
        except:
            start_form_map[f["field"]["label"]] = value

    # ----------------------------------------
    # Mapear fase por label
    # ----------------------------------------
    phase_map = {pf["label"]: pf["id"] for pf in phase_fields}

    updates = {}

    # ----------------------------------------
    # Copiar automaticamente APENAS se estiver vazio
    # ----------------------------------------
    for label, value in start_form_map.items():

        if label in phase_map:

            # Ignorar Responsible Recruiter (já automatizado)
            if label == "Responsible Recruiter":
                continue

            current_value = current_values.get(label)

            if not current_value:
                updates[phase_map[label]] = value

    # ----------------------------------------
    # Automação de endereço via CEP
    # ----------------------------------------
    cep = start_form_map.get("CEP")

    if cep:
        endereco = buscar_endereco_por_cep(cep)

        if "erro" not in endereco:

            if not current_values.get("Rua"):
                updates[phase_map["Rua"]] = endereco.get("logradouro")

            if not current_values.get("Bairro"):
                updates[phase_map["Bairro"]] = endereco.get("bairro")

            if not current_values.get("Cidade"):
                updates[phase_map["Cidade"]] = endereco.get("localidade")

    print("\n📦 Atualizações a serem feitas:\n")
    print(json.dumps(updates, indent=2, ensure_ascii=False))

    if updates:
        response = update_fields_batch(card_id, updates)
        print("\n✅ Resultado do update:\n")
        print(json.dumps(response, indent=2, ensure_ascii=False))
    else:
        print("Nada para atualizar.")