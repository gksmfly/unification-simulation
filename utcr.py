import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 폰트 경로 (GitHub 환경)
FONT_PATH = os.path.join("data", "NanumGothic.ttf")

# 📌 한글 폰트 설정
if os.path.exists(FONT_PATH):
    fm.fontManager.addfont(FONT_PATH)
    plt.rc('font', family=fm.FontProperties(fname=FONT_PATH).get_name())
else:
    plt.rc('font', family='DejaVu Sans')  # 기본 폰트
plt.rcParams['axes.unicode_minus'] = False

def run():
    # 📂 GitHub data 폴더 내 데이터 파일 경로
    file_path = os.path.join("data", "물류_tcr.xlsx")
    
    if not os.path.exists(file_path):
        st.error(f"❌ 데이터 파일을 찾을 수 없습니다: {file_path}")
        return
    
    # 데이터 불러오기
    df = pd.read_excel(file_path)

    # 컬럼명 맞추기
    if not {'구분', '총 비용(USD)'}.issubset(df.columns):
        st.error("❌ 데이터에 '구분' 또는 '총 비용(USD)' 컬럼이 없습니다.")
        return

    labels = df['구분'].tolist()
    costs = df['총 비용(USD)'].tolist()

    # 📊 그래프 그리기
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, costs, color=['#FF9999', '#99CCFF'])

    ax.set_ylim(0, max(costs) * 1.2)

    # 값 표시
    for i, bar in enumerate(bars):
        height = bar.get_height()
        text = f"${height:,.0f}"
        ax.text(bar.get_x() + bar.get_width() / 2,
                height * 1.01,
                text,
                ha='center', va='bottom', fontsize=11)

    ax.set_title('통일 전후 총 물류비용 비교', fontsize=14)
    ax.set_ylabel('총 물류비용 (USD)', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()

    # Streamlit에 출력
    st.pyplot(fig)
    st.dataframe(df)

if __name__ == "__main__":
    run()
