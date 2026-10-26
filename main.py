
from areas import consultar_areas
from carregar_camada import carregar_camada_satelite


def exibir_menu():
    print("\n" + "=" * 35)
    print("          MINEVISION")
    print("=" * 35)
    print("Análise de mineração e alterações topográficas")
    print()
    print("1 - Consultar áreas cadastradas")
    print("2 - Carregar camada geográfica")
    print("3 - Sobre o projeto")
    print("0 - Sair")
    print("=" * 35)


def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            consultar_areas()

        elif opcao == "2":
            carregar_camada()

        elif opcao == "3":
            print("\nMineVision")
            print("Projeto de análise de áreas de mineração")
            print("e alterações da topografia terrestre.")

        elif opcao == "0":
            print("Encerrando o MineVision...")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
