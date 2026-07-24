'''
COISAS IMPORTANTES!!!!
O QUE EH RODADINHA? EH CADA RODADA DO MD3, CADA MINI RODADINHA DESSA EU CHAMEI DE RODADINHA!!

REGRA RECEBERA AS CARTAS JOGADAS NA PARTIDA EM UMA LISTA E SO ENTAO
FARA AS COMPARACOES DE QUEM EH A MAIS FORTE!
NAO TENTE de maneira NENHUMA colocar carta por carta nos parametros da hierarquia
sem que as cartas jogadas estiverem NUMA LISTA >:(

abraco, Quirino
'''
class Rodadinha:
    def __init__(self, cartas_jogadas, vira):       
        self.ordemNum = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        self.cartas_jogadas = cartas_jogadas[:]
        self.cartas_originais = cartas_jogadas[:]  # Backup pra descarte
        #fazendo todas as manilhas
        #logica proposta->pega o numero, soma +1 no indice, se o indice for 
        #o ultimo tipo eh o 3, manilha eh 4, so isso
        indiceManilha = self.ordemNum.index(vira.numero) + 1
        self.manilha = self.ordemNum[indiceManilha % len(self.ordemNum)]

    def _calcular_poder(self, carta):
        """Calcula o poder de uma carta"""
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
        
        return poderAtual

    def briga(self):
        """Retorna vencedor: índice do jogador ou -1 se empardou"""
        poder = [] 

        for carta in self.cartas_jogadas:
            poderAtual = self._calcular_poder(carta)
            poder.append(poderAtual)
        
        poderOrganizado = poder[:]
        poderOrganizado.sort()
        
        # Verifica se empatou (dois maiores iguais)
        if poderOrganizado[-1] == poderOrganizado[-2]:
            return -1
        else:
            maior = max(poder)
            vencedor = poder.index(maior)
        
        return vencedor

    def verificar_empardamento(self):
        """
        Verifica se cartas não-manilhas empardalas
        Retorna: (empadou: bool, cartas_iguais: list de índices)
        """
        # Checa se todas as 4 cartas têm o mesmo número
        numeros = [carta.numero for carta in self.cartas_jogadas]
        
        # Se todos têm o mesmo número
        if len(set(numeros)) == 1:
            numero = numeros[0]
            
            # Se NÃO é manilha → empardam
            if numero != self.manilha:
                return True, list(range(len(self.cartas_jogadas)))
        
        return False, []

    def descartar_empardalas(self):
        """
        Descarta cartas empardalas e retorna as próximas mais fortes
        
        Quando há empardamento em rodadinha 2 ou 3:
        - Remove cartas com mesmo número (as empardalas)
        - Comparação continua com próximas cartas mais fortes
        
        Retorna: lista de cartas sem as empardalas (ordenada por índice original)
        """
        if not self.cartas_jogadas:
            return []
        
        # Se todos têm o mesmo número (empardou)
        numeros = [carta.numero for carta in self.cartas_jogadas]
        
        if len(set(numeros)) == 1:
            numero_empardalado = numeros[0]
            
            # Remove cartas com esse número
            cartas_filtradas = [
                carta for carta in self.cartas_jogadas 
                if carta.numero != numero_empardalado
            ]
            
            if cartas_filtradas:
                self.cartas_jogadas = cartas_filtradas
                return cartas_filtradas
            else:
                # Se todas empardalas, retorna as originais (não descarta nada)
                return self.cartas_originais
        
        return self.cartas_jogadas
