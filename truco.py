class Truco:
    def __init__(self):
        # valores da rodada do truco
        self.progressao = [1, 3, 6, 9, 12]
        
        # indice da progressao
        self.indice_atual = 0
        
        # qual time pediu?(1, 2)
        self.time_que_pediu = None
        
        # Qual é a resposta? (aceito, corrido, contra, aguardando)
        self.resposta = "aguardando"
        
        # Histórico de ofertas (pra debug/logs)
        self.historico = []

    def get_valor(self):
        """Retorna o valor atual da aposta"""
        return self.progressao[self.indice_atual]

    def pode_pedir_truco(self, pontos_time1, pontos_time2):
        """
        Verifica se é permitido pedir truco
        Bloqueia em mão de 11 e mão de ferro
        
        Args:
            pontos_time1: Pontos do Time 1
            pontos_time2: Pontos do Time 2
        
        Returns:
            tuple: (pode_pedir: bool, motivo: str)
        """
        # Mão de 11: um time tem 11 e outro não
        if (pontos_time1 == 11 and pontos_time2 != 11) or (pontos_time2 == 11 and pontos_time1 != 11):
            return False, "Mão de 11! Não pode pedir truco"
        
        # Mão de ferro: ambos com 11
        if pontos_time1 == 11 and pontos_time2 == 11:
            return False, "Mão de ferro! Não pode pedir truco"
        
        return True, "OK"

    def pedir_truco(self, time_que_pediu):
        """
        Time tenta pedir truco
        
        Args:
            time_que_pediu: 1 ou 2 (qual time está pedindo)
        
        Returns:
            bool: True se conseguiu pedir, False se não pode
        """
        # Só pode pedir se não tiver pedido antes nessa rodada
        # ou se a resposta anterior foi 'aceito' e agora quer aumentar
        
        if self.resposta == "aguardando":
            # Primeira oferta da rodada
            self.time_que_pediu = time_que_pediu
            self.resposta = "aguardando_resposta"
            valor_novo = self.get_valor()
            self.historico.append(f"Time {time_que_pediu} pediu {valor_novo} pontos")
            return True
        
        elif self.resposta == "aceito" and self.indice_atual < len(self.progressao) - 1:
            # Pode aumentar a aposta se o outro time aceitar
            self.indice_atual += 1
            self.time_que_pediu = time_que_pediu
            self.resposta = "aguardando_resposta"
            valor_novo = self.get_valor()
            self.historico.append(f"Time {time_que_pediu} ofereceu {valor_novo} pontos")
            return True
        
        return False

    def responder(self, time_que_responde, resposta):
        """
        Time responde ao pedido de truco
        
        Args:
            time_que_responde: 1 ou 2 (qual time está respondendo)
            resposta: "aceito", "corrido" ou "truco" (contra)
        
        Returns:
            dict: informações sobre o resultado
        """
        if resposta == "aceito":
            # Time aceita a nova aposta
            self.resposta = "aceito"
            valor = self.get_valor()
            self.historico.append(f"Time {time_que_responde} aceitou {valor} pontos")
            return {
                "resultado": "aceito",
                "valor": valor,
                "mensagem": f"Time {time_que_responde} aceitou! Jogando por {valor} pontos"
            }
        
        elif resposta == "corrido":
            # Time desiste e perde a aposta ANTERIOR
            valor_aposta_anterior = self.progressao[self.indice_atual - 1] if self.indice_atual > 0 else 1
            self.resposta = "corrido"
            self.historico.append(f"Time {time_que_responde} correu. Time {self.time_que_pediu} ganha {valor_aposta_anterior}")
            return {
                "resultado": "corrido",
                "time_vencedor": self.time_que_pediu,
                "valor": valor_aposta_anterior,
                "mensagem": f"Time {time_que_responde} correu! Time {self.time_que_pediu} ganha {valor_aposta_anterior} pontos"
            }
        
        elif resposta == "truco":
            # Time faz uma contra-oferta (sobe um nível)
            if self.indice_atual < len(self.progressao) - 1:
                self.indice_atual += 1
                self.time_que_pediu = time_que_responde  # Agora quem pediu é o outro
                self.resposta = "aguardando_resposta"
                valor_novo = self.get_valor()
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

    def reset(self):
        """Reseta tudo pra nova rodada"""
        self.indice_atual = 0
        self.time_que_pediu = None
        self.resposta = "aguardando"
        self.historico = []

    def get_status(self):
        """Retorna o status atual do truco (pra debug)"""
        return {
            "valor_atual": self.get_valor(),
            "time_que_pediu": self.time_que_pediu,
            "resposta": self.resposta,
            "historico": self.historico
        }
