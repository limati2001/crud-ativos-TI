import os
from models.asset import AtivoTI, TipoAtivo

class AssetService:
    def __init__(self, file_path="data/assets.txt"):
        self.file_path = file_path
        #requisito 9
        self.assets_indexed: dict[int, AtivoTI] = {}

        #verificar/garantir que a pasta data exista
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        #carrega os dados existentes ao iniciar o service
        self._load_from_file()

    def _load_from_file(self):
        """Carrega os ativos e reconstrói as vulnerabilidades a partir do arquivo (Requisito 3, 7 e 9)."""
        import os
        from models.asset import AtivoTI, TipoAtivo
        from models.vulnerability import Vulnerabilidade

        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        continue
                    
                    partes = linha.split(";")
                    # Uma linha válida de ativo básico precisa de pelo menos 5 campos + campo de vulnerabilidade
                    if len(partes) < 5:
                        continue
                        
                    id_ativo = int(partes[0])
                    hostname = partes[1]
                    responsavel = partes[2]
                    localizacao = partes[3]
                    tipo = TipoAtivo(int(partes[4]))
                    
                    # Cria o objeto Ativo de TI
                    ativo = AtivoTI(id_ativo, hostname, responsavel, localizacao, tipo)
                    
                    # Verifica se existem vulnerabilidades registradas nessa linha (campo após o índice 4)
                    if len(partes) > 5 and partes[5]:
                        vulns_brutas = partes[5].split("::")
                        for vuln_str in vulns_brutas:
                            dados_v = vuln_str.split("||")
                            if len(dados_v) == 4:
                                desc, cat, sev, stat = dados_v
                                nova_vuln = Vulnerabilidade(desc, cat, sev, stat)
                                ativo.adicionar_vulnerabilidade(nova_vuln)
                    
                    # Alimenta os nossos dicionários de busca rápida em memória (Requisito 9)
                    self.assets_indexed[id_ativo] = ativo
                    self.assets_by_hostname[hostname.lower()] = ativo
        except Exception as e:
            print(f"Aviso: Erro ao carregar a base de dados em texto: {e}")
    
    def _save_to_file(self):
        """Salva todos os ativos e suas vulnerabilidades no arquivo de texto (Requisito 3 e 7)."""
        import os
        # Garante que a pasta 'data' existe
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        with open(self.file_path, "w", encoding="utf-8") as f:
            for ativo in self.assets_indexed.values():
                # 1 cria a string com os dados básicos do Ativo
                linha_ativo = f"{ativo.id};{ativo.hostname};{ativo.responsavel};{ativo.localizacao};{ativo.tipo.value}"
                
                # 2 transforma a lista de vulnerabilidades em texto serializado
                lista_vulns_str = []
                for v in ativo.vulnerabilidades:
                    # Usamos '||' para separar os campos de uma única vulnerabilidade
                    vuln_formatada = f"{v.descricao}||{v.categoria}||{v.severidade}||{v.status}"
                    lista_vulns_str.append(vuln_formatada)
                
                # unir todas as vulnerabilidades usando '::' como separador entre elas
                vulnerabilidades_serializadas = "::".join(lista_vulns_str)
                
                # 3 junta tudo na linha final do arquivo
                if vulnerabilidades_serializadas:
                    f.write(f"{linha_ativo};{vulnerabilidades_serializadas}\n")
                else:
                    f.write(f"{linha_ativo};\n")  # Ponto e vírgula no fim indica lista vazia

    def cadastrar_ativo(self, id_ativo:int, hostname: str, responsavel: str, localizacao: str, tipo: TipoAtivo) -> bool:
        if id_ativo in self.assets_indexed:
            print("Erro: Já existe um ativo cadastrado com este ID (único!).")
            return False
        
        novo_ativo = AtivoTI(id_ativo, hostname, responsavel, localizacao, tipo)

        #salva no dicionário
        self.assets_indexed[id_ativo] = novo_ativo

        #persiste no arquivo de texto (pré SQLite)
        self._save_to_file()
        return True
    
    def buscar_por_id(self, id_ativo: int) -> AtivoTI | None:
        return self.assets_indexed.get(id_ativo)
    
    def buscar_por_hostname(self, hostname: str) -> AtivoTI | None:
        for ativo in self.assets_indexed.values():
            if ativo.hostname.lower() == hostname.lower():
                return ativo
        return None
    

    def atualizar_ativo(self, id_ativo: int, novo_hostname: str, novo_responsavel: str, nova_localizacao: str, novo_tipo:TipoAtivo) -> bool:
        ativo = self.buscar_por_id(id_ativo)

        if not ativo:
            print(f"Erro: Ativo com ID {id_ativo} não foi encontrado para atualização!")
            return False
        
        #atualiza os dados do objeto na memória

        ativo.hostname = novo_hostname
        ativo.responsavel = novo_responsavel
        ativo.localizacao = nova_localizacao
        ativo.tipo = novo_tipo

        #persiste a alteração no arquivo de texto (Pré-SQLite!)
        self._save_to_file()
        print(f"Ativo ID {id_ativo} atualizado com sucesso!")
        return True
    
    def deletar_ativo(self, id_ativo: int) -> bool:
        if id_ativo not in self.assets_indexed:
            print(f"Erro: ativo com ID {id_ativo} não existe na base de dados!")
            return False
        
        #remove do dicionário indexado
        del self.assets_indexed[id_ativo]

        #reescreve o arquivo de texto sem o ativo deletado
        self._save_to_file()
        print(f"Ativo ID {id_ativo} e suas vulnerabilidades foram removidos com sucesso!")
        return True


    
