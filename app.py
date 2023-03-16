import os
import yt_dlp
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
    info_df['url'] = info_df['url'].apply(make_clickable)
    return info_df


def make_clickable(link):
    text = link.split('=')[1]
    return f'<a target="_blank" href="{link}">{text}</a>'


def main():
    st.title('YouTube下載器')
    # https://www.youtube.com/watch?v=HQDDlgGy2hg
    url = st.text_input(label='請輸入網址: ')

    if url:
        info_df = get_youtube_video_info(url)
        info_df = info_df.to_html(escape=False)
        st.write(info_df, unsafe_allow_html=True)
        # st.table(info_df)


if __name__ == '__main__':
    main()