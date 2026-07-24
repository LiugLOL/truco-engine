"""
TESTE FASE 2 - Descarte de Empardalas + Ordem de Jogo
"""

from carta import Carta
import jogo

print("=" * 70)
print("🎴 TESTE FASE 2 - DESCARTE E ORDEM DE JOGO")
print("=" * 70)

# Teste 1: Descarte de Empardalas (rodadinha 2)
print("\n[TEST 1] Descarte de Empardalas em rodadinha 2")
print("-" * 70)

game = jogo.Jogo(4)
j0, j1, j2, j3 = game.jogadores[0], game.jogadores[1], game.jogadores[2], game.jogadores[3]

# Rodadinha 1: Cartas diferentes (alguém ganha)
print("\n1ª Rodadinha: Diferentes (alguém ganha e começa próxima)")
j0.receberCartas([Carta('P', '4'), Carta('P', '5'), Carta('P', '6')])
j1.receberCartas([Carta('O', '4'), Carta('O', '5'), Carta('O', '6')])
j2.receberCartas([Carta('C', '7'), Carta('C', 'Q'), Carta('C', 'J')])  # J2 tem 7 forte
j3.receberCartas([Carta('E', '3'), Carta('E', 'K'), Carta('E', 'A')])

resultado1 = game.receberMao([0, 0, 0, 0])  # Todos jogam primeira carta
print(f"  Resultado: {resultado1['resultado']}")
print(f"  Vencedor: Jogador {resultado1['time_vencedor']}")
print(f"  Próximo a jogar: {game.partida.proximo_a_jogar}")
print(f"  Rodadinha atual: {game.partida.rodadinha_atual}")

# Rodadinha 2: Cartas iguais (devem descartar e comparar próximas)
print("\n2ª Rodadinha: Iguais (descarta e compara próximas)")
resultado2 = game.receberMao([0, 0, 0, 0])  # Todos jogam segunda carta
print(f"  Resultado: {resultado2['resultado']}")
print(f"  Rodadinhas Time 1: {resultado2['md3_time1']}")
print(f"  Rodadinhas Time 2: {resultado2['md3_time2']}")
print(f"  Rodadinha atual: {game.partida.rodadinha_atual}")

# Rodadinha 3: Finaliza MD3
print("\n3ª Rodadinha: Finaliza MD3")
resultado3 = game.receberMao([0, 0, 0, 0])  # Todos jogam terceira carta
print(f"  Resultado: {resultado3['resultado']}")
print(f"  MD3 acabou? {resultado3['acabou']}")
print(f"  Rodadinhas Time 1: {resultado3['md3_time1']}")
print(f"  Rodadinhas Time 2: {resultado3['md3_time2']}")

if resultado3['acabou']:
    if resultado3['md3_time1'] == 2:
        print(f"  ✓ Time 1 ganhou o MD3 (2 rodadinhas)")
    else:
        print(f"  ✓ Time 2 ganhou o MD3 (2 rodadinhas)")

# Teste 2: Verificar que pontos foram aplicados
print("\n[TEST 2] Verificação de Pontos Aplicados")
print("-" * 70)
print(f"Pontos Time 1: {resultado3['pontos_time1']}")
print(f"Pontos Time 2: {resultado3['pontos_time2']}")
print(f"Valor da aposta: {resultado3['valor_aposta']}")

if (resultado3['pontos_time1'] > 0 or resultado3['pontos_time2'] > 0):
    print("✓ Pontos foram aplicados corretamente!")
else:
    print("✗ ERRO: Pontos não foram aplicados!")

print("\n" + "=" * 70)
print("✅ TESTES FASE 2 CONCLUÍDOS!")
print("=" * 70)
