import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 설정 (NanumGothic)
font_path = "NanumGothic-Bold.ttf"
fontprop = fm.FontProperties(fname=font_path, size=12)
plt.rcParams['font.family'] = fontprop.get_name()
plt.rcParams['axes.unicode_minus'] = False

DATA_FILE = "monthly_spending.csv"
categories = ["교통", "쇼핑", "식비", "여가", "카페"]

# ✅ UI
st.title("💳 월별 지출 분석 + 연간 평균")
st.sidebar.header("🔧 설정")
month = st.sidebar.selectbox("📅 월 선택", [f"{i}월" for i in range(1, 13)])
budget = st.sidebar.slider("💰 월 예산 (원)", 100000, 1000000, 300000, step=50000)

# ✅ 지출 입력
st.subheader(f"📊 {month} 소비 내역 입력")
spending = {}
for cat in categories:
    spending[cat] = st.number_input(f"{cat} 지출 (원)", min_value=0, step=1000, key=cat)

if st.button("저장 및 분석"):
    df_new = pd.DataFrame([{"month": month, "category": k, "amount": v} for k, v in spending.items()])
    if os.path.exists(DATA_FILE):
        df_old = pd.read_csv(DATA_FILE)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new
    df_all.to_csv(DATA_FILE, index=False)
    st.success(f"{month} 데이터가 저장되었습니다!")

# ✅ 초기화
if st.button("초기화"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        st.success("모든 지출 데이터가 초기화되었습니다.")

# ✅ 시각화
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)

    # 최근 월 비교 그래프
    st.subheader("📈 월별 지출 비교")
    pivot = df.pivot_table(index="category", columns="month", values="amount", aggfunc="sum", fill_value=0)
    pivot = pivot.reindex(categories)

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    pivot.plot(kind="bar", ax=ax1)
    ax1.set_ylabel("지출 금액", fontproperties=fontprop)
    ax1.set_xlabel("카테고리", fontproperties=fontprop)
    ax1.tick_params(axis='x', labelrotation=0)
    ax1.legend(title="월", prop=fontprop)
    st.pyplot(fig1)

    # 연간 평균 그래프
    st.subheader("📉 연간 평균 지출")
    avg_data = df.groupby("category")["amount"].mean().reindex(categories)

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    bars = ax2.bar(avg_data.index, avg_data.values, color='salmon')
    ax2.set_ylabel("지출 금액", fontproperties=fontprop)
    ax2.set_xlabel("카테고리", fontproperties=fontprop)
    ax2.set_title("카테고리별 연간 평균 지출", fontproperties=fontprop)
    ax2.tick_params(axis='x', labelrotation=0)
    st.pyplot(fig2)
