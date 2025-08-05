import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import sys

# 🚨 절대 경로로 NanumGothic.ttf 지정
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NanumGothic.ttf")

def set_korean_font():
    # 디버그: 경로와 파일 존재 여부 로그 출력
    print(f"[폰트 설정] 경로: {FONT_PATH}")
    print(f"[폰트 설정] 존재 여부: {os.path.exists(FONT_PATH)}")

    if not os.path.exists(FONT_PATH):
        # 파일 없으면 현재 작업 경로와 하위 파일 출력해서 디버깅
        print("[폰트 설정] ❌ NanumGothic.ttf 파일 없음!")
        print("[폰트 설정] 현재 작업 경로:", os.getcwd())
        print("[폰트 설정] 현재 폴더 파일 목록:", os.listdir(os.getcwd()))
        print("[폰트 설정] sys.path:", sys.path)
        return  # 기본 폰트 유지

    try:
        fontprop = fm.FontProperties(fname=FONT_PATH)
        font_name = fontprop.get_name()
        plt.rcParams['font.family'] = font_name
        plt.rcParams['axes.unicode_minus'] = False
        print(f"[폰트 설정] ✅ '{font_name}' 폰트 적용 완료")
    except Exception as e:
        print(f"[폰트 설정] ⚠️ 폰트 적용 실패: {e}")
