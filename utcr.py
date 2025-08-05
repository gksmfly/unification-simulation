import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from common_font import set_korean_font  # ✅ 폰트 적용 모듈

# 📌 한글 폰트 적용
set_korean_font()

def run():
    # ✅ 데이터 파일 경로 (깃허브 data 폴더 기준)
    file_before = "data/이동_tcr통일전.xlsx"
    file_after = "data/이동_tcr통일후.xlsx"

    # ✅ 엑셀 불러오기
    df_before = pd.read_excel(file_before)
    df_after = pd.read_excel(file_after)

    # 🔍 컬럼명 확인 후 맞게 수정 (엑셀 실제 컬럼명 사용)
    # 예시: ["총 물류비용 (USD)"] <- 엑셀 파일에 실제 들어있는 값
    total_before = df_before["총 물류비용 (USD)"].sum()
    total_after = df_after["총 물류비용 (USD)"].sum()

    # ✅ 데이터프레임 구성
    df_compare = pd.DataFrame({
        "구분": ["통일 전(해상+TCR)", "통일 후(경의선+TCR)"],
        "총 물류비용 (USD)": [total_before, total_after]
    })

    # 📊 시각화
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(df_compare["구분"], df_compare["총 물류비용 (USD)"],
                  color=["#ff9999", "#66b3ff"], alpha=0.7)

    # 값 표시
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"${height:,.0f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.set_title("통일 전후 총 물류비용 비교", fontsize=14, fontweight="bold")
    ax.set_ylabel("총 물류비용 (USD)", fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()

    # ✅ Streamlit 출력
    st.pyplot(fig)
    plt.close(fig)
    st.dataframe(df_compare)

if __name__ == "__main__":
    run()
