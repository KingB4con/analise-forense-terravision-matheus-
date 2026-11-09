
import numpy as np
import rasterio
from rasterio.transform import from_origin

perfil = {
    "driver": "GTiff",
    "height": 3,
    "width": 3,
    "count": 1,
    "dtype": "float32",
    "crs": "EPSG:4326",
    "transform": from_origin(-49.990, -5.000, 0.001, 0.001),
    "nodata": -9999
}

dados = np.full((3, 3), 100, dtype="float32")

with rasterio.open(
    "dados/entrada/posterior_sem_sobreposicao.tif",
    "w",
    **perfil
) as arquivo:
    arquivo.write(dados, 1)

print("Raster sem sobreposição criado!")
