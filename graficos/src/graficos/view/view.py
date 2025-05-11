from typing import Callable, List
import tkinter as tk
from tkinter import messagebox

from graficos.IUserView import IUserView
from graficos.controller.controllerEvent import ControllerEvent
from graficos.controller.ILogger import ILogger
from graficos.guiview import (
    construir_interface_principal, construir_formulario_parametros,
    obter_parametros_formulario, carregar_ficheiro_csv_com_dialogo,
    guardar_grafico_com_dialogo, preparar_interface_grafico,
    voltar_menu_inicial_interface
)


# Eventos da View
class ImportarFicheiroClickEvt(ControllerEvent):
    """Evento emitido pela View quando o User selecciona importar ficheiro."""
    def invoke(self) -> None:
        super().invoke()


class FicheiroSelecionadoClickEvt(ControllerEvent):
    """Evento emitido pela View quando o User seleccionou um ficheiro do file system.

    Quando invocado este evento passa a fullpath do ficheiro seleccionado para o subscritor.
    """
    def add_handler(self, handler: Callable[[str], None]):
        """O subscritor recebe a fullpath do ficheiro seleccionado."""
        return super().add_handler(handler)


class GraficoSelecionadoClickEvt(ControllerEvent):
    """Evento emitido pela View quando o User escolhe um tipo de gráfico.
    """
    def add_handler(self, handler: Callable[[str], None]):
        super().add_handler(handler)

    def invoke(self, grafico_selecionado: str):
        super().invoke(grafico_selecionado)


class SubmissaoParametrosEvt(ControllerEvent):
    """Emitido quando o utilizador submete os parâmetros para construir o gráfico."""
    def add_handler(self, handler: Callable[[str, str, str, str], None]):
        super().add_handler(handler)

    def invoke(self, x_col: str, y_col: str, x_label: str, y_label: str):
        super().invoke(x_col, y_col, x_label, y_label)


class SolicitaGuardarGraficoClickEvt(ControllerEvent):
    """Evento emitido pela View quando o User seleciona opção de gravar
    "Guardar Gráfico"
    """
    def invoke(self) -> None:
        super().invoke()


class GravaGraficoClickEvt(ControllerEvent):
    """Evento emitido pela View quando o User gravar o gráfico num diálogo de 
    gravação de ficheiros.
    """
    def add_handler(self, handler: Callable[[str], None]):
        super().add_handler(handler)

    def invoke(self, caminho: str) -> None:
        super().invoke(caminho)

# Simula o Throw do C#
class ErroInternoEvt(ControllerEvent):
    """Emitido quando ocorre um erro interno no sistema."""
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, stacktrace: str) -> None:
        super().invoke(stacktrace)


class View(tk.Tk, IUserView):
    def __init__(self, logger: ILogger) -> None:
        super().__init__()
        self.logger = logger 
        # Eventos expostos pela view
        self.__importar_ficheiro_click_evt: ImportarFicheiroClickEvt = ImportarFicheiroClickEvt()
        self.__ficheiro_selecionado_evt: FicheiroSelecionadoClickEvt = FicheiroSelecionadoClickEvt()
        self.__grafico_selecionado_click_evt : GraficoSelecionadoClickEvt = GraficoSelecionadoClickEvt()
        self.__submissao_parametros_evt = SubmissaoParametrosEvt()
        self.__solicita_guardar_grafico_click_evt: SolicitaGuardarGraficoClickEvt = SolicitaGuardarGraficoClickEvt()
        self.__grava_grafico_click_evt: GravaGraficoClickEvt = GravaGraficoClickEvt()

        # Variáveis de Estado
        self.estado_var = tk.StringVar()
        self.grafico_var = tk.StringVar(value="Escolha um gráfico")

    # Propriedades para acesso a eventos
    @property
    def importar_ficheiro_click_evt(self) -> ImportarFicheiroClickEvt:
        return self.__importar_ficheiro_click_evt
        
    @property
    def ficheiro_selecionado_evt(self):
        return self.__ficheiro_selecionado_evt
    
    @property
    def grafico_selecionado_click_evt(self):
        return self.__grafico_selecionado_click_evt
        
    @property
    def submissao_parametros_evt(self):
        return self.__submissao_parametros_evt
        
    @property
    def solicita_guardar_grafico_click_evt(self):
        return self.__solicita_guardar_grafico_click_evt

    @property
    def grava_grafico_click_evt(self):
        return self.__grava_grafico_click_evt

    # Método que ativa a interface gráfica (tkinter)
    def ativar_interface(self) -> None:
        """Constrói a interface principal e ativa o loop principal da aplicação."""
        elementos = construir_interface_principal(
            root=self,
            grafico_var=self.grafico_var,
            estado_var=self.estado_var,
            on_importar_ficheiro_click=self.__on_importar_ficheiro_click,
            on_grafico_selecionado=self.__on_grafico_selecionado,
            on_home_click=self.__on_home_click
        )

        if elementos is None:
            return
        
        # Elementos principais da interface
        self.btn_importar = elementos["btn_importar"]
        self.dropdown_menu = elementos["dropdown_menu"]
        self.label_estado = elementos["label_estado"]
        self.btn_home = elementos["btn_home_frame"]

        # Mensagem inicial
        self.mostra_mensagem_info("Pronto para iniciar.")
        self.logger.log_info("ativar_interface() - Interface gráfica iniciada.")
        self.mainloop()

    # Métodos auxiliares da interface
    def mostra_erro_importacao(self, mensagem: str):
        messagebox.showerror("Erro de Importação", mensagem)
        self.logger.log_erro(f"mostra_erro_importacao() - {mensagem}")

    def mostra_erro_ficheiro(self, mensagem: str):
        messagebox.showwarning("Ficheiro Inválido", mensagem)
        self.logger.log_erro(f"mostra_erro_ficheiro() - {mensagem}")

    def mostra_mensagem_info(self, mensagem: str):
        self.estado_var.set(mensagem)

    def atualiza_lista_graficos(self, graficos: list[str]):
        self.graficos_disponiveis = graficos
        self.btn_importar.place_forget()
        self.dropdown_menu["values"] = graficos
        self.grafico_var.set("Escolha um gráfico")
        self.dropdown_menu.place(relx=0.5, rely=0.4, anchor="center")

    # Callbacks de Ações do utilizador
    def __on_importar_ficheiro_click(self):
        # Método que informa o Controller que o utilizador clicou no botão "Importar Ficheiro"
        self.logger.log_info("on_importar_ficheiro_click() - Botão 'Importar Ficheiro' clicado.")
        self.importar_ficheiro_click_evt.invoke()

    def __on_grafico_selecionado(self, *args):
        # Método que informa o Controller que o utilizador selecionou o tipo de gráfico
        self.mostra_mensagem_info("Escolha de tipo de gráfico.")
        grafico = self.grafico_var.get()
        if grafico != "Escolha um gráfico":
            self.__grafico_selecionado_click_evt.invoke(grafico)
            self.mostra_mensagem_info(f"Gráfico selecionado: {grafico}")
            self.logger.log_info(f"on_grafico_selecionado() - Gráfico selecionado: {grafico}")

    def __on_guardar_grafico_click(self):
        # Método que informa o Controller que o utilizador clicou no botão "Guardar gráfico"
        self.__solicita_guardar_grafico_click_evt.invoke()
        self.logger.log_info("on_guardar_grafico_click() - Botão 'Guardar Gráfico' clicado.")

    def __on_submeter_parametros(self):
        # Método que informa o Controller que os parâmetros do formulário foram preenchidos
        self.mostra_mensagem_info("A validar os parâmetros...")
        self.logger.log_info("on_submeter_parametros() - Validação de parâmetros iniciada.")
        self.update_idletasks()

        # Obtém os parâmetros preenchidos no formulário
        x_col, y_col, x_label, y_label, erro = obter_parametros_formulario(
            self.x_var, self.y_var, self.x_label_var, self.y_label_var, self.opcao_labels
        )

        # Verifica se houve algum erro durante a validação
        if erro:
            self.mostra_erro_ficheiro(erro)
            self.mostra_mensagem_info(erro)
            self.logger.log_erro(f"on_submeter_parametros() - Erro na validação: {erro}")
            return
                
        self.mostra_mensagem_info("Parâmetros corretos. A gerar gráfico...")
        self.logger.log_info(f"on_submeter_parametros() - Parâmetros validados: x={x_col}, y={y_col}, x_label={x_label}, y_label={y_label}")
        self.__submissao_parametros_evt.invoke(x_col, y_col, x_label, y_label)

    def __on_home_click(self):
        """Callback para voltar ao menu inicial quando o botão Home é clicado."""
        self.mostra_mensagem_info("A voltar ao menu principal...")
        voltar_menu_inicial_interface(self)

    # Dialogs
    def mostra_dlg_carregar_ficheiro(self) -> None:
        # Método que mostra o diálogo para carregar um ficheiro 
        path = carregar_ficheiro_csv_com_dialogo(
            self.btn_importar,
            self.mostra_mensagem_info,
            self.mostra_erro_importacao
        )

        # Verifica se um caminho foi retornado pelo diálogo
        if path:
            self.logger.log_info(f"mostra_dlg_carregar_ficheiro() - Ficheiro selecionado: {path}") 
            self.notifica_ficheiro_selecionado(path)

    # Método que mostra ao utilizador as opções de gravação do ficheiro
    def mostra_dlg_grava_grafico(self) -> None:
        guardar_grafico_com_dialogo(
            callback_gravar=self.__grava_grafico_click_evt.invoke,
            mostrar_info=self.mostra_mensagem_info,
            voltar_menu=self.voltar_menu_inicial
        )
        
    # Outros
    def notifica_ficheiro_selecionado(self, fullpath: str):
        # Método que notifica o controller que um ficheiro foi selecionado
        self.__ficheiro_selecionado_evt.invoke(fullpath)

    # Método que mostra o formulário com os vários parâmetros
    def mostra_formulario_parametros(self, colunas: list[str]) -> None:
        # Inicializar variáveis e opções
        self.x_var = tk.StringVar(value="Escolher coluna X")
        self.y_var = tk.StringVar(value="Escolher coluna Y")
        self.x_label_var = tk.StringVar(value="")
        self.y_label_var = tk.StringVar(value="")
        self.opcao_labels = tk.StringVar(value="usar_colunas")

        # Constrói o formulário
        self.form_frame = construir_formulario_parametros(
            parent=self,
            colunas=colunas,
            x_var=self.x_var,
            y_var=self.y_var,
            x_label_var=self.x_label_var,
            y_label_var=self.y_label_var,
            opcao_labels=self.opcao_labels,
            on_submeter_parametros=self.__on_submeter_parametros
        ) 

    # Método para mostrar o gráfico
    def mostrar_grafico(self, __: List[str] = []) -> None:
        preparar_interface_grafico(self, self.__on_guardar_grafico_click)
        self.logger.log_info("mostrar_grafico() - Interface de gráfico exibida.")

    # Método que permite voltar ao menu inicial
    def voltar_menu_inicial(self) -> None:
        voltar_menu_inicial_interface(self)

        self.mostra_mensagem_info("Pronto para importar um novo ficheiro.")
        self.logger.log_info("voltar_menu_inicial() - Retornado ao menu principal.")