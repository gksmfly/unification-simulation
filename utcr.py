import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from common_font import set_korean_font  # 폰트 적용 함수

def run():
    set_korean_font()

    file_path = os.path.join("data", "logistics_tcr.xlsx")

    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        st.error(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        return
    except Exception as e:
        st.error(f"❌ 엑셀 읽기 오류: {e}")
        return

    # ✅ 컬럼명 검증
    if "구분" not in df.columns or "총 비용(USD)" not in df.columns:
        st.error(f"❌ 컬럼명이 일치하지 않습니다. 현재 컬럼명: {list(df.columns)}")
        st.dataframe(df.head())
        return

    # ✅ 값 추출
    labels = df["구분"].tolist()
    costs = df["총 비용(USD)"].tolist()

    # 📊 시각화
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, costs, color=['#FF9999', '#99CCFF'])
    ax.set_ylim(0, max(costs) * 1.2)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height * 1.01,
                f"${height:,.0f}", ha='center', va='bottom', fontsize=11)

    ax.set_title("통일 전후 총 물류비용 비교", fontsize=14)
    ax.set_ylabel("총 물류비용 (USD)", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(df)

if __name__ == "__main__":
    run()
