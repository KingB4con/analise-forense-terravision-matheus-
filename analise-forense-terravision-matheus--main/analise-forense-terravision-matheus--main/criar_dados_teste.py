
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

# Elevação inicial
anterior = np.array([
    [100, 100, 100],
    [100, 100, 100],
    [100, 100, 100]
], dtype="float32")

# Elevação posterior
posterior = np.array([
    [95, 100, 105],
    [90, 100, 110],
    [95, 100, 105]
], dtype="float32")

with rasterio.open("dados/entrada/anterior.tif", "w", **perfil) as arquivo:
    arquivo.write(anterior, 1)

with rasterio.open("dados/entrada/posterior.tif", "w", **perfil) as arquivo:
    arquivo.write(posterior, 1)

print("Dados artificiais criados com sucesso!")
