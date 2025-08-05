import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 함수 밖에서 FONT_PATH 먼저 정의
FONT_PATH = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")

# ✅ 디버그용 로그 (Streamlit Cloud 로그에서 확인 가능)
print("폰트 경로:", FONT_PATH, "존재 여부:", os.path.exists(FONT_PATH))

def set_korean_font():
    """
    Matplotlib 그래프에서 한글이 깨지지 않도록 NanumGothic.ttf 폰트를 적용하는 함수
    """
    if not os.path.exists(FONT_PATH):
        raise FileNotFoundError(f"폰트 파일을 찾을 수 없습니다: {FONT_PATH}")

    fontprop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = fontprop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
