# activities/probability_new/mini/ci_proportion_lab.py
"""
모비율 신뢰구간 챌린지 — 미스터리 항아리 속 p 잡기

- 실생활 시나리오 4종 (피자 선호도 / 양궁 명중률 / SNS 광고 클릭률 / 씨앗 발아율)
- 각 시나리오에는 학생이 모르는 "진짜 모비율 p"가 숨겨져 있음
- 표본 크기 n과 신뢰도(95%·99%)를 바꾸며 신뢰구간 만들기
  → 신뢰구간이 진짜 p를 "잡았는지" 시각적으로 확인
- 신뢰구간 길이 공식 2k√(p̂q̂/n) 를 p̂ 변화에 따라 곡선으로 보여주고
  p̂ = 1/2 일 때 최대 길이 k/√n 임을 산술-기하 평균과 함께 시각화
- 챌린지 모드: 100번 추출 시 "p 명중" 횟수를 카운트
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🏺 미니: 모비율 신뢰구간 챌린지 — 미스터리 항아리 속 p 잡기",
    "description": "실생활 시나리오 4종에서 표본을 뽑아 모비율 p의 신뢰구간을 만들고, "
                   "진짜 p를 신뢰구간이 \"잡는\" 과정을 시각·게임으로 체험합니다. "
                   "신뢰구간 길이 공식 2k√(p̂q̂/n) 과 최대 길이 k/√n 도 시각적으로 확인합니다.",
    "order": 25,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "모비율신뢰구간챌린지"

_QUESTIONS = [
    {"type": "markdown",
     "text": "**📝 활동 성찰 — 모비율의 추정**"},
    {
        "key": "신뢰구간_공식_관찰",
        "label": "표본비율 p̂을 중심으로 95% 신뢰구간 "
                 "`p̂ − 1.96√(p̂q̂/n) ≤ p ≤ p̂ + 1.96√(p̂q̂/n)` 을 만들었을 때, "
                 "이 구간이 진짜 모비율 p를 **잡지 못한 경우**도 있었나요? "
                 "어떤 상황에서 그렇게 되었는지 적어 보세요.",
        "type": "text_area", "height": 110,
        "placeholder": "표본 크기 n이 ___ 이거나, 우연히 뽑힌 표본이 ___ 일 때 신뢰구간이 p를 놓쳤다.",
    },
    {
        "key": "신뢰도_95_99_비교",
        "label": "같은 표본에서 **신뢰도 95%(k=1.96)** 과 **99%(k=2.58)** 두 가지 신뢰구간을 함께 그려 보았어요. "
                 "신뢰도를 99%로 높이면 구간의 **길이**와 **p를 잡는 비율**은 어떻게 달라졌나요?",
        "type": "text_area", "height": 110,
        "placeholder": "신뢰도를 95% → 99% 로 올리면 구간의 길이는 ___ 하고, "
                       "p를 잡는 비율은 ___ 했다.",
    },
    {
        "key": "n_과_길이",
        "label": "표본 크기 **n**을 키우면(예: n=30 → 300) 신뢰구간의 길이는 어떻게 변했나요? "
                 "공식 `2k√(p̂q̂/n)` 에서 왜 그런 변화가 일어나는지 식으로 설명해 보세요.",
        "type": "text_area", "height": 110,
        "placeholder": "n이 커지면 √n 이 ___ 하므로, "
                       "분모가 커져서 신뢰구간의 길이는 ___ 한다.",
    },
    {
        "key": "최대길이_AMGM",
        "label": "활동 마지막의 \"길이 곡선\"에서 신뢰구간의 길이는 **p̂ = 1/2** 일 때 최대가 되었어요. "
                 "산술–기하평균(`a+b ≥ 2√ab`)을 p̂ + q̂ = 1 에 적용하여 "
                 "최대 길이가 왜 `k/√n` 인지 본인의 말로 설명해 보세요.",
        "type": "text_area", "height": 130,
        "placeholder": "p̂ + q̂ = 1 에 산술-기하평균을 적용하면 1 ≥ 2√(p̂q̂) 이므로 "
                       "√(p̂q̂) ≤ ___. 따라서 신뢰구간의 길이는 2k × ___ = ___ 이하이다. "
                       "등호는 p̂ = q̂ = ___ 일 때 성립한다.",
    },
    {
        "key": "실생활_활용",
        "label": "이번에 다룬 4가지 사례(피자 선호도, 양궁 명중률, SNS 광고 클릭률, 씨앗 발아율) 중 하나를 골라, "
                 "실제로 이런 조사를 한다면 표본 크기 n을 어떻게 잡고 싶은지 이유와 함께 적어 보세요.",
        "type": "text_area", "height": 110,
        "placeholder": "나는 ___ 사례를 골랐다. 실제로 조사한다면 표본을 ___명 정도로 잡고 싶다. "
                       "그 이유는 신뢰구간 길이가 ___ 이상으로 커지면 ___ 하기 어렵기 때문이다.",
    },
    {
        "key": "신뢰구간_나만의말",
        "label": "이 활동을 통해 알게 된 **모비율 신뢰구간**의 의미를 본인의 말로 한 문장으로 적어 보세요.",
        "type": "text_area", "height": 80,
        "placeholder": "모비율의 신뢰구간이란 ___ 이다.",
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 이 활동을 통해 새롭게 알게 된 점",
        "type": "text_area", "height": 90,
    },
    {
        "key": "느낀점",
        "label": "💬 활동을 마친 후 느낀 점",
        "type": "text_area", "height": 90,
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
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#0f172a 100%);
  color:#e2e8f0;padding:14px 12px;min-height:100vh;
}

/* ============ 헤더 ============ */
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(244,114,182,.20),rgba(34,211,238,.20));
  border:2px solid rgba(244,114,182,.50);border-radius:18px;
  padding:14px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.65rem;font-weight:900;color:#fbcfe8;margin-bottom:5px;letter-spacing:.3px}
.hdr p{font-size:1.1rem;color:#e2e8f0;line-height:1.6}
.hdr b{color:#fde047}

/* ============ 공식 카드 ============ */
.formula{
  background:rgba(15,23,42,.7);
  border:2px dashed rgba(251,191,36,.55);border-radius:14px;
  padding:14px 18px;margin-bottom:13px;
  display:flex;flex-wrap:wrap;justify-content:center;align-items:center;
  gap:18px;font-size:1.35rem;color:#fde68a;font-weight:800;
}
.formula .lab{color:#fbbf24;font-size:1.15rem}
.formula .eq{
  background:rgba(251,191,36,.10);border:1.5px solid rgba(251,191,36,.45);
  padding:7px 14px;border-radius:10px;letter-spacing:.5px;
}
.formula sup{font-size:.78em}

/* ============ 패널 ============ */
.panel{
  background:rgba(15,23,42,.72);border:1.5px solid rgba(168,85,247,.32);
  border-radius:14px;padding:14px;margin-bottom:13px;
}
.panel h2{
  font-size:1.22rem;font-weight:900;color:#c4b5fd;margin-bottom:11px;
  display:flex;align-items:center;gap:9px;letter-spacing:.3px;
}
.panel h2 .badge{
  font-size:.88rem;color:#cbd5e1;background:rgba(168,85,247,.18);
  padding:3px 10px;border-radius:999px;font-weight:700;
}

/* ============ 시나리오 ============ */
.scn-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:11px}
.scn{
  padding:11px 16px;border-radius:14px;font-size:1.02rem;font-weight:800;
  border:2px solid transparent;cursor:pointer;color:#fff;
  background:linear-gradient(135deg,#475569,#334155);
  transition:all .14s ease;flex:1;min-width:170px;text-align:center;
}
.scn:hover{transform:translateY(-1px)}
.scn.active{
  background:linear-gradient(135deg,#ec4899,#be185d);
  border-color:#fbcfe8;box-shadow:0 4px 14px rgba(236,72,153,.5);color:#fff;
}
.scn small{display:block;margin-top:2px;font-weight:600;opacity:.85;font-size:.85rem}

/* ============ 미스터리 항아리 ============ */
.jar-wrap{
  display:grid;grid-template-columns:1fr 1.4fr;gap:13px;align-items:stretch;
}
@media(max-width:820px){.jar-wrap{grid-template-columns:1fr}}

.jar-card{
  background:linear-gradient(135deg,rgba(236,72,153,.10),rgba(168,85,247,.10));
  border:2px solid rgba(236,72,153,.45);
  border-radius:14px;padding:13px;text-align:center;
}
.jar-title{font-size:1.05rem;color:#fbcfe8;font-weight:900;margin-bottom:8px}
#jarCanvas{display:block;width:100%;height:240px;background:rgba(15,23,42,.4);border-radius:10px}
.jar-hint{
  margin-top:8px;font-size:.95rem;color:#fde68a;font-weight:700;
  background:rgba(251,191,36,.10);border:1.5px solid rgba(251,191,36,.4);
  border-radius:10px;padding:6px 10px;
}
.jar-truep{
  margin-top:8px;font-size:1.05rem;font-weight:900;
  background:rgba(251,191,36,.18);border:2px solid rgba(251,191,36,.55);
  border-radius:10px;padding:8px 10px;color:#fef3c7;letter-spacing:.3px;
  display:flex;justify-content:space-around;align-items:center;gap:8px;
  transition:all .3s ease;
}
.jar-truep .lab{font-size:.95rem;color:#fde68a}
.jar-truep .val{font-size:1.4rem;color:#fde047}
.jar-truep.hidden .val{filter:blur(7px);user-select:none}

.sample-card{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(56,189,248,.35);
  border-radius:12px;padding:13px;
}
#sampleCanvas{display:block;width:100%;height:240px;background:rgba(15,23,42,.4);border-radius:10px}
.sample-stat{
  display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:9px;
}
.ssc{
  background:rgba(56,189,248,.08);border:1.5px solid rgba(56,189,248,.4);
  border-radius:10px;padding:8px 6px;text-align:center;
}
.ssc .lab{font-size:.85rem;color:#7dd3fc;font-weight:800;margin-bottom:2px}
.ssc .val{font-size:1.4rem;color:#bae6fd;font-weight:900;font-variant-numeric:tabular-nums}

/* ============ 컨트롤 ============ */
.ctl-row{
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  background:rgba(56,189,248,.07);border:1.5px solid rgba(56,189,248,.32);
  border-radius:11px;padding:10px 13px;margin-bottom:9px;
}
.ctl-lab{font-size:1.05rem;font-weight:800;color:#7dd3fc;min-width:130px}
.ctl-range{flex:1;min-width:160px;accent-color:#38bdf8;height:6px}
.ctl-val{
  font-size:1.5rem;font-weight:900;color:#fde047;min-width:86px;
  background:rgba(15,23,42,.7);padding:4px 13px;border-radius:9px;text-align:center;
  font-variant-numeric:tabular-nums;
}
.btn-group{display:flex;gap:7px}
.k-btn{
  padding:9px 16px;border-radius:11px;font-size:1.02rem;font-weight:900;
  border:2px solid transparent;background:rgba(71,85,105,.6);color:#cbd5e1;
  cursor:pointer;transition:all .14s ease;letter-spacing:.3px;
}
.k-btn.active{
  background:linear-gradient(135deg,#a855f7,#7e22ce);color:#fff;
  border-color:#c4b5fd;box-shadow:0 3px 10px rgba(168,85,247,.5);
}

.btn-row{display:flex;gap:9px;flex-wrap:wrap;margin-top:6px}
.btn{
  padding:13px 18px;border:none;border-radius:11px;
  font-size:1.08rem;font-weight:900;color:#fff;cursor:pointer;
  transition:all .15s ease;letter-spacing:.3px;
}
.btn:active{transform:scale(.96)}
.btn-pri{
  background:linear-gradient(135deg,#ec4899,#be185d);
  box-shadow:0 3px 12px rgba(236,72,153,.45);flex:1;min-width:180px;
}
.btn-pri:hover{background:linear-gradient(135deg,#db2777,#9d174d);transform:translateY(-1px)}
.btn-sec{
  background:linear-gradient(135deg,#22d3ee,#0e7490);
  box-shadow:0 3px 10px rgba(34,211,238,.4);
}
.btn-sec:hover{background:linear-gradient(135deg,#06b6d4,#155e75);transform:translateY(-1px)}
.btn-warn{
  background:linear-gradient(135deg,#fbbf24,#b45309);
  box-shadow:0 3px 10px rgba(251,191,36,.4);
}
.btn-warn:hover{background:linear-gradient(135deg,#f59e0b,#92400e);transform:translateY(-1px)}
.btn-ghost{background:rgba(71,85,105,.65);border:1.5px solid rgba(148,163,184,.3)}

/* ============ 수직선 (신뢰구간) ============ */
.numline-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(168,85,247,.32);
  border-radius:12px;padding:12px;
}
#numlineCanvas{display:block;width:100%;height:300px;background:rgba(15,23,42,.4);border-radius:8px}

.verdict{
  margin-top:12px;
  display:flex;flex-wrap:wrap;align-items:center;gap:14px;
  border-radius:14px;padding:15px 19px;
  font-size:1.05rem;font-weight:800;
  transition:all .3s ease;
}
.verdict.idle{
  background:rgba(71,85,105,.3);border:2px dashed rgba(148,163,184,.4);
  color:#cbd5e1;
}
.verdict.ok{
  background:linear-gradient(135deg,rgba(34,197,94,.20),rgba(132,204,22,.15));
  border:2px solid rgba(34,197,94,.6);color:#dcfce7;
}
.verdict.bad{
  background:linear-gradient(135deg,rgba(244,63,94,.20),rgba(251,113,133,.15));
  border:2px solid rgba(244,63,94,.6);color:#fecaca;
}
.verdict .big{font-size:2.4rem;line-height:1;flex-shrink:0}
.verdict .ci-info{font-size:.95rem;color:#cbd5e1;margin-top:3px;font-weight:600}

/* ============ 챌린지 모드 ============ */
.challenge-wrap{
  background:linear-gradient(135deg,rgba(34,197,94,.10),rgba(56,189,248,.10));
  border:2px solid rgba(34,197,94,.45);
  border-radius:14px;padding:14px;margin-top:13px;
}
.ch-head{
  display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;
  margin-bottom:10px;gap:8px;
}
.ch-head .title{font-size:1.12rem;color:#86efac;font-weight:900;letter-spacing:.3px}
.ch-stats{
  display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-bottom:9px;
}
.chs{
  background:rgba(34,197,94,.08);border:1.5px solid rgba(34,197,94,.4);
  border-radius:10px;padding:9px;text-align:center;
}
.chs.miss{
  background:rgba(244,63,94,.08);border-color:rgba(244,63,94,.45);
}
.chs.rate{
  background:rgba(251,191,36,.08);border-color:rgba(251,191,36,.45);
}
.chs .lab{font-size:.92rem;font-weight:800;margin-bottom:2px}
.chs.ok .lab{color:#86efac}
.chs.miss .lab{color:#fda4af}
.chs.rate .lab{color:#fde68a}
.chs .val{
  font-size:1.7rem;font-weight:900;font-variant-numeric:tabular-nums;letter-spacing:.4px;
}
.chs.ok .val{color:#dcfce7}
.chs.miss .val{color:#fecaca}
.chs.rate .val{color:#fde047}
#chBar{
  height:18px;border-radius:9px;overflow:hidden;
  background:rgba(244,63,94,.25);border:1px solid rgba(148,163,184,.3);
  display:flex;
}
#chBarOK{height:100%;background:linear-gradient(90deg,#22c55e,#15803d);transition:width .3s ease}

/* ============ 길이 곡선 ============ */
#lengthCanvas{display:block;width:100%;height:300px;background:rgba(15,23,42,.4);border-radius:8px}
.len-summary{
  display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:9px;
}
@media(max-width:760px){.len-summary{grid-template-columns:1fr 1fr}}
.lsc{
  background:rgba(251,191,36,.07);border:1.5px solid rgba(251,191,36,.4);
  border-radius:10px;padding:9px;text-align:center;
}
.lsc .lab{font-size:.92rem;color:#fde68a;font-weight:800;margin-bottom:2px}
.lsc .val{font-size:1.4rem;color:#fef3c7;font-weight:900;font-variant-numeric:tabular-nums}

/* ============ 인사이트 ============ */
.insight{
  background:rgba(251,191,36,.10);border:2px solid rgba(251,191,36,.45);
  border-radius:13px;padding:13px 16px;margin-top:12px;
  font-size:1.04rem;color:#fef3c7;line-height:1.7;
  display:flex;align-items:flex-start;gap:10px;
}
.insight .ico{font-size:1.6rem;flex-shrink:0;line-height:1.2}
.insight b{color:#fde047}
.insight code{
  background:rgba(15,23,42,.6);padding:2px 6px;border-radius:5px;
  color:#fde047;font-size:.97em;letter-spacing:.3px;
}

/* ============ 펄스 애니메이션 ============ */
@keyframes pulse-ok{
  0%{box-shadow:0 0 0 0 rgba(34,197,94,.7)}
  100%{box-shadow:0 0 0 18px rgba(34,197,94,0)}
}
@keyframes pulse-bad{
  0%{box-shadow:0 0 0 0 rgba(244,63,94,.7)}
  100%{box-shadow:0 0 0 18px rgba(244,63,94,0)}
}
.verdict.ok.pulse{animation:pulse-ok .8s ease}
.verdict.bad.pulse{animation:pulse-bad .8s ease}
</style>
</head>
<body>

<div class="hdr">
  <h1>🏺 모비율 신뢰구간 챌린지 — 미스터리 항아리 속 <b>p</b> 잡기</h1>
  <p>항아리 속에 숨겨진 진짜 모비율 <b>p</b>를 표본만 가지고 추정해 봐요!<br>
     표본비율 <b>p̂</b> 으로 만든 신뢰구간이 정말 <b>p</b>를 잡는지 직접 확인합시다.</p>
</div>

<div class="formula">
  <span class="lab">📐 모비율의 신뢰구간</span>
  <span class="eq">p̂ − k √( p̂q̂ / n ) ≤ p ≤ p̂ + k √( p̂q̂ / n )</span>
  <span class="lab">신뢰도 95% → k = 1.96 &nbsp; 99% → k = 2.58</span>
</div>

<!-- ① 시나리오 -->
<div class="panel">
  <h2>🎒 시나리오 선택 <span class="badge">실생활 미스터리 4종</span></h2>
  <div class="scn-row" id="scnRow">
    <button class="scn active" data-key="pizza">🍕 신메뉴 피자<small>매점 학생들의 선호 비율</small></button>
    <button class="scn" data-key="archery">🎯 양궁 명중<small>한 선수의 과녁 명중 비율</small></button>
    <button class="scn" data-key="ad">📱 광고 클릭<small>SNS 광고 클릭 비율</small></button>
    <button class="scn" data-key="seed">🌱 씨앗 발아<small>새 품종의 발아 비율</small></button>
  </div>
</div>

<!-- ② 항아리 + 표본 -->
<div class="panel">
  <h2>🏺 미스터리 항아리와 표본 <span class="badge">표본은 보이지만 진짜 p는 숨겨져 있어요</span></h2>
  <div class="jar-wrap">
    <div class="jar-card">
      <div class="jar-title">🏺 항아리 (모집단)</div>
      <canvas id="jarCanvas" width="520" height="240"></canvas>
      <div class="jar-hint">⚠️ 항아리 속에는 우리가 모르는 진짜 모비율 <b>p</b> 가 숨겨져 있어요</div>
      <div class="jar-truep hidden" id="truePBox">
        <span><span class="lab">진짜 모비율</span> <span class="val" id="truePVal">--</span></span>
        <button class="btn k-btn" id="btnReveal">👁 정답 보기</button>
      </div>
    </div>
    <div class="sample-card">
      <div class="jar-title" style="color:#7dd3fc">🎲 추출된 표본 (n개)</div>
      <canvas id="sampleCanvas" width="620" height="240"></canvas>
      <div class="sample-stat">
        <div class="ssc"><div class="lab">표본크기 n</div><div class="val" id="kN">--</div></div>
        <div class="ssc"><div class="lab">성공 X</div><div class="val" id="kX">--</div></div>
        <div class="ssc"><div class="lab">표본비율 p̂</div><div class="val" id="kPhat" style="color:#fde047">--</div></div>
      </div>
    </div>
  </div>
</div>

<!-- ③ 추출 설정 -->
<div class="panel">
  <h2>🎲 추출 설정 <span class="badge">n과 신뢰도를 바꿔 보세요</span></h2>

  <div class="ctl-row">
    <span class="ctl-lab">표본 크기 n</span>
    <input type="range" min="10" max="500" value="100" step="5" class="ctl-range" id="nRange">
    <span class="ctl-val" id="nVal">100</span>
  </div>
  <div class="ctl-row">
    <span class="ctl-lab">신뢰도</span>
    <div class="btn-group" id="kBtns" style="flex:1">
      <button class="k-btn active" data-k="1.96">95% &nbsp;(k = 1.96)</button>
      <button class="k-btn" data-k="2.58">99% &nbsp;(k = 2.58)</button>
    </div>
  </div>

  <div class="btn-row">
    <button class="btn btn-pri" id="btnDraw">🎲 표본 추출 + 신뢰구간 만들기</button>
    <button class="btn btn-warn" id="btnChallenge">🏆 100번 챌린지! (몇 번 p를 잡을까?)</button>
    <button class="btn btn-ghost" id="btnReset">🔄 챌린지 초기화</button>
  </div>
</div>

<!-- ④ 신뢰구간 시각화 -->
<div class="panel">
  <h2>📏 신뢰구간 — 진짜 <b style="color:#fde047">p</b> 를 잡았는지 보자!
    <span class="badge">노란선 = 진짜 p</span></h2>
  <div class="numline-wrap">
    <canvas id="numlineCanvas" width="900" height="300"></canvas>
  </div>
  <div class="verdict idle" id="verdict">
    <div class="big">🎯</div>
    <div>
      <div style="font-size:1.18rem">왼쪽 버튼을 눌러 표본을 추출해 보세요!</div>
      <div class="ci-info">신뢰구간 안에 진짜 <b style="color:#fde047">p</b> 가 들어가면 ✅ 명중, 아니면 ❌ 실패</div>
    </div>
  </div>

  <!-- 챌린지 결과 -->
  <div class="challenge-wrap">
    <div class="ch-head">
      <span class="title">🏆 챌린지 누적 결과 (현재 시나리오 · 같은 n, k)</span>
      <span style="color:#cbd5e1;font-size:.95rem">기대 명중률: 신뢰도 <b id="chExp" style="color:#fde047">95%</b></span>
    </div>
    <div class="ch-stats">
      <div class="chs ok"><div class="lab">✅ p 명중</div><div class="val" id="chOK">0</div></div>
      <div class="chs miss"><div class="lab">❌ p 실패</div><div class="val" id="chBad">0</div></div>
      <div class="chs rate"><div class="lab">📈 명중률</div><div class="val" id="chRate">--%</div></div>
    </div>
    <div id="chBar"><div id="chBarOK" style="width:0%"></div></div>
    <div style="font-size:.92rem;color:#cbd5e1;margin-top:7px;line-height:1.55">
      💡 100번 챌린지를 여러 번 돌려보면, 명중률이 신뢰도 (95% 또는 99%) 에 가까워지는 것을 볼 수 있어요!
    </div>
  </div>
</div>

<!-- ⑤ 길이 곡선 -->
<div class="panel">
  <h2>📐 신뢰구간의 길이 곡선 <span class="badge">p̂ 가 변할 때 길이 = 2k√(p̂q̂/n)</span></h2>
  <canvas id="lengthCanvas" width="900" height="300"></canvas>

  <div class="len-summary">
    <div class="lsc"><div class="lab">현재 p̂에서 길이</div><div class="val" id="lenNow">--</div></div>
    <div class="lsc"><div class="lab">최대 길이 (p̂=½ 일 때)</div><div class="val" id="lenMax" style="color:#fbcfe8">--</div></div>
    <div class="lsc"><div class="lab">길이 공식의 최대</div><div class="val">k / √n</div></div>
  </div>

  <div class="insight">
    <span class="ico">📏</span>
    <span>
      산술–기하평균 부등식 <code>a + b ≥ 2√(ab)</code> 을 <code>p̂ + q̂ = 1</code> 에 적용하면<br>
      <code>1 = p̂ + q̂ ≥ 2√(p̂q̂)</code> → <code>√(p̂q̂) ≤ 1/2</code> ∴ <code>√(p̂q̂/n) ≤ 1/(2√n)</code><br>
      따라서 신뢰구간의 길이는 <b>2k × 1/(2√n) = k/√n</b> 이하이며, 등호는 <b>p̂ = q̂ = 1/2</b> 일 때 성립해요!
    </span>
  </div>
</div>

<script>
/* =============== 시나리오 정의 =============== */
const SCENARIOS = {
  pizza:   {emoji:"🍕", okEmoji:"🍕", noEmoji:"🥗", trueP:0.62, label:"신메뉴 피자 선호도",
            okWord:"피자 선호", noWord:"다른 메뉴", color1:"#f87171", color2:"#fbbf24"},
  archery: {emoji:"🎯", okEmoji:"🎯", noEmoji:"✖️", trueP:0.78, label:"양궁 선수 명중률",
            okWord:"명중", noWord:"빗나감", color1:"#fbbf24", color2:"#f87171"},
  ad:      {emoji:"📱", okEmoji:"👍", noEmoji:"👋", trueP:0.18, label:"SNS 광고 클릭률",
            okWord:"클릭", noWord:"스킵",  color1:"#22d3ee", color2:"#475569"},
  seed:    {emoji:"🌱", okEmoji:"🌱", noEmoji:"💀", trueP:0.45, label:"새 품종 씨앗 발아율",
            okWord:"발아", noWord:"미발아", color1:"#86efac", color2:"#92400e"}
};

/* =============== 상태 =============== */
let curKey   = "pizza";
let n        = 100;
let k        = 1.96;
let sample   = null;        // {n, X, phat, items:[true/false...]}
let lastCI   = null;        // {lo, hi, ok}
let chStats  = { pizza:{ok:0,bad:0}, archery:{ok:0,bad:0}, ad:{ok:0,bad:0}, seed:{ok:0,bad:0} };
let revealed = false;

const $ = id => document.getElementById(id);

/* =============== 유틸 =============== */
function fmt(v,d=3){ if(!isFinite(v)) return '--'; return Number(v.toFixed(d)).toString(); }
function fmtPct(v,d=1){ if(!isFinite(v)) return '--'; return (v*100).toFixed(d) + '%'; }
function clamp(v,a,b){ return Math.max(a, Math.min(b, v)); }

/* =============== 표본 추출 =============== */
function drawSample(){
  const p = SCENARIOS[curKey].trueP;
  const items = [];
  let X = 0;
  for(let i=0;i<n;i++){
    const ok = Math.random() < p;
    items.push(ok);
    if(ok) X++;
  }
  return { n, X, phat: X/n, items };
}
function makeCI(s){
  const phat = s.phat;
  const qhat = 1 - phat;
  const half = k * Math.sqrt(phat*qhat/s.n);
  return { lo: phat-half, hi: phat+half, half };
}

/* =============== 항아리 그리기 (애니메이션) =============== */
let jarTime = 0;
function drawJar(){
  const cv = $('jarCanvas');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const sc = SCENARIOS[curKey];

  // 항아리 윤곽
  const jx = W*0.18, jy = H*0.18, jw = W*0.64, jh = H*0.74;
  ctx.fillStyle='rgba(168,85,247,.13)';
  ctx.strokeStyle='rgba(196,181,253,.7)';
  ctx.lineWidth=3;
  ctx.beginPath();
  // 항아리 모양 (입구가 살짝 좁은 통)
  ctx.moveTo(jx, jy+jh*0.08);
  ctx.quadraticCurveTo(jx-jw*0.12, jy+jh*0.5, jx, jy+jh);
  ctx.quadraticCurveTo(jx+jw*0.5, jy+jh*1.18, jx+jw, jy+jh);
  ctx.quadraticCurveTo(jx+jw*1.12, jy+jh*0.5, jx+jw, jy+jh*0.08);
  ctx.quadraticCurveTo(jx+jw*0.5, jy-jh*0.06, jx, jy+jh*0.08);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // 항아리 입구
  ctx.fillStyle='rgba(15,23,42,.7)';
  ctx.beginPath();
  ctx.ellipse(jx+jw/2, jy+jh*0.08, jw*0.42, jh*0.07, 0, 0, Math.PI*2);
  ctx.fill();
  ctx.stroke();

  // 안에 떠다니는 공들 (랜덤 위치, 실제 p와는 무관하게 시각용)
  jarTime += 0.012;
  const items = 28;
  for(let i=0;i<items;i++){
    const seed = i*97;
    const ang = (i*0.45 + jarTime*0.5) % (Math.PI*2);
    const rd  = (Math.sin(i*1.3 + jarTime)*0.5 + 0.5);
    const cx = jx + jw/2 + Math.cos(ang)*jw*0.28*rd;
    const cy = jy + jh*0.55 + Math.sin(ang*1.3 + i)*jh*0.28*rd;
    const isOk = (i % 100) / 100 < sc.trueP;  // 시각용
    // 진짜 p를 그대로 보여주면 정답 노출이 되니, 약간 셔플
    const visualOk = Math.sin(seed*11 + jarTime*0.7) > (revealed ? 1-2*sc.trueP : 0);
    ctx.fillStyle = visualOk ? sc.color1 : sc.color2;
    ctx.beginPath();
    ctx.arc(cx, cy, 8 + Math.sin(jarTime*2 + i)*1, 0, Math.PI*2);
    ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,.3)';
    ctx.lineWidth=1;
    ctx.stroke();
    // 이모지
    ctx.font = '12px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillStyle='#fff';
    ctx.fillText(visualOk ? sc.okEmoji : sc.noEmoji, cx, cy);
  }

  // 큰 ? 마크 (숨김 모드일 때)
  if(!revealed){
    ctx.fillStyle='rgba(251,191,36,.85)';
    ctx.font='bold 76px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.shadowColor='rgba(0,0,0,.6)';
    ctx.shadowBlur=8;
    ctx.fillText('?', jx+jw/2, jy+jh*0.45);
    ctx.shadowBlur=0;
  } else {
    // 모비율 표시
    ctx.fillStyle='#fde047';
    ctx.font='bold 24px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('p = '+fmt(sc.trueP,3), jx+jw/2, jy+jh*0.45);
  }
}

/* =============== 표본 그리기 =============== */
let sampleAnim = 0;  // 0~1
function drawSampleCanvas(){
  const cv = $('sampleCanvas');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const sc = SCENARIOS[curKey];

  if(!sample){
    ctx.fillStyle='#94a3b8';
    ctx.font='15px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('🎲 아래 \"표본 추출\" 버튼을 눌러 보세요', W/2, H/2);
    return;
  }

  // 표본 점들을 격자로 배치
  const padding = 16;
  const nn = sample.n;
  const aspect = (W-padding*2)/(H-padding*2);
  let cols = Math.ceil(Math.sqrt(nn * aspect));
  let rows = Math.ceil(nn/cols);
  while(cols*(rows-1) >= nn && rows > 1) rows--;
  const cellW = (W-padding*2)/cols;
  const cellH = (H-padding*2)/rows;
  const r = Math.min(cellW, cellH) * 0.36;

  // 애니메이션: 몇 개까지 보일지
  const shown = Math.min(nn, Math.floor(nn * sampleAnim));
  for(let i=0;i<shown;i++){
    const row = Math.floor(i/cols);
    const col = i%cols;
    const cx = padding + col*cellW + cellW/2;
    const cy = padding + row*cellH + cellH/2;
    const ok = sample.items[i];
    ctx.fillStyle = ok ? sc.color1 : sc.color2;
    ctx.beginPath();
    ctx.arc(cx, cy, r, 0, Math.PI*2);
    ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,.45)';
    ctx.lineWidth=1;
    ctx.stroke();
    // 이모지 (점이 충분히 클 때)
    if(r > 8){
      ctx.font = Math.floor(r*1.05)+'px sans-serif';
      ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillStyle='#fff';
      ctx.fillText(ok ? sc.okEmoji : sc.noEmoji, cx, cy);
    }
  }

  // 범례
  ctx.font='bold 13px sans-serif';
  ctx.textAlign='left'; ctx.textBaseline='top';
  ctx.fillStyle=sc.color1; ctx.fillRect(8, 6, 14, 14);
  ctx.fillStyle='#e2e8f0'; ctx.fillText(sc.okWord+' = '+sample.X+'개', 28, 6);
  ctx.fillStyle=sc.color2; ctx.fillRect(8, 26, 14, 14);
  ctx.fillStyle='#e2e8f0'; ctx.fillText(sc.noWord+' = '+(sample.n-sample.X)+'개', 28, 26);
}

function animateSample(){
  sampleAnim = 0;
  const t0 = performance.now();
  function step(now){
    sampleAnim = Math.min(1, (now - t0)/600);
    drawSampleCanvas();
    if(sampleAnim < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

/* =============== 수직선 (신뢰구간) =============== */
function drawNumline(){
  const cv = $('numlineCanvas');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const sc = SCENARIOS[curKey];
  const padL=60, padR=60, padT=40, padB=70;
  const plotW=W-padL-padR, plotH=H-padT-padB;
  const yMid = padT + plotH/2;

  // 축
  ctx.strokeStyle='rgba(148,163,184,.6)';
  ctx.lineWidth=2;
  ctx.beginPath();
  ctx.moveTo(padL, yMid); ctx.lineTo(W-padR, yMid);
  ctx.stroke();

  // 눈금
  const ticks = 11;
  ctx.strokeStyle='rgba(148,163,184,.4)';
  ctx.lineWidth=1;
  ctx.fillStyle='#cbd5e1';
  ctx.font='13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  for(let i=0;i<ticks;i++){
    const v = i/(ticks-1);
    const x = padL + v*plotW;
    ctx.beginPath();
    ctx.moveTo(x, yMid-7); ctx.lineTo(x, yMid+7);
    ctx.stroke();
    ctx.fillText(fmt(v,1), x, yMid+12);
  }
  ctx.fillStyle='#94a3b8';
  ctx.font='bold 14px sans-serif';
  ctx.fillText('모비율 p', W/2, H-22);

  const X = v => padL + clamp(v,0,1)*plotW;

  // 진짜 p (노란 수직선)
  const truex = X(sc.trueP);
  ctx.strokeStyle='#fde047';
  ctx.lineWidth=3;
  ctx.setLineDash([6,4]);
  ctx.beginPath();
  ctx.moveTo(truex, padT); ctx.lineTo(truex, padT+plotH);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#fde047';
  ctx.font='bold 18px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  ctx.fillText('p = '+fmt(sc.trueP,3), truex, padT-6);
  // 작은 별
  ctx.font='22px sans-serif';
  ctx.fillText('⭐', truex, padT+plotH+50);

  if(!sample){
    ctx.fillStyle='#94a3b8';
    ctx.font='14px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('표본을 추출하면 신뢰구간이 표시됩니다', W/2, yMid - 60);
    return;
  }

  // 신뢰구간 막대
  const ci = lastCI;
  const x1 = X(ci.lo), x2 = X(ci.hi), xc = X(sample.phat);
  const ok = ci.lo <= sc.trueP && sc.trueP <= ci.hi;

  // 95% 막대
  ctx.strokeStyle = ok ? 'rgba(34,197,94,.92)' : 'rgba(244,63,94,.92)';
  ctx.lineWidth = 18;
  ctx.lineCap='round';
  ctx.beginPath();
  ctx.moveTo(x1, yMid); ctx.lineTo(x2, yMid);
  ctx.stroke();
  ctx.lineCap='butt';

  // 양 끝 [, ]
  ctx.strokeStyle = ok ? '#86efac' : '#fca5a5';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(x1, yMid-22); ctx.lineTo(x1, yMid+22);
  ctx.moveTo(x2, yMid-22); ctx.lineTo(x2, yMid+22);
  ctx.stroke();

  // p̂ 점
  ctx.fillStyle = '#fff';
  ctx.beginPath();
  ctx.arc(xc, yMid, 9, 0, Math.PI*2);
  ctx.fill();
  ctx.strokeStyle='#0f172a';
  ctx.lineWidth=2;
  ctx.stroke();

  // 라벨
  ctx.fillStyle = ok ? '#dcfce7' : '#fecaca';
  ctx.font='bold 14px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  ctx.fillText(fmt(ci.lo,3), x1, yMid-28);
  ctx.fillText(fmt(ci.hi,3), x2, yMid-28);
  ctx.fillStyle='#fff';
  ctx.font='bold 15px sans-serif';
  ctx.fillText('p̂ = '+fmt(sample.phat,3), xc, yMid-32);

  // 길이 라벨
  const midY = yMid + 40;
  ctx.strokeStyle='rgba(196,181,253,.55)';
  ctx.lineWidth=1.5;
  ctx.beginPath();
  ctx.moveTo(x1, midY-6); ctx.lineTo(x1, midY+6);
  ctx.moveTo(x2, midY-6); ctx.lineTo(x2, midY+6);
  ctx.moveTo(x1, midY); ctx.lineTo(x2, midY);
  ctx.stroke();
  ctx.fillStyle='#c4b5fd';
  ctx.font='bold 13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  ctx.fillText('길이 ≈ '+fmt(ci.hi-ci.lo,4), (x1+x2)/2, midY+3);
}

/* =============== 길이 곡선 =============== */
function drawLengthCurve(){
  const cv = $('lengthCanvas');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL=64, padR=24, padT=22, padB=56;
  const plotW=W-padL-padR, plotH=H-padT-padB;

  // 함수: L(p̂) = 2k * sqrt(p̂(1-p̂)/n)
  const lenFn = ph => 2*k*Math.sqrt(ph*(1-ph)/n);
  const lenMax = k/Math.sqrt(n);

  const yMax = lenMax * 1.18;
  const X = ph => padL + ph*plotW;
  const Y = L  => padT+plotH - (L/yMax)*plotH;

  // 격자
  ctx.strokeStyle='rgba(148,163,184,.13)';
  ctx.setLineDash([3,3]); ctx.lineWidth=1;
  for(let i=0;i<=10;i++){
    const x = padL + (i/10)*plotW;
    ctx.beginPath();
    ctx.moveTo(x, padT); ctx.lineTo(x, padT+plotH);
    ctx.stroke();
  }
  for(let i=0;i<=4;i++){
    const y = padT + (i/4)*plotH;
    ctx.beginPath();
    ctx.moveTo(padL, y); ctx.lineTo(W-padR, y);
    ctx.stroke();
  }
  ctx.setLineDash([]);

  // 곡선 (반원 모양)
  ctx.strokeStyle='#fbbf24';
  ctx.lineWidth=3;
  ctx.beginPath();
  let first=true;
  for(let i=0;i<=200;i++){
    const ph = i/200;
    const y = Y(lenFn(ph));
    if(first){ ctx.moveTo(X(ph), y); first=false; }
    else      ctx.lineTo(X(ph), y);
  }
  ctx.stroke();
  // 곡선 아래 채움
  ctx.fillStyle='rgba(251,191,36,.10)';
  ctx.lineTo(X(1), Y(0));
  ctx.lineTo(X(0), Y(0));
  ctx.closePath();
  ctx.fill();

  // 최대선 (y=k/√n)
  ctx.strokeStyle='#fbcfe8';
  ctx.lineWidth=2; ctx.setLineDash([7,5]);
  ctx.beginPath();
  ctx.moveTo(padL, Y(lenMax)); ctx.lineTo(W-padR, Y(lenMax));
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#fbcfe8';
  ctx.font='bold 14px sans-serif';
  ctx.textAlign='right'; ctx.textBaseline='alphabetic';
  ctx.fillText('최대길이 k/√n = '+fmt(lenMax,4), W-padR-6, Y(lenMax)-5);

  // p̂ = 1/2 선
  ctx.strokeStyle='rgba(196,181,253,.6)';
  ctx.lineWidth=2; ctx.setLineDash([5,5]);
  ctx.beginPath();
  ctx.moveTo(X(0.5), padT); ctx.lineTo(X(0.5), padT+plotH);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#c4b5fd';
  ctx.font='bold 13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  ctx.fillText('p̂ = ½', X(0.5), padT-6);

  // 현재 p̂ 마커
  if(sample){
    const ph = sample.phat;
    const cx = X(ph), cy = Y(lenFn(ph));
    ctx.strokeStyle='#22d3ee';
    ctx.lineWidth=2;
    ctx.beginPath();
    ctx.moveTo(cx, padT+plotH); ctx.lineTo(cx, cy);
    ctx.stroke();
    ctx.fillStyle='#22d3ee';
    ctx.beginPath();
    ctx.arc(cx, cy, 7, 0, Math.PI*2);
    ctx.fill();
    ctx.strokeStyle='#fff';
    ctx.lineWidth=2;
    ctx.stroke();
    ctx.fillStyle='#22d3ee';
    ctx.font='bold 13px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='alphabetic';
    ctx.fillText('현재 p̂', cx, cy-12);
  }

  // 축
  ctx.strokeStyle='rgba(148,163,184,.5)';
  ctx.lineWidth=1.5;
  ctx.beginPath();
  ctx.moveTo(padL, padT+plotH); ctx.lineTo(W-padR, padT+plotH);
  ctx.moveTo(padL, padT); ctx.lineTo(padL, padT+plotH);
  ctx.stroke();

  // x눈금
  ctx.fillStyle='#cbd5e1';
  ctx.font='13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  for(let i=0;i<=10;i++){
    const v = i/10;
    ctx.fillText(fmt(v,1), X(v), padT+plotH+6);
  }
  ctx.fillStyle='#94a3b8';
  ctx.font='bold 14px sans-serif';
  ctx.fillText('표본비율 p̂', W/2, H-18);

  // y눈금
  ctx.fillStyle='#cbd5e1';
  ctx.font='13px sans-serif';
  ctx.textAlign='right'; ctx.textBaseline='middle';
  for(let i=0;i<=4;i++){
    const v = (i/4)*yMax;
    ctx.fillText(fmt(v,3), padL-6, Y(v));
  }
  ctx.save();
  ctx.translate(20, padT+plotH/2);
  ctx.rotate(-Math.PI/2);
  ctx.fillStyle='#94a3b8';
  ctx.font='bold 14px sans-serif';
  ctx.textAlign='center';
  ctx.fillText('신뢰구간 길이 = 2k√(p̂q̂/n)', 0, 0);
  ctx.restore();

  // 요약값
  $('lenMax').textContent = fmt(lenMax,4);
  $('lenNow').textContent = sample ? fmt(lenFn(sample.phat),4) : '--';
}

/* =============== 챌린지 (100번) =============== */
function runChallenge(){
  const sc = SCENARIOS[curKey];
  let ok=0, bad=0;
  let lastS=null, lastC=null;
  for(let i=0;i<100;i++){
    const s = drawSample();
    const c = makeCI(s);
    if(c.lo<=sc.trueP && sc.trueP<=c.hi) ok++; else bad++;
    lastS=s; lastC=c;
  }
  chStats[curKey].ok += ok;
  chStats[curKey].bad += bad;
  sample = lastS;
  lastCI = lastC;
  updateAll(true);
}

/* =============== 메인 추출 1번 =============== */
function singleDraw(){
  const sc = SCENARIOS[curKey];
  sample = drawSample();
  lastCI = makeCI(sample);
  const ok = lastCI.lo<=sc.trueP && sc.trueP<=lastCI.hi;
  if(ok) chStats[curKey].ok++; else chStats[curKey].bad++;
  animateSample();
  updateAll(true);
}

/* =============== 업데이트 =============== */
function updateAll(animateVerdict=false){
  const sc = SCENARIOS[curKey];
  $('truePVal').textContent = fmt(sc.trueP,3);
  $('kN').textContent = sample ? sample.n : '--';
  $('kX').textContent = sample ? sample.X : '--';
  $('kPhat').textContent = sample ? fmt(sample.phat,3) : '--';

  // 진짜 p 박스 표시 (학생이 정답보기 버튼 눌렀을 때)
  $('truePBox').classList.toggle('hidden', !revealed);
  $('btnReveal').textContent = revealed ? '🙈 정답 숨기기' : '👁 정답 보기';

  // 신뢰구간 verdict
  const v = $('verdict');
  if(!sample){
    v.className='verdict idle';
    v.innerHTML = '<div class="big">🎯</div><div><div style="font-size:1.18rem">위 버튼을 눌러 표본을 추출해 보세요!</div><div class="ci-info">신뢰구간 안에 진짜 <b style="color:#fde047">p</b> 가 들어가면 ✅ 명중, 아니면 ❌ 실패</div></div>';
  } else {
    const ok = lastCI.lo<=sc.trueP && sc.trueP<=lastCI.hi;
    v.className = 'verdict ' + (ok ? 'ok' : 'bad') + (animateVerdict ? ' pulse' : '');
    const conf = Math.round((k===1.96?95:99));
    v.innerHTML =
      '<div class="big">'+(ok?'✅':'❌')+'</div>' +
      '<div>' +
      '<div style="font-size:1.25rem">'+
        (ok ? '신뢰구간이 진짜 <b style="color:#fde047">p</b>를 잡았어요!' :
              '아쉽게도 신뢰구간이 진짜 <b style="color:#fde047">p</b>를 놓쳤어요')+
      '</div>'+
      '<div class="ci-info">'+
        'p̂ = '+fmt(sample.phat,3)+', '+conf+'% 신뢰구간 ['+fmt(lastCI.lo,3)+', '+fmt(lastCI.hi,3)+'] '+
        '/ 진짜 p = '+fmt(sc.trueP,3)+
      '</div>'+
      '</div>';
    if(animateVerdict){
      setTimeout(()=>v.classList.remove('pulse'), 800);
    }
  }

  // 챌린지
  const cs = chStats[curKey];
  const tot = cs.ok + cs.bad;
  $('chOK').textContent = cs.ok;
  $('chBad').textContent = cs.bad;
  $('chRate').textContent = tot>0 ? fmtPct(cs.ok/tot,1) : '--%';
  $('chBarOK').style.width = tot>0 ? (cs.ok/tot*100).toFixed(1)+'%' : '0%';
  $('chExp').textContent = (k===1.96 ? '95%' : '99%');

  drawSampleCanvas();
  drawNumline();
  drawLengthCurve();
}

/* =============== 이벤트 =============== */
document.querySelectorAll('.scn').forEach(b=>{
  b.addEventListener('click', ()=>{
    document.querySelectorAll('.scn').forEach(x=>x.classList.toggle('active', x===b));
    curKey = b.dataset.key;
    sample = null;
    lastCI = null;
    revealed = false;
    updateAll();
  });
});

$('nRange').addEventListener('input', e=>{
  n = parseInt(e.target.value);
  $('nVal').textContent = n;
  drawLengthCurve();  // n만 바뀌면 곡선/최대길이 표시 즉시 갱신
});

document.querySelectorAll('#kBtns .k-btn').forEach(b=>{
  b.addEventListener('click', ()=>{
    document.querySelectorAll('#kBtns .k-btn').forEach(x=>x.classList.toggle('active', x===b));
    k = parseFloat(b.dataset.k);
    // 신뢰도가 바뀌면 직전 신뢰구간도 다시 계산
    if(sample) lastCI = makeCI(sample);
    updateAll();
  });
});

$('btnDraw').addEventListener('click', singleDraw);
$('btnChallenge').addEventListener('click', runChallenge);
$('btnReset').addEventListener('click', ()=>{
  chStats = { pizza:{ok:0,bad:0}, archery:{ok:0,bad:0}, ad:{ok:0,bad:0}, seed:{ok:0,bad:0} };
  updateAll();
});
$('btnReveal').addEventListener('click', ()=>{
  revealed = !revealed;
  updateAll();
});
window.addEventListener('resize', ()=>{ drawJar(); updateAll(); });

/* =============== 항아리 애니메이션 루프 =============== */
function tick(){ drawJar(); requestAnimationFrame(tick); }
tick();

/* =============== 초기화 =============== */
updateAll();
</script>
</body>
</html>
"""


def render():
    st.subheader("🏺 모비율 신뢰구간 챌린지 — 미스터리 항아리 속 p 잡기")
    st.caption(
        "항아리 속에 숨겨진 진짜 모비율 p를 표본만 가지고 추정해 봅시다. "
        "표본비율 p̂으로 만든 95%·99% 신뢰구간이 실제로 p를 잡는지 직접 확인하고, "
        "신뢰구간 길이가 왜 p̂ = ½ 일 때 최대가 되는지도 시각적으로 살펴보세요."
    )

    components.html(_HTML, height=2900, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
