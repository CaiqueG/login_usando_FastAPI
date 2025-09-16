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

### 1. Criar banco de dados PostgreSQL
    No terminal `psql` ou via pgAdmin:

    ```sql
    CREATE DATABASE login_db;

### 2. Configurar variáveis de ambiente
    $env:DB_USER="postgres"
    $env:DB_PASS="SUA_SENHA_DO_POSTGRES"
    $env:DB_NAME="login_db"
    $env:DB_HOST="localhost"
    $env:DB_PORT="5432"


### 3. Configurar variáveis de ambiente
    mkdir keys
    openssl genrsa -out keys/private.pem 2048
    openssl rsa -in keys/private.pem -pubout -out keys/public.pem

### 4. Instalar dependências
    source .venv/bin/activate
    pip install -r requirements.txt

### 5. Rodar servidor FastAPI
    uvicorn main:app --reload --host 127.0.0.1 --port 8000

### 6. Acessar o frontend
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
