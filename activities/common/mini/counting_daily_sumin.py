# activities/common/mini/counting_daily_sumin.py
"""
경우의 수로 바라본 하루 — 수민이의 하루 이야기 속 ⓐ~ⓓ 네 가지 상황에서
합의 법칙·곱의 법칙·순열·조합을 클릭 인터랙션으로 탐구하는 미니 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "경우의수하루탐구"

META = {
    "title":       "📱 경우의 수로 바라본 하루",
    "description": "수민이의 하루 이야기 속 교통수단·스탬프 순서·옷 코디·할 일 고르기를 클릭하며 경우의 수를 탐구합니다.",
    "order":       315,
    "hidden":      False,
}

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 성찰 질문에 답해 보세요**"},
    {
        "key":    "합곱구분",
        "label":  "① ⓐ 교통수단과 ⓒ 옷 코디에서 사용한 법칙이 다릅니다. 합의 법칙과 곱의 법칙을 언제 사용하는지 오늘 상황을 예로 들어 설명해보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "순열조합구분",
        "label":  "② ⓑ 스탬프 장소와 ⓓ 할 일 고르기에서 사용한 방법이 다릅니다. 순열과 조합의 차이를 두 상황을 비교하며 설명해보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "나만의사례",
        "label":  "③ 오늘 내 하루를 돌아보고, 경우의 수(합의 법칙, 곱의 법칙, 순열, 조합 중 하나 이상)로 표현할 수 있는 상황을 직접 만들어 경우의 수를 구해보세요.",
        "type":   "text_area",
        "height": 110,
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

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(145deg,#0d1117,#141a2e,#0d1117);
  color:#dde8ff;
  padding:14px 12px 20px;
  min-height:100vh;
}

/* ── Header ──────────────────────────────────────────── */
.page-title{
  text-align:center;
  font-size:1.45rem;
  font-weight:800;
  color:#ffd166;
  text-shadow:0 0 22px rgba(255,209,102,.5);
  margin-bottom:6px;
  padding:10px 0 4px;
}
.page-sub{
  text-align:center;
  font-size:.82rem;
  color:#7c8fa8;
  margin-bottom:18px;
  line-height:1.5;
}
.click-badges{
  display:inline-flex;
  gap:6px;
  align-items:center;
  flex-wrap:wrap;
  justify-content:center;
  margin-top:4px;
}
.cb{
  padding:2px 9px;
  border-radius:20px;
  font-size:.72rem;
  font-weight:700;
  cursor:default;
}
.cb-a{background:#fef3c7;color:#b45309;}
.cb-b{background:#dcfce7;color:#15803d;}
.cb-c{background:#ede9fe;color:#7c3aed;}
.cb-d{background:#fee2e2;color:#dc2626;}

/* ── Tablet mockup ────────────────────────────────────── */
.tablet-wrap{
  max-width:720px;
  margin:0 auto 22px;
  background:#d1d5db;
  border-radius:22px;
  border:10px solid #6b7280;
  box-shadow:0 8px 40px rgba(0,0,0,.6),inset 0 0 6px rgba(0,0,0,.2);
  padding:8px;
}
.tablet-bar{
  background:#e5e7eb;
  border-radius:8px;
  padding:4px 12px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  margin-bottom:7px;
  font-size:.68rem;
  color:#6b7280;
}
.tablet-screen{
  background:#fff;
  border-radius:10px;
  padding:14px 16px 16px;
  font-size:.8rem;
  color:#1f2937;
  line-height:1.75;
}

/* ── Screen layout ────────────────────────────────────── */
.screen-layout{display:flex;gap:14px;}
.left-col{min-width:140px;flex-shrink:0;}
.right-col{flex:1;min-width:0;}

/* Calendar */
.cal-month{font-weight:800;color:#374151;font-size:.85rem;margin-bottom:5px;}
.cal-grid{
  display:grid;
  grid-template-columns:repeat(7,1fr);
  gap:1px;
  font-size:.63rem;
  text-align:center;
  margin-bottom:10px;
}
.cal-grid .hd{font-weight:700;color:#9ca3af;padding:2px 0;}
.cal-grid .sun{color:#dc2626;}
.cal-grid .sat{color:#2563eb;}
.cal-grid .num{padding:2px 0;color:#374151;}
.cal-grid .today-cell{
  display:flex;align-items:center;justify-content:center;
}
.today-num{
  background:#ef4444;color:#fff;border-radius:50%;
  width:17px;height:17px;font-weight:700;font-size:.62rem;
  display:flex;align-items:center;justify-content:center;
}

/* Todo */
.todo-title{color:#16a34a;font-weight:800;font-size:.77rem;margin-bottom:5px;}
.todo-row{
  display:flex;align-items:flex-start;gap:4px;
  font-size:.69rem;color:#4b5563;margin-bottom:4px;
}
.chk{color:#16a34a;font-size:.77rem;flex-shrink:0;}
.todo-note{
  font-size:.67rem;color:#dc2626;font-weight:700;
  margin-top:8px;margin-bottom:4px;
}

/* Clickable zones */
.czone{
  display:inline;
  border-radius:4px;
  padding:2px 4px;
  cursor:pointer;
  font-weight:700;
  transition:filter .15s,transform .15s;
  position:relative;
}
.czone:hover{filter:brightness(1.12);transform:scale(1.015);}
.czone:active{transform:scale(.98);}
.czone.active{outline:2px solid currentColor;outline-offset:1px;}
.za{background:#fef3c7;color:#b45309;border-bottom:2px solid #f59e0b;}
.zb{background:#dcfce7;color:#15803d;border-bottom:2px solid #22c55e;}
.zc{background:#ede9fe;color:#7c3aed;border-bottom:2px solid #a78bfa;}
.zd{
  display:block;
  background:#fee2e2;color:#dc2626;
  border-radius:6px;
  padding:5px 7px;
  margin-top:3px;
  font-size:.69rem;
  border-bottom:2px solid #fca5a5;
}

/* Good Morning badge */
.gm-badge{
  display:flex;align-items:center;gap:6px;margin-bottom:8px;
}
.sun-emoji{font-size:2.0rem;line-height:1;}
.gm-text{font-size:.95rem;font-weight:800;color:#d97706;line-height:1.2;}
.story{font-size:.77rem;color:#1f2937;line-height:1.8;}

/* ── Hint strip ──────────────────────────────────────── */
.hint-strip{
  max-width:720px;margin:0 auto 18px;
  text-align:center;font-size:.76rem;color:#64748b;
}

/* ── Problem panels ───────────────────────────────────── */
.panels-wrap{max-width:720px;margin:0 auto;}
.panel{
  display:none;
  background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.09);
  border-radius:18px;
  padding:18px 18px 14px;
  margin-bottom:14px;
  animation:slideIn .35s ease;
}
.panel.show{display:block;}
@keyframes slideIn{
  from{opacity:0;transform:translateY(-12px);}
  to{opacity:1;transform:translateY(0);}
}

.ph{display:flex;align-items:center;gap:10px;margin-bottom:14px;}
.pbadge{
  width:38px;height:38px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:1.05rem;font-weight:800;flex-shrink:0;
}
.pa-bg{background:#f59e0b;color:#fff;}
.pb-bg{background:#22c55e;color:#fff;}
.pc-bg{background:#8b5cf6;color:#fff;}
.pd-bg{background:#ef4444;color:#fff;}
.pt{font-size:.92rem;font-weight:700;color:#e0e7ff;line-height:1.35;}

.ia{
  background:rgba(0,0,0,.25);
  border-radius:12px;
  padding:14px;
  margin-bottom:12px;
}
.ia-hint{
  text-align:center;font-size:.76rem;color:#7c8fa8;margin-bottom:12px;
}

/* ── Transport (A) ───────────────────────────────────── */
.tr-section-title{
  text-align:center;font-size:.73rem;font-weight:700;
  margin-bottom:7px;
}
.tgrid{
  display:flex;flex-wrap:wrap;gap:8px;
  justify-content:center;margin-bottom:10px;
}
.tbtn{
  background:rgba(255,255,255,.05);
  border:2px solid rgba(255,255,255,.12);
  border-radius:12px;
  padding:10px 12px;
  cursor:pointer;
  text-align:center;
  transition:all .2s;
  min-width:80px;
}
.tbtn:hover{transform:translateY(-2px);border-color:rgba(255,255,255,.25);}
.tbtn.sel-bus{background:rgba(245,158,11,.18);border-color:#f59e0b;}
.tbtn.sel-sub{background:rgba(59,130,246,.18);border-color:#60a5fa;}
.tbtn-icon{font-size:1.9rem;display:block;margin-bottom:3px;}
.tbtn-label{font-size:.66rem;color:#94a3b8;}

/* ── Stamp locations (B) ──────────────────────────────── */
.sgrid{
  display:grid;
  grid-template-columns:repeat(4,1fr);
  gap:8px;margin-bottom:10px;
}
.sloc{
  background:rgba(255,255,255,.05);
  border:2px solid rgba(255,255,255,.1);
  border-radius:12px;
  padding:9px 4px;
  cursor:pointer;
  text-align:center;
  transition:all .2s;
  user-select:none;
}
.sloc:hover:not(.ssel):not(.sdis){
  border-color:rgba(34,197,94,.4);
  transform:scale(1.04);
}
.sloc.ssel{background:rgba(34,197,94,.18);border-color:#22c55e;}
.sloc.sdis{opacity:.38;cursor:not-allowed;}
.sloc-icon{font-size:1.6rem;display:block;margin-bottom:3px;}
.sloc-name{font-size:.62rem;color:#94a3b8;}
.sloc-order{font-size:1.05rem;font-weight:800;color:#4ade80;margin-top:2px;}

/* ── Clothes (C) ─────────────────────────────────────── */
.clothes-row{display:flex;gap:16px;flex-wrap:wrap;}
.cg{flex:1;min-width:120px;}
.cg-title{
  text-align:center;font-size:.73rem;font-weight:700;
  color:#94a3b8;margin-bottom:8px;
}
.shirtgrid{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;}
.sbt{
  width:52px;height:52px;
  border-radius:10px;
  border:2px solid rgba(255,255,255,.12);
  cursor:pointer;
  font-size:1.6rem;
  transition:all .2s;
  background:rgba(255,255,255,.05);
  display:flex;align-items:center;justify-content:center;
}
.sbt:hover{transform:scale(1.1);}
.sbt.sel{border-color:#8b5cf6;background:rgba(139,92,246,.2);box-shadow:0 0 10px rgba(139,92,246,.4);}
.pantsgrid{display:flex;gap:10px;justify-content:center;}
.pbt{
  padding:8px 14px;
  border-radius:10px;
  border:2px solid rgba(255,255,255,.12);
  cursor:pointer;
  font-size:1.2rem;
  transition:all .2s;
  background:rgba(255,255,255,.05);
  display:flex;flex-direction:column;align-items:center;gap:3px;
}
.pbt:hover{transform:scale(1.08);}
.pbt.sel{border-color:#a78bfa;background:rgba(167,139,250,.2);}
.pbt-label{font-size:.63rem;color:#94a3b8;}

/* ── Todos (D) ───────────────────────────────────────── */
.tdgrid{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:8px;
}
.tdc{
  background:rgba(255,255,255,.04);
  border:2px solid rgba(255,255,255,.09);
  border-radius:10px;
  padding:10px 12px;
  cursor:pointer;
  transition:all .2s;
  display:flex;align-items:center;gap:8px;
  font-size:.76rem;
  color:#c4cfdf;
}
.tdc:hover:not(.tsel):not(.tdis){border-color:rgba(239,68,68,.4);}
.tdc.tsel{background:rgba(239,68,68,.14);border-color:#ef4444;color:#fca5a5;}
.tdc.tdis{opacity:.35;cursor:not-allowed;}
.tdc-icon{font-size:1.1rem;flex-shrink:0;}
.tdc-star{margin-left:auto;color:#ef4444;font-size:1rem;}

/* ── Result box ──────────────────────────────────────── */
.rbox{
  background:rgba(255,255,255,.04);
  border-radius:10px;
  padding:11px 14px;
  text-align:center;
  font-size:.82rem;
  color:#7c8fa8;
  margin-top:10px;
  min-height:44px;
  transition:all .3s;
}
.rnum{font-size:1.3rem;font-weight:800;color:#ffd166;}
.rformula{font-size:.73rem;color:#7c8fa8;margin-top:3px;font-family:'Courier New',monospace;}

/* ── Solution steps ──────────────────────────────────── */
.sol{
  display:none;
  background:rgba(255,255,255,.03);
  border-left:3px solid rgba(255,209,102,.45);
  border-radius:0 10px 10px 0;
  padding:12px 14px;
  margin-top:10px;
}
.sol.show{display:block;}
.step{
  font-size:.76rem;color:#c4cfdf;
  display:flex;align-items:flex-start;gap:7px;
  margin-bottom:7px;
}
.snum{
  background:rgba(255,209,102,.18);color:#ffd166;
  border-radius:50%;width:19px;height:19px;
  font-size:.62rem;font-weight:700;
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;margin-top:1px;
}
.key-law{color:#ffd166;font-weight:700;}

/* ── Btn row ─────────────────────────────────────────── */
.brow{display:flex;gap:8px;flex-wrap:wrap;margin-top:11px;}
.btn{
  border:none;border-radius:8px;
  padding:7px 15px;
  font-family:inherit;font-size:.77rem;font-weight:600;
  cursor:pointer;transition:all .18s;
}
.btn-sol{background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;}
.btn-sol:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(245,158,11,.4);}
.btn-rst{background:rgba(255,255,255,.07);color:#94a3b8;border:1px solid rgba(255,255,255,.1);}
.btn-rst:hover{background:rgba(255,255,255,.12);}

/* ── Summary box ─────────────────────────────────────── */
.summary{
  max-width:720px;margin:16px auto 6px;
  background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.08);
  border-radius:18px;
  padding:16px;
}
.sum-title{
  text-align:center;font-size:.98rem;font-weight:700;
  color:#ffd166;margin-bottom:14px;
}
.sum-grid{
  display:grid;
  grid-template-columns:repeat(2,1fr);
  gap:10px;
}
.sc{
  background:rgba(255,255,255,.03);
  border-radius:12px;padding:11px 10px;
  text-align:center;
  border:1px solid rgba(255,255,255,.06);
  opacity:.35;transition:all .4s;
}
.sc.done{opacity:1;border-color:rgba(255,209,102,.35);}
.sc-lbl{font-size:.68rem;color:#64748b;margin-bottom:4px;}
.sc-ans{font-size:1.25rem;font-weight:800;color:#ffd166;}
.sc-frm{font-size:.62rem;color:#475569;font-family:monospace;margin-top:3px;}

/* ── responsive ─────────────────────────────────────── */
@media(max-width:500px){
  .sgrid{grid-template-columns:repeat(4,1fr);}
  .tdgrid{grid-template-columns:1fr;}
  .sum-grid{grid-template-columns:1fr;}
  .screen-layout{flex-direction:column;}
  .left-col{min-width:unset;}
}
</style>
</head>
<body>

<!-- ═══ HEADER ═══════════════════════════════════════════════════ -->
<div class="page-title">📱 경우의 수로 바라본 하루</div>
<div class="page-sub">
  수민이의 하루 일기에서 경우의 수를 찾아보세요!<br>
  <div class="click-badges">
    형광펜 표시 부분을 클릭하면 문제가 열려요 👆
    <span class="cb cb-a">ⓐ</span>
    <span class="cb cb-b">ⓑ</span>
    <span class="cb cb-c">ⓒ</span>
    <span class="cb cb-d">ⓓ</span>
  </div>
</div>

<!-- ═══ TABLET ════════════════════════════════════════════════════ -->
<div class="tablet-wrap">
  <div class="tablet-bar">
    <span>오전 10:30 &nbsp;○월 ○일 ○요일</span>
    <span>📶 100% 🔋</span>
  </div>
  <div class="tablet-screen">
    <div class="screen-layout">

      <!-- LEFT: Calendar + Todo -->
      <div class="left-col">
        <div class="cal-month">5 May</div>
        <div class="cal-grid">
          <div class="hd sun">일</div><div class="hd">월</div><div class="hd">화</div>
          <div class="hd">수</div><div class="hd">목</div><div class="hd">금</div><div class="hd sat">토</div>
          <div></div><div></div><div></div><div></div><div></div>
          <div class="num">1</div><div class="num sat">2</div>
          <div class="num sun">4</div><div class="num">5</div><div class="num">6</div>
          <div class="num">7</div><div class="num">8</div><div class="num">9</div><div class="num sat">10</div>
          <div class="num sun">11</div><div class="num">12</div><div class="num">13</div>
          <div class="num">14</div><div class="num">15</div><div class="num">16</div><div class="num sat">17</div>
          <div class="num sun">18</div><div class="num">19</div><div class="num">20</div>
          <div class="num">21</div><div class="num">22</div><div class="num">23</div><div class="num sat">24</div>
          <div class="num sun">25</div><div class="num">26</div><div class="num">27</div>
          <div class="num">28</div><div class="num">29</div>
          <div class="today-cell"><div class="today-num">30</div></div>
          <div class="num sat">31</div>
        </div>

        <div class="todo-title">To Do List</div>
        <div class="todo-row"><span class="chk">✓</span> 영어 단어 30개 외우기</div>
        <div class="todo-row"><span class="chk">✓</span> 경우의 수 복습</div>
        <div class="todo-row"><span class="chk">✓</span> 아침 10분 달리기</div>
        <div class="todo-row"><span class="chk">✓</span> 책 2권 읽기 📚</div>
        <div class="todo-row"><span class="chk">✓</span> 12시 전에 잠자기</div>
        <div class="todo-row"><span class="chk">✓</span> 체험 보고서 쓰기 📋</div>

        <div class="todo-note">할 일이 많으니까</div>
        <span onclick="openPanel('d')" class="czone zd">
          ⓓ 이 중에서 꼭 해야 하는 일을 3개 골라서 별표를 해 놓자!
        </span>
      </div>

      <!-- RIGHT: Story -->
      <div class="right-col">
        <div class="gm-badge">
          <span class="sun-emoji">🌞</span>
          <div class="gm-text">Good<br>Morning</div>
        </div>
        <div class="story">
          내일은 현장 학습! 담임 선생님께서 공원 안내소로 늦지 않게 오라고 하셨다.
          찾아보니 <span onclick="openPanel('a')" class="czone za">ⓐ 우리 집에서 공원까지 바로 가는 버스 노선이 3개 있고,
          지하철 노선도 2개 있네. 뭐 타고 갈까?</span>
          <br><br>
          이 공원은 <span onclick="openPanel('b')" class="czone zb">ⓑ 8개의 스탬프 찍는 곳이 있다고 한다. 선생님께서 모둠별로
          4곳을 정해서 방문하고 순서대로 스탬프를 찍어와야 한다고 하셨다.</span>
          우리 모둠은 아직 안 정했는데, 모둠장에게 연락해서 어디를 어떤 순서로 같이 이야기해 봐야겠다.
          <br><br>
          내일 친구들이랑 만날 생각하니 기대된다. 멋지게 꾸미고 가야지!
          <span onclick="openPanel('c')" class="czone zc">ⓒ 내일은 어떻게 입고 나갈까? 상의는 셔츠 5종류 중에
          하나 입으면 되고, 바지는 청바지·면바지 둘 중에서 하나를 고르면 될 것 같은데?</span>
          &nbsp;🧥👖
        </div>
      </div>

    </div>
  </div>
</div>

<!-- hint -->
<div class="hint-strip">
  💡 색칠된 부분(<span class="cb cb-a" style="cursor:default">ⓐ</span>
  <span class="cb cb-b" style="cursor:default">ⓑ</span>
  <span class="cb cb-c" style="cursor:default">ⓒ</span>
  <span class="cb cb-d" style="cursor:default">ⓓ</span>)을 클릭하면 해당 문제 패널이 펼쳐집니다!
</div>

<!-- ═══ PANELS ════════════════════════════════════════════════════ -->
<div class="panels-wrap">

  <!-- ── Panel A ── -->
  <div id="panel-a" class="panel">
    <div class="ph">
      <div class="pbadge pa-bg">ⓐ</div>
      <div class="pt">집에서 공원까지 가는 교통수단을 고르는 경우의 수</div>
    </div>
    <div class="ia">
      <div class="ia-hint">버스나 지하철 중 하나를 클릭해보세요! 🚌🚇</div>
      <div class="tr-section-title" style="color:#fbbf24;">🚌 버스 노선 (3가지)</div>
      <div class="tgrid" id="bus-grid"></div>
      <div class="tr-section-title" style="color:#60a5fa;margin-top:4px;">🚇 지하철 노선 (2가지)</div>
      <div class="tgrid" id="sub-grid"></div>
      <div id="res-a" class="rbox">교통수단을 하나 선택해보세요</div>
    </div>
    <div class="brow">
      <button class="btn btn-sol" onclick="solToggle('a')">📐 풀이 보기</button>
      <button class="btn btn-rst" onclick="resetA()">↺ 초기화</button>
    </div>
    <div id="sol-a" class="sol">
      <div class="step"><div class="snum">1</div>
        <span>버스와 지하철은 <span class="key-law">동시에 탈 수 없어요</span> → <span class="key-law">합의 법칙</span> 사용!</span></div>
      <div class="step"><div class="snum">2</div>
        <span>버스 노선: <strong>3가지</strong>, 지하철 노선: <strong>2가지</strong></span></div>
      <div class="step"><div class="snum">3</div>
        <span>경우의 수 = 3 + 2 = <span class="rnum" style="font-size:1rem">5가지</span></span></div>
      <div class="step"><div class="snum">💡</div>
        <span class="key-law">합의 법칙: A 또는 B 중 하나를 선택 → m + n가지</span></div>
    </div>
  </div>

  <!-- ── Panel B ── -->
  <div id="panel-b" class="panel">
    <div class="ph">
      <div class="pbadge pb-bg">ⓑ</div>
      <div class="pt">8곳의 장소 중에서 4곳을 선택하여 방문하는 순서를 정하는 경우의 수</div>
    </div>
    <div class="ia">
      <div class="ia-hint">방문할 4곳을 순서대로 클릭하세요! 순서가 다르면 다른 경우예요 🗺️</div>
      <div class="sgrid" id="stamp-grid"></div>
      <div id="res-b" class="rbox">장소를 순서대로 4곳 클릭해보세요</div>
    </div>
    <div class="brow">
      <button class="btn btn-sol" onclick="solToggle('b')">📐 풀이 보기</button>
      <button class="btn btn-rst" onclick="resetB()">↺ 초기화</button>
    </div>
    <div id="sol-b" class="sol">
      <div class="step"><div class="snum">1</div>
        <span><span class="key-law">순서가 중요</span>하니까 <span class="key-law">순열(P)</span>을 씁니다!</span></div>
      <div class="step"><div class="snum">2</div>
        <span>1번째 장소: <strong>8가지</strong> → 2번째: <strong>7가지</strong> → 3번째: <strong>6가지</strong> → 4번째: <strong>5가지</strong></span></div>
      <div class="step"><div class="snum">3</div>
        <span>P(8,4) = 8 × 7 × 6 × 5 = <span class="rnum" style="font-size:1rem">1680가지</span></span></div>
      <div class="step"><div class="snum">💡</div>
        <span class="key-law">순열: n개 중 r개를 순서 있게 나열 → P(n,r) = n!÷(n-r)!</span></div>
    </div>
  </div>

  <!-- ── Panel C ── -->
  <div id="panel-c" class="panel">
    <div class="ph">
      <div class="pbadge pc-bg">ⓒ</div>
      <div class="pt">셔츠 5종류와 바지 2종류 중에서 각각 하나씩 택하여 입는 경우의 수</div>
    </div>
    <div class="ia">
      <div class="ia-hint">셔츠 하나, 바지 하나를 골라 오늘의 코디를 완성해보세요! 👗</div>
      <div class="clothes-row">
        <div class="cg">
          <div class="cg-title">👕 셔츠 (5종류)</div>
          <div class="shirtgrid" id="shirt-grid"></div>
        </div>
        <div class="cg">
          <div class="cg-title">👖 바지 (2종류)</div>
          <div class="pantsgrid" id="pants-grid"></div>
        </div>
      </div>
      <div id="res-c" class="rbox">셔츠와 바지를 각각 하나씩 선택해보세요</div>
    </div>
    <div class="brow">
      <button class="btn btn-sol" onclick="solToggle('c')">📐 풀이 보기</button>
      <button class="btn btn-rst" onclick="resetC()">↺ 초기화</button>
    </div>
    <div id="sol-c" class="sol">
      <div class="step"><div class="snum">1</div>
        <span>셔츠 고르기와 바지 고르기는 <span class="key-law">동시에 일어나요</span> → <span class="key-law">곱의 법칙</span>!</span></div>
      <div class="step"><div class="snum">2</div>
        <span>셔츠: <strong>5가지</strong>, 바지: <strong>2가지</strong></span></div>
      <div class="step"><div class="snum">3</div>
        <span>경우의 수 = 5 × 2 = <span class="rnum" style="font-size:1rem">10가지</span></span></div>
      <div class="step"><div class="snum">💡</div>
        <span class="key-law">곱의 법칙: A이고 B일 때(둘 다 선택) → m × n가지</span></div>
    </div>
  </div>

  <!-- ── Panel D ── -->
  <div id="panel-d" class="panel">
    <div class="ph">
      <div class="pbadge pd-bg">ⓓ</div>
      <div class="pt">할 일 목록 6가지 중에서 꼭 해야 하는 목록을 3가지 고르는 경우의 수</div>
    </div>
    <div class="ia">
      <div class="ia-hint">반드시 해야 할 일 3가지를 골라보세요! 순서는 상관없어요 ✅</div>
      <div class="tdgrid" id="todo-grid"></div>
      <div id="res-d" class="rbox">할 일 3가지를 선택해보세요</div>
    </div>
    <div class="brow">
      <button class="btn btn-sol" onclick="solToggle('d')">📐 풀이 보기</button>
      <button class="btn btn-rst" onclick="resetD()">↺ 초기화</button>
    </div>
    <div id="sol-d" class="sol">
      <div class="step"><div class="snum">1</div>
        <span><span class="key-law">순서 없이 고르기</span>만 하니까 <span class="key-law">조합(C)</span>을 씁니다!</span></div>
      <div class="step"><div class="snum">2</div>
        <span>6가지 중 3가지를 순서 없이 선택</span></div>
      <div class="step"><div class="snum">3</div>
        <span>C(6,3) = 6! ÷ (3! × 3!) = 720 ÷ 36 = <span class="rnum" style="font-size:1rem">20가지</span></span></div>
      <div class="step"><div class="snum">💡</div>
        <span class="key-law">조합: n개 중 r개를 순서 없이 선택 → C(n,r) = n!÷(r!×(n-r)!)</span></div>
    </div>
  </div>

</div><!-- /panels-wrap -->

<!-- ═══ SUMMARY ═══════════════════════════════════════════════════ -->
<div class="summary">
  <div class="sum-title">📊 수민이의 하루 — 경우의 수 한눈에 보기</div>
  <div class="sum-grid">
    <div class="sc" id="sum-a">
      <div class="sc-lbl">ⓐ 교통수단 선택</div>
      <div class="sc-ans">5가지</div>
      <div class="sc-frm">3 + 2 = 5 &nbsp;(합의 법칙)</div>
    </div>
    <div class="sc" id="sum-b">
      <div class="sc-lbl">ⓑ 스탬프 장소 순서</div>
      <div class="sc-ans">1680가지</div>
      <div class="sc-frm">P(8,4) = 8×7×6×5</div>
    </div>
    <div class="sc" id="sum-c">
      <div class="sc-lbl">ⓒ 옷 코디 선택</div>
      <div class="sc-ans">10가지</div>
      <div class="sc-frm">5 × 2 = 10 &nbsp;(곱의 법칙)</div>
    </div>
    <div class="sc" id="sum-d">
      <div class="sc-lbl">ⓓ 할 일 고르기</div>
      <div class="sc-ans">20가지</div>
      <div class="sc-frm">C(6,3) = 20</div>
    </div>
  </div>
</div>

<!-- ═══ SCRIPT ════════════════════════════════════════════════════ -->
<script>
// ── helpers ────────────────────────────────────────────────────
function fact(n){let r=1;for(let i=2;i<=n;i++)r*=i;return r;}
function comb(n,r){return fact(n)/(fact(r)*fact(n-r));}

// ── panel open/close ────────────────────────────────────────────
function openPanel(id){
  const p=document.getElementById('panel-'+id);
  const isOpen=p.classList.contains('show');
  // 모든 패널 닫기
  ['a','b','c','d'].forEach(x=>{
    document.getElementById('panel-'+x).classList.remove('show');
    document.getElementById('sol-'+x).classList.remove('show');
  });
  if(!isOpen){
    p.classList.add('show');
    setTimeout(()=>p.scrollIntoView({behavior:'smooth',block:'nearest'}),50);
    document.getElementById('sum-'+id).classList.add('done');
  }
}

function solToggle(id){
  document.getElementById('sol-'+id).classList.toggle('show');
}

// ══════════════════════════════════════════════════════════════
// PANEL A — 교통수단
// ══════════════════════════════════════════════════════════════
const BUSES=[
  {icon:'🚌',label:'1번 버스'},
  {icon:'🚎',label:'2번 버스'},
  {icon:'🚐',label:'3번 버스'},
];
const SUBS=[
  {icon:'🚇',label:'A호선'},
  {icon:'🚊',label:'B호선'},
];
let selTr=null;

function initA(){
  document.getElementById('bus-grid').innerHTML=BUSES.map((b,i)=>
    `<div class="tbtn" id="bus-${i}" onclick="selTransport('bus',${i})">
      <span class="tbtn-icon">${b.icon}</span>
      <span class="tbtn-label">${b.label}</span>
    </div>`).join('');
  document.getElementById('sub-grid').innerHTML=SUBS.map((s,i)=>
    `<div class="tbtn" id="sub-${i}" onclick="selTransport('sub',${i})">
      <span class="tbtn-icon">${s.icon}</span>
      <span class="tbtn-label">${s.label}</span>
    </div>`).join('');
}

function selTransport(type,idx){
  BUSES.forEach((_,i)=>{const e=document.getElementById('bus-'+i);if(e)e.className='tbtn';});
  SUBS.forEach((_,i)=>{const e=document.getElementById('sub-'+i);if(e)e.className='tbtn';});
  selTr={type,idx};
  document.getElementById(type+'-'+idx).classList.add(type==='bus'?'sel-bus':'sel-sub');
  const info=type==='bus'?BUSES[idx]:SUBS[idx];
  document.getElementById('res-a').innerHTML=
    `${info.icon} <strong>${info.label}</strong> 을 선택했어요!<br>
    <span class="rformula">버스 3가지 + 지하철 2가지 중 하나 → <span class="rnum">5가지</span></span>`;
}

function resetA(){
  selTr=null;
  BUSES.forEach((_,i)=>{const e=document.getElementById('bus-'+i);if(e)e.className='tbtn';});
  SUBS.forEach((_,i)=>{const e=document.getElementById('sub-'+i);if(e)e.className='tbtn';});
  document.getElementById('res-a').innerHTML='교통수단을 하나 선택해보세요';
  document.getElementById('sol-a').classList.remove('show');
}

initA();

// ══════════════════════════════════════════════════════════════
// PANEL B — 스탬프 장소
// ══════════════════════════════════════════════════════════════
const PLACES=[
  {icon:'🌸',name:'벚꽃길'},
  {icon:'🏛️',name:'역사관'},
  {icon:'🎠',name:'놀이터'},
  {icon:'🦋',name:'나비원'},
  {icon:'⛲',name:'분수대'},
  {icon:'☕',name:'카페'},
  {icon:'🌿',name:'허브정원'},
  {icon:'🎡',name:'전망대'},
];
let stampSeq=[];

function initB(){renderStamps();}

function renderStamps(){
  const g=document.getElementById('stamp-grid');
  g.innerHTML=PLACES.map((p,i)=>{
    const pos=stampSeq.indexOf(i);
    const sel=pos>=0;
    const dis=!sel&&stampSeq.length>=4;
    return `<div class="sloc${sel?' ssel':''}${dis?' sdis':''}"
              onclick="${dis?'':'stampClick('+i+')'}">
      <span class="sloc-icon">${p.icon}</span>
      <div class="sloc-name">${p.name}</div>
      ${sel?`<div class="sloc-order">${pos+1}번째</div>`:''}
    </div>`;
  }).join('');

  const rbox=document.getElementById('res-b');
  if(stampSeq.length===4){
    const route=stampSeq.map(i=>PLACES[i].icon+' '+PLACES[i].name).join(' → ');
    rbox.innerHTML=`${route}<br>
      <span class="rformula">P(8,4) = 8×7×6×5 = <span class="rnum">1680가지</span> 중 하나!</span>`;
  } else if(stampSeq.length>0){
    rbox.innerHTML=`${stampSeq.length}/4곳 선택됨 — ${4-stampSeq.length}곳 더 선택하세요`;
  } else {
    rbox.innerHTML='장소를 순서대로 4곳 클릭해보세요';
  }
}

function stampClick(i){
  const pos=stampSeq.indexOf(i);
  if(pos>=0) stampSeq.splice(pos,1);
  else { if(stampSeq.length>=4)return; stampSeq.push(i); }
  renderStamps();
}

function resetB(){
  stampSeq=[];
  renderStamps();
  document.getElementById('sol-b').classList.remove('show');
}

initB();

// ══════════════════════════════════════════════════════════════
// PANEL C — 옷 코디
// ══════════════════════════════════════════════════════════════
const SHIRTS=[
  {icon:'👕',name:'민트 셔츠'},
  {icon:'🩱',name:'스트라이프'},
  {icon:'🎽',name:'스포티'},
  {icon:'👔',name:'체크 셔츠'},
  {icon:'🥼',name:'자켓'},
];
const PANTS=[
  {icon:'👖',name:'청바지'},
  {icon:'🩳',name:'면바지'},
];
let selShirt=null, selPants=null;

function initC(){
  document.getElementById('shirt-grid').innerHTML=SHIRTS.map((s,i)=>
    `<div class="sbt" id="sh-${i}" onclick="pickShirt(${i})" title="${s.name}">${s.icon}</div>`
  ).join('');
  document.getElementById('pants-grid').innerHTML=PANTS.map((p,i)=>
    `<div class="pbt" id="pt-${i}" onclick="pickPants(${i})">
      <span style="font-size:1.55rem">${p.icon}</span>
      <span class="pbt-label">${p.name}</span>
    </div>`
  ).join('');
}

function pickShirt(i){
  SHIRTS.forEach((_,j)=>{const e=document.getElementById('sh-'+j);if(e)e.classList.remove('sel');});
  document.getElementById('sh-'+i).classList.add('sel');
  selShirt=i; updateClothes();
}

function pickPants(i){
  PANTS.forEach((_,j)=>{const e=document.getElementById('pt-'+j);if(e)e.classList.remove('sel');});
  document.getElementById('pt-'+i).classList.add('sel');
  selPants=i; updateClothes();
}

function updateClothes(){
  const r=document.getElementById('res-c');
  if(selShirt!==null && selPants!==null){
    r.innerHTML=`${SHIRTS[selShirt].icon} ${SHIRTS[selShirt].name} &nbsp;+&nbsp; ${PANTS[selPants].icon} ${PANTS[selPants].name}<br>
      <span class="rformula">셔츠 5가지 × 바지 2가지 = <span class="rnum">10가지</span> 코디 중 하나!</span>`;
  } else if(selShirt!==null){
    r.innerHTML=`${SHIRTS[selShirt].icon} 셔츠 선택 완료! 이제 바지를 골라보세요 👖`;
  } else if(selPants!==null){
    r.innerHTML=`${PANTS[selPants].icon} 바지 선택 완료! 이제 셔츠를 골라보세요 👕`;
  }
}

function resetC(){
  selShirt=null; selPants=null;
  SHIRTS.forEach((_,i)=>{const e=document.getElementById('sh-'+i);if(e)e.classList.remove('sel');});
  PANTS.forEach((_,i)=>{const e=document.getElementById('pt-'+i);if(e)e.classList.remove('sel');});
  document.getElementById('res-c').innerHTML='셔츠와 바지를 각각 하나씩 선택해보세요';
  document.getElementById('sol-c').classList.remove('show');
}

initC();

// ══════════════════════════════════════════════════════════════
// PANEL D — 할 일 목록
// ══════════════════════════════════════════════════════════════
const TODOS=[
  {icon:'📖',name:'영어 단어 30개 외우기'},
  {icon:'🔢',name:'경우의 수 복습'},
  {icon:'🏃',name:'아침 10분 달리기'},
  {icon:'📚',name:'책 2권 읽기'},
  {icon:'😴',name:'12시 전에 잠자기'},
  {icon:'📋',name:'체험 보고서 쓰기'},
];
let selTodo=new Set();

function initD(){renderTodos();}

function renderTodos(){
  const g=document.getElementById('todo-grid');
  g.innerHTML=TODOS.map((t,i)=>{
    const sel=selTodo.has(i);
    const dis=!sel&&selTodo.size>=3;
    return `<div class="tdc${sel?' tsel':''}${dis?' tdis':''}"
              onclick="${dis?'':'todoClick('+i+')'}">
      <span class="tdc-icon">${t.icon}</span>
      <span>${t.name}</span>
      ${sel?'<span class="tdc-star">★</span>':''}
    </div>`;
  }).join('');

  const r=document.getElementById('res-d');
  if(selTodo.size===3){
    const chosen=[...selTodo].map(i=>TODOS[i].icon+' '+TODOS[i].name).join(', ');
    r.innerHTML=`${chosen}<br>
      <span class="rformula">C(6,3) = 20가지 중 하나! → <span class="rnum">20가지</span></span>`;
  } else if(selTodo.size>0){
    r.innerHTML=`${selTodo.size}/3개 선택됨 — ${3-selTodo.size}개 더 선택하세요`;
  } else {
    r.innerHTML='할 일 3가지를 선택해보세요';
  }
}

function todoClick(i){
  if(selTodo.has(i)) selTodo.delete(i);
  else { if(selTodo.size>=3)return; selTodo.add(i); }
  renderTodos();
}

function resetD(){
  selTodo=new Set();
  renderTodos();
  document.getElementById('sol-d').classList.remove('show');
}

initD();
</script>
</body>
</html>"""


def render():
    st.markdown("### 📱 경우의 수로 바라본 하루")
    st.markdown(
        "수민이의 하루 이야기 속 **ⓐ~ⓓ 네 가지 상황**을 직접 클릭하며 "
        "**합의 법칙 · 곱의 법칙 · 순열 · 조합**을 탐구해보세요!"
    )
    components.html(_HTML, height=1700, scrolling=True)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
