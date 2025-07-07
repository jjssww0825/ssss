import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import streamlit as st

# ✅ 폰트 설정 (TTF 경로)
font_path = "/mnt/data/NanumGothicBold.ttf"
font_prop = fm.FontProperties(fname=font_path)

# ✅ 예제 데이터
monthly_data = {
    '카테고리': ['교통', '쇼핑', '식비', '여가', '카페'],
    '1월': [253000, 252000, 12000, 63000, 23000],
    '2월': [41000, 16000, 180000, 41000, 40000]
}

average_data = {
    '카테고리': ['교통', '쇼핑', '식비', '여가', '카페'],
    '연간 평균': [97406, 89074, 64074, 34074, 20407]
}

df_monthly = pd.DataFrame(monthly_data)
df_avg = pd.DataFrame(average_data)

# ✅ 📊 월별 지출 그래프
st.markdown("### 📈 월별 지출 비교")
fig1, ax1 = plt.subplots()
x = df_monthly['카테고리']
bar_width = 0.35
index = range(len(x))

ax1.bar([i - bar_width/2 for i in index], df_monthly['1월'], bar_width, label='1월')
ax1.bar([i + bar_width/2 for i in index], df_monthly['2월'], bar_width, label='2월')

ax1.set_xlabel('카테고리', fontproperties=font_prop)
ax1.set_ylabel('지출 금액', fontproperties=font_prop)
ax1.set_title('월별 지출 비교', fontproperties=font_prop)
ax1.set_xticks(index)
ax1.set_xticklabels(x, fontproperties=font_prop)
ax1.tick_params(axis='y')
ax1.legend(prop=font_prop)

# ✅ 한글 폰트 적용
for label in ax1.get_yticklabels():
    label.set_fontproperties(font_prop)

st.pyplot(fig1)

# ✅ 📉 연간 평균 지출 그래프
st.markdown("### 📉 연간 평균 지출")
fig2, ax2 = plt.subplots()
x = df_avg['카테고리']
y = df_avg['연간 평균']

bars = ax2.bar(x, y, color='salmon')
ax2.set_xlabel("카테고리", fontproperties=font_prop)
ax2.set_ylabel("지출 금액", fontproperties=font_prop)
ax2.set_title("카테고리별 연간 평균 지출", fontproperties=font_prop)

ax2.set_xticklabels(x, fontproperties=font_prop)
for label in ax2.get_yticklabels():
    label.set_fontproperties(font_prop)

st.pyplot(fig2)
