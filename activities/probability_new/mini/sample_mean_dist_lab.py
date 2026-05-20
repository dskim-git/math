# activities/probability_new/mini/sample_mean_dist_lab.py
"""
표본평균의 평균·분산·표준편차 시뮬레이터.
- 모집단에서 크기 n인 표본을 임의추출(복원)하여 표본평균 X̄을 누적
- n을 1→5까지 조절하며 E(X̄), V(X̄), σ(X̄)가 m, σ²/n, σ/√n에 수렴하는 모습 관찰
- 모든 경우 한꺼번에 열거(N^n)도 가능
- 3 탭: ① 주머니 속 공 {2,4,6,8}, ② 주사위 {1..6}, ③ 카드 {1,3,5,7,9}
"""
import json
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🎲 미니: 표본평균의 평균·분산·표준편차 시뮬레이터",
    "description": "표본의 크기 n을 늘리며 표본평균의 평균·분산·표준편차가 m, σ²/n, σ/√n로 수렴하는 과정을 관찰합니다.",
    "order": 7,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "표본평균분포시뮬"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 표본평균의 평균·분산·표준편차**"},
    {
        "key": "E_Xbar_관찰",
        "label": "표본의 크기 n을 1, 2, 3, 4, 5로 늘려가며 시뮬레이션해 봤을 때, 표본평균의 평균 **E(X̄)** 값은 어떻게 변했나요? 모평균 m과 어떤 관계가 있었나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "n이 바뀌어도 E(X̄)은 ___였고, 모평균 m과 ___...",
    },
    {
        "key": "V_Xbar_관찰",
        "label": "표본평균의 분산 **V(X̄)**은 n이 커질수록 어떻게 변했나요? 모분산 σ²과 어떤 식의 관계가 있을 것 같나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "n이 커질수록 V(X̄)은 ___ 했고, 식으로 쓰면 V(X̄) = ___...",
    },
    {
        "key": "sigma_Xbar_관찰",
        "label": "표본평균의 표준편차 **σ(X̄)**은 n=1, 4, 9 일 때 어떤 비율로 작아졌나요? σ(X̄)과 모표준편차 σ의 관계를 식으로 적어 보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "n=1일 때 σ(X̄) = ___, n=4일 때 ___, n=9일 때 ___. 따라서 σ(X̄) = ___",
    },
    {
        "key": "모든경우열거",
        "label": "‘모든 경우(N^n)를 한꺼번에’ 버튼을 눌렀을 때와, 표본을 100번씩 직접 뽑았을 때 결과가 어떻게 달랐나요? 왜 그런 결과가 나왔다고 생각하나요?",
        "type": "text_area",
        "height": 100,
        "placeholder": "모든 경우를 열거하면 ___이고, 100번 뽑기는 ___ 때문에...",
    },
    {
        "key": "탭간_공통점",
        "label": "주머니 속 공·주사위·카드 세 모집단은 값이 모두 달랐는데도, n이 커질수록 X̄의 분포에서 똑같이 나타난 현상은 무엇이었나요?",
        "type": "text_area",
        "height": 100,
        "placeholder": "세 모집단 모두 n이 커질수록 X̄의 분포가 ___ 모양에 가까워졌고...",
    },
    {
        "key": "n키우면",
        "label": "결국 표본의 크기 n을 크게 한다는 것은 어떤 의미가 있나요? (모평균 추정과 연결지어 생각해 보세요)",
        "type": "text_area",
        "height": 100,
        "placeholder": "n을 크게 하면 X̄이 m에 ___, 그래서 모평균을 ___...",
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 이 활동을 통해 새롭게 알게 된 점",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "느낀점",
        "label": "💬 활동을 마친 후 느낀 점",
        "type": "text_area",
        "height": 90,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# 공통 HTML 템플릿 — population/theme 값만 바꿔 3번 사용
# ─────────────────────────────────────────────────────────────────────────────
_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,__BG_MID__ 50%,#0f172a 100%);
  color:#e2e8f0;padding:14px 12px;min-height:100vh;
}

/* ===== 헤더 ===== */
.hdr{
  text-align:center;
  background:linear-gradient(135deg,__HDR_A__,__HDR_B__);
  border:2px solid __HDR_BORDER__;border-radius:18px;
  padding:14px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.45rem;font-weight:900;color:__HDR_TXT__;margin-bottom:4px}
.hdr p{font-size:1rem;color:#cbd5e1;line-height:1.55}
.hdr b{color:#fde047}
.xb{display:inline-block;text-decoration:overline;text-decoration-thickness:1.5px;padding:0 1px;line-height:1}

/* ===== 패널 ===== */
.panel{
  background:rgba(15,23,42,.72);border:1.5px solid rgba(99,102,241,.3);
  border-radius:14px;padding:14px;margin-bottom:12px;
}
.panel h2{
  font-size:1.1rem;font-weight:900;color:__ACC__;margin-bottom:10px;
  display:flex;align-items:center;gap:8px;
}

/* ===== 모집단 시각화 ===== */
.pop-row{
  display:grid;grid-template-columns:1fr 220px;gap:12px;
}
@media(max-width:760px){.pop-row{grid-template-columns:1fr}}

.pop-viz{
  position:relative;height:170px;
  background:radial-gradient(ellipse at center,rgba(30,41,59,.85),rgba(15,23,42,.95));
  border:2px solid __ACC_DIM__;border-radius:120px / 80px;overflow:hidden;
}
.pop-viz .label{
  position:absolute;top:6px;left:50%;transform:translateX(-50%);
  font-size:.82rem;color:#94a3b8;font-weight:700;letter-spacing:.5px;
}
.ball{
  position:absolute;width:60px;height:60px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-size:1.5rem;font-weight:900;
  background:radial-gradient(circle at 30% 30%,#fde047,#f59e0b);
  color:#1f2937;border:3px solid #fbbf24;
  box-shadow:0 4px 12px rgba(251,191,36,.45),inset 0 -4px 8px rgba(0,0,0,.2);
  transition:all .35s cubic-bezier(.34,1.56,.64,1);
}
.ball.dim{opacity:.32;filter:grayscale(.4)}
.ball.pick{
  transform:scale(1.18);
  box-shadow:0 0 0 4px #f43f5e,0 6px 20px rgba(244,63,94,.6),inset 0 -4px 8px rgba(0,0,0,.2);
  z-index:5;
}

.pop-stats{
  display:flex;flex-direction:column;gap:6px;
  background:rgba(244,63,94,.08);border:1.5px solid rgba(244,63,94,.35);
  border-radius:11px;padding:10px;
}
.ps-title{
  font-size:.85rem;color:#fb7185;font-weight:800;
  text-align:center;margin-bottom:2px;letter-spacing:.3px;
}
.ps-row{
  display:flex;justify-content:space-between;align-items:center;
  font-size:1rem;font-weight:700;color:#fecaca;
  padding:2px 4px;
}
.ps-row .v{color:#fda4af;font-weight:900;font-size:1.08rem}

/* ===== 표본 추출 컨트롤 ===== */
.ctrl-row{
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  background:rgba(56,189,248,.08);border:1.5px solid rgba(56,189,248,.3);
  border-radius:11px;padding:10px;margin-bottom:10px;
}
.ctrl-lab{font-size:1rem;font-weight:800;color:#7dd3fc;min-width:96px}
.ctrl-range{flex:1;min-width:130px;accent-color:#38bdf8;height:6px}
.ctrl-val{
  font-size:1.4rem;font-weight:900;color:#fde047;min-width:38px;
  background:rgba(15,23,42,.7);padding:2px 12px;border-radius:8px;text-align:center;
}

.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}
.btn{
  flex:1;min-width:120px;padding:10px 12px;border:none;border-radius:11px;
  font-size:.97rem;font-weight:900;color:#fff;cursor:pointer;
  transition:all .15s ease;letter-spacing:.3px;
}
.btn:active{transform:scale(.96)}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn-1{background:linear-gradient(135deg,#3b82f6,#1d4ed8);box-shadow:0 3px 10px rgba(59,130,246,.4)}
.btn-1:hover:not(:disabled){background:linear-gradient(135deg,#2563eb,#1e40af);transform:translateY(-1px)}
.btn-2{background:linear-gradient(135deg,#a855f7,#7c3aed);box-shadow:0 3px 10px rgba(168,85,247,.4)}
.btn-2:hover:not(:disabled){background:linear-gradient(135deg,#9333ea,#6d28d9);transform:translateY(-1px)}
.btn-3{background:linear-gradient(135deg,#22c55e,#15803d);box-shadow:0 3px 10px rgba(34,197,94,.4)}
.btn-3:hover:not(:disabled){background:linear-gradient(135deg,#16a34a,#14532d);transform:translateY(-1px)}
.btn-r{background:rgba(71,85,105,.65);border:1.5px solid rgba(148,163,184,.3);flex:0 1 110px}
.btn-r:hover:not(:disabled){background:rgba(71,85,105,.9)}

/* ===== 최근 표본 ===== */
.sample-box{
  background:rgba(34,197,94,.08);border:2px solid rgba(34,197,94,.4);
  border-radius:12px;padding:11px;
}
.sb-title{
  font-size:.95rem;font-weight:800;color:#86efac;margin-bottom:7px;
  display:flex;justify-content:space-between;align-items:center;
}
.sb-xbar{color:#fde047;font-weight:900;font-size:1.05rem}
.sb-chips{display:flex;flex-wrap:wrap;gap:7px;min-height:34px;align-items:center}
.sb-chip{
  display:inline-flex;align-items:center;justify-content:center;
  width:42px;height:42px;border-radius:50%;
  background:radial-gradient(circle at 30% 30%,#fde047,#f59e0b);
  color:#1f2937;font-weight:900;font-size:1.05rem;
  border:2px solid #fbbf24;
  box-shadow:0 3px 8px rgba(251,191,36,.4);
  animation:chipIn .3s cubic-bezier(.34,1.56,.64,1);
}
@keyframes chipIn{from{opacity:0;transform:scale(.3) rotate(-15deg)}to{opacity:1;transform:scale(1) rotate(0)}}
.sb-empty{color:#64748b;font-size:.92rem;font-style:italic}

/* ===== 분포 ===== */
.dist-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(99,102,241,.25);
  border-radius:11px;padding:10px;
}
.dist-title{
  display:flex;justify-content:space-between;align-items:center;
  font-size:.95rem;font-weight:800;color:#cbd5e1;margin-bottom:8px;
}
.dist-cnt{color:#fde047;font-weight:900}
#distCanvas{
  display:block;width:100%;height:230px;
  background:rgba(15,23,42,.5);border-radius:8px;
}

/* ===== 통계 비교 ===== */
.stats{
  display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px;
}
@media(max-width:680px){.stats{grid-template-columns:1fr}}
.s-card{
  background:rgba(30,41,59,.75);border-radius:12px;padding:11px;
  border:1.5px solid rgba(99,102,241,.3);
}
.s-card.s-mean{border-color:rgba(244,63,94,.5);background:rgba(244,63,94,.08)}
.s-card.s-var {border-color:rgba(168,85,247,.5);background:rgba(168,85,247,.08)}
.s-card.s-sd  {border-color:rgba(56,189,248,.5);background:rgba(56,189,248,.08)}

.s-head{font-size:.95rem;font-weight:800;margin-bottom:4px;letter-spacing:.3px}
.s-card.s-mean .s-head{color:#fb7185}
.s-card.s-var  .s-head{color:#c4b5fd}
.s-card.s-sd   .s-head{color:#7dd3fc}

.s-val{font-size:1.5rem;font-weight:900;color:#fef3c7;letter-spacing:.5px;line-height:1.1}
.s-sub{font-size:.82rem;color:#94a3b8;margin-top:4px;line-height:1.4}
.s-sub .th{color:#fde047;font-weight:800}
.s-bar-track{
  height:8px;background:rgba(15,23,42,.7);border-radius:4px;
  overflow:hidden;margin-top:6px;
}
.s-bar-fill{
  height:100%;border-radius:4px;
  transition:width .35s cubic-bezier(.4,1.6,.7,.95);
}
.s-mean .s-bar-fill{background:linear-gradient(90deg,#f43f5e,#fb7185)}
.s-var  .s-bar-fill{background:linear-gradient(90deg,#a855f7,#c4b5fd)}
.s-sd   .s-bar-fill{background:linear-gradient(90deg,#0ea5e9,#7dd3fc)}

/* ===== 인사이트 ===== */
.insight{
  background:rgba(251,191,36,.1);border:1.5px solid rgba(251,191,36,.4);
  border-radius:12px;padding:11px 14px;margin-top:12px;
  font-size:.95rem;color:#fef3c7;line-height:1.65;
  display:flex;align-items:flex-start;gap:9px;
}
.insight .ico{font-size:1.4rem;flex-shrink:0}
.insight b{color:#fde047}

/* ===== n별 요약표 ===== */
.summary-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(99,102,241,.3);
  border-radius:11px;padding:10px;margin-top:10px;overflow-x:auto;
}
.summary-wrap h3{
  font-size:1rem;font-weight:800;color:#c4b5fd;margin-bottom:8px;
}
table.sumtab{
  width:100%;border-collapse:collapse;font-size:.95rem;
  color:#e2e8f0;text-align:center;min-width:480px;
}
table.sumtab th,table.sumtab td{
  border:1px solid rgba(99,102,241,.2);padding:6px 8px;
}
table.sumtab thead th{
  background:rgba(99,102,241,.18);color:#c4b5fd;font-weight:800;
}
table.sumtab tbody th{
  background:rgba(244,63,94,.15);color:#fda4af;font-weight:800;text-align:right;
}
table.sumtab td.live{background:rgba(56,189,248,.1);color:#fde047;font-weight:900}
table.sumtab td .th-v{color:#94a3b8;font-size:.82rem;display:block}

/* ===== 모든 가능한 표본 ===== */
.all-head{
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;
  font-size:.9rem;font-weight:700;color:#cbd5e1;margin-bottom:8px;
}
.all-head .cnt{color:#fde047;font-weight:900}
.all-scroll{
  max-height:360px;overflow:auto;border-radius:9px;
  background:rgba(15,23,42,.55);border:1.5px solid rgba(99,102,241,.25);
}
table.alltab{
  width:100%;border-collapse:collapse;font-size:.95rem;
  color:#e2e8f0;text-align:center;
}
table.alltab thead th{
  position:sticky;top:0;z-index:2;
  background:rgba(99,102,241,.28);color:#e9d5ff;font-weight:800;
  padding:8px 6px;border-bottom:2px solid rgba(99,102,241,.5);
  font-size:.98rem;
}
table.alltab thead th sub{font-size:.78em;color:#c4b5fd}
table.alltab tbody td{
  padding:5px 6px;border-bottom:1px solid rgba(99,102,241,.1);
}
table.alltab tbody tr:nth-child(odd){background:rgba(30,41,59,.4)}
table.alltab tbody tr:hover{background:rgba(56,189,248,.14)}
table.alltab .idx{color:#94a3b8;font-weight:700}
table.alltab .sumcell{color:#fbbf24;font-weight:700}
table.alltab .xbarcell{color:#fde047;font-weight:900}
table.alltab .more{
  background:rgba(244,114,182,.1) !important;color:#fbcfe8;
  font-style:italic;padding:8px;
}
</style>
</head>
<body>

<div class="hdr">
  <h1>__TITLE__</h1>
  <p>표본 크기 <b>n</b>을 늘리며 <span class="xb">X</span>의 평균·분산·표준편차가 어떻게 변하는지 관찰해 봐요!</p>
</div>

<!-- ① 모집단 -->
<div class="panel">
  <h2>__POP_ICON__ 모집단</h2>
  <div class="pop-row">
    <div class="pop-viz" id="popViz">
      <div class="label">__POP_LABEL__</div>
    </div>
    <div class="pop-stats">
      <div class="ps-title">📊 모집단의 통계량</div>
      <div class="ps-row"><span>모평균 m</span><span class="v" id="popMean">--</span></div>
      <div class="ps-row"><span>모분산 σ²</span><span class="v" id="popVar">--</span></div>
      <div class="ps-row"><span>모표준편차 σ</span><span class="v" id="popSd">--</span></div>
    </div>
  </div>
</div>

<!-- ② 표본 추출 -->
<div class="panel">
  <h2>🎯 표본 뽑기 <span style="font-size:.82rem;color:#94a3b8;font-weight:500">(임의·복원추출)</span></h2>

  <div class="ctrl-row">
    <span class="ctrl-lab">표본 크기 n</span>
    <input type="range" min="1" max="__MAX_N__" value="2" class="ctrl-range" id="nRange">
    <span class="ctrl-val" id="nVal">2</span>
  </div>

  <div class="btn-row">
    <button class="btn btn-1" id="btnDraw1">🎲 표본 1개 뽑기</button>
    <button class="btn btn-2" id="btnDraw100">⚡ 100번 뽑기</button>
    <button class="btn btn-3" id="btnEnumAll">📊 모든 경우 (N<sup>n</sup>)</button>
    <button class="btn btn-r" id="btnReset">🔄 초기화</button>
  </div>

  <div class="sample-box">
    <div class="sb-title">
      <span>📦 이번에 뽑힌 공</span>
      <span class="sb-xbar"><span class="xb">X</span> = <span id="curXbar">--</span></span>
    </div>
    <div class="sb-chips" id="curSample">
      <div class="sb-empty">아직 뽑지 않았어요</div>
    </div>
  </div>
</div>

<!-- ③ 분포 + 통계 -->
<div class="panel">
  <h2>📈 표본평균 <span class="xb">X</span>의 분포</h2>

  <div class="dist-wrap">
    <div class="dist-title">
      <span>가로축: 표본평균 값 · 세로축: 상대도수</span>
      <span>누적 <span class="dist-cnt" id="histCnt">0</span>회</span>
    </div>
    <canvas id="distCanvas" width="640" height="230"></canvas>
  </div>

  <div class="stats">
    <div class="s-card s-mean">
      <div class="s-head">E(<span class="xb">X</span>) — 평균</div>
      <div class="s-val" id="ExBar">--</div>
      <div class="s-sub">이론값 <b class="th">m = <span id="ExBarT">--</span></b></div>
      <div class="s-bar-track"><div class="s-bar-fill" id="barEx" style="width:0%"></div></div>
    </div>
    <div class="s-card s-var">
      <div class="s-head">V(<span class="xb">X</span>) — 분산</div>
      <div class="s-val" id="VxBar">--</div>
      <div class="s-sub">이론값 <b class="th">σ²/n = <span id="VxBarT">--</span></b></div>
      <div class="s-bar-track"><div class="s-bar-fill" id="barV" style="width:0%"></div></div>
    </div>
    <div class="s-card s-sd">
      <div class="s-head">σ(<span class="xb">X</span>) — 표준편차</div>
      <div class="s-val" id="SdxBar">--</div>
      <div class="s-sub">이론값 <b class="th">σ/√n = <span id="SdxBarT">--</span></b></div>
      <div class="s-bar-track"><div class="s-bar-fill" id="barSd" style="width:0%"></div></div>
    </div>
  </div>

  <div class="insight" id="insight">
    <span class="ico">💡</span>
    <span>
      n을 <b>크게</b> 할수록 <span class="xb">X</span>의 평균은 <b>여전히 m</b>이고,
      분산은 <b>σ²/n</b> 으로 작아져요. 즉 <span class="xb">X</span>이 m 주위에 더 촘촘히 모입니다!
    </span>
  </div>

  <div class="summary-wrap" style="margin-top:14px">
    <h3>📋 n별 요약 — 모든 경우(N<sup>n</sup>)를 열거하면 정확한 이론값과 일치합니다</h3>
    <table class="sumtab">
      <thead>
        <tr><th>n</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr>
      </thead>
      <tbody>
        <tr><th>E(<span class="xb">X</span>)</th>
          <td id="sE1"></td><td id="sE2"></td><td id="sE3"></td><td id="sE4"></td><td id="sE5"></td>
        </tr>
        <tr><th>V(<span class="xb">X</span>)</th>
          <td id="sV1"></td><td id="sV2"></td><td id="sV3"></td><td id="sV4"></td><td id="sV5"></td>
        </tr>
        <tr><th>σ(<span class="xb">X</span>)</th>
          <td id="sS1"></td><td id="sS2"></td><td id="sS3"></td><td id="sS4"></td><td id="sS5"></td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- ④ 모든 가능한 표본 -->
<div class="panel">
  <h2>📋 n=<span id="allN" style="color:#fde047">2</span>일 때 나올 수 있는 모든 표본
    <span style="font-size:.85rem;color:#94a3b8;font-weight:600;margin-left:8px">
      총 <span class="cnt" style="color:#fde047;font-weight:900" id="allTotal">--</span>가지
    </span>
  </h2>
  <div class="all-head">
    <span>각 행 = 추출 순서(X<sub>1</sub>, X<sub>2</sub>, …)대로 뽑힌 공 · 합 · 표본평균</span>
    <span>n 슬라이더를 바꾸면 자동으로 갱신됩니다</span>
  </div>
  <div class="all-scroll">
    <table class="alltab" id="allTab">
      <thead></thead>
      <tbody></tbody>
    </table>
  </div>
</div>

<script>
const POP = __POP__;
const MAX_N = __MAX_N__;
const BALL_BG = "__BALL_BG__";
const BALL_BORDER = "__BALL_BORDER__";
const BALL_TXT = "__BALL_TXT__";
const ACC = "__ACC__";

const N_POP = POP.length;
const M = POP.reduce((a,b)=>a+b,0)/N_POP;
const SIGMA2 = POP.reduce((s,x)=>s+(x-M)*(x-M),0)/N_POP;
const SIGMA  = Math.sqrt(SIGMA2);

let n = 2;
let xbars = [];      // 누적 표본평균
let lastSample = null;

const $ = id => document.getElementById(id);

/* ============ 모집단 시각화 ============ */
function layoutPop(){
  const wrap = $('popViz');
  // 기존 ball 제거
  wrap.querySelectorAll('.ball').forEach(el => el.remove());
  const W = wrap.clientWidth, H = wrap.clientHeight;
  const BSIZE = N_POP <= 5 ? 60 : 50;
  const gap = Math.min(20, (W - BSIZE*N_POP - 40) / Math.max(1, N_POP-1));
  const totalW = BSIZE*N_POP + gap*(N_POP-1);
  const startX = (W - totalW)/2;
  const cy = H/2 - BSIZE/2 + 12;
  POP.forEach((v,i)=>{
    const el = document.createElement('div');
    el.className = 'ball';
    el.dataset.idx = i;
    el.style.width = BSIZE+'px';
    el.style.height = BSIZE+'px';
    el.style.fontSize = (BSIZE*0.45)+'px';
    el.style.background = BALL_BG;
    el.style.borderColor = BALL_BORDER;
    el.style.color = BALL_TXT;
    el.style.left = (startX + i*(BSIZE+gap))+'px';
    el.style.top = cy+'px';
    el.textContent = v;
    wrap.appendChild(el);
  });
}

function highlightPicks(picks){
  const ballEls = $('popViz').querySelectorAll('.ball');
  ballEls.forEach(el => { el.classList.remove('pick'); el.classList.remove('dim'); });
  if(!picks || picks.length===0) return;
  const set = new Set(picks);
  ballEls.forEach(el=>{
    const i = parseInt(el.dataset.idx);
    if(set.has(i)) el.classList.add('pick');
    else el.classList.add('dim');
  });
}

/* ============ 표본 추출 ============ */
function sampleOnce(nn){
  const idx = [], vals = [];
  for(let i=0;i<nn;i++){
    const k = Math.floor(Math.random()*N_POP);
    idx.push(k); vals.push(POP[k]);
  }
  const xbar = vals.reduce((a,b)=>a+b,0)/nn;
  return {idx, vals, xbar};
}

function enumerateAll(nn){
  // N^n 경우 전체 열거
  const total = Math.pow(N_POP, nn);
  const arr = new Array(total);
  for(let i=0;i<total;i++){
    let k = i, s = 0;
    for(let j=0;j<nn;j++){
      s += POP[k % N_POP];
      k = Math.floor(k/N_POP);
    }
    arr[i] = s/nn;
  }
  return arr;
}

/* ============ 통계 계산 ============ */
function stats(arr){
  if(arr.length===0) return {mean:NaN,var:NaN,sd:NaN};
  const m = arr.reduce((a,b)=>a+b,0)/arr.length;
  const v = arr.reduce((s,x)=>s+(x-m)*(x-m),0)/arr.length;
  return {mean:m, var:v, sd:Math.sqrt(v)};
}

/* ============ 히스토그램 ============ */
function drawHist(){
  const cv = $('distCanvas');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.scale(dpr,dpr);
  ctx.clearRect(0,0,W,H);

  const lo = Math.min(...POP), hi = Math.max(...POP);
  const padL = 36, padR = 16, padT = 16, padB = 30;

  // 축
  ctx.strokeStyle = 'rgba(148,163,184,.35)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(padL, H-padB); ctx.lineTo(W-padR, H-padB);
  ctx.moveTo(padL, padT); ctx.lineTo(padL, H-padB);
  ctx.stroke();

  // 가능한 X̄ 격자(2*POP_value 간격이 깔끔). 그냥 모집단 최솟·최댓값 사이를 균등 분할
  const totalCnt = xbars.length;
  if(totalCnt === 0){
    ctx.fillStyle = '#64748b';
    ctx.font = '14px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('표본을 뽑으면 분포가 그려져요', W/2, H/2);
    return;
  }

  // 히스토그램: 가로축 0..최대 사이 구간을 충분히 분할
  const lo2 = lo, hi2 = hi;
  // 표본평균이 가질 수 있는 값: n이 1일때는 모집단 값 그대로, n이 커지면 평균값 분포
  // bin: (hi - lo) / (n * 10) 정도가 적당 → 너무 잘게 분할되면 안되니 최소 8개~최대 40개
  const span = hi2 - lo2;
  let nBins = Math.max(8, Math.min(40, n * 6 + 4));
  const binW = span / nBins;
  const bins = new Array(nBins+1).fill(0);
  xbars.forEach(x=>{
    let k = Math.floor((x - lo2) / binW + 1e-9);
    if(k<0) k=0; if(k>nBins) k=nBins;
    bins[k]++;
  });
  // 마지막 빈은 hi값 한 점만 들어가니까 그 옆 빈에 합치자
  bins[nBins-1] += bins[nBins]; bins[nBins]=0;
  const maxC = Math.max(...bins, 1);

  // 바
  const plotW = W - padL - padR;
  const plotH = H - padT - padB;
  for(let i=0;i<nBins;i++){
    const c = bins[i]; if(c===0) continue;
    const x0 = padL + (i)/nBins * plotW;
    const x1 = padL + (i+1)/nBins * plotW;
    const bh = c / maxC * plotH;
    const grad = ctx.createLinearGradient(0, H-padB-bh, 0, H-padB);
    grad.addColorStop(0, ACC);
    grad.addColorStop(1, 'rgba(99,102,241,.45)');
    ctx.fillStyle = grad;
    ctx.fillRect(x0+1, H-padB-bh, (x1-x0)-2, bh);
  }

  // 모평균 m 선
  const xm = padL + (M - lo2)/span * plotW;
  ctx.strokeStyle = '#fb7185';
  ctx.setLineDash([5,4]);
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(xm, padT); ctx.lineTo(xm, H-padB);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#fb7185';
  ctx.font = 'bold 13px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('m='+(Number.isInteger(M)?M:M.toFixed(2)), xm, padT-2);

  // 표본평균의 평균(실험값) 선
  const s = stats(xbars);
  const xExp = padL + (s.mean - lo2)/span * plotW;
  ctx.strokeStyle = '#fde047';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(xExp, padT+12); ctx.lineTo(xExp, H-padB);
  ctx.stroke();
  ctx.fillStyle = '#fde047';
  ctx.font = 'bold 12px sans-serif';
  ctx.fillText('표본평균≈'+s.mean.toFixed(2), xExp, H-padB+18);

  // 가로축 눈금 (lo, mid, hi)
  ctx.fillStyle = '#94a3b8';
  ctx.font = '12px sans-serif';
  ctx.textAlign = 'center';
  [lo2, (lo2+hi2)/2, hi2].forEach(v=>{
    const x = padL + (v-lo2)/span * plotW;
    ctx.fillText(Number.isInteger(v)?v:v.toFixed(1), x, H-padB+18);
  });
}

/* ============ UI 업데이트 ============ */
function fmt(v, d=3){ return isNaN(v)? '--' : v.toFixed(d); }

function updateStatsUI(){
  const s = stats(xbars);
  const theE = M;
  const theV = SIGMA2/n;
  const theS = SIGMA/Math.sqrt(n);

  $('ExBar').textContent  = fmt(s.mean);
  $('VxBar').textContent  = fmt(s.var);
  $('SdxBar').textContent = fmt(s.sd);

  $('ExBarT').textContent  = theE.toFixed(3);
  $('VxBarT').textContent  = theV.toFixed(3);
  $('SdxBarT').textContent = theS.toFixed(3);

  // bar fill: 1에 가까울수록 100% (실험/이론)
  function ratioBar(exp, the){
    if(xbars.length===0 || the===0) return 0;
    const r = Math.min(exp,the)/Math.max(exp,the);
    return Math.max(0, Math.min(1, r));
  }
  $('barEx').style.width = (ratioBar(s.mean, theE)*100).toFixed(1)+'%';
  $('barV').style.width  = (ratioBar(s.var,  theV)*100).toFixed(1)+'%';
  $('barSd').style.width = (ratioBar(s.sd,   theS)*100).toFixed(1)+'%';

  $('histCnt').textContent = xbars.length;
}

function renderSample(s){
  lastSample = s;
  const wrap = $('curSample');
  wrap.innerHTML = '';
  s.vals.forEach((v,i)=>{
    const c = document.createElement('div');
    c.className = 'sb-chip';
    c.textContent = v;
    c.style.animationDelay = (i*0.04)+'s';
    c.style.background = BALL_BG;
    c.style.borderColor = BALL_BORDER;
    c.style.color = BALL_TXT;
    wrap.appendChild(c);
  });
  $('curXbar').textContent = (Math.round(s.xbar*100)/100);
}

/* ============ 액션 ============ */
function doDraw1(){
  const s = sampleOnce(n);
  highlightPicks(s.idx);
  renderSample(s);
  xbars.push(s.xbar);
  drawHist();
  updateStatsUI();
}

function doDraw100(){
  const total = 100;
  let i = 0;
  // 마지막 표본 1개를 화면에 보여주기 위해 약간의 단계로 끊어 그리기
  const step = ()=>{
    const burst = 20;
    for(let k=0;k<burst && i<total;k++,i++){
      const s = sampleOnce(n);
      xbars.push(s.xbar);
      if(i===total-1){
        highlightPicks(s.idx);
        renderSample(s);
      }
    }
    drawHist(); updateStatsUI();
    if(i<total) requestAnimationFrame(step);
  };
  step();
}

function doEnumerate(){
  const arr = enumerateAll(n);
  xbars = xbars.concat(arr);
  drawHist();
  updateStatsUI();
  // 마지막 케이스를 표본으로 보여주기
  const last = arr[arr.length-1];
  $('curXbar').textContent = (Math.round(last*100)/100);
  // 화면 표시용: 마지막 경우 인덱스 복원
  const lastIdx = (Math.pow(N_POP,n)-1);
  const vals = [];
  let k = lastIdx;
  for(let j=0;j<n;j++){ vals.push(POP[k%N_POP]); k = Math.floor(k/N_POP); }
  renderSample({vals, xbar:last});
  highlightPicks([]);  // 모두 사용했으므로 강조 해제
}

function doReset(){
  xbars = [];
  lastSample = null;
  highlightPicks([]);
  $('curSample').innerHTML = '<div class="sb-empty">아직 뽑지 않았어요</div>';
  $('curXbar').textContent = '--';
  drawHist();
  updateStatsUI();
  fillSummary();  // 요약표는 이론값 유지
}

/* ============ n별 요약표 ============ */
function fmtFrac(v){
  if(v===0) return '0';
  // 정수면 정수로
  if(Math.abs(v-Math.round(v))<1e-9) return Math.round(v)+'';
  return v.toFixed(3);
}
function fillSummary(){
  for(let k=1;k<=5;k++){
    const tE = M;
    const tV = SIGMA2/k;
    const tS = SIGMA/Math.sqrt(k);
    $('sE'+k).innerHTML = `<span>${fmtFrac(tE)}</span>`;
    $('sV'+k).innerHTML = `<span>${fmtFrac(tV)}</span>`;
    $('sS'+k).innerHTML = `<span>${fmtFrac(tS)}</span>`;
    [$('sE'+k),$('sV'+k),$('sS'+k)].forEach(el=>el.classList.remove('live'));
  }
  // 현재 n 강조
  if(n>=1 && n<=5){
    [$('sE'+n),$('sV'+n),$('sS'+n)].forEach(el=>el.classList.add('live'));
  }
}

/* ============ 모든 가능한 표본 표 ============ */
const ALL_MAX_ROWS = 5000;  // 너무 많을 때 일부만 렌더링 (성능 보호)

function renderAllSamples(){
  const total = Math.pow(N_POP, n);
  $('allN').textContent = n;
  $('allTotal').textContent = total;

  // 헤더
  const headParts = ['<tr><th>#</th>'];
  for(let i=1;i<=n;i++) headParts.push('<th>X<sub>'+i+'</sub></th>');
  headParts.push('<th>합</th><th><span class="xb">X</span></th></tr>');
  $('allTab').querySelector('thead').innerHTML = headParts.join('');

  // 본문
  const showCount = Math.min(total, ALL_MAX_ROWS);
  const rows = new Array(showCount);
  for(let i=0;i<showCount;i++){
    let k = i, sum = 0;
    const cells = ['<tr><td class="idx">'+(i+1)+'</td>'];
    for(let j=0;j<n;j++){
      const v = POP[k % N_POP];
      cells.push('<td>'+v+'</td>');
      sum += v;
      k = Math.floor(k/N_POP);
    }
    const xb = sum/n;
    const xbStr = (Math.abs(xb-Math.round(xb))<1e-9) ? Math.round(xb)+'' : xb.toFixed(3);
    cells.push('<td class="sumcell">'+sum+'</td>');
    cells.push('<td class="xbarcell">'+xbStr+'</td></tr>');
    rows[i] = cells.join('');
  }
  if(total > ALL_MAX_ROWS){
    rows.push('<tr><td class="more" colspan="'+(n+3)+'">… 이하 '+(total-ALL_MAX_ROWS).toLocaleString()+'가지는 생략 (총 '+total.toLocaleString()+'가지)</td></tr>');
  }
  $('allTab').querySelector('tbody').innerHTML = rows.join('');
}

/* ============ 초기화 ============ */
function init(){
  $('popMean').textContent = fmtFrac(M);
  $('popVar').textContent  = fmtFrac(SIGMA2);
  $('popSd').textContent   = (Math.round(SIGMA*1000)/1000)+'';

  layoutPop();
  drawHist();
  updateStatsUI();
  fillSummary();
  renderAllSamples();

  $('nRange').addEventListener('input', e=>{
    n = parseInt(e.target.value);
    $('nVal').textContent = n;
    fillSummary();
    renderAllSamples();
  });
  $('btnDraw1').addEventListener('click', doDraw1);
  $('btnDraw100').addEventListener('click', doDraw100);
  $('btnEnumAll').addEventListener('click', doEnumerate);
  $('btnReset').addEventListener('click', doReset);

  window.addEventListener('resize', ()=>{ layoutPop(); drawHist(); });
}
init();
</script>
</body>
</html>
"""


def _make_html(*, title, pop, max_n, pop_icon, pop_label,
               ball_bg, ball_border, ball_txt,
               bg_mid, hdr_a, hdr_b, hdr_border, hdr_txt, acc, acc_dim):
    """템플릿에 모집단별 설정을 주입하여 완성된 HTML 반환."""
    return (_HTML_TEMPLATE
        .replace("__TITLE__", title)
        .replace("__POP__", json.dumps(pop))
        .replace("__MAX_N__", str(max_n))
        .replace("__POP_ICON__", pop_icon)
        .replace("__POP_LABEL__", pop_label)
        .replace("__BALL_BG__", ball_bg)
        .replace("__BALL_BORDER__", ball_border)
        .replace("__BALL_TXT__", ball_txt)
        .replace("__BG_MID__", bg_mid)
        .replace("__HDR_A__", hdr_a)
        .replace("__HDR_B__", hdr_b)
        .replace("__HDR_BORDER__", hdr_border)
        .replace("__HDR_TXT__", hdr_txt)
        .replace("__ACC__", acc)
        .replace("__ACC_DIM__", acc_dim)
    )


# ─────────────────────────────────────────────────────────────────────────────
# 3개 탭의 HTML 인스턴스
# ─────────────────────────────────────────────────────────────────────────────
_HTML_BALLS = _make_html(
    title="🎒 주머니 속 공 {2, 4, 6, 8}",
    pop=[2, 4, 6, 8], max_n=5,
    pop_icon="🎒", pop_label="공 4개가 든 주머니 (모집단)",
    ball_bg="radial-gradient(circle at 30% 30%,#fde047,#f59e0b)",
    ball_border="#fbbf24", ball_txt="#1f2937",
    bg_mid="#1e1b4b",
    hdr_a="rgba(251,191,36,.18)", hdr_b="rgba(168,85,247,.15)",
    hdr_border="rgba(251,191,36,.45)", hdr_txt="#fbbf24",
    acc="#a5b4fc", acc_dim="rgba(251,191,36,.45)",
)

_HTML_DICE = _make_html(
    title="🎲 주사위 {1, 2, 3, 4, 5, 6}",
    pop=[1, 2, 3, 4, 5, 6], max_n=5,
    pop_icon="🎲", pop_label="주사위 한 개의 눈 (모집단)",
    ball_bg="radial-gradient(circle at 30% 30%,#fca5a5,#dc2626)",
    ball_border="#f87171", ball_txt="#ffffff",
    bg_mid="#3f0a16",
    hdr_a="rgba(244,63,94,.22)", hdr_b="rgba(251,113,133,.15)",
    hdr_border="rgba(244,63,94,.5)", hdr_txt="#fda4af",
    acc="#fda4af", acc_dim="rgba(244,63,94,.5)",
)

_HTML_CARDS = _make_html(
    title="🃏 홀수 카드 {1, 3, 5, 7, 9}",
    pop=[1, 3, 5, 7, 9], max_n=5,
    pop_icon="🃏", pop_label="카드 5장 (모집단)",
    ball_bg="radial-gradient(circle at 30% 30%,#a7f3d0,#059669)",
    ball_border="#34d399", ball_txt="#064e3b",
    bg_mid="#06281d",
    hdr_a="rgba(34,197,94,.2)", hdr_b="rgba(16,185,129,.14)",
    hdr_border="rgba(34,197,94,.5)", hdr_txt="#86efac",
    acc="#86efac", acc_dim="rgba(34,197,94,.45)",
)


# ─────────────────────────────────────────────────────────────────────────────
# render()
# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.subheader("🎲 표본평균의 평균·분산·표준편차 시뮬레이터")
    st.caption(
        "표본의 크기 n을 늘리며 **E(X̄)·V(X̄)·σ(X̄)** 이 어떻게 변하는지 직접 확인해 봐요. "
        "“모든 경우(N^n)”를 한꺼번에 누르면 **이론값과 정확히 일치**합니다!"
    )

    tab1, tab2, tab3 = st.tabs([
        "🎒 주머니 속 공 {2,4,6,8}",
        "🎲 주사위 {1..6}",
        "🃏 홀수 카드 {1,3,5,7,9}",
    ])

    with tab1:
        components.html(_HTML_BALLS, height=2100, scrolling=True)
    with tab2:
        components.html(_HTML_DICE, height=2100, scrolling=True)
    with tab3:
        components.html(_HTML_CARDS, height=2100, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
