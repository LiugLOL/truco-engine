from . import rodada
from . import jogador
class Jogo:
    def __init__(self, numJogadores):
        self.jogadores = []
        for i in range(numJogadores):
            player = jogador.Jogador()
            player.setNome(f"Jogador {i}")
            self.jogadores.append(player)
        self.partida = rodada.Rodada(self.jogadores)
        self.pontosTime1 = 0
        self.pontosTime2 = 0
    def receberMao(self, indice):
        vencedor, empadou_primeira = self.partida.jogada(indice)
        
        # Pega o valor atual da aposta (multiplicador)
        valor_aposta = self.partida.truco.get_valor()
        
        if empadou_primeira:
            # Empardou na primeira rodadinha: ambos ganham 1 ponto
            resultado_mao = "empardou"
        elif vencedor == -1:
            # Empate em manilhas (não deveria acontecer com lógica correta)
            resultado_mao = "empate"
        elif (vencedor % 2) == 0:
            # Time 1 ganha (jogadores 0, 2, etc)
            self.partida.adicionar_placar_time(1, valor_aposta)
            resultado_mao = "time1"
        else:
            # Time 2 ganha (jogadores 1, 3, etc)
            self.partida.adicionar_placar_time(2, valor_aposta)
            resultado_mao = "time2"
        
        # Verifica se MD3 acabou e aplica pontos ANTES de criar nova rodada
        md3_acabou = self.partida.placar_time(1) == 2 or self.partida.placar_time(2) == 2
        
        if md3_acabou:
            if self.partida.placar_time(1) == 2:
                self.pontosTime1 += valor_aposta
            elif self.partida.placar_time(2) == 2:
                self.pontosTime2 += valor_aposta
            
            # Agora cria nova rodada
            self.partida = rodada.Rodada(self.jogadores)
        
        retornar = {
            "acabou": md3_acabou,
            "time_vencedor": vencedor,
            "resultado": resultado_mao,
            "md3_time1": self.partida.placar_time(1) if not md3_acabou else self.partida.placar_time(1),
            "md3_time2": self.partida.placar_time(2) if not md3_acabou else self.partida.placar_time(2),
            "pontos_time1": self.pontosTime1,
            "pontos_time2": self.pontosTime2,
            "valor_aposta": valor_aposta
        }
        
        return retornar
    def checarVitoria(self):
        if self.pontosTime1 >= 12 or self.pontosTime2 >= 12:
            if self.pontosTime1 >= 12:
                return {
                    "acabou": True,
                    "vencedor": 1
                }
            elif self.pontosTime2 >= 12:
                return {
                    "acabou": True,
                    "vencedor": 2
                }
        else:
            return {"acabou": False}

    def pedir_truco(self, time_que_pede):
        """Tenta pedir truco"""
        return self.partida.pedir_truco(time_que_pede, self.pontosTime1, self.pontosTime2)

    def responder_truco(self, time_que_responde, resposta):
        """Responde ao pedido de truco"""
        resultado = self.partida.responder_truco(time_que_responde, resposta)
        
        # Se corrido, o time que pediu ganha automaticamente
        if resultado.get("resultado") == "corrido":
            time_vencedor = resultado["time_vencedor"]
            valor = resultado["valor"]
            if time_vencedor == 1:
                self.pontosTime1 += valor
            else:
                self.pontosTime2 += valor
        
        return resultado

    def obter_valor_truco_atual(self):
        """Retorna o valor atual da aposta"""
        return self.partida.truco.get_valor()
