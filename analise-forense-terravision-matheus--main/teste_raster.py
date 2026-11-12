
from src.raster import ler_metadados
from pathlib import Path

pasta = Path("dados/entrada")

arquivos = list(pasta.glob("*.tif")) + list(pasta.glob("*.tiff"))

if not arquivos:
    print("Nenhum GeoTIFF encontrado em dados/entrada.")
else:
    for arquivo in arquivos:
        print("\n--- METADADOS DO RASTER ---")

        try:
            metadados = ler_metadados(arquivo)

            for chave, valor in metadados.items():
                print(f"{chave}: {valor}")

        except Exception as erro:
            print(f"Erro: {erro}")
