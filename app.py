import streamlit as st

# 제목 추가
st.title("Streamlit 기본 예제")

# 헤더 추가
st.header("이것은 헤더입니다.")

# 서브헤더 추가
st.subheader("이것은 서브헤더입니다.")

# 텍스트 추가
st.write("안녕하세요! 이것은 Streamlit 앱입니다.")

# 마크다운 사용
st.markdown("**마크다운**을 사용할 수도 있습니다.")

# 입력 위젯
name = st.text_input("이름을 입력하세요:")
if name:
    st.write(f"안녕하세요, {name}님!")

# # 슬라이더
# age = st.slider("나이를 선택하세요", 0, 100, 25)
# st.write(f"선택한 나이는 {age}세입니다.")

# # 버튼
# if st.button("클릭하세요"):
#     st.write("버튼이 클릭되었습니다!")

# # 체크박스
# if st.checkbox("체크박스"):
#     st.write("체크박스가 선택되었습니다.")

# # 라디오 버튼
# option = st.radio("옵션을 선택하세요", ("옵션 1", "옵션 2", "옵션 3"))
# st.write(f"선택한 옵션: {option}")

# # 드롭다운 메뉴
# choice = st.selectbox("드롭다운 메뉴", ("선택 1", "선택 2", "선택 3"))
# st.write(f"선택한 항목: {choice}")

# # 파일 업로드
# uploaded_file = st.file_uploader("파일을 업로드하세요", type=["txt", "csv", "png", "jpg"])
# if uploaded_file is not None:
#     st.write("파일이 업로드되었습니다.")
#     st.write(f"파일 이름: {uploaded_file.name}")

# # 데이터프레임 표시
# import pandas as pd
# data = {
#     "이름": ["Alice", "Bob", "Charlie"],
#     "나이": [25, 30, 35],
#     "도시": ["서울", "부산", "인천"]
# }
# df = pd.DataFrame(data)
# st.write("데이터프레임:")
# st.dataframe(df)

# # 차트 그리기
# st.line_chart(df.set_index("이름")["나이"])
