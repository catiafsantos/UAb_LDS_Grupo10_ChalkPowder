from typing import Callable

from graficos.eventos import Event
from graficos.view import View
from graficos.model import Model


class MostraDlgCarregarFicheiroEvt(Event):
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


class MostraDlgGravaGraficoEvt(Event):
    """Evento emitido pelo Controller para informar a View que deve mostrar ao User
    o diálogo de gravação.
    """
    def invoke(self) -> None:
        super().invoke()


class GravaGraficoEvt(Event):
    """Evento emitido pelo Controller para informar o Model que deve gravar o gráfico 
    e em que localização do filesystem e com que nome gravá-lo.
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
        self.__mostra_dlg_carregar_ficheiro_evt: MostraDlgCarregarFicheiroEvt = MostraDlgCarregarFicheiroEvt()
        self.__importar_ficheiro_evt: ImportarFicheiroEvt = ImportarFicheiroEvt()
        self.__mostra_dlg_grava_grafico_evt: MostraDlgGravaGraficoEvt = MostraDlgGravaGraficoEvt()
        self.__grava_grafico_evt : GravaGraficoEvt = GravaGraficoEvt()

        # Subscrição de eventos emitidos pelo Controller
        self.__mostra_dlg_carregar_ficheiro_evt.add_handler(view.mostra_dlg_carregar_ficheiro)
        self.__importar_ficheiro_evt.add_handler(model.importar_ficheiro)
        self.__mostra_dlg_grava_grafico_evt.add_handler(view.mostra_dlg_grava_grafico)
        self.__grava_grafico_evt.add_handler(model.gravar_grafico)

        # Subscrições de eventos da View
        view.importar_ficheiro_click_evt.add_handler(self.user_importa_ficheiro)
        view.ficheiro_selecionado_evt.add_handler(self.user_seleciona_ficheiro)
        view.grafico_selecionado_click_evt.add_handler(self.user_selecionou_grafico)
        view.submissao_parametros_evt.add_handler(self.user_submeteu_parametros)
        view.solicita_guardar_grafico_click_evt.add_handler(self.user_solicitou_gravacao)
        view.grava_grafico_click_evt.add_handler(self.user_grava_grafico)

    def run(self):
        try:
            self.view.ativar_interface()
        except Exception as e:
            print("Biblioteca de interface indisponível, falha crítica.")
            print("Contacte o suporte: erro f{e}")

    def user_importa_ficheiro(self) -> None:
        """User selecionou importar ficheiro"""
        self.__mostra_dlg_carregar_ficheiro_evt.invoke()

    def user_seleciona_ficheiro(self, caminho: str):
        """User selecionou um ficheiro para importar."""
        self.__importar_ficheiro_evt.invoke(caminho)

    def user_selecionou_grafico(self, tipo: str):
        self.tipo_grafico = tipo
        colunas = self.model.get_colunas_disponiveis()
        self.view.mostra_formulario_parametros(colunas)

    def user_submeteu_parametros(self, x: str, y: str, x_label: str, y_label: str):
        self.model.gerar_grafico(self.tipo_grafico, x, y, x_label, y_label)

    def user_solicitou_gravacao(self):
        """User selecionou opção de gravar gráfico"""
        # Notifica a View para mostrar formulário (diálogo) de gravação
        self.__mostra_dlg_grava_grafico_evt.invoke()

    def user_grava_grafico(self, caminho: str):
        """User grava gráfico."""
        # Notifica Model para gravar gráfico com a fullpath especificada
        self.__grava_grafico_evt.invoke(caminho)
