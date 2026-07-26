"""
FastAPI application for Truco Engine
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
from typing import Dict
from .models import GameResponse, PlayRequest, TrucoRequest, TrucoResponseRequest
from .game_manager import GameManager
from .websocket import attach_socketio

app = FastAPI(
    title="Truco Paulista API",
    description="REST API para o engine de Truco Paulista",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach WebSocket
app = attach_socketio(app)

# Game manager instance
game_manager = GameManager()


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Truco Paulista API is running"}


@app.post("/games", response_model=GameResponse)
def create_game(num_players: int = 4):
    """
    Create a new game
    
    - **num_players**: Number of players (default: 4, must be 2, 3, or 4)
    """
    if not(num_players % 2 == 0):
        raise HTTPException(status_code=400, detail="Number of players must be odd")
    
    game_id = str(uuid.uuid4())
    game = game_manager.create_game(game_id, num_players)
    return GameResponse.from_jogo(game_id, game)


@app.get("/games/{game_id}", response_model=GameResponse)
def get_game(game_id: str):
    """Get current game state"""
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return GameResponse.from_jogo(game_id, game)


@app.get("/games")
def list_games():
    """List all active games"""
    return {"games": list(game_manager.games.keys()), "count": len(game_manager.games)}


@app.post("/games/{game_id}/play")
def play_card(game_id: str, request: PlayRequest):
    """
    Play cards for all players in current round
    
    - **game_id**: Game ID
    - **card_indices**: List of card indices for each player [player0_card, player1_card, ...]
    """
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    try:
        result = game.receberMao(request.card_indices)
        
        # Check for game victory
        victory = game.checarVitoria()
        
        return {
            "success": True,
            "play_result": result,
            "game_state": GameResponse.from_jogo(game_id, game),
            "victory": victory
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/games/{game_id}/truco")
def request_truco(game_id: str, request: TrucoRequest):
    """
    Request truco (bet)
    
    - **game_id**: Game ID
    - **time_que_pede**: Team requesting truco (1 or 2)
    """
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    try:
        result = game.pedir_truco(request.time_que_pede)
        return {
            "success": True,
            "truco_result": result,
            "game_state": GameResponse.from_jogo(game_id, game)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/games/{game_id}/truco/response")
def respond_truco(game_id: str, request: TrucoResponseRequest):
    """
    Respond to truco request
    
    - **game_id**: Game ID
    - **time_que_responde**: Team responding to truco (1 or 2)
    - **resposta**: Response ("aceito" or "recusado")
    """
    game = game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    if request.resposta not in ["aceito", "recusado"]:
        raise HTTPException(status_code=400, detail="Response must be 'aceito' or 'recusado'")
    
    try:
        result = game.responder_truco(request.time_que_responde, request.resposta)
        
        # Check for game victory if truco was accepted
        victory = game.checarVitoria()
        
        return {
            "success": True,
            "truco_response": result,
            "game_state": GameResponse.from_jogo(game_id, game),
            "victory": victory
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/games/{game_id}")
def delete_game(game_id: str):
    """Delete/end a game"""
    if not game_manager.get_game(game_id):
        raise HTTPException(status_code=404, detail="Game not found")
    
    game_manager.delete_game(game_id)
    return {"success": True, "message": f"Game {game_id} deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
