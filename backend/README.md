# Backend - Sistema de Aluguel de Imóveis

Este é o backend do sistema de aluguel de imóveis, desenvolvido em Flask. O sistema fornece uma API RESTful para gerenciar usuários, imóveis, reservas e avaliações.

## Estrutura do Projeto

```
backend/
├── app/                    # Módulos da aplicação
│   ├── models/            # Modelos de dados
│   │   ├── user.py        # Modelo de usuário
│   │   ├── property.py    # Modelo de imóvel
│   │   ├── reservation.py # Modelo de reserva
│   │   └── review.py      # Modelo de avaliação
│   ├── routes/            # Rotas da API
│   │   ├── auth_routes.py # Rotas de autenticação
│   │   ├── locador_routes.py # Rotas do locador
│   │   └── locatario_routes.py # Rotas do locatário
│   ├── services/          # Serviços da aplicação
│   │   ├── auth_service.py # Serviços de autenticação
│   │   └── json_storage.py # Serviço de armazenamento
│   └── data_manager.py    # Gerenciamento de dados
├── data/                  # Armazenamento de dados
├── requirements.txt       # Dependências Python
└── run.py                # Script de inicialização
```

## Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Dependências

As principais dependências do projeto estão listadas no arquivo `requirements.txt`:
- Flask: Framework web
- Flask-CORS: Para habilitar CORS
- Outras dependências necessárias

## Configuração do Ambiente

1. Crie um ambiente virtual Python:
```bash
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

4. Inicie o servidor:
```bash
python run.py
```

O servidor estará rodando em `http://localhost:5000`

## API Endpoints

### Autenticação (`/api/auth`)
- `POST /register` - Registro de novo usuário
  - Body: `{ "name": string, "email": string, "user_type": "locador" | "locatario" }`
  - Retorno: `{ "message": string, "user_id": string }`

- `POST /login` - Login de usuário
  - Body: `{ "email": string }`
  - Retorno: `{ "message": string, "user": { "id": string, "name": string, "email": string, "user_type": string } }`

- `PUT /edit` - Edição de informações do usuário
  - Body: `{ "id": string, "name": string, "email": string }`
  - Retorno: `{ "message": string }`

### Locador (`/api/locador`)
- `POST /properties` - Criar novo imóvel
  - Body: `{ "title": string, "description": string, "address": string, "price_per_day": number, "available_from": string, "available_until": string, "owner_id": string, "image_url": string }`
  - Retorno: `{ "message": string, "property_id": string }`

- `GET /properties/<owner_id>` - Listar imóveis do locador
  - Retorno: Lista de imóveis com avaliações e reservas

- `PUT /property/<id>` - Atualizar imóvel
  - Body: `{ "title": string, "description": string, "address": string, "price_per_day": number, "available_from": string, "available_until": string, "image_url": string }`
  - Retorno: `{ "message": string }`

- `DELETE /property/<id>` - Deletar imóvel
  - Retorno: `{ "message": string }`

- `GET /reservations/<owner_id>` - Listar reservas recebidas
  - Retorno: Lista de reservas com informações do locatário

- `PUT /reservation/<id>` - Aprovar/recusar reserva
  - Body: `{ "approved": boolean }`
  - Retorno: `{ "message": string }`

### Locatário (`/api/locatario`)
- `GET /search` - Buscar imóveis disponíveis
  - Query params: `city`, `min_price`, `max_price`, `start_date`, `end_date`
  - Retorno: Lista de imóveis disponíveis

- `POST /reserve` - Realizar reserva
  - Body: `{ "property_id": string, "renter_id": string, "start_date": string, "end_date": string }`
  - Retorno: `{ "message": string, "reservation_id": string }`

- `GET /my-reservations/<user_id>` - Listar minhas reservas
  - Retorno: Lista de reservas com informações do imóvel

- `POST /review` - Criar avaliação
  - Body: `{ "reservation_id": string, "rating": number, "comment": string }`
  - Retorno: `{ "message": string }`

- `GET /property/<property_id>/reviews` - Listar avaliações de um imóvel
  - Retorno: Lista de avaliações com informações do locatário

## Armazenamento de Dados

O sistema utiliza arquivos JSON para armazenamento de dados. Os arquivos são salvos no diretório `data/` e incluem:
- `users.json` - Dados dos usuários
- `properties.json` - Dados dos imóveis
- `reservations.json` - Dados das reservas
- `reviews.json` - Dados das avaliações

## Modelos de Dados

### User
```python
{
    "id": string,
    "name": string,
    "email": string,
    "user_type": "locador" | "locatario"
}
```

### Property
```python
{
    "id": string,
    "title": string,
    "description": string,
    "address": string,
    "price_per_day": number,
    "available_from": string,  # formato: YYYY-MM-DD
    "available_until": string, # formato: YYYY-MM-DD
    "owner_id": string,
    "image_url": string
}
```

### Reservation
```python
{
    "id": string,
    "property_id": string,
    "renter_id": string,
    "start_date": string,  # formato: YYYY-MM-DD
    "end_date": string,    # formato: YYYY-MM-DD
    "approved": boolean
}
```

### Review
```python
{
    "id": string,
    "reservation_id": string,
    "rating": number,  # 1-5
    "comment": string
}
```

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](../LICENSE) para mais detalhes. 