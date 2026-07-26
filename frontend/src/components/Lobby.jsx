import React from 'react';
import './Lobby.css';

export default function Lobby({ onCreateGame, loading }) {
  return (
    <div className="lobby">
      <div className="lobby-card">
        <h2>Bem-vindo ao Truco!</h2>
        <p>Escolha o número de jogadores para começar:</p>
        
        <div className="button-group">
          <button
            onClick={() => onCreateGame(2)}
            disabled={loading}
            className="btn btn-primary"
          >
            👥 2 Jogadores
          </button>
          <button
            onClick={() => onCreateGame(3)}
            disabled={loading}
            className="btn btn-primary"
          >
            👥👥 3 Jogadores
          </button>
          <button
            onClick={() => onCreateGame(4)}
            disabled={loading}
            className="btn btn-primary"
          >
            👥👥👥 4 Jogadores
          </button>
        </div>

        {loading && <p className="loading">Criando jogo...</p>}
      </div>

      <div className="info">
        <h3>🎮 Como Jogar</h3>
        <ul>
          <li>Cada jogador recebe 3 cartas</li>
          <li>Ganhe rodadas comparando cartas</li>
          <li>Primeiro time com 12 pontos vence!</li>
          <li>Use truco para aumentar a aposta</li>
        </ul>
      </div>
    </div>
  );
}
