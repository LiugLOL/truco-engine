"""
Game manager to handle multiple game instances
"""
from typing import Dict, Optional
from engine.jogo import Jogo


class GameManager:
    """
    Manages multiple game instances.
    In production, this would connect to a database instead of in-memory storage.
    """
    
    def __init__(self):
        self.games: Dict[str, Jogo] = {}
    
    def create_game(self, game_id: str, num_players: int = 4) -> Jogo:
        """Create a new game instance"""
        if game_id in self.games:
            raise ValueError(f"Game {game_id} already exists")
        
        game = Jogo(num_players)
        self.games[game_id] = game
        return game
    
    def get_game(self, game_id: str) -> Optional[Jogo]:
        """Get a game instance by ID"""
        return self.games.get(game_id)
    
    def delete_game(self, game_id: str) -> bool:
        """Delete a game instance"""
        if game_id in self.games:
            del self.games[game_id]
            return True
        return False
    
    def game_exists(self, game_id: str) -> bool:
        """Check if a game exists"""
        return game_id in self.games
