import streamlit as st
import pandas as pd
import os
import tempfile
from PIL import Image
from datetime import datetime
import re

# ✅ 파일 저장 폴더 설정
UPLOAD_FOLDER = tempfile.gettempdir()  # 임시 폴더 사용

# 파일 저장 함수 (세션 유지)
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# 게시글 데이터 로드 함수
def load_posts():
    return st.session_state.get("posts", [])

# 게시글 데이터 저장 함수
def save_posts(posts):
    st.session_state.posts = posts

# ✅ 게시글 목록 저장 (세션 활용)
if "posts" not in st.session_state:
    st.session_state.posts = []

# ✅ 게시글 작성 UI
st.title("📌 간단한 게시판")
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
        save_posts(st.session_state.posts)  # 세션 상태에 저장
        st.success("게시글이 등록되었습니다!")
        st.rerun()
    else:
        st.error("제목과 내용을 입력해주세요.")

# ✅ 게시글 목록 표시
st.subheader("📋 게시글 목록")

if st.session_state.posts:
    for post in reversed(st.session_state.posts):
        st.markdown(f"### {post['title']}")
        st.write(post["content"])
        st.caption(f"작성일: {post['timestamp']}")
        
        # ✅ 파일 다운로드 및 이미지 미리보기
        if post["files"]:
            st.markdown("📎 첨부파일:")
            for file_path in post["files"]:
                file_name = os.path.basename(file_path)

                # 파일 존재 여부 확인 후 다운로드 버튼 표시
                if os.path.exists(file_path):
                    with open(file_path, "rb") as file:
                        st.download_button(label=file_name, data=file, file_name=file_name)
                    
                    # 이미지 파일 미리보기
                    if file_name.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                        try:
                            image = Image.open(file_path)
                            image = image.resize((400, 400))
                            st.image(image, caption=file_name, use_container_width=False)
                        except Exception as e:
                            st.warning(f"이미지를 불러오는 중 오류 발생: {e}")
                else:
                    st.warning(f"⚠️ 파일이 존재하지 않습니다: {file_name}")

        # ✅ 외부 링크 표시
        if post["link"]:
            st.markdown(f"🔗 [외부 링크]({post['link']})")
        
        st.divider()
else:
    st.info("아직 게시글이 없습니다.")
