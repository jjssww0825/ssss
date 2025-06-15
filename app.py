# 프로젝트 구조: 자산 관리 및 소비 조언 시스템

# 파일: app.py
# 설명: 사용자 소비 데이터를 기반으로 조언을 제공하는 Flask 백엔드 서버입니다.

from flask import Flask, request, jsonify

app = Flask(__name__)

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

@app.route("/advice/<username>", methods=["GET"])
def get_advice(username):
    user = users.get(username)
    if not user:
        return jsonify({"error": "사용자를 찾을 수 없습니다."}), 404
    
    tips = analyze_spending(user)
    return jsonify({"advice": tips})

if __name__ == "__main__":
    app.run(debug=True)


# 📁 프로젝트 구조 예시 (GitHub 업로드 시)

# 프로젝트 루트
# ├── app.py                   # Flask 백엔드 서버 코드
# ├── templates/              # HTML 템플릿 폴더 (웹 프론트와 연동 시 사용)
# │   └── index.html
# ├── static/                 # CSS/JS 파일 폴더
# ├── requirements.txt        # 의존성 패키지 리스트
# └── README.md               # 프로젝트 설명 파일

# requirements.txt 예시
# Flask==2.3.2

# README.md 예시
# """
# ## 소비 중심 자산 관리 로보어드바이저
# Flask를 기반으로 사용자의 소비 데이터를 분석하고, 소비 습관에 맞는 조언을 제공하는 웹 API 서비스입니다.

# ### 기능
# - 사용자 자산 및 소비 패턴 분석
# - 소비 습관에 대한 피드백 제공
# - API 형태로 조언 전달

# ### 실행 방법
# ```bash
# pip install -r requirements.txt
# python app.py
# ```
# 브라우저에서 http://localhost:5000/advice/user1 접속
# """
