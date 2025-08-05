import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from common_font import set_korean_font
from data_utils import read_excel_safe

def run():
    # 📌 한글 폰트 적용
    set_korean_font()

    # 📂 데이터 불러오기
    df_before = read_excel_safe("data/cost_before.xlsx")
    df_after = read_excel_safe("data/cost_after.xlsx")

    # ✅ 총 물류비용 계산
    total_before = df_before["총물류비용(USD)"].sum()
    total_after = df_after["총물류비용(USD)"].sum()

    # 📊 시각화 데이터
    labels = ["통일 전(해상+TCR)", "통일 후(경의선+TCR)"]
    values = [total_before, total_after]
    colors = ["#f28b82", "#aecbfa"]

    # 📊 그래프 그리기
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values, color=colors)

    # 막대 위에 값 표시
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + (value * 0.01),
            f"${value:,.0f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold"
        )

    # 그래프 스타일
    ax.set_title("통일 전후 총 물류비용 비교", fontsize=14, fontweight="bold")
    ax.set_ylabel("총 물류비용 (USD)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    fig.tight_layout()

    # Streamlit 출력
    st.pyplot(fig)
    plt.close(fig)

    # 📄 데이터프레임 출력
    df_compare = pd.DataFrame({
        "구분": ["통일 전(해상+TCR)", "통일 후(경의선+TCR)"],
        "총 물류비용(USD)": [total_before, total_after]
    })
    st.dataframe(df_compare)

if __name__ == "__main__":
    run()
