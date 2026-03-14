import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
from generator import NameGenerator

class NameGeneratorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Name Generator")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        self.generator = NameGenerator()
        
        # 變數定義
        self.use_adj_var = tk.BooleanVar(value=True)
        self.category_vars = {}
        self.result_var = tk.StringVar(value="Click Generate!")
        self.exclusion_var = tk.StringVar()

        self.setup_ui()

    def setup_ui(self):
        # 主容器
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 標題
        title_label = ttk.Label(main_frame, text="Name Generator", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(0, 20))

        # 設定區
        settings_frame = ttk.LabelFrame(main_frame, text=" Settings ", padding="10")
        settings_frame.pack(fill=tk.X, pady=5)

        # 形容詞開關
        adj_check = ttk.Checkbutton(settings_frame, text="Use Adjectives", variable=self.use_adj_var)
        adj_check.pack(anchor=tk.W, pady=2)

        # 類別選擇區
        cat_label = ttk.Label(settings_frame, text="Noun Categories:")
        cat_label.pack(anchor=tk.W, pady=(10, 2))
        
        cat_container = ttk.Frame(settings_frame)
        cat_container.pack(fill=tk.X)

        # 自動生成類別勾選框 (每行 3 個)
        categories = sorted(self.generator.nouns.keys())
        for i, cat in enumerate(categories):
            var = tk.BooleanVar(value=True)
            self.category_vars[cat] = var
            cb = ttk.Checkbutton(cat_container, text=cat.capitalize(), variable=var)
            cb.grid(row=i//3, column=i%3, sticky=tk.W, padx=5, pady=2)

        # 排除清單
        excl_label = ttk.Label(settings_frame, text="Exclusions (comma separated):")
        excl_label.pack(anchor=tk.W, pady=(10, 2))
        excl_entry = ttk.Entry(settings_frame, textvariable=self.exclusion_var)
        excl_entry.pack(fill=tk.X, pady=2)

        # 結果顯示區
        result_frame = ttk.Frame(main_frame, padding="20")
        result_frame.pack(fill=tk.X)

        result_label = tk.Label(result_frame, textvariable=self.result_var, 
                               font=("Consolas", 20, "bold"), fg="#2c3e50", wraplength=400)
        result_label.pack(pady=10)

        # 按鈕區
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)

        gen_btn = ttk.Button(btn_frame, text="Generate", command=self.on_generate, width=15)
        gen_btn.grid(row=0, column=0, padx=5)

        copy_btn = ttk.Button(btn_frame, text="Copy", command=self.on_copy, width=15)
        copy_btn.grid(row=0, column=1, padx=5)

        # 頁腳
        footer = ttk.Label(main_frame, text="Powered by Python 3", font=("Helvetica", 8))
        footer.pack(side=tk.BOTTOM, pady=10)

    def on_generate(self):
        selected = [cat for cat, var in self.category_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one category!")
            return

        exclusions = [x.strip() for x in self.exclusion_var.get().split(",") if x.strip()]
        
        name = self.generator.generate(
            selected_categories=selected,
            use_adjective=self.use_adj_var.get(),
            exclusions=exclusions
        )
        self.result_var.set(name)

    def on_copy(self):
        res = self.result_var.get()
        if res and res != "Click Generate!":
            pyperclip.copy(res)
            messagebox.showinfo("Success", f"'{res}' copied to clipboard!")

if __name__ == "__main__":
    # 安裝 pyperclip (如果尚未安裝，以便支援剪貼簿功能)
    try:
        import pyperclip
    except ImportError:
        import os
        os.system('pip install pyperclip --quiet')
        import pyperclip

    root = tk.Tk()
    app = NameGeneratorUI(root)
    root.mainloop()
