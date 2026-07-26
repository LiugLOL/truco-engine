# 🎴 Truco Paulista Engine

Projeto de férias: Engine de Truco Paulista para uso em web/API

## 🎯 Objetivos

- ✅ Implementar todas as regras de Truco Paulista
- ✅ Tornar jogável e funcional
- 🔲 Criar REST API (em progresso)
- 🔲 Integrar com frontend web

---

## ✅ FASE 1: Engine Core - COMPLETO

### Engine
- [x] Implementação do baralho
- [x] Implementação das cartas
- [x] Sistema de jogadores
- [x] Implementação da hierarquia das cartas
- [x] Implementação das manilhas
- [x] Detecção de empate
- [x] Sistema de distribuição de cartas
- [x] Sistema de rodadas (MD3)
- [x] Controle de pontuação da rodada
- [x] Controle de pontuação da partida (12 pontos)
- [x] Criação automática de nova rodada

### Truco & Apostas
- [x] Implementar Truco (1→3→6→9→12)
- [x] Implementar pedido de Truco
- [x] Implementar aceitação/recusa do Truco
- [x] Implementar aumento de aposta
- [x] Implementar mão de 11
- [x] Implementar mão de ferro (11x11)

### Tie-Breaking (Empardamento)
- [x] Detecção de cartas iguais (não-manilhas)
- [x] Sistema de descarte de empardalas
- [x] Comparação de cartas subsequentes
- [x] Briga de naipe em manilhas
- [x] Controle de ordem de jogo por rodadinha

### Testes
- [x] Test suite completo (test_final.py)
- [x] Testes de tie-breaking (test_fase2.py)
- [x] Testes de Truco (test_truco_completo.py)

---

## ✅ FASE 2: REST API - EM DESENVOLVIMENTO

### API Structure
- [x] Estrutura base com FastAPI
- [x] Endpoints de game management
- [x] Endpoints de play actions
- [x] Serialização JSON de estado do jogo
- [x] Documentação Swagger/OpenAPI

### Melhorias para API
- [x] Pydantic models para serialização
- [x] Getters/Accessors para estado do jogo
- [x] Tratamento robusto de erros
- [x] Validações de entrada
- [x] Game manager para múltiplas partidas

### Deployment
- [ ] Docker container
- [ ] CI/CD pipeline
- [x] Testes automatizados (pytest)

---

## 🛠️ Como Usar (Engine)

```python
from engine.jogo import Jogo

# Criar jogo com 4 jogadores (2 times)
game = Jogo(4)

# Pedir truco
game.pedir_truco(time=1)

# Responder ao truco
game.responder_truco(time=2, resposta="aceito")

# Jogar cartas (indices das cartas)
resultado = game.receberMao([0, 0, 0, 0])

# Verificar vitória
vitoria = game.checarVitoria()
```

---

---

## 📁 Estrutura do Projeto

```
truco-engine/
├── engine/                  ✅ Core game logic
│   ├── jogo.py
│   ├── rodada.py
│   ├── rodadinha.py
│   ├── truco.py
│   ├── jogador.py
│   ├── carta.py
│   ├── baralho.py
│   └── tests/              (Moved to tests/)
├── api/                    ✅ REST API + WebSocket
│   ├── main.py            (+ WebSocket)
│   ├── models.py
│   ├── game_manager.py
│   ├── websocket.py
│   └── database.py        (You'll implement)
├── tests/                 ✅ All tests
│   ├── test_api.py        (14 tests passing)
│   ├── test_final.py
│   ├── test_fase2.py
│   ├── test_truco_completo.py
│   ├── test_empardamento.py
│   └── README.md
├── frontend/              ✅ React app
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── components/
│   │       ├── GameBoard.jsx
│   │       ├── HandCards.jsx
│   │       ├── Lobby.jsx
│   │       ├── Placar.jsx
│   │       └── TrucoButtons.jsx
│   ├── vite.config.js
│   ├── package.json
│   ├── index.html
│   ├── README.md
│   └── .gitignore
├── run_api.py             ✅ Start server
├── requirements.txt       ✅ Dependencies
├── pytest.ini             ✅ Test config
└── Documentation/
    ├── API.md
    ├── FRONTEND_README.md
    ├── PLANO_CONCLUSAO.md
    ├── GUIA_TESTES.md
    ├── PROXIMOS_PASSOS.md
    └── RESUMO_EXECUTIVO.md
```

---

## 🎮 Regras Implementadas

### Truco Paulista
- **Progressão de apostas:** 1 → 3 → 6 → 9 → 12
- **MD3:** Melhor de 3 rodadinhas
- **Empardamento:** Cartas iguais (não-manilhas) ficam empardalas
- **Manilhas:** Definidas pela vira (flip card)
- **Briga de naipe:** Paus > Copas > Espadas > Ouros
- **Mão de 11:** Bloqueia truco quando 11x<11
- **Mão de Ferro:** Bloqueia truco quando 11x11
- **Vitória:** Primeiro time a 12 pontos

---

## 🎮 REST API (NOVA!)

Agora há uma REST API completa com FastAPI!

### Quick Start
```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar servidor
python run_api.py

# Acessar documentação interativa
http://localhost:8000/docs
```

### Endpoints principais
- `POST /games` - Criar novo jogo
- `GET /games/{game_id}` - Obter estado do jogo
- `POST /games/{game_id}/play` - Jogar rodada
- `POST /games/{game_id}/truco` - Pedir truco
- `POST /games/{game_id}/truco/response` - Responder truco

Veja [API.md](API.md) para documentação completa.

---

## 🚀 Próximos Passos

1. ✅ Criar estrutura da REST API
2. [ ] Banco de dados (PostgreSQL/MongoDB)
3. [ ] WebSocket para tempo real
4. [ ] Autenticação
5. [ ] Docker + CI/CD
6. [ ] Deploy em produção
