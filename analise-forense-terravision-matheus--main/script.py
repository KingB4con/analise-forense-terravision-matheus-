
def carregar_camada_satelite(lista_altitudes):
    """
    Simula a seleção do nível de detalhe (LoD)
    conforme a altitude da câmera virtual.
    """

    if len(lista_altitudes) < 5:
        raise ValueError(
            "Informe pelo menos 5 valores de altitude."
        )

    resultados = []

    print("\n--- SISTEMA DE NÍVEL DE DETALHE - MINEVISION ---")

    for altitude in lista_altitudes:
        altitude = float(altitude)

        if altitude < 0:
            raise ValueError("A altitude não pode ser negativa.")

        if altitude > 10000:
            nivel = "BAIXA RESOLUÇÃO"
            elemento = "Mosaico geral da Terra e localização regional das áreas de mineração."

        elif altitude >= 1000:
            nivel = "MÉDIA RESOLUÇÃO"
            elemento = "Mosaico regional de mineração, vegetação, relevo e limites das áreas de exploração."

        else:
            nivel = "ALTA RESOLUÇÃO"
            elemento = "Topografia detalhada de cavas, bancadas, pilhas de rejeitos e estruturas de mineração."

        resultado = {
            "altitude": altitude,
            "nivel": nivel,
            "elemento": elemento
        }

        resultados.append(resultado)

        print(f"\nAltitude: {altitude:.2f} metros")
        print(f"Nível: {nivel}")
        print(f"Renderização: {elemento}")

    return resultados


if __name__ == "__main__":
    altitudes_teste = [
        25000,
        15000,
        8000,
        3000,
        500,
        100
    ]

    carregar_camada_satelite(altitudes_teste)
