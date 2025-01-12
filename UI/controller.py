import flet as ft
from UI.view import View
from model.model import Model


class Controller:

    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        # read user input
        if self._view.dd_localization.value is None:
            self._view.create_alert("Selezionare un tipo di localizzazione")
            return
        else:
            localization = self._view.dd_localization.value

        # crea grafo e stampa info del grafo
        self._model.build_graph(localization)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Creato grafo con {self._model.num_nodes()} nodi"
                                                       f" e {self._model.num_edges()} archi\n"))

        sorted_edges = self._model.edges()
        for edge in sorted_edges:
            self._view.txt_result.controls.append(ft.Text(f"{edge[0].GeneID} <-> {edge[1].GeneID}: peso {edge[2]["weight"]}"))

        # sorted_nodes = self._model.get_node_max_uscenti()
        # n_nodi = min(len(sorted_nodes), 5)
        # self._view.txt_result1.controls.append(ft.Text(f"\nI {n_nodi} nodi col maggior numero di archi uscenti sono:"))
        # for i in range(n_nodi):
        #     self._view.txt_result1.controls.append(ft.Text(f"{sorted_nodes[i][0]} | "
        #                                                    f"num. archi uscenti: {sorted_nodes[i][1]}  | "
        #                                                    f"peso tot.: {sorted_nodes[i][2]}"))

        # self._view.btn_dettagli.disabled = False
        # self._view.btn_path.disabled = False
        self._view.update_page()

    def analyze_graph(selfself, e):
        pass

    def handle_path(self, e):
        pass

    def fill_dd_localization(self):
        values = self._model.get_distinct_localizations()
        self._view.dd_localization.options = list(map(lambda x: ft.dropdown.Option(key=x, text=x), values))
