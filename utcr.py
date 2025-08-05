import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from common_font import set_korean_font  # 폰트 적용 함수

set_korean_font()

def run():
    file_before = "data/이동_tcr통일전.xlsx"
    file_after = "data/이동_tcr통일후.xlsx"

    df_before = pd.read_excel(file_before)
    df_after = pd.read_excel(file_after)

    # 🔍 컬럼명 확인용 출력
    st.write("통일 전 데이터 컬럼:", df_before.columns.tolist())
    st.write("통일 후 데이터 컬럼:", df_after.columns.tolist())

    # ⚠️ 여기서 실제 컬럼명에 맞게 수정하세요
    cost_col = "총 물류비용(USD)"  # 엑셀에 있는 정확한 컬럼명으로 변경

    total_before = df_before[cost_col].sum()
    total_after = df_after[cost_col].sum()

    df_compare = pd.DataFrame({
        "구분": ["통일 전(해상+TCR)", "통일 후(경의선+TCR)"],
        cost_col: [total_before, total_after]
    })

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(df_compare["구분"], df_compare[cost_col],
                  color=["#ff9999", "#66b3ff"], alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"${height:,.0f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.set_title("통일 전후 총 물류비용 비교", fontsize=14, fontweight="bold")
    ax.set_ylabel(cost_col, fontsize=12)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)
    st.dataframe(df_compare)

if __name__ == "__main__":
    run()
