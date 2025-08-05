import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ✅ 공통 폰트 적용
from common_font import set_korean_font
from data_utils import read_excel_safe

def run():
    # 📌 폰트 적용
    set_korean_font()

    # 📂 데이터 불러오기
    df = read_excel_safe("data/logistics_tcr.xlsx")

    labels = df['구분'].tolist()
    costs = df['총 비용(USD)'].tolist()

    # 📊 그래프
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, costs, color=['#FF9999', '#99CCFF'])

    ax.set_ylim(min(costs) * 0.95, max(costs) * 1.05)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        text = f"{height:,.0f} USD"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height * 1.01,
            text,
            ha='center',
            va='bottom',
            fontsize=11
        )

    ax.set_title('통일 전후 UTCR 비교', fontsize=14)
    ax.set_ylabel('총 비용 (USD)', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()

    # ✅ Streamlit 출력
    st.pyplot(fig)
    plt.close(fig)

    # 📄 데이터프레임 표시
    st.dataframe(df)
