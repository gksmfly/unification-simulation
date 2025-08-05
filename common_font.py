import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 절대 경로로 NanumGothic.ttf 지정
FONT_PATH = os.path.abspath("NanumGothic.ttf")

def set_korean_font():
    if os.path.exists(FONT_PATH):
        fontprop = fm.FontProperties(fname=FONT_PATH)
        plt.rcParams['font.family'] = fontprop.get_name()
        plt.rcParams['axes.unicode_minus'] = False
        print(f"✅ 폰트 적용: {FONT_PATH}")
    else:
        print(f"❌ NanumGothic.ttf 파일을 찾을 수 없습니다: {FONT_PATH}")
