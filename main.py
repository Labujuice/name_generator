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
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        self.generator = NameGenerator()
        
        # 變數定義
        self.use_adj_var = tk.BooleanVar(value=True)
        self.category_vars = {}
        self.result_var = tk.StringVar(value="Click Generate!")
        self.exclusion_var = tk.StringVar()

        # 初始化排除清單內容 (從檔案載入)
        self.exclusion_var.set(", ".join(self.generator.persistent_exclusions))

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

        # 類別選擇區標題與按鈕
        cat_header_frame = ttk.Frame(settings_frame)
        cat_header_frame.pack(fill=tk.X, pady=(10, 2))
        
        ttk.Label(cat_header_frame, text="Noun Categories:").pack(side=tk.LEFT)
        
        ttk.Button(cat_header_frame, text="All", width=5, command=self.select_all).pack(side=tk.RIGHT, padx=2)
        ttk.Button(cat_header_frame, text="None", width=5, command=self.select_none).pack(side=tk.RIGHT, padx=2)
        
        cat_container = ttk.Frame(settings_frame)
        cat_container.pack(fill=tk.X, pady=5)

        # 自動生成類別勾選框 (每行 2 個)
        categories = sorted(self.generator.nouns.keys())
        for i, cat in enumerate(categories):
            var = tk.BooleanVar(value=True)
            self.category_vars[cat] = var
            display_name = cat.replace('_', ' ').capitalize()
            cb = ttk.Checkbutton(cat_container, text=display_name, variable=var)
            cb.grid(row=i//2, column=i%2, sticky=tk.W, padx=10, pady=2)

        # 排除清單管理區
        excl_header_frame = ttk.Frame(settings_frame)
        excl_header_frame.pack(fill=tk.X, pady=(15, 2))
        
        ttk.Label(excl_header_frame, text="Exclusion List:").pack(side=tk.LEFT)
        ttk.Button(excl_header_frame, text="Save to File", width=12, command=self.save_exclusions).pack(side=tk.RIGHT)
        
        excl_entry = ttk.Entry(settings_frame, textvariable=self.exclusion_var)
        excl_entry.pack(fill=tk.X, pady=(2, 5))
        ttk.Label(settings_frame, text="(Comma separated, e.g. ugly, annoying)", font=("Helvetica", 8, "italic")).pack(anchor=tk.W)

        # 結果顯示區
        result_frame = ttk.Frame(main_frame, padding="20")
        result_frame.pack(fill=tk.X)

        result_label = tk.Label(result_frame, textvariable=self.result_var, 
                               font=("Consolas", 22, "bold"), fg="#2c3e50", wraplength=400)
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

    def select_all(self):
        for var in self.category_vars.values():
            var.set(True)

    def select_none(self):
        for var in self.category_vars.values():
            var.set(False)

    def save_exclusions(self):
        # 取得 UI 上的清單並去空格
        new_list = [x.strip() for x in self.exclusion_var.get().split(",") if x.strip()]
        
        # 更新 generator 記憶體中的清單
        self.generator.persistent_exclusions = new_list
        
        # 寫入檔案
        excl_path = os.path.join(self.generator.data_dir, 'exclusions.json')
        try:
            with open(excl_path, 'w', encoding='utf-8') as f:
                json.dump(new_list, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Success", f"Exclusion list saved to {excl_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save exclusions: {str(e)}")

    def on_generate(self):
        selected = [cat for cat, var in self.category_vars.items() if var.get()]
        if not selected:
            messagebox.showwarning("Warning", "Please select at least one category!")
            return

        # 每次產生時都會使用目前輸入框中的內容 (臨時排除)
        current_excl = [x.strip() for x in self.exclusion_var.get().split(",") if x.strip()]
        
        name = self.generator.generate(
            selected_categories=selected,
            use_adjective=self.use_adj_var.get(),
            extra_exclusions=current_excl
        )
        self.result_var.set(name)

    def on_copy(self):
        res = self.result_var.get()
        if res and res not in ["Click Generate!", "No nouns available (check categories or exclusions)"]:
            pyperclip.copy(res)
            messagebox.showinfo("Success", f"'{res}' copied to clipboard!")

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
