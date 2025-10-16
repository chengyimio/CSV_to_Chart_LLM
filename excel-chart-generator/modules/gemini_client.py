import os
import google.generativeai as genai
from typing import Dict, Any
import time

class GeminiClient:
    def __init__(self, api_key: str = None):
        """初始化 Gemini 客戶端"""
        if api_key is None:
            api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("請提供 Gemini API Key")
        
        genai.configure(api_key=api_key)
        # 使用 Gemini 2.5 Flash 模型
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_chart_code(self, user_query: str, data_info: Dict[str, Any], available_modules: Dict[str, Any] = None, max_retries: int = 3) -> Dict[str, Any]:
        """
        生成圖表代碼
        
        Args:
            user_query: 用戶查詢
            data_info: 數據資訊
            available_modules: 可用模組字典
            max_retries: 最大重試次數
            
        Returns:
            包含生成的代碼和相關資訊的字典
        """
        
        prompt = self._create_prompt(user_query, data_info, available_modules)
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                
                # 提取代碼部分
                code = self._extract_code(response.text)
                
                return {
                    'success': True,
                    'code': code,
                    'raw_response': response.text,
                    'attempt': attempt + 1
                }
                
            except Exception as e:
                if attempt == max_retries - 1:
                    return {
                        'success': False,
                        'error': str(e),
                        'attempts': max_retries
                    }
                # 短暫等待後重試
                time.sleep(1)
        
        return {'success': False, 'error': '未知錯誤'}
    
    def _create_prompt(self, user_query: str, data_info: Dict[str, Any], available_modules: Dict[str, Any] = None) -> str:
        """建立提示詞"""
        
        columns_info = f"""
        數據欄位資訊：
        - 數值欄位: {data_info.get('numeric', [])}
        - 日期時間欄位: {data_info.get('datetime', [])}
        - 類別欄位: {data_info.get('categorical', [])}
        - 總行數: {data_info.get('row_count', 0)}
        - 數據樣本前3行: {str(data_info.get('sample_data', {}).get('head', [])[:3])}
        """
        
        # 建立可用模組資訊
        if available_modules:
            available_list = list(available_modules.keys())
            modules_info = f"""
        可用的模組和別名（請只使用這些，不要使用其他模組）：
        {', '.join(available_list)}

        核心模組說明：
        - pd: pandas 數據處理
        - np: numpy 數值計算  
        - plt: matplotlib 繪圖
        - px: plotly express 互動圖表
        - go: plotly graph objects 進階圖表
        - sns: seaborn 統計圖表
        - st: streamlit 顯示功能

        可選進階模組（如果可用）：
        - sm: statsmodels 統計分析
        - stats: scipy.stats 統計測試
        - sklearn相關: 機器學習功能
        """
        else:
            modules_info = """
            可用的基本模組：
            - pd: pandas 數據處理
            - np: numpy 數值計算
            - plt: matplotlib 繪圖  
            - px: plotly express 互動圖表
            - go: plotly graph objects
            - sns: seaborn 統計圖表
            - st: streamlit 顯示功能
            """
        
        prompt = f"""
            你是一個數據視覺化專家。根據用戶需求和數據資訊，生成 Python 代碼來建立圖表。

{columns_info}

{modules_info}

用戶需求：{user_query}

重要限制和要求：
1. 數據已載入為 df 變數，請直接使用
2. 只能使用上面列出的可用模組，絕對不要import其他模組
3. 不要寫任何 import 語句（所有模組已經載入）
4. 必須使用 st.plotly_chart(fig) 顯示 plotly 圖表
5. 必須使用 st.pyplot(fig) 顯示 matplotlib 圖表
6. 圖表要有清楚的標題、軸標籤和圖例
7. 如果用戶需求需要未列出的模組，請使用基本模組實現類似功能
8. 確保欄位名稱與數據中的欄位完全匹配（注意大小寫和空格）
9. 如果有圖表文字請用英文字呈現，不要有任何中文字

代碼風格要求：
- 簡潔清晰，避免複雜的統計分析
- 優先使用 plotly (px) 製作互動圖表
- 如果數據量大，考慮適當採樣
- 處理可能的缺失值
- 如果有圖表文字請用英文字呈現，不要有任何中文字

請只返回 Python 代碼，用 ```python 包圍，不包含任何 import 語句：

```python
# 你的代碼（不包含 import，使用可用模組）
```
"""
        
        return prompt
    
    def _extract_code(self, response_text: str) -> str:
        """從回應中提取 Python 代碼"""
        
        # 尋找 ```python 代碼塊
        import re
        
        # 匹配 ```python ... ``` 格式
        python_code_pattern = r'```python\s*(.*?)\s*```'
        matches = re.findall(python_code_pattern, response_text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # 如果沒有找到標準格式，嘗試匹配 ``` ... ``` 格式
        general_code_pattern = r'```\s*(.*?)\s*```'
        matches = re.findall(general_code_pattern, response_text, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # 如果都沒有找到，返回原始文本（去除前後空白）
        return response_text.strip()