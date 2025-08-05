import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt

# ✅ 공통 로더 적용
from common_loader import set_korean_font

# 그래프 모듈 불러오기
import container
import mtcr
import utcr
import timer
from logistics_calc import run_logistics_comparison

# folium 지도 시각화 라이브러리
import folium
from streamlit_folium import st_folium

# 초기 설정
plt.close('all')
set_korean_font()

# 페이지 설정
st.set_page_config(layout="wide")

# ✅ matplotlib 환경 초기화 + 폰트 적용
plt.rcParams.update(plt.rcParamsDefault)
set_korean_font()

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
# SECTION 4: 시나리오 기반 절감액 예측
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
    default_base_saving = time_saved * unit_cost

    st.sidebar.subheader(" 시나리오 선택")
    scenario = st.sidebar.selectbox("예측 시나리오", ["보수적", "기준", "공격적"])
    growth_rate_map = {
         "보수적": 0.01,
         "기준": 0.03,
         "공격적": 0.05
    }
    growth_rate = growth_rate_map[scenario]
    forecast_years = st.sidebar.slider("예측 연도 수", 1, 15, 5)

    # 시작 연도 고정
    start_year = 2025
    years = list(range(start_year, start_year + forecast_years + 1))

    # 절감액 예측 (지수 성장 기반)
    savings = [base_saving_input * ((1 + growth_rate) ** i) for i in range(len(years))]
    df_forecast = pd.DataFrame({"연도": years, "절감액(억원)": savings}).set_index("연도")

    # 시각화
    st.subheader("📈 예측 결과 시각화")
    st.line_chart(df_forecast)

    # 예측 테이블
    st.subheader("📋 예측 데이터 테이블")
    st.dataframe(df_forecast.style.format("{:.2f}"))

except FileNotFoundError as e:
    st.error(f"❌ 파일을 찾을 수 없습니다: {e.filename}")
except Exception as e:
    st.error(f"❌ 예측 중 오류 발생: {e}")

# ----------------------------
# SECTION 5: 실제 지도 기반 경로 시각화
# ----------------------------

st.header("5. 실제 지도 기반 경로 시각화")

try:
    # 통일 전 경로 (API 기반 해상 경로)
    df_pre = pd.read_excel("data/busan_qingdao_searoutes.xlsx")
    # 통일 후 경로 (육상 직통)
    df_post = pd.read_excel("data/Post_unification_coordinates.xlsx")

    # 컬럼 이름 맞추기 (통일 후 데이터)
    if "위도(x)" in df_post.columns:
        df_post = df_post.rename(columns={"위도(x)": "위도", "경도(y)": "경도"})

    # 지도 초기화
    m = folium.Map(location=[37.5, 127.5], zoom_start=5)

    # 통일 전 경로 (빨간색)
    coords_pre = df_pre[["위도", "경도"]].values.tolist()
    folium.PolyLine(coords_pre, color="red", weight=4, tooltip="통일 전 경로").add_to(m)
    for lat, lon in coords_pre:
        folium.CircleMarker(location=[lat, lon], radius=1, color="red", fill=True).add_to(m)

    # 통일 후 경로 (파란색)
    coords_post = df_post[["위도", "경도"]].values.tolist()
    folium.PolyLine(coords_post, color="blue", weight=4, tooltip="통일 후 경로").add_to(m)
    for lat, lon in coords_post:
        folium.CircleMarker(location=[lat, lon], radius=1, color="blue", fill=True).add_to(m)

    # 지도 출력
    st_folium(m, width=900, height=600)

except FileNotFoundError as e:
    st.error(f"❌ 경로 데이터 파일을 찾을 수 없습니다: {e.filename}")
except Exception as e:
    st.error(f"❌ 지도 시각화 중 오류 발생: {e}")
