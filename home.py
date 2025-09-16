import streamlit as st
from utils import set_base_page, page_header, callout

set_base_page(page_title="수학 시뮬레이션 허브", page_icon="🧮")

page_header("수학 시뮬레이션 허브", "수업에 바로 쓰는 인터랙티브 실험실")

st.markdown("""
이 웹앱은 수업에 활용할 **시뮬레이션/시각화 도구**를 모아둔 멀티 페이지 허브입니다.
왼쪽 **사이드바**에서 원하는 시뮬레이터를 선택해 주세요.  
필요한 기능은 언제든지 요청해 주세요. 제가 **새 페이지**로 깔끔하게 추가해 드릴게요. 😄
""")

with st.expander("📂 내 자료(CSV) 빠르게 불러오기/미리보기"):
    st.write("로컬 CSV를 올려 간단히 확인하거나, 각 페이지에서 재활용하세요.")
    up = st.file_uploader("CSV 업로드", type=["csv"])
    if up is not None:
        import pandas as pd
        df = pd.read_csv(up)
        st.dataframe(df.head(50))
        st.session_state["__LAST_UPLOADED_DF__"] = df
        st.success("세션에 저장했어요. 다른 페이지에서도 사용 가능!")

callout(
    "새 페이지를 추가하려면?",
    """
    1) `pages/6_✨_내_시뮬레이터.py` 파일을 만들고,
    2) 아래 템플릿을 복붙한 뒤, 본문에 원하는 로직과 그래프를 작성하세요.
    3) 파일을 저장하면 **자동으로 사이드바**에 나타납니다.
    """
)

st.code(
    '''import streamlit as st
from utils import set_base_page, page_header
import numpy as np
import plotly.express as px

set_base_page(page_title="내 시뮬레이터", page_icon="✨")
page_header("내 시뮬레이터", "여기에 한 줄 설명")

st.sidebar.subheader("⚙️ 설정")
n = st.sidebar.slider("표본 개수", 10, 5000, 500)
x = np.random.randn(n)
fig = px.histogram(x, nbins=30, title="표본 분포")
st.plotly_chart(fig, use_container_width=True)''',
    language="python"
)

st.info("문의/요청: 파라미터 옵션, 레이아웃, 설명 도형, 실험 기록 저장 등 무엇이든 말씀해 주세요!")
