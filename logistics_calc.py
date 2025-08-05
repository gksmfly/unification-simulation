import streamlit as st
import pandas as pd
import os

# ---------------------------
# 기존 run_logistics_comparison 함수
# ---------------------------
def run_logistics_comparison(before_path, after_path, nk_path):
    def load_excel_or_csv(path):
        ext = os.path.splitext(path)[-1]
        try_encodings = ["utf-8-sig", "cp949", "euc-kr"]
        for enc in try_encodings:
            try:
                if ext == ".xlsx":
                    return pd.read_excel(path)
                elif ext == ".csv":
                    return pd.read_csv(path, encoding=enc)
            except Exception:
                continue
        raise FileNotFoundError(f"파일을 열 수 없습니다: {path}")

    nk_df = load_excel_or_csv(nk_path)
    if not all(col in nk_df.columns for col in ["지명", "X좌표", "Y좌표"]):
        raise ValueError("❌ 북한 파일에는 '지명', 'X좌표', 'Y좌표' 컬럼이 포함되어야 합니다.")

    def calculate_total_time(df, label):
        required_cols = ["출발역", "도착역", "거리(km)", "속도(km/h)"]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"❌ '{label}' 파일에 '{col}' 컬럼이 없습니다.")
        df["거리(km)"] = pd.to_numeric(df["거리(km)"], errors="coerce")
        df["속도(km/h)"] = pd.to_numeric(df["속도(km/h)"], errors="coerce")
        df.dropna(subset=["거리(km)", "속도(km/h)"], inplace=True)
        df["시간(h)"] = df["거리(km)"] / df["속도(km/h)"]
        total_time = df["시간(h)"].sum()
        return round(total_time, 2)

    before_df = load_excel_or_csv(before_path)
    before_total_time = calculate_total_time(before_df, "통일 전")

    after_df = load_excel_or_csv(after_path)
    after_total_time = calculate_total_time(after_df, "통일 후")

    return {
        "통일 전 시간": before_total_time,
        "통일 후 시간": after_total_time,
        "절감 시간": round(before_total_time - after_total_time, 2)
    }

# ---------------------------
# Streamlit UI 시작
# ---------------------------
st.title("5. 통일 시나리오 기반 물류비용 절감 예측")

# 파일 경로 (환경에 맞게 수정)
before_path = "data/before_unification.xlsx"
after_path = "data/after_unification.xlsx"
nk_path = "data/nk_station_map.csv"

try:
    result = run_logistics_comparison(before_path, after_path, nk_path)

    # ---------------------------
    # 기존 시나리오 선택 부분 (주석 처리)
    # ---------------------------
    # st.sidebar.subheader(" 시나리오 선택")
    # scenario = st.sidebar.selectbox("예측 시나리오", ["보수적", "기준", "공격적"])
    # growth_rate_map = {
    #     "보수적": 0.01,
    #     "기준": 0.03,
    #     "공격적": 0.05
    # }
    # growth_rate = growth_rate_map[scenario]
    # forecast_years = st.sidebar.slider("예측 연도 수", 1, 15, 5)

    # ---------------------------
    # 새 입력 UI
    # ---------------------------
    st.sidebar.header("예측 시나리오 입력")
    base_saving_input = st.sidebar.number_input("기준 절감액 (억원)", value=50000, step=1000)
    growth_rate = st.sidebar.slider("연평균 물류 수요 증가율 (%)", 0.0, 10.0, 2.0) / 100
    forecast_years = st.sidebar.slider("예측 연도 수", 1, 15, 5)

    # 시작 연도 고정
    start_year = 2024
    years = list(range(start_year, start_year + forecast_years + 1))

    # 절감액 예측 계산
    savings = [base_saving_input * ((1 + growth_rate) ** i) for i in range(len(years))]
    df_forecast = pd.DataFrame({"연도": years, "절감액(억원)": savings})

    # ---------------------------
    # 시각화
    # ---------------------------
    st.subheader("📈 예측 결과 시각화")
    st.line_chart(df_forecast.set_index("연도"))

    st.subheader("📋 예측 데이터 테이블")
    st.dataframe(df_forecast.style.format("{:.2f}"))

except FileNotFoundError as e:
    st.error(f"❌ 파일을 찾을 수 없습니다: {e.filename}")
except Exception as e:
    st.error(f"❌ 예측 중 오류 발생: {e}")
