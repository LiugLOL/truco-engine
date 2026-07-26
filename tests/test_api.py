"""
Tests for Truco API
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestHealthCheck:
    def test_root_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestGameCreation:
    def test_create_game_default(self):
        """Test creating a game with default parameters"""
        response = client.post("/games")
        assert response.status_code == 200
        data = response.json()
        assert "game_id" in data
        assert data["pontos_time1"] == 0
        assert data["pontos_time2"] == 0
        assert len(data["jogadores"]) == 4

    def test_create_game_custom_players(self):
        """Test creating a game with custom number of players"""
        response = client.post("/games?num_players=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["jogadores"]) == 2

    def test_create_game_invalid_players(self):
        """Test creating a game with invalid number of players"""
        response = client.post("/games?num_players=5")
        assert response.status_code == 400


class TestGameState:
    def test_get_game(self):
        """Test getting game state"""
        # Create a game
        create_response = client.post("/games")
        game_id = create_response.json()["game_id"]
        
        # Get the game
        response = client.get(f"/games/{game_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["game_id"] == game_id
        assert data["vitoria"]["acabou"] == False

    def test_get_nonexistent_game(self):
        """Test getting a non-existent game"""
        response = client.get("/games/invalid-game-id")
        assert response.status_code == 404

    def test_list_games(self):
        """Test listing all games"""
        response = client.get("/games")
        assert response.status_code == 200
        data = response.json()
        assert "games" in data
        assert "count" in data


class TestGameplay:
    def test_play_cards(self):
        """Test playing cards in a round"""
        # Create game
        create_response = client.post("/games")
        game_id = create_response.json()["game_id"]
        
        # Play a round
        response = client.post(
            f"/games/{game_id}/play",
            json={"card_indices": [0, 1, 2, 0]}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "play_result" in data
        assert "game_state" in data

    def test_play_invalid_game(self):
        """Test playing on non-existent game"""
        response = client.post(
            "/games/invalid-id/play",
            json={"card_indices": [0, 1, 2, 0]}
        )
        assert response.status_code == 404


class TestTruco:
    def test_request_truco(self):
        """Test requesting truco"""
        # Create game
        create_response = client.post("/games")
        game_id = create_response.json()["game_id"]
        
        # Request truco
        response = client.post(
            f"/games/{game_id}/truco",
            json={"time_que_pede": 1}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True

    def test_respond_truco_accept(self):
        """Test accepting truco"""
        # Create game
        create_response = client.post("/games")
        game_id = create_response.json()["game_id"]
        
        # Request truco
        client.post(
            f"/games/{game_id}/truco",
            json={"time_que_pede": 1}
        )
        
        # Accept truco
        response = client.post(
            f"/games/{game_id}/truco/response",
            json={"time_que_responde": 2, "resposta": "aceito"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True

    def test_respond_truco_invalid_response(self):
        """Test invalid truco response"""
        # Create game
        create_response = client.post("/games")
        game_id = create_response.json()["game_id"]
        
        # Try invalid response
        response = client.post(
            f"/games/{game_id}/truco/response",
            json={"time_que_responde": 2, "resposta": "invalido"}
        )
        assert response.status_code == 400


class TestGameDeletion:
    def test_delete_game(self):
        """Test deleting a game"""
        # Create game
        create_response = client.post("/games")
        game_id = create_response.json()["game_id"]
        
        # Verify it exists
        response = client.get(f"/games/{game_id}")
        assert response.status_code == 200
        
        # Delete it
        response = client.delete(f"/games/{game_id}")
        assert response.status_code == 200
        assert response.json()["success"] == True
        
        # Verify it's gone
        response = client.get(f"/games/{game_id}")
        assert response.status_code == 404

    def test_delete_nonexistent_game(self):
        """Test deleting non-existent game"""
        response = client.delete("/games/invalid-id")
        assert response.status_code == 404


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
