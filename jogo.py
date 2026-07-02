import rodada
import jogador
class Jogo:
    def __init__(self, numJogadores):
        self.jogadores = []
        for i in range(numJogadores):
            player = jogador.Jogador()
            player.setNome(i)
            self.jogadores.append(player)
        self.partida = rodada.Rodada(self.jogadores)
        self.pontosTime1 = 0
        self.pontosTime2 = 0
    def receberMao(self, indice):
        vencedor = self.partida.jogada(indice) #retorna vencedor da mao
        if vencedor == -1:
            self.partida.adicionar_placar_time(1)
            self.partida.adicionar_placar_time(2)
        elif (vencedor % 2) == 0:
            self.partida.adicionar_placar_time(1)
        elif (vencedor % 2) == 1:
            self.partida.adicionar_placar_time(2)
        retornar = {
            "acabou": self.partida.getAcabou(),
            "time_vencedor": vencedor,
            "md3_time1": self.partida.placar_time(1),
            "md3_time2": self.partida.placar_time(2),
            "pontos_time1": self.pontosTime1,
            "pontos_time2": self.pontosTime2,
        }
        if self.partida.placar_time(1) == 2 or self.partida.placar_time(2) == 2:
            if self.partida.placar_time(1) == 2:
                self.pontosTime1 += 1
            elif self.partida.placar_time(2) == 2:
                self.pontosTime2 += 1

            self.partida = rodada.Rodada(self.jogadores)
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