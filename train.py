import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

# 그래프 모듈 불러오기
import container
import mtcr
import utcr
import timer
from logistics_calc import run_logistics_comparison

st.write("📂 현재 실행 경로:", os.getcwd())

if os.path.exists("data"):
    st.write("📂 data 폴더 안 파일:", os.listdir("data"))
else:
    st.error("❌ data 폴더가 없습니다.")

# 페이지 설정
st.set_page_config(layout="wide")
st.title("남북통일 교통망 통합 시뮬레이션 플랫폼")

# ----------------------------
# SECTION 1~4: 그래프 출력
# ----------------------------

# 1. 통일 전후 이동시간 비교
st.header("1. 통일 전후 이동시간 비교")
timer.run()

# 2. 통일 전후 물류비용 비교
st.header("2. 통일 전후 물류비용 비교")
container.run()

# 3. 통일 전후 TCR 비교
st.header("3. 통일 전후 TCR 비교")
col1, col2 = st.columns(2)
with col1:
    mtcr.run()
with col2:
    utcr.run()

# ----------------------------
# SECTION 5: 시나리오 기반 절감액 예측
# ----------------------------

st.header("4. 통일 시나리오 기반 물류비용 절감 예측")

# 파일 경로 설정
before_path = "data/before_unification.xlsx"
after_path = "data/after_unification.xlsx"
nk_path = "data/nk_station_map.csv"

try:
    # 물류 비교 실행
    result = run_logistics_comparison(before_path, after_path, nk_path)
    time_saved = result["통일 전 시간"] - result["통일 후 시간"]
    unit_cost = 800  # 억 원/시간
    base_saving_input = time_saved * unit_cost

    # 시나리오 선택
    st.sidebar.subheader(" 시나리오 선택")
    scenario = st.sidebar.selectbox("예측 시나리오", ["보수적", "기준", "공격적"])

    growth_rate_map = {
        "보수적": 0.01,
        "기준": 0.03,
        "공격적": 0.05
    }
    growth_rate = growth_rate_map[scenario]

    # 예측 연도 설정
    forecast_years = st.sidebar.slider("예측 연도 수", 1, 15, 5)
    start_year = 2024
    years = list(range(start_year, start_year + forecast_years + 1))

    # 절감액 예측 (지수 성장 기반)
    savings = [base_saving_input * ((1 + growth_rate) ** i) for i in range(len(years))]
    df_forecast = pd.DataFrame({"연도": years, "절감액(억원)": savings}).set_index("연도")

    # 시각화
    st.subheader(" 예측 결과 시각화 (시나리오 반영)")
    st.line_chart(df_forecast)

    # 예측 테이블
    st.subheader(" 예측 데이터 테이블")
    st.dataframe(df_forecast.style.format("{:.2f}"))

except FileNotFoundError as e:
    st.error(f"❌ 파일을 찾을 수 없습니다: {e.filename}")
except Exception as e:
    st.error(f"❌ 예측 중 오류 발생: {e}")
