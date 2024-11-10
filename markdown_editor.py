import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkhtmlview import HTMLLabel
import markdown
from file_utils import open_file, save_file, create_file

class MarkdownEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela principal
        self.title("Markdown Editor")
        self.geometry("1280x600")
        self.resizable(True, True)
        
        # Variável para armazenar o caminho do arquivo aberto
        self.current_file_path = None
        
        # Configurar layout de grade para a janela principal
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Dividir a tela com áreas para Markdown e HTML
        self.create_widgets()
    
    def open_file(self):
        self.current_file_path = open_file(self.markdown_text)
        if self.current_file_path:
            self.title(f"Arquivo Aberto: {self.current_file_path}")
            self.render_markdown()
    
    def save_file(self):
        if not self.current_file_path:
            self.current_file_path = create_file(self.markdown_text)
        else:
            save_file(self.current_file_path, self.markdown_text)
        
        if self.current_file_path:
            self.title(f"Arquivo Salvo: {self.current_file_path}")
    
    def create_widgets(self):
        # Editor de Markdown (entrada)
        self.markdown_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Arial", 12))
        self.markdown_text.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Visualizador de HTML (saída) usando HTMLLabel
        self.html_view = HTMLLabel(self, wrap=tk.WORD)
        self.html_view.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        
        # Desabilitar interações de clique no HTMLLabel
        self.html_view.bind("<1>", lambda e: "break")

        # Frame para widgets
        self.frame = tk.Frame(self, relief=tk.RAISED, bd=2)
        self.frame.grid(row=0, column=0)

        # Botão para limpar texto
        self.clear_button = ttk.Button(self, text="Limpar Markdown", command=self.clear_text)
        self.clear_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Botão para Salvar
        self.save_button = ttk.Button(self.frame, text="Salvar", command=self.save_file)
        self.save_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Botão para Abrir um arquivo
        self.open_button = ttk.Button(self.frame, text="Abrir", command=self.open_file)
        self.open_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        # Botão para Criar novo arquivo
        self.create_button = ttk.Button(self.frame, text="Criar", command=lambda: self.create_file())
        self.create_button.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        # Vincular o evento de atualização automática ao campo de texto Markdown
        self.markdown_text.bind("<KeyRelease>", lambda event: self.render_markdown())

    def render_markdown(self):
        # Obter o texto do editor Markdown
        markdown_content = self.markdown_text.get("1.0", tk.END)
        
        # Renderizar o Markdown em HTML com estilos CSS básicos
        html_content = markdown.markdown(markdown_content)        
        # Mostrar o HTML na área de visualização
        self.html_view.set_html(html_content)

    def clear_text(self):
        # Limpar o conteúdo do editor de Markdown
        self.markdown_text.delete("1.0", tk.END)
        self.render_markdown()
