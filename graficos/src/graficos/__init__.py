from graficos.controller import Controller
from graficos.view import View


def main() -> None:
    controller = Controller(View)
    controller.run()
