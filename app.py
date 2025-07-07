import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 설정
font_path = "NanumGothic.ttf"  # 프로젝트 폴더에 이 파일이 있어야 함
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False

# ✅ 데이터 파일 경로
DATA_FILE = "monthly_spending.csv"
categories = ["교통", "쇼핑", "식비", "여가", "카페"]

# ✅ UI 구성
st.title("📉 월별 지출 비교")
month = st.sidebar.selectbox("월 선택", [f"{i}월" for i in range(1, 13)])
budget = st.sidebar.slider("예산 (원)", 100000, 1000000, 300000, step=50000)

st.subheader(f"📋 {month} 소비 입력")
spending = {cat: st.number_input(f"{cat} 지출", min_value=0, step=1000, key=cat) for cat in categories}

# ✅ 저장
if st.button("저장"):
    new_df = pd.DataFrame([{"month": month, "category": k, "amount": v} for k, v in spending.items()])
    if os.path.exists(DATA_FILE):
        old_df = pd.read_csv(DATA_FILE)
        df = pd.concat([old_df, new_df], ignore_index=True)
    else:
        df = new_df
    df.to_csv(DATA_FILE, index=False)
    st.success("데이터 저장 완료")

# ✅ 초기화
if st.button("초기화"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        st.success("모든 데이터 초기화 완료")

# ✅ 그래프
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    pivot = df.pivot_table(index="category", columns="month", values="amount", aggfunc="sum", fill_value=0)
    pivot = pivot.reindex(categories)

    st.subheader("📊 월별 지출 비교")
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot(kind="bar", ax=ax)
    ax.set_xlabel("카테고리")
    ax.set_ylabel("지출 금액")
    ax.tick_params(axis='x', labelrotation=0)
    ax.legend(title="월")
    st.pyplot(fig)
