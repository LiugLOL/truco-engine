class Carta:
    def __init__(self, naipe, numero):
            self.naipe= naipe.upper()
            self.numero = str(numero)
            self.carta =  str(numero) + naipe.upper()    
    #mostra o "id" da carta   
    def id(self):
          return self.carta
    #mostra a carta no formato bonitinho, tipo 7 de paus, as de sei la oq sabe?
    def nomeCarta(self):
        if self.naipe == "P":
              nomeNaipe = "paus"
        elif self.naipe == "C":
              nomeNaipe = "copas"
        elif self.naipe == "E":
              nomeNaipe = "espadas"
        else:
              nomeNaipe = "ouros"
        return (f"{self.numero} de {nomeNaipe}")

