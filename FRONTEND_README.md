# 🎨 Frontend React - Truco Paulista

Frontend em React para o Truco Paulista com WebSocket em tempo real.

## 🚀 Setup Rápido

### 1. Instalar Node.js
Se ainda não tem: https://nodejs.org (versão 16+)

### 2. Criar projeto React com Vite
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

### 3. Instalar dependências
```bash
npm install socket.io-client axios
```

### 4. Copiar componentes
```bash
# Copiar arquivos de src/ para frontend/src/components/
# Copiar App.jsx para frontend/src/
# Copiar App.css para frontend/src/
# etc...
```

### 5. Rodar frontend
```bash
npm run dev
```

Frontend estará em: **http://localhost:5173**

---

## 📁 Estrutura de Arquivos

```
frontend/
├── src/
│   ├── components/
│   │   ├── GameBoard.jsx
│   │   ├── GameBoard.css
│   │   ├── HandCards.jsx
│   │   ├── HandCards.css
│   │   ├── Lobby.jsx
│   │   ├── Lobby.css
│   │   ├── Placar.jsx
│   │   ├── Placar.css
│   │   ├── TrucoButtons.jsx
│   │   └── TrucoButtons.css
│   ├── App.jsx
│   ├── App.css
│   └── main.jsx
├── index.html
├── vite.config.js
└── package.json
```

---

## 🎮 Como Usar

### 1. Rodar Backend
```bash
# Terminal 1
cd ..  # Volta para truco-engine
python run_api.py
```

API estará em: **http://localhost:8000**

### 2. Rodar Frontend
```bash
# Terminal 2
cd frontend
npm run dev
```

Frontend estará em: **http://localhost:5173**

### 3. Abrir no Browser
```
http://localhost:5173
```

---

## 🔌 WebSocket Eventos

### Cliente envia:
- `join_game` → Entrar em uma partida
- `play_card` → Jogar uma carta
- `request_truco` → Pedir truco
- `respond_truco` → Responder truco
- `broadcast_state` → Atualizar estado para todos

### Cliente recebe:
- `game_state_update` → Estado do jogo foi atualizado
- `truco_requested` → Alguém pediu truco
- `truco_responded` → Alguém respondeu ao truco
- `player_joined` → Novo jogador entrou
- `player_disconnected` → Jogador saiu
- `error` → Erro na operação

---

## 🔧 Configuração de URL

Se mudar a porta do backend, editar em **App.jsx**:

```javascript
const API_URL = 'http://localhost:8000';
const SOCKET_URL = 'http://localhost:8000';
```

---

## 📦 Dependências

- **React 18+** - Framework UI
- **Vite** - Build tool rápido
- **Socket.io-client** - WebSocket
- **Axios** - HTTP requests

---

## 🎨 Customização

### Cores
Editar em **App.css**:
```css
:root {
  --primary: #2c3e50;
  --success: #27ae60;
  --danger: #e74c3c;
  /* ... */
}
```

### Componentes
Cada componente é independente:
- `GameBoard.jsx` → Tabuleiro principal
- `Lobby.jsx` → Tela inicial
- `HandCards.jsx` → Cartas da mão
- `Placar.jsx` → Placar
- `TrucoButtons.jsx` → Botões de ação

---

## 🐛 Troubleshooting

### "Cannot reach API"
- Certifique-se de que o backend está rodando em :8000
- Verifique se as URLs em App.jsx estão corretas

### "WebSocket connection failed"
- CORS pode estar bloqueando
- Certifique-se de que CORSMiddleware está habilitado em main.py

### "Module not found"
```bash
npm install socket.io-client axios
```

---

## 🚀 Build para Produção

```bash
npm run build
```

Arquivos otimizados estarão em **dist/**

---

## 📝 Próximas Melhorias

- [ ] Animações de cartas
- [ ] Som
- [ ] Notificações
- [ ] Histórico de jogadas
- [ ] Estatísticas
- [ ] Chat entre jogadores
- [ ] Seletor de personagens

---

**Divirta-se!** 🎉
