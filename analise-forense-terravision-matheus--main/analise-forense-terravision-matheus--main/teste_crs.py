import numpy as np
import rasterio
from rasterio.transform import from_bounds
from rasterio.warp import transform_bounds

# Limites geográficos aproximados do MDE anterior
limites = transform_bounds(
    "EPSG:4326",
    "EPSG:3857",
    -50.000,
    -5.003,
    -49.997,
    -5.000
)

# Pequena margem para garantir cobertura completa
largura = limites[2] - limites[0]
altura = limites[3] - limites[1]

esquerda = limites[0] - largura * 0.01
direita = limites[2] + largura * 0.01
inferior = limites[1] - altura * 0.01
superior = limites[3] + altura * 0.01

perfil = {
    "driver": "GTiff",
    "height": 6,
    "width": 6,
    "count": 1,
    "dtype": "float32",
    "crs": "EPSG:3857",
    "transform": from_bounds(
        esquerda, inferior, direita, superior, 6, 6
    ),
    "nodata": -9999
}

dados = np.full((6, 6), 100, dtype="float32")

with rasterio.open(
    "dados/entrada/posterior_crs.tif",
    "w",
    **perfil
) as arquivo:
    arquivo.write(dados, 1)

print("GeoTIFF com CRS diferente criado!")