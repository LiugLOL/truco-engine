import rodadinha
import baralho
import truco
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
        self.truco = truco.Truco()
        
        # Rastrear rodadinhas (cada mão do MD3)
        self.rodadinhas_time1 = 0
        self.rodadinhas_time2 = 0
        
        # Sistema de ordem de jogo
        self.rodadinha_atual = 1  # 1, 2 ou 3
        self.quem_comecou_rodada = 0  # Qual jogador começou a rodada
        self.proximo_a_jogar = 0  # Quem joga na próxima rodadinha
        
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
        """
        Executa uma jogada com suporte a empardamento e descarte
        Retorna: (vencedor_idx, empadou_na_primeira)
        """
        cartasJogadas = []

        for i in range(len(self.jogadores)):
            jogadorAtual = self.jogadores[i]
            cartaAtual = jogadorAtual.jogarCarta(indice[i])
            cartasJogadas.append(cartaAtual)

        rodadinha_obj = rodadinha.Rodadinha(cartasJogadas, self.vira)
        
        # Verifica se empadou na primeira rodadinha
        empadou_primeira, _ = rodadinha_obj.verificar_empardamento()
        
        if empadou_primeira and self.rodadinha_atual == 1:
            # Primeira rodadinha: ambos ganham 1 ponto
            self.rodadinhas_time1 += 1
            self.rodadinhas_time2 += 1
            self.proximo_a_jogar = 0  # Quem começou começa dnv
            self.rodadinha_atual += 1
            return -1, True  # -1 = empardou, True = empadou na primeira
        
        elif empadou_primeira and self.rodadinha_atual > 1:
            # Rodadinha 2 ou 3: descartar empardalas e comparar próximas
            cartas_restantes = rodadinha_obj.descartar_empardalas()
            
            if cartas_restantes:
                # Recria Rodadinha com cartas restantes
                rodadinha_obj = rodadinha.Rodadinha(cartas_restantes, self.vira)
            else:
                # Todas empardalas: ambos ganham 1
                self.rodadinhas_time1 += 1
                self.rodadinhas_time2 += 1
                self.proximo_a_jogar = 0
                self.rodadinha_atual += 1
                return -1, True
        
        # Se não empadou, prossegue normalmente
        idxJogador = rodadinha_obj.briga()
        
        if idxJogador != -1:
            # Alguém venceu: registra ponto
            if (idxJogador % 2) == 0:
                self.rodadinhas_time1 += 1
            else:
                self.rodadinhas_time2 += 1
            
            # Próximo jogador a começar é o vencedor
            self.proximo_a_jogar = idxJogador
            self.rodadinha_atual += 1
        
        return idxJogador, False

    def adicionar_placar_time(self, time, valor_aposta=1):
        if time == 1:
            self.md3time1 += 1
        else:
            self.md3time2 += 1
        if self.placar_time(time) == 2:
            self.acabou = True
            

    def placar_time(self, time):
        if time == 1:
            return self.md3time1
        else:
            return self.md3time2
    def getAcabou(self):
        return self.acabou

    def pedir_truco(self, time_que_pede, pontos_time1, pontos_time2):
        """Tenta pedir truco"""
        pode_pedir, motivo = self.truco.pode_pedir_truco(pontos_time1, pontos_time2)
        
        if not pode_pedir:
            return {
                "sucesso": False,
                "motivo": motivo
            }
        
        resultado = self.truco.pedir_truco(time_que_pede)
        return {
            "sucesso": resultado,
            "valor": self.truco.get_valor() if resultado else None
        }

    def responder_truco(self, time_que_responde, resposta):
        """Time responde ao pedido de truco"""
        return self.truco.responder(time_que_responde, resposta)

    def reset_truco(self):
        """Reseta truco pra nova rodada"""
        self.truco.reset()

