import streamlit as st
import pandas as pd

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
