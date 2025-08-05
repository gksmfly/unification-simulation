import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 📌 NanumGothic 폰트 경로
FONT_PATH = os.path.join(os.path.dirname(__file__), "NanumGothic.ttf")

def set_korean_font():
    """
    Matplotlib 그래프에서 한글이 깨지지 않도록
    NanumGothic.ttf 폰트를 적용하는 안전한 함수
    (Streamlit Cloud 환경 대응)
    """
    try:
        if os.path.exists(FONT_PATH):
            # 폰트 파일 경로에서 폰트 속성 불러오기
            fontprop = fm.FontProperties(fname=FONT_PATH)
            font_name = fontprop.get_name()
            # 디버그 로그 (Cloud에서 View logs로 확인 가능)
            print(f"✅ NanumGothic 폰트 적용: {font_name}")
            plt.rcParams.update({
                'font.family': font_name,
                'axes.unicode_minus': False
            })
        else:
            # 폰트 파일이 없으면 기본 폰트로 fallback
            print(f"⚠️ NanumGothic.ttf 파일 없음 → 기본 폰트 사용")
            plt.rcParams.update({
                'font.family': 'DejaVu Sans',
                'axes.unicode_minus': False
            })
    except Exception as e:
        # 예기치 못한 오류 발생 시에도 기본 폰트 적용
        print(f"❌ 폰트 설정 중 오류 발생: {e} → 기본 폰트 사용")
        plt.rcParams.update({
            'font.family': 'DejaVu Sans',
            'axes.unicode_minus': False
        })
import os
print("폰트 경로:", FONT_PATH, "존재 여부:", os.path.exists(FONT_PATH))
