import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ NanumGothic 한글 폰트 적용
font_path = "/mnt/data/NanumGothic.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False

# ✅ 기본 카테고리
categories = ["교통", "쇼핑", "식비", "여가", "카페"]

# ✅ 세션 상태 초기화
if "data" not in st.session_state:
    st.session_state.data = {}

# ✅ 제목
st.title("💳 월간 소비 분석 자산 조언 시스템")

# ✅ 월 선택
selected_month = st.selectbox("📅 지출 월을 선택하세요", [f"{i}월" for i in range(1, 13)])

# ✅ 선택한 월의 기존 데이터 가져오기 (없으면 기본값 0)
month_data = st.session_state.data.get(selected_month, {cat: 0 for cat in categories})

# ✅ 지출 입력
st.subheader(f"💰 {selected_month} 지출 입력")
updated_data = {}
cols = st.columns(len(categories))
for idx, cat in enumerate(categories):
    updated_data[cat] = cols[idx].number_input(f"{cat} 지출 (원)", min_value=0, value=month_data.get(cat, 0), key=f"{selected_month}_{cat}")

# ✅ 저장 버튼
if st.button("💾 저장"):
    st.session_state.data[selected_month] = updated_data
    st.success(f"{selected_month} 지출 내역이 저장되었습니다.")

# ✅ 초기화 버튼
if st.button("🔄 모든 데이터 초기화"):
    st.session_state.data = {}
    st.experimental_rerun()

# ✅ 데이터 존재 시 시각화
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data).T
    df.index.name = "월"
    df = df.sort_index()
    
    # ✅ 월별 소비 비교 그래프
    st.markdown("### 📊 월별 지출 비교")
    fig, ax = plt.subplots(figsize=(10, 5))
    df.plot(kind="bar", ax=ax)
    ax.set_ylabel("지출 금액", fontproperties=fontprop)
    ax.set_xlabel("카테고리", fontproperties=fontprop)
    ax.set_xticklabels(df.columns, rotation=0, fontproperties=fontprop)
    ax.legend(title="월", prop=fontprop)
    st.pyplot(fig)

    # ✅ 연간 평균 소비 그래프
    st.markdown("### 📉 연간 평균 지출")
    avg_df = df.mean().round(0)

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    bars = ax2.bar(avg_df.index, avg_df.values, color='skyblue')
    ax2.set_title("카테고리별 연간 평균 지출", fontproperties=fontprop)
    ax2.set_ylabel("지출 금액", fontproperties=fontprop)
    ax2.set_xlabel("카테고리", fontproperties=fontprop)
    ax2.set_xticks(range(len(avg_df.index)))
    ax2.set_xticklabels(avg_df.index, rotation=0, fontproperties=fontprop)
    st.pyplot(fig2)
