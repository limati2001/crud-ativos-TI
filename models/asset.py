from enum import Enum
from typing import List
from models.vulnerability import Vulnerabilidade

class TipoAtivo(Enum):
    NOTEBOOK = 1
    SERVIDOR = 2
    ROTEADOR = 3
    CAFETEIRA = 4

class AtivoTI:
    def __init__(self, id_ativo: int, hostname: str, responsavel: str, localizacao: str, tipo: TipoAtivo):
        self.id = id_ativo
        self.hostname = hostname
        self.responsavel = responsavel
        self.localizacao = localizacao
        self.tipo = tipo 
        self.vulnerabilidades: List[Vulnerabilidade] = []

    def adicionar_vulnerabilidade(self, vuln: Vulnerabilidade):
         self.vulnerabilidades.append(vuln)        