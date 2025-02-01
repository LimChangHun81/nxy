import streamlit as st
import pandas as pd


import time

progress_bar = st.progress(0)
for i in range(50):
    time.sleep(0.01)
    progress_bar.progress(i + 1)
st.write("완료!")
# st.title("테스트 앱")
# st.write("Hello, Streamlit!@@@jnnjinjuinu  jju")
st.title("Streamlit 기초 예제")
st.header("헤더입니다.")
st.subheader("서브헤더입니다.")
st.write("안녕하세요! Streamlit을 사용해 보세요.")
st.markdown("**마크다운**을 사용할 수도 있습니다.")

name = st.text_input("1. 이름을 입력하세요:")
age = st.slider("2. 나이를 선택하세요", 0, 100, 25)
if st.button("제출"):
    st.write(f"안녕하세요, {name}님! 나이는 {age}세입니다.")
st.set_page_config(page_title="My App", layout="wide")
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="Streamlit 기초 예제", layout="wide")

# 제목
st.title("Streamlit 기초 예제")

# 입력 위젯
name = st.text_input("이름을 입력하세요:")
age = st.slider("나이를 선택하세요", 0, 100, 25)

# 버튼
if st.button("제출"):
    st.write(f"안녕하세요, {name}님! 나이는 {age}세입니다.")

# 데이터프레임
import pandas as pd
data = {
    "이름": ["Alice", "Bob", "Charlie"],
    "나이": [25, 30, 35],
    "도시": ["서울", "부산", "인천"]
}
df = pd.DataFrame(data)
st.dataframe(df)

# 차트
st.line_chart(df.set_index("이름")["나이"])
