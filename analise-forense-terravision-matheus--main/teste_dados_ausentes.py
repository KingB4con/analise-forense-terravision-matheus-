
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
    "transform": from_origin(-50, -5, 0.001, 0.001),
    "nodata": -9999
}

# MDE anterior
anterior = np.array([
    [100, 100, 100],
    [100, 100, 100],
    [100, 100, 100]
], dtype="float32")

# MDE posterior com um pixel sem informação
posterior = np.array([
    [105, 100, 95],
    [110, -9999, 90],
    [105, 100, 95]
], dtype="float32")

for nome, dados in [
    ("anterior_ausentes.tif", anterior),
    ("posterior_ausentes.tif", posterior)
]:
    with rasterio.open(
        f"dados/entrada/{nome}",
        "w",
        **perfil
    ) as arquivo:
        arquivo.write(dados, 1)

print("Arquivos com dados ausentes criados!")
