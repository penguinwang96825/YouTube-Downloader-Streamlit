# -*- coding: utf-8 -*-
"""
YouTube video download scripts

Authors
 * Yang Wang 2023
"""
import os
import yt_dlp
import pandas as pd


def get_youtube_video_info(url, options):
    # Extract the YouTube video information
    os.system(f'yt-dlp --list-formats {url}')
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    
    # Transform the dict into a dataframe
    info_df = pd.DataFrame(info['formats'])
    info_df = info_df[
        ['format_note', 'ext', 'acodec', 'vcodec', 'url']
    ]

    # Data  pre-processing
    info_df = info_df.query('ext not in ["mhtml", "webm"]')
    info_df = info_df.query(f'ext in {options["ext"]}')
    info_df = info_df.replace({'acodec': 'none'}, 'video only')
    info_df = info_df.replace({'vcodec': 'none'}, 'audio only')
    info_df['acodec'] = info_df['acodec'].apply(
        lambda x: '❎' if x=='video only' else '✅'
    )
    info_df['vcodec'] = info_df['vcodec'].apply(
        lambda x: '❎' if x=='audio only' else '✅'
    )
    info_df['url'] = info_df['url'].apply(make_clickable)
    info_df.columns = ['畫質', '檔名', '音訊', '影像', '網址']
    info_df = info_df.reset_index(drop=True)

    return info_df


def make_clickable(link):
    return f'<a target="_blank" href="{link}">link</a>'