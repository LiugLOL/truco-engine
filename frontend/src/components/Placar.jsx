import React from 'react';
import './Placar.css';

export default function Placar({ pontos1, pontos2, md3_1, md3_2, trucoValor }) {
  return (
    <div className="placar">
      <div className="score-team">
        <div className="team-name">Time 1</div>
        <div className="team-score">{pontos1}</div>
        <div className="md3">MD3: {md3_1}</div>
      </div>

      <div className="center-info">
        <div className="truco-badge">
          <span className="label">Aposta:</span>
          <span className="value">{trucoValor} pontos</span>
        </div>
      </div>

      <div className="score-team">
        <div className="team-name">Time 2</div>
        <div className="team-score">{pontos2}</div>
        <div className="md3">MD3: {md3_2}</div>
      </div>
    </div>
  );
}
