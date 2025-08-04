import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 설정
def set_korean_font():
    mpl.rcParams.update(mpl.rcParamsDefault)  # 초기화

    font_path = None
    if os.path.exists('/System/Library/Fonts/Supplemental/AppleGothic.ttf'):
        font_path = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'  # macOS
    elif os.path.exists('/usr/share/fonts/truetype/nanum/NanumGothic.ttf'):
        font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # Linux
    elif os.path.exists('C:/Windows/Fonts/malgun.ttf'):
        font_path = 'C:/Windows/Fonts/malgun.ttf'  # Windows

    if font_path:
        fm.fontManager.addfont(font_path)
        mpl.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
    else:
        mpl.rcParams['font.family'] = 'DejaVu Sans'

    mpl.rcParams['axes.unicode_minus'] = False

# ✅ CSV 안전하게 읽기
def read_csv_with_fallback(path):
    encodings = ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr', 'latin1']
    for enc in encodings:
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
