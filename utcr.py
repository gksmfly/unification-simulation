import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import os

def run():
    # 폰트 설정
    if platform.system() == 'Darwin':
        font_path = '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
    elif platform.system() == 'Windows':
        font_path = 'C:/Windows/Fonts/malgun.ttf'
    else:
        font_path = '/usr/share/fonts/truetype/nanum/NanumGothicCoding.ttf'
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        plt.rc('font', family=fm.FontProperties(fname=font_path).get_name())
    plt.rcParams['axes.unicode_minus'] = False

    # 데이터 불러오기
    df = pd.read_excel('data/물류_utcr.xlsx')

    labels = df['구분'].tolist()
    distances = df['총 거리(km)'].tolist()
    times = df['총 시간(h)'].tolist()

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, distances, color=['#FFCC99', '#99FF99'])

    ax.set_ylim(9000, 11500)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        time_h = times[i]
        hh = int(time_h)
        mm = int(round((time_h - hh) * 60))
        text = f"{height:,.0f} km\n({hh}h {mm}m)"
        ax.text(bar.get_x() + bar.get_width() / 2,
                height * 1.01,
                text,
                ha='center', va='bottom', fontsize=11)

    ax.set_title('통일 후 UTCR 비교', fontsize=14)
    ax.set_ylabel('총 이동 거리 (km)', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()

    st.pyplot(fig)
    st.dataframe(df)
