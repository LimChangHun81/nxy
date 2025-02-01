import streamlit as st
import pandas as pd
import time
import webbrowser
from PIL import Image


# ✅ 1. 페이지 설정 (가장 먼저 위치)
st.set_page_config(page_title="Streamlit 기초 예제", layout="wide")


st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")


# ✅ 3. 제목 및 텍스트
st.title("Streamlit 기초 예제")
st.header("헤더입니다.")
st.subheader("서브헤더입니다.")
st.write("안녕하세요! Streamlit을 사용해 보세요.")
st.markdown("**마크다운**을 사용할 수도 있습니다.")

# ✅ 4. 입력 위젯
name = st.text_input("이름을 입력하세요:")
age = st.slider("나이를 선택하세요", 0, 100, 25)

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")


# ✅ 5. 버튼 클릭 시 출력
if st.button("제출"):
    st.write(f"안녕하세요, {name}님! 나이는 {age}세입니다.")




# ✅ 6. 데이터프레임 표시
data = {
    "이름": ["Alice", "Bob", "Charlie"],
    "나이": [25, 30, 35],
    "도시": ["서울", "부산", "인천"]
}
df = pd.DataFrame(data)
st.dataframe(df)


st.markdown("# Page 3 🎉")
st.sidebar.markdown("# Page 3 🎉")


# ✅ 7. 차트 표시
st.line_chart(df.set_index("이름")["나이"])

# st.markdown("[구글로 이동하기](https://www.google.com)")
st.markdown('[구글로 이동하기](https://www.google.com)', unsafe_allow_html=True)


# # 이미지 불러오기
# image = Image.open("IMG_2773-2.jpg")  # 이미지 파일 경로

# # 이미지 표시 (400x400 크기)
# st.image(image, width=400, height=400)
