import streamlit as st
import streamlit.components.v1 as components

def page_header(title: str, subtitle: str = "", icon: str = ""):
    icon_html = f"{icon} " if icon else ""
    st.markdown(
        f"""
        <div style="margin-top:0; padding-top:0;">
          <h3 style="margin:0.2rem 0 0.5rem 0; font-weight:600;">
            {icon_html}{title}
          </h3>
          {f"<div style='color:var(--secondary-text-color); font-size:0.95rem; margin:0 0 0.6rem 0;'>{subtitle}</div>" if subtitle else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def anchor(name: str = "content"):
    st.markdown(f"<a id='{name}'></a>", unsafe_allow_html=True)

def scroll_to(name: str = "content"):
    components.html(f"<script>window.location.hash = '{name}'</script>", height=0)

def keep_scroll(key: str = "default"):
    """
    위젯 변경으로 rerun이 발생해도 직전의 스크롤 위치를 복원합니다.
    key: 액티비티/페이지별로 구분 저장하고 싶을 때 식별자.
    """
    components.html(f"""
    <script>
    (function(){{
      const KEY = 'st_scroll::{key}::' + location.pathname + location.search;
      function restore() {{
        const y = sessionStorage.getItem(KEY);
        if (y !== null) {{
          window.scrollTo(0, parseFloat(y));
        }}
      }}
      // 복원: 즉시 + 약간 지연 2회 (DOM 렌더 이후도 커버)
      restore();
      setTimeout(restore, 50);
      setTimeout(restore, 250);

      // 저장: 스크롤 시 requestAnimationFrame으로 쓰로틀
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

      // 혹시 값을 못 저장한 경우 대비, 주기적으로도 백업
      setInterval(function(){{
        sessionStorage.setItem(KEY, window.scrollY);
      }}, 500);
    }})();
    </script>
    """, height=0)
