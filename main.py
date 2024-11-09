import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import markdown
from tkinter import scrolledtext
from tkhtmlview import HTMLLabel

class MarkdownEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela principal
        self.title("Markdown Editor")
        self.geometry("1280x600")
        self.resizable(True, True)
        
        # Configurar layout de grade para a janela principal
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Dividir a tela com áreas para Markdown e HTML
        self.create_widgets()
    
    def open_file(self):
        filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])

        if not filepath:
            return
        
        self.markdown_text.delete(1.0, tk.END)

        with open(filepath, "r") as f:
            content = f.read()
            self.markdown_text.insert(tk.END, content)

        self.title(f"Arquivo Aberto: {filepath}")
    
    def save_file(self):
        filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])

        if not filepath:
            return
        
        with open(filepath, "w") as f:
            content = self.markdown_text.get(1.0, tk.END)
            f.write(content)
        
        self.title(f"Arquivo Aberto: {filepath}")
        
    
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

        # Botão para limpar texto, centralizado abaixo das áreas de texto
        self.clear_button = ttk.Button(self, text="Limpar Markdown", command=self.clear_text)
        self.clear_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Botão para Salvar
        self.save_button = ttk.Button(self.frame, text="Salvar", command=lambda: self.save_file())
        self.save_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Botão para Abrir um arquivo
        self.open_button = ttk.Button(self.frame, text="Abrir", command=lambda: self.open_file())
        self.open_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

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

if __name__ == "__main__":
    app = MarkdownEditor()
    app.mainloop()
