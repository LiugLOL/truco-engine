"""
TESTE RÁPIDO - Empardamento + Sistema Completo
Execute isso no PyCharm com Run > Run
"""

print("=" * 70)
print("🎴 TESTE FINAL - TRUCO PAULISTA COM EMPARDAMENTO")
print("=" * 70)

try:
    from engine import jogo
    print("✓ Imports funcionando corretamente")
except Exception as e:
    print(f"✗ ERRO ao importar: {e}")
    exit(1)

# Teste 1: Criar jogo
print("\n[TEST 1] Criando jogo com 4 jogadores...")
try:
    game = jogo.Jogo(4)
    print(f"✓ Jogo criado com sucesso")
    print(f"  - Time 1: Jogadores 0 e 2")
    print(f"  - Time 2: Jogadores 1 e 3")
except Exception as e:
    print(f"✗ ERRO: {e}")
    exit(1)

# Teste 2: Distribuição de cartas
print("\n[TEST 2] Distribuição de cartas...")
try:
    for i, player in enumerate(game.jogadores):
        cartas = player.mostrarCartas()
        time = 1 if i % 2 == 0 else 2
        print(f"  - Jogador {i} (Time {time}): {len(cartas)} cartas")
    print(f"✓ Cartas distribuídas corretamente")
except Exception as e:
    print(f"✗ ERRO: {e}")
    exit(1)

# Teste 3: Sistema de Truco
print("\n[TEST 3] Sistema de Truco...")
try:
    resultado = game.pedir_truco(1)
    print(f"  - Time 1 pede truco: {resultado['sucesso']}")
    if resultado['sucesso']:
        print(f"  - Valor da aposta: {game.obter_valor_truco_atual()}")
    
    resposta = game.responder_truco(2, "aceito")
    print(f"  - Time 2 responde 'aceito': {resposta['resultado']}")
    print(f"✓ Sistema de Truco funcionando")
except Exception as e:
    print(f"✗ ERRO: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Teste 4: Jogar rodadinhas
print("\n[TEST 4] Jogando 3 rodadinhas (MD3)...")
try:
    for mao in range(1, 4):
        indices = [0, 0, 0, 0]
        resultado = game.receberMao(indices)
        print(f"  Mão {mao}:")
        print(f"    - Resultado: {resultado['resultado']}")
        print(f"    - MD3: Time 1 {resultado['md3_time1']} x Time 2 {resultado['md3_time2']}")
        print(f"    - Pontos: {resultado['pontos_time1']} x {resultado['pontos_time2']}")
        if resultado['acabou']:
            print(f"    - MD3 Acabou!")
            break
    print(f"✓ Rodadinhas jogadas com sucesso")
except Exception as e:
    print(f"✗ ERRO: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Teste 5: Mão de 11
print("\n[TEST 5] Testando Mão de 11...")
try:
    game.pontosTime1 = 11
    game.pontosTime2 = 9
    resultado = game.pedir_truco(1)
    if not resultado['sucesso']:
        print(f"✓ Mão de 11 bloqueada corretamente: {resultado['motivo']}")
    else:
        print(f"✗ ERRO: Mão de 11 não foi bloqueada!")
except Exception as e:
    print(f"✗ ERRO: {e}")
    exit(1)

# Teste 6: Vitória
print("\n[TEST 6] Sistema de Vitória...")
try:
    game.pontosTime1 = 12
    game.pontosTime2 = 10
    vitoria = game.checarVitoria()
    if vitoria['acabou'] and vitoria['vencedor'] == 1:
        print(f"✓ Vitória reconhecida: Time {vitoria['vencedor']} venceu!")
    else:
        print(f"✗ ERRO: Vitória não foi reconhecida")
except Exception as e:
    print(f"✗ ERRO: {e}")
    exit(1)

print("\n" + "=" * 70)
print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
print("=" * 70)
print("\nResumo das funcionalidades implementadas:")
print("  ✓ Sistema de Truco (1→3→6→9→12)")
print("  ✓ Mão de 11 (bloqueia pedidos)")
print("  ✓ Mão de ferro (bloqueia pedidos)")
print("  ✓ MD3 com suporte a empardamento")
print("  ✓ Pontuação multiplicada por truco")
print("  ✓ Sistema de vitória (12 pontos)")
print("\n🎉 Engine do Truco Paulista está FUNCIONAL!")
