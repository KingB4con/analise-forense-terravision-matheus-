
import json
from pathlib import Path
from uuid import uuid4

ARQUIVO_AREAS = Path(__file__).resolve().parent / "dados" / "areas.json"


def listar_areas():
    if not ARQUIVO_AREAS.exists():
        return []

    with open(ARQUIVO_AREAS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_areas(areas):
    ARQUIVO_AREAS.parent.mkdir(parents=True, exist_ok=True)

    with open(ARQUIVO_AREAS, "w", encoding="utf-8") as arquivo:
        json.dump(areas, arquivo, indent=4, ensure_ascii=False)


def cadastrar_area(nome, localizacao, descricao=""):
    nome = nome.strip()
    localizacao = localizacao.strip()

    if not nome or not localizacao:
        raise ValueError("Nome e localização são obrigatórios.")

    areas = listar_areas()

    for area in areas:
        if area["nome"].casefold() == nome.casefold():
            raise ValueError("Já existe uma área com esse nome.")

    nova_area = {
        "id": str(uuid4()),
        "nome": nome,
        "localizacao": localizacao,
        "descricao": descricao.strip(),
        "rasters": []
    }

    areas.append(nova_area)
    salvar_areas(areas)

    return nova_area


def excluir_area(area_id):
    areas = listar_areas()

    areas_atualizadas = [
        area for area in areas if area["id"] != area_id
    ]

    if len(areas_atualizadas) == len(areas):
        return False

    salvar_areas(areas_atualizadas)
    return True


def listar_rasters(area_id):
    for area in listar_areas():
        if area["id"] == area_id:
            return area.get("rasters", [])

    return []


def registrar_raster(area_id, metadados):
    areas = listar_areas()

    for area in areas:
        if area["id"] == area_id:
            area.setdefault("rasters", [])

            caminho = metadados["caminho"]

            for raster in area["rasters"]:
                if raster["caminho"] == caminho:
                    raise ValueError("Esse arquivo já está associado à área.")

            dados = dict(metadados)
            dados["resolucao"] = list(dados["resolucao"])
            dados["tipo_dado"] = list(dados["tipo_dado"])

            area["rasters"].append(dados)
            salvar_areas(areas)
            return dados

    raise ValueError("Área não encontrada.")
