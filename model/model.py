import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

    def getLocalizations(self):
        return DAO.getLocalizations()

    def buildGraph(self, localization):
        self._graph.clear()
        self._idMap = {}

        nodes = DAO.getNodes(localization)
        for node in nodes:
            self._idMap[node.GeneID] =  node
        self._graph.add_nodes_from(nodes)

        allInteractions = DAO.get_all_interactions()
        for i in allInteractions:
            if i.GeneID1 in self._idMap.keys() and i.GeneID2 in self._idMap.keys():
                peso = DAO.getPesoArco(i.GeneID1, i.GeneID2)
                self._graph.add_edge(self._idMap[i.GeneID1], self._idMap[i.GeneID2], weight=peso)

        return self._graph.number_of_nodes(), self._graph.number_of_edges()