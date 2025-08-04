import pandas as pd
import matplotlib as mpl
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 강제 적용
def set_korean_font():
    mpl.rcParams.update(mpl.rcParamsDefault)  # 초기화

    # 1) 프로젝트 폰트 폴더 내 NanumGothic.ttf 먼저 시도
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "NanumGothic.ttf")

    # 2) macOS
    if not os.path.exists(font_path):
        mac_font = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
        if os.path.exists(mac_font):
            font_path = mac_font

    # 3) Linux
    if not os.path.exists(font_path):
        linux_font = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
        if os.path.exists(linux_font):
            font_path = linux_font

    # 4) Windows
    if not os.path.exists(font_path):
        win_font = "C:/Windows/Fonts/malgun.ttf"
        if os.path.exists(win_font):
            font_path = win_font

    # 최종 적용
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        mpl.rcParams["font.family"] = fm.FontProperties(fname=font_path).get_name()
    else:
        mpl.rcParams["font.family"] = "DejaVu Sans"

    mpl.rcParams["axes.unicode_minus"] = False

# ✅ CSV 안전 읽기
def read_csv_with_fallback(path):
    encodings = ["utf-8-sig", "utf-8", "cp949", "euc-kr", "latin1"]
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
        except Exception:
            continue
    return pd.read_csv(path, encoding="latin1", errors="ignore")

# ✅ Excel 안전 읽기
def read_excel_safe(path):
    try:
        return pd.read_excel(path, engine="openpyxl")
    except Exception:
        return pd.read_excel(path, engine="openpyxl")
