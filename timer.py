import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import platform

# ✅ 나눔고딕 강제 적용 (없으면 설치)
def set_korean_font():
    try:
        # 나눔고딕 경로 찾기
        nanum_fonts = [f.fname for f in fm.fontManager.ttflist if 'NanumGothic' in f.name]
        if nanum_fonts:
            mpl.rcParams['font.family'] = 'NanumGothic'
        else:
            # 기본 폰트 (영문 포함)
            mpl.rcParams['font.family'] = 'DejaVu Sans'
    except:
        mpl.rcParams['font.family'] = 'DejaVu Sans'
    mpl.rcParams['axes.unicode_minus'] = False

set_korean_font()

# ✅ Haversine 거리 계산 (km)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))


# ✅ CSV 안전하게 읽기 (인코딩 자동 시도)
def read_csv_with_fallback(path):
    encodings_to_try = ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr', 'latin1']
    for enc in encodings_to_try:
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
        except Exception:
            continue
    return pd.read_csv(path, encoding='latin1', errors='ignore')


# ✅ Excel 안전하게 읽기
def read_excel_safe(path):
    try:
        return pd.read_excel(path, engine='openpyxl')
    except Exception:
        return pd.read_excel(path, engine='openpyxl')


def run():
    # 📂 파일 경로
    file_before = 'data/tongil_before.xlsx'
    file_after = 'data/tongil_after.xlsx'
    file_nk = 'data/nk_station_map.csv'

    # 1️⃣ 통일 전 데이터
    df_before = read_excel_safe(file_before)
    df_before['위도(y)'] = pd.to_numeric(df_before['위도(y)'], errors='coerce')
    df_before['경도(x)'] = pd.to_numeric(df_before['경도(x)'], errors='coerce')
    df_before['거리(km)'] = pd.to_numeric(df_before['거리(km)'], errors='coerce')

    거리_list = []
    for idx in range(len(df_before)):
        if idx + 1 >= len(df_before):
            거리_list.append(0)
            continue
        lat1, lon1 = df_before.loc[idx, ['위도(y)', '경도(x)']]
        lat2, lon2 = df_before.loc[idx + 1, ['위도(y)', '경도(x)']]
        if not np.isnan(lat1) and not np.isnan(lon1) and not np.isnan(lat2) and not np.isnan(lon2):
            dist = haversine(lat1, lon1, lat2, lon2)
        else:
            dist = np.nan
        if pd.isna(df_before.loc[idx, '거리(km)']):
            거리_list.append(dist)
        else:
            거리_list.append(df_before.loc[idx, '거리(km)'])
    df_before['거리(km)'] = 거리_list
    df_before['속도(km/h)'] = pd.to_numeric(df_before['속도(km/h)'], errors='coerce').fillna(34)
    df_before['시간(h)'] = df_before['거리(km)'] / df_before['속도(km/h)']

    # 2️⃣ 통일 후 데이터
    df_after = read_excel_safe(file_after)
    df_after['속도(km/h)'] = pd.to_numeric(df_after['속도(km/h)'], errors='coerce')
    df_after['시간(h)'] = df_after['거리(km)'] / df_after['속도(km/h)']

    # 3️⃣ 북한 구간 데이터
    df_nk = read_csv_with_fallback(file_nk)
    target_nk_stations = ['판문역', '평산역', '사리원역', '구성역', '신의주역']
    nk_filtered = df_nk[df_nk['지명'].isin(target_nk_stations)][['지명', 'Y좌표', 'X좌표']]
    nk_filtered = nk_filtered.set_index('지명').loc[target_nk_stations].reset_index()

    distances = []
    for i in range(len(nk_filtered) - 1):
        lat1, lon1 = nk_filtered.loc[i, ['Y좌표', 'X좌표']]
        lat2, lon2 = nk_filtered.loc[i + 1, ['Y좌표', 'X좌표']]
        dist_km = haversine(lat1, lon1, lat2, lon2)
        distances.append(dist_km)

    df_nk_dist = pd.DataFrame({
        '출발역': target_nk_stations[:-1],
        '도착역': target_nk_stations[1:],
        '거리(km)': distances
    })
    df_nk_dist['속도(km/h)'] = 40
    df_nk_dist['시간(h)'] = df_nk_dist['거리(km)'] / df_nk_dist['속도(km/h)']

    # 4️⃣ 데이터 합치기
    df_after_renamed = df_after.rename(columns={'출발역': '출발지', '도착역': '도착지'})
    df_after_renamed = df_after_renamed[['출발지', '도착지', '거리(km)', '속도(km/h)', '시간(h)']]

    df_nk_dist_renamed = df_nk_dist.rename(columns={'출발역': '출발지', '도착역': '도착지'})
    df_nk_dist_renamed = df_nk_dist_renamed[['출발지', '도착지', '거리(km)', '속도(km/h)', '시간(h)']]

    df_after_full = pd.concat([df_after_renamed, df_nk_dist_renamed], ignore_index=True)

    # 5️⃣ 총합 비교
    total_before_distance = df_before['거리(km)'].sum()
    total_before_time = df_before['시간(h)'].sum()
    total_after_distance = df_after_full['거리(km)'].sum()
    total_after_time = df_after_full['시간(h)'].sum()

    df_compare = pd.DataFrame({
        '구분': ['통일 전', '통일 후'],
        '총 거리(km)': [total_before_distance, total_after_distance],
        '총 시간(h)': [total_before_time, total_after_time]
    }).round(2)

    # 6️⃣ 시각화
    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(df_compare['구분'], df_compare['총 거리(km)'], color=['#ff6b6b', '#4dabf7'], width=0.6)

    for i, bar in enumerate(bars):
        height = bar.get_height()
        time_val = df_compare['총 시간(h)'][i]
        hh = int(time_val)
        mm = int(round((time_val - hh) * 60))
        ax.text(bar.get_x() + bar.get_width() / 2, height + 50,
                f"{hh}h {mm}m",
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    ax.set_ylabel('이동거리 (km)', fontsize=13)
    ax.set_xlabel('구분', fontsize=13)
    ax.set_title('부산 → 신의주 이동거리 / 소요시간 비교', fontsize=15, fontweight='bold')
    ax.set_ylim(0, max(df_compare['총 거리(km)']) * 1.2)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()

    # Streamlit 출력
    st.subheader("📊 부산 → 신의주 이동거리 및 소요시간 비교")
    st.pyplot(fig)
    st.dataframe(df_compare)


if __name__ == "__main__":
    run()
