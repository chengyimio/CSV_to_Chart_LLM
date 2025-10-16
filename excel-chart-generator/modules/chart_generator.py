import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
from typing import Dict, Any, Tuple
import io
import base64

class ChartGenerator:
    def __init__(self, df: pd.DataFrame):
        """初始化圖表生成器"""
        self.df = df
        self.current_chart = None
        
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
from typing import Dict, Any, Tuple
import io
import base64
import importlib
import sys

class ChartGenerator:
    def __init__(self, df: pd.DataFrame):
        """初始化圖表生成器"""
        self.df = df
        self.current_chart = None
        self.available_modules = self._discover_available_modules()
        
    def _discover_available_modules(self) -> Dict[str, Any]:
        """動態發現可用的模組"""
        modules = {
            # 核心模組（必須）
            'pd': pd,
            'plt': plt, 
            'px': px,
            'go': go,
            'sns': sns,
            'st': st
        }
        
        # 嘗試載入 numpy（通常都有）
        try:
            import numpy as np
            modules['np'] = np
        except ImportError:
            pass
        
        # 嘗試載入可選模組
        optional_modules = [
            ('statsmodels.api', 'sm'),
            ('scipy.stats', 'stats'),
            ('scipy', 'scipy'),
            ('sklearn.preprocessing', 'preprocessing'),
            ('sklearn.metrics', 'metrics'),
            ('sklearn', 'sklearn'),
            ('xgboost', 'xgb'),
            ('lightgbm', 'lgb'),
            ('wordcloud', 'WordCloud'),
            ('networkx', 'nx')
        ]
        
        available_optional = []
        unavailable_optional = []
        
        for module_name, alias in optional_modules:
            try:
                module = importlib.import_module(module_name)
                modules[alias] = module
                available_optional.append(f"{alias} ({module_name})")
            except ImportError:
                unavailable_optional.append(f"{alias} ({module_name})")
        
        # 在側邊欄顯示模組狀態（更簡潔）
        if available_optional:
            st.sidebar.success(f"✅ 可用進階模組: {len(available_optional)} 個")
            with st.sidebar.expander("查看詳細"):
                for module in available_optional:
                    st.write(f"• {module}")
        
        if unavailable_optional:
            st.sidebar.info(f"ℹ️ 未安裝模組: {len(unavailable_optional)} 個")
            with st.sidebar.expander("查看詳細"):
                for module in unavailable_optional:
                    st.write(f"• {module}")
        
        return modules
    
    def _try_install_module(self, module_name: str) -> bool:
        """嘗試自動安裝缺少的模組（謹慎使用）"""
        
        # 常見模組的安裝映射
        install_mapping = {
            'statsmodels': 'statsmodels',
            'scipy': 'scipy', 
            'sklearn': 'scikit-learn',
            'xgboost': 'xgboost',
            'lightgbm': 'lightgbm',
            'tensorflow': 'tensorflow',
            'torch': 'torch',
            'networkx': 'networkx',
            'wordcloud': 'wordcloud'
        }
        
        if module_name in install_mapping:
            try:
                import subprocess
                package_name = install_mapping[module_name]
                
                # 詢問用戶是否要安裝
                install_confirm = st.button(
                    f"🔧 安裝 {package_name} 模組？", 
                    key=f"install_{module_name}",
                    help="點擊自動安裝缺少的模組"
                )
                
                if install_confirm:
                    with st.spinner(f"正在安裝 {package_name}..."):
                        result = subprocess.run(
                            [sys.executable, '-m', 'pip', 'install', package_name],
                            capture_output=True,
                            text=True
                        )
                        
                        if result.returncode == 0:
                            st.success(f"✅ {package_name} 安裝成功！請重新整理頁面。")
                            return True
                        else:
                            st.error(f"❌ {package_name} 安裝失敗: {result.stderr}")
                            return False
                            
            except Exception as e:
                st.error(f"安裝過程出現錯誤: {str(e)}")
                return False
        
        return False
    
    def execute_chart_code(self, code: str) -> Dict[str, Any]:
        """
        安全執行圖表生成代碼
        
        Args:
            code: 要執行的 Python 代碼
            
        Returns:
            執行結果字典
        """
        
        try:
            global_vars = {
                # Python 內建函數
                "__builtins__": {
                    'len', 'range', 'enumerate', 'zip', 'list', 'dict', 'set', 
                    'tuple', 'str', 'int', 'float', 'bool', 'min', 'max', 'sum',
                    'abs', 'round', 'sorted', 'reversed', 'print', 'type',
                    'isinstance', 'hasattr', 'getattr', 'setattr'
                },
                # 動態載入的模組
                **self.available_modules
            }
            
            local_vars = {
                'df': self.df.copy(),  # 使用副本避免修改原始數據
            }
            
            # 清理代碼 - 移除多餘的 import 語句
            cleaned_code = self._clean_code(code)
            
            # 執行代碼
            exec(cleaned_code, global_vars, local_vars)
            
            return {
                'success': True,
                'message': '圖表生成成功',
                'local_vars': local_vars
            }
            
        except NameError as e:
            error_msg = str(e)
            
            # 檢查是否是缺少模組的錯誤
            if "is not defined" in error_msg:
                missing_module = error_msg.split("'")[1] if "'" in error_msg else "unknown"
                
                return {
                    'success': False,
                    'error': f'缺少模組: {missing_module}',
                    'error_type': 'MissingModule',
                    'missing_module': missing_module,
                    'suggestion': f'請安裝 {missing_module} 模組或使用其他圖表類型'
                }
            
            return {
                'success': False,
                'error': str(e),
                'error_type': 'NameError'
            }
            
        except ImportError as e:
            return {
                'success': False,
                'error': f'模組導入錯誤: {str(e)}',
                'error_type': 'ImportError',
                'suggestion': '請安裝缺少的套件或使用更簡單的圖表類型'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__
            }
    
    def _clean_code(self, code: str) -> str:
        """清理代碼，移除不必要的 import 語句"""
        
        import re
        
        lines = code.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            
            # 跳過這些 import 語句（因為已經在環境中提供）
            skip_imports = [
                'import pandas as pd',
                'import numpy as np', 
                'import matplotlib.pyplot as plt',
                'import plotly.express as px',
                'import plotly.graph_objects as go',
                'import seaborn as sns',
                'import streamlit as st',
                'from plotly import express as px',
                'from plotly import graph_objects as go',
                'import statsmodels.api as sm',
                'from scipy import stats',
                'from sklearn import',
                'import scipy',
                'import statsmodels'
            ]
            
            # 檢查是否是要跳過的 import
            should_skip = False
            for skip_import in skip_imports:
                if line_stripped.startswith(skip_import):
                    should_skip = True
                    break
            
            # 如果是一般的 import 語句但模組不在允許清單中，也跳過
            if line_stripped.startswith('import ') or line_stripped.startswith('from '):
                if not any(allowed in line_stripped for allowed in ['pd', 'np', 'plt', 'px', 'go', 'sns', 'st']):
                    should_skip = True
            
            if not should_skip:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def create_fallback_chart(self, data_info: Dict[str, Any], user_query: str) -> Dict[str, Any]:
        """
        當自動生成失敗時，創建後備圖表
        
        Args:
            data_info: 數據分析結果
            user_query: 用戶查詢
            
        Returns:
            後備圖表結果
        """
        
        try:
            numeric_cols = data_info.get('numeric', [])
            categorical_cols = data_info.get('categorical', [])
            datetime_cols = data_info.get('datetime', [])
            
            # 根據數據類型選擇合適的預設圖表
            if datetime_cols and numeric_cols:
                # 時間序列圖
                return self._create_time_series_chart(datetime_cols[0], numeric_cols[0])
            
            elif len(numeric_cols) >= 2:
                # 散點圖
                return self._create_scatter_chart(numeric_cols[0], numeric_cols[1])
            
            elif categorical_cols and numeric_cols:
                # 柱狀圖
                return self._create_bar_chart(categorical_cols[0], numeric_cols[0])
            
            elif len(numeric_cols) == 1:
                # 直方圖
                return self._create_histogram(numeric_cols[0])
            
            else:
                # 數據摘要表
                return self._create_data_summary()
                
        except Exception as e:
            return {
                'success': False,
                'error': f'後備圖表生成失敗: {str(e)}'
            }
    
    def _create_time_series_chart(self, date_col: str, value_col: str) -> Dict[str, Any]:
        """創建時間序列圖表"""
        try:
            # 確保日期欄位是日期時間格式
            df_copy = self.df.copy()
            df_copy[date_col] = pd.to_datetime(df_copy[date_col])
            df_copy = df_copy.sort_values(date_col)
            
            fig = px.line(df_copy, x=date_col, y=value_col, 
                         title=f'{value_col} 隨時間變化趨勢')
            
            st.plotly_chart(fig, use_container_width=True)
            
            return {
                'success': True,
                'chart_type': 'time_series',
                'message': f'已生成 {date_col} vs {value_col} 的時間序列圖'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_scatter_chart(self, x_col: str, y_col: str) -> Dict[str, Any]:
        """創建散點圖"""
        try:
            fig = px.scatter(self.df, x=x_col, y=y_col, 
                           title=f'{x_col} vs {y_col} 散點圖')
            
            st.plotly_chart(fig, use_container_width=True)
            
            return {
                'success': True,
                'chart_type': 'scatter',
                'message': f'已生成 {x_col} vs {y_col} 的散點圖'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_bar_chart(self, cat_col: str, num_col: str) -> Dict[str, Any]:
        """創建柱狀圖"""
        try:
            # 計算每個類別的平均值或總和
            if self.df[cat_col].nunique() > 20:
                # 如果類別太多，只取前20個
                top_categories = self.df[cat_col].value_counts().head(20).index
                df_filtered = self.df[self.df[cat_col].isin(top_categories)]
            else:
                df_filtered = self.df
            
            # 按類別分組計算平均值
            grouped_data = df_filtered.groupby(cat_col)[num_col].mean().reset_index()
            
            fig = px.bar(grouped_data, x=cat_col, y=num_col,
                        title=f'{cat_col} 各類別的 {num_col} 平均值')
            
            st.plotly_chart(fig, use_container_width=True)
            
            return {
                'success': True,
                'chart_type': 'bar',
                'message': f'已生成 {cat_col} 的 {num_col} 柱狀圖'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_histogram(self, num_col: str) -> Dict[str, Any]:
        """創建直方圖"""
        try:
            fig = px.histogram(self.df, x=num_col, 
                             title=f'{num_col} 分布直方圖')
            
            st.plotly_chart(fig, use_container_width=True)
            
            return {
                'success': True,
                'chart_type': 'histogram',
                'message': f'已生成 {num_col} 的分布直方圖'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_data_summary(self) -> Dict[str, Any]:
        """創建數據摘要表"""
        try:
            st.subheader("數據摘要")
            
            # 基本統計資訊
            st.write("**數據基本資訊**")
            st.write(f"- 總行數: {len(self.df)}")
            st.write(f"- 總列數: {len(self.df.columns)}")
            
            # 顯示前幾行數據
            st.write("**數據預覽**")
            st.dataframe(self.df.head(10))
            
            # 數據類型資訊
            st.write("**欄位類型**")
            dtype_df = pd.DataFrame({
                '欄位名稱': self.df.columns,
                '數據類型': [str(dtype) for dtype in self.df.dtypes],
                '缺失值數量': [self.df[col].isnull().sum() for col in self.df.columns]
            })
            st.dataframe(dtype_df)
            
            return {
                'success': True,
                'chart_type': 'summary',
                'message': '已生成數據摘要'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def validate_chart_code(self, code: str) -> Tuple[bool, str]:
        """
        驗證圖表代碼的安全性
        
        Args:
            code: 要驗證的代碼
            
        Returns:
            (是否安全, 錯誤訊息)
        """
        
        # 危險的函數和模組
        dangerous_patterns = [
            'import os', 'import sys', 'import subprocess', 
            'eval(', 'exec(', '__import__',
            'open(', 'file(', 'input(', 'raw_input(',
            'delete', 'remove', 'rmdir'
        ]
        
        code_lower = code.lower()
        
        for pattern in dangerous_patterns:
            if pattern in code_lower:
                return False, f"代碼包含潛在危險操作: {pattern}"
        
        return True, "代碼驗證通過"