from pathlib import Path
from datetime import datetime


def gerar_relatorio(resultados, arquivo_anterior, arquivo_posterior, pasta_saida,
                    descricao_area="Serra dos Carajás, Pará"):
    stats = resultados["estatisticas"]
    texto = f"""# Relatório — MineVision

## Identificação
- **Área de estudo:** {descricao_area}
- **Data de processamento:** {datetime.now().strftime("%d/%m/%Y %H:%M")}
- **MDE anterior:** `{Path(arquivo_anterior).name}`
- **MDE posterior:** `{Path(arquivo_posterior).name}`

## Objetivo
Comparar dois modelos digitais de elevação (MDEs) espacialmente alinhados para identificar diferenças na superfície representada.

## Método
O segundo raster foi alinhado à grade do primeiro. Em cada pixel válido foi calculada a diferença:

`D = MDE posterior - MDE anterior`

Valores negativos indicam uma superfície representada mais baixa no segundo modelo; valores positivos indicam uma superfície representada mais alta.

## Resultados numéricos
| Indicador | Resultado |
|---|---:|
| Pixels válidos | {stats['pixels_validos']} |
| Diferença média | {stats['diferenca_media_m']:.3f} m |
| Mediana | {stats['diferenca_mediana_m']:.3f} m |
| Mínima | {stats['diferenca_minima_m']:.3f} m |
| Máxima | {stats['diferenca_maxima_m']:.3f} m |
| Desvio padrão | {stats['desvio_padrao_m']:.3f} m |
| Percentil 5 | {stats['percentil_05_m']:.3f} m |
| Percentil 95 | {stats['percentil_95_m']:.3f} m |

## Metadados espaciais
- **CRS:** {stats['crs']}
- **Dimensões:** {stats['dimensoes']}
- **Resolução indicada pelo raster:** {stats['resolucao_raster']}
- **Limites:** {stats['limites_raster']}

## Produtos gerados
- `mapa_diferencas.png`
- `histograma_diferencas.png`
- `diferenca_topografica.tif`
- `estatisticas.csv`

## Discussão e limitações
As diferenças calculadas não podem ser atribuídas automaticamente à atividade mineradora. Elas também podem decorrer de diferenças entre sensores, datas de aquisição, resolução, alinhamento, vegetação, edificações, água, ruído e erros verticais dos modelos.

O Copernicus DEM GLO-30 é um modelo digital de superfície, que inclui vegetação e estruturas, e foi produzido a partir de dados adquiridos principalmente entre 2011 e 2015. Ele não constitui, sozinho, uma série temporal. Para sustentar uma conclusão sobre alteração topográfica ao longo do tempo, é necessário documentar dois modelos independentes, com datas de aquisição distintas e qualidade compatível.

Os resultados deste processamento são exploratórios. Não representam, por si só, medição validada de volume extraído ou prova de impacto ambiental.

## Conclusão
A ferramenta demonstrou um fluxo computacional reproduzível para comparar dois MDEs e visualizar diferenças de elevação. A interpretação geográfica depende da qualidade, temporalidade e proveniência dos dados de entrada. A próxima etapa é validar os dados utilizados e delimitar precisamente a área de estudo.

## Fontes de dados
Preencher antes da entrega:
- Provedor e produto do MDE anterior:
- Data de aquisição do MDE anterior:
- Provedor e produto do MDE posterior:
- Data de aquisição do MDE posterior:
- Datas de download:
- Licença/atribuição exigida:
"""
    path = Path(pasta_saida) / "relatorio_minevision.md"
    path.write_text(texto, encoding="utf-8")
    return str(path)
