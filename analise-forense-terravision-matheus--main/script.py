def obter_configuracao_lod(altitude):
    altitude = float(altitude)

    if altitude < 0:
        raise ValueError("A altitude não pode ser negativa.")

    if altitude > 10000:
        return {
            "nivel": "BAIXA RESOLUÇÃO",
            "max_dimensao": 512,
            "elemento": "Visão regional da área de mineração."
        }

    elif altitude >= 1000:
        return {
            "nivel": "MÉDIA RESOLUÇÃO",
            "max_dimensao": 1024,
            "elemento": "Visão intermediária do relevo e das estruturas."
        }

    else:
        return {
            "nivel": "ALTA RESOLUÇÃO",
            "max_dimensao": 1800,
            "elemento": "Detalhamento de cavas, bancadas e estruturas."
        }


def carregar_camada_satelite(lista_altitudes):
    if len(lista_altitudes) < 5:
        raise ValueError(
            "Informe pelo menos 5 valores de altitude."
        )

    resultados = []

    print("\n--- SISTEMA DE NÍVEL DE DETALHE - MINEVISION ---")

    for altitude in lista_altitudes:
        configuracao = obter_configuracao_lod(altitude)

        resultado = {
            "altitude": float(altitude),
            **configuracao
        }

        resultados.append(resultado)

        print(f"\nAltitude: {resultado['altitude']:.2f} metros")
        print(f"Nível: {resultado['nivel']}")
        print(f"Renderização: {resultado['elemento']}")

    return resultados


if __name__ == "__main__":
    altitudes_teste = [
        25000, 15000, 8000,
        3000, 500, 100
    ]

    carregar_camada_satelite(altitudes_teste)