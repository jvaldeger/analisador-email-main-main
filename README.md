PROJETO ANALISADOR-EMAIL

Este projeto é uma aplicação full stack composta por:

- Frontend: Angular 21
- Backend: Python + FastAPI

A estrutura do projeto é organizada dentro da pasta "apps", separando frontend e backend.

--------------------------------------------------

ESTRUTURA DO PROJETO

.
├── apps
│   ├── frontend
│   │   └── Aplicação Angular 21
│   └── backend
│       └── API em FastAPI (Python)
└── README.txt

--------------------------------------------------

FRONTEND — ANGULAR 21

Caminho:
apps/frontend

Instalação das dependências:

Dentro da pasta apps/frontend, execute o comando:

npm i

Build do projeto:

Para buildar o frontend, execute:

npm run build

--------------------------------------------------

BACKEND — PYTHON + FASTAPI

Caminho:
apps/backend

Instalação das dependências:

As dependências do backend estão definidas no arquivo:

pyproject.toml

poetry install

--------------------------------------------------

EXECUTAR O BACKEND

Para rodar a aplicação FastAPI, execute:

python src/main.py

--------------------------------------------------

TECNOLOGIAS UTILIZADAS

- Angular 21
- Node.js / NPM
- Python
- FastAPI

--------------------------------------------------

OBSERVAÇÕES IMPORTANTES

- Certifique-se de ter o Node.js instalado.
- Certifique-se de ter o Python instalado.
- Recomenda-se o uso de ambiente virtual no backend.
- Frontend e backend podem ser executados separadamente.

--------------------------------------------------

LICENÇA

Este projeto está sob a licença MIT.
