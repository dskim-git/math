# activities/probability/binomial_galton_board.py
import time
from math import comb
from typing import Optional

import numpy as np
import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components

META = {
    "title": "갈톤보드(이항분포) 시뮬레이터",
    "description": "핀을 통과하며 좌/우로 움직이는 공을 모사합니다. 누적(빠름) + 실시간(부드러운 캔버스)",
    "order": 20,
}

# ─────────────────────────────────────────────────────────────────────────────
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
    # ▶ 여유(headroom) 15%
    ymax = float(max(float(np.max(counts)) if counts.size else 0.0,
                     float(np.max(theory)) if theory.size else 0.0))
    top = max(1.0, ymax * 1.15)
    fig.update_layout(
        xaxis_title="슬롯(오른쪽 횟수)",
        yaxis_title="도수",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig.update_xaxes(dtick=1)
    fig.update_yaxes(range=[0, top])
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# ⚠️ 확률 변수명이 p5 인스턴스 매개변수 p와 절대 충돌하지 않도록 'probRight' 사용
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
    #wrap { display:flex; gap:12px; align-items:flex-start; justify-content:center; padding:0 12px 12px; }
    #holder { flex: 0 0 auto; }
    #tableBox { flex: 0 0 240px; font: 13px/1.35 system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }
    #tableBox table { border-collapse: collapse; width: 240px; }
    #tableBox th, #tableBox td { border: 1px solid #ddd; padding: 4px 6px; }
    #tableBox th { background: #f5f7fb; }
    #tableBox td:nth-child(1), #tableBox th:nth-child(1) { text-align:center; width: 44px; }
    #tableBox td:nth-child(2), #tableBox th:nth-child(2) { text-align:right; width: 80px; }
    #tableBox td:nth-child(3), #tableBox th:nth-child(3) { text-align:right; width: 90px; }
    .legend { font: 12px/1.2 system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; color:#222; }
    .box { display:inline-block; width:12px; height:12px; vertical-align:middle; margin-right:6px; border-radius:2px; }
    .badge { background:#fff0d6; border:1px solid #ff9a2d; color:#b35900; padding:2px 8px; border-radius:10px; font-weight:700; }
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
      <button id="runonce">⏩ Run Once</button>
    </div>
    <div class="row small" id="info">-</div>
  </div>

  <div id="wrap">
    <div id="holder"></div>
    <div id="tableBox">
      <div class="caption">누적 표</div>
      <table id="countTable"></table>
    </div>
  </div>

<script>
(() => {
  // Panel sizes
  const W = 1000, H = 590;               // ← 아래 여백 조금 넉넉히
  const leftW = 600, rightW = W - leftW;

  // Params & state (⚠ 이름 충돌 방지: probRight)
  let nRows = 10, probRight = 0.5, totalBalls = 300, speed = 1.5;
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
  const elRunOnce = document.getElementById('runonce');
  const elTable = document.getElementById('countTable');

  function intVal(el, defv){ const v=parseInt(el.value,10); return Number.isFinite(v)?v:defv; }
  function floatVal(el, defv){ const v=parseFloat(el.value); return Number.isFinite(v)?v:defv; }
  function clamp(x,a,b){ return Math.min(b, Math.max(a,x)); }
  function clampFloat(x,a,b){ return Math.min(b, Math.max(a,x)); }

  function updateInfo(){
    elInfo.textContent = `진행: ${ballIdx} / ${totalBalls}  ·  남은 공: ${Math.max(0,totalBalls-ballIdx)}  ·  속도: ${speed.toFixed(1)}x`;
  }

  function renderTable(){
    if (!elTable) return;
    const sum = counts.reduce((a,b)=>a+b,0);
    let html = '<tr><th>k</th><th>count</th><th>p̂ = count/총</th></tr>';
    for (let k=0;k<=nRows;k++){
      const freq = sum>0 ? (counts[k]/sum) : 0;
      html += `<tr><td>${k}</td><td>${counts[k]}</td><td>${freq.toFixed(4)}</td></tr>`;
    }
    html += `<tr><th>합계</th><th>${sum}</th><th>${sum>0?'1.0000':'0.0000'}</th></tr>`;
    elTable.innerHTML = html;
  }

  function resetState() {
    nRows = clamp(intVal(elRows,10), 3, 15);
    probRight = clampFloat(floatVal(elProb,0.5), 0, 1);
    totalBalls = clamp(intVal(elBalls,300), 10, 5000);
    speed = clampFloat(floatVal(elSpeed,1.5), 0.2, 5);
    elSpeedVal.textContent = speed.toFixed(1) + "x";

    running = false;
    ballIdx = 0; row = 0; rights = 0; lastSlot = null;
    counts = Array(nRows + 1).fill(0);
    acc = 0;
    updateInfo();
    renderTable();
  }

  // 이론 이항분포(해당 시점까지의 떨어진 공 개수에 맞춰 스케일)
  function nCk(n,k){
    if (k<0||k>n) return 0;
    if (k===0||k===n) return 1;
    if (k>n-k) k=n-k;
    let r=1;
    for (let i=1;i<=k;i++){ r = (r * (n-k+i))/i; }
    return r;
  }
  function theoryCounts(total) {
    const res = Array(nRows+1).fill(0);
    if (total <= 0) return res;
    for (let k=0; k<=nRows; k++){
      const c = nCk(nRows,k) * Math.pow(probRight,k) * Math.pow(1-probRight, nRows-k);
      res[k] = c * total;
    }
    return res;
  }

  function binomSample(n, p){
    // n<=15 범위라 단순 합으로도 충분히 빠름
    let r=0;
    for (let i=0;i<n;i++) if (Math.random()<p) r++;
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

      // 왼쪽 판
      p.push();
      p.translate(40, 40);
      drawBoard(p);
      p.pop();

      // 오른쪽 히스토그램 + 이론선
      p.push();
      p.translate(leftW + 40, 30);
      drawHistogram(p);
      p.pop();

      // 상단 정보
      updateInfo();
    };

    function drawBoard(p){
      const panelW = leftW-80, panelH = H-120;
      const xMin = -nRows/2 - 0.8, xMax = nRows/2 + 0.8;
      const yMin = 0, yMax = nRows + 0.8;
      const sx = panelW/(xMax-xMin), sy = panelH/(yMax-yMin);

      // 외곽
      p.noFill();
      p.stroke(0,80);
      p.rect(0,0,panelW,panelH);

      // 핀
      p.noStroke();
      p.fill(200);
      for (let r=0;r<nRows;r++){
        for (let j=0;j<=r;j++){
          const x = j - r/2;
          const y = r+1;   // 위→아래
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

      // 우상단: 마지막 슬롯(배지로 강조)
      p.noStroke();
      p.fill(255,240,214);
      p.rect(panelW-160, 6, 150, 24, 8);
      p.fill(179,89,0);
      p.textSize(14);
      p.textAlign(p.CENTER, p.CENTER);
      p.text(`Last slot: ${lastSlot==null?'—':lastSlot}`, panelW-85, 18);
    }

    function drawHistogram(p){
      const panelW = rightW-80, panelH = H-120;
      const th = theoryCounts(ballIdx);
      const maxBar = Math.max(0, ...counts);
      const maxTh  = Math.max(0, ...th);
      const yMax   = Math.max(5, maxBar, maxTh) * 1.15;   // ▶ 머리공간

      const ticks = 5;                     // y축 눈금 갯수
      const barW = panelW/(nRows+1);

      // 틀
      p.noFill();
      p.stroke(0,80);
      p.rect(0,0,panelW,panelH);

      // y축 그리드/눈금/값
      p.stroke(230);
      p.textSize(12);
      p.textAlign(p.RIGHT, p.CENTER);
      for (let i=0;i<=ticks;i++){
        const frac = i/ticks;
        const y = panelH - frac*panelH;
        const val = Math.round(frac*yMax);
        p.stroke(235);
        p.line(0,y,panelW,y);
        p.noStroke();
        p.fill(0);
        p.text(`${val}`, -6, y);   // ← 왼쪽 바깥에 값
      }

      // 막대 (실험)
      for (let k=0;k<=nRows;k++){
        const h = (counts[k]/Math.max(1,yMax))*panelH;
        p.fill(60,120,255,180);
        p.noStroke();
        p.rect(k*barW+2, panelH-h, barW-4, h, 2);
      }

      // 이론선
      p.stroke(220,0,60);
      p.noFill();
      p.beginShape();
      for (let k=0;k<=nRows;k++){
        const h = (th[k]/Math.max(1,yMax))*panelH;
        p.vertex(k*barW+barW/2, panelH-h);
      }
      p.endShape();

      // last slot 바 강조(외곽선)
      if (lastSlot!=null){
        const hL = (counts[lastSlot]/Math.max(1,yMax))*panelH;
        p.noFill();
        p.stroke(255,140,0);
        p.strokeWeight(2);
        p.rect(lastSlot*barW+1, panelH-hL-1, barW-2, hL+2, 3);
        p.strokeWeight(1);
      }

      // x축 눈금/라벨(겹침 방지: 숫자 아래, 축제목 더 아래)
      p.fill(0);
      p.textSize(12);
      p.textAlign(p.CENTER, p.TOP);
      for (let k=0;k<=nRows;k++) p.text(k, k*barW+barW/2, panelH+6);
      p.textAlign(p.CENTER, p.TOP);
      p.text(`슬롯(오른쪽 횟수)`, panelW/2, panelH+26);  // ← 더 아래로 이동

      // y축 제목
      p.textAlign(p.LEFT, p.BOTTOM);
      p.text("도수", 4, 12);

      // 간단한 범례
      p.textAlign(p.LEFT, p.TOP);
      p.fill(0);
      p.textSize(12);
      p.noStroke();
      p.fill(60,120,255,200); p.rect(4, -20, 12, 12, 2);
      p.fill(0); p.text("실험(누적)", 20, -22);
      p.stroke(220,0,60); p.line(98, -14, 118, -14);
      p.noStroke(); p.fill(0); p.text("이론(이항)", 122, -22);
    }

    function stepOnce(){
      // 한 핀 통과
      if (row < nRows){
        if (Math.random() < probRight) rights += 1;
        row += 1;
      } else {
        // 슬롯 확정
        counts[rights] += 1;
        lastSlot = rights;
        renderTable();              // 표 갱신
        // 다음 공
        ballIdx += 1;
        row = 0; rights = 0;
        if (ballIdx >= totalBalls) running = false;
      }
    }
  });

  // UI 바인딩
  function onAnyChange(){
    speed = Math.min(5, Math.max(0.2, parseFloat(document.getElementById('speed').value)||1.5));
    document.getElementById('speedVal').textContent = speed.toFixed(1) + "x";
  }
  document.getElementById('speed').addEventListener('input', onAnyChange);

  document.getElementById('start').onclick = () => { running = true; };
  document.getElementById('pause').onclick = () => { running = false; };
  document.getElementById('reset').onclick = () => { resetState(); };
  document.getElementById('runonce').onclick = () => {
    // 한 번에 끝까지(애니메이션 없이) 실행
    const remain = Math.max(0, totalBalls - ballIdx);
    if (remain <= 0) return;
    for (let t=0; t<remain; t++){
      const r = binomSample(nRows, probRight);
      counts[r] += 1;
      lastSlot = r;
      ballIdx += 1;
    }
    running = false;
    renderTable();
    updateInfo();
  };

  // 처음 세팅
  resetState();
})();
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.header("🎯 갈톤보드(이항분포) 시뮬레이터")

    tab_fast, tab_live = st.tabs(["이항분포", "갈톤보드"])

    with tab_fast:
        c1, c2, c3 = st.columns([1.2, 1.2, 1.2])
        n_rows = c1.slider("핀(충돌) 횟수 n", 3, 20, 12, 1, key="gb_fast_n")
        n_balls = c2.slider("공의 개수", 50, 50_000, 5_000, step=50, key="gb_fast_b")
        p = c3.slider("오른쪽 확률 p", 0.0, 1.0, 0.5, 0.01, key="gb_fast_p")

        if "gb_counts" not in st.session_state or st.session_state.get("gb_n_rows") != n_rows:
            st.session_state["gb_counts"] = np.zeros(n_rows + 1, dtype=int)
            st.session_state["gb_total"] = 0
            st.session_state["gb_n_rows"] = n_rows

        colA, colB = st.columns(2)
        if colA.button("▶ 한 번에 실행"):
            counts = _binom_counts(n_rows, n_balls, p, None)
            st.session_state["gb_counts"] = counts
            st.session_state["gb_total"] = int(counts.sum())

        if colB.button("🧹 초기화"):
            st.session_state["gb_counts"] = np.zeros(n_rows + 1, dtype=int)
            st.session_state["gb_total"] = 0

        total_now = st.session_state["gb_total"]
        counts = st.session_state["gb_counts"]
        theory = _binom_theory(n_rows, p, total_now)
        fig = _plot_hist_with_theory(counts, theory)
        st.plotly_chart(fig, use_container_width=True)

    with tab_live:
        components.html(P5_HTML, height=720, scrolling=False)
