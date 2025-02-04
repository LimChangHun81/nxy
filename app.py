import streamlit as st
import pandas as pd
import os
import json
import tempfile
from PIL import Image
from datetime import datetime
from pathlib import Path



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

                    # ✅ 이미지 파일이면 미리보기
                    if file_name.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                        try:
                            image = Image.open(file_path)
                            image = image.resize((400, 400))
                            st.image(image, caption=file_name, use_container_width=False)
                        except Exception as e:
                            st.warning(f"이미지 불러오기 오류: {e}")
                else:
                    st.warning(f"⚠️ 파일이 존재하지 않습니다: {file_name}")

        # ✅ 외부 링크 표시
        if post["link"]:
            st.markdown(f"🔗 [외부 링크]({post['link']})")
        
        st.divider()
else:
    st.info("아직 게시글이 없습니다.")

# First, we will need the following imports for our application.


# As for Streamlit Elements, we will need all these objects.
# All available objects and there usage are listed there: https://github.com/okld/streamlit-elements#getting-started

from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo

# Change page layout to make the dashboard take the whole page.

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("🗓️ #30DaysOfStreamlit")
    st.header("Day 27 - Streamlit Elements")
    st.write("Build a draggable and resizable dashboard with Streamlit Elements.")
    st.write("---")

    # Define URL for media player.
    media_url = st.text_input("Media URL", value="https://www.youtube.com/watch?v=vIQQR_yq-8I")

# Initialize default data for code editor and chart.
#
# For this tutorial, we will need data for a Nivo Bump chart.
# You can get random data there, in tab 'data': https://nivo.rocks/bump/
#
# As you will see below, this session state item will be updated when our
# code editor change, and it will be read by Nivo Bump chart to draw the data.

if "data" not in st.session_state:
    st.session_state.data = Path("data.json").read_text()

# Define a default dashboard layout.
# Dashboard grid has 12 columns by default.
#
# For more information on available parameters:
# https://github.com/react-grid-layout/react-grid-layout#grid-item-props

layout = [
    # Editor item is positioned in coordinates x=0 and y=0, and takes 6/12 columns and has a height of 3.
    dashboard.Item("editor", 0, 0, 6, 3),
    # Chart item is positioned in coordinates x=6 and y=0, and takes 6/12 columns and has a height of 3.
    dashboard.Item("chart", 6, 0, 6, 3),
    # Media item is positioned in coordinates x=0 and y=3, and takes 6/12 columns and has a height of 4.
    dashboard.Item("media", 0, 2, 12, 4),
]

# Create a frame to display elements.

with elements("demo"):

    # Create a new dashboard with the layout specified above.
    #
    # draggableHandle is a CSS query selector to define the draggable part of each dashboard item.
    # Here, elements with a 'draggable' class name will be draggable.
    #
    # For more information on available parameters for dashboard grid:
    # https://github.com/react-grid-layout/react-grid-layout#grid-layout-props
    # https://github.com/react-grid-layout/react-grid-layout#responsive-grid-layout-props

    with dashboard.Grid(layout, draggableHandle=".draggable"):

        # First card, the code editor.
        #
        # We use the 'key' parameter to identify the correct dashboard item.
        #
        # To make card's content automatically fill the height available, we will use CSS flexbox.
        # sx is a parameter available with every Material UI widget to define CSS attributes.
        #
        # For more information regarding Card, flexbox and sx:
        # https://mui.com/components/cards/
        # https://mui.com/system/flexbox/
        # https://mui.com/system/the-sx-prop/

        with mui.Card(key="editor", sx={"display": "flex", "flexDirection": "column"}):

            # To make this header draggable, we just need to set its classname to 'draggable',
            # as defined above in dashboard.Grid's draggableHandle.

            mui.CardHeader(title="Editor", className="draggable")

            # We want to make card's content take all the height available by setting flex CSS value to 1.
            # We also want card's content to shrink when the card is shrinked by setting minHeight to 0.

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # Here is our Monaco code editor.
                #
                # First, we set the default value to st.session_state.data that we initialized above.
                # Second, we define the language to use, JSON here.
                #
                # Then, we want to retrieve changes made to editor's content.
                # By checking Monaco documentation, there is an onChange property that takes a function.
                # This function is called everytime a change is made, and the updated content value is passed in
                # the first parameter (cf. onChange: https://github.com/suren-atoyan/monaco-react#props)
                #
                # Streamlit Elements provide a special sync() function. This function creates a callback that will
                # automatically forward its parameters to Streamlit's session state items.
                #
                # Examples
                # --------
                # Create a callback that forwards its first parameter to a session state item called "data":
                # >>> editor.Monaco(onChange=sync("data"))
                # >>> print(st.session_state.data)
                #
                # Create a callback that forwards its second parameter to a session state item called "ev":
                # >>> editor.Monaco(onChange=sync(None, "ev"))
                # >>> print(st.session_state.ev)
                #
                # Create a callback that forwards both of its parameters to session state:
                # >>> editor.Monaco(onChange=sync("data", "ev"))
                # >>> print(st.session_state.data)
                # >>> print(st.session_state.ev)
                #
                # Now, there is an issue: onChange is called everytime a change is made, which means everytime
                # you type a single character, your entire Streamlit app will rerun.
                #
                # To avoid this issue, you can tell Streamlit Elements to wait for another event to occur
                # (like a button click) to send the updated data, by wrapping your callback with lazy().
                #
                # For more information on available parameters for Monaco:
                # https://github.com/suren-atoyan/monaco-react
                # https://microsoft.github.io/monaco-editor/api/interfaces/monaco.editor.IStandaloneEditorConstructionOptions.html

                editor.Monaco(
                    defaultValue=st.session_state.data,
                    language="json",
                    onChange=lazy(sync("data"))
                )

            with mui.CardActions:

                # Monaco editor has a lazy callback bound to onChange, which means that even if you change
                # Monaco's content, Streamlit won't be notified directly, thus won't reload everytime.
                # So we need another non-lazy event to trigger an update.
                #
                # The solution is to create a button that fires a callback on click.
                # Our callback doesn't need to do anything in particular. You can either create an empty
                # Python function, or use sync() with no argument.
                #
                # Now, everytime you will click that button, onClick callback will be fired, but every other
                # lazy callbacks that changed in the meantime will also be called.

                mui.Button("Apply changes", onClick=sync())

        # Second card, the Nivo Bump chart.
        # We will use the same flexbox configuration as the first card to auto adjust the content height.

        with mui.Card(key="chart", sx={"display": "flex", "flexDirection": "column"}):

            # To make this header draggable, we just need to set its classname to 'draggable',
            # as defined above in dashboard.Grid's draggableHandle.

            mui.CardHeader(title="Chart", className="draggable")

            # Like above, we want to make our content grow and shrink as the user resizes the card,
            # by setting flex to 1 and minHeight to 0.

            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # This is where we will draw our Bump chart.
                #
                # For this exercise, we can just adapt Nivo's example and make it work with Streamlit Elements.
                # Nivo's example is available in the 'code' tab there: https://nivo.rocks/bump/
                #
                # Data takes a dictionary as parameter, so we need to convert our JSON data from a string to
                # a Python dictionary first, with `json.loads()`.
                #
                # For more information regarding other available Nivo charts:
                # https://nivo.rocks/

                nivo.Bump(
                    data=json.loads(st.session_state.data),
                    colors={ "scheme": "spectral" },
                    lineWidth=3,
                    activeLineWidth=6,
                    inactiveLineWidth=3,
                    inactiveOpacity=0.15,
                    pointSize=10,
                    activePointSize=16,
                    inactivePointSize=0,
                    pointColor={ "theme": "background" },
                    pointBorderWidth=3,
                    activePointBorderWidth=3,
                    pointBorderColor={ "from": "serie.color" },
                    axisTop={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "",
                        "legendPosition": "middle",
                        "legendOffset": -36
                    },
                    axisBottom={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "",
                        "legendPosition": "middle",
                        "legendOffset": 32
                    },
                    axisLeft={
                        "tickSize": 5,
                        "tickPadding": 5,
                        "tickRotation": 0,
                        "legend": "ranking",
                        "legendPosition": "middle",
                        "legendOffset": -40
                    },
                    margin={ "top": 40, "right": 100, "bottom": 40, "left": 60 },
                    axisRight=None,
                )

        # Third element of the dashboard, the Media player.

        with mui.Card(key="media", sx={"display": "flex", "flexDirection": "column"}):
            mui.CardHeader(title="Media Player", className="draggable")
            with mui.CardContent(sx={"flex": 1, "minHeight": 0}):

                # This element is powered by ReactPlayer, it supports many more players other
                # than YouTube. You can check it out there: https://github.com/cookpete/react-player#props

                media.Player(url=media_url, width="100%", height="100%", controls=True)
