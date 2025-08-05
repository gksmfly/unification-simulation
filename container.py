import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt

# ✅ 공통 폰트 설정 불러오기
from common_font import set_korean_font

# ✅ 데이터 로딩 함수
def read_excel_safe(path):
    """엑셀 파일 안전하게 읽기"""
    try:
        return pd.read_excel(path)
    except FileNotFoundError:
        raise
    except Exception as e:
        raise RuntimeError(f"엑셀 파일 읽기 실패: {path} ({e})")

def read_csv_with_fallback(path):
    """CSV 파일 인코딩 자동 감지 후 읽기"""
    try_encodings = ["utf-8-sig", "cp949", "euc-kr"]
    for enc in try_encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception:
            continue
    raise RuntimeError(f"CSV 파일 읽기 실패: {path}")

def run():
    # 📌 그래프 그리기 전에 한 번만 폰트 적용
    set_korean_font()

    # 📂 파일 경로
    trade_file = 'data/trade_items_20220531.csv'
    pre_file = 'data/cost_before.xlsx'
    post_file = 'data/cost_after.xlsx'

    # ✅ CSV 안전하게 읽기
    df_trade = read_csv_with_fallback(trade_file)

    # 총 중량 & TEU 계산
    total_weight_kg = df_trade['반입_중량(kg)'].sum()
    TEU_weight_kg = 28000
    total_TEU = math.ceil(total_weight_kg / TEU_weight_kg)

    # ✅ 통일 전 거리 데이터
    df_pre = read_excel_safe(pre_file)

    def calc_pre_cost(row):
        if row['출발역'] == '부산신항' and row['도착역'] == '칭다오항':
            return (30 * 1300) * total_TEU  # 해상 운임
        else:
            return (95000 + 384.75 * row['거리(km)']) * total_TEU  # 철도 운임

    df_pre['통일전_총비용(원)'] = df_pre.apply(calc_pre_cost, axis=1)
    total_pre_cost = df_pre['통일전_총비용(원)'].sum()

    # ✅ 통일 후 거리 데이터
    df_post = read_excel_safe(post_file)
    df_post['통일후_총비용(원)'] = df_post['거리(km)'].apply(lambda d: (5.16 * d) * total_TEU)
    total_post_cost = df_post['통일후_총비용(원)'].sum()

    # 절감액 & 절감률
    saving_amount = total_pre_cost - total_post_cost
    saving_rate = (saving_amount / total_pre_cost) * 100

    # 요약 데이터프레임
    summary_df = pd.DataFrame({
        '총반입중량(kg)': [total_weight_kg],
        '총TEU(올림)': [total_TEU],
        '통일전총운송비(원)': [total_pre_cost],
        '통일후총운송비(원)': [total_post_cost],
        '절감액(원)': [saving_amount],
        '절감률(%)': [saving_rate]
    })

    # 시각화 데이터
    labels = ['통일 전', '통일 후']
    costs = [total_pre_cost / 1e8, total_post_cost / 1e8]  # 억 원 단위

    # 📊 시각화
    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(labels, costs, color=['#ff6b6b', '#4dabf7'])  # 좀 더 진한 빨강/파랑

    for bar, cost in zip(bars, costs):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            cost + (cost * 0.01),
            f"{cost:,.0f} 억원",
            ha='center', va='bottom',
            fontsize=11, fontweight='bold'
        )

    ax.set_title('부산 → 신의주 총 운송비 비교', fontsize=14, fontweight='bold')
    ax.set_ylabel('총 운송비 (억원)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # 출력
    st.pyplot(fig)
    plt.close(fig)
    st.dataframe(summary_df)
