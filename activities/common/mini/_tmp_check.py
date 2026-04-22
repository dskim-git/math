# activities/common/mini/equation_history_flash.py
"""
방정식 해법의 역사 – 인터랙티브 플래시 스토리 (초상화·영상·애니메이션 포함)
이차방정식 → 삼·사차방정식 쟁탈전 → 5차 방정식의 비가해성
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "방정식역사플래시"
