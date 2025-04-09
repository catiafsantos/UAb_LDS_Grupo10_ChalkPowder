from typing import List, Dict, Any, Callable
from graficos.eventos import Event

# =============================================================================
# Eventos Utilizados pelo Model
# =============================================================================

class FicheiroInvalidoEvt(Event):
    """
    Evento emitido quando ocorre algum erro relacionado com o ficheiro.
    Os handlers subscritos recebem uma mensagem (string) a explicar o erro.
    """
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, mensagem: str) -> None:
        super().invoke(mensagem)

class EstadoProcessamentoEvt(Event):
    """
    Evento para notificar alterações no estado do processamento.
    Ex.: "Início da importação", "Processamento concluído", "Gravação concluída", etc.
    """
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, estado: str) -> None:
        super().invoke(estado)

class ImportacaoConcluidaEvt(Event):
    """
    Evento para notificar que a importação foi concluída com sucesso.
    (Sem argumentos)
    """
    def add_handler(self, handler: Callable[[], None]) -> None:
        super().add_handler(handler)
    def invoke(self) -> None:
        super().invoke()

class GraficoGravadoEvt(Event):
    """
    Evento para notificar que a gravação do gráfico foi concluída com sucesso.
    (Sem argumentos)
    """
    def add_handler(self, handler: Callable[[], None]) -> None:
        super().add_handler(handler)
    def invoke(self) -> None:
        super().invoke()

class GraficoDisponivelEvt(Event):
    """
    Evento para notificar que existem gráficos disponíveis após a importação.
    Os handlers recebem a lista de gráficos.
    """
    def add_handler(self, handler: Callable[[List[str]], None]) -> None:
        super().add_handler(handler)
    def invoke(self, lista_graficos: List[str]) -> None:
        super().invoke(lista_graficos)

# --- Novos eventos para diferenciar os tipos de falha ---
class FalhaImportacaoEvt(Event):
    """
    Evento para notificar que ocorreu uma falha de importação (dados/ficheiro).
    Os handlers recebem uma mensagem específica de falha de importação.
    """
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, mensagem: str) -> None:
        super().invoke(mensagem)

class FalhaGravacaoEvt(Event):
    """
    Evento para notificar que ocorreu uma falha na gravação do gráfico.
    Os handlers recebem uma mensagem específica de falha na gravação.
    """
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, mensagem: str) -> None:
        super().invoke(mensagem)

# =============================================================================
# Classe Model
# =============================================================================

class Model:
    def __init__(self, view) -> None:  
        self.view = view
        self.dados: List[Dict[str, Any]] = []   # Armazena os dados importados
        self.graficos: List[str] = []             # Lista de gráficos gerados

        # Eventos de sucesso e estado
        self.__estado_processamento_evt: EstadoProcessamentoEvt = EstadoProcessamentoEvt()
        self.__importacao_concluida_evt: ImportacaoConcluidaEvt = ImportacaoConcluidaEvt()
        self.__grafico_gravado_evt: GraficoGravadoEvt = GraficoGravadoEvt()
        self.__grafico_disponivel_evt: GraficoDisponivelEvt = GraficoDisponivelEvt()

        # Eventos para falhas diferenciadas
        self.__falha_importacao_evt: FalhaImportacaoEvt = FalhaImportacaoEvt()
        self.__falha_gravacao_evt: FalhaGravacaoEvt = FalhaGravacaoEvt()

        # Evento genérico de ficheiro inválido:
        self.__ficheiro_invalido_evt: FicheiroInvalidoEvt = FicheiroInvalidoEvt()

    # =========================================================================
    # Propriedades para acesso aos eventos
    # =========================================================================

    @property
    def estado_processamento_evt(self) -> EstadoProcessamentoEvt:
        return self.__estado_processamento_evt

    @property
    def importacao_concluida_evt(self) -> ImportacaoConcluidaEvt:
        return self.__importacao_concluida_evt

    @property
    def grafico_gravado_evt(self) -> GraficoGravadoEvt:
        return self.__grafico_gravado_evt

    @property
    def grafico_disponivel_evt(self) -> GraficoDisponivelEvt:
        return self.__grafico_disponivel_evt

    @property
    def falha_importacao_evt(self) -> FalhaImportacaoEvt:
        return self.__falha_importacao_evt

    @property
    def falha_gravacao_evt(self) -> FalhaGravacaoEvt:
        return self.__falha_gravacao_evt

    @property
    def ficheiro_invalido_evt(self) -> FicheiroInvalidoEvt:
        return self.__ficheiro_invalido_evt

    # =========================================================================
    # Métodos de Notificação (Invokes encapsulados)
    # =========================================================================

    def mensagem_estado_processamento(self, estado: str) -> None:
        """
        Notifica os interessados de uma alteração no estado do processamento.
        (Ex.: "Início da importação", "Processamento concluído", etc.)
        """
        self.__estado_processamento_evt.invoke(estado)

    def mensagem_importacao_concluida(self) -> None:
        """
        Notifica que a importação foi concluída com sucesso.
        """
        self.__importacao_concluida_evt.invoke()

    def mensagem_grafico_gravado(self) -> None:
        """
        Notifica que a gravação do gráfico foi concluída com sucesso.
        """
        self.__grafico_gravado_evt.invoke()

    def notifica_graficos_disponiveis(self) -> None:
        """
        Notifica que existem gráficos disponíveis (por exemplo, "Barras", "Linhas", "Pizza").
        """
        self.__grafico_disponivel_evt.invoke(self.graficos)

    # --- Novos métodos de notificação de falhas diferenciadas ---
    def mensagem_falha_importacao(self, mensagem: str = "Falha de importação do ficheiro.") -> None:
        """
        Notifica que ocorreu uma falha específica na importação.
        """
        self.__falha_importacao_evt.invoke(mensagem)

    def mensagem_falha_gravacao(self, mensagem: str = "Falha na gravação do gráfico.") -> None:
        """
        Notifica que ocorreu uma falha específica na gravação.
        """
        self.__falha_gravacao_evt.invoke(mensagem)

    # =========================================================================
    # Métodos de dados (Importação e Gravação)
    # =========================================================================

    def importar_ficheiro(self, caminho: str) -> None:
        """
        Importa e processa o ficheiro de dados.        
        :param caminho: Caminho do ficheiro a importar.
        """
        pass
        # TODO: Implementar a lógica de importação do ficheiro.

    def gravar_grafico(self, caminho: str) -> None:
        """
        Grava o gráfico num ficheiro.        
        :param caminho: Caminho onde o gráfico será gravado.
        """
        pass
        # TODO: Implementar a lógica de gravação do gráfico.
