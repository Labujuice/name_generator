import json
import random
import os

class NameGenerator:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.adjectives = []
        self.nouns = {}
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

    def generate(self, selected_categories=None, use_adjective=True, exclusions=None):
        """
        產生名稱
        :param selected_categories: 想要使用的名詞類別清單 (例如 ['animals', 'plants'])
        :param use_adjective: 是否加上形容詞
        :param exclusions: 排除清單
        :return: 產生的名稱字串
        """
        if exclusions is None:
            exclusions = []
        
        # 轉換排除清單為小寫以進行不分大小寫的比對
        exclusions = [word.lower() for word in exclusions]

        # 決定可用的名詞池
        available_nouns = []
        if selected_categories:
            for cat in selected_categories:
                if cat in self.nouns:
                    available_nouns.extend(self.nouns[cat])
        else:
            # 如果沒選類別，預設使用所有名詞
            for cat_list in self.nouns.values():
                available_nouns.extend(cat_list)

        # 過濾排除清單
        available_nouns = [n for n in available_nouns if n.lower() not in exclusions]
        
        if not available_nouns:
            return "No nouns available (check categories or exclusions)"

        noun = random.choice(available_nouns)

        if use_adjective and self.adjectives:
            # 過濾形容詞排除清單
            available_adjectives = [a for a in self.adjectives if a.lower() not in exclusions]
            if available_adjectives:
                adj = random.choice(available_adjectives)
                # 依據需求：單名詞或形容詞+名詞 (空格分隔或連字元，這裡先採空格或駝峰，使用者需求通常是專案名)
                # 我們回傳 "Adjective Noun" 格式，首字母大寫
                return f"{adj.capitalize()} {noun.capitalize()}"
        
        return noun.capitalize()

# 測試代碼
if __name__ == "__main__":
    gen = NameGenerator()
    print("預設產生 (含形容詞):", gen.generate())
    print("僅動物 (不含形容詞):", gen.generate(selected_categories=['animals'], use_adjective=False))
    print("排除測試 (排除 'Agile'):", gen.generate(exclusions=['Agile']))
