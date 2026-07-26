# 🚀 Plano de Conclusão - Truco Paulista (2 dias de férias)

## Status Atual
✅ Engine completo
✅ API REST funcional (14/14 testes passando)
⏳ Faltam: WebSocket, Frontend, Banco de Dados, Docker

---

## 📋 PLANO DETALHADO

### FASE 1: WebSocket (2-3 horas) - PRIORIDADE ALTA
**Por que?** Multiplayer real-time sem polling

#### O que fazer:
- [ ] Instalar `python-socketio` e `python-socketio[asyncio_client]`
- [ ] Criar arquivo `api/websocket.py` com handlers:
  - `@sio.on('connect')` → Jogador conecta
  - `@sio.on('play_card', namespace='/games/{game_id}')` → Jogador joga
  - `@sio.on('request_truco')` → Pedir truco
  - `@sio.emit('game_state')` → Broadcast estado para todos
- [ ] Integrar ao `api/main.py`
- [ ] Testar com 2 clientes simultâneos

#### Tecnologia:
```
WebSocket = Socket bidirecional em tempo real
HTTP = Unidirecional (client pede, server responde)
```

---

### FASE 2: Banco de Dados - VOCÊ FARÁ DEPOIS
**Deixar pronto para você conectar:**

#### Opções:
1. **PostgreSQL** (melhor para produção)
   - Arquivo SQL: `db/init.sql` (criar structure)
   - SQLAlchemy ORM em `api/database.py`

2. **MongoDB** (mais flexível, mais fácil)
   - Motor async em `api/database.py`

#### Structure para PostgreSQL:
```sql
CREATE TABLE games (
  id VARCHAR(36) PRIMARY KEY,
  player1 VARCHAR(100),
  player2 VARCHAR(100),
  player3 VARCHAR(100),
  player4 VARCHAR(100),
  team1_points INT DEFAULT 0,
  team2_points INT DEFAULT 0,
  game_state JSONB,
  started_at TIMESTAMP,
  ended_at TIMESTAMP
);

CREATE TABLE moves (
  id SERIAL PRIMARY KEY,
  game_id VARCHAR(36) REFERENCES games(id),
  player_id INT,
  card_played VARCHAR(3),
  timestamp TIMESTAMP
);
```

#### Arquivo que você vai criar:
```python
# api/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost:5432/trucoengine"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def save_game(game_id, game_state):
    # Você implementa aqui

def load_game(game_id):
    # Você implementa aqui
```

---

### FASE 3: Frontend React (4-5 horas) - PRIORIDADE ALTA

#### Structure:
```
frontend/
├── src/
│   ├── components/
│   │   ├── GameBoard.jsx      ← Main component
│   │   ├── HandCards.jsx      ← Cards do jogador
│   │   ├── OpponentCards.jsx  ← Cards dos opponents (viradas)
│   │   ├── Placar.jsx         ← Pontuação
│   │   └── TrucoButtons.jsx   ← Pedir/Responder truco
│   ├── hooks/
│   │   ├── useSocket.js       ← WebSocket logic
│   │   └── useGame.js         ← Game state
│   ├── App.jsx
│   └── index.css
├── public/
│   └── index.html
└── package.json
```

#### Componentes principais:

**1. App.jsx** - Tela inicial
```jsx
// Cria novo jogo
// Mostra lobby esperando players
```

**2. GameBoard.jsx** - Jogo em progresso
```jsx
// Layout de 4 posições (4 jogadores em uma mesa)
// Cartas na mesa da rodadinha
// Placar MD3 e pontos
```

**3. HandCards.jsx** - Mão do jogador
```jsx
// 3 cartas (clicáveis para jogar)
// Mostrar ID e nome (ex: "7P - 7 de paus")
```

**4. Placar.jsx** - Pontuação
```jsx
// Time 1: X pontos
// Time 2: Y pontos
// MD3: X-Y
// Valor truco: Z
```

**5. TrucoButtons.jsx** - Ações
```jsx
// Se é sua vez e nenhum truco:
//   [PEDIR TRUCO]
// Se tem truco aberto:
//   [ACEITAR] [RECUSAR]
```

#### Com WebSocket:
```javascript
// Conecta ao servidor
const socket = io('http://localhost:8000');

// Recebe atualizações em tempo real
socket.on('game_state', (gameState) => {
  // Atualiza interface
});

// Envia ação
socket.emit('play_card', {game_id, card_index});
```

---

### FASE 4: Docker (1-2 horas) - NICE TO HAVE

#### Dockerfile
```dockerfile
FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run_api.py"]
```

#### docker-compose.yml
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: senha
      POSTGRES_DB: trucoengine
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## ⏱️ CRONOGRAMA (2 DIAS = 16 HORAS)

| Fase | Tempo | Status |
|------|-------|--------|
| 1. WebSocket | 3h | TODO |
| 2. Frontend React | 5h | TODO |
| 3. Testes integração | 2h | TODO |
| 4. Docker | 2h | NICE |
| **BANCO (sua parte)** | **? horas** | **SUA RESPONSABILIDADE** |

---

## 🎯 ORDEM DE EXECUÇÃO

### DIA 1 (Hoje)
```
1. Implementar WebSocket (3h)
2. Começar Frontend React (3h)
3. Testes básicos WebSocket+Frontend (1h)
```

### DIA 2 (Amanhã)
```
1. Finalizar Frontend (2h)
2. Testes integração (2h)
3. Docker (1h)
4. Troubleshooting (flexível)
```

### DEPOIS (Você faz)
```
1. Escolher banco (PostgreSQL/MongoDB)
2. Criar schema
3. Implementar `api/database.py`
4. Testar integração
5. Deploy
```

---

## 📦 PRÓXIMAS DEPENDÊNCIAS A INSTALAR

```bash
pip install python-socketio python-socketio[asyncio_client]
pip install aiofiles  # Para arquivos async

# Frontend (Node.js)
npm create vite@latest frontend -- --template react
npm install socket.io-client axios
```

---

## 🚀 COMEÇAMOS?

Qual fase você quer que eu comece?

1. ✨ **WebSocket agora** (recomendado - a base do multiplayer)
2. 🎨 **Frontend React** (visual rápido)
3. 🐳 **Docker** (setup produção)
