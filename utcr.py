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

    # ✅ 컬럼 확인
    if "구분" not in df.columns or "총 비용(USD)" not in df.columns:
        st.error("❌ 엑셀 컬럼명이 올바르지 않습니다. '구분', '총 비용(USD)' 컬럼이 필요합니다.")
        st.dataframe(df.head())
        return

    labels = df['구분'].tolist()
    costs = df['총 비용(USD)'].tolist()

    # 📊 그래프
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, costs, color=['#ff6b6b', '#4dabf7'])

    ax.set_ylim(0, max(costs) * 1.2)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        text = f"${height:,.0f}"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height * 1.01,
            text,
            ha='center',
            va='bottom',
            fontsize=11
        )

    ax.set_title('통일전/후 총 물류비용 비교', fontsize=14)
    ax.set_ylabel('총 물류비용 (USD)', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()

    # ✅ Streamlit 출력
    st.pyplot(fig)
    plt.close(fig)

    # 📄 그래프와 같은 값만 요약표로 표시
    df_compare = pd.DataFrame({
        "구분": df["구분"],
        "총 물류비용 (USD)": df["총 비용(USD)"]
    })
    st.dataframe(df_compare)
