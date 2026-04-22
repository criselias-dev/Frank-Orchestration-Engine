# Pipefy Real Case Scenarios – Frank 🚀🤖

[![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)](https://www.python.org/) 
[![Flask](https://img.shields.io/badge/Flask-2.3-orange?logo=flask)](https://flask.palletsprojects.com/) 
[![Ngrok](https://img.shields.io/badge/Ngrok-4.0-purple?logo=ngrok)](https://ngrok.com/) 
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 Resumo

**BE FREE, BE FRANK!**  
Frank é nosso mini Zapier caseiro, artesanal e imbatível.  
Ele nasceu pequeno, humilde e obcecado por CEPs, mas com uma ambição gigante: **dominar workflows inteiros**, mesmo com os limites do plano gratuito do Pipefy.

> Funciona de verdade. Funciona tanto que você quase acredita que ele poderia ser contratado como funcionário da sua empresa. 😎

---

## 🤖 Nascimento do Frank

Frank surgiu assim:

- **Problema inicial:** Pipefy free limita automações e chamadas de API → impossível preencher cards automaticamente sem gastar o número de chamadas permitido  
- **Solução artesanal:** Python + Flask + Ngrok + scripts que pegam CEP, consultam ViaCep e preenchem o card  
- **Resultado:** automação confiável, gratuita, escalável — sem depender de R$100+/mês de Zapier/N8N  

> Pequeno, mas já mais esperto que o limite free do Pipefy! 💪🤖

---

## 🛠 Arquitetura Técnica

- **Python 3.14** – motor principal  
- **Flask** – micro servidor para receber webhooks do Pipefy  
- **Ngrok** – expõe localmente o Flask para integração real  
- **requests + GraphQL** – consulta e atualiza cards  
- **Scripts modulares:** `automacao.py`, `pipefy.py`, `pipefy_update.py`, `webhook.py`  

<details>
<summary>Como Frank pensa 🤖</summary>

1. Recebe evento de card via **webhook**  
2. Verifica dados faltantes (CEP, endereço, etc.)  
3. Consulta **ViaCep**  
4. Atualiza card no Pipefy  
5. Repetição eficiente — atualmente consome mais de uma chamada, mas estamos evoluindo para **orquestrar o diabo usando o mínimo de chamadas possível**, vencendo os limites do plano free 😏  

> Começou com CEP, mas pode crescer e virar **orquestrador completo de workflows**.
</details>

---

## ⚡ Rodando o Frank (Local)

<details>
<summary>Passo a passo 🏃‍♂️</summary>

1. Clone o repositório  
2. Instale dependências:  
```bash
pip install -r requirements.txt
```
3. Configure variáveis de ambiente com o token do Pipefy  
4. Rode Flask:  
```bash
python webhook.py
```
5. Exponha com Ngrok:  
```bash
ngrok http 5000
```
6. Observe Frank preenchendo CEPs, otimizando chamadas e dominando cards 🤖  

> ⚠️ GitHub Pages não roda Python/Flask. Pages é só para documentação ou front-end estático.
</details>

---

## 🔐 Segurança

- **Nunca** commitar tokens ou credenciais  
- Use variáveis de ambiente  
- Frank é poderoso, mas não é hacker… ainda 🤖  

---

## 📈 Status Atual

- Funcionalidade inicial: CEP → ViaCep → Pipefy  
- Modular e expansível  
- Contorna limites do plano free do Pipefy  
- Potencial para orquestração total de workflows  
- Otimização em andamento para **minimizar chamadas de API**  

---

## 🚀 Próximos Passos

- Adicionar novos triggers e automações  
- Criar relatórios automáticos e dashboards  
- Tornar Frank um **orquestrador multi-API completo**, rivalizando com Zapier/N8N, mas totalmente artesanal 🐷💪  

---

> 🤖💻 Esse foi meu primeiro exercício em Python — Frank, a engine caseira que nasceu pequena, mas promete dominar workflows! 🚀
