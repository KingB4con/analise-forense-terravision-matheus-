import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget
)
from PySide6.QtCore import Qt


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

        paginas = [
            ("⌂", "Dashboard"),
            ("▦", "Áreas de estudo"),
            ("◎", "Visualizador"),
            ("⌁", "Análises"),
            ("▤", "Relatórios"),
        ]

        self.conteudo = QStackedWidget()

        for indice, (icone, nome) in enumerate(paginas):
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

        self.conteudo.addWidget(self.criar_dashboard())

        nomes = [
            "Áreas de estudo",
            "Visualizador geográfico",
            "Análises",
            "Relatórios",
        ]

        for nome in nomes:
            self.conteudo.addWidget(self.criar_pagina_vazia(nome))

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

    def mudar_pagina(self, indice):
        self.conteudo.setCurrentIndex(indice)

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