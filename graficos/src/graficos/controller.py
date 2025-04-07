from typing import Callable

from graficos.eventos import Event
from graficos.view import View
from graficos.model import Model


class MostraDlgImportaDadosEvt(Event):
    """Evento emitido pelo Controller para informar a View que deve obter do user 
    um ficheiro de dados."""
    def invoke(self) -> None:
        super().invoke()


class ImportarFicheiroEvt(Event):
    """Evento emitido pelo Controller para informar o Model que o ficheiro de dados 
    selecionado pelo user está disponível para ser importado.
    """
    def add_handler(self, handler: Callable[[str], None]):
        super().add_handler(handler)

    def invoke(self, caminho: str) -> None:
        super().invoke(caminho)


class Controller:
    def __init__(self) -> None:
        self.view = view = View()
        self.model = model = Model(view)

        # Definição de eventos do Controller
        self.__mostra_dlg_importa_dados_evt: MostraDlgImportaDadosEvt = MostraDlgImportaDadosEvt()
        self.__importar_ficheiro_evt: ImportarFicheiroEvt = ImportarFicheiroEvt()

        # Subscrição de eventos emitidos pelo Controller
        self.__mostra_dlg_importa_dados_evt.add_handler(view.mostra_dlg_carregar_ficheiro)
        self.__importar_ficheiro_evt.add_handler(model.importar_ficheiro)

        # Subscrições de eventos da View
        self.view.importar_ficheiro_click_evt.add_handler(self.user_importa_ficheiro)
        self.view.ficheiro_selecionado_evt.add_handler(self.user_seleciona_ficheiro)

    def run(self):
        self.view.ativar_interface()

    def user_importa_ficheiro(self) -> None:
        """User selecionou importar ficheiro"""
        self.__mostra_dlg_importa_dados_evt.invoke()

    def user_seleciona_ficheiro(self, caminho: str):
        """User selecionou um ficheiro para importar."""
        self.__importar_ficheiro_evt.invoke(caminho)
