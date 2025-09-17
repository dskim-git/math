# utils.py
import streamlit as st
import streamlit.components.v1 as components

def page_header(title: str, subtitle: str = "", icon: str = "", top_rule: bool = True):
    """
    라인(얇은 회색) + 제목 + 부제를 한 세트로, 여백을 최소화해 렌더합니다.
    - 제목은 render()에서만 호출해 '중복 제목'을 방지하세요.
    - top_rule=False로 주면 라인을 생략할 수 있습니다.
    """
    if top_rule:
        st.markdown(
            "<hr style='margin:0.25rem 0 0.35rem 0; border:none; "
            "border-top:1px solid var(--secondary-background-color);' />",
            unsafe_allow_html=True,
        )

    icon_html = f"{icon} " if icon else ""
    st.markdown(
        f"<h3 style='margin:0.25rem 0 0.45rem 0; font-weight:700;'>{icon_html}{title}</h3>",
        unsafe_allow_html=True,
    )

    if subtitle:
        st.markdown(
            "<div style='color:var(--secondary-text-color); font-size:0.95rem; "
            "margin:0 0 0.6rem 0;'>"
            f"{subtitle}"
            "</div>",
            unsafe_allow_html=True,
        )

def anchor(name: str = "content"):
    """현재 위치에 스크롤 앵커를 심습니다."""
    st.markdown(f"<a id='{name}'></a>", unsafe_allow_html=True)

def scroll_to(name: str = "content"):
    """지정한 앵커로 즉시 스크롤 이동합니다."""
    components.html(f"<script>window.location.hash = '{name}'</script>", height=0)

def keep_scroll(key: str = "default"):
    """
    rerun이 발생해도 직전 스크롤 위치를 복원합니다.
    같은 페이지라도 쿼리스트링/경로가 다르면 별도로 저장됩니다.
    """
    components.html(
        f"""
        <script>
        (function(){{
          const KEY = 'st_scroll::{key}::' + location.pathname + location.search;
          function restore(){{
            const y = sessionStorage.getItem(KEY);
            if (y !== null) {{
              window.scrollTo(0, parseFloat(y));
            }}
          }}
          // 렌더 직후와 약간의 지연 후 2회 복원
          restore(); setTimeout(restore, 50); setTimeout(restore, 250);

          // 스크롤 이벤트를 rAF로 쓰로틀하여 저장
          let ticking = false;
          window.addEventListener('scroll', function(){{
            if (!ticking) {{
              window.requestAnimationFrame(function(){{
                sessionStorage.setItem(KEY, window.scrollY);
                ticking = false;
              }});
              ticking = true;
            }}
          }});
          // 혹시 모를 누락 대비 주기적 백업
          setInterval(function(){{
            sessionStorage.setItem(KEY, window.scrollY);
          }}, 500);
        }})();
        </script>
        """,
        height=0,
    )

# ---- 과거 코드 호환용 (중복 제목 방지를 위해 아무것도 하지 않는 no-op) ----
def set_base_page(title: str, icon: str = "📊"):
    """레거시 코드 호환용. 현재 레이아웃에서는 수행할 작업이 없습니다."""
    return
