# 用自然語言生成圖表(可用你自己的CSV或excel資料)

[English](README.md) | [繁體中文](README.zh-TW.md)

一個基於 AI 的數據視覺化工具，能夠自動分析 Excel/CSV 檔案並根據自然語言描述生成各種圖表。

## 功能特色

- **LLM驅動**: 使用 Google Gemini API 理解自然語言指令
- **多格式支援**: 支援 Excel (.xlsx) 和 CSV (.csv) 檔案
- **數據分析**: 自動識別數據類型（數值、日期、類別）
- **圖表支援**: 支援柱狀圖、折線圖、散點圖、圓餅圖等
- **互動視覺化**: 基於 Plotly 的互動式圖表
- **安全執行**: 代碼安全檢查和沙箱執行環境
- **重試機制**: 自動錯誤處理和後備圖表機制
- **響應式界面**: 基於 Streamlit 的現代化 Web 界面

## 快速開始

### 環境要求

- Python 3.11 或 3.12 （推薦，Python 3.13 可能有兼容性問題）
- Google Gemini API Key

### 安裝步驟

#### 方法 1: 快速安裝（推薦）

1. **克隆專案**
   ```bash
   git clone https://github.com/chengyimio/CSV_to_Chart_LLM.git
   cd CSV_to_Chart_LLM/excel-chart-generator
   ```

2. **使用自動安裝腳本**

   **Windows:**
   ```bash
   python setup.py
   ```

   **macOS/Linux:**
   ```bash
   python3 setup.py
   ```

   腳本會自動完成：
   - 檢查 Python 版本
   - 建立虛擬環境
   - 安裝所有依賴
   - 創建 `.env` 配置文件

3. **設定 API Key**
   - 前往 [Google AI Studio](https://ai.google.dev) 取得 Gemini API Key
   - 編輯 `excel-chart-generator/.env` 檔案，填入你的 API Key：
     ```env
     GEMINI_API_KEY=你的_API_金鑰
     ```

4. **運行應用**

   **Windows:**
   ```bash
   venv\Scripts\activate
   streamlit run app.py
   ```

   **macOS/Linux:**
   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```

#### 方法 2: 手動安裝

1. **克隆專案**
   ```bash
   git clone https://github.com/chengyimio/CSV_to_Chart_LLM.git
   cd CSV_to_Chart_LLM/excel-chart-generator
   ```

2. **建立虛擬環境**

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

4. **設定環境變數**
   ```bash
   # 複製環境變數模板
   cp .env.example .env

   # 編輯 .env 並填入你的 Gemini API Key
   ```

5. **運行應用**
   ```bash
   streamlit run app.py
   ```

## 系統架構

```
excel-chart-generator/
├── app.py                     # 主應用程式
├── .env                       # 環境變數配置
├── requirements.txt           # 專案依賴
├── modules/
│   ├── __init__.py
│   ├── data_analyzer.py       # 數據分析模組
│   ├── gemini_client.py       # Gemini API 客戶端
│   ├── chart_generator.py     # 圖表生成器
│   └── module_manager.py      # 模組管理配置
└── uploads/                   # 暫存上傳檔案
```

## 使用方式

### 基本使用流程

1. **上傳數據檔案**: 支援 Excel (.xlsx) 或 CSV (.csv)
2. **分析數據結構**: 系統自動識別欄位類型
3. **描述圖表需求**: 用自然語言描述想要的圖表
4. **生成視覺化**: AI 自動生成並顯示圖表

### 範例指令

```
基礎圖表：
- "畫一個銷售額的柱狀圖"
- "顯示各月份的趨勢圖" 
- "製作產品類別的圓餅圖"

進階圖表：
- "比較各地區的銷售表現，用分組柱狀圖"
- "分析價格和數量的相關性，用散點圖"
- "顯示時間序列數據的趨勢變化"

統計分析：
- "顯示數據的分布情況"
- "比較不同類別的平均值"
- "分析各變數之間的相關性"
```

## 技術棧

### 核心依賴
- **Streamlit**: Web 應用框架
- **Pandas**: 數據處理和分析
- **Plotly**: 互動式圖表庫
- **Matplotlib & Seaborn**: 統計圖表
- **Google GenerativeAI**: Gemini API 客戶端
- **NumPy**: 數值計算支援

### 可選依賴（進階功能）
- **Statsmodels**: 統計分析
- **Scikit-learn**: 機器學習
- **SciPy**: 科學計算

## 配置說明

### requirements.txt
```txt
# 核心依賴
streamlit==1.40.0
pandas==2.2.3
numpy==1.24.4
openpyxl==3.1.5
plotly==5.24.1
matplotlib==3.9.2
seaborn==0.13.2
google-generativeai==0.8.3
python-dotenv==1.0.1

# 可選依賴
statsmodels==0.14.0
scipy==1.11.4
scikit-learn==1.3.2
```

### .env 檔案範例
```env
# Google Gemini API 配置
GEMINI_API_KEY=your_api_key_here

# 可選配置
MAX_FILE_SIZE_MB=50
DEFAULT_CHART_TYPE=plotly
DEBUG_MODE=false
```

## 支援的圖表類型

| 圖表類型 | 適用場景 | 示例指令 |
|---------|---------|---------|
| 柱狀圖 | 類別比較 | "各產品的銷量對比" |
| 折線圖 | 趨勢分析 | "月銷售額變化趨勢" |
| 散點圖 | 相關性分析 | "價格與銷量的關係" |
| 圓餅圖 | 比例展示 | "市場占有率分布" |
| 直方圖 | 分布分析 | "年齡分布情況" |
| 箱線圖 | 統計摘要 | "各組數據的分布特徵" |
| 熱力圖 | 相關性矩陣 | "變數間相關性分析" |

## 故障排除

### 常見問題

**1. 安裝失敗 (Python 3.13 兼容性問題)**
```bash
# 解決方案：使用 Python 3.11 或 3.12
python --version  # 確認版本
pip install --upgrade pip setuptools
```

**2. API Key 錯誤**
```bash
# 檢查 .env 檔案是否正確設定
# 確認 API Key 有效性
```

**3. 模組導入錯誤**
```bash
# 重新安裝依賴
pip install --upgrade --force-reinstall -r requirements.txt
```

**4. 圖表生成失敗**
- 檢查數據格式是否正確
- 確認欄位名稱匹配
- 嘗試更簡單的圖表描述

### 效能優化

- **大型檔案**: 建議數據量控制在 5000 行以內
- **記憶體使用**: 可調整 Streamlit 的記憶體配置
- **API 配額**: 注意 Gemini API 的使用限制

## 貢獻指南

歡迎貢獻程式碼、回報問題或提出改進建議！

### 開發環境設定
1. Fork 專案
2. 建立功能分支: `git checkout -b feature/new-feature`
3. 提交變更: `git commit -am 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 建立 Pull Request

### 代碼規範
- 使用 Python PEP 8 風格
- 添加適當的註釋和文檔
- 確保向後兼容性
- 包含測試案例



## 支援與回饋

如果您遇到問題或有改進建議：

- **回報 Bug**: 請在 Issues 中詳細描述問題
- **功能建議**: 歡迎提出新功能想法
- **聯絡我們**: [chengyimio@gmail.com]
- **文檔問題**: 幫助改善使用說明

---

## 未來規劃

- [ ] 支援更多檔案格式 (JSON, XML)
- [ ] 增加儀表板功能
- [ ] 多語言支援
- [ ] 圖表匯出功能 (PNG, PDF)
- [ ] 數據清理建議
- [ ] 協作功能
- [ ] 自訂圖表樣式
- [ ] API 介面開發

## 版本歷史

### v1.0.0 (目前版本)
- 基礎圖表生成功能
- Excel/CSV 檔案支援
- Gemini AI 整合
- 安全代碼執行
- 響應式 UI

---

**如果這個專案對您有幫助，請給我們一個 Star！**