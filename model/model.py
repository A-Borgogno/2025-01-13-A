import copy
import networkx as nx
from networkx import Graph

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._chromosomes_map = {}
        self.get_all_chromosomes_interaction()

    def get_list_nodes(self):
        self._bestListNodes = []
        self._bestScore = len(self._graph.nodes)
        self._bestLen = 0

        allNodes = list(self._graph.nodes)
        allNodes.sort(key=lambda x: x.GeneID)

        for root in allNodes:
            rimanenti = copy.deepcopy(allNodes)
            rimanenti.remove(root)
            rimanenti = [x for x in rimanenti if x.Essential == root.Essential]

            self._ricorsione([root], list(rimanenti))

        print(self._bestLen, self._bestScore)
        return self._bestListNodes, self._bestLen, self._bestScore

    def _ricorsione(self, parziale, rimanenti):
        if len (parziale) > self._bestLen:
            self._bestLen = len(parziale)
            self._bestScore = self._getScore(parziale)
            self._bestListNodes = copy.deepcopy(parziale)
            if len(parziale) == self._bestLen:
                if self._getScore(parziale) < self._bestScore:
                    self._bestScore = self._getScore(parziale)
                    self._bestListNodes = copy.deepcopy(parziale)


        if len(rimanenti) == 0:
            return

        for n in rimanenti:
            if n.GeneID > parziale[-1].GeneID:
                parziale.append(n)
                rimanenti.remove(n)
                self._ricorsione(parziale, rimanenti)
                parziale.remove(n)
                rimanenti.append(n)

    def _getScore(self, parziale):
        return nx.number_connected_components(self._graph.subgraph(parziale))

    def get_all_chromosomes_interaction(self):
        for interaction in DAO.get_all_interactions():
            DAO.get_all_chromosomes_interaction(interaction, self._chromosomes_map)

    def get_distinct_localizations(self):
        return DAO.get_distinct_localizations()

    def build_graph(self, localization):
        self._graph.clear()

        #Calcolo nodi
        nodes = DAO.get_nodes_w_essentiality(localization)
        self._graph.add_nodes_from(nodes)

        #Calcolo degli edges in modo programmatico
        for i in range(len(nodes)-1):
            nodei = nodes[i].GeneID
            for j in range(i+1, len(nodes)):
                nodej = nodes[j].GeneID
                key = (nodei, nodej)
                if self._chromosomes_map.get(key) is not None:
                    peso = self._chromosomes_map.get((nodei, nodej))
                    self._graph.add_edge(nodes[i], nodes[j], weight=peso)

        # Calcolo degli edges da query (commentare la parte sopra per usare questa versione)
        # edges = DAO.get_edges(localization)
        # self._graph.add_weighted_edges_from(edges)


    def num_nodes(self):
        return len(self._graph.nodes)

    def nodes(self):
        return self._graph.nodes

    def num_edges(self):
        return len(self._graph.edges)

    def edges(self):
        sorted_edges = sorted(self._graph.edges(data=True), key=lambda edge: edge[2]["weight"], reverse=False)
        return sorted_edges

    def get_connesse(self):
        return sorted(nx.connected_components(self._graph), key=lambda connessa: len(connessa), reverse=True)