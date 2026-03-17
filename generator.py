import json
import random
import os

class NameGenerator:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.adjectives = []
        self.nouns = {}
        self.persistent_exclusions = []
        self.load_data()

    def load_data(self):
        # 讀取形容詞
        adj_path = os.path.join(self.data_dir, 'adjectives.json')
        if os.path.exists(adj_path):
            with open(adj_path, 'r', encoding='utf-8') as f:
                self.adjectives = json.load(f)

        # 讀取各類別名詞 (nouns/*.json)
        noun_dir = os.path.join(self.data_dir, 'nouns')
        if os.path.exists(noun_dir):
            for filename in sorted(os.listdir(noun_dir)): # 排序確保 UI 穩定
                if filename.endswith('.json'):
                    category = filename.replace('.json', '')
                    with open(os.path.join(noun_dir, filename), 'r', encoding='utf-8') as f:
                        self.nouns[category] = json.load(f)

        # 讀取永久排除清單
        excl_path = os.path.join(self.data_dir, 'exclusions.json')
        if os.path.exists(excl_path):
            with open(excl_path, 'r', encoding='utf-8') as f:
                self.persistent_exclusions = json.load(f)

    def get_categories(self):
        """回傳目前載入的所有類別名稱"""
        return sorted(self.nouns.keys())

    def generate(self, selected_categories=None, use_adjective=True, extra_exclusions=None):
        all_exclusions = [word.lower() for word in self.persistent_exclusions]
        if extra_exclusions:
            all_exclusions.extend([word.lower() for word in extra_exclusions])

        available_nouns = []
        if selected_categories:
            for cat in selected_categories:
                if cat in self.nouns:
                    available_nouns.extend(self.nouns[cat])
        else:
            for cat_list in self.nouns.values():
                available_nouns.extend(cat_list)

        available_nouns = [n for n in available_nouns if n.lower() not in all_exclusions]
        
        if not available_nouns:
            return "No nouns available"

        noun = random.choice(available_nouns)

        if use_adjective and self.adjectives:
            available_adjectives = [a for a in self.adjectives if a.lower() not in all_exclusions]
            if available_adjectives:
                adj = random.choice(available_adjectives)
                return f"{adj.capitalize()} {noun.capitalize()}"
        
        return noun.capitalize()

if __name__ == "__main__":
    gen = NameGenerator()
    print("Categories found:", gen.get_categories())
    print("Example:", gen.generate())
