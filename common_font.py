import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

FONT_PATH = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")

def set_korean_font():
    if os.path.exists(FONT_PATH):
        fontprop = fm.FontProperties(fname=FONT_PATH)
        font_name = fontprop.get_name()
        print(f"✅ 폰트 적용: {font_name}")
        plt.rcParams.update({
            'font.family': font_name,
            'axes.unicode_minus': False
        })
    else:
        print("⚠️ NanumGothic.ttf 찾지 못함 → 기본 폰트 적용")
        plt.rcParams.update({
            'font.family': 'DejaVu Sans',
            'axes.unicode_minus': False
        })
