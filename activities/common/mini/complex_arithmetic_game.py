# activities/common/mini/complex_arithmetic_game.py
"""
복소수 사칙연산 마스터 – 계산 배틀!
덧셈·뺄셈 → 곱셈 → 켤레·나눗셈의 3단계 게임으로
복소수 연산을 실수처럼 능숙하게 다루는 능력을 키우는 활동입니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

# ── Google Sheets 연동 ──────────────────────────────────────────────────────
_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "복소수사칙연산"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key":    "곱셈오류분석",
        "label":  "복소수 곱셈 (2+3i)(1−2i)를 직접 전개하여 답을 구하고, 실수와 달리 i²=−1을 적용해야 하는 이유를 설명하세요.",
        "type":   "text_area",
        "height": 90,
    },
    {
        "key":    "켤레활용",
        "label":  "복소수 나눗셈에서 분모의 켤레복소수를 곱하면 왜 분모가 실수가 되는지, (a+bi)(a−bi) 계산과 연결하여 설명하세요.",
        "type":   "text_area",
        "height": 90,
    },
    {
        "key":    "새롭게알게된점",
        "label":  "💡 이 활동을 통해 새롭게 알게 된 점",
        "type":   "text_area",
        "height": 90,
    },
    {
        "key":    "느낀점",
        "label":  "💬 이 활동을 하면서 느낀 점",
        "type":   "text_area",
        "height": 90,
    },
]

META = {
    "title":       "⚡ 복소수 계산 배틀!",
    "description": "덧셈·뺄셈→곱셈→켤레·나눗셈 3단계 게임으로 복소수 사칙연산을 정복하는 활동입니다.",
    "order":       202,
}

# ─────────────────────────────────────────────────────────────────────────────
_GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>복소수 계산 배틀</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(160deg,#0a0a1f 0%,#1a0a3a 50%,#0d1a2e 100%);
  color:#e2e8f0;min-height:900px;padding:14px 12px;
  overflow-x:hidden;
}

/* ── 화면 전환 ── */
.screen{display:none;animation:fadeIn .35s ease}
.screen.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}

/* ── 공통 ── */
h2{text-align:center;color:#a78bfa;font-size:1.35rem;margin-bottom:5px}
.subtitle{text-align:center;color:#c4b5fd;font-size:.83rem;margin-bottom:14px}

/* ── 공식 칩 (실수=초록, 허수=보라, i=핑크) ── */
.re{color:#34d399;font-weight:700}
.im{color:#c084fc;font-weight:700}
.ii{color:#f0abfc;font-weight:700;font-style:italic}
.hi{background:rgba(245,158,11,.25);border-radius:4px;padding:0 3px;color:#fcd34d;font-weight:700}

/* ── 탑바 ── */
.top-bar{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px}
.phase-badge{
  background:rgba(167,139,250,.18);border:1.5px solid #7c3aed;
  border-radius:99px;padding:3px 14px;font-size:.76rem;color:#c4b5fd;font-weight:600;
}
.score-badge{
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(245,158,11,.12);border:1.5px solid #f59e0b;
  border-radius:99px;padding:3px 12px;font-size:.8rem;color:#fcd34d;font-weight:700;
}

/* ── 진행 바 ── */
.prog-wrap{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.prog-bar{flex:1;height:8px;background:rgba(255,255,255,.1);border-radius:99px;overflow:hidden}
.prog-fill{height:100%;background:linear-gradient(90deg,#f0abfc,#7c3aed);border-radius:99px;transition:width .4s ease}
.prog-label{font-size:.74rem;color:#9ca3af;white-space:nowrap;min-width:44px;text-align:right}

/* ── 공식 카드 (위쪽 힌트) ── */
.formula-card{
  background:rgba(99,102,241,.12);border:1.5px solid rgba(129,140,248,.35);
  border-radius:12px;padding:10px 14px;margin-bottom:10px;font-size:.82rem;
  color:#c7d2fe;line-height:1.7;
}
.formula-card b{color:#e2e8f0}
.formula-card .re{color:#34d399}
.formula-card .im{color:#c084fc}
.formula-card .ii{color:#f0abfc;font-style:italic}

/* ── 문제 카드 ── */
.q-card{
  background:rgba(255,255,255,.05);backdrop-filter:blur(8px);
  border:1.5px solid rgba(167,139,250,.32);border-radius:16px;
  padding:16px 14px;margin-bottom:12px;text-align:center;
  box-shadow:0 4px 28px rgba(0,0,0,.5);
}
.q-type-label{font-size:.71rem;color:#9ca3af;margin-bottom:8px;letter-spacing:.06em;text-transform:uppercase}
.complex-expr{
  font-size:1.75rem;font-weight:800;color:#f5f3ff;
  margin-bottom:6px;line-height:1.45;
}
.complex-expr .re{color:#34d399}
.complex-expr .im{color:#c084fc}
.complex-expr .ii{color:#f0abfc;font-style:italic}
.q-sub{font-size:.85rem;color:#9ca3af;margin-top:4px}

/* ── 보기 (4지선다 2×2 그리드) ── */
.choices-grid{
  display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:12px;
}
.choice-btn{
  padding:11px 10px;border-radius:12px;
  border:2px solid rgba(167,139,250,.22);
  background:rgba(255,255,255,.04);
  color:#e2e8f0;font-size:.9rem;font-weight:700;
  cursor:pointer;transition:all .18s;text-align:center;line-height:1.35;
}
.choice-btn:hover:not(:disabled){
  border-color:#a78bfa;background:rgba(167,139,250,.18);
  transform:translateY(-2px);
}
.choice-btn:disabled{opacity:.45;cursor:default;transform:none}
.choice-btn.correct{
  border-color:#34d399 !important;background:rgba(16,185,129,.22) !important;
  color:#6ee7b7 !important;animation:popIn .35s;
}
.choice-btn.wrong{
  border-color:#ef4444 !important;background:rgba(239,68,68,.18) !important;
  color:#fca5a5 !important;
}
@keyframes popIn{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}

/* ── 레이블 A B C D ── */
.choice-label{
  display:inline-block;width:22px;height:22px;line-height:22px;
  border-radius:50%;background:rgba(167,139,250,.3);
  font-size:.72rem;font-weight:800;margin-right:6px;
  text-align:center;flex-shrink:0;
}
.choice-inner{display:flex;align-items:center;justify-content:center;gap:4px}

/* ── 피드백 박스 ── */
.feedback{
  border-radius:12px;padding:11px 14px;margin-bottom:10px;
  font-size:.86rem;line-height:1.6;
}
.feedback.correct{background:rgba(16,185,129,.14);border:1.5px solid #34d399;color:#6ee7b7}
.feedback.wrong{background:rgba(239,68,68,.13);border:1.5px solid #f87171;color:#fca5a5}
.feedback.hidden{visibility:hidden;min-height:40px}

/* ── 풀이 스텝 ── */
.sol-steps{
  margin-top:8px;padding:8px 12px;
  background:rgba(0,0,0,.2);border-radius:8px;
  font-size:.81rem;color:#c4b5fd;line-height:1.8;
}
.sol-steps .re{color:#34d399}
.sol-steps .im{color:#c084fc}
.sol-steps .ii{color:#f0abfc;font-style:italic}
.sol-steps .hi{background:rgba(245,158,11,.25);border-radius:3px;padding:0 3px;color:#fcd34d}
.sol-steps b{color:#e2e8f0}

/* ── 다음 버튼 ── */
.next-btn{
  display:block;margin:4px auto 0;padding:9px 30px;
  background:linear-gradient(135deg,#7c3aed,#4338ca);
  border:none;border-radius:99px;color:#fff;
  font-size:.92rem;font-weight:700;cursor:pointer;
  transition:.18s;box-shadow:0 4px 16px rgba(124,58,237,.4);
}
.next-btn:hover{transform:translateY(-2px);box-shadow:0 6px 22px rgba(124,58,237,.55)}

/* ── 인트로 박스 ── */
.intro-box{
  background:rgba(255,255,255,.05);border:1.5px solid rgba(167,139,250,.26);
  border-radius:16px;padding:16px 14px;margin-bottom:12px;
}
.intro-row{display:flex;align-items:flex-start;gap:10px;padding:5px 0;font-size:.87rem;line-height:1.55}
.intro-icon{font-size:1.25rem;min-width:30px;text-align:center;padding-top:1px}
.rule-box{
  background:rgba(99,102,241,.1);border-left:3px solid #818cf8;
  border-radius:0 10px 10px 0;padding:9px 13px;margin:6px 0;
  font-size:.84rem;color:#c7d2fe;line-height:1.7;
}
.rule-box .re{color:#34d399}
.rule-box .im{color:#c084fc}
.rule-box .ii{color:#f0abfc;font-style:italic}
.rule-box b{color:#e2e8f0}

/* ── Break 화면 ── */
.break-box{
  background:rgba(255,255,255,.05);border:1.5px solid rgba(167,139,250,.26);
  border-radius:18px;padding:22px 18px;text-align:center;margin-bottom:16px;
}
.break-icon{font-size:3rem;margin-bottom:8px}
.break-title{font-size:1.15rem;font-weight:700;color:#f0abfc;margin-bottom:10px}
.break-formula{
  background:rgba(0,0,0,.25);border:1.5px solid rgba(167,139,250,.28);
  border-radius:12px;padding:12px 14px;margin:10px 0;
  font-size:.85rem;color:#c4b5fd;line-height:1.8;text-align:left;
}
.break-formula b{color:#e2e8f0}
.break-formula .re{color:#34d399}
.break-formula .im{color:#c084fc}
.break-formula .ii{color:#f0abfc;font-style:italic}
.break-formula .hi{background:rgba(245,158,11,.25);border-radius:3px;padding:0 3px;color:#fcd34d}

/* ── 결과 화면 ── */
.result-wrap{text-align:center}
.result-circle{
  width:130px;height:130px;border-radius:50%;
  border:4px solid #a78bfa;background:rgba(139,92,246,.18);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  margin:12px auto 14px;box-shadow:0 0 40px rgba(139,92,246,.4);
}
.result-emoji{font-size:2.5rem;line-height:1}
.result-score{font-size:1.05rem;font-weight:800;color:#e2e8f0;margin-top:5px}
.result-max{font-size:.74rem;color:#9ca3af}
.result-msg{font-size:.88rem;color:#c4b5fd;line-height:1.7;margin-bottom:14px;padding:0 8px}
.result-bar-wrap{background:rgba(255,255,255,.08);border-radius:99px;height:12px;overflow:hidden;margin:8px 0 16px}
.result-bar-fill{height:100%;border-radius:99px;background:linear-gradient(90deg,#f0abfc,#7c3aed);transition:width 1.2s ease}
.summary-chips{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:14px}
.summary-chip{
  border-radius:8px;padding:5px 14px;font-size:.78rem;font-weight:700;
  border:1.5px solid;
}
.chip-add{background:rgba(16,185,129,.15);border-color:#34d399;color:#6ee7b7}
.chip-mul{background:rgba(99,102,241,.15);border-color:#818cf8;color:#c7d2fe}
.chip-conj{background:rgba(245,158,11,.15);border-color:#f59e0b;color:#fcd34d}
</style>
</head>
<body>

<!-- ════════════════ 인트로 ════════════════ -->
<div id="introScreen" class="screen active">
  <h2>⚡ 복소수 계산 배틀!</h2>
  <p class="subtitle">3단계 게임으로 복소수 사칙연산을 완전 정복해 봅시다!</p>

  <div class="intro-box">
    <div class="intro-row">
      <span class="intro-icon">➕</span>
      <div>
        <strong style="color:#34d399">Phase 1 · 덧셈&뺄셈</strong>&nbsp; (5문제)<br>
        실수부분끼리, 허수부분끼리 따로 계산해요.
      </div>
    </div>
    <div class="intro-row">
      <span class="intro-icon">✖️</span>
      <div>
        <strong style="color:#c084fc">Phase 2 · 곱셈</strong>&nbsp; (5문제)<br>
        다항식처럼 전개하되, <span style="color:#fcd34d;font-weight:700">i²= −1</span> 을 꼭 적용해야 해요!
      </div>
    </div>
    <div class="intro-row">
      <span class="intro-icon">🔗</span>
      <div>
        <strong style="color:#f0abfc">Phase 3 · 켤레·나눗셈</strong>&nbsp; (5문제)<br>
        켤레복소수를 찾고, 분모의 켤레를 곱해 나눗셈을 계산해요.
      </div>
    </div>
  </div>

  <div class="rule-box">
    💡 핵심 공식 미리 보기<br>
    &nbsp;• 덧셈: <span class="re">(a+c)</span> + <span class="im">(b+d)</span><span class="ii">i</span><br>
    &nbsp;• 곱셈: <span class="re">(ac−bd)</span> + <span class="im">(ad+bc)</span><span class="ii">i</span> &nbsp;←&nbsp; <span class="hi">i²=−1</span> 적용<br>
    &nbsp;• 켤레: <span class="re">a</span>+<span class="im">b</span><span class="ii">i</span> 의 켤레 = <span class="re">a</span>−<span class="im">b</span><span class="ii">i</span><br>
    &nbsp;• 나눗셈: 분모의 켤레복소수를 분자·분모에 곱함 → 분모를 실수화
  </div>

  <br>
  <button class="next-btn" onclick="startGame()">▶ 배틀 시작!</button>
</div>


<!-- ════════════════ 게임 ════════════════ -->
<div id="gameScreen" class="screen">
  <div class="top-bar">
    <div class="phase-badge" id="phaseBadge">Phase 1</div>
    <div class="score-badge">⚡ <span id="scoreDisp">0</span> / 150점</div>
  </div>
  <div class="prog-wrap">
    <div class="prog-bar"><div class="prog-fill" id="progFill" style="width:0%"></div></div>
    <div class="prog-label" id="progLabel">1 / 5</div>
  </div>

  <div class="formula-card" id="formulaCard"></div>

  <div class="q-card">
    <div class="q-type-label" id="qTypeLabel">계산하세요</div>
    <div class="complex-expr" id="complexExpr"></div>
    <div class="q-sub" id="qSub"></div>
  </div>

  <div class="choices-grid" id="choicesGrid"></div>

  <div class="feedback hidden" id="feedbackBox"></div>
  <button class="next-btn" id="nextBtn" onclick="nextQuestion()" style="display:none">다음 ▶</button>
</div>


<!-- ════════════════ Break ════════════════ -->
<div id="breakScreen" class="screen">
  <div class="break-box">
    <div class="break-icon" id="breakIcon">🎯</div>
    <div class="break-title" id="breakTitle"></div>
    <div class="break-formula" id="breakFormula"></div>
  </div>
  <button class="next-btn" onclick="startNextPhase()">다음 단계로 ▶</button>
</div>


<!-- ════════════════ 결과 ════════════════ -->
<div id="resultScreen" class="screen">
  <h2>🏆 배틀 완주!</h2>
  <div class="result-wrap">
    <div class="result-circle">
      <div class="result-emoji" id="resultEmoji">🌟</div>
      <div class="result-score" id="resultScore">0점</div>
      <div class="result-max">/ 150점</div>
    </div>
    <div class="result-bar-wrap">
      <div class="result-bar-fill" id="resultBarFill" style="width:0%"></div>
    </div>
    <div class="result-msg" id="resultMsg"></div>
  </div>

  <div class="summary-chips">
    <span class="summary-chip chip-add">➕ 덧셈·뺄셈</span>
    <span class="summary-chip chip-mul">✖️ 곱셈 (i²=−1!)</span>
    <span class="summary-chip chip-conj">🔗 켤레·나눗셈</span>
  </div>

  <div class="rule-box" style="font-size:.82rem">
    🔑 <b>최종 정리</b><br>
    &nbsp;• 덧셈·뺄셈은 <b>실수↔실수, 허수↔허수</b>끼리 계산<br>
    &nbsp;• 곱셈은 다항식 전개 후 <span class="hi">i²=−1</span> 대입<br>
    &nbsp;• 나눗셈은 분모의 <b>켤레복소수</b>를 곱해 분모를 실수로 변환<br>
    &nbsp;• (<span class="re">a</span>+<span class="im">b</span><span class="ii">i</span>)(<span class="re">a</span>−<span class="im">b</span><span class="ii">i</span>) = <span class="re">a²</span>+<span class="im">b²</span> &nbsp;→&nbsp; 항상 실수!
  </div>
  <br>
  <button class="next-btn" onclick="restartGame()">🔄 처음부터 다시</button>
</div>


<!-- ════════════════ JavaScript ════════════════ -->
<script>
// ── 게임 데이터 ────────────────────────────────────────────────────────────

// Phase 1: 덧셈·뺄셈 (5문제)
const P1 = [
  {
    expr: '(<span class="re">3</span>+<span class="im">2</span><span class="ii">i</span>) + (<span class="re">1</span>+<span class="im">4</span><span class="ii">i</span>) = ?',
    choices: [
      '4+6<span class="ii">i</span>',
      '4+8<span class="ii">i</span>',
      '3+6<span class="ii">i</span>',
      '4+2<span class="ii">i</span>'
    ],
    correct: 0,
    solution: `
      <b>실수끼리:</b> <span class="re">3+1=4</span><br>
      <b>허수끼리:</b> <span class="im">2+4=6</span><br>
      ∴ 답 = <b>4+6<span class="ii">i</span></b>`
  },
  {
    expr: '(<span class="re">5</span>−<span class="im">3</span><span class="ii">i</span>) + (<span class="re">−2</span>+<span class="im">1</span><span class="ii">i</span>) = ?',
    choices: [
      '3+2<span class="ii">i</span>',
      '3−2<span class="ii">i</span>',
      '7−4<span class="ii">i</span>',
      '3−4<span class="ii">i</span>'
    ],
    correct: 1,
    solution: `
      <b>실수끼리:</b> <span class="re">5+(−2)=3</span><br>
      <b>허수끼리:</b> <span class="im">−3+1=−2</span><br>
      ∴ 답 = <b>3−2<span class="ii">i</span></b>`
  },
  {
    expr: '(<span class="re">4</span>+<span class="im">1</span><span class="ii">i</span>) − (<span class="re">1</span>+<span class="im">3</span><span class="ii">i</span>) = ?',
    choices: [
      '5+4<span class="ii">i</span>',
      '3+4<span class="ii">i</span>',
      '3−2<span class="ii">i</span>',
      '3+2<span class="ii">i</span>'
    ],
    correct: 2,
    solution: `
      <b>실수끼리:</b> <span class="re">4−1=3</span><br>
      <b>허수끼리:</b> <span class="im">1−3=−2</span><br>
      ∴ 답 = <b>3−2<span class="ii">i</span></b>`
  },
  {
    expr: '(<span class="re">2</span>+<span class="im">5</span><span class="ii">i</span>) + (<span class="re">−2</span>−<span class="im">5</span><span class="ii">i</span>) = ?',
    choices: [
      '4+10<span class="ii">i</span>',
      '10<span class="ii">i</span>',
      '4',
      '0'
    ],
    correct: 3,
    solution: `
      <b>실수끼리:</b> <span class="re">2+(−2)=0</span><br>
      <b>허수끼리:</b> <span class="im">5+(−5)=0</span><br>
      ∴ 답 = <b>0</b> &nbsp;← 켤레복소수를 더하면 실수가 돼요!`
  },
  {
    expr: '(<span class="re">−1</span>+<span class="im">3</span><span class="ii">i</span>) − (<span class="re">−3</span>−<span class="im">2</span><span class="ii">i</span>) = ?',
    choices: [
      '−4+<span class="ii">i</span>',
      '2+5<span class="ii">i</span>',
      '2+<span class="ii">i</span>',
      '−4+5<span class="ii">i</span>'
    ],
    correct: 1,
    solution: `
      <b>실수끼리:</b> <span class="re">−1−(−3)=−1+3=2</span><br>
      <b>허수끼리:</b> <span class="im">3−(−2)=3+2=5</span><br>
      ∴ 답 = <b>2+5<span class="ii">i</span></b>`
  },
];

// Phase 2: 곱셈 (5문제)
const P2 = [
  {
    expr: '(<span class="re">2</span>+<span class="ii">i</span>)(<span class="re">1</span>+<span class="im">3</span><span class="ii">i</span>) = ?',
    choices: [
      '2+7<span class="ii">i</span>',
      '−1−7<span class="ii">i</span>',
      '−1+7<span class="ii">i</span>',
      '5+7<span class="ii">i</span>'
    ],
    correct: 2,
    solution: `
      전개: 2·1 + 2·3<span class="ii">i</span> + <span class="ii">i</span>·1 + <span class="ii">i</span>·3<span class="ii">i</span><br>
      = 2 + 6<span class="ii">i</span> + <span class="ii">i</span> + 3<span class="hi">i²</span><br>
      = 2 + 7<span class="ii">i</span> + 3×<span class="hi">(−1)</span><br>
      = <b>−1+7<span class="ii">i</span></b>`
  },
  {
    expr: '(<span class="re">3</span>−<span class="ii">i</span>)(<span class="re">3</span>+<span class="ii">i</span>) = ?',
    choices: [
      '8',
      '9',
      '10<span class="ii">i</span>',
      '10'
    ],
    correct: 3,
    solution: `
      합차공식 적용: <span class="re">3²</span> − (<span class="ii">i</span>)²<br>
      = 9 − <span class="hi">i²</span><br>
      = 9 − (<span class="hi">−1</span>)<br>
      = <b>10</b> &nbsp;← 켤레끼리 곱하면 항상 실수!`
  },
  {
    expr: '(1+2<span class="ii">i</span>)² = ?',
    choices: [
      '−3+4<span class="ii">i</span>',
      '1+4<span class="ii">i</span>',
      '3+4<span class="ii">i</span>',
      '−3−4<span class="ii">i</span>'
    ],
    correct: 0,
    solution: `
      (1+2<span class="ii">i</span>)² = 1² + 2·1·2<span class="ii">i</span> + (2<span class="ii">i</span>)²<br>
      = 1 + 4<span class="ii">i</span> + 4<span class="hi">i²</span><br>
      = 1 + 4<span class="ii">i</span> + 4×<span class="hi">(−1)</span><br>
      = <b>−3+4<span class="ii">i</span></b>`
  },
  {
    expr: '(<span class="re">2</span>+<span class="im">3</span><span class="ii">i</span>)(<span class="re">2</span>−<span class="im">3</span><span class="ii">i</span>) = ?',
    choices: [
      '4',
      '13',
      '−5',
      '13<span class="ii">i</span>'
    ],
    correct: 1,
    solution: `
      합차공식 적용: <span class="re">2²</span> + <span class="im">3²</span><br>
      = 4 + 9 = <b>13</b><br>
      일반식: (<span class="re">a</span>+<span class="im">b</span><span class="ii">i</span>)(<span class="re">a</span>−<span class="im">b</span><span class="ii">i</span>) = <span class="re">a²</span>+<span class="im">b²</span> → 항상 실수!`
  },
  {
    expr: '<span class="ii">i</span>·(3−4<span class="ii">i</span>) = ?',
    choices: [
      '3<span class="ii">i</span>−4<span class="ii">i</span>',
      '−4+3<span class="ii">i</span>',
      '4+3<span class="ii">i</span>',
      '3−4<span class="ii">i</span>'
    ],
    correct: 2,
    solution: `
      <span class="ii">i</span>·3 + <span class="ii">i</span>·(−4<span class="ii">i</span>)<br>
      = 3<span class="ii">i</span> − 4<span class="hi">i²</span><br>
      = 3<span class="ii">i</span> − 4×<span class="hi">(−1)</span><br>
      = <b>4+3<span class="ii">i</span></b>`
  },
];

// Phase 3: 켤레·나눗셈 (5문제)
const P3 = [
  {
    qtype: 'conjugate',
    expr: '3+4<span class="ii">i</span> 의 켤레복소수는?',
    choices: [
      '−3+4<span class="ii">i</span>',
      '4+3<span class="ii">i</span>',
      '−3−4<span class="ii">i</span>',
      '3−4<span class="ii">i</span>'
    ],
    correct: 3,
    solution: `
      <span class="re">a</span>+<span class="im">b</span><span class="ii">i</span> 의 켤레 = <span class="re">a</span>−<span class="im">b</span><span class="ii">i</span><br>
      3+4<span class="ii">i</span> → 허수부분 부호만 바꾸면<br>
      켤레복소수 = <b>3−4<span class="ii">i</span></b>`
  },
  {
    qtype: 'conjugate',
    expr: '5<span class="ii">i</span> 의 켤레복소수는?',
    choices: [
      '−5<span class="ii">i</span>',
      '5<span class="ii">i</span>',
      '5',
      '−5'
    ],
    correct: 0,
    solution: `
      5<span class="ii">i</span> = 0 + 5<span class="ii">i</span> &nbsp;→&nbsp; 실수부분=0, 허수부분=5<br>
      켤레 = 0 − 5<span class="ii">i</span> = <b>−5<span class="ii">i</span></b><br>
      순허수의 켤레도 순허수예요!`
  },
  {
    qtype: 'division',
    expr: '<div style="display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle"><span>2+4<span class="ii">i</span></span><div style="width:100%;height:2px;background:#c084fc;margin:2px 0"></div><span>1+<span class="ii">i</span></span></div> = ?',
    choices: [
      '3−<span class="ii">i</span>',
      '3+<span class="ii">i</span>',
      '6+2<span class="ii">i</span>',
      '2+4<span class="ii">i</span>'
    ],
    correct: 1,
    solution: `
      분모의 켤레 <b>(1−<span class="ii">i</span>)</b> 를 분자·분모에 곱함<br>
      분자: (2+4<span class="ii">i</span>)(1−<span class="ii">i</span>)<br>
      &nbsp;&nbsp;&nbsp;= 2−2<span class="ii">i</span>+4<span class="ii">i</span>−4<span class="hi">i²</span><br>
      &nbsp;&nbsp;&nbsp;= 2+2<span class="ii">i</span>+4 = <b>6+2<span class="ii">i</span></b><br>
      분모: (1+<span class="ii">i</span>)(1−<span class="ii">i</span>) = 1+1 = <b>2</b><br>
      ∴ (6+2<span class="ii">i</span>)÷2 = <b>3+<span class="ii">i</span></b>`
  },
  {
    qtype: 'division',
    expr: '<div style="display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle"><span>1+<span class="ii">i</span></span><div style="width:100%;height:2px;background:#c084fc;margin:2px 0"></div><span>1−<span class="ii">i</span></span></div> = ?',
    choices: [
      '1',
      '−<span class="ii">i</span>',
      '<span class="ii">i</span>',
      '2<span class="ii">i</span>'
    ],
    correct: 2,
    solution: `
      분모의 켤레 <b>(1+<span class="ii">i</span>)</b> 를 곱함<br>
      분자: (1+<span class="ii">i</span>)² = 1+2<span class="ii">i</span>+<span class="hi">i²</span> = 1+2<span class="ii">i</span>−1 = <b>2<span class="ii">i</span></b><br>
      분모: (1−<span class="ii">i</span>)(1+<span class="ii">i</span>) = 1²+1² = <b>2</b><br>
      ∴ 2<span class="ii">i</span> ÷ 2 = <b><span class="ii">i</span></b>`
  },
  {
    qtype: 'division',
    expr: '<div style="display:inline-flex;flex-direction:column;align-items:center;vertical-align:middle"><span>3+<span class="ii">i</span></span><div style="width:100%;height:2px;background:#c084fc;margin:2px 0"></div><span>2−<span class="ii">i</span></span></div> = ?',
    choices: [
      '1−<span class="ii">i</span>',
      '3+<span class="ii">i</span>',
      '5+5<span class="ii">i</span>',
      '1+<span class="ii">i</span>'
    ],
    correct: 3,
    solution: `
      분모의 켤레 <b>(2+<span class="ii">i</span>)</b> 를 곱함<br>
      분자: (3+<span class="ii">i</span>)(2+<span class="ii">i</span>)<br>
      &nbsp;&nbsp;&nbsp;= 6+3<span class="ii">i</span>+2<span class="ii">i</span>+<span class="hi">i²</span><br>
      &nbsp;&nbsp;&nbsp;= 6+5<span class="ii">i</span>−1 = <b>5+5<span class="ii">i</span></b><br>
      분모: (2−<span class="ii">i</span>)(2+<span class="ii">i</span>) = 4+1 = <b>5</b><br>
      ∴ (5+5<span class="ii">i</span>)÷5 = <b>1+<span class="ii">i</span></b>`
  },
];

// ── 단계별 공식 카드 텍스트 ─────────────────────────────────────────────────
const FORMULA_CARDS = {
  1: '➕ <b>덧셈</b>: (<span class="re">a</span>+<span class="im">b</span><span class="ii">i</span>) + (<span class="re">c</span>+<span class="im">d</span><span class="ii">i</span>) = <span class="re">(a+c)</span> + <span class="im">(b+d)</span><span class="ii">i</span><br>➖ <b>뺄셈</b>: (<span class="re">a</span>+<span class="im">b</span><span class="ii">i</span>) − (<span class="re">c</span>+<span class="im">d</span><span class="ii">i</span>) = <span class="re">(a−c)</span> + <span class="im">(b−d)</span><span class="ii">i</span>',
  2: '✖️ <b>곱셈</b>: (<span class="re">a</span>+<span class="im">b</span><span class="ii">i</span>)(<span class="re">c</span>+<span class="im">d</span><span class="ii">i</span>) = <span class="re">(ac−bd)</span> + <span class="im">(ad+bc)</span><span class="ii">i</span><br>⚠️ 핵심: <span class="hi">i²= −1</span> 적용! &nbsp;(다항식 展開 + i²=−1)',
  3: '🔗 <b>켤레</b>: <span class="re">a</span>+<span class="im">b</span><span class="ii">i</span> 의 켤레 = <span class="re">a</span>−<span class="im">b</span><span class="ii">i</span><br>➗ <b>나눗셈</b>: 분모×켤레 → 분모 실수화 &nbsp; (<span class="re">a</span>+<span class="im">b</span><span class="ii">i</span>)(<span class="re">a</span>−<span class="im">b</span><span class="ii">i</span>) = <span class="re">a²</span>+<span class="im">b²</span>',
};

// ── Break 화면 데이터 ──────────────────────────────────────────────────────
const BREAKS = {
  after1: {
    icon: '✖️',
    title: 'Phase 1 클리어! 이제 곱셈이다!',
    html: `<b>복소수 곱셈의 핵심</b>은 <span class="hi">i² = −1</span> 을 잊지 않는 것!<br><br>
      (a+b<span class="ii">i</span>)(c+d<span class="ii">i</span>) 전개 시:<br>
      &nbsp;ac + ad<span class="ii">i</span> + bc<span class="ii">i</span> + bd<span class="hi">i²</span><br>
      = ac + (ad+bc)<span class="ii">i</span> + bd×<span class="hi">(−1)</span><br>
      = <span class="re">(ac−bd)</span> + <span class="im">(ad+bc)</span><span class="ii">i</span><br><br>
      실수부분에서 <b>bd가 빠지는 것</b>이 다항식 곱셈과의 차이점!`
  },
  after2: {
    icon: '🔗',
    title: 'Phase 2 클리어! 마지막 단계!',
    html: `<b>복소수 나눗셈</b>은 <b>켤레복소수</b>가 핵심!<br><br>
      <span class="re">a</span>+<span class="im">b</span><span class="ii">i</span> 의 켤레복소수 = <span class="re">a</span>−<span class="im">b</span><span class="ii">i</span><br><br>
      왜 켤레를 곱하나? → 분모를 <b>실수</b>로 만들기 위해!<br>
      (<span class="re">a</span>+<span class="im">b</span><span class="ii">i</span>)(<span class="re">a</span>−<span class="im">b</span><span class="ii">i</span>) = <span class="re">a²</span> + <span class="im">b²</span> &nbsp;← 항상 실수!<br><br>
      이건 무리수 분모의 유리화와 같은 원리예요!<br>
      <span style="color:#fcd34d">√2 분모 유리화</span>: ×√2/√2 &nbsp;→&nbsp; <span style="color:#fcd34d">복소수 나눗셈</span>: ×켤레/켤레`
  }
};

// ── 상태 변수 ──────────────────────────────────────────────────────────────
let phase = 0;
let qIdx  = 0;
let score = 0;
let answered = false;
const MAX_SCORE = 150;

function currentData(){
  if(phase === 1) return P1[qIdx];
  if(phase === 2) return P2[qIdx];
  return P3[qIdx];
}
function currentTotal(){
  if(phase === 1) return P1.length;
  if(phase === 2) return P2.length;
  return P3.length;
}

// ── 화면 전환 ──────────────────────────────────────────────────────────────
function showScreen(id){
  document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
}

// ── 게임 시작 ──────────────────────────────────────────────────────────────
function startGame(){
  phase = 1; qIdx = 0; score = 0;
  document.getElementById('scoreDisp').textContent = score;
  showScreen('gameScreen');
  loadQuestion();
}

function startNextPhase(){
  phase++;
  qIdx = 0;
  showScreen('gameScreen');
  loadQuestion();
}

function restartGame(){
  showScreen('introScreen');
}

// ── 문제 로드 ──────────────────────────────────────────────────────────────
function loadQuestion(){
  answered = false;
  document.getElementById('feedbackBox').className = 'feedback hidden';
  document.getElementById('nextBtn').style.display = 'none';

  const data  = currentData();
  const total = currentTotal();

  // 탑바
  const phaseNames = {1:'Phase 1 · 덧셈&뺄셈', 2:'Phase 2 · 곱셈', 3:'Phase 3 · 켤레&나눗셈'};
  document.getElementById('phaseBadge').innerHTML = phaseNames[phase];

  // 진행 바
  document.getElementById('progFill').style.width  = (qIdx / total * 100) + '%';
  document.getElementById('progLabel').textContent = (qIdx + 1) + ' / ' + total;

  // 공식 카드
  document.getElementById('formulaCard').innerHTML = FORMULA_CARDS[phase];

  // 문제
  const typeLabel = phase === 3
    ? (data.qtype === 'conjugate' ? '켤레복소수 찾기' : '나눗셈 계산')
    : (phase === 1 ? '덧셈·뺄셈 계산' : '곱셈 계산');
  document.getElementById('qTypeLabel').textContent = typeLabel;
  document.getElementById('complexExpr').innerHTML  = data.expr;
  document.getElementById('qSub').textContent = '';

  // 선택지 렌더링
  renderChoices(data.choices, data.correct);
}

// ── 선택지 렌더링 ──────────────────────────────────────────────────────────
function renderChoices(choices, correct){
  const labels = ['A', 'B', 'C', 'D'];
  const grid   = document.getElementById('choicesGrid');
  grid.innerHTML = '';

  choices.forEach((text, idx) => {
    const btn = document.createElement('button');
    btn.className = 'choice-btn';
    btn.innerHTML = `<span class="choice-inner"><span class="choice-label">${labels[idx]}</span><span>${text}</span></span>`;
    btn.onclick = () => answerChoice(idx, correct, choices);
    grid.appendChild(btn);
  });
}

// ── 정답 처리 ──────────────────────────────────────────────────────────────
function answerChoice(chosen, correct, choices){
  if(answered) return;
  answered = true;

  const btns = document.querySelectorAll('#choicesGrid .choice-btn');
  btns.forEach(b => b.disabled = true);
  btns[chosen].classList.add(chosen === correct ? 'correct' : 'wrong');
  if(chosen !== correct) btns[correct].classList.add('correct');

  if(chosen === correct){
    score += 10;
    document.getElementById('scoreDisp').textContent = score;
  }

  // 피드백
  const data = currentData();
  const fb   = document.getElementById('feedbackBox');
  fb.className = 'feedback ' + (chosen === correct ? 'correct' : 'wrong');
  fb.innerHTML = (chosen === correct ? '✅ 정답! ' : '❌ 틀렸어요! ') +
    '<div class="sol-steps">' + data.solution + '</div>';

  document.getElementById('nextBtn').style.display = 'block';
}

// ── 다음 문제 ──────────────────────────────────────────────────────────────
function nextQuestion(){
  qIdx++;
  const total = currentTotal();

  if(qIdx >= total){
    // 단계 완료
    if(phase === 1){
      showBreak('after1');
    } else if(phase === 2){
      showBreak('after2');
    } else {
      showResult();
    }
  } else {
    loadQuestion();
  }
}

// ── Break 화면 ─────────────────────────────────────────────────────────────
function showBreak(key){
  const b = BREAKS[key];
  document.getElementById('breakIcon').textContent  = b.icon;
  document.getElementById('breakTitle').textContent = b.title;
  document.getElementById('breakFormula').innerHTML = b.html;
  showScreen('breakScreen');
}

// ── 결과 화면 ──────────────────────────────────────────────────────────────
function showResult(){
  const pct = score / MAX_SCORE;
  let emoji, msg;
  if(pct >= 0.93){
    emoji = '🏆'; msg = '완벽합니다! 복소수 사칙연산을 완전히 마스터했어요! 다항식처럼 전개하면서 i²=−1만 잊지 않으면 돼요!';
  } else if(pct >= 0.73){
    emoji = '⭐'; msg = '훌륭해요! 대부분의 문제를 풀었네요. 틀린 문제의 풀이 과정을 다시 한번 살펴보세요.';
  } else if(pct >= 0.53){
    emoji = '💪'; msg = '좋은 시작입니다! 특히 곱셈에서 i²=−1 적용, 나눗셈에서 켤레 곱하기를 다시 연습해 보세요.';
  } else {
    emoji = '🌱'; msg = '괜찮아요! 복소수 연산의 핵심은 ① i²=−1 ② 나눗셈=켤레로 분모 실수화예요. 다시 도전해 봐요!';
  }

  document.getElementById('resultEmoji').textContent = emoji;
  document.getElementById('resultScore').textContent = score + '점';
  document.getElementById('resultMsg').textContent   = msg;

  showScreen('resultScreen');
  setTimeout(() => {
    document.getElementById('resultBarFill').style.width = (pct * 100) + '%';
  }, 100);
}
</script>
</body>
</html>
"""


def render():
    st.markdown("## ⚡ 복소수 계산 배틀!")
    st.markdown(
        "덧셈·뺄셈 → 곱셈 → 켤레·나눗셈의 3단계 게임으로 "
        "복소수 사칙연산을 완전히 정복해 봅시다!"
    )
    components.html(_GAME_HTML, height=920, scrolling=True)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
