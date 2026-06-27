'''
COISAS IMPORTANTES DAS REGRAS DE DUELO!!!!
REGRA RECEBERA AS CARTAS JOGADAS NA PARTIDA EM UMA LISTA E SO ENTAO
FARA AS COMPARACOES DE QUEM EH A MAIS FORTE!
NAO TENTE de maneira NENHUMA colocar carta por carta nos parametros da hierarquia
sem que as cartas jogadas estiverem NUMA LISTA >:(
abraco, Quirino
'''
class Regra:
    def __init__(self, cartas_jogadas, vira):       
        self.ordemNum = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        self.cartas_jogadas = cartas_jogadas[:]
        #fazendo todas as manilhas
        #logica proposta->pega o numero, soma +1 no indice, se o indice for 
        #o ultimo tipo eh o 3, manilha eh 4, so isso
        indiceManilha = self.ordemNum.index(vira.numero) + 1
        self.manilha = self.ordemNum[indiceManilha % len(self.ordemNum)]

    def briga(self):
        poder = [] 

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