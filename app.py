# -*- coding: utf-8 -*-
"""
Entrypoint file

Authors
 * Yang Wang 2023
"""
import os
import pysbd
import streamlit as st
from datetime import timedelta
from transformers import pipeline

from src.downloader import get_youtube_video_info
from src.audio import to_mp3
from src.transcriber import Transcriber
from src.utils import hide_footer, read_markdown_file


def page_introduction():
    markdown = read_markdown_file('media/introduction.md')
    st.markdown(markdown, unsafe_allow_html=True)


def page_youtube_downloader():
    st.title('YouTube下載器')
    options = {}
    options['ext'] = st.sidebar.multiselect(
        '副檔名',
        ['3gp', 'm4a', 'mp4'], 
        ['3gp', 'm4a', 'mp4']
    )
    # https://www.youtube.com/watch?v=HQDDlgGy2hg
    url = st.text_input(label='請輸入網址: ')

    if url:
        info_df = get_youtube_video_info(url, options)
        info_df = info_df.to_html(escape=False)
        st.write(info_df, unsafe_allow_html=True)


def page_audio_transcriber():
    st.title('語音轉譯器')

    upload_path = "tmp/uploads/"
    download_path = "tmp/downloads/"
    transcript_path = "tmp/transcripts/"
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists(transcript_path):
        os.makedirs(transcript_path)
    uploaded_file = st.file_uploader(
        "上傳語音檔案", 
        type=["wav", "mp3", "ogg", "wma", "aac", "flac", "mp4", "m4a", "flv"]
    )

    markdown = read_markdown_file('media/model.md')
    st.markdown(markdown, unsafe_allow_html=True)

    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        with open(os.path.join(upload_path, uploaded_file.name), "wb") as f:
            f.write((uploaded_file).getbuffer())
        with st.spinner(f"語音文件處理中..."):
            output_audio_file = uploaded_file.name.split('.')[0] + '.mp3'
            output_audio_file = to_mp3(uploaded_file, output_audio_file, upload_path, download_path)
            audio_file = open(os.path.join(download_path, output_audio_file), 'rb')
            audio_bytes = audio_file.read()

        # st.markdown("播放語音")
        st.audio(audio_bytes)

        col1, col2 = st.columns(2)
        with col1:
            language = st.radio(
                "語言種類", 
                ('Multi-language', 'English')
            )
        with col2:
            model_size = st.radio(
                "語音模型大小", 
                ('Tiny', 'Base', 'Small', 'Medium', 'Large')
            )

        if st.button('轉譯'):
            with st.spinner("加載模型中..."):
                transcriber = Transcriber(language=language, model_size=model_size)
            with st.spinner(f"語音文件轉譯中..."):
                audio_file = str(os.path.abspath(os.path.join(download_path, output_audio_file)))
                result = transcriber(audio_file)
            # st.write(result['text'])

            transcript_file = os.path.join(transcript_path, 'subtitles.srt')
            with open(transcript_file, 'w') as f:
                for segment in result['segments']:
                    since = timedelta(seconds=segment["start"])
                    until = timedelta(seconds=segment["end"])
                    text = segment['text']
                    msg = f'{since} --> {until} {text}\n\n'
                    f.write(msg)
            output_file = open(os.path.join(transcript_path, 'subtitles.srt'), "r")
            output_file_data = output_file.read()

            if st.download_button(
                label='下載SRT檔', 
                data=output_file_data, 
                file_name='subtitles.srt', 
                mime='text/plain'
            ):
                st.success('下載成功！')


def page_audio_summariser():
    st.title("語音摘要器 (TBD)")
    upload_path = "tmp/uploads/"
    download_path = "tmp/downloads/"
    transcript_path = "tmp/transcripts/"
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists(transcript_path):
        os.makedirs(transcript_path)
    uploaded_file = st.file_uploader(
        "上傳語音檔案", 
        type=["wav", "mp3", "ogg", "wma", "aac", "flac", "mp4", "m4a", "flv"]
    )

    markdown = read_markdown_file('media/model.md')
    st.markdown(markdown, unsafe_allow_html=True)
    
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        with open(os.path.join(upload_path, uploaded_file.name), "wb") as f:
            f.write((uploaded_file).getbuffer())
        with st.spinner(f"語音文件處理中..."):
            output_audio_file = uploaded_file.name.split('.')[0] + '.mp3'
            output_audio_file = to_mp3(uploaded_file, output_audio_file, upload_path, download_path)
            audio_file = open(os.path.join(download_path, output_audio_file), 'rb')
            audio_bytes = audio_file.read()

        # st.markdown("播放語音")
        st.audio(audio_bytes)

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            language = st.radio(
                "語言種類", 
                ('English', )
            )
        with col2:
            model_size = st.radio(
                "語音模型大小", 
                ('Tiny', 'Base', 'Small', 'Medium', 'Large')
            )
        with col3:
            ratio = st.slider(
                '摘要比例',
                0, 100, (10, 20)
            )
            print(ratio)

        if st.button('摘要'):
            with st.spinner("加載模型中..."):
                transcriber = Transcriber(language=language, model_size=model_size)
            with st.spinner(f"語音文件轉譯中..."):
                audio_file = str(os.path.abspath(os.path.join(download_path, output_audio_file)))
                result = transcriber(audio_file)

            # seg = pysbd.Segmenter(language="en", clean=False)
            # for text in seg.segment(result['text']):
            #     st.write(text)

            with st.spinner("生成摘要中..."):
                summarizer = pipeline("summarization", model='philschmid/bart-large-cnn-samsum')
                text = result['text']
                summary = summarizer(
                    text, 
                    min_length=int(ratio[0] * len(text) / 100), 
                    max_length=int(ratio[1] * len(text) / 100)
                )
                summary = summary[0]['summary_text']
                st.write(summary)


def main():
    page = st.sidebar.selectbox(
        "功能選單",
        ("介紹", "YouTube下載器", '語音轉譯器')
    )
    if page == "介紹":
        page_introduction()
    elif page == "YouTube下載器":
        page_youtube_downloader()
    elif page == "語音轉譯器":
        page_audio_transcriber()
    elif page == "語音摘要器 (TBD)":
        page_audio_summariser()


if __name__ == '__main__':
    st.set_page_config(
        page_title="Side Project",
        # page_icon="👋",
    )
    hide_footer()
    main()
