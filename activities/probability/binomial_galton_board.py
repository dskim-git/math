# activities/probability/binomial_galton_board.py
import time
from math import comb
from typing import Optional

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components

META = {
    "title": "갈톤보드(이항분포) 시뮬레이터",
    "description": "핀을 통과하며 좌/우로 움직이는 공을 모사합니다. 누적(빠름) + 실시간(부드러운 캔버스)",
    "order": 20,
}

# ─────────────────────────────────────────────────────────────────────────────
# 빠른 누적 시뮬에 쓰는 유틸
def _binom_counts(n_rows: int, n_balls: int, p: float, seed: Optional[int] = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    rights = rng.binomial(n_rows, p, size=n_balls)
    return np.bincount(rights, minlength=n_rows + 1)

def _binom_theory(n_rows: int, p: float, total: int) -> np.ndarray:
    if total <= 0:
        return np.zeros(n_rows + 1, dtype=float)
    k = np.arange(n_rows + 1)
    pmf = np.array([comb(n_rows, int(i)) * (p ** i) * ((1 - p) ** (n_rows - i)) for i in k], dtype=float)
    return pmf * total

def _plot_hist_with_theory(counts: np.ndarray, theory: np.ndarray) -> go.Figure:
    n_rows = len(counts) - 1
    x = np.arange(n_rows + 1)
    fig = go.Figure()
    fig.add_bar(x=x, y=counts, name="실험(누적)", opacity=0.85)
    fig.add_scatter(x=x, y=theory, mode="lines", name="이론(이항)", line=dict(width=2))
    fig.update_layout(
        xaxis_title="오른쪽으로 간 횟수 (슬롯)",
        yaxis_title="개수",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig.update_xaxes(dtick=1)
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# p5.js 실시간(부드러운) 모드 – Streamlit rerun 불필요(스크롤 튐 방지)
P5_HTML = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
  <style>
    body{ margin:0; padding:0; }
    .ui { font: 14px/1.4 system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; padding: 10px 12px; }
    .row { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }
    .row > * { margin: 2px 0; }
    label { font-weight: 600; }
    input[type=number], input[type=range] { vertical-align: middle; }
    button { padding: 6px 10px; }
    .small { font-size: 12px; color:#555; }
    #holder { display:flex; justify-content:center; }
  </style>
</head>
<body>
  <div class="ui">
    <div class="row">
      <label>핀 수(n):</label>
      <input id="rows" type="number" min="3" max="15" step="1" value="10"/>
      <label>p(오른쪽 확률):</label>
      <input id="prob" type="number" min="0" max="1" step="0.01" value="0.5"/>
      <label>총 공 개수:</label>
      <input id="balls" type="number" min="10" max="5000" step="10" value="300"/>
      <label>속도:</label>
      <input id="speed" type="range" min="0.2" max="5" step="0.1" value="1.5"/>
      <span id="speedVal" class="small">1.5x</span>
      <button id="start">▶ Start</button>
      <button id="pause">⏸ Pause</button>
      <button id="reset">🧹 Reset</button>
    </div>
    <div class="row small" id="info">-</div>
  </div>
  <div id="holder"></div>

<script>
(() => {
  // Panel sizes
  const W = 1000, H = 560;
  const leftW = 600, rightW = W - leftW;

  // Params & state
  let nRows = 10, p = 0.5, totalBalls = 300, speed = 1.5;
  let running = false;

  let ballIdx = 0;   // 0..totalBalls
  let row = 0;
  let rights = 0;
  let counts = [];
  let lastSlot = null; // 마지막으로 들어간 슬롯 번호

  // Timing (속도 체감 확실)
  let stepInterval = 0.12; // seconds per pin at speed 1.0
  let acc = 0;

  // UI refs
  const elRows  = document.getElementById('rows');
  const elProb  = document.getElementById('prob');
  const elBalls = document.getElementById('balls');
  const elSpeed = document.getElementById('speed');
  const elSpeedVal = document.getElementById('speedVal');
  const elInfo  = document.getElementById('info');
  const elStart = document.getElementById('start');
  const elPause = document.getElementById('pause');
  const elReset = document.getElementById('reset');

  function resetState() {
    nRows = clamp(intVal(elRows,10), 3, 15);
    p     = clampFloat(floatVal(elProb,0.5), 0, 1);
    totalBalls = clamp(intVal(elBalls,300), 10, 5000);
    speed = clampFloat(floatVal(elSpeed,1.5), 0.2, 5);
    elSpeedVal.textContent = speed.toFixed(1) + "x";

    running = false;
    ballIdx = 0; row = 0; rights = 0; lastSlot = null;
    counts = Array(nRows + 1).fill(0);
    acc = 0;
    updateInfo();
  }

  function intVal(el, defv){ const v=parseInt(el.value,10); return Number.isFinite(v)?v:defv; }
  function floatVal(el, defv){ const v=parseFloat(el.value); return Number.isFinite(v)?v:defv; }
  function clamp(x,a,b){ return Math.min(b, Math.max(a,x)); }
  function clampFloat(x,a,b){ return Math.min(b, Math.max(a,x)); }

  // 이론 이항분포(해당 시점까지의 떨어진 공 개수에 맞춰 스케일)
  function theoryCounts(total) {
    const res = Array(nRows+1).fill(0);
    if (total <= 0) return res;
    for (let k=0; k<=nRows; k++){
      const c = nCk(nRows,k) * Math.pow(p,k) * Math.pow(1-p, nRows-k);
      res[k] = c * total;
    }
    return res;
  }
  function nCk(n,k){
    if (k<0||k>n) return 0;
    if (k===0||k===n) return 1;
    // fast
    if (k>n-k) k=n-k;
    let r=1;
    for (let i=1;i<=k;i++){ r = (r * (n-k+i))/i; }
    return r;
  }

  // p5
  new p5(p => {
    p.setup = () => {
      const cnv = p.createCanvas(W, H);
      cnv.parent('holder');
      p.frameRate(60);
      resetState();
    };

    p.draw = () => {
      // 진행
      if (running && ballIdx < totalBalls){
        const dt = p.deltaTime/1000;                 // seconds
        const interval = stepInterval / speed;       // quick = small interval
        acc += dt;
        while (acc >= interval) {
          stepOnce();
          acc -= interval;
          if (!running) break;
        }
      }

      // 배경
      p.background(255);

      // 왼쪽 판: 좌표계
      p.push();
      p.translate(40, 40);
      drawBoard(p);
      p.pop();

      // 오른쪽 히스토그램
      p.push();
      p.translate(leftW + 30, 30);
      drawHistogram(p);
      p.pop();

      updateInfo();
    };

    function drawBoard(p){
      const panelW = leftW-60, panelH = H-100;
      // 스케일: x축 [-n/2, n/2], y축 [0..n]
      const xMin = -nRows/2 - 0.8, xMax = nRows/2 + 0.8;
      const yMin = 0, yMax = nRows + 0.8;
      const sx = panelW/(xMax-xMin), sy = panelH/(yMax-yMin);

      // 틀
      p.noFill();
      p.stroke(0,80);
      p.rect(0,0,panelW,panelH);

      // 핀
      p.noStroke();
      p.fill(200);
      for (let r=0;r<nRows;r++){
        for (let j=0;j<=r;j++){
          const x = j - r/2;
          const y = r+1;  // 위→아래
          p.circle((x-xMin)*sx, (y-yMin)*sy, 6);
        }
      }

      // 공
      if (ballIdx < totalBalls){
        const bx = rights - row/2;
        const by = row;
        p.fill(220,0,60);
        p.noStroke();
        p.circle((bx-xMin)*sx, ((by+0.4)-yMin)*sy, 10);
      }

      // 상단 텍스트(진입 슬롯)
      p.fill(0);
      p.textSize(14);
      let slotText = lastSlot==null ? '—' : lastSlot.toString();
      p.text(`Last slot: ${slotText}`, panelW-120, 16);
    }

    function drawHistogram(p){
      const panelW = rightW-60, panelH = H-100;
      const maxY = Math.max(5, Math.max(...counts));
      const barW = panelW/(nRows+1);

      // 틀
      p.noFill();
      p.stroke(0,80);
      p.rect(0,0,panelW,panelH);

      // 막대
      for (let k=0;k<=nRows;k++){
        const h = (counts[k]/Math.max(1,maxY))*panelH;
        p.fill(60,120,255,180);
        p.noStroke();
        p.rect(k*barW+2, panelH-h, barW-4, h);
      }

      // 이론선
      const th = theoryCounts(ballIdx);
      p.stroke(220,0,60);
      p.noFill();
      p.beginShape();
      for (let k=0;k<=nRows;k++){
        const h = (th[k]/Math.max(1,maxY))*panelH;
        p.vertex(k*barW+barW/2, panelH-h);
      }
      p.endShape();

      // 축 눈금
      p.fill(0);
      p.textSize(12);
      p.textAlign(p.CENTER, p.TOP);
      for (let k=0;k<=nRows;k++){
        p.text(k, k*barW+barW/2, panelH+4);
      }
      p.textAlign(p.LEFT, p.BOTTOM);
      p.text("개수", 4, 12);
      p.textAlign(p.CENTER, p.BOTTOM);
      p.text(`슬롯(오른쪽 횟수)`, panelW/2, panelH+22);
    }

    function stepOnce(){
      // 한 핀 통과
      if (row < nRows){
        if (Math.random() < p) rights += 1;
        row += 1;
      } else {
        // 슬롯 확정
        counts[rights] += 1;
        lastSlot = rights;
        // 다음 공 준비
        ballIdx += 1;
        row = 0; rights = 0;
        if (ballIdx >= totalBalls) {
          running = false;
        }
      }
    }
  });

  // UI 바인딩
  function updateInfo(){
    elInfo.textContent = `진행: ${ballIdx} / ${totalBalls}  ·  남은 공: ${Math.max(0,totalBalls-ballIdx)}  ·  속도: ${speed.toFixed(1)}x`;
  }
  function onChange(){
    // 파라미터만 갱신(Reset은 하지 않음)
    speed = clampFloat(floatVal(elSpeed,1.5), 0.2, 5);
    elSpeedVal.textContent = speed.toFixed(1) + "x";
    updateInfo();
  }
  elSpeed.addEventListener('input', onChange);

  elStart.onclick = () => { running = true; };
  elPause.onclick = () => { running = false; };
  elReset.onclick = () => { resetState(); };

  // 초기화
  resetState();
})();
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.header("🎯 갈톤보드(이항분포) 시뮬레이터")

    tab_fast, tab_live = st.tabs(["누적(빠름)", "실시간(부드러운 캔버스, 권장)"])

    # ── 1) 누적(빠름): Plotly (정확한 누적 + 이론선)
    with tab_fast:
        c1, c2, c3, c4 = st.columns([1.2, 1.2, 1.2, 1])
        with c1:
            n_rows = st.slider("핀(충돌) 횟수 n", 3, 20, 12, 1, key="gb_fast_n")
        with c2:
            n_balls = st.slider("공의 개수", 50, 50_000, 5_000, step=50, key="gb_fast_b")
        with c3:
            p = st.slider("오른쪽 확률 p", 0.0, 1.0, 0.5, 0.01, key="gb_fast_p")
        with c4:
            seed_text = st.text_input("시드(선택)", value="", key="gb_fast_seed")
            seed = int(seed_text) if seed_text.strip().isdigit() else None

        if "gb_counts" not in st.session_state:
            st.session_state["gb_counts"] = np.zeros(n_rows + 1, dtype=int)
            st.session_state["gb_total"] = 0
            st.session_state["gb_n_rows"] = n_rows

        def _reset_fast():
            st.session_state["gb_counts"] = np.zeros(n_rows + 1, dtype=int)
            st.session_state["gb_total"] = 0
            st.session_state["gb_n_rows"] = n_rows

        if st.session_state.get("gb_n_rows") != n_rows:
            _reset_fast()

        run_col, step_col, clear_col = st.columns([1, 1, 1])
        placeholder = st.empty()

        with run_col:
            if st.button("▶ 한 번에 실행", key="gb_fast_run"):
                counts = _binom_counts(n_rows, n_balls, p, seed)
                st.session_state["gb_counts"] = counts
                st.session_state["gb_total"] = int(counts.sum())

        with step_col:
            if st.button("⏩ 점점 늘리기(애니)", key="gb_fast_anim"):
                _reset_fast()
                batch = max(50, n_balls // 50)
                done = 0
                while done < n_balls:
                    this = min(batch, n_balls - done)
                    counts = _binom_counts(n_rows, this, p, None if seed is None else seed + done)
                    st.session_state["gb_counts"] += counts
                    st.session_state["gb_total"] += int(counts.sum())
                    theory = _binom_theory(n_rows, p, st.session_state["gb_total"])
                    fig = _plot_hist_with_theory(st.session_state["gb_counts"], theory)
                    placeholder.plotly_chart(fig, use_container_width=True)
                    done += this
                    time.sleep(0.03)

        with clear_col:
            if st.button("🧹 초기화", key="gb_fast_clear"):
                _reset_fast()

        total_now = st.session_state["gb_total"]
        counts = st.session_state["gb_counts"] if total_now > 0 else np.zeros(n_rows + 1, dtype=int)
        theory = _binom_theory(n_rows, p, total_now)
        fig = _plot_hist_with_theory(counts, theory)
        placeholder.plotly_chart(fig, use_container_width=True)

        k = np.arange(n_rows + 1)
        mean_emp = (k * counts).sum() / max(1, total_now)
        var_emp = (((k - mean_emp) ** 2) * counts).sum() / max(1, total_now)
        st.caption(
            f"실험 개수: **{total_now:,}** · 경험적 평균 **{mean_emp:.3f}** / 분산 **{var_emp:.3f}**  "
            f"· 이론 평균 **{n_rows * p:.3f}** / 이론 분산 **{n_rows * p * (1 - p):.3f}**"
        )

    # ── 2) 실시간(부드러운 캔버스): p5.js + 단일 iframe(스크롤 튐 없음)
    with tab_live:
        components.html(P5_HTML, height=640, scrolling=False)
