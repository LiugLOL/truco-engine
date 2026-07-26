"""
Example usage of the Truco API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def example_game_flow():
    """Example of a complete game flow"""
    
    # 1. Create a new game
    print("1. Creating a new game...")
    response = requests.post(f"{BASE_URL}/games", params={"num_players": 4})
    game_data = response.json()
    game_id = game_data["game_id"]
    print(f"   ✓ Game created: {game_id}")
    print(f"   State: {json.dumps(game_data, indent=2, ensure_ascii=False)}")
    
    # 2. Get game state
    print("\n2. Fetching game state...")
    response = requests.get(f"{BASE_URL}/games/{game_id}")
    game_state = response.json()
    print(f"   ✓ Current scores - Time 1: {game_state['pontos_time1']} | Time 2: {game_state['pontos_time2']}")
    print(f"   Players: {[j['nome'] for j in game_state['jogadores']]}")
    
    # 3. Request truco (Time 1)
    print("\n3. Team 1 requesting truco...")
    response = requests.post(
        f"{BASE_URL}/games/{game_id}/truco",
        json={"time_que_pede": 1}
    )
    print(f"   ✓ Truco requested")
    
    # 4. Respond to truco (Time 2)
    print("\n4. Team 2 responding to truco...")
    response = requests.post(
        f"{BASE_URL}/games/{game_id}/truco/response",
        json={"time_que_responde": 2, "resposta": "aceito"}
    )
    print(f"   ✓ Truco accepted")
    
    # 5. Play a round
    print("\n5. Playing a round...")
    response = requests.post(
        f"{BASE_URL}/games/{game_id}/play",
        json={"card_indices": [0, 1, 2, 0]}  # Each player plays a card
    )
    play_result = response.json()
    print(f"   ✓ Round played")
    print(f"   Result: {play_result['play_result']}")
    
    # 6. Check final game state
    print("\n6. Final game state...")
    response = requests.get(f"{BASE_URL}/games/{game_id}")
    final_state = response.json()
    print(f"   Time 1: {final_state['pontos_time1']} pts | Time 2: {final_state['pontos_time2']} pts")
    print(f"   MD3: Time 1: {final_state['md3_time1']} | Time 2: {final_state['md3_time2']}")
    print(f"   Victory: {final_state['vitoria']}")
    
    # 7. List all games
    print("\n7. Listing all games...")
    response = requests.get(f"{BASE_URL}/games")
    games = response.json()
    print(f"   ✓ Active games: {games['count']}")
    
    # 8. Delete game
    print("\n8. Deleting game...")
    response = requests.delete(f"{BASE_URL}/games/{game_id}")
    print(f"   ✓ Game deleted")


if __name__ == "__main__":
    print("=" * 60)
    print("Truco Paulista API - Example Usage")
    print("=" * 60)
    print("\nMake sure the API is running: python run_api.py\n")
    
    try:
        example_game_flow()
        print("\n" + "=" * 60)
        print("Example completed successfully!")
        print("=" * 60)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API. Is it running?")
        print("   Start the API with: python run_api.py")
    except Exception as e:
        print(f"❌ Error: {e}")
