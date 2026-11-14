import sys

from pathlib import Path

from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QGraphicsView,
    QGraphicsScene
)

from PySide6.QtGui import (
    QImage,
    QPixmap,
    QPainter
)

import numpy as np

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget
)
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QLineEdit,
    QPlainTextEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox
)

from PySide6.QtWidgets import QFileDialog
from src.raster import ler_metadados

from src.raster import carregar_imagem_raster
from script import obter_configuracao_lod

from areas import (
    listar_areas,
    cadastrar_area,
    excluir_area,
    listar_rasters,
    registrar_raster
)


class VisualizadorRaster(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.cena = QGraphicsScene(self)
        self.setScene(self.cena)

        self.item_imagem = None
        self.nivel_zoom = 0

        self.setRenderHint(
            QPainter.RenderHint.SmoothPixmapTransform
        )

        self.setDragMode(
            QGraphicsView.DragMode.ScrollHandDrag
        )

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorViewCenter
        )

        self.setBackgroundBrush(Qt.GlobalColor.darkGray)

    def exibir_imagem(self, imagem):
        self.cena.clear()
        self.nivel_zoom = 0

        pixmap = QPixmap.fromImage(imagem)

        self.item_imagem = self.cena.addPixmap(pixmap)

        self.cena.setSceneRect(
            self.item_imagem.boundingRect()
        )

        self.ajustar_imagem()

    def ajustar_imagem(self):
        if self.item_imagem is None:
            return

        self.nivel_zoom = 0

        self.fitInView(
            self.item_imagem,
            Qt.AspectRatioMode.KeepAspectRatio
        )

    def wheelEvent(self, evento):
        if self.item_imagem is None:
            return

        fator = 1.25

        if evento.angleDelta().y() > 0:
            if self.nivel_zoom >= 12:
                return

            self.scale(fator, fator)
            self.nivel_zoom += 1

        else:
            if self.nivel_zoom <= -5:
                return

            self.scale(1 / fator, 1 / fator)
            self.nivel_zoom -= 1

    def resizeEvent(self, evento):
        super().resizeEvent(evento)

        if self.item_imagem is not None and self.nivel_zoom == 0:
            self.ajustar_imagem()


class MineVisionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MineVision | Plataforma Geoespacial")
        self.resize(1150, 720)
        self.setMinimumSize(900, 600)

        self.tema_escuro = True
        self.botoes_menu = []

        self.criar_interface()
        self.aplicar_tema()

    def criar_interface(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QHBoxLayout(central)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # MENU LATERAL
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(230)

        menu_layout = QVBoxLayout(self.sidebar)
        menu_layout.setContentsMargins(18, 25, 18, 20)
        menu_layout.setSpacing(10)

        logo = QLabel("MINEVISION")
        logo.setObjectName("logo")
        menu_layout.addWidget(logo)

        subtitulo = QLabel("PLATAFORMA GEOESPACIAL")
        subtitulo.setObjectName("subtitulo")
        menu_layout.addWidget(subtitulo)

        menu_layout.addSpacing(30)

        pagina = [
            ("⌂", "Dashboard"),
            ("▦", "Áreas de estudo"),
            ("◎", "Visualizador"),
            ("⌁", "Análises"),
            ("▤", "Relatórios"),
        ]

        self.conteudo = QStackedWidget()

        for indice, (icone, nome) in enumerate(pagina):
            botao = QPushButton(f"{icone}    {nome}")
            botao.setObjectName("menu_button")
            botao.setCursor(Qt.CursorShape.PointingHandCursor)
            botao.clicked.connect(
                lambda checked=False, i=indice: self.mudar_pagina(i)
            )

            menu_layout.addWidget(botao)
            self.botoes_menu.append(botao)

        menu_layout.addStretch()

        self.botao_tema = QPushButton("☀  Alternar tema")
        self.botao_tema.setObjectName("theme_button")
        self.botao_tema.setCursor(Qt.CursorShape.PointingHandCursor)
        self.botao_tema.clicked.connect(self.alternar_tema)
        menu_layout.addWidget(self.botao_tema)

        versao = QLabel("MineVision • MVP 1.0")
        versao.setObjectName("versao")
        menu_layout.addWidget(versao)

        layout_principal.addWidget(self.sidebar)

        # ÁREA PRINCIPAL
        self.area_principal = QFrame()
        area_layout = QVBoxLayout(self.area_principal)
        area_layout.setContentsMargins(32, 28, 32, 28)

        nomes = [
            "Áreas de estudo",
            "Visualizador geográfico",
            "Análises",
            "Relatórios",
        ]

        self.conteudo = QStackedWidget()

        self.conteudo.addWidget(self.criar_dashboard())
        self.conteudo.addWidget(self.criar_pagina_areas())

        self.conteudo.addWidget(
            self.criar_pagina_visualizador()
        )

        for nome in nomes[2:]: 
            self.conteudo.addWidget(
                self.criar_pagina_vazia(nome)
            )

        area_layout.addWidget(self.conteudo)
        layout_principal.addWidget(self.area_principal)

        self.mudar_pagina(0)

    def criar_dashboard(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        titulo = QLabel("Dashboard")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        descricao = QLabel(
            "Visão geral do monitoramento e das análises geoespaciais."
        )
        descricao.setObjectName("descricao")
        layout.addWidget(descricao)

        # INDICADORES
        indicadores = QHBoxLayout()
        indicadores.setSpacing(15)

        dados = [
            ("ÁREAS MONITORADAS", "0", "Nenhuma área cadastrada"),
            ("ANÁLISES REALIZADAS", "0", "Nenhuma análise registrada"),
            ("PROJETOS ATIVOS", "0", "Nenhum projeto cadastrado"),
        ]

        for titulo_card, valor, detalhe in dados:
            card = QFrame()
            card.setObjectName("card")

            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 18, 20, 18)
            card_layout.setSpacing(9)

            label = QLabel(titulo_card)
            label.setObjectName("card_label")

            numero = QLabel(valor)
            numero.setObjectName("card_number")

            info = QLabel(detalhe)
            info.setObjectName("card_info")

            card_layout.addWidget(label)
            card_layout.addWidget(numero)
            card_layout.addWidget(info)

            indicadores.addWidget(card)

        layout.addLayout(indicadores)

        # PAINEL INFERIOR
        painel = QFrame()
        painel.setObjectName("panel")

        painel_layout = QVBoxLayout(painel)
        painel_layout.setContentsMargins(22, 20, 22, 20)
        painel_layout.setSpacing(12)

        painel_titulo = QLabel("Atividade recente")
        painel_titulo.setObjectName("panel_title")

        painel_texto = QLabel(
            "Ainda não existem atividades registradas.\n\n"
            "Quando você cadastrar áreas e executar análises, "
            "o histórico aparecerá aqui."
        )
        painel_texto.setObjectName("descricao")
        painel_texto.setWordWrap(True)

        painel_layout.addWidget(painel_titulo)
        painel_layout.addWidget(painel_texto)
        painel_layout.addStretch()

        layout.addWidget(painel, 1)

        aviso = QLabel(
            "MineVision é uma ferramenta de análise exploratória. "
            "Diferenças entre modelos de elevação não comprovam, "
            "isoladamente, atividade de mineração."
        )
        aviso.setObjectName("aviso")
        aviso.setWordWrap(True)
        layout.addWidget(aviso)

        return pagina

    
    def criar_pagina_areas(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)

        titulo = QLabel("Áreas de estudo")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        descricao = QLabel("Cadastre e gerencie suas áreas monitoradas.")
        descricao.setObjectName("descricao")
        layout.addWidget(descricao)

        self.campo_nome = QLineEdit()
        self.campo_nome.setPlaceholderText("Nome da área")

        self.campo_localizacao = QLineEdit()
        self.campo_localizacao.setPlaceholderText("Ex: Serra dos Carajás, Pará")

        self.campo_descricao = QPlainTextEdit()
        self.campo_descricao.setPlaceholderText("Descrição da área (opcional)")
        self.campo_descricao.setMaximumHeight(90)

        layout.addWidget(QLabel("Nome"))
        layout.addWidget(self.campo_nome)

        layout.addWidget(QLabel("Localização"))
        layout.addWidget(self.campo_localizacao)

        layout.addWidget(QLabel("Descrição"))
        layout.addWidget(self.campo_descricao)

        botao_cadastrar = QPushButton("Cadastrar área")
        botao_cadastrar.clicked.connect(self.salvar_area)
        layout.addWidget(botao_cadastrar)

        layout.addWidget(QLabel("Áreas cadastradas"))

        self.lista_areas = QListWidget()
        self.lista_areas.currentItemChanged.connect(
            self.atualizar_lista_rasters
        )
        layout.addWidget(self.lista_areas)

        botao_excluir = QPushButton("Excluir área selecionada")
        botao_excluir.clicked.connect(self.remover_area)
        layout.addWidget(botao_excluir)

        layout.addWidget(QLabel("Arquivos GeoTIFF da área selecionada"))

        self.lista_rasters = QListWidget()
        layout.addWidget(self.lista_rasters)

        botao_importar = QPushButton("Importar GeoTIFF")
        botao_importar.clicked.connect(self.importar_raster)
        layout.addWidget(botao_importar)

        self.atualizar_lista_areas()

        return pagina



    def atualizar_lista_areas(self):
        self.lista_areas.clear()

        for area in listar_areas():
            item = QListWidgetItem(
                f"{area['nome']} — {area['localizacao']}"
            )

            item.setData(Qt.ItemDataRole.UserRole, area["id"])
            self.lista_areas.addItem(item)

    
    def atualizar_lista_rasters(self, *args):
        self.lista_rasters.clear()

        item = self.lista_areas.currentItem()

        if item is None:
            return

        area_id = item.data(Qt.ItemDataRole.UserRole)

        for raster in listar_rasters(area_id):
            texto = (
                f"{raster['nome']} — "
                f"{raster['largura']}x{raster['altura']} pixels"
            )

            self.lista_rasters.addItem(texto)


    def importar_raster(self):
        item = self.lista_areas.currentItem()

        if item is None:
            QMessageBox.warning(
                self,
                "MineVision",
                "Selecione uma área antes de importar arquivos."
            )
            return

        area_id = item.data(Qt.ItemDataRole.UserRole)

        arquivos, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar arquivos GeoTIFF",
            "",
            "GeoTIFF (*.tif *.tiff)"
        )

        if not arquivos:
            return

        importados = 0
        erros = []

        for caminho in arquivos:
            try:
                metadados = ler_metadados(caminho)
                registrar_raster(area_id, metadados)
                importados += 1

            except Exception as erro:
                erros.append(f"{Path(caminho).name}: {erro}")

        self.atualizar_lista_rasters()

        mensagem = f"{importados} arquivo(s) importado(s) com sucesso."

        if erros:
            mensagem += "\n\nProblemas encontrados:\n" + "\n".join(erros)

        QMessageBox.information(self, "Importação GeoTIFF", mensagem)

    def salvar_area(self):
        try:
            cadastrar_area(
                self.campo_nome.text(),
                self.campo_localizacao.text(),
                self.campo_descricao.toPlainText()
            )

            self.campo_nome.clear()
            self.campo_localizacao.clear()
            self.campo_descricao.clear()

            self.atualizar_lista_areas()

            QMessageBox.information(
                self, "MineVision", "Área cadastrada com sucesso!"
            )

        except (ValueError, OSError) as erro:
            QMessageBox.warning(self, "Erro", str(erro))


    def remover_area(self):
        item = self.lista_areas.currentItem()

        if item is None:
            QMessageBox.warning(
                self, "MineVision", "Selecione uma área primeiro."
            )
            return

        area_id = item.data(Qt.ItemDataRole.UserRole)

        resposta = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Deseja realmente excluir esta área?"
        )

        if resposta == QMessageBox.StandardButton.Yes:
            excluir_area(area_id)
            self.atualizar_lista_areas()

    def criar_pagina_vazia(self, nome):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        titulo = QLabel(nome)
        titulo.setObjectName("titulo")

        descricao = QLabel(
            "Este módulo será desenvolvido nas próximas etapas."
        )
        descricao.setObjectName("descricao")

        painel = QFrame()
        painel.setObjectName("panel")

        painel_layout = QVBoxLayout(painel)
        painel_layout.setContentsMargins(25, 25, 25, 25)

        mensagem = QLabel("Módulo em desenvolvimento")
        mensagem.setObjectName("panel_title")

        painel_layout.addWidget(mensagem)

        layout.addWidget(titulo)
        layout.addWidget(descricao)
        layout.addSpacing(20)
        layout.addWidget(painel)

        return pagina

    def criar_pagina_visualizador(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)

        titulo = QLabel("Visualizador geográfico")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        descricao = QLabel(
            "Explore imagens georreferenciadas e dados de mineração."
        )
        descricao.setObjectName("descricao")
        layout.addWidget(descricao)

        controles = QHBoxLayout()

        self.combo_area_visualizador = QComboBox()
        self.combo_area_visualizador.addItem("Selecione uma área")

        self.combo_raster_visualizador = QComboBox()
        self.combo_raster_visualizador.addItem("Selecione um GeoTIFF")

        self.altitude_visualizador = QDoubleSpinBox()
        self.altitude_visualizador.setRange(0, 1000000)
        self.altitude_visualizador.setDecimals(0)
        self.altitude_visualizador.setValue(5000)
        self.altitude_visualizador.setSuffix(" m")

        botao_exibir = QPushButton("Carregar imagem")
        botao_exibir.clicked.connect(
            self.exibir_raster_visualizador
        )

        botao_ajustar = QPushButton("Ajustar à tela")
        botao_ajustar.clicked.connect(
            lambda: self.visualizador.ajustar_imagem()
        )

        controles.addWidget(self.combo_area_visualizador)
        controles.addWidget(self.combo_raster_visualizador)
        controles.addWidget(self.altitude_visualizador)
        controles.addWidget(botao_exibir)
        controles.addWidget(botao_ajustar)

        layout.addLayout(controles)

        self.combo_area_visualizador.currentIndexChanged.connect(
            self.atualizar_rasters_visualizador
        )

        self.visualizador = VisualizadorRaster()

        layout.addWidget(self.visualizador, 1)

        self.info_lod = QLabel(
            "Selecione uma área e um GeoTIFF para começar."
        )
        self.info_lod.setObjectName("descricao")
        layout.addWidget(self.info_lod)

        self.atualizar_areas_visualizador()

        return pagina

    def atualizar_areas_visualizador(self): 
        self.combo_area_visualizador.clear()
        self.combo_area_visualizador.addItem("Selecione uma área")

        for area in listar_areas(): 
            self.combo_area_visualizador.addItem(
                area["nome"],
                area["id"]
            )

        self.atualizar_rasters_visualizador()

    def atualizar_rasters_visualizador(self, indice=None): 
        self.combo_raster_visualizador.clear()
        self.combo_raster_visualizador.addItem("Selecione um GeoTIFF")

        area_id = self.combo_area_visualizador.currentData()

        if not area_id: 
            return

        for raster in listar_rasters(area_id):
            self.combo_raster_visualizador.addItem(
                raster["nome"],
                raster["caminho"]
            )

    def exibir_raster_visualizador(self):
        caminho = self.combo_raster_visualizador.currentData()

        if not caminho:
            QMessageBox.warning(
                self,
                "MineVision",
                "Selecione um GeoTIFF para visualizar."
            )
            return

        try:
            altitude = self.altitude_visualizador.value()

            configuracao = obter_configuracao_lod(altitude)

            imagem, extent, tipo, informacoes = carregar_imagem_raster(
                caminho,
                configuracao["max_dimensao"]
            )

            if tipo == "rgb":
                dados = np.clip(
                    imagem * 255,
                    0,
                    255
                ).astype(np.uint8)

                dados = np.ascontiguousarray(dados)

                altura, largura, canais = dados.shape

                imagem_qt = QImage(
                    dados.data,
                    largura,
                    altura,
                    dados.strides[0],
                    QImage.Format.Format_RGB888
                ).copy()

            else:
                valores = imagem.compressed()

                if valores.size == 0:
                    raise ValueError(
                        "O raster não possui pixels válidos."
                    )

                minimo, maximo = np.percentile(
                    valores,
                    [2, 98]
                )

                if maximo <= minimo:
                    maximo = minimo + 1

                normalizada = np.clip(
                    (imagem.filled(minimo) - minimo)
                    / (maximo - minimo),
                    0,
                    1
                )

                dados = (
                    normalizada * 255
                ).astype(np.uint8)

                dados = np.ascontiguousarray(dados)

                altura, largura = dados.shape

                imagem_qt = QImage(
                    dados.data,
                    largura,
                    altura,
                    dados.strides[0],
                    QImage.Format.Format_Grayscale8
                ).copy()

            self.visualizador.exibir_imagem(imagem_qt)

            self.info_lod.setText(
                f"LoD: {configuracao['nivel']} | "
                f"Altitude: {altitude:.0f} m | "
                f"Imagem: {largura} x {altura} pixels | "
                f"CRS: {informacoes['crs']}"
            )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro na visualização",
                str(erro)
            )


    def mudar_pagina(self, indice):
        self.conteudo.setCurrentIndex(indice)

        if indice == 2:
            self.atualizar_areas_visualizador()

        for i, botao in enumerate(self.botoes_menu):
            botao.setProperty("active", i == indice)
            botao.style().unpolish(botao)
            botao.style().polish(botao)

    def alternar_tema(self):
        self.tema_escuro = not self.tema_escuro
        self.aplicar_tema()

    def aplicar_tema(self):
        if self.tema_escuro:
            fundo = "#111827"
            sidebar = "#0B1220"
            card = "#1F2937"
            texto = "#F9FAFB"
            secundario = "#9CA3AF"
            borda = "#374151"
            destaque = "#2563EB"
            botao_tema = "☀  Tema claro"
        else:
            fundo = "#F3F4F6"
            sidebar = "#FFFFFF"
            card = "#FFFFFF"
            texto = "#111827"
            secundario = "#6B7280"
            borda = "#E5E7EB"
            destaque = "#2563EB"
            botao_tema = "☾  Tema escuro"

        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {fundo};
                color: {texto};
                font-family: 'Segoe UI';
                font-size: 10pt;
            }}

            QFrame#sidebar {{
                background-color: {sidebar};
                border-right: 1px solid {borda};
            }}

            QLabel#logo {{
                font-size: 21pt;
                font-weight: bold;
                color: {destaque};
            }}

            QLabel#subtitulo, QLabel#versao {{
                color: {secundario};
                font-size: 8pt;
            }}

            QPushButton#menu_button {{
                text-align: left;
                padding: 12px;
                border: none;
                border-radius: 7px;
                color: {secundario};
                background: transparent;
            }}

            QPushButton#menu_button:hover {{
                background-color: {card};
                color: {texto};
            }}

            QPushButton#menu_button[active="true"] {{
                background-color: {destaque};
                color: white;
                font-weight: bold;
            }}

            QPushButton#theme_button {{
                padding: 11px;
                border: 1px solid {borda};
                border-radius: 7px;
                color: {texto};
                background-color: {card};
            }}

            QLabel#titulo {{
                font-size: 25pt;
                font-weight: bold;
            }}

            QLabel#descricao, QLabel#card_info {{
                color: {secundario};
            }}

            QFrame#card, QFrame#panel {{
                background-color: {card};
                border: 1px solid {borda};
                border-radius: 10px;
            }}

            QLabel#card_label {{
                color: {secundario};
                font-size: 8pt;
                font-weight: bold;
            }}

            QLabel#card_number {{
                font-size: 27pt;
                font-weight: bold;
            }}

            QLabel#panel_title {{
                font-size: 14pt;
                font-weight: bold;
            }}

            QLabel#aviso {{
                color: {secundario};
                font-size: 9pt;
            }}
        """)

        self.sidebar.setObjectName("sidebar")
        self.botao_tema.setText(botao_tema)

def iniciar_interface():
    app = QApplication(sys.argv)
    janela = MineVisionApp()
    janela.show()
    sys.exit(app.exec())