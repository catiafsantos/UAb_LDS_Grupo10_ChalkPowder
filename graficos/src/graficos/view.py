import traceback
from typing import Callable
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
        self.graficos_disponiveis: list[str] = []
        self.grafico_var = tk.StringVar(value="Escolha um gráfico")

    # Propriedades para acesso a eventos
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

    def ativar_interface(self):
        try:
            self.title("Conversor .csv para Gráfico")
            self.geometry("500x300")
            self.configure(bg="#1E3A5F")

            # Frame principal
            outer_frame = tk.Frame(self, bg="#1E3A5F")
            outer_frame.pack(expand=True, fill=tk.BOTH)

            container = tk.Frame(outer_frame, bg="White", bd=1, relief="solid")
            container.place(relx=0.5, rely=0.5, anchor="center", width=485, height=285)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            # Título
            titulo = tk.Label(
                container, text="Conversor CSV para Gráfico",
                font=("Helvetica", 14, "bold"), bg="white", fg="#1E3A5F"
            )
            titulo.place(relx=0.5, rely=0.20, anchor="center")

            # Botão Importar
            self.btn_importar = tk.Button(
                container, text="Importar Ficheiro", command=self.__on_importar_ficheiro_click,
                font=("Helvetica", 12), bg="#1E3A5F", fg="white", activebackground="#27496d",
                activeforeground="white", relief="raised", padx=10, pady=5, cursor="hand2"
            )
            self.btn_importar.place(relx=0.5, rely=0.4, anchor="center")

            # Dropdown escondido
            self.__configura_estilo_dropdown()
            self.dropdown_menu = ttk.Combobox(
                container, textvariable=self.grafico_var, state="readonly",
                font=("Helvetica", 11), width=30, style="CustomCombobox.TCombobox"
            )
            self.dropdown_menu.place_forget()
            self.grafico_var.trace_add("write", self.__on_grafico_selecionado)

            # Label estado
            self.label_estado = tk.Label(
                container, textvariable=self.estado_var,
                font=("Helvetica", 10), bg="white", fg="#1E3A5F"
            )
            self.label_estado.place(relx=0.5, rely=0.9, anchor="center")

            self.mostra_mensagem_info("Pronto para iniciar.")
            self.mainloop()

        except Exception as e:
            stack = traceback.format_exc()
            print(stack)
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro ao iniciar a interface: {str(e)}")
            self.destroy()

    # configurações de estilo (combobox)
    def __configura_estilo_dropdown(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "CustomCombobox.TCombobox",
            foreground="white", background="#1E3A5F",
            fieldbackground="#1E3A5F", arrowcolor="white",
            selectforeground="white", selectbackground="#1E3A5F"
        )
        style.map(
            "CustomCombobox.TCombobox",
            fieldbackground=[('readonly', '#1E3A5F')],
            foreground=[('readonly', 'white')],
            background=[('readonly', '#1E3A5F')],
            arrowcolor=[('active', 'white'), ('!disabled', 'white')]
        )

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
        
    def __on_importar_ficheiro_click(self):
        # Método que informa o Controller que o utilizador clicou no botão "Importar Ficheiro"
        self.importar_ficheiro_click_evt.invoke()
        
    def mostra_dlg_carregar_ficheiro(self):
        # Método que mostra o diálogo para carregar um ficheiro 
        print("View recebeu comando para mostra file selection dlg e obter ficheiro de dados do User")
        path = filedialog.askopenfilename(
        title="Selecionar ficheiro CSV",
        filetypes=[("Ficheiros CSV", "*.csv"), ("Todos os ficheiros", "*.*")]
        )

        if path:
            print(f"Ficheiro selecionado: {path}")
            self.notifica_ficheiro_selecionado(path)
        else:
            print("Nenhum ficheiro foi selecionado.")

    # Método que informa o Controller que o utilizador selecionou um ficheiro com determinado caminho
    def notifica_ficheiro_selecionado(self, fullpath: str):
        self.__ficheiro_selecionado_evt.invoke(fullpath)
        
    def mostra_dlg_grava_grafico(self):
        # chamado pelo controller quando é hora de gravar o gráfico
        # TODO: Penso que a melhor opção é usar um diálogo de tkinter.filedialog
        print("View recebeu comando para gravar gráfico")
    
    
