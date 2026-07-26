"""
Pydantic models for request/response serialization
"""
from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any


class CartaResponse(BaseModel):
    """Card representation"""
    id: str
    nome: str
    
    @staticmethod
    def from_carta(carta):
        return CartaResponse(
            id=carta.id(),
            nome=carta.nomeCarta()
        )


class JogadorResponse(BaseModel):
    """Player representation"""
    nome: str
    mao: List[CartaResponse]
    
    @staticmethod
    def from_jogador(jogador):
        return JogadorResponse(
            nome=jogador.getNome(),
            mao=[CartaResponse.from_carta(carta) for carta in jogador.mao]
        )


class GameResponse(BaseModel):
    """Complete game state"""
    game_id: str
    pontos_time1: int
    pontos_time2: int
    jogadores: List[JogadorResponse]
    vira: Optional[CartaResponse]
    rodadinha_atual: int
    md3_time1: int
    md3_time2: int
    truco_valor_atual: int
    truco_em_andamento: bool
    vitoria: Dict[str, Any]
    
    @staticmethod
    def from_jogo(game_id: str, jogo):
        """Convert Jogo instance to GameResponse"""
        vira = None
        if hasattr(jogo.partida, 'vira') and jogo.partida.vira:
            vira = CartaResponse.from_carta(jogo.partida.vira)
        
        # Get current truco state
        truco_valor = jogo.obter_valor_truco_atual()
        truco_em_andamento = jogo.partida.truco.resposta != "aguardando"
        
        # Check for victory
        vitoria = jogo.checarVitoria()
        
        return GameResponse(
            game_id=game_id,
            pontos_time1=jogo.pontosTime1,
            pontos_time2=jogo.pontosTime2,
            jogadores=[JogadorResponse.from_jogador(j) for j in jogo.jogadores],
            vira=vira,
            rodadinha_atual=jogo.partida.rodadinha_atual,
            md3_time1=jogo.partida.placar_time(1),
            md3_time2=jogo.partida.placar_time(2),
            truco_valor_atual=truco_valor,
            truco_em_andamento=truco_em_andamento,
            vitoria=vitoria
        )


class PlayRequest(BaseModel):
    """Request to play cards"""
    card_indices: List[int]
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"card_indices": [0, 1, 2, 0]}
        }
    )


class TrucoRequest(BaseModel):
    """Request to initiate truco"""
    time_que_pede: int
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"time_que_pede": 1}
        }
    )


class TrucoResponseRequest(BaseModel):
    """Request to respond to truco"""
    time_que_responde: int
    resposta: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {"time_que_responde": 2, "resposta": "aceito"}
        }
    )
