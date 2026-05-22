# activities/probability_new/mini/sample_proportion_dist_lab.py
"""
표본비율 p̂의 분포 — 실생활 시뮬레이션 미니활동
- 4가지 모집단(동전·자유투·매점 빵·SNS 광고 클릭)에서 크기 n의 표본을 반복 추출
- 각 표본의 성공 비율 p̂ = X/n 을 누적하여 히스토그램으로 시각화
- 이론값 E(p̂)=p, V(p̂)=pq/n, σ(p̂)=√(pq/n) 와 비교
- 정규근사 N(p, pq/n) 곡선을 함께 그려 종 모양으로 수렴하는 모습 관찰
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🎯 미니: 표본비율 p̂의 분포 — 실생활 시뮬레이션",
    "description": "동전·자유투·매점 단팥빵·SNS 광고 클릭 4가지 실생활 사례에서 "
                   "표본비율 p̂의 분포가 N(p, pq/n)로 나타나는 과정을 직접 시뮬레이션합니다.",
    "order": 24,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "표본비율분포시뮬"

_QUESTIONS = [
    {"type": "markdown",
     "text": "**📝 활동 성찰 — 표본비율 p̂의 분포**"},
    {
        "key": "E_phat_관찰",
        "label": "**E(p̂) ≈ p** 인지 직접 시뮬레이션으로 확인해 보았어요. "
                 "4가지 사례(동전 0.5 / 자유투 0.7 / 단팥빵 0.4 / 광고 0.15)에서 "
                 "표본을 충분히 많이 뽑았을 때 p̂의 평균(경험값)은 모비율 p와 어떻게 일치했나요?",
        "type": "text_area", "height": 110,
        "placeholder": "동전에서는 ___, 자유투에서는 ___, 단팥빵에서는 ___, 광고에서는 ___. "
                       "결국 E(p̂)는 ___와 가까웠다.",
    },
    {
        "key": "n_바꿀때_분포",
        "label": "표본 크기 **n**을 작게(예: n=10)와 크게(예: n=200) 바꿔 보았을 때 "
                 "p̂들의 히스토그램은 어떻게 달라졌나요? 폭(σ(p̂))과 모양은 어떻게 변했나요?",
        "type": "text_area", "height": 110,
        "placeholder": "n이 작을 때는 히스토그램이 ___, n이 클 때는 ___. "
                       "표준편차 √(pq/n)는 n이 커질수록 ___ 했다.",
    },
    {
        "key": "정규곡선_비교",
        "label": "히스토그램 위에 그려진 **정규곡선 N(p, pq/n)**과 실제 누적된 막대들의 "
                 "모양은 얼마나 잘 일치했나요? n이 충분히 크다는 게 어떤 의미라고 느꼈나요?",
        "type": "text_area", "height": 100,
        "placeholder": "처음에는 곡선과 막대가 ___, 표본을 더 많이 뽑을수록 ___. "
                       "n이 충분히 크다는 것은 ___ 이라는 의미이다.",
    },
    {
        "key": "p_다를때",
        "label": "p가 다른 4가지 사례를 비교해 보면, 같은 n에서도 p̂의 **퍼짐 정도**(σ(p̂))는 어떻게 달랐나요? "
                 "어떤 p에서 가장 폭이 넓고 어떤 p에서 가장 좁았나요?",
        "type": "text_area", "height": 100,
        "placeholder": "동전(p=0.5)에서는 σ(p̂)가 가장 ___, 광고(p=0.15)에서는 ___. "
                       "이는 pq가 p=___ 일 때 최대가 되기 때문이다.",
    },
    {
        "key": "실생활_의미",
        "label": "이 시뮬레이션은 실생활에서 어떤 의미가 있을까요? "
                 "예를 들어 \"광고 클릭률이 15%다\" 라는 광고주의 말을 듣고 "
                 "표본조사로 확인하려고 할 때, n을 어느 정도로 잡아야 결과를 신뢰할 수 있을까요?",
        "type": "text_area", "height": 110,
        "placeholder": "n이 작으면 한 번 측정한 p̂이 진짜 p에서 ___ 떨어져 있을 수 있다. "
                       "그래서 광고 효과를 측정할 때는 ___",
    },
    {
        "key": "표본비율_정의_나만의말",
        "label": "이 활동을 통해 알게 된 **표본비율 p̂의 분포**(평균·분산·근사 정규성)를 "
                 "본인의 말로 한 문장으로 적어 보세요.",
        "type": "text_area", "height": 80,
        "placeholder": "표본의 크기 n이 충분히 크면 p̂은 ___ 라는 정규분포에 가까워진다.",
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


# ─────────────────────────────────────────────────────────────────────────────
# HTML 템플릿 — scenario마다 색/이모지/p/라벨만 바꿔서 재사용
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
/* ============ 헤더 ============ */
.hdr{
  text-align:center;
  background:linear-gradient(135deg,__HDR_A__,__HDR_B__);
  border:2.5px solid __HDR_BORDER__;border-radius:18px;
  padding:14px 18px;margin-bottom:13px;
}
.hdr h1{font-size:1.55rem;font-weight:900;color:__HDR_TXT__;margin-bottom:5px;letter-spacing:.3px}
.hdr .scn{font-size:1.05rem;color:#cbd5e1;line-height:1.55}
.hdr .scn b{color:#fde047}
.hdr .pval{
  display:inline-block;background:rgba(15,23,42,.5);
  padding:5px 14px;border-radius:999px;margin-top:7px;
  font-size:1.15rem;color:#fde047;font-weight:900;letter-spacing:.4px;
}

/* ============ 모집단 카드 (큰 사례 시각화) ============ */
.pop-card{
  background:rgba(15,23,42,.72);border:2px solid __ACC_DIM__;
  border-radius:16px;padding:14px;margin-bottom:13px;
}
.pop-grid{
  display:grid;grid-template-columns:1.2fr 1fr;gap:14px;
}
@media(max-width:760px){.pop-grid{grid-template-columns:1fr}}
.pop-viz{
  background:rgba(15,23,42,.5);border-radius:13px;padding:14px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  min-height:170px;border:1.5px dashed __ACC_DIM__;
}
.pop-emo{font-size:3.4rem;margin-bottom:4px;line-height:1;}
.pop-name{font-size:1.05rem;color:#cbd5e1;font-weight:800;margin-bottom:9px;text-align:center}
.bar-stack{
  width:100%;max-width:340px;height:34px;border-radius:17px;
  background:rgba(15,23,42,.7);overflow:hidden;
  border:1.5px solid rgba(148,163,184,.3);display:flex;
}
.bar-succ{background:linear-gradient(90deg,__SUCC_A__,__SUCC_B__);
  display:flex;align-items:center;justify-content:center;
  font-weight:900;color:#fff;font-size:.95rem;letter-spacing:.5px;
  transition:width .4s ease;
}
.bar-fail{background:linear-gradient(90deg,#475569,#334155);
  display:flex;align-items:center;justify-content:center;
  font-weight:900;color:#cbd5e1;font-size:.95rem;
  transition:width .4s ease;
}
.legend{
  display:flex;gap:14px;margin-top:8px;font-size:.93rem;font-weight:700;
}
.legend .l-sw{display:inline-block;width:14px;height:14px;border-radius:4px;margin-right:5px;vertical-align:middle}
.legend .l-succ .l-sw{background:__SUCC_B__}
.legend .l-fail .l-sw{background:#64748b}
.legend .l-succ{color:__HDR_TXT__}
.legend .l-fail{color:#cbd5e1}

.pop-stats{
  display:flex;flex-direction:column;justify-content:center;gap:9px;
  background:rgba(15,23,42,.5);border:1.5px solid rgba(99,102,241,.3);
  border-radius:13px;padding:13px;
}
.pop-stats h3{font-size:.95rem;color:#a5b4fc;font-weight:800;margin-bottom:2px;letter-spacing:.3px}
.ps-row{
  display:flex;justify-content:space-between;align-items:center;
  background:rgba(15,23,42,.55);border:1px solid rgba(148,163,184,.18);
  border-radius:9px;padding:6px 11px;
}
.ps-lab{font-size:1rem;color:#cbd5e1;font-weight:700}
.ps-val{font-size:1.25rem;color:#fde047;font-weight:900;font-variant-numeric:tabular-nums}

/* ============ 컨트롤 ============ */
.panel{
  background:rgba(15,23,42,.72);border:1.5px solid rgba(99,102,241,.3);
  border-radius:14px;padding:14px;margin-bottom:13px;
}
.panel h2{
  font-size:1.15rem;font-weight:900;color:__ACC__;margin-bottom:10px;
  display:flex;align-items:center;gap:8px;letter-spacing:.3px;
}
.panel h2 .badge{
  font-size:.85rem;color:#cbd5e1;background:rgba(99,102,241,.2);
  padding:3px 9px;border-radius:999px;font-weight:700;
}

.ctl-row{
  display:flex;align-items:center;gap:11px;flex-wrap:wrap;
  background:rgba(56,189,248,.07);border:1.5px solid rgba(56,189,248,.32);
  border-radius:11px;padding:10px 13px;margin-bottom:10px;
}
.ctl-lab{font-size:1.05rem;font-weight:800;color:#7dd3fc;min-width:140px;display:flex;align-items:center;gap:6px}
.ctl-range{flex:1;min-width:180px;accent-color:#38bdf8;height:7px}
.ctl-val{
  font-size:1.45rem;font-weight:900;color:#fde047;min-width:78px;
  background:rgba(15,23,42,.7);padding:3px 14px;border-radius:9px;text-align:center;
}

.btn-row{display:flex;gap:9px;flex-wrap:wrap}
.btn{
  flex:1;min-width:135px;padding:12px 14px;border:none;border-radius:11px;
  font-size:1.02rem;font-weight:900;color:#fff;cursor:pointer;
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
.btn-r{background:rgba(71,85,105,.65);border:1.5px solid rgba(148,163,184,.3);flex:0 1 100px;font-size:.95rem}
.btn-r:hover:not(:disabled){background:rgba(71,85,105,.9)}

/* ============ 최근 표본 ============ */
.sample-box{
  background:rgba(34,197,94,.08);border:2px solid rgba(34,197,94,.35);
  border-radius:12px;padding:12px;margin-top:10px;
}
.sb-title{
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;
  font-size:1rem;font-weight:800;color:#86efac;margin-bottom:7px;
}
.sb-title .phat-line{color:#fde047;font-size:1.2rem;font-weight:900}
.sb-grid{
  display:flex;flex-wrap:wrap;gap:5px;min-height:36px;align-items:center;
}
.sb-cell{
  width:24px;height:24px;border-radius:7px;
  display:flex;align-items:center;justify-content:center;
  font-size:.9rem;font-weight:900;color:#fff;line-height:1;
  animation:cellPop .35s cubic-bezier(.34,1.56,.64,1) both;
}
.sb-cell.succ{background:linear-gradient(135deg,__SUCC_A__,__SUCC_B__);box-shadow:0 1px 4px rgba(0,0,0,.3)}
.sb-cell.fail{background:linear-gradient(135deg,#64748b,#475569)}
@keyframes cellPop{from{opacity:0;transform:scale(.2)}to{opacity:1;transform:scale(1)}}
.sb-empty{color:#64748b;font-size:.95rem;font-style:italic}

/* ============ 분포 ============ */
.dist-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(99,102,241,.3);
  border-radius:12px;padding:12px;
}
.dist-title{
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;
  font-size:1rem;font-weight:800;color:#cbd5e1;margin-bottom:8px;
}
.dist-title .cnt{color:#fde047;font-weight:900}
.dist-legend{
  display:flex;gap:14px;font-size:.88rem;color:#94a3b8;font-weight:700;margin-top:8px;
  flex-wrap:wrap;
}
.dist-legend span i{display:inline-block;vertical-align:middle;margin-right:4px}
.dlg-bar i{width:14px;height:11px;background:linear-gradient(180deg,__ACC__,rgba(99,102,241,.4))}
.dlg-curve i{width:18px;height:0;border-top:3px solid #fde047}
.dlg-p i{width:0;height:14px;border-left:2.5px dashed #fb7185}
#distCanvas{
  display:block;width:100%;height:280px;
  background:rgba(15,23,42,.5);border-radius:8px;
}

/* ============ 통계 카드 ============ */
.stats{
  display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px;
}
@media(max-width:680px){.stats{grid-template-columns:1fr}}
.s-card{
  background:rgba(30,41,59,.75);border-radius:13px;padding:11px;
  border:1.5px solid rgba(99,102,241,.3);
}
.s-card.s-mean{border-color:rgba(244,63,94,.5);background:rgba(244,63,94,.08)}
.s-card.s-var {border-color:rgba(168,85,247,.5);background:rgba(168,85,247,.08)}
.s-card.s-sd  {border-color:rgba(56,189,248,.5);background:rgba(56,189,248,.08)}

.s-head{font-size:1rem;font-weight:800;margin-bottom:4px;letter-spacing:.3px}
.s-card.s-mean .s-head{color:#fb7185}
.s-card.s-var  .s-head{color:#c4b5fd}
.s-card.s-sd   .s-head{color:#7dd3fc}

.s-val{font-size:1.6rem;font-weight:900;color:#fef3c7;letter-spacing:.5px;line-height:1.1;
       font-variant-numeric:tabular-nums}
.s-sub{font-size:.92rem;color:#94a3b8;margin-top:4px;line-height:1.4}
.s-sub .th{color:#fde047;font-weight:800}
.s-bar-track{
  height:7px;background:rgba(15,23,42,.7);border-radius:4px;
  overflow:hidden;margin-top:6px;
}
.s-bar-fill{
  height:100%;border-radius:4px;
  transition:width .35s cubic-bezier(.4,1.6,.7,.95);
}
.s-mean .s-bar-fill{background:linear-gradient(90deg,#f43f5e,#fb7185)}
.s-var  .s-bar-fill{background:linear-gradient(90deg,#a855f7,#c4b5fd)}
.s-sd   .s-bar-fill{background:linear-gradient(90deg,#0ea5e9,#7dd3fc)}

/* ============ 인사이트 ============ */
.insight{
  background:rgba(251,191,36,.1);border:2px solid rgba(251,191,36,.4);
  border-radius:13px;padding:12px 15px;margin-top:12px;
  font-size:1.02rem;color:#fef3c7;line-height:1.65;
  display:flex;align-items:flex-start;gap:9px;
}
.insight .ico{font-size:1.5rem;flex-shrink:0;line-height:1.2}
.insight b{color:#fde047}
.insight .ok{color:#86efac;font-weight:900}
</style>
</head>
<body>

<!-- 헤더 -->
<div class="hdr">
  <h1>__TITLE__</h1>
  <div class="scn">__SCN_TEXT__</div>
  <div class="pval">모비율 p = __P_DISP__</div>
</div>

<!-- 모집단 카드 -->
<div class="pop-card">
  <div class="pop-grid">
    <div class="pop-viz">
      <div class="pop-emo">__POP_EMO__</div>
      <div class="pop-name">__POP_NAME__</div>
      <div class="bar-stack">
        <div class="bar-succ" id="barSucc"></div>
        <div class="bar-fail" id="barFail"></div>
      </div>
      <div class="legend">
        <span class="l-succ"><span class="l-sw"></span>__SUCC_LABEL__</span>
        <span class="l-fail"><span class="l-sw"></span>__FAIL_LABEL__</span>
      </div>
    </div>
    <div class="pop-stats">
      <h3>📊 모집단 정보</h3>
      <div class="ps-row"><span class="ps-lab">모비율 p</span><span class="ps-val" id="psP">--</span></div>
      <div class="ps-row"><span class="ps-lab">실패확률 q = 1−p</span><span class="ps-val" id="psQ">--</span></div>
      <div class="ps-row"><span class="ps-lab">pq</span><span class="ps-val" id="psPQ">--</span></div>
    </div>
  </div>
</div>

<!-- 컨트롤 -->
<div class="panel">
  <h2>🎯 표본을 뽑아 p̂ = X/n 을 계산해 봐요 <span class="badge">각 표본 = n번 독립시행</span></h2>

  <div class="ctl-row">
    <span class="ctl-lab">🧮 표본 크기 n</span>
    <input type="range" min="10" max="500" step="5" value="50" class="ctl-range" id="nRange">
    <span class="ctl-val" id="nVal">50</span>
  </div>

  <div class="btn-row">
    <button class="btn btn-1" id="btnDraw1">🎲 표본 1개 뽑기</button>
    <button class="btn btn-2" id="btnDraw50">⚡ 50번 뽑기</button>
    <button class="btn btn-3" id="btnDraw500">🚀 500번 뽑기</button>
    <button class="btn btn-r" id="btnReset">🔄 초기화</button>
  </div>

  <div class="sample-box">
    <div class="sb-title">
      <span>📦 가장 최근 표본 (X = 성공 횟수)</span>
      <span class="phat-line">p̂ = <span id="curPhat">--</span></span>
    </div>
    <div class="sb-grid" id="curSample">
      <div class="sb-empty">아직 뽑지 않았어요. ‘표본 1개 뽑기’ 를 눌러보세요!</div>
    </div>
  </div>
</div>

<!-- 분포 -->
<div class="panel">
  <h2>📈 표본비율 p̂ 의 분포
       <span class="badge">노란 곡선 = 이론 정규분포 N(p, pq/n)</span></h2>

  <div class="dist-wrap">
    <div class="dist-title">
      <span>가로축: p̂ 값 · 세로축: 상대도수</span>
      <span>누적 표본 <span class="cnt" id="histCnt">0</span>개</span>
    </div>
    <canvas id="distCanvas" width="900" height="280"></canvas>
    <div class="dist-legend">
      <span class="dlg-bar"><i></i> 시뮬레이션 히스토그램</span>
      <span class="dlg-curve"><i></i> 이론 곡선 N(p, pq/n)</span>
      <span class="dlg-p"><i></i> 모비율 p</span>
    </div>
  </div>

  <div class="stats">
    <div class="s-card s-mean">
      <div class="s-head">E(p̂) — 평균</div>
      <div class="s-val" id="ExpE">--</div>
      <div class="s-sub">이론값 <b class="th">p = <span id="theE">--</span></b></div>
      <div class="s-bar-track"><div class="s-bar-fill" id="barE" style="width:0%"></div></div>
    </div>
    <div class="s-card s-var">
      <div class="s-head">V(p̂) — 분산</div>
      <div class="s-val" id="ExpV">--</div>
      <div class="s-sub">이론값 <b class="th">pq/n = <span id="theV">--</span></b></div>
      <div class="s-bar-track"><div class="s-bar-fill" id="barV" style="width:0%"></div></div>
    </div>
    <div class="s-card s-sd">
      <div class="s-head">σ(p̂) — 표준편차</div>
      <div class="s-val" id="ExpS">--</div>
      <div class="s-sub">이론값 <b class="th">√(pq/n) = <span id="theS">--</span></b></div>
      <div class="s-bar-track"><div class="s-bar-fill" id="barS" style="width:0%"></div></div>
    </div>
  </div>

  <div class="insight">
    <span class="ico">💡</span>
    <span>
      n이 <b>충분히 크면</b> p̂의 분포는 <span class="ok">정규분포 N(p, pq/n)</span>에 가까워져요.<br>
      표본을 더 많이 뽑을수록 <b>E(p̂) ≈ p</b> 그리고
      <b>σ(p̂) ≈ √(pq/n)</b> 에 수렴합니다.
    </span>
  </div>
</div>

<script>
/* ============ 설정 ============ */
const P = __P_VALUE__;          // 모비율
const SUCC_LABEL = "__SUCC_LABEL__";
const ACC = "__ACC__";
const SUCC_COLOR_A = "__SUCC_A__";
const SUCC_COLOR_B = "__SUCC_B__";

/* ============ 상태 ============ */
let n = 50;
let phats = [];   // 누적 p̂

/* ============ 유틸 ============ */
const $ = id => document.getElementById(id);
function fmt(v, d=4){ return (isFinite(v)? Number(v.toFixed(d)) : '--'); }
function fmtPct(v){ return (v*100).toFixed(1)+'%'; }

function bernoulli(){ return Math.random() < P ? 1 : 0; }

function drawSampleOnce(nn){
  let x = 0;
  const cells = new Array(nn);
  for(let i=0;i<nn;i++){
    const b = bernoulli();
    x += b;
    cells[i] = b;
  }
  return {cells, x, phat: x/nn};
}

function bulkDraw(times){
  // 단순 누적용 — 화면 표시 없음
  for(let i=0;i<times;i++){
    let x = 0;
    for(let j=0;j<n;j++) x += bernoulli();
    phats.push(x/n);
  }
}

function expStats(){
  if(phats.length===0) return {m:NaN, v:NaN, s:NaN};
  const m = phats.reduce((a,b)=>a+b,0)/phats.length;
  const v = phats.reduce((a,b)=>a+(b-m)*(b-m),0)/phats.length;
  return {m, v, s:Math.sqrt(v)};
}

/* ============ 모집단 비율 막대 ============ */
function renderPopBar(){
  $('barSucc').style.width = (P*100)+'%';
  $('barFail').style.width = ((1-P)*100)+'%';
  $('barSucc').textContent = (P*100>=10)? Math.round(P*100)+'%' : '';
  $('barFail').textContent = ((1-P)*100>=10)? Math.round((1-P)*100)+'%' : '';
  $('psP').textContent  = P.toFixed(2);
  $('psQ').textContent  = (1-P).toFixed(2);
  $('psPQ').textContent = (P*(1-P)).toFixed(4);
}

/* ============ 최근 표본 시각화 ============ */
function renderSample(s){
  const wrap = $('curSample');
  wrap.innerHTML = '';
  // 너무 많을 때는 일부만 표시
  const maxShow = 200;
  const showN = Math.min(s.cells.length, maxShow);
  for(let i=0;i<showN;i++){
    const c = document.createElement('div');
    c.className = 'sb-cell ' + (s.cells[i]===1 ? 'succ' : 'fail');
    c.textContent = s.cells[i]===1 ? '✓' : '·';
    c.style.animationDelay = Math.min(i*4, 600)+'ms';
    wrap.appendChild(c);
  }
  if(s.cells.length > maxShow){
    const more = document.createElement('div');
    more.style.cssText = 'color:#cbd5e1;font-size:.92rem;font-weight:700;padding:0 8px;align-self:center';
    more.textContent = '… 외 ' + (s.cells.length-maxShow) + '개';
    wrap.appendChild(more);
  }
  $('curPhat').textContent =
      s.x + '/' + s.cells.length + ' = ' + s.phat.toFixed(3);
}

/* ============ 히스토그램 + 정규곡선 ============ */
function pdfNormal(x, mu, sigma){
  if(sigma<=0) return 0;
  const z = (x-mu)/sigma;
  return Math.exp(-0.5*z*z) / (sigma*Math.sqrt(2*Math.PI));
}

function drawHist(){
  const cv = $('distCanvas');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL=46, padR=18, padT=18, padB=42;
  const plotW=W-padL-padR, plotH=H-padT-padB;

  // x 범위: [0, 1]
  const xLo = 0, xHi = 1;
  const X = v => padL + (v-xLo)/(xHi-xLo) * plotW;

  // 격자
  ctx.strokeStyle='rgba(148,163,184,.13)';
  ctx.lineWidth=1;
  ctx.setLineDash([3,3]);
  for(let i=1;i<=4;i++){
    const y = padT + (i/5)*plotH;
    ctx.beginPath();
    ctx.moveTo(padL,y); ctx.lineTo(W-padR,y);
    ctx.stroke();
  }
  ctx.setLineDash([]);

  // 축
  ctx.strokeStyle='rgba(148,163,184,.55)';
  ctx.lineWidth=1.2;
  ctx.beginPath();
  ctx.moveTo(padL, H-padB); ctx.lineTo(W-padR, H-padB);
  ctx.moveTo(padL, padT); ctx.lineTo(padL, H-padB);
  ctx.stroke();

  // x눈금 (0, 0.25, 0.5, 0.75, 1)
  ctx.fillStyle='#94a3b8';
  ctx.font='12px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  [0,0.25,0.5,0.75,1].forEach(v=>{
    const x = X(v);
    ctx.beginPath();
    ctx.strokeStyle='rgba(148,163,184,.55)';
    ctx.moveTo(x, H-padB); ctx.lineTo(x, H-padB+4);
    ctx.stroke();
    ctx.fillStyle='#94a3b8';
    ctx.fillText(v.toFixed(2), x, H-padB+6);
  });

  // x축 라벨
  ctx.fillStyle='#cbd5e1';
  ctx.font='bold 13px sans-serif';
  ctx.fillText('p̂  (표본비율)', (padL+W-padR)/2, H-18);

  // 막대 개수: 표본 수와 n에 따라 적응적
  const sigmaT = Math.sqrt(P*(1-P)/n);
  let nBins = 40;
  if(n<=20) nBins = 21;          // n이 작으면 가능한 p̂ 값이 적음
  else if(n<=50) nBins = 30;
  const binW = (xHi-xLo)/nBins;
  const bins = new Array(nBins).fill(0);
  phats.forEach(p=>{
    let k = Math.floor((p-xLo)/binW);
    if(k<0) k=0; if(k>=nBins) k=nBins-1;
    bins[k]++;
  });

  // y스케일: 막대 상대도수와 정규 PDF 모두 고려
  const total = phats.length;
  // 정규곡선 max
  let curveMax = 0;
  if(sigmaT>0){
    for(let i=0;i<=200;i++){
      const x = xLo + (i/200)*(xHi-xLo);
      curveMax = Math.max(curveMax, pdfNormal(x, P, sigmaT));
    }
  }
  // 히스토그램(밀도) max — bin당 빈도/총개수/binW
  let histMax = 0;
  if(total>0){
    bins.forEach(c=>{
      const d = (c/total)/binW;
      if(d>histMax) histMax = d;
    });
  }
  const yMax = Math.max(curveMax*1.1, histMax*1.1, 0.5);
  const Y = v => padT+plotH - (v/yMax)*plotH;

  // y눈금
  ctx.fillStyle='#94a3b8';
  ctx.font='11px sans-serif';
  ctx.textAlign='right'; ctx.textBaseline='middle';
  for(let i=0;i<=5;i++){
    const v = (yMax)*(i/5);
    const y = Y(v);
    ctx.fillText(v.toFixed(1), padL-5, y);
  }

  // 히스토그램
  if(total>0){
    for(let i=0;i<nBins;i++){
      const c = bins[i];
      if(c===0) continue;
      const density = (c/total)/binW;
      const x0 = X(xLo + i*binW), x1 = X(xLo + (i+1)*binW);
      const y0 = Y(density), y1 = Y(0);
      const grad = ctx.createLinearGradient(0,y0,0,y1);
      grad.addColorStop(0, ACC);
      grad.addColorStop(1, 'rgba(99,102,241,.4)');
      ctx.fillStyle = grad;
      ctx.fillRect(x0+0.6, y0, (x1-x0)-1.2, y1-y0);
      ctx.strokeStyle = ACC;
      ctx.lineWidth = 1;
      ctx.strokeRect(x0+0.6, y0, (x1-x0)-1.2, y1-y0);
    }
  }

  // 정규곡선
  if(sigmaT>0){
    ctx.strokeStyle = '#fde047';
    ctx.lineWidth = 3;
    ctx.beginPath();
    const STEPS = 240;
    for(let i=0;i<=STEPS;i++){
      const x = xLo + (i/STEPS)*(xHi-xLo);
      const y = pdfNormal(x, P, sigmaT);
      const cx = X(x), cy = Y(y);
      if(i===0) ctx.moveTo(cx, cy);
      else ctx.lineTo(cx, cy);
    }
    ctx.stroke();

    // p에서 점 표시
    ctx.fillStyle = '#fde047';
    ctx.beginPath();
    ctx.arc(X(P), Y(pdfNormal(P, P, sigmaT)), 5, 0, Math.PI*2);
    ctx.fill();
  }

  // 모비율 p 세로 점선
  ctx.strokeStyle='#fb7185';
  ctx.lineWidth=2.3;
  ctx.setLineDash([6,4]);
  ctx.beginPath();
  ctx.moveTo(X(P), padT); ctx.lineTo(X(P), H-padB);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#fb7185';
  ctx.font='bold 13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='bottom';
  ctx.fillText('p = '+P.toFixed(2), X(P), padT-1);

  // 경험 평균 세로선 (있을 때)
  if(total>0){
    const s = expStats();
    ctx.strokeStyle='#22d3ee';
    ctx.lineWidth=2;
    ctx.beginPath();
    ctx.moveTo(X(s.m), padT+14); ctx.lineTo(X(s.m), H-padB);
    ctx.stroke();
    ctx.fillStyle='#22d3ee';
    ctx.font='bold 12px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='top';
    ctx.fillText('p̂평균≈'+s.m.toFixed(3), X(s.m), padT+14);
  }
}

/* ============ 통계 카드 ============ */
function updateStatsUI(){
  const s = expStats();
  const tE = P;
  const tV = P*(1-P)/n;
  const tS = Math.sqrt(tV);

  $('ExpE').textContent = isNaN(s.m) ? '--' : s.m.toFixed(4);
  $('ExpV').textContent = isNaN(s.v) ? '--' : s.v.toFixed(5);
  $('ExpS').textContent = isNaN(s.s) ? '--' : s.s.toFixed(4);

  $('theE').textContent = tE.toFixed(4);
  $('theV').textContent = tV.toFixed(5);
  $('theS').textContent = tS.toFixed(4);

  // 0~1 비율 막대 (이론값 대비 경험값이 얼마나 가까운지)
  function ratio(exp, the){
    if(phats.length===0 || the===0) return 0;
    const r = Math.min(exp,the)/Math.max(exp,the);
    return Math.max(0, Math.min(1, r));
  }
  $('barE').style.width = (ratio(s.m, tE)*100).toFixed(1)+'%';
  $('barV').style.width = (ratio(s.v, tV)*100).toFixed(1)+'%';
  $('barS').style.width = (ratio(s.s, tS)*100).toFixed(1)+'%';

  $('histCnt').textContent = phats.length;
}

/* ============ 액션 ============ */
function actDraw1(){
  const s = drawSampleOnce(n);
  phats.push(s.phat);
  renderSample(s);
  drawHist();
  updateStatsUI();
}

function actDraw(times){
  // 마지막 표본만 화면 표시
  let last = null;
  let i = 0;
  const burst = 40;
  const step = ()=>{
    const end = Math.min(i+burst, times);
    for(; i<end; i++){
      const s = drawSampleOnce(n);
      phats.push(s.phat);
      if(i===times-1) last = s;
    }
    drawHist(); updateStatsUI();
    if(i<times) requestAnimationFrame(step);
    else if(last) renderSample(last);
  };
  step();
}

function actReset(){
  phats = [];
  $('curSample').innerHTML = '<div class="sb-empty">초기화되었어요. 다시 표본을 뽑아보세요!</div>';
  $('curPhat').textContent = '--';
  drawHist();
  updateStatsUI();
}

/* ============ 초기화 ============ */
function init(){
  renderPopBar();
  drawHist();
  updateStatsUI();

  $('nRange').addEventListener('input', e=>{
    n = parseInt(e.target.value);
    $('nVal').textContent = n;
    // n이 바뀌면 누적된 p̂은 다른 분포의 결과이므로 초기화
    phats = [];
    $('curSample').innerHTML = '<div class="sb-empty">표본 크기 n이 변경되어 초기화되었어요!</div>';
    $('curPhat').textContent = '--';
    drawHist();
    updateStatsUI();
  });
  $('btnDraw1').addEventListener('click', actDraw1);
  $('btnDraw50').addEventListener('click', ()=>actDraw(50));
  $('btnDraw500').addEventListener('click', ()=>actDraw(500));
  $('btnReset').addEventListener('click', actReset);

  window.addEventListener('resize', drawHist);
}
init();
</script>
</body>
</html>
"""


def _make_html(*, title, scn_text, p, p_disp, pop_emo, pop_name,
               succ_label, fail_label, succ_a, succ_b,
               bg_mid, hdr_a, hdr_b, hdr_border, hdr_txt, acc, acc_dim):
    return (_HTML_TEMPLATE
        .replace("__TITLE__", title)
        .replace("__SCN_TEXT__", scn_text)
        .replace("__P_VALUE__", str(p))
        .replace("__P_DISP__", p_disp)
        .replace("__POP_EMO__", pop_emo)
        .replace("__POP_NAME__", pop_name)
        .replace("__SUCC_LABEL__", succ_label)
        .replace("__FAIL_LABEL__", fail_label)
        .replace("__SUCC_A__", succ_a)
        .replace("__SUCC_B__", succ_b)
        .replace("__BG_MID__", bg_mid)
        .replace("__HDR_A__", hdr_a)
        .replace("__HDR_B__", hdr_b)
        .replace("__HDR_BORDER__", hdr_border)
        .replace("__HDR_TXT__", hdr_txt)
        .replace("__ACC__", acc)
        .replace("__ACC_DIM__", acc_dim)
    )


# ─────────────────────────────────────────────────────────────────────────────
# 4가지 실생활 시나리오
# ─────────────────────────────────────────────────────────────────────────────
_HTML_COIN = _make_html(
    title="🪙 동전 던지기 — 앞면이 나올 비율",
    scn_text="<b>균형 잡힌 동전</b>을 n번 던졌을 때 앞면(H)이 나온 비율 p̂ 의 분포를 관찰해요.",
    p=0.5, p_disp="0.5  (앞면)",
    pop_emo="🪙", pop_name="동전 1개",
    succ_label="앞면 H", fail_label="뒷면 T",
    succ_a="#fbbf24", succ_b="#f59e0b",
    bg_mid="#3f2e0e",
    hdr_a="rgba(251,191,36,.22)", hdr_b="rgba(250,204,21,.16)",
    hdr_border="rgba(251,191,36,.55)", hdr_txt="#fde047",
    acc="#fbbf24", acc_dim="rgba(251,191,36,.45)",
)

_HTML_FREE = _make_html(
    title="🏀 자유투 — 슛 성공 비율",
    scn_text="자유투 성공률이 <b>70%</b>인 농구 선수가 n번 던졌을 때 성공 비율 p̂ 의 분포를 관찰해요.",
    p=0.7, p_disp="0.7  (슛 성공)",
    pop_emo="🏀", pop_name="자유투 1회",
    succ_label="성공 🎯", fail_label="실패 ✗",
    succ_a="#fb923c", succ_b="#ea580c",
    bg_mid="#3a1607",
    hdr_a="rgba(249,115,22,.22)", hdr_b="rgba(251,146,60,.16)",
    hdr_border="rgba(249,115,22,.55)", hdr_txt="#fdba74",
    acc="#fb923c", acc_dim="rgba(249,115,22,.45)",
)

_HTML_BREAD = _make_html(
    title="🍞 학교 매점 — 단팥빵을 고른 학생 비율",
    scn_text="학생 중 <b>40%</b>가 매점에서 단팥빵을 고를 때, 표본 n명에서 단팥빵 선택 비율 p̂의 분포를 관찰해요.",
    p=0.4, p_disp="0.4  (단팥빵 선택)",
    pop_emo="🍞", pop_name="매점 방문 학생 1명",
    succ_label="단팥빵 🥖", fail_label="다른 빵",
    succ_a="#f472b6", succ_b="#db2777",
    bg_mid="#3f0c2a",
    hdr_a="rgba(236,72,153,.22)", hdr_b="rgba(244,114,182,.16)",
    hdr_border="rgba(236,72,153,.55)", hdr_txt="#f9a8d4",
    acc="#f472b6", acc_dim="rgba(236,72,153,.45)",
)

_HTML_AD = _make_html(
    title="📱 SNS 광고 — 클릭한 사용자 비율",
    scn_text="SNS 광고 클릭률이 <b>15%</b>일 때, 표본 n명에서 광고를 클릭한 비율 p̂의 분포를 관찰해요.",
    p=0.15, p_disp="0.15  (광고 클릭)",
    pop_emo="📱", pop_name="광고에 노출된 사용자 1명",
    succ_label="클릭 👆", fail_label="무시",
    succ_a="#22d3ee", succ_b="#0891b2",
    bg_mid="#062c33",
    hdr_a="rgba(34,211,238,.22)", hdr_b="rgba(56,189,248,.16)",
    hdr_border="rgba(34,211,238,.55)", hdr_txt="#67e8f9",
    acc="#22d3ee", acc_dim="rgba(34,211,238,.45)",
)


# ─────────────────────────────────────────────────────────────────────────────
# render()
# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.subheader("🎯 표본비율 p̂의 분포 — 실생활 시뮬레이션")
    st.caption(
        "동전·자유투·매점 단팥빵·SNS 광고 4가지 실생활 사례에서 표본 n명을 반복 추출해 "
        "**p̂ = X/n**의 분포가 **N(p, pq/n)** 정규분포에 가까워지는 모습을 직접 확인해 봐요!"
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "🪙 동전 (p=0.5)",
        "🏀 자유투 (p=0.7)",
        "🍞 단팥빵 (p=0.4)",
        "📱 광고 클릭 (p=0.15)",
    ])

    with tab1:
        components.html(_HTML_COIN, height=1600, scrolling=True)
    with tab2:
        components.html(_HTML_FREE, height=1600, scrolling=True)
    with tab3:
        components.html(_HTML_BREAD, height=1600, scrolling=True)
    with tab4:
        components.html(_HTML_AD, height=1600, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
