# -*- coding: utf-8 -*-
"""
Helper functions

Authors
 * Yang Wang 2023
"""
import streamlit as st
from pathlib import Path


def hide_footer():
    hide_streamlit_style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def read_markdown_file(markdown_file):
    """
    Examples
    --------
    >>> markdown = read_markdown_file("introduction.md")
    >>> st.markdown(markdown, unsafe_allow_html=True)
    """
    return Path(markdown_file).read_text()