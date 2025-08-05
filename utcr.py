import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.font_manager as fm

# ✅ 폰트 경로 설정
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NanumGothic.ttf")

def set_korean_font():
    """NanumGothic 폰트 적용"""
    if os.path.exists(FONT_PATH):
        fm.fontManager.addfont(FONT_PATH)
        font_name = fm.FontProperties(fname=FONT_PATH).get_name()
        plt.rcParams["font.family"] = font_name
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

def run():
    # 📌 폰트 적용
    set_korean_font()

    # ✅ 파일 경로 (네가 업로드한 이름 그대로 사용)
    file_before = "data/이동_tcr통일전.xlsx"
    file_after = "data/이동_tcr통일후.xlsx"

    # ✅ 데이터 불러오기
    df_before = pd.read_excel(file_before)
    df_after = pd.read_excel(file_after)

    # ✅ 컬럼명 확인 후 맞춰주기 (불필요한 공백 제거)
    df_before.columns = df_before.columns.str.strip()
    df_after.columns = df_after.columns.str.strip()

    # ✅ 물류비 합계 계산
    total_before = df_before["총물류비용(USD)"].sum()
    total_after = df_after["총물류비용(USD)"].sum()

    # ✅ 비교 DataFrame 생성
    df_compare = pd.DataFrame({
        "구분": ["통일 전(해상+TCR)", "통일 후(경의선+TCR)"],
        "총물류비용(USD)": [total_before, total_after]
    })

    # 📊 시각화
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#ff9999", "#66b3ff"]
    bars = ax.bar(df_compare["구분"], df_compare["총물류비용(USD)"], color=colors)

    # 바 위에 값 표시
    for bar, value in zip(bars, df_compare["총물류비용(USD)"]):
        ax.text(bar.get_x() + bar.get_width()/2, value,
                f"${value:,.0f}", ha='center', va='bottom', fontsize=10, fontweight="bold")

    ax.set_title("통일 전후 총 물류비용 비교", fontsize=14, fontweight="bold")
    ax.set_ylabel("총 물류비용 (USD)", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)
    plt.close(fig)

    # 데이터프레임 출력
    st.dataframe(df_compare)

if __name__ == "__main__":
    run()
