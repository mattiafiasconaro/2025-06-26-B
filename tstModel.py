from model.model import Model

myModel=Model()

myModel.buildGraph(1998,1993)
nodi,archi=myModel.getGraphDetails()
print(nodi,archi)

