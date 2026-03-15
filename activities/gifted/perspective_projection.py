import base64
import os

import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 실제 사물과 그림 속 사물의 관계식 탐구",
    "description": "눈(E)의 높이 22cm, 화면까지 거리 28cm 조건에서 실제 좌표 A(a,b)와 화면 좌표 A'(a',b') 사이의 관계식을 단계별로 탐구합니다.",
    "order": 34,
    "hidden": True,
}

_HTML = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  background: #0f172a; color: #e2e8f0;
  font-family: 'Segoe UI', 'Noto Sans KR', sans-serif;
  user-select: none; -webkit-user-select: none;
}
#app { max-width: 900px; margin: 0 auto; padding: 12px; }

/* Tabs */
.tabs { display: flex; gap: 6px; margin-bottom: 14px; flex-wrap: wrap; }
.tab-btn {
  padding: 8px 18px; border-radius: 999px; border: 1.5px solid #334155;
  background: #1e293b; color: #94a3b8; cursor: pointer;
  font-size: 0.82rem; font-weight: 700; transition: all .15s;
}
.tab-btn.active { background: #0369a1; color: #e0f2fe; border-color: #38bdf8; }
.tab-btn:hover:not(.active) { border-color: #475569; color: #cbd5e1; }

/* panels */
.panel { display: none; }
.panel.show { display: block; }

/* Canvas container */
.cvs-wrap {
  background: #111827; border: 1px solid #1e3a5f;
  border-radius: 12px; overflow: hidden; position: relative;
  margin-bottom: 10px;
}
canvas { display: block; width: 100%; }

/* Controls */
.ctrl-card {
  background: #1e293b; border: 1px solid #334155;
  border-radius: 10px; padding: 12px 14px; margin-bottom: 10px;
}
.ctrl-title { font-size: 0.78rem; font-weight: 800; color: #7dd3fc; margin-bottom: 10px; }
.slider-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.sl-lbl { font-size: 0.76rem; color: #64748b; min-width: 80px; }
.sl-val { font-size: 0.82rem; color: #f0abfc; min-width: 36px; text-align: right; font-weight: 700; }
input[type=range] { flex: 1; cursor: pointer; height: 6px; accent-color: #38bdf8; }

/* Coord display */
.coord-display {
  display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 10px;
}
.coord-box {
  flex: 1; min-width: 120px;
  background: #0f172a; border: 1.5px solid #1e3a5f;
  border-radius: 10px; padding: 10px 14px; text-align: center;
}
.coord-label { font-size: 0.7rem; color: #64748b; margin-bottom: 4px; font-weight: 700; letter-spacing: .06em; }
.coord-val { font-size: 1.15rem; font-weight: 800; }
.real-val  { color: #4ade80; }
.proj-val  { color: #f59e0b; }

/* Step cards */
.step-card {
  background: #0f172a; border: 1px solid #1e3a5f;
  border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;
}
.step-num {
  display: inline-block; background: #0369a1; color: #e0f2fe;
  border-radius: 6px; padding: 2px 10px; font-size: 0.72rem;
  font-weight: 800; margin-bottom: 8px;
}
.step-body { font-size: 0.82rem; color: #94a3b8; line-height: 1.85; }
.step-body b { color: #e2e8f0; }
.formula {
  background: #1e293b; border: 1px solid #334155;
  border-radius: 8px; padding: 8px 14px; margin: 8px 0;
  font-family: 'Courier New', monospace; font-size: 0.92rem;
  color: #7dd3fc; text-align: center;
}
.hl-g { color: #4ade80; font-weight: 700; }
.hl-y { color: #f59e0b; font-weight: 700; }
.hl-p { color: #f0abfc; font-weight: 700; }
.hl-r { color: #f87171; font-weight: 700; }

/* Quiz */
.quiz-card {
  background: #0f172a; border: 1.5px solid #334155;
  border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;
}
.quiz-q { font-size: 0.85rem; color: #e2e8f0; margin-bottom: 10px; line-height: 1.7; }
.quiz-input-row { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 8px; }
.quiz-input-row input[type=number] {
  background: #1e293b; border: 1.5px solid #475569;
  border-radius: 8px; padding: 7px 12px; color: #e2e8f0;
  font-size: 0.88rem; width: 90px; outline: none;
  transition: border-color .15s;
}
.quiz-input-row input[type=number]:focus { border-color: #38bdf8; }
.quiz-btn {
  padding: 8px 16px; border-radius: 8px; border: 1.5px solid #334155;
  background: #1e3a5f; color: #7dd3fc; cursor: pointer;
  font-size: 0.8rem; font-weight: 700; transition: all .15s;
}
.quiz-btn:hover { background: #0369a1; border-color: #38bdf8; color: #e0f2fe; }
.quiz-feedback {
  font-size: 0.8rem; border-radius: 8px; padding: 8px 12px;
  margin-top: 6px; display: none;
}
.quiz-feedback.correct { background: #14532d; color: #86efac; border: 1px solid #16a34a; display: block; }
.quiz-feedback.wrong   { background: #450a0a; color: #fca5a5; border: 1px solid #b91c1c; display: block; }

/* Inverse section */
.inv-note {
  background: #1a1a2e; border: 1.5px solid #7e22ce;
  border-radius: 10px; padding: 12px 16px; margin-bottom: 10px;
  font-size: 0.82rem; color: #c4b5fd; line-height: 1.8;
}
.inv-note .inv-title { font-size: 0.88rem; font-weight: 800; color: #a78bfa; margin-bottom: 6px; }

/* Live inverse calculator */
.calc-card {
  background: #1e293b; border: 1px solid #334155;
  border-radius: 10px; padding: 12px 14px; margin-bottom: 10px;
}
.calc-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 8px; }
.calc-col { flex: 1; min-width: 140px; }
.calc-label { font-size: 0.72rem; color: #64748b; margin-bottom: 4px; }
.calc-inp {
  background: #0f172a; border: 1.5px solid #334155;
  border-radius: 8px; padding: 8px 12px; color: #e2e8f0;
  font-size: 0.9rem; width: 100%; outline: none;
  transition: border-color .15s;
}
.calc-inp:focus { border-color: #38bdf8; }
.calc-result {
  background: #0f172a; border: 1px solid #1e3a5f;
  border-radius: 10px; padding: 12px 14px;
  font-size: 0.88rem; color: #94a3b8; line-height: 1.9;
}
.calc-result b { color: #4ade80; font-size: 1rem; }

/* Diagram canvas */
.diag-wrap {
  background: #060f1e; border: 1px solid #1e3a5f;
  border-radius: 10px; overflow: hidden; margin-bottom: 12px;
}
.diag-wrap canvas { display: block; width: 100%; }

/* Legend row */
.legend-row {
  display: flex; gap: 14px; flex-wrap: wrap;
  font-size: 0.76rem; color: #94a3b8; margin: 8px 0 4px;
}
.leg { display: flex; align-items: center; gap: 5px; }
.leg-dot {
  width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0;
}

@media (max-width: 480px) {
  .coord-display { gap: 8px; }
  .coord-box { min-width: 100px; padding: 8px; }
  .coord-val { font-size: 1rem; }
}

/* ── Arnolfini tab ── */
.arno-toolbar {
  background: #1e293b; border: 1px solid #334155; border-radius: 10px;
  padding: 7px 10px; margin-bottom: 8px;
  display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
}
.atl-btn {
  padding: 5px 12px; border-radius: 7px; border: 1.5px solid #334155;
  background: #0f172a; color: #94a3b8; cursor: pointer;
  font-size: 0.78rem; font-weight: 700; transition: all .15s; white-space: nowrap;
}
.atl-btn.active  { background: #1e3a5f; color: #bfdbfe; border-color: #3b82f6; }
.atl-btn.mark-on { background: #4c1d95; color: #ede9fe; border-color: #8b5cf6; }
.atl-btn:hover:not(.active):not(.mark-on) { border-color: #475569; color: #cbd5e1; }
.arno-vsep { width:1px; height:24px; background:#334155; flex-shrink:0; }
.acswatch {
  width:20px; height:20px; border-radius:4px; cursor:pointer;
  border:2px solid transparent; transition:all .1s; flex-shrink:0;
}
.acswatch.active { border-color:#f8fafc; transform:scale(1.2); }
.acswatch:hover  { transform:scale(1.1); }

.arno-cvs-outer {
  background: #0a0f1a; border: 1px solid #334155; border-radius: 10px;
  overflow: hidden; line-height: 0; position: relative; margin-bottom: 8px;
}
#cvsArno { display: block; cursor: crosshair; touch-action: none; width: 100%; }

.arno-tip {
  padding: 7px 12px; border-radius: 6px;
  font-size: 0.74rem; margin-bottom: 8px; display: none;
}
.arno-tip.tip-ruler { background:#1e3a5f; border-left:3px solid #3b82f6; color:#93c5fd; }
.arno-tip.tip-mark  { background:#2d1b69; border-left:3px solid #8b5cf6; color:#c4b5fd; }

.coord-badge { display:flex; gap:10px; flex-wrap:wrap; margin-bottom:10px; }
.coord-badge-box {
  flex:1; min-width:130px; background:#0f172a; border:1.5px solid #334155;
  border-radius:8px; padding:8px 12px; text-align:center;
}
.cb-label { font-size:0.68rem; color:#64748b; margin-bottom:3px; font-weight:700; }
.cb-val   { font-size:1.05rem; font-weight:800; }

/* Step progress bar */
.arno-step-bar {
  display:flex; align-items:center; margin: 14px 0 4px;
}
.asb-dot {
  width:30px; height:30px; border-radius:50%; border:2px solid #334155;
  background:#1e293b; color:#475569; font-weight:800; font-size:0.82rem;
  display:flex; align-items:center; justify-content:center; flex-shrink:0;
  transition:all .3s;
}
.asb-dot.active { background:#0369a1; border-color:#38bdf8; color:#e0f2fe; }
.asb-dot.done   { background:#059669; border-color:#34d399; color:#fff; }
.asb-line { flex:1; height:2px; background:#334155; transition:background .3s; }
.asb-line.done  { background:#059669; }
.asb-label-row  {
  display:flex; justify-content:space-between; margin-bottom:16px;
  font-size:0.68rem; color:#475569; padding:0 2px;
}

/* Sections revealed progressively */
.arno-section { display:none; }
.arno-section.show { display:block; }

/* Formula box */
.arno-formula {
  background:#0f2340; border:1px solid #1e3a5f; border-radius:10px;
  padding:14px 18px; margin-bottom:14px; line-height:2;
}
.arno-formula .fml-title { font-size:0.72rem; font-weight:800; color:#64748b; margin-bottom:6px; letter-spacing:.05em; text-transform:uppercase; }
.arno-formula .fml { color:#bae6fd; font-family:monospace; font-size:0.95rem; }
.arno-formula .fml .fhl { color:#fcd34d; font-weight:800; }
.arno-formula .fml-note { font-size:0.75rem; color:#475569; margin-top:4px; }

/* Calculator */
.arno-calc-box {
  background: #022c22; border: 1px solid #14b8a6;
  border-radius: 10px; padding: 14px; margin-bottom: 14px;
}
.arno-calc-title { font-size:0.85rem; font-weight:800; color:#34d399; margin-bottom:10px; }
.arno-calc-row   { display:flex; align-items:center; gap:8px; margin-bottom:7px; flex-wrap:wrap; }
.arno-calc-lbl   { font-size:0.78rem; color:#6ee7b7; min-width:220px; }
.arno-calc-inp {
  width:90px; padding:5px 8px; border-radius:6px;
  background:#064e3b; border:1px solid #14b8a6; color:#ecfdf5;
  font-size:0.82rem; text-align:right; outline:none;
}
.arno-calc-inp:focus { border-color:#34d399; }
.arno-calc-btn {
  margin-top:6px; padding:7px 18px; border-radius:7px;
  border:1.5px solid #14b8a6; background:#065f46; color:#6ee7b7;
  cursor:pointer; font-size:0.82rem; font-weight:700; transition:all .15s;
}
.arno-calc-btn:hover { background:#047857; }
.arno-result {
  display:none; margin-top:10px; padding:14px;
  background:#065f46; border-radius:8px; line-height:2.1;
  font-size:0.82rem; color:#a7f3d0;
}
.arno-result strong { color:#6ee7b7; font-size:1rem; }
.arno-result .big-ans { color:#fcd34d; font-size:1.05rem; font-weight:800; }

/* Next-step button */
.arno-next-btn {
  display:block; width:100%; margin-top:14px; padding:11px 14px;
  border-radius:9px; border:1.5px solid #334155;
  background:#1e293b; color:#475569;
  cursor:not-allowed; font-size:0.85rem; font-weight:800;
  transition:all .2s; text-align:center;
}
.arno-next-btn.ready {
  border-color:#38bdf8; background:#0369a1; color:#e0f2fe; cursor:pointer;
}
.arno-next-btn.ready:hover { background:#0284c7; }

/* 3D wrap */
.arno-3d-wrap {
  background: #060f1e; border: 1px solid #1e3a5f;
  border-radius: 10px; overflow: hidden; margin-bottom: 10px;
  position: relative;
}
#cvsArno3D { display:block; width:100%; touch-action:none; cursor:grab; }
#cvsArno3D.dragging { cursor:grabbing; }
.arno-3d-hint {
  position:absolute; bottom:8px; right:10px;
  font-size:0.66rem; color:#334155; pointer-events:none;
}
</style>
</head>
<body>
<div id="app">

<div class="tabs">
  <button class="tab-btn active" id="tabSim">🎯 시뮬레이션</button>
  <button class="tab-btn" id="tabEx4">📐 탐구활동 4</button>
  <button class="tab-btn" id="tabEx5">🔄 탐구활동 5</button>
  <button class="tab-btn" id="tabArno">🖼 아르놀피니 적용</button>
</div>

<!-- ═══════════════════════════════════════════════════
     TAB 1: 시뮬레이션
═══════════════════════════════════════════════════ -->
<div id="panel-sim" class="panel show">

  <div class="cvs-wrap">
    <canvas id="cvsSide" height="220"></canvas>
  </div>
  <div class="cvs-wrap">
    <canvas id="cvsTop" height="200"></canvas>
  </div>

  <div class="ctrl-card">
    <div class="ctrl-title">🕹 실제 점 A의 위치 조절</div>
    <div class="slider-row">
      <span class="sl-lbl">a (좌우)</span>
      <input type="range" id="slA" min="-60" max="60" value="30" step="1">
      <span class="sl-val" id="valA">30</span>
    </div>
    <div class="slider-row">
      <span class="sl-lbl">b (깊이)</span>
      <input type="range" id="slB" min="1" max="100" value="28" step="1">
      <span class="sl-val" id="valB">28</span>
    </div>
  </div>

  <div class="coord-display">
    <div class="coord-box">
      <div class="coord-label">실제 점 A</div>
      <div class="coord-val real-val">(<span id="dA">30</span>, <span id="dB">28</span>)</div>
    </div>
    <div class="coord-box">
      <div class="coord-label">화면 속 점 A′</div>
      <div class="coord-val proj-val">(<span id="dAp">—</span>, <span id="dBp">—</span>)</div>
    </div>
  </div>

  <div class="step-card" style="margin-bottom:0">
    <div class="step-body" style="font-size:0.78rem;color:#64748b">
      ↑ <b style="color:#4ade80">초록 점</b>은 실제 사물 A(a,b),&nbsp;
      <b style="color:#f59e0b">노란 점</b>은 화면 속 A′(a′,b′)입니다.<br>
      슬라이더로 A를 움직여 투영 위치가 어떻게 바뀌는지 확인하세요.
    </div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════
     TAB 2: 탐구활동 4 — 관계식 유도
═══════════════════════════════════════════════════ -->
<div id="panel-ex4" class="panel">

  <div class="step-card">
    <span class="step-num">상황 설명</span>
    <div class="diag-wrap"><canvas id="cvsDiagSetup" height="170"></canvas></div>
    <div class="legend-row">
      <span class="leg"><span class="leg-dot" style="background:#f43f5e"></span>눈 E</span>
      <span class="leg"><span class="leg-dot" style="background:#4ade80"></span>실제 점 A(a,b)</span>
      <span class="leg"><span class="leg-dot" style="background:#f59e0b"></span>화면 속 A′(a′,b′)</span>
      <span class="leg"><span class="leg-dot" style="background:#a78bfa;border-radius:2px"></span>화면(그림)</span>
    </div>
    <div class="step-body">
      눈(E)은 수평면으로부터 <b class="hl-r">높이 22cm</b> 위에 있고,
      화면(그림)으로부터 <b class="hl-r">28cm</b> 떨어진 위치에서 바라봅니다.<br>
      수평면 위의 점 <b class="hl-g">A(a, b)</b> 는 화면에 <b class="hl-y">A′(a′, b′)</b> 로 투영됩니다.
    </div>
  </div>

  <div class="step-card">
    <span class="step-num">STEP 1 — 옆에서 본 단면 (b′ 구하기)</span>
    <div class="diag-wrap"><canvas id="cvsDiag4b" height="210"></canvas></div>
    <div class="step-body">
      위 그림처럼 <b>옆에서 본 단면</b>에서 꼭짓점 A를 공유하는
      <b class="hl-y">닮음인 직각삼각형</b> 두 개를 찾을 수 있습니다.<br><br>
      <span style="color:#4ade80">■</span> <b>큰 삼각형</b> : 밑변 = b + 28,&nbsp; 높이 = 22 &nbsp;(직각: E발밑)<br>
      <span style="color:#f59e0b">■</span> <b>작은 삼각형</b> : 밑변 = b,&nbsp; 높이 = b′ &nbsp;(직각: 화면·바닥 교점)
      <div class="formula">b′ / 22 = b / (b + 28)</div>
      따라서:
      <div class="formula" style="color:#f59e0b; font-size:1.05rem">b′ = 22b / (b + 28)</div>
    </div>
  </div>

  <div class="step-card">
    <span class="step-num">STEP 2 — 위에서 본 평면 (a′ 구하기)</span>
    <div class="diag-wrap"><canvas id="cvsDiag4a" height="195"></canvas></div>
    <div class="step-body">
      위 그림처럼 <b>위에서 본 평면</b>에서 꼭짓점 E를 공유하는
      <b class="hl-y">닮음인 직각삼각형</b> 두 개를 찾을 수 있습니다.<br><br>
      <span style="color:#4ade80">■</span> <b>큰 삼각형</b> : 밑변 = b + 28,&nbsp; 높이 = a &nbsp;(직각: A발밑)<br>
      <span style="color:#f59e0b">■</span> <b>작은 삼각형</b> : 밑변 = 28,&nbsp; 높이 = a′ &nbsp;(직각: 화면·중심축 교점)
      <div class="formula">a′ / a = 28 / (b + 28)</div>
      따라서:
      <div class="formula" style="color:#f59e0b; font-size:1.05rem">a′ = 28a / (b + 28)</div>
    </div>
  </div>

  <div class="step-card">
    <span class="step-num">STEP 3 — 관계식 정리</span>
    <div class="step-body">
      실제 점 <b class="hl-g">A(a, b)</b> → 화면 속 점 <b class="hl-y">A′(a′, b′)</b> :
      <div class="formula" style="font-size:1rem; color:#7dd3fc; line-height:2">
        a′ = 28a / (b + 28)<br>
        b′ = 22b / (b + 28)
      </div>
    </div>
  </div>

  <!-- Quiz -->
  <div class="quiz-card">
    <div class="ctrl-title">🧩 확인 문제 — A(a,b)를 직접 넣어봐요</div>
    <div class="quiz-q">
      눈의 높이 = 22, 화면까지 거리 = 28 일 때,<br>
      실제 점 A(<b class="hl-g" id="qa">?</b>, <b class="hl-g" id="qb">?</b>)의 화면 좌표 A′(a′, b′)를 구하세요.
    </div>
    <div class="quiz-input-row">
      <span style="font-size:.82rem;color:#94a3b8">a′ =</span>
      <input type="number" id="ans-ap" placeholder="소수점 2자리" step="0.01">
      <span style="font-size:.82rem;color:#94a3b8">b′ =</span>
      <input type="number" id="ans-bp" placeholder="소수점 2자리" step="0.01">
      <button class="quiz-btn" id="checkBtn4">확인</button>
      <button class="quiz-btn" id="newQ4" style="background:#1e293b;color:#64748b;border-color:#334155">새 문제</button>
    </div>
    <div class="quiz-feedback" id="fb4"></div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════
     TAB 3: 탐구활동 5 — 역방향 관계식
═══════════════════════════════════════════════════ -->
<div id="panel-ex5" class="panel">

  <div class="step-card">
    <span class="step-num">목표</span>
    <div class="diag-wrap"><canvas id="cvsDiag5" height="195"></canvas></div>
    <div class="legend-row">
      <span class="leg"><span class="leg-dot" style="background:#f59e0b"></span>알고 있는 것: A′(a′,b′) — 화면의 좌표</span>
      <span class="leg"><span class="leg-dot" style="background:#4ade80"></span>구하는 것: A(a,b) — 실제 좌표</span>
    </div>
    <div class="step-body">
      탐구활동 4에서 구한 공식을 <b>역으로</b> 풀어,<br>
      화면 좌표 <b class="hl-y">A′(a′, b′)</b> 로부터 실제 좌표 <b class="hl-g">A(a, b)</b> 를 구해봅니다.
    </div>
  </div>

  <div class="step-card">
    <span class="step-num">STEP 1 — b′에서 b 구하기</span>
    <div class="step-body">
      탐구활동 4의 결과:
      <div class="formula">b′ / 22 = b / (b + 28)</div>
      양변을 교차 곱하면: <span class="hl-y">b′</span>(b + 28) = 22b
      <div class="formula">b′·b + 28b′ = 22b</div>
      b를 한쪽으로 모으면: 22b − b′·b = 28b′
      <div class="formula">(22 − b′)·b = 28b′</div>
      따라서:
      <div class="formula" style="color:#4ade80; font-size:1.05rem">b = 28b′ / (22 − b′)</div>
    </div>
  </div>

  <div class="step-card">
    <span class="step-num">STEP 2 — a′에서 a 구하기</span>
    <div class="step-body">
      탐구활동 4의 결과: a′ = 28a / (b + 28)<br><br>
      STEP 1에서 b + 28 = 28b′/(22 − b′) + 28 을 계산하면:
      <div class="formula">b + 28 = (28b′ + 28(22 − b′)) / (22 − b′) = 28·22 / (22 − b′)</div>
      따라서 a = a′·(b + 28) / 28 이므로:
      <div class="formula" style="color:#4ade80; font-size:1.05rem">a = 22a′ / (22 − b′)</div>
    </div>
  </div>

  <div class="step-card">
    <span class="step-num">STEP 3 — 역관계식 정리</span>
    <div class="step-body">
      화면 속 점 <b class="hl-y">A′(a′, b′)</b> → 실제 점 <b class="hl-g">A(a, b)</b> :
      <div class="formula" style="font-size:1rem; color:#7dd3fc; line-height:2">
        a = 22a′ / (22 − b′)<br>
        b = 28b′ / (22 − b′)
      </div>
      <span style="font-size:0.78rem;color:#64748b">
        단, b′ &lt; 22 이어야 합니다. (b′ = 22 이면 b → ∞, 즉 무한히 먼 곳)
      </span>
    </div>
  </div>

  <!-- Live calculator -->
  <div class="calc-card">
    <div class="ctrl-title">🔢 역공식 계산기 — 화면 좌표를 넣으면 실제 좌표가!</div>
    <div class="calc-row">
      <div class="calc-col">
        <div class="calc-label">a′ (화면 x)</div>
        <input class="calc-inp" type="number" id="inp-ap" value="14" step="0.1">
      </div>
      <div class="calc-col">
        <div class="calc-label">b′ (화면 y, &lt; 22)</div>
        <input class="calc-inp" type="number" id="inp-bp" value="11" step="0.1">
      </div>
    </div>
    <div class="calc-result" id="calc-out">—</div>
  </div>

  <!-- Quiz -->
  <div class="quiz-card">
    <div class="ctrl-title">🧩 확인 문제 — A′(a′,b′)에서 A(a,b)를 구하세요</div>
    <div class="quiz-q">
      화면 좌표 A′(<b class="hl-y" id="qa2">?</b>, <b class="hl-y" id="qb2">?</b>)에 해당하는<br>
      실제 좌표 A(a, b)를 구하세요.
    </div>
    <div class="quiz-input-row">
      <span style="font-size:.82rem;color:#94a3b8">a =</span>
      <input type="number" id="ans-a2" placeholder="소수점 2자리" step="0.01">
      <span style="font-size:.82rem;color:#94a3b8">b =</span>
      <input type="number" id="ans-b2" placeholder="소수점 2자리" step="0.01">
      <button class="quiz-btn" id="checkBtn5">확인</button>
      <button class="quiz-btn" id="newQ5" style="background:#1e293b;color:#64748b;border-color:#334155">새 문제</button>
    </div>
    <div class="quiz-feedback" id="fb5"></div>
  </div>
</div>

<!-- ═══════════════════════════════════════════════════
     TAB 4: 아르놀피니 부부의 초상 적용
═══════════════════════════════════════════════════ -->
<div id="panel-arno" class="panel">

  <!-- 배경 설명 -->
  <div class="step-card">
    <span class="step-num">배경 설명</span>
    <div class="step-body">
      <b>아르놀피니 부부의 초상</b> (얀 판 에이크, 1434), 실제 크기 <b class="hl-r">82.2 × 60 cm</b>.<br>
      관찰자 눈 높이 <b class="hl-r">H = 77.8 cm</b> (그림 아랫단 기준),
      그림까지 수평 거리 <b class="hl-r">D = 150 cm</b>.<br>
      4단계 활동으로 <b class="hl-g">Mr. 아르놀피니의 실제 위치</b>를 계산해봅시다!
    </div>
  </div>

  <!-- 4단계 진행 바 -->
  <div class="arno-step-bar">
    <div class="asb-dot active" id="asbDot1">1</div>
    <div class="asb-line" id="asbLine1"></div>
    <div class="asb-dot" id="asbDot2">2</div>
    <div class="asb-line" id="asbLine2"></div>
    <div class="asb-dot" id="asbDot3">3</div>
    <div class="asb-line" id="asbLine3"></div>
    <div class="asb-dot" id="asbDot4">4</div>
  </div>
  <div class="asb-label-row">
    <span>📐 그림 측정</span>
    <span>🌐 3D 장면</span>
    <span>📌 변수 확인</span>
    <span>🧮 역공식 계산</span>
  </div>

  <!-- ══ STEP 1: 그림에서 a′, b′ 측정 ══ -->
  <div class="arno-section show" id="arnoSec1">
    <div class="step-card">
      <span class="step-num">STEP 1 — 그림에서 a′, b′ 측정하기</span>
      <div class="step-body" style="margin-bottom:12px">
        그림의 실제 크기는 <b class="hl-r">82.2 cm × 60 cm</b>입니다.<br>
        <b class="hl-p">📍 발 클릭</b> 도구로 Mr. 아르놀피니의 <b>발 위치를 클릭</b>하세요.<br>
        <span style="color:#f59e0b">■ a′</span> = 그림 <b>가운데 세로선</b>에서 발까지 <b>수평 거리</b> (cm)<br>
        <span style="color:#4ade80">■ b′</span> = 그림 <b>아랫단</b>에서 발까지 <b>수직 거리</b> (cm)<br>
        <span style="font-size:0.76rem;color:#64748b">📐 자 도구로 cm 거리를 직접 측정하거나, ✏️ 직선으로 보조선을 그을 수도 있습니다.</span>
      </div>

      <div class="arno-toolbar">
        <button class="atl-btn mark-on" id="arnoBtnMark">📍 발 클릭</button>
        <button class="atl-btn" id="arnoBtnLine">✏️ 직선</button>
        <button class="atl-btn" id="arnoBtnRuler">📐 자 (cm)</button>
        <div class="arno-vsep"></div>
        <div class="acswatch active" style="background:#ef4444" data-ac="#ef4444"></div>
        <div class="acswatch" style="background:#facc15" data-ac="#facc15"></div>
        <div class="acswatch" style="background:#22c55e" data-ac="#22c55e"></div>
        <div class="acswatch" style="background:#38bdf8" data-ac="#38bdf8"></div>
        <div class="acswatch" style="background:#f8fafc" data-ac="#f8fafc"></div>
        <div class="arno-vsep"></div>
        <button class="atl-btn" id="arnoBtnUndo">↩ 되돌리기</button>
        <button class="atl-btn" id="arnoBtnClear">🗑 전체삭제</button>
      </div>

      <div class="arno-tip tip-mark" id="arnoMarkTip" style="display:block">
        📍 <b>발 클릭</b>: 그림 안에서 Mr. 아르놀피니의 발 위치를 클릭하면 a′, b′가 자동 계산됩니다.
      </div>
      <div class="arno-tip tip-ruler" id="arnoRulerTip">
        📐 <b>자 도구</b>: 드래그로 자를 놓고 끝점을 조정하세요. 그림 실제 크기(60×82.2 cm) 기준 cm 값 표시. 우클릭으로 삭제.
      </div>

      <div class="arno-cvs-outer" id="arnoCvsOuter">
        <canvas id="cvsArno"></canvas>
      </div>

      <div class="coord-badge">
        <div class="coord-badge-box">
          <div class="cb-label">a′ — 가운데 세로선에서 발까지 수평 거리 (cm)</div>
          <div class="cb-val" id="cbAp" style="color:#f59e0b">— 발을 클릭하세요</div>
        </div>
        <div class="coord-badge-box">
          <div class="cb-label">b′ — 아랫단에서 발까지 수직 거리 (cm)</div>
          <div class="cb-val" id="cbBp" style="color:#4ade80">— 발을 클릭하세요</div>
        </div>
      </div>

      <button class="arno-next-btn" id="arnoNext1Btn">
        발 위치를 먼저 표시하세요 (📍 클릭 후 활성화)
      </button>
    </div>
  </div>

  <!-- ══ STEP 2: 3D 갤러리 장면 ══ -->
  <div class="arno-section" id="arnoSec2">
    <div class="step-card">
      <span class="step-num">STEP 2 — 3D 갤러리 장면</span>
      <div class="step-body" style="margin-bottom:8px">
        그림이 벽에 걸려 있고 관찰자가 앞에서 바라보고 있습니다.<br>
        Mr. 아르놀피니는 <b class="hl-y">그림 뒤</b>에 서 있습니다 — 마치 <b>창문 너머</b>를 포착한 것처럼요!<br>
        <span style="font-size:0.75rem;color:#64748b">🖱 드래그: 회전 &nbsp;|&nbsp; 스크롤/핀치: 확대·축소 &nbsp;|&nbsp; 더블클릭: 초기화</span>
      </div>
      <div class="arno-3d-wrap">
        <canvas id="cvsArno3D"></canvas>
        <div class="arno-3d-hint">드래그 회전 · 스크롤 확대·축소 · 더블클릭 초기화</div>
      </div>
      <button class="arno-next-btn ready" id="arnoNext2Btn" style="margin-top:12px">
        다음: 변수 확인하기 →
      </button>
    </div>
  </div>

  <!-- ══ STEP 3: 변수 확인 ══ -->
  <div class="arno-section" id="arnoSec3">
    <div class="step-card">
      <span class="step-num">STEP 3 — 3D 장면에서 변수 확인</span>
      <div class="step-body" style="margin-bottom:10px">
        3D 장면에서 각 변수가 어디에 해당하는지 확인하세요.<br>
        <span style="color:#f87171">■ <b>H = 77.8 cm</b></span> : 관찰자 눈 높이 (그림 아랫단 기준)<br>
        <span style="color:#93c5fd">■ <b>D = 150 cm</b></span> : 관찰자 눈에서 그림까지 수평 거리<br>
        <span style="color:#f59e0b">■ <b>a′</b></span> : 그림 가운데 세로선에서 발 위치까지 수평 거리 (그림에서 측정)<br>
        <span style="color:#4ade80">■ <b>b′</b></span> : 그림 아랫단에서 발 위치까지 수직 거리 (그림에서 측정)<br>
        <span style="color:#60a5fa">■ <b>a</b></span> : 실제 공간에서 중심 세로선으로부터의 수평 거리 (구하는 값)<br>
        <span style="color:#a78bfa">■ <b>b</b></span> : 실제 공간에서 그림에서 아르놀피니까지의 거리 (구하는 값)
      </div>
      <button class="arno-next-btn ready" id="arnoNext3Btn">
        다음: 역공식으로 계산하기 →
      </button>
    </div>
  </div>

  <!-- ══ STEP 4: 역공식 계산 ══ -->
  <div class="arno-section" id="arnoSec4">
    <div class="step-card">
      <span class="step-num">STEP 4 — 역공식으로 실제 위치 계산</span>
      <div class="step-body" style="margin-bottom:12px">
        STEP 1에서 측정한 <span style="color:#f59e0b"><b>a′</b></span>,
        <span style="color:#4ade80"><b>b′</b></span>를 역공식에 대입하면
        Mr. 아르놀피니의 실제 위치 <span style="color:#60a5fa"><b>A(a, b)</b></span>를 구할 수 있습니다!
      </div>

      <div class="arno-formula">
        <div class="fml-title">역공식 (탐구활동 5 결과)</div>
        <div class="fml">
          b = <span class="fhl">D · b′</span> / (<span class="fhl">H − b′</span>)
          &nbsp;=&nbsp; 150 · b′ / (77.8 − b′)
        </div>
        <div class="fml">
          a = <span class="fhl">H · a′</span> / (<span class="fhl">H − b′</span>)
          &nbsp;=&nbsp; 77.8 · a′ / (77.8 − b′)
        </div>
        <div class="fml-note">H = 77.8 cm (눈 높이, 그림 아랫단 기준) &nbsp;|&nbsp; D = 150 cm (그림까지 수평 거리)</div>
      </div>

      <div class="arno-calc-box">
        <div class="arno-calc-title">🧮 계산기 (STEP 1 측정값이 자동 입력됩니다)</div>
        <div class="arno-calc-row">
          <span class="arno-calc-lbl">a′ = 가운데선에서 발까지 수평 거리 (cm)</span>
          <input class="arno-calc-inp" id="arnoInpAp" type="number" step="0.1" placeholder="예: 11.5">
        </div>
        <div class="arno-calc-row">
          <span class="arno-calc-lbl">b′ = 아랫단에서 발까지 수직 거리 (cm)</span>
          <input class="arno-calc-inp" id="arnoInpBp" type="number" step="0.1" placeholder="예: 12.7">
        </div>
        <button class="arno-calc-btn" id="arnoCalcBtn">계산하기 → 3D 업데이트</button>
        <div class="arno-result" id="arnoResult"></div>
      </div>
    </div>
  </div>

</div><!-- panel-arno -->

</div><!-- #app -->

<script>
(function () {
'use strict';

/* ── Constants ── */
const H = 22;   // eye height
const D = 28;   // distance from screen to eye (horizontal)

/* ── Projection formulas ── */
function project(a, b) {
  const denom = b + D;
  return { ap: D * a / denom, bp: H * b / denom };
}
function inverse(ap, bp) {
  const den = H - bp;
  if (Math.abs(den) < 0.001) return null;
  return { a: H * ap / den, b: D * bp / den };
}

/* ── State ── */
let a = 30, b = 28;

/* ── DOM refs ── */
const slA = document.getElementById('slA');
const slB = document.getElementById('slB');
const cvsSide = document.getElementById('cvsSide');
const ctxS = cvsSide.getContext('2d');
const cvsTop = document.getElementById('cvsTop');
const ctxT = cvsTop.getContext('2d');

function px(canvas) { return window.devicePixelRatio || 1; }

function fitCvs(cvs, h) {
  const r = window.devicePixelRatio || 1;
  const w = cvs.parentElement.clientWidth;
  cvs.width  = w * r;
  cvs.height = h * r;
  cvs.style.height = h + 'px';
  cvs.getContext('2d').setTransform(r, 0, 0, r, 0, 0);
  return { w, h };
}

/* ═══════════════════════════════════
   SIDE VIEW (b direction — height)
   Shows: Eye E at (0, 22) looking at A on ground at depth b
   Screen at x=0 (depth=0)
═══════════════════════════════════ */
function drawSide() {
  const { w, h } = fitCvs(cvsSide, 220);
  const ctx = ctxS;
  const { ap, bp } = project(a, b);

  // coordinate mapping
  // horizontal axis: depth.  0 = screen, left = behind screen (eye side), right = far
  // screen x=0 maps to px X_SCREEN
  const X_SCREEN = w * 0.35;
  const X_EYE    = X_SCREEN - D * 3.2;   // eye is 28 units left of screen
  const X_A      = X_SCREEN + b * 3.2;   // A is b units right of screen
  const Y_GND    = h * 0.72;             // ground line y
  const Y_EYE    = Y_GND - H * 3.2;      // eye is H units above ground
  const Y_Ap     = Y_GND - bp * 3.2;     // A' is bp units above ground on screen

  ctx.clearRect(0, 0, w, h);

  // background
  ctx.fillStyle = '#0a1628';
  ctx.fillRect(0, 0, w, h);

  // title
  ctx.fillStyle = '#475569';
  ctx.font = 'bold 11px Segoe UI';
  ctx.fillText('옆에서 본 단면 (b′ 유도)', 10, 16);

  // ground plane
  ctx.strokeStyle = '#1e40af';
  ctx.lineWidth = 1.5;
  ctx.setLineDash([6, 4]);
  ctx.beginPath(); ctx.moveTo(0, Y_GND); ctx.lineTo(w, Y_GND); ctx.stroke();
  ctx.setLineDash([]);

  // screen line (vertical at X_SCREEN)
  ctx.strokeStyle = '#7c3aed';
  ctx.lineWidth = 2.5;
  ctx.beginPath(); ctx.moveTo(X_SCREEN, Y_GND - H * 3.8); ctx.lineTo(X_SCREEN, Y_GND + 10); ctx.stroke();
  ctx.fillStyle = '#a78bfa';
  ctx.font = 'bold 11px Segoe UI';
  ctx.fillText('화면', X_SCREEN + 5, Y_GND - H * 3.8 + 14);

  // dimensions: D arrow under eye-to-screen
  ctx.strokeStyle = '#475569'; ctx.lineWidth = 1;
  ctx.setLineDash([3,3]);
  ctx.beginPath(); ctx.moveTo(X_EYE, Y_GND + 12); ctx.lineTo(X_SCREEN, Y_GND + 12); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#64748b'; ctx.font = '10px Segoe UI';
  ctx.textAlign = 'center';
  ctx.fillText('28', (X_EYE + X_SCREEN) / 2, Y_GND + 24);
  ctx.textAlign = 'left';

  // b dimension
  ctx.strokeStyle = '#475569'; ctx.lineWidth = 1;
  ctx.setLineDash([3,3]);
  ctx.beginPath(); ctx.moveTo(X_SCREEN, Y_GND + 12); ctx.lineTo(X_A, Y_GND + 12); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#64748b'; ctx.font = '10px Segoe UI';
  ctx.textAlign = 'center';
  ctx.fillText('b=' + b, (X_SCREEN + X_A) / 2, Y_GND + 24);
  ctx.textAlign = 'left';

  // H dimension (eye height)
  ctx.strokeStyle = '#475569'; ctx.lineWidth = 1;
  ctx.setLineDash([3,3]);
  ctx.beginPath(); ctx.moveTo(X_EYE - 12, Y_GND); ctx.lineTo(X_EYE - 12, Y_EYE); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#64748b'; ctx.font = '10px Segoe UI';
  ctx.textAlign = 'right';
  ctx.fillText('22', X_EYE - 14, (Y_GND + Y_EYE) / 2 + 4);
  ctx.textAlign = 'left';

  // b' dimension
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(X_SCREEN + 10, Y_GND); ctx.lineTo(X_SCREEN + 10, Y_Ap);
  ctx.stroke();
  ctx.fillStyle = '#fbbf24'; ctx.font = 'bold 10px Segoe UI';
  ctx.fillText("b'=" + bp.toFixed(1), X_SCREEN + 13, (Y_GND + Y_Ap) / 2 + 4);

  // similar triangle fill (big: E→A, small: projected)
  // Big triangle: E → ground at A's x → A on ground
  ctx.fillStyle = 'rgba(34,197,94,0.07)';
  ctx.beginPath();
  ctx.moveTo(X_EYE, Y_EYE);
  ctx.lineTo(X_EYE, Y_GND);
  ctx.lineTo(X_A, Y_GND);
  ctx.closePath();
  ctx.fill();

  // ray line E → A
  ctx.strokeStyle = '#22c55e';
  ctx.lineWidth = 1.5;
  ctx.setLineDash([6,4]);
  ctx.beginPath(); ctx.moveTo(X_EYE, Y_EYE); ctx.lineTo(X_A, Y_GND); ctx.stroke();
  ctx.setLineDash([]);

  // Small triangle: E → screen → A'
  ctx.fillStyle = 'rgba(250,204,21,0.1)';
  ctx.beginPath();
  ctx.moveTo(X_EYE, Y_EYE);
  ctx.lineTo(X_SCREEN, Y_Ap);
  ctx.lineTo(X_SCREEN, Y_GND);
  ctx.lineTo(X_EYE, Y_GND);
  ctx.closePath();
  ctx.fill();
  ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 1.5;
  ctx.strokeRect(X_EYE, Y_GND - 6, 6, 6); // right angle mark

  // Eye E
  ctx.fillStyle = '#f43f5e';
  ctx.beginPath(); ctx.arc(X_EYE, Y_EYE, 7, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Segoe UI';
  ctx.fillText('E', X_EYE + 10, Y_EYE + 4);

  // A point
  ctx.fillStyle = '#4ade80';
  ctx.beginPath(); ctx.arc(X_A, Y_GND, 7, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#4ade80'; ctx.font = 'bold 11px Segoe UI';
  ctx.fillText('A', X_A + 8, Y_GND - 4);

  // A' point on screen
  ctx.fillStyle = '#f59e0b';
  ctx.beginPath(); ctx.arc(X_SCREEN, Y_Ap, 7, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#f59e0b'; ctx.font = "bold 11px Segoe UI";
  ctx.fillText("A'", X_SCREEN + 8, Y_Ap - 4);
}

/* ═══════════════════════════════════
   TOP VIEW (a direction — width)
   Shows plan view: eye at left, screen vertical line, A on right
═══════════════════════════════════ */
function drawTop() {
  const { w, h } = fitCvs(cvsTop, 200);
  const ctx = ctxT;
  const { ap, bp } = project(a, b);

  const CY = h / 2;
  const X_SCREEN = w * 0.35;
  const X_EYE    = X_SCREEN - D * 3.2;
  const X_A      = X_SCREEN + b * 3.2;

  // Map a-coordinate to screen y (center = CY)
  const scaleA = 3.0;
  const Y_A  = CY - a  * scaleA;
  const Y_Ap = CY - ap * scaleA;

  ctx.clearRect(0, 0, w, h);
  ctx.fillStyle = '#0a1628';
  ctx.fillRect(0, 0, w, h);

  // title
  ctx.fillStyle = '#475569';
  ctx.font = 'bold 11px Segoe UI';
  ctx.fillText('위에서 본 평면 (a′ 유도)', 10, 16);

  // center axis (b direction)
  ctx.strokeStyle = '#1e3a5f'; ctx.lineWidth = 1;
  ctx.setLineDash([5,4]);
  ctx.beginPath(); ctx.moveTo(0, CY); ctx.lineTo(w, CY); ctx.stroke();
  ctx.setLineDash([]);

  // screen
  ctx.strokeStyle = '#7c3aed'; ctx.lineWidth = 2.5;
  ctx.beginPath(); ctx.moveTo(X_SCREEN, 10); ctx.lineTo(X_SCREEN, h - 10); ctx.stroke();
  ctx.fillStyle = '#a78bfa'; ctx.font = 'bold 11px Segoe UI';
  ctx.fillText('화면', X_SCREEN + 5, 20);

  // D and b dimensions
  ctx.strokeStyle = '#475569'; ctx.lineWidth = 1;
  ctx.setLineDash([3,3]);
  ctx.beginPath(); ctx.moveTo(X_EYE, h-14); ctx.lineTo(X_SCREEN, h-14); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#64748b'; ctx.font = '10px Segoe UI';
  ctx.textAlign = 'center';
  ctx.fillText('28', (X_EYE + X_SCREEN)/2, h-4);

  ctx.setLineDash([3,3]);
  ctx.beginPath(); ctx.moveTo(X_SCREEN, h-14); ctx.lineTo(X_A, h-14); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillText('b='+b, (X_SCREEN+X_A)/2, h-4);
  ctx.textAlign = 'left';

  // a dimension
  if (Math.abs(a) > 2) {
    ctx.strokeStyle = '#4ade80'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(X_A + 10, CY); ctx.lineTo(X_A + 10, Y_A); ctx.stroke();
    ctx.fillStyle = '#4ade80'; ctx.font = '10px Segoe UI';
    ctx.textAlign = 'right';
    ctx.fillText('a='+a, X_A + 8, (CY + Y_A) / 2 + 4);
    ctx.textAlign = 'left';
  }

  // a' dimension
  if (Math.abs(ap) > 1) {
    ctx.strokeStyle = '#fbbf24'; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(X_SCREEN - 10, CY); ctx.lineTo(X_SCREEN - 10, Y_Ap); ctx.stroke();
    ctx.fillStyle = '#fbbf24'; ctx.font = '10px Segoe UI';
    ctx.textAlign = 'right';
    ctx.fillText("a'="+ap.toFixed(1), X_SCREEN - 12, (CY + Y_Ap)/2 + 4);
    ctx.textAlign = 'left';
  }

  // Similar triangle fill
  ctx.fillStyle = 'rgba(34,197,94,0.07)';
  ctx.beginPath();
  ctx.moveTo(X_EYE, CY); ctx.lineTo(X_A, CY); ctx.lineTo(X_A, Y_A); ctx.closePath();
  ctx.fill();

  // Ray line E → A
  ctx.strokeStyle = '#22c55e'; ctx.lineWidth = 1.5;
  ctx.setLineDash([6,4]);
  ctx.beginPath(); ctx.moveTo(X_EYE, CY); ctx.lineTo(X_A, Y_A); ctx.stroke();
  ctx.setLineDash([]);

  // Small triangle
  ctx.fillStyle = 'rgba(250,204,21,0.1)';
  ctx.beginPath();
  ctx.moveTo(X_EYE, CY); ctx.lineTo(X_SCREEN, Y_Ap); ctx.lineTo(X_SCREEN, CY); ctx.closePath();
  ctx.fill();

  // Eye
  ctx.fillStyle = '#f43f5e';
  ctx.beginPath(); ctx.arc(X_EYE, CY, 7, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = '#fff'; ctx.font = 'bold 11px Segoe UI';
  ctx.fillText('E', X_EYE + 10, CY + 4);

  // A
  ctx.fillStyle = '#4ade80';
  ctx.beginPath(); ctx.arc(X_A, Y_A, 7, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = '#4ade80'; ctx.font = 'bold 11px Segoe UI';
  ctx.fillText('A', X_A + 8, Y_A - 4);

  // A'
  ctx.fillStyle = '#f59e0b';
  ctx.beginPath(); ctx.arc(X_SCREEN, Y_Ap, 7, 0, Math.PI*2); ctx.fill();
  ctx.fillStyle = '#f59e0b'; ctx.font = "bold 11px Segoe UI";
  ctx.fillText("A'", X_SCREEN + 8, Y_Ap - 4);
}

function updateCoords() {
  const { ap, bp } = project(a, b);
  document.getElementById('dA').textContent  = a;
  document.getElementById('dB').textContent  = b;
  document.getElementById('dAp').textContent = ap.toFixed(2);
  document.getElementById('dBp').textContent = bp.toFixed(2);
}

/* ════════════════════════════════════════════════════
   Static diagram helpers
════════════════════════════════════════════════════ */
function fitDiag(id, hpx) {
  const el = document.getElementById(id);
  if (!el) return null;
  const r = window.devicePixelRatio || 1;
  const w = el.parentElement.clientWidth;
  el.width  = w * r; el.height = hpx * r;
  el.style.height = hpx + 'px';
  const c = el.getContext('2d');
  c.setTransform(r, 0, 0, r, 0, 0);
  return { c, w, h: hpx };
}

function rr(c, x, y, w, h, r) { // rounded rect fill+stroke helper
  c.beginPath();
  c.moveTo(x+r,y); c.lineTo(x+w-r,y); c.arcTo(x+w,y,x+w,y+r,r);
  c.lineTo(x+w,y+h-r); c.arcTo(x+w,y+h,x+w-r,y+h,r);
  c.lineTo(x+r,y+h); c.arcTo(x,y+h,x,y+h-r,r);
  c.lineTo(x,y+r); c.arcTo(x,y,x+r,y,r);
  c.closePath();
}

function dimH(c, x1, x2, y, lbl, col) { // horizontal dimension
  c.save(); c.strokeStyle=col||'#64748b'; c.fillStyle=col||'#94a3b8';
  c.lineWidth=1; c.setLineDash([3,3]);
  c.beginPath(); c.moveTo(x1,y); c.lineTo(x2,y); c.stroke();
  c.setLineDash([]);
  const mx=(x1+x2)/2;
  c.font='bold 11px sans-serif'; c.textAlign='center'; c.textBaseline='middle';
  const tw=c.measureText(lbl).width+6;
  c.fillStyle='#060f1e'; c.fillRect(mx-tw/2,y-7,tw,14);
  c.fillStyle=col||'#94a3b8'; c.fillText(lbl,mx,y);
  c.restore();
}

function dimV(c, x, y1, y2, lbl, col, side) { // vertical dimension
  c.save(); c.strokeStyle=col||'#64748b'; c.fillStyle=col||'#94a3b8';
  c.lineWidth=1; c.setLineDash([3,3]);
  c.beginPath(); c.moveTo(x,y1); c.lineTo(x,y2); c.stroke();
  c.setLineDash([]);
  const my=(y1+y2)/2;
  c.font='bold 11px sans-serif';
  c.textAlign=side==='left'?'right':'left'; c.textBaseline='middle';
  c.fillStyle='#060f1e';
  const tw=c.measureText(lbl).width+6;
  if(side==='left') c.fillRect(x-tw-2,my-7,tw,14);
  else c.fillRect(x+2,my-7,tw,14);
  c.fillStyle=col||'#94a3b8'; c.fillText(lbl,side==='left'?x-4:x+4,my);
  c.restore();
}

function dot(c, x, y, col, lbl, lx, ly) {
  c.save();
  c.fillStyle=col; c.beginPath(); c.arc(x,y,6,0,Math.PI*2); c.fill();
  c.fillStyle='#fff'; c.shadowColor=col; c.shadowBlur=8;
  c.beginPath(); c.arc(x,y,3,0,Math.PI*2); c.fill();
  c.shadowBlur=0;
  if(lbl){ c.fillStyle=col; c.font='bold 13px sans-serif';
    c.textAlign='left'; c.textBaseline='middle'; c.fillText(lbl,lx||x+9,ly||y); }
  c.restore();
}

/* ── SETUP OVERVIEW: isometric-ish bird-eye sketch ── */
function drawDiagSetup() {
  const d = fitDiag('cvsDiagSetup',170); if(!d) return;
  const {c,w,h} = d;
  c.fillStyle='#060f1e'; c.fillRect(0,0,w,h);

  // Isometric-like projection: oblique at 30°
  // We'll draw a simplified 2.5D view: ground plane, screen, eye, A, A'
  const ox=w*0.25, oy=h*0.78; // origin (screen-ground corner)
  const sx=3.2, sy=1.6;       // oblique scale x,y for "depth" axis
  const pxU=sx, pyU=-sy;      // unit vector for "depth" (into scene, rightward)
  const vxU=0,  vyU=-4.0;     // unit vector for "up" (vertical)
  const axU=3.2, ayU=0;       // unit vector for "width" (sideways)

  // Dimensions  (D=28, H=22, b_rep=24, a_rep=15)
  const Dsc=14, Hsc=22*0.9, bsc=24, asc=15; // scaled units

  function pt(d_,a_,v_) { // depth, width, height → screen xy
    return [ox + d_*pxU + a_*axU + v_*vxU, oy + d_*pyU + a_*ayU + v_*vyU];
  }

  // Ground plane (parallelogram)
  c.save();
  c.fillStyle='rgba(14,116,144,0.13)'; c.strokeStyle='#164e63'; c.lineWidth=1;
  c.beginPath();
  const g0=pt(0,0,0), g1=pt(bsc+Dsc,0,0), g2=pt(bsc+Dsc,asc*2,0), g3=pt(0,asc*2,0);
  c.moveTo(g0[0],g0[1]); c.lineTo(g1[0],g1[1]); c.lineTo(g2[0],g2[1]); c.lineTo(g3[0],g3[1]);
  c.closePath(); c.fill(); c.stroke();
  c.restore();

  // Screen plane (rectangle in 3D)
  c.save();
  c.fillStyle='rgba(109,40,217,0.18)'; c.strokeStyle='#7c3aed'; c.lineWidth=2;
  const s0=pt(Dsc,0,0), s1=pt(Dsc,asc*2,0), s2=pt(Dsc,asc*2,Hsc*1.1), s3=pt(Dsc,0,Hsc*1.1);
  c.beginPath();
  c.moveTo(s0[0],s0[1]); c.lineTo(s1[0],s1[1]); c.lineTo(s2[0],s2[1]); c.lineTo(s3[0],s3[1]);
  c.closePath(); c.fill(); c.stroke();
  // "화면" label
  const sm=pt(Dsc,asc,Hsc*1.15);
  c.fillStyle='#a78bfa'; c.font='bold 11px sans-serif'; c.textAlign='center';
  c.fillText('화면(그림)',sm[0],sm[1]-5); c.restore();

  // x-axis line on ground (a direction)
  c.save(); c.strokeStyle='#22d3ee'; c.lineWidth=1.2;
  const ax0=pt(Dsc,0,0), ax1=pt(Dsc,asc*2,0);
  c.beginPath(); c.moveTo(ax0[0],ax0[1]); c.lineTo(ax1[0],ax1[1]); c.stroke();
  const axM=pt(Dsc,asc*2+1,0);
  c.fillStyle='#22d3ee'; c.font='bold 10px sans-serif'; c.textAlign='left';
  c.fillText('x축(a)',axM[0]+2,axM[1]); c.restore();

  // y-axis line on ground (b direction)
  c.save(); c.strokeStyle='#22d3ee'; c.lineWidth=1.2;
  const ay0=pt(Dsc,asc,0), ay1=pt(Dsc+bsc,asc,0);
  c.beginPath(); c.moveTo(ay0[0],ay0[1]); c.lineTo(ay1[0],ay1[1]); c.stroke();
  const ayM=pt(Dsc+bsc+1,asc,0);
  c.fillStyle='#22d3ee'; c.font='bold 10px sans-serif'; c.textAlign='left';
  c.fillText('y축(b)',ayM[0],ayM[1]); c.restore();

  // Dimension: 22 (height) on screen left edge
  c.save(); c.strokeStyle='#f87171'; c.lineWidth=1; c.setLineDash([3,3]);
  const hB=pt(Dsc,0,0), hT=pt(Dsc,0,Hsc);
  c.beginPath(); c.moveTo(hB[0]-8,hB[1]); c.lineTo(hT[0]-8,hT[1]); c.stroke();
  c.setLineDash([]); const hM=[(hB[0]+hT[0])/2-18,(hB[1]+hT[1])/2];
  c.fillStyle='#f87171'; c.font='bold 11px sans-serif'; c.textAlign='center';
  c.fillText('22',hM[0],hM[1]); c.restore();

  // Dimension: 28 (depth to screen) on ground
  c.save(); c.strokeStyle='#f87171'; c.lineWidth=1; c.setLineDash([3,3]);
  const dA=pt(0,asc,0), dB=pt(Dsc,asc,0);
  c.beginPath(); c.moveTo(dA[0],dA[1]+12); c.lineTo(dB[0],dB[1]+12); c.stroke();
  c.setLineDash([]); const dM=[(dA[0]+dB[0])/2,(dA[1]+dB[1])/2+22];
  c.fillStyle='#f87171'; c.font='bold 11px sans-serif'; c.textAlign='center';
  c.fillText('28',dM[0],dM[1]); c.restore();

  // Point A on ground
  const pA=pt(Dsc+bsc, asc, 0);
  dot(c,pA[0],pA[1],'#4ade80','A(a,b)',pA[0]+8,pA[1]-4);

  // b dimension (screen to A along ground)
  c.save(); c.strokeStyle='#4ade80'; c.lineWidth=1; c.setLineDash([3,3]);
  const bA=pt(Dsc,asc,0), bB=pt(Dsc+bsc,asc,0);
  c.beginPath(); c.moveTo(bA[0],bA[1]+12); c.lineTo(bB[0],bB[1]+12); c.stroke();
  c.setLineDash([]); const bM=[(bA[0]+bB[0])/2,(bA[1]+bB[1])/2+22];
  c.fillStyle='#4ade80'; c.font='bold 11px sans-serif'; c.textAlign='center';
  c.fillText('b',bM[0],bM[1]); c.restore();

  // a dimension on screen plane
  c.save(); c.strokeStyle='#4ade80'; c.lineWidth=1; c.setLineDash([3,3]);
  const aA=pt(Dsc,asc,0), aB=pt(Dsc,asc,0);
  // draw a vertical bar on screen at A' position
  const apPos = pt(Dsc, asc, Hsc * bsc/(bsc+Dsc)); // approximate A' height
  c.setLineDash([]); c.restore();

  // A' on screen
  const bp_ov = H * bsc/(bsc+Dsc), ap_ov = D * asc/(bsc+Dsc);
  const pAp = pt(Dsc, asc, bp_ov);
  dot(c,pAp[0],pAp[1],'#f59e0b',"A'(a',b')",pAp[0]+8,pAp[1]-4);

  // Ray line E→A through A'
  c.save();
  const pE=pt(0, asc, Hsc);
  c.strokeStyle='rgba(125,211,252,0.5)'; c.lineWidth=1.5; c.setLineDash([5,4]);
  c.beginPath(); c.moveTo(pE[0],pE[1]); c.lineTo(pA[0],pA[1]); c.stroke();
  c.setLineDash([]); c.restore();

  // Eye E
  dot(c,pE[0],pE[1],'#f43f5e','E',pE[0]-20,pE[1]-6);
  // "28" label for horizontal from E to screen
  c.fillStyle='#f87171'; c.font='10px sans-serif'; c.textAlign='center';
}

/* ── DIAGRAM 4b: side view for b' (with similar triangles) ── */
function drawDiag4b() {
  const d = fitDiag('cvsDiag4b',210); if(!d) return;
  const {c,w,h} = d;
  c.fillStyle='#060f1e'; c.fillRect(0,0,w,h);
  c.fillStyle='#334155'; c.font='bold 11px sans-serif';
  c.fillText('옆에서 본 단면 (b′ 유도) — 대표값 b=28',10,16);

  const Y_GND=h-38, LM=55;
  const avail=w-LM-20;
  const S = Math.min(avail/62, (Y_GND-28)/24); // scale px/unit
  const XEf=LM, XScr=XEf+D*S, XA=XScr+28*S; // b_rep=28
  const YE=Y_GND-H*S, YAp=Y_GND-(H*28/(28+D))*S; // bp_rep=22*28/56=11

  // Ground
  c.strokeStyle='#1e3a5f'; c.lineWidth=1.5; c.setLineDash([7,4]);
  c.beginPath(); c.moveTo(LM-15,Y_GND); c.lineTo(w-10,Y_GND); c.stroke();
  c.setLineDash([]);

  // Screen
  c.strokeStyle='#7c3aed'; c.lineWidth=3;
  c.beginPath(); c.moveTo(XScr,Y_GND+8); c.lineTo(XScr,YE-18); c.stroke();
  c.fillStyle='#a78bfa'; c.font='bold 11px sans-serif'; c.textAlign='center';
  c.fillText('화면',XScr,YE-22); c.textAlign='left';

  // BIG green triangle: E-foot → E → A (right angle at E-foot)
  c.save();
  c.fillStyle='rgba(34,197,94,0.12)'; c.strokeStyle='rgba(34,197,94,0.55)'; c.lineWidth=1.8;
  c.beginPath(); c.moveTo(XEf,Y_GND); c.lineTo(XEf,YE); c.lineTo(XA,Y_GND); c.closePath();
  c.fill(); c.stroke();
  // right angle mark at E-foot
  c.strokeStyle='rgba(34,197,94,0.7)'; c.lineWidth=1.2;
  c.strokeRect(XEf,Y_GND-9,9,9);
  // "큰△" label
  c.fillStyle='rgba(34,197,94,0.8)'; c.font='10px sans-serif';
  c.fillText('큰 △', XEf+8, Y_GND-15);
  c.restore();

  // SMALL amber triangle: A'-foot → A' → A (right angle at A'-foot = (XScr, Y_GND))
  c.save();
  c.fillStyle='rgba(251,191,36,0.18)'; c.strokeStyle='rgba(251,191,36,0.7)'; c.lineWidth=1.8;
  c.beginPath(); c.moveTo(XScr,Y_GND); c.lineTo(XScr,YAp); c.lineTo(XA,Y_GND); c.closePath();
  c.fill(); c.stroke();
  // right angle mark at A'-foot
  c.strokeStyle='rgba(251,191,36,0.8)'; c.lineWidth=1.2;
  c.strokeRect(XScr-9,Y_GND-9,9,9);
  // "작은△" label
  c.fillStyle='rgba(251,191,36,0.9)'; c.font='10px sans-serif'; c.textAlign='right';
  c.fillText('작은 △',XScr-2,(Y_GND+YAp)/2-4);
  c.textAlign='left'; c.restore();

  // Ray E→A
  c.strokeStyle='rgba(125,211,252,0.4)'; c.lineWidth=1.5; c.setLineDash([6,4]);
  c.beginPath(); c.moveTo(XEf,YE); c.lineTo(XA,Y_GND); c.stroke();
  c.setLineDash([]);

  // Dimension: 22
  dimV(c,XEf-16,Y_GND,YE,'22','#f87171','left');
  // Dimension: 28 (E to screen)
  dimH(c,XEf,XScr,Y_GND+18,'28','#94a3b8');
  // Dimension: b (screen to A)
  dimH(c,XScr,XA,Y_GND+18,'b','#4ade80');
  // Dimension: b'
  dimV(c,XScr+16,Y_GND,YAp,"b'  ",'#f59e0b','right');

  // Dots
  dot(c,XEf,YE,'#f43f5e','E',XEf-18,YE-8);
  dot(c,XA,Y_GND,'#4ade80','A(a,b)',XA+8,Y_GND-6);
  dot(c,XScr,YAp,'#f59e0b',"A'(a',b')",XScr+8,YAp-8);

  // Similarity badge
  c.save();
  c.fillStyle='rgba(251,191,36,0.13)'; c.strokeStyle='#fbbf24'; c.lineWidth=1;
  rr(c,w-138,24,130,42,7); c.fill(); c.stroke();
  c.fillStyle='#fcd34d'; c.font='bold 11px sans-serif'; c.textAlign='center';
  c.fillText('b′/22 = b/(b+28)',w-73,42);
  c.fillStyle='#f59e0b'; c.font='bold 12px sans-serif';
  c.fillText('b′ = 22b/(b+28)',w-73,60);
  c.textAlign='left'; c.restore();
}

/* ── DIAGRAM 4a: top view for a' (with similar triangles) ── */
function drawDiag4a() {
  const d = fitDiag('cvsDiag4a',195); if(!d) return;
  const {c,w,h} = d;
  c.fillStyle='#060f1e'; c.fillRect(0,0,w,h);
  c.fillStyle='#334155'; c.font='bold 11px sans-serif';
  c.fillText('위에서 본 평면 (a′ 유도) — 대표값 b=28, a=20',10,16);

  const CY=h*0.52, LM=55;
  const avail=w-LM-20;
  const S = Math.min(avail/62, (CY-24)/22);
  const XE=LM, XScr=XE+D*S, XA=XScr+28*S; // b_rep=28
  const a_rep=20, ap_rep=D*a_rep/(28+D); // 28*20/56=10
  const YA=CY-a_rep*S, YAp=CY-ap_rep*S;

  // Center axis (E to A direction)
  c.strokeStyle='#1e3a5f'; c.lineWidth=1; c.setLineDash([5,4]);
  c.beginPath(); c.moveTo(LM-10,CY); c.lineTo(w-10,CY); c.stroke();
  c.setLineDash([]);
  c.fillStyle='#334155'; c.font='10px sans-serif';
  c.fillText('중심축',w-42,CY-4);

  // Screen
  c.strokeStyle='#7c3aed'; c.lineWidth=3;
  c.beginPath(); c.moveTo(XScr,25); c.lineTo(XScr,h-25); c.stroke();
  c.fillStyle='#a78bfa'; c.font='bold 11px sans-serif'; c.textAlign='center';
  c.fillText('화면',XScr,20); c.textAlign='left';

  // BIG green triangle: E → A-foot → A (right angle at A-foot)
  c.save();
  c.fillStyle='rgba(34,197,94,0.12)'; c.strokeStyle='rgba(34,197,94,0.55)'; c.lineWidth=1.8;
  c.beginPath(); c.moveTo(XE,CY); c.lineTo(XA,CY); c.lineTo(XA,YA); c.closePath();
  c.fill(); c.stroke();
  c.strokeStyle='rgba(34,197,94,0.7)'; c.lineWidth=1.2;
  c.strokeRect(XA-9,CY-9,9,9); // right angle at A-foot
  c.fillStyle='rgba(34,197,94,0.8)'; c.font='10px sans-serif';
  c.fillText('큰 △',(XE+XScr)/2-10,CY-8);
  c.restore();

  // SMALL amber triangle: E → screen-center → A' (right angle at screen-center)
  c.save();
  c.fillStyle='rgba(251,191,36,0.18)'; c.strokeStyle='rgba(251,191,36,0.7)'; c.lineWidth=1.8;
  c.beginPath(); c.moveTo(XE,CY); c.lineTo(XScr,CY); c.lineTo(XScr,YAp); c.closePath();
  c.fill(); c.stroke();
  c.strokeStyle='rgba(251,191,36,0.8)'; c.lineWidth=1.2;
  c.strokeRect(XScr,CY,9,-9); // right angle at screen-center
  c.fillStyle='rgba(251,191,36,0.9)'; c.font='10px sans-serif';
  c.fillText('작은 △',XScr+4,(CY+YAp)/2-4);
  c.restore();

  // Ray E→A
  c.strokeStyle='rgba(125,211,252,0.4)'; c.lineWidth=1.5; c.setLineDash([6,4]);
  c.beginPath(); c.moveTo(XE,CY); c.lineTo(XA,YA); c.stroke();
  c.setLineDash([]);

  // Dimensions
  dimH(c,XE,XScr,h-22,'28','#94a3b8');
  dimH(c,XScr,XA,h-22,'b','#4ade80');
  dimV(c,XA+16,CY,YA,'a','#4ade80','right');
  dimV(c,XScr-16,CY,YAp,"a'",'#f59e0b','left');

  // Dots
  dot(c,XE,CY,'#f43f5e','E',XE-18,CY-8);
  dot(c,XA,YA,'#4ade80','A(a,b)',XA+8,YA-6);
  dot(c,XScr,YAp,'#f59e0b',"A'(a',b')",XScr+8,YAp-8);

  // Similarity badge
  c.save();
  c.fillStyle='rgba(251,191,36,0.13)'; c.strokeStyle='#fbbf24'; c.lineWidth=1;
  rr(c,w-138,24,130,42,7); c.fill(); c.stroke();
  c.fillStyle='#fcd34d'; c.font='bold 11px sans-serif'; c.textAlign='center';
  c.fillText("a′/a = 28/(b+28)",w-73,42);
  c.fillStyle='#f59e0b'; c.font='bold 12px sans-serif';
  c.fillText("a′ = 28a/(b+28)",w-73,60);
  c.textAlign='left'; c.restore();
}

/* ── DIAGRAM 5: inverse — known A', find A ── */
function drawDiag5() {
  const d = fitDiag('cvsDiag5',195); if(!d) return;
  const {c,w,h} = d;
  c.fillStyle='#060f1e'; c.fillRect(0,0,w,h);
  c.fillStyle='#334155'; c.font='bold 11px sans-serif';
  c.fillText("역방향 탐구: A'(a',b') 를 알 때 A(a,b) 구하기",10,16);

  // Same side-view layout as drawDiag4b
  const Y_GND=h-38, LM=55;
  const avail=w-LM-20;
  const S = Math.min(avail/62, (Y_GND-28)/24);
  const XEf=LM, XScr=XEf+D*S, XA=XScr+28*S;
  const YE=Y_GND-H*S, YAp=Y_GND-(H*28/(28+D))*S;

  // Ground
  c.strokeStyle='#1e3a5f'; c.lineWidth=1.5; c.setLineDash([7,4]);
  c.beginPath(); c.moveTo(LM-15,Y_GND); c.lineTo(w-10,Y_GND); c.stroke();
  c.setLineDash([]);

  // Screen
  c.strokeStyle='#7c3aed'; c.lineWidth=3;
  c.beginPath(); c.moveTo(XScr,Y_GND+8); c.lineTo(XScr,YE-18); c.stroke();
  c.fillStyle='#a78bfa'; c.font='bold 11px sans-serif'; c.textAlign='center';
  c.fillText('화면',XScr,YE-22); c.textAlign='left';

  // Triangle (faded)
  c.save();
  c.fillStyle='rgba(100,116,139,0.06)'; c.strokeStyle='rgba(100,116,139,0.3)'; c.lineWidth=1;
  c.beginPath(); c.moveTo(XScr,Y_GND); c.lineTo(XScr,YAp); c.lineTo(XA,Y_GND); c.closePath();
  c.fill(); c.stroke(); c.restore();
  c.save();
  c.fillStyle='rgba(100,116,139,0.05)'; c.strokeStyle='rgba(100,116,139,0.2)'; c.lineWidth=1;
  c.beginPath(); c.moveTo(XEf,Y_GND); c.lineTo(XEf,YE); c.lineTo(XA,Y_GND); c.closePath();
  c.fill(); c.stroke(); c.restore();

  // Ray (faded)
  c.strokeStyle='rgba(125,211,252,0.25)'; c.lineWidth=1.5; c.setLineDash([6,4]);
  c.beginPath(); c.moveTo(XEf,YE); c.lineTo(XA,Y_GND); c.stroke();
  c.setLineDash([]);

  // KNOWN: b' annotation (amber, prominent)
  dimV(c,XScr+16,Y_GND,YAp,"b' (알고 있음)",'#f59e0b','right');
  // UNKNOWN: b annotation (green, with question mark glow)
  dimH(c,XScr,XA,Y_GND+18,'b = ?','#4ade80');
  dimV(c,XEf-16,Y_GND,YE,'22','#f87171','left');
  dimH(c,XEf,XScr,Y_GND+34,'28','#94a3b8');

  // Dots — A' bright (known), A dim with glow (unknown)
  dot(c,XEf,YE,'#f43f5e','E',XEf-18,YE-8);
  // A' — known, bright
  c.save(); c.shadowColor='#f59e0b'; c.shadowBlur=14;
  dot(c,XScr,YAp,'#f59e0b',"A'(a',b')  ← 알고 있음",XScr+8,YAp-8);
  c.restore();
  // A — unknown, with pulsing look (static dashed circle)
  c.save();
  c.strokeStyle='#4ade80'; c.lineWidth=1.5; c.setLineDash([4,3]);
  c.beginPath(); c.arc(XA,Y_GND,10,0,Math.PI*2); c.stroke();
  c.setLineDash([]);
  c.fillStyle='rgba(74,222,128,0.2)'; c.beginPath(); c.arc(XA,Y_GND,10,0,Math.PI*2); c.fill();
  c.fillStyle='#86efac'; c.font='bold 13px sans-serif';
  c.fillText('A(a,b)  ← 구해야 함',XA+14,Y_GND-6);
  c.restore();

  // Formula boxes
  const fx=w-145, fy=26;
  c.save();
  c.fillStyle='rgba(74,222,128,0.1)'; c.strokeStyle='#16a34a'; c.lineWidth=1;
  rr(c,fx,fy,135,52,8); c.fill(); c.stroke();
  c.fillStyle='#86efac'; c.font='bold 11px sans-serif'; c.textAlign='center';
  c.fillText('역공식',fx+67,fy+14);
  c.fillStyle='#4ade80'; c.font='bold 11px sans-serif';
  c.fillText("b = 28b'/(22−b')",fx+67,fy+31);
  c.fillText("a = 22a'/(22−b')",fx+67,fy+47);
  c.textAlign='left'; c.restore();

  // Arrow: A' → A
  c.save();
  c.strokeStyle='#7dd3fc'; c.lineWidth=2; c.fillStyle='#7dd3fc';
  const asx=XScr+22, asy=(Y_GND+YAp)/2, aex=XA-16, aey=Y_GND-8;
  c.beginPath(); c.moveTo(asx,asy); c.bezierCurveTo(asx+30,asy-20,aex-30,aey+10,aex,aey); c.stroke();
  const ang2=Math.atan2(aey-(asy-20+aey+10)/2,aex-(asx+30+aex-30)/2);
  c.beginPath(); c.moveTo(aex,aey);
  c.lineTo(aex-9*Math.cos(ang2-0.5),aey-9*Math.sin(ang2-0.5));
  c.lineTo(aex-9*Math.cos(ang2+0.5),aey-9*Math.sin(ang2+0.5));
  c.closePath(); c.fill();
  c.fillStyle='#7dd3fc'; c.font='bold 10px sans-serif'; c.textAlign='center';
  c.fillText('역산',( asx+aex)/2,(asy+aey)/2-8);
  c.textAlign='left'; c.restore();
}

function renderDiagrams() {
  drawDiagSetup();
  drawDiag4b();
  drawDiag4a();
  drawDiag5();
}

function renderAll() {
  drawSide();
  drawTop();
  updateCoords();
  renderDiagrams();
}

/* ── Slider handlers ── */
slA.addEventListener('input', () => {
  a = +slA.value;
  document.getElementById('valA').textContent = a;
  renderAll();
});
slB.addEventListener('input', () => {
  b = +slB.value;
  document.getElementById('valB').textContent = b;
  renderAll();
});

/* ── Tabs ── */
const tabIds = ['Sim','Ex4','Ex5','Arno'];
tabIds.forEach(id => {
  document.getElementById('tab'+id).addEventListener('click', () => {
    tabIds.forEach(t => {
      document.getElementById('tab'+t).classList.toggle('active', t === id);
      document.getElementById('panel-'+t.toLowerCase()).classList.toggle('show', t === id);
    });
    setTimeout(renderAll, 60);
  });
});

/* ── ResizeObserver ── */
const ro = new ResizeObserver(() => renderAll());
ro.observe(document.getElementById('app'));

/* ══════════════════════════════
   QUIZ — Tab 4
══════════════════════════════ */
let q4 = { a: 0, b: 0 };

function newQuiz4() {
  q4.a = Math.floor(Math.random() * 80 - 40);
  q4.b = Math.floor(Math.random() * 60 + 10);
  document.getElementById('qa').textContent = q4.a;
  document.getElementById('qb').textContent = q4.b;
  document.getElementById('ans-ap').value = '';
  document.getElementById('ans-bp').value = '';
  const fb = document.getElementById('fb4');
  fb.className = 'quiz-feedback'; fb.textContent = '';
}
newQuiz4();

document.getElementById('newQ4').addEventListener('click', newQuiz4);
document.getElementById('checkBtn4').addEventListener('click', () => {
  const { ap, bp } = project(q4.a, q4.b);
  const userAp = parseFloat(document.getElementById('ans-ap').value);
  const userBp = parseFloat(document.getElementById('ans-bp').value);
  const fb = document.getElementById('fb4');
  if (isNaN(userAp) || isNaN(userBp)) {
    fb.className = 'quiz-feedback wrong';
    fb.textContent = '숫자를 입력하세요!'; return;
  }
  const ok = Math.abs(userAp - ap) < 0.1 && Math.abs(userBp - bp) < 0.1;
  if (ok) {
    fb.className = 'quiz-feedback correct';
    fb.textContent = `✅ 정답! a′ = ${ap.toFixed(2)}, b′ = ${bp.toFixed(2)}`;
  } else {
    fb.className = 'quiz-feedback wrong';
    fb.textContent = `❌ 다시 도전! 공식: a′ = 28a/(b+28), b′ = 22b/(b+28)\n정답: a′ ≈ ${ap.toFixed(2)}, b′ ≈ ${bp.toFixed(2)}`;
  }
});

/* ══════════════════════════════
   QUIZ — Tab 5 & Live Calc
══════════════════════════════ */
let q5 = { ap: 0, bp: 0 };

function newQuiz5() {
  // generate from valid real coords
  const ra = Math.floor(Math.random() * 80 - 40);
  const rb = Math.floor(Math.random() * 60 + 10);
  const { ap, bp } = project(ra, rb);
  q5.ap = Math.round(ap * 10) / 10;
  q5.bp = Math.round(bp * 10) / 10;
  document.getElementById('qa2').textContent = q5.ap.toFixed(1);
  document.getElementById('qb2').textContent = q5.bp.toFixed(1);
  document.getElementById('ans-a2').value = '';
  document.getElementById('ans-b2').value = '';
  const fb = document.getElementById('fb5');
  fb.className = 'quiz-feedback'; fb.textContent = '';
}
newQuiz5();

document.getElementById('newQ5').addEventListener('click', newQuiz5);
document.getElementById('checkBtn5').addEventListener('click', () => {
  const res = inverse(q5.ap, q5.bp);
  if (!res) return;
  const userA = parseFloat(document.getElementById('ans-a2').value);
  const userB = parseFloat(document.getElementById('ans-b2').value);
  const fb = document.getElementById('fb5');
  if (isNaN(userA) || isNaN(userB)) {
    fb.className = 'quiz-feedback wrong';
    fb.textContent = '숫자를 입력하세요!'; return;
  }
  const ok = Math.abs(userA - res.a) < 0.2 && Math.abs(userB - res.b) < 0.2;
  if (ok) {
    fb.className = 'quiz-feedback correct';
    fb.textContent = `✅ 정답! a = ${res.a.toFixed(2)}, b = ${res.b.toFixed(2)}`;
  } else {
    fb.className = 'quiz-feedback wrong';
    fb.textContent = `❌ 다시 도전! 공식: a = 22a′/(22-b′), b = 28b′/(22-b′)\n정답: a ≈ ${res.a.toFixed(2)}, b ≈ ${res.b.toFixed(2)}`;
  }
});

function updateCalc() {
  const ap = parseFloat(document.getElementById('inp-ap').value);
  const bp = parseFloat(document.getElementById('inp-bp').value);
  const out = document.getElementById('calc-out');
  if (isNaN(ap) || isNaN(bp)) { out.textContent = '값을 입력하세요.'; return; }
  if (bp >= 22) { out.innerHTML = '<span style="color:#f87171">b′는 22보다 작아야 합니다! (b′ ≥ 22이면 b → ∞)</span>'; return; }
  const res = inverse(ap, bp);
  if (!res) { out.textContent = '계산 불가'; return; }
  out.innerHTML =
    `a′ = <b>${ap}</b>, b′ = <b>${bp}</b> 일 때,<br>` +
    `실제 a = <b>${res.a.toFixed(3)}</b>,&nbsp; b = <b>${res.b.toFixed(3)}</b><br>` +
    `<span style="color:#64748b;font-size:.76rem">검증: 다시 투영하면 a′≈${project(res.a,res.b).ap.toFixed(2)}, b′≈${project(res.a,res.b).bp.toFixed(2)}</span>`;
}

document.getElementById('inp-ap').addEventListener('input', updateCalc);
document.getElementById('inp-bp').addEventListener('input', updateCalc);
updateCalc();

/* ── Initial render ── */
renderAll();

/* ════════════════════════════════════════════════════════
   ARNOLFINI TAB  — 4단계 활동 + 인터랙티브 3D
════════════════════════════════════════════════════════ */
(function() {
'use strict';

/* ── 상수 ── */
const PAINT_W_CM  = 60.0;
const PAINT_H_CM  = 82.2;
const PAINT_FLOOR = 82.2;      // 그림 아랫단 바닥 높이 (cm)
const H_EYE       = 77.8;      // 눈 높이 (그림 아랫단 기준)
const D_EYE       = 150.0;     // 그림까지 수평 거리
const OBS_EYE_Z   = PAINT_FLOOR + H_EYE;  // = 160 (바닥 기준 눈 높이)
const OBS_HEIGHT  = 170.0;

/* ── 단계 진행 (4단계) ── */
function goToStep(n) {
  for (let i = 1; i <= 4; i++) {
    document.getElementById('arnoSec' + i).classList.toggle('show', i <= n);
  }
  for (let i = 1; i <= 4; i++) {
    const dot  = document.getElementById('asbDot' + i);
    const line = i < 4 ? document.getElementById('asbLine' + i) : null;
    dot.classList.remove('active', 'done');
    if (i < n)        { dot.classList.add('done');   dot.textContent = '✓'; }
    else if (i === n) { dot.classList.add('active'); dot.textContent = String(i); }
    else                dot.textContent = String(i);
    if (line) line.classList.toggle('done', i < n);
  }
  AS.step = n;
  const sec = document.getElementById('arnoSec' + n);
  if (sec) setTimeout(() => sec.scrollIntoView({ behavior: 'smooth', block: 'start' }), 60);
  if (n >= 2) setTimeout(drawArno3D, 100);
}

/* ── 그림 캔버스 상태 ── */
const AS = {
  tool: 'mark',
  color: '#ef4444', rulerColor: '#fbbf24',
  strokes: [], rulers: [], rulerDrag: null, selectedRuler: -1,
  drawing: false, sx: 0, sy: 0,
  mark: null,
  bgImg: null,
  imgX: 0, imgY: 0, imgW: 0, imgH: 0,
  ap: null, bp: null,
  calcA: null, calcB: null,
  step: 1,
};

const cvs = document.getElementById('cvsArno');
if (!cvs) return;
const ctx = cvs.getContext('2d');

/* ── Projection helpers ── */
function cmToScreen(ax, ay) { // painting cm coords to canvas pixels
  // ax: horizontal from left in cm  ay: vertical from bottom in cm
  return {
    px: AS.imgX + (ax / PAINT_W_CM) * AS.imgW,
    py: AS.imgY + ((PAINT_H_CM - ay) / PAINT_H_CM) * AS.imgH,
  };
}
function screenToCm(px, py) { // canvas pixels to painting cm
  const ax = (px - AS.imgX) / AS.imgW * PAINT_W_CM;
  const ay = PAINT_H_CM - (py - AS.imgY) / AS.imgH * PAINT_H_CM;
  return { ax, ay };
}
function pxPerCm() { return AS.imgW / PAINT_W_CM; }

/* ── Pointer helpers ── */
function pxCoords(e) {
  const r   = cvs.getBoundingClientRect();
  const scX = cvs.width  / r.width;
  const scY = cvs.height / r.height;
  const src = e.touches ? e.touches[0] : e;
  return { x: (src.clientX - r.left) * scX, y: (src.clientY - r.top) * scY };
}
function dist2(ax,ay,bx,by){ return Math.sqrt((ax-bx)**2+(ay-by)**2); }
function distToSeg(px,py,ax,ay,bx,by){
  const dx=bx-ax,dy=by-ay,len2=dx*dx+dy*dy;
  if(len2<1) return dist2(px,py,ax,ay);
  const t=Math.max(0,Math.min(1,((px-ax)*dx+(py-ay)*dy)/len2));
  return dist2(px,py,ax+t*dx,ay+t*dy);
}

/* ── Image load ── */
const ARNO_B64 = 'PLACEHOLDER_ARNOLFINI';

/* 캔버스 레이아웃 초기화 — clientWidth가 0이면 재시도 */
function initArnoCanvas() {
  const outer = document.getElementById('arnoCvsOuter');
  if (!outer) return;
  const W = outer.clientWidth;
  if (!W) { setTimeout(initArnoCanvas, 60); return; }
  const maxW = Math.min(W, 520);
  if (AS.bgImg) {
    const sc = maxW / AS.bgImg.naturalWidth;
    AS.imgW = Math.round(AS.bgImg.naturalWidth  * sc);
    AS.imgH = Math.round(AS.bgImg.naturalHeight * sc);
  } else {
    AS.imgW = maxW;
    AS.imgH = Math.round(maxW * PAINT_H_CM / PAINT_W_CM);
  }
  AS.imgX = Math.max(0, Math.round((W - AS.imgW) / 2));
  AS.imgY = 0;
  cvs.width  = W;
  cvs.height = AS.imgH;
  cvs.style.height = AS.imgH + 'px';
  redrawArno();
}

const arnoImg = new Image();
arnoImg.onload = () => { AS.bgImg = arnoImg; initArnoCanvas(); };
if (ARNO_B64) {
  arnoImg.src = 'data:image/jpeg;base64,' + ARNO_B64;
} else {
  initArnoCanvas();
}

/* 컨테이너 크기 변경 시 캔버스 재조정 */
new ResizeObserver(() => {
  if (AS.bgImg || !ARNO_B64) initArnoCanvas();
}).observe(document.getElementById('arnoCvsOuter'));

/* ── Ruler draw ── */
function drawArnoRuler(c, r, selected) {
  const dx=r.x2-r.x1, dy=r.y2-r.y1;
  const len=Math.sqrt(dx*dx+dy*dy);
  if(len<3) return;
  const ppc = pxPerCm();
  const lenCm = len / ppc;
  const angle=Math.atan2(dy,dx);
  const col = r.color||'#fbbf24';
  c.save(); c.translate(r.x1,r.y1); c.rotate(angle);
  c.shadowColor='rgba(0,0,0,0.8)'; c.shadowBlur=4;
  c.strokeStyle='rgba(0,0,0,0.6)'; c.lineWidth=6; c.lineCap='square';
  c.beginPath(); c.moveTo(0,0); c.lineTo(len,0); c.stroke();
  c.strokeStyle=col; c.lineWidth=3;
  c.beginPath(); c.moveTo(0,0); c.lineTo(len,0); c.stroke();
  [0,len].forEach(tx => {
    c.strokeStyle='rgba(0,0,0,0.6)'; c.lineWidth=4;
    c.beginPath(); c.moveTo(tx,-11); c.lineTo(tx,11); c.stroke();
    c.strokeStyle=col; c.lineWidth=2;
    c.beginPath(); c.moveTo(tx,-11); c.lineTo(tx,11); c.stroke();
  });
  c.shadowBlur=0;
  const tickCm = lenCm>20?5:lenCm>8?2:1;
  for(let t=0; t<=lenCm+0.01; t+=tickCm) {
    const tx2 = t * ppc;
    const h2 = t % (tickCm*2)===0 ? 8 : 5;
    c.strokeStyle=col; c.lineWidth=1.2;
    c.beginPath(); c.moveTo(tx2,0); c.lineTo(tx2,h2); c.stroke();
  }
  c.save();
  const flip = Math.abs(angle) > Math.PI/2;
  c.translate(len/2,0); if(flip) c.rotate(Math.PI);
  const label = lenCm.toFixed(1)+' cm';
  c.font='bold 13px sans-serif';
  const tw=c.measureText(label).width;
  c.fillStyle='rgba(0,0,0,0.75)';
  c.beginPath(); c.roundRect(-tw/2-5,-28,tw+10,18,4); c.fill();
  c.fillStyle=col; c.textAlign='center'; c.textBaseline='alphabetic';
  c.fillText(label,0,-13); c.restore(); c.restore();
  [[r.x1,r.y1],[r.x2,r.y2]].forEach(([x,y])=>{
    c.beginPath(); c.arc(x,y,8,0,Math.PI*2);
    c.fillStyle='rgba(0,0,0,0.5)'; c.fill();
    c.beginPath(); c.arc(x,y,6,0,Math.PI*2);
    c.fillStyle=selected?'#f97316':col; c.fill();
    c.beginPath(); c.arc(x,y,6,0,Math.PI*2);
    c.strokeStyle='#f8fafc'; c.lineWidth=1.2; c.stroke();
  });
}

/* ── Main redraw ── */
function redrawArno(previewStroke, previewRuler) {
  ctx.clearRect(0,0,cvs.width,cvs.height);
  ctx.fillStyle='#0a0f1a'; ctx.fillRect(0,0,cvs.width,cvs.height);

  if(AS.bgImg) {
    ctx.drawImage(AS.bgImg, AS.imgX, AS.imgY, AS.imgW, AS.imgH);
  } else {
    ctx.fillStyle='#1e293b'; ctx.fillRect(AS.imgX, AS.imgY, AS.imgW, AS.imgH);
    ctx.fillStyle='#475569'; ctx.font='bold 14px sans-serif'; ctx.textAlign='center';
    ctx.fillText('아르놀피니 그림 로드 중...', AS.imgX+AS.imgW/2, AS.imgY+AS.imgH/2);
    ctx.textAlign='left';
  }

  // Painting border
  ctx.strokeStyle='#334155'; ctx.lineWidth=1; ctx.setLineDash([4,4]);
  ctx.strokeRect(AS.imgX,AS.imgY,AS.imgW,AS.imgH); ctx.setLineDash([]);

  // Coordinate axes overlay
  const ppc = pxPerCm();
  // Y-axis (center vertical)
  const cx = AS.imgX + AS.imgW/2;
  ctx.strokeStyle='rgba(250,204,21,0.55)'; ctx.lineWidth=1.5; ctx.setLineDash([5,4]);
  ctx.beginPath(); ctx.moveTo(cx, AS.imgY+4); ctx.lineTo(cx, AS.imgY+AS.imgH-4); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='rgba(250,204,21,0.8)'; ctx.font='bold 10px sans-serif';
  ctx.textAlign='center'; ctx.fillText('x축(a방향)', cx, AS.imgY+12); ctx.textAlign='left';
  // X-axis (bottom)
  const by = AS.imgY + AS.imgH;
  ctx.strokeStyle='rgba(74,222,128,0.55)'; ctx.lineWidth=1.5; ctx.setLineDash([5,4]);
  ctx.beginPath(); ctx.moveTo(AS.imgX+4,by-4); ctx.lineTo(AS.imgX+AS.imgW-4,by-4); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='rgba(74,222,128,0.8)'; ctx.font='bold 10px sans-serif';
  ctx.fillText('y축(b방향)→아랫단', AS.imgX+4, by-7);

  // Strokes
  AS.strokes.forEach(st => {
    if(!st.pts||st.pts.length<2) return;
    ctx.save();
    ctx.strokeStyle=st.color; ctx.lineWidth=st.thick||2;
    ctx.lineCap='round'; ctx.lineJoin='round';
    ctx.beginPath();
    if(st.type==='line'){ ctx.moveTo(st.pts[0].x,st.pts[0].y); ctx.lineTo(st.pts[st.pts.length-1].x,st.pts[st.pts.length-1].y); }
    else { ctx.moveTo(st.pts[0].x,st.pts[0].y); st.pts.slice(1).forEach(p=>ctx.lineTo(p.x,p.y)); }
    ctx.stroke(); ctx.restore();
  });
  if(previewStroke && previewStroke.pts && previewStroke.pts.length>=2) {
    ctx.save(); ctx.globalAlpha=0.7;
    ctx.strokeStyle=previewStroke.color; ctx.lineWidth=previewStroke.thick||2;
    ctx.lineCap='round'; ctx.beginPath();
    ctx.moveTo(previewStroke.pts[0].x,previewStroke.pts[0].y);
    ctx.lineTo(previewStroke.pts[previewStroke.pts.length-1].x,previewStroke.pts[previewStroke.pts.length-1].y);
    ctx.stroke(); ctx.globalAlpha=1; ctx.restore();
  }

  // Rulers
  AS.rulers.forEach((r,i)=>drawArnoRuler(ctx,r,i===AS.selectedRuler));
  if(previewRuler){ ctx.globalAlpha=0.8; drawArnoRuler(ctx,previewRuler,false); ctx.globalAlpha=1; }

  // Marked foot point
  if(AS.mark) {
    const mx=AS.mark.x, my=AS.mark.y;
    // crosshair lines
    ctx.save();
    ctx.strokeStyle='rgba(167,139,250,0.7)'; ctx.lineWidth=1; ctx.setLineDash([4,3]);
    ctx.beginPath(); ctx.moveTo(mx, AS.imgY); ctx.lineTo(mx, AS.imgY+AS.imgH); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(AS.imgX, my); ctx.lineTo(AS.imgX+AS.imgW, my); ctx.stroke();
    ctx.setLineDash([]);
    // a' bracket (horizontal from center to mark)
    ctx.strokeStyle='#f59e0b'; ctx.lineWidth=2;
    ctx.beginPath(); ctx.moveTo(cx, my+12); ctx.lineTo(mx, my+12); ctx.stroke();
    // b' bracket (vertical from bottom to mark)
    ctx.strokeStyle='#4ade80'; ctx.lineWidth=2;
    ctx.beginPath(); ctx.moveTo(mx+12, by-4); ctx.lineTo(mx+12, my); ctx.stroke();
    ctx.restore();
    // dot
    ctx.save(); ctx.shadowColor='#a78bfa'; ctx.shadowBlur=16;
    ctx.fillStyle='#a78bfa'; ctx.beginPath(); ctx.arc(mx,my,9,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#fff'; ctx.shadowBlur=0; ctx.beginPath(); ctx.arc(mx,my,4,0,Math.PI*2); ctx.fill();
    ctx.restore();
    // labels
    if(AS.ap!==null && AS.bp!==null) {
      ctx.save();
      ctx.fillStyle='#f59e0b'; ctx.font='bold 12px sans-serif';
      ctx.fillText("a'="+AS.ap.toFixed(1)+'cm', Math.min(cx,mx)+4, my+25);
      ctx.fillStyle='#4ade80';
      ctx.fillText("b'="+AS.bp.toFixed(1)+'cm', mx+16, (my+by)/2);
      ctx.restore();
    }
  }
}

/* ── Ruler hit test ── */
function hitArnoRuler(x,y){
  for(let i=AS.rulers.length-1;i>=0;i--){
    const r=AS.rulers[i];
    if(dist2(x,y,r.x1,r.y1)<10) return {idx:i,type:'ep1'};
    if(dist2(x,y,r.x2,r.y2)<10) return {idx:i,type:'ep2'};
    if(distToSeg(x,y,r.x1,r.y1,r.x2,r.y2)<8) return {idx:i,type:'body'};
  }
  return null;
}

/* ── Pointer events ── */
cvs.addEventListener('pointerdown', e=>{
  e.preventDefault();
  const {x,y}=pxCoords(e);
  if(AS.tool==='mark'){
    if(x>=AS.imgX&&x<=AS.imgX+AS.imgW&&y>=AS.imgY&&y<=AS.imgY+AS.imgH){
      AS.mark={x,y};
      const {ax,ay}=screenToCm(x,y);
      AS.ap = Math.abs(ax - PAINT_W_CM/2);
      AS.bp = Math.max(0, ay);
      document.getElementById('cbAp').textContent = AS.ap.toFixed(2)+' cm';
      document.getElementById('cbBp').textContent = AS.bp.toFixed(2)+' cm';
      document.getElementById('arnoInpAp').value = AS.ap.toFixed(2);
      document.getElementById('arnoInpBp').value = AS.bp.toFixed(2);
      const nb = document.getElementById('arnoNext1Btn');
      nb.classList.add('ready');
      nb.textContent = '측정 완료 ✓  →  STEP 2: 3D 갤러리 장면 보기';
      redrawArno();
    }
    return;
  }
  if(AS.tool==='ruler'){
    const hit=hitArnoRuler(x,y);
    if(hit){
      AS.selectedRuler=hit.idx;
      const r=AS.rulers[hit.idx];
      AS.rulerDrag={type:hit.type,idx:hit.idx,ox:x,oy:y,ox1:r.x1,oy1:r.y1,ox2:r.x2,oy2:r.y2};
    } else {
      AS.selectedRuler=-1;
      AS.rulerDrag={type:'new',x1:x,y1:y};
    }
    cvs.setPointerCapture(e.pointerId); redrawArno(); return;
  }
  AS.selectedRuler=-1; AS.drawing=true; AS.sx=x; AS.sy=y;
  if(AS.tool==='eraser'&&AS.strokes.length){AS.strokes.pop();redrawArno();AS.drawing=false;return;}
  cvs.setPointerCapture(e.pointerId);
});

cvs.addEventListener('pointermove', e=>{
  const {x,y}=pxCoords(e);
  if(AS.tool==='ruler'){
    if(AS.rulerDrag){
      const d=AS.rulerDrag;
      if(d.type==='new'){
        redrawArno(null,{x1:d.x1,y1:d.y1,x2:x,y2:y,color:AS.rulerColor});
      } else {
        const r=AS.rulers[d.idx], dx=x-d.ox, dy=y-d.oy;
        if(d.type==='ep1'){r.x1=d.ox1+dx;r.y1=d.oy1+dy;}
        else if(d.type==='ep2'){r.x2=d.ox2+dx;r.y2=d.oy2+dy;}
        else{r.x1=d.ox1+dx;r.y1=d.oy1+dy;r.x2=d.ox2+dx;r.y2=d.oy2+dy;}
        redrawArno();
      }
    } else {
      const hit=hitArnoRuler(x,y);
      cvs.style.cursor=hit?(hit.type.startsWith('ep')?'grab':'move'):'crosshair';
    }
    return;
  }
  if(!AS.drawing) return; e.preventDefault();
  if(AS.tool==='line')
    redrawArno({type:'line',color:AS.color,thick:2,pts:[{x:AS.sx,y:AS.sy},{x,y}]});
});

cvs.addEventListener('pointerup', e=>{
  const {x,y}=pxCoords(e);
  if(AS.tool==='ruler'){
    if(AS.rulerDrag){
      const d=AS.rulerDrag;
      if(d.type==='new'&&dist2(d.x1,d.y1,x,y)>10)
        AS.rulers.push({x1:d.x1,y1:d.y1,x2:x,y2:y,color:AS.rulerColor});
      AS.rulerDrag=null; redrawArno();
    }
    return;
  }
  if(!AS.drawing) return; AS.drawing=false;
  if(AS.tool==='line'){
    const dx=x-AS.sx,dy=y-AS.sy;
    if(dx*dx+dy*dy>25)
      AS.strokes.push({type:'line',color:AS.color,thick:2,pts:[{x:AS.sx,y:AS.sy},{x,y}]});
    redrawArno();
  }
});

cvs.addEventListener('contextmenu', e=>{
  e.preventDefault();
  const {x,y}=pxCoords(e);
  const hit=hitArnoRuler(x,y);
  if(hit){ AS.rulers.splice(hit.idx,1); AS.selectedRuler=-1; redrawArno(); }
});

/* ── 도구 버튼 ── */
function setArnoTool(t) {
  AS.tool = t;
  const map = {line:'arnoBtnLine', ruler:'arnoBtnRuler', mark:'arnoBtnMark'};
  Object.entries(map).forEach(([name, id]) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.remove('active', 'mark-on');
    if (name === t) el.classList.add(t === 'mark' ? 'mark-on' : 'active');
  });
  cvs.style.cursor = 'crosshair';
  document.getElementById('arnoRulerTip').style.display = t === 'ruler' ? 'block' : 'none';
  document.getElementById('arnoMarkTip').style.display  = t === 'mark'  ? 'block' : 'none';
}
document.getElementById('arnoBtnLine').addEventListener('click',  () => setArnoTool('line'));
document.getElementById('arnoBtnRuler').addEventListener('click', () => setArnoTool('ruler'));
document.getElementById('arnoBtnMark').addEventListener('click',  () => setArnoTool('mark'));
document.getElementById('arnoBtnUndo').addEventListener('click', () => {
  if (AS.tool === 'ruler' && AS.rulers.length) { AS.rulers.pop(); AS.selectedRuler = -1; }
  else if (AS.strokes.length) AS.strokes.pop();
  redrawArno();
});
document.getElementById('arnoBtnClear').addEventListener('click', () => {
  AS.strokes = []; AS.rulers = []; AS.selectedRuler = -1; AS.mark = null;
  AS.ap = null; AS.bp = null; AS.calcA = null; AS.calcB = null;
  document.getElementById('cbAp').textContent = '— 발을 클릭하세요';
  document.getElementById('cbBp').textContent = '— 발을 클릭하세요';
  const res = document.getElementById('arnoResult');
  if (res) res.style.display = 'none';
  const nb = document.getElementById('arnoNext1Btn');
  nb.classList.remove('ready');
  nb.textContent = '발 위치를 먼저 표시하세요 (📍 클릭 후 활성화)';
  redrawArno();
  if (AS.step >= 2) drawArno3D();
});
document.querySelectorAll('.acswatch').forEach(el => {
  el.addEventListener('click', () => {
    document.querySelectorAll('.acswatch').forEach(s => s.classList.remove('active'));
    el.classList.add('active');
    AS.color = el.dataset.ac;
    AS.rulerColor = el.dataset.ac;
  });
});

/* ── 단계 이동 버튼 ── */
document.getElementById('arnoNext1Btn').addEventListener('click', () => {
  if (document.getElementById('arnoNext1Btn').classList.contains('ready')) goToStep(2);
});
document.getElementById('arnoNext2Btn').addEventListener('click', () => goToStep(3));
document.getElementById('arnoNext3Btn').addEventListener('click', () => {
  goToStep(4);
  if (AS.ap !== null) document.getElementById('arnoInpAp').value = AS.ap.toFixed(2);
  if (AS.bp !== null) document.getElementById('arnoInpBp').value = AS.bp.toFixed(2);
});

/* ── 탭 전환 시 3D 렌더 ── */
document.getElementById('tabArno').addEventListener('click', () => {
  if (AS.step >= 2) setTimeout(drawArno3D, 80);
});

/* ════════════════════════════════════════════════════════
   인터랙티브 3D 시각화
════════════════════════════════════════════════════════ */
const cvs3D = document.getElementById('cvsArno3D');
const ctx3D = cvs3D.getContext('2d');

/* 3D 뷰 상태 */
const S3D = {
  az: 0.50, el: 0.30, zoom: 2.4,
  drag: false, lx: 0, ly: 0,
  pinch: null,
};
const AZ0 = 0.50, EL0 = 0.30, ZM0 = 2.4;

/* 3D 좌표(a=좌우, b=깊이, z=높이) → 화면 좌표 (직교 투영 + 회전) */
function p3(a_cm, b_cm, z_cm, W, H) {
  const ca = Math.cos(S3D.az), sa = Math.sin(S3D.az);
  const rx = a_cm * ca - b_cm * sa;
  const ry = a_cm * sa + b_cm * ca;
  const ce = Math.cos(S3D.el), se = Math.sin(S3D.el);
  const rz = z_cm * ce + ry * se;
  return {
    x: W * 0.44 + rx * S3D.zoom,
    y: H * 0.70 - rz * S3D.zoom,
  };
}

function drawArno3D() {
  const outer = cvs3D.parentElement;
  if (!outer || !outer.clientWidth) return;
  const W = outer.clientWidth;
  const H = Math.max(320, Math.round(W * 0.58));
  const dpr = window.devicePixelRatio || 1;
  cvs3D.width = W * dpr; cvs3D.height = H * dpr;
  cvs3D.style.height = H + 'px';
  ctx3D.setTransform(dpr, 0, 0, dpr, 0, 0);
  const c = ctx3D;
  const step = AS.step;
  const pw = PAINT_W_CM / 2;  // 30 cm

  c.fillStyle = '#060f1e'; c.fillRect(0, 0, W, H);

  /* ── 선/점 헬퍼 ── */
  function seg(ax,ab,az, bx,bb,bz, col, lw, dash) {
    const p = p3(ax,ab,az,W,H), q = p3(bx,bb,bz,W,H);
    c.save(); c.strokeStyle=col; c.lineWidth=lw||1;
    if (dash) c.setLineDash(dash);
    c.beginPath(); c.moveTo(p.x,p.y); c.lineTo(q.x,q.y); c.stroke();
    c.setLineDash([]); c.restore();
  }
  function dot(ax,ab,az, col, r, lbl, lo) {
    const p = p3(ax,ab,az,W,H);
    c.save(); c.shadowColor=col; c.shadowBlur=12;
    c.fillStyle=col; c.beginPath(); c.arc(p.x,p.y,r,0,Math.PI*2); c.fill();
    c.fillStyle='#fff'; c.shadowBlur=0; c.beginPath(); c.arc(p.x,p.y,r*0.38,0,Math.PI*2); c.fill();
    if (lbl) { c.fillStyle=col; c.font='bold 10px sans-serif'; c.fillText(lbl,p.x+(lo?lo[0]:9),p.y+(lo?lo[1]:-5)); }
    c.restore();
  }

  /* ── 바닥 그리드 (z=0) ── */
  c.save();
  const gPts = [p3(-70,-D_EYE*1.1,0,W,H), p3(70,-D_EYE*1.1,0,W,H),
                p3(70,100,0,W,H), p3(-70,100,0,W,H)];
  c.fillStyle='rgba(14,116,144,0.14)'; c.strokeStyle='#164e63'; c.lineWidth=0.5;
  c.beginPath(); c.moveTo(gPts[0].x,gPts[0].y);
  gPts.slice(1).forEach(p=>c.lineTo(p.x,p.y));
  c.closePath(); c.fill(); c.stroke();
  for (let a=-60; a<=60; a+=20) seg(a,-D_EYE*1.1,0, a,100,0, 'rgba(14,116,144,0.25)',0.5);
  for (let b=-D_EYE*1.1; b<=100; b+=30) seg(-70,b,0, 70,b,0, 'rgba(14,116,144,0.25)',0.5);
  c.restore();

  /* ── 벽 (painting이 걸린 벽, b=0 평면) ── */
  const wallW = 95, wallTop = 215;
  const wTL = p3(-wallW, 0, wallTop, W, H), wTR = p3(wallW, 0, wallTop, W, H);
  const wBL = p3(-wallW, 0, 0,       W, H), wBR = p3(wallW, 0, 0,       W, H);
  c.save();
  c.fillStyle = 'rgba(75, 58, 44, 0.38)'; c.strokeStyle = 'rgba(100, 78, 58, 0.5)'; c.lineWidth = 1;
  c.beginPath(); c.moveTo(wTL.x,wTL.y); c.lineTo(wTR.x,wTR.y);
  c.lineTo(wBR.x,wBR.y); c.lineTo(wBL.x,wBL.y); c.closePath(); c.fill(); c.stroke();
  /* 벽 라벨 */
  const wallLbl = p3(-wallW+4, 0, wallTop-8, W, H);
  c.fillStyle='rgba(100,78,58,0.8)'; c.font='9px sans-serif'; c.fillText('벽', wallLbl.x, wallLbl.y);
  c.restore();

  /* ── 그림(painting) — 바닥에서 PAINT_FLOOR 높이에 걸림 ── */
  const pBL = p3(-pw, 0, PAINT_FLOOR,            W, H);
  const pBR = p3( pw, 0, PAINT_FLOOR,            W, H);
  const pTL = p3(-pw, 0, PAINT_FLOOR+PAINT_H_CM, W, H);
  const pTR = p3( pw, 0, PAINT_FLOOR+PAINT_H_CM, W, H);

  if (AS.bgImg) {
    /* 아핀 변환으로 그림 이미지를 평행사변형에 텍스처 매핑 */
    const iW = AS.bgImg.naturalWidth, iH = AS.bgImg.naturalHeight;
    // (0,0)→pTL, (iW,0)→pTR, (0,iH)→pBL
    const ta = (pTR.x - pTL.x) / iW, tb = (pTR.y - pTL.y) / iW;
    const tc = (pBL.x - pTL.x) / iH, td = (pBL.y - pTL.y) / iH;
    c.save();
    c.globalAlpha = 0.90;
    c.transform(ta, tb, tc, td, pTL.x, pTL.y);
    c.drawImage(AS.bgImg, 0, 0, iW, iH);
    c.restore();
  } else {
    c.save();
    c.fillStyle='rgba(120,80,50,0.45)';
    c.beginPath(); c.moveTo(pTL.x,pTL.y); c.lineTo(pTR.x,pTR.y);
    c.lineTo(pBR.x,pBR.y); c.lineTo(pBL.x,pBL.y); c.closePath(); c.fill();
    c.restore();
  }
  /* 액자 테두리 */
  c.save(); c.strokeStyle='#7c3aed'; c.lineWidth=2.5;
  c.beginPath(); c.moveTo(pTL.x,pTL.y); c.lineTo(pTR.x,pTR.y);
  c.lineTo(pBR.x,pBR.y); c.lineTo(pBL.x,pBL.y); c.closePath(); c.stroke();
  c.restore();
  /* 그림 중심 세로선 */
  seg(0, 0, PAINT_FLOOR, 0, 0, PAINT_FLOOR+PAINT_H_CM, 'rgba(250,204,21,0.45)', 1, [4,3]);
  /* 제목 */
  const topCtr = p3(0, 0, PAINT_FLOOR+PAINT_H_CM+6, W, H);
  c.save(); c.fillStyle='#a78bfa'; c.font='bold 10px sans-serif'; c.textAlign='center';
  c.fillText('아르놀피니 부부 (60×82.2 cm)', topCtr.x, topCtr.y); c.textAlign='left'; c.restore();

  /* ── 관찰자 (observer) ── */
  const obsB = -D_EYE;
  const obsFootP = p3(0, obsB, 0,           W, H);
  const obsEyeP  = p3(0, obsB, OBS_EYE_Z,   W, H);
  const obsHeadP = p3(0, obsB, OBS_HEIGHT,  W, H);
  c.save();
  c.fillStyle='rgba(200,70,40,0.6)';
  c.beginPath(); c.ellipse(obsFootP.x, obsFootP.y, 12, 4, 0, 0, Math.PI*2); c.fill();
  c.fillStyle='rgba(200,70,40,0.85)';
  if (obsHeadP.y < obsFootP.y) {
    const bT = obsHeadP.y + 8, bB = obsFootP.y;
    if (bB > bT) c.fillRect(obsEyeP.x - 7, bT, 14, bB - bT);
  }
  c.beginPath(); c.arc(obsHeadP.x, obsHeadP.y - 5, 8, 0, Math.PI*2);
  c.fillStyle='rgba(220,90,50,0.9)'; c.fill();
  c.fillStyle='#fff'; c.beginPath(); c.arc(obsEyeP.x+3, obsEyeP.y, 2.5, 0, Math.PI*2); c.fill();
  c.fillStyle='#fca5a5'; c.font='bold 10px sans-serif'; c.textAlign='center';
  c.fillText('관찰자 (170cm)', obsHeadP.x, obsHeadP.y - 18); c.textAlign='left';
  c.restore();

  /* ── STEP 2+: 그림 뒤 아르놀피니 유령 인물 (그림 왼쪽 = 음수 a) ── */
  if (step >= 2) {
    const gB = (AS.calcB !== null) ? AS.calcB : 35;
    const gA = (AS.calcA !== null) ? -AS.calcA : -10;  // 왼쪽(음수 a)
    const gFoot = p3(gA, gB, 0,          W, H);
    const gHead = p3(gA, gB, OBS_HEIGHT, W, H);
    c.save(); c.globalAlpha = 0.45;
    c.fillStyle = '#93c5fd';
    c.beginPath(); c.ellipse(gFoot.x, gFoot.y, 10, 3, 0, 0, Math.PI*2); c.fill();
    if (gHead.y < gFoot.y) {
      const bT = gHead.y + 8, bB = gFoot.y;
      if (bB > bT) c.fillRect(gFoot.x - 6, bT, 12, bB - bT);
    }
    c.beginPath(); c.arc(gHead.x, gHead.y - 4, 7, 0, Math.PI*2); c.fill();
    c.globalAlpha = 0.7; c.font='bold 10px sans-serif'; c.textAlign='center';
    c.fillText('Mr.아르놀피니', gHead.x, gHead.y - 16); c.textAlign='left';
    c.restore();
  }

  /* ── STEP 3+: H, D 치수 + A′ 표시 ── */
  if (step >= 3 && AS.ap !== null && AS.bp !== null) {
    const apZ = PAINT_FLOOR + AS.bp;

    /* A' 점 (그림 위, 왼쪽 = 음수 a) */
    dot(-AS.ap, 0, apZ, '#f59e0b', 8, "A′", [-36, -5]);

    /* H 치수선: 그림 아랫단 → 눈 높이 */
    const hBot = p3(-(pw+8), 0, PAINT_FLOOR,  W, H);
    const hTop = p3(-(pw+8), 0, OBS_EYE_Z,    W, H);
    c.save(); c.strokeStyle='#f87171'; c.lineWidth=2;
    c.beginPath(); c.moveTo(hBot.x, hBot.y); c.lineTo(hTop.x, hTop.y); c.stroke();
    const hMid = p3(-(pw+8), 0, (PAINT_FLOOR+OBS_EYE_Z)/2, W, H);
    c.fillStyle='#f87171'; c.font='bold 11px sans-serif'; c.textAlign='right';
    c.fillText('H=77.8cm', hMid.x-4, hMid.y+4); c.textAlign='left'; c.restore();

    /* D 치수선: 관찰자 눈 → 그림 */
    const dObs  = p3(0, obsB, OBS_EYE_Z, W, H);
    const dPnt  = p3(0, 0,    OBS_EYE_Z, W, H);
    c.save(); c.strokeStyle='#93c5fd'; c.lineWidth=2; c.setLineDash([5,3]);
    c.beginPath(); c.moveTo(dObs.x, dObs.y); c.lineTo(dPnt.x, dPnt.y); c.stroke();
    c.setLineDash([]); c.fillStyle='#93c5fd'; c.font='bold 11px sans-serif'; c.textAlign='center';
    c.fillText('D=150cm', (dObs.x+dPnt.x)/2, (dObs.y+dPnt.y)/2 - 8); c.textAlign='left'; c.restore();

    /* a′ 치수선 (그림 위 수평, 왼쪽) */
    const cx0 = p3(0,        0, apZ, W, H);
    const ap2 = p3(-AS.ap,   0, apZ, W, H);
    c.save(); c.strokeStyle='#f59e0b'; c.lineWidth=2;
    c.beginPath(); c.moveTo(cx0.x, cx0.y); c.lineTo(ap2.x, ap2.y); c.stroke();
    c.fillStyle='#f59e0b'; c.font='bold 10px sans-serif'; c.textAlign='center';
    c.fillText("a′="+AS.ap.toFixed(1)+"cm", (cx0.x+ap2.x)/2, (cx0.y+ap2.y)/2-7); c.textAlign='left'; c.restore();

    /* b′ 치수선 (그림 위 수직) */
    const bBot0 = p3(-AS.ap, 0, PAINT_FLOOR, W, H);
    const bTop0 = p3(-AS.ap, 0, apZ,         W, H);
    c.save(); c.strokeStyle='#4ade80'; c.lineWidth=2;
    c.beginPath(); c.moveTo(bBot0.x, bBot0.y); c.lineTo(bTop0.x, bTop0.y); c.stroke();
    c.fillStyle='#4ade80'; c.font='bold 10px sans-serif';
    c.fillText("b′="+AS.bp.toFixed(1)+"cm", bTop0.x-58, (bBot0.y+bTop0.y)/2); c.restore();
  }

  /* ── STEP 4+: 계산 결과 A + 치수선 ── */
  if (step >= 4 && AS.calcA !== null && AS.calcB !== null) {
    const calcA = AS.calcA, calcB = AS.calcB;

    /* A 점 (바닥, 왼쪽 = 음수 a) */
    dot(-calcA, calcB, 0, '#60a5fa', 9, 'A('+calcA.toFixed(1)+','+calcB.toFixed(1)+')', [-60,-4]);

    /* b 치수선 (그림→A, 바닥) */
    const bS=p3(-calcA,0,0,W,H), bE=p3(-calcA,calcB,0,W,H), bMd=p3(-calcA,calcB/2,0,W,H);
    c.save(); c.strokeStyle='#a78bfa'; c.lineWidth=2; c.setLineDash([4,3]);
    c.beginPath(); c.moveTo(bS.x,bS.y+10); c.lineTo(bE.x,bE.y+10); c.stroke();
    c.setLineDash([]); c.fillStyle='#a78bfa'; c.font='bold 10px sans-serif'; c.textAlign='center';
    c.fillText('b='+calcB.toFixed(1)+'cm', bMd.x, bMd.y+22); c.textAlign='left'; c.restore();

    /* a 치수선 (중심→A, 바닥) */
    const aS=p3(0,-calcA,calcB,W,H); // unused placeholder
    const aS2=p3(0,calcB,0,W,H), aE2=p3(-calcA,calcB,0,W,H), aMd2=p3(-calcA/2,calcB,0,W,H);
    c.save(); c.strokeStyle='#60a5fa'; c.lineWidth=2; c.setLineDash([4,3]);
    c.beginPath(); c.moveTo(aS2.x,aS2.y-10); c.lineTo(aE2.x,aE2.y-10); c.stroke();
    c.setLineDash([]); c.fillStyle='#60a5fa'; c.font='bold 10px sans-serif'; c.textAlign='center';
    c.fillText('a='+calcA.toFixed(1)+'cm', aMd2.x, aMd2.y-14); c.textAlign='left'; c.restore();

    /* 투영 삼각형: 눈→A' 시선 + 그림아랫단 높이의 수평 밑변 (b+D 길이) */
    const eyePt = p3(0, obsB, OBS_EYE_Z, W, H);
    const apPt  = p3(-AS.ap||0, 0, PAINT_FLOOR+(AS.bp||0), W, H); // A' on painting
    c.save(); c.strokeStyle='rgba(250,204,21,0.70)'; c.lineWidth=1.5;
    c.beginPath(); c.moveTo(eyePt.x, eyePt.y); c.lineTo(apPt.x, apPt.y); c.stroke(); c.restore();
    /* 수평 밑변: 관찰자 발 아랫단 높이 → A 아랫단 높이 (탐구활동 5 직각삼각형 아랫변) */
    const baseL = p3(-calcA, obsB,  PAINT_FLOOR, W, H);  // 관찰자 아래, 그림아랫단 높이
    const baseR = p3(-calcA, calcB, PAINT_FLOOR, W, H);  // A 위치, 그림아랫단 높이
    c.save(); c.strokeStyle='#f87171'; c.lineWidth=2; c.setLineDash([6,3]);
    c.beginPath(); c.moveTo(baseL.x, baseL.y); c.lineTo(baseR.x, baseR.y); c.stroke();
    c.setLineDash([]); c.fillStyle='#f87171'; c.font='bold 10px sans-serif'; c.textAlign='center';
    c.fillText('b+D='+(calcB+D_EYE).toFixed(1)+'cm', (baseL.x+baseR.x)/2, (baseL.y+baseR.y)/2-7);
    c.textAlign='left'; c.restore();
  }

  /* ── 범례 ── */
  c.save(); c.fillStyle='#334155'; c.font='10px sans-serif';
  c.fillText('H=77.8 cm  D=150 cm  |  드래그:회전  스크롤:확대  더블클릭:초기화', 8, 14);
  c.restore();
}

/* ── 3D 마우스/터치 인터랙션 ── */
cvs3D.addEventListener('pointerdown', e => {
  S3D.drag = true; S3D.lx = e.clientX; S3D.ly = e.clientY;
  cvs3D.classList.add('dragging');
  cvs3D.setPointerCapture(e.pointerId);
});
cvs3D.addEventListener('pointermove', e => {
  if (!S3D.drag) return;
  const dx = e.clientX - S3D.lx, dy = e.clientY - S3D.ly;
  S3D.az += dx * 0.007;
  S3D.el  = Math.max(-Math.PI/2+0.05, Math.min(Math.PI/2-0.05, S3D.el - dy * 0.007));
  S3D.lx = e.clientX; S3D.ly = e.clientY;
  drawArno3D();
});
cvs3D.addEventListener('pointerup',     () => { S3D.drag=false; cvs3D.classList.remove('dragging'); });
cvs3D.addEventListener('pointercancel', () => { S3D.drag=false; cvs3D.classList.remove('dragging'); });
cvs3D.addEventListener('wheel', e => {
  e.preventDefault();
  S3D.zoom = Math.max(0.5, Math.min(12, S3D.zoom - e.deltaY * 0.004));
  drawArno3D();
}, { passive: false });
cvs3D.addEventListener('dblclick', () => {
  S3D.az=AZ0; S3D.el=EL0; S3D.zoom=ZM0; drawArno3D();
});
cvs3D.addEventListener('touchstart', e => {
  if (e.touches.length === 2) {
    S3D.drag = false;
    const dx = e.touches[0].clientX - e.touches[1].clientX;
    const dy = e.touches[0].clientY - e.touches[1].clientY;
    S3D.pinch = Math.sqrt(dx*dx + dy*dy);
  }
}, { passive: true });
cvs3D.addEventListener('touchmove', e => {
  if (e.touches.length === 2 && S3D.pinch !== null) {
    e.preventDefault();
    const dx = e.touches[0].clientX - e.touches[1].clientX;
    const dy = e.touches[0].clientY - e.touches[1].clientY;
    const d = Math.sqrt(dx*dx + dy*dy);
    S3D.zoom = Math.max(0.5, Math.min(12, S3D.zoom * (d / S3D.pinch)));
    S3D.pinch = d;
    drawArno3D();
  }
}, { passive: false });
cvs3D.addEventListener('touchend', () => { S3D.pinch = null; }, { passive: true });

/* ── 역공식 계산기 (STEP 4) ── */
document.getElementById('arnoCalcBtn').addEventListener('click', () => {
  const ap  = parseFloat(document.getElementById('arnoInpAp').value);
  const bp  = parseFloat(document.getElementById('arnoInpBp').value);
  const res = document.getElementById('arnoResult');
  if (isNaN(ap) || isNaN(bp)) {
    res.style.display = 'block';
    res.innerHTML = '<span style="color:#f87171">a′와 b′ 값을 입력하세요.</span>';
    return;
  }
  if (bp >= H_EYE) {
    res.style.display = 'block';
    res.innerHTML = `<span style="color:#f87171">b′는 H(${H_EYE})보다 작아야 합니다.</span>`;
    return;
  }
  const b = D_EYE * bp / (H_EYE - bp);
  const a = H_EYE * ap  / (H_EYE - bp);
  AS.calcA = a; AS.calcB = b;
  AS.ap = ap; AS.bp = bp;
  drawArno3D();
  res.style.display = 'block';
  res.innerHTML =
    `<span style="color:#6ee7b7">측정값: a′ = ${ap.toFixed(2)} cm,&nbsp; b′ = ${bp.toFixed(2)} cm</span><br>` +
    `<strong>b = 150 × ${bp.toFixed(2)} / (77.8 − ${bp.toFixed(2)}) = <span class="big-ans">${b.toFixed(1)} cm</span></strong><br>` +
    `<strong>a = 77.8 × ${ap.toFixed(2)} / (77.8 − ${bp.toFixed(2)}) = <span class="big-ans">${a.toFixed(1)} cm</span></strong><br>` +
    `<span style="color:#6ee7b7">⬆ 위의 3D 장면을 확인하세요! Mr. 아르놀피니는 그림 기준 ` +
    `<b style="color:#fcd34d">뒤로 약 ${b.toFixed(1)} cm</b>, ` +
    `옆으로 <b style="color:#fcd34d">약 ${a.toFixed(1)} cm</b> 위치입니다! 🎨</span>`;
});

})(); // end Arnolfini scope

})();
</script>
</body>
</html>
"""


def _b64_arno() -> str:
    root = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "gifted_art")
    )
    with open(os.path.join(root, "Arnolfini.jpg"), "rb") as f:
        return base64.b64encode(f.read()).decode()


def render():
    st.header("📐 실제 사물과 그림 속 사물의 관계식 탐구")
    st.caption("눈의 높이 22cm, 화면까지 거리 28cm 조건에서 투영 관계식을 단계별로 탐구합니다.")

    with st.expander("💡 활동 안내", expanded=False):
        st.markdown(
            """
1. **시뮬레이션** 탭: 슬라이더로 실제 점 A(a,b)를 움직여 화면 투영점 A′(a′,b′)를 확인하세요.
2. **탐구활동 4** 탭: 닮음 삼각형을 이용해 `a′`, `b′` 공식을 단계별로 유도하고, 확인 문제를 풀어보세요.
3. **탐구활동 5** 탭: 반대로 화면 좌표 A′에서 실제 좌표 A를 역산하는 공식을 유도하고, 역공식 계산기를 사용해보세요.
4. **아르놀피니 적용** 탭: 아르놀피니 초상화에서 직접 좌표를 측정하고 실제 공간 좌표를 계산해보세요.
            """
        )

    html = _HTML.replace("PLACEHOLDER_ARNOLFINI", _b64_arno())
    components.html(html, height=4000, scrolling=True)
