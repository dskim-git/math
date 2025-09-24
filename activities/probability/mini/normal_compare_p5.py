# activities/probability/mini/normal_compare_p5.py
import json
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "정규분포 비교 (미니, p5.js)",
    "description": "두 개의 정규분포(평균/표준편차)를 슬라이더로 조절하며 한 화면에서 비교",
    "order": 9999,
    "hidden": True,  # ← 사이드바/교과메인에 숨김 (수업에서만 링크해 쓰기 좋음)
}

def render():
    st.subheader("🎯 정규분포 비교 (p5.js)")

    with st.sidebar:
        st.markdown("### ⚙️ 설정")
        height_px = st.slider("캔버스 높이(px)", 300, 700, 420, step=10)
        fill_alpha = st.slider("면적 채우기 투명도(%)", 0, 60, 20, help="곡선 아래 영역을 반투명으로 채웁니다.")
        show_grid = st.checkbox("눈금/그리드 보이기", True)

    st.markdown("#### 분포 1 (파랑)")
    c1, c2 = st.columns(2)
    with c1:
        mu1 = st.slider("μ₁ (평균)", -5.0, 5.0, 0.0, step=0.1)
    with c2:
        sigma1 = st.slider("σ₁ (표준편차)", 0.2, 5.0, 1.0, step=0.1)

    st.markdown("#### 분포 2 (주황)")
    c3, c4 = st.columns(2)
    with c3:
        mu2 = st.slider("μ₂ (평균)", -5.0, 5.0, 0.0, step=0.1)
    with c4:
        sigma2 = st.slider("σ₂ (표준편차)", 0.2, 5.0, 2.0, step=0.1)

    params = {
        "mu1": mu1, "sigma1": sigma1,
        "mu2": mu2, "sigma2": sigma2,
        "fillAlpha": int(fill_alpha),
        "showGrid": bool(show_grid),
    }

    html = f"""
<div id="p5-holder" style="width:100%;"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
<script id="params" type="application/json">{json.dumps(params)}</script>
<script>
const P = JSON.parse(document.getElementById('params').textContent);

new p5((p) => {{
  let W, H, M;
  const margin = {{l:60, r:20, t:20, b:48}};
  const blue = p.color(36, 99, 235);   // Tailwind blue-600 느낌
  const orange = p.color(234, 88, 12); // orange-600

  function pdf(x, mu, sigma) {{
    const a = 1.0 / (sigma * Math.sqrt(2*Math.PI));
    const z = (x - mu) / sigma;
    return a * Math.exp(-0.5 * z * z);
  }}

  function niceTicks(min, max, count) {{
    const span = max - min;
    if (span <= 0) return [min];
    const step0 = span / Math.max(1, count);
    const pow10 = Math.pow(10, Math.floor(Math.log10(step0)));
    const steps = [1, 2, 2.5, 5, 10].map(k => k*pow10);
    let step = steps[0];
    for (let s of steps) {{ if (Math.abs(step0 - s) < Math.abs(step0 - step)) step = s; }}
    const niceMin = Math.floor(min/step)*step;
    const niceMax = Math.ceil(max/step)*step;
    const ticks = [];
    for (let v = niceMin; v <= niceMax + 1e-9; v += step) ticks.push(v);
    return ticks;
  }}

  function getDomain() {{
    const left  = Math.min(P.mu1 - 4*P.sigma1, P.mu2 - 4*P.sigma2);
    const right = Math.max(P.mu1 + 4*P.sigma1, P.mu2 + 4*P.sigma2);
    return [left, right];
  }}

  function getYMax() {{
    const m1 = 1.0/(P.sigma1*Math.sqrt(2*Math.PI));
    const m2 = 1.0/(P.sigma2*Math.sqrt(2*Math.PI));
    return Math.max(m1, m2) * 1.10; // 10% 여유
  }}

  function xToPx(x, x0, x1) {{
    return p.map(x, x0, x1, margin.l, W - margin.r);
  }}
  function yToPx(y, y0, y1) {{
    return p.map(y, y0, y1, H - margin.b, margin.t);
  }}

  p.setup = () => {{
    const holder = document.getElementById("p5-holder");
    W = holder.clientWidth || 800;
    H = {height_px};
    p.createCanvas(W, H).parent(holder);
    p.noLoop(); // 정적 렌더(슬라이더 바꾸면 Streamlit이 블록을 재생성)
    drawScene();
  }};

  p.windowResized = () => {{
    const holder = document.getElementById("p5-holder");
    W = holder.clientWidth || W;
    p.resizeCanvas(W, H);
    drawScene();
  }};

  function drawGrid(x0, x1, y0, y1) {{
    // X ticks
    const xt = niceTicks(x0, x1, 6);
    p.stroke(220);
    p.strokeWeight(1);
    xt.forEach(v => {{
      const xx = xToPx(v, x0, x1);
      p.line(xx, margin.t, xx, H - margin.b);
    }});

    // Y ticks
    const yt = niceTicks(0, y1, 5);
    yt.forEach(v => {{
      const yy = yToPx(v, 0, y1);
      p.line(margin.l, yy, W - margin.r, yy);
    }});

    // axes
    p.stroke(0);
    p.strokeWeight(1.5);
    p.line(margin.l, H - margin.b, W - margin.r, H - margin.b); // x-axis
    p.line(margin.l, margin.t, margin.l, H - margin.b);         // y-axis

    // tick labels
    p.fill(0); p.noStroke();
    p.textAlign(p.CENTER, p.TOP);
    xt.forEach(v => {{
      const xx = xToPx(v, x0, x1);
      p.text(niceNum(v), xx, H - margin.b + 6);
    }});
    p.textAlign(p.RIGHT, p.CENTER);
    yt.forEach(v => {{
      const yy = yToPx(v, 0, y1);
      p.text(niceNum(v), margin.l - 6, yy);
    }});

    // axis titles
    p.textAlign(p.CENTER, p.TOP);
    p.text("x", (margin.l + W - margin.r)/2, H - margin.b + 26);
    p.push();
    p.translate(18, (margin.t + H - margin.b)/2);
    p.rotate(-Math.PI/2);
    p.text("f(x)", 0, 0);
    p.pop();

    function niceNum(v){{
      const s = Math.abs(v) < 1e-3 || Math.abs(v) >= 1e3 ? v.toExponential(0) : v.toFixed(Math.abs(v) < 1 ? 2 : 1);
      return s.replace(/\\.0+$/,'').replace(/\\.$/,'');
    }}
  }}

  function drawCurve(mu, sigma, col, x0, x1, y1, fillAlpha) {{
    // 곡선 아래 면적 채우기
    if (fillAlpha > 0) {{
      p.noStroke();
      const c = p.color(col);
      c.setAlpha(p.map(fillAlpha,0,100,0,180));
      p.fill(c);
      p.beginShape();
      for (let px = margin.l; px <= W - margin.r; px++) {{
        const x = p.map(px, margin.l, W - margin.r, x0, x1);
        const y = pdf(x, mu, sigma);
        p.vertex(px, yToPx(y, 0, y1));
      }}
      p.vertex(W - margin.r, yToPx(0, 0, y1));
      p.vertex(margin.l, yToPx(0, 0, y1));
      p.endShape(p.CLOSE);
    }}

    // 라인
    p.noFill();
    p.stroke(col);
    p.strokeWeight(2);
    p.beginShape();
    for (let px = margin.l; px <= W - margin.r; px++) {{
      const x = p.map(px, margin.l, W - margin.r, x0, x1);
      const y = pdf(x, mu, sigma);
      p.vertex(px, yToPx(y, 0, y1));
    }}
    p.endShape();
  }}

  function drawLegend() {{
    const Lx = margin.l, Ly = margin.t - 2;
    p.noStroke(); p.fill(0);
    p.textAlign(p.LEFT, p.BOTTOM);
    p.textSize(12);
    p.fill(blue);   p.rect(Lx, Ly-10, 14, 3, 2); p.fill(0); p.text(`  μ₁={{{{P.mu1}}}}, σ₁={{{{P.sigma1}}}}`, Lx+20, Ly);
    p.fill(orange); p.rect(Lx+150, Ly-10, 14, 3, 2); p.fill(0); p.text(`  μ₂={{{{P.mu2}}}}, σ₂={{{{P.sigma2}}}}`, Lx+170, Ly);
  }}

  function drawScene() {{
    p.clear(); p.background(255);
    const [x0, x1] = getDomain();
    const y1 = getYMax();

    if (P.showGrid) drawGrid(x0, x1, 0, y1);

    drawCurve(P.mu1, P.sigma1, blue,   x0, x1, y1, P.fillAlpha);
    drawCurve(P.mu2, P.sigma2, orange, x0, x1, y1, P.fillAlpha);
    drawLegend();
  }}
}});
</script>
    """
    components.html(html, height=height_px + 12, scrolling=False)
