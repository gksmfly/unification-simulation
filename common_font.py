import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# NanumGothic.ttf 경로 (common_font.py와 같은 위치)
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NanumGothic.ttf")

def set_korean_font():
    """
    한글 폰트 설정
    - NanumGothic.ttf 있으면 적용
    - 없으면 기본 폰트로 fallback
    """
    if os.path.exists(FONT_PATH):
        try:
            # 폰트 로드 및 등록
            fm.fontManager.addfont(FONT_PATH)
            font_name = fm.FontProperties(fname=FONT_PATH).get_name()
            plt.rcParams["font.family"] = font_name
            print(f"✅ NanumGothic 적용 완료: {font_name}")
        except Exception as e:
            print(f"⚠️ NanumGothic 적용 실패 → 기본 폰트 사용 ({e})")
            plt.rcParams["font.family"] = "DejaVu Sans"
    else:
        print(f"⚠️ NanumGothic.ttf 없음 → 기본 폰트 사용")
        plt.rcParams["font.family"] = "DejaVu Sans"

    # 마이너스 기호 깨짐 방지
    plt.rcParams["axes.unicode_minus"] = False
