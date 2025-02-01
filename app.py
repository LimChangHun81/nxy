import streamlit as st
import pandas as pd
import numpy as np
# Install Plotly
# st.set_option('deprecation.showPyplotGlobalUse', False)
# !pip install plotly

# import plotly.express as px

# ===== 📢 1. 페이지 타이틀 및 스타일 =====
st.markdown("""
    <h1 style='color: #FF5733; text-align: center;'>🎯 Streamlit 고급 대시보드 🎯</h1>
    <p style='font-size:20px; color:#2E86C1; text-align: center;'>한 페이지로 모든 기능을 보여줍니다! 🚀</p>
""", unsafe_allow_html=True)

# ===== 📊 2. 데이터 생성 =====
np.random.seed(42)
data = pd.DataFrame(np.random.randn(50, 3), columns=['나스닥', 'S&P 500', '다우존스'])

# ===== 🎛️ 3. 사이드바 설정 =====
st.sidebar.header("⚙️ 설정")
selected_index = st.sidebar.selectbox("분석할 지수 선택", data.columns)
range_val = st.sidebar.slider("데이터 범위 선택", 0, 50, (10, 30))
show_chart = st.sidebar.checkbox("📈 차트 표시", value=True)

# ===== 🗂️ 4. 컬럼 레이아웃 =====
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 데이터 미리보기")
    st.dataframe(data.head(10))

with col2:
    st.subheader("📋 통계 정보")
    st.write(data.describe())

# ===== 📈 5. 데이터 시각화 =====
if show_chart:
    st.markdown("### 🚀 선택한 지수의 차트")
    st.line_chart(data[selected_index].iloc[range_val[0]:range_val[1]])

# # ===== 🔍 6. Plotly 고급 시각화 =====
# st.markdown("### 📊 고급 그래프 (Plotly)")
# fig = px.line(data, x=data.index, y=data.columns, title="📈 지수 비교 그래프")
# fig.update_traces(line=dict(width=3))  # 선 두께 조절
# fig.update_layout(title_font_size=18)  # 제목 폰트 크기
# st.plotly_chart(fig)

# ===== ✅ 7. 버튼 기능 =====
if st.button("📊 데이터 새로고침"):
    data = pd.DataFrame(np.random.randn(50, 3), columns=['나스닥', 'S&P 500', '다우존스'])
    st.success("✅ 데이터가 새로고침되었습니다!")
    st.line_chart(data[selected_index])

# ===== ℹ️ 8. 추가 정보 =====
st.markdown("""
    ---
    <p style='text-align: center; color: gray;'>© 2024 고급 Streamlit 대시보드 튜토리얼</p>
""", unsafe_allow_html=True)
