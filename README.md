# Exemplo: Login com FastAPI + JWT (RS256)
 **Caique Maia - NUSP: 1255572** 

## O que tem aqui
- Backend em FastAPI que cadastra usuário (SQLite) e gera JWT assinado com **RS256** (private key).
- Frontend estático (HTML + JS) que pede token ao backend, verifica assinatura com a public key e guarda token em cookie.
- Token expira em **15 minutos**.

## Como usar
1. Gere chaves:
   ```bash
   mkdir keys
   openssl genrsa -out keys/private.pem 2048
   openssl rsa -in keys/private.pem -pubout -out keys/public.pem

2. Gere chaves:
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

3. Rode:
    uvicorn main:app --reload

4. Abra a página gerada: 
    http://127.0.0.1:8000/static/index.html


## Endpoints importantes
POST /register — JSON: { "username", "email", "password" } → retorna 201
POST /login — JSON: { "username", "password" } → retorna { access_token } e cookie
GET /public_key — retorna chave pública (PEM) usada para verificar token