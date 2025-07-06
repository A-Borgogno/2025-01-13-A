import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDD(self):
        localizations = self._model.getLocalizations()
        for l in localizations:
            self._view.dd_localization.options.append(ft.dropdown.Option(l))
        self._view.update_page()


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        localization = self._view.dd_localization.value
        if not localization:
            self._view.txt_result.controls.append(ft.Text("Selezionare la localizzazione", color="red"))
            self._view.update_page()
            return
        nodes, edges = self._model.buildGraph(localization)
        self._view.txt_result.controls.append(ft.Text(f"Creato grafo con {nodes} nodi e {edges} archi"))
        bestEdges = self._model.getBestEdges()
        for e in bestEdges:
            self._view.txt_result.controls.append(ft.Text(f"{e[0].GeneID} <-> {e[1].GeneID}: peso {e[2]["weight"]}"))
        self._view.btn_analizza_grafo.disabled = False
        self._view.btn_path.disabled = False
        self._view.update_page()

    def analyze_graph(self, e):
        self._view.txt_result.controls.append(ft.Text(""))
        self._view.txt_result.controls.append(ft.Text("Le componenti connesse sono:"))
        componenti_connesse = self._model.getComponentiConnesse()
        for c in componenti_connesse:
            if len(c) > 1:
                nodi = ""
                for n in list(c):
                    nodi += f"{n.GeneID}, "
                self._view.txt_result.controls.append(ft.Text(f"{nodi} | dimensione componente = {len(c)}"))
        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result.controls.clear()
        path, compConnesse = self._model.getPath()
        self._view.txt_result.controls.append(ft.Text(f"Trovato cammino con dimensione {len(path)}"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(f"{p}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero componenti connesse: {compConnesse} "))
        self._view.update_page()

