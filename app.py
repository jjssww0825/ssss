import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# ✅ 폰트 설정
FONT_PATH = "NanumGothic-Bold.ttf"
if os.path.exists(FONT_PATH):
    fontprop = fm.FontProperties(fname=FONT_PATH)
    plt.rcParams['font.family'] = fontprop.get_name()
    plt.rcParams['axes.unicode_minus'] = False
else:
    st.warning("⚠️ NanumGothic-Bold.ttf 파일이 없습니다. 앱과 같은 폴더에 추가하세요.")
    fontprop = None

# ✅ 파일 설정
DATA_FILE = "monthly_spending.csv"
CATEGORIES = ["식비", "카페", "쇼핑", "교통", "여가"]

# ✅ 소비 분석
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

# ✅ UI 구성
st.set_page_config(page_title="자산 소비 분석 시스템", layout="wide")
st.title("📊 월간 소비 분석 자산 조언 시스템")

st.sidebar.header("설정")
month = st.sidebar.selectbox("📆 분석할 월", [f"{i}월" for i in range(1, 13)])
budget = st.sidebar.slider("💰 월 예산 (원)", 100000, 1000000, 300000, step=50000)

# ✅ 데이터 로드
if os.path.exists(DATA_FILE):
    df_all = pd.read_csv(DATA_FILE)
else:
    df_all = pd.DataFrame(columns=["month", "category", "amount"])

# ✅ 기존 데이터 불러오기
previous = df_all[df_all["month"] == month]
st.subheader("✍️ 소비 내역 입력")
spending_data = []
for category in CATEGORIES:
    default = int(previous[previous["category"] == category]["amount"].values[0]) if category in previous["category"].values else 0
    amount = st.number_input(f"{category} 지출 (원)", min_value=0, step=1000, value=default, key=category)
    spending_data.append({"month": month, "category": category, "amount": amount})

# ✅ 버튼
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

# ✅ 초기화 버튼
if col2.button("🗑️ 전체 초기화"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    st.warning("📂 모든 저장 데이터를 삭제했습니다.")
    st.experimental_rerun()

# ✅ 비교할 월 수 선택
compare_n = st.sidebar.selectbox("📅 비교할 최근 월 수", [1, 3, 6, 9, 12])

# ✅ 월별 비교 그래프
if not df_all.empty:
    st.subheader("📊 월별 지출 비교")
    recent_months = sorted(df_all["month"].unique(), key=lambda x: int(x.replace("월", "")))[-compare_n:]
    pivot = df_all[df_all["month"].isin(recent_months)].pivot_table(index="category", columns="month", values="amount", aggfunc="sum", fill_value=0)
    
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    pivot.plot(kind="bar", ax=ax2)

    ax2.set_xlabel("지출 항목", fontproperties=fontprop)
    ax2.set_ylabel("지출 금액", fontproperties=fontprop)
    ax2.set_title("월별 지출 비교", fontproperties=fontprop)
    plt.xticks(rotation=0, fontproperties=fontprop)
    plt.yticks(fontproperties=fontprop)
    plt.legend(prop=fontprop)
    plt.tight_layout()
    st.pyplot(fig2)
