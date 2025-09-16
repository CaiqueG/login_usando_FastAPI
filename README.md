# 🔑 Exemplo: Login com FastAPI + JWT (RS256)

**Autor:** Caique Maia — **NUSP:** 1255572  

Este repositório demonstra uma implementação simples de autenticação com **FastAPI** usando **JWT assinado com RS256**, incluindo backend e um frontend estático para testes.

---

## 📌 Funcionalidades

- ✅ **Cadastro de usuário** (armazenado em SQLite)
- ✅ **Login** que gera um JWT com expiração de **15 minutos**
- ✅ **Assinatura RS256** com chave privada (no backend)
- ✅ **Verificação da assinatura** no frontend usando chave pública
- ✅ **Armazenamento seguro** do token em cookie

---

## 🛠️ Pré-requisitos

- Python 3.10+
- OpenSSL (para gerar as chaves)
- Navegador para acessar o frontend

---

## 🚀 Como usar

1. **Gerar chaves:**
   ```bash
   mkdir keys
   openssl genrsa -out keys/private.pem 2048
   openssl rsa -in keys/private.pem -pubout -out keys/public.pem

2. **Instalar dependências:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # .venv\Scripts\activate   # Windows (PowerShell)
   pip install -r requirements.txt

3. **Rodar servidor:**
   ```bash
   uvicorn main:app --reload

4. **Acessar o frontend:**
   Abra no navegador: http://127.0.0.1:8000/static/index.html

## 📡 Endpoints da API
http://127.0.0.1:8000/docs#/default/public_key_public_key_get

    ### POST /register (exemplo)
        {
        "username": "string",
        "email": "string",
        "password": "string"
        }

    ### POST /login (exemplo)
        {
        "username": "string",
        "password": "string"
        }

    ### GET /public_key (exemplo)
        Retorna a chave pública em formato PEM usada para verificar a assinatura do token.
        -----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqh...
        -----END PUBLIC KEY-----
