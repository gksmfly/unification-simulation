import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 1. 폰트 파일 경로 지정 (Python 파일과 같은 위치에 있는 경우)
FONT_PATH = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")
fontprop = fm.FontProperties(fname=FONT_PATH)

# 2. Matplotlib 전역 폰트 설정
plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False
