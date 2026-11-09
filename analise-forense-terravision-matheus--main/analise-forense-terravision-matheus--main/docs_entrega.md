# Roteiro para apresentação/entrega

## Título
MineVision: ferramenta de análise exploratória de alterações topográficas na região da Serra dos Carajás (PA)

## Resumo
O MineVision é um protótipo em Python que compara dois Modelos Digitais de Elevação (MDEs) em formato GeoTIFF. O sistema alinha os rasters, calcula a diferença entre as elevações e gera mapas, histograma, estatísticas e relatório. O estudo de caso proposto é a Serra dos Carajás, no Pará. A análise depende da obtenção de dois modelos com datas de aquisição distintas e metadados documentados.

## Problema
Atividades de mineração a céu aberto podem modificar o relevo. A comparação de dados de elevação é uma forma de investigar diferenças na superfície ao longo do tempo.

## Objetivo geral
Desenvolver uma aplicação que auxilie na comparação exploratória de modelos de elevação para investigar possíveis alterações topográficas.

## Objetivos específicos
1. Organizar dados geoespaciais em formato GeoTIFF.
2. Alinhar dois modelos de elevação para uma comparação espacial.
3. Calcular a diferença de elevação por pixel.
4. Produzir visualizações e estatísticas.
5. Documentar limitações e a origem dos dados.

## Metodologia
1. Seleção e delimitação da área de estudo.
2. Obtenção de dois MDEs independentes e temporalmente distintos.
3. Verificação dos metadados, cobertura, resolução, CRS e datas.
4. Alinhamento dos rasters.
5. Cálculo: D = MDE posterior − MDE anterior.
6. Geração de mapa, histograma e estatísticas.
7. Interpretação cautelosa dos resultados.

## Tecnologias
Python, Tkinter, Rasterio, NumPy e Matplotlib.

## O que ainda deve ser preenchido antes da entrega
- Nome do aluno, turma, disciplina e professor.
- Coordenadas/polígono da área efetivamente analisada.
- Identificação e datas dos dois dados de elevação.
- Captura de tela da aplicação em execução.
- Mapa e estatísticas gerados com dados reais.
- Conclusão baseada nos resultados reais, sem inventar números.

## Referência técnica principal
Copernicus Data Space Ecosystem — Copernicus DEM:
https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM

Documentação técnica de DEM:
https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/DEM.html
