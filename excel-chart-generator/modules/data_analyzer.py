import pandas as pd
import numpy as np
from typing import Dict, List, Any
import re

class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        """初始化數據分析器"""
        self.df = df
        self.column_types = {}
        self.analysis_result = {}
    
    def analyze_data(self) -> Dict[str, Any]:
        """完整分析數據結構"""
        
        # 識別欄位類型
        self.column_types = self._identify_column_types()
        
        # 生成數據摘要
        summary = self._generate_data_summary()
        
        # 取得數據樣本
        sample_data = self._get_sample_data()
        
        self.analysis_result = {
            'column_types': self.column_types,
            'summary': summary,
            'sample_data': sample_data,
            'row_count': len(self.df),
            'column_count': len(self.df.columns),
            'numeric': self.column_types.get('numeric', []),
            'datetime': self.column_types.get('datetime', []),
            'categorical': self.column_types.get('categorical', [])
        }
        
        return self.analysis_result
    
    def _identify_column_types(self) -> Dict[str, List[str]]:
        """智能識別欄位類型"""
        
        numeric_cols = []
        datetime_cols = []
        categorical_cols = []
        
        for col in self.df.columns:
            col_data = self.df[col].dropna()
            
            if len(col_data) == 0:
                categorical_cols.append(col)
                continue
            
            # 檢查是否為數值類型
            if self._is_numeric_column(col_data):
                numeric_cols.append(col)
            
            # 檢查是否為日期時間類型
            elif self._is_datetime_column(col_data):
                datetime_cols.append(col)
            
            # 否則歸類為類別型
            else:
                categorical_cols.append(col)
        
        return {
            'numeric': numeric_cols,
            'datetime': datetime_cols,
            'categorical': categorical_cols
        }
    
    def _is_numeric_column(self, series: pd.Series) -> bool:
        """判斷是否為數值欄位"""
        
        # 如果已經是數值類型
        if pd.api.types.is_numeric_dtype(series):
            return True
        
        # 嘗試轉換為數值
        try:
            pd.to_numeric(series)
            return True
        except:
            pass
        
        # 檢查是否包含數值模式（如貨幣、百分比等）
        sample = series.astype(str).head(10)
        numeric_pattern = re.compile(r'^[\s]*[$¥€£]?[\s]*-?[\d,]+\.?\d*[\s]*[%]?[\s]*$')
        
        numeric_count = sum(1 for val in sample if numeric_pattern.match(str(val)))
        
        return numeric_count / len(sample) > 0.7
    
    def _is_datetime_column(self, series: pd.Series) -> bool:
        """判斷是否為日期時間欄位"""
        
        # 如果已經是日期時間類型
        if pd.api.types.is_datetime64_any_dtype(series):
            return True
        
        # 檢查欄位名稱是否包含日期關鍵字
        col_name = series.name.lower()
        date_keywords = ['date', 'time', '日期', '時間', 'year', 'month', 'day', 
                        '年', '月', '日', 'created', 'updated', 'timestamp']
        
        if any(keyword in col_name for keyword in date_keywords):
            # 嘗試轉換樣本數據
            try:
                sample = series.head(5).dropna()
                pd.to_datetime(sample)
                return True
            except:
                pass
        
        # 嘗試自動檢測日期格式
        try:
            sample = series.dropna().head(10)
            parsed_count = 0
            
            for val in sample:
                try:
                    pd.to_datetime(str(val))
                    parsed_count += 1
                except:
                    continue
            
            return parsed_count / len(sample) > 0.7
        
        except:
            return False
    
    def _generate_data_summary(self) -> Dict[str, Any]:
        """生成數據摘要統計"""
        
        summary = {
            'shape': self.df.shape,
            'missing_values': self.df.isnull().sum().to_dict(),
            'data_types': self.df.dtypes.astype(str).to_dict()
        }
        
        # 數值欄位統計
        if self.column_types.get('numeric'):
            numeric_df = self.df[self.column_types['numeric']].select_dtypes(include=[np.number])
            if not numeric_df.empty:
                summary['numeric_stats'] = numeric_df.describe().to_dict()
        
        # 類別欄位統計
        if self.column_types.get('categorical'):
            categorical_stats = {}
            for col in self.column_types['categorical']:
                if col in self.df.columns:
                    value_counts = self.df[col].value_counts().head(10)
                    categorical_stats[col] = {
                        'unique_count': self.df[col].nunique(),
                        'top_values': value_counts.to_dict()
                    }
            summary['categorical_stats'] = categorical_stats
        
        return summary
    
    def _get_sample_data(self) -> Dict[str, Any]:
        """取得數據樣本"""
        
        sample_size = min(5, len(self.df))
        
        return {
            'head': self.df.head(sample_size).to_dict('records'),
            'columns': list(self.df.columns),
            'sample_size': sample_size
        }
    
    def get_suitable_chart_suggestions(self, user_query: str = None) -> List[str]:
        """根據數據特性建議合適的圖表類型"""
        
        suggestions = []
        numeric_count = len(self.column_types.get('numeric', []))
        datetime_count = len(self.column_types.get('datetime', []))
        categorical_count = len(self.column_types.get('categorical', []))
        
        # 時間序列數據
        if datetime_count > 0 and numeric_count > 0:
            suggestions.extend(['line', 'area', 'time_series'])
        
        # 多個數值欄位
        if numeric_count >= 2:
            suggestions.extend(['scatter', 'correlation', 'heatmap'])
        
        # 類別數據
        if categorical_count > 0 and numeric_count > 0:
            suggestions.extend(['bar', 'pie', 'box'])
        
        # 單一數值欄位
        if numeric_count == 1:
            suggestions.extend(['histogram', 'distribution'])
        
        return list(set(suggestions))  # 去除重複