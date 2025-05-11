from abc import ABC, abstractmethod
from typing import List

class IUserView(ABC):

    # Propriedades para eventos
    @property
    @abstractmethod
    def importar_ficheiro_click_evt(self): pass

    @property
    @abstractmethod
    def ficheiro_selecionado_evt(self): pass

    @property
    @abstractmethod
    def grafico_selecionado_click_evt(self): pass

    @property
    @abstractmethod
    def submissao_parametros_evt(self): pass

    @property
    @abstractmethod
    def solicita_guardar_grafico_click_evt(self): pass

    @property
    @abstractmethod
    def grava_grafico_click_evt(self): pass

    # Métodos públicos obrigatórios
    @abstractmethod
    def ativar_interface(self) -> None: pass

    @abstractmethod
    def mostra_dlg_carregar_ficheiro(self) -> None: pass

    @abstractmethod
    def mostra_dlg_grava_grafico(self) -> None: pass

    @abstractmethod
    def mostra_formulario_parametros(self, colunas: List[str]) -> None: pass

    @abstractmethod
    def mostra_mensagem_info(self, mensagem: str) -> None: pass

    @abstractmethod
    def atualiza_lista_graficos(self, graficos: List[str]) -> None: pass

    @abstractmethod
    def mostrar_grafico(self, lista_graficos: List[str]) -> None: pass

    @abstractmethod
    def mostra_erro_importacao(self, mensagem: str) -> None: pass

    @abstractmethod
    def mostra_erro_ficheiro(self, mensagem: str) -> None: pass

    @abstractmethod
    def voltar_menu_inicial(self) -> None: pass
