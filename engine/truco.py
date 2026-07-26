from typing import Tuple, Dict, List, Optional


class Truco:
    def __init__(self) -> None:
        self.progressao: List[int] = [1, 3, 6, 9, 12]
        self.indice_atual: int = 0
        self.time_que_pediu: Optional[int] = None
        self.resposta: str = "aguardando"
        self.historico: List[str] = []

    def get_valor(self) -> int:
        """Retorna o valor atual da aposta"""
        return self.progressao[self.indice_atual]

    def pode_pedir_truco(self, pontos_time1: int, pontos_time2: int) -> Tuple[bool, str]:
        """
        Verifica se é permitido pedir truco
        Bloqueia em mão de 11 e mão de ferro
        
        Args:
            pontos_time1: Pontos do Time 1
            pontos_time2: Pontos do Time 2
        
        Returns:
            Tuple[bool, str]: (pode_pedir, motivo)
        """
        if (pontos_time1 == 11 and pontos_time2 != 11) or (pontos_time2 == 11 and pontos_time1 != 11):
            return False, "Mão de 11! Não pode pedir truco"
        
        if pontos_time1 == 11 and pontos_time2 == 11:
            return False, "Mão de ferro! Não pode pedir truco"
        
        return True, "OK"

    def pedir_truco(self, time_que_pediu: int) -> bool:
        """
        Time tenta pedir truco
        
        Args:
            time_que_pediu: 1 ou 2
        
        Returns:
            bool: True se conseguiu pedir
        """
        if self.resposta == "aguardando":
            self.time_que_pediu = time_que_pediu
            self.resposta = "aguardando_resposta"
            valor_novo: int = self.get_valor()
            self.historico.append(f"Time {time_que_pediu} pediu {valor_novo} pontos")
            return True
        
        elif self.resposta == "aceito" and self.indice_atual < len(self.progressao) - 1:
            self.indice_atual += 1
            self.time_que_pediu = time_que_pediu
            self.resposta = "aguardando_resposta"
            valor_novo = self.get_valor()
            self.historico.append(f"Time {time_que_pediu} ofereceu {valor_novo} pontos")
            return True
        
        return False

    def responder(self, time_que_responde: int, resposta: str) -> Dict:
        """
        Time responde ao pedido de truco
        
        Args:
            time_que_responde: 1 ou 2
            resposta: "aceito", "corrido" ou "truco"
        
        Returns:
            Dict: Resultado da resposta
        """
        if resposta == "aceito":
            self.resposta = "aceito"
            valor: int = self.get_valor()
            self.historico.append(f"Time {time_que_responde} aceitou {valor} pontos")
            return {
                "resultado": "aceito",
                "valor": valor,
                "mensagem": f"Time {time_que_responde} aceitou! Jogando por {valor} pontos"
            }
        
        elif resposta == "corrido":
            valor_aposta_anterior: int = self.progressao[self.indice_atual - 1] if self.indice_atual > 0 else 1
            self.resposta = "corrido"
            self.historico.append(f"Time {time_que_responde} correu. Time {self.time_que_pediu} ganha {valor_aposta_anterior}")
            return {
                "resultado": "corrido",
                "time_vencedor": self.time_que_pediu,
                "valor": valor_aposta_anterior,
                "mensagem": f"Time {time_que_responde} correu! Time {self.time_que_pediu} ganha {valor_aposta_anterior} pontos"
            }
        
        elif resposta == "truco":
            if self.indice_atual < len(self.progressao) - 1:
                self.indice_atual += 1
                self.time_que_pediu = time_que_responde
                self.resposta = "aguardando_resposta"
                valor_novo: int = self.get_valor()
                self.historico.append(f"Time {time_que_responde} ofereceu {valor_novo} pontos (contra-oferta)")
                return {
                    "resultado": "contra",
                    "valor": valor_novo,
                    "mensagem": f"Time {time_que_responde} ofereceu {valor_novo}! Time {self.time_que_pediu} decide"
                }
            else:
                return {
                    "resultado": "erro",
                    "mensagem": "Já atingiu o máximo (12 pontos)!"
                }
        
        return {
            "resultado": "erro",
            "mensagem": "Resposta inválida"
        }

    def reset(self) -> None:
        """Reseta tudo para nova rodada"""
        self.indice_atual = 0
        self.time_que_pediu = None
        self.resposta = "aguardando"
        self.historico = []

    def get_status(self) -> Dict:
        """Retorna o status atual do truco para debug"""
        return {
            "valor_atual": self.get_valor(),
            "time_que_pediu": self.time_que_pediu,
            "resposta": self.resposta,
            "historico": self.historico
        }
