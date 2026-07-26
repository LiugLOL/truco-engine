import React from 'react';
import './TrucoButtons.css';

export default function TrucoButtons({
  trucoEmAndamento,
  onRequestTruco,
  onRespondTruco,
}) {
  return (
    <div className="truco-buttons">
      {!trucoEmAndamento ? (
        <button
          className="btn btn-truco btn-primary"
          onClick={onRequestTruco}
        >
          📢 Pedir Truco
        </button>
      ) : (
        <div className="button-group">
          <button
            className="btn btn-success"
            onClick={() => onRespondTruco('aceito')}
          >
            ✓ Aceitar
          </button>
          <button
            className="btn btn-danger"
            onClick={() => onRespondTruco('recusado')}
          >
            ✗ Recusar
          </button>
        </div>
      )}
    </div>
  );
}
