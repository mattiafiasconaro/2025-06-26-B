import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleBuildGraph(self, e):
        annoMin=int(self._view._ddYear1.value)
        annoMax=int(self._view._ddYear2.value)

        if annoMax is None or annoMin is None:
            self._view._txt_result.controls.append(ft.Text("Inserire un anno ", color="red"))

            self._view.update_page()
            return
        if annoMax<annoMin:
            self._view._txt_result.controls.append(ft.Text("Inserire un anno minore ", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(annoMax,annoMin)
        nodi,archi=self._model.getGraphDetails()
        self._view._txt_result.controls.append(ft.Text("grafo correttamente eseguito", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"Numero nodi :{nodi} - numero archi {archi}", color="blue"))


        self._view.update_page()

    def handlePrintDetails(self, e):
        numComponents, nodiOrdinati,lunghezza=self._model.getConnectedComponents()
        for n in nodiOrdinati:
            self._view._txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()

    def handleCercaDreamChampionship(self, e):
        pass

    def fillDDYears(self):
        anni= self._model.getAllYears()
        for a in anni :
            self._view._ddYear1.options.append(ft.dropdown.Option(a))
            self._view._ddYear2.options.append(ft.dropdown.Option(a))
        self._view.update_page()

