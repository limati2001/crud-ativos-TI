from services.asset_service import AssetService
from services.vulnerability_service import VulnerabilityService
from models.asset import TipoAtivo

def exibir_menu():
    print("\n" + "=" *40)
    print(" Inventário de Ativos e Vulnerabilidades")
    print("="*40)
    print("[1] Cadastrar Novo Ativo de TI")
    print("[2] Buscar Ativo (por ID ou Hostname)")
    print("[3] Atualizar Ativo Existente")
    print("[4] Deletar Ativo (e suas vulnerabilidades)")
    print("[5] Cadastrar Vulnerabilidade em um Ativo")
    print("[6] Visualizar Vulnerabilidades de um Ativo")
    print("[0] Sair do Sistema")
    print("="*40)

def main():
    asset_service= AssetService()
    vulnerability_service = VulnerabilityService(asset_service)

    while True:
        exibir_menu()
        opcao = input("Selecione uma opção: ").strip()

        if opcao == "1":
            print("\n--- CADASTRO DE ATIVO ---")
            try:
                id_ativo = int(input("ID Único (Inteiro): "))
                hostname = input("Hostname/Nome: ").strip()
                responsavel = input("Responsável: ").strip()
                localizacao = input("Setor/Localização: ").strip()

                print("\nCategorias disponíveis")
                for tipo in TipoAtivo:
                    print(f" {tipo.value} - {tipo.name}")

                codigo_tipo = int(input("Escolha o código do tipo de ativo: "))
                tipo_ativo = TipoAtivo(codigo_tipo)

                if asset_service.cadastrar_ativo(id_ativo, hostname, responsavel, localizacao, tipo_ativo):
                    print("Ativo cadastrado com êxito.")
            except ValueError:
                print("Erro: Entrada inválida. Certifique-se de digitar números para o ID e Código do Tipo")
            except Exception as e:
                print(f"Erro inesperado: {e}")

        elif opcao == "2":
            print("\n--- BUSCAR ATIVO ---")
            print("[1] Buscar por ID")
            print("[2] Buscar por Hostname")
            sub_opcao = input("Escolha o método de busca: ").strip()

            if sub_opcao == "1":
                try:
                    id_busca = int(input("Digite o ID do ativo: "))
                    ativo = asset_service.buscar_por_id(id_busca)
                    if ativo:
                        print(f"\nAchou! ID: {ativo.id} | Hostname: {ativo.hostname} | Responsável: {ativo.responsavel} | Localização: {ativo.localizacao} | Tipo: {ativo.tipo.name}")
                    else:
                        print("Ativo não encontrado")
                except ValueError:
                    print("Erro: O ID deve ser um número inteiro.")
            elif sub_opcao == "2":
                host_busca = input("Digite o Hostname: ").strip()
                ativo = asset_service.buscar_por_hostname(host_busca)
                if ativo:
                    print(f"\nAchou! ID: {ativo.id} | Hostname: {ativo.hostname} | Responsável: {ativo.responsavel} | Localização: {ativo.localizacao} | Tipo: {ativo.tipo.name}")
                else:
                    print("Ativo não encontrado")

        elif opcao == "3":
            print("\n--- Atualizar Ativo ---")
            try:
                id_ativo = int(input("Digite o ID do ativo que deseja atualizar: "))
                # verifica primeiro se existe antes de pedir os novos dados
                if not asset_service.buscar_por_id(id_ativo):
                    print("Erro: Ativo não encontrado.")
                    continue
                
                novo_hostname = input("Novo Hostname/Nome: ").strip()
                novo_responsavel = input("Novo Responsável: ").strip()
                nova_localizacao = input("Nova Setor/Localização: ").strip()

                print("\nCategorias disponíveis:")
                for tipo in TipoAtivo:
                    print(f"  {tipo.value} - {tipo.name}")
                codigo_tipo = int(input("Escolha o novo código do tipo: "))
                novo_tipo = TipoAtivo(codigo_tipo)
                asset_service.atualizar_ativo(id_ativo, novo_hostname, novo_responsavel, nova_localizacao, novo_tipo)
        
            except ValueError:
                print("Erro: Entrada inválida.")

        elif opcao == "4":
            print("\n--- DELETAR ATIVO ---")
            try:
                id_ativo = int(input("Digite o ID do ativo a ser excluído: "))
                asset_service.deletar_ativo(id_ativo)
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")

        elif opcao == "5":
            print("\n--- CADASTRAR VULNERABILIDADE ---")
            try:
                id_ativo = int(input("ID do Ativo afetado: "))
                descricao = input("Descrição da vulnerabilidade: ").strip()
                categoria = input("Categoria/Tipo (Ex: Senha Fraca, Desatualizado): ").strip()
                severidade = input("Severidade (Baixa, Média, Alta, Crítica): ").strip()
                status = input("Status (Aberta, Em tratamento, Corrigida): ").strip()

                vulnerability_service.cadastrar_vulnerabilidade_no_ativo(id_ativo, descricao, categoria, severidade, status)
            except ValueError:
                print("Erro: O ID do ativo deve ser um número inteiro.")

        elif opcao == "6":
            print("\n--- VISUALIZAR VULNERABILIDADES ---")
            try:
                id_ativo = int(input("Digite o ID do ativo: "))
                vulnerability_service.visualizar_vulnerabilidades_do_ativo(id_ativo)
            except ValueError:
                print("Erro: O ID deve ser um número inteiro.")

        elif opcao == "0":
            print("\nSaindo do sistema de segurança")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()