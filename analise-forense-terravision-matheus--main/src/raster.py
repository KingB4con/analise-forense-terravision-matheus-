import rasterio
import numpy as np

from pathlib import Path
from rasterio.enums import Resampling


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


def carregar_imagem_raster(caminho, max_dimensao=1800):
    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError("Arquivo não encontrado.")

    with rasterio.open(caminho) as raster:

        if raster.crs is None:
            raise ValueError(
                "O GeoTIFF não possui sistema de coordenadas (CRS)."
            )

        escala = min(
            1.0,
            max_dimensao / max(raster.width, raster.height)
        )

        nova_largura = max(1, int(raster.width * escala))
        nova_altura = max(1, int(raster.height * escala))

        dimensoes = (nova_altura, nova_largura)

        if raster.count >= 3:
            dados = raster.read(
                indexes=[1, 2, 3],
                out_shape=(3, nova_altura, nova_largura),
                resampling=Resampling.average,
                masked=True
            )

            canais = []

            for banda in dados:
                valores = banda.compressed()

                if valores.size == 0:
                    raise ValueError(
                        "O raster não possui pixels válidos."
                    )

                minimo, maximo = np.percentile(
                    valores, [2, 98]
                )

                if maximo <= minimo:
                    maximo = minimo + 1

                normalizada = np.clip(
                    (banda.filled(minimo) - minimo)
                    / (maximo - minimo),
                    0,
                    1
                )

                canais.append(normalizada)

            imagem = np.stack(canais, axis=-1)
            tipo = "rgb"

        else:
            imagem = raster.read(
                1,
                out_shape=dimensoes,
                resampling=Resampling.average,
                masked=True
            )

            if imagem.count() == 0:
                raise ValueError(
                    "O raster não possui pixels válidos."
                )

            tipo = "elevacao"

        limites = raster.bounds

        extent = (
            limites.left,
            limites.right,
            limites.bottom,
            limites.top
        )

        informacoes = {
            "crs": str(raster.crs),
            "resolucao": raster.res,
            "largura_original": raster.width,
            "altura_original": raster.height,
            "largura_renderizada": nova_largura,
            "altura_renderizada": nova_altura
        }

        return imagem, extent, tipo, informacoes