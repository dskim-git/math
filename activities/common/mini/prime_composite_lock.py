"""
소수·합성수 잠금 해제
인수분해 공식을 이용해 큰 수가 소수인지 합성수인지 판단하는 활동
"""

import streamlit as st
import streamlit.components.v1 as components

from reflection_utils import render_reflection_form

_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "소수합성수잠금해제"

_QUESTIONS = [
    {
        "type": "markdown",
        "text": "**📝 오늘처럼 큰 수를 식으로 다시 보고 인수분해하는 활동을 떠올리며 스스로 문제를 만들어 보세요.**",
    },
    {
        "key": "문제1",
        "label": "문제 1 : 세제곱의 합, 세제곱의 차, 제곱의 차, 완전제곱식 중 하나를 이용해 큰 수 하나를 직접 만드세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "답1",
        "label": "문제 1의 답 : 그 수를 어떤 식으로 다시 쓰고, 어떻게 인수분해해서 합성수임을 설명할지 적어 보세요.",
        "type": "text_area",
        "height": 100,
    },
    {
        "key": "문제2",
        "label": "문제 2 : 오늘 활동에서 가장 흥미로웠던 큰 수 하나를 고르고, 어떤 단서 때문에 적절한 공식을 떠올렸는지 써 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "답2",
        "label": "문제 2의 답 : 그 수가 소수인지 합성수인지 한 문장으로 판정하고, 이유를 써 보세요.",
        "type": "text_area",
        "height": 100,
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점", "label": "💬 느낀 점", "type": "text_area", "height": 90},
]

META = {
    "title": "🔐 소수·합성수 잠금 해제",
    "description": "큰 수를 적절한 식으로 다시 보고 인수분해 공식을 골라 소수인지 합성수인지 판정하는 잠금 해제형 활동입니다.",
    "order": 109,
}

_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>소수·합성수 잠금 해제</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg1:#07111f;
  --bg2:#13233b;
  --panel:#081424dd;
  --line:#dbeafe29;
  --gold:#fbbf24;
  --mint:#4ade80;
  --sky:#38bdf8;
  --rose:#fb7185;
  --ink:#eef6ff;
  --soft:#b9cbe4;
}
body{
  font-family:'SUIT','Pretendard','Noto Sans KR',sans-serif;
  min-height:100vh;
  color:var(--ink);
  background:
    radial-gradient(circle at 8% 8%,rgba(251,191,36,.22),transparent 25%),
    radial-gradient(circle at 92% 14%,rgba(56,189,248,.20),transparent 24%),
    radial-gradient(circle at 72% 88%,rgba(74,222,128,.14),transparent 28%),
    linear-gradient(165deg,var(--bg1) 0%,#0d1a2f 42%,var(--bg2) 100%);
  padding:14px 10px 28px;
}
.shell{max-width:1160px;margin:0 auto}
.hero{
  position:relative;
  overflow:hidden;
  border-radius:28px;
  border:1px solid rgba(255,255,255,.12);
  background:linear-gradient(135deg,rgba(15,27,45,.94),rgba(8,20,36,.86));
  box-shadow:0 28px 80px rgba(0,0,0,.34);
  padding:24px 22px 20px;
}
.hero:before,.hero:after{content:'';position:absolute;border-radius:999px;pointer-events:none}
.hero:before{width:300px;height:300px;right:-110px;top:-140px;background:radial-gradient(circle,rgba(251,191,36,.18),transparent 70%)}
.hero:after{width:240px;height:240px;left:-90px;bottom:-130px;background:radial-gradient(circle,rgba(56,189,248,.14),transparent 70%)}
.eyebrow{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;border-radius:999px;background:rgba(251,191,36,.12);border:1px solid rgba(251,191,36,.24);color:#fde68a;font-size:.77rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px}
.hero-grid{display:grid;grid-template-columns:1.15fr .85fr;gap:14px;align-items:start}
.hero h1{font-size:2rem;line-height:1.18;margin-bottom:10px}
.hero p{max-width:760px;color:#c9daef;line-height:1.76;font-size:.95rem}
.comic-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.bubble{
  min-height:118px;
  padding:14px 14px 12px;
  border-radius:18px;
  border:1px solid rgba(255,255,255,.12);
  background:linear-gradient(160deg,rgba(12,24,41,.92),rgba(20,35,58,.88));
  position:relative;
}
.bubble:after{
  content:'';
  position:absolute;
  bottom:-12px;
  left:22px;
  width:20px;height:20px;
  background:inherit;
  border-left:1px solid rgba(255,255,255,.08);
  border-bottom:1px solid rgba(255,255,255,.08);
  transform:rotate(-45deg);
}
.bubble h3{font-size:.84rem;color:#a5f3fc;margin-bottom:7px}
.bubble p{font-size:.8rem;color:#c8d6ea;line-height:1.6}

.formula-deck{
  margin-top:14px;
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:10px;
}
.formula-card{
  border-radius:18px;
  border:1px solid rgba(255,255,255,.11);
  background:linear-gradient(145deg,rgba(10,23,40,.92),rgba(15,27,45,.82));
  padding:14px;
  min-height:118px;
}
.formula-card strong{display:block;font-size:.82rem;color:#fef3c7;margin-bottom:8px}
.formula-card .math{min-height:42px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.05rem;margin-bottom:8px}
.formula-card p{font-size:.77rem;color:#b8cae2;line-height:1.55}

.board{display:grid;grid-template-columns:1.2fr .8fr;gap:14px;margin-top:16px}
.panel{
  border-radius:24px;
  border:1px solid var(--line);
  background:var(--panel);
  backdrop-filter:blur(10px);
  padding:16px;
}
.panel-title{display:flex;align-items:center;gap:8px;font-size:.92rem;font-weight:900;color:#93c5fd;margin-bottom:10px}

.hud{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.hud-card{padding:14px;border-radius:18px;background:linear-gradient(180deg,rgba(16,28,47,.88),rgba(11,19,32,.88));border:1px solid rgba(255,255,255,.09)}
.hud-label{font-size:.75rem;color:#8fa8c9;margin-bottom:6px}
.hud-value{font-size:1.28rem;font-weight:900;color:#f8fbff}
.hud-sub{font-size:.79rem;color:#aec4df;margin-top:4px}

.mission-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;flex-wrap:wrap;margin-bottom:12px}
.case-tag{display:inline-flex;align-items:center;gap:8px;padding:6px 11px;border-radius:999px;background:rgba(56,189,248,.12);border:1px solid rgba(125,211,252,.22);color:#a5f3fc;font-size:.76rem;font-weight:900;margin-bottom:8px}
.mission-title{font-size:1.28rem;font-weight:900;color:#fff;margin-bottom:8px}
.mission-note{font-size:.9rem;color:#bfd0e6;line-height:1.7;max-width:720px}
.number-box{
  min-width:260px;
  border-radius:20px;
  background:linear-gradient(180deg,rgba(13,22,37,.96),rgba(9,17,28,.92));
  border:1px solid rgba(255,255,255,.12);
  padding:16px;
  text-align:center;
}
.number-label{font-size:.74rem;color:#90a8ca;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px}
.number-value{font-size:2rem;font-weight:900;letter-spacing:.04em;color:#fdf4bf;word-break:break-word}

.stage-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.stage-card{
  border-radius:22px;
  background:linear-gradient(180deg,rgba(9,17,29,.92),rgba(13,22,37,.9));
  border:1px solid rgba(255,255,255,.1);
  padding:16px;
  display:flex;
  flex-direction:column;
  gap:12px;
  min-height:400px;
}
.stage-head{display:flex;justify-content:space-between;gap:10px;align-items:flex-start}
.stage-left{display:flex;gap:10px;align-items:flex-start}
.stage-num{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:rgba(56,189,248,.16);border:1px solid rgba(125,211,252,.3);color:#a5f3fc;font-weight:900;flex-shrink:0}
.stage-name{font-size:1rem;font-weight:900;color:#fff}
.stage-desc{font-size:.82rem;line-height:1.6;color:#97b1cc;margin-top:4px}
.status{padding:5px 10px;border-radius:999px;font-size:.72rem;font-weight:900;white-space:nowrap}
.status.live{background:rgba(56,189,248,.14);color:#a5f3fc}
.status.lock{background:rgba(100,116,139,.18);color:#94a3b8}
.status.done{background:rgba(34,197,94,.16);color:#c7f9d4}
.tip{padding:11px 12px;border-radius:14px;background:rgba(251,191,36,.08);border:1px solid rgba(251,191,36,.18);font-size:.82rem;line-height:1.65;color:#fde68a}

.option-wrap{display:flex;flex-direction:column;gap:8px}
.choice{
  width:100%;
  text-align:left;
  border-radius:16px;
  border:1px solid rgba(255,255,255,.12);
  background:linear-gradient(135deg,rgba(14,26,44,.95),rgba(16,30,49,.86));
  padding:12px;
  color:#edf6ff;
  cursor:pointer;
  transition:transform .16s,box-shadow .16s,border-color .16s,background .16s;
}
.choice:hover{transform:translateY(-1px);box-shadow:0 12px 24px rgba(2,8,23,.32);border-color:rgba(125,211,252,.34)}
.choice.selected{border-color:#fcd34d;background:linear-gradient(135deg,rgba(72,48,12,.95),rgba(31,41,67,.92))}
.choice.correct{border-color:#4ade80;background:linear-gradient(135deg,rgba(13,52,31,.96),rgba(14,37,28,.92))}
.choice.wrong{border-color:#fb7185;background:linear-gradient(135deg,rgba(57,17,31,.96),rgba(38,21,33,.92))}
.choice.locked{opacity:.45;cursor:not-allowed;pointer-events:none}
.choice-label{font-size:.74rem;color:#8ba5c8;font-weight:800;letter-spacing:.04em;text-transform:uppercase;margin-bottom:7px}
.choice-math{min-height:26px;display:flex;align-items:center;color:#fff;font-size:1rem}
.choice-text{font-size:.84rem;line-height:1.55;color:#d9e8f8}

.verdict-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.verdict-btn{
  padding:14px 10px;
  border-radius:16px;
  border:1px solid rgba(255,255,255,.12);
  background:linear-gradient(135deg,rgba(14,26,44,.95),rgba(16,30,49,.86));
  color:#f1f7ff;
  font-size:.95rem;
  font-weight:900;
  cursor:pointer;
  transition:transform .16s,border-color .16s,box-shadow .16s,background .16s;
}
.verdict-btn:hover{transform:translateY(-1px);box-shadow:0 10px 20px rgba(2,8,23,.28)}
.verdict-btn.selected{border-color:#fcd34d;background:linear-gradient(135deg,rgba(72,48,12,.95),rgba(31,41,67,.92))}
.verdict-btn.correct{border-color:#4ade80;background:linear-gradient(135deg,rgba(13,52,31,.96),rgba(14,37,28,.92))}
.verdict-btn.wrong{border-color:#fb7185;background:linear-gradient(135deg,rgba(57,17,31,.96),rgba(38,21,33,.92))}
.verdict-btn.locked{opacity:.45;cursor:not-allowed;pointer-events:none}

.hint{display:none;padding:11px 12px;border-radius:14px;background:rgba(56,189,248,.1);border:1px solid rgba(103,232,249,.24);font-size:.82rem;line-height:1.7;color:#cffafe}
.hint.show{display:block}
.feedback{min-height:24px;font-size:.86rem;font-weight:900}
.feedback.ok{color:#86efac}
.feedback.ng{color:#fda4af}

.btn-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:auto}
.stage-card .btn-row{margin-top:6px}
.btn{
  border:none;
  border-radius:999px;
  padding:9px 14px;
  font-size:.83rem;
  font-weight:900;
  cursor:pointer;
  transition:transform .16s,filter .16s;
}
.btn:hover{transform:translateY(-1px);filter:brightness(1.05)}
.btn-check{background:linear-gradient(135deg,#f59e0b,#f97316);color:#fff}
.btn-hint{background:rgba(56,189,248,.14);border:1px solid rgba(103,232,249,.3);color:#a5f3fc}
.btn-reset{background:rgba(100,116,139,.22);color:#dbeafe}
.btn-next{background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;display:none}

.reveal{
  margin-top:14px;
  border-radius:22px;
  padding:18px;
  background:linear-gradient(135deg,rgba(22,163,74,.16),rgba(37,99,235,.14));
  border:1px solid rgba(134,239,172,.22);
  display:none;
}
.reveal.show{display:block;animation:pop .3s ease}
.reveal h3{font-size:1.05rem;color:#ecfdf5;margin-bottom:8px}
.reveal p{font-size:.92rem;color:#d9fbe4;line-height:1.8}
.factor-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.factor-badge{padding:7px 11px;border-radius:999px;background:rgba(240,253,244,.12);border:1px solid rgba(187,247,208,.28);color:#f0fdf4;font-size:.83rem;font-weight:900}

.summary{
  margin-top:14px;
  border-radius:22px;
  padding:18px;
  background:linear-gradient(135deg,rgba(251,191,36,.16),rgba(56,189,248,.14));
  border:1px solid rgba(253,224,71,.22);
  display:none;
}
.summary.show{display:block}
.summary h3{font-size:1.14rem;margin-bottom:8px;color:#fff7cc}
.summary p{font-size:.92rem;line-height:1.75;color:#f8fbff}

.lab-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}
.lab-card{
  border-radius:20px;
  border:1px solid rgba(255,255,255,.1);
  background:linear-gradient(180deg,rgba(11,20,34,.94),rgba(14,24,39,.88));
  padding:16px;
}
.lab-tabs{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
.lab-tab{
  padding:8px 12px;
  border-radius:999px;
  border:1px solid rgba(255,255,255,.12);
  background:rgba(15,25,41,.9);
  color:#dbeafe;
  font-size:.8rem;
  font-weight:900;
  cursor:pointer;
}
.lab-tab.active{border-color:#67e8f9;background:rgba(8,145,178,.16);color:#cffafe}
.lab-controls{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.field{display:flex;flex-direction:column;gap:6px}
.field label{font-size:.77rem;color:#9fb8d4;font-weight:800}
.field input{
  border-radius:12px;
  border:1px solid rgba(255,255,255,.14);
  background:rgba(12,23,38,.92);
  color:#f8fbff;
  padding:10px 12px;
  font-size:.95rem;
  font-weight:800;
}
.field input:focus{outline:none;border-color:#67e8f9;box-shadow:0 0 0 3px rgba(34,211,238,.12)}
.field-static{
  border-radius:12px;
  border:1px solid rgba(255,255,255,.14);
  background:rgba(12,23,38,.92);
  color:#dbeafe;
  padding:10px 12px;
  font-size:.9rem;
  font-weight:800;
  min-height:44px;
  display:flex;
  align-items:center;
}
.lab-math{min-height:56px;border-radius:16px;background:rgba(8,16,28,.86);border:1px solid rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center;padding:12px;margin:12px 0;color:#fff;font-size:1.08rem}
.lab-result{padding:13px 14px;border-radius:16px;background:rgba(34,197,94,.08);border:1px solid rgba(74,222,128,.2);font-size:.87rem;line-height:1.75;color:#dcfce7}
.lab-note{font-size:.79rem;line-height:1.6;color:#b7cae3}

@keyframes pop{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}

@media (max-width:1080px){
  .hero-grid,.board,.lab-grid{grid-template-columns:1fr}
  .formula-deck{grid-template-columns:repeat(2,1fr)}
  .hud{grid-template-columns:repeat(2,1fr)}
  .stage-grid{grid-template-columns:1fr}
}
@media (max-width:640px){
  body{padding:10px 8px 22px}
  .hero{padding:18px 16px}
  .hero h1{font-size:1.58rem}
  .comic-strip,.formula-deck,.hud,.lab-controls{grid-template-columns:1fr}
  .number-value{font-size:1.55rem}
}
</style>
</head>
<body>
<div class="shell">
  <section class="hero">
    <div class="eyebrow">Prime Or Composite Vault</div>
    <div class="hero-grid">
      <div>
        <h1>🔐 소수·합성수 잠금 해제</h1>
        <p>
          거대한 숫자가 보인다고 바로 겁먹을 필요는 없습니다. 숫자를 그대로 보지 말고,
          <strong>익숙한 식의 값</strong>으로 다시 보면 숨어 있던 인수분해 공식이 튀어나옵니다.
          각 사건에서 숫자의 변장을 벗기고, 맞는 공식을 선택해 금고가 <strong>소수 문</strong>인지 <strong>합성수 문</strong>인지 판정해 보세요.
        </p>
      </div>

      <div class="comic-strip">
        <article class="bubble">
          <h3>단서 1</h3>
          <p>1,000,000이나 27처럼 익숙한 완전거듭제곱이 보이면 세제곱의 합·차를 먼저 의심합니다.</p>
        </article>
        <article class="bubble">
          <h3>단서 2</h3>
          <p>1000, 100, 10 같은 기준 수를 넣어 보면 다항식의 인수분해 공식을 숫자 판별에 바로 연결할 수 있습니다.</p>
        </article>
        <article class="bubble">
          <h3>단서 3</h3>
          <p>인수분해가 되어서 두 인수가 모두 1보다 크면 그 순간 그 수는 합성수로 확정됩니다.</p>
        </article>
      </div>
    </div>

    <div class="formula-deck">
      <article class="formula-card">
        <strong>세제곱의 합</strong>
        <div class="math" data-math="a^3+b^3=(a+b)(a^2-ab+b^2)"></div>
        <p>큰 수를 두 세제곱의 합으로 볼 수 있으면 바로 두 인수로 나눌 수 있습니다.</p>
      </article>
      <article class="formula-card">
        <strong>세제곱의 차</strong>
        <div class="math" data-math="a^3-b^3=(a-b)(a^2+ab+b^2)"></div>
        <p>조금 덜 떨어져 보이는 수라도 가까운 세제곱끼리의 차일 수 있습니다.</p>
      </article>
      <article class="formula-card">
        <strong>제곱의 차</strong>
        <div class="math" data-math="a^2-b^2=(a-b)(a+b)"></div>
        <p>거대한 수라도 기준 수의 앞뒤 한 칸 차이면 빠르게 분해됩니다.</p>
      </article>
      <article class="formula-card">
        <strong>특별한 다항식</strong>
        <div class="math" data-math="x^4-3x^2+1=(x^2+x-1)(x^2-x-1)"></div>
        <p>다항식 인수분해를 특정 값 대입과 연결하면 큰 수 판별 도구가 됩니다.</p>
      </article>
    </div>
  </section>

  <section class="board">
    <section class="panel">
      <div class="panel-title">🛰️ 사건 진행 현황</div>
      <div class="hud">
        <div class="hud-card">
          <div class="hud-label">현재 사건</div>
          <div class="hud-value" id="caseNow">1 / 6</div>
          <div class="hud-sub">순서대로 해제</div>
        </div>
        <div class="hud-card">
          <div class="hud-label">해제 성공</div>
          <div class="hud-value" id="caseSolved">0</div>
          <div class="hud-sub">총 6개</div>
        </div>
        <div class="hud-card">
          <div class="hud-label">연속 성공</div>
          <div class="hud-value" id="streakNow">0</div>
          <div class="hud-sub" id="bestStreak">최고 기록 0</div>
        </div>
        <div class="hud-card">
          <div class="hud-label">힌트 사용</div>
          <div class="hud-value" id="hintCount">0</div>
          <div class="hud-sub">적게 쓸수록 좋음</div>
        </div>
      </div>
    </section>

    <section class="panel">
      <div class="panel-title">🔍 잠금 해제 규칙</div>
      <div style="font-size:.9rem;line-height:1.78;color:#c9daef">
        1단계에서 숫자를 어떤 식으로 볼지 고르고,<br>
        2단계에서 맞는 인수분해 공식을 선택한 뒤,<br>
        3단계에서 <strong>소수</strong>인지 <strong>합성수</strong>인지 판정합니다.<br><br>
        핵심은 계산을 길게 하는 것이 아니라, <strong>적절한 구조를 먼저 알아보는 것</strong>입니다.
      </div>
    </section>
  </section>

  <section class="panel" style="margin-top:14px">
    <div class="mission-head">
      <div>
        <div class="case-tag" id="caseTag">사건 1</div>
        <div class="mission-title" id="caseTitle">거대한 수의 변장을 벗겨라</div>
        <div class="mission-note" id="caseStory"></div>
      </div>
      <div class="number-box">
        <div class="number-label">금고에 적힌 수</div>
        <div class="number-value" id="caseNumber"></div>
      </div>
    </div>

    <div class="stage-grid">
      <section class="stage-card" id="stage1Card">
        <div class="stage-head">
          <div class="stage-left">
            <div class="stage-num">1</div>
            <div>
              <div class="stage-name">식으로 다시 보기</div>
              <div class="stage-desc" id="rewritePrompt"></div>
            </div>
          </div>
          <div class="status live" id="status1">진행 중</div>
        </div>
        <div class="tip">큰 수를 그대로 계산하지 말고, 1000, 100, 10 같은 기준 수와 완전거듭제곱을 먼저 떠올려 보세요.</div>
        <div class="option-wrap" id="rewriteOptions"></div>
        <div class="hint" id="hint1"></div>
        <div class="feedback" id="feedback1"></div>
        <div class="btn-row">
          <button class="btn btn-check" onclick="checkStage('rewrite')">단서 확인</button>
          <button class="btn btn-hint" onclick="showHint(1)">힌트</button>
          <button class="btn btn-reset" onclick="resetStage('rewrite')">선택 초기화</button>
        </div>
      </section>

      <section class="stage-card" id="stage2Card">
        <div class="stage-head">
          <div class="stage-left">
            <div class="stage-num">2</div>
            <div>
              <div class="stage-name">맞는 인수분해 고르기</div>
              <div class="stage-desc" id="factorPrompt"></div>
            </div>
          </div>
          <div class="status lock" id="status2">잠김</div>
        </div>
        <div class="tip">공식의 부호와 가운데 항의 부호를 끝까지 정확히 비교해야 합니다.</div>
        <div class="option-wrap" id="factorOptions"></div>
        <div class="hint" id="hint2"></div>
        <div class="feedback" id="feedback2"></div>
        <div class="btn-row">
          <button class="btn btn-check" onclick="checkStage('factor')">공식 매칭</button>
          <button class="btn btn-hint" onclick="showHint(2)">힌트</button>
          <button class="btn btn-reset" onclick="resetStage('factor')">선택 초기화</button>
        </div>
      </section>

      <section class="stage-card" id="stage3Card">
        <div class="stage-head">
          <div class="stage-left">
            <div class="stage-num">3</div>
            <div>
              <div class="stage-name">소수인가, 합성수인가</div>
              <div class="stage-desc">인수분해 결과를 근거로 최종 판정을 내려 보세요.</div>
            </div>
          </div>
          <div class="status lock" id="status3">잠김</div>
        </div>
        <div class="tip">두 인수가 모두 1보다 크면 합성수입니다. 소수는 1과 자기 자신만 인수로 가집니다.</div>
        <div class="verdict-grid" id="verdictOptions"></div>
        <div class="hint" id="hint3"></div>
        <div class="feedback" id="feedback3"></div>
        <div class="btn-row">
          <button class="btn btn-check" onclick="checkStage('verdict')">판정 확정</button>
          <button class="btn btn-hint" onclick="showHint(3)">힌트</button>
          <button class="btn btn-reset" onclick="resetStage('verdict')">선택 초기화</button>
          <button class="btn btn-next" id="nextBtn" onclick="nextCase()">다음 사건</button>
        </div>
      </section>
    </div>

    <section class="reveal" id="revealBox">
      <h3>✅ 잠금 해제 완료</h3>
      <p id="revealText"></p>
      <div class="factor-row" id="factorRow"></div>
    </section>

    <section class="summary" id="summaryBox">
      <h3>🏁 모든 금고 해제 완료</h3>
      <p>
        이제 큰 수를 봐도 먼저 <strong>어떤 식의 값인지</strong>를 떠올리며 접근할 수 있어야 합니다.
        인수분해 공식은 다항식 문제 안에서만 쓰이는 것이 아니라, 숫자의 성질을 판별하는 도구로도 연결됩니다.
      </p>
    </section>
  </section>

  <section class="lab-grid">
    <section class="lab-card">
      <div class="panel-title">🧪 직접 큰 수 만들기</div>
      <div class="lab-tabs">
        <button class="lab-tab active" id="tab-sum3" onclick="setLabMode('sum3')">세제곱의 합</button>
        <button class="lab-tab" id="tab-diff3" onclick="setLabMode('diff3')">세제곱의 차</button>
        <button class="lab-tab" id="tab-quartic" onclick="setLabMode('quartic')">특별한 다항식</button>
      </div>
      <div class="lab-controls" id="labControls"></div>
      <div class="lab-math" id="labMath"></div>
      <div class="lab-result" id="labResult"></div>
    </section>

    <section class="lab-card">
      <div class="panel-title">📝 활동 포인트</div>
      <div class="lab-note">
        큰 수가 나와도 바로 소수 판별 알고리즘으로 뛰어들기보다, 먼저 <strong>익숙한 구조를 발견하는 눈</strong>을 기르는 것이 중요합니다.<br><br>
        1. 완전제곱수, 완전세제곱수와 얼마나 가까운지 본다.<br>
        2. 1000, 100, 10 같은 기준 수를 대입한 다항식 형태가 있는지 본다.<br>
        3. 적절한 인수분해 공식을 떠올린다.<br>
        4. 인수 두 개가 모두 1보다 크면 합성수라고 판정한다.<br><br>
        아래 성찰 기록에는 직접 만든 큰 수 문제와 판정 과정을 남겨 보세요.
      </div>
    </section>
  </section>
</div>

<script>
const CASES = [
  {
    tag:'사건 1',
    title:'만화 속 첫 번째 금고',
    number:'1,000,027',
    story:'1,000,000과 27이 보이면 세제곱의 합을 떠올릴 수 있어야 합니다. 숫자의 변장을 벗겨 보세요.',
    rewritePrompt:'이 수를 가장 자연스럽게 다시 쓴 식을 고르세요.',
    rewriteOptions:[
      {kind:'math', value:'100^3+3^3', correct:true},
      {kind:'math', value:'10^6+3^2', correct:false},
      {kind:'math', value:'103^3', correct:false}
    ],
    factorPrompt:'선택한 식에 맞는 인수분해 결과를 고르세요.',
    factorOptions:[
      {kind:'math', value:'(100+3)(100^2-100\\cdot 3+3^2)', correct:true},
      {kind:'math', value:'(100-3)(100^2+100\\cdot 3+3^2)', correct:false},
      {kind:'math', value:'(100+3)^3', correct:false}
    ],
    verdict:'합성수',
    factors:['103','9709'],
    reveal:'\\(1,000,027 = 103 \\times 9709\\) 이므로 합성수입니다.',
    hint1:'1,000,000은 100의 세제곱이고, 27은 3의 세제곱입니다.',
    hint2:'\\(a^3+b^3=(a+b)(a^2-ab+b^2)\\) 꼴입니다.',
    hint3:'103과 9709는 둘 다 1보다 크므로 소수가 될 수 없습니다.'
  },
  {
    tag:'사건 2',
    title:'가까운 세제곱의 차를 찾아라',
    number:'7,999,973',
    story:'8,000,000 바로 아래에 있는 숫자입니다. 8,000,000이 어떤 거듭제곱인지 떠올려 보세요.',
    rewritePrompt:'이 수를 가장 자연스럽게 다시 쓴 식을 고르세요.',
    rewriteOptions:[
      {kind:'math', value:'200^3-3^3', correct:true},
      {kind:'math', value:'20^4-3^3', correct:false},
      {kind:'math', value:'199^3+2^3', correct:false}
    ],
    factorPrompt:'세제곱의 차 공식에 맞는 식을 고르세요.',
    factorOptions:[
      {kind:'math', value:'(200-3)(200^2+200\\cdot 3+3^2)', correct:true},
      {kind:'math', value:'(200+3)(200^2-200\\cdot 3+3^2)', correct:false},
      {kind:'math', value:'(200-3)^3', correct:false}
    ],
    verdict:'합성수',
    factors:['197','40609'],
    reveal:'\\(7,999,973 = 197 \\times 40,609\\) 이므로 합성수입니다.',
    hint1:'8,000,000은 200의 세제곱이고, 27은 3의 세제곱입니다.',
    hint2:'\\(a^3-b^3=(a-b)(a^2+ab+b^2)\\) 꼴입니다.',
    hint3:'197과 40,609라는 두 인수로 나누어지므로 합성수입니다.'
  },
  {
    tag:'사건 3',
    title:'다항식 금고의 비밀',
    number:'99,970,001',
    story:'이 숫자는 100을 대입한 다항식 값으로 볼 수 있습니다. PPT 속 인수분해 공식을 숫자 판정에 연결해 보세요.',
    rewritePrompt:'어떤 다항식에 x=100을 넣은 값인지 고르세요.',
    rewriteOptions:[
      {kind:'math', value:'100^4-3\\cdot 100^2+1', correct:true},
      {kind:'math', value:'100^4-3\\cdot 100+1', correct:false},
      {kind:'math', value:'100^2-3\\cdot 100^4+1', correct:false}
    ],
    factorPrompt:'x^4-3x^2+1의 인수분해 결과에 맞는 것을 고르세요.',
    factorOptions:[
      {kind:'math', value:'(100^2+100-1)(100^2-100-1)', correct:true},
      {kind:'math', value:'(100^2+100+1)(100^2-100+1)', correct:false},
      {kind:'math', value:'(100^2-1)^2', correct:false}
    ],
    verdict:'합성수',
    factors:['10099','9899'],
    reveal:'\\(99,970,001 = 10,099 \\times 9,899\\) 이므로 합성수입니다.',
    hint1:'\\(100^4-3\\cdot100^2+1\\) 모양을 확인해 보세요.',
    hint2:'\\(x^4-3x^2+1=(x^2+x-1)(x^2-x-1)\\) 입니다.',
    hint3:'10,099와 9,899가 둘 다 1보다 크므로 합성수입니다.'
  },
  {
    tag:'사건 4',
    title:'완전제곱 함정 문',
    number:'1,002,001',
    story:'앞뒤가 비슷한 숫자가 반복되면 완전제곱식을 의심할 수 있습니다. 1000을 기준으로 다시 보세요.',
    rewritePrompt:'이 수를 가장 자연스럽게 다시 쓴 식을 고르세요.',
    rewriteOptions:[
      {kind:'math', value:'1000^2+2\\cdot1000+1', correct:true},
      {kind:'math', value:'1000^2-2\\cdot1000+1', correct:false},
      {kind:'math', value:'100^3+2^3+1', correct:false}
    ],
    factorPrompt:'완전제곱식 인수분해 결과를 고르세요.',
    factorOptions:[
      {kind:'math', value:'(1000+1)^2', correct:true},
      {kind:'math', value:'(1000-1)^2', correct:false},
      {kind:'math', value:'(1000+1)(1000-1)', correct:false}
    ],
    verdict:'합성수',
    factors:['1001','1001'],
    reveal:'\\(1,002,001 = 1,001 \\times 1,001\\) 이므로 합성수입니다.',
    hint1:'\\(a^2+2ab+b^2\\) 꼴에서 \\(a=1000, b=1\\) 입니다.',
    hint2:'완전제곱식은 같은 인수가 두 번 곱해진 꼴로 바뀝니다.',
    hint3:'1,001이 두 번 곱해진 수이므로 합성수입니다.'
  },
  {
    tag:'사건 5',
    title:'앞뒤 한 칸 차이 금고',
    number:'999,999',
    story:'1,000,000보다 1 작은 수입니다. 기준 수 1000을 중심으로 제곱의 차를 떠올려 보세요.',
    rewritePrompt:'이 수를 가장 자연스럽게 다시 쓴 식을 고르세요.',
    rewriteOptions:[
      {kind:'math', value:'1000^2-1^2', correct:true},
      {kind:'math', value:'1000^2+1^2', correct:false},
      {kind:'math', value:'100^3-1', correct:false}
    ],
    factorPrompt:'제곱의 차 공식에 맞는 결과를 고르세요.',
    factorOptions:[
      {kind:'math', value:'(1000-1)(1000+1)', correct:true},
      {kind:'math', value:'(1000-1)^2', correct:false},
      {kind:'math', value:'(1000+1)^2', correct:false}
    ],
    verdict:'합성수',
    factors:['999','1001'],
    reveal:'\\(999,999 = 999 \\times 1,001\\) 이므로 합성수입니다.',
    hint1:'\\(a^2-b^2=(a-b)(a+b)\\) 로 분해됩니다.',
    hint2:'\\(1000^2-1^2\\) 는 가운데 항이 없는 제곱의 차입니다.',
    hint3:'999와 1,001이 둘 다 1보다 크므로 합성수입니다.'
  },
  {
    tag:'보너스 사건',
    title:'초대형 마지막 금고',
    number:'1,000,000,001',
    story:'10억보다 1 큰 수입니다. 1000의 세제곱과 연결하면 계산 없이도 판정할 수 있습니다.',
    rewritePrompt:'이 수를 가장 자연스럽게 다시 쓴 식을 고르세요.',
    rewriteOptions:[
      {kind:'math', value:'1000^3+1^3', correct:true},
      {kind:'math', value:'100^4+1', correct:false},
      {kind:'math', value:'1001^3', correct:false}
    ],
    factorPrompt:'세제곱의 합 공식에 맞는 결과를 고르세요.',
    factorOptions:[
      {kind:'math', value:'(1000+1)(1000^2-1000+1)', correct:true},
      {kind:'math', value:'(1000-1)(1000^2+1000+1)', correct:false},
      {kind:'math', value:'(1000+1)^3', correct:false}
    ],
    verdict:'합성수',
    factors:['1001','999001'],
    reveal:'\\(1,000,000,001 = 1,001 \\times 999,001\\) 이므로 합성수입니다.',
    hint1:'1,000,000,000은 1000의 세제곱입니다.',
    hint2:'\\(a^3+b^3\\) 공식에 \\(a=1000, b=1\\) 을 넣어 보세요.',
    hint3:'1,001과 999,001이라는 두 인수가 생기므로 합성수입니다.'
  }
];

const state = {
  index:0,
  solved:0,
  hints:0,
  streak:0,
  bestStreak:0,
  rewriteOptions:[],
  factorOptions:[],
  verdictOptions:[],
  rewriteSelected:null,
  factorSelected:null,
  verdictSelected:null,
  rewriteDone:false,
  factorDone:false,
  verdictDone:false,
  hintShown:{1:false,2:false,3:false}
};

const verdictChoices = ['소수','합성수'];

const labState = {
  mode:'sum3',
  a:100,
  b:3,
  x:100
};

function shuffleArray(items){
  const copied = items.map((item)=>({ ...item }));
  for(let index = copied.length - 1; index > 0; index -= 1){
    const swapIndex = Math.floor(Math.random() * (index + 1));
    const temp = copied[index];
    copied[index] = copied[swapIndex];
    copied[swapIndex] = temp;
  }
  return copied;
}

function prepareCaseOptions(){
  const current = CASES[state.index];
  state.rewriteOptions = shuffleArray(current.rewriteOptions);
  state.factorOptions = shuffleArray(current.factorOptions);
  state.verdictOptions = shuffleArray(verdictChoices.map((value)=>({
    value:value,
    correct:value === current.verdict
  })));
}

function renderMath(latex, displayMode){
  if(window.katex){
    try{
      return katex.renderToString(latex,{throwOnError:false,displayMode:!!displayMode});
    }catch(error){}
  }
  return latex;
}

function renderTextWithInlineMath(text){
  return text.replace(/\\\((.+?)\\\)/g, function(match, latex){
    return renderMath(latex, false);
  });
}

function paintStaticMath(){
  document.querySelectorAll('[data-math]').forEach((node)=>{
    node.innerHTML = renderMath(node.getAttribute('data-math'), false);
  });
}

function formatBigInt(value){
  const text = value.toString();
  return text.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function setFeedback(id, ok, text){
  const node = document.getElementById(id);
  node.textContent = text;
  node.className = ok ? 'feedback ok' : 'feedback ng';
}

function clearFeedback(){
  ['feedback1','feedback2','feedback3'].forEach((id)=>{
    const node = document.getElementById(id);
    node.textContent = '';
    node.className = 'feedback';
  });
}

function updateHud(){
  document.getElementById('caseNow').textContent = (state.index + 1) + ' / ' + CASES.length;
  document.getElementById('caseSolved').textContent = String(state.solved);
  document.getElementById('streakNow').textContent = String(state.streak);
  document.getElementById('bestStreak').textContent = '최고 기록 ' + state.bestStreak;
  document.getElementById('hintCount').textContent = String(state.hints);
}

function resetSelections(){
  state.rewriteSelected = null;
  state.factorSelected = null;
  state.verdictSelected = null;
  state.rewriteDone = false;
  state.factorDone = false;
  state.verdictDone = false;
  state.hintShown = {1:false,2:false,3:false};
}

function updateStatus(){
  const s1 = document.getElementById('status1');
  const s2 = document.getElementById('status2');
  const s3 = document.getElementById('status3');
  s1.className = 'status ' + (state.rewriteDone ? 'done' : 'live');
  s1.textContent = state.rewriteDone ? '완료' : '진행 중';
  s2.className = 'status ' + (state.factorDone ? 'done' : state.rewriteDone ? 'live' : 'lock');
  s2.textContent = state.factorDone ? '완료' : state.rewriteDone ? '진행 중' : '잠김';
  s3.className = 'status ' + (state.verdictDone ? 'done' : state.factorDone ? 'live' : 'lock');
  s3.textContent = state.verdictDone ? '완료' : state.factorDone ? '진행 중' : '잠김';
}

function makeChoiceButton(option, index, selectedIndex, locked, kind, clickHandler){
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'choice';
  if(selectedIndex === index) button.classList.add('selected');
  if(locked) button.classList.add('locked');
  button.onclick = function(){ clickHandler(index, locked); };

  const label = document.createElement('div');
  label.className = 'choice-label';
  label.textContent = kind;
  button.appendChild(label);

  const content = document.createElement('div');
  if(option.kind === 'math'){
    content.className = 'choice-math';
    content.innerHTML = renderMath(option.value, false);
  }else{
    content.className = 'choice-text';
    content.textContent = option.value;
  }
  button.appendChild(content);
  return button;
}

function renderOptions(){
  const rewriteBox = document.getElementById('rewriteOptions');
  rewriteBox.innerHTML = '';
  state.rewriteOptions.forEach((option, index)=>{
    rewriteBox.appendChild(makeChoiceButton(option, index, state.rewriteSelected, state.rewriteDone, 'Rewrite', function(i, locked){
      if(locked) return;
      state.rewriteSelected = i;
      renderOptions();
    }));
  });

  const factorBox = document.getElementById('factorOptions');
  factorBox.innerHTML = '';
  state.factorOptions.forEach((option, index)=>{
    factorBox.appendChild(makeChoiceButton(option, index, state.factorSelected, !state.rewriteDone || state.factorDone, 'Factor', function(i, locked){
      if(locked) return;
      state.factorSelected = i;
      renderOptions();
    }));
  });

  const verdictBox = document.getElementById('verdictOptions');
  verdictBox.innerHTML = '';
  state.verdictOptions.forEach((option)=>{
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'verdict-btn';
    if(state.verdictSelected === option.value) button.classList.add('selected');
    if(!state.factorDone || state.verdictDone) button.classList.add('locked');
    button.textContent = option.value;
    button.onclick = function(){
      if(!state.factorDone || state.verdictDone) return;
      state.verdictSelected = option.value;
      renderOptions();
    };
    verdictBox.appendChild(button);
  });
}

function showHint(step){
  const current = CASES[state.index];
  const key = 'hint' + step;
  if(!state.hintShown[step]){
    state.hintShown[step] = true;
    state.hints += 1;
    updateHud();
  }
  const node = document.getElementById(key);
  node.classList.add('show');
  node.innerHTML = renderTextWithInlineMath(current[key]);
}

function resetStage(stage){
  if(stage === 'rewrite') state.rewriteSelected = null;
  if(stage === 'factor') state.factorSelected = null;
  if(stage === 'verdict') state.verdictSelected = null;
  renderOptions();
}

function showReveal(){
  const current = CASES[state.index];
  const revealBox = document.getElementById('revealBox');
  const factorRow = document.getElementById('factorRow');
  factorRow.innerHTML = '';
  current.factors.forEach((factor)=>{
    const badge = document.createElement('div');
    badge.className = 'factor-badge';
    badge.textContent = '인수 ' + factor;
    factorRow.appendChild(badge);
  });
  document.getElementById('revealText').innerHTML = renderTextWithInlineMath(current.reveal);
  revealBox.className = 'reveal show';
}

function markButtons(kind, correctIndex){
  if(kind === 'rewrite'){
    [...document.querySelectorAll('#rewriteOptions .choice')].forEach((button, index)=>{
      if(index === correctIndex) button.classList.add('correct');
      else if(index === state.rewriteSelected) button.classList.add('wrong');
    });
  }
  if(kind === 'factor'){
    [...document.querySelectorAll('#factorOptions .choice')].forEach((button, index)=>{
      if(index === correctIndex) button.classList.add('correct');
      else if(index === state.factorSelected) button.classList.add('wrong');
    });
  }
  if(kind === 'verdict'){
    [...document.querySelectorAll('#verdictOptions .verdict-btn')].forEach((button)=>{
      if(button.textContent === CASES[state.index].verdict) button.classList.add('correct');
      else if(button.textContent === state.verdictSelected) button.classList.add('wrong');
    });
  }
}

function checkStage(stage){
  const current = CASES[state.index];

  if(stage === 'rewrite'){
    if(state.rewriteSelected === null){
      setFeedback('feedback1', false, '먼저 식 하나를 선택하세요.');
      return;
    }
    const correctIndex = state.rewriteOptions.findIndex((item)=>item.correct);
    const ok = state.rewriteSelected === correctIndex;
    if(ok){
      state.rewriteDone = true;
      setFeedback('feedback1', true, '좋습니다. 이제 맞는 인수분해 공식을 골라 보세요.');
    }else{
      state.streak = 0;
      setFeedback('feedback1', false, '아직 구조를 잘못 본 것입니다. 완전거듭제곱과 기준 수를 다시 보세요.');
      markButtons('rewrite', correctIndex);
    }
  }

  if(stage === 'factor'){
    if(!state.rewriteDone) return;
    if(state.factorSelected === null){
      setFeedback('feedback2', false, '먼저 인수분해 식을 선택하세요.');
      return;
    }
    const correctIndex = state.factorOptions.findIndex((item)=>item.correct);
    const ok = state.factorSelected === correctIndex;
    if(ok){
      state.factorDone = true;
      setFeedback('feedback2', true, '맞습니다. 이제 소수인지 합성수인지 최종 판정을 내리세요.');
    }else{
      state.streak = 0;
      setFeedback('feedback2', false, '공식의 부호가 맞지 않습니다. 가운데 항의 부호를 다시 보세요.');
      markButtons('factor', correctIndex);
    }
  }

  if(stage === 'verdict'){
    if(!state.factorDone) return;
    if(state.verdictSelected === null){
      setFeedback('feedback3', false, '먼저 소수 또는 합성수를 고르세요.');
      return;
    }
    const ok = state.verdictSelected === current.verdict;
    if(ok){
      state.verdictDone = true;
      state.streak += 1;
      state.bestStreak = Math.max(state.bestStreak, state.streak);
      if(state.solved === state.index) state.solved += 1;
      setFeedback('feedback3', true, '판정 완료. 금고가 열렸습니다.');
      document.getElementById('nextBtn').style.display = state.index < CASES.length - 1 ? 'inline-flex' : 'none';
      showReveal();
      markButtons('verdict');
      if(state.index === CASES.length - 1) document.getElementById('summaryBox').classList.add('show');
    }else{
      state.streak = 0;
      setFeedback('feedback3', false, '인수분해가 되었으니 다시 생각해 보세요.');
      markButtons('verdict');
    }
  }

  updateStatus();
  updateHud();
  renderOptions();
}

function renderCase(){
  const current = CASES[state.index];
  if(!state.rewriteOptions.length || !state.factorOptions.length || !state.verdictOptions.length){
    prepareCaseOptions();
  }
  document.getElementById('caseTag').textContent = current.tag;
  document.getElementById('caseTitle').textContent = current.title;
  document.getElementById('caseStory').textContent = current.story;
  document.getElementById('caseNumber').textContent = current.number;
  document.getElementById('rewritePrompt').textContent = current.rewritePrompt;
  document.getElementById('factorPrompt').textContent = current.factorPrompt;
  document.getElementById('hint1').className = 'hint';
  document.getElementById('hint2').className = 'hint';
  document.getElementById('hint3').className = 'hint';
  document.getElementById('hint1').innerHTML = current.hint1;
  document.getElementById('hint2').innerHTML = current.hint2;
  document.getElementById('hint3').innerHTML = current.hint3;
  clearFeedback();
  document.getElementById('revealBox').className = 'reveal';
  document.getElementById('factorRow').innerHTML = '';
  document.getElementById('nextBtn').style.display = state.verdictDone && state.index < CASES.length - 1 ? 'inline-flex' : 'none';
  if(state.index !== CASES.length - 1 || !state.verdictDone){
    document.getElementById('summaryBox').classList.remove('show');
  }
  updateStatus();
  updateHud();
  renderOptions();
}

function nextCase(){
  if(!state.verdictDone) return;
  if(state.index < CASES.length - 1){
    state.index += 1;
    resetSelections();
    prepareCaseOptions();
    renderCase();
  }
}

function setLabMode(mode){
  labState.mode = mode;
  document.querySelectorAll('.lab-tab').forEach((button)=>button.classList.remove('active'));
  document.getElementById('tab-' + mode).classList.add('active');
  renderLabControls();
  updateLab();
}

function createNumberField(id, label, value, min){
  const wrap = document.createElement('div');
  wrap.className = 'field';
  const tag = document.createElement('label');
  tag.setAttribute('for', id);
  tag.textContent = label;
  wrap.appendChild(tag);
  const input = document.createElement('input');
  input.type = 'number';
  input.id = id;
  input.value = String(value);
  input.min = String(min || 1);
  input.oninput = updateLab;
  wrap.appendChild(input);
  return wrap;
}

function createInfoField(label, text){
  const wrap = document.createElement('div');
  wrap.className = 'field';
  const tag = document.createElement('label');
  tag.textContent = label;
  wrap.appendChild(tag);
  const info = document.createElement('div');
  info.className = 'field-static';
  info.textContent = text;
  wrap.appendChild(info);
  return wrap;
}

function renderLabControls(){
  const box = document.getElementById('labControls');
  box.innerHTML = '';
  if(labState.mode === 'quartic'){
    box.appendChild(createNumberField('labX', 'x 값', labState.x, 2));
    box.appendChild(createInfoField('사용 공식', 'x^4-3x^2+1')); 
  }else{
    box.appendChild(createNumberField('labA', 'a 값', labState.a, 2));
    box.appendChild(createNumberField('labB', 'b 값', labState.b, 1));
  }
}

function updateLab(){
  const mathBox = document.getElementById('labMath');
  const resultBox = document.getElementById('labResult');

  if(labState.mode === 'sum3'){
    const a = BigInt(Math.max(2, Number(document.getElementById('labA').value || labState.a)));
    const b = BigInt(Math.max(1, Number(document.getElementById('labB').value || labState.b)));
    labState.a = Number(a);
    labState.b = Number(b);
    const numberValue = a*a*a + b*b*b;
    const factor1 = a + b;
    const factor2 = a*a - a*b + b*b;
    mathBox.innerHTML = renderMath(String(a) + '^3+' + String(b) + '^3', false);
    resultBox.innerHTML = '생성된 수: <strong>' + formatBigInt(numberValue) + '</strong><br>' +
      '인수분해: ' + formatBigInt(numberValue) + ' = ' + formatBigInt(factor1) + ' × ' + formatBigInt(factor2) + '<br>' +
      '따라서 이 수는 합성수입니다.';
    return;
  }

  if(labState.mode === 'diff3'){
    const a = BigInt(Math.max(2, Number(document.getElementById('labA').value || labState.a)));
    let bValue = Math.max(1, Number(document.getElementById('labB').value || labState.b));
    if(bValue >= Number(a)) bValue = Number(a) - 1;
    if(bValue < 1) bValue = 1;
    const b = BigInt(bValue);
    document.getElementById('labB').value = String(bValue);
    labState.a = Number(a);
    labState.b = bValue;
    const numberValue = a*a*a - b*b*b;
    const factor1 = a - b;
    const factor2 = a*a + a*b + b*b;
    mathBox.innerHTML = renderMath(String(a) + '^3-' + String(b) + '^3', false);
    resultBox.innerHTML = '생성된 수: <strong>' + formatBigInt(numberValue) + '</strong><br>' +
      '인수분해: ' + formatBigInt(numberValue) + ' = ' + formatBigInt(factor1) + ' × ' + formatBigInt(factor2) + '<br>' +
      '따라서 이 수는 합성수입니다.';
    return;
  }

  const x = BigInt(Math.max(2, Number(document.getElementById('labX').value || labState.x)));
  labState.x = Number(x);
  const numberValue = x*x*x*x - 3n*x*x + 1n;
  const factor1 = x*x + x - 1n;
  const factor2 = x*x - x - 1n;
  mathBox.innerHTML = renderMath(String(x) + '^4-3\\cdot' + String(x) + '^2+1', false);
  resultBox.innerHTML = '생성된 수: <strong>' + formatBigInt(numberValue) + '</strong><br>' +
    '인수분해: ' + formatBigInt(numberValue) + ' = ' + formatBigInt(factor1) + ' × ' + formatBigInt(factor2) + '<br>' +
    '따라서 이 수는 합성수입니다.';
}

function waitForKatex(){
  if(window.katex){
    paintStaticMath();
    renderCase();
    renderLabControls();
    updateLab();
    return;
  }
  let count = 0;
  const timer = setInterval(function(){
    count += 1;
    if(window.katex){
      clearInterval(timer);
      paintStaticMath();
      renderCase();
      renderLabControls();
      updateLab();
    }
    if(count > 60){
      clearInterval(timer);
      renderCase();
      renderLabControls();
      updateLab();
    }
  }, 120);
}

resetSelections();
prepareCaseOptions();
updateHud();
updateStatus();
waitForKatex();
</script>
</body>
</html>
"""


def render():
    st.set_page_config(page_title="소수·합성수 잠금 해제", layout="wide")

    st.markdown(
        """
        <style>
        .main { max-width: 100%; }
        iframe { width: 100% !important; height: 3400px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    components.html(_HTML, height=3400, scrolling=False)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


if __name__ == "__main__":
    render()