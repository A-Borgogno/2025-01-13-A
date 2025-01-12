import copy
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._chromosomes_map = {}
        self.get_all_chromosomes_interaction()

    def get_all_chromosomes_interaction(self):
        for interaction in DAO.get_all_interactions():
            DAO.get_all_chromosomes_interaction(interaction, self._chromosomes_map)

    def get_distinct_localizations(self):
        return DAO.get_distinct_localizations()

    def build_graph(self, localization):
        self._graph.clear()
        nodes = DAO.get_nodes(localization)
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

        # Calcolo degli edges da query
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
