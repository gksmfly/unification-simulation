# common_loader.py
import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as fm

# ✅ CSV 안전하게 읽기 (cp949 제거)
def read_csv_with_fallback(path):
    encodings_to_try = ['utf-8-sig', 'utf-8', 'euc-kr', 'latin1']
    for enc in encodings_to_try:
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
        except Exception:
            continue
    return pd.read_csv(path, encoding='latin1', errors='ignore')

# ✅ Excel 안전하게 읽기
def read_excel_safe(path):
    try:
        return pd.read_excel(path, engine='openpyxl')
    except Exception:
        return pd.read_excel(path, engine='openpyxl')

# ✅ 한글 폰트 설정 (AppleGothic 완전 제거)
def set_korean_font():
    available_fonts = set(f.name for f in fm.fontManager.ttflist)
    if "NanumGothic" in available_fonts:
        mpl.rcParams['font.family'] = 'NanumGothic'
    else:
        mpl.rcParams['font.family'] = 'DejaVu Sans'
    mpl.rcParams['axes.unicode_minus'] = False

# 실행 시 바로 폰트 세팅
set_korean_font()
