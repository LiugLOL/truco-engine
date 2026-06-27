import jogador
import regra
import baralho
import random


class Rodada:
    def __init__(self):
        self.baralho = baralho.Baralho()
        self.numJogadores = 0
        self.jogadores = []
        #manilha da rodada
        indice = random.randint(0, 39)
        #seleciona o vira para ser depois a manilha, da pop pra carta virada
        #nao poder ser usada por jogadores durante a rodada, indisponivel
        #no baralho
        self.vira = self.baralho.select_card(indice)
    def setJogadores(self, num):
        self.numJogadores = num
        for i in range(num):
            player = jogador.Jogador()
            player.setNome(i)
            self.jogadores.append(player)
    def jogadas(self):
        #FAZER:DAR PRINT NA VIRA
        cartasJogadas = []
        for i in range(len(self.numJogadores)):
            self.jogadores[i].mostrarCartas()
            indice = int(input("Selecione qual carta quer jogar(cartas comecam no 1 e terminam no 3): "))
            cartasJogadas.append(self.jogadores[i].jogarCarta(indice))
        regra.Regra(cartasJogadas, )
            #terminar:fazer a carta selecionada ser escolhida pro combate das cartas
