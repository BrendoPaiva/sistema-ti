import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json

# Nome do arquivo JSON
ARQUIVO_HISTORICO = "historico_computadores.json"

# Lista para armazenar os dados
historico = []

# Funções para manipulação de JSON
def salvar_dados():
    """Salva os dados no arquivo JSON."""
    with open(ARQUIVO_HISTORICO, "w") as arquivo:
        json.dump(historico, arquivo, indent=4)

def carregar_dados():
    """Carrega os dados do arquivo JSON."""
    global historico
    try:
        with open(ARQUIVO_HISTORICO, "r") as arquivo:
            historico = json.load(arquivo)
    except FileNotFoundError:
        historico = []

# Atualiza a tabela com base no filtro ou exibe todos os dados
def atualizar_tabela(filtro=None):
    """Atualiza os dados na tabela."""
    for item in tabela.get_children():
        tabela.delete(item)

    for registro in historico:
        if filtro == "entrada" and registro["data_hora_saida"]:
            continue
        if filtro == "saida" and not registro["data_hora_saida"]:
            continue

        tabela.insert("", tk.END, values=(
            registro["equipamento"],
            registro["responsavel_entrada"],
            registro["data_hora_entrada"],
            registro["destino"] or "-",
            registro["data_hora_saida"] or "-",
            registro["responsavel_saida"] or "-"
        ))

# Registra uma entrada no sistema
def registrar_entrada():
    equipamento = entrada_equipamento.get()
    responsavel = entrada_responsavel.get()

    if not equipamento or not responsavel:
        messagebox.showwarning("Erro", "Preencha todos os campos de entrada.")
        return

    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    registro = {
        "equipamento": equipamento,
        "responsavel_entrada": responsavel,
        "data_hora_entrada": data_hora,
        "destino": None,
        "data_hora_saida": None,
        "responsavel_saida": None
    }
    historico.append(registro)
    salvar_dados()
    atualizar_tabela()
    entrada_equipamento.delete(0, tk.END)
    entrada_responsavel.delete(0, tk.END)
    messagebox.showinfo("Sucesso", "Entrada registrada com sucesso!")

# Registra uma saída no sistema
def registrar_saida():
    equipamento = saida_equipamento.get()
    destino = saida_destino.get()
    responsavel = saida_responsavel.get()

    if not equipamento or not destino or not responsavel:
        messagebox.showwarning("Erro", "Preencha todos os campos de saída.")
        return

    for registro in historico:
        if registro["equipamento"] == equipamento and not registro["data_hora_saida"]:
            registro["destino"] = destino
            registro["data_hora_saida"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            registro["responsavel_saida"] = responsavel
            salvar_dados()
            atualizar_tabela()
            saida_equipamento.delete(0, tk.END)
            saida_destino.delete(0, tk.END)
            saida_responsavel.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Saída registrada com sucesso!")
            return

    messagebox.showwarning("Erro", "Equipamento não encontrado ou já saiu.")

# Pesquisa equipamentos
def pesquisar_equipamento():
    termo = pesquisa_entrada.get().lower()
    filtro = filtro_var.get()

    for item in tabela.get_children():
        tabela.delete(item)

    for registro in historico:
        if filtro == "entrada" and registro["data_hora_saida"]:
            continue
        if filtro == "saida" and not registro["data_hora_saida"]:
            continue
        if termo in registro["equipamento"].lower():
            tabela.insert("", tk.END, values=(
                registro["equipamento"],
                registro["responsavel_entrada"],
                registro["data_hora_entrada"],
                registro["destino"] or "-",
                registro["data_hora_saida"] or "-",
                registro["responsavel_saida"] or "-"
            ))

# Inicialização da interface gráfica
janela = tk.Tk()
janela.title("Gerenciamento de Entrada e Saída de Computadores TI")
janela.state("zoomed")  # Preencher a tela inteira

# Configuração de estilos
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("TLabel", font=("Arial", 12))
estilo.configure("TButton", font=("Arial", 12))
estilo.configure("Treeview", font=("Arial", 10))
estilo.configure("Treeview.Heading", font=("Arial", 12, "bold"))

# Frame para registro de entrada
frame_entrada = ttk.LabelFrame(janela, text="Registrar Entrada", padding=(10, 10))
frame_entrada.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

ttk.Label(frame_entrada, text="Equipamento:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entrada_equipamento = ttk.Entry(frame_entrada, width=30)
entrada_equipamento.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_entrada, text="Responsável:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entrada_responsavel = ttk.Entry(frame_entrada, width=30)
entrada_responsavel.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(frame_entrada, text="Registrar Entrada", command=registrar_entrada).grid(row=2, column=0, columnspan=2, pady=10)

# Frame para registro de saída
frame_saida = ttk.LabelFrame(janela, text="Registrar Saída", padding=(10, 10))
frame_saida.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

ttk.Label(frame_saida, text="Equipamento:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
saida_equipamento = ttk.Entry(frame_saida, width=30)
saida_equipamento.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_saida, text="Destino:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
saida_destino = ttk.Entry(frame_saida, width=30)
saida_destino.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_saida, text="Responsável:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
saida_responsavel = ttk.Entry(frame_saida, width=30)
saida_responsavel.grid(row=2, column=1, padx=5, pady=5)

ttk.Button(frame_saida, text="Registrar Saída", command=registrar_saida).grid(row=3, column=0, columnspan=2, pady=10)

# Frame para pesquisa
frame_pesquisa = ttk.LabelFrame(janela, text="Pesquisar Equipamentos", padding=(10, 10))
frame_pesquisa.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

ttk.Label(frame_pesquisa, text="Pesquisar:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
pesquisa_entrada = ttk.Entry(frame_pesquisa, width=30)
pesquisa_entrada.grid(row=0, column=1, padx=5, pady=5)

filtro_var = tk.StringVar(value="todos")
ttk.Radiobutton(frame_pesquisa, text="Todos", variable=filtro_var, value="todos").grid(row=1, column=0, padx=5, pady=5, sticky="w")
ttk.Radiobutton(frame_pesquisa, text="Entrada", variable=filtro_var, value="entrada").grid(row=1, column=1, padx=5, pady=5, sticky="w")
ttk.Radiobutton(frame_pesquisa, text="Saída", variable=filtro_var, value="saida").grid(row=1, column=2, padx=5, pady=5, sticky="w")

ttk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar_equipamento).grid(row=2, column=0, columnspan=3, pady=10)

# Tabela para exibir o histórico
colunas = ("Equipamento", "Responsável Entrada", "Data/Hora Entrada", "Destino", "Data/Hora Saída", "Responsável Saída")
tabela = ttk.Treeview(janela, columns=colunas, show="headings", height=20)

for col in colunas:
    tabela.heading(col, text=col)
    tabela.column(col, width=150, anchor="center")

tabela.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

scroll = ttk.Scrollbar(janela, orient="vertical", command=tabela.yview)
tabela.configure(yscroll=scroll.set)
scroll.grid(row=2, column=2, sticky="ns")

# Carrega os dados salvos
carregar_dados()
atualizar_tabela()

# Inicia o programa
janela.mainloop()
