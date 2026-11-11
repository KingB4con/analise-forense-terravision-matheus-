import json
from pathlib import Path
from uuid import uuid4

ARQUIVO_AREAS = Path(__file__).resolve().parent / "dados" / "areas.json"


def listar_areas():
    if not ARQUIVO_AREAS.exists():
        return []

    with open(ARQUIVO_AREAS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


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
        "descricao": descricao.strip()
    }

    areas.append(nova_area)

    ARQUIVO_AREAS.parent.mkdir(parents=True, exist_ok=True)

    with open(ARQUIVO_AREAS, "w", encoding="utf-8") as arquivo:
        json.dump(areas, arquivo, indent=4, ensure_ascii=False)

    return nova_area


def excluir_area(area_id):
    areas = listar_areas()
    areas_atualizadas = [
        area for area in areas if area["id"] != area_id
    ]

    if len(areas_atualizadas) == len(areas):
        return False

    with open(ARQUIVO_AREAS, "w", encoding="utf-8") as arquivo:
        json.dump(areas_atualizadas, arquivo, indent=4, ensure_ascii=False)

    return True