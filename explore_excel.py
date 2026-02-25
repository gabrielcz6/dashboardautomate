import pandas as pd
import json

file_path = "Launch Crea y Lanza tu Curso Online - Marzo 2026.xlsx"

try:
    xl = pd.ExcelFile(file_path)
    with open("excel_summary.txt", "w", encoding="utf-8") as f:
        f.write(f"Sheets: {xl.sheet_names}\n")
        for sheet in xl.sheet_names:
            f.write(f"\n--- Sheet: {sheet} ---\n")
            df = pd.read_excel(file_path, sheet_name=sheet, nrows=5)
            f.write(f"Columns: {df.columns.tolist()}\n")
            f.write(df.head().to_string() + "\n")
except Exception as e:
    print("Error:", e)
