# 🎯 PRÓXIMOS PASSOS - PASSO A PASSO

**Data:** 26 de Julho de 2026 - 23:35  
**Tempo restante:** ~30 horas de férias  
**Objetivo:** Projeto 100% completo e deployado

---

## 🚀 FASE 1: SETUP FRONTEND (30 min) - AGORA!

### Passo 1: Criar projeto React
```bash
npm create vite@latest frontend -- --template react --yes
cd frontend
npm install
```

### Passo 2: Instalar dependências
```bash
npm install socket.io-client axios
```

### Passo 3: Copiar componentes
Você tem estes arquivos já criados:
- `frontend-src-App.jsx` → `src/App.jsx`
- `frontend-src-App.css` → `src/App.css`
- `frontend-src-components-Lobby.jsx` → `src/components/Lobby.jsx`
- `frontend-src-components-Lobby.css` → `src/components/Lobby.css`
- ... (copiar todos os outros também)

```bash
mkdir -p src/components

# Copiar todos os arquivos JSX e CSS para seus lugares
```

### Passo 4: Testar
```bash
npm run dev
```

Você verá: `http://localhost:5173`

**Esperado:** Tela com 3 botões (2, 3, 4 jogadores)

---

## ✅ FASE 2: TESTAR TUDO JUNTO (1-2 horas)

### Terminal 1: Backend
```bash
python run_api.py
```
Esperado: `Uvicorn running on http://0.0.0.0:8000`

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```
Esperado: `http://localhost:5173`

### Terminal 3: Testes
```bash
pytest test_api.py -v
```
Esperado: `14 passed`

### Teste Manual
1. Abrir `http://localhost:5173`
2. Clicar em "4 Jogadores"
3. Deve criar novo jogo
4. Deve mostrar mesa com 4 posições
5. Deve mostrar suas 3 cartas
6. Pode clicar em uma carta para jogar

---

## 🛢️ FASE 3: BANCO DE DADOS (3-4 horas) - VOCÊ FAZ

### Escolher: PostgreSQL vs MongoDB

#### PostgreSQL (Recomendado)
```bash
# Instalar (Windows)
# https://www.postgresql.org/download/windows/

# Depois criar database
createdb trucoengine
```

#### MongoDB (Alternativa)
```bash
# https://www.mongodb.com/try/download/community
```

### Implementar `api/database.py`

Você precisa fazer isso:

```python
# api/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/trucoengine"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class GameDB:
    def save_game(self, game_id: str, game_state: dict):
        """Salvar jogo no banco"""
        # TODO: Implementar
        pass
    
    def load_game(self, game_id: str) -> dict:
        """Carregar jogo do banco"""
        # TODO: Implementar
        pass
    
    def list_games(self):
        """Listar todos os jogos"""
        # TODO: Implementar
        pass
```

### Schema SQL (PostgreSQL)
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
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE moves (
    id SERIAL PRIMARY KEY,
    game_id VARCHAR(36) REFERENCES games(id),
    player_id INT,
    card_played VARCHAR(3),
    timestamp TIMESTAMP DEFAULT NOW()
);
```

### Integrar ao `api/main.py`
```python
from .database import GameDB

db = GameDB()

# Antes de salvar jogo:
db.save_game(game_id, game_state)

# Ao carregar jogo:
game_state = db.load_game(game_id)
```

---

## 🐳 FASE 4: DOCKER (1 hora) - OPCIONAL

### Criar `Dockerfile`
```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run_api.py"]
```

### Criar `docker-compose.yml`
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/trucoengine

  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: trucoengine
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Rodar
```bash
docker-compose up
```

---

## 🧪 FASE 5: TESTES FINAIS (1 hora)

### Checklist
- [ ] Backend rodando: `python run_api.py`
- [ ] Frontend rodando: `npm run dev`
- [ ] Testes passando: `pytest test_api.py -v`
- [ ] Swagger acessível: `http://localhost:8000/docs`
- [ ] Frontend carrega: `http://localhost:5173`
- [ ] Criar jogo funciona
- [ ] Jogar carta funciona
- [ ] Pedir truco funciona
- [ ] Responder truco funciona
- [ ] Placar atualiza
- [ ] 2+ abas sincronizam em tempo real

---

## 🚀 FASE 6: DEPLOY (DEPOIS)

1. Escolher host:
   - Railway
   - Render
   - Heroku
   - AWS/Azure

2. Configurar:
   - Database na nuvem
   - Variáveis de ambiente
   - CORS/Domains
   - SSL/HTTPS

3. Deployar:
   ```bash
   git push heroku main
   ```

---

## ⏱️ CRONOGRAMA REALISTA

```
DIA 1 (HOJE - ~8h restantes):
├─ Setup Vite (30 min)         ✅
├─ Testar Frontend+Backend (1h) ✅
├─ Debug/Fix (1h)              ✅
└─ Banco de dados começo (5h)  ⏳

DIA 2 (AMANHÃ - ~16h):
├─ Finalizar banco dados (2h)  ⏳
├─ Docker setup (1h)           ⏳
├─ Testes integração (2h)      ⏳
├─ Deploy (2h)                 ⏳
└─ Buffer/Polish (7h)          ⏳
```

---

## 📚 REFERÊNCIAS RÁPIDAS

### Instalar PostgreSQL
```bash
# Windows
# https://www.postgresql.org/download/windows/

# macOS
brew install postgresql

# Linux
sudo apt-get install postgresql
```

### Conectar ao DB
```bash
psql -U user -d trucoengine
```

### Instalar SQLAlchemy
```bash
pip install sqlalchemy psycopg2
```

### Deploy rápido
```bash
# Railway (mais fácil)
npm install -g railway
railway login
railway init
railway up
```

---

## 🎯 RESUMO DO QUE FAZER

1. **HOJE (próximas 30 min):**
   ```bash
   npm create vite@latest frontend -- --template react
   cd frontend && npm install socket.io-client axios
   # Copiar componentes React
   npm run dev
   ```

2. **DEPOIS (próxima 1h):**
   ```bash
   # Terminal 1
   python run_api.py
   # Terminal 2
   cd frontend && npm run dev
   # Testar tudo junto
   ```

3. **BANCO (você vai fazer):**
   - Instalar PostgreSQL
   - Criar database
   - Implementar `api/database.py`
   - Testar persistência

4. **FINALIZAR:**
   - Docker (opcional)
   - Deploy
   - Celebrate! 🎉

---

## 💡 DICAS OURO

1. **Salve progresso frequentemente:**
   ```bash
   git add -A
   git commit -m "Feature: Nova funcionalidade"
   ```

2. **Teste localmente ANTES de subir:**
   ```bash
   pytest test_api.py -v
   # Tudo verde? OK para commit
   ```

3. **Use DevTools:**
   - F12 no navegador
   - Ver WebSocket events
   - Debug de UI

4. **Debug backend:**
   ```python
   print(f"DEBUG: {game_state}")
   ```

5. **Slack/Discord:**
   - Compartilhe o link quando deployar
   - Pessoas vão testar para você!

---

## 🏁 FINISH LINE

Você está 70% lá!

**Faltam:**
- Frontend setup (30 min)
- Testes integração (1-2h)
- Banco dados (3-4h)

**Tempo disponível:** ~30h

**Conclusão:** Você acabará com MUITO tempo sobrando! 🎉

---

**Vamos começar?** Próximo passo: `npm create vite...`

Good luck! 🚀
