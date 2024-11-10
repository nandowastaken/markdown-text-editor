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
        self.dark_mode = False  # Estado inicial do modo (Light Mode)

        # Configurar layout de grade para a janela principal
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Dividir a tela com áreas para Markdown e HTML
        self.create_widgets()
        self.apply_theme()

    def toggle_dark_mode(self):
        # Alterna entre o modo claro e escuro
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.render_markdown()
    
    def apply_theme(self):
        # Define as cores para os temas claro e escuro
        if self.dark_mode:
            bg_color = "#2e2e2e"
            fg_color = "#ffffff"
            editor_bg = "#1e1e1e"
            viewer_bg = "#1e1e1e"
            button_bg = "#444444"
            button_fg = "#ffffff"
            self.title("Markdown Editor - Dark Mode")
        else:
            bg_color = "#f0f0f0"
            fg_color = "#000000"
            editor_bg = "#ffffff"
            viewer_bg = "#ffffff"
            button_bg = "#e0e0e0"
            button_fg = "#ffffff"
            self.title("Markdown Editor - Light Mode")
        
        # Aplicar as cores nos componentes
        self.configure(bg=bg_color)
        self.markdown_text.configure(bg=editor_bg, fg=fg_color, insertbackground=fg_color)
        self.html_view.configure(bg=viewer_bg, fg=fg_color)
        self.frame.configure(bg=bg_color)
        self.clear_button.configure(style="Custom.TButton")
        self.save_button.configure(style="Custom.TButton")
        self.open_button.configure(style="Custom.TButton")
        self.create_button.configure(style="Custom.TButton")
        self.toggle_button.configure(style="Custom.TButton")
        
        # Configuração do estilo dos botões
        style = ttk.Style()
        style.configure("Custom.TButton",
                    background=button_bg,
                    foreground=button_fg,
                    relief="flat",
                    padding=0,
                    borderWidth=0)
    
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
        self.frame.grid(row=0, column=0, sticky="nsew")

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
        
        # Botão para alternar o modo escuro
        self.toggle_button = ttk.Button(self.frame, text="Dark Mode", command=self.toggle_dark_mode)
        self.toggle_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # Vincular o evento de atualização automática ao campo de texto Markdown
        self.markdown_text.bind("<KeyRelease>", lambda event: self.render_markdown())

    def render_markdown(self):
        # Obter o texto do editor Markdown
        markdown_content = self.markdown_text.get("1.0", tk.END)
        
        # Renderizar o Markdown em HTML com estilos CSS básicos
        html_content = markdown.markdown(markdown_content) 
        if self.dark_mode:
            html_content = f"""
            <div style="color: white; background-color: #1e1e1e;">
                {html_content}
            </div>
            """
        else:
            html_content = f"""
            <div style="color: black; background-color: #ffffff;">
                {html_content}
            </div>
            """

        # html_content = markdown.markdown(markdown_content)        
        # Mostrar o HTML na área de visualização
        self.html_view.set_html(html_content)

    def clear_text(self):
        # Limpar o conteúdo do editor de Markdown
        self.markdown_text.delete("1.0", tk.END)
        self.render_markdown()
