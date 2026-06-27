import carta
class Jogador:
    def __init__(self):
        self.mao = []
        self.nome = ""
    def setNome(self, nome):
        self.nome = nome
    def getNome(self):
        return self.nome
    def receberCartas(self, cartas):
        self.mao = cartas[:]
    def jogarCarta(self, indice):
        carta = self.mao[indice]
        self.mao.pop(indice)
        return carta
    def mostrarCartas(self):
        print("Suas cartas atuais sao:")
        for i in range(len(self.mao)):
            cartaAtual = self.mao[i]
            cartaAtual.printEntendivel()