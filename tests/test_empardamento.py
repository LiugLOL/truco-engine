"""
Teste de Empardamento
Simula situação onde cartas iguais (não-manilhas) são jogadas
"""
import jogo

print("=" * 60)
print("🎴 TESTE DE EMPARDAMENTO")
print("=" * 60)

# Criar jogo
game = jogo.Jogo(4)
print(f"\n✓ Jogo criado com 4 jogadores")

# Exibir cartas atuais
print("\n" + "=" * 60)
print("[TEST 1] Cartas distribuídas")
print("=" * 60)
for i, player in enumerate(game.jogadores):
    cartas = player.mostrarCartas()
    time = 1 if i % 2 == 0 else 2
    print(f"Jogador {i} (Time {time}): {', '.join(cartas)}")

print(f"\nVira: {game.partida.vira.nomeCarta()}")
print(f"Manilha: {game.partida.truco.progressao[game.partida.truco.indice_atual]} (número: {game.partida.vira.numero})")

# Teste 2: Tentar forçar um empardamento simulando cartas iguais
print("\n" + "=" * 60)
print("[TEST 2] Simulando empardamento (cartas iguais não-manilha)")
print("=" * 60)

# Obter referência dos jogadores
j0, j1, j2, j3 = game.jogadores[0], game.jogadores[1], game.jogadores[2], game.jogadores[3]

# Manualmente dar cartas iguais para teste
# Dar K (rei) de paus pra todos
from carta import Carta
k_paus = Carta('P', 'K')
k_ouros = Carta('O', 'K')
k_copas = Carta('C', 'K')
k_espadas = Carta('E', 'K')

j0.receberCartas([k_paus, k_paus, k_paus])
j1.receberCartas([k_ouros, k_ouros, k_ouros])
j2.receberCartas([k_copas, k_copas, k_copas])
j3.receberCartas([k_espadas, k_espadas, k_espadas])

print("Cartas simuladas (todos com K):")
for i, player in enumerate(game.jogadores):
    cartas = player.mostrarCartas()
    print(f"  Jogador {i}: {', '.join(cartas)}")

# Jogar a primeira carta (índice 0)
print("\nJogando primeira rodadinha (todos jogam K)...")
resultado = game.receberMao([0, 0, 0, 0])

print(f"\n✓ Resultado:")
print(f"  - Tipo: {resultado['resultado']}")
print(f"  - Vencedor: {resultado['time_vencedor'] if resultado['time_vencedor'] != -1 else 'EMPARDOU'}")
print(f"  - MD3 Time 1: {resultado['md3_time1']} (rodadinhas)")
print(f"  - MD3 Time 2: {resultado['md3_time2']} (rodadinhas)")
print(f"  - Pontos: Time 1: {resultado['pontos_time1']} | Time 2: {resultado['pontos_time2']}")

if resultado['resultado'] == 'empardou':
    print(f"\n✓ EMPARDAMENTO FUNCIONANDO CORRETAMENTE!")
else:
    print(f"\n✗ ERRO: Deveria ter empardado!")

print("\n" + "=" * 60)
print("✓ TESTE DE EMPARDAMENTO CONCLUÍDO")
print("=" * 60)
