import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 한글 폰트 설정
font_path = "NanumGothic-Bold.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['axes.unicode_minus'] = False

# ✅ 저장 파일 경로
DATA_FILE = "monthly_spending.csv"

# ✅ 소비 분석 함수
def analyze_spending(spending_data, monthly_budget):
    total_spent = sum(item['amount'] for item in spending_data)
    tips = []

    if total_spent > monthly_budget:
        tips.append(f"예산 초과! 설정한 월 예산({monthly_budget:,}원)을 {total_spent - monthly_budget:,}원 초과했습니다.")
    elif total_spent > monthly_budget * 0.9:
        tips.append("예산의 90% 이상을 지출했습니다.")
    elif total_spent < monthly_budget * 0.5:
        tips.append("예산의 절반 이하만 지출 중입니다.")
    else:
        tips.append("예산 내에서 잘 지출하고 있습니다.")

    for item in spending_data:
        category = item['category']
        amount = item['amount']
        if category == "카페" and amount > 70000:
            tips.append("☕ 카페 지출이 많습니다.")
        elif category == "쇼핑" and amount > 100000:
            tips.append("🛍️ 쇼핑 지출이 높습니다.")
        elif category == "식비" and amount > 200000:
            tips.append("🍽️ 식비가 많은 편입니다.")
        elif category == "여가" and amount > 100000:
            tips.append("🎮 여가 활동 지출이 높습니다.")
        elif category == "교통" and amount > 100000:
            tips.append("🚆 교통비가 높습니다.")

    saving_score = max(0, min(100, int((1 - total_spent / monthly_budget) * 100)))
    tips.append(f"📊 절약 점수: {saving_score}/100")
    tips.append(f"💡 권장 저축액: {int(monthly_budget * 0.2):,}원")

    return tips

# ✅ Streamlit UI
st.title("💳 월간 소비 분석 자산 조언 시스템")

st.sidebar.header("🔧 설정")
month = st.sidebar.selectbox("분석할 월 선택", [f"{i}월" for i in range(1, 13)])
monthly_budget = st.sidebar.slider("월 예산 설정 (원)", 100000, 1000000, 300000, step=50000)

categories = ["식비", "카페", "쇼핑", "교통", "여가"]
spending_data = []

st.write(f"### 💰 {month} 예산: {monthly_budget:,}원")

st.subheader("📊 소비 내역 입력")
for category in categories:
    amount = st.number_input(f"{category} 지출 (원)", min_value=0, step=1000, key=category)
    spending_data.append({"month": month, "category": category, "amount": amount})

# ✅ 저장 및 분석 버튼
if st.button("저장 및 분석"):
    df_new = pd.DataFrame(spending_data)
    if os.path.exists(DATA_FILE):
        df_old = pd.read_csv(DATA_FILE)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new
    df_all.to_csv(DATA_FILE, index=False)
    st.success(f"{month} 데이터가 저장되었습니다!")

    # ✅ 월별 지출 비교 그래프
    st.subheader("📊 월별 지출 비교")
    pivot = df_all.pivot_table(index="category", columns="month", values="amount", aggfunc="sum", fill_value=0)
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    pivot.plot(kind="bar", ax=ax1)
    ax1.set_ylabel("지출 금액", fontproperties=fontprop)
    ax1.set_xlabel("카테고리", fontproperties=fontprop)
    ax1.set_xticks(range(len(pivot.index)))
    ax1.set_xticklabels(pivot.index, fontproperties=fontprop)
    ax1.legend(prop=fontprop)
    st.pyplot(fig1)

    # ✅ 연간 평균 그래프
    st.subheader("📉 연간 평균 지출")
    avg_data = df_all.groupby("category")["amount"].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    bars = ax2.bar(avg_data["category"], avg_data["amount"], color='salmon')
    ax2.set_title("카테고리별 연간 평균 지출", fontproperties=fontprop)
    ax2.set_ylabel("지출 금액", fontproperties=fontprop)
    ax2.set_xlabel("카테고리", fontproperties=fontprop)
    ax2.set_xticks(range(len(avg_data["category"])))
    ax2.set_xticklabels(avg_data["category"], fontproperties=fontprop)
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, height, f"{int(height):,}", ha='center', va='bottom', fontproperties=fontprop, fontsize=10)
    st.pyplot(fig2)

# ✅ 소비 조언 출력
st.subheader("💡 소비 조언")
if spending_data:
    tips = analyze_spending(spending_data, monthly_budget)
    for tip in tips:
        st.success(tip)
