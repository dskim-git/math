# activities/common/mini/imaginary_unit_cycle.py
"""
허수단위 i의 순환 탐구
i의 거듭제곱 주기성, 합의 패턴, 복소평면 회전, 큰 지수 계산을 탐구하는 미니활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "허수단위순환탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 탐구를 마치고 아래 질문에 답해 보세요**"},
    {
        "key": "순환이유",
        "label": "i의 거듭제곱이 주기 4로 순환하는 이유를 i²=−1임을 이용해 설명하세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "합설명",
        "label": "i+i²+i³+...+i¹⁰⁰ = 0인 이유를 연속된 4개의 합과 연결하여 설명하세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "기하의미",
        "label": "복소평면에서 i를 곱하는 것이 어떤 기하학적 의미를 갖는지, i⁴=1이 되는 이유를 기하학적으로 설명하세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 이 활동을 통해 새롭게 알게 된 점",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "느낀점",
        "label": "💬 이 활동을 하면서 느낀 점",
        "type": "text_area",
        "height": 90,
    },
]

META = {
    "title": "🔄 허수단위 i의 순환 탐구",
    "description": "i의 거듭제곱이 주기 4로 순환하는 성질, 합 공식, 복소평면 기하를 표 채우기·나침반·계산기·도전 문제로 탐구하는 활동입니다.",
    "order": 203,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>허수단위 i의 순환 탐구</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI','Malgun Gothic',system-ui,sans-serif;
  background:linear-gradient(155deg,#0f0c29 0%,#1e1550 45%,#0d1225 100%);
  color:#ede9ff;min-height:100vh;padding:12px 10px 20px;
}
.shell{max-width:1060px;margin:0 auto}

/* Hero */
.hero{
  position:relative;overflow:hidden;
  background:linear-gradient(135deg,rgba(109,40,217,.22),rgba(79,70,229,.14));
  border:1px solid rgba(150,100,255,.3);border-radius:22px;
  padding:18px 24px;margin-bottom:14px;
}
.hero::before{
  content:'i';position:absolute;right:16px;top:-14px;
  font-size:160px;font-weight:900;color:rgba(150,100,255,.07);
  pointer-events:none;line-height:1;
}
.hero>*{position:relative;z-index:1}
.hero-tag{
  display:inline-flex;align-items:center;gap:6px;
  background:rgba(150,100,255,.18);border:1px solid rgba(180,130,255,.3);
  border-radius:999px;padding:4px 12px;
  color:#d4b4ff;font-size:.76rem;font-weight:700;letter-spacing:.07em;
  margin-bottom:10px;
}
.hero h1{font-size:1.55rem;font-weight:900;color:#fff;margin-bottom:6px}
.hero p{color:#cfc0f0;line-height:1.7;font-size:.88rem;max-width:820px}
.hero strong{color:#c4a0ff}

/* Tabs */
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.tab-btn{
  padding:8px 14px;border-radius:12px;
  background:rgba(109,40,217,.15);border:1px solid rgba(150,100,255,.22);
  color:#c4a0ff;font-size:.82rem;font-weight:700;cursor:pointer;
  transition:all .18s;white-space:nowrap;
}
.tab-btn:hover{background:rgba(109,40,217,.28);border-color:#a78bfa;color:#e0d0ff}
.tab-btn.active{
  background:linear-gradient(135deg,#7c3aed,#6d28d9);
  border-color:#a78bfa;color:#fff;
  box-shadow:0 4px 14px rgba(109,40,217,.4);
}
.tab-panel{display:none}
.tab-panel.active{display:block;animation:fadeUp .28s ease}
@keyframes fadeUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

/* Section common */
.sec{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(150,100,255,.18);
  border-radius:20px;padding:18px 20px;
}
.sec-title{
  font-size:1rem;font-weight:800;color:#c4a0ff;
  margin-bottom:10px;display:flex;align-items:center;gap:8px;
}
.sec-desc{color:#c0b4e0;font-size:.86rem;line-height:1.72;margin-bottom:14px}

/* ── TAB 1: 순환표 ── */
.fill-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;align-items:center}
.fill-label{color:#a78bfa;font-size:.84rem;font-weight:700}
.fchoice{
  padding:8px 16px;border-radius:12px;
  background:rgba(109,40,217,.16);border:1px solid rgba(150,100,255,.28);
  color:#d4b4ff;font-size:1rem;font-weight:700;cursor:pointer;
  transition:all .18s;user-select:none;
}
.fchoice:hover{background:rgba(109,40,217,.3);border-color:#a78bfa;color:#fff}
.fchoice.active{
  background:linear-gradient(135deg,rgba(109,40,217,.55),rgba(124,58,237,.45));
  border-color:#c4a0ff;color:#fff;transform:translateY(-1px);
  box-shadow:0 6px 18px rgba(109,40,217,.35);
}
.cycle-table-wrap{overflow-x:auto;margin-bottom:12px}
.cycle-table{border-collapse:separate;border-spacing:4px;min-width:680px}
.cycle-table th{
  background:linear-gradient(135deg,#6d28d9,#7c3aed);
  color:#fff;font-weight:800;font-size:.86rem;
  padding:10px 6px;border-radius:10px;text-align:center;min-width:56px;
}
.cycle-table td{
  background:rgba(30,18,65,.75);
  border:1.5px dashed rgba(150,100,255,.3);
  border-radius:10px;padding:10px 6px;
  text-align:center;font-size:1.05rem;font-weight:700;
  color:#a78bfa;cursor:pointer;
  transition:background .18s,transform .15s,border-color .2s;
  min-width:56px;
}
.cycle-table td.empty:hover{background:rgba(109,40,217,.22);transform:scale(1.07)}
.cycle-table td.given{
  background:rgba(80,55,170,.35);border:1.5px solid rgba(150,100,255,.4);
  color:#c4b0ff;cursor:default;
}
.cycle-table td.correct{
  background:linear-gradient(135deg,rgba(34,197,94,.18),rgba(16,185,129,.12));
  border:1.5px solid rgba(34,197,94,.4);color:#86efac;cursor:default;
  animation:cellPop .3s ease;
}
.cycle-table td.wrong{
  background:rgba(239,68,68,.18);border:1.5px solid rgba(239,68,68,.45);
  color:#fca5a5;animation:shake .35s ease;
}
@keyframes cellPop{0%{transform:scale(.75)}60%{transform:scale(1.12)}100%{transform:scale(1)}}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-5px)}75%{transform:translateX(5px)}}
.table-progress{color:#a78bfa;font-size:.84rem;margin-bottom:8px;min-height:18px}
.reveal-box{
  display:none;border-radius:16px;padding:14px 16px;margin-top:10px;
  background:linear-gradient(135deg,rgba(34,197,94,.1),rgba(16,185,129,.07));
  border:1px solid rgba(34,197,94,.3);
}
.reveal-box.show{display:block;animation:fadeUp .4s ease}
.reveal-text{color:#a7f3d0;font-size:.88rem;line-height:1.85}
.reveal-text strong{color:#6ee7b7}

/* ── TAB 2: 나침반 ── */
.compass-wrap{display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap}
.canvas-col{flex:0 0 252px;display:flex;flex-direction:column;align-items:center;gap:10px}
canvas#compass{
  border-radius:50%;background:rgba(8,4,28,.85);
  border:2px solid rgba(150,100,255,.28);display:block;
}
.btn-row{display:flex;gap:8px;flex-wrap:wrap}
.btn{
  border:none;border-radius:999px;padding:9px 16px;
  font-size:.84rem;font-weight:800;cursor:pointer;
  transition:transform .18s,filter .18s;
}
.btn:hover{transform:translateY(-1px);filter:brightness(1.1)}
.btn-purple{background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff}
.btn-ghost{background:rgba(100,80,180,.2);color:#c4a0ff;border:1px solid rgba(150,100,255,.3)}
.info-col{flex:1;min-width:200px}
.power-disp{
  font-size:1.15rem;font-weight:900;color:#e0d0ff;
  background:rgba(109,40,217,.2);border:1px solid rgba(150,100,255,.28);
  border-radius:14px;padding:11px 14px;margin-bottom:12px;text-align:center;
}
.dir-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:12px}
.dir-card{
  padding:10px 12px;border-radius:11px;
  background:rgba(30,18,65,.7);border:1px solid rgba(100,80,200,.2);
  transition:background .2s,border-color .2s;
}
.dir-card.active{background:rgba(109,40,217,.3);border-color:rgba(150,100,255,.5)}
.dir-label{color:#a78bfa;font-size:.73rem;font-weight:700;margin-bottom:3px}
.dir-value{color:#e0d0ff;font-weight:800;font-size:.85rem}
.tip-box{
  background:rgba(109,40,217,.1);border:1px solid rgba(150,100,255,.2);
  border-radius:12px;padding:12px;color:#c4b0ff;font-size:.84rem;line-height:1.72;
}
.tip-box strong{color:#d4b4ff}

/* ── TAB 3: 합 탐구 ── */
.sum-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start}
.slider-col{display:flex;flex-direction:column;gap:10px}
.slider-label{color:#c4a0ff;font-size:.87rem;font-weight:700}
input[type=range]{width:100%;accent-color:#7c3aed;cursor:pointer}
.pattern-box{
  background:rgba(109,40,217,.1);border:1px solid rgba(150,100,255,.2);
  border-radius:12px;padding:12px;
}
.pattern-label{color:#c4a0ff;font-size:.8rem;font-weight:700;margin-bottom:5px}
.pattern-text{color:#c4b8e0;font-size:.85rem;line-height:1.72;min-height:18px}
.sum-panel{
  background:rgba(20,12,50,.8);border:1px solid rgba(150,100,255,.2);
  border-radius:16px;padding:14px;
}
.sum-formula{color:#a78bfa;font-size:.9rem;margin-bottom:10px}
.sum-groups{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px;align-items:center}
.sg-zero{
  padding:4px 9px;border-radius:7px;font-size:.79rem;font-weight:700;
  background:rgba(109,40,217,.2);border:1px solid rgba(150,100,255,.22);color:#c4a0ff;
}
.sg-rem{
  padding:4px 9px;border-radius:7px;font-size:.79rem;font-weight:700;
  background:rgba(234,179,8,.1);border:1px solid rgba(234,179,8,.22);color:#fde68a;
}
.sg-plus{color:#a78bfa;font-size:.85rem;margin:0 1px}
.sum-result{
  font-size:1.1rem;font-weight:900;color:#e0d0ff;
  background:linear-gradient(135deg,rgba(109,40,217,.28),rgba(79,70,229,.16));
  border:1px solid rgba(150,100,255,.3);border-radius:12px;
  padding:10px 14px;text-align:center;
}
.quiz-block{
  margin-top:14px;
  background:rgba(234,179,8,.07);border:1px solid rgba(234,179,8,.22);
  border-radius:16px;padding:14px;
}
.quiz-title{color:#fde68a;font-weight:800;font-size:.88rem;margin-bottom:7px}
.quiz-desc{color:#f5e09a;font-size:.84rem;line-height:1.66;margin-bottom:10px}
.qchoices{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.qchoice{
  padding:8px 14px;border-radius:12px;
  background:rgba(234,179,8,.1);border:1px solid rgba(234,179,8,.22);
  color:#fde68a;font-size:.9rem;font-weight:700;cursor:pointer;transition:all .18s;
}
.qchoice:hover{background:rgba(234,179,8,.2);border-color:#fbbf24;transform:translateY(-1px)}
.qchoice.ok{background:rgba(34,197,94,.18);border-color:rgba(34,197,94,.45);color:#86efac;cursor:default}
.qchoice.ng{background:rgba(239,68,68,.15);border-color:rgba(239,68,68,.4);color:#fca5a5;cursor:default}
.q-feedback{font-size:.87rem;font-weight:700;min-height:18px}

/* ── TAB 4: 신기한 성질 ── */
.props-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px}
.prop-card{
  background:rgba(20,12,50,.75);border:1px solid rgba(150,100,255,.18);
  border-radius:16px;padding:14px;
}
.prop-icon{font-size:1.35rem;margin-bottom:6px}
.prop-title{font-size:.86rem;font-weight:800;color:#c4a0ff;margin-bottom:6px}
.prop-body{font-size:.84rem;color:#c0b4e0;line-height:1.7}
.pf{
  display:inline-block;background:rgba(109,40,217,.2);
  border-radius:7px;padding:3px 9px;color:#e0d0ff;font-weight:700;
  margin:3px 0;font-size:.87rem;
}

/* ── TAB 5: 큰 지수 ── */
.modcalc-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start}
.inp-panel,.res-panel{
  background:rgba(20,12,50,.8);border:1px solid rgba(150,100,255,.2);
  border-radius:16px;padding:16px;
}
.inp-label,.res-label{color:#a78bfa;font-size:.84rem;font-weight:700;margin-bottom:8px}
input[type=number]{
  width:100%;padding:10px 14px;border-radius:10px;
  background:rgba(109,40,217,.15);border:1.5px solid rgba(150,100,255,.28);
  color:#e0d0ff;font-size:1.1rem;font-weight:700;outline:none;
}
input[type=number]:focus{border-color:#a78bfa}
.inp-hint{color:#a78bfa;font-size:.78rem;margin-top:5px}
.res-chain{color:#c4b0ff;font-size:.87rem;line-height:1.82;margin-bottom:10px;min-height:58px}
.res-final{
  font-size:1.2rem;font-weight:900;color:#e0d0ff;
  background:linear-gradient(135deg,rgba(109,40,217,.3),rgba(79,70,229,.18));
  border:1px solid rgba(150,100,255,.3);border-radius:12px;
  padding:10px 14px;text-align:center;min-height:42px;
}

/* ── TAB 6: 도전 ── */
.score-bar{
  display:flex;justify-content:space-around;
  background:rgba(109,40,217,.13);border:1px solid rgba(150,100,255,.22);
  border-radius:13px;padding:11px;margin-bottom:13px;
}
.score-item{text-align:center}
.score-label{font-size:.73rem;color:#a78bfa;margin-bottom:3px}
.score-val{font-size:1.15rem;font-weight:900;color:#e0d0ff}
.mission-card{
  background:rgba(20,12,50,.7);border:1px solid rgba(150,100,255,.18);
  border-radius:16px;padding:14px;margin-bottom:10px;
}
.mnum{
  display:inline-flex;align-items:center;justify-content:center;
  width:27px;height:27px;border-radius:50%;
  background:linear-gradient(135deg,#7c3aed,#6d28d9);
  color:#fff;font-size:.8rem;font-weight:900;margin-bottom:9px;
}
.mq{font-size:.94rem;font-weight:700;color:#e0d0ff;margin-bottom:11px;line-height:1.5}
.mchoices{display:flex;gap:7px;flex-wrap:wrap}
.mchoice{
  padding:8px 14px;border-radius:11px;
  background:rgba(109,40,217,.12);border:1px solid rgba(150,100,255,.22);
  color:#c4a0ff;font-size:.88rem;font-weight:700;cursor:pointer;transition:all .18s;
}
.mchoice:hover{background:rgba(109,40,217,.25);border-color:#a78bfa;color:#e0d0ff;transform:translateY(-1px)}
.mchoice.ok{background:rgba(34,197,94,.18);border-color:rgba(34,197,94,.45);color:#86efac;cursor:default}
.mchoice.ng{background:rgba(239,68,68,.14);border-color:rgba(239,68,68,.38);color:#fca5a5;cursor:default}
.mexplain{
  display:none;margin-top:9px;padding:10px 12px;border-radius:11px;
  background:rgba(109,40,217,.14);border:1px solid rgba(150,100,255,.22);
  color:#c4b0ff;font-size:.84rem;line-height:1.74;
}
.mexplain.show{display:block;animation:fadeUp .3s ease}
.mexplain strong{color:#d4b4ff}

@media(max-width:680px){
  .compass-wrap,.sum-grid,.modcalc-grid,.props-grid{grid-template-columns:1fr}
  .canvas-col{flex:unset;width:100%}
  .hero h1{font-size:1.25rem}
  .tabs{gap:5px}
  .tab-btn{font-size:.78rem;padding:7px 11px}
}
</style>
</head>
<body>
<div class="shell">

<!-- Hero -->
<section class="hero">
  <div class="hero-tag">🔄 허수단위 i 순환 탐구</div>
  <h1>i의 순환 – 4번이면 제자리!</h1>
  <p>
    허수단위 i는 곱할 때마다 <strong>i → −1 → −i → 1 → i → ...</strong>로 순환합니다.
    주기 4의 신기한 성질을 직접 탐구하고, 큰 지수도 순식간에 계산해 봅시다!
  </p>
</section>

<!-- Tab bar -->
<div class="tabs">
  <button class="tab-btn active" data-tab="t1" onclick="showTab('t1')">📋 순환표</button>
  <button class="tab-btn"        data-tab="t2" onclick="showTab('t2')">🧭 나침반</button>
  <button class="tab-btn"        data-tab="t3" onclick="showTab('t3')">➕ 합 탐구</button>
  <button class="tab-btn"        data-tab="t4" onclick="showTab('t4')">✨ 신기한 성질</button>
  <button class="tab-btn"        data-tab="t5" onclick="showTab('t5')">⚡ 큰 지수 계산기</button>
  <button class="tab-btn"        data-tab="t6" onclick="showTab('t6')">🎯 도전 미션</button>
</div>

<!-- TAB 1: 순환표 -->
<div class="tab-panel active" id="tab-t1">
<section class="sec">
  <div class="sec-title">📋 미션 1 · 순환표 채우기</div>
  <div class="sec-desc">
    먼저 채울 값을 선택한 뒤, 빈 칸을 클릭해서 채워 보세요. 처음 3개는 힌트로 주어져 있습니다.
  </div>
  <div class="fill-row">
    <span class="fill-label">채울 값 →</span>
    <button class="fchoice" onclick="selFill(this,'i')">i</button>
    <button class="fchoice" onclick="selFill(this,'-1')">−1</button>
    <button class="fchoice" onclick="selFill(this,'-i')">−i</button>
    <button class="fchoice" onclick="selFill(this,'1')">1</button>
  </div>
  <div class="cycle-table-wrap">
    <table class="cycle-table">
      <thead><tr>
        <th>i¹</th><th>i²</th><th>i³</th><th>i⁴</th>
        <th>i⁵</th><th>i⁶</th><th>i⁷</th><th>i⁸</th>
        <th>i⁹</th><th>i¹⁰</th><th>i¹¹</th><th>i¹²</th>
      </tr></thead>
      <tbody><tr>
        <td class="given">i</td>
        <td class="given">−1</td>
        <td class="given">−i</td>
        <td id="c4"  class="empty" onclick="fillCell(this,'1')"></td>
        <td id="c5"  class="empty" onclick="fillCell(this,'i')"></td>
        <td id="c6"  class="empty" onclick="fillCell(this,'-1')"></td>
        <td id="c7"  class="empty" onclick="fillCell(this,'-i')"></td>
        <td id="c8"  class="empty" onclick="fillCell(this,'1')"></td>
        <td id="c9"  class="empty" onclick="fillCell(this,'i')"></td>
        <td id="c10" class="empty" onclick="fillCell(this,'-1')"></td>
        <td id="c11" class="empty" onclick="fillCell(this,'-i')"></td>
        <td id="c12" class="empty" onclick="fillCell(this,'1')"></td>
      </tr></tbody>
    </table>
  </div>
  <div class="table-progress" id="tableProgress">빈 칸 9개를 채워 보세요.</div>
  <div class="reveal-box" id="tableReveal">
    <div class="reveal-text">
      🎉 <strong>완성!</strong> 패턴이 보이나요?<br><br>
      i⁴ = 1이므로 지수가 4만큼 커질 때마다 <strong>원래 값으로 돌아옵니다 (주기 = 4).</strong><br>
      따라서 iⁿ의 값은 <strong>n을 4로 나눈 나머지</strong>에 따라 결정됩니다!<br><br>
      &nbsp;• 나머지가 1이면 → <strong>i</strong><br>
      &nbsp;• 나머지가 2이면 → <strong>−1</strong><br>
      &nbsp;• 나머지가 3이면 → <strong>−i</strong><br>
      &nbsp;• 나머지가 0이면 (4의 배수) → <strong>1</strong>
    </div>
  </div>
</section>
</div>

<!-- TAB 2: 나침반 -->
<div class="tab-panel" id="tab-t2">
<section class="sec">
  <div class="sec-title">🧭 미션 2 · i의 나침반 – 복소평면에서 90° 회전</div>
  <div class="sec-desc">
    복소평면에서 i를 한 번 곱하면 <strong>반시계 방향으로 90° 회전</strong>합니다.
    버튼을 눌러 1에서 출발해 i를 차례로 곱해 보세요!
  </div>
  <div class="compass-wrap">
    <div class="canvas-col">
      <canvas id="compass" width="240" height="240"></canvas>
      <div class="btn-row">
        <button class="btn btn-purple" onclick="rotatePow()">× i 곱하기</button>
        <button class="btn btn-ghost"  onclick="resetCompass()">↺ 초기화</button>
      </div>
    </div>
    <div class="info-col">
      <div class="power-disp" id="powDisp">시작: 1 (i⁰)</div>
      <div class="dir-grid">
        <div class="dir-card active" id="dc0"><div class="dir-label">i⁰ = 1</div><div class="dir-value">→ 오른쪽 (실수축 +)</div></div>
        <div class="dir-card" id="dc1"><div class="dir-label">i¹ = i</div><div class="dir-value">↑ 위쪽 (허수축 +)</div></div>
        <div class="dir-card" id="dc2"><div class="dir-label">i² = −1</div><div class="dir-value">← 왼쪽 (실수축 −)</div></div>
        <div class="dir-card" id="dc3"><div class="dir-label">i³ = −i</div><div class="dir-value">↓ 아래쪽 (허수축 −)</div></div>
      </div>
      <div class="tip-box">
        💡 <strong>핵심:</strong> i를 한 번 곱할 때마다 90° 반시계 회전!<br>
        4번 곱하면 360° 회전 → 제자리 → i⁴ = 1<br><br>
        이것이 바로 주기 4의 기하학적 의미입니다.
      </div>
    </div>
  </div>
</section>
</div>

<!-- TAB 3: 합 탐구 -->
<div class="tab-panel" id="tab-t3">
<section class="sec">
  <div class="sec-title">➕ 미션 3 · i의 합 탐구기</div>
  <div class="sec-desc">
    슬라이더를 움직여 i + i² + ... + iⁿ 의 값을 탐구하세요.
    연속 4개씩 묶으면 패턴이 보입니다!
  </div>
  <div class="sum-grid">
    <div class="slider-col">
      <div class="slider-label">n = <span id="sliderVal">8</span></div>
      <input type="range" id="nSlider" min="1" max="20" value="8" oninput="updateSum()">
      <div style="color:#a78bfa;font-size:.8rem">1 ~ 20 사이 탐구 (4의 배수를 꼭 확인!)</div>
      <div class="pattern-box">
        <div class="pattern-label">🔍 규칙:</div>
        <div class="pattern-text" id="patternText"></div>
      </div>
    </div>
    <div class="sum-panel">
      <div class="sum-formula" id="sumFormula"></div>
      <div class="sum-groups" id="sumGroups"></div>
      <div class="sum-result" id="sumResult"></div>
    </div>
  </div>
  <div class="quiz-block">
    <div class="quiz-title">🏆 핵심 문제: i + i² + i³ + ... + i¹⁰⁰ = ?</div>
    <div class="quiz-desc">
      슬라이더에서 n = 4, 8, 12, 16, 20 일 때의 합을 확인하고 패턴을 찾아 답하세요.
      100 = 4 × 25 라는 사실을 활용해 보세요!
    </div>
    <div class="qchoices" id="q100choices">
      <button class="qchoice" data-val="0"  onclick="check100(this)">0</button>
      <button class="qchoice" data-val="1"  onclick="check100(this)">1</button>
      <button class="qchoice" data-val="i"  onclick="check100(this)">i</button>
      <button class="qchoice" data-val="-1" onclick="check100(this)">−1</button>
    </div>
    <div class="q-feedback" id="q100fb"></div>
  </div>
</section>
</div>

<!-- TAB 4: 신기한 성질 -->
<div class="tab-panel" id="tab-t4">
<section class="sec">
  <div class="sec-title">✨ i의 신기한 성질 모음</div>
  <div class="props-grid">
    <div class="prop-card">
      <div class="prop-icon">🔁</div>
      <div class="prop-title">역수도 i의 거듭제곱!</div>
      <div class="prop-body">
        1/i = −i 입니다. 분자·분모에 i를 곱하면:<br>
        <span class="pf">1/i = i/i² = i/(−1) = −i</span><br>
        즉 i⁻¹ = −i = i³ → 주기 4가 그대로 성립!
      </div>
    </div>
    <div class="prop-card">
      <div class="prop-icon">🌀</div>
      <div class="prop-title">연속 4개의 합은 항상 0</div>
      <div class="prop-body">
        어떤 자연수 k에 대해서도:<br>
        <span class="pf">iᵏ + iᵏ⁺¹ + iᵏ⁺² + iᵏ⁺³ = 0</span><br>
        iᵏ으로 묶으면 iᵏ(1+i−1−i) = iᵏ · 0 = 0
      </div>
    </div>
    <div class="prop-card">
      <div class="prop-icon">💎</div>
      <div class="prop-title">i는 x⁴=1의 허수 근</div>
      <div class="prop-body">
        i, −1, −i, 1은 모두 x⁴ = 1의 해입니다.<br>
        <span class="pf">x⁴ − 1 = 0</span>의 4개의 근이<br>
        복소평면에서 <strong>정사각형</strong>을 이룹니다!
      </div>
    </div>
    <div class="prop-card">
      <div class="prop-icon">⚡</div>
      <div class="prop-title">(1+i)를 반복 곱하면?</div>
      <div class="prop-body">
        (1+i)² = 2i,&nbsp;&nbsp;(1+i)⁴ = −4<br>
        <span class="pf">(1+i)⁸ = 16</span><br>
        8번 곱하면 다시 실수! 복소 회전의 묘미입니다.
      </div>
    </div>
  </div>
</section>
</div>

<!-- TAB 5: 큰 지수 계산기 -->
<div class="tab-panel" id="tab-t5">
<section class="sec">
  <div class="sec-title">⚡ 미션 4 · 어떤 지수든 바로 계산하기</div>
  <div class="sec-desc">
    iⁿ의 값은 <strong>n을 4로 나눈 나머지</strong>만 알면 바로 구할 수 있습니다.
    아무 정수나 입력해 보세요. 음수 지수도 도전!
  </div>
  <div class="modcalc-grid">
    <div class="inp-panel">
      <div class="inp-label">지수 n 입력 (정수, 음수 가능)</div>
      <input type="number" id="modInp" value="2023" oninput="calcMod()">
      <div class="inp-hint">예: 101, 2023, −5, 1000, 4000001 ...</div>
    </div>
    <div class="res-panel">
      <div class="res-label">계산 과정</div>
      <div class="res-chain" id="resChain"></div>
      <div class="res-final" id="resFinal"></div>
    </div>
  </div>
  <div style="margin-top:14px;background:rgba(109,40,217,.1);border:1px solid rgba(150,100,255,.2);border-radius:14px;padding:14px">
    <div style="color:#c4a0ff;font-size:.84rem;font-weight:700;margin-bottom:8px">📌 핵심 규칙 정리</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px">
      <div style="text-align:center;background:rgba(109,40,217,.2);border-radius:10px;padding:10px">
        <div style="color:#a78bfa;font-size:.76rem;margin-bottom:4px">나머지 1</div>
        <div style="color:#e0d0ff;font-weight:800;font-size:1.1rem">i</div>
      </div>
      <div style="text-align:center;background:rgba(109,40,217,.2);border-radius:10px;padding:10px">
        <div style="color:#a78bfa;font-size:.76rem;margin-bottom:4px">나머지 2</div>
        <div style="color:#e0d0ff;font-weight:800;font-size:1.1rem">−1</div>
      </div>
      <div style="text-align:center;background:rgba(109,40,217,.2);border-radius:10px;padding:10px">
        <div style="color:#a78bfa;font-size:.76rem;margin-bottom:4px">나머지 3</div>
        <div style="color:#e0d0ff;font-weight:800;font-size:1.1rem">−i</div>
      </div>
      <div style="text-align:center;background:rgba(109,40,217,.2);border-radius:10px;padding:10px">
        <div style="color:#a78bfa;font-size:.76rem;margin-bottom:4px">나머지 0</div>
        <div style="color:#e0d0ff;font-weight:800;font-size:1.1rem">1</div>
      </div>
    </div>
  </div>
</section>
</div>

<!-- TAB 6: 도전 미션 -->
<div class="tab-panel" id="tab-t6">
<section class="sec">
  <div class="sec-title">🎯 도전 미션 5선</div>
  <div class="score-bar">
    <div class="score-item"><div class="score-label">정답</div><div class="score-val" id="scOk">0</div></div>
    <div class="score-item"><div class="score-label">오답</div><div class="score-val" id="scNg">0</div></div>
    <div class="score-item"><div class="score-label">남은 문제</div><div class="score-val" id="scLeft">5</div></div>
  </div>

  <div class="mission-card">
    <div class="mnum">1</div>
    <div class="mq">i²⁰²³의 값은?</div>
    <div class="mchoices">
      <button class="mchoice" data-val="i"  onclick="chk(1,this,'-i')">i</button>
      <button class="mchoice" data-val="-1" onclick="chk(1,this,'-i')">−1</button>
      <button class="mchoice" data-val="-i" onclick="chk(1,this,'-i')">−i</button>
      <button class="mchoice" data-val="1"  onclick="chk(1,this,'-i')">1</button>
    </div>
    <div class="mexplain" id="exp1">
      2023 ÷ 4 = 505 … 나머지 <strong>3</strong><br>
      → 나머지가 3이므로 i²⁰²³ = i³ = <strong>−i</strong>
    </div>
  </div>

  <div class="mission-card">
    <div class="mnum">2</div>
    <div class="mq">i + i² + i³ + i⁴ + i⁵ = ?</div>
    <div class="mchoices">
      <button class="mchoice" data-val="0"  onclick="chk(2,this,'i')">0</button>
      <button class="mchoice" data-val="i"  onclick="chk(2,this,'i')">i</button>
      <button class="mchoice" data-val="-1" onclick="chk(2,this,'i')">−1</button>
      <button class="mchoice" data-val="1"  onclick="chk(2,this,'i')">1</button>
    </div>
    <div class="mexplain" id="exp2">
      앞 4개의 합 (i + (−1) + (−i) + 1) = 0, 남은 항 i⁵ = i<br>
      → 합 = 0 + <strong>i</strong> = i
    </div>
  </div>

  <div class="mission-card">
    <div class="mnum">3</div>
    <div class="mq">i⁻⁵의 값은? &nbsp;(힌트: −5를 4로 나눈 나머지를 구하세요)</div>
    <div class="mchoices">
      <button class="mchoice" data-val="i"  onclick="chk(3,this,'-i')">i</button>
      <button class="mchoice" data-val="-1" onclick="chk(3,this,'-i')">−1</button>
      <button class="mchoice" data-val="-i" onclick="chk(3,this,'-i')">−i</button>
      <button class="mchoice" data-val="1"  onclick="chk(3,this,'-i')">1</button>
    </div>
    <div class="mexplain" id="exp3">
      −5 = (−2) × 4 + 3 → 나머지 <strong>3</strong><br>
      → 나머지가 3이므로 i⁻⁵ = i³ = <strong>−i</strong><br>
      검산: 1/i⁵ = 1/i = i/i² = i/(−1) = −i ✓
    </div>
  </div>

  <div class="mission-card">
    <div class="mnum">4</div>
    <div class="mq">(1 + i)⁴ 의 값은? &nbsp;(힌트: 먼저 (1+i)²를 전개하세요)</div>
    <div class="mchoices">
      <button class="mchoice" data-val="4"  onclick="chk(4,this,'-4')">4</button>
      <button class="mchoice" data-val="-4" onclick="chk(4,this,'-4')">−4</button>
      <button class="mchoice" data-val="4i" onclick="chk(4,this,'-4')">4i</button>
      <button class="mchoice" data-val="2i" onclick="chk(4,this,'-4')">2i</button>
    </div>
    <div class="mexplain" id="exp4">
      (1+i)² = 1 + 2i + i² = 1 + 2i − 1 = 2i<br>
      → (1+i)⁴ = (2i)² = 4i² = 4 × (−1) = <strong>−4</strong>
    </div>
  </div>

  <div class="mission-card">
    <div class="mnum">5</div>
    <div class="mq">n이 자연수일 때, i⁴ⁿ⁺² 의 값은?</div>
    <div class="mchoices">
      <button class="mchoice" data-val="i"  onclick="chk(5,this,'-1')">i</button>
      <button class="mchoice" data-val="-1" onclick="chk(5,this,'-1')">−1</button>
      <button class="mchoice" data-val="-i" onclick="chk(5,this,'-1')">−i</button>
      <button class="mchoice" data-val="1"  onclick="chk(5,this,'-1')">1</button>
    </div>
    <div class="mexplain" id="exp5">
      4n+2를 4로 나누면 나머지는 항상 <strong>2</strong><br>
      i⁴ⁿ = (i⁴)ⁿ = 1ⁿ = 1<br>
      → i⁴ⁿ⁺² = i⁴ⁿ · i² = 1 × (−1) = <strong>−1</strong><br>
      n이 어떤 자연수여도 값은 항상 −1!
    </div>
  </div>
</section>
</div>

</div><!-- shell -->
<script>
// ── 탭 전환 ────────────────────────────────────────────────────────────
function showTab(name){
  document.querySelectorAll('.tab-btn').forEach(function(b){ b.classList.remove('active'); });
  document.querySelectorAll('.tab-panel').forEach(function(p){ p.classList.remove('active'); });
  document.querySelector('.tab-btn[data-tab="'+name+'"]').classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
  if(name==='t2'){ drawCompass(cPow); }
}

// ── 순환표 채우기 ──────────────────────────────────────────────────────
var selVal=null, fillCount=0;
var DISP={'i':'i','-1':'−1','-i':'−i','1':'1'};

function selFill(btn,v){
  document.querySelectorAll('.fchoice').forEach(function(b){b.classList.remove('active')});
  btn.classList.add('active');
  selVal=v;
}
function fillCell(td,correct){
  if(!selVal){
    td.style.outline='2px solid #f59e0b';
    setTimeout(function(){td.style.outline=''},900);
    return;
  }
  if(td.classList.contains('correct')) return;
  if(selVal===correct){
    td.textContent=DISP[correct];
    td.classList.remove('empty','wrong');
    td.classList.add('correct');
    td.onclick=null;
    fillCount++;
    var left=9-fillCount;
    document.getElementById('tableProgress').textContent=
      left>0?('빈 칸 '+left+'개 남았습니다.'):'✅ 모든 칸 완성! 아래에서 패턴을 확인하세요.';
    if(fillCount===9) document.getElementById('tableReveal').classList.add('show');
  } else {
    td.classList.add('wrong');
    setTimeout(function(){td.classList.remove('wrong');},480);
  }
}

// ── i 나침반 ───────────────────────────────────────────────────────────
var cPow=0;
var CVALS=[
  {label:'1', x:1,  y:0,  color:'#a78bfa'},
  {label:'i', x:0,  y:1,  color:'#818cf8'},
  {label:'−1',x:-1, y:0,  color:'#c084fc'},
  {label:'−i',x:0,  y:-1, color:'#e879f9'}
];
var SUP=['⁰','¹','²','³','⁴','⁵','⁶','⁷','⁸','⁹'];
function toSup(n){return String(Math.abs(n)).split('').map(function(c){return SUP[+c]||c}).join('');}

function drawCompass(pow){
  var canvas=document.getElementById('compass');
  var ctx=canvas.getContext('2d');
  var W=canvas.width,H=canvas.height,cx=W/2,cy=H/2,r=84;
  ctx.clearRect(0,0,W,H);
  ctx.strokeStyle='rgba(150,100,255,.2)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(cx-r-22,cy);ctx.lineTo(cx+r+22,cy);ctx.stroke();
  ctx.beginPath();ctx.moveTo(cx,cy-r-22);ctx.lineTo(cx,cy+r+22);ctx.stroke();
  ctx.strokeStyle='rgba(150,100,255,.22)';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);ctx.stroke();
  ctx.fillStyle='rgba(160,130,255,.5)';ctx.font='11px Segoe UI';ctx.textAlign='center';
  ctx.fillText('+실수',cx+r+14,cy+4);
  ctx.fillText('−실수',cx-r-14,cy+4);
  ctx.fillText('+허수',cx,cy-r-10);
  ctx.fillText('−허수',cx,cy+r+16);
  CVALS.forEach(function(p){
    var px=cx+p.x*r,py=cy-p.y*r;
    ctx.beginPath();ctx.arc(px,py,5,0,Math.PI*2);
    ctx.fillStyle='rgba(150,100,255,.18)';ctx.fill();
  });
  var cur=CVALS[pow%4];
  var px=cx+cur.x*r,py=cy-cur.y*r;
  var ang=Math.atan2(py-cy,px-cx);
  ctx.strokeStyle=cur.color;ctx.lineWidth=2.5;
  ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(px,py);ctx.stroke();
  ctx.fillStyle=cur.color;
  ctx.beginPath();
  ctx.moveTo(px,py);
  ctx.lineTo(px-12*Math.cos(ang-0.4),py-12*Math.sin(ang-0.4));
  ctx.lineTo(px-12*Math.cos(ang+0.4),py-12*Math.sin(ang+0.4));
  ctx.closePath();ctx.fill();
  ctx.beginPath();ctx.arc(px,py,9,0,Math.PI*2);
  ctx.fillStyle=cur.color;ctx.fill();
  ctx.strokeStyle='rgba(255,255,255,.7)';ctx.lineWidth=1.8;ctx.stroke();
  ctx.font='bold 13px Segoe UI';ctx.fillStyle='#fff';
  var lx=px+(cur.x>0?18:cur.x<0?-18:0);
  var ly=py+(cur.y>0?-16:cur.y<0?18:5);
  ctx.fillText(cur.label,lx,ly);
}
function updateCompassInfo(pow){
  var cur=CVALS[pow%4];
  document.getElementById('powDisp').textContent=
    pow===0?'시작: 1 (i⁰)':('i'+toSup(pow)+' = '+cur.label);
  for(var i=0;i<4;i++){
    var el=document.getElementById('dc'+i);
    if(i===pow%4) el.classList.add('active');
    else el.classList.remove('active');
  }
}
function rotatePow(){cPow++;drawCompass(cPow);updateCompassInfo(cPow);}
function resetCompass(){cPow=0;drawCompass(0);updateCompassInfo(0);}

// ── 합 계산기 ──────────────────────────────────────────────────────────
var IVALS=['i','-1','-i','1'];
var IDISP={'i':'i','-1':'−1','-i':'−i','1':'1'};
var INUM={'i':[0,1],'-1':[-1,0],'-i':[0,-1],'1':[1,0]};
function addC(a,b){return[a[0]+b[0],a[1]+b[1]];}
function cStr(c){
  if(c[0]===0&&c[1]===0) return '0';
  if(c[0]===0) return c[1]===1?'i':c[1]===-1?'−i':c[1]+'i';
  if(c[1]===0) return String(c[0]);
  var im=c[1]===1?'+i':c[1]===-1?'−i':(c[1]>0?'+'+c[1]+'i':c[1]+'i');
  return c[0]+im;
}
function updateSum(){
  var n=parseInt(document.getElementById('nSlider').value);
  document.getElementById('sliderVal').textContent=n;
  var sum=[0,0];
  for(var k=1;k<=n;k++) sum=addC(sum,INUM[IVALS[(k-1)%4]]);
  document.getElementById('sumFormula').innerHTML='i + i² + ... + i<sup>'+n+'</sup>';
  var full=Math.floor(n/4),rem=n%4,html='';
  for(var g=0;g<full;g++){
    if(g>0) html+='<span class="sg-plus">+</span>';
    html+='<span class="sg-zero">(i−1−i+1)</span>';
  }
  if(rem>0){
    var pts=[];
    for(var k=1;k<=rem;k++) pts.push(IDISP[IVALS[(k-1)%4]]);
    if(full>0) html+='<span class="sg-plus">+</span>';
    html+='<span class="sg-rem">('+pts.join('+')+') ← 나머지 '+rem+'개</span>';
  }
  document.getElementById('sumGroups').innerHTML=html||'<span class="sg-zero">(항 없음)</span>';
  document.getElementById('sumResult').innerHTML='= <strong>'+cStr(sum)+'</strong>';
  var pat='';
  if(rem===0) pat='4로 나눈 나머지가 0 (4의 배수) → 완전한 묶음 '+full+'개 → 합 = 0';
  else if(rem===1) pat='4로 나눈 나머지가 1 → 남는 항 i → 합 = i';
  else if(rem===2) pat='4로 나눈 나머지가 2 → 남는 항 i+(−1) → 합 = −1';
  else if(rem===3) pat='4로 나눈 나머지가 3 → 남는 항 i+(−1)+(−i) → 합 = −i';
  document.getElementById('patternText').textContent=pat;
}
var q100done=false;
function check100(btn){
  if(q100done) return;
  q100done=true;
  var v=btn.dataset.val;
  document.querySelectorAll('#q100choices .qchoice').forEach(function(b){
    b.onclick=null;
    if(b.dataset.val==='0') b.classList.add('ok');
    else if(b===btn&&v!=='0') b.classList.add('ng');
  });
  var fb=document.getElementById('q100fb');
  if(v==='0'){
    fb.style.color='#86efac';
    fb.textContent='✅ 정답! 100 ÷ 4 = 25 나머지 0 → 25개의 완전한 묶음 → 합 = 0';
  } else {
    fb.style.color='#fca5a5';
    fb.textContent='❌ 슬라이더에서 n=4, 8, 12일 때 합을 다시 확인해 보세요!';
  }
}

// ── 큰 지수 계산기 ─────────────────────────────────────────────────────
var IMAP={0:'1',1:'i',2:'−1',3:'−i'};
function calcMod(){
  var n=parseInt(document.getElementById('modInp').value,10);
  if(isNaN(n)){
    document.getElementById('resChain').innerHTML='숫자를 입력하세요';
    document.getElementById('resFinal').innerHTML='';
    return;
  }
  var r=((n%4)+4)%4;
  document.getElementById('resChain').innerHTML=
    'n = '+n+'<br>'+
    Math.abs(n)+' ÷ 4 = '+Math.floor(Math.abs(n)/4)+' … 나머지 <strong>'+r+'</strong><br>'+
    '→ i<sup>'+n+'</sup> = (i<sup>4</sup>)<sup>□</sup> × i<sup>'+r+'</sup> = 1 × i<sup>'+r+'</sup>';
  document.getElementById('resFinal').innerHTML='i<sup>'+n+'</sup> = <strong>'+IMAP[r]+'</strong>';
}

// ── 도전 미션 ───────────────────────────────────────────────────────────
var okCount=0,ngCount=0,done=new Set();
function chk(qNum,btn,correct){
  if(done.has(qNum)) return;
  done.add(qNum);
  var sel=btn.dataset.val;
  var card=document.querySelectorAll('.mission-card')[qNum-1];
  card.querySelectorAll('.mchoice').forEach(function(b){
    b.onclick=null;
    if(b.dataset.val===correct) b.classList.add('ok');
  });
  if(sel!==correct) btn.classList.add('ng');
  if(sel===correct) okCount++; else ngCount++;
  document.getElementById('scOk').textContent=okCount;
  document.getElementById('scNg').textContent=ngCount;
  document.getElementById('scLeft').textContent=5-done.size;
  document.getElementById('exp'+qNum).classList.add('show');
}

// ── 초기화 ─────────────────────────────────────────────────────────────
drawCompass(0);
updateCompassInfo(0);
updateSum();
calcMod();
</script>
</body>
</html>"""


def render():
    st.set_page_config(page_title="허수단위 i의 순환 탐구", layout="wide")
    st.markdown(
        """
        <style>
        .main { max-width: 100%; }
        iframe { width: 100% !important; height: 2200px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    components.html(_HTML, height=1800, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
