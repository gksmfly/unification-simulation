import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 절대 경로로 NanumGothic.ttf 지정
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NanumGothic.ttf")

def set_korean_font():
    print(f"[폰트 설정] 경로: {FONT_PATH}")
    print(f"[폰트 설정] 존재 여부: {os.path.exists(FONT_PATH)}")

    if not os.path.exists(FONT_PATH):
        print("[폰트 설정] ❌ NanumGothic.ttf 없음, 기본 폰트 사용")
        return

    try:
        # 💡 절대 경로를 직접 적용
        plt.rcParams['font.family'] = fm.FontProperties(fname=FONT_PATH).get_name()
        plt.rcParams['axes.unicode_minus'] = False
        print(f"[폰트 설정] ✅ '{plt.rcParams['font.family']}' 적용 완료")
    except Exception as e:
        print(f"[폰트 설정] ⚠️ 적용 실패: {e}")
