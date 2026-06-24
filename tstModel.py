from model.model import Model

myModel=Model()

myModel.buildGraph(2016,2010)
nodi,archi=myModel.getGraphDetails()
print(nodi,archi)

