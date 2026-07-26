class Carta:
    def __init__(self, naipe: str, numero: str | int) -> None:
        self.naipe: str = naipe.upper()
        self.numero: str = str(numero)
        self.carta: str = str(numero) + naipe.upper()

    def id(self) -> str:
        """Retorna o ID da carta (ex: 7P, KE)"""
        return self.carta

    def nomeCarta(self) -> str:
        """Retorna o nome formatado da carta (ex: 7 de paus)"""
        if self.naipe == "P":
            nomeNaipe = "paus"
        elif self.naipe == "C":
            nomeNaipe = "copas"
        elif self.naipe == "E":
            nomeNaipe = "espadas"
        else:
            nomeNaipe = "ouros"
        return f"{self.numero} de {nomeNaipe}"

