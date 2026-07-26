from typing import List
from .carta import Carta

class Jogador:
    def __init__(self) -> None:
        self.mao: List[Carta] = []
        self.nome: str = ""

    def setNome(self, nome: str) -> None:
        """Define o nome do jogador"""
        self.nome = nome

    def getNome(self) -> str:
        """Retorna o nome do jogador"""
        return self.nome

    def receberCartas(self, cartas: List[Carta]) -> None:
        """Recebe um conjunto de cartas"""
        self.mao = cartas[:]

    def jogarCarta(self, indice: int) -> Carta:
        """Joga uma carta pelo índice e a remove da mão"""
        carta = self.mao[indice]
        self.mao.pop(indice)
        return carta

    def mostrarCartas(self) -> List[str]:
        """Retorna a lista de cartas da mão com nomes formatados"""
        cartasMao: List[str] = []
        for i in range(len(self.mao)):
            cartaAtual = self.mao[i]
            cartasMao.append(cartaAtual.nomeCarta())
        return cartasMao