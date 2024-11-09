import tkinter as tk
from tkinter import ttk
import markdown
from tkinter import scrolledtext
from tkhtmlview import HTMLLabel

class MarkdownEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela principal
        self.title("Markdown Editor")
        self.geometry("1280x600")
        self.resizable(False, True)
        
        # Dividir a tela com áreas para Markdown e HTML
        self.create_widgets()

    def create_widgets(self):
        # Editor de Markdown (entrada)
        self.markdown_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, font=("Arial", 12))
        self.markdown_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Visualizador de HTML (saída) usando HTMLLabel
        self.html_view = HTMLLabel(self, wrap=tk.WORD, font=("Arial", 12))
        self.html_view.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Desabilitar interações de clique no HTMLLabel
        self.html_view.bind("<1>", lambda e: "break")

        # Botão de atualizar
        #self.update_button = ttk.Button(self, text="Renderizar Markdown", command=self.render_markdown)
        #self.update_button.pack(side=tk.BOTTOM, pady=10)

        # Vincular o evento de atualização automática ao campo de texto Markdown
        self.markdown_text.bind("<KeyRelease>", lambda event: self.render_markdown())

    def render_markdown(self):
        # Obter o texto do editor Markdown
        markdown_content = self.markdown_text.get("1.0", tk.END)
        
        # Renderizar o Markdown em HTML
        html_content = markdown.markdown(markdown_content)
        
        # Mostrar o HTML na área de visualização
        self.html_view.set_html(html_content)

if __name__ == "__main__":
    app = MarkdownEditor()
    app.mainloop()
