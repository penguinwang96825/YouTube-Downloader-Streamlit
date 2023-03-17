# -*- coding: utf-8 -*-
"""
Entrypoint file

Authors
 * Yang Wang 2023
"""
import os
import streamlit as st

from src.downloader import get_youtube_video_info
from src.utils import hide_footer


def page_introduction():
    st.markdown(
        f"# DONE\n"
        f" - 提供網頁版下載YouTube影片\n"
        f"# TODO\n"
        f" - 影片Transcribe功能\n"
    )


def page_youtube_downloader():
    st.title('YouTube下載器')
    options = {}
    options['ext'] = st.sidebar.multiselect(
        '檔名',
        ['3gp', 'm4a', 'mp4'], 
        ['3gp', 'm4a', 'mp4']
    )
    # https://www.youtube.com/watch?v=HQDDlgGy2hg
    url = st.text_input(label='請輸入網址: ')

    if url:
        info_df = get_youtube_video_info(url, options)
        info_df = info_df.to_html(escape=False)
        st.write(info_df, unsafe_allow_html=True)


def page_audio_summariser():
    st.title('語音摘要器')


def main():
    page = st.sidebar.selectbox(
        "功能選單",
        ("介紹", "YouTube下載器", '語音摘要器 (TBD)')
    )
    if page == "介紹":
        page_introduction()
    elif page == "YouTube下載器":
        page_youtube_downloader()
    elif page == "語音摘要器 (TBD)":
        page_audio_summariser()


if __name__ == '__main__':
    st.set_page_config(
        page_title="Side Project",
        # page_icon="👋",
    )
    hide_footer()
    main()
