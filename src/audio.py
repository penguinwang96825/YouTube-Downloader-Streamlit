# -*- coding: utf-8 -*-
"""
Audio processing functions

Authors
 * Yang Wang 2023
"""
import os
import whisper
import streamlit as st
from pydub import AudioSegment


@st.cache_data(persist=True)
def to_mp3(audio_file, output_audio_file, upload_path, download_path):
    audio_tags = {'comments': 'Converted using pydub!'}

    # Converting Different Audio Formats To MP3
    if audio_file.name.split('.')[-1].lower()=="wav":
        audio_data = AudioSegment.from_wav(os.path.join(upload_path, audio_file.name))
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="mp3":
        audio_data = AudioSegment.from_mp3(os.path.join(upload_path, audio_file.name))
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="ogg":
        audio_data = AudioSegment.from_ogg(os.path.join(upload_path, audio_file.name))
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="wma":
        audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name),"wma")
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="aac":
        audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name),"aac")
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="flac":
        audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name),"flac")
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="flv":
        audio_data = AudioSegment.from_flv(os.path.join(upload_path, audio_file.name))
        audio_data.export(os.path.join(download_path,  output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="mp4":
        audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name),"mp4")
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)
    
    elif audio_file.name.split('.')[-1].lower()=="m4a":
        audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name),"m4a")
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)
    
    return output_audio_file
