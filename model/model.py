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
        #x.connected_components(self._graph) restituisce un generatore di insiemi di nodi
        #uno per ogni componente connessa del grafo e lo trasformiamo in una lista




        num_components = len(components) # calcoliamo la lunghezza della lista
        largest_component = max(components, key=len) # prendi la lista piu grande
        pesi_minimi = {} #creiamo un dict vuoto che conterra per ogni nodo della
        # componente piu grande il peso minimo dei suoi archi
        for nodo in largest_component: #esaminiamo un nodo alla volta (della componente + grande)
            archi_incidenti = self._graph.edges(nodo, data='weight')
            #x il nodo corrente chiediamo a network x tutti gli archi collegati a quel nodo
            #e includiamo anche il peso di ciascun risultato
            pesi = [peso for _, _, peso in archi_incidenti]
            #scorre gli archi incidenti e per ogni tupla (nodo1,nodo2,peso) prende solo il peso
            pesi_minimi[nodo] = min(pesi) if pesi else 0
            # salviamo per quel nodo quello col peso minimo

        # ordina i nodi in senso decrescente di peso minimo
        nodi_ordinati = sorted(largest_component,
                               key=lambda n: pesi_minimi[n],
                               reverse=True)
        # ordiniamo e restituiamo

        return num_components, nodi_ordinati, len(largest_component)
