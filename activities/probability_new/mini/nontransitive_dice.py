# activities/probability_new/mini/nontransitive_dice.py
"""
신기한(비추이적) 주사위 — 확률의 곱셈정리 연결 미니활동

탭1: 🎲 주사위 소개     — 세 주사위 A/B/C를 살펴보고 "누가 이길까?" 직관 퀴즈
탭2: 📐 이론 계산       — 확률의 곱셈정리로 P(A>B), P(B>C), P(C>A) 계산
탭3: 🏆 대결 시뮬레이션 — 애니메이션 주사위 굴리기와 토너먼트 결과 확인
"""
import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🎲 신기한(비추이적) 주사위",
    "description": "A가 B를 이기고 B가 C를 이기면 A가 C를 이긴다? 확률의 곱셈정리로 놀라운 역설을 분석합니다.",
    "order": 60,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "비추이적주사위"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 신기한(비추이적) 주사위**"},
    {
        "key": "비추이성설명",
        "label": "A가 B를 이기고 B가 C를 이기지만 C가 A를 이기는 '비추이성'이 왜 가위-바위-보와 비슷한지 설명해보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "가위-바위-보도 가위→보→바위→가위 처럼 순환하는 구조인데...",
    },
    {
        "key": "곱셈정리연결",
        "label": "P(A>B) 계산에서 확률의 곱셈정리(전체확률의 법칙)를 어떻게 사용했는지 설명해보세요. P(A=3)×P(B<3) + P(A=6)×P(B<6) 형태가 왜 성립하는지 적어보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "A가 3이 나왔을 때와 6이 나왔을 때를 경우로 나누어...",
    },
    {
        "key": "직관과차이",
        "label": "활동 전에 어떤 주사위가 가장 강하다고 생각했나요? 실제 분석 결과와 어떻게 달랐나요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "처음에는 B주사위가 가장 강할 것 같았는데...",
    },
    {
        "key": "실생활연결",
        "label": "비추이적 관계(순환적 우열)가 나타나는 실생활 사례를 하나 더 찾아보고, 이것이 '최강자'를 정하기 어렵게 만드는 이유를 설명해보세요.",
        "type": "text_area",
        "height": 90,
        "placeholder": "예) 운동 경기의 상성 관계, 음식 선호도, 선거 결과에서...",
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 이 활동으로 새롭게 알게 된 점",
        "type": "text_area",
        "height": 80,
    },
    {
        "key": "느낀점",
        "label": "💬 활동을 마친 후 느낀 점",
        "type": "text_area",
        "height": 80,
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 탭 1: 주사위 소개 + 직관 퀴즈
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB1 = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);color:#e2e8f0;padding:16px 14px 32px}
.hdr{text-align:center;padding:18px 20px 14px;background:linear-gradient(135deg,rgba(168,85,247,.15),rgba(99,102,241,.12));border:1px solid rgba(168,85,247,.35);border-radius:16px;margin-bottom:14px}
.hdr h1{font-size:1.4rem;font-weight:800;color:#c084fc;margin-bottom:6px}
.hdr p{font-size:.82rem;color:#94a3b8;line-height:1.7}
.section{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:14px;padding:15px 14px;margin-bottom:12px}
.sec-title{font-size:.97rem;font-weight:700;margin-bottom:12px;color:#c084fc;display:flex;align-items:center;gap:7px}
.dice-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}
.dice-card{border-radius:14px;padding:14px 10px;text-align:center;cursor:default;transition:transform .2s}
.dice-card:hover{transform:translateY(-3px)}
.dc-a{background:rgba(59,130,246,.12);border:2px solid rgba(59,130,246,.45)}
.dc-b{background:rgba(34,197,94,.12);border:2px solid rgba(34,197,94,.45)}
.dc-c{background:rgba(249,115,22,.12);border:2px solid rgba(249,115,22,.45)}
.dice-label{font-size:1.5rem;font-weight:800;margin-bottom:6px}
.dc-a .dice-label{color:#60a5fa}
.dc-b .dice-label{color:#4ade80}
.dc-c .dice-label{color:#fb923c}
.face-row{display:flex;flex-wrap:wrap;gap:4px;justify-content:center;margin:8px 0}
.face{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.05rem;font-weight:700}
.fa-a{background:rgba(59,130,246,.25);color:#bfdbfe;border:1px solid rgba(59,130,246,.4)}
.fa-b{background:rgba(34,197,94,.25);color:#bbf7d0;border:1px solid rgba(34,197,94,.4)}
.fa-c{background:rgba(249,115,22,.25);color:#fed7aa;border:1px solid rgba(249,115,22,.4)}
.dice-stat{font-size:.73rem;color:#94a3b8;margin-top:6px;line-height:1.8}
.dice-stat strong{color:#e2e8f0}
.rps-diagram{display:flex;align-items:center;justify-content:center;gap:0;margin:10px 0 4px}
.rps-node{width:52px;height:52px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.3rem;font-weight:800;border:2px solid}
.rps-a{background:rgba(59,130,246,.2);border-color:#60a5fa;color:#60a5fa}
.rps-b{background:rgba(34,197,94,.2);border-color:#4ade80;color:#4ade80}
.rps-c{background:rgba(249,115,22,.2);border-color:#fb923c;color:#fb923c}
.rps-arrow{font-size:1.2rem;color:#7c3aed;margin:0 4px;font-weight:700}
.rps-back{font-size:.8rem;color:#a78bfa;margin:0 4px;display:flex;align-items:center}
.quiz-section{background:rgba(139,92,246,.07);border:1px solid rgba(139,92,246,.25);border-radius:14px;padding:14px}
.quiz-title{font-size:.95rem;font-weight:700;color:#a78bfa;margin-bottom:12px}
.quiz-match{margin-bottom:14px}
.qm-label{font-size:.85rem;color:#cbd5e1;margin-bottom:7px;font-weight:600}
.btn-row{display:flex;gap:8px;flex-wrap:wrap}
.q-btn{padding:8px 14px;border-radius:10px;border:1.5px solid;font-size:.82rem;font-weight:700;cursor:pointer;transition:all .2s;background:transparent}
.q-btn:hover{transform:scale(1.04)}
.btn-a{border-color:#60a5fa;color:#60a5fa}.btn-a:hover{background:rgba(59,130,246,.15)}
.btn-b{border-color:#4ade80;color:#4ade80}.btn-b:hover{background:rgba(34,197,94,.15)}
.btn-c{border-color:#fb923c;color:#fb923c}.btn-c:hover{background:rgba(249,115,22,.15)}
.btn-tie{border-color:#94a3b8;color:#94a3b8}.btn-tie:hover{background:rgba(148,163,184,.12)}
.result-box{margin-top:8px;padding:9px 12px;border-radius:9px;font-size:.82rem;line-height:1.7;display:none}
.res-correct{background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.35);color:#86efac}
.res-wrong{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.35);color:#fca5a5}
.reveal-btn{margin-top:12px;width:100%;padding:11px;border-radius:12px;border:2px solid rgba(168,85,247,.5);background:rgba(168,85,247,.1);color:#c084fc;font-size:.9rem;font-weight:700;cursor:pointer;transition:all .25s}
.reveal-btn:hover{background:rgba(168,85,247,.2);border-color:#a855f7}
.reveal-box{margin-top:12px;padding:13px;border-radius:12px;background:rgba(168,85,247,.08);border:1px solid rgba(168,85,247,.3);display:none}
.reveal-box h3{color:#c084fc;font-size:.95rem;margin-bottom:8px}
.reveal-box p{font-size:.8rem;color:#cbd5e1;line-height:1.8}
.cycle-big{text-align:center;font-size:1.3rem;font-weight:800;color:#fbbf24;margin:10px 0;letter-spacing:2px}
.prob-badges{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:10px}
.pbadge{padding:5px 12px;border-radius:20px;font-size:.78rem;font-weight:700;border:1px solid}
.pb-ab{background:rgba(59,130,246,.12);border-color:rgba(59,130,246,.4);color:#93c5fd}
.pb-bc{background:rgba(34,197,94,.12);border-color:rgba(34,197,94,.4);color:#86efac}
.pb-ca{background:rgba(249,115,22,.12);border-color:rgba(249,115,22,.4);color:#fdba74}
</style>
</head>
<body>
<div class="hdr">
  <h1>🎲 신기한(비추이적) 주사위</h1>
  <p>A, B, C 세 주사위가 있습니다. A는 B를 자주 이기고, B는 C를 자주 이기는데...<br>
  그렇다면 A가 C를 이길까요? 🤔 직관을 먼저 테스트해보세요!</p>
</div>

<!-- 주사위 소개 -->
<div class="section">
  <div class="sec-title">🎲 세 주사위 살펴보기</div>
  <div class="dice-grid">
    <div class="dice-card dc-a">
      <div class="dice-label">A</div>
      <div class="face-row">
        <span class="face fa-a">3</span><span class="face fa-a">3</span><span class="face fa-a">3</span>
        <span class="face fa-a">3</span><span class="face fa-a">3</span><span class="face fa-a">6</span>
      </div>
      <div class="dice-stat">눈: <strong>3×5, 6×1</strong><br>평균: <strong>3.5</strong></div>
    </div>
    <div class="dice-card dc-b">
      <div class="dice-label">B</div>
      <div class="face-row">
        <span class="face fa-b">2</span><span class="face fa-b">2</span><span class="face fa-b">2</span>
        <span class="face fa-b">5</span><span class="face fa-b">5</span><span class="face fa-b">5</span>
      </div>
      <div class="dice-stat">눈: <strong>2×3, 5×3</strong><br>평균: <strong>3.5</strong></div>
    </div>
    <div class="dice-card dc-c">
      <div class="dice-label">C</div>
      <div class="face-row">
        <span class="face fa-c">1</span><span class="face fa-c">4</span><span class="face fa-c">4</span>
        <span class="face fa-c">4</span><span class="face fa-c">4</span><span class="face fa-c">4</span>
      </div>
      <div class="dice-stat">눈: <strong>1×1, 4×5</strong><br>평균: <strong>3.5</strong></div>
    </div>
  </div>
  <div style="margin-top:10px;padding:9px 12px;border-radius:10px;background:rgba(251,191,36,.07);border:1px solid rgba(251,191,36,.25);font-size:.8rem;color:#fcd34d;line-height:1.8;text-align:center">
    ⭐ 세 주사위 모두 평균이 3.5로 동일합니다. 그런데 승부 결과는 완전히 다릅니다!
  </div>
</div>

<!-- 직관 퀴즈 -->
<div class="quiz-section">
  <div class="quiz-title">🤔 직관 퀴즈 — 어느 주사위가 이길까요?</div>
  
  <div class="quiz-match">
    <div class="qm-label">① A와 B가 대결하면?</div>
    <div class="btn-row">
      <button class="q-btn btn-a" onclick="answer('ab','A')">A 승</button>
      <button class="q-btn btn-b" onclick="answer('ab','B')">B 승</button>
      <button class="q-btn btn-tie" onclick="answer('ab','T')">비슷함</button>
    </div>
    <div id="res-ab" class="result-box"></div>
  </div>
  
  <div class="quiz-match">
    <div class="qm-label">② B와 C가 대결하면?</div>
    <div class="btn-row">
      <button class="q-btn btn-b" onclick="answer('bc','B')">B 승</button>
      <button class="q-btn btn-c" onclick="answer('bc','C')">C 승</button>
      <button class="q-btn btn-tie" onclick="answer('bc','T')">비슷함</button>
    </div>
    <div id="res-bc" class="result-box"></div>
  </div>
  
  <div class="quiz-match">
    <div class="qm-label">③ C와 A가 대결하면? (위 결과를 바탕으로 예상해보세요)</div>
    <div class="btn-row">
      <button class="q-btn btn-c" onclick="answer('ca','C')">C 승</button>
      <button class="q-btn btn-a" onclick="answer('ca','A')">A 승</button>
      <button class="q-btn btn-tie" onclick="answer('ca','T')">비슷함</button>
    </div>
    <div id="res-ca" class="result-box"></div>
  </div>
  
  <button class="reveal-btn" onclick="revealAll()">🔍 전체 결과 공개하기</button>
  <div id="reveal-all" class="reveal-box">
    <h3>🎯 놀라운 결과!</h3>
    <div class="cycle-big">A → B → C → A</div>
    <p>A가 B를 이기고(약 58.3%), B가 C를 이기고(약 58.3%), 그런데 <strong>C가 A를 이깁니다</strong>(약 69.4%)!<br>
    가위-바위-보처럼 순환하는 구조를 <strong>비추이성(Non-transitivity)</strong>이라고 합니다.<br><br>
    평균이 똑같은 주사위인데도 이런 일이 생기는 이유는 무엇일까요? 탭 2에서 확률의 곱셈정리로 분석해봅시다!</p>
    <div class="prob-badges">
      <span class="pbadge pb-ab">P(A>B) = 7/12 ≈ 58.3%</span>
      <span class="pbadge pb-bc">P(B>C) = 7/12 ≈ 58.3%</span>
      <span class="pbadge pb-ca">P(C>A) = 25/36 ≈ 69.4%</span>
    </div>
  </div>
</div>

<script>
const answers = {ab:'A', bc:'B', ca:'C'};
const msgs = {
  ab: {
    A:'✅ 정답! A가 B를 약 58.3% 확률로 이깁니다. A의 3이 B의 2를 이기는 경우가 많기 때문입니다.',
    B:'❌ 아닙니다! 실제로는 A가 B를 약 58.3% 확률로 이깁니다.',
    T:'❌ 비슷하지 않습니다. A가 B를 약 58.3%로 꽤 자주 이깁니다.',
  },
  bc: {
    B:'✅ 정답! B가 C를 약 58.3% 확률로 이깁니다. B의 5가 C의 4를 이기는 경우가 결정적입니다.',
    C:'❌ 아닙니다! 실제로는 B가 C를 약 58.3% 확률로 이깁니다.',
    T:'❌ 비슷하지 않습니다. B가 C를 약 58.3%로 자주 이깁니다.',
  },
  ca: {
    C:'✅ 정답! 놀랍게도 C가 A를 약 69.4%로 이깁니다! A≻B, B≻C 이지만 C≻A 입니다.',
    A:'❌ 직관적으로는 맞을 것 같지만, 실제로는 C가 A를 약 69.4%로 이깁니다!',
    T:'❌ 전혀 비슷하지 않습니다. C가 A를 약 69.4%로 압도합니다!',
  }
};
function answer(match, choice) {
  const correct = answers[match] === choice;
  const box = document.getElementById('res-' + match);
  box.textContent = msgs[match][choice];
  box.className = 'result-box ' + (correct ? 'res-correct' : 'res-wrong');
  box.style.display = 'block';
}
function revealAll() {
  document.getElementById('reveal-all').style.display = 'block';
}
</script>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# 탭 2: 확률의 곱셈정리로 계산
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB2 = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);color:#e2e8f0;padding:16px 14px 32px}
.hdr{text-align:center;padding:16px 20px 12px;background:linear-gradient(135deg,rgba(251,191,36,.14),rgba(249,115,22,.1));border:1px solid rgba(251,191,36,.32);border-radius:14px;margin-bottom:12px}
.hdr h1{font-size:1.25rem;font-weight:800;color:#fbbf24;margin-bottom:5px}
.hdr p{font-size:.8rem;color:#94a3b8;line-height:1.7}
.section{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:14px;padding:15px 14px;margin-bottom:12px}
.sec-title{font-size:.97rem;font-weight:700;margin-bottom:10px;color:#fbbf24;display:flex;align-items:center;gap:7px}
.formula-box{background:rgba(251,191,36,.06);border:1px solid rgba(251,191,36,.28);border-radius:11px;padding:13px 14px;margin-bottom:12px;text-align:center}
.formula{font-size:1rem;color:#fcd34d;font-weight:700;letter-spacing:.5px;line-height:1.9}
.formula .sub{font-size:.78rem;color:#94a3b8;font-weight:400}
.step-list{display:flex;flex-direction:column;gap:10px}
.step{background:rgba(255,255,255,.03);border-left:3px solid;border-radius:0 11px 11px 0;padding:11px 13px;transition:all .25s}
.step-1{border-color:#60a5fa}
.step-2{border-color:#4ade80}
.step-3{border-color:#fb923c}
.step-4{border-color:#a78bfa}
.step-title{font-size:.88rem;font-weight:700;margin-bottom:6px}
.s1 .step-title{color:#60a5fa}
.s2 .step-title{color:#4ade80}
.s3 .step-title{color:#fb923c}
.s4 .step-title{color:#a78bfa}
.step-body{font-size:.79rem;color:#cbd5e1;line-height:1.9}
.step-body .hl{color:#fbbf24;font-weight:700}
.step-body .eq{color:#7dd3fc;font-weight:600}
.calc-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:8px}
.calc-row{background:rgba(255,255,255,.04);border-radius:10px;padding:9px 11px}
.calc-label{font-size:.73rem;color:#94a3b8;margin-bottom:4px}
.calc-val{font-size:.88rem;font-weight:700;color:#fbbf24}
.prob-bar-wrap{margin-top:14px}
.pb-item{margin-bottom:10px}
.pb-header{display:flex;justify-content:space-between;font-size:.8rem;margin-bottom:4px}
.pb-name{font-weight:600}
.pb-pct{font-weight:700;color:#fbbf24}
.pb-track{height:22px;background:rgba(255,255,255,.07);border-radius:11px;overflow:hidden}
.pb-fill{height:100%;border-radius:11px;display:flex;align-items:center;padding-left:10px;font-size:.72rem;font-weight:700;color:#fff;transition:width 1s ease}
.fill-ab{background:linear-gradient(90deg,#3b82f6,#60a5fa)}
.fill-bc{background:linear-gradient(90deg,#16a34a,#4ade80)}
.fill-ca{background:linear-gradient(90deg,#ea580c,#fb923c)}
.match-tabs{display:flex;gap:6px;margin-bottom:12px;flex-wrap:wrap}
.mtab{padding:7px 14px;border-radius:20px;font-size:.82rem;font-weight:700;cursor:pointer;border:1.5px solid;transition:all .2s}
.mtab.active-ab{background:rgba(59,130,246,.2);border-color:#60a5fa;color:#93c5fd}
.mtab.active-bc{background:rgba(34,197,94,.2);border-color:#4ade80;color:#86efac}
.mtab.active-ca{background:rgba(249,115,22,.2);border-color:#fb923c;color:#fdba74}
.mtab:not(.active-ab):not(.active-bc):not(.active-ca){background:transparent;border-color:#334155;color:#64748b}
.mtab:hover{opacity:.8}
.detail-panel{display:none}
.detail-panel.active{display:block}
.table-wrap{overflow-x:auto;margin-top:10px}
table{width:100%;border-collapse:collapse;font-size:.79rem}
th{background:rgba(255,255,255,.08);color:#94a3b8;font-weight:600;padding:7px 10px;text-align:center}
td{padding:7px 10px;text-align:center;border-bottom:1px solid rgba(255,255,255,.06)}
tr:last-child td{border-bottom:none}
.td-hi{color:#fbbf24;font-weight:700}
.td-win{background:rgba(34,197,94,.08);color:#86efac}
.td-lose{background:rgba(239,68,68,.08);color:#fca5a5}
.summary-chip{display:inline-block;padding:5px 13px;border-radius:20px;font-size:.82rem;font-weight:700;margin:4px 3px}
.chip-ab{background:rgba(59,130,246,.15);border:1px solid rgba(59,130,246,.4);color:#93c5fd}
.chip-bc{background:rgba(34,197,94,.15);border:1px solid rgba(34,197,94,.4);color:#86efac}
.chip-ca{background:rgba(249,115,22,.15);border:1px solid rgba(249,115,22,.4);color:#fdba74}
.key-insight{background:rgba(168,85,247,.08);border:1.5px solid rgba(168,85,247,.35);border-radius:13px;padding:13px 14px;margin-top:12px}
.ki-title{font-size:.9rem;font-weight:700;color:#c084fc;margin-bottom:8px}
.ki-body{font-size:.79rem;color:#e2e8f0;line-height:1.9}
</style>
</head>
<body>
<div class="hdr">
  <h1>📐 확률의 곱셈정리로 분석하기</h1>
  <p>P(A>B) = P(A=3)×P(B&lt;3) + P(A=6)×P(B&lt;6) — 이 계산이 바로 <strong>확률의 곱셈정리(전체확률의 법칙)</strong>입니다!</p>
</div>

<!-- 핵심 공식 -->
<div class="section">
  <div class="sec-title">📌 핵심 공식</div>
  <div class="formula-box">
    <div class="formula">P(A &gt; B) = Σ P(A=k) × P(B &lt; k)</div>
    <div class="formula sub">= P(A=k₁)·P(B&lt;k₁) + P(A=k₂)·P(B&lt;k₂) + ···</div>
    <div style="margin-top:8px;font-size:.77rem;color:#94a3b8;line-height:1.8">
      A가 나올 수 있는 각 눈 k에 대해 "A=k가 나왔을 때 B가 그보다 작을 확률"을 곱하여 모두 더합니다.<br>
      → <span style="color:#fbbf24;font-weight:600">이것이 바로 확률의 곱셈정리(전체확률의 법칙)의 적용!</span>
    </div>
  </div>
</div>

<!-- 대결 선택 탭 -->
<div class="section">
  <div class="sec-title">🔍 대결 선택 후 단계별 계산 확인</div>
  <div class="match-tabs">
    <button class="mtab active-ab" onclick="showMatch('ab', this)">A vs B</button>
    <button class="mtab" onclick="showMatch('bc', this)">B vs C</button>
    <button class="mtab" onclick="showMatch('ca', this)">C vs A</button>
  </div>

  <!-- A vs B -->
  <div id="panel-ab" class="detail-panel active">
    <div class="step-list">
      <div class="step step-1 s1">
        <div class="step-title">Step 1. 표본공간 확인</div>
        <div class="step-body">
          A = {3, 3, 3, 3, 3, 6} → P(A=3) = <span class="hl">5/6</span>, P(A=6) = <span class="hl">1/6</span><br>
          B = {2, 2, 2, 5, 5, 5} → P(B=2) = <span class="hl">1/2</span>, P(B=5) = <span class="hl">1/2</span>
        </div>
      </div>
      <div class="step step-2 s2">
        <div class="step-title">Step 2. 곱셈정리 적용</div>
        <div class="step-body">
          P(A&gt;B | A=3) = P(B&lt;3) = P(B=2) = <span class="hl">1/2</span><br>
          P(A&gt;B | A=6) = P(B&lt;6) = P(B=2)+P(B=5) = <span class="hl">1</span>
        </div>
      </div>
      <div class="step step-3 s3">
        <div class="step-title">Step 3. 전체확률의 법칙으로 합산</div>
        <div class="step-body">
          P(A&gt;B) = P(A=3)×P(B&lt;3) + P(A=6)×P(B&lt;6)<br>
          = <span class="eq">5/6 × 1/2</span> + <span class="eq">1/6 × 1</span><br>
          = <span class="eq">5/12 + 2/12</span> = <span class="hl">7/12 ≈ 58.3%</span>
        </div>
      </div>
      <div class="step step-4 s4">
        <div class="step-title">Step 4. 전체 경우의 수로 검증</div>
        <div class="step-body">
          총 36가지 경우 중 A&gt;B인 경우: (3,2)×15가지 + (6,2)×3 + (6,5)×3 = 15+3+3 = <span class="hl">21가지</span><br>
          P(A&gt;B) = <span class="hl">21/36 = 7/12 ✓</span>
        </div>
      </div>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>A＼B</th><th>2 (확률 1/2)</th><th>5 (확률 1/2)</th></tr></thead>
        <tbody>
          <tr><td class="td-hi">3 (확률 5/6)</td><td class="td-win">3&gt;2 ✅</td><td class="td-lose">3&lt;5 ❌</td></tr>
          <tr><td class="td-hi">6 (확률 1/6)</td><td class="td-win">6&gt;2 ✅</td><td class="td-win">6&gt;5 ✅</td></tr>
        </tbody>
      </table>
    </div>
    <div style="text-align:center;margin-top:10px"><span class="summary-chip chip-ab">P(A&gt;B) = 7/12 ≈ 58.3% → A 우세</span></div>
  </div>

  <!-- B vs C -->
  <div id="panel-bc" class="detail-panel">
    <div class="step-list">
      <div class="step step-1 s2">
        <div class="step-title">Step 1. 표본공간 확인</div>
        <div class="step-body">
          B = {2, 2, 2, 5, 5, 5} → P(B=2) = <span class="hl">1/2</span>, P(B=5) = <span class="hl">1/2</span><br>
          C = {1, 4, 4, 4, 4, 4} → P(C=1) = <span class="hl">1/6</span>, P(C=4) = <span class="hl">5/6</span>
        </div>
      </div>
      <div class="step step-2 s2">
        <div class="step-title">Step 2. 곱셈정리 적용</div>
        <div class="step-body">
          P(B&gt;C | B=2) = P(C&lt;2) = P(C=1) = <span class="hl">1/6</span><br>
          P(B&gt;C | B=5) = P(C&lt;5) = P(C=1)+P(C=4) = <span class="hl">1</span>
        </div>
      </div>
      <div class="step step-3 s3">
        <div class="step-title">Step 3. 전체확률의 법칙으로 합산</div>
        <div class="step-body">
          P(B&gt;C) = P(B=2)×P(C&lt;2) + P(B=5)×P(C&lt;5)<br>
          = <span class="eq">1/2 × 1/6</span> + <span class="eq">1/2 × 1</span><br>
          = <span class="eq">1/12 + 6/12</span> = <span class="hl">7/12 ≈ 58.3%</span>
        </div>
      </div>
      <div class="step step-4 s4">
        <div class="step-title">Step 4. 전체 경우의 수로 검증</div>
        <div class="step-body">
          총 36가지 경우 중 B&gt;C인 경우: (2,1)×3 + (5,1)×3 + (5,4)×15 = 3+3+15 = <span class="hl">21가지</span><br>
          P(B&gt;C) = <span class="hl">21/36 = 7/12 ✓</span>
        </div>
      </div>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>B＼C</th><th>1 (확률 1/6)</th><th>4 (확률 5/6)</th></tr></thead>
        <tbody>
          <tr><td class="td-hi">2 (확률 1/2)</td><td class="td-win">2&gt;1 ✅</td><td class="td-lose">2&lt;4 ❌</td></tr>
          <tr><td class="td-hi">5 (확률 1/2)</td><td class="td-win">5&gt;1 ✅</td><td class="td-win">5&gt;4 ✅</td></tr>
        </tbody>
      </table>
    </div>
    <div style="text-align:center;margin-top:10px"><span class="summary-chip chip-bc">P(B&gt;C) = 7/12 ≈ 58.3% → B 우세</span></div>
  </div>

  <!-- C vs A -->
  <div id="panel-ca" class="detail-panel">
    <div class="step-list">
      <div class="step step-1 s3">
        <div class="step-title">Step 1. 표본공간 확인</div>
        <div class="step-body">
          C = {1, 4, 4, 4, 4, 4} → P(C=1) = <span class="hl">1/6</span>, P(C=4) = <span class="hl">5/6</span><br>
          A = {3, 3, 3, 3, 3, 6} → P(A=3) = <span class="hl">5/6</span>, P(A=6) = <span class="hl">1/6</span>
        </div>
      </div>
      <div class="step step-2 s2">
        <div class="step-title">Step 2. 곱셈정리 적용</div>
        <div class="step-body">
          P(C&gt;A | C=1) = P(A&lt;1) = <span class="hl">0</span><br>
          P(C&gt;A | C=4) = P(A&lt;4) = P(A=3) = <span class="hl">5/6</span>
        </div>
      </div>
      <div class="step step-3 s3">
        <div class="step-title">Step 3. 전체확률의 법칙으로 합산</div>
        <div class="step-body">
          P(C&gt;A) = P(C=1)×P(A&lt;1) + P(C=4)×P(A&lt;4)<br>
          = <span class="eq">1/6 × 0</span> + <span class="eq">5/6 × 5/6</span><br>
          = <span class="eq">0 + 25/36</span> = <span class="hl">25/36 ≈ 69.4%</span>
        </div>
      </div>
      <div class="step step-4 s4">
        <div class="step-title">Step 4. 전체 경우의 수로 검증</div>
        <div class="step-body">
          총 36가지 경우 중 C&gt;A인 경우: (4,3)×5×5 = <span class="hl">25가지</span><br>
          P(C&gt;A) = <span class="hl">25/36 ≈ 69.4% ✓</span> (가장 강력한 역전!)
        </div>
      </div>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>C＼A</th><th>3 (확률 5/6)</th><th>6 (확률 1/6)</th></tr></thead>
        <tbody>
          <tr><td class="td-hi">1 (확률 1/6)</td><td class="td-lose">1&lt;3 ❌</td><td class="td-lose">1&lt;6 ❌</td></tr>
          <tr><td class="td-hi">4 (확률 5/6)</td><td class="td-win">4&gt;3 ✅</td><td class="td-lose">4&lt;6 ❌</td></tr>
        </tbody>
      </table>
    </div>
    <div style="text-align:center;margin-top:10px"><span class="summary-chip chip-ca">P(C&gt;A) = 25/36 ≈ 69.4% → C 우세 (역설!)</span></div>
  </div>
</div>

<!-- 확률 비교 바 -->
<div class="section">
  <div class="sec-title">📊 확률 비교</div>
  <div class="prob-bar-wrap">
    <div class="pb-item">
      <div class="pb-header"><span class="pb-name" style="color:#60a5fa">P(A &gt; B)</span><span class="pb-pct">7/12 = 58.3%</span></div>
      <div class="pb-track"><div class="pb-fill fill-ab" style="width:58.3%">58.3%</div></div>
    </div>
    <div class="pb-item">
      <div class="pb-header"><span class="pb-name" style="color:#4ade80">P(B &gt; C)</span><span class="pb-pct">7/12 = 58.3%</span></div>
      <div class="pb-track"><div class="pb-fill fill-bc" style="width:58.3%">58.3%</div></div>
    </div>
    <div class="pb-item">
      <div class="pb-header"><span class="pb-name" style="color:#fb923c">P(C &gt; A)</span><span class="pb-pct">25/36 = 69.4%</span></div>
      <div class="pb-track"><div class="pb-fill fill-ca" style="width:69.4%">69.4%</div></div>
    </div>
  </div>
</div>

<!-- 핵심 인사이트 -->
<div class="key-insight">
  <div class="ki-title">💡 핵심 인사이트</div>
  <div class="ki-body">
    세 주사위 모두 평균이 <strong>3.5로 동일</strong>하지만, <strong>값의 분포 방식</strong>이 다르기 때문에 이런 역설이 생깁니다.<br><br>
    A는 대부분 3이지만 가끔 6이 나오고, B는 절반이 2, 절반이 5 입니다.<br>
    → A는 B의 2를 자주 이기지만 5에는 집니다. 그런데 3이 5개라 전체적으로 A가 유리합니다.<br><br>
    C는 대부분 4인데, A의 대부분인 3보다 큽니다. 그래서 C가 A를 상대로 강합니다.<br><br>
    <span style="color:#fbbf24;font-weight:700">이처럼 '평균이 같아도 분포가 다르면 다른 결과'가 나올 수 있습니다!</span>
  </div>
</div>

<script>
const panels = ['ab','bc','ca'];
const tabs = document.querySelectorAll('.mtab');
function showMatch(id, btn) {
  panels.forEach(p => document.getElementById('panel-'+p).classList.remove('active'));
  tabs.forEach(t => t.className = 'mtab');
  document.getElementById('panel-'+id).classList.add('active');
  const classMap = {ab:'active-ab', bc:'active-bc', ca:'active-ca'};
  btn.classList.add(classMap[id]);
}
</script>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
# 탭 3: 대결 시뮬레이션 (애니메이션)
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TAB3 = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);color:#e2e8f0;padding:16px 14px 32px}
.hdr{text-align:center;padding:16px 20px 12px;background:linear-gradient(135deg,rgba(16,185,129,.12),rgba(99,102,241,.1));border:1px solid rgba(16,185,129,.3);border-radius:14px;margin-bottom:12px}
.hdr h1{font-size:1.25rem;font-weight:800;color:#34d399;margin-bottom:5px}
.hdr p{font-size:.8rem;color:#94a3b8;line-height:1.7}
.section{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:14px;padding:15px 14px;margin-bottom:12px}
.sec-title{font-size:.97rem;font-weight:700;margin-bottom:10px;color:#34d399;display:flex;align-items:center;gap:7px}
.ctrl-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.ctrl-row label{font-size:.8rem;color:#94a3b8}
select,input[type=number]{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);border-radius:8px;color:#e2e8f0;padding:6px 10px;font-size:.85rem;width:auto}
.roll-btn{padding:10px 22px;border-radius:11px;background:linear-gradient(135deg,#10b981,#059669);border:none;color:#fff;font-size:.92rem;font-weight:700;cursor:pointer;transition:all .2s;flex-shrink:0}
.roll-btn:hover{background:linear-gradient(135deg,#34d399,#10b981);transform:scale(1.04)}
.roll-btn:active{transform:scale(.97)}
.auto-btn{padding:10px 18px;border-radius:11px;background:rgba(99,102,241,.15);border:1.5px solid rgba(99,102,241,.4);color:#a5b4fc;font-size:.88rem;font-weight:700;cursor:pointer;transition:all .2s}
.auto-btn:hover{background:rgba(99,102,241,.25)}
.battle-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:14px}
.battle-card{border-radius:14px;padding:14px 10px;text-align:center}
.bc-ab{background:rgba(59,130,246,.08);border:1.5px solid rgba(59,130,246,.3)}
.bc-bc{background:rgba(34,197,94,.08);border:1.5px solid rgba(34,197,94,.3)}
.bc-ca{background:rgba(249,115,22,.08);border:1.5px solid rgba(249,115,22,.3)}
.bc-header{font-size:.82rem;font-weight:700;margin-bottom:10px}
.bc-ab .bc-header{color:#60a5fa}
.bc-bc .bc-header{color:#4ade80}
.bc-ca .bc-header{color:#fb923c}
.dice-display{display:flex;align-items:center;justify-content:center;gap:8px;margin-bottom:8px}
.die-face{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;font-weight:900;border:2px solid;transition:all .15s;position:relative}
.die-a{background:rgba(59,130,246,.2);border-color:#60a5fa;color:#bfdbfe}
.die-b{background:rgba(34,197,94,.2);border-color:#4ade80;color:#bbf7d0}
.die-c{background:rgba(249,115,22,.2);border-color:#fb923c;color:#fed7aa}
.die-face.rolling{animation:shake .15s infinite}
@keyframes shake{0%,100%{transform:rotate(-8deg) scale(1.1)}50%{transform:rotate(8deg) scale(1.05)}}
.vs-label{font-size:.7rem;color:#475569;font-weight:700}
.result-label{font-size:.78rem;font-weight:700;padding:3px 10px;border-radius:12px;display:inline-block}
.win-a{background:rgba(59,130,246,.2);color:#93c5fd}
.win-b{background:rgba(34,197,94,.2);color:#86efac}
.win-c{background:rgba(249,115,22,.2);color:#fdba74}
.tie-res{background:rgba(148,163,184,.15);color:#94a3b8}
.score-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}
.score-item{border-radius:12px;padding:11px 8px;text-align:center}
.sc-ab{background:rgba(59,130,246,.07);border:1px solid rgba(59,130,246,.25)}
.sc-bc{background:rgba(34,197,94,.07);border:1px solid rgba(34,197,94,.25)}
.sc-ca{background:rgba(249,115,22,.07);border:1px solid rgba(249,115,22,.25)}
.sc-label{font-size:.72rem;color:#64748b;margin-bottom:5px}
.sc-vals{display:flex;justify-content:space-around;margin-bottom:5px}
.sc-val{font-size:.88rem;font-weight:700}
.sc-bar-wrap{height:8px;background:rgba(255,255,255,.07);border-radius:4px;overflow:hidden;margin-top:4px}
.sc-bar{height:100%;border-radius:4px;transition:width .4s ease}
.bar-a{background:#3b82f6}.bar-b{background:#22c55e}.bar-c{background:#f97316}
.sc-pct{font-size:.7rem;margin-top:4px}
.cycle-result{text-align:center;padding:14px;border-radius:13px;background:rgba(168,85,247,.07);border:1.5px solid rgba(168,85,247,.3);margin-top:10px;display:none}
.cr-title{font-size:.95rem;font-weight:700;color:#c084fc;margin-bottom:8px}
.cr-cycle{font-size:1.1rem;font-weight:800;color:#fbbf24;letter-spacing:2px}
.cr-desc{font-size:.79rem;color:#cbd5e1;margin-top:8px;line-height:1.8}
.reset-btn{margin-top:10px;padding:8px 18px;border-radius:10px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.15);color:#94a3b8;font-size:.8rem;cursor:pointer;transition:all .2s}
.reset-btn:hover{background:rgba(255,255,255,.1);color:#e2e8f0}
</style>
</head>
<body>
<div class="hdr">
  <h1>🏆 대결 시뮬레이션</h1>
  <p>직접 주사위를 굴려서 비추이성을 확인해보세요! 많이 굴릴수록 이론값에 가까워집니다.</p>
</div>

<div class="section">
  <div class="sec-title">🎮 주사위 굴리기</div>
  <div class="ctrl-row">
    <label>굴리기 횟수:</label>
    <input type="number" id="nRolls" value="1" min="1" max="100" style="width:70px">
    <button class="roll-btn" onclick="rollDice()">🎲 굴리기!</button>
    <button class="auto-btn" id="autoBtn" onclick="toggleAuto()">▶ 자동 (1초)</button>
    <button class="reset-btn" onclick="resetAll()">🔄 초기화</button>
  </div>
  
  <div class="battle-grid">
    <!-- A vs B -->
    <div class="battle-card bc-ab">
      <div class="bc-header">⚔ A vs B</div>
      <div class="dice-display">
        <div class="die-face die-a" id="die-a1">3</div>
        <div class="vs-label">vs</div>
        <div class="die-face die-b" id="die-b1">2</div>
      </div>
      <div><span class="result-label" id="res-ab">-</span></div>
    </div>
    <!-- B vs C -->
    <div class="battle-card bc-bc">
      <div class="bc-header">⚔ B vs C</div>
      <div class="dice-display">
        <div class="die-face die-b" id="die-b2">2</div>
        <div class="vs-label">vs</div>
        <div class="die-face die-c" id="die-c1">4</div>
      </div>
      <div><span class="result-label" id="res-bc">-</span></div>
    </div>
    <!-- C vs A -->
    <div class="battle-card bc-ca">
      <div class="bc-header">⚔ C vs A</div>
      <div class="dice-display">
        <div class="die-face die-c" id="die-c2">4</div>
        <div class="vs-label">vs</div>
        <div class="die-face die-a" id="die-a2">3</div>
      </div>
      <div><span class="result-label" id="res-ca">-</span></div>
    </div>
  </div>
</div>

<div class="section">
  <div class="sec-title">📊 누적 점수판 <span id="total-label" style="font-size:.78rem;color:#64748b;font-weight:400"></span></div>
  <div class="score-grid">
    <div class="score-item sc-ab">
      <div class="sc-label">A vs B</div>
      <div class="sc-vals">
        <div><div class="sc-val" style="color:#60a5fa" id="s-a-ab">0</div><div style="font-size:.65rem;color:#64748b">A승</div></div>
        <div><div class="sc-val" style="color:#4ade80" id="s-b-ab">0</div><div style="font-size:.65rem;color:#64748b">B승</div></div>
        <div><div class="sc-val" style="color:#475569" id="s-t-ab">0</div><div style="font-size:.65rem;color:#64748b">무</div></div>
      </div>
      <div class="sc-bar-wrap"><div class="sc-bar bar-a" id="bar-ab" style="width:50%"></div></div>
      <div class="sc-pct" id="pct-ab" style="color:#60a5fa">-</div>
    </div>
    <div class="score-item sc-bc">
      <div class="sc-label">B vs C</div>
      <div class="sc-vals">
        <div><div class="sc-val" style="color:#4ade80" id="s-b-bc">0</div><div style="font-size:.65rem;color:#64748b">B승</div></div>
        <div><div class="sc-val" style="color:#fb923c" id="s-c-bc">0</div><div style="font-size:.65rem;color:#64748b">C승</div></div>
        <div><div class="sc-val" style="color:#475569" id="s-t-bc">0</div><div style="font-size:.65rem;color:#64748b">무</div></div>
      </div>
      <div class="sc-bar-wrap"><div class="sc-bar bar-b" id="bar-bc" style="width:50%"></div></div>
      <div class="sc-pct" id="pct-bc" style="color:#4ade80">-</div>
    </div>
    <div class="score-item sc-ca">
      <div class="sc-label">C vs A</div>
      <div class="sc-vals">
        <div><div class="sc-val" style="color:#fb923c" id="s-c-ca">0</div><div style="font-size:.65rem;color:#64748b">C승</div></div>
        <div><div class="sc-val" style="color:#60a5fa" id="s-a-ca">0</div><div style="font-size:.65rem;color:#64748b">A승</div></div>
        <div><div class="sc-val" style="color:#475569" id="s-t-ca">0</div><div style="font-size:.65rem;color:#64748b">무</div></div>
      </div>
      <div class="sc-bar-wrap"><div class="sc-bar bar-c" id="bar-ca" style="width:50%"></div></div>
      <div class="sc-pct" id="pct-ca" style="color:#fb923c">-</div>
    </div>
  </div>
  <div id="cycle-result" class="cycle-result">
    <div class="cr-title">🔄 비추이성 패턴 확인!</div>
    <div class="cr-cycle">A → B → C → A (순환)</div>
    <div class="cr-desc">이론값: P(A&gt;B) = 58.3%, P(B&gt;C) = 58.3%, P(C&gt;A) = 69.4%<br>
    시뮬레이션이 이론값에 가까워지고 있나요? 더 많이 굴려볼수록 이론값에 가까워집니다!</div>
  </div>
</div>

<script>
const DICE = {A:[3,3,3,3,3,6], B:[2,2,2,5,5,5], C:[1,4,4,4,4,4]};
const score = {ab:{a:0,b:0,t:0}, bc:{b:0,c:0,t:0}, ca:{c:0,a:0,t:0}};
let total = 0, autoTimer = null;

function choice(arr){ return arr[Math.floor(Math.random()*arr.length)]; }

function rollDice() {
  const n = parseInt(document.getElementById('nRolls').value) || 1;
  for(let i=0; i<n; i++) singleRoll(i < n-1);
  updateScores();
}

function singleRoll(silent) {
  const a1 = choice(DICE.A), b1 = choice(DICE.B);
  const b2 = choice(DICE.B), c1 = choice(DICE.C);
  const c2 = choice(DICE.C), a2 = choice(DICE.A);
  
  if(!silent) {
    animateDice('die-a1', a1, 'die-a'); animateDice('die-b1', b1, 'die-b');
    animateDice('die-b2', b2, 'die-b'); animateDice('die-c1', c1, 'die-c');
    animateDice('die-c2', c2, 'die-c'); animateDice('die-a2', a2, 'die-a');
    showResult('res-ab', a1, b1, 'A', 'B', 'win-a', 'win-b');
    showResult('res-bc', b2, c1, 'B', 'C', 'win-b', 'win-c');
    showResult('res-ca', c2, a2, 'C', 'A', 'win-c', 'win-a');
  }
  
  // A vs B
  if(a1>b1) score.ab.a++;
  else if(a1<b1) score.ab.b++;
  else score.ab.t++;
  // B vs C
  if(b2>c1) score.bc.b++;
  else if(b2<c1) score.bc.c++;
  else score.bc.t++;
  // C vs A
  if(c2>a2) score.ca.c++;
  else if(c2<a2) score.ca.a++;
  else score.ca.t++;
  total++;
}

function animateDice(id, val, cls) {
  const el = document.getElementById(id);
  el.classList.add('rolling');
  setTimeout(()=>{
    el.textContent = val;
    el.classList.remove('rolling');
  }, 200);
}

function showResult(id, v1, v2, n1, n2, cls1, cls2) {
  const el = document.getElementById(id);
  if(v1>v2){ el.textContent = n1+' 승 ('+v1+' > '+v2+')'; el.className='result-label '+cls1; }
  else if(v1<v2){ el.textContent = n2+' 승 ('+v1+' < '+v2+')'; el.className='result-label '+cls2; }
  else { el.textContent = '무승부 ('+v1+' = '+v2+')'; el.className='result-label tie-res'; }
}

function updateScores() {
  document.getElementById('total-label').textContent = '(총 '+total+'회)';
  // A vs B
  const ab = score.ab.a+score.ab.b+score.ab.t||1;
  document.getElementById('s-a-ab').textContent = score.ab.a;
  document.getElementById('s-b-ab').textContent = score.ab.b;
  document.getElementById('s-t-ab').textContent = score.ab.t;
  const pAB = score.ab.a/ab*100;
  document.getElementById('bar-ab').style.width = pAB+'%';
  document.getElementById('pct-ab').textContent = 'A승률 '+pAB.toFixed(1)+'% (이론 58.3%)';
  // B vs C
  const bc = score.bc.b+score.bc.c+score.bc.t||1;
  document.getElementById('s-b-bc').textContent = score.bc.b;
  document.getElementById('s-c-bc').textContent = score.bc.c;
  document.getElementById('s-t-bc').textContent = score.bc.t;
  const pBC = score.bc.b/bc*100;
  document.getElementById('bar-bc').style.width = pBC+'%';
  document.getElementById('pct-bc').textContent = 'B승률 '+pBC.toFixed(1)+'% (이론 58.3%)';
  // C vs A
  const ca = score.ca.c+score.ca.a+score.ca.t||1;
  document.getElementById('s-c-ca').textContent = score.ca.c;
  document.getElementById('s-a-ca').textContent = score.ca.a;
  document.getElementById('s-t-ca').textContent = score.ca.t;
  const pCA = score.ca.c/ca*100;
  document.getElementById('bar-ca').style.width = pCA+'%';
  document.getElementById('pct-ca').textContent = 'C승률 '+pCA.toFixed(1)+'% (이론 69.4%)';
  
  if(total >= 30) document.getElementById('cycle-result').style.display = 'block';
}

function toggleAuto() {
  const btn = document.getElementById('autoBtn');
  if(autoTimer) {
    clearInterval(autoTimer);
    autoTimer = null;
    btn.textContent = '▶ 자동 (1초)';
    btn.style.background = 'rgba(99,102,241,.15)';
  } else {
    autoTimer = setInterval(()=>{ singleRoll(false); updateScores(); }, 800);
    btn.textContent = '⏹ 중지';
    btn.style.background = 'rgba(239,68,68,.2)';
  }
}

function resetAll() {
  if(autoTimer){ clearInterval(autoTimer); autoTimer=null; }
  Object.assign(score, {ab:{a:0,b:0,t:0}, bc:{b:0,c:0,t:0}, ca:{c:0,a:0,t:0}});
  total = 0;
  updateScores();
  document.getElementById('total-label').textContent = '';
  document.getElementById('cycle-result').style.display = 'none';
  ['res-ab','res-bc','res-ca'].forEach(id=>{
    const el=document.getElementById(id); el.textContent='-'; el.className='result-label';
  });
  document.getElementById('autoBtn').textContent='▶ 자동 (1초)';
  document.getElementById('autoBtn').style.background='rgba(99,102,241,.15)';
}
</script>
</body></html>"""

# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.markdown("## 🎲 신기한(비추이적) 주사위")
    st.markdown(
        "> A가 B를 자주 이기고, B가 C를 자주 이기는데도 C가 A를 이긴다?  \n"
        "> **확률의 곱셈정리**로 이 놀라운 역설을 분석해봅시다!"
    )

    tab1, tab2, tab3 = st.tabs(["🎲 주사위 소개", "📐 이론 계산", "🏆 대결 시뮬레이션"])

    with tab1:
        components.html(_HTML_TAB1, height=1300, scrolling=False)

    with tab2:
        components.html(_HTML_TAB2, height=1600, scrolling=False)

    with tab3:
        components.html(_HTML_TAB3, height=1100, scrolling=False)

    st.divider()

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
