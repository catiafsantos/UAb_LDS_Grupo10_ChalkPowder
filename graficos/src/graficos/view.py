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


class SolicitaGuardarGraficoEvt(Event):
    """Evento emitido pela View quando o User seleciona opção de gravar
    "Guardar Gráfico"
    """
    def invoke(self) -> None:
        super().invoke()


class GravaGraficoClickEvt(Event):
    """Evento emitido pela View quando o User gravar o gráfico num diálogo de 
    gravação de ficheiros.
    """
    def add_handler(self, handler: Callable[[str], None]):
        super().add_handler(handler)

    def invoke(self, caminho: str) -> None:
        super().invoke(caminho)


class View:
    def __init__(self) -> None:
        # TODO: Cenas da View, Tk...

        # Eventos expostos pela view
        self.importar_ficheiro_click_evt: ImportarFicheiroClickEvt = ImportarFicheiroClickEvt()
        # TODO: temos que fazer invoke() deste evento self.importar_ficheiro_click_evt quando o User
        # selecionar importar ficheiro no UI

        self.__ficheiro_selecionado_evt: FicheiroSelecionadoEvt = FicheiroSelecionadoEvt()

        # TODO: é preciso fazer invoke() deste evento quando o User selecionar/clicar opção para 
        #  gravar gráfico
        self.__solicita_guardar_grafico_click_evt: SolicitaGuardarGraficoEvt = SolicitaGuardarGraficoEvt()

        # TODO: é preciso fazer invoke() deste evento quando o User selecionar/clicar opção para 
        #  gravar gráfico
        self.__grava_grafico_click_evt: GravaGraficoClickEvt = GravaGraficoClickEvt()

    @property
    def ficheiro_selecionado_evt(self):
        return self.__ficheiro_selecionado_evt
    
    @property
    def solicita_guardar_grafico_click_evt(self):
        return self.__solicita_guardar_grafico_click_evt

    @property
    def grava_grafico_click_evt(self):
        return self.__grava_grafico_click_evt

    def ativar_interface(self):
        # Inicia a interface gráfica
        print("Iniciando a interface gráfica...")
        # Aqui você pode adicionar o código para iniciar a interface gráfica, como criar janelas, botões, etc.
        # Exemplo simples de interface gráfica com Tkinter

    def mostra_dlg_carregar_ficheiro(self):
        # TODO: tk mostra tkinter.filedialog para obter um ficheiro do utilizador
        # Quando a View tiver um ficheiro do utilizador de emitir um evento (ainda não criado) para
        # informar os interessados (o Controller)
        print("View recebeu comando para mostra file selection dlg e obter ficheiro de dados do User")
    
    def mostra_dlg_grava_grafico(self):
        # chamado pelo controller quando é hora de gravar o gráfico
        # TODO: Penso que a melhor opção é usar um diálogo de tkinter.filedialog
        print("View recebeu comando para gravar gráfico")
    
    def notifica_ficheiro_selecionado(self, fullpath: str):
        self.__ficheiro_selecionado_evt.invoke(fullpath)
