"""
WebSocket handlers for real-time multiplayer Truco
"""
from typing import Dict, List, Set
from socketio import AsyncServer, ASGIApp
from fastapi import FastAPI
from .models import GameResponse

# Create AsyncServer
sio = AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    ping_timeout=60,
    ping_interval=25
)

# Track connected clients per game
connected_clients: Dict[str, Set[str]] = {}  # game_id -> set of client sids
client_to_game: Dict[str, str] = {}  # client_sid -> game_id


@sio.event
async def connect(sid: str, environ):
    """Client connects to WebSocket"""
    print(f"✓ Client connected: {sid}")
    

@sio.event
async def disconnect(sid: str):
    """Client disconnects from WebSocket"""
    print(f"✗ Client disconnected: {sid}")
    
    # Remove from game tracking
    if sid in client_to_game:
        game_id = client_to_game[sid]
        if game_id in connected_clients:
            connected_clients[game_id].discard(sid)
            
            # Notify other players
            await sio.emit(
                'player_disconnected',
                {'sid': sid, 'message': f'Player {sid} left the game'},
                room=game_id,
                skip_sid=sid
            )
        
        del client_to_game[sid]


@sio.event
async def join_game(sid: str, data: dict):
    """
    Client joins a game room
    
    Args:
        data: {"game_id": "..."}
    """
    game_id = data.get('game_id')
    
    if not game_id:
        await sio.emit('error', {'message': 'game_id required'}, to=sid)
        return
    
    # Track connection
    if game_id not in connected_clients:
        connected_clients[game_id] = set()
    
    connected_clients[game_id].add(sid)
    client_to_game[sid] = game_id
    
    # Join socket.io room
    sio.enter_room(sid, game_id)
    
    # Notify others
    await sio.emit(
        'player_joined',
        {'sid': sid, 'count': len(connected_clients[game_id])},
        room=game_id
    )
    
    print(f"✓ Client {sid} joined game {game_id}")


@sio.event
async def play_card(sid: str, data: dict):
    """
    Client plays a card
    
    Args:
        data: {"game_id": "...", "card_index": 0}
    """
    game_id = data.get('game_id')
    card_index = data.get('card_index')
    
    if not game_id or card_index is None:
        await sio.emit('error', {'message': 'game_id and card_index required'}, to=sid)
        return
    
    # Broadcast play action to room
    await sio.emit(
        'card_played',
        {
            'player_sid': sid,
            'card_index': card_index,
            'timestamp': None  # Will be added by client if needed
        },
        room=game_id
    )
    
    print(f"► Card played in {game_id}: player {sid} played card {card_index}")


@sio.event
async def broadcast_state(sid: str, data: dict):
    """
    Broadcast game state to all players in room
    
    Args:
        data: {"game_id": "...", "game_state": {...}}
    """
    game_id = data.get('game_id')
    game_state = data.get('game_state')
    
    if not game_id:
        await sio.emit('error', {'message': 'game_id required'}, to=sid)
        return
    
    # Send to everyone in the room
    await sio.emit(
        'game_state_update',
        game_state,
        room=game_id
    )
    
    print(f"📡 State broadcast in {game_id}")


@sio.event
async def request_truco(sid: str, data: dict):
    """
    Broadcast truco request
    
    Args:
        data: {"game_id": "...", "time": 1}
    """
    game_id = data.get('game_id')
    time = data.get('time')
    
    await sio.emit(
        'truco_requested',
        {'player_sid': sid, 'time': time},
        room=game_id,
        skip_sid=sid  # Don't send back to sender
    )
    
    print(f"📣 Truco requested in {game_id}: Team {time}")


@sio.event
async def respond_truco(sid: str, data: dict):
    """
    Broadcast truco response
    
    Args:
        data: {"game_id": "...", "resposta": "aceito"}
    """
    game_id = data.get('game_id')
    resposta = data.get('resposta')
    
    await sio.emit(
        'truco_responded',
        {'player_sid': sid, 'resposta': resposta},
        room=game_id,
        skip_sid=sid
    )
    
    print(f"✓ Truco response in {game_id}: {resposta}")


@sio.event
async def sync_request(sid: str, data: dict):
    """
    Request game state sync
    
    Args:
        data: {"game_id": "..."}
    """
    # Client will request full state from HTTP endpoint
    # This is just a signal that sync is needed
    game_id = data.get('game_id')
    await sio.emit('sync_required', room=game_id)
    print(f"🔄 Sync requested for {game_id}")


def attach_socketio(app: FastAPI) -> FastAPI:
    """Attach SocketIO to FastAPI app"""
    # Create ASGI app with SocketIO
    asgi_app = ASGIApp(sio, app)
    return asgi_app
