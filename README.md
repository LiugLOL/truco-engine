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

## 🔲 FASE 2: REST API - EM DESENVOLVIMENTO

### API Structure
- [ ] Estrutura base com Flask/FastAPI
- [ ] Endpoints de game management
- [ ] Endpoints de play actions
- [ ] Serialização JSON de estado do jogo
- [ ] Documentação Swagger/OpenAPI

### Melhorias para API
- [ ] Type hints em todas as classes
- [ ] Métodos to_dict() para serialização
- [ ] Getters/Accessors para estado do jogo
- [ ] Tratamento robusto de erros
- [ ] Validações de entrada

### Deployment
- [ ] Docker container
- [ ] CI/CD pipeline
- [ ] Testes automatizados

---

## 🛠️ Como Usar (Engine)

```python
from jogo import Jogo

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

## 📁 Estrutura

```
truco-engine/
├── carta.py           # Classe Carta
├── baralho.py         # Classe Baralho
├── jogador.py         # Classe Jogador
├── rodadinha.py       # Comparação de cartas (1 rodadinha do MD3)
├── rodada.py          # Gerencia MD3 (3 rodadinhas)
├── truco.py           # Sistema de apostas
├── jogo.py            # Orquestrador principal
└── test_*.py          # Testes
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

## 🚀 Próximos Passos

1. Criar estrutura da REST API
2. Implementar type hints
3. Adicionar serialização JSON
4. Testes de integração com API
5. Deploy
