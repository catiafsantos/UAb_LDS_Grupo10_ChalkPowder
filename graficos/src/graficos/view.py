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
        # Inicia a interface gráfica
        print("Iniciando a interface gráfica...")    # No futuro deve ser removido
        self.title("Conversor .csv para Gráfico")
        self.geometry("500x300")      # Tamanho da janela
        self.configure(bg="#1E3A5F")  # Fundo azul escuro

        self.frames = {}

        # Frame externo com fundo azul escuro
        outer_frame = tk.Frame(self, bg="#1E3A5F")
        outer_frame.pack(expand=True, fill=tk.BOTH)

        # Frame interno com fundo branco
        container = tk.Frame(outer_frame, bg="White", bd=1, relief="solid")
        container.place(relx=0.5, rely=0.5, anchor="center", width=485, height=285)

        # Permitir expansão dos frames internos
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
    
        # Botão "Importar Ficheiro"
        btn_importar = tk.Button(
            container,
            text="Importar Ficheiro",
            command=self.__on_importar_ficheiro_click,
            font=("Helvetica", 12),
            bg="#1E3A5F",       # Azul escuro
            fg="white",         # Texto branco
            activebackground="#27496d",  # Tom mais claro ao clicar
            activeforeground="white",
            relief="raised",      # Tipo de bordas
            padx=10,
            pady=5
        )
        btn_importar.place(relx=0.5, rely=0.5, anchor="center")

        # Apenas para sabermos o que está a acontecer, no futuro podemos remover
        print("Interface gráfica pronta.")
        self.mainloop()

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
    
    
