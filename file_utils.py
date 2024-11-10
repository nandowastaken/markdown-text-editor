from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file(text_widget):
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])

    if not filepath:
        return None

    with open(filepath, "r") as f:
        content = f.read()
        text_widget.delete(1.0, "end")
        text_widget.insert("end", content)

    return filepath

def save_file(filepath, text_widget):
    with open(filepath, "w") as f:
        content = text_widget.get(1.0, "end")
        f.write(content)

def create_file(text_widget):
    filepath = asksaveasfilename(defaultextension="txt", filetypes=[("Text Files", "*.txt")])

    if not filepath:
        return None
    
    with open(filepath, "w") as f:
        content = text_widget.get(1.0, "end")
        f.write(content)

    return filepath
