import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 절대 경로 생성
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NanumGothic.ttf")

def set_korean_font():
    """Matplotlib 그래프에서 한글 폰트 적용"""
    if os.path.exists(FONT_PATH):
        fontprop = fm.FontProperties(fname=FONT_PATH)
        plt.rcParams['font.family'] = fontprop.get_name()
        plt.rcParams['axes.unicode_minus'] = False
        print(f"✅ 한글 폰트 적용 완료: {fontprop.get_name()}")
    else:
        print(f"❌ NanumGothic.ttf 파일을 찾을 수 없습니다: {FONT_PATH}")
