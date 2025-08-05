# logistics_tcr_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf'
fm.fontManager.addfont(font_path)
plt.rc('font', family='NanumGothicCoding')
plt.rcParams['axes.unicode_minus'] = False

# ✅ Streamlit 페이지 설정
st.set_page_config(page_title="TCR 물류비용 비교", layout="centered")

# 제목
st.title("📦 통일 전후 총 물류비용 비교")

# 파일 경로 (같은 디렉토리에 logistics_tcr.xlsx가 있다고 가정)
file_path = os.path.join("logistics_tcr.xlsx")

# 파일 불러오기
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.error(f"❌ 파일을 찾을 수 없습니다: {file_path}")
    st.stop()

# 데이터 확인
if "구분" not in df.columns or "총 비용(USD)" not in df.columns:
    st.error("❌ 엑셀 컬럼명이 올바르지 않습니다. '구분', '총 비용(USD)' 컬럼이 필요합니다.")
    st.dataframe(df.head())
    st.stop()

labels = df['구분'].tolist()
costs = df['총 비용(USD)'].tolist()

# 📊 matplotlib 그래프 그리기
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(labels, costs, color=['#FF9999', '#99CCFF'])

ax.set_ylim(0, max(costs) * 1.2)

# 값 표시
for i, bar in enumerate(bars):
    height = bar.get_height()
    text = f"${height:,.0f}"
    ax.text(bar.get_x() + bar.get_width()/2,
            height * 1.01,
            text,
            ha='center', va='bottom', fontsize=11)

ax.set_title('통일 전후 총 물류비용 비교', fontsize=14)
ax.set_ylabel('총 물류비용 (USD)', fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.5)

# Streamlit에서 그래프 출력
st.pyplot(fig)

# 데이터 테이블도 함께 표시
with st.expander("📄 원본 데이터 보기"):
    st.dataframe(df)
