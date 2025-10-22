#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema Administrativo - Projeto N2 Etapa 1
Baseado nas diretrizes do documento PDF e interface JPG
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime

class SistemaAdministrativo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema Administrativo - N2")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Dados do sistema (simulando banco de dados)
        self.dados = {
            'usuarios': [],
            'produtos': [],
            'vendas': [],
            'relatorios': []
        }
        
        self.carregar_dados()
        self.criar_interface()
    
    def carregar_dados(self):
        """Carrega dados do arquivo JSON (simulando banco de dados)"""
        try:
            if os.path.exists('dados_sistema.json'):
                with open('dados_sistema.json', 'r', encoding='utf-8') as f:
                    self.dados = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
    
    def salvar_dados(self):
        """Salva dados no arquivo JSON"""
        try:
            with open('dados_sistema.json', 'w', encoding='utf-8') as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def criar_interface(self):
        """Cria a interface principal do sistema"""
        # Menu principal
        self.criar_menu()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Sistema Administrativo", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Botões principais
        self.criar_botoes_principais(main_frame)
        
        # Área de conteúdo
        self.criar_area_conteudo(main_frame)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Sistema pronto")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def criar_menu(self):
        """Cria o menu superior"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Novo", command=self.novo_arquivo)
        arquivo_menu.add_command(label="Abrir", command=self.abrir_arquivo)
        arquivo_menu.add_command(label="Salvar", command=self.salvar_arquivo)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Editar
        editar_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Editar", menu=editar_menu)
        editar_menu.add_command(label="Usuários", command=self.gerenciar_usuarios)
        editar_menu.add_command(label="Produtos", command=self.gerenciar_produtos)
        
        # Menu Relatórios
        relatorios_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Relatórios", menu=relatorios_menu)
        relatorios_menu.add_command(label="Vendas", command=self.relatorio_vendas)
        relatorios_menu.add_command(label="Usuários", command=self.relatorio_usuarios)
        
        # Menu Ajuda
        ajuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=ajuda_menu)
        ajuda_menu.add_command(label="Sobre", command=self.sobre)
    
    def criar_botoes_principais(self, parent):
        """Cria os botões principais da interface"""
        botoes_frame = ttk.Frame(parent)
        botoes_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Botões
        botoes = [
            ("Gerenciar Usuários", self.gerenciar_usuarios, '#4CAF50'),
            ("Gerenciar Produtos", self.gerenciar_produtos, '#2196F3'),
            ("Registrar Venda", self.registrar_venda, '#FF9800'),
            ("Relatórios", self.mostrar_relatorios, '#9C27B0'),
            ("Configurações", self.configuracoes, '#607D8B')
        ]
        
        for i, (texto, comando, cor) in enumerate(botoes):
            btn = tk.Button(botoes_frame, text=texto, command=comando,
                           bg=cor, fg='white', font=('Arial', 10, 'bold'),
                           width=15, height=2)
            btn.grid(row=0, column=i, padx=5)
    
    def criar_area_conteudo(self, parent):
        """Cria a área de conteúdo principal"""
        self.conteudo_frame = ttk.Frame(parent)
        self.conteudo_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.conteudo_frame.columnconfigure(0, weight=1)
        self.conteudo_frame.rowconfigure(0, weight=1)
        
        # Conteúdo inicial
        self.mostrar_dashboard()
    
    def mostrar_dashboard(self):
        """Mostra o dashboard principal"""
        # Limpa o conteúdo anterior
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()
        
        # Título do dashboard
        titulo = ttk.Label(self.conteudo_frame, text="Dashboard", 
                          font=('Arial', 14, 'bold'))
        titulo.grid(row=0, column=0, pady=(0, 20))
        
        # Estatísticas
        stats_frame = ttk.Frame(self.conteudo_frame)
        stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        stats = [
            ("Total de Usuários", len(self.dados['usuarios'])),
            ("Total de Produtos", len(self.dados['produtos'])),
            ("Total de Vendas", len(self.dados['vendas'])),
            ("Data/Hora", datetime.now().strftime("%d/%m/%Y %H:%M"))
        ]
        
        for i, (label, valor) in enumerate(stats):
            stat_frame = ttk.LabelFrame(stats_frame, text=label)
            stat_frame.grid(row=0, column=i, padx=10, sticky=(tk.W, tk.E))
            
            valor_label = ttk.Label(stat_frame, text=str(valor), 
                                   font=('Arial', 16, 'bold'))
            valor_label.pack(pady=10)
    
    def gerenciar_usuarios(self):
        """Interface para gerenciar usuários"""
        self.status_var.set("Gerenciando usuários...")
        # Implementar interface de usuários
        messagebox.showinfo("Info", "Funcionalidade de usuários em desenvolvimento")
    
    def gerenciar_produtos(self):
        """Interface para gerenciar produtos"""
        self.status_var.set("Gerenciando produtos...")
        # Implementar interface de produtos
        messagebox.showinfo("Info", "Funcionalidade de produtos em desenvolvimento")
    
    def registrar_venda(self):
        """Interface para registrar vendas"""
        self.status_var.set("Registrando venda...")
        # Implementar interface de vendas
        messagebox.showinfo("Info", "Funcionalidade de vendas em desenvolvimento")
    
    def mostrar_relatorios(self):
        """Mostra relatórios do sistema"""
        self.status_var.set("Gerando relatórios...")
        # Implementar relatórios
        messagebox.showinfo("Info", "Funcionalidade de relatórios em desenvolvimento")
    
    def configuracoes(self):
        """Interface de configurações"""
        self.status_var.set("Abrindo configurações...")
        # Implementar configurações
        messagebox.showinfo("Info", "Funcionalidade de configurações em desenvolvimento")
    
    def novo_arquivo(self):
        """Cria novo arquivo"""
        self.status_var.set("Criando novo arquivo...")
        messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")
    
    def abrir_arquivo(self):
        """Abre arquivo"""
        self.status_var.set("Abrindo arquivo...")
        messagebox.showinfo("Info", "Funcionalidade em desenvolvimento")
    
    def salvar_arquivo(self):
        """Salva arquivo"""
        self.salvar_dados()
        self.status_var.set("Arquivo salvo com sucesso!")
        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
    
    def relatorio_vendas(self):
        """Gera relatório de vendas"""
        self.status_var.set("Gerando relatório de vendas...")
        messagebox.showinfo("Info", "Relatório de vendas em desenvolvimento")
    
    def relatorio_usuarios(self):
        """Gera relatório de usuários"""
        self.status_var.set("Gerando relatório de usuários...")
        messagebox.showinfo("Info", "Relatório de usuários em desenvolvimento")
    
    def sobre(self):
        """Mostra informações sobre o sistema"""
        sobre_texto = """
Sistema Administrativo - N2 Etapa 1

Desenvolvido em Python com Tkinter
Baseado nas diretrizes do documento PDF

Funcionalidades:
- Gerenciamento de usuários
- Gerenciamento de produtos
- Registro de vendas
- Relatórios
- Configurações

Versão: 1.0
        """
        messagebox.showinfo("Sobre o Sistema", sobre_texto)
    
    def executar(self):
        """Executa o sistema"""
        self.root.mainloop()

def main():
    """Função principal"""
    try:
        app = SistemaAdministrativo()
        app.executar()
    except Exception as e:
        print(f"Erro ao executar o sistema: {e}")
        messagebox.showerror("Erro", f"Erro ao executar o sistema: {e}")

if __name__ == "__main__":
    main()

