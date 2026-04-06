# activities/probability_new/mini/prob_basic_properties.py
"""
확률의 기본 성질 미니활동
확률 범위(0≤P(A)≤1), 공사건(P=0), 전사건(P=1)을 다양한 생활 속 사례로 탐구합니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "⚖️ 확률의 기본 성질 탐험",
    "description": "확률 범위(0≤P≤1), 공사건(P=0), 전사건(P=1)을 다양한 사례로 재미있게 탐구합니다.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "확률기본성질"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 – 확률의 기본 성질**"},
    {
        "key": "공사건전사건자신말로",
        "label": "공사건과 전사건을 각각 자신의 말로 설명하고, 오늘 활동에서 인상 깊었던 사례를 하나씩 써보세요.",
        "type": "text_area",
        "height": 120,
        "placeholder": "공사건: ...\n전사건: ...\n인상 깊었던 사례: ..."
    },
    {
        "key": "확률범위왜",
        "label": "확률이 0보다 작거나 1보다 클 수 없는 이유를 수학적으로 설명해보세요.",
        "type": "text_area",
        "height": 90,
        "placeholder": "확률은 (사건이 일어나는 경우의 수) ÷ (전체 경우의 수)이므로..."
    },
    {
        "key": "일상속사례",
        "label": "💡 일상에서 찾을 수 있는 공사건과 전사건의 예를 각각 2가지씩 직접 만들어보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "공사건 예1: ...\n공사건 예2: ...\n전사건 예1: ...\n전사건 예2: ..."
    },
    {
        "key": "헷갈린부분",
        "label": "이 활동에서 헷갈렸던 부분이 있다면 무엇이었나요? 지금은 어떻게 이해했나요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "처음에는 ... 가 헷갈렸지만, 지금은 ..."
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 80},
    {"key": "느낀점", "label": "💬 느낀 점", "type": "text_area", "height": 80},
]

_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>확률의 기본 성질 탐험</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);
  color:#e2e8f0;
  padding:14px 12px 30px;
  min-height:100vh;
}
/* ── 헤더 ── */
.hdr{
  text-align:center;
  padding:18px 20px 16px;
  background:linear-gradient(135deg,rgba(139,92,246,.18),rgba(59,130,246,.18));
  border:1px solid rgba(139,92,246,.35);
  border-radius:16px;
  margin-bottom:20px;
}
.hdr h1{font-size:1.4rem;font-weight:700;color:#a78bfa;margin-bottom:6px}
.hdr p{font-size:.88rem;color:#94a3b8;margin-bottom:12px}
.prop-box{
  display:flex;flex-wrap:wrap;justify-content:center;gap:10px;
  margin-top:10px;
}
.prop-pill{
  background:rgba(139,92,246,.15);
  border:1px solid rgba(139,92,246,.4);
  border-radius:10px;
  padding:8px 16px;
  font-size:.85rem;
  color:#c4b5fd;
  font-weight:600;
}
.prop-pill span{color:#fbbf24}
/* ── 섹션 ── */
.section{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.1);
  border-radius:14px;
  padding:18px 16px;
  margin-bottom:18px;
}
.section-title{
  font-size:1.08rem;font-weight:700;
  margin-bottom:6px;display:flex;align-items:center;gap:8px;
}
.section-desc{font-size:.82rem;color:#94a3b8;margin-bottom:14px;line-height:1.5}

/* ── 스코어보드 ── */
.scoreboard{
  display:flex;gap:12px;justify-content:center;margin-bottom:16px;flex-wrap:wrap;
}
.score-card{
  background:rgba(255,255,255,.06);
  border:1px solid rgba(255,255,255,.12);
  border-radius:10px;padding:8px 16px;text-align:center;min-width:90px;
}
.score-card .num{font-size:1.5rem;font-weight:700}
.score-card .lbl{font-size:.7rem;color:#94a3b8;margin-top:1px}
.score-correct .num{color:#34d399}
.score-wrong .num{color:#f87171}
.score-total .num{color:#60a5fa}

/* ── 탐구1: 확률 수사대 ── */
.prob-grid{
  display:grid;
  grid-template-columns:repeat(auto-fill,minmax(190px,1fr));
  gap:10px;
}
.prob-card{
  background:rgba(255,255,255,.05);
  border:2px solid rgba(255,255,255,.12);
  border-radius:12px;
  padding:14px 12px;
  text-align:center;
  transition:all .2s;
}
.prob-card .prob-val{
  font-size:1.3rem;font-weight:700;color:#e2e8f0;margin-bottom:10px;
  font-family:'Courier New',monospace;
}
.prob-btn-row{display:flex;gap:6px;justify-content:center}
.pbtn{
  padding:6px 12px;border-radius:8px;border:none;cursor:pointer;
  font-size:.78rem;font-weight:600;transition:all .15s;
}
.pbtn-valid{background:rgba(52,211,153,.2);color:#34d399;border:1px solid #34d399}
.pbtn-invalid{background:rgba(248,113,113,.2);color:#f87171;border:1px solid #f87171}
.pbtn:hover{opacity:.85;transform:scale(1.04)}
.prob-card.correct{border-color:#34d399;background:rgba(52,211,153,.08)}
.prob-card.wrong{border-color:#f87171;background:rgba(248,113,113,.08)}
.prob-card.correct .prob-val{color:#34d399}
.prob-card.wrong .prob-val{color:#f87171}
.prob-note{font-size:.74rem;color:#94a3b8;margin-top:8px;line-height:1.4;display:none}
.prob-card.correct .prob-note,
.prob-card.wrong .prob-note{display:block}
.result-badge{
  display:none;font-size:.72rem;font-weight:700;
  padding:2px 8px;border-radius:6px;margin-bottom:6px;
}
.prob-card.correct .result-badge{display:inline-block;background:#34d399;color:#0f2027}
.prob-card.wrong .result-badge{display:inline-block;background:#f87171;color:#0f2027}

/* ── 탐구2: 공사건·전사건 판별 ── */
.scenario-card.answered-correct{border-color:#34d399;background:rgba(52,211,153,.07)}
.scenario-card.answered-wrong{border-color:#f87171;background:rgba(248,113,113,.07)}
.sc-emoji{font-size:1.6rem;margin-bottom:6px}
.sc-context{font-size:.8rem;color:#94a3b8;margin-bottom:4px}
.sc-event{font-size:.92rem;color:#e2e8f0;margin-bottom:12px;line-height:1.5}
.sc-btn-row{display:flex;gap:7px;flex-wrap:wrap}
.sc-btn{
  padding:7px 14px;border-radius:9px;border:2px solid;
  cursor:pointer;font-size:.78rem;font-weight:700;transition:all .15s;
  background:transparent;
}
.sc-btn:hover:not(:disabled){transform:scale(1.04);opacity:.9}
.sc-btn:disabled{cursor:default;opacity:.6}
.sc-btn-impossible{color:#f87171;border-color:#f87171}
.sc-btn-certain{color:#34d399;border-color:#34d399}
.sc-btn-normal{color:#60a5fa;border-color:#60a5fa}
.sc-btn.selected-correct{
  color:#0f2027;font-weight:800;opacity:1!important;
}
.sc-btn-impossible.selected-correct{background:#f87171}
.sc-btn-certain.selected-correct{background:#34d399}
.sc-btn-normal.selected-correct{background:#60a5fa}
.sc-btn.selected-wrong{
  background:rgba(248,113,113,.15);
  border-color:#f87171;color:#f87171;
}
.sc-explanation{
  display:none;font-size:.78rem;margin-top:10px;
  padding:8px 12px;border-radius:8px;line-height:1.5;
  background:rgba(255,255,255,.06);color:#cbd5e1;
}
.scenario-card.answered-correct .sc-explanation,
.scenario-card.answered-wrong .sc-explanation{display:block}
.sc-expl-icon{margin-right:4px}
.verdict{
  font-size:.75rem;font-weight:700;padding:2px 8px;border-radius:5px;
  display:none;margin-bottom:5px;
}
.scenario-card.answered-correct .verdict{display:inline-block;background:#34d399;color:#0f2027}
.scenario-card.answered-wrong .verdict{display:inline-block;background:#f87171;color:#0f2027}

/* ── 탐구3: 공 뽑기 문제 ── */
.ball-setup{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.1);
  border-radius:12px;
  padding:14px;
  margin-bottom:14px;
}
.ball-setup-title{font-size:.85rem;font-weight:700;color:#fbbf24;margin-bottom:10px}
.slider-row{display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap}
.slider-row label{font-size:.8rem;min-width:70px;color:#e2e8f0}
.slider-row input[type=range]{flex:1;min-width:120px;accent-color:#a78bfa}
.slider-val{font-size:.9rem;font-weight:700;min-width:28px;text-align:center}
.ball-display{
  display:flex;flex-wrap:wrap;gap:6px;
  padding:12px;background:rgba(0,0,0,.25);
  border-radius:10px;min-height:54px;align-items:center;
  margin-bottom:12px;border:1px solid rgba(255,255,255,.08);
}
.ball{
  width:34px;height:34px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:.7rem;font-weight:700;color:#fff;
  box-shadow:0 2px 6px rgba(0,0,0,.4);
  flex-shrink:0;
}
.ball-red{background:radial-gradient(circle at 35% 35%,#f87171,#dc2626)}
.ball-blue{background:radial-gradient(circle at 35% 35%,#60a5fa,#2563eb)}
.pick-n-row{display:flex;align-items:center;gap:10px;margin-bottom:12px;flex-wrap:wrap}
.pick-n-row label{font-size:.8rem;color:#e2e8f0}
.pick-input{
  width:55px;padding:5px 8px;border-radius:7px;border:1px solid rgba(255,255,255,.2);
  background:rgba(255,255,255,.08);color:#e2e8f0;font-size:.9rem;text-align:center;
}
.event-grid{
  display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));
  gap:9px;margin-bottom:14px;
}
.event-card{
  background:rgba(255,255,255,.04);
  border:2px solid rgba(255,255,255,.1);
  border-radius:11px;
  padding:12px 10px;cursor:pointer;
  transition:all .18s;text-align:center;
}
.event-card:hover{border-color:#a78bfa;background:rgba(139,92,246,.1)}
.event-card.ev-selected{border-color:#a78bfa;background:rgba(139,92,246,.15)}
.event-card.ev-impossible{border-color:#f87171;background:rgba(248,113,113,.1)}
.event-card.ev-certain{border-color:#34d399;background:rgba(52,211,153,.1)}
.event-card.ev-normal{border-color:#60a5fa;background:rgba(96,165,250,.1)}
.event-title{font-size:.83rem;font-weight:600;color:#e2e8f0;margin-bottom:4px}
.event-prob{font-size:.76rem;color:#94a3b8}
.event-result{
  font-size:.75rem;font-weight:700;padding:3px 9px;border-radius:6px;
  display:none;margin-top:6px;
}
.ev-impossible .event-result{display:inline-block;background:#f87171;color:#0f2027}
.ev-certain .event-result{display:inline-block;background:#34d399;color:#0f2027}
.ev-normal .event-result{display:inline-block;background:#60a5fa;color:#0f2027}
.calc-btn{
  padding:9px 22px;border-radius:10px;border:none;cursor:pointer;
  background:linear-gradient(135deg,#7c3aed,#2563eb);
  color:#fff;font-size:.88rem;font-weight:700;
  transition:all .15s;width:100%;
}
.calc-btn:hover{opacity:.88;transform:scale(1.01)}
.result-panel{
  background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.12);
  border-radius:12px;
  padding:14px;
  margin-top:12px;
  display:none;
}
.result-panel.show{display:block}
.res-row{display:flex;align-items:center;gap:8px;margin-bottom:7px;flex-wrap:wrap}
.res-label{font-size:.8rem;color:#94a3b8;min-width:130px}
.res-val{font-size:.88rem;font-weight:700;color:#e2e8f0}
.res-type-badge{
  padding:3px 10px;border-radius:7px;font-size:.78rem;font-weight:700;
}
.badge-impossible{background:#f87171;color:#0f2027}
.badge-certain{background:#34d399;color:#0f2027}
.badge-normal{background:#60a5fa;color:#0f2027}
.res-formula{
  font-size:.78rem;color:#94a3b8;font-family:'Courier New',monospace;
  background:rgba(0,0,0,.2);padding:6px 10px;border-radius:7px;margin-top:8px;
}

/* ── 종합 정리 ── */
.summary-box{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
  gap:10px;margin-top:4px;
}
.sum-card{
  border-radius:12px;padding:14px 12px;text-align:center;
}
.sum-card-range{background:rgba(139,92,246,.15);border:1px solid rgba(139,92,246,.4)}
.sum-card-imp{background:rgba(248,113,113,.12);border:1px solid rgba(248,113,113,.4)}
.sum-card-cert{background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.4)}
.sum-icon{font-size:1.6rem;margin-bottom:6px}
.sum-title{font-size:.82rem;font-weight:700;margin-bottom:5px}
.sum-card-range .sum-title{color:#a78bfa}
.sum-card-imp .sum-title{color:#f87171}
.sum-card-cert .sum-title{color:#34d399}
.sum-math{font-size:1rem;font-weight:700;font-family:'Courier New',monospace;margin-bottom:4px}
.sum-card-range .sum-math{color:#c4b5fd}
.sum-card-imp .sum-math{color:#fca5a5}
.sum-card-cert .sum-math{color:#6ee7b7}
.sum-desc{font-size:.74rem;color:#94a3b8;line-height:1.45}

/* ── 공통 ── */
.progress-bar-wrap{
  background:rgba(255,255,255,.08);
  border-radius:99px;height:7px;margin-bottom:14px;overflow:hidden;
}
.progress-bar-fill{
  height:100%;background:linear-gradient(90deg,#7c3aed,#2563eb);
  border-radius:99px;transition:width .4s;
}
.reset-btn{
  background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);
  color:#94a3b8;padding:5px 14px;border-radius:8px;cursor:pointer;
  font-size:.75rem;transition:all .15s;margin-top:8px;
}
.reset-btn:hover{background:rgba(255,255,255,.12);color:#e2e8f0}

/* ── 탭 ── */
.tab-section{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.1);
  border-radius:14px;
  margin-bottom:18px;
  overflow:hidden;
}
.tab-bar{
  display:flex;
  border-bottom:1px solid rgba(255,255,255,.1);
  background:rgba(0,0,0,.2);
}
.tab-btn{
  flex:1;padding:12px 8px;border:none;background:transparent;
  color:#64748b;font-size:.85rem;font-weight:700;cursor:pointer;
  transition:all .2s;border-bottom:3px solid transparent;
  margin-bottom:-1px;
}
.tab-btn:hover{color:#cbd5e1;background:rgba(255,255,255,.04)}
.tab-btn.active{color:#e2e8f0;border-bottom-color:var(--tc,#a78bfa);background:rgba(255,255,255,.04)}
.tab-panel{display:none;padding:18px 16px}
.tab-panel.active{display:block}

/* ── 탐구2 2열 그리드 ── */
.scenario-grid{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:10px;
}
@media(max-width:560px){
  .scenario-grid{grid-template-columns:1fr}
}
.scenario-card{
  background:rgba(255,255,255,.04);
  border:2px solid rgba(255,255,255,.1);
  border-radius:14px;
  padding:14px 12px;
  transition:all .2s;
  margin-bottom:0;
}
</style>
</head>
<body>

<!-- ── 헤더 ── -->
<div class="hdr">
  <h1>⚖️ 확률의 기본 성질 탐험</h1>
  <p>세 가지 탐구 활동으로 확률의 기본 성질을 완벽하게 이해해봐요!</p>
  <div class="prop-box">
    <div class="prop-pill">① <span>0 ≤ P(A) ≤ 1</span></div>
    <div class="prop-pill">② P(S) = <span>1</span> &nbsp;,&nbsp; P(∅) = <span>0</span></div>
  </div>
</div>

<!-- ═══════════════════════════════════════
     탐구 1 + 2: 탭
════════════════════════════════════════ -->
<div class="tab-section">
  <div class="tab-bar">
    <button class="tab-btn active" style="--tc:#a78bfa" onclick="switchTab('t1')" id="tbtn-t1">
      🔍 탐구 1
    </button>
    <button class="tab-btn" style="--tc:#34d399" onclick="switchTab('t2')" id="tbtn-t2">
      🎮 탐구 2
    </button>
    <button class="tab-btn" style="--tc:#fbbf24" onclick="switchTab('t3')" id="tbtn-t3">
      🎯 탐구 3
    </button>
    <button class="tab-btn" style="--tc:#818cf8" onclick="switchTab('t4')" id="tbtn-t4">
      📌 정리
    </button>
  </div>

  <!-- 탐구 1 패널 -->
  <div class="tab-panel active" id="panel-t1">
    <div class="section-desc">
      아래 확률값이 <strong>올바른 확률</strong>인지 아닌지 판단해보세요.<br>
      확률은 반드시 <strong>0 이상 1 이하</strong>여야 합니다!
    </div>

    <div class="scoreboard">
      <div class="score-card score-correct"><div class="num" id="p1-correct">0</div><div class="lbl">정답</div></div>
      <div class="score-card score-wrong"><div class="num" id="p1-wrong">0</div><div class="lbl">오답</div></div>
      <div class="score-card score-total"><div class="num" id="p1-total">0</div><div class="lbl">/ 8</div></div>
    </div>

    <div class="progress-bar-wrap"><div class="progress-bar-fill" id="p1-bar" style="width:0%"></div></div>

    <div class="prob-grid" id="prob-grid"></div>
    <div style="text-align:right"><button class="reset-btn" onclick="resetP1()">↺ 초기화</button></div>
  </div>

  <!-- 탐구 2 패널 -->
  <div class="tab-panel" id="panel-t2">
    <div class="section-desc">
      각 상황에서 주어진 사건이 <strong style="color:#f87171">공사건</strong>(P=0),
      <strong style="color:#34d399">전사건</strong>(P=1), 또는
      <strong style="color:#60a5fa">일반 사건</strong>(0&lt;P&lt;1)인지 골라보세요!
    </div>

    <div class="scoreboard">
      <div class="score-card score-correct"><div class="num" id="p2-correct">0</div><div class="lbl">정답</div></div>
      <div class="score-card score-wrong"><div class="num" id="p2-wrong">0</div><div class="lbl">오답</div></div>
      <div class="score-card score-total"><div class="num" id="p2-total">0</div><div class="lbl">/ 12</div></div>
    </div>

    <div class="progress-bar-wrap"><div class="progress-bar-fill" id="p2-bar" style="width:0%;background:linear-gradient(90deg,#059669,#10b981)"></div></div>

    <div class="scenario-grid" id="scenario-list"></div>
    <div style="text-align:right"><button class="reset-btn" onclick="resetP2()">↺ 초기화</button></div>
  </div>
</div>

  <!-- 탐구 3 패널 -->
  <div class="tab-panel" id="panel-t3">
    <div class="section-desc">
      상자 속 공의 수를 직접 설정하고, 꺼낼 공의 수를 정한 뒤<br>
      각 사건이 공사건인지 전사건인지 일반 사건인지 확인해보세요!
    </div>

    <div class="ball-setup">
      <div class="ball-setup-title">📦 상자 설정</div>
      <div class="slider-row">
        <label>🔴 빨간 공</label>
        <input type="range" id="sl-red" min="0" max="8" value="1"
               oninput="updateBalls()">
        <span class="slider-val" id="val-red" style="color:#f87171">1</span>
      </div>
      <div class="slider-row">
        <label>🔵 파란 공</label>
        <input type="range" id="sl-blue" min="0" max="8" value="3"
               oninput="updateBalls()">
        <span class="slider-val" id="val-blue" style="color:#60a5fa">3</span>
      </div>
      <div class="ball-display" id="ball-display"></div>
      <div class="pick-n-row">
        <label>꺼낼 공의 수:</label>
        <input type="number" id="pick-n" class="pick-input" min="1" max="8" value="2">
        <span style="font-size:.78rem;color:#94a3b8" id="pick-hint"></span>
      </div>
      <button class="calc-btn" onclick="calcEvents()">🔍 사건 분석하기</button>
    </div>

    <div class="result-panel" id="result-panel">
      <div style="font-size:.85rem;font-weight:700;color:#fbbf24;margin-bottom:10px" id="res-title"></div>
      <div class="event-grid" id="event-grid"></div>
    </div>
  </div>

  <!-- 정리 패널 -->
  <div class="tab-panel" id="panel-t4">
    <div class="section-desc" style="margin-bottom:14px">
      활동을 통해 알게 된 확률의 기본 성질 세 가지를 정리해봐요!
    </div>
    <div class="summary-box">
      <div class="sum-card sum-card-range">
        <div class="sum-icon">📊</div>
        <div class="sum-title">확률의 범위</div>
        <div class="sum-math">0 ≤ P(A) ≤ 1</div>
        <div class="sum-desc">확률은 항상 0 이상 1 이하의 값을 가집니다.</div>
      </div>
      <div class="sum-card sum-card-imp">
        <div class="sum-icon">🚫</div>
        <div class="sum-title">공사건 (∅)</div>
        <div class="sum-math">P(∅) = 0</div>
        <div class="sum-desc">절대로 일어날 수 없는 사건입니다. 확률 = 0</div>
      </div>
      <div class="sum-card sum-card-cert">
        <div class="sum-icon">✅</div>
        <div class="sum-title">전사건 (S)</div>
        <div class="sum-math">P(S) = 1</div>
        <div class="sum-desc">반드시 일어나는 사건(표본공간 전체)입니다. 확률 = 1</div>
      </div>
    </div>
  </div>

</div>

<script>
// ═══════════════════════════════
// 탭 전환
// ═══════════════════════════════
function switchTab(id){
  ['t1','t2','t3','t4'].forEach(k=>{
    document.getElementById('panel-'+k).classList.toggle('active', k===id);
    document.getElementById('tbtn-'+k).classList.toggle('active', k===id);
  });
}

// ═══════════════════════════════
// 탐구 1 – 확률 수사대
// ═══════════════════════════════
const probCases = [
  {val:'P(A) = 0.7',   valid:true,  note:'0과 1 사이의 값이므로 올바른 확률입니다. ✓'},
  {val:'P(A) = 1.2',   valid:false, note:'확률은 1을 넘을 수 없습니다! (경우의 수가 전체보다 클 수 없으므로)'},
  {val:'P(A) = −0.3',  valid:false, note:'확률은 음수가 될 수 없습니다! (경우의 수는 0 이상이므로)'},
  {val:'P(A) = 0',     valid:true,  note:'P=0은 공사건! 절대 일어나지 않는 사건의 확률입니다. ✓'},
  {val:'P(A) = 1',     valid:true,  note:'P=1은 전사건! 반드시 일어나는 사건의 확률입니다. ✓'},
  {val:'P(A) = 3/4',   valid:true,  note:'0과 1 사이의 분수이므로 올바른 확률입니다. ✓'},
  {val:'P(A) = 2',     valid:false, note:'확률의 최댓값은 1입니다! 2는 될 수 없어요.'},
  {val:'P(A) = −1',    valid:false, note:'확률은 반드시 0 이상이어야 합니다!'},
];
let p1Correct=0, p1Wrong=0;

function buildP1(){
  const grid = document.getElementById('prob-grid');
  grid.innerHTML = '';
  probCases.forEach((c,i)=>{
    grid.innerHTML += `
    <div class="prob-card" id="pc-${i}">
      <div class="result-badge" id="pb-badge-${i}">●</div>
      <div class="prob-val">${c.val}</div>
      <div class="prob-btn-row">
        <button class="pbtn pbtn-valid"  onclick="judgeP1(${i},true)"  id="pb-v-${i}">✓ 유효</button>
        <button class="pbtn pbtn-invalid" onclick="judgeP1(${i},false)" id="pb-i-${i}">✗ 무효</button>
      </div>
      <div class="prob-note" id="pn-${i}">${c.note}</div>
    </div>`;
  });
}

function judgeP1(i, chosen){
  const card = document.getElementById('pc-'+i);
  if(card.classList.contains('correct')||card.classList.contains('wrong')) return;
  const isCorrect = (chosen === probCases[i].valid);
  card.classList.add(isCorrect?'correct':'wrong');
  const badge = document.getElementById('pb-badge-'+i);
  badge.textContent = isCorrect ? '✓ 정답!' : '✗ 오답';
  document.getElementById('pb-v-'+i).disabled = true;
  document.getElementById('pb-i-'+i).disabled = true;
  if(isCorrect) p1Correct++; else p1Wrong++;
  updateP1Score();
}

function updateP1Score(){
  document.getElementById('p1-correct').textContent = p1Correct;
  document.getElementById('p1-wrong').textContent   = p1Wrong;
  document.getElementById('p1-total').textContent   = p1Correct+p1Wrong;
  document.getElementById('p1-bar').style.width     = ((p1Correct+p1Wrong)/8*100)+'%';
}

function resetP1(){
  p1Correct=0; p1Wrong=0; updateP1Score(); buildP1();
}

// ═══════════════════════════════
// 탐구 2 – 공사건·전사건 판별기
// ═══════════════════════════════
const scenarios = [
  {emoji:'🎲',
   ctx:'주사위(1~6) 한 개를 던질 때',
   ev:'눈의 수가 <strong>7</strong>인 사건',
   ans:'impossible',
   expl:'주사위 눈은 1~6뿐! 7은 절대 나올 수 없으므로 <strong>공사건</strong> (P=0)입니다.'},
  {emoji:'🎲',
   ctx:'주사위(1~6) 한 개를 던질 때',
   ev:'눈의 수가 <strong>1 이상 6 이하</strong>인 사건',
   ans:'certain',
   expl:'주사위를 던지면 반드시 1~6 중 하나! 표본공간 전체이므로 <strong>전사건</strong> (P=1)입니다.'},
  {emoji:'🪙',
   ctx:'동전 한 개를 던질 때',
   ev:'<strong>앞면 또는 뒷면</strong>이 나오는 사건',
   ans:'certain',
   expl:'동전의 표본공간 = {앞, 뒤}. 반드시 둘 중 하나이므로 <strong>전사건</strong> (P=1)입니다.'},
  {emoji:'🪙',
   ctx:'동전 한 개를 던질 때',
   ev:'동전이 <strong>옆면</strong>으로 서는 사건',
   ans:'impossible',
   expl:'이론적 표본공간 = {앞, 뒤}. 옆면은 포함되지 않으므로 <strong>공사건</strong> (P=0)입니다.'},
  {emoji:'🔴',
   ctx:'빨간 공 4개만 들어 있는 상자에서 공 1개를 꺼낼 때',
   ev:'<strong>파란 공</strong>이 나오는 사건',
   ans:'impossible',
   expl:'상자에 파란 공이 없으니 절대 불가능! <strong>공사건</strong> (P=0)입니다.'},
  {emoji:'🔴',
   ctx:'빨간 공 4개만 들어 있는 상자에서 공 1개를 꺼낼 때',
   ev:'<strong>빨간 공</strong>이 나오는 사건',
   ans:'certain',
   expl:'모든 공이 빨간색이니 꺼내면 반드시 빨간 공! <strong>전사건</strong> (P=1)입니다.'},
  {emoji:'🃏',
   ctx:'52장 트럼프 카드(조커 없음) 중 1장을 뽑을 때',
   ev:'<strong>♥ 무늬</strong> 카드가 나오는 사건',
   ans:'normal',
   expl:'♥ 카드는 13장. P = 13/52 = 1/4. <strong>일반 사건</strong>입니다!'},
  {emoji:'✂️',
   ctx:'가위바위보에서 한 번 낼 때',
   ev:'<strong>가위, 바위, 보</strong> 중 하나를 내는 사건',
   ans:'certain',
   expl:'표본공간 = {가위, 바위, 보}. 반드시 셋 중 하나이므로 <strong>전사건</strong> (P=1)입니다.'},
  {emoji:'📦',
   ctx:'두 자리 자연수(10~99) 중 하나를 무작위로 뽑을 때',
   ev:'뽑은 수가 <strong>세 자리 수</strong>인 사건',
   ans:'impossible',
   expl:'두 자리 자연수에 세 자리 수는 없습니다! <strong>공사건</strong> (P=0)입니다.'},
  {emoji:'🪙',
   ctx:'동전 <strong>2개</strong>를 동시에 던질 때',
   ev:'동전 <strong>3개 모두</strong> 앞면인 사건',
   ans:'impossible',
   expl:'동전이 2개뿐인데 3개 모두 앞면? 불가능! <strong>공사건</strong> (P=0)입니다.'},
  {emoji:'🎲',
   ctx:'주사위 한 개를 던질 때',
   ev:'눈의 수가 <strong>홀수</strong>인 사건',
   ans:'normal',
   expl:'홀수 눈 = {1,3,5} → P = 3/6 = 1/2. <strong>일반 사건</strong>입니다!'},
  {emoji:'🃏',
   ctx:'52장 트럼프 카드(조커 없음) 중 1장을 뽑을 때',
   ev:'뽑은 카드가 <strong>♠, ♥, ♦, ♣</strong> 중 하나인 사건',
   ans:'certain',
   expl:'모든 카드가 4가지 무늬 중 하나이므로 표본공간 전체! <strong>전사건</strong> (P=1)입니다.'},
];
let p2Correct=0, p2Wrong=0;
const ansLabel={impossible:'공사건 (P=0)', certain:'전사건 (P=1)', normal:'일반 사건'};
const ansColor={impossible:'#f87171', certain:'#34d399', normal:'#60a5fa'};

function buildP2(){
  const list = document.getElementById('scenario-list');
  list.innerHTML = '';
  scenarios.forEach((s,i)=>{
    list.innerHTML += `
    <div class="scenario-card" id="sc-${i}">
      <div class="verdict" id="sc-verdict-${i}">●</div>
      <div class="sc-emoji">${s.emoji}</div>
      <div class="sc-context">${s.ctx}</div>
      <div class="sc-event">${s.ev}</div>
      <div class="sc-btn-row">
        <button class="sc-btn sc-btn-impossible" onclick="judgeP2(${i},'impossible')" id="sb-imp-${i}">🚫 공사건</button>
        <button class="sc-btn sc-btn-certain"    onclick="judgeP2(${i},'certain')"    id="sb-cert-${i}">✅ 전사건</button>
        <button class="sc-btn sc-btn-normal"     onclick="judgeP2(${i},'normal')"     id="sb-norm-${i}">📊 일반 사건</button>
      </div>
      <div class="sc-explanation" id="sc-expl-${i}">
        <span class="sc-expl-icon">💡</span>${s.expl}
      </div>
    </div>`;
  });
}

function judgeP2(i, chosen){
  const card = document.getElementById('sc-'+i);
  if(card.classList.contains('answered-correct')||card.classList.contains('answered-wrong')) return;
  const isCorrect = (chosen === scenarios[i].ans);
  card.classList.add(isCorrect?'answered-correct':'answered-wrong');
  ['imp','cert','norm'].forEach(k=>{
    document.getElementById('sb-'+k+'-'+i).disabled = true;
  });
  const chosenKey = chosen==='impossible'?'imp':chosen==='certain'?'cert':'norm';
  const btn = document.getElementById('sb-'+chosenKey+'-'+i);
  if(isCorrect){
    btn.classList.add('selected-correct');
  } else {
    btn.classList.add('selected-wrong');
    // 정답 버튼 표시
    const corrKey = scenarios[i].ans==='impossible'?'imp':scenarios[i].ans==='certain'?'cert':'norm';
    document.getElementById('sb-'+corrKey+'-'+i).classList.add('selected-correct');
  }
  const verdict = document.getElementById('sc-verdict-'+i);
  verdict.textContent = isCorrect ? '✓ 정답! ' + ansLabel[scenarios[i].ans] : '✗ 오답 → 정답: ' + ansLabel[scenarios[i].ans];
  if(isCorrect) p2Correct++; else p2Wrong++;
  updateP2Score();
}

function updateP2Score(){
  document.getElementById('p2-correct').textContent = p2Correct;
  document.getElementById('p2-wrong').textContent   = p2Wrong;
  document.getElementById('p2-total').textContent   = p2Correct+p2Wrong;
  document.getElementById('p2-bar').style.width     = ((p2Correct+p2Wrong)/12*100)+'%';
}

function resetP2(){
  p2Correct=0; p2Wrong=0; updateP2Score(); buildP2();
}

// ═══════════════════════════════
// 탐구 3 – 공 뽑기 계산기
// ═══════════════════════════════
function updateBalls(){
  const r = +document.getElementById('sl-red').value;
  const b = +document.getElementById('sl-blue').value;
  document.getElementById('val-red').textContent  = r;
  document.getElementById('val-blue').textContent = b;
  const total = r+b;
  const display = document.getElementById('ball-display');
  display.innerHTML = '';
  if(total===0){
    display.innerHTML = '<span style="color:#64748b;font-size:.8rem">공이 없습니다</span>';
  } else {
    for(let i=0;i<r;i++) display.innerHTML += '<div class="ball ball-red">빨</div>';
    for(let i=0;i<b;i++) display.innerHTML += '<div class="ball ball-blue">파</div>';
  }
  const maxPick = Math.max(1, total);
  const pickN = document.getElementById('pick-n');
  pickN.max = maxPick;
  if(+pickN.value > maxPick) pickN.value = maxPick;
  document.getElementById('pick-hint').textContent = `(최대 ${maxPick}개)`;
  document.getElementById('result-panel').classList.remove('show');
}

// C(n,r)
function C(n,r){
  if(r<0||r>n) return 0;
  if(r===0||r===n) return 1;
  r = Math.min(r,n-r);
  let num=1,den=1;
  for(let i=0;i<r;i++){num*=(n-i);den*=(i+1);}
  return Math.round(num/den);
}

function calcEvents(){
  const r = +document.getElementById('sl-red').value;
  const b = +document.getElementById('sl-blue').value;
  const k = +document.getElementById('pick-n').value;
  const total = r+b;
  if(total===0){alert('공을 1개 이상 넣어주세요!');return;}
  if(k<1||k>total){alert(`꺼낼 공의 수는 1~${total}개여야 합니다!`);return;}

  const totalWays = C(total, k);
  const panel = document.getElementById('result-panel');
  const titleEl = document.getElementById('res-title');
  titleEl.textContent = `📦 상자: 빨간 ${r}개 + 파란 ${b}개 | ${k}개를 꺼낼 때 (전체 ${totalWays}가지)`;

  // 생성할 사건들
  const events = [];

  // 빨간 공이 j개 (j=0,...,min(k,r))
  for(let j=0;j<=Math.min(k,r);j++){
    const blueNeeded = k-j;
    const ways = C(r,j)*C(b,blueNeeded);
    const frac = ways+'/'+totalWays;
    const probNum = ways/totalWays;
    let type, label;
    if(ways===0)   { type='impossible'; label='공사건 (P=0)'; }
    else if(ways===totalWays){ type='certain';   label='전사건 (P=1)'; }
    else           { type='normal';    label=`P = ${frac}`; }
    events.push({
      title: `빨간 공 정확히 ${j}개`,
      prob: probNum, ways, frac, type, label,
      formula:`C(${r},${j})×C(${b},${blueNeeded}) / C(${total},${k}) = ${ways}/${totalWays}`
    });
  }

  // 파란 공 1개 이상
  const waysAtLeast1Blue = totalWays - C(r,k);
  {
    const ways = Math.max(0, waysAtLeast1Blue);
    let type, label;
    if(ways<=0)    { type='impossible'; label='공사건 (P=0)'; }
    else if(ways>=totalWays){ type='certain';   label='전사건 (P=1)'; }
    else           { type='normal';    label=`P = ${ways}/${totalWays}`; }
    events.push({
      title:'파란 공 1개 이상',
      ways, frac:`${ways}/${totalWays}`, type, label,
      formula:`전체 - (빨간만) = ${totalWays} - ${C(r,k)} = ${ways}`
    });
  }

  const grid = document.getElementById('event-grid');
  grid.innerHTML='';
  events.forEach((ev,i)=>{
    grid.innerHTML += `
    <div class="event-card ev-${ev.type}" id="ev-${i}" onclick="toggleEvDetail(${i})">
      <div class="event-title">${ev.title}</div>
      <div class="event-result">${ev.label}</div>
      <div class="event-prob" id="ev-prob-${i}" style="display:none;margin-top:6px;font-size:.72rem;font-family:'Courier New',monospace;color:#94a3b8">${ev.formula}</div>
    </div>`;
  });
  panel.classList.add('show');
}

function toggleEvDetail(i){
  const el = document.getElementById('ev-prob-'+i);
  el.style.display = el.style.display==='none'?'block':'none';
}

// ═══════════════════════════════
// 초기화
// ═══════════════════════════════
buildP1();
buildP2();
updateBalls();
</script>
</body>
</html>"""


def render():
    st.subheader("⚖️ 확률의 기본 성질 탐험")
    st.caption("세 가지 탐구 활동으로 확률의 범위, 공사건, 전사건을 재미있게 이해해봐요!")
    components.html(_HTML, height=1920, scrolling=False)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
