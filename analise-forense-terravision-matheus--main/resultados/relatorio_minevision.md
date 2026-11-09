# Relatório — MineVision

## Identificação
- **Área de estudo:** Serra dos Carajás, Pará
- **Data de processamento:** 09/11/2026 10:03
- **MDE anterior:** `anterior.tif`
- **MDE posterior:** `posterior_crs.tif`

## Objetivo
Comparar dois modelos digitais de elevação (MDEs) espacialmente alinhados para identificar diferenças na superfície representada.

## Método
O segundo raster foi alinhado à grade do primeiro. Em cada pixel válido foi calculada a diferença:

`D = MDE posterior - MDE anterior`

Valores negativos indicam uma superfície representada mais baixa no segundo modelo; valores positivos indicam uma superfície representada mais alta.

## Resultados numéricos
| Indicador | Resultado |
|---|---:|
| Pixels válidos | 9 |
| Diferença média | 0.000 m |
| Mediana | 0.000 m |
| Mínima | 0.000 m |
| Máxima | 0.000 m |
| Desvio padrão | 0.000 m |
| Percentil 5 | 0.000 m |
| Percentil 95 | 0.000 m |

## Metadados espaciais
- **CRS:** EPSG:4326
- **Dimensões:** 3 x 3
- **Resolução indicada pelo raster:** (0.001, 0.001)
- **Limites:** BoundingBox(left=-50.0, bottom=-5.003, right=-49.997, top=-5.0)

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
