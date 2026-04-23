# activities/common/mini/simultaneous_quadratic_quiz.py
"""
연립이차방정식 해의 개수 스피드퀴즈
- 연립이차방정식의 구조를 보고 정확히 몇 개의 해를 가지는지 판단
- 60초 기본 + 정답 시 +5초 스피드 퀴즈 + 구글 시트 랭킹 보드
"""
import json
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL        = st.secrets["gas_url_common"]
_SHEET_NAME     = "연립이차방정식퀴즈"   # 성찰 기록 시트
_RANKING_SHEET  = "연립이차방정식랭킹"   # 점수 랭킹 시트

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 질문에 답해 보세요**"},
    {
        "key": "판단기준",
        "label": "연립이차방정식의 해의 개수를 판단할 때 어떤 순서로 생각하나요? 자신만의 판단 순서를 서술하세요.",
        "type": "text_area",
        "height": 110,
    },
    {
        "key": "3쌍이유",
        "label": "B₁타입에서 해가 '최대 4쌍'이지만 실제로 3쌍이 되는 경우는 어떤 경우인가요? 이번 활동에서 만난 문제를 예로 들어 설명하세요.",
        "type": "text_area",
        "height": 110,
    },
    {
        "key": "0쌍이유",
        "label": "A타입(일차+이차)에서 해가 0쌍이 되는 조건을 판별식과 연결하여 설명하세요.",
        "type": "text_area",
        "height": 100,
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
    "title": "🎯 연립이차방정식 해의 개수 스피드퀴즈",
    "description": "연립이차방정식의 구조를 보고 정확히 몇 쌍의 해를 가지는지 빠르게 판단! 60초 기본 타이머에 정답마다 +5초 추가, 랭킹 보드로 친구들과 경쟁하세요.",
    "order": 254,
    "hidden": False,
}

_HTML_RAW = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>연립이차방정식 해의 개수 스피드퀴즈</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(155deg,#100820 0%,#1e0f40 55%,#0d0618 100%);
  color:#ede9fe;padding:14px 12px 28px;min-height:100vh;
}
.shell{max-width:860px;margin:0 auto}

/* HERO */
.hero{
  background:linear-gradient(135deg,rgba(124,58,237,.22),rgba(109,40,217,.1));
  border:1px solid rgba(167,139,250,.35);border-radius:18px;
  padding:15px 20px;margin-bottom:14px;position:relative;overflow:hidden;
}
.hero::before{
  content:'{ }';position:absolute;right:16px;top:-10px;font-size:120px;
  font-weight:900;color:rgba(167,139,250,.07);pointer-events:none;
  font-family:'Times New Roman',serif;line-height:1;
}
.hero-tag{
  display:inline-flex;align-items:center;gap:5px;
  background:rgba(167,139,250,.18);border:1px solid rgba(167,139,250,.35);
  border-radius:999px;padding:3px 12px;color:#c4b5fd;
  font-size:.74rem;font-weight:700;letter-spacing:.06em;margin-bottom:8px;
}
.hero h1{font-size:1.35rem;font-weight:900;color:#fff;margin-bottom:5px}
.hero p{color:#c4b5fd;font-size:.86rem;line-height:1.65;max-width:700px}
.hero strong{color:#a78bfa}

/* TABS */
.tabs{display:flex;gap:7px;margin-bottom:14px}
.tab-btn{
  flex:1;padding:10px 8px;border-radius:12px;
  background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.2);
  color:#a78bfa;font-size:.84rem;font-weight:700;cursor:pointer;
  transition:.18s;font-family:inherit;line-height:1.45;
}
.tab-btn:hover:not(.active){background:rgba(167,139,250,.2)}
.tab-btn.active{
  background:linear-gradient(135deg,#7c3aed,#6d28d9);
  border-color:#8b5cf6;color:#fff;box-shadow:0 4px 14px rgba(124,58,237,.45);
}
.tab-panel{display:none}
.tab-panel.active{display:block;animation:fadeUp .3s ease}
@keyframes fadeUp{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:none}}

/* ── TAB1: 비주얼 판단 카드 ── */
.ref-cards{display:flex;flex-direction:column;gap:10px}
.ref-card{
  border-radius:16px;padding:14px 16px;border:1.5px solid;
  display:flex;align-items:center;gap:12px;flex-wrap:wrap;
}
.rc-a{background:rgba(52,211,153,.07);border-color:rgba(52,211,153,.28)}
.rc-b1{background:rgba(167,139,250,.07);border-color:rgba(167,139,250,.28)}
.rc-b2{background:rgba(96,165,250,.07);border-color:rgba(96,165,250,.28)}

.rc-badge{
  flex-shrink:0;font-size:.72rem;font-weight:900;letter-spacing:.06em;
  padding:4px 10px;border-radius:8px;min-width:58px;text-align:center;
}
.badge-a{background:rgba(52,211,153,.2);color:#34d399;border:1px solid rgba(52,211,153,.35)}
.badge-b1{background:rgba(167,139,250,.2);color:#a78bfa;border:1px solid rgba(167,139,250,.35)}
.badge-b2{background:rgba(96,165,250,.2);color:#60a5fa;border:1px solid rgba(96,165,250,.35)}

.rc-body{display:flex;align-items:center;gap:10px;flex:1;flex-wrap:wrap}
.rc-eq-box{
  display:flex;align-items:center;gap:5px;
  background:rgba(255,255,255,.04);border-radius:10px;padding:8px 10px;
}
.rc-brace{font-size:2.6rem;line-height:1;font-family:'Times New Roman',serif;flex-shrink:0}
.rc-eqs{display:flex;flex-direction:column;gap:4px}
.rc-eq{font-family:'Times New Roman',Georgia,serif;font-style:italic;font-size:1rem;color:#fde68a}
.rc-eq.linear{color:#6ee7b7}
.rc-eq.purple{color:#c4b5fd}
.rc-eq.blue{color:#93c5fd}

.rc-arrow{font-size:1.4rem;color:#4b5563;flex-shrink:0}

.rc-step{
  background:rgba(255,255,255,.04);border-radius:10px;padding:8px 12px;
  font-size:.82rem;color:#94a3b8;text-align:center;line-height:1.6;
}
.rc-step .step-eq{
  font-family:'Times New Roman',serif;font-style:italic;
  font-size:1rem;color:#e2e8ff;margin-top:3px;
}

.rc-result{
  flex-shrink:0;text-align:center;min-width:64px;
  background:rgba(255,255,255,.04);border-radius:12px;padding:8px 10px;
}
.rc-num{font-size:1.6rem;font-weight:900;line-height:1}
.rc-num-green{color:#34d399}.rc-num-purple{color:#c4b5fd}.rc-num-blue{color:#93c5fd}
.rc-num-label{font-size:.72rem;color:#64748b;margin-top:2px}

/* 예시 행 */
.rc-example{
  width:100%;margin-top:8px;padding:8px 12px;
  background:rgba(255,255,255,.03);border-radius:10px;
  font-size:.82rem;color:#64748b;line-height:1.7;
  border-left:3px solid rgba(255,255,255,.1);
}
.rc-example em{font-family:'Times New Roman',serif;font-style:italic;color:#fde68a}
.rc-example .ok{color:#34d399;font-weight:700}
.rc-example .ok-p{color:#c4b5fd;font-weight:700}
.rc-example .ok-b{color:#93c5fd;font-weight:700}

/* DISCRIMINANT HINT */
.disc-hint{
  margin-top:10px;
  background:rgba(245,158,11,.07);border:1px solid rgba(245,158,11,.2);
  border-radius:12px;padding:10px 14px;
  display:flex;align-items:center;gap:14px;flex-wrap:wrap;
}
.disc-item{text-align:center;flex:1;min-width:70px}
.disc-cond{font-family:'Times New Roman',serif;font-style:italic;font-size:.92rem;color:#fde68a}
.disc-arrow{font-size:1.1rem;color:#64748b}
.disc-res{font-size:.88rem;font-weight:700;margin-top:2px}

/* ── TAB2: 스피드퀴즈 ── */
.name-screen{text-align:center;padding:20px 10px}
.name-screen h2{font-size:1.45rem;font-weight:900;color:#fff;margin-bottom:8px}
.name-screen p{color:#a78bfa;font-size:.88rem;margin-bottom:16px;line-height:1.7}
.name-input{
  width:100%;max-width:300px;padding:12px 18px;border-radius:12px;
  background:rgba(167,139,250,.12);border:1.5px solid rgba(167,139,250,.3);
  color:#ede9fe;font-size:1.1rem;font-weight:700;outline:none;
  font-family:inherit;text-align:center;margin-bottom:14px;
  display:block;margin-left:auto;margin-right:auto;
}
.name-input:focus{border-color:#8b5cf6}
.name-input::placeholder{color:#5b21b6;font-weight:400}
.rules-box{
  margin-top:16px;background:rgba(167,139,250,.08);
  border:1px solid rgba(167,139,250,.18);border-radius:12px;
  padding:12px 16px;text-align:left;font-size:.82rem;color:#94a3b8;line-height:1.9;
}
.rules-box .r-title{color:#c4b5fd;font-weight:700;margin-bottom:5px}

/* GAME SCREEN */
.timer-bar-wrap{height:6px;background:rgba(255,255,255,.08);border-radius:3px;overflow:hidden;margin-bottom:10px}
.timer-bar-fill{height:100%;border-radius:3px;transition:width .9s linear;background:linear-gradient(90deg,#7c3aed,#c4b5fd)}
.timer-bar-fill.warning{background:linear-gradient(90deg,#f59e0b,#fbbf24)}
.timer-bar-fill.danger{background:linear-gradient(90deg,#ef4444,#f87171)}
.timer-bar-fill.bonus{background:linear-gradient(90deg,#10b981,#34d399);transition:width .2s ease}

.game-hud{
  display:flex;justify-content:space-between;align-items:center;
  margin-bottom:12px;background:rgba(167,139,250,.1);
  border:1px solid rgba(167,139,250,.18);border-radius:13px;padding:10px 16px;
  position:relative;
}
.hud-item{text-align:center}
.hud-lbl{font-size:.68rem;color:#a78bfa;font-weight:700;letter-spacing:.05em;margin-bottom:2px}
.hud-val{font-size:1.3rem;font-weight:900;color:#fff;transition:color .3s}
.hud-warn{color:#fbbf24}.hud-danger{color:#f87171;animation:blink .5s infinite alternate}
@keyframes blink{from{opacity:.5}to{opacity:1}}

/* +5초 보너스 팝업 */
.time-bonus-pop{
  position:absolute;top:-22px;left:50%;transform:translateX(-50%);
  color:#34d399;font-size:1rem;font-weight:900;
  opacity:0;transition:opacity .3s ease,transform .5s ease;
  pointer-events:none;white-space:nowrap;
  text-shadow:0 0 10px rgba(52,211,153,.8);
}
.time-bonus-pop.show{opacity:1;transform:translateX(-50%) translateY(-8px)}

.quiz-card{
  background:rgba(255,255,255,.04);border:1px solid rgba(167,139,250,.18);
  border-radius:18px;padding:14px 16px;margin-bottom:10px;
}
.q-label{
  font-size:.7rem;font-weight:800;letter-spacing:.08em;
  color:#7c3aed;margin-bottom:8px;text-transform:uppercase;
}
.q-sys-box{
  display:flex;align-items:center;justify-content:center;
  background:rgba(167,139,250,.06);border:1px solid rgba(167,139,250,.12);
  border-radius:12px;padding:16px 12px;margin-bottom:12px;gap:8px;
}
.q-brace{font-size:4rem;color:#8b5cf6;line-height:1;font-family:'Times New Roman',serif}
.q-eqs{display:flex;flex-direction:column;gap:9px}
.q-eq{
  font-family:'Times New Roman',Georgia,serif;font-style:italic;
  font-size:1.45rem;color:#fde68a;white-space:nowrap;
}
.q-hint{font-size:.78rem;color:#64748b;text-align:center;margin-bottom:11px}

/* 5-button answer row */
.ans-row5{display:flex;gap:7px;margin-bottom:8px}
.ans-btn5{
  flex:1;padding:14px 4px;border-radius:12px;border:2px solid;cursor:pointer;
  font-size:1rem;font-weight:800;transition:.15s;font-family:inherit;text-align:center;
  line-height:1.3;
}
.ab0{background:rgba(248,113,113,.08);border-color:rgba(248,113,113,.3);color:#fca5a5}
.ab1{background:rgba(251,191,36,.08);border-color:rgba(251,191,36,.3);color:#fde68a}
.ab2{background:rgba(52,211,153,.08);border-color:rgba(52,211,153,.3);color:#6ee7b7}
.ab3{background:rgba(20,184,166,.08);border-color:rgba(20,184,166,.3);color:#5eead4}
.ab4{background:rgba(167,139,250,.08);border-color:rgba(167,139,250,.3);color:#c4b5fd}
.ans-btn5:hover{filter:brightness(1.3);transform:translateY(-2px)}
.ans-btn5:disabled{opacity:.4;cursor:not-allowed;transform:none;filter:none}

/* FEEDBACK OVERLAY */
.fb-overlay{
  position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
  background:rgba(8,4,18,.96);border-radius:20px;
  padding:20px 28px;text-align:center;z-index:999;
  border:2px solid;min-width:230px;max-width:350px;
  animation:popIn .18s ease;
}
@keyframes popIn{from{transform:translate(-50%,-50%) scale(.8);opacity:0}to{transform:translate(-50%,-50%) scale(1);opacity:1}}
.fb-ok{border-color:rgba(52,211,153,.5);box-shadow:0 0 50px rgba(52,211,153,.2)}
.fb-ng{border-color:rgba(248,113,113,.5);box-shadow:0 0 50px rgba(248,113,113,.15)}
.fb-icon{font-size:2rem;margin-bottom:6px}
.fb-msg{font-size:1rem;font-weight:700;line-height:1.5;margin-bottom:7px}
.fb-ok .fb-msg{color:#6ee7b7}.fb-ng .fb-msg{color:#fca5a5}
.fb-sub{font-size:.8rem;color:#94a3b8;line-height:1.7}

/* RESULT */
.result-hero{
  text-align:center;padding:22px 12px;
  background:linear-gradient(135deg,rgba(124,58,237,.15),rgba(109,40,217,.08));
  border:1px solid rgba(167,139,250,.3);border-radius:18px;margin-bottom:12px;
}
.result-name{font-size:.9rem;color:#a78bfa;margin-bottom:4px}
.result-score{font-size:4rem;font-weight:900;color:#c4b5fd;line-height:1.1}
.result-stars{font-size:1.8rem;margin:8px 0 4px}
.result-msg{color:#94a3b8;font-size:.84rem}
.stats-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:12px}
.stat-card{
  text-align:center;background:rgba(255,255,255,.04);
  border:1px solid rgba(167,139,250,.15);border-radius:12px;padding:11px 8px;
}
.stat-val{font-size:1.6rem;font-weight:900;color:#c4b5fd}
.stat-lbl{font-size:.72rem;color:#64748b;margin-top:2px}

/* 랭킹 안내 박스 */
.rank-guide{
  background:rgba(167,139,250,.06);border:1px solid rgba(167,139,250,.15);
  border-radius:12px;padding:12px 16px;text-align:center;
  margin-bottom:12px;font-size:.83rem;color:#a78bfa;
}

/* BUTTON */
.btn{padding:10px 22px;border-radius:12px;border:none;cursor:pointer;font-size:.94rem;font-weight:700;transition:.18s;font-family:inherit}
.btn-primary{background:linear-gradient(135deg,#7c3aed,#6d28d9);color:#fff;box-shadow:0 4px 14px rgba(124,58,237,.4)}
.btn-primary:hover{opacity:.88;transform:translateY(-1px)}
.btn-ghost{background:transparent;border:1px solid rgba(167,139,250,.3);color:#c4b5fd}
.btn-ghost:hover{background:rgba(167,139,250,.12)}

@media(max-width:600px){
  .rc-card{flex-direction:column}
  .ans-row5{gap:4px}
  .ans-btn5{font-size:.88rem;padding:12px 2px}
  .q-eq{font-size:1.15rem}
  .hero h1{font-size:1.1rem}
  .disc-hint{gap:8px}
}
</style>
</head>
<body>
<div class="shell">

<!-- HERO -->
<section class="hero">
  <div class="hero-tag">🎯 연립이차방정식 탐구</div>
  <h1>해의 개수, 형태만 보고 맞혀라!</h1>
  <p><strong>일차식 포함 여부</strong>와 <strong>이차식의 인수분해 꼴</strong>을 보면 해의 개수를 판단할 수 있습니다.</p>
</section>

<!-- TABS -->
<div class="tabs">
  <button class="tab-btn active" id="tabBtnC" onclick="showTab('c')">📋 판단 지도</button>
  <button class="tab-btn" id="tabBtnQ" onclick="showTab('q')">⚡ 스피드퀴즈</button>
</div>

<!-- ═══════ TAB1: 판단 지도 (Visual only) ═══════ -->
<div class="tab-panel active" id="tab-c">

<div class="ref-cards">

  <!-- A타입 -->
  <div class="ref-card rc-a">
    <div class="rc-badge badge-a">A타입</div>
    <div class="rc-body">
      <div class="rc-eq-box">
        <span class="rc-brace" style="color:#34d399">{</span>
        <div class="rc-eqs">
          <div class="rc-eq linear">(일차식) = 0</div>
          <div class="rc-eq">(이차식) = 0</div>
        </div>
      </div>
      <div class="rc-arrow">→</div>
      <div class="rc-step">
        대입<br>
        <div class="step-eq">a<em>t</em>²+b<em>t</em>+c = 0</div>
      </div>
      <div class="rc-arrow">→</div>
      <div class="rc-result">
        <div class="rc-num rc-num-green">0·1·2</div>
        <div class="rc-num-label">쌍</div>
      </div>
    </div>
    <div class="rc-example">
      예: <em>x</em>+<em>y</em>=3 &amp; <em>x</em>²+<em>y</em>²=5
      → <em>x</em>=3−<em>y</em> 대입 → 2<em>y</em>²−6<em>y</em>+4=0 → (<em>y</em>−1)(<em>y</em>−2)=0 → <span class="ok">2쌍</span>
    </div>
  </div>

  <!-- B₁타입 -->
  <div class="ref-card rc-b1">
    <div class="rc-badge badge-b1">B₁타입</div>
    <div class="rc-body">
      <div class="rc-eq-box">
        <span class="rc-brace" style="color:#a78bfa">{</span>
        <div class="rc-eqs">
          <div class="rc-eq purple">(일차₁)(일차₂) = 0</div>
          <div class="rc-eq">(이차식) = 0</div>
        </div>
      </div>
      <div class="rc-arrow">→</div>
      <div class="rc-step">
        A타입₁<br>
        <span style="color:#4b5563;font-size:.75rem">+</span><br>
        A타입₂
      </div>
      <div class="rc-arrow">→</div>
      <div class="rc-result">
        <div class="rc-num rc-num-purple">0~4</div>
        <div class="rc-num-label">쌍</div>
      </div>
    </div>
    <div class="rc-example">
      예: <em>x</em>²−<em>y</em>²=0 &amp; <em>x</em>²+<em>y</em>²=4
      → (<em>x</em>+<em>y</em>)(<em>x</em>−<em>y</em>)=0 → 두 A타입 → <span class="ok-p">4쌍</span><br>
      ※ 두 가지에 공통해가 생기면 <span class="ok-p">3쌍</span> 이하가 될 수 있어요
    </div>
  </div>

  <!-- B₂타입 -->
  <div class="ref-card rc-b2">
    <div class="rc-badge badge-b2">B₂타입</div>
    <div class="rc-body">
      <div class="rc-eq-box">
        <span class="rc-brace" style="color:#60a5fa">{</span>
        <div class="rc-eqs">
          <div class="rc-eq blue">(일차식)² = 0</div>
          <div class="rc-eq">(이차식) = 0</div>
        </div>
      </div>
      <div class="rc-arrow">→</div>
      <div class="rc-step">
        일차식 = 0<br>
        <span style="color:#93c5fd;font-size:.78rem">= A타입!</span>
      </div>
      <div class="rc-arrow">→</div>
      <div class="rc-result">
        <div class="rc-num rc-num-blue">0·1·2</div>
        <div class="rc-num-label">쌍</div>
      </div>
    </div>
    <div class="rc-example">
      예: (<em>x</em>−<em>y</em>)²=0 &amp; <em>x</em>²+<em>y</em>²=4
      → <em>x</em>=<em>y</em> → 2<em>y</em>²=4 → <em>y</em>=±√2 → <span class="ok-b">2쌍</span>
    </div>
  </div>

</div><!-- ref-cards -->

<!-- 판별식 힌트 (A타입 & B₂타입 공통) -->
<div class="disc-hint" style="margin-top:10px">
  <div style="font-size:.75rem;font-weight:800;color:#f59e0b;flex:100%;margin-bottom:4px">
    ⚠ A타입 · B₂타입: 대입 후 이차방정식의 판별식 D 확인
  </div>
  <div class="disc-item">
    <div class="disc-cond">D &gt; 0</div>
    <div class="disc-arrow">→</div>
    <div class="disc-res" style="color:#34d399">2쌍</div>
  </div>
  <div style="color:#374151;font-size:1rem">|</div>
  <div class="disc-item">
    <div class="disc-cond">D = 0</div>
    <div class="disc-arrow">→</div>
    <div class="disc-res" style="color:#fbbf24">1쌍</div>
  </div>
  <div style="color:#374151;font-size:1rem">|</div>
  <div class="disc-item">
    <div class="disc-cond">D &lt; 0</div>
    <div class="disc-arrow">→</div>
    <div class="disc-res" style="color:#f87171">0쌍</div>
  </div>
</div>

</div><!-- tab-c -->

<!-- ═══════ TAB2: 스피드퀴즈 ═══════ -->
<div class="tab-panel" id="tab-q">

  <!-- 이름 입력 -->
  <div id="nameScreen" class="name-screen">
    <div style="font-size:2.8rem;margin-bottom:10px">⚡</div>
    <h2>스피드퀴즈 도전!</h2>
    <p>연립방정식을 보고 <strong style="color:#a78bfa">정확한 해의 쌍의 수</strong>를 고르세요!<br>
    기본 <span style="color:#fbbf24;font-weight:700">60초</span>에서 시작, 정답마다 <span style="color:#34d399;font-weight:700">+5초!</span></p>
    <input class="name-input" id="nameInput" type="text" placeholder="이름 또는 별명" maxlength="10">
    <button class="btn btn-primary" onclick="startGame()">게임 시작! →</button>
    <div class="rules-box">
      <div class="r-title">📋 게임 규칙</div>
      <div>• 0·1·2·3·4 중 <strong style="color:#ede9fe">정확한 해의 쌍의 수</strong>를 선택하세요</div>
      <div>• 정답 → <span style="color:#34d399;font-weight:700">+10점</span> + 타이머 <span style="color:#34d399;font-weight:700">+5초</span></div>
      <div>• 5초 이내 정답이면 <span style="color:#fbbf24;font-weight:700">⚡ +5 스피드 보너스</span></div>
      <div>• 오답도 패널티 없어요. 과감하게 도전하세요!</div>
      <div style="margin-top:6px;font-size:.76rem;color:#4b5563">🏆 점수는 구글 시트에 저장되어 다른 기기에서도 랭킹을 확인할 수 있어요</div>
    </div>
  </div>

  <!-- 게임 화면 -->
  <div id="gameScreen" style="display:none">
    <div class="timer-bar-wrap">
      <div class="timer-bar-fill" id="timerBar" style="width:100%"></div>
    </div>
    <div class="game-hud">
      <div class="time-bonus-pop" id="timeBonusPop">+5초!</div>
      <div class="hud-item">
        <div class="hud-lbl">⏱ 남은 시간</div>
        <div class="hud-val" id="hudTimer">1:00</div>
      </div>
      <div class="hud-item">
        <div class="hud-lbl">🏆 점수</div>
        <div class="hud-val" id="hudScore">0</div>
      </div>
      <div class="hud-item">
        <div class="hud-lbl">✅ 정답</div>
        <div class="hud-val" id="hudOk">0</div>
      </div>
      <div class="hud-item">
        <div class="hud-lbl">❌ 오답</div>
        <div class="hud-val" id="hudNg">0</div>
      </div>
    </div>

    <div class="quiz-card">
      <div class="q-label" id="qLabel">문제 1</div>
      <div class="q-sys-box" id="qSysBox"></div>
      <div class="q-hint">이 연립방정식의 실수 해는 정확히 몇 쌍인가요?</div>
      <div class="ans-row5">
        <button class="ans-btn5 ab0" id="ab0" onclick="answer(0)">0쌍</button>
        <button class="ans-btn5 ab1" id="ab1" onclick="answer(1)">1쌍</button>
        <button class="ans-btn5 ab2" id="ab2" onclick="answer(2)">2쌍</button>
        <button class="ans-btn5 ab3" id="ab3" onclick="answer(3)">3쌍</button>
        <button class="ans-btn5 ab4" id="ab4" onclick="answer(4)">4쌍</button>
      </div>
    </div>
  </div>

  <!-- 피드백 오버레이 -->
  <div class="fb-overlay" id="fbOverlay" style="display:none">
    <div class="fb-icon" id="fbIcon"></div>
    <div class="fb-msg" id="fbMsg"></div>
    <div class="fb-sub" id="fbSub"></div>
  </div>

  <!-- 결과 화면 -->
  <div id="resultScreen" style="display:none">
    <div class="result-hero">
      <div class="result-name" id="resultName">—</div>
      <div class="result-score" id="resultScore">0</div>
      <div style="font-size:.85rem;color:#6b7280">점</div>
      <div class="result-stars" id="resultStars">⭐</div>
      <div class="result-msg" id="resultMsg">—</div>
    </div>
    <div class="stats-grid">
      <div class="stat-card"><div class="stat-val" id="sOk">0</div><div class="stat-lbl">정답</div></div>
      <div class="stat-card"><div class="stat-val" id="sNg">0</div><div class="stat-lbl">오답</div></div>
      <div class="stat-card"><div class="stat-val" id="sTotal">0</div><div class="stat-lbl">푼 문제</div></div>
    </div>
    <div id="scoreSubmitStatus" style="text-align:center;font-size:.82rem;color:#64748b;padding:8px 0 4px"></div>
    <div class="rank-guide">
      ⬇️ 아래 <strong>랭킹 보드</strong>에서 내 순위를 확인하세요!<br>
      <span style="font-size:.76rem;color:#6b7280">(새로고침 버튼을 누르면 최신 순위가 보여요)</span>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;justify-content:center">
      <button class="btn btn-primary" onclick="restartGame()">다시 도전! 🔄</button>
      <button class="btn btn-ghost" onclick="showTab('c')">📋 판단 지도</button>
    </div>
  </div>

</div><!-- tab-q -->
</div><!-- shell -->

<script>
/* ── 높이 자동 조절 ── */
function notifyH(){
  var h=Math.max(document.body.scrollHeight,document.documentElement.scrollHeight)+40;
  window.parent.postMessage({isStreamlitMessage:true,type:'streamlit:setFrameHeight',args:{height:h}},'*');
  window.parent.postMessage({type:'streamlit:setFrameHeight',height:h},'*');
}
new ResizeObserver(function(){notifyH();}).observe(document.body);
window.addEventListener('load',function(){setTimeout(notifyH,120);});

/* ── 탭 전환 ── */
function showTab(n){
  document.getElementById('tab-c').classList.toggle('active',n==='c');
  document.getElementById('tab-q').classList.toggle('active',n==='q');
  document.getElementById('tabBtnC').classList.toggle('active',n==='c');
  document.getElementById('tabBtnQ').classList.toggle('active',n==='q');
  setTimeout(notifyH,60);
}

/* ── 퀴즈 데이터 (정확한 해의 수) ── */
var POOL = [

  /* ─── 0쌍 ─── */
  {q1:'<em>x</em> + <em>y</em> = 3',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 2',
   ans:0,
   reason:'<em>x</em>=3−<em>y</em> 대입 → 2<em>y</em>²−6<em>y</em>+7=0<br>판별식 D=36−56=−20&lt;0 → <strong style="color:#f87171">실근 없음 → 0쌍</strong>'},

  {q1:'<em>x</em> + <em>y</em> = 5',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 4',
   ans:0,
   reason:'<em>x</em>=5−<em>y</em> 대입 → 2<em>y</em>²−10<em>y</em>+21=0<br>D=100−168&lt;0 → <strong style="color:#f87171">0쌍</strong>'},

  {q1:'<em>x</em><sup>2</sup>+2<em>xy</em>+<em>y</em><sup>2</sup>=0',
   q2:'<em>x</em><sup>2</sup> − <em>y</em><sup>2</sup> = 3',
   ans:0,
   reason:'(<em>x</em>+<em>y</em>)²=0 → <em>x</em>=−<em>y</em><br><em>x</em>²−<em>y</em>²=(<em>x</em>+<em>y</em>)(<em>x</em>−<em>y</em>)=0 ≠ 3 → <strong style="color:#f87171">0쌍</strong>'},

  /* ─── 1쌍 ─── */
  {q1:'<em>x</em> + <em>y</em> = 2',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 2',
   ans:1,
   reason:'<em>x</em>=2−<em>y</em> 대입 → 2<em>y</em>²−4<em>y</em>+2=0<br>(<em>y</em>−1)²=0 → <em>y</em>=1, <em>x</em>=1 → <strong style="color:#fbbf24">(1,1) 1쌍</strong>'},

  {q1:'<em>x</em> − <em>y</em> = 2',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 2',
   ans:1,
   reason:'<em>x</em>=<em>y</em>+2 대입 → 2<em>y</em>²+4<em>y</em>+2=0<br>(<em>y</em>+1)²=0 → <em>y</em>=−1, <em>x</em>=1 → <strong style="color:#fbbf24">(1,−1) 1쌍</strong>'},

  {q1:'<em>x</em><sup>2</sup>−2<em>xy</em>+<em>y</em><sup>2</sup>=0',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 0',
   ans:1,
   reason:'(<em>x</em>−<em>y</em>)²=0 → <em>x</em>=<em>y</em><br>2<em>x</em>²=0 → <em>x</em>=0, <em>y</em>=0 → <strong style="color:#fbbf24">(0,0) 1쌍</strong>'},

  /* ─── 2쌍 · A타입 ─── */
  {q1:'<em>x</em> + <em>y</em> = 3',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 5',
   ans:2,
   reason:'<em>x</em>=3−<em>y</em> 대입 → 2<em>y</em>²−6<em>y</em>+4=0<br>(<em>y</em>−1)(<em>y</em>−2)=0 → <strong style="color:#34d399">(2,1),(1,2) 2쌍</strong>'},

  {q1:'<em>x</em> − <em>y</em> = 2',
   q2:'<em>xy</em> = 8',
   ans:2,
   reason:'<em>x</em>=<em>y</em>+2 대입 → <em>y</em>²+2<em>y</em>−8=0<br>(<em>y</em>+4)(<em>y</em>−2)=0 → <strong style="color:#34d399">(−2,−4),(4,2) 2쌍</strong>'},

  {q1:'<em>x</em> + <em>y</em> = 0',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 2',
   ans:2,
   reason:'<em>x</em>=−<em>y</em> 대입 → 2<em>y</em>²=2 → <em>y</em>=±1<br>→ <strong style="color:#34d399">(−1,1),(1,−1) 2쌍</strong>'},

  /* ─── 2쌍 · B₂타입 ─── */
  {q1:'<em>x</em><sup>2</sup>−2<em>xy</em>+<em>y</em><sup>2</sup>=0',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 4',
   ans:2,
   reason:'(<em>x</em>−<em>y</em>)²=0 → <em>x</em>=<em>y</em><br>2<em>y</em>²=4 → <em>y</em>=±√2 → <strong style="color:#34d399">2쌍</strong>'},

  {q1:'4<em>x</em><sup>2</sup>−4<em>xy</em>+<em>y</em><sup>2</sup>=0',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 5',
   ans:2,
   reason:'(2<em>x</em>−<em>y</em>)²=0 → <em>y</em>=2<em>x</em><br>5<em>x</em>²=5 → <em>x</em>=±1 → <strong style="color:#34d399">(1,2),(−1,−2) 2쌍</strong>'},

  /* ─── 3쌍 · B₁타입 (공통해 포함) ─── */
  {q1:'<em>x</em><sup>2</sup> − <em>y</em><sup>2</sup> = 0',
   q2:'<em>x</em><sup>2</sup> − 2<em>x</em> + <em>y</em><sup>2</sup> = 0',
   ans:3,
   reason:'(<em>x</em>+<em>y</em>)(<em>x</em>−<em>y</em>)=0<br>'
         +'<em>x</em>=<em>y</em>: 2<em>y</em>(<em>y</em>−1)=0 → (0,0),(1,1)<br>'
         +'<em>x</em>=−<em>y</em>: 2<em>y</em>(<em>y</em>+1)=0 → (0,0),(1,−1)<br>'
         +'(0,0) 중복 → <strong style="color:#5eead4">(0,0),(1,1),(1,−1) 3쌍</strong>'},

  {q1:'<em>x</em><sup>2</sup> − <em>xy</em> = 0',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> − 2<em>y</em> = 0',
   ans:3,
   reason:'<em>x</em>(<em>x</em>−<em>y</em>)=0<br>'
         +'<em>x</em>=0: <em>y</em>(<em>y</em>−2)=0 → (0,0),(0,2)<br>'
         +'<em>x</em>=<em>y</em>: 2<em>y</em>(<em>y</em>−1)=0 → (0,0),(1,1)<br>'
         +'(0,0) 중복 → <strong style="color:#5eead4">(0,0),(0,2),(1,1) 3쌍</strong>'},

  /* ─── 4쌍 · B₁타입 (모두 다름) ─── */
  {q1:'<em>x</em><sup>2</sup> − <em>y</em><sup>2</sup> = 0',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 4',
   ans:4,
   reason:'(<em>x</em>+<em>y</em>)(<em>x</em>−<em>y</em>)=0<br>'
         +'각 분기: 2<em>y</em>²=4 → <em>y</em>=±√2<br>'
         +'→ <strong style="color:#c4b5fd">(√2,√2),(−√2,−√2),(√2,−√2),(−√2,√2) 4쌍</strong>'},

  {q1:'<em>x</em><sup>2</sup> − 4<em>y</em><sup>2</sup> = 0',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 5',
   ans:4,
   reason:'(<em>x</em>+2<em>y</em>)(<em>x</em>−2<em>y</em>)=0<br>'
         +'각 분기: 5<em>y</em>²=5 → <em>y</em>=±1<br>'
         +'→ <strong style="color:#c4b5fd">(2,1),(−2,−1),(−2,1),(2,−1) 4쌍</strong>'},

  {q1:'<em>x</em><sup>2</sup> − <em>xy</em> = 0',
   q2:'<em>x</em><sup>2</sup> + <em>y</em><sup>2</sup> = 5',
   ans:4,
   reason:'<em>x</em>(<em>x</em>−<em>y</em>)=0<br>'
         +'<em>x</em>=0: <em>y</em>=±√5 → (0,√5),(0,−√5)<br>'
         +'<em>x</em>=<em>y</em>: 2<em>y</em>²=5 → <em>y</em>=±√(5/2)<br>'
         +'→ <strong style="color:#c4b5fd">모두 다른 4쌍</strong>'},
];

/* ── 게임 상태 ── */
var GS={
  name:'',timeLeft:30,maxTime:30,score:0,ok:0,ng:0,total:0,
  qs:[],qi:0,qStartTime:0,timerID:null,locked:false
};
var BONUS_SECS=5;

function shuffle(arr){
  var a=arr.slice();
  for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}
  return a;
}

function startGame(){
  var nm=document.getElementById('nameInput').value.trim();
  if(!nm){
    document.getElementById('nameInput').style.borderColor='#f87171';
    setTimeout(function(){document.getElementById('nameInput').style.borderColor='';},900);
    return;
  }
  GS.name=nm; GS.timeLeft=60; GS.maxTime=60; GS.score=0;
  GS.ok=0; GS.ng=0; GS.total=0; GS.qi=0; GS.locked=false;
  GS.qs=shuffle(POOL.concat(shuffle(POOL.slice())));

  document.getElementById('nameScreen').style.display='none';
  document.getElementById('gameScreen').style.display='block';
  document.getElementById('resultScreen').style.display='none';
  document.getElementById('fbOverlay').style.display='none';

  updateHUD(); showQ();
  GS.timerID=setInterval(tick,1000);
  setTimeout(notifyH,50);
}

function tick(){
  GS.timeLeft--;
  updateHUD();
  if(GS.timeLeft<=0){
    clearInterval(GS.timerID);
    GS.locked=true;
    document.getElementById('fbOverlay').style.display='none';
    setTimeout(showResult,200);
  }
}

function updateHUD(){
  var t=GS.timeLeft;
  var tv=Math.max(t,0);
  var s=Math.floor(tv/60)+':'+(tv%60<10?'0':'')+tv%60;
  var el=document.getElementById('hudTimer');
  el.textContent=s;
  el.className='hud-val'+(t<=5?' hud-danger':t<=10?' hud-warn':'');

  var pct=Math.min(100,t/GS.maxTime*100);
  var bar=document.getElementById('timerBar');
  bar.style.width=pct+'%';
  bar.className='timer-bar-fill'+(t<=5?' danger':t<=10?' warning':'');

  document.getElementById('hudScore').textContent=GS.score;
  document.getElementById('hudOk').textContent=GS.ok;
  document.getElementById('hudNg').textContent=GS.ng;
}

function showQ(){
  if(GS.qi>=GS.qs.length){
    GS.qs=shuffle(POOL.concat(shuffle(POOL.slice())));
    GS.qi=0;
  }
  var q=GS.qs[GS.qi];
  GS.qStartTime=Date.now();
  document.getElementById('qLabel').textContent='문제 '+(GS.total+1);
  document.getElementById('qSysBox').innerHTML=
    '<span class="q-brace">{</span>'+
    '<div class="q-eqs"><div class="q-eq">'+q.q1+'</div><div class="q-eq">'+q.q2+'</div></div>';
  for(var i=0;i<=4;i++){
    var b=document.getElementById('ab'+i);
    b.disabled=false; b.style.opacity='1';
  }
  setTimeout(notifyH,20);
}

function showTimeBonusPop(){
  var el=document.getElementById('timeBonusPop');
  el.classList.add('show');
  setTimeout(function(){el.classList.remove('show');},1100);
}

function answer(choice){
  if(GS.locked) return;
  GS.locked=true;
  GS.total++;
  for(var i=0;i<=4;i++) document.getElementById('ab'+i).disabled=true;

  var q=GS.qs[GS.qi];
  var elapsed=(Date.now()-GS.qStartTime)/1000;
  var correct=(choice===q.ans);
  var pts=0;
  if(correct){
    pts=10; if(elapsed<=5) pts+=5;
    GS.score+=pts; GS.ok++;
    GS.timeLeft+=BONUS_SECS;
    GS.maxTime=Math.max(GS.maxTime,GS.timeLeft);
    showTimeBonusPop();
    updateHUD();
  } else {
    GS.ng++;
  }

  var fb=document.getElementById('fbOverlay');
  fb.className='fb-overlay '+(correct?'fb-ok':'fb-ng');
  document.getElementById('fbIcon').textContent=correct?'✅':'❌';
  document.getElementById('fbMsg').innerHTML=correct
    ?('정답! <span style="color:#fbbf24">+'+pts+'점</span>'+(pts>10?' ⚡':'')+'  <span style="color:#34d399">+5초</span>')
    :('오답! 정답: <strong>'+q.ans+'쌍</strong>');
  document.getElementById('fbSub').innerHTML=q.reason;
  fb.style.display='block';

  var delay=correct?1000:1600;
  setTimeout(function(){
    fb.style.display='none';
    GS.qi++;
    GS.locked=false;
    if(GS.timeLeft>0) showQ();
  },delay);
}

function showResult(){
  document.getElementById('gameScreen').style.display='none';
  document.getElementById('resultScreen').style.display='block';
  document.getElementById('resultName').textContent=GS.name+'님의 결과';
  document.getElementById('resultScore').textContent=GS.score;
  document.getElementById('sOk').textContent=GS.ok;
  document.getElementById('sNg').textContent=GS.ng;
  document.getElementById('sTotal').textContent=GS.total;

  var stars,msg;
  if(GS.score>=150){stars='🌟🌟🌟';msg='완벽한 실력! 연립이차방정식 마스터!';}
  else if(GS.score>=100){stars='⭐⭐⭐';msg='훌륭해요! 구조 분석 속도가 빨라지고 있어요!';}
  else if(GS.score>=60){stars='⭐⭐';msg='잘 하고 있어요! 조금 더 연습하면 더 빨라져요!';}
  else if(GS.score>=20){stars='⭐';msg='판단 지도를 보고 다시 도전해 보세요!';}
  else{stars='💪';msg='개념 정리 탭을 먼저 보고 다시 도전하세요!';}
  document.getElementById('resultStars').textContent=stars;
  document.getElementById('resultMsg').textContent=msg;

  submitScore();
  setTimeout(notifyH,80);
}

function submitScore(){
  var statusEl=document.getElementById('scoreSubmitStatus');
  if(!_U.id||!_U.gasUrl){
    statusEl.textContent='ℹ️ 로그인 학생만 랭킹에 기록됩니다.';
    return;
  }
  if(GS.score<=0){
    statusEl.textContent='ℹ️ 0점은 랭킹에 기록되지 않습니다.';
    return;
  }
  statusEl.textContent='📡 점수('+GS.score+'점) 저장 중...';
  statusEl.style.color='#94a3b8';
  var now=new Date();
  var kst=new Date(now.getTime()+9*3600*1000);
  var ts=kst.toISOString().replace('T',' ').slice(0,19);
  var payload=JSON.stringify({
    sheet:'연립이차방정식랭킹',
    timestamp:ts,
    학번:_U.id,
    이름:_U.name,
    점수:GS.score,
    정답:GS.ok,
    문제수:GS.total
  });
  fetch(_U.gasUrl,{method:'POST',body:payload,
    headers:{'Content-Type':'text/plain'},redirect:'follow'})
  .then(function(r){
    if(!r.ok&&r.status!==0) throw new Error(r.status);
    statusEl.textContent='✅ 점수 저장 완료! 아래 랭킹 보드를 새로고침하세요.';
    statusEl.style.color='#6ee7b7';
  }).catch(function(){
    statusEl.textContent='⚠️ 점수 저장 실패. 잠시 후 다시 시도하세요.';
    statusEl.style.color='#fca5a5';
  });
}

function restartGame(){
  document.getElementById('resultScreen').style.display='none';
  document.getElementById('nameScreen').style.display='block';
  document.getElementById('nameInput').value=GS.name;
  setTimeout(notifyH,40);
}
</script>
</body>
</html>"""


def _build_html(short_id: str, user_name: str) -> str:
    init = (
        '<script>const _U={id:' + json.dumps(short_id)
        + ',name:' + json.dumps(user_name)
        + ',gasUrl:' + json.dumps(str(_GAS_URL)) + '};</script>'
    )
    return _HTML_RAW.replace('</head>', init + '</head>', 1)


@st.cache_data(ttl=60, show_spinner=False)
def _load_ranking_data(sheet_id: str) -> tuple:
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        creds = Credentials.from_service_account_info(
            dict(st.secrets["gcp_service_account"]),
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        client = gspread.authorize(creds)
        sh = client.open_by_key(str(sheet_id))
        try:
            ws = sh.worksheet(_RANKING_SHEET)
        except Exception:
            # 시트 이름이 약간 다를 경우 유사 이름으로 매칭
            all_ws = sh.worksheets()
            ws = next(
                (w for w in all_ws if "랭킹" in w.title and "연립" in w.title),
                None,
            )
            if ws is None:
                titles = [w.title for w in all_ws]
                return [], f"'{_RANKING_SHEET}' 시트를 찾을 수 없습니다.\n현재 시트 목록: {titles}"
        return ws.get_all_records(), None
    except Exception as e:
        return [], str(e)


def _render_ranking() -> None:
    st.subheader("🏆 스피드퀴즈 랭킹")
    _, col_btn = st.columns([5, 1])
    with col_btn:
        if st.button("🔄 새로고침", key="rank_refresh_btn_simq"):
            st.cache_data.clear()
            st.rerun()

    sheet_id = st.secrets.get("reflection_spreadsheet_common", "")
    if not sheet_id:
        st.error("⚠️ secrets에 `reflection_spreadsheet_common` 키가 없습니다.")
        return

    records, err = _load_ranking_data(sheet_id)

    if err:
        st.error(f"랭킹을 불러오지 못했습니다.\n\n```\n{err}\n```")
        return

    if not records:
        st.info("아직 도전 기록이 없습니다. 첫 번째 도전자가 되어보세요! 🎯")
        return

    # 학번별 최고점 집계
    best: dict = {}
    for r in records:
        sid  = str(r.get("학번", "")).strip()
        name = str(r.get("이름", "")).strip()
        try:
            score = int(r.get("점수", 0) or 0)
        except (ValueError, TypeError):
            score = 0
        try:
            ok    = int(r.get("정답", 0) or 0)
            total = int(r.get("문제수", 0) or 0)
        except (ValueError, TypeError):
            ok, total = 0, 0
        if sid and (sid not in best or score > best[sid]["최고점"]):
            best[sid] = {"학번": sid, "이름": name, "최고점": score, "정답": ok, "문제수": total}

    ranked = sorted(best.values(), key=lambda x: -x["최고점"])

    if not ranked:
        # records는 있지만 학번이 빈 행만 있는 경우 — 로그인 없이 게임한 경우
        first_keys = list(records[0].keys()) if records else []
        st.warning(
            f"🔍 시트에서 {len(records)}개 행을 읽었지만 학번 정보가 없어 표시할 수 없습니다.\n\n"
            f"로그인 상태에서 게임을 완료해야 랭킹에 기록됩니다.\n"
            f"(실제 시트 컬럼: `{first_keys}`)"
        )
        return

    cur_id   = st.session_state.get("_user_id", "")
    short_me = cur_id[4:] if len(cur_id) >= 9 and cur_id[:2] == "20" else cur_id

    medals = ["🥇", "🥈", "🥉"]
    rows_html = ""
    for i, row in enumerate(ranked[:20]):
        medal  = medals[i] if i < 3 else f"{i + 1}위"
        is_me  = row["학번"] == short_me
        tr_sty = ' style="background:rgba(124,58,237,.12);outline:2px solid rgba(124,58,237,.3);"' if is_me else ""
        me_tag = " &nbsp;<span style='color:#a78bfa;font-size:11px'>← 나</span>" if is_me else ""
        rate   = f"{round(row['정답'] / row['문제수'] * 100)}%" if row["문제수"] > 0 else "—"
        rows_html += (
            f"<tr{tr_sty}>"
            f"<td style='text-align:center;font-size:18px'>{medal}</td>"
            f"<td><strong>{row['이름']}</strong>{me_tag}</td>"
            f"<td style='text-align:right;font-weight:800;color:#7c3aed'>{row['최고점']:,}점</td>"
            f"<td style='text-align:center;font-size:12px;color:#6b7280'>"
            f"{row['정답']}/{row['문제수']} ({rate})</td>"
            f"</tr>"
        )

    table_html = (
        "<style>"
        ".rank-tbl{width:100%;border-collapse:collapse;font-size:14px}"
        ".rank-tbl th{padding:7px 10px;"
        "color:#6b7280;font-size:11px;letter-spacing:.05em;text-transform:uppercase;"
        "border-bottom:2px solid rgba(139,92,246,.2)}"
        ".rank-tbl td{padding:8px 10px;border-bottom:1px solid rgba(139,92,246,.08)}"
        ".rank-tbl tr:hover td{background:rgba(139,92,246,.05)}"
        "</style>"
        "<table class='rank-tbl'>"
        "<thead><tr>"
        "<th style='width:52px'>순위</th><th>이름</th>"
        "<th style='text-align:right'>최고점</th>"
        "<th style='text-align:center'>정답/문제</th>"
        "</tr></thead>"
        f"<tbody>{rows_html}</tbody></table>"
    )
    st.markdown(table_html, unsafe_allow_html=True)


def render():
    user_id   = st.session_state.get("_user_id", "")
    user_name = st.session_state.get("_user_name", "")
    short_id  = (user_id[4:] if len(user_id) >= 9 and user_id[:2] == "20" else user_id)

    components.html(_build_html(short_id, user_name), height=1200, scrolling=False)
    st.markdown("---")
    _render_ranking()
    st.markdown("---")
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()
