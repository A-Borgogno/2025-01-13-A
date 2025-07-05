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
        self._view.btn_analizza_grafo.disabled = False
        self._view.btn_path.disabled = False
        self._view.update_page()

    def analyze_graph(selfself, e):
        pass

    def handle_path(self, e):
        pass

