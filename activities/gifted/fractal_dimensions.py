import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 프랙털 — 길이·넓이·부피와 차원 탐구",
    "description": "멩거 스펀지·코흐 곡선·칸토어 집합의 단계별 측정값을 계산하며 프랙털 차원을 탐구합니다.",
    "order": 25,
    "hidden": True,
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
/* ── 기본 ── */
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR','Segoe UI',sans-serif;background:#0f172a;color:#e2e8f0;}
#app{max-width:960px;margin:0 auto;padding:14px;}
h1{font-size:1.3rem;font-weight:800;text-align:center;color:#f8fafc;margin-bottom:3px;}
.subtitle{text-align:center;font-size:0.82rem;color:#64748b;margin-bottom:14px;}

/* ── 탭 ── */
.tabs{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:16px;}
.tab{padding:7px 15px;border-radius:20px;border:1.5px solid #334155;background:#1e293b;
  font-size:0.82rem;font-weight:700;cursor:pointer;color:#94a3b8;transition:all .15s;}
.tab.active{background:#3b82f6;color:#fff;border-color:#3b82f6;}
.tab:hover:not(.active){background:#1e3a5f;border-color:#3b82f6;color:#93c5fd;}
.pane{display:none;}.pane.active{display:block;}

/* ── 카드 ── */
.card{background:#1e293b;border:1px solid #334155;border-radius:14px;padding:16px;margin-bottom:12px;}
.card-title{font-size:1rem;font-weight:700;color:#fbbf24;margin-bottom:10px;}
.card-sub{font-size:0.8rem;color:#94a3b8;margin-bottom:8px;line-height:1.6;}

/* ── 공식 박스 ── */
.formula-box{background:#0f172a;border:1px solid #3b82f6;border-radius:10px;
  padding:10px 14px;font-size:0.82rem;color:#93c5fd;margin:8px 0;line-height:1.8;}
.formula-box .formula-title{font-size:0.75rem;color:#64748b;text-transform:uppercase;margin-bottom:4px;}
.emph{color:#fbbf24;font-weight:700;}
.emph2{color:#4ade80;font-weight:700;}
.emph3{color:#f472b6;font-weight:700;}

/* ── 단계 슬라이더 ── */
.ctrl-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px;}
.ctrl-row label{font-weight:700;font-size:0.88rem;color:#cbd5e1;white-space:nowrap;}
input[type=range]{flex:1;min-width:100px;accent-color:#3b82f6;cursor:pointer;}
.n-badge{background:#3b82f6;color:#fff;font-weight:800;font-size:1.1rem;
  padding:4px 14px;border-radius:8px;min-width:42px;text-align:center;}

/* ── 결과 표 ── */
.res-table{width:100%;border-collapse:collapse;font-size:0.8rem;margin-top:6px;}
.res-table th{background:#0f172a;color:#94a3b8;padding:7px 10px;text-align:center;
  font-weight:700;border-bottom:1px solid #334155;}
.res-table td{padding:7px 10px;text-align:center;border-bottom:1px solid #1e293b;}
.res-table tr.highlight td{background:#172554;color:#93c5fd;}
.res-table .lbl{text-align:left;color:#94a3b8;}
.val-blue{color:#60a5fa;font-weight:700;}
.val-green{color:#4ade80;font-weight:700;}
.val-red{color:#f87171;font-weight:700;}
.val-yellow{color:#fbbf24;font-weight:700;}

/* ── 두 플렉스 ── */
.two-col{display:flex;gap:12px;flex-wrap:wrap;}
.two-col > *{flex:1;min-width:260px;}

/* ── 캔버스 ── */
canvas{display:block;border-radius:10px;border:1px solid #334155;width:100%;}
.canvas-wrap{position:relative;}
.canvas-label{text-align:center;font-size:0.75rem;color:#64748b;margin-top:4px;}

/* ── 버튼 ── */
.btn{display:inline-block;padding:7px 16px;border-radius:10px;border:none;
  font-size:0.82rem;font-weight:700;cursor:pointer;transition:all .15s;}
.btn:active{transform:scale(.96);}
.btn-blue{background:#3b82f6;color:#fff;}.btn-blue:hover{background:#2563eb;}
.btn-green{background:#22c55e;color:#fff;}.btn-green:hover{background:#16a34a;}
.btn-gray{background:#334155;color:#cbd5e1;}.btn-gray:hover{background:#475569;}

/* ── 차원 시각화 ── */
.dim-card{background:linear-gradient(135deg,#1a1a2e,#16213e);
  border:1.5px solid #4f46e5;border-radius:14px;padding:16px;margin-bottom:12px;}
.dim-title{font-size:0.95rem;font-weight:800;color:#a78bfa;margin-bottom:8px;}
.big-eq{font-size:1.6rem;font-weight:900;text-align:center;color:#f8fafc;
  padding:12px;background:#0f0f23;border-radius:10px;letter-spacing:1px;margin:10px 0;}
.big-eq .frac{display:inline-flex;flex-direction:column;align-items:center;
  font-size:1rem;vertical-align:middle;margin:0 4px;}
.big-eq .frac span{border-top:2px solid #fff;padding:1px 4px;}
.big-eq .frac span:first-child{border-top:none;border-bottom:2px solid #fff;}
.dim-value{font-size:2.2rem;font-weight:900;text-align:center;color:#a78bfa;margin:8px 0;}
.dim-compare{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-top:8px;}
.dim-pil{background:#0f172a;border-radius:8px;padding:8px 14px;text-align:center;
  border:1px solid #334155;font-size:0.8rem;}
.dim-pil .dp-num{font-size:1.3rem;font-weight:800;margin:3px 0;}
.dim-pil .dp-lbl{font-size:0.7rem;color:#64748b;}

/* ── 퀴즈 ── */
.quiz-box{background:#1e293b;border:1px solid #334155;border-radius:14px;padding:16px;margin-bottom:12px;}
.quiz-q{font-weight:700;font-size:0.9rem;color:#f8fafc;margin-bottom:10px;line-height:1.6;}
.quiz-opts{display:flex;flex-direction:column;gap:6px;margin-bottom:10px;}
.quiz-opt{padding:9px 14px;border-radius:10px;border:1.5px solid #334155;
  background:#0f172a;color:#94a3b8;cursor:pointer;font-size:0.82rem;transition:all .15s;}
.quiz-opt:hover:not(.answered){background:#1e3a5f;border-color:#3b82f6;color:#93c5fd;}
.quiz-opt.correct{background:#14532d;border-color:#22c55e;color:#86efac;}
.quiz-opt.wrong{background:#450a0a;border-color:#ef4444;color:#fca5a5;}
.quiz-opt.reveal{background:#14532d;border-color:#22c55e;color:#86efac;}
.quiz-feedback{font-size:0.82rem;padding:8px 12px;border-radius:8px;display:none;}
.quiz-feedback.show{display:block;}
.quiz-feedback.ok{background:#14532d;color:#86efac;}
.quiz-feedback.ng{background:#450a0a;color:#fca5a5;}

/* ── 수렴/발산 배지 ── */
.badge{display:inline-block;padding:3px 12px;border-radius:20px;font-size:0.75rem;font-weight:700;}
.badge-conv{background:#166534;color:#86efac;}
.badge-div{background:#7f1d1d;color:#fca5a5;}
.badge-gray{background:#1e293b;color:#94a3b8;}

/* ── progress bar ── */
.progress-wrap{background:#0f172a;border-radius:8px;height:10px;overflow:hidden;margin:4px 0;}
.progress-bar{height:10px;border-radius:8px;transition:width .3s;}

/* ── 반응형 ── */
@media(max-width:580px){
  h1{font-size:1.1rem;}
  .big-eq{font-size:1.2rem;}
  .dim-value{font-size:1.6rem;}
}
</style>
</head>
<body>
<div id="app">
  <h1>🔬 프랙털 — 길이·넓이·부피와 차원 탐구</h1>
  <p class="subtitle">멩거 스펀지 · 코흐 곡선 · 칸토어 집합을 단계별로 탐구하고 프랙털 차원을 발견해 보자</p>

  <!-- 탭 -->
  <div class="tabs">
    <button class="tab active" onclick="switchTab('menger')">🧊 멩거 스펀지</button>
    <button class="tab" onclick="switchTab('koch')">❄️ 코흐 곡선</button>
    <button class="tab" onclick="switchTab('cantor')">📏 칸토어 집합</button>
    <button class="tab" onclick="switchTab('dimension')">🔢 프랙털 차원</button>
  </div>

  <!-- ════════════════ 멩거 스펀지 ════════════════ -->
  <div id="pane-menger" class="pane active">

    <div class="card">
      <div class="card-title">🧊 멩거 스펀지란?</div>
      <div class="card-sub">
        정육면체를 27개의 작은 정육면체로 나누고,<br>
        <b>중앙 1개</b>와 <b>각 면의 가운데 6개</b>를 제거합니다. → 20개 남음<br>
        이 과정을 각각의 작은 정육면체에 반복하면 멩거 스펀지가 만들어집니다.
      </div>
      <div class="formula-box">
        <div class="formula-title">핵심 규칙</div>
        27개 중 7개 제거 → <span class="emph">20개 유지</span><br>
        한 변의 길이 비율: 1 → 1/3 (3분의 1로 축소)<br>
        n단계 정육면체 수: <span class="emph">20ⁿ</span><br>
        작은 정육면체 한 변 길이: <span class="emph">(1/3)ⁿ</span>
      </div>
    </div>

    <div class="card">
      <div class="card-title">📊 단계별 계산</div>
      <div class="ctrl-row">
        <label>단계 n =</label>
        <input type="range" id="menger-n" min="0" max="5" value="0" oninput="updateMenger(this.value)">
        <div class="n-badge" id="menger-n-badge">0</div>
      </div>

      <div class="two-col">
        <div>
          <div class="res-table" style="overflow-x:auto">
            <table class="res-table" id="menger-table">
              <thead>
                <tr>
                  <th>단계</th>
                  <th>정육면체 수</th>
                  <th>겉넓이</th>
                  <th>부피</th>
                </tr>
              </thead>
              <tbody id="menger-tbody"></tbody>
            </table>
          </div>
        </div>
        <div>
          <div class="card" style="margin-bottom:0">
            <div class="card-title" style="color:#93c5fd">n = <span id="menger-cur-n">0</span>단계</div>
            <div style="display:flex;flex-direction:column;gap:8px;">
              <div>
                <div style="font-size:0.75rem;color:#64748b;margin-bottom:2px;">정육면체 수</div>
                <div class="val-blue" style="font-size:1.4rem;font-weight:900;" id="menger-cnt">1</div>
                <div style="font-size:0.72rem;color:#475569;margin-top:1px;" id="menger-cnt-expr">= 20⁰ = 1</div>
              </div>
              <div>
                <div style="font-size:0.75rem;color:#64748b;margin-bottom:2px;">겉넓이 (한 변=1 기준)</div>
                <div class="val-green" style="font-size:1.4rem;font-weight:900;" id="menger-sa">6.000</div>
                <div style="font-size:0.72rem;color:#475569;margin-top:1px;" id="menger-sa-expr">= 6</div>
              </div>
              <div>
                <div style="font-size:0.75rem;color:#64748b;margin-bottom:2px;">부피 (한 변=1 기준)</div>
                <div class="val-yellow" style="font-size:1.4rem;font-weight:900;" id="menger-vol">1.000</div>
                <div style="font-size:0.72rem;color:#475569;margin-top:1px;" id="menger-vol-expr">= (20/27)⁰ = 1</div>
                <div style="margin-top:4px;" id="menger-vol-badge"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="formula-box" style="margin-top:12px;">
        <div class="formula-title">n단계 공식</div>
        겉넓이 = <span class="emph2">2·(20/9)ⁿ + 4·(8/9)ⁿ</span> &nbsp;(발산 → ∞)<br>
        부피 = <span class="emph">(20/27)ⁿ</span> &nbsp;(수렴 → 0)
      </div>
    </div>

    <div class="card">
      <div class="card-title">🎨 단면 시각화 (2D 격자)</div>
      <div class="ctrl-row">
        <label>단계 n =</label>
        <input type="range" id="menger-vis-n" min="0" max="4" value="0" oninput="drawMenger(this.value)">
        <div class="n-badge" id="menger-vis-badge">0</div>
        <button class="btn btn-gray" onclick="animateMenger()">▶ 애니메이션</button>
      </div>
      <div class="canvas-wrap" style="max-width:66%;margin:0 auto;">
        <canvas id="menger-canvas" height="200"></canvas>
      </div>
      <div class="canvas-label">정면에서 본 멩거 스펀지 단면 (중앙과 4면 가운데가 뚫려 있음)</div>
    </div>

    <div class="card">
      <div class="card-title">🧊 3D 시뮬레이션</div>
      <div class="card-sub">등각 투영법(isometric)으로 멩거 스펀지를 3D로 표현합니다. 단계가 올라갈수록 뚫린 구멍이 많아집니다.</div>
      <div class="ctrl-row">
        <label>단계 n =</label>
        <input type="range" id="menger3d-n" min="0" max="3" value="0" oninput="drawMenger3D(this.value)">
        <div class="n-badge" id="menger3d-badge">0</div>
        <button class="btn btn-gray" onclick="animateMenger3D()">▶ 애니메이션</button>
        <button class="btn btn-gray" id="menger3d-rot-btn" onclick="toggleMenger3DRotate()">🔄 자동 회전</button>
      </div>
      <div class="canvas-wrap">
        <canvas id="menger3d-canvas" height="420"></canvas>
      </div>
      <div class="canvas-label" id="menger3d-label">0단계 멩거 스펀지 — 정육면체 1개</div>
    </div>

    <div class="card">
      <div class="card-title">🧩 확인 문제</div>
      <div class="quiz-box">
        <div class="quiz-q">Q1. 3단계 멩거 스펀지의 정육면체 개수는?</div>
        <div class="quiz-opts" id="mq1-opts">
          <div class="quiz-opt" onclick="checkMQ(1,this,'wrong')">400개</div>
          <div class="quiz-opt" onclick="checkMQ(1,this,'correct')">8000개</div>
          <div class="quiz-opt" onclick="checkMQ(1,this,'wrong')">27000개</div>
          <div class="quiz-opt" onclick="checkMQ(1,this,'wrong')">729개</div>
        </div>
        <div class="quiz-feedback" id="mq1-fb"></div>
      </div>
      <div class="quiz-box">
        <div class="quiz-q">Q2. 단계를 무한히 반복하면 멩거 스펀지의 부피는 어떻게 될까?</div>
        <div class="quiz-opts" id="mq2-opts">
          <div class="quiz-opt" onclick="checkMQ(2,this,'wrong')">1에 수렴한다</div>
          <div class="quiz-opt" onclick="checkMQ(2,this,'correct')">0에 수렴한다</div>
          <div class="quiz-opt" onclick="checkMQ(2,this,'wrong')">무한히 커진다</div>
          <div class="quiz-opt" onclick="checkMQ(2,this,'wrong')">변하지 않는다</div>
        </div>
        <div class="quiz-feedback" id="mq2-fb"></div>
      </div>
      <div class="quiz-box">
        <div class="quiz-q">Q3. 단계를 무한히 반복하면 멩거 스펀지의 겉넓이는 어떻게 될까?</div>
        <div class="quiz-opts" id="mq3-opts">
          <div class="quiz-opt" onclick="checkMQ(3,this,'wrong')">6으로 수렴한다</div>
          <div class="quiz-opt" onclick="checkMQ(3,this,'wrong')">0에 수렴한다</div>
          <div class="quiz-opt" onclick="checkMQ(3,this,'correct')">무한히 커진다(발산)</div>
          <div class="quiz-opt" onclick="checkMQ(3,this,'wrong')">20에 수렴한다</div>
        </div>
        <div class="quiz-feedback" id="mq3-fb"></div>
      </div>
    </div>
  </div>

  <!-- ════════════════ 코흐 곡선 ════════════════ -->
  <div id="pane-koch" class="pane">

    <div class="card">
      <div class="card-title">❄️ 코흐 곡선이란?</div>
      <div class="card-sub">
        선분을 3등분하고, 가운데 구간을 <b>정삼각형</b> 모양으로 교체합니다.<br>
        새로 생긴 4개의 선분에 이 과정을 반복하면 코흐 곡선이 됩니다.<br>
        3개의 코흐 곡선을 이어 붙이면 <b>코흐 눈송이(스노우플레이크)</b>가 됩니다.
      </div>
      <div class="formula-box">
        <div class="formula-title">핵심 규칙</div>
        선분 1개 → 선분 4개 (각 길이 1/3)<br>
        n단계 선분 수: <span class="emph">4ⁿ</span><br>
        선분 하나의 길이: <span class="emph">(1/3)ⁿ</span><br>
        총 둘레 길이: <span class="emph">(4/3)ⁿ</span>
      </div>
    </div>

    <!-- 수학 탭 -->
    <div class="card">
      <div class="card-title">📊 단계별 계산</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;">
        <button class="btn btn-blue" id="koch-mode-curve" onclick="setKochMode('curve')">코흐 곡선</button>
        <button class="btn btn-gray" id="koch-mode-snow" onclick="setKochMode('snow')">코흐 눈송이</button>
      </div>
      <div class="ctrl-row">
        <label>단계 n =</label>
        <input type="range" id="koch-n" min="0" max="6" value="0" oninput="updateKoch(this.value)">
        <div class="n-badge" id="koch-n-badge">0</div>
      </div>

      <div class="two-col">
        <div style="overflow-x:auto">
          <table class="res-table">
            <thead>
              <tr>
                <th>단계</th>
                <th>선분 수</th>
                <th>선분 길이</th>
                <th>총 둘레</th>
                <th id="koch-area-th">-</th>
              </tr>
            </thead>
            <tbody id="koch-tbody"></tbody>
          </table>
        </div>
        <div>
          <div class="card" style="margin-bottom:0">
            <div class="card-title" style="color:#a5f3fc">n = <span id="koch-cur-n">0</span>단계</div>
            <div style="display:flex;flex-direction:column;gap:8px;">
              <div>
                <div style="font-size:0.75rem;color:#64748b;">선분 수</div>
                <div class="val-blue" style="font-size:1.3rem;font-weight:900;" id="koch-seg">1</div>
                <div style="font-size:0.72rem;color:#475569;" id="koch-seg-expr">= 4⁰ = 1</div>
              </div>
              <div>
                <div style="font-size:0.75rem;color:#64748b;">총 둘레 길이</div>
                <div class="val-green" style="font-size:1.3rem;font-weight:900;" id="koch-perim">1.000</div>
                <div style="font-size:0.72rem;color:#475569;" id="koch-perim-expr"></div>
                <div style="margin-top:4px;"><span class="badge badge-div">발산 → ∞</span></div>
              </div>
              <div id="koch-snow-area-wrap" style="display:none">
                <div style="font-size:0.75rem;color:#64748b;">눈송이 넓이</div>
                <div class="val-yellow" style="font-size:1.3rem;font-weight:900;" id="koch-area">0.433</div>
                <div style="font-size:0.72rem;color:#475569;" id="koch-area-expr"></div>
                <div style="margin-top:4px;"><span class="badge badge-conv">수렴 → √3/5 · A</span></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="formula-box" style="margin-top:12px;" id="koch-formula-box">
        <div class="formula-title">n단계 코흐 곡선 공식 (초기 길이 1)</div>
        선분 수 = <span class="emph">4ⁿ</span><br>
        선분 길이 = <span class="emph">(1/3)ⁿ</span><br>
        총 둘레 = <span class="emph2">(4/3)ⁿ</span> &nbsp;<span class="badge badge-div">발산</span>
      </div>
    </div>

    <div class="card">
      <div class="card-title">🎨 코흐 곡선 시각화</div>
      <div class="ctrl-row">
        <label>단계 n =</label>
        <input type="range" id="koch-vis-n" min="0" max="6" value="0" oninput="drawKoch(this.value)">
        <div class="n-badge" id="koch-vis-badge">0</div>
        <button class="btn btn-gray" onclick="setKochVis('curve')" id="kv-curve-btn">코흐 곡선</button>
        <button class="btn btn-gray" onclick="setKochVis('snow')" id="kv-snow-btn">눈송이</button>
      </div>
      <div class="canvas-wrap">
        <canvas id="koch-canvas" height="320"></canvas>
      </div>
      <div class="canvas-label" id="koch-canvas-label">0단계 코흐 곡선</div>
    </div>

    <div class="card">
      <div class="card-title">🧩 확인 문제</div>
      <div class="quiz-box">
        <div class="quiz-q">Q1. 코흐 곡선의 총 둘레 길이를 무한히 반복하면?</div>
        <div class="quiz-opts" id="kq1-opts">
          <div class="quiz-opt" onclick="checkKQ(1,this,'wrong')">1에 수렴한다</div>
          <div class="quiz-opt" onclick="checkKQ(1,this,'correct')">무한히 커진다(발산)</div>
          <div class="quiz-opt" onclick="checkKQ(1,this,'wrong')">4/3에 수렴한다</div>
          <div class="quiz-opt" onclick="checkKQ(1,this,'wrong')">0에 수렴한다</div>
        </div>
        <div class="quiz-feedback" id="kq1-fb"></div>
      </div>
      <div class="quiz-box">
        <div class="quiz-q">Q2. 코흐 눈송이의 넓이는 단계를 무한히 반복하면?</div>
        <div class="quiz-opts" id="kq2-opts">
          <div class="quiz-opt" onclick="checkKQ(2,this,'correct')">어떤 값에 수렴한다</div>
          <div class="quiz-opt" onclick="checkKQ(2,this,'wrong')">무한히 커진다</div>
          <div class="quiz-opt" onclick="checkKQ(2,this,'wrong')">0에 수렴한다</div>
          <div class="quiz-opt" onclick="checkKQ(2,this,'wrong')">3에 수렴한다</div>
        </div>
        <div class="quiz-feedback" id="kq2-fb"></div>
      </div>
      <div class="quiz-box">
        <div class="quiz-q">Q3. 4단계 코흐 곡선의 선분 개수는?</div>
        <div class="quiz-opts" id="kq3-opts">
          <div class="quiz-opt" onclick="checkKQ(3,this,'wrong')">16개</div>
          <div class="quiz-opt" onclick="checkKQ(3,this,'wrong')">64개</div>
          <div class="quiz-opt" onclick="checkKQ(3,this,'correct')">256개</div>
          <div class="quiz-opt" onclick="checkKQ(3,this,'wrong')">1024개</div>
        </div>
        <div class="quiz-feedback" id="kq3-fb"></div>
      </div>
    </div>
  </div>

  <!-- ════════════════ 칸토어 집합 ════════════════ -->
  <div id="pane-cantor" class="pane">

    <div class="card">
      <div class="card-title">📏 칸토어 집합이란?</div>
      <div class="card-sub">
        [0, 1] 구간을 3등분하고 가운데 열린 구간 (1/3, 2/3)를 제거합니다.<br>
        남은 두 구간에 같은 과정을 반복합니다. 이를 무한히 반복하면 칸토어 집합이 됩니다.
      </div>
      <div class="formula-box">
        <div class="formula-title">핵심 규칙</div>
        선분 1개 → 2개 (각 길이 1/3)<br>
        n단계 선분 수: <span class="emph">2ⁿ</span><br>
        선분 하나의 길이: <span class="emph">(1/3)ⁿ</span><br>
        총 길이: <span class="emph">(2/3)ⁿ</span>
      </div>
    </div>

    <div class="card">
      <div class="card-title">📊 단계별 계산</div>
      <div class="ctrl-row">
        <label>단계 n =</label>
        <input type="range" id="cantor-n" min="0" max="7" value="0" oninput="updateCantor(this.value)">
        <div class="n-badge" id="cantor-n-badge">0</div>
      </div>

      <div class="two-col">
        <div style="overflow-x:auto">
          <table class="res-table">
            <thead>
              <tr><th>단계</th><th>선분 수</th><th>선분 길이</th><th>총 길이</th></tr>
            </thead>
            <tbody id="cantor-tbody"></tbody>
          </table>
        </div>
        <div>
          <div class="card" style="margin-bottom:0">
            <div class="card-title" style="color:#f9a8d4">n = <span id="cantor-cur-n">0</span>단계</div>
            <div style="display:flex;flex-direction:column;gap:8px;">
              <div>
                <div style="font-size:0.75rem;color:#64748b;">선분 수</div>
                <div class="val-blue" style="font-size:1.3rem;font-weight:900;" id="cantor-cnt">1</div>
                <div style="font-size:0.72rem;color:#475569;" id="cantor-cnt-expr">= 2⁰ = 1</div>
              </div>
              <div>
                <div style="font-size:0.75rem;color:#64748b;">선분 하나의 길이</div>
                <div style="font-size:1.3rem;font-weight:900;color:#f9a8d4;" id="cantor-seg-len">1.0000</div>
                <div style="font-size:0.72rem;color:#475569;" id="cantor-seg-expr">= (1/3)⁰ = 1</div>
              </div>
              <div>
                <div style="font-size:0.75rem;color:#64748b;">총 길이</div>
                <div class="val-green" style="font-size:1.3rem;font-weight:900;" id="cantor-total">1.0000</div>
                <div style="font-size:0.72rem;color:#475569;" id="cantor-total-expr">= (2/3)⁰ = 1</div>
                <div style="margin-top:4px;"><span class="badge badge-conv">수렴 → 0</span></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="formula-box" style="margin-top:12px;">
        <div class="formula-title">n단계 공식</div>
        선분 수 = <span class="emph">2ⁿ</span><br>
        선분 길이 = <span class="emph">(1/3)ⁿ</span><br>
        총 길이 = <span class="emph2">(2/3)ⁿ</span> &nbsp;<span class="badge badge-conv">수렴 → 0</span><br>
        <br>
        <span style="color:#94a3b8;font-size:0.78rem;">
        길이는 0으로 수렴하지만, 점은 무수히 많이 남아있다는 것이 칸토어 집합의 역설!
        </span>
      </div>
    </div>

    <div class="card">
      <div class="card-title">🎨 칸토어 집합 시각화</div>
      <div class="ctrl-row">
        <label>단계 n =</label>
        <input type="range" id="cantor-vis-n" min="0" max="7" value="0" oninput="drawCantor(this.value)">
        <div class="n-badge" id="cantor-vis-badge">0</div>
        <button class="btn btn-gray" onclick="animateCantor()">▶ 애니메이션</button>
      </div>
      <div class="canvas-wrap">
        <canvas id="cantor-canvas" height="260"></canvas>
      </div>
      <div class="canvas-label">각 행이 한 단계씩 — 빨간 선이 제거되고 파란 선이 남습니다</div>
    </div>

    <div class="card">
      <div class="card-title">🧩 확인 문제</div>
      <div class="quiz-box">
        <div class="quiz-q">Q1. 칸토어 집합에서 총 길이(2/3)ⁿ은 n→∞ 일 때?</div>
        <div class="quiz-opts" id="cq1-opts">
          <div class="quiz-opt" onclick="checkCQ(1,this,'correct')">0에 수렴한다</div>
          <div class="quiz-opt" onclick="checkCQ(1,this,'wrong')">1에 수렴한다</div>
          <div class="quiz-opt" onclick="checkCQ(1,this,'wrong')">무한히 커진다</div>
          <div class="quiz-opt" onclick="checkCQ(1,this,'wrong')">2/3에 수렴한다</div>
        </div>
        <div class="quiz-feedback" id="cq1-fb"></div>
      </div>
      <div class="quiz-box">
        <div class="quiz-q">Q2. 칸토어 집합에서 5단계의 선분 수는?</div>
        <div class="quiz-opts" id="cq2-opts">
          <div class="quiz-opt" onclick="checkCQ(2,this,'wrong')">10개</div>
          <div class="quiz-opt" onclick="checkCQ(2,this,'correct')">32개</div>
          <div class="quiz-opt" onclick="checkCQ(2,this,'wrong')">64개</div>
          <div class="quiz-opt" onclick="checkCQ(2,this,'wrong')">16개</div>
        </div>
        <div class="quiz-feedback" id="cq2-fb"></div>
      </div>
      <div class="quiz-box">
        <div class="quiz-q">Q3. 칸토어 집합은 총 길이가 0이지만 왜 점이 무수히 많은가?</div>
        <div class="quiz-opts" id="cq3-opts">
          <div class="quiz-opt" onclick="checkCQ(3,this,'wrong')">매 단계 점이 추가되기 때문</div>
          <div class="quiz-opt" onclick="checkCQ(3,this,'wrong')">점이 유한히 많기 때문</div>
          <div class="quiz-opt" onclick="checkCQ(3,this,'correct')">유한 번 제거만 하므로 끝점/경계점이 무한히 남기 때문</div>
          <div class="quiz-opt" onclick="checkCQ(3,this,'wrong')">구간이 점으로 쪼개지기 때문</div>
        </div>
        <div class="quiz-feedback" id="cq3-fb"></div>
      </div>
    </div>
  </div>

  <!-- ════════════════ 프랙털 차원 ════════════════ -->
  <div id="pane-dimension" class="pane">

    <div class="card">
      <div class="card-title">🔢 자기 닮음 차원이란?</div>
      <div class="card-sub">
        일반적인 도형은 크기를 k배 키우면, 넓이는 k²배, 부피는 k³배가 됩니다.<br>
        프랙털에서는 k배 키울 때 <b>N배</b>가 된다면,<br>
        <b>kᵈ = N</b>이 되는 d를 <b>프랙털 차원(자기 닮음 차원)</b>이라 합니다.
      </div>
      <div class="formula-box">
        <div class="formula-title">프랙털 차원 공식</div>
        <span class="emph">d = log(N) / log(k)</span><br>
        <br>
        여기서<br>
        &nbsp;• N = 축소 복사본의 개수<br>
        &nbsp;• k = 각 복사본의 확대 비율 (= 1 / 축소 비율)
      </div>
    </div>

    <!-- 일반 도형 먼저 -->
    <div class="card">
      <div class="card-title">📐 일반 도형은 차원이 정수!</div>
      <div class="two-col">
        <div class="dim-card">
          <div class="dim-title">🟥 정사각형</div>
          <div style="font-size:0.8rem;color:#c4b5fd;margin-bottom:8px;">2배로 키우면 → <b style="color:#fff">4배</b> 많아짐</div>
          <div class="big-eq">k=2, N=4</div>
          <div style="font-size:0.8rem;color:#c4b5fd;text-align:center;margin-top:4px;">d = log 4 / log 2 = <span class="emph3">2</span></div>
        </div>
        <div class="dim-card">
          <div class="dim-title">🧊 정육면체</div>
          <div style="font-size:0.8rem;color:#c4b5fd;margin-bottom:8px;">2배로 키우면 → <b style="color:#fff">8배</b> 많아짐</div>
          <div class="big-eq">k=2, N=8</div>
          <div style="font-size:0.8rem;color:#c4b5fd;text-align:center;margin-top:4px;">d = log 8 / log 2 = <span class="emph3">3</span></div>
        </div>
      </div>
    </div>

    <!-- 각 프랙털 -->
    <div class="card">
      <div class="card-title">📐 프랙털의 차원 계산해보기</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
        <button class="btn btn-blue" id="dim-menger-btn" onclick="showDim('menger')">🧊 멩거 스펀지</button>
        <button class="btn btn-gray" id="dim-koch-btn" onclick="showDim('koch')">❄️ 코흐 곡선</button>
        <button class="btn btn-gray" id="dim-cantor-btn" onclick="showDim('cantor')">📏 칸토어 집합</button>
      </div>

      <!-- 멩거 -->
      <div id="dim-menger" class="dim-show">
        <div class="dim-card">
          <div class="dim-title">🧊 멩거 스펀지의 차원</div>
          <div style="font-size:0.82rem;color:#c4b5fd;line-height:1.8;margin-bottom:10px;">
            3배 키우면 → <b style="color:#fff">20개</b>의 복사본이 생깁니다<br>
            (27개 중 7개 제거했으므로)
          </div>
          <div class="big-eq">k = 3, N = 20</div>
          <div style="text-align:center;margin:8px 0;font-size:0.85rem;color:#c4b5fd;">
            d = log(20) / log(3) ≈
          </div>
          <div class="dim-value">2.727...</div>
          <div class="dim-compare">
            <div class="dim-pil"><div class="dp-num" style="color:#4ade80">2</div><div class="dp-lbl">일반 넓이</div></div>
            <div class="dim-pil"><div class="dp-num" style="color:#a78bfa">2.727</div><div class="dp-lbl">멩거 스펀지</div></div>
            <div class="dim-pil"><div class="dp-num" style="color:#f87171">3</div><div class="dp-lbl">일반 부피</div></div>
          </div>
          <div style="margin-top:10px;font-size:0.8rem;color:#94a3b8;text-align:center;">
            2차원과 3차원 사이 — 면보다 복잡하고, 부피는 없다!
          </div>
        </div>
      </div>

      <!-- 코흐 -->
      <div id="dim-koch" class="dim-show" style="display:none">
        <div class="dim-card">
          <div class="dim-title">❄️ 코흐 곡선의 차원</div>
          <div style="font-size:0.82rem;color:#c4b5fd;line-height:1.8;margin-bottom:10px;">
            3배 키우면 → <b style="color:#fff">4개</b>의 복사본이 생깁니다
          </div>
          <div class="big-eq">k = 3, N = 4</div>
          <div style="text-align:center;margin:8px 0;font-size:0.85rem;color:#c4b5fd;">
            d = log(4) / log(3) ≈
          </div>
          <div class="dim-value">1.262...</div>
          <div class="dim-compare">
            <div class="dim-pil"><div class="dp-num" style="color:#4ade80">1</div><div class="dp-lbl">일반 선</div></div>
            <div class="dim-pil"><div class="dp-num" style="color:#a78bfa">1.262</div><div class="dp-lbl">코흐 곡선</div></div>
            <div class="dim-pil"><div class="dp-num" style="color:#f87171">2</div><div class="dp-lbl">일반 넓이</div></div>
          </div>
          <div style="margin-top:10px;font-size:0.8rem;color:#94a3b8;text-align:center;">
            1차원과 2차원 사이 — 선보다 복잡하고, 넓이는 없다!
          </div>
        </div>
      </div>

      <!-- 칸토어 -->
      <div id="dim-cantor" class="dim-show" style="display:none">
        <div class="dim-card">
          <div class="dim-title">📏 칸토어 집합의 차원</div>
          <div style="font-size:0.82rem;color:#c4b5fd;line-height:1.8;margin-bottom:10px;">
            3배 키우면 → <b style="color:#fff">2개</b>의 복사본이 생깁니다
          </div>
          <div class="big-eq">k = 3, N = 2</div>
          <div style="text-align:center;margin:8px 0;font-size:0.85rem;color:#c4b5fd;">
            d = log(2) / log(3) ≈
          </div>
          <div class="dim-value">0.630...</div>
          <div class="dim-compare">
            <div class="dim-pil"><div class="dp-num" style="color:#4ade80">0</div><div class="dp-lbl">점</div></div>
            <div class="dim-pil"><div class="dp-num" style="color:#a78bfa">0.630</div><div class="dp-lbl">칸토어 집합</div></div>
            <div class="dim-pil"><div class="dp-num" style="color:#f87171">1</div><div class="dp-lbl">일반 선</div></div>
          </div>
          <div style="margin-top:10px;font-size:0.8rem;color:#94a3b8;text-align:center;">
            0차원과 1차원 사이 — 점보다 많고, 선보다 적다!
          </div>
        </div>
      </div>
    </div>

    <!-- 상호작용 계산기 -->
    <div class="card">
      <div class="card-title">🧮 프랙털 차원 계산기</div>
      <div class="card-sub">k배 크기를 키울 때 N개의 복사본이 생기는 프랙털의 차원을 계산해보자!</div>
      <div class="ctrl-row" style="justify-content:center;">
        <label>k (확대 배율) =</label>
        <input type="range" id="dim-k" min="2" max="10" value="3" oninput="calcDim()">
        <div class="n-badge" id="dim-k-val">3</div>
        <label style="margin-left:10px">N (복사본 수) =</label>
        <input type="range" id="dim-N" min="2" max="50" value="20" oninput="calcDim()">
        <div class="n-badge" id="dim-N-val">20</div>
      </div>
      <div style="text-align:center;margin:10px 0;">
        <div style="font-size:1rem;color:#94a3b8;">d = log(<span id="dim-N-disp">20</span>) / log(<span id="dim-k-disp">3</span>) =</div>
        <div id="dim-result" style="font-size:2.5rem;font-weight:900;color:#a78bfa;margin:6px 0;">2.727</div>
        <div id="dim-interp" style="font-size:0.82rem;color:#64748b;"></div>
      </div>
      <div style="height:20px;background:#0f172a;border-radius:10px;overflow:hidden;margin-top:6px;position:relative;">
        <div id="dim-bar" style="height:100%;background:linear-gradient(90deg,#4ade80,#a78bfa,#f87171);border-radius:10px;transition:width .3s;"></div>
        <div style="position:absolute;top:50%;left:0;right:0;display:flex;justify-content:space-between;transform:translateY(-50%);padding:0 4px;font-size:0.65rem;color:#475569;">
          <span>0 (점)</span><span>1 (선)</span><span>2 (면)</span><span>3 (부피)</span>
        </div>
      </div>
    </div>

    <!-- 비교 표 -->
    <div class="card">
      <div class="card-title">📋 세 프랙털 한눈에 비교</div>
      <div style="overflow-x:auto">
        <table class="res-table">
          <thead>
            <tr>
              <th>프랙털</th><th>축소 비율</th><th>복사본 수(N)</th><th>확대 배율(k)</th><th>차원 d</th><th>길이/넓이/부피</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>📏 칸토어 집합</td>
              <td>1/3씩</td>
              <td class="val-blue">2</td>
              <td class="val-blue">3</td>
              <td class="val-yellow">≈ 0.630</td>
              <td><span class="badge badge-conv">길이 → 0</span></td>
            </tr>
            <tr>
              <td>❄️ 코흐 곡선</td>
              <td>1/3씩</td>
              <td class="val-blue">4</td>
              <td class="val-blue">3</td>
              <td class="val-yellow">≈ 1.262</td>
              <td><span class="badge badge-div">둘레 → ∞</span></td>
            </tr>
            <tr>
              <td>🧊 멩거 스펀지</td>
              <td>1/3씩</td>
              <td class="val-blue">20</td>
              <td class="val-blue">3</td>
              <td class="val-yellow">≈ 2.727</td>
              <td><span class="badge badge-div">겉넓이 → ∞</span> <span class="badge badge-conv">부피 → 0</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 퀴즈 -->
    <div class="card">
      <div class="card-title">🧩 확인 문제</div>
      <div class="quiz-box">
        <div class="quiz-q">Q1. 시어핀스키 삼각형은 2배 키우면 3개의 복사본이 나옵니다. 차원은?</div>
        <div class="quiz-opts" id="dq1-opts">
          <div class="quiz-opt" onclick="checkDQ(1,this,'wrong')">1.0</div>
          <div class="quiz-opt" onclick="checkDQ(1,this,'correct')">log3/log2 ≈ 1.585</div>
          <div class="quiz-opt" onclick="checkDQ(1,this,'wrong')">2.0</div>
          <div class="quiz-opt" onclick="checkDQ(1,this,'wrong')">log2/log3 ≈ 0.630</div>
        </div>
        <div class="quiz-feedback" id="dq1-fb"></div>
      </div>
      <div class="quiz-box">
        <div class="quiz-q">Q2. 프랙털 차원이 2.727인 멩거 스펀지는 어떤 도형들 사이에 있는 차원인가?</div>
        <div class="quiz-opts" id="dq2-opts">
          <div class="quiz-opt" onclick="checkDQ(2,this,'wrong')">0차원 ~ 1차원</div>
          <div class="quiz-opt" onclick="checkDQ(2,this,'wrong')">1차원 ~ 2차원</div>
          <div class="quiz-opt" onclick="checkDQ(2,this,'correct')">2차원 ~ 3차원</div>
          <div class="quiz-opt" onclick="checkDQ(2,this,'wrong')">3차원 이상</div>
        </div>
        <div class="quiz-feedback" id="dq2-fb"></div>
      </div>
      <div class="quiz-box">
        <div class="quiz-q">Q3. 4배 키울 때 16개의 복사본이 생기는 프랙털의 차원은?</div>
        <div class="quiz-opts" id="dq3-opts">
          <div class="quiz-opt" onclick="checkDQ(3,this,'wrong')">1</div>
          <div class="quiz-opt" onclick="checkDQ(3,this,'wrong')">2.5</div>
          <div class="quiz-opt" onclick="checkDQ(3,this,'correct')">2</div>
          <div class="quiz-opt" onclick="checkDQ(3,this,'wrong')">4</div>
        </div>
        <div class="quiz-feedback" id="dq3-fb"></div>
      </div>
    </div>
  </div>

</div><!-- /app -->

<script>
// ═══════════════════════════════════════════
// 탭 전환
// ═══════════════════════════════════════════
function switchTab(id){
  document.querySelectorAll('.pane').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('pane-'+id).classList.add('active');
  event.currentTarget.classList.add('active');
  if(id==='menger') { drawMenger(document.getElementById('menger-vis-n').value); drawMenger3D(document.getElementById('menger3d-n').value); }
  if(id==='koch')   drawKoch(document.getElementById('koch-vis-n').value);
  if(id==='cantor') drawCantor(document.getElementById('cantor-vis-n').value);
}

// ═══════════════════════════════════════════
// 멩거 스펀지 계산
// ═══════════════════════════════════════════
function mengerData(nMax){
  let rows=[];
  for(let n=0;n<=nMax;n++){
    let cnt = Math.pow(20,n);
    // 겉넓이: 멩거 스펀지 공식 face 2*(20/9)^n + 4*(8/9)^n
    let sa = 2*Math.pow(20/9,n) + 4*Math.pow(8/9,n);
    let vol = Math.pow(20/27,n);
    rows.push({n, cnt, sa, vol});
  }
  return rows;
}

function updateMenger(n){
  n=parseInt(n);
  document.getElementById('menger-n-badge').textContent=n;
  document.getElementById('menger-cur-n').textContent=n;
  let data = mengerData(n);
  // 표 그리기
  let tbody = document.getElementById('menger-tbody');
  tbody.innerHTML='';
  data.forEach(r=>{
    let hi = r.n===n;
    let tr=document.createElement('tr');
    if(hi)tr.className='highlight';
    let cntStr = r.n<=4 ? `20^${r.n} = ${fmt(r.cnt)}` : `20^${r.n}`;
    tr.innerHTML=`<td>${r.n}</td><td class="val-blue">${fmt(r.cnt)}</td><td class="val-green">${r.sa.toFixed(3)}</td><td class="val-yellow">${r.vol.toFixed(4)}</td>`;
    tbody.appendChild(tr);
  });
  let d = data[n];
  document.getElementById('menger-cnt').textContent = fmt(d.cnt);
  document.getElementById('menger-cnt-expr').textContent = `= 20^${n} = ${fmt(d.cnt)}`;
  document.getElementById('menger-sa').textContent = d.sa.toFixed(4);
  document.getElementById('menger-sa-expr').textContent = `≈ 2×(20/9)^${n} + 4×(8/9)^${n}`;
  document.getElementById('menger-vol').textContent = d.vol.toFixed(5);
  document.getElementById('menger-vol-expr').textContent = `= (20/27)^${n}`;
  let badge = document.getElementById('menger-vol-badge');
  if(n===0) badge.innerHTML='';
  else if(d.vol < 0.001) badge.innerHTML='<span class="badge badge-conv">거의 0!</span>';
  else badge.innerHTML=`<span class="badge badge-gray">0을 향해 수렴 중</span>`;
}

// ═══════════════════════════════════════════
// 멩거 스펀지 시각화 (정면 단면)
// ═══════════════════════════════════════════
function isMengerHole(x,y,size){
  while(size>=3){
    let s=size/3;
    let xi=Math.floor(x/s), yi=Math.floor(y/s);
    x-=xi*s; y-=yi*s;
    // 중앙(1,1) + 각 면 중앙: (0,1),(1,0),(2,1),(1,2)
    if((xi===1&&yi===1)||(xi===0&&yi===1)||(xi===1&&yi===0)||(xi===2&&yi===1)||(xi===1&&yi===2))
      return true;
    size=s;
  }
  return false;
}

function drawMenger(n){
  n=parseInt(n);
  document.getElementById('menger-vis-badge').textContent=n;
  let canvas=document.getElementById('menger-canvas');
  let W=canvas.clientWidth||330; canvas.width=W; canvas.height=W;
  let ctx=canvas.getContext('2d');
  ctx.clearRect(0,0,W,W);
  let sz = Math.pow(3,n);
  let cell = W/sz;
  for(let row=0;row<sz;row++){
    for(let col=0;col<sz;col++){
      if(isMengerHole(col,row,sz)){
        ctx.fillStyle='#0f172a';
      } else {
        let t=n/4;
        let r=Math.floor(59+t*(200-59)), g=Math.floor(130+t*(30-130)), b=Math.floor(246+t*(50-246));
        ctx.fillStyle=`rgb(${r},${g},${b})`;
      }
      ctx.fillRect(col*cell, row*cell, cell-0.5, cell-0.5);
    }
  }
}

let mengerAnim=null;
function animateMenger(){
  if(mengerAnim)clearInterval(mengerAnim);
  let n=0,el=document.getElementById('menger-vis-n');
  mengerAnim=setInterval(()=>{
    el.value=n; drawMenger(n);
    document.getElementById('menger-vis-badge').textContent=n;
    n++; if(n>4){clearInterval(mengerAnim);mengerAnim=null;}
  },700);
}

// ═══════════════════════════════════════════
// 멩거 스펀지 3D (등각 투영)
// ═══════════════════════════════════════════
let menger3dRotAngle=0;
let menger3dRotTimer=null;
let menger3dRotating=false;
let menger3dCache={};

function isMengerHole3D(cx,cy,cz,sz){
  // sz = 3^n grid size
  // check if ANY axis projection is a hole
  let x=cx,y=cy,z=cz,s=sz;
  while(s>=3){
    let ds=s/3;
    let xi=Math.floor(x/ds), yi=Math.floor(y/ds), zi=Math.floor(z/ds);
    // cross pattern: exactly two of xi,yi,zi equal 1
    let cnt=(xi===1?1:0)+(yi===1?1:0)+(zi===1?1:0);
    if(cnt>=2) return true;
    x-=xi*ds; y-=yi*ds; z-=zi*ds;
    s=ds;
  }
  return false;
}

function buildMengerCubes(n){
  // returns array of {cx,cy,cz} grid coords (0..3^n-1)
  let sz=Math.pow(3,n);
  let cubes=[];
  for(let cx=0;cx<sz;cx++)
    for(let cy=0;cy<sz;cy++)
      for(let cz=0;cz<sz;cz++)
        if(!isMengerHole3D(cx,cy,cz,sz))
          cubes.push({cx,cy,cz});
  return {cubes,sz};
}

function getMengerGeometry(n){
  if(menger3dCache[n]) return menger3dCache[n];

  let {cubes,sz}=buildMengerCubes(n);
  let cubeSet=new Set(cubes.map(({cx,cy,cz})=>`${cx},${cy},${cz}`));
  let faceDefs=[
    {delta:[ 1, 0, 0], shade:0.86, normal:[ 1, 0, 0], corners:[[1,0,0],[1,0,1],[1,1,1],[1,1,0]]},
    {delta:[-1, 0, 0], shade:0.60, normal:[-1, 0, 0], corners:[[0,0,0],[0,1,0],[0,1,1],[0,0,1]]},
    {delta:[ 0, 1, 0], shade:1.00, normal:[ 0, 1, 0], corners:[[0,1,0],[1,1,0],[1,1,1],[0,1,1]]},
    {delta:[ 0,-1, 0], shade:0.52, normal:[ 0,-1, 0], corners:[[0,0,0],[0,0,1],[1,0,1],[1,0,0]]},
    {delta:[ 0, 0, 1], shade:0.74, normal:[ 0, 0, 1], corners:[[0,0,1],[0,1,1],[1,1,1],[1,0,1]]},
    {delta:[ 0, 0,-1], shade:0.58, normal:[ 0, 0,-1], corners:[[0,0,0],[1,0,0],[1,1,0],[0,1,0]]},
  ];

  let faces=[];
  cubes.forEach(({cx,cy,cz})=>{
    faceDefs.forEach(face=>{
      let nx=cx+face.delta[0], ny=cy+face.delta[1], nz=cz+face.delta[2];
      if(cubeSet.has(`${nx},${ny},${nz}`)) return;
      faces.push({
        shade: face.shade,
        normal: face.normal,
        corners: face.corners.map(([dx,dy,dz])=>({x:cx+dx,y:cy+dy,z:cz+dz}))
      });
    });
  });

  menger3dCache[n]={sz,faces};
  return menger3dCache[n];
}

function drawMenger3D(n){
  n=parseInt(n);
  document.getElementById('menger3d-badge').textContent=n;
  let cnt=Math.pow(20,n);
  document.getElementById('menger3d-label').textContent=
    `${n}단계 멩거 스펀지 — 작은 정육면체 ${fmt(cnt)}개`;
  let canvas=document.getElementById('menger3d-canvas');
  let W=canvas.clientWidth||600; canvas.width=W;
  let H=420; canvas.height=H;
  _renderMenger3D(canvas, n, menger3dRotAngle);
}

function _renderMenger3D(canvas, n, angleY){
  let W=canvas.width, H=canvas.height;
  let ctx=canvas.getContext('2d');
  ctx.fillStyle='#0f172a'; ctx.fillRect(0,0,W,H);

  let {sz,faces}=getMengerGeometry(n);
  let scale=Math.min(W,H)*0.60/sz;
  let cosY=Math.cos(angleY), sinY=Math.sin(angleY);
  let angleX=0.45; // tilt down
  let cosX=Math.cos(angleX), sinX=Math.sin(angleX);

  // project 3D -> 2D (isometric-like)
  function proj(x,y,z){
    // center at origin
    let cx=x-sz/2, cy=y-sz/2, cz=z-sz/2;
    // rotate Y
    let rx=cx*cosY+cz*sinY;
    let rz=-cx*sinY+cz*cosY;
    // rotate X
    let ry2=cy*cosX-rz*sinX;
    let rz2=cy*sinX+rz*cosX;
    return {
      sx: W/2 + rx*scale,
      sy: H/2 - ry2*scale,
      depth: rz2
    };
  }

  function rotVec(x,y,z){
    let rx=x*cosY+z*sinY;
    let rz=-x*sinY+z*cosY;
    let ry2=y*cosX-rz*sinX;
    let rz2=y*sinX+rz*cosX;
    return {x:rx,y:ry2,z:rz2};
  }

  function drawFace(pts, lightFactor){
    let r=Math.floor((60+n*30)*lightFactor);
    let g=Math.floor((100+n*20)*lightFactor);
    let b=Math.floor((200+n*10)*lightFactor);
    ctx.fillStyle=`rgb(${Math.min(255,r)},${Math.min(255,g)},${Math.min(255,b)})`;
    ctx.strokeStyle=`rgba(0,0,0,0.35)`;
    ctx.lineWidth=0.5;
    ctx.beginPath();
    pts.forEach((p,i)=>i===0?ctx.moveTo(p.sx,p.sy):ctx.lineTo(p.sx,p.sy));
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  }

  let rendered=faces.map(face=>{
    let rotatedNormal=rotVec(face.normal[0], face.normal[1], face.normal[2]);
    if(rotatedNormal.z<=0.001) return null;
    let pts=face.corners.map(({x,y,z})=>proj(x,y,z));
    let depth=pts.reduce((sum,p)=>sum+p.depth,0)/pts.length;
    return {pts, depth, shade: face.shade};
  }).filter(Boolean);

  rendered.sort((a,b)=>a.depth-b.depth);
  rendered.forEach(face=>drawFace(face.pts, face.shade));
}

let menger3dAnim2=null;
function animateMenger3D(){
  if(menger3dAnim2)clearInterval(menger3dAnim2);
  let n=0,el=document.getElementById('menger3d-n');
  menger3dAnim2=setInterval(()=>{
    el.value=n; menger3dRotAngle=Math.PI/6; drawMenger3D(n);
    n++; if(n>3){clearInterval(menger3dAnim2);menger3dAnim2=null;}
  },900);
}

function toggleMenger3DRotate(){
  menger3dRotating=!menger3dRotating;
  let btn=document.getElementById('menger3d-rot-btn');
  btn.textContent=menger3dRotating?'⏹ 정지':'🔄 자동 회전';
  btn.className='btn '+(menger3dRotating?'btn-green':'btn-gray');
  if(menger3dRotating){
    let canvas=document.getElementById('menger3d-canvas');
    let n=parseInt(document.getElementById('menger3d-n').value);
    function rotate(){
      if(!menger3dRotating)return;
      menger3dRotAngle+=0.025;
      _renderMenger3D(canvas,n,menger3dRotAngle);
      requestAnimationFrame(rotate);
    }
    rotate();
  }
}

// ═══════════════════════════════════════════
// 코흐 곡선 계산
// ═══════════════════════════════════════════
let kochMode='curve';
function setKochMode(m){
  kochMode=m;
  document.getElementById('koch-mode-curve').className='btn '+(m==='curve'?'btn-blue':'btn-gray');
  document.getElementById('koch-mode-snow').className='btn '+(m==='snow'?'btn-blue':'btn-gray');
  let n=document.getElementById('koch-n').value;
  updateKoch(n);
}

// 코흐 눈송이 넓이: A_n = A_0*(8/5)*(1-(4/9)^n*(1-5/8)) 
// 실제 공식: S_n = A * (8/5) * (1 - (1/3) * (4/9)^n) 복잡하므로 수치적으로 계산
function kochSnowArea(n){
  // 초기 정삼각형 한변=1, 넓이 = sqrt(3)/4
  let A = Math.sqrt(3)/4;
  let area = A;
  let triangles = 3;
  let side = 1/3;
  for(let i=1;i<=n;i++){
    let dA = triangles * Math.sqrt(3)/4 * side*side;
    area += dA;
    triangles *= 4;
    side /= 3;
  }
  return area;
}

function updateKoch(n){
  n=parseInt(n);
  document.getElementById('koch-n-badge').textContent=n;
  document.getElementById('koch-cur-n').textContent=n;
  let tbody = document.getElementById('koch-tbody');
  tbody.innerHTML='';
  for(let i=0;i<=n;i++){
    let segs=Math.pow(4,i);
    let segLen=Math.pow(1/3,i);
    let perim=Math.pow(4/3,i);
    let tr=document.createElement('tr');
    if(i===n)tr.className='highlight';
    let areaCell = kochMode==='snow'?`<td class="val-yellow">${kochSnowArea(i).toFixed(5)}</td>`:'<td>-</td>';
    tr.innerHTML=`<td>${i}</td><td class="val-blue">${fmt(segs)}</td><td>${segLen.toFixed(5)}</td><td class="val-green">${perim.toFixed(5)}</td>${areaCell}`;
    tbody.appendChild(tr);
  }
  let segs=Math.pow(4,n);
  let perim=Math.pow(4/3,n);
  document.getElementById('koch-seg').textContent=fmt(segs);
  document.getElementById('koch-seg-expr').textContent=`= 4^${n} = ${fmt(segs)}`;
  document.getElementById('koch-perim').textContent=perim.toFixed(5);
  document.getElementById('koch-perim-expr').textContent=`= (4/3)^${n}`;
  let snowWrap = document.getElementById('koch-snow-area-wrap');
  let areaTh = document.getElementById('koch-area-th');
  if(kochMode==='snow'){
    snowWrap.style.display='block';
    areaTh.textContent='눈송이 넓이';
    let area=kochSnowArea(n);
    document.getElementById('koch-area').textContent=area.toFixed(5);
    document.getElementById('koch-area-expr').textContent=`≈ ${area.toFixed(5)}`;
    document.getElementById('koch-formula-box').innerHTML=`
      <div class="formula-title">n단계 코흐 눈송이 공식 (한 변=1 정삼각형)</div>
      선분 수(한 변) = <span class="emph">4ⁿ</span><br>
      총 둘레 = <span class="emph2">(4/3)ⁿ × 3</span> &nbsp;<span class="badge badge-div">발산</span><br>
      넓이 = <span class="emph">A₀ + Σ (덧붙인 삼각형)</span> &nbsp;<span class="badge badge-conv">수렴 → 8/5 A₀</span>
    `;
  } else {
    snowWrap.style.display='none';
    areaTh.textContent='-';
    document.getElementById('koch-formula-box').innerHTML=`
      <div class="formula-title">n단계 코흐 곡선 공식 (초기 길이 1)</div>
      선분 수 = <span class="emph">4ⁿ</span><br>
      선분 길이 = <span class="emph">(1/3)ⁿ</span><br>
      총 둘레 = <span class="emph2">(4/3)ⁿ</span> &nbsp;<span class="badge badge-div">발산</span>
    `;
  }
}

// ═══════════════════════════════════════════
// 코흐 곡선 그리기
// ═══════════════════════════════════════════
let kochVisMode='curve';
function setKochVis(m){
  kochVisMode=m;
  document.getElementById('kv-curve-btn').className='btn '+(m==='curve'?'btn-blue':'btn-gray');
  document.getElementById('kv-snow-btn').className='btn '+(m==='snow'?'btn-blue':'btn-gray');
  let n=document.getElementById('koch-vis-n').value;
  drawKoch(n);
}

function kochSubdivision(x1,y1,x2,y2,turnSign){
  let dx=x2-x1, dy=y2-y1;
  let ax=x1+dx/3, ay=y1+dy/3;
  let bx=x1+2*dx/3, by=y1+2*dy/3;
  let mx=(ax+bx)/2, my=(ay+by)/2;
  let offX=(Math.sqrt(3)/2)*(by-ay)*turnSign;
  let offY=-(Math.sqrt(3)/2)*(bx-ax)*turnSign;
  return {
    a:{x:ax,y:ay},
    peak:{x:mx+offX,y:my+offY},
    b:{x:bx,y:by}
  };
}

function kochPoints(x1,y1,x2,y2,n,turnSign=1){
  if(n===0) return [{x:x1,y:y1},{x:x2,y:y2}];
  let {a,peak,b}=kochSubdivision(x1,y1,x2,y2,turnSign);
  return [
    ...kochPoints(x1,y1,a.x,a.y,n-1,turnSign).slice(0,-1),
    ...kochPoints(a.x,a.y,peak.x,peak.y,n-1,turnSign).slice(0,-1),
    ...kochPoints(peak.x,peak.y,b.x,b.y,n-1,turnSign).slice(0,-1),
    ...kochPoints(b.x,b.y,x2,y2,n-1,turnSign)
  ];
}

function kochOutwardTurnSign(a,b,center){
  let up=kochSubdivision(a.x,a.y,b.x,b.y,1).peak;
  let down=kochSubdivision(a.x,a.y,b.x,b.y,-1).peak;
  let upDist=(up.x-center.x)*(up.x-center.x)+(up.y-center.y)*(up.y-center.y);
  let downDist=(down.x-center.x)*(down.x-center.x)+(down.y-center.y)*(down.y-center.y);
  return upDist>=downDist ? 1 : -1;
}

function drawKoch(n){
  n=parseInt(n);
  document.getElementById('koch-vis-badge').textContent=n;
  document.getElementById('koch-canvas-label').textContent=`${n}단계 ` + (kochVisMode==='snow'?'코흐 눈송이':'코흐 곡선');
  let canvas=document.getElementById('koch-canvas');
  let W=canvas.clientWidth||600;
  // 코흐 곡선은 위로 자람 -> 높이를 충분히 확보
  let H=Math.round(W*0.65);
  canvas.width=W; canvas.height=H;
  let ctx=canvas.getContext('2d');
  ctx.fillStyle='#f8fafc';
  ctx.fillRect(0,0,W,H);
  ctx.lineWidth=Math.max(1, 2-n*0.25);

  if(kochVisMode==='snow'){
    let pad=W*0.10;
    let sideLen=W-2*pad;
    let triH=sideLen*Math.sqrt(3)/2;
    let maxSide=(H*0.75)/Math.sqrt(3)*2;
    if(sideLen>maxSide){ sideLen=maxSide; triH=sideLen*Math.sqrt(3)/2; }
    let cx=W/2;
    let centY=H*0.52;
    let p0={x:cx,           y:centY-triH*2/3};
    let p1={x:cx+sideLen/2, y:centY+triH/3};
    let p2={x:cx-sideLen/2, y:centY+triH/3};
    let center={x:(p0.x+p1.x+p2.x)/3, y:(p0.y+p1.y+p2.y)/3};
    let sides=[
      [p0,p1],[p1,p2],[p2,p0]
    ];
    let allPts=[];
    for(let [a,b] of sides){
      let turnSign=kochOutwardTurnSign(a,b,center);
      let seg=kochPoints(a.x,a.y,b.x,b.y,n,turnSign);
      allPts=allPts.concat(seg.slice(0,-1));
    }
    ctx.beginPath();
    ctx.strokeStyle='#1e40af';
    ctx.fillStyle='#dbeafe';
    allPts.forEach((p,i)=>i===0?ctx.moveTo(p.x,p.y):ctx.lineTo(p.x,p.y));
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
  } else {
    // 코흐 곡선: 기본선을 아래쪽에 두고 위로 돌출
    let margin=W*0.07;
    // 기본선 y를 아래쪽으로 (H의 75% 위치)
    // n단계에서 최대 높이 ≈ (√3/2)*(4/3)^n * lineLen/3 이므로 여유 확보
    let baseY=H*0.78;
    let pts=kochPoints(margin, baseY, W-margin, baseY, n, 1);
    ctx.beginPath();
    ctx.strokeStyle='#3b82f6';
    pts.forEach((p,i)=>i===0?ctx.moveTo(p.x,p.y):ctx.lineTo(p.x,p.y));
    ctx.stroke();
  }
}

// ═══════════════════════════════════════════
// 칸토어 집합 계산
// ═══════════════════════════════════════════
function updateCantor(n){
  n=parseInt(n);
  document.getElementById('cantor-n-badge').textContent=n;
  document.getElementById('cantor-cur-n').textContent=n;
  let tbody=document.getElementById('cantor-tbody');
  tbody.innerHTML='';
  for(let i=0;i<=n;i++){
    let cnt=Math.pow(2,i);
    let segLen=Math.pow(1/3,i);
    let total=Math.pow(2/3,i);
    let tr=document.createElement('tr');
    if(i===n)tr.className='highlight';
    tr.innerHTML=`<td>${i}</td><td class="val-blue">${cnt}</td><td>${segLen.toFixed(6)}</td><td class="val-green">${total.toFixed(6)}</td>`;
    tbody.appendChild(tr);
  }
  let cnt=Math.pow(2,n);
  let segLen=Math.pow(1/3,n);
  let total=Math.pow(2/3,n);
  document.getElementById('cantor-cnt').textContent=cnt;
  document.getElementById('cantor-cnt-expr').textContent=`= 2^${n} = ${cnt}`;
  document.getElementById('cantor-seg-len').textContent=segLen.toFixed(6);
  document.getElementById('cantor-seg-expr').textContent=`= (1/3)^${n}`;
  document.getElementById('cantor-total').textContent=total.toFixed(6);
  document.getElementById('cantor-total-expr').textContent=`= (2/3)^${n}`;
}

// ═══════════════════════════════════════════
// 칸토어 집합 시각화
// ═══════════════════════════════════════════
function drawCantor(n){
  n=parseInt(n);
  document.getElementById('cantor-vis-badge').textContent=n;
  let canvas=document.getElementById('cantor-canvas');
  let W=canvas.clientWidth||600;
  let levels=n+1;
  let rowH=Math.max(18, Math.min(30, 220/levels));
  canvas.width=W; canvas.height=rowH*levels+20;
  let ctx=canvas.getContext('2d');
  ctx.fillStyle='#0f172a'; ctx.fillRect(0,0,W,canvas.height);

  function drawLevel(segs, row){
    let y=row*rowH+10;
    let barH=rowH*0.5;
    // removed segments shown faintly
    ctx.fillStyle='#1e293b';
    ctx.fillRect(0, y, W, barH);
    segs.forEach(seg=>{
      let x1=seg[0]*W, x2=seg[1]*W;
      ctx.fillStyle='#3b82f6';
      ctx.fillRect(x1+1, y+1, x2-x1-2, barH-2);
    });
    // label
    ctx.fillStyle='#475569';
    ctx.font=`${Math.min(11,rowH*0.4)}px sans-serif`;
    ctx.textAlign='right';
    ctx.fillText(`n=${row}`, W-4, y+barH*0.7+2);
  }

  // build segments
  let segs=[[0,1]];
  drawLevel(segs,0);
  for(let i=1;i<=n;i++){
    let newSegs=[];
    segs.forEach(s=>{
      let len=(s[1]-s[0])/3;
      newSegs.push([s[0], s[0]+len]);
      newSegs.push([s[0]+2*len, s[1]]);
    });
    segs=newSegs;
    drawLevel(segs,i);
  }
}

let cantorAnim=null;
function animateCantor(){
  if(cantorAnim)clearInterval(cantorAnim);
  let n=0,el=document.getElementById('cantor-vis-n');
  cantorAnim=setInterval(()=>{
    el.value=n; drawCantor(n); updateCantor(n);
    document.getElementById('cantor-vis-badge').textContent=n;
    n++; if(n>7){clearInterval(cantorAnim);cantorAnim=null;}
  },600);
}

// ═══════════════════════════════════════════
// 프랙털 차원 탭
// ═══════════════════════════════════════════
function showDim(id){
  ['menger','koch','cantor'].forEach(x=>{
    let el=document.getElementById('dim-'+x);
    if(el) el.style.display=(x===id?'block':'none');
    let btn=document.getElementById('dim-'+x+'-btn');
    if(btn)btn.className='btn '+(x===id?'btn-blue':'btn-gray');
  });
}

function calcDim(){
  let k=parseInt(document.getElementById('dim-k').value);
  let N=parseInt(document.getElementById('dim-N').value);
  document.getElementById('dim-k-val').textContent=k;
  document.getElementById('dim-N-val').textContent=N;
  document.getElementById('dim-k-disp').textContent=k;
  document.getElementById('dim-N-disp').textContent=N;
  let d=Math.log(N)/Math.log(k);
  document.getElementById('dim-result').textContent=d.toFixed(4);
  let interp='';
  if(d<0.5) interp='매우 희박 — 점에 가깝습니다';
  else if(d<1) interp='0차원 ~ 1차원 사이 (칸토어 집합 유형)';
  else if(d<1.5) interp='1차원 ~ 1.5차원 사이';
  else if(d<2) interp='1차원 ~ 2차원 사이 (코흐 곡선 유형)';
  else if(d<2.5) interp='2차원 ~ 2.5차원 사이';
  else if(d<3) interp='2차원 ~ 3차원 사이 (멩거 스펀지 유형)';
  else interp='3차원 이상 — 일반 부피와 비슷';
  document.getElementById('dim-interp').textContent=interp;
  // bar: d/3 비율
  let pct=Math.min(100,Math.max(0,d/3*100));
  document.getElementById('dim-bar').style.width=pct+'%';
}

// ═══════════════════════════════════════════
// 퀴즈 공통 로직
// ═══════════════════════════════════════════
function checkQuiz(optsId, fbId, el, status){
  let opts=document.getElementById(optsId);
  if(opts.classList.contains('answered'))return;
  opts.classList.add('answered');
  opts.querySelectorAll('.quiz-opt').forEach(o=>{
    o.classList.add('answered');
    if(o.getAttribute('onclick')&&o.getAttribute('onclick').includes("'correct'")) o.classList.add('reveal');
  });
  el.classList.add(status);
  let fb=document.getElementById(fbId);
  fb.className='quiz-feedback show '+(status==='correct'?'ok':'ng');
  fb.textContent=status==='correct'?'✅ 정답입니다! 잘했어요!':'❌ 아쉬워요. 초록색 선택지가 정답입니다.';
}
function checkMQ(q,el,s){checkQuiz('mq'+q+'-opts','mq'+q+'-fb',el,s);}
function checkKQ(q,el,s){checkQuiz('kq'+q+'-opts','kq'+q+'-fb',el,s);}
function checkCQ(q,el,s){checkQuiz('cq'+q+'-opts','cq'+q+'-fb',el,s);}
function checkDQ(q,el,s){checkQuiz('dq'+q+'-opts','dq'+q+'-fb',el,s);}

// ═══════════════════════════════════════════
// 숫자 포맷
// ═══════════════════════════════════════════
function fmt(n){return n>=1e7?n.toExponential(2):n.toLocaleString();}

// ═══════════════════════════════════════════
// 초기화
// ═══════════════════════════════════════════
window.addEventListener('load',()=>{
  updateMenger(0);
  drawMenger(0);
  menger3dRotAngle=Math.PI/6;
  drawMenger3D(0);
  updateKoch(0);
  drawKoch(0);
  updateCantor(0);
  drawCantor(0);
  calcDim();
});
window.addEventListener('resize',()=>{
  let mn=document.getElementById('menger-vis-n').value;
  drawMenger(mn);
  let mn3=document.getElementById('menger3d-n').value;
  drawMenger3D(mn3);
  let kn=document.getElementById('koch-vis-n').value;
  drawKoch(kn);
  let cn=document.getElementById('cantor-vis-n').value;
  drawCantor(cn);
});
</script>
</body>
</html>
"""


def render():
    st.title("🔬 프랙털 — 길이·넓이·부피와 차원 탐구")
    st.caption("멩거 스펀지 · 코흐 곡선 · 칸토어 집합의 단계별 측정값을 탐구하고, 프랙털 차원 개념을 발견해 봅니다.")
    components.html(HTML, height=4000, scrolling=True)
