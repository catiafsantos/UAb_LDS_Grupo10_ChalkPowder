from graficos.eventos import Event
from graficos.view import View
from graficos.model import Model


class MostraDlgImportaDadosEvt(Event):
    """Evento emitido pelo Controller para informar a View que deve obter do user 
    um ficheiro de dados."""
    def invoke(self) -> None:
        super().invoke()


class Controller:
    def __init__(self) -> None:
        self.view = view = View()
        self.model = Model(view)

        # Definição de eventos do Controller
        self.__mostra_dlg_importa_dados_evt: MostraDlgImportaDadosEvt = MostraDlgImportaDadosEvt()

        # Subscrição de eventos emitidos pelo Controller
        self.__mostra_dlg_importa_dados_evt.add_handler(view.mostra_dlg_carregar_ficheiro)

        # Subscrições de eventos da View
        self.view.importar_ficheiro_click_evt.add_handler(self.user_importa_ficheiro)
        self.view.ficheiro_selecionado_evt.add_handler(self.user_seleciona_ficheiro)

    def run(self):
        self.view.iniciar_interface()

    def user_importa_ficheiro(self) -> None:
        self.__mostra_dlg_importa_dados_evt.invoke()
    
    def user_seleciona_ficheiro(self, fullpath: str):
        self.model.importa_ficheiro(fullpath)