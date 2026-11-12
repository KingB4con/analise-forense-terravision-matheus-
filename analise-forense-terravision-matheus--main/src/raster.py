
import rasterio
from pathlib import Path


def ler_metadados(caminho):
    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError("Arquivo não encontrado.")

    if caminho.suffix.lower() not in (".tif", ".tiff"):
        raise ValueError("Formato inválido. Selecione um GeoTIFF.")

    with rasterio.open(caminho) as raster:
        return {
            "nome": caminho.name,
            "caminho": str(caminho.resolve()),
            "largura": raster.width,
            "altura": raster.height,
            "bandas": raster.count,
            "crs": str(raster.crs) if raster.crs else "Não definido",
            "resolucao": raster.res,
            "tipo_dado": raster.dtypes,
            "nodata": raster.nodata
        }
