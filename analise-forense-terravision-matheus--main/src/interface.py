import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from .analise import analisar_mdes
from .relatorio import gerar_relatorio


class MineVisionApp:
    def __init__(self, root):
        self.root = root
        root.title("MineVision — Análise topográfica")
        root.geometry("760x520")
        root.minsize(680, 460)

        self.anterior = tk.StringVar()
        self.posterior = tk.StringVar()
        self.saida = tk.StringVar(value=str(Path.cwd() / "resultados"))
        self.area = tk.StringVar(value="Serra dos Carajás, Pará")

        frame = ttk.Frame(root, padding=18)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="MineVision", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Comparação exploratória de Modelos Digitais de Elevação").pack(anchor="w", pady=(0, 18))

        self._file_row(frame, "MDE anterior (.tif)", self.anterior)
        self._file_row(frame, "MDE posterior (.tif)", self.posterior)
        self._folder_row(frame, "Pasta de resultados", self.saida)

        ttk.Label(frame, text="Descrição da área de estudo").pack(anchor="w", pady=(12, 3))
        ttk.Entry(frame, textvariable=self.area).pack(fill="x")

        ttk.Button(frame, text="Analisar e gerar relatório", command=self.executar).pack(anchor="w", pady=18)
        self.status = tk.Text(frame, height=10, wrap="word", state="disabled")
        self.status.pack(fill="both", expand=True)

        ttk.Label(frame, text="Atenção: diferenças entre MDEs não provam, sozinhas, que houve mineração.",
                  foreground="#9a4b00", wraplength=700).pack(anchor="w", pady=(10, 0))

    def _file_row(self, parent, label, variable):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=5)
        ttk.Label(row, text=label, width=25).pack(side="left")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(row, text="Procurar", command=lambda: self._choose_file(variable)).pack(side="right")

    def _folder_row(self, parent, label, variable):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=5)
        ttk.Label(row, text=label, width=25).pack(side="left")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True, padx=6)
        ttk.Button(row, text="Procurar", command=lambda: self._choose_folder(variable)).pack(side="right")

    def _choose_file(self, variable):
        path = filedialog.askopenfilename(filetypes=[("GeoTIFF", "*.tif *.tiff"), ("Todos", "*.*")])
        if path:
            variable.set(path)

    def _choose_folder(self, variable):
        path = filedialog.askdirectory()
        if path:
            variable.set(path)

    def _log(self, message):
        self.status.configure(state="normal")
        self.status.insert("end", message + "\n")
        self.status.see("end")
        self.status.configure(state="disabled")

    def executar(self):
        try:
            self._log("Iniciando processamento...")
            resultados = analisar_mdes(self.anterior.get(), self.posterior.get(), self.saida.get())
            relatorio = gerar_relatorio(resultados, self.anterior.get(), self.posterior.get(),
                                        self.saida.get(), self.area.get())
            self._log("Processamento concluído.")
            self._log(f"Mapa: {resultados['mapa']}")
            self._log(f"Histograma: {resultados['histograma']}")
            self._log(f"GeoTIFF: {resultados['raster']}")
            self._log(f"Relatório: {relatorio}")
            messagebox.showinfo("MineVision", "Análise concluída! Confira a pasta de resultados.")
        except Exception as exc:
            messagebox.showerror("Erro na análise", str(exc))
            self._log(f"ERRO: {exc}")


def iniciar_interface():
    root = tk.Tk()
    MineVisionApp(root)
    root.mainloop()
