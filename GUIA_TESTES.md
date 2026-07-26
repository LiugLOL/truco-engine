# 🧪 GUIA DE TESTES - Truco Paulista

Como testar cada parte do projeto.

---

## 1️⃣ TESTES DA API

### Rodar todos os testes
```bash
.venv\Scripts\python.exe -m pytest test_api.py -v
```

**Esperado:** 14/14 testes PASSANDO ✅

### Testes específicos
```bash
# Testar apenas criação de jogo
.venv\Scripts\python.exe -m pytest test_api.py::TestGameCreation -v

# Testar apenas gameplay
.venv\Scripts\python.exe -m pytest test_api.py::TestGameplay -v

# Testar apenas truco
.venv\Scripts\python.exe -m pytest test_api.py::TestTruco -v
```

---

## 2️⃣ TESTES MANUAIS COM SWAGGER

### 1. Iniciar servidor
```bash
python run_api.py
```

### 2. Abrir Swagger UI
```
http://localhost:8000/docs
```

### 3. Testar endpoints

**A) Criar jogo**
```
POST /games?num_players=4
Response: game_id (copie este ID)
```

**B) Ver estado**
```
GET /games/{seu_game_id}
Response: Estado completo do jogo
```

**C) Pedir truco**
```
POST /games/{seu_game_id}/truco
Body: {"time_que_pede": 1}
```

**D) Aceitar truco**
```
POST /games/{seu_game_id}/truco/response
Body: {"time_que_responde": 2, "resposta": "aceito"}
```

**E) Jogar rodada**
```
POST /games/{seu_game_id}/play
Body: {"card_indices": [0, 1, 2, 0]}
```

---

## 3️⃣ TESTES COM cURL

### Criar jogo
```bash
curl -X POST "http://localhost:8000/games?num_players=4"
```

### Ver estado
```bash
curl "http://localhost:8000/games/{game_id}"
```

### Pedir truco
```bash
curl -X POST "http://localhost:8000/games/{game_id}/truco" \
  -H "Content-Type: application/json" \
  -d "{\"time_que_pede\": 1}"
```

### Jogar cartas
```bash
curl -X POST "http://localhost:8000/games/{game_id}/play" \
  -H "Content-Type: application/json" \
  -d "{\"card_indices\": [0, 1, 2, 0]}"
```

---

## 4️⃣ TESTES DO WEBSOCKET

### Pré-requisito
- Backend rodando em :8000
- Node.js instalado

### Instalar cliente WebSocket
```bash
npm install -g wscat
```

### Conectar
```bash
wscat -c "ws://localhost:8000/socket.io/?EIO=4&transport=websocket"
```

### Enviar eventos
```json
{"event": "join_game", "data": {"game_id": "seu_game_id"}}
{"event": "play_card", "data": {"game_id": "seu_game_id", "card_index": 0}}
```

---

## 5️⃣ TESTE COMPLETO (Final-to-End)

### Setup
```bash
# Terminal 1: Backend
python run_api.py

# Terminal 2: Frontend (depois)
cd frontend
npm run dev
```

### Teste manual
1. Abrir `http://localhost:5173` em 2 abas
2. Ambas clicam em "4 Jogadores"
3. Primeira aba joga uma carta
4. Segunda aba deve ver atualização em tempo real
5. Teste pedir e responder truco

---

## 6️⃣ TESTES DE STRESS

### Script Python para simular múltiplos jogos
```python
import requests
import time

BASE_URL = "http://localhost:8000"

# Criar 5 jogos simultâneos
games = []
for i in range(5):
    r = requests.post(f"{BASE_URL}/games?num_players=4")
    game_id = r.json()["game_id"]
    games.append(game_id)
    print(f"✓ Game {i+1}: {game_id}")

# Jogar rodadas
for game_id in games:
    for rodada in range(3):
        r = requests.post(
            f"{BASE_URL}/games/{game_id}/play",
            json={"card_indices": [0, 1, 2, 0]}
        )
        print(f"✓ Game {game_id}: Rodada {rodada+1} jogada")
        time.sleep(0.5)
```

---

## 7️⃣ CHECKLIST DE TESTES

### Antes do Deploy

```
BACKEND:
[ ] 14 testes pytest PASSANDO
[ ] API responde em http://localhost:8000
[ ] Swagger acessível em /docs
[ ] CORS habilitado

FRONTEND:
[ ] Vite setup completo
[ ] Componentes renderizam
[ ] WebSocket conecta
[ ] Estado atualiza em tempo real
[ ] 2+ jogadores sincronizam

DATABASE (Quando implementar):
[ ] Jogos salvam no banco
[ ] Jogos carregam do banco
[ ] Reconectar não perde dados

DOCKER (Opcional):
[ ] Docker build bem-sucedido
[ ] docker-compose up funciona
[ ] Todos os serviços online
```

---

## 8️⃣ DEBUGGING

### Ver logs do servidor
```bash
python run_api.py
```

Você verá:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✓ Client connected: sid123
► Card played in game-abc: player sid123 played card 0
📡 State broadcast in game-abc
```

### Ver logs do WebSocket no browser
Abrir DevTools (F12) → Console → Filtrar por "socket"

### Testar conexão
```bash
curl -v http://localhost:8000/
```

---

## 🐛 Troubleshooting Comum

### "Connection refused"
- ✅ Backend rodando? `python run_api.py`
- ✅ Porta 8000 disponível? `netstat -an | findstr 8000`

### "WebSocket connection failed"
- ✅ CORS habilitado no backend?
- ✅ Frontend apontando para URL correta?

### "Game not found (404)"
- ✅ game_id correto?
- ✅ Jogo expirou (memória)?

### "Card index out of bounds"
- ✅ Índices são 0, 1, 2?
- ✅ Jogador tem 3 cartas?

### Testes falhando
```bash
# Limpar cache
rm -rf .pytest_cache

# Rodar novamente
pytest test_api.py -v --tb=short
```

---

## ✅ PRÓXIMO PASSO

Depois que tudo estiver testado e funcionando:

1. Setup Vite com componentes React
2. Testar frontend com backend
3. Implementar banco de dados
4. Docker containerization
5. Deploy em produção!

**Boa sorte!** 🚀
