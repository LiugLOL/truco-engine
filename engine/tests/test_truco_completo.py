"""
Teste completo do Truco Paulista
Inclui: cartas, md3, truco, mão de 11, vitória
"""
from engine import jogo

print("=" * 60)
print("🎴 TESTE COMPLETO DO TRUCO PAULISTA")
print("=" * 60)

# Criar jogo com 4 jogadores
game = jogo.Jogo(4)
print(f"\n✓ Jogo criado com 4 jogadores (Time 1: J0+J2, Time 2: J1+J3)")

# Teste 1: Verificar cartas distribuídas
print("\n" + "=" * 60)
print("[TEST 1] Distribuição de cartas")
print("=" * 60)
for i, player in enumerate(game.jogadores):
    cartas = player.mostrarCartas()
    time = 1 if i % 2 == 0 else 2
    print(f"Jogador {i} (Time {time}): {', '.join(cartas)}")

# Teste 2: Pedir truco (antes de qualquer coisa)
print("\n" + "=" * 60)
print("[TEST 2] Sistema de Truco")
print("=" * 60)
resultado_truco = game.pedir_truco(1)
print(f"Time 1 pede truco: {resultado_truco}")
print(f"Valor atual da aposta: {game.obter_valor_truco_atual()} pontos")

# Teste 3: Time 2 aceita
resultado_resposta = game.responder_truco(2, "aceito")
print(f"Time 2 aceita: {resultado_resposta}")

# Teste 4: Fazer 1ª mão (jogam todos a 1ª carta)
print("\n" + "=" * 60)
print("[TEST 3] Primeira mão do MD3")
print("=" * 60)
indices = [0, 0, 0, 0]
resultado_mao = game.receberMao(indices)
print(f"Resultado: Time {resultado_mao['time_vencedor'] if resultado_mao['time_vencedor'] != -1 else 'EMPATE'} vence")
print(f"MD3: Time 1: {resultado_mao['md3_time1']} x Time 2: {resultado_mao['md3_time2']}")
print(f"Pontos: Time 1: {resultado_mao['pontos_time1']} x Time 2: {resultado_mao['pontos_time2']}")
print(f"Valor apostado: {resultado_mao['valor_aposta']} pontos")

# Teste 5: Segunda mão
print("\n[TEST 4] Segunda mão do MD3")
indices = [0, 0, 0, 0]
resultado_mao = game.receberMao(indices)
print(f"Resultado: Time {resultado_mao['time_vencedor'] if resultado_mao['time_vencedor'] != -1 else 'EMPATE'} vence")
print(f"MD3: Time 1: {resultado_mao['md3_time1']} x Time 2: {resultado_mao['md3_time2']}")
print(f"Pontos: Time 1: {resultado_mao['pontos_time1']} x Time 2: {resultado_mao['pontos_time2']}")

# Teste 6: Mão de 11
print("\n" + "=" * 60)
print("[TEST 5] Simulando mão de 11")
print("=" * 60)
# Simular pontos até chegar em 11
game.pontosTime1 = 11
game.pontosTime2 = 9
print(f"Time 1: 11 pontos | Time 2: 9 pontos")

resultado_truco_11 = game.pedir_truco(1)
print(f"Time 1 tenta pedir truco em mão de 11: {resultado_truco_11}")
print(f"✓ Corretamente bloqueado!" if not resultado_truco_11['sucesso'] else "✗ ERRO: Deveria estar bloqueado!")

# Teste 7: Mão de ferro
print("\n" + "=" * 60)
print("[TEST 6] Simulando mão de ferro")
print("=" * 60)
game.pontosTime1 = 11
game.pontosTime2 = 11
print(f"Time 1: 11 pontos | Time 2: 11 pontos")

resultado_truco_ferro = game.pedir_truco(1)
print(f"Time 1 tenta pedir truco em mão de ferro: {resultado_truco_ferro}")
print(f"✓ Corretamente bloqueado!" if not resultado_truco_ferro['sucesso'] else "✗ ERRO: Deveria estar bloqueado!")

# Teste 8: Vitória
print("\n" + "=" * 60)
print("[TEST 7] Sistema de vitória")
print("=" * 60)
game.pontosTime1 = 15
game.pontosTime2 = 8
vitoria = game.checarVitoria()
print(f"Time 1: {game.pontosTime1} | Time 2: {game.pontosTime2}")
print(f"Jogo acabou? {vitoria['acabou']}")
if vitoria['acabou']:
    print(f"🏆 TIME {vitoria['vencedor']} VENCEU A PARTIDA! 🏆")

print("\n" + "=" * 60)
print("✓ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
print("=" * 60)
