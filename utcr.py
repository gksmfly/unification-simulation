import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ✅ 공통 폰트 설정 불러오기
from common_font import set_korean_font
from data_utils import read_excel_safe

def run():
    # 📌 폰트 적용
    set_korean_font()

    # 📂 파일 경로 (서버 실제 파일명 기준)
    file_before = "data/tcr_before.xlsx"
    file_after = "data/tcr_after.xlsx"

    # ✅ 데이터 불러오기
    df_before = read_excel_safe(file_before)
    df_after = read_excel_safe(file_after)

    # 📊 합계 계산
    total_before = df_before["총물류비용(USD)"].sum()
    total_after = df_after["총물류비용(USD)"].sum()

    # 시각화 데이터
    labels = ["통일 전(해상+TCR)", "통일 후(경의선+TCR)"]
    values = [total_before, total_after]
    colors = ["#ff9999", "#99ccff"]

    # 📊 그래프 그리기
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(labels, values, color=colors)

    # 값 표시
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value * 1.01,
            f"${value:,.0f}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold"
        )

    ax.set_title("통일 전후 총 물류비용 비교", fontsize=14, fontweight="bold")
    ax.set_ylabel("총 물류비용 (USD)")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # ✅ Streamlit 출력
    st.pyplot(fig)
    plt.close(fig)

    # 📄 표 표시
    df_compare = pd.DataFrame({
        "구분": labels,
        "총 물류비용(USD)": values
    })
    st.dataframe(df_compare)

if __name__ == "__main__":
    run()
