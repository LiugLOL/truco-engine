import regra
import baralho
import random


class Rodada:
    def __init__(self, jog):
        self.baralho = baralho.Baralho()
        self.jogadores = jog
        #manilha da rodada
        indice = random.randint(0, len(self.baralho.cartas)-1)
        #seleciona o vira para ser depois a manilha, da pop pra carta virada
        #nao poder ser usada por jogadores durante a rodada, indisponivel
        #no baralho
        self.vira = self.baralho.select_card(indice)
        self.md3time1 = 0
        self.md3time2 = 0
        self.acabou = False
        self.darCarta()
    def darCarta(self):
        for jogador in self.jogadores:
            mao = []
            for i in range(3):
                carta = self.baralho.select_card(0)
                mao.append(carta)
            jogador.receberCartas(mao)
    
    '''
    O parametro INDICE da funcao jogada se refere a um vetor com os indices de
    qual carta o jogador jogou, vamos supor q temos 4 jogadores, todos com 3 cartas na
    mao, e o indices seja [0, 1, 1, 2], o jogador 0 jogou a carta da mao dele na
    posicao 0, jogador 1 jogou a carta na mao na posicao 1, jogador 2 jogou a carta
    na mao na posicao 1 tambem, e o jogador 3 jogou a carta na posicao 3, ai 
    o parametro receberia aquele vetor, a funcao iria ate os jogadores pegar cada carta
    e ver quem ganhou o md3 atual.
    '''
    def jogada(self, indice):
        cartasJogadas = []

        for i in range(len(self.jogadores)):
            jogadorAtual = self.jogadores[i]
            cartaAtual = jogadorAtual.jogarCarta(indice[i])
            cartasJogadas.append(cartaAtual)

        regra_obj = regra.Regra(cartasJogadas, self.vira)
        idxJogador = regra_obj.briga()

        return idxJogador

    def adicionar_placar_time(self, time):
        if time == 1:
            self.md3time1 +=1
        else:
            self.md3time2 +=1
        if self.placar_time(time) == 2:
            self.acabou = True
            

    def placar_time(self, time):
        if time == 1:
            return self.md3time1
        else:
            return self.md3time2
    def getAcabou(self):
        return self.acabou

