# Project Name Generator (專案名稱產生器)

一個基於 Python 3 的桌面應用工具，幫助您在想不到專案名稱時，透過隨機組合形容詞與多種名詞類別（動物、植物、食物、水果等）來產生靈感。

A Python 3 based desktop tool that generates project name inspirations by randomly combining adjectives and various noun categories.

---

## 🌟 Features (主要功能)

- **Multiple Categories (多樣化類別)**: 包含陸生/水生/飛行動物、植物、昆蟲、食物、水果及無機物。
- **Adjective Toggle (形容詞開關)**: 可自由選擇產生「單一名詞」或「形容詞 + 名詞」。
- **Exclusion Management (排除清單管理)**: 
    - 支援從介面直接輸入臨時排除詞。
    - 支援透過 `data/exclusions.json` 進行永久排除。
    - 介面提供「Save to File」功能，方便管理不想看到的單字。
- **One-click Copy (一鍵複製)**: 產生的名稱可直接複製到剪貼簿。
- **Customizable Data (高度客製化)**: 所有語詞皆儲存在 `data/` 資料夾下的 JSON 檔案，您可以輕鬆新增或刪除單字。

---

## 🚀 Quick Start (快速開始)

### Prerequisites (前置作業)
- Python 3.x
- `pyperclip` library (程式啟動時會自動嘗試安裝，或手動執行 `pip install pyperclip`)

### Running the App (執行程式)
在終端機中執行：
```bash
python3 main.py
```

---

## 📂 Project Structure (專案結構)

```text
name_generator/
├── main.py              # GUI 介面程式碼 (Main entry)
├── generator.py         # 核心邏輯 (Core logic)
├── requiremnet.md       # 開發需求與進度 (Requirements & TODO)
└── data/                # 語詞資料庫 (Word databases)
    ├── adjectives.json  # 形容詞
    ├── exclusions.json  # 排除清單
    └── nouns/           # 名詞類別資料夾
        ├── aquatic_animals.json
        ├── terrestrial_animals.json
        ├── flying_animals.json
        ├── fruits.json
        └── ...
```

---

## 🛠 Customization (客製化)

### Adding New Words (新增語詞)
您可以進入 `data/nouns/` 建立新的 `.json` 檔案（格式為字串陣列），程式會自動識別並在 UI 產生對應的勾選框。
Example format: `["word1", "word2", "word3"]`

### Permanent Exclusions (永久排除)
編輯 `data/exclusions.json`，將您不希望出現的單字加入陣列中。

---

## 📝 License
This project is for personal inspiration and educational use.
