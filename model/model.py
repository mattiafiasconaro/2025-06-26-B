import networkx as nx
from networkx.classes import nodes

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._circuito=[]
        self._idMap={}

    def getAllYears(self):
        return DAO.getAllYears()


    def buildGraph(self,annoMax,annoMin):
        self._graph.clear()
        self._circuito=DAO.getAllNodes()
        for i in self._circuito:
            self._idMap[i.circuitId]=i

        self._graph.add_nodes_from(self._circuito)

        allEdges=DAO.getAllEges(annoMax,annoMin,self._idMap)
        for e in allEdges:
            self._graph.add_edge(e.circuito1,e.circuito2,weight=e.peso)


    def getGraphDetails(self):
        return len(self._graph.nodes),len(self._graph.edges)

    def getConnectedComponents(self):
        components = list(nx.connected_components(self._graph))
        num_components = len(components)
        largest_component = max(components, key=len)
        pesi_minimi = {}
        for nodo in largest_component:
            archi_incidenti = self._graph.edges(nodo, data='weight')
            pesi = [peso for _, _, peso in archi_incidenti]
            pesi_minimi[nodo] = min(pesi) if pesi else 0

        # ordina i nodi in senso decrescente di peso minimo
        nodi_ordinati = sorted(largest_component,
                               key=lambda n: pesi_minimi[n],
                               reverse=True)

        return num_components, nodi_ordinati, len(largest_component)
