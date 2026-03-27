# activities/common/mini/negative_sqrt_trap.py
"""
음수의 제곱근 함정 탈출!
'a의 제곱근'과 '√a'의 차이, 음수 포함 제곱근의 곱셈·나눗셈 성질을
카드 뒤집기·단계별 탐구·오답 찾기·도전 문제로 재미있게 익히는 미니활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "음수제곱근탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key":    "용어구분",
        "label":  "'-4의 제곱근'과 '√(-4)'의 차이를 설명하고, 각각의 값을 구하세요.",
        "type":   "text_area",
        "height": 90,
    },
    {
        "key":    "함정설명",
        "label":  "√(-2) × √(-3) = √6 이라는 계산이 왜 틀렸는지 설명하고, 올바른 계산 과정을 쓰세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "규칙정리",
        "label":  "a < 0, b < 0일 때 √a·√b = -√(ab)가 성립하는 이유를, i를 이용한 변환 과정으로 설명하세요.",
        "type":   "text_area",
        "height": 100,
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
    "title":       "🚨 음수의 제곱근 함정 탈출!",
    "description": "'a의 제곱근'과 '√a'의 차이, 음수 포함 제곱근 곱셈·나눗셈의 올바른 계산법을 오답 찾기·단계별 탐구로 익히는 활동입니다.",
    "order":       204,
    "hidden":      False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>음수의 제곱근 함정 탈출</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI','Malgun Gothic',system-ui,sans-serif;
  background:linear-gradient(155deg,#0d0b1e 0%,#1a0f3d 50%,#0d1225 100%);
  color:#e2e8f0;min-height:100vh;padding:14px 12px 24px;
  overflow-x:hidden;
}
.shell{max-width:880px;margin:0 auto}

/* Hero */
.hero{
  position:relative;overflow:hidden;
  background:linear-gradient(135deg,rgba(220,38,38,.18),rgba(124,58,237,.14));
  border:1px solid rgba(248,113,113,.35);border-radius:18px;
  padding:16px 20px 14px;margin-bottom:14px;text-align:center;
}
.hero::before{
  content:'!';position:absolute;right:14px;top:-10px;
  font-size:140px;font-weight:900;color:rgba(248,113,113,.06);
  pointer-events:none;line-height:1;
}
.hero>*{position:relative;z-index:1}
.hero h1{font-size:1.45rem;color:#f87171;margin-bottom:4px;font-weight:800}
.hero p{font-size:.83rem;color:#fca5a5;opacity:.85}

/* Tabs */
.tabs{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap}
.tab-btn{
  flex:1;min-width:110px;padding:8px 6px;font-size:.8rem;font-weight:700;
  background:rgba(255,255,255,.05);border:1.5px solid rgba(255,255,255,.12);
  border-radius:10px;color:#c4b5fd;cursor:pointer;transition:all .2s;text-align:center;
}
.tab-btn.active{background:rgba(220,38,38,.25);border-color:#ef4444;color:#fff}
.tab-btn:hover:not(.active){background:rgba(255,255,255,.1)}

.tab-panel{display:none;animation:fadeIn .3s ease}
.tab-panel.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

/* Section */
.sec{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:14px;padding:14px 16px;margin-bottom:12px;
}
.sec-title{
  font-size:.98rem;font-weight:700;color:#a78bfa;margin-bottom:10px;
  display:flex;align-items:center;gap:6px;
}

/* Info boxes */
.formula-box{
  background:rgba(124,58,237,.12);border:1.5px solid rgba(124,58,237,.4);
  border-radius:10px;padding:11px 15px;margin:8px 0;font-size:.93rem;
  text-align:center;color:#ddd6fe;font-weight:600;line-height:1.6;
}
.formula-box .sub{font-size:.76rem;color:#a78bfa;margin-top:4px;font-weight:400}
.danger-box{
  background:rgba(220,38,38,.1);border:1.5px solid rgba(239,68,68,.4);
  border-radius:10px;padding:11px 15px;margin:8px 0;color:#fca5a5;font-size:.88rem;
  line-height:1.5;
}
.danger-box .title{font-weight:700;color:#f87171;margin-bottom:4px;font-size:.85rem}
.safe-box{
  background:rgba(34,197,94,.08);border:1.5px solid rgba(34,197,94,.35);
  border-radius:10px;padding:11px 15px;margin:8px 0;color:#86efac;font-size:.88rem;
  text-align:center;
}
.safe-box .title{font-weight:700;color:#4ade80;margin-bottom:4px;font-size:.85rem}
.warn-box{
  background:rgba(251,191,36,.08);border:1.5px solid rgba(251,191,36,.35);
  border-radius:10px;padding:11px 15px;margin:8px 0;color:#fde68a;font-size:.88rem;
  line-height:1.5;
}
.warn-box .title{font-weight:700;color:#fbbf24;margin-bottom:4px;font-size:.85rem}

/* ── Tab 1: Flip Cards ── */
.card-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:10px;margin:10px 0}
.flip-card{height:115px;perspective:600px;cursor:pointer}
.flip-card-inner{
  position:relative;width:100%;height:100%;
  transition:transform .45s;transform-style:preserve-3d;
}
.flip-card.flipped .flip-card-inner{transform:rotateY(180deg)}
.flip-front,.flip-back{
  position:absolute;width:100%;height:100%;backface-visibility:hidden;
  border-radius:12px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;padding:10px;text-align:center;
}
.flip-front{
  background:rgba(124,58,237,.2);border:1.5px solid rgba(124,58,237,.45);
  color:#c4b5fd;font-size:1rem;font-weight:700;
}
.flip-front .hint{font-size:.7rem;color:#8b5cf6;margin-top:6px}
.flip-back{
  background:rgba(34,197,94,.15);border:1.5px solid rgba(34,197,94,.45);
  transform:rotateY(180deg);
}
.flip-back .answer{font-size:1.05rem;font-weight:700;color:#4ade80}
.flip-back .reason{font-size:.72rem;color:#86efac;margin-top:5px;line-height:1.4}

/* Tab 1 quiz */
.quiz-block{margin:10px 0;padding:10px;background:rgba(255,255,255,.03);border-radius:10px;border:1px solid rgba(255,255,255,.08)}
.quiz-q{font-size:.9rem;color:#e2e8f0;margin-bottom:8px;font-weight:600}
.quiz-options{display:flex;gap:7px;flex-wrap:wrap}
.qbtn{
  padding:7px 14px;border-radius:8px;font-size:.83rem;font-weight:600;cursor:pointer;
  border:1.5px solid rgba(255,255,255,.2);background:rgba(255,255,255,.06);
  color:#c4b5fd;transition:all .15s;
}
.qbtn:hover:not(:disabled){background:rgba(255,255,255,.12)}
.qbtn.correct{background:rgba(34,197,94,.2)!important;border-color:#4ade80!important;color:#4ade80!important}
.qbtn.wrong{background:rgba(239,68,68,.2)!important;border-color:#f87171!important;color:#f87171!important}
.qbtn:disabled{cursor:default}
.quiz-feedback{margin-top:7px;font-size:.8rem;min-height:18px;font-weight:600;line-height:1.4}

/* ── Tab 2: Step reveal ── */
.prob-header{font-size:.93rem;font-weight:700;color:#fbbf24;margin-bottom:10px}
.wrong-calc{
  background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.3);
  border-radius:8px;padding:8px 12px;margin-bottom:10px;font-size:.85rem;color:#fca5a5;
}
.wrong-calc .label{font-size:.72rem;color:#f87171;font-weight:700;margin-bottom:3px}
.steps-list{display:flex;flex-direction:column;gap:5px;margin-bottom:10px}
.step-item{
  display:flex;align-items:flex-start;gap:10px;padding:10px 12px;
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);
  border-radius:10px;opacity:.3;transition:all .4s;
}
.step-item.show{opacity:1;background:rgba(124,58,237,.1);border-color:rgba(124,58,237,.3)}
.step-num{
  width:24px;height:24px;border-radius:50%;background:rgba(124,58,237,.3);
  color:#c4b5fd;font-size:.72rem;font-weight:700;display:flex;align-items:center;
  justify-content:center;flex-shrink:0;margin-top:1px;
}
.step-body{flex:1}
.step-eq{font-size:.87rem;color:#e2e8f0;font-weight:600;line-height:1.5}
.step-eq em{color:#a78bfa;font-style:normal}
.step-why{font-size:.74rem;color:#94a3b8;display:block;margin-top:2px;line-height:1.4}
.step-final{font-size:.9rem;font-weight:700;color:#4ade80}
.reveal-btn{
  padding:7px 18px;border-radius:8px;font-size:.83rem;font-weight:700;
  background:linear-gradient(135deg,#7c3aed,#6d28d9);border:none;color:#fff;
  cursor:pointer;transition:all .2s;
}
.reveal-btn:hover:not(:disabled){background:linear-gradient(135deg,#6d28d9,#5b21b6)}
.reveal-btn:disabled{opacity:.5;cursor:default}

/* ── Tab 3: 오답 찾기 ── */
.hyunmin-guide{
  background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.3);
  border-radius:10px;padding:10px 14px;margin-bottom:12px;font-size:.83rem;color:#fde68a;line-height:1.5;
}
.hyunmin-card{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.12);
  border-radius:12px;padding:13px;margin-bottom:10px;
}
.hyunmin-card .card-title{font-size:.82rem;font-weight:700;color:#94a3b8;margin-bottom:10px}
.calc-step{
  display:flex;align-items:center;gap:10px;padding:9px 12px;
  border:1.5px solid transparent;border-radius:9px;cursor:pointer;
  transition:all .18s;margin-bottom:5px;
}
.calc-step:hover{background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.15)}
.calc-step.locked{cursor:default}
.calc-step.flash-wrong{animation:shake .35s ease}
.calc-step.highlight-wrong{background:rgba(239,68,68,.15);border-color:#ef4444}
.calc-step.highlight-ok{background:rgba(34,197,94,.1);border-color:#22c55e}
@keyframes shake{
  0%,100%{transform:translateX(0)}20%,60%{transform:translateX(-6px)}40%,80%{transform:translateX(6px)}
}
.calc-icon{font-size:.9rem;width:22px;text-align:center;flex-shrink:0}
.calc-eq{font-size:.88rem;color:#ddd6fe;flex:1;font-weight:500}
.hyunmin-result{
  margin-top:8px;padding:9px 12px;border-radius:9px;font-size:.82rem;
  display:none;line-height:1.5;
}
.hyunmin-result.show{display:block}
.hyunmin-result.ok{background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.3);color:#86efac}
.hyunmin-result.fail{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.3);color:#fca5a5}
.progress-bar{
  display:flex;gap:6px;margin-bottom:12px;
}
.prog-dot{
  width:12px;height:12px;border-radius:50%;background:rgba(255,255,255,.15);
  transition:all .3s;
}
.prog-dot.done{background:#4ade80}
.solutions{
  background:rgba(124,58,237,.08);border:1px solid rgba(124,58,237,.3);
  border-radius:12px;padding:14px;margin-top:4px;display:none;
}
.solutions.show{display:block}
.sol-title{font-size:.9rem;font-weight:700;color:#a78bfa;margin-bottom:10px}
.sol-item{margin-bottom:12px}
.sol-item .sol-num{font-size:.8rem;font-weight:700;color:#fbbf24;margin-bottom:5px}
.sol-box{
  background:rgba(124,58,237,.12);border:1px solid rgba(124,58,237,.3);
  border-radius:8px;padding:8px 14px;font-size:.88rem;color:#ddd6fe;font-weight:600;
  text-align:center;line-height:1.7;
}
.sol-note{font-size:.76rem;color:#94a3b8;margin-top:4px;line-height:1.4}

/* ── Tab 4: Challenge ── */
.score-bar{
  display:flex;align-items:center;justify-content:space-between;
  background:rgba(124,58,237,.12);border:1px solid rgba(124,58,237,.3);
  border-radius:10px;padding:9px 16px;margin-bottom:12px;
}
.score-label{font-size:.83rem;color:#c4b5fd}
.score-val{font-size:1.05rem;font-weight:700;color:#a78bfa}
.challenge-q{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:12px;padding:13px;margin-bottom:10px;
}
.q-num{font-size:.76rem;color:#94a3b8;font-weight:700;margin-bottom:3px}
.q-text{font-size:.92rem;color:#e2e8f0;font-weight:600;margin-bottom:9px;line-height:1.5}
.q-options{display:flex;flex-direction:column;gap:5px}
.qopt{
  padding:8px 13px;border-radius:8px;font-size:.86rem;cursor:pointer;
  border:1.5px solid rgba(255,255,255,.14);background:rgba(255,255,255,.05);
  color:#c4b5fd;transition:all .15s;text-align:left;
}
.qopt:hover:not(:disabled){background:rgba(124,58,237,.15);border-color:rgba(124,58,237,.4)}
.qopt.correct{background:rgba(34,197,94,.15)!important;border-color:#4ade80!important;color:#4ade80!important}
.qopt.wrong{background:rgba(239,68,68,.15)!important;border-color:#f87171!important;color:#f87171!important}
.qopt:disabled{cursor:default}
.q-fb{font-size:.78rem;margin-top:6px;min-height:16px;font-weight:600;line-height:1.4}

/* Complete */
.complete{
  text-align:center;padding:18px;
  background:rgba(34,197,94,.08);border:1.5px solid rgba(34,197,94,.3);
  border-radius:14px;margin-top:10px;display:none;
}
.complete.show{display:block;animation:fadeIn .5s ease}
.complete-title{font-size:1.1rem;font-weight:700;color:#4ade80;margin-bottom:6px}
.complete-msg{font-size:.85rem;color:#86efac}

::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(124,58,237,.5);border-radius:3px}
</style>
</head>
<body>
<div class="shell">

<!-- Hero -->
<div class="hero">
  <h1>🚨 음수의 제곱근 함정 탈출!</h1>
  <p>'a의 제곱근'과 '√a'의 차이, 음수 포함 제곱근 계산의 함정을 정복하세요</p>
</div>

<!-- Tabs -->
<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('t1',this)">📚 용어 구분</button>
  <button class="tab-btn" onclick="switchTab('t2',this)">🔍 함정 탐구</button>
  <button class="tab-btn" onclick="switchTab('t3',this)">🔎 오답 찾기</button>
  <button class="tab-btn" onclick="switchTab('t4',this)">🏆 도전 문제</button>
</div>

<!-- ═══════════════════════ TAB 1: 용어 구분 ═══════════════════════ -->
<div class="tab-panel active" id="tab-t1">
  <div class="sec">
    <div class="sec-title">📌 핵심 개념 비교</div>
    <div class="formula-box">
      <strong>a의 제곱근</strong> → x² = a 를 만족하는 <em style="color:#f87171">모든</em> x의 값
      <div class="sub">-4의 제곱근: x² = -4 &nbsp;⟹&nbsp; x = 2i 또는 x = -2i &nbsp;<strong>(두 개)</strong></div>
    </div>
    <div class="formula-box">
      <strong>√a &nbsp;(제곱근 a)</strong> → a의 제곱근 중 정해진 <em style="color:#f87171">하나</em>의 값
      <div class="sub">√(-4) = 2i &nbsp;&nbsp;(단, a &lt; 0이면 √(-a)·i 로 변환) &nbsp;<strong>(하나)</strong></div>
    </div>
    <div class="danger-box">
      <div class="title">⚠️ 혼동 주의!</div>
      <strong>-9의 제곱근</strong>은 3i 와 -3i <strong>(두 개)</strong><br>
      <strong>√(-9)</strong> = 3i &nbsp;<strong>(하나, -3i가 아님)</strong>
    </div>
  </div>

  <div class="sec">
    <div class="sec-title">🃏 카드 뒤집기 – 클릭하여 답 확인</div>
    <div class="card-grid">
      <div class="flip-card" onclick="this.classList.toggle('flipped')">
        <div class="flip-card-inner">
          <div class="flip-front">-9의 제곱근<div class="hint">👆 클릭해서 확인</div></div>
          <div class="flip-back"><div class="answer">+3i 와 -3i</div><div class="reason">x²=-9 → x=±3i<br>(두 개의 허수)</div></div>
        </div>
      </div>
      <div class="flip-card" onclick="this.classList.toggle('flipped')">
        <div class="flip-card-inner">
          <div class="flip-front">√(-9)<div class="hint">👆 클릭해서 확인</div></div>
          <div class="flip-back"><div class="answer">3i</div><div class="reason">√(-9)=√9·i=3i<br>(하나의 값)</div></div>
        </div>
      </div>
      <div class="flip-card" onclick="this.classList.toggle('flipped')">
        <div class="flip-card-inner">
          <div class="flip-front">-16의 제곱근<div class="hint">👆 클릭해서 확인</div></div>
          <div class="flip-back"><div class="answer">+4i 와 -4i</div><div class="reason">x²=-16 → x=±4i<br>(두 개의 허수)</div></div>
        </div>
      </div>
      <div class="flip-card" onclick="this.classList.toggle('flipped')">
        <div class="flip-card-inner">
          <div class="flip-front">√(-16)<div class="hint">👆 클릭해서 확인</div></div>
          <div class="flip-back"><div class="answer">4i</div><div class="reason">√(-16)=√16·i=4i<br>(하나의 값)</div></div>
        </div>
      </div>
      <div class="flip-card" onclick="this.classList.toggle('flipped')">
        <div class="flip-card-inner">
          <div class="flip-front">-2의 제곱근<div class="hint">👆 클릭해서 확인</div></div>
          <div class="flip-back"><div class="answer">+√2·i 와 -√2·i</div><div class="reason">x²=-2 → x=±√2i<br>(두 개의 허수)</div></div>
        </div>
      </div>
      <div class="flip-card" onclick="this.classList.toggle('flipped')">
        <div class="flip-card-inner">
          <div class="flip-front">√(-6)<div class="hint">👆 클릭해서 확인</div></div>
          <div class="flip-back"><div class="answer">√6·i</div><div class="reason">√(-6)=√6·i<br>(하나의 값)</div></div>
        </div>
      </div>
    </div>
  </div>

  <div class="sec">
    <div class="sec-title">❓ 빠른 확인 퀴즈</div>

    <div class="quiz-block" id="q1">
      <div class="quiz-q">① -25의 제곱근을 모두 고르면?</div>
      <div class="quiz-options">
        <button class="qbtn" onclick="checkQ('q1',this,false)">5</button>
        <button class="qbtn" onclick="checkQ('q1',this,false)">5i</button>
        <button class="qbtn" onclick="checkQ('q1',this,true)">5i 와 -5i</button>
        <button class="qbtn" onclick="checkQ('q1',this,false)">-5i</button>
      </div>
      <div class="quiz-feedback" id="q1-fb"></div>
    </div>

    <div class="quiz-block" id="q2" style="margin-top:10px">
      <div class="quiz-q">② √(-25) 의 값은?</div>
      <div class="quiz-options">
        <button class="qbtn" onclick="checkQ('q2',this,false)">5</button>
        <button class="qbtn" onclick="checkQ('q2',this,true)">5i</button>
        <button class="qbtn" onclick="checkQ('q2',this,false)">±5i</button>
        <button class="qbtn" onclick="checkQ('q2',this,false)">-5i</button>
      </div>
      <div class="quiz-feedback" id="q2-fb"></div>
    </div>

    <div class="quiz-block" id="q3" style="margin-top:10px">
      <div class="quiz-q">③ '-3의 제곱근'과 '√(-3)'은 같은가?</div>
      <div class="quiz-options">
        <button class="qbtn" onclick="checkQ('q3',this,false)">같다 — 둘 다 √3·i</button>
        <button class="qbtn" onclick="checkQ('q3',this,true)">다르다 — 개수가 다름</button>
        <button class="qbtn" onclick="checkQ('q3',this,false)">음수라서 둘 다 없다</button>
      </div>
      <div class="quiz-feedback" id="q3-fb"></div>
    </div>
  </div>
</div>

<!-- ═══════════════════════ TAB 2: 함정 탐구 ═══════════════════════ -->
<div class="tab-panel" id="tab-t2">
  <div class="sec">
    <div class="sec-title">⚠️ 공식 사용의 조건!</div>
    <div class="safe-box">
      <div class="title">✅ a &gt; 0, b &gt; 0일 때만 성립</div>
      √a · √b = √(ab) &nbsp;&nbsp;&nbsp;&nbsp; √a / √b = √(a/b)
    </div>
    <div class="danger-box">
      <div class="title">❌ a &lt; 0 또는 b &lt; 0이면 위 공식 직접 사용 금지!</div>
      반드시 <strong>√(-a) = √a · i</strong> 로 변환한 뒤 계산해야 합니다.
    </div>
    <div class="warn-box">
      <div class="title">📐 음수 포함 시 성립하는 공식</div>
      <strong>a &lt; 0, b &lt; 0이면</strong> &nbsp; √a · √b = <strong>-√(ab)</strong> &nbsp; (부호 뒤집힘!)<br>
      <strong>a &gt; 0, b &lt; 0이면</strong> &nbsp; √a / √b = <strong>-√(a/b)</strong> &nbsp; (부호 뒤집힘!)
    </div>
  </div>

  <!-- 탐구 1 -->
  <div class="sec">
    <div class="sec-title">🔬 단계별 탐구 ①&nbsp; √(-4) × √(-9) = ?</div>
    <div class="wrong-calc">
      <div class="label">⛔ 잘못된 계산</div>
      √(-4) × √(-9) = √{(-4)×(-9)} = √36 = 6 &nbsp;← a,b &lt; 0인데 공식 그대로 사용!
    </div>
    <div class="steps-list" id="sl1">
      <div class="step-item" id="s1-1">
        <div class="step-num">1</div>
        <div class="step-body">
          <div class="step-eq">√(-4) = √4 · i = <em>2i</em></div>
          <span class="step-why">√(-a) = √a · i (a &gt; 0) 규칙 적용</span>
        </div>
      </div>
      <div class="step-item" id="s1-2">
        <div class="step-num">2</div>
        <div class="step-body">
          <div class="step-eq">√(-9) = √9 · i = <em>3i</em></div>
          <span class="step-why">마찬가지로 변환</span>
        </div>
      </div>
      <div class="step-item" id="s1-3">
        <div class="step-num">3</div>
        <div class="step-body">
          <div class="step-eq">2i × 3i = <em>6i²</em></div>
          <span class="step-why">실수끼리, i끼리 묶어 계산</span>
        </div>
      </div>
      <div class="step-item" id="s1-4">
        <div class="step-num">4</div>
        <div class="step-body">
          <div class="step-eq step-final">6i² = 6 × (-1) = -6 ✓</div>
          <span class="step-why">i² = -1 대입. 정답은 6이 아닌 <strong style="color:#4ade80">-6</strong>!</span>
        </div>
      </div>
    </div>
    <button class="reveal-btn" id="rb1" onclick="revealStep(1)">▶ 다음 단계 보기</button>
  </div>

  <!-- 탐구 2 -->
  <div class="sec">
    <div class="sec-title">🔬 단계별 탐구 ②&nbsp; √8 / √(-4) = ?</div>
    <div class="wrong-calc">
      <div class="label">⛔ 잘못된 계산</div>
      √8 / √(-4) = √{8/(-4)} = √(-2) = √2·i &nbsp;← b &lt; 0인데 공식 그대로 사용!
    </div>
    <div class="steps-list" id="sl2">
      <div class="step-item" id="s2-1">
        <div class="step-num">1</div>
        <div class="step-body">
          <div class="step-eq">√8 = 2√2, &nbsp; √(-4) = <em>2i</em></div>
          <span class="step-why">각각 변환하여 준비</span>
        </div>
      </div>
      <div class="step-item" id="s2-2">
        <div class="step-num">2</div>
        <div class="step-body">
          <div class="step-eq">2√2 / 2i = <em>√2 / i</em></div>
          <span class="step-why">분자·분모 공약수 2로 약분</span>
        </div>
      </div>
      <div class="step-item" id="s2-3">
        <div class="step-num">3</div>
        <div class="step-body">
          <div class="step-eq">√2 / i = √2·i / (i · i) = <em>√2·i / i²</em></div>
          <span class="step-why">분모 유리화: 분자·분모에 i 곱하기</span>
        </div>
      </div>
      <div class="step-item" id="s2-4">
        <div class="step-num">4</div>
        <div class="step-body">
          <div class="step-eq step-final">√2·i / (-1) = -√2·i ✓</div>
          <span class="step-why">i² = -1. 정답은 √2i가 아닌 <strong style="color:#4ade80">-√2i</strong>!</span>
        </div>
      </div>
    </div>
    <button class="reveal-btn" id="rb2" onclick="revealStep(2)">▶ 다음 단계 보기</button>
  </div>

  <!-- 탐구 3 -->
  <div class="sec">
    <div class="sec-title">🔬 단계별 탐구 ③&nbsp; √(-2) × √(-3) = ?</div>
    <div class="wrong-calc">
      <div class="label">⛔ 잘못된 계산</div>
      √(-2) × √(-3) = √{(-2)×(-3)} = √6 &nbsp;← 음수끼리 공식 그대로 사용!
    </div>
    <div class="steps-list" id="sl3">
      <div class="step-item" id="s3-1">
        <div class="step-num">1</div>
        <div class="step-body">
          <div class="step-eq">√(-2) = √2·i, &nbsp; √(-3) = <em>√3·i</em></div>
          <span class="step-why">각각 i를 이용해 변환</span>
        </div>
      </div>
      <div class="step-item" id="s3-2">
        <div class="step-num">2</div>
        <div class="step-body">
          <div class="step-eq">(√2·i)(√3·i) = <em>√6 · i²</em></div>
          <span class="step-why">실수끼리(√2·√3=√6), i끼리(i·i=i²) 묶기</span>
        </div>
      </div>
      <div class="step-item" id="s3-3">
        <div class="step-num">3</div>
        <div class="step-body">
          <div class="step-eq step-final">√6 · (-1) = -√6 ✓</div>
          <span class="step-why">i² = -1. 정답은 +√6이 아닌 <strong style="color:#4ade80">-√6</strong>!</span>
        </div>
      </div>
    </div>
    <button class="reveal-btn" id="rb3" onclick="revealStep(3)">▶ 다음 단계 보기</button>
  </div>
</div>

<!-- ═══════════════════════ TAB 3: 오답 찾기 ═══════════════════════ -->
<div class="tab-panel" id="tab-t3">
  <div class="sec">
    <div class="sec-title">🔎 잘못된 계산, 네가 찾아라!</div>
    <div class="hyunmin-guide">
      아래 두 계산에는 각각 틀린 단계가 하나씩 있습니다.<br>
      잘못된 계산이 <strong>처음 시작된 단계</strong>를 클릭하여 찾아보세요!<br>
      힌트: 규칙을 잘못 적용한 단계가 어디일까요?
    </div>

    <!-- 진행 상태 -->
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">
      <span style="font-size:.78rem;color:#94a3b8">풀이 진행:</span>
      <div class="progress-bar">
        <div class="prog-dot" id="pd1"></div>
        <div class="prog-dot" id="pd2"></div>
      </div>
    </div>

    <!-- 계산 ① -->
    <div class="hyunmin-card">
      <div class="card-title">① √(-4) × √(-9) 계산</div>
      <div id="hm1-steps">
        <div class="calc-step" id="hm1-s0" onclick="clickStep(1,0,false)">
          <span class="calc-icon">·</span>
          <span class="calc-eq">√(-4) × √(-9)</span>
        </div>
        <div class="calc-step" id="hm1-s1" onclick="clickStep(1,1,true)">
          <span class="calc-icon">·</span>
          <span class="calc-eq">= √{ (-4) × (-9) }</span>
        </div>
        <div class="calc-step" id="hm1-s2" onclick="clickStep(1,2,false)">
          <span class="calc-icon">·</span>
          <span class="calc-eq">= √36</span>
        </div>
        <div class="calc-step" id="hm1-s3" onclick="clickStep(1,3,false)">
          <span class="calc-icon">·</span>
          <span class="calc-eq">= 6</span>
        </div>
      </div>
      <div class="hyunmin-result" id="hm1-result"></div>
    </div>

    <!-- 계산 ② -->
    <div class="hyunmin-card">
      <div class="card-title">② √8 / √(-4) 계산</div>
      <div id="hm2-steps">
        <div class="calc-step" id="hm2-s0" onclick="clickStep(2,0,false)">
          <span class="calc-icon">·</span>
          <span class="calc-eq">√8 / √(-4)</span>
        </div>
        <div class="calc-step" id="hm2-s1" onclick="clickStep(2,1,true)">
          <span class="calc-icon">·</span>
          <span class="calc-eq">= √{ 8 / (-4) }</span>
        </div>
        <div class="calc-step" id="hm2-s2" onclick="clickStep(2,2,false)">
          <span class="calc-icon">·</span>
          <span class="calc-eq">= √(-2)</span>
        </div>
        <div class="calc-step" id="hm2-s3" onclick="clickStep(2,3,false)">
          <span class="calc-icon">·</span>
          <span class="calc-eq">= √2 · i</span>
        </div>
      </div>
      <div class="hyunmin-result" id="hm2-result"></div>
    </div>

    <!-- 올바른 풀이 (두 문제 모두 맞추면 공개) -->
    <div class="solutions" id="solutions">
      <div class="sol-title">✅ 올바른 풀이 공개!</div>
      <div class="sol-item">
        <div class="sol-num">① √(-4) × √(-9) 의 올바른 계산</div>
        <div class="sol-box">
          √(-4) × √(-9) = 2i × 3i = 6i² = 6×(-1) = <strong>-6</strong>
        </div>
        <div class="sol-note">√(-4)=2i, √(-9)=3i로 먼저 변환 후 곱하기. 정답은 6이 아닌 <strong>-6</strong>!</div>
      </div>
      <div class="sol-item">
        <div class="sol-num">② √8 / √(-4) 의 올바른 계산</div>
        <div class="sol-box">
          √8 / √(-4) = 2√2 / 2i = √2 / i = √2·i / i² = √2·i / (-1) = <strong>-√2·i</strong>
        </div>
        <div class="sol-note">√(-4)=2i로 변환 후 분모 유리화. 정답은 √2i가 아닌 <strong>-√2i</strong>!</div>
      </div>
    </div>
  </div>
</div>

<!-- ═══════════════════════ TAB 4: 도전 문제 ═══════════════════════ -->
<div class="tab-panel" id="tab-t4">
  <div class="score-bar">
    <div class="score-label">🎯 맞힌 문제</div>
    <div class="score-val" id="score-display">0 / 5</div>
  </div>

  <div class="challenge-q" id="cq1">
    <div class="q-num">문제 1</div>
    <div class="q-text">-36의 제곱근을 모두 구하면?</div>
    <div class="q-options">
      <button class="qopt" onclick="check(1,this,'w')">① 6</button>
      <button class="qopt" onclick="check(1,this,'w')">② 6i</button>
      <button class="qopt" onclick="check(1,this,'c')">③ 6i 와 -6i</button>
      <button class="qopt" onclick="check(1,this,'w')">④ ±6</button>
    </div>
    <div class="q-fb" id="cq1-fb"></div>
  </div>

  <div class="challenge-q" id="cq2">
    <div class="q-num">문제 2</div>
    <div class="q-text">√(-3) × √(-12) 를 계산하면?</div>
    <div class="q-options">
      <button class="qopt" onclick="check(2,this,'w')">① 6</button>
      <button class="qopt" onclick="check(2,this,'c')">② -6</button>
      <button class="qopt" onclick="check(2,this,'w')">③ 6i</button>
      <button class="qopt" onclick="check(2,this,'w')">④ -6i</button>
    </div>
    <div class="q-fb" id="cq2-fb"></div>
  </div>

  <div class="challenge-q" id="cq3">
    <div class="q-num">문제 3</div>
    <div class="q-text">√12 / √(-3) 를 계산하면?</div>
    <div class="q-options">
      <button class="qopt" onclick="check(3,this,'w')">① 2i</button>
      <button class="qopt" onclick="check(3,this,'c')">② -2i</button>
      <button class="qopt" onclick="check(3,this,'w')">③ 2</button>
      <button class="qopt" onclick="check(3,this,'w')">④ -2</button>
    </div>
    <div class="q-fb" id="cq3-fb"></div>
  </div>

  <div class="challenge-q" id="cq4">
    <div class="q-num">문제 4</div>
    <div class="q-text">√(-2) × √(-8) + √(-1) × √(-9) 를 계산하면?</div>
    <div class="q-options">
      <button class="qopt" onclick="check(4,this,'w')">① 7</button>
      <button class="qopt" onclick="check(4,this,'c')">② -7</button>
      <button class="qopt" onclick="check(4,this,'w')">③ -1</button>
      <button class="qopt" onclick="check(4,this,'w')">④ 1</button>
    </div>
    <div class="q-fb" id="cq4-fb"></div>
  </div>

  <div class="challenge-q" id="cq5">
    <div class="q-num">문제 5 (옳지 않은 것 찾기)</div>
    <div class="q-text">다음 중 옳지 않은 것은?</div>
    <div class="q-options">
      <button class="qopt" onclick="check(5,this,'w')">① √(-4) = 2i</button>
      <button class="qopt" onclick="check(5,this,'w')">② -9의 제곱근은 3i와 -3i이다</button>
      <button class="qopt" onclick="check(5,this,'c')">③ √(-2) × √(-3) = √6</button>
      <button class="qopt" onclick="check(5,this,'w')">④ √6 / √(-2) = -√3·i</button>
    </div>
    <div class="q-fb" id="cq5-fb"></div>
  </div>

  <div class="complete" id="complete-banner">
    <div class="complete-title" id="complete-title">🎉 모든 문제 완료!</div>
    <div class="complete-msg" id="complete-msg"></div>
  </div>
</div>

</div><!-- .shell -->

<script>
/* ── Tab 전환 ─────────────────────────────────────────────────── */
function switchTab(id, btn){
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.getElementById('tab-'+id).classList.add('active');
  btn.classList.add('active');
}

/* ── Tab 1 Quiz ──────────────────────────────────────────────── */
const Q_FB = {
  q1:{
    ok:'✅ 맞아요! -25의 제곱근은 x²=-25의 해 → x = ±5i, 두 개입니다.',
    no:'❌ -25의 제곱근은 x²=-25를 만족하는 x이므로 5i와 -5i 두 개입니다.'
  },
  q2:{
    ok:'✅ 정확! √(-25) = √25·i = 5i. 하나의 확정된 값입니다.',
    no:'❌ √(-25) = √25·i = 5i 로 하나의 값입니다. ±5i가 아닙니다!'
  },
  q3:{
    ok:'✅ 맞아요! -3의 제곱근은 ±√3i (두 개), √(-3)은 √3i (하나). 개수가 다릅니다.',
    no:'❌ 다시 생각해 보세요. -3의 제곱근은 두 개, √(-3)은 하나입니다!'
  }
};

function checkQ(qid, btn, isCorrect){
  const block = document.getElementById(qid);
  if(block.dataset.done) return;
  block.dataset.done = '1';
  block.querySelectorAll('.qbtn').forEach(b=>b.disabled=true);
  const fb = document.getElementById(qid+'-fb');
  btn.classList.add(isCorrect ? 'correct' : 'wrong');
  fb.style.color = isCorrect ? '#4ade80' : '#f87171';
  fb.textContent = isCorrect ? Q_FB[qid].ok : Q_FB[qid].no;
}

/* ── Tab 2 Step Reveal ───────────────────────────────────────── */
const stepIdx  = {1:0, 2:0, 3:0};
const stepMax  = {1:4, 2:4, 3:3};

function revealStep(n){
  stepIdx[n]++;
  const el = document.getElementById('s'+n+'-'+stepIdx[n]);
  if(el) el.classList.add('show');
  if(stepIdx[n] >= stepMax[n]){
    const btn = document.getElementById('rb'+n);
    btn.disabled = true;
    btn.textContent = '✅ 완료!';
  }
}

/* ── Tab 3 오답 찾기 ────────────────────────────────────────────── */
const hmBusy    = {1:false, 2:false};
const hmSolved  = {1:false, 2:false};

function clickStep(calcNum, stepIdx, isWrong){
  if(hmBusy[calcNum] || hmSolved[calcNum]) return;
  hmBusy[calcNum] = true;

  const stepEl = document.getElementById('hm'+calcNum+'-s'+stepIdx);
  const resultEl = document.getElementById('hm'+calcNum+'-result');

  if(isWrong){
    // 정답!
    hmSolved[calcNum] = true;
    lockCalc(calcNum);
    stepEl.classList.add('highlight-wrong');
    stepEl.querySelector('.calc-icon').textContent = '❌';
    resultEl.className = 'hyunmin-result show ok';
    resultEl.innerHTML = '🎉 정확히 찾았어요! 음수가 포함되어 있는데 √a·√b=√(ab) 공식을 그대로 쓴 게 문제입니다.';
    document.getElementById('pd'+calcNum).classList.add('done');
    if(hmSolved[1] && hmSolved[2]){
      document.getElementById('solutions').classList.add('show');
    }
  } else {
    // 오답
    stepEl.classList.add('flash-wrong');
    resultEl.className = 'hyunmin-result show fail';
    resultEl.textContent = '❌ 이 단계는 옳아요. 공식을 잘못 적용한 단계를 찾아보세요!';
    setTimeout(()=>{
      stepEl.classList.remove('flash-wrong');
      hmBusy[calcNum] = false;
      resultEl.className = 'hyunmin-result';
    }, 1200);
  }
}

function lockCalc(n){
  document.querySelectorAll('#hm'+n+'-steps .calc-step').forEach(s=>{
    s.classList.add('locked');
  });
}

/* ── Tab 4 Challenge ─────────────────────────────────────────── */
let score = 0;
const done = {1:false,2:false,3:false,4:false,5:false};

const FB = {
  1:{c:'✅ 맞아요! -36의 제곱근 → x²=-36 → x=±6i, 두 개입니다.',
     w:'❌ -36의 제곱근은 x²=-36의 해이므로 6i와 -6i, 두 개입니다.'},
  2:{c:'✅ 정확! √(-3)=√3i, √(-12)=2√3i → √3i·2√3i = 2·3·i² = -6',
     w:'❌ √(-3)·√(-12) = √3i·2√3i = 6i² = -6. 음수끼리는 부호가 뒤집혀요!'},
  3:{c:'✅ 맞아요! √12/√(-3) = 2√3/(√3·i) = 2/i = 2i/i² = -2i',
     w:'❌ √(-3)=√3·i 변환 후: 2√3/(√3·i)=2/i → 분모 유리화하면 -2i입니다.'},
  4:{c:'✅ 정확! √(-2)·√(-8)=√2i·2√2i=-4, √(-1)·√(-9)=i·3i=-3 → 합=-7',
     w:'❌ 각각: √(-2)·√(-8)=–4, √(-1)·√(-9)=i·3i=3i²=–3. 합은 –7이에요.'},
  5:{c:'✅ 찾았어요! √(-2)·√(-3)=√2i·√3i=√6·i²=-√6. √6이 아닙니다!',
     w:'❌ ①②④는 모두 옳습니다. ③이 틀렸어요: √(-2)·√(-3)=-√6이어야 해요.'}
};

function check(n, btn, result){
  if(done[n]) return;
  done[n] = true;
  document.querySelectorAll('#cq'+n+' .qopt').forEach(b=>b.disabled=true);
  const fb = document.getElementById('cq'+n+'-fb');
  const ok = (result==='c');
  btn.classList.add(ok ? 'correct' : 'wrong');
  fb.style.color = ok ? '#4ade80' : '#f87171';
  fb.textContent = ok ? FB[n].c : FB[n].w;
  if(ok) score++;
  document.getElementById('score-display').textContent = score+' / 5';

  if(Object.values(done).every(v=>v)){
    const banner = document.getElementById('complete-banner');
    banner.classList.add('show');
    const msgs = {
      5:'🏆 완벽한 점수! 음수의 제곱근 함정을 완전히 정복했어요!',
      4:'🥈 훌륭해요! 거의 다 왔어요. 틀린 문제를 한 번 더 확인해 보세요.',
      3:'👍 좋아요! 함정 탐구 탭을 다시 보며 개념을 다져보세요.',
      2:'💪 조금 더 연습이 필요해요. 탐구 탭부터 다시 복습해 봐요!',
      1:'📚 음수의 제곱근 변환부터 차근차근 다시 해봐요.',
      0:'🔄 탭 1부터 다시 탐구해 보면 잘 이해될 거예요!'
    };
    document.getElementById('complete-msg').textContent = msgs[score] || '수고했어요!';
  }
}
</script>
</body>
</html>"""


def render():
    st.markdown("## 🚨 음수의 제곱근 함정 탈출!")
    st.caption(
        "카드 뒤집기·단계별 탐구·오답 찾기·도전 문제로 음수의 제곱근 성질을 정복해 봅시다. "
        "활동을 마친 후 아래 성찰 폼을 작성해 주세요."
    )
    components.html(_HTML, height=1800, scrolling=True)

    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
