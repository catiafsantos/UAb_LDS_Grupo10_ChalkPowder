import traceback
import tkinter as tk
from tkinter import messagebox, filedialog, ttk

import matplotlib.pyplot as plt

# configurações de estilo (combobox)
def configurar_estilo_dropdown():
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

# Interface Principal (tkinter). Funciona com o método ativar_interface no ficheiro view.py.
def construir_interface_principal(root, grafico_var, estado_var, on_importar_ficheiro_click, on_grafico_selecionado, on_home_click):
    try:
        root.title("Conversor .csv para Gráfico")
        root.geometry("500x300")
        root.configure(bg="#1E3A5F")

        # Frame principal
        outer_frame = tk.Frame(root, bg="#1E3A5F")
        outer_frame.pack(expand=True, fill=tk.BOTH)

        # Container central
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
        btn_importar = tk.Button(
            container, text="Importar Ficheiro", command=on_importar_ficheiro_click,
            font=("Helvetica", 12), bg="#1E3A5F", fg="white", activebackground="#27496d",
            activeforeground="white", relief="raised", padx=10, pady=5, cursor="hand2"
        )
        btn_importar.place(relx=0.5, rely=0.4, anchor="center")

        # Dropdown escondido
        configurar_estilo_dropdown()
        dropdown_menu = ttk.Combobox(
            container, textvariable=grafico_var, state="readonly",
            font=("Helvetica", 11), width=30, style="CustomCombobox.TCombobox"
        )
        dropdown_menu.place_forget()
        grafico_var.trace_add("write", on_grafico_selecionado)

        # Label estado
        label_estado = tk.Label(
            container, textvariable=estado_var,
            font=("Helvetica", 10), bg="white", fg="#1E3A5F"
        )
        label_estado.place(relx=0.5, rely=0.9, anchor="center")

        # Frame do botão personalizado
        btn_home_frame = tk.Frame(container, bg="white", cursor="hand2")
        btn_home_frame.place(relx=0.05, rely=0.05, anchor="nw")

        # Ícone (casa grande)
        label_icone = tk.Label(
            btn_home_frame, text="🏠", font=("Helvetica", 14, "bold"),
            bg="white", fg="#1E3A5F"
        )
        label_icone.pack(side=tk.LEFT)

        # Texto "Início" pequeno
        label_texto = tk.Label(
            btn_home_frame, text="Início", font=("Helvetica", 9),
            bg="white", fg="#1E3A5F"
        )
        label_texto.pack(side=tk.LEFT, padx=(2, 0))

        # Função de clique comum aos dois elementos
        def clique_home(_=None):
            on_home_click()

        # Associa o clique a todo o frame e labels
        btn_home_frame.bind("<Button-1>", clique_home)
        label_icone.bind("<Button-1>", clique_home)
        label_texto.bind("<Button-1>", clique_home)

        return {
            "btn_importar": btn_importar,
            "dropdown_menu": dropdown_menu,
            "label_estado": label_estado,
            "btn_home_frame": btn_home_frame,
            "btn_home_icon": label_icone,
            "btn_home_text": label_texto
        }

    except Exception as e:
        stack = traceback.format_exc()
        print(stack)
        messagebox.showerror("Erro Crítico", f"Ocorreu um erro ao iniciar a interface: {str(e)}")
        root.destroy()
        return None

# Método que constrói o formulário de parâmetros (tkinter). Funciona com o método mostra_formulario_parametros no ficheiro view.py.
def construir_formulario_parametros(
    parent: tk.Tk,
    colunas: list[str],
    x_var: tk.StringVar,
    y_var: tk.StringVar,
    x_label_var: tk.StringVar,
    y_label_var: tk.StringVar,
    opcao_labels: tk.StringVar,
    on_submeter_parametros
) -> tk.Frame:
    
    #Frame do formulário
    form_frame = tk.Frame(parent, bg="white")
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Funções de atualização do dropdown
    def atualizar_dropdown_y(_=None):
        coluna_x = x_var.get()
        novas_opcoes_y = [col for col in colunas if col != coluna_x]
        dropdown_y['values'] = novas_opcoes_y
        if y_var.get() == coluna_x:
            y_var.set("Escolher coluna Y")

    def atualizar_dropdown_x(_=None):
        coluna_y = y_var.get()
        novas_opcoes_x = [col for col in colunas if col != coluna_y]
        dropdown_x['values'] = novas_opcoes_x
        if x_var.get() == coluna_y:
            x_var.set("Escolher coluna X")

    # Método que atualiza a visibilidade dos labels
    def atualizar_visibilidade_labels():
        if opcao_labels.get() == "personalizar":
            # Mostrar caixas de texto personalizadas
            label_x_entry.grid(row=2, column=0, sticky="e", padx=(10, 5), pady=5)
            entry_x_label.grid(row=2, column=1, sticky="w", padx=(5, 10), pady=5)

            label_y_entry.grid(row=3, column=0, sticky="e", padx=(10, 5), pady=5)
            entry_y_label.grid(row=3, column=1, sticky="w", padx=(5, 10), pady=5)

            dropdown_x.grid_remove()
            dropdown_y.grid_remove()
        else:
            # Mostrar dropdowns de colunas
            dropdown_x.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
            dropdown_y.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

            label_x_entry.grid_remove()
            label_y_entry.grid_remove()
            entry_x_label.grid_remove()
            entry_y_label.grid_remove()

    # Opções de labels
    tk.Radiobutton(
        form_frame, text="Usar nomes das colunas como rótulos dos eixos",
        variable=opcao_labels, value="usar_colunas",
        command=atualizar_visibilidade_labels, bg="white"
    ).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")

    tk.Radiobutton(
        form_frame, text="Personalizar nomes dos eixos",
        variable=opcao_labels, value="personalizar",
        command=atualizar_visibilidade_labels, bg="white"
    ).grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky="w")

    # Dropdowns para escolha de colunas
    dropdown_x = ttk.Combobox(form_frame, textvariable=x_var, values=colunas, state="readonly", width=30)
    dropdown_y = ttk.Combobox(form_frame, textvariable=y_var, values=colunas, state="readonly", width=30)
    dropdown_x.grid(row=2, column=0, columnspan=2, pady=5)
    dropdown_y.grid(row=3, column=0, columnspan=2, pady=5)

    dropdown_x.bind("<<ComboboxSelected>>", atualizar_dropdown_y)
    dropdown_y.bind("<<ComboboxSelected>>", atualizar_dropdown_x)

    # Entradas de texto para personalizar labels
    style = ttk.Style()
    style.configure("Custom.TEntry", foreground="#1E3A5F", font=("Helvetica", 11),
                    padding=10, relief="solid", borderwidth=1, background="white")

    entry_x_label = ttk.Entry(form_frame, textvariable=x_label_var, style="Custom.TEntry", width=30)
    entry_y_label = ttk.Entry(form_frame, textvariable=y_label_var, style="Custom.TEntry", width=30)

    label_x_entry = tk.Label(form_frame, text="Eixo X", bg="white", font=("Helvetica", 10))
    label_y_entry = tk.Label(form_frame, text="Eixo Y", bg="white", font=("Helvetica", 10))

    # Botão Submeter
    tk.Button(
        form_frame, text="Submeter", command=on_submeter_parametros,
        font=("Helvetica", 11), bg="#1E3A5F", fg="white"
    ).grid(row=5, column=0, columnspan=2, pady=20)

    # Inicializa visibilidade correta
    atualizar_visibilidade_labels()

    return form_frame

# Método que obtém os parâmetros do formulário (tkinter). Funciona com o método __on_submeter_parametros no ficheiro view.py.
def obter_parametros_formulario(x_var, y_var, x_label_var, y_label_var, opcao_labels):
    if opcao_labels.get() == "usar_colunas":
        x_col, y_col = x_var.get(), y_var.get()
        if x_col == "Escolher coluna X" or y_col == "Escolher coluna Y":
            return None, None, None, None, "Tem de selecionar colunas para os eixos."
        return x_col, y_col, x_col, y_col, None
    else:
        x_label, y_label = x_label_var.get().strip(), y_label_var.get().strip()
        if not x_label or not y_label:
            return None, None, None, None, "Tem de preencher os nomes dos eixos."
        return None, None, x_label, y_label, None

# Método que mostra o diálogo para carregar um ficheiro (Tkinter). Funciona com o método mostra_dlg_carregar_ficheiro no ficheiro view.py
def carregar_ficheiro_csv_com_dialogo(btn_importar, mostra_mensagem_info, mostra_erro_importacao):
    mostra_mensagem_info("A iniciar importação de ficheiro...")
    btn_importar.config(state="disabled", text="A carregar...", cursor="watch")
    btn_importar.update_idletasks() # Atualiza o GUI imediatamente

    try:
        path = filedialog.askopenfilename(
            title="Selecionar ficheiro CSV",
            filetypes=[("Ficheiros CSV", "*.csv"), ("Todos os ficheiros", "*.*")]
        )
        if not path:
            mostra_mensagem_info("Importação cancelada pelo utilizador.")
            return None
        return path
    except Exception as e:
        stack = traceback.format_exc()
        print(stack)
        mostra_mensagem_info("Erro ao selecionar ficheiro.")
        mostra_erro_importacao(f"Ocorreu um erro ao selecionar o ficheiro: {str(e)}")
        return None
    finally:
        btn_importar.config(state="normal", text="Importar Ficheiro", cursor="hand2")

# Método que mostra ao utilizador as opções de gravação do ficheiro (tkinter). Funciona com o método mostra_dlg_grava_grafico no ficheiro view.py.
def guardar_grafico_com_dialogo(callback_gravar, mostrar_info, voltar_menu):
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
        callback_gravar(path)
        messagebox.showinfo("Sucesso", f"Gráfico guardado em:\n{path}")
        voltar_menu()
    else:
        mostrar_info("Operação de gravação cancelada.")

# Método para mostrar gráfico (tkinter). Funciona com o método mostrar_grafico(self)
def preparar_interface_grafico(view, on_guardar_click):
    # Esconde todos os elementos anteriores da interface
    if hasattr(view, "form_frame") and view.form_frame.winfo_exists():
        view.form_frame.destroy()
    if hasattr(view, "dropdown_menu") and view.dropdown_menu.winfo_exists():
        view.dropdown_menu.place_forget()
    if hasattr(view, "btn_importar") and view.btn_importar.winfo_exists():
        view.btn_importar.place_forget()

    # Frame para botão de guardar
    view.botao_frame = tk.Frame(view, bg="white")
    view.botao_frame.place(relx=0.5, rely=0.5, anchor="center")

    view.btn_guardar_grafico = tk.Button(
        view.botao_frame, text="Guardar Gráfico",
        command=on_guardar_click,
        font=("Helvetica", 11), bg="#1E3A5F", fg="white"
    )
    view.btn_guardar_grafico.pack(pady=10)

    view.mostra_mensagem_info("Gráfico gerado.")
    # Mostra o gráfico
    plt.show()
