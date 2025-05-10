from graficos.controller.controller import Controller
from graficos.view import View


def main() -> None:
    controller = Controller(View)
    controller.run()
