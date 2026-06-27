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
        #pega a carta, retorna a carta, explode a carta da mao pra nao ser mais
        #usada
        carta = self.mao[indice]
        self.mao.pop(indice)
        return carta
    def mostrarCartas(self):
        #lista anotando todas as cartas da mao formatadas bonitinhas
        cartasMao = []
        for i in range(len(self.mao)):
            cartaAtual = self.mao[i]
            cartasMao.append(cartaAtual.nomeCarta())
        return cartasMao