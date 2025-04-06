from typing import Callable

from graficos.eventos import Event


class ImportarFicheiroClickEvt(Event):
    """Evento emitido pela View quando o User selecciona importar ficheiro."""
    def invoke(self) -> None:
        super().invoke()


class FicheiroSelecionadoEvt(Event):
    """Evento emitido pela View quando o User seleccionou um ficheiro do file system.

    Quando invocado este evento passa a fullpath do ficheiro seleccionado para o subscritor.
    """
    def add_handler(self, handler: Callable[[str], None]):
        """O subscritor recebe a fullpath do ficheiro seleccionado."""
        return super().add_handler(handler)


class View:
    def __init__(self) -> None:
        # TODO: Cenas da View, Tk...

        # Eventos expostos pela view
        self.importar_ficheiro_click_evt: ImportarFicheiroClickEvt = ImportarFicheiroClickEvt()
        # TODO: temos que fazer invoke() deste evento self.importar_ficheiro_click_evt quando o User
        # selecionar importar ficheiro no UI

        self.__ficheiro_selecionado_evt: FicheiroSelecionadoEvt = FicheiroSelecionadoEvt()

    @property
    def ficheiro_selecionado_evt(self):
        return self.__ficheiro_selecionado_evt

    def iniciar_interface(self):
        # Inicia a interface gráfica
        print("Iniciando a interface gráfica...")
        # Aqui você pode adicionar o código para iniciar a interface gráfica, como criar janelas, botões, etc.
        # Exemplo simples de interface gráfica com Tkinter

    def mostra_dlg_carregar_ficheiro(self):
        # TODO: tk mostra tkinter.filedialog para obter um ficheiro do utilizador
        # Quando a View tiver um ficheiro do utilizador de emitir um evento (ainda não criado) para
        # informar os interessados (o Controller)
        print("View recebeu comando para mostra file selection dlg e obter ficheiro de dados do User")
    
    def notifica_ficheiro_selecionado(self, fullpath: str):
        self.__ficheiro_selecionado_evt.invoke(fullpath)
