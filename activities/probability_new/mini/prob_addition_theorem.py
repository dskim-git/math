# activities/probability_new/mini/prob_addition_theorem.py
"""
확률의 덧셈정리 미니활동 (v2)
- 탭 네비게이션
- P(A∪B) ≤ 1 제약 적용
- 문제 2단계: 배반/비배반 판단 → 확률 계산
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "➕ 확률의 덧셈정리 탐험",
    "description": "P(A∪B)=P(A)+P(B)−P(A∩B)를 벤다이어그램·문제 퀴즈·배반사건 분류로 탐구합니다.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "확률덧셈정리"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 – 확률의 덧셈정리**"},
    {
        "key": "빼야하는이유",
        "label": "P(A∪B) = P(A) + P(B) − P(A∩B) 에서 P(A∩B)를 빼야 하는 이유를 자신의 말로 설명해보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "A와 B에 동시에 속하는 부분은 P(A)와 P(B) 모두에 포함되므로..."
    },
    {
        "key": "배반사건구별",
        "label": "배반사건과 비배반사건의 차이를 설명하고, 일상에서 각각의 예를 하나씩 찾아보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "배반사건(A∩B=∅): 예) ...\n비배반사건(A∩B≠∅): 예) ..."
    },
    {
        "key": "어려운문제",
        "label": "탐구2의 4가지 문제 중 가장 어려웠던 것은 무엇이고, 어떻게 해결했나요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "문제 번호와 이유, 해결 방법..."
    },
    {
        "key": "새로알게된점",
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

_HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0a0e1a 0%,#0f1b2d 55%,#0a1420 100%);
  color:#e2e8f0;padding:14px 12px 30px;min-height:100vh;
}
/* ── 헤더 ── */
.hdr{
  text-align:center;padding:18px 20px 14px;
  background:linear-gradient(135deg,rgba(251,146,60,.15),rgba(245,101,101,.15));
  border:1px solid rgba(251,146,60,.35);border-radius:16px;margin-bottom:14px;
}
.hdr h1{font-size:1.4rem;font-weight:700;color:#fb923c;margin-bottom:5px}
.hdr .formula{
  font-size:1rem;color:#fcd34d;font-family:'Courier New',monospace;
  background:rgba(0,0,0,.3);display:inline-block;
  padding:5px 16px;border-radius:8px;margin:6px 0;
}
.hdr p{font-size:.83rem;color:#94a3b8;margin-top:5px}

/* ── 스코어보드 ── */
.scoreboard{display:flex;gap:10px;justify-content:center;margin-bottom:14px;flex-wrap:wrap}
.score-card{
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
  border-radius:10px;padding:7px 20px;text-align:center;
}
.score-card .num{font-size:1.45rem;font-weight:700}
.score-card .lbl{font-size:.68rem;color:#94a3b8}
.sc-correct .num{color:#34d399}
.sc-total .num{color:#60a5fa}

/* ── 탭 ── */
.tabs{
  display:flex;gap:6px;margin-bottom:14px;
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.1);
  border-radius:12px;padding:6px;
}
.tab{
  flex:1;padding:9px 8px;border-radius:9px;
  border:2px solid transparent;
  background:transparent;color:#64748b;
  font-weight:700;font-size:.85rem;cursor:pointer;
  transition:all .2s;
}
.tab:hover{color:#94a3b8;background:rgba(255,255,255,.05)}
.tab.active{
  background:rgba(251,146,60,.15);
  border-color:rgba(251,146,60,.5);color:#fb923c;
}
.tab-pane{display:none}
.tab-pane.active{display:block}

/* ── 섹션 공통 ── */
.section{
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.1);
  border-radius:14px;padding:16px 15px;
}
.section-title{font-size:1.02rem;font-weight:700;margin-bottom:5px;display:flex;align-items:center;gap:7px}
.section-desc{font-size:.82rem;color:#94a3b8;margin-bottom:13px;line-height:1.6}

/* ── 탐구1: 벤다이어그램 ── */
.venn-wrap{display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start}
.venn-canvas-box{flex:0 0 auto}
canvas#vc{border-radius:12px;display:block;background:#0d1828}
.venn-ctrls{flex:1;min-width:200px}
.ctrl-row{margin-bottom:10px}
.ctrl-lbl{
  font-size:.79rem;color:#94a3b8;
  margin-bottom:3px;display:flex;justify-content:space-between;align-items:center;
}
.ctrl-lbl .val{color:#fbbf24;font-weight:700;font-family:monospace;font-size:.9rem}
input[type=range]{width:100%;accent-color:#fb923c;cursor:pointer}
.formula-box{
  background:rgba(251,146,60,.1);border:1px solid rgba(251,146,60,.3);
  border-radius:10px;padding:11px 13px;margin-top:5px;
  font-family:'Courier New',monospace;font-size:.84rem;line-height:1.95;color:#fcd34d;
}
.formula-box strong{color:#34d399;font-size:.98rem}
.warn-box{
  display:none;margin-top:7px;padding:7px 12px;border-radius:8px;
  background:rgba(248,113,113,.12);border:1px solid rgba(248,113,113,.4);
  color:#fca5a5;font-size:.8rem;font-weight:600;
}
.mutually-badge{
  display:none;margin-top:7px;padding:6px 12px;border-radius:8px;
  background:rgba(52,211,153,.13);border:1px solid rgba(52,211,153,.4);
  color:#34d399;font-size:.8rem;font-weight:700;text-align:center;
}

/* ── 탐구2: 문제 카드 ── */
.prob-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:13px}
.prob-card{
  background:rgba(255,255,255,.05);border:2px solid rgba(255,255,255,.12);
  border-radius:14px;padding:14px 13px;transition:border-color .25s,background .25s;
}
.prob-card.card-ok{border-color:#34d399;background:rgba(52,211,153,.06)}
.prob-card.card-ng{border-color:#f87171;background:rgba(248,113,113,.06)}
.prob-num{font-size:.7rem;color:#94a3b8;margin-bottom:5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.prob-visual{margin-bottom:9px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.prob-q{font-size:.86rem;color:#e2e8f0;margin-bottom:10px;line-height:1.65}
.prob-q strong{color:#fbbf24}

/* 주사위 */
.dice-row{display:flex;gap:6px;justify-content:center;margin-bottom:5px}
.die{
  width:44px;height:44px;border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-size:1.1rem;font-weight:700;border:2px solid rgba(255,255,255,.13);
  background:rgba(255,255,255,.06);color:#e2e8f0;
}
.die.sa{background:rgba(96,165,250,.28);border-color:#60a5fa;color:#93c5fd}
.die.sb{background:rgba(251,146,60,.28);border-color:#fb923c;color:#fde68a}
.die.sab{background:rgba(167,139,250,.32);border-color:#a78bfa;color:#ddd6fe}

/* 숫자 그리드 */
.ng{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;max-width:205px;margin:0 auto 5px}
.nc{
  aspect-ratio:1;border-radius:6px;display:flex;align-items:center;justify-content:center;
  font-size:.78rem;font-weight:700;border:1px solid rgba(255,255,255,.1);
  background:rgba(255,255,255,.05);color:#64748b;
}
.nc.sa{background:rgba(96,165,250,.28);border-color:#60a5fa;color:#93c5fd}
.nc.sb{background:rgba(52,211,153,.28);border-color:#34d399;color:#6ee7b7}
.nc.sab{background:rgba(167,139,250,.32);border-color:#a78bfa;color:#ddd6fe}

/* 사람 아이콘 */
.people-row{display:flex;gap:4px;justify-content:center;flex-wrap:wrap;font-size:1.45rem;margin-bottom:4px}

/* 색상 범례 */
.ckey{display:flex;gap:7px;flex-wrap:wrap;justify-content:center;font-size:.68rem;color:#94a3b8;margin-top:4px}
.ckey span{display:flex;align-items:center;gap:3px}
.cd{width:9px;height:9px;border-radius:2px;flex-shrink:0}

/* STEP 배지 */
.step-badge{
  font-size:.68rem;font-weight:800;letter-spacing:.07em;text-transform:uppercase;
  padding:3px 9px;border-radius:5px;display:inline-block;margin-bottom:6px;
}
.step1-badge{background:rgba(251,146,60,.18);color:#fb923c;border:1px solid rgba(251,146,60,.35)}
.step2-badge{background:rgba(96,165,250,.15);color:#60a5fa;border:1px solid rgba(96,165,250,.35)}

/* STEP1 버튼 */
.s1row{display:flex;gap:7px;margin-bottom:7px;flex-wrap:wrap}
.s1btn{
  padding:7px 16px;border-radius:8px;border:2px solid;
  cursor:pointer;font-size:.8rem;font-weight:700;
  background:transparent;transition:all .15s;
}
.s1btn:hover:not(:disabled){opacity:.8;transform:scale(1.03)}
.s1btn:disabled{cursor:default}
.s1-mut{color:#f87171;border-color:#f87171}
.s1-nomut{color:#60a5fa;border-color:#60a5fa}
.s1btn.s1ok{font-weight:800;opacity:1!important}
.s1-mut.s1ok{background:#f87171;color:#0f2027}
.s1-nomut.s1ok{background:#60a5fa;color:#0f2027}
.s1btn.s1ng{background:rgba(248,113,113,.15)}

/* STEP1 피드백 */
.s1fb{
  display:none;font-size:.77rem;padding:7px 10px;border-radius:7px;
  margin-bottom:9px;line-height:1.55;
}
.s1fb.show{display:block}
.s1fb.fok{background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.3);color:#6ee7b7}
.s1fb.fng{background:rgba(248,113,113,.09);border:1px solid rgba(248,113,113,.3);color:#fca5a5}

/* STEP2 */
.step2-wrap{
  display:none;border-top:1px solid rgba(255,255,255,.1);
  padding-top:11px;margin-top:8px;
}
.step2-wrap.open{display:block}

/* 힌트 */
.hint-btn{
  padding:5px 12px;border-radius:8px;border:1px solid rgba(251,191,36,.4);
  background:rgba(251,191,36,.07);color:#fbbf24;font-size:.74rem;
  cursor:pointer;margin-bottom:8px;transition:background .15s;
}
.hint-btn:hover{background:rgba(251,191,36,.16)}
.hint-box{
  display:none;background:rgba(255,255,255,.06);border-radius:8px;
  padding:9px 11px;margin-bottom:9px;font-size:.78rem;line-height:1.75;color:#cbd5e1;
}
.hint-box.open{display:block}
.hint-box strong{color:#fbbf24}

/* 선택지 */
.choices{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin-bottom:5px}
.cbtn{
  padding:7px 4px;border-radius:8px;border:2px solid rgba(255,255,255,.2);
  background:rgba(255,255,255,.06);color:#e2e8f0;
  font-size:.83rem;font-weight:700;cursor:pointer;transition:all .15s;
  font-family:'Courier New',monospace;text-align:center;
}
.cbtn:hover:not(:disabled){border-color:#60a5fa;background:rgba(96,165,250,.15)}
.cbtn:disabled{cursor:default}
.cbtn.ok{background:#34d399;border-color:#34d399;color:#0f2027}
.cbtn.ng{background:#f87171;border-color:#f87171;color:#0f2027}
.cbtn.reveal{border-color:#34d399;color:#34d399}

/* 피드백 */
.feedback{
  display:none;padding:9px 11px;border-radius:8px;
  font-size:.78rem;line-height:1.65;margin-top:4px;
}
.feedback.show{display:block}
.feedback.fok{background:rgba(52,211,153,.1);border:1px solid rgba(52,211,153,.3);color:#6ee7b7}
.feedback.fng{background:rgba(248,113,113,.09);border:1px solid rgba(248,113,113,.3);color:#fca5a5}
.feedback strong{color:#e2e8f0}

/* ── 탐구3: 분류기 ── */
.cls-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.cls-card{
  background:rgba(255,255,255,.05);border:2px solid rgba(255,255,255,.12);
  border-radius:12px;padding:13px 12px;transition:all .2s;
}
.cls-card.cc{border-color:#34d399;background:rgba(52,211,153,.07)}
.cls-card.cw{border-color:#f87171;background:rgba(248,113,113,.07)}
.cls-ctx{font-size:.7rem;color:#94a3b8;margin-bottom:4px}
.cls-evt{font-size:.85rem;color:#e2e8f0;margin-bottom:9px;line-height:1.5}
.cls-btns{display:flex;gap:8px}
.clsbtn{
  padding:6px 13px;border-radius:8px;border:2px solid;
  cursor:pointer;font-size:.74rem;font-weight:700;
  background:transparent;transition:all .15s;
}
.clsbtn:hover:not(:disabled){opacity:.8;transform:scale(1.03)}
.clsbtn:disabled{cursor:default;opacity:.65}
.btn-yes{color:#f87171;border-color:#f87171}
.btn-no{color:#60a5fa;border-color:#60a5fa}
.clsbtn.cpick{font-weight:800;opacity:1!important}
.btn-yes.cpick{background:#f87171;color:#0f2027}
.btn-no.cpick{background:#60a5fa;color:#0f2027}
.clsbtn.wpick{background:rgba(248,113,113,.15);border-color:#f87171;color:#f87171}
.cls-expl{
  display:none;font-size:.74rem;color:#94a3b8;
  margin-top:8px;line-height:1.55;
  padding-top:7px;border-top:1px solid rgba(255,255,255,.08);
}
.cls-card.cc .cls-expl,.cls-card.cw .cls-expl{display:block}
</style>
</head>
<body>

<!-- ── 헤더 ── -->
<div class="hdr">
  <h1>➕ 확률의 덧셈정리 탐험</h1>
  <div class="formula">P(A∪B) = P(A) + P(B) − P(A∩B)</div>
  <p>세 가지 탐구 활동으로 덧셈정리의 핵심을 체험해봐요!</p>
</div>

<!-- ── 스코어보드 ── -->
<div class="scoreboard">
  <div class="score-card sc-correct">
    <div class="num" id="sc-cor">0</div>
    <div class="lbl">정답</div>
  </div>
  <div class="score-card sc-total">
    <div class="num" id="sc-tot">0 / 14</div>
    <div class="lbl">전체 진도</div>
  </div>
</div>

<!-- ── 탭 ── -->
<div class="tabs">
  <button class="tab active" data-target="t1" onclick="switchTab(this)">🔵 탐구 1<br><span style="font-size:.7rem;font-weight:400;color:inherit">벤다이어그램</span></button>
  <button class="tab" data-target="t2" onclick="switchTab(this)">🎯 탐구 2<br><span style="font-size:.7rem;font-weight:400;color:inherit">문제 퀴즈</span></button>
  <button class="tab" data-target="t3" onclick="switchTab(this)">✂️ 탐구 3<br><span style="font-size:.7rem;font-weight:400;color:inherit">배반 분류</span></button>
</div>

<!-- ══════════ 탭 1: 벤다이어그램 ══════════ -->
<div class="tab-pane active" id="t1">
<div class="section">
  <div class="section-title">🔵 탐구 1 — 벤 다이어그램 시뮬레이터</div>
  <div class="section-desc">슬라이더로 P(A), P(B), P(A∩B)를 바꿔 보세요. P(A∩B)는 확률 조건에 맞게 자동으로 범위가 제한됩니다.</div>

  <div class="venn-wrap">
    <div class="venn-canvas-box">
      <canvas id="vc" width="290" height="200"></canvas>
    </div>
    <div class="venn-ctrls">
      <div class="ctrl-row">
        <div class="ctrl-lbl">P(A) <span class="val" id="lpa">0.50</span></div>
        <input type="range" id="sA" min="1" max="99" value="50">
      </div>
      <div class="ctrl-row">
        <div class="ctrl-lbl">P(B) <span class="val" id="lpb">0.40</span></div>
        <input type="range" id="sB" min="1" max="99" value="40">
      </div>
      <div class="ctrl-row">
        <div class="ctrl-lbl">
          P(A∩B) <span class="val" id="lpab">0.15</span>
          <span id="ab-range-hint" style="font-size:.68rem;color:#64748b"></span>
        </div>
        <input type="range" id="sAB" min="0" max="40" value="15">
      </div>
      <div class="formula-box" id="fbox">
        P(A∪B) = 0.50 + 0.40 − 0.15 = <strong>0.75</strong>
      </div>
      <div class="mutually-badge" id="mbadge">⊘ 배반사건! &nbsp;P(A∩B) = 0 &nbsp;→&nbsp; P(A∪B) = P(A) + P(B)</div>
    </div>
  </div>
</div>
</div>

<!-- ══════════ 탭 2: 문제 카드 ══════════ -->
<div class="tab-pane" id="t2">
<div class="section">
  <div class="section-title">🎯 탐구 2 — 실생활 문제 카드</div>
  <div class="section-desc">
    <strong style="color:#fb923c">STEP 1</strong>에서 두 사건이 배반인지 비배반인지 먼저 판단한 뒤,
    <strong style="color:#60a5fa">STEP 2</strong>에서 확률값을 계산하세요!
  </div>

  <div class="prob-grid">

    <!-- ── 문제 1: 주사위 ── -->
    <div class="prob-card" id="pc1">
      <div class="prob-num">문제 1 &nbsp;🎲 주사위</div>
      <div class="prob-visual">
        <div class="dice-row" id="drow"></div>
        <div class="ckey">
          <span><div class="cd" style="background:#60a5fa"></div>A: 3의 배수</span>
          <span><div class="cd" style="background:#fb923c"></div>B: 4 이상</span>
          <span><div class="cd" style="background:#a78bfa"></div>A∩B</span>
        </div>
      </div>
      <div class="prob-q">주사위를 한 번 던질 때,<br><strong>3의 배수이거나 4 이상</strong>인 눈이 나올 확률은?</div>

      <!-- STEP 1 -->
      <div><span class="step-badge step1-badge">STEP 1</span></div>
      <div style="font-size:.8rem;color:#94a3b8;margin-bottom:7px">A = {3,6} &nbsp; B = {4,5,6} — 두 사건은?</div>
      <div class="s1row" id="s1r1">
        <button class="s1btn s1-mut"   onclick="step1(1,true,this)">⊘ 배반사건</button>
        <button class="s1btn s1-nomut" onclick="step1(1,false,this)">↔ 비배반사건</button>
      </div>
      <div class="s1fb" id="s1f1"></div>

      <!-- STEP 2 -->
      <div class="step2-wrap" id="sw1">
        <div><span class="step-badge step2-badge">STEP 2</span></div>
        <button class="hint-btn" onclick="th('h1',this)">💡 힌트 보기</button>
        <div class="hint-box" id="h1">
          A = {3, 6} → P(A) = 2/6<br>
          B = {4, 5, 6} → P(B) = 3/6<br>
          A∩B = {6} → P(A∩B) = 1/6<br>
          <strong>→ P(A∩B)를 빼야 합니다</strong>
        </div>
        <div class="choices">
          <button class="cbtn" data-ok="0" onclick="ca(1,this)">1/2</button>
          <button class="cbtn" data-ok="1" onclick="ca(1,this)">2/3</button>
          <button class="cbtn" data-ok="0" onclick="ca(1,this)">5/6</button>
          <button class="cbtn" data-ok="0" onclick="ca(1,this)">1</button>
        </div>
        <div class="feedback" id="fb1">
          ✅ P(A∪B) = 2/6 + 3/6 − 1/6 = <strong>4/6 = 2/3</strong><br>
          A∪B = {3,4,5,6} → 4가지 / 6 = 2/3
        </div>
      </div>
    </div>

    <!-- ── 문제 2: 숫자 카드 ── -->
    <div class="prob-card" id="pc2">
      <div class="prob-num">문제 2 &nbsp;🃏 숫자 카드 1~20</div>
      <div class="prob-visual">
        <div class="ng" id="ngrid"></div>
        <div class="ckey">
          <span><div class="cd" style="background:#60a5fa"></div>A: 짝수</span>
          <span><div class="cd" style="background:#34d399"></div>B: 3의 배수</span>
          <span><div class="cd" style="background:#a78bfa"></div>A∩B</span>
        </div>
      </div>
      <div class="prob-q">1~20 카드 중 1장을 뽑을 때,<br><strong>짝수이거나 3의 배수</strong>인 카드를 뽑을 확률은?</div>

      <!-- STEP 1 -->
      <div><span class="step-badge step1-badge">STEP 1</span></div>
      <div style="font-size:.8rem;color:#94a3b8;margin-bottom:7px">A = 짝수 &nbsp; B = 3의 배수 — 두 사건은?</div>
      <div class="s1row" id="s1r2">
        <button class="s1btn s1-mut"   onclick="step1(2,true,this)">⊘ 배반사건</button>
        <button class="s1btn s1-nomut" onclick="step1(2,false,this)">↔ 비배반사건</button>
      </div>
      <div class="s1fb" id="s1f2"></div>

      <!-- STEP 2 -->
      <div class="step2-wrap" id="sw2">
        <div><span class="step-badge step2-badge">STEP 2</span></div>
        <button class="hint-btn" onclick="th('h2',this)">💡 힌트 보기</button>
        <div class="hint-box" id="h2">
          A = {2,4,6,8,10,12,14,16,18,20} → P(A) = 10/20<br>
          B = {3,6,9,12,15,18} → P(B) = 6/20<br>
          A∩B = {6,12,18} → P(A∩B) = 3/20<br>
          <strong>→ 보라색 3개를 빼야 합니다</strong>
        </div>
        <div class="choices">
          <button class="cbtn" data-ok="0" onclick="ca(2,this)">3/5</button>
          <button class="cbtn" data-ok="1" onclick="ca(2,this)">13/20</button>
          <button class="cbtn" data-ok="0" onclick="ca(2,this)">7/10</button>
          <button class="cbtn" data-ok="0" onclick="ca(2,this)">4/5</button>
        </div>
        <div class="feedback" id="fb2">
          ✅ P(A∪B) = 10/20 + 6/20 − 3/20 = <strong>13/20</strong><br>
          짝수(10개) + 3의 배수(6개) − 공통 {6,12,18}(3개) = 13개
        </div>
      </div>
    </div>

    <!-- ── 문제 3: 반려동물 ── -->
    <div class="prob-card" id="pc3">
      <div class="prob-num">문제 3 &nbsp;🐾 반려동물 조사</div>
      <div class="prob-visual">
        <svg width="246" height="92" viewBox="0 0 246 92">
          <ellipse cx="85"  cy="50" rx="76" ry="36" fill="rgba(96,165,250,.2)"  stroke="#60a5fa" stroke-width="2"/>
          <ellipse cx="161" cy="50" rx="76" ry="36" fill="rgba(52,211,153,.2)"  stroke="#34d399" stroke-width="2"/>
          <text x="85"  y="15" text-anchor="middle" fill="#60a5fa" font-size="11" font-weight="600">🐕 개 (A)</text>
          <text x="161" y="15" text-anchor="middle" fill="#34d399" font-size="11" font-weight="600">🐱 고양이 (B)</text>
          <text x="50"  y="47" text-anchor="middle" fill="#93c5fd" font-size="14" font-weight="700">32</text>
          <text x="50"  y="62" text-anchor="middle" fill="#94a3b8" font-size="10">가구</text>
          <text x="123" y="47" text-anchor="middle" fill="#ddd6fe" font-size="14" font-weight="700">8</text>
          <text x="123" y="62" text-anchor="middle" fill="#94a3b8" font-size="10">둘 다</text>
          <text x="196" y="47" text-anchor="middle" fill="#6ee7b7" font-size="14" font-weight="700">12</text>
          <text x="196" y="62" text-anchor="middle" fill="#94a3b8" font-size="10">가구</text>
        </svg>
      </div>
      <div class="prob-q">100가구: 개 40가구, 고양이 20가구, 둘 다 8가구<br>임의의 가구가 <strong>개 또는 고양이</strong>를 기를 확률은?</div>

      <!-- STEP 1 -->
      <div><span class="step-badge step1-badge">STEP 1</span></div>
      <div style="font-size:.8rem;color:#94a3b8;margin-bottom:7px">A = 개 기르는 가구 &nbsp; B = 고양이 기르는 가구 — 두 사건은?</div>
      <div class="s1row" id="s1r3">
        <button class="s1btn s1-mut"   onclick="step1(3,true,this)">⊘ 배반사건</button>
        <button class="s1btn s1-nomut" onclick="step1(3,false,this)">↔ 비배반사건</button>
      </div>
      <div class="s1fb" id="s1f3"></div>

      <!-- STEP 2 -->
      <div class="step2-wrap" id="sw3">
        <div><span class="step-badge step2-badge">STEP 2</span></div>
        <button class="hint-btn" onclick="th('h3',this)">💡 힌트 보기</button>
        <div class="hint-box" id="h3">
          P(A) = 40/100, &nbsp;P(B) = 20/100, &nbsp;P(A∩B) = 8/100<br>
          개만 32 + 고양이만 12 + 둘 다 8 = <strong>52가구</strong>
        </div>
        <div class="choices">
          <button class="cbtn" data-ok="0" onclick="ca(3,this)">3/5</button>
          <button class="cbtn" data-ok="0" onclick="ca(3,this)">1/2</button>
          <button class="cbtn" data-ok="1" onclick="ca(3,this)">13/25</button>
          <button class="cbtn" data-ok="0" onclick="ca(3,this)">7/10</button>
        </div>
        <div class="feedback" id="fb3">
          ✅ P(A∪B) = 40/100 + 20/100 − 8/100 = <strong>52/100 = 13/25</strong>
        </div>
      </div>
    </div>

    <!-- ── 문제 4: 동아리 ── -->
    <div class="prob-card" id="pc4">
      <div class="prob-num">문제 4 &nbsp;📸 사진 동아리</div>
      <div class="prob-visual">
        <div class="people-row" id="prow"></div>
        <div style="text-align:center;font-size:.72rem;color:#94a3b8;margin-top:3px">
          👦 남학생 4명 &nbsp;+&nbsp; 👧 여학생 5명 → 2명 선발
        </div>
      </div>
      <div class="prob-q">9명 중 2명을 임의로 뽑을 때,<br><strong>모두 남학생이거나 모두 여학생</strong>일 확률은?</div>

      <!-- STEP 1 -->
      <div><span class="step-badge step1-badge">STEP 1</span></div>
      <div style="font-size:.8rem;color:#94a3b8;margin-bottom:7px">A = 모두 남학생 &nbsp; B = 모두 여학생 — 두 사건은?</div>
      <div class="s1row" id="s1r4">
        <button class="s1btn s1-mut"   onclick="step1(4,true,this)">⊘ 배반사건</button>
        <button class="s1btn s1-nomut" onclick="step1(4,false,this)">↔ 비배반사건</button>
      </div>
      <div class="s1fb" id="s1f4"></div>

      <!-- STEP 2 -->
      <div class="step2-wrap" id="sw4">
        <div><span class="step-badge step2-badge">STEP 2</span></div>
        <button class="hint-btn" onclick="th('h4',this)">💡 힌트 보기</button>
        <div class="hint-box" id="h4">
          A = {모두 남} → C(4,2)/C(9,2) = 6/36<br>
          B = {모두 여} → C(5,2)/C(9,2) = 10/36<br>
          A∩B = ∅ &nbsp;→&nbsp; <strong>그냥 더하면 됩니다!</strong>
        </div>
        <div class="choices">
          <button class="cbtn" data-ok="0" onclick="ca(4,this)">1/3</button>
          <button class="cbtn" data-ok="1" onclick="ca(4,this)">4/9</button>
          <button class="cbtn" data-ok="0" onclick="ca(4,this)">5/9</button>
          <button class="cbtn" data-ok="0" onclick="ca(4,this)">2/3</button>
        </div>
        <div class="feedback" id="fb4">
          ✅ 배반사건 → P(A∪B) = 6/36 + 10/36 = <strong>16/36 = 4/9</strong>
        </div>
      </div>
    </div>

  </div><!-- /prob-grid -->
</div>
</div>

<!-- ══════════ 탭 3: 배반 분류기 ══════════ -->
<div class="tab-pane" id="t3">
<div class="section">
  <div class="section-title">✂️ 탐구 3 — 배반사건 분류기</div>
  <div class="section-desc">두 사건이 <strong style="color:#f87171">배반사건(A∩B=∅)</strong>인지 <strong style="color:#60a5fa">비배반사건(A∩B≠∅)</strong>인지 판단하세요!</div>
  <div class="cls-grid" id="clsg"></div>
</div>
</div>

<script>
/* ─── 전역 점수 ──────────────────────── */
var score = {cor:0, tot:0};
var TOTAL = 14;
function addScore(ok){
  score.tot++;
  if(ok) score.cor++;
  document.getElementById('sc-cor').textContent = score.cor;
  document.getElementById('sc-tot').textContent = score.tot+' / '+TOTAL;
}

/* ─── 탭 전환 ────────────────────────── */
function switchTab(btn){
  document.querySelectorAll('.tab-pane').forEach(function(p){p.classList.remove('active')});
  document.querySelectorAll('.tab').forEach(function(t){t.classList.remove('active')});
  document.getElementById(btn.dataset.target).classList.add('active');
  btn.classList.add('active');
}

/* ─── 벤다이어그램 캔버스 ────────────── */
(function(){
  var canvas = document.getElementById('vc');
  var ctx = canvas.getContext('2d');
  var W=290, H=200;
  var sA=document.getElementById('sA');
  var sB=document.getElementById('sB');
  var sAB=document.getElementById('sAB');

  function clamp(){
    var pa=+sA.value/100, pb=+sB.value/100;
    // A∩B must satisfy: 0 ≤ pab ≤ min(pa,pb) AND pab ≥ pa+pb-1
    var minAB = Math.max(0, Math.round((pa+pb-1)*100));
    var maxAB = Math.round(Math.min(pa,pb)*100);
    sAB.min = minAB;
    sAB.max = maxAB;
    var hint = document.getElementById('ab-range-hint');
    hint.textContent = '['+( minAB/100).toFixed(2)+' ~ '+(maxAB/100).toFixed(2)+']';
    if(+sAB.value < minAB) sAB.value = minAB;
    if(+sAB.value > maxAB) sAB.value = maxAB;
  }

  function draw(){
    clamp();
    var pa=+sA.value/100, pb=+sB.value/100, pab=+sAB.value/100;
    var union = pa+pb-pab; // guaranteed ≤ 1 by clamp

    document.getElementById('lpa').textContent  = pa.toFixed(2);
    document.getElementById('lpb').textContent  = pb.toFixed(2);
    document.getElementById('lpab').textContent = pab.toFixed(2);
    document.getElementById('fbox').innerHTML =
      'P(A&cup;B) = '+pa.toFixed(2)+' + '+pb.toFixed(2)+' &minus; '+pab.toFixed(2)+
      ' = <strong>'+union.toFixed(2)+'</strong>';
    document.getElementById('mbadge').style.display = (pab<0.005)?'block':'none';

    ctx.clearRect(0,0,W,H);
    ctx.fillStyle='#0d1828'; ctx.fillRect(0,0,W,H);

    var cx=W/2, cy=H/2+10;
    var maxR=72;
    var rA=maxR*Math.sqrt(pa);
    var rB=maxR*Math.sqrt(pb);
    var overRatio = (Math.min(pa,pb)>0) ? pab/Math.min(pa,pb) : 0;
    var dMax=rA+rB, dMin=Math.abs(rA-rB);
    var dist=dMax - Math.min(0.95,overRatio*2.1)*(dMax-dMin);
    dist=Math.max(dMin+1,Math.min(dMax-1,dist));
    var xA=cx-dist/2, xB=cx+dist/2;

    // A
    ctx.beginPath(); ctx.arc(xA,cy,rA,0,2*Math.PI);
    ctx.fillStyle='rgba(96,165,250,0.22)'; ctx.fill();
    ctx.strokeStyle='#60a5fa'; ctx.lineWidth=2; ctx.stroke();
    // B
    ctx.beginPath(); ctx.arc(xB,cy,rB,0,2*Math.PI);
    ctx.fillStyle='rgba(251,146,60,0.22)'; ctx.fill();
    ctx.strokeStyle='#fb923c'; ctx.lineWidth=2; ctx.stroke();
    // overlap
    if(pab>0.005){
      ctx.save();
      ctx.beginPath(); ctx.arc(xA,cy,rA,0,2*Math.PI); ctx.clip();
      ctx.beginPath(); ctx.arc(xB,cy,rB,0,2*Math.PI);
      ctx.fillStyle='rgba(167,139,250,0.42)'; ctx.fill();
      ctx.restore();
    }
    // labels
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.font='bold 12px Segoe UI';
    ctx.fillStyle='#93c5fd';
    ctx.fillText('A', xA-rA*0.5, cy-4);
    ctx.font='10px Courier New';
    ctx.fillText('P='+pa.toFixed(2), xA-rA*0.5, cy+10);
    ctx.font='bold 12px Segoe UI';
    ctx.fillStyle='#fde68a';
    ctx.fillText('B', xB+rB*0.5, cy-4);
    ctx.font='10px Courier New';
    ctx.fillText('P='+pb.toFixed(2), xB+rB*0.5, cy+10);
    if(pab>0.01){
      ctx.font='bold 10px Segoe UI';
      ctx.fillStyle='#ddd6fe';
      ctx.fillText('A∩B', cx, cy-5);
      ctx.fillText('='+pab.toFixed(2), cx, cy+8);
    }
    ctx.font='bold 12px Segoe UI';
    ctx.fillStyle='#34d399';
    ctx.fillText('P(A∪B) = '+union.toFixed(2), W/2, 16);
  }

  sA.addEventListener('input',draw);
  sB.addEventListener('input',draw);
  sAB.addEventListener('input',draw);
  draw();
})();

/* ─── 주사위 시각화 ─────────────────── */
(function(){
  var row=document.getElementById('drow');
  var sa={3:1,6:1}, sb={4:1,5:1,6:1};
  for(var i=1;i<=6;i++){
    var d=document.createElement('div');
    d.className='die'+(sa[i]&&sb[i]?' sab':sa[i]?' sa':sb[i]?' sb':'');
    d.textContent=i; row.appendChild(d);
  }
})();

/* ─── 숫자 카드 시각화 ──────────────── */
(function(){
  var g=document.getElementById('ngrid');
  for(var n=1;n<=20;n++){
    var a=n%2===0, b=n%3===0;
    var c=document.createElement('div');
    c.className='nc'+(a&&b?' sab':a?' sa':b?' sb':'');
    c.textContent=n; g.appendChild(c);
  }
})();

/* ─── 동아리 아이콘 ─────────────────── */
(function(){
  var r=document.getElementById('prow');
  ['👦','👦','👦','👦','👧','👧','👧','👧','👧'].forEach(function(e){
    var s=document.createElement('span'); s.textContent=e; r.appendChild(s);
  });
})();

/* ─── 힌트 토글 ──────────────────────── */
function th(id,btn){
  var b=document.getElementById(id);
  b.classList.toggle('open');
  btn.textContent=b.classList.contains('open')?'💡 힌트 숨기기':'💡 힌트 보기';
}

/* ─── STEP 1: 배반/비배반 판단 ─────── */
var S1_CORRECT = {1:false, 2:false, 3:false, 4:true};
var S1_OK = {
  1:'✅ 비배반사건! {6}이 A와 B 모두에 속해요',
  2:'✅ 비배반사건! {6,12,18}이 A와 B 모두에 속해요',
  3:'✅ 비배반사건! 개와 고양이를 함께 기르는 8가구가 겹쳐요',
  4:'✅ 배반사건! 동시에 모두 남 + 모두 여는 불가능해요'
};
var S1_NG = {
  1:'❌ 비배반사건이에요! A={3,6}, B={4,5,6}에서 6이 겹쳐요',
  2:'❌ 비배반사건이에요! 6, 12, 18이 짝수이면서 3의 배수예요',
  3:'❌ 비배반사건이에요! 개+고양이 함께 기르는 8가구가 있어요',
  4:'❌ 배반사건이에요! 모두 남 / 모두 여는 절대 겹치지 않아요'
};
var s1done={};
function step1(n, choice, btn){
  if(s1done[n]) return;
  s1done[n]=true;
  var ok=(choice===S1_CORRECT[n]);
  var row=document.getElementById('s1r'+n);
  var fb=document.getElementById('s1f'+n);
  var btns=row.querySelectorAll('.s1btn');
  btns.forEach(function(b){b.disabled=true});
  btns.forEach(function(b){
    var isMutBtn=b.classList.contains('s1-mut');
    if(S1_CORRECT[n]===isMutBtn) b.classList.add('s1ok');
    else if(b===btn && !ok) b.classList.add('s1ng');
  });
  fb.className='s1fb show '+(ok?'fok':'fng');
  fb.innerHTML=ok?S1_OK[n]:S1_NG[n];
  addScore(ok);
  setTimeout(function(){
    document.getElementById('sw'+n).classList.add('open');
  }, 550);
}

/* ─── STEP 2: 확률 계산 ─────────────── */
var s2done={};
function ca(n,btn){
  if(s2done[n]) return;
  s2done[n]=true;
  var ok=btn.getAttribute('data-ok')==='1';
  var card=document.getElementById('pc'+n);
  var fb=document.getElementById('fb'+n);
  var btns=card.querySelectorAll('.step2-wrap .cbtn');
  btns.forEach(function(b){
    b.disabled=true;
    if(b.getAttribute('data-ok')==='1') b.classList.add('reveal');
  });
  if(ok){
    btn.classList.add('ok');
    card.classList.add('card-ok');
    fb.className='feedback show fok';
  } else {
    btn.classList.add('ng');
    card.classList.add('card-ng');
    fb.className='feedback show fng';
    fb.innerHTML='❌ '+fb.innerHTML+'<br><span style="font-size:.76rem">힌트를 확인하고 다시 생각해봐요!</span>';
  }
  addScore(ok);
}

/* ─── 탐구3: 배반사건 분류기 ──────── */
var CLS=[
  {ctx:'🎲 주사위 한 번',       evt:'A = {1,2,3} &nbsp; vs &nbsp; B = {4,5,6}',           mut:true,  expl:'완전히 분리 → A∩B = ∅'},
  {ctx:'🎲 주사위 한 번',       evt:'A = {짝수} &nbsp; vs &nbsp; B = {소수}',              mut:false, expl:'2가 짝수이면서 소수 → A∩B = {2} ≠ ∅'},
  {ctx:'🪙 동전 한 번',         evt:'A = {앞면} &nbsp; vs &nbsp; B = {뒷면}',              mut:true,  expl:'앞·뒷면 동시 불가 → A∩B = ∅'},
  {ctx:'🃏 1~30 숫자 카드',     evt:'A = {4의 배수} &nbsp; vs &nbsp; B = {6의 배수}',      mut:false, expl:'12, 24가 공통 → A∩B ≠ ∅'},
  {ctx:'👥 30명 중 2명 선발',   evt:'A = {준우 포함} &nbsp; vs &nbsp; B = {준우 미포함}',  mut:true,  expl:'준우는 포함·미포함 동시 불가 → A∩B = ∅'},
  {ctx:'🃏 1~12 숫자 카드',     evt:'A = {3의 배수} &nbsp; vs &nbsp; B = {4의 배수}',      mut:false, expl:'12가 공통 → A∩B = {12} ≠ ∅'},
];
var clsDone={};
(function(){
  var grid=document.getElementById('clsg');
  CLS.forEach(function(d,i){
    var card=document.createElement('div');
    card.className='cls-card'; card.id='cl'+i;
    card.innerHTML=
      '<div class="cls-ctx">'+d.ctx+'</div>'+
      '<div class="cls-evt">'+d.evt+'</div>'+
      '<div class="cls-btns">'+
        '<button class="clsbtn btn-yes" onclick="cp('+i+',true)">⊘ 배반사건</button>'+
        '<button class="clsbtn btn-no"  onclick="cp('+i+',false)">↔ 비배반사건</button>'+
      '</div>'+
      '<div class="cls-expl" id="cex'+i+'">'+d.expl+'</div>';
    grid.appendChild(card);
  });
})();
function cp(i,choice){
  if(clsDone[i]) return;
  clsDone[i]=true;
  var d=CLS[i], card=document.getElementById('cl'+i);
  var btns=card.querySelectorAll('.clsbtn');
  btns.forEach(function(b){b.disabled=true});
  var ok=(choice===d.mut);
  card.classList.add(ok?'cc':'cw');
  btns.forEach(function(b){
    var isY=b.classList.contains('btn-yes');
    if((d.mut&&isY)||(!d.mut&&!isY)) b.classList.add('cpick');
    else if((choice&&isY)||(!choice&&!isY)) b.classList.add('wpick');
  });
  addScore(ok);
}
</script>
</body>
</html>"""


def render():
    st.subheader("➕ 확률의 덧셈정리 탐험")
    st.caption("세 가지 탐구 활동으로 P(A∪B) = P(A) + P(B) − P(A∩B)의 핵심을 재미있게 익혀봐요!")
    components.html(_HTML, height=1420, scrolling=False)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
