# 🎨 Frontend - Truco Paulista

React frontend for Truco Paulista with WebSocket real-time updates.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- npm or yarn

### Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be at: **http://localhost:5173**

### Build for Production

```bash
npm run build
npm run preview
```

## 📁 Project Structure

```
src/
├── App.jsx              # Main app component
├── App.css              # Global styles
├── main.jsx             # Entry point
└── components/
    ├── Lobby.jsx        # Game creation screen
    ├── Lobby.css
    ├── GameBoard.jsx    # Main game board (4 players)
    ├── GameBoard.css
    ├── HandCards.jsx    # Player's cards
    ├── HandCards.css
    ├── Placar.jsx       # Score board
    ├── Placar.css
    ├── TrucoButtons.jsx # Truco actions
    └── TrucoButtons.css
```

## 🎮 Features

- ✅ Real-time multiplayer with WebSocket
- ✅ Create games with 2-4 players
- ✅ Play cards from your hand
- ✅ Request and respond to truco bets
- ✅ Live score updates
- ✅ Beautiful UI with CSS animations

## 🔌 WebSocket Connection

Connected to backend at: **http://localhost:8000**

Events:
- `join_game` - Join a game
- `play_card` - Play a card
- `request_truco` - Request truco bet
- `respond_truco` - Respond to truco
- `game_state_update` - Receive game state updates

## ⚙️ Configuration

Backend URL: Edit in **App.jsx**

```javascript
const API_URL = 'http://localhost:8000';
const SOCKET_URL = 'http://localhost:8000';
```

## 🎨 Customization

Colors and styles are in **App.css**:

```css
:root {
  --primary: #2c3e50;
  --success: #27ae60;
  --danger: #e74c3c;
  --warning: #f39c12;
  --info: #3498db;
}
```

## 🐛 Troubleshooting

**"Cannot reach API"**
- Ensure backend is running: `python run_api.py`
- Check port 8000 is available

**"WebSocket failed"**
- CORS might be blocked
- Verify URLs in App.jsx

**"Module not found"**
```bash
npm install socket.io-client axios
```

## 📦 Dependencies

- **React 18** - UI framework
- **Vite** - Build tool
- **Socket.io-client** - WebSocket
- **Axios** - HTTP client

## 🚀 Next Steps

1. Run backend: `python run_api.py`
2. Run frontend: `npm run dev`
3. Open http://localhost:5173
4. Enjoy! 🎴
