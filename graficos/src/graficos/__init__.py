from graficos.controller import Controller
from graficos.model import Model
from graficos.view import View

def main() -> None:
    view = View()
    model = Model(view)
    controller = Controller(view, model)
    controller.run()
