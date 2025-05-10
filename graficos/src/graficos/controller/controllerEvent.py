from typing import Callable, Any


class ControllerEvent:
    """Classe que representa um evento para subscrição.

    Esta classe pode ser instanciada na forma atual ou pode ser especializada de modo a 
    a especificar a assinatura do handler aceite de modo mais estrito (usando type-hints) 
    e/ou para implementar outras customizações desejadas.
    """
    def __init__(self):
        self.__handlers = set()

    def add_handler(self, handler: Callable) -> None:
        """Método chamado para realizar a subscrição de um evento."""
        self.__handlers.add(handler)
    
    def remove_handler(self, handler: Callable) -> None:
        """Remove um handler/subscritor por object identity.
        
        Se o handler não está presente, simplesmente retorna None.
        """
        self.__handlers.discard(handler)
    
    def invoke(self, *args: Any, **kwargs: Any) -> None:
        """Realiza a notificação dos objectos subscritores.

        A classe/componente que implementa o evento chama este método quando a notificação
        dos subscritores deve ser realizada.
        """
        for handler in self.__handlers:
            handler(*args, **kwargs)