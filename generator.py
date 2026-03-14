import json
import random
import os

class NameGenerator:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.adjectives = []
        self.nouns = {}
        self.persistent_exclusions = [] # 儲存來自檔案的排除清單
        self.load_data()

    def load_data(self):
        # 讀取形容詞
        adj_path = os.path.join(self.data_dir, 'adjectives.json')
        if os.path.exists(adj_path):
            with open(adj_path, 'r', encoding='utf-8') as f:
                self.adjectives = json.load(f)

        # 讀取各類別名詞
        noun_dir = os.path.join(self.data_dir, 'nouns')
        if os.path.exists(noun_dir):
            for filename in os.listdir(noun_dir):
                if filename.endswith('.json'):
                    category = filename.replace('.json', '')
                    with open(os.path.join(noun_dir, filename), 'r', encoding='utf-8') as f:
                        self.nouns[category] = json.load(f)

        # 讀取永久排除清單
        excl_path = os.path.join(self.data_dir, 'exclusions.json')
        if os.path.exists(excl_path):
            with open(excl_path, 'r', encoding='utf-8') as f:
                self.persistent_exclusions = json.load(f)

    def generate(self, selected_categories=None, use_adjective=True, extra_exclusions=None):
        """
        產生名稱
        :param selected_categories: 想要使用的名詞類別清單
        :param use_adjective: 是否加上形容詞
        :param extra_exclusions: UI 額外輸入的臨時排除清單
        :return: 產生的名稱字串
        """
        # 合併永久排除清單與臨時排除清單
        all_exclusions = [word.lower() for word in self.persistent_exclusions]
        if extra_exclusions:
            all_exclusions.extend([word.lower() for word in extra_exclusions])

        # 決定可用的名詞池
        available_nouns = []
        if selected_categories:
            for cat in selected_categories:
                if cat in self.nouns:
                    available_nouns.extend(self.nouns[cat])
        else:
            for cat_list in self.nouns.values():
                available_nouns.extend(cat_list)

        # 過濾排除清單 (不論是在檔案裡還是 UI 輸入的都會被過濾)
        available_nouns = [n for n in available_nouns if n.lower() not in all_exclusions]
        
        if not available_nouns:
            return "No nouns available (check categories or exclusions)"

        noun = random.choice(available_nouns)

        if use_adjective and self.adjectives:
            # 過濾形容詞
            available_adjectives = [a for a in self.adjectives if a.lower() not in all_exclusions]
            if available_adjectives:
                adj = random.choice(available_adjectives)
                return f"{adj.capitalize()} {noun.capitalize()}"
        
        return noun.capitalize()

# 測試代碼
if __name__ == "__main__":
    gen = NameGenerator()
    print("永久排除清單中的內容:", gen.persistent_exclusions)
    print("產生的名稱:", gen.generate())
