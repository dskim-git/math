# activities/probability/pascal_modulo_view.py
import streamlit as st
import streamlit.components.v1 as components

# utils: 제목/라인(여백 최소), 앵커/점프
try:
    from utils import page_header, anchor, scroll_to
except Exception:
    def page_header(title: str, subtitle: str = "", icon: str = "", top_rule: bool = True):
        if top_rule:
            st.markdown("---")
        st.markdown(f"### {icon+' ' if icon else ''}{title}")
        if subtitle:
            st.caption(subtitle)
    def anchor(name: str = "content"):
        st.markdown(f"<a id='{name}'></a>", unsafe_allow_html=True)
    def scroll_to(name: str = "content"):
        import streamlit.components.v1 as _components
        _components.html(f"<script>window.location.hash='{name}'</script>", height=0)

META = {
    "title": "파스칼 삼각형 모듈로 시각화",
    "description": "파스칼 삼각형의 항을 mod m로 색칠하여 패턴(예: 시에르핀스키 삼각형 등)을 관찰합니다.",
}

# ---- 세션 키 & 기본값 ----
K_ZOOM = "pascal_zoom"
K_MOD  = "pascal_mod"
K_REM  = "pascal_rem"
JUMP   = "pascal_jump"

DEFAULTS = {
    K_ZOOM: 5.0,  # 확대 배율 (baseSpacing / zoom)
    K_MOD:  2,
    K_REM:  0,
}

def _ensure_defaults():
    for k, v in DEFAULTS.items():
        if k not in st.session_state:
            st.session_state[k] = v

def _mark_changed():
    # 위젯 변경 시, rerun 후 캔버스 위치로 점프
    st.session_state[JUMP] = "canvas"

def render():
    _ensure_defaults()

    page_header("파스칼 삼각형 모듈로 시각화", "이항계수를 mod m로 색칠하여 패턴을 탐구합니다.", icon="🔺", top_rule=True)

    # ---- 사이드바 컨트롤 (즉시 반영) ----
    with st.sidebar:
        st.subheader("⚙️ 설정")

        st.slider("🔍 확대 (View Scale)", 1.0, 20.0, step=0.1, key=K_ZOOM, on_change=_mark_changed)
        st.slider("🎯 modulo m", 2, 12, step=1, key=K_MOD, on_change=_mark_changed)

        # modulo 변경에 따라 remainder 상한 조정
        mod_val = int(st.session_state[K_MOD])
        # 슬라이더는 value 없이 key만 쓰므로, 상한만 동적으로 바뀌어도 세션값 표시가 자동 동기화됨
        st.slider("🎯 remainder (0 ≤ r ≤ m−1)", 0, mod_val - 1, step=1, key=K_REM, on_change=_mark_changed)

    # ---- 현재 설정 ----
    zoom = float(st.session_state[K_ZOOM])
    mod  = int(st.session_state[K_MOD])
    rem  = int(st.session_state[K_REM])

    # 안전장치: remainder가 범위를 벗어나면 0으로 보정
    if rem > mod - 1:
        st.session_state[K_REM] = 0
        rem = 0

    # ---- 앵커(캔버스 위치) ----
    anchor("canvas")

    # ---- p5.js 캔버스 임베드 ----
    # - Streamlit iframe 내부에서 CDN을 로드해도 브라우저가 처리하므로 OK
    # - windowWidth/Height는 iframe 크기를 사용
    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<style>
  html, body {{ margin:0; padding:0; overflow:hidden; background:#ffffff; }}
  #label-wrap {{
    position: fixed; left: 12px; top: 12px; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    background: rgba(255,255,255,0.85); padding: 8px 10px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    user-select: none; font-size: 13px; line-height: 1.25;
  }}
  .pill {{ display:inline-block; margin-right:8px; padding:2px 8px; border-radius:999px; background:#f2f4f7; }}
  canvas {{ display:block; }}
</style>
</head>
<body>
<div id="label-wrap">
  <span class="pill">🔍 Scale: {zoom:.1f}</span>
  <span class="pill">m = {mod}</span>
  <span class="pill">r = {rem}</span>
</div>
<script>
  // Python에서 전달된 현재 설정
  const PY_SCALE = {zoom};
  const PY_MOD   = {mod};
  const PY_REM   = {rem};

  let pascalTriangle = [];
  const baseSpacing = 60;

  function setup() {{
    createCanvas(windowWidth, windowHeight);
    noStroke();
  }}

  function windowResized() {{
    resizeCanvas(windowWidth, windowHeight);
  }}

  function draw() {{
    background(255);

    const scaleFactor = PY_SCALE;
    const spacing = baseSpacing / scaleFactor;
    const marginTop = 16 + 40; // 라벨 영역 고려한 약간의 상단 여백
    const visibleRows = Math.floor((height - marginTop) / spacing);

    generatePascalTriangle(visibleRows);
    drawPascalTriangle(spacing, visibleRows, marginTop);
  }}

  function generatePascalTriangle(rowCount) {{
    pascalTriangle = [];
    for (let n = 0; n < rowCount; n++) {{
      pascalTriangle[n] = [];
      for (let k = 0; k <= n; k++) {{
        if (k === 0 || k === n) {{
          pascalTriangle[n][k] = 1n;
        }} else {{
          pascalTriangle[n][k] = pascalTriangle[n - 1][k - 1] + pascalTriangle[n - 1][k];
        }}
      }}
    }}
  }}

  function drawPascalTriangle(spacing, rowCount, offsetY) {{
    textAlign(CENTER, CENTER);
    for (let i = 0; i < rowCount; i++) {{
      for (let j = 0; j < pascalTriangle[i].length; j++) {{
        const val = pascalTriangle[i][j];
        const x = width / 2 + (j - i / 2) * spacing;
        const y = i * spacing + offsetY;

        if (val % BigInt(PY_MOD) === BigInt(PY_REM)) {{
          fill(0, 102, 204);
        }} else {{
          fill(230);
        }}

        ellipse(x, y, spacing * 0.6);

        if (spacing >= 20) {{
          fill(0);
          textSize(spacing * 0.25);
          text(val.toString(), x, y);
        }}
      }}
    }}
  }}
</script>
</body>
</html>
    """

    # 캔버스 높이(px). 필요하면 사이드바에서 높이 slider 추가 가능
    components.html(html, height=720, scrolling=False)

    # 변경 직후 캔버스 위치로 점프(스크롤 복귀)
    if st.session_state.get(JUMP) == "canvas":
        scroll_to("canvas")
        st.session_state[JUMP] = None

    # 도움말(수업용): 모듈러 패턴 힌트
    with st.expander("📘 관찰 포인트"):
        st.markdown(
            "- m=2, r=1 → 시에르핀스키 삼각형 패턴이 나타납니다.  \n"
            "- 소수 m일 때 각 행의 항들은 페르마 성질과 연결되어 흥미로운 격자 패턴을 보입니다.  \n"
            "- 확대를 줄이면(Scale↑) 더 많은 행이 한 화면에 보이고, 늘리면(Scale↓) 개별 항의 숫자까지 읽을 수 있어요."
        )
