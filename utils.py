# utils.py
import streamlit as st
import streamlit.components.v1 as components

def page_header(title: str, subtitle: str = "", icon: str = "", top_rule: bool = True):
    """회색 라인과 제목을 한 블록으로 출력(여백 극소화)."""
    icon_html = f"{icon} " if icon else ""
    rule_html = (
        "<hr style='margin:0.25rem 0 0.25rem 0; border:none; "
        "border-top:1px solid var(--secondary-background-color);' />"
        if top_rule else ""
    )
    subtitle_html = (
        f"<div style='color:var(--secondary-text-color); font-size:0.95rem; "
        f"margin:0 0 0.50rem 0;'>{subtitle}</div>"
        if subtitle else ""
    )
    st.markdown(
        f"""
        <div style="margin:0; padding:0;">
          {rule_html}
          <h3 style="margin:0.15rem 0 0.35rem 0; font-weight:700;">
            {icon_html}{title}
          </h3>
          {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

def anchor(name: str = "content"):
    st.markdown(f"<a id='{name}'></a>", unsafe_allow_html=True)

def scroll_to(name: str = "content"):
    components.html(f"<script>window.location.hash = '{name}'</script>", height=0)

def keep_scroll(key: str = "default", mount: str = "sidebar"):
    """
    rerun 후 직전 스크롤 위치 복원 스크립트.
    mount: 'sidebar' | 'main'  (여백을 없애려면 'sidebar' 권장)
    - 일부 환경에서 components.html이 기본 높이(≈150px)를 차지하는 문제를 피하기 위해
      height=1 로 지정 + iframe 내부에서 body를 0x0 로 축소합니다.
    """
    html = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <style>
          /* iframe 내부를 사실상 0x0로 축소 */
          html, body {{
            margin:0 !important; padding:0 !important;
            width:0 !important; height:0 !important; overflow:hidden !important;
          }}
        </style>
      </head>
      <body>
        <script>
        (function(){{
          const KEY = 'st_scroll::{key}::' + location.pathname + location.search;
          function restore(){{
            const y = sessionStorage.getItem(KEY);
            if (y !== null) window.scrollTo(0, parseFloat(y));
          }}
          restore(); setTimeout(restore, 50); setTimeout(restore, 250);
          let ticking = false;
          window.addEventListener('scroll', function(){{
            if (!ticking) {{
              window.requestAnimationFrame(function(){{
                sessionStorage.setItem(KEY, window.scrollY);
                ticking = false;
              }}); ticking = true;
            }}
          }});
          setInterval(function(){{
            sessionStorage.setItem(KEY, window.scrollY);
          }}, 500);
        }})();
        </script>
      </body>
    </html>
    """
    # height=1 로 지정(0은 일부 빌드에서 기본값으로 치환되어 큰 빈칸이 생김)
    if mount == "sidebar":
        with st.sidebar:
            components.html(html, height=0, scrolling=False)
            # 사이드바 쪽 components 외곽 여백도 0으로(한 번만 주입)
            if "_side_comp_tight" not in st.session_state:
                st.session_state["_side_comp_tight"] = True
                st.markdown(
                    """
                    <style>
                      /* 사이드바 안의 컴포넌트 컨테이너 여백 최소화 */
                      section[data-testid="stSidebar"] .stComponent { margin: 0 !important; padding: 0 !important; }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        components.html(html, height=1, scrolling=False)

# 레거시 호환(아무 것도 안 함)
def set_base_page(title: str, icon: str = "📊"):
    return
