import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import os
import json
from generator import NameGenerator

class NameGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Name Generator")
        self.root.geometry("550x700")
        self.root.resizable(False, False)

        self.generator = NameGenerator()
        self.history = []
        
        # 變數定義
        self.use_adj_var = tk.BooleanVar(value=True)
        self.category_vars = {}
        self.result_var = tk.StringVar(value="Click Generate!")
        self.exclusion_var = tk.StringVar()

        # 載入排除清單
        self.exclusion_var.set(", ".join(self.generator.persistent_exclusions))

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 標題
        ttk.Label(main_frame, text="Name Generator", font=("Helvetica", 18, "bold")).pack(pady=(0, 20))

        # 設定區
        settings_frame = ttk.LabelFrame(main_frame, text=" Settings ", padding="10")
        settings_frame.pack(fill=tk.X, pady=5)

        ttk.Checkbutton(settings_frame, text="Use Adjectives", variable=self.use_adj_var).pack(anchor=tk.W)

        # 類別 (三欄式佈局)
        cat_header = ttk.Frame(settings_frame)
        cat_header.pack(fill=tk.X, pady=(10, 2))
        ttk.Label(cat_header, text="Noun Categories:").pack(side=tk.LEFT)
        ttk.Button(cat_header, text="None", width=5, command=self.select_none).pack(side=tk.RIGHT, padx=2)
        ttk.Button(cat_header, text="All", width=5, command=self.select_all).pack(side=tk.RIGHT, padx=2)
        
        cat_container = ttk.Frame(settings_frame)
        cat_container.pack(fill=tk.X, pady=5)

        categories = self.generator.get_categories()
        for i, cat in enumerate(categories):
            var = tk.BooleanVar(value=True)
            self.category_vars[cat] = var
            display_name = cat.replace('_', ' ').capitalize()
            cb = ttk.Checkbutton(cat_container, text=display_name, variable=var)
            cb.grid(row=i//3, column=i%3, sticky=tk.W, padx=5, pady=2)

        # 排除清單
        excl_frame = ttk.Frame(settings_frame)
        excl_frame.pack(fill=tk.X, pady=(15, 2))
        ttk.Label(excl_frame, text="Exclusion List:").pack(side=tk.LEFT)
        ttk.Button(excl_frame, text="Save to File", width=12, command=self.save_exclusions).pack(side=tk.RIGHT)
        
        ttk.Entry(settings_frame, textvariable=self.exclusion_var).pack(fill=tk.X, pady=2)
        ttk.Label(settings_frame, text="(Comma separated)", font=("Helvetica", 8, "italic")).pack(anchor=tk.W)

        # 結果區
        result_frame = ttk.Frame(main_frame, padding="15")
        result_frame.pack(fill=tk.X)
        tk.Label(result_frame, textvariable=self.result_var, font=("Consolas", 22, "bold"), fg="#2c3e50", wraplength=450).pack()

        # 按鈕區
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Generate", command=self.on_generate, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Copy Result", command=self.on_copy, width=15).grid(row=0, column=1, padx=5)

        # 歷史記錄區
        history_frame = ttk.LabelFrame(main_frame, text=" History (Last 5) ", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.history_listbox = tk.Listbox(history_frame, height=5, font=("Consolas", 10))
        self.history_listbox.pack(fill=tk.BOTH, expand=True)
        self.history_listbox.bind('<Double-Button-1>', lambda e: self.copy_history())

        ttk.Label(main_frame, text="Double-click history to copy", font=("Helvetica", 8)).pack(side=tk.BOTTOM)

    def select_all(self):
        for var in self.category_vars.values(): var.set(True)

    def select_none(self):
        for var in self.category_vars.values(): var.set(False)

    def save_exclusions(self):
        new_list = [x.strip() for x in self.exclusion_var.get().split(",") if x.strip()]
        self.generator.persistent_exclusions = new_list
        excl_path = os.path.join(self.generator.data_dir, 'exclusions.json')
        try:
            with open(excl_path, 'w', encoding='utf-8') as f:
                json.dump(new_list, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Success", "Exclusions saved!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_generate(self):
        selected = [cat for cat, var in self.category_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("Warning", "Select a category!")
            return

        current_excl = [x.strip() for x in self.exclusion_var.get().split(",") if x.strip()]
        name = self.generator.generate(selected, self.use_adj_var.get(), current_excl)
        
        if name != "No nouns available":
            self.result_var.set(name)
            self.history.insert(0, name)
            self.history = self.history[:5]
            self.update_history_ui()

    def update_history_ui(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            self.history_listbox.insert(tk.END, item)

    def on_copy(self):
        res = self.result_var.get()
        if res and "!" not in res:
            pyperclip.copy(res)
            messagebox.showinfo("Copied", f"'{res}' copied!")

    def copy_history(self):
        selection = self.history_listbox.curselection()
        if selection:
            item = self.history_listbox.get(selection[0])
            pyperclip.copy(item)
            messagebox.showinfo("Copied", f"'{item}' copied from history!")

if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        import os
        os.system('pip install pyperclip --quiet')
        import pyperclip

    root = tk.Tk()
    app = NameGeneratorUI(root)
    root.mainloop()
