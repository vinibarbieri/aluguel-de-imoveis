# 🏡 Sistema de Aluguel de Imóveis

Este é um sistema completo de aluguel de imóveis desenvolvido com **Flask** no backend e **React** no frontend, utilizando arquivos `.json` como banco de dados (sem uso de SQL). O sistema possui funcionalidades para **locadores** e **locatários**, e utiliza a API do Google Places para busca e cadastro de endereços.

---

## ✨ Funcionalidades

### 👤 Locador
- Cadastro e login
- Cadastra imóveis com:
  - Endereço via Google Maps Autocomplete
  - Período de disponibilidade
  - Preço da diária
  - Imagem ilustrativa
- Edita ou remove imóveis
- Visualiza reservas recebidas
- Aprova ou recusa reservas

### 🔍 Locatário
- Busca imóveis por cidade, bairro ou rua
- Filtra por preço e datas
- Solicita reservas
- Avalia os imóveis após o período de locação
- Visualiza suas reservas (futuras e passadas)

---

## ⚙️ Tecnologias

- **Backend**: Python + Flask + JSON (sem banco relacional)
- **Frontend**: React + TypeScript + Bootstrap
- **APIs externas**: Google Places Autocomplete

---

## Estrutura do Projeto

```
aluguel-de-imoveis/
├── backend/                 # Backend em Flask
│   ├── app/                # Módulos da aplicação
│   │   ├── models/         # Modelos de dados
│   │   ├── routes/         # Rotas da API
│   │   ├── services/       # Serviços da aplicação
│   │   └── data_manager.py # Gerenciamento de dados
│   ├── data/               # Armazenamento de dados
│   ├── requirements.txt    # Dependências Python
│   └── run.py             # Script de inicialização
└── frontend/              # Frontend em React
    ├── public/            # Arquivos estáticos
    └── src/               # Código fonte React
```

## Requisitos

- Python 3.8 ou superior
- Node.js 14 ou superior
- npm ou yarn

## Configuração do Ambiente

### Backend

1. Crie um ambiente virtual Python:
```bash
cd backend
python -m venv venv
```

2. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie o servidor backend:
```bash
python run.py
```

O servidor backend estará rodando em `http://localhost:5000`

### Frontend

1. Instale as dependências:
```bash
cd frontend
npm install
```

2. Inicie o servidor de desenvolvimento:
```bash
npm start
```

O frontend estará disponível em `http://localhost:3000`

## API Endpoints

### Autenticação
- `POST /api/auth/register` - Registro de novo usuário
- `POST /api/auth/login` - Login de usuário
- `PUT /api/auth/edit` - Edição de informações do usuário

### Locador
- `POST /api/locador/properties` - Criar novo imóvel
- `GET /api/locador/properties/<owner_id>` - Listar imóveis do locador
- `PUT /api/locador/property/<id>` - Atualizar imóvel
- `DELETE /api/locador/property/<id>` - Deletar imóvel
- `GET /api/locador/reservations/<owner_id>` - Listar reservas recebidas
- `PUT /api/locador/reservation/<id>` - Aprovar/recusar reserva

### Locatário
- `GET /api/locatario/search` - Buscar imóveis disponíveis
- `POST /api/locatario/reserve` - Realizar reserva
- `GET /api/locatario/my-reservations/<user_id>` - Listar minhas reservas
- `POST /api/locatario/review` - Criar avaliação
- `GET /api/locatario/property/<property_id>/reviews` - Listar avaliações de um imóvel

## Armazenamento de Dados

O sistema utiliza arquivos JSON para armazenamento de dados. Os arquivos são salvos no diretório `backend/data/` e incluem:
- `users.json` - Dados dos usuários
- `properties.json` - Dados dos imóveis
- `reservations.json` - Dados das reservas
- `reviews.json` - Dados das avaliações

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes. 