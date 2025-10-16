import streamlit as st
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 導入自訂模組
from modules.data_analyzer import DataAnalyzer
from modules.gemini_client import GeminiClient
from modules.chart_generator import ChartGenerator

# 設定頁面
st.set_page_config(
    page_title="Excel/CSV 圖表生成器",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto"
)

# 自訂 CSS 樣式
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stButton > button {
        width: 100%;
    }
    .plot-container {
        width: 100%;
        margin: 1rem 0;
    }
    .stSelectbox > div > div {
        min-width: 200px;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """初始化 session state"""
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'data_analysis' not in st.session_state:
        st.session_state.data_analysis = None
    if 'gemini_client' not in st.session_state:
        st.session_state.gemini_client = None
    if 'chart_history' not in st.session_state:
        st.session_state.chart_history = []

def setup_gemini_client():
    """設定 Gemini 客戶端"""
    if st.session_state.gemini_client is None:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_api_key_here':
            st.sidebar.error("請先設定 Gemini API Key！")
            st.sidebar.info("請在 .env 檔案中設定 GEMINI_API_KEY")
            return False
        
        try:
            st.session_state.gemini_client = GeminiClient(api_key)
            return True
        except Exception as e:
            st.sidebar.error(f"Gemini 客戶端初始化失敗: {str(e)}")
            return False
    
    return True

def load_file(uploaded_file):
    """載入 Excel 或 CSV 檔案"""
    try:
        # 儲存上傳的檔案
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        
        file_path = uploads_dir / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 根據檔案類型讀取
        file_extension = uploaded_file.name.lower().split('.')[-1]
        
        if file_extension == 'xlsx':
            df = pd.read_excel(file_path)
        elif file_extension == 'csv':
            # 嘗試不同的編碼格式
            encodings = ['utf-8', 'gbk', 'big5', 'cp1252', 'iso-8859-1']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    st.info(f"使用 {encoding} 編碼成功載入 CSV")
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise ValueError("無法使用常見編碼格式讀取 CSV 檔案")
        
        else:
            raise ValueError(f"不支援的檔案格式: {file_extension}")
        
        # 清理欄位名稱（移除前後空白）
        df.columns = df.columns.str.strip()
        
        return df, str(file_path)
    
    except Exception as e:
        st.error(f"檔案載入失敗: {str(e)}")
        return None, None

def display_data_analysis(data_analysis):
    """顯示數據分析結果"""

    st.subheader("數據分析結果")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("總行數", data_analysis['row_count'])
    
    with col2:
        st.metric("總欄位數", data_analysis['column_count'])
    
    with col3:
        numeric_count = len(data_analysis['numeric'])
        st.metric("數值欄位", numeric_count)
    
    # 欄位類型展示
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if data_analysis['numeric']:
            st.write("**數值欄位:**")
            for col in data_analysis['numeric']:
                st.write(f"• {col}")

    with col2:
        if data_analysis['datetime']:
            st.write("**日期時間欄位:**")
            for col in data_analysis['datetime']:
                st.write(f"• {col}")

    with col3:
        if data_analysis['categorical']:
            st.write("**類別欄位:**")
            for col in data_analysis['categorical'][:5]:  # 只顯示前5個
                st.write(f"• {col}")
            if len(data_analysis['categorical']) > 5:
                st.write(f"... 還有 {len(data_analysis['categorical']) - 5} 個")

def generate_chart(user_query, data_analysis, gemini_client, chart_generator):
    """生成圖表"""

    with st.spinner("正在分析您的需求並生成圖表..."):
        
        # 獲取可用模組資訊
        available_modules = chart_generator.available_modules
        
        # 調用 Gemini API 生成圖表代碼（傳入可用模組）
        result = gemini_client.generate_chart_code(user_query, data_analysis, available_modules)
        
        if result['success']:
            st.success(f"代碼生成成功！（第 {result['attempt']} 次嘗試）")

            # 顯示生成的代碼
            with st.expander("查看生成的代碼"):
                st.code(result['code'], language='python')

            # 驗證代碼安全性
            is_safe, safety_msg = chart_generator.validate_chart_code(result['code'])

            if not is_safe:
                st.error(f"代碼安全檢查失敗: {safety_msg}")
                return False

            # 執行圖表代碼
            exec_result = chart_generator.execute_chart_code(result['code'])

            if exec_result['success']:
                st.success("圖表生成成功！")
                
                # 記錄到歷史
                st.session_state.chart_history.append({
                    'query': user_query,
                    'code': result['code'],
                    'timestamp': pd.Timestamp.now()
                })
                
                return True
            
            else:
                st.error(f"圖表執行失敗: {exec_result['error']}")

                # 特殊處理缺少模組的情況
                if exec_result.get('error_type') == 'MissingModule':
                    missing_module = exec_result.get('missing_module', 'unknown')

                    st.warning(f"缺少模組: {missing_module}")
                    st.info("系統正在學習可用模組，請重新嘗試或使用更簡單的圖表描述")

                    # 更新可用模組（重新掃描）
                    chart_generator.available_modules = chart_generator._discover_available_modules()

                st.info("正在嘗試生成後備圖表...")

                # 嘗試後備圖表
                fallback_result = chart_generator.create_fallback_chart(data_analysis, user_query)

                if fallback_result['success']:
                    st.warning(f"已生成後備圖表: {fallback_result['message']}")
                    return True
                else:
                    st.error(f"後備圖表也失敗了: {fallback_result['error']}")
                    return False
        
        else:
            st.error(f"代碼生成失敗: {result['error']}")

            # 嘗試後備圖表
            st.info("正在嘗試生成後備圖表...")
            fallback_result = chart_generator.create_fallback_chart(data_analysis, user_query)

            if fallback_result['success']:
                st.warning(f"已生成後備圖表: {fallback_result['message']}")
                return True
            else:
                st.error(f"後備圖表也失敗了: {fallback_result['error']}")
                return False

def main():
    """主函數"""
    
    # 初始化
    initialize_session_state()
    
    # 標題
    st.title("Excel/CSV 智能圖表生成器")
    st.markdown("---")

    # 側邊欄 - API 設定檢查
    with st.sidebar:
        st.header("系統設定")

        # 檢查 API Key
        if setup_gemini_client():
            st.success("Gemini API 已連接")
        else:
            st.error("請設定 Gemini API Key")
            st.info("在專案根目錄的 .env 檔案中添加：\nGEMINI_API_KEY=你的API金鑰")
            st.stop()

        st.markdown("---")

        # 顯示使用說明
        st.header("使用說明")
        st.write("1. 上傳 Excel 或 CSV 檔案")
        st.write("2. 點擊分析數據")
        st.write("3. 描述想要的圖表")
        st.write("4. 生成圖表")
        
        if st.session_state.df is not None:
            st.markdown("---")
            st.write(f"**當前檔案:** {len(st.session_state.df)} 行")
            st.write(f"**欄位數:** {len(st.session_state.df.columns)} 個")
    
    # 主要內容區域
    # 步驟1: 上傳檔案
    st.header("步驟 1: 上傳數據檔案")
    
    uploaded_file = st.file_uploader(
        "選擇 Excel 或 CSV 檔案",
        type=['xlsx', 'csv'],
        help="支援 .xlsx 和 .csv 格式的檔案"
    )
    
    if uploaded_file is not None:
        # 載入數據
        df, file_path = load_file(uploaded_file)
        
        if df is not None:
            st.session_state.df = df
            st.success(f"檔案載入成功！共 {len(df)} 行，{len(df.columns)} 欄")

            # 顯示數據預覽
            with st.expander("數據預覽"):
                st.dataframe(df.head(10))

            # 步驟2: 分析數據
            st.header("步驟 2: 數據分析")

            if st.button("開始分析數據", type="primary"):
                with st.spinner("正在分析數據結構..."):
                    analyzer = DataAnalyzer(df)
                    data_analysis = analyzer.analyze_data()
                    st.session_state.data_analysis = data_analysis

                st.success("數據分析完成！")
            
            # 顯示分析結果
            if st.session_state.data_analysis is not None:
                display_data_analysis(st.session_state.data_analysis)
                
                # 步驟3: 生成圖表
                st.header("步驟 3: 生成圖表")

                # 用戶輸入
                user_query = st.text_area(
                    "描述您想要的圖表:",
                    placeholder="例如：幫我畫一個銷售額隨時間變化的趨勢圖\n或：比較各產品類別的平均價格",
                    height=100
                )

                col1, col2 = st.columns([1, 1])

                with col1:
                    generate_btn = st.button("生成圖表", type="primary", disabled=not user_query)

                with col2:
                    clear_btn = st.button("清除歷史")
                    if clear_btn:
                        st.session_state.chart_history = []
                        st.success("歷史已清除！")
                
                if generate_btn and user_query:
                    chart_generator = ChartGenerator(st.session_state.df)
                    generate_chart(
                        user_query, 
                        st.session_state.data_analysis,
                        st.session_state.gemini_client,
                        chart_generator
                    )
                
                # 圖表歷史
                if st.session_state.chart_history:
                    st.header("圖表歷史")

                    for i, record in enumerate(reversed(st.session_state.chart_history[-5:])):
                        with st.expander(f"{record['timestamp'].strftime('%H:%M:%S')} - {record['query'][:50]}..."):
                            st.write(f"**查詢:** {record['query']}")
                            st.code(record['code'], language='python')

if __name__ == "__main__":
    main()