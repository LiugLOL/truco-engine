import React from 'react';
import './GameBoard.css';
import HandCards from './HandCards';
import Placar from './Placar';
import TrucoButtons from './TrucoButtons';

export default function GameBoard({
  gameState,
  playerPosition,
  onPlayCard,
  onRequestTruco,
  onRespondTruco,
}) {
  if (!gameState) {
    return <div className="loading">Carregando jogo...</div>;
  }

  const players = gameState.jogadores || [];
  const currentPlayer = players[playerPosition];

  return (
    <div className="game-board">
      <Placar
        pontos1={gameState.pontos_time1}
        pontos2={gameState.pontos_time2}
        md3_1={gameState.md3_time1}
        md3_2={gameState.md3_time2}
        trucoValor={gameState.truco_valor_atual}
      />

      {/* Mesa de jogo (4 posições) */}
      <div className="mesa">
        {/* Posição topo (Opponent) */}
        <div className="player-position top">
          <div className="player-name">{players[2]?.nome || 'Vazio'}</div>
          <div className="cards-display">Cartas viradas</div>
        </div>

        {/* Posição esquerda (Opponent) */}
        <div className="player-position left">
          <div className="player-name">{players[3]?.nome || 'Vazio'}</div>
          <div className="cards-display">Cartas viradas</div>
        </div>

        {/* Centro (Cartas jogadas) */}
        <div className="center">
          <div className="rodadinha-info">
            Rodadinha {gameState.rodadinha_atual} de 3
          </div>
          <div className="table-cards">
            {/* Aqui vão as cartas jogadas na mesa */}
          </div>
        </div>

        {/* Posição direita (Opponent) */}
        <div className="player-position right">
          <div className="player-name">{players[1]?.nome || 'Vazio'}</div>
          <div className="cards-display">Cartas viradas</div>
        </div>

        {/* Posição inferior (Você) */}
        <div className="player-position bottom you">
          <div className="player-name">{currentPlayer?.nome || 'Você'}</div>
          <HandCards
            cards={currentPlayer?.mao || []}
            onPlayCard={onPlayCard}
          />
        </div>
      </div>

      {/* Botões de ação */}
      <TrucoButtons
        trucoEmAndamento={gameState.truco_em_andamento}
        onRequestTruco={onRequestTruco}
        onRespondTruco={onRespondTruco}
      />

      {/* Debug info */}
      {process.env.NODE_ENV === 'development' && (
        <div className="debug">
          <p>Game ID: {gameState.game_id}</p>
          <p>Posição: {playerPosition}</p>
        </div>
      )}
    </div>
  );
}
