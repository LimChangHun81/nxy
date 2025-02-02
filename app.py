import streamlit as st
import pandas as pd
import time
import webbrowser
from PIL import Image
import os
from datetime import datetime
import re


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



def extract_youtube_thumbnail(url):
    match = re.search(r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]+)", url)
    if match:
        video_id = match.group(1)
        return f"https://img.youtube.com/vi/{video_id}/0.jpg"
    return None

# 게시글 데이터를 저장할 리스트
if 'posts' not in st.session_state:
    st.session_state.posts = []

# 파일 저장 폴더 설정
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# 페이지 제목
st.title("📌 간단한 게시판")

# 새 글 작성
st.subheader("새 글 작성")
title = st.text_input("제목")
content = st.text_area("내용")
uploaded_files = st.file_uploader("파일 업로드", accept_multiple_files=True)
external_link = st.text_input("추가 링크 (선택 사항)")

if st.button("게시하기"):
    if title and content:
        file_paths = [save_uploaded_file(file) for file in uploaded_files] if uploaded_files else []
        post = {
            "title": title,
            "content": content,
            "files": file_paths,
            "link": external_link,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        st.session_state.posts.append(post)
        st.success("게시글이 등록되었습니다!")
        st.rerun()
    else:
        st.error("제목과 내용을 입력해주세요.")

# 게시글 목록
st.subheader("📋 게시글 목록")
if st.session_state.posts:
    for i, post in enumerate(reversed(st.session_state.posts)):
        st.markdown(f"### {post['title']}")
        st.write(post["content"])
        st.caption(f"작성일: {post['timestamp']}")
        
        # 파일 다운로드 및 미리보기 표시
        if post["files"]:
            st.markdown("📎 첨부파일:")
            for file_path in post["files"]:
                file_name = os.path.basename(file_path)
                with open(file_path, "rb") as file:
                    st.download_button(label=file_name, data=file, file_name=file_name)
                
                # 이미지 파일 미리보기
                if file_name.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                    image = Image.open(file_path)
                    image = image.resize((400, 400))
                    st.image(image, caption=file_name, use_column_width=False)
        
        # 외부 링크 표시
        if post["link"]:
            youtube_thumbnail = extract_youtube_thumbnail(post["link"])
            if youtube_thumbnail:
                st.image(youtube_thumbnail, caption="YouTube 썸네일", use_column_width=False)
            st.markdown(f"🔗 [외부 링크]({post['link']})")
        
        st.divider()
else:
    st.info("아직 게시글이 없습니다.")
