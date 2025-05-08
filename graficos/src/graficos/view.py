from typing import Callable, List
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt

from graficos.eventos import Event


# Eventos da View
class ImportarFicheiroClickEvt(Event):
    """Evento emitido pela View quando o User selecciona importar ficheiro."""
    def invoke(self) -> None:
        super().invoke()


class FicheiroSelecionadoClickEvt(Event):
    """Evento emitido pela View quando o User seleccionou um ficheiro do file system.

    Quando invocado este evento passa a fullpath do ficheiro seleccionado para o subscritor.
    """
    def add_handler(self, handler: Callable[[str], None]):
        """O subscritor recebe a fullpath do ficheiro seleccionado."""
        return super().add_handler(handler)


class GraficoSelecionadoClickEvt(Event):
    """Evento emitido pela View quando o User escolhe um tipo de gráfico.
    """
    def add_handler(self, handler: Callable[[str], None]):
        super().add_handler(handler)

    def invoke(self, grafico_selecionado: str):
        super().invoke(grafico_selecionado)


class SubmissaoParametrosEvt(Event):
    """Emitido quando o utilizador submete os parâmetros para construir o gráfico."""
    def add_handler(self, handler: Callable[[str, str, str, str], None]):
        super().add_handler(handler)

    def invoke(self, x_col: str, y_col: str, x_label: str, y_label: str):
        super().invoke(x_col, y_col, x_label, y_label)


class SolicitaGuardarGraficoClickEvt(Event):
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

# Simula o Throw do C#
class ErroInternoEvt(Event):
    """Emitido quando ocorre um erro interno no sistema."""
    def add_handler(self, handler: Callable[[str], None]) -> None:
        super().add_handler(handler)
    def invoke(self, stacktrace: str) -> None:
        super().invoke(stacktrace)


class View(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        # Eventos expostos pela view
        self.importar_ficheiro_click_evt: ImportarFicheiroClickEvt = ImportarFicheiroClickEvt()
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
        self.mainloop()

    # Métodos auxiliares da interface
    def mostra_erro_importacao(self, mensagem: str):
        messagebox.showerror("Erro de Importação", mensagem)

    def mostra_erro_ficheiro(self, mensagem: str):
        messagebox.showwarning("Ficheiro Inválido", mensagem)

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
        self.importar_ficheiro_click_evt.invoke()

    def __on_grafico_selecionado(self, *args):
        # Método que informa o Controller que o utilizador selecionou o tipo de gráfico
        self.mostra_mensagem_info("Escolha de tipo de gráfico.")
        grafico = self.grafico_var.get()
        if grafico != "Escolha um gráfico":
            self.__grafico_selecionado_click_evt.invoke(grafico)
            self.mostra_mensagem_info(f"Gráfico selecionado: {grafico}")

    def __on_guardar_grafico_click(self):
        # Método que informa o Controller que o utilizador clicou no botão "Guardar gráfico"
        self.__solicita_guardar_grafico_click_evt.invoke()

    def __on_submeter_parametros(self):
        # Método que informa o Controller que os parâmetros do formulário foram preenchidos
        self.mostra_mensagem_info("A validar os parâmetros...")
        self.update_idletasks()

        # Obtém os parâmetros preenchidos no formulário
        x_col, y_col, x_label, y_label, erro = obter_parametros_formulario(
            self.x_var, self.y_var, self.x_label_var, self.y_label_var, self.opcao_labels
        )

        # Verifica se houve algum erro durante a validação
        if erro:
            self.mostra_erro_ficheiro(erro)
            self.mostra_mensagem_info(erro)
            return
                
        self.mostra_mensagem_info("Parâmetros corretos. A gerar gráfico...")
        self.__submissao_parametros_evt.invoke(x_col, y_col, x_label, y_label)

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
    def mostra_formulario_parametros(self, colunas: list[str]):
        # Inicializar variáveis e opções
        self.x_var = tk.StringVar(value="Escolher coluna X")
        self.y_var = tk.StringVar(value="Escolher coluna Y")
        self.x_label_var = tk.StringVar(value="")
        self.y_label_var = tk.StringVar(value="")
        self.opcao_labels = tk.StringVar(value="usar_colunas")

        # Frame do formulário
        self.form_frame = tk.Frame(self, bg="white")
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Opções de labels
        self.rb_usar_colunas = tk.Radiobutton(
            self.form_frame, text="Usar nomes das colunas como rótulos dos eixos",
            variable=self.opcao_labels, value="usar_colunas",
            command=self.__atualizar_visibilidade_labels, bg="white"
        )
        self.rb_usar_colunas.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

        self.rb_personalizar = tk.Radiobutton(
            self.form_frame, text="Personalizar nomes dos eixos",
            variable=self.opcao_labels, value="personalizar",
            command=self.__atualizar_visibilidade_labels, bg="white"
        )
        self.rb_personalizar.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="w")

        # Dropdowns para escolha de colunas
        self.dropdown_x = ttk.Combobox(self.form_frame, textvariable=self.x_var, values=colunas, state="readonly", width=30)
        self.dropdown_y = ttk.Combobox(self.form_frame, textvariable=self.y_var, values=colunas, state="readonly", width=30)
        self.dropdown_x.grid(row=2, column=0, columnspan=2, pady=5)
        self.dropdown_y.grid(row=3, column=0, columnspan=2, pady=5)

        # Entradas de texto para personalizar labels
        style = ttk.Style()
        style.configure("Custom.TEntry", foreground="#1E3A5F", font=("Helvetica", 11),
                        padding=10, relief="solid", borderwidth=1, background="white")

        self.entry_x_label = ttk.Entry(self.form_frame, textvariable=self.x_label_var, style="Custom.TEntry", width=30)
        self.entry_y_label = ttk.Entry(self.form_frame, textvariable=self.y_label_var, style="Custom.TEntry", width=30)

        self.label_x_entry = tk.Label(self.form_frame, text="Eixo X", bg="white", font=("Helvetica", 10))
        self.label_y_entry = tk.Label(self.form_frame, text="Eixo Y", bg="white", font=("Helvetica", 10))

        # Botão Submeter
        self.btn_submeter = tk.Button(
            self.form_frame, text="Submeter",
            command=self.__on_submeter_parametros,
            font=("Helvetica", 11), bg="#1E3A5F", fg="white"
        )
        self.btn_submeter.grid(row=5, column=0, columnspan=2, pady=20)

        self.__atualizar_visibilidade_labels() 

    # Método que atualiza a visibilidade dos labels
    def __atualizar_visibilidade_labels(self):
        if self.opcao_labels.get() == "personalizar":
            # Mostrar caixas de texto personalizadas
            self.label_x_entry.grid(row=2, column=0, sticky="e", padx=(10, 5), pady=5)
            self.entry_x_label.grid(row=2, column=1, sticky="w", padx=(5, 10), pady=5)

            self.label_y_entry.grid(row=3, column=0, sticky="e", padx=(10, 5), pady=5)
            self.entry_y_label.grid(row=3, column=1, sticky="w", padx=(5, 10), pady=5)

            self.dropdown_x.grid_remove()
            self.dropdown_y.grid_remove()
        else:
            # Mostrar dropdowns de colunas
            self.dropdown_x.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
            self.dropdown_y.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

            self.label_x_entry.grid_remove()
            self.label_y_entry.grid_remove()
            self.entry_x_label.grid_remove()
            self.entry_y_label.grid_remove()

    # Método para mostrar o gráfico
    def mostrar_grafico(self):
        # Esconde todos os elementos anteriores da interface
        if hasattr(self, "form_frame") and self.form_frame.winfo_exists():
            self.form_frame.destroy()
        if hasattr(self, "dropdown_menu") and self.dropdown_menu.winfo_exists():
            self.dropdown_menu.place_forget()
        if hasattr(self, "btn_importar") and self.btn_importar.winfo_exists():
            self.btn_importar.place_forget()

        # Frame para botão de guardar
        self.botao_frame = tk.Frame(self, bg="white")
        self.botao_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.btn_guardar_grafico = tk.Button(
            self.botao_frame, text="Guardar Gráfico",
            command=self.__on_guardar_grafico_click,
            font=("Helvetica", 11), bg="#1E3A5F", fg="white"
        )
        self.btn_guardar_grafico.pack(pady=10)

        self.mostra_mensagem_info("Gráfico gerado.")
        # Mostra o gráfico
        plt.show()

    # Método que permite voltar ao menu inicial
    def voltar_menu_inicial(self):
        """Reiniciar a interface para importar novo ficheiro."""
        if hasattr(self, "form_frame") and self.form_frame.winfo_exists():
            self.form_frame.destroy()
        if hasattr(self, "dropdown_menu") and self.dropdown_menu.winfo_exists():
            self.dropdown_menu.place_forget()
        if hasattr(self, "botao_frame") and self.botao_frame.winfo_exists():
            self.botao_frame.destroy()

        if hasattr(self, "btn_importar"):
            self.btn_importar.place(relx=0.5, rely=0.4, anchor="center")

        self.mostra_mensagem_info("Pronto para importar um novo ficheiro.")
