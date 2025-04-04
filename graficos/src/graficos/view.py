from typing import Callable

from graficos.eventos import Event


class ImportarFicheiroClickEvt(Event):
    """Evento emitido pela View quando o User selecciona importar ficheiro."""
    def invoke(self) -> None:
        super().invoke()


class View:
    def __init__(self) -> None:
        # TODO: Cenas da View, Tk...

        # Eventos expostos pela view
        self.importar_ficheiro_click_evt: ImportarFicheiroClickEvt = ImportarFicheiroClickEvt()
        # TODO: temos que fazer invoke() deste evento self.importar_ficheiro_click_evt quando o User
        # selecionar importar ficheiro no UI

    def iniciar_interface(self):
        # Inicia a interface gráfica
        print("Iniciando a interface gráfica...")
        # Aqui você pode adicionar o código para iniciar a interface gráfica, como criar janelas, botões, etc.
        # Exemplo simples de interface gráfica com Tkinter