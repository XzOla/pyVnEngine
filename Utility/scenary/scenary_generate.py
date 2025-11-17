import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class VNTextGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("VN Text Generator")

        # Frame for inputs
        frm = ttk.Frame(root, padding=10)
        frm.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frm, text="ID реплики:").grid(row=0, column=0, sticky="w")
        self.entry_id = ttk.Entry(frm, width=10)
        self.entry_id.grid(row=0, column=1, sticky="w")

        ttk.Label(frm, text="Имя спикера (None — пусто):").grid(row=1, column=0, sticky="w")
        self.entry_speaker = ttk.Entry(frm, width=20)
        self.entry_speaker.grid(row=1, column=1, sticky="w")

        ttk.Label(frm, text="Текст реплики:").grid(row=2, column=0, sticky="nw")
        self.text_box = scrolledtext.ScrolledText(frm, width=60, height=15)
        self.text_box.grid(row=2, column=1, sticky="w")

        self.btn_add = ttk.Button(frm, text="Добавить во внутренний словарь", command=self.add_entry)
        self.btn_add.grid(row=3, column=1, sticky="e", pady=6)

        # Output
        ttk.Label(frm, text="Сгенерированный код:").grid(row=4, column=0, sticky="nw", pady=4)
        self.output_box = scrolledtext.ScrolledText(frm, width=80, height=20)
        self.output_box.grid(row=4, column=1, sticky="w")

        self.entries = {}

    def add_entry(self):
        try:
            idx = int(self.entry_id.get())
        except ValueError:
            messagebox.showerror("Ошибка", "ID должен быть числом")
            return

        sp = self.entry_speaker.get().strip()
        if sp == "" or sp.lower() == "none":
            sp_val = None
        else:
            sp_val = sp

        text_val = self.text_box.get("1.0", tk.END).rstrip()
        if not text_val:
            messagebox.showerror("Ошибка", "Текст пустой")
            return

        self.entries[idx] = {"speaker": sp_val, "text": text_val}

        self.generate_output()
        self.entry_id.delete(0, tk.END)
        self.text_box.delete("1.0", tk.END)

    def generate_output(self):
        lines = []
        lines.append("# --- Словарь текстов ---")
        lines.append("TEXTS = {")
        for k in sorted(self.entries.keys()):
            e = self.entries[k]
            sp = "None" if e["speaker"] is None else f'\"{e["speaker"]}\"'
            t = e["text"].replace("\\", "\\\\").replace("\"", "\\\"")
            t = t.replace("\n", "\\n")
            line = f"    {k}: {{\"speaker\": {sp}, \"text\": \"{t}\"}},"
            lines.append(line)
        lines.append("}")

        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, "\n".join(lines))


if __name__ == "__main__":
    root = tk.Tk()
    app = VNTextGUI(root)
    root.mainloop()
