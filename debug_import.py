"""
调试导入脚本 - 检查 Excel 列名
"""
import pandas as pd
import sys

# 读取上传的文件（从命令行参数或默认路径）
file_path = sys.argv[1] if len(sys.argv) > 1 else '/tmp/test_import.xlsx'

try:
    df = pd.read_excel(file_path, sheet_name='汇总表')
    
    print("=== Excel 文件列名 ===")
    for i, col in enumerate(df.columns):
        print(f"{i}. '{col}'")
    
    print("\n=== 前 3 行数据 ===")
    print(df.head(3).to_string())
    
    print("\n=== 第 1 行数据（字典格式）===")
    first_row = df.iloc[0].to_dict()
    for key, value in first_row.items():
        print(f"'{key}': {value}")
        
except Exception as e:
    print(f"错误：{e}")
