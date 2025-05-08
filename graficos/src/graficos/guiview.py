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
