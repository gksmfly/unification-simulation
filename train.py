import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import folium
from streamlit_folium import st_folium

# ✅ 공통 로더 & 폰트 적용
from data_utils import read_csv_with_fallback, read_excel_safe
from common_font import set_korean_font

# 그래프 모듈
import container
import mtcr
import utcr
import timer
from logistics_calc import run_logistics_comparison

# 📌 페이지 설정 & 한글 폰트 적용
st.set_page_config(layout="wide")
set_korean_font()

st.title("남북통일 교통망 통합 시뮬레이션 플랫폼")

# ----------------------------
# SECTION 1~4: 그래프 출력
# ----------------------------
st.header("1. 통일 전후 이동시간 비교")
timer.run()

st.header("2. 통일 전후 물류비용 비교")
container.run()

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

before_path = "data/before_unification.xlsx"
after_path = "data/after_unification.xlsx"
nk_path = "data/nk_station_map.csv"

try:
    result = run_logistics_comparison(before_path, after_path, nk_path)
    time_saved = result["통일 전 시간"] - result["통일 후 시간"]
    unit_cost = 800  # 억 원/시간
    default_base_saving = time_saved * unit_cost

    with st.sidebar:
        st.sidebar.subheader("물류비용 절감액 성장률 시나리오")
        st.markdown("""
        **이 시나리오는 무엇인가요?**  
        - 통일 이후 물류 인프라 개선, 경로 최적화, 운송 속도 향상 등으로  
          **물류비용 절감액이 매년 얼마나 증가할지**에 대한 가정입니다.  
        - 값이 높을수록 절감액 증가 속도가 빠릅니다.
        """)
        
        scenario = st.selectbox(
            "성장률 시나리오 선택",
            ["성장률 1% (완만한 개선)", "성장률 3% (보통 개선)", "성장률 5% (빠른 개선)"]
        )
        growth_rate_map = {
            "성장률 1% (완만한 개선)": 0.01,
            "성장률 3% (보통 개선)": 0.03,
            "성장률 5% (빠른 개선)": 0.05
        }
        growth_rate = growth_rate_map[scenario]

        forecast_years = st.slider("예측 연도 수", 1, 15, 5)

    start_year = 2025
    years = list(range(start_year, start_year + forecast_years + 1))

    savings = [default_base_saving * ((1 + growth_rate) ** i) for i in range(len(years))]
    df_forecast = pd.DataFrame({"연도": years, "절감액(억원)": savings}).set_index("연도")

    st.subheader("예측 결과 시각화")
    st.line_chart(df_forecast)

    st.subheader("예측 데이터 테이블")
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
    df_pre = pd.read_excel("data/busan_qingdao_searoutes.xlsx")
    df_post = pd.read_excel("data/Post_unification_coordinates.xlsx")

    if "위도(x)" in df_post.columns:
        df_post = df_post.rename(columns={"위도(x)": "위도", "경도(y)": "경도"})

    m = folium.Map(location=[37.5, 127.5], zoom_start=5)

    coords_pre = df_pre[["위도", "경도"]].values.tolist()
    folium.PolyLine(coords_pre, color="red", weight=4, tooltip="통일 전 경로").add_to(m)
    for lat, lon in coords_pre:
        folium.CircleMarker(location=[lat, lon], radius=1, color="red", fill=True).add_to(m)

    coords_post = df_post[["위도", "경도"]].values.tolist()
    folium.PolyLine(coords_post, color="blue", weight=4, tooltip="통일 후 경로").add_to(m)
    for lat, lon in coords_post:
        folium.CircleMarker(location=[lat, lon], radius=1, color="blue", fill=True).add_to(m)

    st_folium(m, width=900, height=600)

except FileNotFoundError as e:
    st.error(f"❌ 경로 데이터 파일을 찾을 수 없습니다: {e.filename}")
except Exception as e:
    st.error(f"❌ 지도 시각화 중 오류 발생: {e}")
