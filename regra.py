'''
COISAS IMPORTANTES DAS REGRAS DE DUELO!!!!
REGRA RECEBERA AS CARTAS JOGADAS NA PARTIDA EM UMA LISTA E SO ENTAO
FARA AS COMPARACOES DE QUEM EH A MAIS FORTE!
NAO TENTE de maneira NENHUMA colocar carta por carta nos parametros da hierarquia
sem que as cartas jogadas estiverem NUMA LISTA >:(
abraco, Quirino
'''
class Regra:
    def __init__(self, cartas_jogadas, manilha):       
        self.ordemNum = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        self.cartas_jogadas = cartas_jogadas[:]
        self.manilha = manilha
        #logica proposta: sem manilha ainda, mas fazer o seguinte:
        #ve qual numero tem o menor indice, pegar da carta o atriburo numero e comparar
        #os indices, quem tiver o menor indice ganha, se tiver o mesmo indice apela pro
        #naipe

        #selecionando 2 cartas do baralho

    def duelo(self):
        poder = [] #numero do jogador e qual carta lancou, indice 0 = jogador 1, indice 1 = jogador 2 e por ai vai, e ele vai retoranr o indice de qual eh o maior aqui

        for carta in self.cartas_jogadas:
            num = carta.numero
            poderAtual = self.ordemNum.index(num)
            if num == self.manilha:
                poderAtual += 10
                naipe = carta.naipe
                if naipe == 'P':
                    poderAtual += 3
                elif naipe == 'C':
                    poderAtual += 2
                elif naipe == 'E':
                    poderAtual += 1
                #ouros nao precisa
            poder.append(poderAtual)
        poderOrganizado = poder[:]
        poderOrganizado.sort()
        if poderOrganizado[-1] == poderOrganizado[-2]:
            vencedor = -1
        else:
            maior = max(poder)
            vencedor = poder.index(maior)
        return vencedor