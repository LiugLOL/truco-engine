import random
from typing import List
from . import carta

class Baralho:
    def __init__(self) -> None:
        naipes: List[str] = ["P", "C", "E", "O"]
        numeros: List[str] = ["4", "5", "6", "7", "Q", "J", "K", "A", "2", "3"]
        self.cartas: List[carta.Carta] = []
        for naipe in naipes:
            for numero in numeros:
                carta_atual = carta.Carta(naipe, numero)
                self.cartas.append(carta_atual)
        random.shuffle(self.cartas)

    def show(self) -> None:
        """Exibe todas as cartas do baralho no console"""
        for i in range(len(self.cartas)):
            carta_obj = self.cartas[i]
            if i == (len(self.cartas) - 1):
                print(f"{carta_obj.id()}")
            else:
                print(f"{carta_obj.id()}", end=" ")

    def select_card(self, i: int) -> carta.Carta:
        """Seleciona uma carta do baralho e a remove"""
        cartaSelecionada = self.cartas[i]
        self.cartas.pop(i)
        return cartaSelecionada