import os
import pydub
import yt_dlp
import whisper
import datetime
import pandas as pd
import streamlit as st
from pathlib import Path
from tempfile import NamedTemporaryFile


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
        ("主頁", "YouTube下載器", "語音辨識")
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
            # st.table(info_df)
    elif page == "語音辨識":
        uploaded_file = st.file_uploader("上傳語音檔", type=['wav', 'mp3', "m4a"])
        model = whisper.load_model("base")

        if uploaded_file is not None:
            if uploaded_file.name.endswith('wav'):
                audio = pydub.AudioSegment.from_wav(uploaded_file)
                file_type = 'wav'
            elif uploaded_file.name.endswith('mp3'):
                audio = pydub.AudioSegment.from_mp3(uploaded_file)
                file_type = 'mp3'
            elif uploaded_file.name.endswith('m4a'):
                audio = pydub.AudioSegment.from_file(uploaded_file, format='m4a')
                file_type = 'mp4'

            save_path = os.path.abspath(uploaded_file.name)
            audio.export(save_path, format=file_type)

            audio_bytes = open(save_path, 'rb').read()
            st.audio(audio_bytes, format=f'audio/{file_type}', start_time=0)

            result = model.transcribe(uploaded_file.name)
            # st.write(result["text"])
            for segment in result['segments']:
                st.write(
                    f'{time(segment["start"])}'
                    f' --> '
                    f'{time(segment["end"])} '
                    f'{segment["text"][1:]}'
                )


if __name__ == '__main__':
    main()