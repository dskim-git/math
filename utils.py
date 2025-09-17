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
    rerun 후 직전 스크롤 위치 복원.
    mount: 'sidebar' | 'main'  (여백을 없애려면 'sidebar' 권장)
    """
    html = f"""
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
    """
    if mount == "sidebar":
        with st.sidebar:
            components.html(html, height=0)
    else:
        components.html(html, height=0)

# 레거시 호환(아무 것도 안 함)
def set_base_page(title: str, icon: str = "📊"):
    return
