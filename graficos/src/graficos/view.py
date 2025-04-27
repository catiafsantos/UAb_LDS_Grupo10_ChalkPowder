# Este código no futuro vai ter de ser dividido em ficheiros mais pequenos.
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

        if self.opcao_labels.get() == "usar_colunas":
            x_col, y_col = self.x_var.get(), self.y_var.get()
            if x_col == "Escolher coluna X" or y_col == "Escolher coluna Y":
                self.mostra_erro_ficheiro("Tem de selecionar colunas para os eixos.")
                self.mostra_mensagem_info("Faltam selecionar colunas.")
                return
            x_label, y_label = x_col, y_col
        else:
            x_col, y_col = None, None
            x_label, y_label = self.x_label_var.get().strip(), self.y_label_var.get().strip()
            if not x_label or not y_label:
                self.mostra_erro_ficheiro("Tem de preencher os nomes dos eixos.")
                self.mostra_mensagem_info("Faltam nomes personalizados.")
                return
                
        self.mostra_mensagem_info("Parâmetros corretos. A gerar gráfico...")
        self.__submissao_parametros_evt.invoke(x_col, y_col, x_label, y_label)

    # Dialogs
    def mostra_dlg_carregar_ficheiro(self):
        # Método que mostra o diálogo para carregar um ficheiro 
        self.mostra_mensagem_info("A iniciar importação de ficheiro...")
        self.btn_importar.config(state="disabled", text="A carregar...", cursor="watch")
        self.update_idletasks()  # Atualiza o GUI imediatamente

        try:
            path = filedialog.askopenfilename(
                title="Selecionar ficheiro CSV",
                filetypes=[("Ficheiros CSV", "*.csv"), ("Todos os ficheiros", "*.*")]
            )
            if path:
                self.notifica_ficheiro_selecionado(path)
            else:
                self.mostra_mensagem_info("Importação cancelada pelo utilizador.")
        except Exception as e:
            stack = traceback.format_exc()
            print(stack)
            self.mostra_mensagem_info("Erro ao selecionar ficheiro.")
            self.mostra_erro_importacao(f"Ocorreu um erro ao selecionar o ficheiro: {str(e)}")
        finally:
            self.btn_importar.config(state="normal", text="Importar Ficheiro", cursor="hand2")

    # Método que mostra ao utilizador as opções de gravação do ficheiro
    def mostra_dlg_grava_grafico(self):
        path = filedialog.asksaveasfilename(
            title="Guardar Gráfico Como",
            defaultextension=".png",
            filetypes=[
                ("Imagem PNG", "*.png"),
                ("Imagem JPEG", "*.jpg"),
                ("Imagem SVG", "*.svg"),
                ("Documento PDF", "*.pdf"),
            ]
        )
        if path:
            self.__grava_grafico_click_evt.invoke(path)
            messagebox.showinfo("Sucesso", f"Gráfico guardado em:\n{path}")
            self.voltar_menu_inicial()
        else:
            self.mostra_mensagem_info("Operação de gravação cancelada.")
        
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
