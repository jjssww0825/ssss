import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ✅ NanumGothic 폰트 직접 경로로 지정
font_path = "NanumGothic-Bold.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['axes.unicode_minus'] = False  # 음수 깨짐 방지

# 소비 조언 생성 함수
def analyze_spending(spending_data, monthly_budget):
    total_spent = sum(item['amount'] for item in spending_data)
    tips = []

    if total_spent > monthly_budget:
        tips.append(f"예산 초과! 설정한 월 예산({monthly_budget:,}원)을 {total_spent - monthly_budget:,}원 초과했습니다.")
    elif total_spent > monthly_budget * 0.9:
        tips.append("예산의 90% 이상을 지출했습니다. 남은 기간 동안 지출을 줄이는 것이 좋습니다.")
    else:
        tips.append("예산 내에서 잘 지출하고 있습니다. 좋은 소비 습관을 유지하세요!")

    for item in spending_data:
        if item['category'] == "카페" and item['amount'] > 70000:
            tips.append("카페 소비가 많습니다. 일주일 1~2회로 줄이면 절약에 도움이 됩니다.")
        elif item['category'] == "쇼핑" and item['amount'] > 100000:
            tips.append("쇼핑 지출이 높습니다. 충동구매를 줄이도록 노력해보세요.")
        elif item['category'] == "식비" and item['amount'] > 200000:
            tips.append("식비가 많은 편입니다. 외식보다는 집밥을 고려해보세요.")
        elif item['category'] == "여가" and item['amount'] > 100000:
            tips.append("여가 활동 지출이 높습니다. 무료 또는 저비용 활동도 고려해보세요.")

    return tips

# Streamlit UI
st.title("월간 소비 분석 자산 조언 시스템")

st.sidebar.header("🔧 설정")
monthly_budget = st.sidebar.slider("월 예산 설정 (원)", min_value=100000, max_value=1000000, step=50000, value=300000)

st.write(f"### 💰 이번 달 예산: {monthly_budget:,}원")

# 사용자 입력을 받아 소비 내역 구성
st.subheader("📊 소비 내역 입력")
categories = ["식비", "카페", "쇼핑", "교통", "여가", "기타"]
spending_data = []

for category in categories:
    amount = st.number_input(f"{category} 지출 (원)", min_value=0, step=1000, key=category)
    spending_data.append({"category": category, "amount": amount})

# 시각화: 원형 그래프
st.subheader("📈 지출 비율 시각화")
if spending_data and sum([item['amount'] for item in spending_data]) > 0:
    df = pd.DataFrame(spending_data)
    df = df[df['amount'] > 0]  # ✅ 0원 항목 제거
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        df['amount'],
        labels=df['category'],
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontproperties': fontprop, 'fontsize': 12}
    )
    for text in texts + autotexts:
        text.set_fontproperties(fontprop)
    ax.axis('equal')  # 원형 유지
    st.pyplot(fig)
else:
    st.info("지출 금액을 입력하면 그래프가 표시됩니다.")

# 소비 조언 출력
st.subheader("💡 소비 조언")
if spending_data:
    tips = analyze_spending(spending_data, monthly_budget)
    for tip in tips:
        st.success(tip)
