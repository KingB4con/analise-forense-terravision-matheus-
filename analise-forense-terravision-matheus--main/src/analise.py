from pathlib import Path
import csv
import numpy as np
import rasterio
from rasterio.vrt import WarpedVRT
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def analisar_mdes(arquivo_anterior, arquivo_posterior, pasta_saida):
    """Compara dois MDEs e grava GeoTIFF, PNGs, CSV e retorna estatísticas."""
    anterior = Path(arquivo_anterior)
    posterior = Path(arquivo_posterior)
    saida = Path(pasta_saida)
    saida.mkdir(parents=True, exist_ok=True)

    if not anterior.is_file() or not posterior.is_file():
        raise FileNotFoundError("Selecione dois arquivos GeoTIFF existentes.")

    with rasterio.open(anterior) as src_a, rasterio.open(posterior) as src_p:
        if src_a.crs is None or src_p.crs is None:
            raise ValueError("Os dois rasters precisam ter sistema de coordenadas (CRS).")

        # Alinha o raster posterior à grade do anterior, reprojetando se necessário.
        with WarpedVRT(
            src_p,
            crs=src_a.crs,
            transform=src_a.transform,
            width=src_a.width,
            height=src_a.height,
            resampling=Resampling.bilinear,
            nodata=src_p.nodata
        ) as aligned_p:
            a = src_a.read(1, masked=True).astype("float32")
            p = aligned_p.read(1, masked=True).astype("float32")

            invalid = np.ma.getmaskarray(a) | np.ma.getmaskarray(p)
            av = np.asarray(a.filled(np.nan), dtype="float32")
            pv = np.asarray(p.filled(np.nan), dtype="float32")
            diff = pv - av
            invalid |= ~np.isfinite(diff)
            diff[invalid] = np.nan

            valid = diff[np.isfinite(diff)]
            if valid.size == 0:
                raise ValueError("Não há área válida em comum entre os dois modelos.")

            profile = src_a.profile.copy()
            profile.update(
                driver="GTiff",
                dtype="float32",
                count=1,
                nodata=-9999.0,
                compress="deflate"
            )
            raster_path = saida / "diferenca_topografica.tif"
            out = np.where(np.isfinite(diff), diff, -9999.0).astype("float32")
            with rasterio.open(raster_path, "w", **profile) as dst:
                dst.write(out, 1)
                dst.set_band_description(1, "MDE posterior - MDE anterior (metros)")

            crs = str(src_a.crs)
            transform = src_a.transform
            shape = f"{src_a.height} x {src_a.width}"
            bounds = src_a.bounds
            res = src_a.res
            nodata_a = src_a.nodata
            nodata_p = src_p.nodata

    stats = {
        "pixels_validos": int(valid.size),
        "diferenca_media_m": float(np.mean(valid)),
        "diferenca_mediana_m": float(np.median(valid)),
        "diferenca_minima_m": float(np.min(valid)),
        "diferenca_maxima_m": float(np.max(valid)),
        "desvio_padrao_m": float(np.std(valid)),
        "percentil_05_m": float(np.percentile(valid, 5)),
        "percentil_95_m": float(np.percentile(valid, 95)),
        "crs": crs,
        "dimensoes": shape,
        "resolucao_raster": str(res),
        "limites_raster": str(bounds),
        "nodata_anterior": str(nodata_a),
        "nodata_posterior": str(nodata_p),
    }

    csv_path = saida / "estatisticas.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["indicador", "valor"])
        writer.writerows(stats.items())

    fig, ax = plt.subplots(figsize=(10, 7))
    image = ax.imshow(diff, cmap="RdYlBu", vmin=np.nanpercentile(valid, 2),
                      vmax=np.nanpercentile(valid, 98))
    ax.set_title("MineVision — diferença de elevação (posterior − anterior)")
    ax.set_xlabel("Colunas do raster")
    ax.set_ylabel("Linhas do raster")
    fig.colorbar(image, ax=ax, label="Diferença (m)")
    fig.tight_layout()
    map_path = saida / "mapa_diferencas.png"
    fig.savefig(map_path, dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(valid, bins=60)
    ax.set_title("Distribuição das diferenças de elevação")
    ax.set_xlabel("Diferença (m)")
    ax.set_ylabel("Quantidade de pixels")
    ax.grid(alpha=0.2)
    fig.tight_layout()
    hist_path = saida / "histograma_diferencas.png"
    fig.savefig(hist_path, dpi=180)
    plt.close(fig)

    return {
        "estatisticas": stats,
        "raster": str(raster_path),
        "mapa": str(map_path),
        "histograma": str(hist_path),
        "csv": str(csv_path),
    }
