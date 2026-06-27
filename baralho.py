import random
import carta
class Baralho:
    def __init__(self):
        naipes = ["P", "C", "E", "O"]
        numeros = ["A", 2, 3, 4, 5, 6, 7, "Q", "J", "K"]
        self.cartas = []
        for naipe in naipes:
            for numero in numeros:
                carta_atual = carta.Carta(naipe, numero)
                self.cartas.append(carta_atual)
        random.shuffle(self.cartas)
    #imprime e mostra o baralho, fins de debug
    def show(self):
        for i in range(len(self.cartas)):
            carta = self.cartas[i]
            if i == (len(self.cartas)-1):
                print(f"{carta.id()}")
            else:
                print(f"{carta.id()}", end = " ")
    #imprime e mostra a carta selecionada do baralho
    def select_card(self, i):
        cartaSelecionada = self.cartas[i]
        #retira a carta do baralho pra nao poder mais ser usada
        self.cartas.pop(i)
        return cartaSelecionada