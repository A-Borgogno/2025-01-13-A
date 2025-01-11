import copy
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def get_distinct_localizations(self):
        return DAO.get_distinct_localizations()
