# 프로젝트 구조: 자산 관리 및 소비 조언 시스템 (Streamlit 버전)

# 파일: app.py
# 설명: 사용자 소비 데이터를 기반으로 조언을 제공하는 Streamlit 앱입니다.

import streamlit as st

# 예시 사용자 데이터베이스 (실제 서비스에서는 DB 연결 필요)
users = {
    "user1": {
        "age": 30,
        "assets": 50000000,  # 자산
        "risk_tolerance": "medium",
        "spending": [
            {"category": "식비", "amount": 400000},
            {"category": "카페", "amount": 150000},
            {"category": "쇼핑", "amount": 300000},
            {"category": "저축", "amount": 1000000}
        ]
    }
}

# 소비 조언 생성 함수
def analyze_spending(user_data):
    total_spent = sum(item['amount'] for item in user_data['spending'])
    total_assets = user_data['assets']

    tips = []

    if total_spent > 0.3 * total_assets:
        tips.append("소비가 자산의 30% 이상입니다. 지출을 줄이는 것이 좋습니다.")

    for item in user_data['spending']:
        if item['category'] == "카페" and item['amount'] > 100000:
            tips.append("카페 지출이 많습니다. 일주일에 한 번 정도 줄여보는 건 어떨까요?")
        if item['category'] == "쇼핑" and item['amount'] > 200000:
            tips.append("쇼핑 비용이 높은 편입니다. 필요한 지출인지 점검해보세요.")

    if not tips:
        tips.append("소비 패턴이 안정적입니다. 저축을 더 늘려보는 것도 좋습니다.")

    return tips

# Streamlit UI
st.title("소비 분석 기반 자산 조언 시스템")

selected_user = st.selectbox("사용자를 선택하세요", list(users.keys()))

if selected_user:
    user_data = users[selected_user]

    st.subheader("🧾 소비 내역")
    for item in user_data["spending"]:
        st.write(f"- {item['category']}: {item['amount']:,}원")

    st.subheader("💡 소비 조언")
    tips = analyze_spending(user_data)
    for tip in tips:
        st.success(tip)
