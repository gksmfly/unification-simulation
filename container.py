import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
# redeploy trigger
def run():
    mpl.rcParams['font.family'] = 'AppleGothic'
    mpl.rcParams['axes.unicode_minus'] = False

    # 파일 경로
    trade_file = 'data/통일부남북교역품목별통계20220531.csv'
    pre_file = 'data/통일전전체거리비용.xlsx'
    post_file = 'data/통일후전체거리비용.xlsx'

    # CSV 읽기
    df_trade = pd.read_csv(trade_file, encoding='cp949')

    total_weight_kg = df_trade['반입_중량(kg)'].sum()
    TEU_weight_kg = 28000
    total_TEU = math.ceil(total_weight_kg / TEU_weight_kg)

    # 통일 전 거리 데이터
    df_pre = pd.read_excel(pre_file)
    def calc_pre_cost(row):
        if row['출발역'] == '부산신항' and row['도착역'] == '칭다오항':
            return (30 * 1300) * total_TEU
        else:
            return (95000 + 384.75 * row['거리(km)']) * total_TEU
    df_pre['통일전_총비용(원)'] = df_pre.apply(calc_pre_cost, axis=1)
    total_pre_cost = df_pre['통일전_총비용(원)'].sum()

    # 통일 후 거리 데이터
    df_post = pd.read_excel(post_file)
    df_post['통일후_총비용(원)'] = df_post['거리(km)'].apply(lambda d: (5.16 * d) * total_TEU)
    total_post_cost = df_post['통일후_총비용(원)'].sum()

    saving_amount = total_pre_cost - total_post_cost
    saving_rate = (saving_amount / total_pre_cost) * 100

    summary_df = pd.DataFrame({
        '총반입중량(kg)': [total_weight_kg],
        '총TEU(올림)': [total_TEU],
        '통일전총운송비(원)': [total_pre_cost],
        '통일후총운송비(원)': [total_post_cost],
        '절감액(원)': [saving_amount],
        '절감률(%)': [saving_rate]
    })

    labels = ['통일 전', '통일 후']
    costs = [total_pre_cost / 1e8, total_post_cost / 1e8]

    fig, ax = plt.subplots(figsize=(8, 6))
    bars = ax.bar(labels, costs, color=['salmon', 'skyblue'])
    for bar, cost in zip(bars, costs):
        ax.text(bar.get_x() + bar.get_width()/2, cost + (cost * 0.01),
                f"{cost:,.0f} 억원", ha='center', va='bottom', fontsize=11, fontweight='bold')
    ax.set_title('부산 → 신의주 총 운송비 비교', fontsize=14, fontweight='bold')
    ax.set_ylabel('총 운송비 (억원)')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)
    st.dataframe(summary_df)
