"""
Rodadinha: Uma rodada individual do MD3

IMPORTANTE: Rodadinha recebe um LIST de cartas jogadas e uma vira,
depois faz as comparações de quem tem a carta mais forte!
"""
from typing import List, Tuple
from .carta import Carta


class Rodadinha:
    def __init__(self, cartas_jogadas: List[Carta], vira: Carta) -> None:
        self.ordemNum: List[str] = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
        self.cartas_jogadas: List[Carta] = cartas_jogadas[:]
        self.cartas_originais: List[Carta] = cartas_jogadas[:]
        
        indiceManilha: int = self.ordemNum.index(vira.numero) + 1
        self.manilha: str = self.ordemNum[indiceManilha % len(self.ordemNum)]

    def _calcular_poder(self, carta: Carta) -> int:
        """Calcula o poder de uma carta (hierarquia + bônus de naipe para manilhas)"""
        num: str = carta.numero
        poderAtual: int = self.ordemNum.index(num)
        
        if num == self.manilha:
            poderAtual += 10
            naipe: str = carta.naipe
            if naipe == 'P':
                poderAtual += 3
            elif naipe == 'C':
                poderAtual += 2
            elif naipe == 'E':
                poderAtual += 1
        
        return poderAtual

    def briga(self) -> int:
        """
        Compara cartas e retorna o vencedor
        
        Returns:
            int: Índice do jogador vencedor ou -1 se empardar
        """
        poder: List[int] = []
        
        for carta in self.cartas_jogadas:
            poderAtual: int = self._calcular_poder(carta)
            poder.append(poderAtual)
        
        poderOrganizado: List[int] = poder[:]
        poderOrganizado.sort()
        
        # Verifica se empatou (dois maiores iguais)
        if poderOrganizado[-1] == poderOrganizado[-2]:
            return -1
        else:
            maior: int = max(poder)
            vencedor: int = poder.index(maior)
        
        return vencedor

    def verificar_empardamento(self) -> Tuple[bool, List[int]]:
        """
        Verifica se cartas não-manilhas empardalas
        
        Returns:
            Tuple[bool, List[int]]: (empadou, índices das cartas iguais)
        """
        numeros: List[str] = [carta.numero for carta in self.cartas_jogadas]
        
        if len(set(numeros)) == 1:
            numero: str = numeros[0]
            
            if numero != self.manilha:
                return True, list(range(len(self.cartas_jogadas)))
        
        return False, []

    def descartar_empardalas(self) -> List[Carta]:
        """
        Descarta cartas empardalas e retorna próximas mais fortes
        
        Returns:
            List[Carta]: Cartas sem as empardalas
        """
        if not self.cartas_jogadas:
            return []
        
        numeros: List[str] = [carta.numero for carta in self.cartas_jogadas]
        
        if len(set(numeros)) == 1:
            numero_empardalado: str = numeros[0]
            
            cartas_filtradas: List[Carta] = [
                carta for carta in self.cartas_jogadas 
                if carta.numero != numero_empardalado
            ]
            
            if cartas_filtradas:
                self.cartas_jogadas = cartas_filtradas
                return cartas_filtradas
            else:
                return self.cartas_originais
        
        return self.cartas_jogadas
