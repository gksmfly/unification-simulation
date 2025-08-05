import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

def set_korean_font():
    """
    Matplotlib 그래프에서 한글이 깨지지 않도록
    NanumGothic.ttf 폰트를 적용하는 함수
    """
    FONT_PATH = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")

    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError(f"폰트 파일을 찾을 수 없습니다: {FONT_PATH}")

    fontprop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = fontprop.get_name()
    plt.rcParams['axes.unicode_minus'] = False

print("폰트 경로:", FONT_PATH, "존재 여부:", os.path.exists(FONT_PATH))
