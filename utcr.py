import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ✅ 공통 폰트 적용
from common_font import set_korean_font

def run():
    # 📌 폰트 적용
    set_korean_font()

    # 📂 GitHub data 폴더 경로
    file_path = os.path.join("data", "logistics_tcr.xlsx")  # 파일명 확인 필요

    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        st.error(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        return
    except Exception as e:
        st.error(f"❌ 엑셀 파일 읽기 오류: {e}")
        return

    # ✅ 정확한 컬럼명 확인
    expected_cols = ["구분", "총 비용(USD)"]
    for col in expected_cols:
        if col not in df.columns:
            st.error(f"❌ 엑셀 컬럼명이 올바르지 않습니다. 현재 컬럼명:
