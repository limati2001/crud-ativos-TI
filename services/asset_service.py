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
        if not os.path.exists(self.file_path):
            return
        
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                #ex. de linha separada por ";"
                #id;hostname;responsavel;localizacao;codigo_tipo
                parts = line.split(";")
                if len(parts) >=5:
                    id_ativo = int(parts[0])
                    hostname = parts[1]
                    responsavel = parts[2]
                    localizacao = parts[3]
                    codigo_tipo = int(parts[4])

                #reconstrói o enum tipo ativo a partir do código inteiro
                tipo = TipoAtivo(codigo_tipo)

                #cria o objeto e adiciona no dicionário indexado
                ativo = AtivoTI(id_ativo, hostname, responsavel, localizacao, tipo)
                self.assets_indexed[id_ativo] = ativo
    
    def _save_to_file(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            for ativo in self.assets_indexed.values():
                line = f"{ativo.id};{ativo.hostname};{ativo.responsavel};{ativo.localizacao};{ativo.tipo.value}\n"
                f.write(line)

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


    
