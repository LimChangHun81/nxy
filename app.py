import streamlit as st
import pandas as pd  
import numpy as np

view = [100,150,40]
st.write(' # 자유대한민국 !!!')
st.bar_chart(view)

sview = pd.Series(view)
sview

# 제목
st.title('📈 나스닥 선물 분석 대시보드')

# 데이터 생성
data = pd.DataFrame(
    np.random.randn(100, 2),
    columns=['나스닥', 'S&P 500']
)

# 라인 차트로 시각화
st.line_chart(data)

# 슬라이더로 데이터 필터링
range_val = st.slider('데이터 범위 선택', 0, 100, (10, 50))
st.line_chart(data.iloc[range_val[0]:range_val[1]])

# 버튼 추가
if st.button('새로고침'):
    st.write('데이터를 새로고침했습니다!')
