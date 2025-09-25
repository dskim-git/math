# activities/probability/mini/polygon_edge_arrangements_p5.py
import math
import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "다각형 변 위 원(칩) 배열 — 대칭을 고려한 경우의수",
    "description": "정/비정다각형에서 변마다 다른 개수의 원(칩)을 둘 수 있음. 변 개수 배열의 회전·반사 대칭을 자동 판단해 M!/|H| (직순열÷중복) = (M−1)!×(M/|H|) (원순열×기준)을 비교합니다.",
    "order": 9999,
    "hidden": True,   # mini는 보통 숨김
}

# ─────────────────────────────────────────────────────────────
# 로그-팩토리얼(크기 클 때 표시용)
def _log10_factorial(n: int) -> float:
    if n <= 1:
        return 0.0
    if n <= 5000:
        import numpy as _np
        return float(_np.sum(_np.log10(_np.arange(2, n + 1))))
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
# 변 개수 배열 counts 의 대칭(회전/반사) 안정자 크기 |H| 계산
# - 회전 안정자 크기 R = |{ s | rotate(counts, s) == counts }|
# - 반사 안정자 여부: counts == reverse(rotate(counts, s)) (축이 꼭 꼭짓점/변 중앙 둘 다 가능)
#   반사가 하나라도 존재하면 반사 수 = R (각 주기마다 축이 함께 이동)
def _rot_count(counts: list[int]) -> int:
    n = len(counts)
    def eq_rot(s):
        return all(counts[(i+s) % n] == counts[i] for i in range(n))
    return sum(1 for s in range(n) if eq_rot(s))

def _has_reflection(counts: list[int]) -> bool:
    n = len(counts)
    # (1) 꼭짓점-축 반사: counts == reverse(rotate(counts, s))
    def eq_ref_vtx(s):
        for i in range(n):
            if counts[(s + i) % n] != counts[(s - i) % n]:
                return False
        return True
    # (2) 변-중점 축 반사: counts == reverse(rotate(counts, s)) with half-step
    # 구현상: reverse 후 한 칸 시프트 비교와 동일
    def eq_ref_edge(s):
        for i in range(n):
            if counts[(s + i) % n] != counts[(s - i - 1) % n]:
                return False
        return True
    for s in range(n):
        if eq_ref_vtx(s) or eq_ref_edge(s):
            return True
    return False

def _stabilizer_size(counts: list[int]) -> int:
    R = _rot_count(counts)           # 회전 안정자 크기
    has_ref = _has_reflection(counts)
    return R * (2 if has_ref else 1)

# ─────────────────────────────────────────────────────────────
def render():
    st.header("⚪ 다각형 변 위 원(칩) 배열 — 대칭을 고려한 경우의수")

    with st.sidebar:
        st.subheader("⚙️ 설정")
        n_sides = st.slider("다각형 변의 수 n", 3, 12, 8)
        is_regular = st.checkbox("정다각형(모든 변/각 동일)", True)

        # 변별 원(칩) 개수 입력
        edge_counts: list[int] = []
        if is_regular:
            k = st.slider("한 변의 원(칩) 개수 k", 1, 12, 3)
            edge_counts = [int(k)] * n_sides
        else:
            st.markdown("**비정다각형: 변마다 다른 개수 입력**")
            # 일괄 채우기 값
            seed_all = st.number_input("모두 동일로 채우기", 0, 12, 2, key="fill_all_default")
            cols = st.columns(4)
            for i in range(n_sides):
                key = f"edgecnt_{i}"
                if key not in st.session_state:
                    st.session_state[key] = int(seed_all)
                with cols[i % 4]:
                    val = st.number_input(f"변 {i+1}", 0, 12, int(st.session_state[key]), key=key)
                edge_counts.append(int(val))
            if st.button("⬇️ 모두 동일 값으로 채우기"):
                for i in range(n_sides):
                    st.session_state[f"edgecnt_{i}"] = int(seed_all)
                st.experimental_rerun()

        # 반사를 같은 것으로 볼지(=디헤드랄 부분군에 반사 포함시킬지)
        consider_reflection = st.checkbox("거울대칭(반사)도 같은 배열로 본다", False)

        # 무작위 라벨링 시드
        if "poly_arr_seed" not in st.session_state:
            st.session_state["poly_arr_seed"] = np.random.randint(0, 10**9)
        if st.button("🔀 원(칩) 번호 재배열(무작위)"):
            st.session_state["poly_arr_seed"] = np.random.randint(0, 10**9)

    # 총 원 수
    M = int(sum(edge_counts))
    disp_counts = ", ".join(map(str, edge_counts))

    # ── 안정자 크기 |H| 계산 (반사 포함/제외 선택 반영)
    # 회전 안정자 R은 항상 고려. 반사 포함을 끄면 반사 부분은 제거.
    R = _rot_count(edge_counts)
    has_ref_all = _has_reflection(edge_counts)
    H = R * (2 if (consider_reflection and has_ref_all) else 1)
    H = max(1, H)   # 안전 가드

    st.markdown(
        f"""
**세팅**  
- 변의 수: **n = {n_sides}**  
- 변별 원(칩) 개수: **[{disp_counts}]** → 총 원 수 **M = {M}**  
- 변 개수 배열의 **회전 안정자 크기**: **R = {R}**  
- **반사 안정자 존재**: {'예' if has_ref_all else '아니오'}  
- 실제 사용한 안정자 크기(선택 반영): **|H| = {H}**  
        """
    )

    # ── (A) 직순열 ÷ 중복  :  M! / |H|
    st.subheader("A) 직순열로 보고 **중복을 나눠주기**")
    st.latex(r"\text{서로 다른 배열 수} \;=\; \dfrac{M!}{\,|H|\,}")
    if M <= 20:
        import math as _m
        valA = _m.factorial(M) // H
        st.code(f"= {valA:,}")
    else:
        logA = _log10_factorial(M) - math.log10(H)
        st.code(_sci_from_log10(logA))

    # ── (B) 원순열 × 기준 : (M−1)! × (M/|H|)
    st.subheader("B) 원순열로 보고 **기준(앵커 수)**을 곱하기")
    st.latex(r"\text{서로 다른 배열 수} \;=\; (M-1)!\times\Big(\dfrac{M}{\,|H|\,}\Big)")
    if M <= 20:
        import math as _m
        valB = (_m.factorial(M-1) * (M // H)) if (M % H == 0) else (_m.factorial(M-1) * (M/H))
        st.code(f"= {valB:,}" if isinstance(valB, int) else f"= {valB:.6g}")
    else:
        logB = _log10_factorial(M-1) + math.log10(M) - math.log10(H)
        st.code(_sci_from_log10(logB))

    st.caption("두 값은 항상 같아야 합니다(Burnside 적용). 서로 다른 라벨(1..M)이라 비항등 대칭이 고정시키는 배치는 없기 때문입니다.")

    st.divider()

    # ── p5.js 시각화 (기존과 동일, counts를 그대로 사용)
    seed = int(st.session_state["poly_arr_seed"])
    counts_json = json.dumps(edge_counts)

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
    • 변 수 n = <b>{n_sides}</b>,
    변별 원 수 = <b>[{disp_counts}]</b>,
    총 원 수 M = <b>{M}</b>,
    |H| = <b>{H}</b>
  </div>
</div>

<script>
let nSides = {n_sides};
let counts = {counts_json};
let seed   = {seed};
let M      = {M};

let W=960, H=560;
let verts=[], circles=[], labels=[];

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
  // 비정다각형은 반지름을 약간씩 다르게(시각적 구분용)
  for(let i=0;i<nSides;i++){{
    let ang = -HALF_PI + TWO_PI*i/nSides;
    let r = R * (0.88 + 0.22*noise(i*0.251));
    verts.push({{x:r*Math.cos(ang), y:r*Math.sin(ang)}});
  }}
}}

function centroid(){{
  let cx=0, cy=0;
  for(const v of verts){{ cx+=v.x; cy+=v.y; }}
  return {{x:cx/verts.length, y:cy/verts.length}};
}}

function placeCircles(){{
  circles=[];
  let C = centroid();
  for(let i=0;i<nSides;i++){{
    const a=verts[i], b=verts[(i+1)%nSides];
    let mx=(a.x+b.x)/2, my=(a.y+b.y)/2;
    let ex=b.x-a.x, ey=b.y-a.y;
    let nx=-ey, ny=ex;
    let len=Math.hypot(nx,ny); nx/=len; ny/=len;
    // 바깥쪽으로
    let vx=mx-C.x, vy=my-C.y;
    if(nx*vx+ny*vy<0){{ nx=-nx; ny=-ny; }}

    let k = counts[i];
    for(let j=0;j<k;j++){{
      let t=(j+1)/(k+1);
      let px=a.x*(1-t)+b.x*t;
      let py=a.y*(1-t)+b.y*t;
      let off=24;
      px+=nx*off; py+=ny*off;
      circles.push({{x:px,y:py}});
    }}
  }}
}}

function drawPolygon(){{
  noFill(); stroke(0); strokeWeight(1.5);
  beginShape(); for(const v of verts) vertex(v.x, v.y); endShape(CLOSE);
  textAlign(CENTER,BOTTOM); noStroke(); fill(120); textSize(12);
  for(let i=0;i<nSides;i++) {{
    let a=verts[i], b=verts[(i+1)%nSides];
    let mx=(a.x+b.x)/2, my=(a.y+b.y)/2;
    text((i+1), mx, my-4);
  }}
}}

function drawEdgeCircles(){{
  textAlign(CENTER, CENTER); textSize(14);
  for(let i=0;i<circles.length;i++){{
    const c=circles[i];
    noStroke(); fill(245); circle(c.x,c.y,34);
    stroke(0); noFill(); circle(c.x,c.y,34);
    noStroke(); fill(20); text(i < labels.length ? labels[i] : '', c.x, c.y+1);
  }}
}}
</script>
</body>
</html>
    """
    components.html(html, height=620)

    st.info(
        "비정다각형이라도 변별 원 개수 배열이 **주기**를 가지거나 **대칭**이면 회전/반사 안정자 |H|가 1보다 커집니다. "
        "예: `[3,2,3,2]` 는 회전 2단(180°)이 유지되므로 R=2, 반사도 성립하면 |H|=4가 됩니다. "
        "이 대칭을 자동 감지해 M!/|H| 로 중복을 제거합니다."
    )
