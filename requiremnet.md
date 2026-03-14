# name generator

一個產生專案名稱的工具, 用於想不到專案名稱時可以使用。有基本的類別、形容詞、組合與否、例外排除功能。

## function description
- 類別需要討論動物、植物、昆蟲、食物、無機物....哪些類別合適當專案名稱
- 形容詞種類: 盡可能使用形容人類、動物、昆蟲、食物、無機物的形容詞, 比如說 搞笑的、敏捷的、討厭的、安靜的、無與倫比的、完美的、煮沸的、等等。
- 名稱產生可以選取單名詞 或者 形容詞加上名詞
- 選詞一律使用單詞, 例如 bear, car, cat, jungle, 避免使用 Taiwan black bear
- 可以依據我的設定產生名字, 需要有使用者界面讓人設定, 盡量讓所有人都可以學會使用
- 語詞資料庫使用 csv 進行管理, 或者也可以使用 json, 擇優者
- 針對語詞的例外排除同上, 建議使用相容格式
- 名詞各類別、形容詞皆使用獨立的檔案管理
- 語詞請使用英文
- 技術實作：Python 3
- 最後請撰寫 README.md

## TODO
### Phase 1: Project Setup & Data Preparation
- [x] Initialize Python project structure (data/ directory)
- [x] Create initial JSON data files for adjectives and noun categories (animals, plants, foods, etc.)
- [x] Populate JSON data with English word lists (single words only)

### Phase 2: Core Logic Development
- [ ] Implement data loading logic using Python `json` module
- [ ] Implement core name generation logic (Category selection, Adjective toggle)
- [ ] Implement exclusion filtering system

### Phase 3: User Interface (UI)
- [ ] Develop a user interface (Simple CLI or Tkinter GUI) for settings
- [ ] Implement "Generate" button and display area
- [ ] Add "Copy to Clipboard" functionality

### Phase 4: Final Polish & Documentation
- [ ] Final testing and word list refinement
- [ ] Write comprehensive README.md (English/Traditional Chinese)
- [ ] Package as a portable script or executable