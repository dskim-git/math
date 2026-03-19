import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 시에르핀스키 삼각형 — 단계별 분석",
    "description": "단계별 삼각형 개수·넓이·둘레를 직접 탐구하며 수열 공식과 프랙털 차원을 발견합니다.",
    "order": 24,
    "hidden": True,
}

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR','Segoe UI',sans-serif;background:#0f172a;color:#e2e8f0;}
#app{max-width:900px;margin:0 auto;padding:12px;}

/* ── 탭 ── */
.tabs{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:14px;}
.tab-btn{
  padding:7px 15px;border-radius:20px;border:1.5px solid #334155;
  background:#1e293b;font-size:0.82rem;font-weight:700;
  cursor:pointer;color:#94a3b8;transition:all .15s;
}
.tab-btn:hover:not(.active){border-color:#64748b;color:#e2e8f0;}
.tab-btn.active{background:#b45309;color:#fff;border-color:#f59e0b;}
.tab-btn.quiz-tab.active{background:#7c3aed;border-color:#a78bfa;}
.pane{display:none;}.pane.active{display:block;}

/* ── 단계 버튼 ── */
.step-bar{display:flex;gap:8px;align-items:center;margin-bottom:12px;flex-wrap:wrap;}
.step-label{font-size:0.83rem;color:#94a3b8;font-weight:600;}
.step-btn{
  width:40px;height:40px;border-radius:50%;border:2.5px solid #334155;
  background:#1e293b;color:#94a3b8;cursor:pointer;
  font-size:0.88rem;font-weight:700;transition:all .15s;
  display:flex;align-items:center;justify-content:center;
}
.step-btn.active{background:#f59e0b;color:#0f172a;border-color:#fbbf24;box-shadow:0 0 12px #f59e0b66;}
.step-btn:hover:not(.active){border-color:#f59e0b;color:#fbbf24;}

/* ── SVG 캔버스 ── */
#svgWrap{
  background:#1e293b;border-radius:14px;padding:10px;
  margin-bottom:12px;text-align:center;border:1px solid #334155;
}
#svgWrap svg{max-width:100%;height:auto;}

/* ── 통계 카드 ── */
.stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px;}
.stat-card{
  background:#1e293b;border-radius:10px;padding:12px;text-align:center;
  border:1px solid #334155;
}
.stat-label{font-size:0.71rem;color:#64748b;margin-bottom:4px;}
.stat-val{font-size:1.35rem;font-weight:900;color:#fbbf24;margin-bottom:2px;}
.stat-formula{font-size:0.7rem;color:#94a3b8;}

/* ── 표 탐구 ── */
.table-section{margin-bottom:16px;}
.table-title{font-size:0.97rem;font-weight:700;color:#f1f5f9;margin-bottom:8px;}
.prop-table{width:100%;border-collapse:collapse;}
.prop-table th{
  background:#92400e;color:#fef3c7;padding:9px 8px;
  font-size:0.82rem;font-weight:700;text-align:center;
  border:1px solid #b45309;
}
.prop-table td{
  background:#1e293b;border:1px solid #334155;
  padding:10px 6px;text-align:center;font-size:0.88rem;color:#cbd5e1;
}
.prop-table td.hdr{background:#1c1917;color:#d4a97a;font-weight:700;font-size:0.8rem;}
.rcell{
  cursor:pointer;color:#475569;font-size:1.2rem;
  transition:all .15s;user-select:none;
}
.rcell:hover{color:#fbbf24;transform:scale(1.2);}
.rcell.revealed{color:#6ee7b7;cursor:default;font-size:0.9rem;font-weight:700;}
.reveal-btn{
  margin-top:6px;padding:5px 14px;border-radius:8px;
  border:1.5px solid #f59e0b;background:transparent;
  color:#fbbf24;cursor:pointer;font-size:0.78rem;font-weight:700;
  transition:all .15s;
}
.reveal-btn:hover{background:#78350f;}
.hint-box{
  background:#1e293b;border-radius:10px;padding:11px 14px;
  font-size:0.78rem;color:#64748b;line-height:1.8;margin-top:8px;
  border-left:3px solid #f59e0b;
}

/* ── 공식 카드 ── */
.f-card{
  background:#1e293b;border-radius:12px;padding:14px 16px;
  border-left:4px solid #f59e0b;margin-bottom:10px;
}
.f-title{font-size:0.85rem;font-weight:700;color:#fbbf24;margin-bottom:7px;}
.f-formula{
  font-size:1.05rem;color:#e2e8f0;font-weight:700;
  background:#0f172a;padding:7px 14px;border-radius:8px;
  display:inline-block;margin-bottom:7px;font-family:'Courier New',monospace;
}
.f-explain{font-size:0.78rem;color:#94a3b8;line-height:1.75;}
.f-limit{font-size:0.8rem;color:#f87171;margin-top:5px;font-weight:600;}
.dim-card{
  background:#1e293b;border-radius:12px;padding:14px;
  border:1px solid #7c3aed;margin-bottom:10px;
}
.dim-eq{font-size:1.2rem;font-weight:900;color:#c084fc;text-align:center;padding:8px 0;}
.dim-sub{font-size:0.79rem;color:#94a3b8;text-align:center;line-height:1.8;}

/* ── 계산기 ── */
.calc-box{background:#1e293b;border-radius:12px;padding:14px;margin-top:10px;}
.calc-title{font-size:0.9rem;font-weight:700;color:#f1f5f9;margin-bottom:10px;}
.calc-row{display:flex;align-items:center;gap:8px;margin-bottom:7px;flex-wrap:wrap;}
.calc-lbl{font-size:0.82rem;color:#94a3b8;min-width:80px;}
.calc-input{
  width:72px;padding:5px 8px;border-radius:7px;
  border:1.5px solid #334155;background:#0f172a;
  color:#e2e8f0;font-size:0.95rem;font-weight:700;text-align:center;
}
.calc-result{
  font-size:0.88rem;color:#6ee7b7;font-weight:700;
  background:#0f172a;padding:4px 12px;border-radius:6px;
}
.calc-btn{
  padding:6px 16px;border-radius:8px;border:none;
  background:#b45309;color:#fff;cursor:pointer;
  font-size:0.82rem;font-weight:700;transition:background .15s;
}
.calc-btn:hover{background:#92400e;}

/* ── 퀴즈 ── */
.q-card{
  background:#1e293b;border-radius:11px;padding:13px 14px;margin-bottom:11px;
  border:2px solid transparent;transition:border-color .2s;
}
.q-card.correct{border-color:#059669;}
.q-card.wrong{border-color:#dc2626;}
.q-num{font-size:0.68rem;color:#64748b;font-weight:700;text-transform:uppercase;margin-bottom:5px;}
.q-text{font-size:0.86rem;color:#e2e8f0;margin-bottom:9px;line-height:1.5;}
.q-choices{display:flex;flex-direction:column;gap:5px;}
.q-choice{
  padding:7px 11px;border-radius:7px;border:1.5px solid #334155;
  background:#0f172a;color:#cbd5e1;cursor:pointer;font-size:0.81rem;
  text-align:left;transition:all .15s;
}
.q-choice:hover:not(:disabled){border-color:#f59e0b;color:#fff;background:#1c1917;}
.q-choice.sel-correct{background:#064e3b;border-color:#10b981;color:#6ee7b7;}
.q-choice.sel-wrong{background:#450a0a;border-color:#f87171;color:#fca5a5;}
.q-choice.show-ans{background:#064e3b;border-color:#10b981;color:#6ee7b7;}
.q-choice:disabled{cursor:default;}
.q-fb{font-size:0.79rem;margin-top:7px;padding:5px 9px;border-radius:5px;}
.q-fb.correct{background:#064e3b;color:#6ee7b7;}
.q-fb.wrong{background:#450a0a;color:#fca5a5;}
.score-box{
  background:#1e293b;border-radius:11px;padding:14px;
  text-align:center;margin-top:8px;
}
.score-big{font-size:2rem;font-weight:900;color:#fbbf24;}
.score-msg{font-size:0.84rem;color:#94a3b8;margin-top:4px;}
.re-btn{
  display:inline-block;margin-top:10px;padding:7px 18px;
  background:#7c3aed;color:#fff;border-radius:8px;border:none;
  cursor:pointer;font-weight:700;font-size:0.83rem;
}

/* ── 차원 원리 탭 ── */
.tab-btn.dim-tab.active{background:#6d28d9;border-color:#8b5cf6;}
.concept-card{background:#13001e;border:1px solid #7c3aed;border-radius:12px;padding:14px;margin-bottom:12px;}
.concept-title{font-size:0.9rem;font-weight:700;color:#c084fc;margin-bottom:8px;}
.concept-body{font-size:0.82rem;color:#e2e8f0;line-height:1.75;margin-bottom:8px;}
.concept-eq{font-size:1.1rem;font-weight:900;color:#a78bfa;background:#0f172a;padding:8px 14px;border-radius:8px;text-align:center;margin-bottom:6px;}
.concept-sub{font-size:0.78rem;color:#94a3b8;text-align:center;}
.sc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px;}
@media(max-width:580px){.sc-grid{grid-template-columns:1fr;}}
.sc-card{background:#1e293b;border-radius:11px;padding:10px;border:1px solid #334155;text-align:center;}
.sc-fractal{border-color:#7c3aed;background:#13001e;}
.sc-name{font-size:0.78rem;font-weight:700;color:#f1f5f9;margin-bottom:6px;}
.sc-eq{font-size:0.82rem;color:#fbbf24;margin-top:6px;font-weight:700;}
.sc-eq-frac{color:#c084fc;}
.derive-card{background:#1e293b;border-radius:12px;padding:14px;margin-bottom:12px;border-left:4px solid #7c3aed;}
.derive-title{font-size:0.88rem;font-weight:700;color:#c084fc;margin-bottom:10px;}
.d-step{font-size:0.82rem;color:#e2e8f0;padding:7px 10px;background:#0f172a;border-radius:7px;margin-bottom:5px;line-height:1.65;}
.derive-note{font-size:0.8rem;color:#a78bfa;margin-top:8px;text-align:center;font-weight:600;}
.dim-calc{background:#1e293b;border-radius:12px;padding:14px;}
.dim-calc-title{font-size:0.9rem;font-weight:700;color:#f1f5f9;margin-bottom:10px;}
.dc-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;}
.dc-lbl{font-size:0.82rem;color:#94a3b8;}
.dim-input{width:65px;padding:5px 8px;border-radius:7px;border:1.5px solid #334155;background:#0f172a;color:#e2e8f0;font-size:0.9rem;font-weight:700;text-align:center;}
.dim-btn{padding:6px 16px;border-radius:8px;border:none;background:#7c3aed;color:#fff;cursor:pointer;font-size:0.82rem;font-weight:700;transition:background .15s;}
.dim-btn:hover{background:#6d28d9;}
.dc-result-eq{font-size:1rem;font-weight:700;color:#c084fc;padding:8px 12px;background:#0f172a;border-radius:8px;margin:8px 0;}
.dc-interpret{font-size:0.8rem;color:#94a3b8;margin-top:3px;line-height:1.7;}
.dc-presets{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px;align-items:center;}
.dc-plbl{font-size:0.78rem;color:#64748b;margin-right:2px;}
.dc-preset{padding:4px 10px;border-radius:6px;border:1px solid #334155;background:#0f172a;color:#94a3b8;cursor:pointer;font-size:0.76rem;font-weight:600;transition:all .15s;}
.dc-preset:hover{border-color:#7c3aed;color:#c084fc;background:#1a0033;}
.compare-note{background:#0f172a;border-radius:10px;padding:10px 14px;font-size:0.78rem;color:#64748b;margin-bottom:12px;line-height:1.8;border-left:3px solid #7c3aed;}
</style>
</head>
<body>
<div id="app">

<!-- 탭 -->
<div class="tabs">
  <button class="tab-btn active" data-tab="viz">🔺 시각화</button>
  <button class="tab-btn" data-tab="table">📊 표 탐구</button>
  <button class="tab-btn dim-tab" data-tab="dim">🌀 차원 원리</button>
  <button class="tab-btn" data-tab="formula">📐 일반화</button>
  <button class="tab-btn quiz-tab" data-tab="quiz">🎯 퀴즈</button>
</div>

<!-- 시각화 -->
<div id="pane-viz" class="pane active">
  <div class="step-bar">
    <span class="step-label">단계 선택:</span>
    <button class="step-btn active" data-step="0">0</button>
    <button class="step-btn" data-step="1">1</button>
    <button class="step-btn" data-step="2">2</button>
    <button class="step-btn" data-step="3">3</button>
    <button class="step-btn" data-step="4">4</button>
  </div>
  <div id="svgWrap"></div>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-label">삼각형 개수</div>
      <div class="stat-val" id="st-count">1</div>
      <div class="stat-formula" id="st-count-f">3⁰ = 1</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">넓이 (S₀ = 1)</div>
      <div class="stat-val" id="st-area">1</div>
      <div class="stat-formula" id="st-area-f">(3/4)⁰ = 1</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">둘레의 합 (변 = 1)</div>
      <div class="stat-val" id="st-peri">3</div>
      <div class="stat-formula" id="st-peri-f">3×(3/2)⁰ = 3</div>
    </div>
  </div>
</div>

<!-- 표 탐구 -->
<div id="pane-table" class="pane">
  <div class="table-section">
    <div class="table-title">① 삼각형의 개수</div>
    <table class="prop-table">
      <tr><th>단계</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th></tr>
      <tr>
        <td class="hdr">개수</td>
        <td class="rcell" data-val="1" data-g="c">?</td>
        <td class="rcell" data-val="3" data-g="c">?</td>
        <td class="rcell" data-val="9" data-g="c">?</td>
        <td class="rcell" data-val="27" data-g="c">?</td>
        <td class="rcell" data-val="81" data-g="c">?</td>
      </tr>
    </table>
    <button class="reveal-btn" data-g="c">모두 보기</button>
  </div>

  <div class="table-section">
    <div class="table-title">② 삼각형의 넓이 (S₀ = 1)</div>
    <table class="prop-table">
      <tr><th>단계</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th></tr>
      <tr>
        <td class="hdr">넓이</td>
        <td class="rcell" data-val="1" data-g="a">?</td>
        <td class="rcell" data-val="3/4" data-g="a">?</td>
        <td class="rcell" data-val="9/16" data-g="a">?</td>
        <td class="rcell" data-val="27/64" data-g="a">?</td>
        <td class="rcell" data-val="81/256" data-g="a">?</td>
      </tr>
    </table>
    <button class="reveal-btn" data-g="a">모두 보기</button>
  </div>

  <div class="table-section">
    <div class="table-title">③ 삼각형의 둘레의 합 (한 변의 길이 = 1)</div>
    <table class="prop-table">
      <tr><th>단계</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th></tr>
      <tr>
        <td class="hdr">둘레의 합</td>
        <td class="rcell" data-val="3" data-g="p">?</td>
        <td class="rcell" data-val="9/2" data-g="p">?</td>
        <td class="rcell" data-val="27/4" data-g="p">?</td>
        <td class="rcell" data-val="81/8" data-g="p">?</td>
        <td class="rcell" data-val="243/16" data-g="p">?</td>
      </tr>
    </table>
    <button class="reveal-btn" data-g="p">모두 보기</button>
  </div>

  <div class="hint-box">
    💡 <strong style="color:#fbbf24">힌트</strong>: 매 단계마다 삼각형은 <strong style="color:#fbbf24">3배</strong>로 늘어나고,
    각 삼각형의 한 변의 길이는 <strong style="color:#fbbf24">1/2배</strong>가 됩니다.
    따라서 넓이는 (1/2)² = 1/4배, 둘레의 합의 각 항은 1/2배가 됩니다.
    <br>각 셀을 클릭하면 답이 공개됩니다.
  </div>
</div>

<!-- 차원 원리 -->
<div id="pane-dim" class="pane">
  <div class="concept-card">
    <div class="concept-title">💡 차원을 구하는 핵심 원리</div>
    <div class="concept-body">
      어떤 도형을 <strong>r배 확대</strong>하면 원래 도형과 똑같은 <strong>복사본이 N개</strong> 생긴다고 할 때,
      이 도형의 차원 D는 다음과 같이 정의됩니다.
    </div>
    <div class="concept-eq">r<sup>D</sup> = N &nbsp;⟹&nbsp; D = log N / log r = log<sub>r</sub>N</div>
    <div class="concept-sub">D가 정수(1, 2, 3)이면 보통 도형 &nbsp;|&nbsp; D가 소수이면 프랙털!</div>
  </div>

  <div class="sc-grid">
    <div class="sc-card">
      <div class="sc-name">선분 (1차원)</div>
      <div id="svgLine"></div>
      <div class="sc-eq">r=2, N=2 &nbsp;→&nbsp; <strong>D = 1</strong></div>
    </div>
    <div class="sc-card">
      <div class="sc-name">정삼각형 (2차원)</div>
      <div id="svgTriComp"></div>
      <div class="sc-eq">r=2, N=4 &nbsp;→&nbsp; <strong>D = 2</strong></div>
    </div>
    <div class="sc-card sc-fractal">
      <div class="sc-name">시에르핀스키 (프랙털!)</div>
      <div id="svgSierComp"></div>
      <div class="sc-eq sc-eq-frac">r=2, N=3 &nbsp;→&nbsp; <strong>D ≈ 1.585</strong></div>
    </div>
  </div>

  <div class="compare-note">
    🔑 정삼각형을 2배 확대하면 <strong style="color:#fbbf24">4개</strong>의 복사본(색깔 구분)이 생기지만,
    시에르핀스키 삼각형은 가운데를 제거했기 때문에 <strong style="color:#c084fc">3개</strong>만 생깁니다.
    (오른쪽 그림의 점선 삼각형 = 제거된 자리)<br>
    이 차이 하나가 비정수 차원(≈1.585)을 만들어냅니다!
  </div>

  <div class="derive-card">
    <div class="derive-title">🔍 시에르핀스키 삼각형 차원 계산 과정</div>
    <div class="d-step">① 크기를 <strong>2배</strong> 확대하면 자기 자신과 닮은 복사본이 <strong>3개</strong> 생깁니다.</div>
    <div class="d-step">② 차원의 정의에 대입: &nbsp;&nbsp; 2<sup>D</sup> = 3</div>
    <div class="d-step">③ 양변에 로그 적용: &nbsp;&nbsp; D · log 2 = log 3</div>
    <div class="d-step">④ 양변을 log 2로 나누기: &nbsp;&nbsp; D = log 3 / log 2 = log<sub>2</sub>3</div>
    <div class="d-step" style="border-left:3px solid #c084fc;">
      ⑤ 계산 결과: &nbsp;&nbsp; D = log<sub>2</sub>3 ≈ <strong style="color:#c084fc;font-size:1rem">1.5849…</strong>
      &nbsp;&nbsp;&nbsp; (1차원과 2차원 사이!)
    </div>
    <div class="derive-note">넓이는 0이지만 선도 아닌 — 차원 ≈ 1.59의 프랙털!</div>
  </div>

  <div class="dim-calc">
    <div class="dim-calc-title">🧮 프랙털 차원 계산기</div>
    <div class="dc-row">
      <span class="dc-lbl">배율 r =</span>
      <input id="dimR" type="number" class="dim-input" value="2" min="1.01" step="0.5">
      <span class="dc-lbl" style="margin-left:10px">복사본 수 N =</span>
      <input id="dimN" type="number" class="dim-input" value="3" min="2" step="1">
      <button id="dimBtn" class="dim-btn">계산</button>
    </div>
    <div id="dimResult" style="display:none">
      <div class="dc-result-eq">D = log N / log r = <span id="dimOut"></span></div>
      <div class="dc-interpret" id="dimInterp"></div>
    </div>
    <div class="dc-presets">
      <span class="dc-plbl">예시:</span>
      <button class="dc-preset" data-r="2" data-n="2">선분</button>
      <button class="dc-preset" data-r="2" data-n="4">정삼각형</button>
      <button class="dc-preset" data-r="3" data-n="9">정사각형</button>
      <button class="dc-preset" data-r="2" data-n="3">시에르핀스키</button>
      <button class="dc-preset" data-r="3" data-n="20">멩거 스펀지</button>
      <button class="dc-preset" data-r="3" data-n="4">코흐 곡선</button>
    </div>
  </div>
</div>

<!-- 일반화 -->
<div id="pane-formula" class="pane">
  <div class="f-card">
    <div class="f-title">🔢 삼각형의 개수</div>
    <div class="f-formula">aₙ = 3ⁿ</div>
    <div class="f-explain">
      단계 0: 1개 → 단계 1: 3개 → 단계 2: 9개 → …<br>
      매 단계마다 각 삼각형이 3개의 더 작은 삼각형으로 분열됩니다.
    </div>
    <div class="f-limit">n → ∞ 이면 aₙ → ∞ &nbsp;(삼각형 개수가 무한히 증가!)</div>
  </div>

  <div class="f-card">
    <div class="f-title">📐 삼각형의 넓이 (S₀ = 1)</div>
    <div class="f-formula">Sₙ = (3/4)ⁿ</div>
    <div class="f-explain">
      한 변이 1/2배 → 넓이는 (1/2)² = <strong style="color:#fbbf24">1/4</strong>배<br>
      개수는 <strong style="color:#fbbf24">3</strong>배 증가 → Sₙ = 3ⁿ × (1/4)ⁿ = (3/4)ⁿ<br>
      단계 4: (3/4)⁴ = 81/256 ≈ 0.316
    </div>
    <div class="f-limit">n → ∞ 이면 Sₙ → 0 &nbsp;(넓이가 0에 수렴! 면적이 사라진다.)</div>
  </div>

  <div class="f-card">
    <div class="f-title">📏 둘레의 합 (한 변의 길이 = 1)</div>
    <div class="f-formula">Pₙ = 3 × (3/2)ⁿ</div>
    <div class="f-explain">
      n단계: 한 변 = (1/2)ⁿ, 개수 = 3ⁿ<br>
      Pₙ = 3ⁿ × 3 × (1/2)ⁿ = <strong style="color:#fbbf24">3 × (3/2)ⁿ</strong><br>
      단계 4: 3 × (3/2)⁴ = 243/16 ≈ 15.2
    </div>
    <div class="f-limit">n → ∞ 이면 Pₙ → ∞ &nbsp;(둘레가 무한히 증가!)</div>
  </div>

  <div class="dim-card">
    <div class="f-title" style="text-align:center;margin-bottom:8px">🌀 프랙털 차원</div>
    <div class="dim-eq">크기를 2배 확대 → 닮은 도형 3개 출현<br>2ˣ = 3 &nbsp;⟹&nbsp; x = log₂3 ≈ 1.585</div>
    <div class="dim-sub">
      1차원(선): 2¹ = 2개, 2차원(면): 2² = 4개 → 시에르핀스키는 그 사이!<br>
      <strong style="color:#c084fc">프랙털 차원 ≈ 1.59 (선도 아니고 면도 아닌 사이의 세계)</strong>
    </div>
  </div>

  <!-- 계산기 -->
  <div class="calc-box">
    <div class="calc-title">🧮 단계별 계산기</div>
    <div class="calc-row">
      <span class="calc-lbl">단계 n =</span>
      <input type="number" class="calc-input" id="calcN" value="5" min="0" max="30">
      <button class="calc-btn" id="calcBtn">계산하기</button>
    </div>
    <div id="calcOut" style="display:none">
      <div class="calc-row"><span class="calc-lbl">개수:</span><span class="calc-result" id="r-c"></span></div>
      <div class="calc-row"><span class="calc-lbl">넓이:</span><span class="calc-result" id="r-a"></span></div>
      <div class="calc-row"><span class="calc-lbl">둘레의 합:</span><span class="calc-result" id="r-p"></span></div>
    </div>
  </div>
</div>

<!-- 퀴즈 -->
<div id="pane-quiz" class="pane">
  <div id="quizArea"></div>
</div>

</div><!-- #app -->

<script>
(function(){
'use strict';

// ── 시에르핀스키 SVG 그리기 ──
const W = 480, H = 420, PAD = 22;
const AX = W/2, AY = PAD;      // 꼭대기
const BX = PAD, BY = H - PAD;  // 왼쪽 아래
const CX = W - PAD, CY = H - PAD; // 오른쪽 아래

function getTriangles(depth, ax,ay,bx,by,cx,cy){
  if(depth===0) return [[ax,ay,bx,by,cx,cy]];
  const mx1=(ax+bx)/2, my1=(ay+by)/2;
  const mx2=(ax+cx)/2, my2=(ay+cy)/2;
  const mx3=(bx+cx)/2, my3=(by+cy)/2;
  return [
    ...getTriangles(depth-1, ax,ay, mx1,my1, mx2,my2),
    ...getTriangles(depth-1, mx1,my1, bx,by, mx3,my3),
    ...getTriangles(depth-1, mx2,my2, mx3,my3, cx,cy),
  ];
}

function drawSVG(step){
  const tris = getTriangles(step, AX,AY, BX,BY, CX,CY);
  const sw = Math.max(0.4, 1.6 - step*0.3);
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">`;
  s += `<rect width="${W}" height="${H}" fill="#0f172a" rx="10"/>`;
  // 외곽 점선 삼각형
  s += `<polygon points="${AX},${AY} ${BX},${BY} ${CX},${CY}" fill="none" stroke="#1e3a5f" stroke-width="1.5" stroke-dasharray="6 4"/>`;
  for(const [ax,ay,bx,by,cx,cy] of tris){
    s += `<polygon points="${ax},${ay} ${bx},${by} ${cx},${cy}" fill="#b45309" stroke="#fbbf24" stroke-width="${sw}"/>`;
  }
  s += '</svg>';
  document.getElementById('svgWrap').innerHTML = s;
}

// ── 통계 업데이트 ──
function p3(n){let r=1;for(let i=0;i<n;i++)r*=3;return r;}
function p4(n){let r=1;for(let i=0;i<n;i++)r*=4;return r;}
function p2(n){let r=1;for(let i=0;i<n;i++)r*=2;return r;}
function gcd(a,b){return b===0?a:gcd(b,a%b);}
function toFrac(num,den){
  const g=gcd(num,den);
  const n2=num/g, d2=den/g;
  return d2===1 ? `${n2}` : `${n2}/${d2}`;
}

function updateStats(n){
  const cnt = p3(n);
  const aStr = toFrac(p3(n), p4(n));
  const pStr = toFrac(3*p3(n), p2(n));
  document.getElementById('st-count').textContent = cnt;
  document.getElementById('st-count-f').textContent = `3^${n} = ${cnt}`;
  document.getElementById('st-area').textContent = aStr;
  document.getElementById('st-area-f').textContent = `(3/4)^${n}`;
  document.getElementById('st-peri').textContent = pStr;
  document.getElementById('st-peri-f').textContent = `3×(3/2)^${n}`;
}

function setStep(step){
  document.querySelectorAll('.step-btn').forEach(b=>b.classList.toggle('active',+b.dataset.step===step));
  drawSVG(step);
  updateStats(step);
}
document.querySelectorAll('.step-btn').forEach(b=>{
  b.addEventListener('click',()=>setStep(+b.dataset.step));
});

// ── 표 탐구 ──
document.querySelectorAll('.rcell').forEach(cell=>{
  cell.addEventListener('click',function(){
    if(this.classList.contains('revealed'))return;
    this.textContent = this.dataset.val;
    this.classList.add('revealed');
  });
});
document.querySelectorAll('.reveal-btn').forEach(btn=>{
  btn.addEventListener('click',function(){
    const g = this.dataset.g;
    document.querySelectorAll(`.rcell[data-g="${g}"]`).forEach(c=>{
      if(!c.classList.contains('revealed')){
        c.textContent=c.dataset.val;
        c.classList.add('revealed');
      }
    });
  });
});

// ── 차원 원리 탭 SVG ──
function polyStr(t){return `${t[0]},${t[1]} ${t[2]},${t[3]} ${t[4]},${t[5]}`;}

function drawLineSVG(){
  let s=`<svg viewBox="0 0 260 78" width="100%">`;
  s+=`<rect width="260" height="78" fill="#0f172a" rx="8"/>`;
  s+=`<text x="52" y="16" text-anchor="middle" font-size="9" fill="#64748b">r배 확대 전</text>`;
  s+=`<line x1="12" y1="42" x2="92" y2="42" stroke="#3b82f6" stroke-width="5" stroke-linecap="round"/>`;
  s+=`<text x="52" y="60" text-anchor="middle" font-size="9" fill="#60a5fa">① 1개</text>`;
  s+=`<text x="115" y="46" text-anchor="middle" font-size="16" fill="#475569">→</text>`;
  s+=`<text x="115" y="61" text-anchor="middle" font-size="8" fill="#475569">×2배</text>`;
  s+=`<text x="192" y="16" text-anchor="middle" font-size="9" fill="#64748b">2배 확대 후</text>`;
  s+=`<line x1="138" y1="42" x2="192" y2="42" stroke="#f59e0b" stroke-width="5" stroke-linecap="round"/>`;
  s+=`<line x1="192" y1="42" x2="246" y2="42" stroke="#6ee7b7" stroke-width="5" stroke-linecap="round"/>`;
  s+=`<circle cx="138" cy="42" r="2.5" fill="#94a3b8"/>`;
  s+=`<circle cx="192" cy="42" r="2.5" fill="#94a3b8"/>`;
  s+=`<circle cx="246" cy="42" r="2.5" fill="#94a3b8"/>`;
  s+=`<text x="165" y="60" text-anchor="middle" font-size="8" fill="#f59e0b">①</text>`;
  s+=`<text x="219" y="60" text-anchor="middle" font-size="8" fill="#6ee7b7">②</text>`;
  s+=`<text x="192" y="73" text-anchor="middle" font-size="9" fill="#c084fc">N = 2개</text>`;
  s+='</svg>';
  return s;
}

function drawTriSVG(){
  let s=`<svg viewBox="0 0 260 128" width="100%">`;
  s+=`<rect width="260" height="128" fill="#0f172a" rx="8"/>`;
  s+=`<text x="52" y="14" text-anchor="middle" font-size="9" fill="#64748b">r배 확대 전</text>`;
  s+=`<polygon points="52,20 12,100 92,100" fill="#1d4ed8" stroke="#3b82f6" stroke-width="1.5"/>`;
  s+=`<text x="52" y="115" text-anchor="middle" font-size="9" fill="#60a5fa">1개</text>`;
  s+=`<text x="115" y="65" text-anchor="middle" font-size="16" fill="#475569">→</text>`;
  s+=`<text x="115" y="80" text-anchor="middle" font-size="8" fill="#475569">×2배</text>`;
  s+=`<text x="192" y="14" text-anchor="middle" font-size="9" fill="#64748b">2배 확대 후</text>`;
  const ax=192,ay=20,bx=137,by=100,cx=252,cy=100;
  const mx1=(ax+bx)/2,my1=(ay+by)/2;
  const mx2=(ax+cx)/2,my2=(ay+cy)/2;
  const mx3=(bx+cx)/2,my3=(by+cy)/2;
  s+=`<polygon points="${ax},${ay} ${mx1},${my1} ${mx2},${my2}" fill="#92400e" stroke="#f59e0b" stroke-width="1"/>`;
  s+=`<polygon points="${mx1},${my1} ${bx},${by} ${mx3},${my3}" fill="#064e3b" stroke="#10b981" stroke-width="1"/>`;
  s+=`<polygon points="${mx2},${my2} ${mx3},${my3} ${cx},${cy}" fill="#3b0764" stroke="#a78bfa" stroke-width="1"/>`;
  s+=`<polygon points="${mx1},${my1} ${mx2},${my2} ${mx3},${my3}" fill="#7f1d1d" stroke="#f87171" stroke-width="1"/>`;
  s+=`<text x="192" y="115" text-anchor="middle" font-size="9" fill="#94a3b8">N = 4개 (= 2²)</text>`;
  s+='</svg>';
  return s;
}

function drawSierSVG(){
  let s=`<svg viewBox="0 0 260 128" width="100%">`;
  s+=`<rect width="260" height="128" fill="#0f172a" rx="8"/>`;
  s+=`<text x="52" y="14" text-anchor="middle" font-size="9" fill="#64748b">r배 확대 전</text>`;
  for(const t of getTriangles(1,52,20,12,100,92,100))
    s+=`<polygon points="${polyStr(t)}" fill="#1d4ed8" stroke="#3b82f6" stroke-width="1.5"/>`;
  s+=`<text x="52" y="115" text-anchor="middle" font-size="9" fill="#60a5fa">1개</text>`;
  s+=`<text x="115" y="65" text-anchor="middle" font-size="16" fill="#475569">→</text>`;
  s+=`<text x="115" y="80" text-anchor="middle" font-size="8" fill="#475569">×2배</text>`;
  s+=`<text x="192" y="14" text-anchor="middle" font-size="9" fill="#64748b">2배 확대 후</text>`;
  const rax=192,ray=20,rbx=137,rby=100,rcx=252,rcy=100;
  const rmx1=(rax+rbx)/2,rmy1=(ray+rby)/2;
  const rmx2=(rax+rcx)/2,rmy2=(ray+rcy)/2;
  const rmx3=(rbx+rcx)/2,rmy3=(rby+rcy)/2;
  for(const t of getTriangles(1,rax,ray,rmx1,rmy1,rmx2,rmy2))
    s+=`<polygon points="${polyStr(t)}" fill="#92400e" stroke="#f59e0b" stroke-width="0.8"/>`;
  for(const t of getTriangles(1,rmx1,rmy1,rbx,rby,rmx3,rmy3))
    s+=`<polygon points="${polyStr(t)}" fill="#064e3b" stroke="#10b981" stroke-width="0.8"/>`;
  for(const t of getTriangles(1,rmx2,rmy2,rmx3,rmy3,rcx,rcy))
    s+=`<polygon points="${polyStr(t)}" fill="#3b0764" stroke="#a78bfa" stroke-width="0.8"/>`;
  s+=`<polygon points="${rmx1},${rmy1} ${rmx2},${rmy2} ${rmx3},${rmy3}" fill="#060f1a" stroke="#374151" stroke-width="1.2" stroke-dasharray="4 2"/>`;
  s+=`<text x="192" y="115" text-anchor="middle" font-size="9" fill="#c084fc">N = 3개 (가운데 없음!)</text>`;
  s+='</svg>';
  return s;
}

document.getElementById('svgLine').innerHTML = drawLineSVG();
document.getElementById('svgTriComp').innerHTML = drawTriSVG();
document.getElementById('svgSierComp').innerHTML = drawSierSVG();

// ── 프랙털 차원 계산기 ──
function calcDim(){
  const r=parseFloat(document.getElementById('dimR').value);
  const n=parseFloat(document.getElementById('dimN').value);
  if(isNaN(r)||isNaN(n)||r<=1||n<1) return;
  const d=Math.log(n)/Math.log(r);
  document.getElementById('dimOut').textContent=d.toFixed(4);
  let msg='';
  if(Math.abs(d-1)<0.001) msg='→ 1차원 도형 (선)';
  else if(Math.abs(d-2)<0.001) msg='→ 2차원 도형 (면)';
  else if(Math.abs(d-3)<0.001) msg='→ 3차원 도형 (입체)';
  else if(d>0&&d<1) msg=`→ 프랙털! 점(0차원)과 선(1차원) 사이의 ${d.toFixed(3)}차원`;
  else if(d>1&&d<2) msg=`→ 프랙털! 선(1차원)과 면(2차원) 사이의 ${d.toFixed(3)}차원`;
  else if(d>2&&d<3) msg=`→ 프랙털! 면(2차원)과 입체(3차원) 사이의 ${d.toFixed(3)}차원`;
  else msg=`→ ${d.toFixed(4)}차원`;
  document.getElementById('dimInterp').textContent=msg;
  document.getElementById('dimResult').style.display='block';
}
document.getElementById('dimBtn').addEventListener('click',calcDim);
document.querySelectorAll('.dc-preset').forEach(btn=>{
  btn.addEventListener('click',function(){
    document.getElementById('dimR').value=this.dataset.r;
    document.getElementById('dimN').value=this.dataset.n;
    calcDim();
  });
});

// ── 계산기 ──
document.getElementById('calcBtn').addEventListener('click',function(){
  const n = Math.max(0,Math.min(30,parseInt(document.getElementById('calcN').value)||0));
  const cnt = Math.pow(3,n);
  const area = Math.pow(3/4,n);
  const peri = 3*Math.pow(3/2,n);
  document.getElementById('r-c').textContent =
    cnt>1e15 ? cnt.toExponential(3) + '개' : cnt.toLocaleString() + '개';
  document.getElementById('r-a').textContent =
    area<1e-12 ? area.toExponential(4) : area.toFixed(8).replace(/\.?0+$/,'');
  document.getElementById('r-p').textContent =
    peri>1e15 ? peri.toExponential(3) : peri.toFixed(5).replace(/\.?0+$/,'');
  document.getElementById('calcOut').style.display='block';
});

// ── 탭 전환 ──
document.querySelectorAll('.tab-btn').forEach(btn=>{
  btn.addEventListener('click',function(){
    document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
    document.querySelectorAll('.pane').forEach(p=>p.classList.remove('active'));
    this.classList.add('active');
    document.getElementById(`pane-${this.dataset.tab}`).classList.add('active');
  });
});

// ── 퀴즈 ──
const QUIZ = [
  {
    q: 'n단계에서 남아 있는 삼각형의 개수를 나타내는 식은?',
    choices:['2ⁿ','3ⁿ','n²','4ⁿ'],
    answer:1,
    explain:'매 단계마다 각 삼각형이 3개로 분열됩니다. 0단계: 1=3⁰, 1단계: 3=3¹, 2단계: 9=3², …'
  },
  {
    q: 'n단계 삼각형들의 넓이의 합은? (단, S₀ = 1로 놓겠습니다.)',
    choices:['(1/2)ⁿ','(2/3)ⁿ','(3/4)ⁿ','(3/2)ⁿ'],
    answer:2,
    explain:'한 변이 1/2배 → 넓이 1/4배, 개수 3배 → Sₙ = 3ⁿ×(1/4)ⁿ = (3/4)ⁿ'
  },
  {
    q: '4단계에서 삼각형의 개수는?',
    choices:['27개','64개','81개','256개'],
    answer:2,
    explain:'3⁴ = 81개'
  },
  {
    q: '단계가 무한히 커질 때 시에르핀스키 삼각형의 넓이는?',
    choices:['무한히 증가','1에 수렴','0에 수렴','3에 수렴'],
    answer:2,
    explain:'Sₙ = (3/4)ⁿ이고 3/4 < 1이므로 n→∞일 때 0에 수렴합니다. 넓이가 사라집니다!'
  },
  {
    q: '단계가 무한히 커질 때 삼각형들의 둘레의 합은?',
    choices:['0에 수렴','3에 수렴','무한히 증가','변하지 않음'],
    answer:2,
    explain:'Pₙ = 3×(3/2)ⁿ이고 3/2 > 1이므로 n→∞일 때 ∞로 발산합니다. 길이가 무한히 길어집니다!'
  },
  {
    q: '시에르핀스키 삼각형의 프랙털 차원(소수 둘째 자리 근사)은?',
    choices:['약 1.00','약 1.26','약 1.59','약 2.00'],
    answer:2,
    explain:'크기 2배 확대 → 자기 복사본 3개. 2ˣ = 3 → x = log₂3 ≈ 1.585. 1차원과 2차원 사이!'
  },
  {
    q: '3단계에서 각 작은 삼각형 한 변의 길이는? (처음 한 변의 길이 = 1)',
    choices:['1/4','1/6','1/8','1/9'],
    answer:2,
    explain:'각 단계마다 변의 길이가 1/2배로 줄어듭니다. 3단계 → (1/2)³ = 1/8'
  },
  {
    q: '시에르핀스키 삼각형에서 넓이와 둘레의 합이 보이는 행동으로 맞는 것은?',
    choices:[
      '넓이 → ∞, 둘레 → 0',
      '넓이 → 0, 둘레 → ∞',
      '둘 다 0에 수렴',
      '둘 다 무한히 증가',
    ],
    answer:1,
    explain:'넓이는 (3/4)ⁿ→0, 둘레는 3×(3/2)ⁿ→∞. 넓이가 0인데 둘레는 무한한 역설적 도형!'
  },
];

const scores = new Array(QUIZ.length).fill(null);

function buildQuiz(){
  const area = document.getElementById('quizArea');
  area.innerHTML='';
  QUIZ.forEach((q,qi)=>{
    const card = document.createElement('div');
    card.className='q-card'; card.id=`qc${qi}`;
    card.innerHTML=`<div class="q-num">문제 ${qi+1} / ${QUIZ.length}</div>
      <div class="q-text">${q.q}</div>
      <div class="q-choices" id="qch${qi}"></div>
      <div class="q-fb" id="qfb${qi}" style="display:none"></div>`;
    q.choices.forEach((ch,ci)=>{
      const btn=document.createElement('button');
      btn.className='q-choice';
      btn.textContent=`${'①②③④'[ci]} ${ch}`;
      btn.addEventListener('click',()=>onChoice(qi,ci));
      card.querySelector(`#qch${qi}`).appendChild(btn);
    });
    area.appendChild(card);
  });
  const sb=document.createElement('div');
  sb.className='score-box'; sb.id='scoreBox';
  sb.innerHTML=`<div class="score-big" id="scoreBig">-</div>
    <div class="score-msg" id="scoreMsg">문제를 풀어보세요!</div>`;
  area.appendChild(sb);
}

function onChoice(qi,ci){
  if(scores[qi]!==null)return;
  const ok=ci===QUIZ[qi].answer;
  scores[qi]=ok;
  const card=document.getElementById(`qc${qi}`);
  card.classList.add(ok?'correct':'wrong');
  card.querySelectorAll('.q-choice').forEach((b,i)=>{
    b.disabled=true;
    if(i===QUIZ[qi].answer)b.classList.add('show-ans');
    else if(i===ci&&!ok)b.classList.add('sel-wrong');
  });
  const fb=document.getElementById(`qfb${qi}`);
  fb.style.display='block';
  fb.className=`q-fb ${ok?'correct':'wrong'}`;
  fb.textContent=(ok?'✔ 정답! ':'✘ 오답. ')+QUIZ[qi].explain;
  updateScore();
}

function updateScore(){
  const ans=scores.filter(s=>s!==null).length;
  const ok=scores.filter(s=>s===true).length;
  document.getElementById('scoreBig').textContent=`${ok} / ${ans}`;
  const msg=ans<QUIZ.length
    ?`${ans}문제 완료 (${QUIZ.length-ans}문제 남음)`
    :`정답률 ${Math.round(ok/QUIZ.length*100)}% — ${
        ok===QUIZ.length?'🎉 완벽! 프랙털 마스터!':
        ok>=Math.ceil(QUIZ.length*.7)?'👏 잘했어요!':'📚 탭으로 돌아가 다시 탐구해봐요.'}`;
  document.getElementById('scoreMsg').textContent=msg;
  if(ans===QUIZ.length&&!document.getElementById('reBtn')){
    const btn=document.createElement('button');
    btn.className='re-btn';btn.id='reBtn';btn.textContent='다시 풀기';
    btn.addEventListener('click',()=>{scores.fill(null);buildQuiz();});
    document.getElementById('scoreBox').appendChild(btn);
  }
}

buildQuiz();
setStep(0);

})();
</script>
</body>
</html>
"""


def render():
    st.header("🔺 시에르핀스키 삼각형 — 단계별 분석")
    st.caption("단계별 삼각형 개수·넓이·둘레를 직접 탐구하며 수열 공식과 프랙털 차원을 발견합니다.")
    components.html(HTML, height=2300, scrolling=False)
