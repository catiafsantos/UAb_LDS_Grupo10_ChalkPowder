from .ILogger import ILogger


class ControllerConsoleLogger(ILogger):
    """Classe responsável por registar mensagens no terminal (stdout), usada pelo Controller.

    Esta classe implementa a interface ILogger e pode ser instanciada diretamente
    ou substituída por outras variantes (ex: logs para ficheiro, serviços externos, mocks).

    O Controller utiliza esta classe para registar eventos de execução e mensagens
    de erro de forma genérica e desacoplada, de acordo com os princípios do padrão MVC 
    e da SimProgramming.
    """
    def log_info(self, mensagem: str) -> None:
        print(f"[INFO] {mensagem}")

    def log_erro(self, mensagem: str) -> None:
        print(f"[ERRO] {mensagem}")