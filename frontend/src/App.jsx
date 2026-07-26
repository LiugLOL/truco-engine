import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import axios from 'axios';
import './App.css';
import GameBoard from './components/GameBoard';
import Lobby from './components/Lobby';

const API_URL = 'http://localhost:8000';
const SOCKET_URL = 'http://localhost:8000';

export default function App() {
  const [socket, setSocket] = useState(null);
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [playerPosition, setPlayerPosition] = useState(0); // 0, 1, 2, or 3
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize Socket.IO
  useEffect(() => {
    const newSocket = io(SOCKET_URL, {
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5,
    });

    newSocket.on('connect', () => {
      console.log('✓ Connected to server');
    });

    newSocket.on('game_state_update', (state) => {
      console.log('📡 State update received');
      setGameState(state);
    });

    newSocket.on('truco_requested', (data) => {
      console.log('📣 Truco requested:', data);
    });

    newSocket.on('player_joined', (data) => {
      console.log('👤 Player joined:', data);
    });

    newSocket.on('error', (data) => {
      console.error('❌ Error:', data);
      setError(data.message);
    });

    setSocket(newSocket);

    return () => {
      newSocket.disconnect();
    };
  }, []);

  const createGame = async (numPlayers = 4) => {
    try {
      setLoading(true);
      setError(null);

      // Create game via HTTP
      const response = await axios.post(`${API_URL}/games?num_players=${numPlayers}`);
      const newGameId = response.data.game_id;

      setGameId(newGameId);
      setGameState(response.data);

      // Join game via WebSocket
      if (socket) {
        socket.emit('join_game', { game_id: newGameId });
        setPlayerPosition(0); // You're always player 0
      }

      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const playCard = async (cardIndex) => {
    if (!gameId || !socket) return;

    try {
      // Play card via HTTP
      const response = await axios.post(`${API_URL}/games/${gameId}/play`, {
        card_indices: [cardIndex, 0, 0, 0], // TODO: Get other players' choices
      });

      // Broadcast via WebSocket
      socket.emit('broadcast_state', {
        game_id: gameId,
        game_state: response.data.game_state,
      });

      setGameState(response.data.game_state);

      // Check for victory
      if (response.data.victory.acabou) {
        alert(`🎉 Time ${response.data.victory.vencedor} venceu!`);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const requestTruco = async () => {
    if (!gameId || !socket) return;

    try {
      // Request truco via HTTP
      const response = await axios.post(`${API_URL}/games/${gameId}/truco`, {
        time_que_pede: (playerPosition % 2) + 1, // Teams: 0,2 -> Team1; 1,3 -> Team2
      });

      // Notify others via WebSocket
      socket.emit('request_truco', {
        game_id: gameId,
        time: (playerPosition % 2) + 1,
      });

      setGameState(response.data.game_state);
    } catch (err) {
      setError(err.message);
    }
  };

  const respondTruco = async (resposta) => {
    if (!gameId || !socket) return;

    try {
      // Respond via HTTP
      const response = await axios.post(`${API_URL}/games/${gameId}/truco/response`, {
        time_que_responde: (playerPosition % 2) + 1,
        resposta,
      });

      // Notify others via WebSocket
      socket.emit('respond_truco', {
        game_id: gameId,
        resposta,
      });

      setGameState(response.data.game_state);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>🎴 Truco Paulista Online</h1>
      </header>

      {error && <div className="error-banner">{error}</div>}

      {!gameId ? (
        <Lobby onCreateGame={createGame} loading={loading} />
      ) : (
        <GameBoard
          gameState={gameState}
          playerPosition={playerPosition}
          onPlayCard={playCard}
          onRequestTruco={requestTruco}
          onRespondTruco={respondTruco}
        />
      )}
    </div>
  );
}
