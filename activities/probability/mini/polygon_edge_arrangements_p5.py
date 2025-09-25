# activities/probability/mini/polygon_edge_arrangements_p5.py
import math
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "다각형 변 위 원(칩) 배열 — 경우의 수 직관",
    "description": "정다각형 변 바깥쪽에 동일 간격으로 원(칩)을 놓고 1..M을 배치할 때 ‘서로 다른 배열’ 개수를 두 관점(직순열 ÷ 중복, 원순열 × 기준 선택)으로 비교합니다. p5.js 시각화 포함.",
    "order": 9999,
    "hidden": True,   # mini 활동은 보통 숨김
}

def _stirling_log10_factorial(n: int) -> float:
    if n <= 1:
        return 0.0
    if n <= 5000:
        return float(np.sum(np.log10(np.arange(2, n + 1))))
    return (n * (math.log10(n) - math.log10(math.e))
            + 0.5 * math.log10(2 * math.pi * n))

def _sci_from_log10(log10x: float) -> str:
    if log10x < -6:
        return "≈ 0"
    exp = int(math.floor(log10x))
    mant = 10 ** (log10x - exp)
    return f"≈ {mant:.3f}×10^{exp}"

def render():
    st.header("⚪ 다각형 변 위 원(칩) 배열 — 서로 다른 배치 수")

    with st.sidebar:
        st.subheader("⚙️ 설정")
        n_sides = st.slider("다각형 변의 수 n", 3, 12, 8)
        is_regular = st.checkbox("정다각형", True)
        if is_regular:
            k_per_edge = st.slider("한 변에 놓을 원(칩) 개수 k", 1, 8, 3)
        else:
            k_per_edge = 1
            st.caption("※ 비정다각형에서는 한 변당 원(칩) 1개로 고정합니다.")
        consider_reflection = st.checkbox("거울대칭(반사)도 같은 배열로 본다", False)

        if "poly_arr_seed" not in st.session_state:
            st.session_state["poly_arr_seed"] = np.random.randint(0, 10**9)
        if st.button("🔀 원(칩) 번호 재배열(무작위)"):
            st.session_state["poly_arr_seed"] = np.random.randint(0, 10**9)

    M = n_sides * k_per_edge
    divisor = 1
    if is_regular:
        divisor *= (n_sides * k_per_edge)
        if consider_reflection and M >= 3:
            divisor *= 2

    log10_Mfact = _stirling_log10_factorial(M)
    log10_div = math.log10(divisor) if divisor > 1 else 0.0
    log10_unique_A = log10_Mfact - log10_div

    if is_regular:
        log10_circ = _stirling_log10_factorial(M - 1)
        if consider_reflection and M >= 3:
            log10_circ -= math.log10(2)
        log10_linear_from_circ = log10_circ + math.log10(n_sides * k_per_edge)
    else:
        log10_circ = None
        log10_linear_from_circ = None

    st.markdown(
        f"""
**문제 세팅**  
- 변의 수: **n = {n_sides}**, (정다각형: **{('네' if is_regular else '아니오')}**), 한 변의 원(칩) 수: **k = {k_per_edge}**  
- 전체 원(칩) 수: **M = n×k = {M}**

**‘서로 다른 배열’의 기준**  
- 정다각형일 때는 **회전(필수)**, 선택적으로 **거울대칭(반사)**까지 같은 배열로 봅니다.  
- 비정다각형일 때는 모든 변이 구분되므로 회전/반사 대칭이 **없습니다**(모두 다른 위치).
        """
    )

    colA, colB = st.columns(2)
    with colA:
        st.markdown("#### (A) 직순열로 보고 **중복을 나눠주기**")
        st.latex(r"\text{서로 다른 배열 수} \;=\; \dfrac{M!}{\;(\text{회전 중복})\times(\text{반사 중복})\;}")
        if is_regular:
            if consider_reflection and M >= 3:
                st.latex(fr"\;=\; \dfrac{{{M}!}}{{({n_sides}\times{k_per_edge})\times 2}}")
            else:
                st.latex(fr"\;=\; \dfrac{{{M}!}}{{({n_sides}\times{k_per_edge})}}")
        else:
            st.latex(fr"\;=\; {M}!")
        if M <= 20:
            import math as _m
            valA = _m.factorial(M) // (divisor if divisor > 0 else 1)
            st.code(f"= {valA:,}")
        else:
            st.code(_sci_from_log10(log10_unique_A))

    with colB:
        st.markdown("#### (B) **원순열**로 보고 ‘기준 선택’을 **곱해주기**")
        if is_regular:
            st.latex(r"\text{원순열(회전 무시)} \;=\; (M-1)! \quad (\text{반사까지 무시면 } (M-1)!/2)")
            if consider_reflection and M >= 3:
                st.latex(fr"\Rightarrow\ \text{{직선배열}} = \dfrac{{({M}-1)!}}{{2}}\;\times\;({n_sides}\times{k_per_edge})")
            else:
                st.latex(fr"\Rightarrow\ \text{{직선배열}} = ({M}-1)!\;\times\;({n_sides}\times{k_per_edge})")
            if M <= 20:
                import math as _m
                circ = _m.factorial(M - 1)
                if consider_reflection and M >= 3:
                    circ //= 2
                valB = circ * (n_sides * k_per_edge)
                st.code(f"= {valB:,}")
            else:
                st.code(_sci_from_log10(log10_linear_from_circ))
        else:
            st.info("비정다각형에서는 회전/반사 대칭이 없으므로 ‘원순열’ 관점이 의미 없습니다. 모든 위치가 구분 → M! 개.")

    st.divider()

    seed = int(st.session_state["poly_arr_seed"])
    html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <script src="https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.min.js"></script>
  <style>
    body{{margin:0}}
    .wrap{{max-width:1000px;margin:0 auto}}
    canvas{{border:1px solid #e5e7eb;border-radius:12px}}
    .legend{{font: 14px/1.4 system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; color:#334155; margin:6px 2px}}
  </style>
</head>
<body>
<div class="wrap">
  <div id="holder"></div>
  <div class="legend">
    • 정{'/' if is_regular else ''}비정: <b>{'정다각형' if is_regular else '비정다각형'}</b>,
    변 수 n = <b>{n_sides}</b>,
    한 변 원 수 k = <b>{k_per_edge}</b>,
    총 원 수 M = <b>{M}</b>
  </div>
</div>

<script>
let nSides   = {n_sides};
let isRegular= {str(is_regular).lower()};
let kPerEdge = {k_per_edge};
let seed     = {seed};

let W=960, H=560;
let verts=[];        // polygon vertices in CCW
let circles=[];      // {{x,y,label}}   // ← 이 주석 중괄호 이스케이프

let labels=[];       // shuffled [1..M]

function setup(){{
  let c=createCanvas(W,H); c.parent("holder");
  textFont("Arial"); randomSeed(seed); noiseSeed(seed);
  buildPolygon();
  placeCircles();
  labels = [];
  for(let i=1;i<=circles.length;i++) labels.push(i);
  shuffle(labels, true);
}}

function draw(){{
  background(255);
  translate(width/2, height/2);
  drawPolygon();
  drawEdgeCircles();
}}

function buildPolygon(){{
  verts=[];
  let R = 180;
  if(isRegular){{
    for(let i=0;i<nSides;i++) {{
      let ang = -HALF_PI + TWO_PI*i/nSides;
      let x = R*Math.cos(ang);
      let y = R*Math.sin(ang);
      verts.push({{x,y}});
    }}
  }} else {{
    for(let i=0;i<nSides;i++) {{
      let ang = -HALF_PI + TWO_PI*i/nSides;
      let r = R * (0.8 + 0.4*noise(i*0.17));
      let x = r*Math.cos(ang);
      let y = r*Math.sin(ang);
      verts.push({{x,y}});
    }}
  }}
}}

function centroid(){{
  let cx=0, cy=0;
  for(const v of verts){{ cx+=v.x; cy+=v.y; }}
  cx/=verts.length; cy/=verts.length;
  return {{x:cx, y:cy}};
}}

function placeCircles(){{
  circles = [];
  let C = centroid();
  for(let i=0;i<nSides;i++) {{
    const a = verts[i];
    const b = verts[(i+1)%nSides];
    let mx=(a.x+b.x)/2, my=(a.y+b.y)/2;
    let ex=b.x-a.x, ey=b.y-a.y;
    let nx = -ey, ny = ex;
    let len = Math.hypot(nx,ny); nx/=len; ny/=len;
    let vx = mx - C.x, vy = my - C.y;
    if(nx*vx + ny*vy < 0) {{ nx=-nx; ny=-ny; }}
    let K = isRegular ? kPerEdge : 1;
    for(let j=0;j<K;j++) {{
      let t = (j+1)/(K+1);
      let px = a.x*(1-t) + b.x*t;
      let py = a.y*(1-t) + b.y*t;
      let off = 24;
      px += nx*off; py += ny*off;
      circles.push({{x:px, y:py}});
    }}
  }}
}}

function drawPolygon(){{
  noFill(); stroke(0); strokeWeight(1.5);
  beginShape();
  for(const v of verts) vertex(v.x, v.y);
  endShape(CLOSE);
  textAlign(CENTER, BOTTOM); noStroke(); fill(120); textSize(12);
  for(let i=0;i<nSides;i++) {{
    let a=verts[i], b=verts[(i+1)%nSides];
    let mx=(a.x+b.x)/2, my=(a.y+b.y)/2;
    text((i+1), mx, my-4);
  }}
}}

function drawEdgeCircles(){{
  textAlign(CENTER, CENTER); textSize(14);
  for(let i=0;i<circles.length;i++) {{
    const c = circles[i];
    noStroke(); fill(245);
    circle(c.x, c.y, 34);
    stroke(0); noFill(); circle(c.x, c.y, 34);
    noStroke(); fill(20);
    text(labels[i], c.x, c.y+1);
  }}
}}
</script>
</body>
</html>
    """
    components.html(html, height=620)

    st.divider()
    st.markdown(
        """
### 🧠 두 가지 관점 요약

1) **직선(일렬) 배치로 본 뒤, 대칭으로 생기는 ‘중복’을 나눠준다.**  
   - (정다각형) 회전으로 같은 배치가 **n×k**개 → `M! / (n·k)`  
   - (선택) 거울대칭까지 같으면 → `M! / ((n·k)·2)`  
   - (비정다각형) 모든 위치가 구분됨 → `M!`

2) **원순열(회전 무시)로 본 뒤, ‘기준 선택’을 곱해준다.**  
   - 회전 무시면 `(M−1)!` (반사도 무시면 `(M−1)!/2`)  
   - 직선(기준)으로 환산: 기준 자리 **n·k**가지 → `(M−1)! · (n·k)` (반사 포함 시 `/2`)
        """
    )
