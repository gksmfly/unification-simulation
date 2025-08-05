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
    distances = df['총 거리(km)'].tolist()
    times = df['총 시간(h)'].tolist()

    # 📊 그래프
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, distances, color=['#ff6b6b', '#4dabf7'])

    ax.set_ylim(9000, 11500)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        time_h = times[i]
        hh = int(time_h)
        mm = int(round((time_h - hh) * 60))
        text = f"{height:,.0f} km\n({hh}h {mm}m)"
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height * 1.01,
            text,
            ha='center',
            va='bottom',
            fontsize=11
        )

    ax.set_title('통일 전후 MTCR 비교', fontsize=14)
    ax.set_ylabel('총 이동 거리 (km)', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()

    # ✅ Streamlit 출력
    st.pyplot(fig)
    plt.close(fig)

    # 📄 데이터프레임 표시
    st.dataframe(df)
