import React from 'react';
import './HandCards.css';

export default function HandCards({ cards, onPlayCard }) {
  return (
    <div className="hand-cards">
      {cards.map((card, index) => (
        <button
          key={index}
          className="card"
          onClick={() => onPlayCard(index)}
          title={card.nome}
        >
          <div className="card-id">{card.id}</div>
          <div className="card-name">{card.nome.split(' de ')[0]}</div>
        </button>
      ))}
    </div>
  );
}
