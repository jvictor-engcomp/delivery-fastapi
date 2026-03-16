# 🍔 Delivery FastAPI

Backend de um sistema de delivery desenvolvido com FastAPI.
Permite cadastro de usuários, autenticação com JWT e gerenciamento de pedidos.

---

## 🚀 Tecnologias Utilizadas

- Python
- FastAPI
- SQLAlchemy
- Alembic
- SQLite
- JWT Authentication
- Passlib (Argon2)

---

## 📦 Estrutura do Projeto

app/

├── main.py

├── models/

├── schemas/

├── routes/

├── database/

├── core/



---

## 🔐 Funcionalidades

- Cadastro de usuário
- Login com geração de Access Token e Refresh token(JWT)
- Criação de pedidos 
- Consulta de pedidos
- Criação de cardápio
- Proteção de rotas autenticadas

---

## ⚙️ Como Executar o Projeto

### 1️⃣ Clone o repositório

git clone https://github.com/jvictor-engcomp/delivery-fastapi.git
cd delivery-fastapi


### 2️⃣ Crie e ative o ambiente virtual

python -m venv venv
venv\Scripts\activate # Windows


### 3️⃣ Instale as dependências

pip install -r requirements.txt


### 4️⃣ Configure as variáveis de ambiente

Crie um arquivo `.env` baseado no `.env.example`:

SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


### 5️⃣ Execute as migrations

alembic upgrade head


### 6️⃣ Popular o menu

na raiz do proejeto digite a linha de código no terminal:

python -m scripts.populate_menu

### 6️⃣ Inicie o servidor

uvicorn app.main:app --reload


---

## 📚 Documentação da API

Após rodar o servidor, acesse:

http://127.0.0.1:8000/docs

---

## 🧠 Arquitetura

O projeto segue separação por camadas:

- **Routes** → Endpoints
- **Schemas** → Validação de dados
- **Models** → Estrutura do banco
- **Alembic** → Controle de migrations
- **Scripts** → Código para popular banco de dados
- **Core** → Contém dependencies.py
- **Database** → Dados do banco

---

## 📌 Melhorias Futuras

- Usar PostgreSQL
- Dockerização
- Deploy em produção
