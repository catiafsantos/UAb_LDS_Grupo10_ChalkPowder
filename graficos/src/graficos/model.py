from typing import List, Dict, Any
from graficos.eventos import Event

# Definição de eventos específicos para o model
class FicheiroInvalidoEvt(Event):
    ''' Evento emitido quando o ficheiro é inválido.     
        Por exemplo, quando o ficheiro não existe ou não é um ficheiro de dados válido.
    '''
    #def add_handler(self, handler: Callable[[str], None]) -> None:
        #super().add_handler(handler) 

    def invoke(self, mensagem: str) -> None: 
        super().invoke(mensagem)

class EstadoProcessamentoEvt(Event):
    ''' Evento emitido quando o estado do processamento muda. 
        Por exemplo, quando o processamento de um ficheiro é iniciado ou terminado.
        Ou quando o processamento de um ficheiro falha.
    '''

    #def add_handler(self, handler: Callable[[str], None]) -> None:
        #super().add_handler(handler) 

    def invoke(self, estado: str) -> None:
        super().invoke(estado)

# TODO: Restantes eventos de notificação


# Classe Model
class Model:
    def __init__(self, view) -> None:
        self.view = view
        # Indica explicitamente o tipo das estruturas internas para satisfazer Mypy
        self.dados: List[Dict[str, Any]] = []
        self.graficos: List[str] = []

        # Definição dos eventos com type hints
        self.__ficheiro_invalido_evt: FicheiroInvalidoEvt = FicheiroInvalidoEvt()
        self.__estado_processamento_evt: EstadoProcessamentoEvt = EstadoProcessamentoEvt()
		# TODO: Restantes eventos

    # Propriedades para acesso aos eventos, facilitando a ligação entre o model e a view
    @property
    def ficheiro_invalido_evt(self) -> FicheiroInvalidoEvt:
        return self.__ficheiro_invalido_evt

    @property
    def estado_processamento_evt(self) -> EstadoProcessamentoEvt:
        return self.__estado_processamento_evt

	# TODO: Restantes eventos

    # Método para notificar interessados que o ficheiro é inválido
    def mensagem_ficheiro_invalido(self) -> None:
        """Notifica interessados que houve um erro na importação do ficheiro."""
        # mensagem = "Erro: Ficheiro inválido."
        self.__ficheiro_invalido_evt.invoke("Erro: Ficheiro inválido.")

    def mensagem_estado_processamento(self) -> None:
        """Notifica interessados que o estado do processamento mudou."""
        # estado = "Estado do processamento atualizado."
        self.__estado_processamento_evt.invoke("Estado do processamento atualizado.")

    # Método para importar ficheiro
    def importar_ficheiro(self, caminho: str) -> None:
        pass
    

	# TODO: Restantes eventos
  
