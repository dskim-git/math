# activities/common/mini/omega_law_explorer.py
"""
ω-법칙 탐구 미니활동
x³=1의 허수근 ω의 4가지 성질 탐구 + 다양한 ω 거듭제곱 식 계산 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "오메가법칙탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key": "순환이유",
        "label": "ω의 거듭제곱이 주기 3으로 순환하는 이유를 ω³=1을 이용해 설명하세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "핵심성질활용",
        "label": "ωⁿ 형태의 식을 계산할 때 가장 유용한 성질은 무엇이고, 어떻게 활용하나요? 구체적인 예를 들어 설명하세요.",
        "type": "text_area",
        "height": 100,
    },
    {
        "key": "연속합전략",
        "label": "ω³⁰+ω²⁹+···+ω+1처럼 연속된 ω 거듭제곱의 합을 구하는 전략을 설명하세요.",
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
    "title": "🌀 ω-법칙 탐구",
    "description": "x³=1의 허수근 ω의 4가지 핵심 성질을 탐구하고, 순환표·계산기·단계별 풀이·도전 문제로 ω 법칙을 완벽히 익히는 활동입니다.",
    "order": 253,
    "hidden": False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ω-법칙 탐구</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(155deg,#060d18 0%,#0c1f34 50%,#060d18 100%);
  color:#e0f2fe;min-height:100vh;padding:12px 10px 24px;
}
.shell{max-width:1060px;margin:0 auto}
.conj{text-decoration:overline}

/* ── Hero ── */
.hero{
  position:relative;overflow:hidden;
  background:linear-gradient(135deg,rgba(20,184,166,.18),rgba(5,150,105,.1));
  border:1px solid rgba(20,184,166,.35);border-radius:22px;
  padding:18px 24px;margin-bottom:14px;
}
.hero::before{
  content:'ω';position:absolute;right:20px;top:-14px;
  font-size:160px;font-weight:900;color:rgba(20,184,166,.06);
  pointer-events:none;line-height:1;font-family:'Times New Roman',serif;
}
.hero>*{position:relative;z-index:1}
.hero-tag{
  display:inline-flex;align-items:center;gap:6px;
  background:rgba(20,184,166,.18);border:1px solid rgba(20,184,166,.35);
  border-radius:999px;padding:4px 12px;
  color:#5eead4;font-size:.76rem;font-weight:700;letter-spacing:.07em;margin-bottom:10px;
}
.hero h1{font-size:1.55rem;font-weight:900;color:#fff;margin-bottom:6px}
.hero p{color:#94d5cc;line-height:1.7;font-size:.88rem;max-width:820px}
.hero strong{color:#2dd4bf}
.hero .def-box{
  display:inline-block;margin-top:10px;
  background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.25);
  border-radius:10px;padding:8px 16px;
  font-family:'Times New Roman',Georgia,serif;font-style:italic;
  color:#fde68a;font-size:1rem;line-height:1.8;
}

/* ── Tabs ── */
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.tab-btn{
  padding:8px 14px;border-radius:12px;
  background:rgba(20,184,166,.1);border:1px solid rgba(20,184,166,.2);
  color:#5eead4;font-size:.82rem;font-weight:700;cursor:pointer;
  transition:all .18s;white-space:nowrap;
}
.tab-btn:hover{background:rgba(20,184,166,.22);border-color:#14b8a6;color:#99f6e4}
.tab-btn.active{
  background:linear-gradient(135deg,#0d9488,#14b8a6);
  border-color:#2dd4bf;color:#fff;
  box-shadow:0 4px 14px rgba(20,184,166,.4);
}
.tab-panel{display:none}
.tab-panel.active{display:block;animation:fadeUp .28s ease}
@keyframes fadeUp{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

/* ── Section ── */
.sec{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(20,184,166,.18);
  border-radius:20px;padding:18px 20px;margin-bottom:12px;
}
.sec-title{
  font-size:1rem;font-weight:800;color:#2dd4bf;
  margin-bottom:10px;display:flex;align-items:center;gap:8px;
}
.sec-desc{color:#94d5cc;font-size:.86rem;line-height:1.72;margin-bottom:14px}

/* ── Property grid (Tab 1) ── */
.prop-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px}
.prop-card{
  background:rgba(6,13,24,.65);border:1.5px solid rgba(20,184,166,.22);
  border-radius:16px;padding:14px 16px;transition:border-color .2s;
}
.prop-card:hover{border-color:rgba(20,184,166,.5)}
.prop-badge{
  display:inline-flex;align-items:center;justify-content:center;
  width:28px;height:28px;border-radius:50%;
  background:linear-gradient(135deg,#0d9488,#14b8a6);
  color:#fff;font-size:.82rem;font-weight:900;margin-bottom:8px;
}
.prop-title{font-size:.83rem;font-weight:800;color:#5eead4;margin-bottom:6px}
.prop-formula{
  font-family:'Times New Roman',Georgia,serif;font-style:italic;
  font-size:1.1rem;color:#fde68a;line-height:1.85;margin-bottom:7px;
}
.prop-why{color:#94d5cc;font-size:.83rem;line-height:1.75}
.prop-why strong{color:#2dd4bf}
.proof-btn{
  margin-top:8px;padding:5px 12px;border-radius:8px;
  background:rgba(20,184,166,.1);border:1px solid rgba(20,184,166,.22);
  color:#5eead4;font-size:.78rem;font-weight:700;cursor:pointer;transition:all .15s;
}
.proof-btn:hover{background:rgba(20,184,166,.22)}
.proof-box{
  display:none;margin-top:8px;padding:10px 12px;border-radius:10px;
  background:rgba(13,148,136,.08);border:1px solid rgba(20,184,166,.2);
  color:#a7f3d0;font-size:.82rem;line-height:1.85;
}
.proof-box.open{display:block;animation:fadeUp .25s ease}

.key-formula{
  background:rgba(245,158,11,.07);border:1px solid rgba(245,158,11,.25);
  border-radius:14px;padding:14px 18px;text-align:center;
  font-family:'Times New Roman',Georgia,serif;font-style:italic;
  font-size:1.15rem;color:#fde68a;line-height:1.9;
}
.key-formula .label{font-family:'Malgun Gothic',sans-serif;font-style:normal;
  font-size:.75rem;font-weight:700;color:#f59e0b;letter-spacing:.05em;
  display:block;margin-bottom:4px;}

/* ── Fill table (Tab 2) ── */
.fill-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;align-items:center}
.fill-label{color:#5eead4;font-size:.84rem;font-weight:700}
.fchoice{
  padding:8px 18px;border-radius:12px;
  background:rgba(20,184,166,.12);border:1px solid rgba(20,184,166,.22);
  color:#5eead4;font-size:1rem;font-weight:700;cursor:pointer;
  transition:all .18s;user-select:none;
  font-family:'Times New Roman',Georgia,serif;font-style:italic;
}
.fchoice:hover{background:rgba(20,184,166,.25);border-color:#14b8a6;color:#99f6e4}
.fchoice.active{
  background:linear-gradient(135deg,rgba(13,148,136,.55),rgba(20,184,166,.45));
  border-color:#5eead4;color:#fff;transform:translateY(-1px);
  box-shadow:0 6px 18px rgba(20,184,166,.3);
}
.cycle-wrap{overflow-x:auto;margin-bottom:12px}
.cycle-table{border-collapse:separate;border-spacing:4px;min-width:560px}
.cycle-table th{
  background:linear-gradient(135deg,#0d9488,#14b8a6);
  color:#fff;font-weight:800;font-size:.86rem;
  padding:10px 6px;border-radius:10px;text-align:center;min-width:58px;
  font-family:'Times New Roman',Georgia,serif;
}
.cycle-table td{
  background:rgba(6,13,24,.8);border:1.5px dashed rgba(20,184,166,.28);
  border-radius:10px;padding:10px 6px;
  text-align:center;font-size:1rem;font-weight:700;
  color:#5eead4;cursor:pointer;transition:all .18s;min-width:58px;
  font-family:'Times New Roman',Georgia,serif;font-style:italic;
}
.cycle-table td.empty:hover{background:rgba(20,184,166,.18);transform:scale(1.06)}
.cycle-table td.given{
  background:rgba(13,148,136,.22);border:1.5px solid rgba(20,184,166,.32);
  color:#99f6e4;cursor:default;
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
.tbl-progress{color:#5eead4;font-size:.84rem;margin-bottom:8px;min-height:18px}
.reveal-box{
  display:none;border-radius:16px;padding:14px 16px;margin-top:10px;
  background:rgba(34,197,94,.07);border:1px solid rgba(34,197,94,.28);
}
.reveal-box.show{display:block;animation:fadeUp .4s ease}
.reveal-text{color:#a7f3d0;font-size:.88rem;line-height:1.9}
.reveal-text strong{color:#6ee7b7}

/* ── Calc (Tab 2) ── */
.t2-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start}
.calc-panel{
  background:rgba(6,13,24,.75);border:1px solid rgba(20,184,166,.2);
  border-radius:16px;padding:16px;
}
.calc-label{color:#5eead4;font-size:.84rem;font-weight:700;margin-bottom:8px}
input[type=number]{
  width:100%;padding:10px 14px;border-radius:10px;
  background:rgba(20,184,166,.12);border:1.5px solid rgba(20,184,166,.25);
  color:#e0f2fe;font-size:1.1rem;font-weight:700;outline:none;font-family:inherit;
}
input[type=number]:focus{border-color:#14b8a6}
.calc-step{color:#94d5cc;font-size:.88rem;line-height:1.85;margin-top:10px;min-height:50px}
.calc-final{
  font-size:1.2rem;font-weight:900;
  background:linear-gradient(135deg,rgba(13,148,136,.25),rgba(20,184,166,.15));
  border:1px solid rgba(20,184,166,.3);border-radius:12px;
  padding:10px 14px;text-align:center;margin-top:8px;min-height:42px;
  font-family:'Times New Roman',Georgia,serif;font-style:italic;color:#fde68a;
}

/* ── Step problems (Tab 3) ── */
.problem-card{
  background:rgba(6,13,24,.65);border:1.5px solid rgba(20,184,166,.2);
  border-radius:18px;padding:16px 18px;margin-bottom:14px;
}
.prob-num{
  display:inline-flex;align-items:center;justify-content:center;
  width:30px;height:30px;border-radius:50%;
  background:linear-gradient(135deg,#0d9488,#14b8a6);
  color:#fff;font-size:.85rem;font-weight:900;margin-bottom:10px;
}
.prob-q{
  font-family:'Times New Roman',Georgia,serif;font-style:italic;
  font-size:1.3rem;color:#fde68a;
  background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.2);
  border-radius:10px;padding:10px 14px;text-align:center;margin-bottom:14px;
}
.step-block{margin-bottom:12px}
.step-hint{
  background:rgba(20,184,166,.07);border:1px solid rgba(20,184,166,.18);
  border-radius:10px;padding:9px 12px;
  color:#94d5cc;font-size:.85rem;line-height:1.72;margin-bottom:7px;
}
.step-hint strong{color:#2dd4bf}
.choices{display:flex;gap:7px;flex-wrap:wrap}
.schoice{
  padding:8px 16px;border-radius:11px;
  background:rgba(20,184,166,.1);border:1px solid rgba(20,184,166,.2);
  color:#5eead4;font-size:.95rem;font-weight:700;cursor:pointer;transition:all .18s;
  font-family:'Times New Roman',Georgia,serif;font-style:italic;
}
.schoice:hover{background:rgba(20,184,166,.22);border-color:#14b8a6;transform:translateY(-1px)}
.schoice.ok{background:rgba(34,197,94,.18);border-color:rgba(34,197,94,.4);color:#86efac;cursor:default}
.schoice.ng{background:rgba(239,68,68,.14);border-color:rgba(239,68,68,.35);color:#fca5a5;cursor:default}
.step-fb{
  display:none;padding:8px 12px;border-radius:10px;margin-top:6px;
  font-size:.84rem;line-height:1.72;
}
.step-fb.show{display:block;animation:fadeUp .3s ease}
.step-fb.ok{background:rgba(34,197,94,.09);border:1px solid rgba(34,197,94,.28);color:#a7f3d0}
.step-fb.ng{background:rgba(239,68,68,.09);border:1px solid rgba(239,68,68,.28);color:#fca5a5}
.final-ans{
  display:none;margin-top:12px;padding:12px 16px;border-radius:14px;
  background:linear-gradient(135deg,rgba(13,148,136,.2),rgba(20,184,166,.12));
  border:1.5px solid rgba(20,184,166,.45);
  font-family:'Times New Roman',Georgia,serif;font-style:italic;
  font-size:1.2rem;color:#fde68a;text-align:center;font-weight:700;
}
.final-ans.show{display:block;animation:fadeUp .4s ease}

/* ── Quiz (Tab 4) ── */
.score-bar{
  display:flex;justify-content:space-around;
  background:rgba(20,184,166,.1);border:1px solid rgba(20,184,166,.18);
  border-radius:13px;padding:11px;margin-bottom:13px;
}
.score-item{text-align:center}
.score-lbl{font-size:.73rem;color:#5eead4;margin-bottom:3px}
.score-val{font-size:1.15rem;font-weight:900;color:#e0f2fe}
.quiz-card{
  background:rgba(6,13,24,.65);border:1.5px solid rgba(20,184,166,.18);
  border-radius:16px;padding:14px 16px;margin-bottom:10px;
}
.qnum-badge{
  display:inline-flex;align-items:center;justify-content:center;
  width:26px;height:26px;border-radius:50%;
  background:linear-gradient(135deg,#0d9488,#14b8a6);
  color:#fff;font-size:.78rem;font-weight:900;margin-bottom:8px;
}
.diff{
  display:inline-block;font-size:.72rem;font-weight:700;padding:2px 8px;
  border-radius:99px;margin-left:6px;vertical-align:middle;
}
.diff-e{background:rgba(34,197,94,.15);color:#34d399;border:1px solid rgba(34,197,94,.3)}
.diff-m{background:rgba(245,158,11,.15);color:#fbbf24;border:1px solid rgba(245,158,11,.3)}
.diff-h{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.3)}
.q-text{font-size:.92rem;font-weight:700;color:#e0f2fe;margin-bottom:11px;line-height:1.6}
.q-math{font-family:'Times New Roman',Georgia,serif;font-style:italic;color:#fde68a;font-size:1.1rem}
.qchoices{display:flex;gap:7px;flex-wrap:wrap}
.qchoice{
  padding:8px 18px;border-radius:11px;
  background:rgba(20,184,166,.1);border:1px solid rgba(20,184,166,.2);
  color:#5eead4;font-size:.95rem;font-weight:700;cursor:pointer;transition:all .18s;
  font-family:'Times New Roman',Georgia,serif;font-style:italic;
}
.qchoice:hover{background:rgba(20,184,166,.22);border-color:#14b8a6;color:#99f6e4;transform:translateY(-1px)}
.qchoice.ok{background:rgba(34,197,94,.18);border-color:rgba(34,197,94,.45);color:#86efac;cursor:default}
.qchoice.ng{background:rgba(239,68,68,.14);border-color:rgba(239,68,68,.38);color:#fca5a5;cursor:default}
.qexp{
  display:none;margin-top:9px;padding:10px 12px;border-radius:11px;
  background:rgba(20,184,166,.07);border:1px solid rgba(20,184,166,.2);
  color:#94d5cc;font-size:.84rem;line-height:1.8;
}
.qexp.show{display:block;animation:fadeUp .3s ease}
.qexp strong{color:#5eead4}

@media(max-width:680px){
  .prop-grid,.t2-grid{grid-template-columns:1fr}
  .hero h1{font-size:1.25rem}
  .tabs{gap:4px}
  .tab-btn{font-size:.76rem;padding:7px 10px}
}
</style>
</head>
<body>
<div class="shell">

<!-- Hero -->
<section class="hero">
  <div class="hero-tag">🌀 ω-법칙 탐구</div>
  <h1>x³=1의 비밀 – ω의 4가지 법칙</h1>
  <p>삼차방정식 x³=1의 허수근 <strong>ω</strong>는 특별한 성질을 가집니다.<br>
  4가지 법칙을 익히면 어떤 ω 거듭제곱도 순식간에 계산할 수 있습니다!</p>
  <div class="def-box">
    ω = <sup>−1+√3 i</sup>⁄<sub>2</sub> &nbsp;,&nbsp;
    <span class="conj">ω</span> = <sup>−1−√3 i</sup>⁄<sub>2</sub>
  </div>
</section>

<!-- Tabs -->
<div class="tabs">
  <button class="tab-btn active" data-tab="t1" onclick="showTab('t1')">🔍 ω 법칙</button>
  <button class="tab-btn" data-tab="t2" onclick="showTab('t2')">🔄 순환 탐구</button>
  <button class="tab-btn" data-tab="t3" onclick="showTab('t3')">📐 기본 계산</button>
  <button class="tab-btn" data-tab="t4" onclick="showTab('t4')">🎯 활용 문제</button>
</div>

<!-- ════════════════════════════════════════
     TAB 1: ω 법칙 4가지
════════════════════════════════════════ -->
<div class="tab-panel active" id="tab-t1">
<section class="sec">
  <div class="sec-title">🔍 ω의 4가지 핵심 성질</div>
  <div class="sec-desc">각 성질 카드를 읽고, 아래 <strong>▼ 증명 보기</strong>를 눌러 왜 성립하는지 확인해 보세요.</div>

  <div class="prop-grid">
    <!-- 성질 1 -->
    <div class="prop-card">
      <div class="prop-badge">1</div>
      <div class="prop-title">주기성 – 3번이면 제자리!</div>
      <div class="prop-formula">
        ω³ = 1 ,&nbsp; <span class="conj">ω</span>³ = 1
      </div>
      <div class="prop-why">
        ω와 <span class="conj">ω</span>는 <strong>x³=1의 해</strong>이므로
        대입하면 바로 성립합니다.
      </div>
      <button class="proof-btn" id="pf1-btn" onclick="toggleProof('pf1')">▼ 증명 보기</button>
      <div class="proof-box" id="pf1">
        x³ − 1 = (x−1)(x²+x+1) = 0<br>
        → x=1 또는 x²+x+1=0의 근<br>
        ω와 <span class="conj">ω</span>는 x²+x+1=0의 근이므로<br>
        ω는 x³=1을 만족 → <strong>ω³=1</strong> ✓
      </div>
    </div>

    <!-- 성질 2 -->
    <div class="prop-card">
      <div class="prop-badge">2</div>
      <div class="prop-title">방정식 관계</div>
      <div class="prop-formula">
        ω² + ω + 1 = 0<br>
        <span class="conj">ω</span>² + <span class="conj">ω</span> + 1 = 0
      </div>
      <div class="prop-why">
        ω와 <span class="conj">ω</span>는 <strong>x²+x+1=0의 해</strong>이므로 직접 대입하면 성립합니다.
      </div>
      <button class="proof-btn" id="pf2-btn" onclick="toggleProof('pf2')">▼ 증명 보기</button>
      <div class="proof-box" id="pf2">
        x³−1 = (x−1)(x²+x+1) = 0 에서<br>
        x ≠ 1 → x²+x+1 = 0<br>
        ω는 이 이차방정식의 근 → <strong>ω²+ω+1=0</strong> ✓<br><br>
        ★ 이 성질이 ω 계산에서 가장 자주 �입니다!
      </div>
    </div>

    <!-- 성질 3 -->
    <div class="prop-card">
      <div class="prop-badge">3</div>
      <div class="prop-title">켤레의 합·곱</div>
      <div class="prop-formula">
        ω + <span class="conj">ω</span> = −1<br>
        ω · <span class="conj">ω</span> = 1
      </div>
      <div class="prop-why">
        ω와 <span class="conj">ω</span>는 <strong>x²+x+1=0의 두 근</strong>이므로
        근과 계수의 관계에 의해 성립합니다.
      </div>
      <button class="proof-btn" id="pf3-btn" onclick="toggleProof('pf3')">▼ 증명 보기</button>
      <div class="proof-box" id="pf3">
        x²+x+1=0의 두 근이 ω, <span class="conj">ω</span>이므로<br>
        근과 계수의 관계에 의해:<br>
        • (두 근의 합) = −(1차 계수)/(최고차 계수) = −1<br>
        → <strong>ω + <span class="conj">ω</span> = −1</strong> ✓<br>
        • (두 근의 곱) = 상수항/최고차 계수 = 1<br>
        → <strong>ω · <span class="conj">ω</span> = 1</strong> ✓
      </div>
    </div>

    <!-- 성질 4 -->
    <div class="prop-card">
      <div class="prop-badge">4</div>
      <div class="prop-title">제곱과 켤레의 관계</div>
      <div class="prop-formula">
        ω² = <span class="conj">ω</span> ,&nbsp; <span class="conj">ω</span>² = ω
      </div>
      <div class="prop-why">
        ω·<span class="conj">ω</span>=1 이라는 사실에서
        양변에 ω를 곱하면 바로 유도됩니다.
      </div>
      <button class="proof-btn" id="pf4-btn" onclick="toggleProof('pf4')">▼ 증명 보기</button>
      <div class="proof-box" id="pf4">
        ω·<span class="conj">ω</span> = 1 양변에 ω를 곱하면:<br>
        ω²·<span class="conj">ω</span> = ω →
        ω²(ω·<span class="conj">ω</span>) 아니라<br>
        ω³·<span class="conj">ω</span> = ω²·1... 다시 정리:<br>
        ω·<span class="conj">ω</span>=1 → ω²·<span class="conj">ω</span>=ω²·(1/ω)=ω<br>
        그런데 ω³=1이므로 1/ω=ω² → <span class="conj">ω</span>=ω² ✓<br>
        마찬가지로 <strong><span class="conj">ω</span>² = ω</strong> ✓
      </div>
    </div>
  </div>

  <!-- 핵심 요약 -->
  <div class="key-formula">
    <span class="label">⭐ 계산에서 가장 자주 쓰는 성질</span>
    ω³ = 1 &nbsp;,&nbsp; ω² + ω + 1 = 0 &nbsp;⟹&nbsp; ω + ω² = −1
  </div>
</section>
</div>

<!-- ════════════════════════════════════════
     TAB 2: 순환 탐구
════════════════════════════════════════ -->
<div class="tab-panel" id="tab-t2">
<section class="sec">
  <div class="sec-title">🔄 미션 1 · ω 순환표 채우기</div>
  <div class="sec-desc">
    값을 먼저 선택한 뒤, 빈 칸을 클릭해서 채워 보세요.
    ω³=1이므로 지수를 <strong>3으로 나눈 나머지</strong>에 따라 값이 결정됩니다!
  </div>
  <div class="fill-row">
    <span class="fill-label">채울 값 →</span>
    <button class="fchoice" onclick="selFill(this,'one')">1</button>
    <button class="fchoice" onclick="selFill(this,'w')">ω</button>
    <button class="fchoice" onclick="selFill(this,'w2')">ω²</button>
  </div>
  <div class="cycle-wrap">
    <table class="cycle-table">
      <thead><tr>
        <th>ω⁰</th><th>ω¹</th><th>ω²</th>
        <th>ω³</th><th>ω⁴</th><th>ω⁵</th>
        <th>ω⁶</th><th>ω⁷</th><th>ω⁸</th>
      </tr></thead>
      <tbody><tr>
        <td class="given">1</td>
        <td class="given">ω</td>
        <td id="c2" class="empty" onclick="fillCell(this,'w2')"></td>
        <td id="c3" class="empty" onclick="fillCell(this,'one')"></td>
        <td id="c4" class="empty" onclick="fillCell(this,'w')"></td>
        <td id="c5" class="empty" onclick="fillCell(this,'w2')"></td>
        <td id="c6" class="empty" onclick="fillCell(this,'one')"></td>
        <td id="c7" class="empty" onclick="fillCell(this,'w')"></td>
        <td id="c8" class="empty" onclick="fillCell(this,'w2')"></td>
      </tr></tbody>
    </table>
  </div>
  <div class="tbl-progress" id="tblProg">빈 칸 7개를 채워 보세요.</div>
  <div class="reveal-box" id="tblReveal">
    <div class="reveal-text">
      🎉 <strong>완성!</strong> 패턴이 보이나요?<br><br>
      ω³=1이므로 지수가 3만큼 커질 때마다 <strong>원래 값으로 돌아옵니다 (주기=3).</strong><br>
      따라서 ωⁿ의 값은 <strong>n을 3으로 나눈 나머지</strong>에 따라 결정됩니다!<br><br>
      &nbsp;• 나머지가 0이면 (3의 배수) → <strong>1</strong><br>
      &nbsp;• 나머지가 1이면 → <strong>ω</strong><br>
      &nbsp;• 나머지가 2이면 → <strong>ω²</strong>
    </div>
  </div>
</section>

<section class="sec">
  <div class="sec-title">⚡ 미션 2 · ω 거듭제곱 계산기</div>
  <div class="t2-grid">
    <div>
      <div class="calc-label">지수 n 입력 (정수, 음수 가능)</div>
      <input type="number" id="omegaInp" value="10" oninput="calcOmega()">
      <div style="color:#5eead4;font-size:.78rem;margin-top:5px">예: 10, 100, 2023, −2, −7 ...</div>
      <div class="calc-step" id="calcStep"></div>
      <div class="calc-final" id="calcFinal"></div>
    </div>
    <div>
      <canvas id="cycleCanvas" width="260" height="260"
        style="border-radius:14px;border:1px solid rgba(20,184,166,.22);display:block;margin:0 auto"></canvas>
    </div>
  </div>
</section>
</div>

<!-- ════════════════════════════════════════
     TAB 3: 기본 계산 3선 (단계별)
════════════════════════════════════════ -->
<div class="tab-panel" id="tab-t3">
<section class="sec">
  <div class="sec-title">📐 기본 계산 3선 – 단계별로 풀어 봅시다</div>
  <div class="sec-desc">각 단계의 선택지를 클릭해서 정답을 맞혀 가며 풀이 전략을 익혀 보세요.</div>

  <!-- 문제 1 -->
  <div class="problem-card">
    <div class="prob-num">1</div>
    <div class="prob-q">ω<sup>10</sup> + ω<sup>5</sup></div>

    <div class="step-block">
      <div class="step-hint"><strong>STEP 1.</strong> 10 = 3×3+1 이므로, ω<sup>10</sup> = ?</div>
      <div class="choices">
        <button class="schoice" data-grp="p1s1" data-val="one" onclick="chkStep('p1','s1',this,'w')">1</button>
        <button class="schoice" data-grp="p1s1" data-val="w"   onclick="chkStep('p1','s1',this,'w')">ω</button>
        <button class="schoice" data-grp="p1s1" data-val="w2"  onclick="chkStep('p1','s1',this,'w')">ω²</button>
      </div>
      <div class="step-fb" id="fb-p1-s1"></div>
    </div>

    <div class="step-block">
      <div class="step-hint"><strong>STEP 2.</strong> 5 = 3×1+2 이므로, ω<sup>5</sup> = ?</div>
      <div class="choices">
        <button class="schoice" data-grp="p1s2" data-val="one" onclick="chkStep('p1','s2',this,'w2')">1</button>
        <button class="schoice" data-grp="p1s2" data-val="w"   onclick="chkStep('p1','s2',this,'w2')">ω</button>
        <button class="schoice" data-grp="p1s2" data-val="w2"  onclick="chkStep('p1','s2',this,'w2')">ω²</button>
      </div>
      <div class="step-fb" id="fb-p1-s2"></div>
    </div>

    <div class="step-block">
      <div class="step-hint"><strong>STEP 3.</strong> ω²+ω+1=0 이므로, ω + ω² = ?</div>
      <div class="choices">
        <button class="schoice" data-grp="p1s3" data-val="0"  onclick="chkStep('p1','s3',this,'-1')">0</button>
        <button class="schoice" data-grp="p1s3" data-val="-1" onclick="chkStep('p1','s3',this,'-1')">−1</button>
        <button class="schoice" data-grp="p1s3" data-val="1"  onclick="chkStep('p1','s3',this,'-1')">1</button>
        <button class="schoice" data-grp="p1s3" data-val="2"  onclick="chkStep('p1','s3',this,'-1')">2</button>
      </div>
      <div class="step-fb" id="fb-p1-s3"></div>
    </div>
    <div class="final-ans" id="ans-p1">
      ω<sup>10</sup> + ω<sup>5</sup> = ω + ω² = <strong>−1</strong>
    </div>
  </div>

  <!-- 문제 2 -->
  <div class="problem-card">
    <div class="prob-num">2</div>
    <div class="prob-q">ω<sup>20</sup> + <sup>1</sup>⁄<sub>ω<sup>20</sup></sub></div>

    <div class="step-block">
      <div class="step-hint"><strong>STEP 1.</strong> 20 = 3×6+2 이므로, ω<sup>20</sup> = ?</div>
      <div class="choices">
        <button class="schoice" data-grp="p2s1" data-val="one" onclick="chkStep('p2','s1',this,'w2')">1</button>
        <button class="schoice" data-grp="p2s1" data-val="w"   onclick="chkStep('p2','s1',this,'w2')">ω</button>
        <button class="schoice" data-grp="p2s1" data-val="w2"  onclick="chkStep('p2','s1',this,'w2')">ω²</button>
      </div>
      <div class="step-fb" id="fb-p2-s1"></div>
    </div>

    <div class="step-block">
      <div class="step-hint"><strong>STEP 2.</strong> ω³=1 이므로 1/ω² = ω³/ω² = ω. 즉 <sup>1</sup>⁄<sub>ω<sup>20</sup></sub> = ?</div>
      <div class="choices">
        <button class="schoice" data-grp="p2s2" data-val="one" onclick="chkStep('p2','s2',this,'w')">1</button>
        <button class="schoice" data-grp="p2s2" data-val="w"   onclick="chkStep('p2','s2',this,'w')">ω</button>
        <button class="schoice" data-grp="p2s2" data-val="w2"  onclick="chkStep('p2','s2',this,'w')">ω²</button>
        <button class="schoice" data-grp="p2s2" data-val="-1"  onclick="chkStep('p2','s2',this,'w')">−1</button>
      </div>
      <div class="step-fb" id="fb-p2-s2"></div>
    </div>

    <div class="step-block">
      <div class="step-hint"><strong>STEP 3.</strong> ω² + ω = ?</div>
      <div class="choices">
        <button class="schoice" data-grp="p2s3" data-val="0"  onclick="chkStep('p2','s3',this,'-1')">0</button>
        <button class="schoice" data-grp="p2s3" data-val="-1" onclick="chkStep('p2','s3',this,'-1')">−1</button>
        <button class="schoice" data-grp="p2s3" data-val="1"  onclick="chkStep('p2','s3',this,'-1')">1</button>
        <button class="schoice" data-grp="p2s3" data-val="2"  onclick="chkStep('p2','s3',this,'-1')">2</button>
      </div>
      <div class="step-fb" id="fb-p2-s3"></div>
    </div>
    <div class="final-ans" id="ans-p2">
      ω<sup>20</sup> + <sup>1</sup>⁄<sub>ω<sup>20</sup></sub> = ω² + ω = <strong>−1</strong>
    </div>
  </div>

  <!-- 문제 3 -->
  <div class="problem-card">
    <div class="prob-num">3</div>
    <div class="prob-q">ω<sup>30</sup> + ω<sup>29</sup> + ω<sup>28</sup> + ··· + ω + 1</div>

    <div class="step-block">
      <div class="step-hint"><strong>STEP 1.</strong> 이 합의 항의 개수는? (ω⁰=1 포함)</div>
      <div class="choices">
        <button class="schoice" data-grp="p3s1" data-val="29" onclick="chkStep('p3','s1',this,'31')">29개</button>
        <button class="schoice" data-grp="p3s1" data-val="30" onclick="chkStep('p3','s1',this,'31')">30개</button>
        <button class="schoice" data-grp="p3s1" data-val="31" onclick="chkStep('p3','s1',this,'31')">31개</button>
      </div>
      <div class="step-fb" id="fb-p3-s1"></div>
    </div>

    <div class="step-block">
      <div class="step-hint"><strong>STEP 2.</strong> 31 = 3×□+1 에서 □ = ? (3개씩 몇 묶음?)</div>
      <div class="choices">
        <button class="schoice" data-grp="p3s2" data-val="9"  onclick="chkStep('p3','s2',this,'10')">9</button>
        <button class="schoice" data-grp="p3s2" data-val="10" onclick="chkStep('p3','s2',this,'10')">10</button>
        <button class="schoice" data-grp="p3s2" data-val="11" onclick="chkStep('p3','s2',this,'10')">11</button>
      </div>
      <div class="step-fb" id="fb-p3-s2"></div>
    </div>

    <div class="step-block">
      <div class="step-hint"><strong>STEP 3.</strong> 10묶음 × (1+ω+ω²) = 0 후, 남은 항 ω<sup>30</sup> = ?</div>
      <div class="choices">
        <button class="schoice" data-grp="p3s3" data-val="w"  onclick="chkStep('p3','s3',this,'one')">ω</button>
        <button class="schoice" data-grp="p3s3" data-val="w2" onclick="chkStep('p3','s3',this,'one')">ω²</button>
        <button class="schoice" data-grp="p3s3" data-val="one" onclick="chkStep('p3','s3',this,'one')">1</button>
        <button class="schoice" data-grp="p3s3" data-val="-1" onclick="chkStep('p3','s3',this,'one')">−1</button>
      </div>
      <div class="step-fb" id="fb-p3-s3"></div>
    </div>
    <div class="final-ans" id="ans-p3">
      = 10×(1+ω+ω²) + ω<sup>30</sup> = 10×0 + 1 = <strong>1</strong>
    </div>
  </div>
</section>
</div>

<!-- ════════════════════════════════════════
     TAB 4: 활용 문제 8선
════════════════════════════════════════ -->
<div class="tab-panel" id="tab-t4">
<section class="sec">
  <div class="sec-title">🎯 활용 문제 8선</div>
  <div class="score-bar">
    <div class="score-item"><div class="score-lbl">정답</div><div class="score-val" id="qOk">0</div></div>
    <div class="score-item"><div class="score-lbl">오답</div><div class="score-val" id="qNg">0</div></div>
    <div class="score-item"><div class="score-lbl">남은 문제</div><div class="score-val" id="qLeft">8</div></div>
  </div>

  <!-- Q1 -->
  <div class="quiz-card">
    <div class="qnum-badge">1</div><span class="diff diff-e">쉬움</span>
    <div class="q-text">다음 식의 값을 구하시오.<br><span class="q-math">ω<sup>7</sup></span></div>
    <div class="qchoices">
      <button class="qchoice" data-qn="1" data-val="one" onclick="chkQ(1,this,'w')">1</button>
      <button class="qchoice" data-qn="1" data-val="w"   onclick="chkQ(1,this,'w')">ω</button>
      <button class="qchoice" data-qn="1" data-val="w2"  onclick="chkQ(1,this,'w')">ω²</button>
      <button class="qchoice" data-qn="1" data-val="-1"  onclick="chkQ(1,this,'w')">−1</button>
    </div>
    <div class="qexp" id="qexp-1">7 = 3×2+1 → 나머지 <strong>1</strong> → ω<sup>7</sup> = ω<sup>1</sup> = <strong>ω</strong></div>
  </div>

  <!-- Q2 -->
  <div class="quiz-card">
    <div class="qnum-badge">2</div><span class="diff diff-e">쉬움</span>
    <div class="q-text">다음 식의 값을 구하시오.<br><span class="q-math">ω<sup>100</sup></span></div>
    <div class="qchoices">
      <button class="qchoice" data-qn="2" data-val="one" onclick="chkQ(2,this,'w')">1</button>
      <button class="qchoice" data-qn="2" data-val="w"   onclick="chkQ(2,this,'w')">ω</button>
      <button class="qchoice" data-qn="2" data-val="w2"  onclick="chkQ(2,this,'w')">ω²</button>
      <button class="qchoice" data-qn="2" data-val="-1"  onclick="chkQ(2,this,'w')">−1</button>
    </div>
    <div class="qexp" id="qexp-2">100 = 3×33+1 → 나머지 <strong>1</strong> → ω<sup>100</sup> = <strong>ω</strong></div>
  </div>

  <!-- Q3 -->
  <div class="quiz-card">
    <div class="qnum-badge">3</div><span class="diff diff-e">쉬움</span>
    <div class="q-text">다음 식의 값을 구하시오.<br><span class="q-math">ω<sup>−1</sup></span>
    <span style="font-size:.8rem;color:#5eead4">&nbsp;(힌트: ω · ? = 1)</span></div>
    <div class="qchoices">
      <button class="qchoice" data-qn="3" data-val="one" onclick="chkQ(3,this,'w2')">1</button>
      <button class="qchoice" data-qn="3" data-val="w"   onclick="chkQ(3,this,'w2')">ω</button>
      <button class="qchoice" data-qn="3" data-val="w2"  onclick="chkQ(3,this,'w2')">ω²</button>
      <button class="qchoice" data-qn="3" data-val="-w"  onclick="chkQ(3,this,'w2')">−ω</button>
    </div>
    <div class="qexp" id="qexp-3">ω·ω² = ω³ = 1 → 1/ω = ω² → ω<sup>−1</sup> = <strong>ω²</strong></div>
  </div>

  <!-- Q4 -->
  <div class="quiz-card">
    <div class="qnum-badge">4</div><span class="diff diff-m">보통</span>
    <div class="q-text">다음 식의 값을 구하시오.<br><span class="q-math">(1+ω)(1+ω²)</span></div>
    <div class="qchoices">
      <button class="qchoice" data-qn="4" data-val="0"  onclick="chkQ(4,this,'1')">0</button>
      <button class="qchoice" data-qn="4" data-val="1"  onclick="chkQ(4,this,'1')">1</button>
      <button class="qchoice" data-qn="4" data-val="-1" onclick="chkQ(4,this,'1')">−1</button>
      <button class="qchoice" data-qn="4" data-val="2"  onclick="chkQ(4,this,'1')">2</button>
    </div>
    <div class="qexp" id="qexp-4">
      전개하면: 1+ω²+ω+ω³<br>
      = (1+ω+ω²) + ω³ = <strong>0</strong> + <strong>1</strong> = <strong>1</strong>
    </div>
  </div>

  <!-- Q5 -->
  <div class="quiz-card">
    <div class="qnum-badge">5</div><span class="diff diff-m">보통</span>
    <div class="q-text">다음 식의 값을 구하시오.<br>
      <span class="q-math"><sup>1</sup>⁄<sub>1+ω</sub> + <sup>1</sup>⁄<sub>1+ω²</sub></span>
      <span style="font-size:.8rem;color:#5eead4">&nbsp;(힌트: ω²+ω+1=0 → 1+ω = ?)</span>
    </div>
    <div class="qchoices">
      <button class="qchoice" data-qn="5" data-val="0"  onclick="chkQ(5,this,'1')">0</button>
      <button class="qchoice" data-qn="5" data-val="1"  onclick="chkQ(5,this,'1')">1</button>
      <button class="qchoice" data-qn="5" data-val="-1" onclick="chkQ(5,this,'1')">−1</button>
      <button class="qchoice" data-qn="5" data-val="2"  onclick="chkQ(5,this,'1')">2</button>
    </div>
    <div class="qexp" id="qexp-5">
      ω²+ω+1=0 → 1+ω = −ω², 1+ω² = −ω<br>
      = 1/(−ω²) + 1/(−ω) = −ω − ω² (∵ 1/ω²=ω, 1/ω=ω²)<br>
      = −(ω+ω²) = −(−1) = <strong>1</strong>
    </div>
  </div>

  <!-- Q6 -->
  <div class="quiz-card">
    <div class="qnum-badge">6</div><span class="diff diff-m">보통</span>
    <div class="q-text">다음 식의 값을 구하시오.<br><span class="q-math">ω<sup>100</sup> + ω<sup>50</sup> + 1</span></div>
    <div class="qchoices">
      <button class="qchoice" data-qn="6" data-val="0"  onclick="chkQ(6,this,'0')">0</button>
      <button class="qchoice" data-qn="6" data-val="1"  onclick="chkQ(6,this,'0')">1</button>
      <button class="qchoice" data-qn="6" data-val="-1" onclick="chkQ(6,this,'0')">−1</button>
      <button class="qchoice" data-qn="6" data-val="3"  onclick="chkQ(6,this,'0')">3</button>
    </div>
    <div class="qexp" id="qexp-6">
      100=3×33+1 → ω<sup>100</sup>=ω<br>
      50=3×16+2 → ω<sup>50</sup>=ω²<br>
      → ω + ω² + 1 = <strong>0</strong>
    </div>
  </div>

  <!-- Q7 -->
  <div class="quiz-card">
    <div class="qnum-badge">7</div><span class="diff diff-h">어려움</span>
    <div class="q-text">다음 식의 값을 구하시오. (항이 51개)<br>
      <span class="q-math">ω<sup>50</sup> + ω<sup>49</sup> + ··· + ω + 1</span>
    </div>
    <div class="qchoices">
      <button class="qchoice" data-qn="7" data-val="0"  onclick="chkQ(7,this,'0')">0</button>
      <button class="qchoice" data-qn="7" data-val="1"  onclick="chkQ(7,this,'0')">1</button>
      <button class="qchoice" data-qn="7" data-val="-1" onclick="chkQ(7,this,'0')">−1</button>
      <button class="qchoice" data-qn="7" data-val="51" onclick="chkQ(7,this,'0')">51</button>
    </div>
    <div class="qexp" id="qexp-7">
      51개 = 3×17묶음 → 17×(1+ω+ω²) = 17×0 = <strong>0</strong>
    </div>
  </div>

  <!-- Q8 -->
  <div class="quiz-card">
    <div class="qnum-badge">8</div><span class="diff diff-h">어려움</span>
    <div class="q-text">다음 식의 값을 구하시오.<br>
      <span class="q-math">ω<sup>2024</sup> + ω<sup>2023</sup> + ω<sup>2022</sup></span>
    </div>
    <div class="qchoices">
      <button class="qchoice" data-qn="8" data-val="0"  onclick="chkQ(8,this,'0')">0</button>
      <button class="qchoice" data-qn="8" data-val="1"  onclick="chkQ(8,this,'0')">1</button>
      <button class="qchoice" data-qn="8" data-val="-1" onclick="chkQ(8,this,'0')">−1</button>
      <button class="qchoice" data-qn="8" data-val="3"  onclick="chkQ(8,this,'0')">3</button>
    </div>
    <div class="qexp" id="qexp-8">
      2024=3×674+2 → ω<sup>2024</sup>=ω²<br>
      2023=3×674+1 → ω<sup>2023</sup>=ω<br>
      2022=3×674+0 → ω<sup>2022</sup>=1<br>
      → ω²+ω+1 = <strong>0</strong>
    </div>
  </div>

</section>
</div>

</div><!-- shell -->
<script>
/* ── iframe 높이 자동 조절 ── */
function notifyH(){
  var h=Math.max(document.body.scrollHeight,document.documentElement.scrollHeight)+40;
  window.parent.postMessage({isStreamlitMessage:true,type:'streamlit:setFrameHeight',args:{height:h}},'*');
  window.parent.postMessage({type:'streamlit:setFrameHeight',height:h},'*');
}
new ResizeObserver(function(){notifyH();}).observe(document.body);
window.addEventListener('load',function(){setTimeout(notifyH,120);});

/* ── 탭 전환 ── */
function showTab(name){
  document.querySelectorAll('.tab-btn').forEach(function(b){b.classList.remove('active');});
  document.querySelectorAll('.tab-panel').forEach(function(p){p.classList.remove('active');});
  document.querySelector('[data-tab="'+name+'"]').classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
  if(name==='t2'){drawCycle();calcOmega();}
  setTimeout(notifyH,60);
}

/* ── Tab1: 증명 토글 ── */
function toggleProof(id){
  var el=document.getElementById(id);
  el.classList.toggle('open');
  var btn=document.getElementById(id+'-btn');
  btn.textContent=el.classList.contains('open')?'▲ 닫기':'▼ 증명 보기';
  setTimeout(notifyH,60);
}

/* ── Tab2: 순환표 채우기 ── */
var fillSel=null, fillCount=0;
var DISP={one:'1',w:'ω',w2:'ω²'};

function selFill(btn,v){
  document.querySelectorAll('.fchoice').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  fillSel=v;
}

function fillCell(td,correct){
  if(!fillSel){
    td.style.outline='2px solid #f59e0b';
    setTimeout(function(){td.style.outline='';},900);
    return;
  }
  if(td.classList.contains('correct')) return;
  if(fillSel===correct){
    td.innerHTML=DISP[correct];
    td.classList.remove('empty','wrong');
    td.classList.add('correct');
    td.onclick=null;
    fillCount++;
    var left=7-fillCount;
    document.getElementById('tblProg').textContent=
      left>0?('빈 칸 '+left+'개 남았습니다.'):'✅ 모든 칸 완성! 패턴을 확인해 보세요.';
    if(fillCount===7) document.getElementById('tblReveal').classList.add('show');
    setTimeout(notifyH,60);
  } else {
    td.classList.add('wrong');
    setTimeout(function(){td.classList.remove('wrong');},480);
  }
}

/* ── Tab2: ω 계산기 ── */
var WMAP={0:'1',1:'ω',2:'ω²'};
function calcOmega(){
  var n=parseInt(document.getElementById('omegaInp').value,10);
  if(isNaN(n)){return;}
  var r=((n%3)+3)%3;
  document.getElementById('calcStep').innerHTML=
    'n = '+n+'<br>'+
    Math.abs(n)+' ÷ 3 = '+Math.floor(Math.abs(n)/3)+' ··· 나머지 <strong>'+r+'</strong><br>'+
    '→ ω<sup>'+n+'</sup> = (ω³)<sup>□</sup> × ω<sup>'+r+'</sup> = 1 × ω<sup>'+r+'</sup>';
  document.getElementById('calcFinal').innerHTML=
    'ω<sup>'+n+'</sup> = <strong>'+WMAP[r]+'</strong>';
}

/* ── Tab2: 순환 캔버스 ── */
function drawCycle(){
  var cv=document.getElementById('cycleCanvas');
  if(!cv) return;
  var ctx=cv.getContext('2d');
  var W=cv.width,H=cv.height;
  var cx=W/2,cy=H/2,r=88;
  var sq3=Math.sqrt(3);

  ctx.clearRect(0,0,W,H);

  /* background */
  var bg=ctx.createLinearGradient(0,0,W,H);
  bg.addColorStop(0,'#060d18'); bg.addColorStop(1,'#0c1f34');
  ctx.fillStyle=bg; ctx.fillRect(0,0,W,H);

  /* circle */
  ctx.strokeStyle='rgba(20,184,166,.2)'; ctx.lineWidth=1.5;
  ctx.beginPath(); ctx.arc(cx,cy,r,0,Math.PI*2); ctx.stroke();

  /* nodes */
  var nodes=[
    {x:cx+r,        y:cy,            lbl:'1',  col:'#60a5fa'},
    {x:cx-r/2,      y:cy-r*sq3/2,   lbl:'ω',  col:'#14b8a6'},
    {x:cx-r/2,      y:cy+r*sq3/2,   lbl:'ω²', col:'#f59e0b'}
  ];

  /* curved arrows: 0→1, 1→2, 2→0 */
  var nodeR=20;
  for(var i=0;i<3;i++){
    var from=nodes[i], to=nodes[(i+1)%3];
    var mx=(from.x+to.x)/2, my=(from.y+to.y)/2;
    var dx=mx-cx, dy=my-cy;
    var len=Math.sqrt(dx*dx+dy*dy)||1;
    var cpx=mx+dx/len*r*0.6, cpy=my+dy/len*r*0.6;

    /* direction from cp to endpoint */
    var ex=to.x, ey=to.y;
    var tx=ex-cpx, ty=ey-cpy;
    var tl=Math.sqrt(tx*tx+ty*ty)||1;
    tx/=tl; ty/=tl;
    var sx2=from.x+(cpx-from.x)/Math.sqrt((cpx-from.x)*(cpx-from.x)+(cpy-from.y)*(cpy-from.y))*nodeR;
    var sy2=from.y+(cpy-from.y)/Math.sqrt((cpx-from.x)*(cpx-from.x)+(cpy-from.y)*(cpy-from.y))*nodeR;
    var ex2=to.x-tx*nodeR, ey2=to.y-ty*nodeR;

    ctx.strokeStyle='rgba(20,184,166,.65)'; ctx.lineWidth=2;
    ctx.beginPath();
    ctx.moveTo(sx2,sy2);
    ctx.quadraticCurveTo(cpx,cpy,ex2,ey2);
    ctx.stroke();

    /* arrowhead */
    var aS=8;
    ctx.fillStyle='rgba(20,184,166,.8)';
    ctx.beginPath();
    ctx.moveTo(ex2,ey2);
    ctx.lineTo(ex2-tx*aS+ty*aS*0.4, ey2-ty*aS-tx*aS*0.4);
    ctx.lineTo(ex2-tx*aS-ty*aS*0.4, ey2-ty*aS+tx*aS*0.4);
    ctx.closePath(); ctx.fill();

    /* ×ω label */
    var lx=(sx2+2*cpx+ex2)/4;
    var ly=(sy2+2*cpy+ey2)/4;
    var ldx=lx-cx, ldy=ly-cy;
    var ll=Math.sqrt(ldx*ldx+ldy*ldy)||1;
    lx+=ldx/ll*10; ly+=ldy/ll*10;
    ctx.fillStyle='#5eead4';
    ctx.font='bold 11px Malgun Gothic';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('×ω',lx,ly);
  }

  /* draw nodes */
  nodes.forEach(function(n){
    ctx.shadowColor=n.col; ctx.shadowBlur=14;
    ctx.fillStyle=n.col;
    ctx.beginPath(); ctx.arc(n.x,n.y,nodeR,0,Math.PI*2); ctx.fill();
    ctx.shadowBlur=0;

    /* ring */
    ctx.strokeStyle=n.col; ctx.lineWidth=1.5; ctx.globalAlpha=0.3;
    ctx.beginPath(); ctx.arc(n.x,n.y,nodeR+6,0,Math.PI*2); ctx.stroke();
    ctx.globalAlpha=1;

    /* label */
    ctx.fillStyle='#0c1f34';
    ctx.font='bold 13px Times New Roman';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    if(n.lbl==='ω²'){
      ctx.font='bold 12px Times New Roman';
      ctx.fillText('ω',n.x-4,n.y);
      ctx.font='bold 9px Times New Roman';
      ctx.fillText('2',n.x+6,n.y-5);
    } else {
      ctx.fillText(n.lbl,n.x,n.y);
    }
  });

  /* center label */
  ctx.fillStyle='rgba(20,184,166,.5)';
  ctx.font='11px Malgun Gothic';
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText('주기 3',cx,cy);
}

/* ── Tab3: 단계별 문제 ── */
var stepDone={};
var stepCounts={p1:3,p2:3,p3:3};

var stepMessages={
  'p1-s1':{ok:'맞아요! 10÷3=3···1 → ω¹⁰=ω',ng:'10을 3으로 나눈 나머지를 확인하세요. 10=3×3+1 → 나머지 1'},
  'p1-s2':{ok:'맞아요! 5÷3=1···2 → ω⁵=ω²',ng:'5를 3으로 나눈 나머지를 확인하세요. 5=3×1+2 → 나머지 2'},
  'p1-s3':{ok:'정답! ω²+ω+1=0에서 ω+ω²=−1',ng:'ω²+ω+1=0을 변형하세요. ω+ω²= ?'},
  'p2-s1':{ok:'맞아요! 20÷3=6···2 → ω²⁰=ω²',ng:'20을 3으로 나눈 나머지를 확인하세요. 20=3×6+2'},
  'p2-s2':{ok:'맞아요! 1/ω²=ω³/ω²=ω',ng:'ω³=1이므로 1/ω²=ω³÷ω²=ω'},
  'p2-s3':{ok:'정답! ω²+ω=−1',ng:'ω²+ω+1=0을 이용하세요'},
  'p3-s1':{ok:'맞아요! ω³⁰부터 ω⁰(=1)까지 31개',ng:'ω⁰=1도 포함해서 세어 보세요 (30−0+1=31)'},
  'p3-s2':{ok:'맞아요! 31=3×10+1이므로 10묶음',ng:'31을 3으로 나눠 보세요. 31=3×?+1'},
  'p3-s3':{ok:'맞아요! ω³⁰=(ω³)¹⁰=1¹⁰=1',ng:'30÷3=10 → 나머지 0 → ω³⁰=1'}
};

function chkStep(pid,sid,btn,correct){
  var key=pid+'-'+sid;
  if(stepDone[key]) return;
  var grp=btn.dataset.grp;
  var sel=btn.dataset.val;
  var ok=sel===correct;
  document.querySelectorAll('[data-grp="'+grp+'"]').forEach(function(b){
    b.onclick=null;
    if(b.dataset.val===correct) b.classList.add('ok');
    else if(b===btn&&!ok) b.classList.add('ng');
  });
  stepDone[key]=true;
  var fb=document.getElementById('fb-'+pid+'-'+sid);
  var msg=stepMessages[key];
  if(fb&&msg){
    fb.textContent=(ok?'✅ ':'❌ ')+(ok?msg.ok:msg.ng);
    fb.classList.add('show',ok?'ok':'ng');
  }
  checkProbDone(pid);
  setTimeout(notifyH,60);
}

function checkProbDone(pid){
  var total=stepCounts[pid];
  var done=0;
  for(var s=1;s<=total;s++){
    if(stepDone[pid+'-s'+s]) done++;
  }
  if(done===total){
    var ans=document.getElementById('ans-'+pid);
    if(ans) ans.classList.add('show');
    setTimeout(notifyH,80);
  }
}

/* ── Tab4: 퀴즈 ── */
var qDone={}, qOk=0, qNg=0;

function chkQ(n,btn,correct){
  if(qDone[n]) return;
  qDone[n]=true;
  var sel=btn.dataset.val;
  var ok=sel===correct;
  document.querySelectorAll('[data-qn="'+n+'"]').forEach(function(b){
    b.onclick=null;
    if(b.dataset.val===correct) b.classList.add('ok');
    else if(b===btn&&!ok) b.classList.add('ng');
  });
  if(ok) qOk++; else qNg++;
  document.getElementById('qOk').textContent=qOk;
  document.getElementById('qNg').textContent=qNg;
  document.getElementById('qLeft').textContent=8-Object.keys(qDone).length;
  var exp=document.getElementById('qexp-'+n);
  if(exp) exp.classList.add('show');
  setTimeout(notifyH,60);
}

/* ── 초기화 ── */
drawCycle();
calcOmega();
</script>
</body>
</html>"""


def render():
    components.html(_HTML, height=2500, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
