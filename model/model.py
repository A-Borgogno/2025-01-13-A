import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestSol = []
        self._minConnesse = None

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
            if i.GeneID1 in self._idMap.keys() and i.GeneID2 in self._idMap.keys() and i.GeneID1 != i.GeneID2:
                if not self._graph.has_edge(self._idMap[i.GeneID2], self._idMap[i.GeneID1]):
                    cromosomi = DAO.getPesoArco(i.GeneID1, i.GeneID2)
                    if cromosomi[0][0] != cromosomi[0][1]:
                        self._graph.add_edge(self._idMap[i.GeneID1], self._idMap[i.GeneID2], weight=cromosomi[0][0]+cromosomi[0][1])
                    else:
                        self._graph.add_edge(self._idMap[i.GeneID1], self._idMap[i.GeneID2], weight=cromosomi[0][0])

        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getBestEdges(self):
        return list(sorted(list(self._graph.edges(data=True)), key=lambda e:e[2]["weight"]))

    def getComponentiConnesse(self):
        return sorted(list(nx.connected_components(self._graph)), key=lambda c:len(c), reverse=True)

    def getPath(self):
        self._bestSol = []
        self._minConnesse = None

        for node in self._graph.nodes:
            if node.Essential != "":
                self._ricorsione([node], node)

        return self._bestSol, self._minConnesse

    def _ricorsione(self, parziale, source):
        if len(parziale) > len(self._bestSol):
            self._bestSol = copy.deepcopy(parziale)
            self._minConnesse = nx.number_connected_components(nx.subgraph(self._graph, parziale))
        # elif len(parziale) == len(self._bestSol):
        #     if len(list(nx.connected_components(nx.subgraph(self._graph, parziale)))) < self._minConnesse:
        #         self._bestSol = copy.deepcopy(parziale)
        #         self._minConnesse = len(list(nx.connected_components(nx.subgraph(self._graph, parziale))))
        for n in self._graph.neighbors(source):
            if n not in parziale:
                if n.GeneID > source.GeneID and n.Essential == source.Essential:
                    parziale.append(n)
                    self._ricorsione(parziale, n)
                    parziale.pop()
