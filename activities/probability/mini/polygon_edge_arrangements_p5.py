# activities/probability/mini/polygon_edge_arrangements_p5.py
import math
import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "다각형 변 위 원(칩) 배열 — 경우의 수 직관",
    "description": "정/비정다각형 변 바깥쪽에 원(칩)을 두고 1..M 라벨을 배치. 비정다각형에서는 각 변별로 원 개수를 다르게 설정 가능. 직순열÷중복 vs 원순열×기준 관점 비교 + p5.js 시각화.",
    "order": 9999,
    "hidden": True,  # mini는 보통 숨김
}

# ─────────────────────────────────────────────────────────────
def _log10_factorial(n: int) -> float:
    if n <= 1:
        return 0.0
    if n <= 5000:
        return float(np.sum(np.log10(np.arange(2, n + 1))))
    # Stirling 근사
    return (n * (math.log10(n) - math.log10(math.e))
            + 0.5 * math.log10(2 * math.pi * n))

def _sci_from_log10(log10x: float) -> str:
    if log10x < -6:
        return "≈ 0"
    exp = int(math.floor(log10x))
    mant = 10 ** (log10x - exp)
    return f"≈ {mant:.3f}×10^{exp}"

# ─────────────────────────────────────────────────────────────
def render():
    st.header("⚪ 다각형 변 위 원(칩) 배열 — 서로 다른 배치 수")

    with st.sidebar:
        st.subheader("⚙️ 설정")
        n_sides = st.slider("다각형 변의 수 n", 3, 12, 8)
        is_regular = st.checkbox("정다각형(모든 변/각 동일, 회전/반사 대칭 허용)", True)

        # 정다각형: 한 변에 동일 k, 비정다각형: 변별 개수 개별 설정
        edge_counts: list[int] = []
        if is_regular:
            k_per_edge = st.slider("한 변에 놓을 원(칩) 개수 k", 1, 12, 3)
            edge_counts = [int(k_per_edge)] * n_sides
        else:
            st.markdown("**각 변별 원(칩) 개수**")
            # ‘모두 동일로 채우기’ 편의 기능
            c_default = st.number_input("모두 동일로 채우기 값", 0, 12, 2, key="fill_all_default")
            cols = st.columns(4)
            for i in range(n_sides):
                key = f"edgecnt_{i}"
                if key not in st.session_state:
                    st.session_state[key] = c_default
                with cols[i % 4]:
                    val = st.number_input(f"변 {i+1}", 0, 12, int(st.session_state[key]), key=key)
                edge_counts.append(int(val))
            if st.button("모든 변을 위 값으로 채우기"):
                for i in range(n_sides):
                    st.session_state[f"edgecnt_{i}"] = int(c_default)
                st.experimental_rerun()

        consider_reflection = st.checkbox("거울대칭(반사)도 같은 배열로 본다 (정다각형일 때만 의미)", False)

        # 무작위 라벨 시드
        if "poly_arr_seed" not in st.session_state:
            st.session_state["poly_arr_seed"] = np.random.randint(0, 10**9)
        if st.button("🔀 원(칩) 번호 재배열(무작위)"):
            st.session_state["poly_arr_seed"] = np.random.randint(0, 10**9)

    # 총 원(칩) 수
    M = int(sum(edge_counts))

    # ── 경우의 수 계산 ─────────────────────────────────────────────
    # (A) 직순열로 보고 중복 나누기
    divisor = 1
    if is_regular:
        divisor *= (n_sides * edge_counts[0])  # 회전 중복
        if consider_reflection and M >= 3:
            divisor *= 2                         # 반사 중복

    log10_Mfact = _log10_factorial(M)
    log10_div = math.log10(divisor) if divisor > 1 else 0.0
    log10_unique_A = log10_Mfact - log10_div

    # (B) 원순열 × 기준 자리 수 (정다각형에서만 의미)
    if is_regular and M >= 1:
        log10_circ = _log10_factorial(M - 1)
        if consider_reflection and M >= 3:
            log10_circ -= math.log10(2)
        log10_linear_from_circ = log10_circ + math.log10(n_sides * edge_counts[0])
    else:
        log10_circ = None
        log10_linear_from_circ = None

    # 설명
    disp_counts = ", ".join(map(str, edge_counts))
    st.markdown(
        f"""
**문제 세팅**  
- 변의 수: **n = {n_sides}**  
- 각 변의 원(칩) 개수: **[{disp_counts}]** → 총 원 수 **M = {M}**  
- **정다각형**이면 회전(필수), 선택 시 반사(거울대칭)까지 같은 배열로 취급.  
- **비정다각형**이면 모든 위치가 구분되므로 대칭 중복을 적용하지 **않습니다**.
        """
    )

    colA, colB = st.columns(2)
    with colA:
        st.markdown("#### (A) 직순열로 보고 **중복을 나눠주기**")
        if is_regular:
            st.latex(r"\text{서로 다른 배열 수} \;=\; \dfrac{M!}{\;(\text{회전}=n\cdot k)\times(\text{반사})\;}")
            if consider_reflection and M >= 3:
                st.latex(fr"\;=\; \dfrac{{{M}!}}{{({n_sides}\times{edge_counts[0]})\times 2}}")
            else:
                st.latex(fr"\;=\; \dfrac{{{M}!}}{{({n_sides}\times{edge_counts[0]})}}")
        else:
            st.latex(r"\text{비정다각형:}\quad \text{대칭 중복 없음} \;\Rightarrow\; M!")

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
                st.latex(fr"\Rightarrow\ \text{{직선배열}} = \dfrac{{({M}-1)!}}{{2}}\;\times\;({n_sides}\times{edge_counts[0]})")
            else:
                st.latex(fr"\Rightarrow\ \text{{직선배열}} = ({M}-1)!\;\times\;({n_sides}\times{edge_counts[0]})")
            if M <= 20:
                import math as _m
                circ = _m.factorial(M - 1) if M >= 1 else 1
                if consider_reflection and M >= 3:
                    circ //= 2
                valB = circ * (n_sides * edge_counts[0] if M >= 1 else 1)
                st.code(f"= {valB:,}")
            else:
                st.code(_sci_from_log10(log10_linear_from_circ))
        else:
            st.info("비정다각형에서는 회전/반사 대칭이 없으므로 ‘원순열×기준자리’ 관점이 의미 없습니다. (모든 위치가 구분 → M!)")

    st.divider()

    # ── p5.js 시각화: 변별 개수(edge_counts) 그대로 전달 ──────────────────
    seed = int(st.session_state["poly_arr_seed"])
    counts_json = json.dumps(edge_counts)  # JS로 보낼 배열
    counts_disp = disp_counts
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
    • 형태: <b>{'정다각형' if is_regular else '비정다각형'}</b>,
    변 수 n = <b>{n_sides}</b>,
    변별 원 수 = <b>[{counts_disp}]</b>,
    총 원 수 M = <b>{M}</b>
  </div>
</div>

<script>
let nSides   = {n_sides};
let isRegular= {str(is_regular).lower()};
let counts   = {counts_json};   // 각 변별 원 개수 배열
let seed     = {seed};
let M        = {M};

let W=960, H=560;
let verts=[];        // polygon vertices
let circles=[];      // {{x,y}}  // f-string 중괄호 이스케이프
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
      verts.push({{x:R*Math.cos(ang), y:R*Math.sin(ang)}});
    }}
  }} else {{
    for(let i=0;i<nSides;i++) {{
      let ang = -HALF_PI + TWO_PI*i/nSides;
      let r = R * (0.8 + 0.4*noise(i*0.17));
      verts.push({{x:r*Math.cos(ang), y:r*Math.sin(ang)}});
    }}
  }}
}}

function centroid(){{
  let cx=0, cy=0;
  for(const v of verts){{ cx+=v.x; cy+=v.y; }}
  return {{x:cx/verts.length, y:cy/verts.length}};
}}

function placeCircles(){{
  circles = [];
  let C = centroid();
  for(let i=0;i<nSides;i++) {{
    const a = verts[i];
    const b = verts[(i+1)%nSides];
    // 변의 중점과 외측 법선
    let mx=(a.x+b.x)/2, my=(a.y+b.y)/2;
    let ex=b.x-a.x, ey=b.y-a.y;
    let nx = -ey, ny = ex;
    let len = Math.hypot(nx,ny); nx/=len; ny/=len;
    // 다각형 바깥쪽으로 향하게
    let vx = mx - C.x, vy = my - C.y;
    if(nx*vx + ny*vy < 0) {{ nx=-nx; ny=-ny; }}
    // 변 i에 counts[i]개 균등 배치
    let k = counts[i];
    for(let j=0;j<k;j++) {{
      let t = (j+1)/(k+1);
      let px = a.x*(1-t) + b.x*t;
      let py = a.y*(1-t) + b.y*t;
      let off = 24;  // 바깥 오프셋
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
    noStroke(); fill(245); circle(c.x, c.y, 34);
    stroke(0); noFill(); circle(c.x, c.y, 34);
    noStroke(); fill(20); text(i < labels.length ? labels[i] : '', c.x, c.y+1);
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
   - (정다각형) 회전으로 같은 배치가 **n·k**개 → `M! / (n·k)`  
   - (선택) 거울대칭까지 같으면 → `M! / ((n·k)·2)`  
   - (비정다각형) 모든 위치가 구분됨 → **`M!`**

2) **원순열(회전 무시)로 본 뒤, ‘기준 선택’을 곱해준다.**  
   - 회전 무시면 `(M−1)!` (반사도 무시면 `(M−1)!/2`)  
   - 직선(기준)으로 환산: 기준 자리 **n·k**가지 → `(M−1)! · (n·k)` (반사 포함 시 `/2`)
        """
    )
