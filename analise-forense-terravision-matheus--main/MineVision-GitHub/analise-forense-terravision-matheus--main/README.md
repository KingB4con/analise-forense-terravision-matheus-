# MineVision — análise exploratória de alterações topográficas

Projeto acadêmico para comparar dois Modelos Digitais de Elevação (MDE/DEM) de uma mesma área e produzir:
- raster GeoTIFF de diferença (`posterior - anterior`);
- mapa PNG da diferença;
- histograma das diferenças;
- estatísticas em CSV;
- relatório em Markdown com limitações e metadados.

**Estudo de caso:** Serra dos Carajás, Pará, Brasil.

## Importante: o que este projeto mede
O programa calcula diferenças entre dois rasters de elevação. Ele não identifica sozinho a causa da diferença e não prova que toda variação seja mineração. Diferenças podem resultar de datas, sensores, resolução, georreferenciamento, vegetação, construções, água, erros verticais e processamento.

O Copernicus DEM GLO-30 é um **modelo digital de superfície (MDS/DSM)**, que inclui vegetação e estruturas, e seus dados foram adquiridos principalmente entre 2011 e 2015. Portanto, não use duas cópias/versões do mesmo produto como se fossem épocas distintas. Para um estudo temporal, obtenha dois produtos com datas de aquisição realmente diferentes e documentadas. Se só houver um MDE confiável, apresente o trabalho como análise do relevo atual, não como mudança temporal comprovada.

## Requisitos
- Python 3.10 ou superior
- Windows, Linux ou macOS
- Dependências: `rasterio`, `numpy`, `matplotlib`

## Instalação (Windows / CMD)
Abra o CMD na pasta do projeto:

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Executar
```bat
python main.py
```

A interface permite selecionar:
1. MDE anterior (GeoTIFF `.tif` ou `.tiff`);
2. MDE posterior (GeoTIFF `.tif` ou `.tiff`);
3. pasta de saída.

Clique em **Analisar**. Os resultados serão salvos na pasta escolhida.

## Dados de elevação
Fontes para procurar dados e registrar a proveniência:
- Copernicus DEM: https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM
- Documentação de DEM: https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/DEM.html
- OpenTopography: https://opentopography.org/

O Copernicus DEM GLO-30 tem resolução nominal de 30 m e cobertura global, mas a disponibilidade/acesso e os termos devem ser conferidos no portal. Registre no trabalho o nome do produto, data de aquisição, resolução, sistema de coordenadas, fonte e data de download.

## Como interpretar
O raster de diferença é calculado como:

`diferença = MDE_posterior - MDE_anterior`

- valor negativo: superfície representada mais baixa no segundo modelo;
- valor positivo: superfície representada mais alta no segundo modelo;
- valor próximo de zero: diferença pequena em relação aos dois modelos.

**Não confunda diferença de superfície com volume de minério extraído.** Para estimar volume seriam necessários dados adequados, delimitação da área, alinhamento, resolução e avaliação de incerteza. O projeto não calcula volume.

## Estrutura
```text
MineVision/
├── main.py
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── analise.py
│   ├── relatorio.py
│   └── interface.py
├── dados/
│   ├── entrada/
│   └── processados/
├── resultados/
└── tests/
    └── test_analise.py
```

## Limitações conhecidas
- A comparação exige rasters com cobertura espacial sobreposta.
- O segundo raster é reprojetado/alinhado à grade do primeiro antes da subtração.
- O alinhamento não elimina diferenças de qualidade ou de data.
- A análise é exploratória e não substitui validação de campo ou avaliação geodésica.
- A área de estudo ainda precisa ser delimitada com coordenadas ou polígono.
- Nenhum resultado real da Serra dos Carajás é incluído neste pacote sem dados de entrada verificados.

## Citação dos dados
Siga a licença e a forma de atribuição indicadas pelo provedor do conjunto utilizado. Para Copernicus DEM, consulte a página oficial do produto e registre a referência/DOI quando aplicável.
