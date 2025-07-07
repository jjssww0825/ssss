import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

# ✅ 폰트 설정
FONT_PATH = "NanumGothic-Bold.ttf"
if os.path.exists(FONT_PATH):
    fontprop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = fontprop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    st.warning("⚠️ NanumGothic-Bold.ttf 파일이 없습니다. 앱과 같은 폴더에 넣어주세요.")
    fontprop = None

# ✅ 파일/카테고리 정의
DATA_FILE = "monthly_spending.csv"
CATEGORIES = ["식비", "카페", "쇼핑", "교통", "여가"]

# ✅ 소비 조언 생성 함수
def analyze_spending(spending_data, budget):
    total = sum([x["amount"] for x in spending_data])
    tips = []

    if total > budget:
        tips.append(f"❗ 예산 초과: {total - budget:,}원 초과")
    elif total > budget * 0.9:
        tips.append("⚠️ 예산의 90% 이상 사용 중")
    elif total < budget * 0.5:
        tips.append("🔎 예산의 절반 이하 사용")
    else:
        tips.append("✅ 예산 내 지출 중입니다.")

    for item in spending_data:
        if item["category"] == "카페" and item["amount"] > 70000:
            tips.append("☕ 카페 지출이 많습니다. 주 1~2회로 줄여보세요.")
        if item["category"] == "쇼핑" and item["amount"] > 100000:
            tips.append("🛍️ 쇼핑 지출이 높습니다. 충동구매를 줄이세요.")
        if item["category"] == "식비" and item["amount"] > 200000:
            tips.append("🍱 식비가 높습니다. 외식보다 집밥을 고려하세요.")
        if item["category"] == "여가" and item["amount"] > 100000:
            tips.append("🎮 여가 활동이 많습니다. 저비용 활동도 고려해보세요.")
        if item["category"] == "교통" and item["amount"] > 100000:
            tips.append("🚆 교통비가 높습니다. 정기권 활용도 좋습니다.")

    score = max(0, min(100, int((1 - total / budget) * 100)))
    tips.append(f"📊 절약 점수: {score}/100")
    tips.append(f"💡 최소 저축 권장액: {int(budget * 0.2):,}원")

    return tips

# ✅ 앱 UI 구성
st.set_page_config(page_title="자산 소비 분석 시스템", layout="wide")
st.title("📊 월간 소비 분석 자산 조언 시스템")

st.sidebar.header("설정")
month = st.sidebar.selectbox("📆 분석할 월", [f"{i}월" for i in range(1, 13)])
budget = st.sidebar.slider("💰 월 예산 (원)", 100000, 1000000, 300000, step=50000)

# ✅ 데이터 불러오기
if os.path.exists(DATA_FILE):
    df_all = pd.read_csv(DATA_FILE)
else:
    df_all = pd.DataFrame(columns=["month", "category", "amount"])

# ✅ 기존 입력 값 불러오기
previous = df_all[df_all["month"] == month]
st.subheader("✍️ 소비 내역 입력")
spending_data = []
for category in CATEGORIES:
    default = int(previous[previous["category"] == category]["amount"].values[0]) if category in previous["category"].values else 0
    amount = st.number_input(f"{category} 지출 (원)", min_value=0, step=1000, value=default, key=category)
    spending_data.append({"month": month, "category": category, "amount": amount})

# ✅ 버튼: 저장 & 초기화
col1, col2 = st.columns(2)

if col1.button("💾 저장 및 분석"):
    df_new = pd.DataFrame(spending_data)
    df_all = df_all[df_all["month"] != month]
    df_all = pd.concat([df_all, df_new], ignore_index=True)
    df_all.to_csv(DATA_FILE, index=False)
    st.success(f"{month} 데이터 저장 완료!")

    st.subheader("📈 지출 비율 원형 그래프")
    pie_df = df_new[df_new["amount"] > 0]
    if not pie_df.empty:
        fig, ax = plt.subplots()
        ax.pie(pie_df["amount"], labels=pie_df["category"], autopct="%1.1f%%", startangle=90, textprops={'fontsize': 12, 'fontproperties': fontprop})
        ax.axis("equal")
        st.pyplot(fig)

    st.subheader("💡 소비 조언")
    for tip in analyze_spending(spending_data, budget):
        st.info(tip)

if col2.button("🗑️ 전체 초기화"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    st.warning("📂 모든 저장 데이터를 삭제했습니다.")
    st.experimental_rerun()

# ✅ 최근 비교할 월 수 선택
compare_n = st.sidebar.selectbox("📅 비교할 최근 월 수", [1, 3, 6, 9, 12])

# ✅ 하나의 그래프: 최근 월별 지출 + 연간 평균
if not df_all.empty:
    st.subheader("📊 최근 월별 지출 + 연간 평균 (하나의 그래프)")

    recent_months = sorted(df_all["month"].unique(), key=lambda x: int(x.replace("월", "")))[-compare_n:]
    pivot = df_all[df_all["month"].isin(recent_months)].pivot_table(index="category", columns="month", values="amount", aggfunc="sum", fill_value=0)

    full_months = [f"{i}월" for i in range(1, 13)]
    filtered_df = df_all[df_all["month"].isin(full_months)]
    avg_df = filtered_df.groupby("category")["amount"].mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    bar_width = 0.8 / len(recent_months)
    x = np.arange(len(pivot.index))

    for i, month in enumerate(recent_months):
        ax.bar(x + i * bar_width, pivot[month], width=bar_width, label=month)

    ax.plot(x + bar_width * (len(recent_months) - 1) / 2, avg_df[pivot.index], 
            color='red', marker='o', linestyle='-', label='연간 평균')

    ax.set_xticks(x + bar_width * (len(recent_months) - 1) / 2)
    ax.set_xticklabels(pivot.index, fontproperties=fontprop)
    ax.set_ylabel("지출 금액", fontproperties=fontprop)
    ax.set_title("최근 월별 지출 + 연간 평균", fontproperties=fontprop)
    ax.legend(prop=fontprop)
    plt.grid(True, axis='y')
    plt.tight_layout()
    st.pyplot(fig)
