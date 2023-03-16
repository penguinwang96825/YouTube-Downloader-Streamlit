import os
import yt_dlp
import datetime
import pandas as pd
import streamlit as st


def get_youtube_video_info(url):
    os.system(f'yt-dlp --list-formats {url}')
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info_df = pd.DataFrame(info['formats'])
    info_df = info_df[
        ['format_note', 'ext', 'acodec', 'vcodec', 'url']
    ]
    info_df = info_df.query('ext not in ["mhtml", "webm"]')
    info_df = info_df.replace({'acodec': 'none'}, 'video only')
    info_df = info_df.replace({'vcodec': 'none'}, 'audio only')
    info_df['acodec'] = info_df['acodec'].apply(
        lambda x: 'X' if x=='video only' else 'O'
    )
    info_df['vcodec'] = info_df['vcodec'].apply(
        lambda x: 'X' if x=='audio only' else 'O'
    )
    info_df['url'] = info_df['url'].apply(make_clickable)
    info_df.columns = ['畫質', '檔名', '音訊', '影像', '網址']
    info_df = info_df.reset_index(drop=True)
    return info_df


def make_clickable(link):
    text = link.split('=')[1]
    return f'<a target="_blank" href="{link}">link</a>'


def hide():
    hide_streamlit_style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


def time(sec):
    return datetime.timedelta(seconds=round(sec))


def main():
    hide()
    page = st.sidebar.selectbox(
        "功能頁",
        ("主頁", "YouTube下載器")
    )
    if page == "主頁":
        st.title('主頁')
    elif page == "YouTube下載器":
        st.title('YouTube下載器')
        # https://www.youtube.com/watch?v=HQDDlgGy2hg
        url = st.text_input(label='請輸入網址: ')

        if url:
            info_df = get_youtube_video_info(url)
            info_df = info_df.to_html(escape=False)
            st.write(info_df, unsafe_allow_html=True)


if __name__ == '__main__':
    main()