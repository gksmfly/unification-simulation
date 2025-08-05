import pandas as pd
import os

def read_excel_safe(path):
    """엑셀 파일 안전하게 읽기"""
    try:
        return pd.read_excel(path)
    except FileNotFoundError:
        raise
    except Exception as e:
        raise RuntimeError(f"엑셀 파일 읽기 실패: {path} ({e})")

def read_csv_with_fallback(path):
    """CSV 파일 인코딩 자동 감지 후 읽기"""
    try_encodings = ["utf-8-sig", "cp949", "euc-kr"]
    ext = os.path.splitext(path)[-1].lower()
    for enc in try_encodings:
        try:
            if ext == ".csv":
                return pd.read_csv(path, encoding=enc)
        except Exception:
            continue
    raise RuntimeError(f"CSV 파일 읽기 실패: {path}")
