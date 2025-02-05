import streamlit as st
import pandas as pd
import os
import json
import tempfile
from PIL import Image
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# ✅ 저장할 JSON 파일 경로 설정 (임시 폴더 사용)
UPLOAD_FOLDER = tempfile.gettempdir()
POSTS_FILE = os.path.join(UPLOAD_FOLDER, "posts.json")

# ✅ 기존 게시글 불러오기
def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# ✅ 게시글 저장 함수
def save_posts(posts):
    with open(POSTS_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, ensure_ascii=False, indent=4)

# ✅ Streamlit 세션 상태 초기화
if "posts" not in st.session_state:
    st.session_state.posts = load_posts()

# ✅ 파일 저장 함수
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# ✅ 유튜브 썸네일 추출 함수
def get_youtube_thumbnail(url):
    parsed_url = urlparse(url)
    video_id = None
    
    if "youtube.com" in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get("v", [None])[0]
    elif "youtu.be" in parsed_url.netloc:
        video_id = parsed_url.path[1:]
    
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/0.jpg"
    return None

# ✅ Streamlit UI
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
        save_posts(st.session_state.posts)  # JSON 파일로 저장
        st.success("게시글이 등록되었습니다!")
        st.rerun()  # 화면 새로고침
    else:
        st.error("제목과 내용을 입력해주세요.")

# ✅ 게시글 목록 표시
st.subheader("📋 게시글 목록")

if st.session_state.posts:
    for post in reversed(st.session_state.posts):
        st.markdown(f"### {post['title']}")
        st.write(post["content"])
        st.caption(f"📅 작성일: {post['timestamp']}")

        # ✅ 파일 다운로드 및 이미지 미리보기
        if post["files"]:
            st.markdown("📎 첨부파일:")
            for file_path in post["files"]:
                file_name = os.path.basename(file_path)
                
                if os.path.exists(file_path):
                    with open(file_path, "rb") as file:
                        st.download_button(label=file_name, data=file, file_name=file_name)

                    # ✅ 이미지 파일이면 클릭 확대 기능 추가
                    if file_name.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                        try:
                            image = Image.open(file_path)
                            image = image.resize((400, 400))
                            with st.container():
                                st.image(image, caption=file_name, use_column_width=True)
                                st.markdown(
                                    f"""
                                    <div style="text-align: center;">
                                        <img src="data:image/png;base64,{file_path}" 
                                             style="width: 100%; max-width: 400px; cursor: pointer;" 
                                             onclick="toggleSize(this)">
                                    </div>
                                    <script>
                                        function toggleSize(img) {{
                                            if (img.style.maxWidth === "400px") {{
                                                img.style.maxWidth = "100%";
                                            }} else {{
                                                img.style.maxWidth = "400px";
                                            }}
                                        }}
                                    </script>
                                    """,
                                    unsafe_allow_html=True,
                                )
                        except Exception as e:
                            st.warning(f"이미지 불러오기 오류: {e}")

        # ✅ 유튜브 링크 썸네일 추가
        if post["link"]:
            youtube_thumbnail = get_youtube_thumbnail(post["link"])
            if youtube_thumbnail:
                st.markdown(f"[![YouTube Video]({youtube_thumbnail})]({post['link']})")
            else:
                st.markdown(f"🔗 [외부 링크]({post['link']})")
        
        st.divider()
else:
    st.info("아직 게시글이 없습니다.")
