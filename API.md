# 🎴 API REST - Truco Paulista

Documentação completa da REST API para o engine de Truco Paulista.

---

## 🚀 Quick Start

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Rodar o servidor
```bash
python run_api.py
```

O servidor estará disponível em `http://localhost:8000`

### 3. Acessar documentação interativa
```
http://localhost:8000/docs
```

---

## 📚 Endpoints

### Health Check
```http
GET /
```
Verifica se a API está rodando.

**Response:**
```json
{
  "status": "ok",
  "message": "Truco Paulista API is running"
}
```

---

### Criar Jogo
```http
POST /games
```

**Query Parameters:**
- `num_players` (int): Número de jogadores (2, 3 ou 4) - default: 4

**Response:**
```json
{
  "game_id": "550e8400-e29b-41d4-a716-446655440000",
  "pontos_time1": 0,
  "pontos_time2": 0,
  "jogadores": [
    {
      "nome": "Jogador 0",
      "mao": [
        {"id": "7P", "nome": "7 de paus"},
        {"id": "KE", "nome": "K de espadas"},
        {"id": "AC", "nome": "A de copas"}
      ]
    },
    // ... outros jogadores
  ],
  "vira": {"id": "3O", "nome": "3 de ouros"},
  "rodadinha_atual": 1,
  "md3_time1": 0,
  "md3_time2": 0,
  "truco_valor_atual": 1,
  "truco_em_andamento": false,
  "vitoria": {"acabou": false}
}
```

---

### Obter Estado do Jogo
```http
GET /games/{game_id}
```

**Response:** Mesmo formato do CREATE /games

---

### Listar Jogos Ativos
```http
GET /games
```

**Response:**
```json
{
  "games": ["game_id_1", "game_id_2"],
  "count": 2
}
```

---

### Jogar Cartas
```http
POST /games/{game_id}/play
```

**Request Body:**
```json
{
  "card_indices": [0, 1, 2, 0]
}
```

Cada índice corresponde à carta que cada jogador joga (na ordem dos jogadores).
- Jogador 0 joga carta no índice 0
- Jogador 1 joga carta no índice 1
- Jogador 2 joga carta no índice 2
- Jogador 3 joga carta no índice 0

**Response:**
```json
{
  "success": true,
  "play_result": {
    "acabou": false,
    "time_vencedor": 0,
    "resultado": "time1",
    "md3_time1": 1,
    "md3_time2": 0,
    "pontos_time1": 1,
    "pontos_time2": 0,
    "valor_aposta": 1
  },
  "game_state": { /* estado atual do jogo */ },
  "victory": {"acabou": false}
}
```

---

### Pedir Truco
```http
POST /games/{game_id}/truco
```

**Request Body:**
```json
{
  "time_que_pede": 1
}
```

Time 1 ou 2 que está pedindo truco.

**Response:**
```json
{
  "success": true,
  "truco_result": {
    "pode_pedir": true,
    "valor_novo": 3,
    "resultado": "pedido_realizado"
  },
  "game_state": { /* estado atual */ }
}
```

---

### Responder ao Truco
```http
POST /games/{game_id}/truco/response
```

**Request Body:**
```json
{
  "time_que_responde": 2,
  "resposta": "aceito"
}
```

- `resposta`: `"aceito"` ou `"recusado"`

Se **recusado**: Time que pediu ganha pontos automaticamente.
Se **aceito**: Jogo continua com nova aposta.

**Response:**
```json
{
  "success": true,
  "truco_response": {
    "resultado": "aceito",
    "valor_atual": 3
  },
  "game_state": { /* estado atual */ },
  "victory": {"acabou": false}
}
```

---

### Deletar Jogo
```http
DELETE /games/{game_id}
```

**Response:**
```json
{
  "success": true,
  "message": "Game {game_id} deleted"
}
```

---

## 🎮 Exemplo de Fluxo Completo

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Criar jogo
response = requests.post(f"{BASE_URL}/games")
game_id = response.json()["game_id"]

# 2. Pedir truco (Time 1)
requests.post(f"{BASE_URL}/games/{game_id}/truco", 
              json={"time_que_pede": 1})

# 3. Aceitar truco (Time 2)
requests.post(f"{BASE_URL}/games/{game_id}/truco/response",
              json={"time_que_responde": 2, "resposta": "aceito"})

# 4. Jogar rodada
result = requests.post(f"{BASE_URL}/games/{game_id}/play",
                       json={"card_indices": [0, 1, 2, 0]})

# 5. Verificar vitória
game_state = requests.get(f"{BASE_URL}/games/{game_id}").json()
if game_state["vitoria"]["acabou"]:
    print(f"Time {game_state['vitoria']['vencedor']} venceu!")
```

---

## 🔍 Estrutura de Dados

### Carta
```json
{
  "id": "7P",
  "nome": "7 de paus"
}
```

### Jogador
```json
{
  "nome": "Jogador 0",
  "mao": [
    {"id": "7P", "nome": "7 de paus"},
    {"id": "KE", "nome": "K de espadas"}
  ]
}
```

### Game State (GameResponse)
```json
{
  "game_id": "...",
  "pontos_time1": 0,
  "pontos_time2": 0,
  "jogadores": [...],
  "vira": {"id": "3O", "nome": "3 de ouros"},
  "rodadinha_atual": 1,
  "md3_time1": 0,
  "md3_time2": 0,
  "truco_valor_atual": 1,
  "truco_em_andamento": false,
  "vitoria": {"acabou": false}
}
```

---

## 🛠️ Usar o Swagger/OpenAPI

A documentação interativa fica em:
```
http://localhost:8000/docs
```

Você pode:
- Ver todos os endpoints
- Ler a documentação
- Testar requisições diretamente
- Ver exemplos de response

---

## 📝 Status Codes

| Código | Significado |
|--------|------------|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 404 | Game não encontrado |
| 500 | Erro no servidor |

---

## 🚀 Próximas Melhorias

- [ ] Banco de dados (PostgreSQL/MongoDB)
- [ ] Autenticação e autorização
- [ ] WebSocket para tempo real
- [ ] Rate limiting
- [ ] Logging e monitoring
- [ ] Testes automatizados
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

## 📖 Regras de Truco Implementadas

- ✅ Progressão de apostas: 1 → 3 → 6 → 9 → 12
- ✅ MD3: Melhor de 3 rodadinhas
- ✅ Empardamento: Cartas iguais (não-manilhas) ficam empardalas
- ✅ Manilhas: Definidas pela vira
- ✅ Briga de naipe: Paus > Copas > Espadas > Ouros
- ✅ Mão de 11: Bloqueia truco quando 11x<11
- ✅ Mão de Ferro: Bloqueia truco quando 11x11
- ✅ Vitória: Primeiro time a 12 pontos
