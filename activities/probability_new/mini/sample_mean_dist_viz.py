# activities/probability_new/mini/sample_mean_dist_viz.py
"""
표본평균 X̄의 분포 — 시각적 탐구 미니활동
- 모집단에서 크기 n의 표본을 임의(복원)추출했을 때 X̄이 가질 수 있는
  **모든 값**과 그 확률을 다항식 합성곱으로 정확히 계산해 막대그래프로 보여줌
- 모집단 미리보기 / 표본 예시 5개 / X̄의 분포표 / 모집단 vs X̄ 통계 비교
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "📊 미니: 표본평균 X̄의 분포 탐험",
    "description": "모집단을 직접 만들고 표본 크기 n을 바꾸며, X̄이 가질 수 있는 모든 값과 그 확률을 막대그래프로 살펴봅니다.",
    "order": 8,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "표본평균분포탐험"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 표본평균 X̄의 분포**"},
    {
        "key": "분포_모양",
        "label": "표본 크기 **n=1**일 때와 **n=5**, **n=10**일 때 X̄의 분포 막대그래프 모양은 어떻게 달랐나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "n=1일 때는 ___ 모양이었고, n이 커질수록 ___ 모양으로 ...",
    },
    {
        "key": "가운데_쏠림",
        "label": "n을 크게 할수록 X̄의 분포에서 막대들이 **어느 값 주위에 모이는지** 관찰한 점을 적어보세요. 그 값은 모평균과 어떤 관계인가요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "n이 커질수록 X̄의 분포가 ___ 값 근처로 ___ 졌다. 그 값은 모평균 m과 ...",
    },
    {
        "key": "퍼짐_변화",
        "label": "분포의 **퍼짐(분산·표준편차)**은 n이 커질 때 어떻게 변했나요? 공식 V(X̄)=σ²/n 과 어떻게 연결되나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "n이 커질수록 X̄의 분포는 점점 ___ 모여서 분산이 ___ 졌다. 이는 V(X̄)=σ²/n에서 ...",
    },
    {
        "key": "가능한_값의_개수",
        "label": "모집단이 4개 값일 때, **n=2이면 가능한 X̄ 값은 몇 가지**였고, **n=3이면 몇 가지**였나요? 왜 그렇게 늘어났을까요?",
        "type": "text_area",
        "height": 100,
        "placeholder": "n=2일 때는 ___ 가지, n=3일 때는 ___ 가지. n이 커지면 합으로 만들 수 있는 값이 ...",
    },
    {
        "key": "확률_가장_큰_값",
        "label": "분포에서 **확률이 가장 큰 X̄ 값**은 어디였나요? 왜 그 값이 가장 자주 나타날까요?",
        "type": "text_area",
        "height": 100,
        "placeholder": "확률이 가장 큰 X̄ 값은 ___ 였다. 왜냐하면 그 값을 만들 수 있는 표본의 조합이 ...",
    },
    {
        "key": "정규분포_느낌",
        "label": "n을 크게 했을 때 X̄의 분포가 닮아가는 **종 모양 곡선**이 있다면 무엇일까요? (생각나는 이름을 적어보세요)",
        "type": "text_area",
        "height": 90,
        "placeholder": "n이 커질수록 X̄의 분포는 ___ 곡선을 닮아갔다. 이를 ___ 라고 부르는 것 같다.",
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
# HTML — 표본평균 X̄의 분포 탐험
# ─────────────────────────────────────────────────────────────────────────────
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
  background:linear-gradient(135deg,rgba(56,189,248,.18),rgba(168,85,247,.18));
  border:2px solid rgba(56,189,248,.45);border-radius:18px;
  padding:14px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.5rem;font-weight:900;color:#7dd3fc;margin-bottom:4px;letter-spacing:.3px}
.hdr p{font-size:1.02rem;color:#cbd5e1;line-height:1.55}
.hdr b{color:#fde047}
.xb{
  display:inline-block;position:relative;
  padding:2px 2px 0 2px;line-height:1;font-weight:900;
}
.xb::before{
  content:'';position:absolute;left:1px;right:1px;top:0;
  height:2px;background:currentColor;border-radius:1px;
}

/* ============ 패널 ============ */
.panel{
  background:rgba(15,23,42,.72);border:1.5px solid rgba(99,102,241,.3);
  border-radius:14px;padding:14px;margin-bottom:12px;
}
.panel h2{
  font-size:1.15rem;font-weight:900;color:#a5b4fc;margin-bottom:11px;
  display:flex;align-items:center;gap:8px;letter-spacing:.3px;
}
.panel h2 .badge{
  font-size:.78rem;color:#cbd5e1;background:rgba(99,102,241,.18);
  padding:2px 8px;border-radius:999px;font-weight:700;
}

/* ============ 모집단 프리셋 ============ */
.preset-row{
  display:flex;flex-wrap:wrap;gap:7px;margin-bottom:10px;
}
.preset{
  padding:7px 13px;border-radius:999px;font-size:.95rem;font-weight:800;
  border:2px solid transparent;cursor:pointer;color:#fff;
  background:linear-gradient(135deg,#475569,#334155);
  transition:all .14s ease;
}
.preset:hover{transform:translateY(-1px)}
.preset.active{
  background:linear-gradient(135deg,#3b82f6,#1d4ed8);
  border-color:#7dd3fc;box-shadow:0 4px 12px rgba(59,130,246,.45);
}

/* ============ 모집단 편집기 ============ */
.pop-edit{
  background:rgba(56,189,248,.06);border:1.5px solid rgba(56,189,248,.3);
  border-radius:11px;padding:11px;margin-bottom:10px;
}
.pop-edit-row{
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:9px;
}
.pop-edit-lab{
  font-size:1rem;font-weight:800;color:#7dd3fc;min-width:120px;
}
.pop-edit-range{flex:1;min-width:140px;accent-color:#38bdf8;height:6px}
.pop-edit-val{
  font-size:1.4rem;font-weight:900;color:#fde047;min-width:48px;
  background:rgba(15,23,42,.7);padding:2px 12px;border-radius:8px;text-align:center;
}
.val-inputs{
  display:flex;flex-wrap:wrap;gap:7px;align-items:center;
}
.val-inputs label{
  display:flex;align-items:center;gap:5px;
  background:rgba(15,23,42,.6);border:1.5px solid rgba(99,102,241,.3);
  border-radius:9px;padding:4px 8px;font-size:.92rem;color:#cbd5e1;font-weight:700;
}
.val-inputs input{
  width:54px;background:transparent;border:none;color:#fde047;
  font-size:1.08rem;font-weight:900;text-align:center;outline:none;
}
.val-inputs input:focus{color:#fef3c7}

/* ============ 모집단 시각화 (가방) ============ */
.basket-wrap{
  display:grid;grid-template-columns:1fr 250px;gap:12px;
}
@media(max-width:780px){.basket-wrap{grid-template-columns:1fr}}

.basket{
  position:relative;height:200px;
  background:radial-gradient(ellipse 60% 70% at center 60%,rgba(217,119,6,.22),rgba(15,23,42,.95));
  border:3px solid rgba(217,119,6,.55);border-radius:80px 80px 16px 16px / 100px 100px 16px 16px;
  overflow:hidden;
}
.basket::before{
  content:'';position:absolute;top:0;left:0;right:0;height:22px;
  background:linear-gradient(180deg,rgba(217,119,6,.6),rgba(180,83,9,.3));
  border-bottom:2px solid rgba(217,119,6,.6);
}
.basket-label{
  position:absolute;top:4px;left:50%;transform:translateX(-50%);
  font-size:.85rem;color:#fbbf24;font-weight:800;letter-spacing:.4px;z-index:3;
}
.ball{
  position:absolute;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-weight:900;color:#1f2937;
  background:radial-gradient(circle at 30% 30%,#fef3c7,#f59e0b);
  border:3px solid #fbbf24;
  box-shadow:0 4px 10px rgba(251,191,36,.45),inset 0 -4px 8px rgba(0,0,0,.15);
  transition:all .35s cubic-bezier(.34,1.56,.64,1);
}
.ball.pick{
  transform:scale(1.18);
  background:radial-gradient(circle at 30% 30%,#fecaca,#dc2626);
  border-color:#fca5a5;color:#fff;
  box-shadow:0 0 0 4px #f43f5e,0 6px 20px rgba(244,63,94,.6);
  z-index:5;
}

.pop-stats{
  display:flex;flex-direction:column;gap:7px;
  background:rgba(168,85,247,.08);border:1.5px solid rgba(168,85,247,.4);
  border-radius:11px;padding:11px;
}
.pop-stats h3{
  font-size:.95rem;color:#c4b5fd;font-weight:900;
  text-align:center;letter-spacing:.3px;margin-bottom:3px;
}
.ps-row{
  display:flex;justify-content:space-between;align-items:center;
  font-size:1rem;font-weight:700;color:#ddd6fe;padding:2px 4px;
}
.ps-row .v{color:#fef3c7;font-weight:900;font-size:1.1rem;background:rgba(15,23,42,.55);padding:2px 9px;border-radius:7px}

/* ============ 표본 크기 슬라이더 ============ */
.n-row{
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  background:rgba(34,197,94,.07);border:1.5px solid rgba(34,197,94,.35);
  border-radius:11px;padding:11px;margin-bottom:10px;
}
.n-lab{font-size:1.02rem;font-weight:800;color:#86efac;min-width:108px}
.n-range{flex:1;min-width:140px;accent-color:#22c55e;height:6px}
.n-val{
  font-size:1.55rem;font-weight:900;color:#fde047;min-width:54px;
  background:rgba(15,23,42,.7);padding:2px 14px;border-radius:8px;text-align:center;
}

/* ============ 예시 표본 ============ */
.ex-head{
  display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:7px;
  margin-bottom:8px;
}
.ex-title{font-size:1rem;color:#cbd5e1;font-weight:700}
.btn{
  padding:9px 14px;border:none;border-radius:11px;
  font-size:.97rem;font-weight:900;color:#fff;cursor:pointer;
  transition:all .15s ease;letter-spacing:.3px;
}
.btn:active{transform:scale(.96)}
.btn-pri{background:linear-gradient(135deg,#22c55e,#15803d);box-shadow:0 3px 10px rgba(34,197,94,.4)}
.btn-pri:hover{background:linear-gradient(135deg,#16a34a,#14532d);transform:translateY(-1px)}

.ex-list{
  display:flex;flex-direction:column;gap:7px;
}
.ex-item{
  display:grid;grid-template-columns:30px 1fr 130px;align-items:center;gap:9px;
  background:rgba(30,41,59,.6);border:1.5px solid rgba(99,102,241,.22);
  border-radius:11px;padding:8px 11px;
}
.ex-idx{
  font-size:.95rem;font-weight:900;color:#a5b4fc;
  background:rgba(99,102,241,.18);width:28px;height:28px;
  border-radius:8px;display:flex;align-items:center;justify-content:center;
}
.ex-chips{display:flex;flex-wrap:wrap;gap:5px}
.ex-chip{
  display:inline-flex;align-items:center;justify-content:center;
  width:34px;height:34px;border-radius:50%;
  background:radial-gradient(circle at 30% 30%,#fef3c7,#f59e0b);
  color:#1f2937;font-weight:900;font-size:.98rem;
  border:2px solid #fbbf24;
  box-shadow:0 2px 6px rgba(251,191,36,.35);
  animation:popIn .3s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes popIn{from{opacity:0;transform:scale(.3) rotate(-15deg)}to{opacity:1;transform:scale(1) rotate(0)}}
.ex-xbar{
  text-align:right;font-size:.98rem;color:#fde047;font-weight:900;
  background:rgba(15,23,42,.6);border:1.5px solid rgba(251,191,36,.35);
  border-radius:8px;padding:4px 9px;letter-spacing:.3px;
}
.ex-xbar .sm{font-size:.82rem;color:#94a3b8;font-weight:700;display:block;margin-bottom:1px}

/* ============ 분포 차트 ============ */
.dist-info{
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;
  font-size:.95rem;color:#cbd5e1;font-weight:700;margin-bottom:8px;
}
.dist-info .v{color:#fde047;font-weight:900}
.dist-info span b{color:#7dd3fc;font-weight:900}
.chart-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(56,189,248,.3);
  border-radius:12px;padding:12px;
}
#distChart{
  display:block;width:100%;height:340px;
  background:rgba(15,23,42,.5);border-radius:8px;
}

.dist-legend{
  display:flex;flex-wrap:wrap;gap:13px;justify-content:center;
  font-size:.9rem;color:#cbd5e1;font-weight:700;margin-top:8px;
}
.lg{display:flex;align-items:center;gap:5px}
.lg .swatch{display:inline-block;width:18px;height:8px;border-radius:2px}

/* ============ 분포표 ============ */
.dist-table-wrap{
  margin-top:11px;max-height:230px;overflow:auto;
  border-radius:9px;background:rgba(15,23,42,.55);
  border:1.5px solid rgba(56,189,248,.25);
}
table.dtab{
  width:100%;border-collapse:collapse;font-size:1rem;color:#e2e8f0;text-align:center;
  min-width:520px;
}
table.dtab thead th{
  position:sticky;top:0;z-index:2;
  background:rgba(56,189,248,.22);color:#bae6fd;font-weight:900;
  padding:8px 8px;border-bottom:2px solid rgba(56,189,248,.5);
  font-size:1rem;
}
table.dtab tbody td{
  padding:6px 8px;border-bottom:1px solid rgba(56,189,248,.12);
}
table.dtab tbody tr:nth-child(odd){background:rgba(30,41,59,.4)}
table.dtab tbody tr:hover{background:rgba(56,189,248,.16)}
table.dtab td.xb-cell{color:#fde047;font-weight:900}
table.dtab td.p-cell{color:#86efac;font-weight:800}
table.dtab td.frac-cell{color:#cbd5e1;font-weight:700;font-size:.95rem}

/* ============ 통계 비교 ============ */
.cmp-grid{
  display:grid;grid-template-columns:1fr 1fr;gap:11px;
}
@media(max-width:680px){.cmp-grid{grid-template-columns:1fr}}
.cmp-card{
  background:rgba(30,41,59,.7);border-radius:13px;padding:13px;
  border:2px solid rgba(99,102,241,.3);
}
.cmp-pop{border-color:rgba(251,191,36,.5);background:rgba(251,191,36,.07)}
.cmp-xb {border-color:rgba(244,63,94,.5);background:rgba(244,63,94,.07)}

.cmp-head{
  font-size:1.05rem;font-weight:900;margin-bottom:10px;letter-spacing:.3px;
  display:flex;align-items:center;gap:7px;
}
.cmp-pop .cmp-head{color:#fbbf24}
.cmp-xb  .cmp-head{color:#fb7185}

.cmp-row{
  display:grid;grid-template-columns:auto 1fr;gap:9px;align-items:center;
  background:rgba(15,23,42,.55);border-radius:9px;padding:9px 11px;margin-bottom:7px;
}
.cmp-formula{
  font-size:1.05rem;font-weight:800;color:#cbd5e1;letter-spacing:.3px;
  white-space:nowrap;
}
.cmp-formula .frac{display:inline-block;vertical-align:middle;text-align:center;font-size:.92em;margin:0 2px}
.cmp-formula .frac .num{display:block;border-bottom:1.5px solid #cbd5e1;padding:0 4px;line-height:1.1}
.cmp-formula .frac .den{display:block;padding:0 4px;line-height:1.1}
.cmp-val{
  font-size:1.4rem;font-weight:900;color:#fef3c7;text-align:right;letter-spacing:.5px;
}

/* ============ 인사이트 박스 ============ */
.insight{
  background:rgba(251,191,36,.1);border:2px solid rgba(251,191,36,.45);
  border-radius:13px;padding:12px 15px;margin-top:12px;
  font-size:1rem;color:#fef3c7;line-height:1.65;
  display:flex;align-items:flex-start;gap:10px;
}
.insight .ico{font-size:1.5rem;flex-shrink:0;line-height:1.3}
.insight b{color:#fde047}
.insight .xb{color:#fbbf24}

/* ============ 경고 박스 ============ */
.warn{
  background:rgba(244,63,94,.12);border:1.5px solid rgba(244,63,94,.4);
  border-radius:10px;padding:9px 12px;margin-top:9px;
  font-size:.92rem;color:#fecaca;line-height:1.5;display:none;
}
.warn.show{display:block}
</style>
</head>
<body>

<div class="hdr">
  <h1>📊 표본평균 <span class="xb">X</span>의 분포 탐험</h1>
  <p>모집단에서 표본을 뽑으면 <span class="xb">X</span>이 가질 수 있는 값들과 그 확률을 <b>모든 경우</b>로부터 계산해 봅니다.</p>
</div>

<!-- ① 모집단 -->
<div class="panel">
  <h2>🎒 모집단 만들기 <span class="badge">프리셋을 고르거나 값을 직접 바꿔보세요</span></h2>

  <div class="preset-row" id="presetRow">
    <button class="preset active" data-preset="balls">🎒 공 {2, 4, 6, 8}</button>
    <button class="preset" data-preset="dice">🎲 주사위 {1, 2, 3, 4, 5, 6}</button>
    <button class="preset" data-preset="cards">🃏 카드 {1, 3, 5, 7, 9}</button>
    <button class="preset" data-preset="custom">✏️ 직접 입력</button>
  </div>

  <div class="pop-edit">
    <div class="pop-edit-row">
      <span class="pop-edit-lab">모집단 원소 수</span>
      <input type="range" min="2" max="8" value="4" class="pop-edit-range" id="mRange">
      <span class="pop-edit-val" id="mVal">4</span>
    </div>
    <div class="val-inputs" id="valInputs"></div>
  </div>

  <div class="basket-wrap">
    <div class="basket">
      <div class="basket-label">📦 모집단 (크기 N=<span id="popSize">4</span>)</div>
    </div>
    <div class="pop-stats">
      <h3>📊 모집단의 통계량</h3>
      <div class="ps-row"><span>모평균 m</span><span class="v" id="popMean">--</span></div>
      <div class="ps-row"><span>모분산 σ²</span><span class="v" id="popVar">--</span></div>
      <div class="ps-row"><span>모표준편차 σ</span><span class="v" id="popSd">--</span></div>
    </div>
  </div>
</div>

<!-- ② 표본 크기 + 예시 -->
<div class="panel">
  <h2>🎯 표본 뽑기 <span class="badge">크기 n인 표본을 임의·복원추출합니다</span></h2>

  <div class="n-row">
    <span class="n-lab">표본 크기 n</span>
    <input type="range" min="1" max="10" value="2" class="n-range" id="nRange">
    <span class="n-val" id="nVal">2</span>
  </div>

  <div class="ex-head">
    <span class="ex-title">📦 예시 표본 5개와 각 표본평균</span>
    <button class="btn btn-pri" id="btnResample">🎲 다시 뽑기</button>
  </div>
  <div class="ex-list" id="exList"></div>
</div>

<!-- ③ X̄의 분포 -->
<div class="panel">
  <h2>📈 표본평균 <span class="xb">X</span>의 분포 — 가능한 모든 경우</h2>

  <div class="dist-info">
    <span>가능한 <span class="xb">X</span> 값: <span class="v" id="distCnt">--</span>가지</span>
    <span>전체 표본 경우의 수: <b id="totalCases">--</b>가지 (= N<sup>n</sup>)</span>
  </div>

  <div class="chart-wrap">
    <canvas id="distChart" width="800" height="340"></canvas>
    <div class="dist-legend">
      <span class="lg"><span class="swatch" style="background:linear-gradient(90deg,#38bdf8,#818cf8)"></span> P(<span class="xb">X</span> = 값)</span>
      <span class="lg"><span class="swatch" style="background:#fb7185"></span> 모평균 m</span>
      <span class="lg"><span class="swatch" style="background:#fde047"></span> E(<span class="xb">X</span>) = m</span>
    </div>
  </div>

  <div class="warn" id="warnBox"></div>

  <div class="dist-table-wrap">
    <table class="dtab" id="distTable">
      <thead>
        <tr><th>표본평균 <span class="xb">X</span></th><th>분수 형태</th><th>확률 P(<span class="xb">X</span>=x̄)</th></tr>
      </thead>
      <tbody></tbody>
    </table>
  </div>
</div>

<!-- ④ 비교 -->
<div class="panel">
  <h2>🔍 모집단 vs 표본평균 <span class="xb">X</span> — 비교</h2>
  <div class="cmp-grid">
    <div class="cmp-card cmp-pop">
      <div class="cmp-head">🎒 모집단 (원자료 X)</div>
      <div class="cmp-row">
        <span class="cmp-formula">μ = E(X)</span>
        <span class="cmp-val" id="cPopM">--</span>
      </div>
      <div class="cmp-row">
        <span class="cmp-formula">σ² = V(X)</span>
        <span class="cmp-val" id="cPopV">--</span>
      </div>
      <div class="cmp-row">
        <span class="cmp-formula">σ = √V(X)</span>
        <span class="cmp-val" id="cPopS">--</span>
      </div>
    </div>
    <div class="cmp-card cmp-xb">
      <div class="cmp-head">🌟 표본평균 <span class="xb">X</span></div>
      <div class="cmp-row">
        <span class="cmp-formula">E(<span class="xb">X</span>) = m</span>
        <span class="cmp-val" id="cXbM">--</span>
      </div>
      <div class="cmp-row">
        <span class="cmp-formula">V(<span class="xb">X</span>) = <span class="frac"><span class="num">σ²</span><span class="den">n</span></span></span>
        <span class="cmp-val" id="cXbV">--</span>
      </div>
      <div class="cmp-row">
        <span class="cmp-formula">σ(<span class="xb">X</span>) = <span class="frac"><span class="num">σ</span><span class="den">√n</span></span></span>
        <span class="cmp-val" id="cXbS">--</span>
      </div>
    </div>
  </div>

  <div class="insight">
    <span class="ico">💡</span>
    <span>
      n이 <b>커질수록</b> <span class="xb">X</span>의 분포는 모평균 m 주변에 <b>더 촘촘히</b> 모이고,
      분포 모양은 점점 <b>종 모양 곡선</b>(정규분포)에 가까워져요!
    </span>
  </div>
</div>

<script>
/* ====================== 상태 ====================== */
const PRESETS = {
  balls: [2, 4, 6, 8],
  dice:  [1, 2, 3, 4, 5, 6],
  cards: [1, 3, 5, 7, 9],
};
let pop = [...PRESETS.balls];   // 현재 모집단
let n = 2;                       // 표본 크기
let preset = 'balls';

const $ = id => document.getElementById(id);

/* ====================== Canvas — X 위에 가로선(X̄) 그리기 헬퍼 ======================
 * canvas에서 X+combining macron(U+0304)은 폰트에 따라 깨질 수 있어,
 * X 글자를 그린 뒤 그 위에 사각형으로 직접 가로선을 칠합니다.
 * parts: [{t:"문자열", bar:true|false}, ...]
 */
function fillTextParts(ctx, parts, x, y){
  let totalW = 0;
  parts.forEach(p => totalW += ctx.measureText(p.t).width);
  let cursor;
  const align = ctx.textAlign;
  if(align === 'center')      cursor = x - totalW/2;
  else if(align === 'right')  cursor = x - totalW;
  else                        cursor = x;
  const fm = (ctx.font.match(/(\d+(?:\.\d+)?)px/) || [0,'12'])[1];
  const fpx = parseFloat(fm);
  const oldAlign = ctx.textAlign;
  const oldBaseline = ctx.textBaseline;
  ctx.textAlign = 'left';
  parts.forEach(p => {
    const w = ctx.measureText(p.t).width;
    ctx.fillText(p.t, cursor, y);
    if(p.bar && w > 0){
      let top;
      if(oldBaseline === 'top')                  top = y - 1;
      else if(oldBaseline === 'middle')          top = y - fpx*0.55;
      else if(oldBaseline === 'bottom')          top = y - fpx*1.0 - 1;
      else                                       top = y - fpx*0.92;
      const barH = Math.max(1.5, fpx*0.09);
      const oldFill = ctx.fillStyle;
      ctx.fillRect(cursor+1, top, w-2, barH);
      ctx.fillStyle = oldFill;
    }
    cursor += w;
  });
  ctx.textAlign = oldAlign;
}
function fillXBar(ctx, x, y, prefix, suffix){
  const parts = [];
  if(prefix) parts.push({t: prefix, bar:false});
  parts.push({t: 'X', bar:true});
  if(suffix) parts.push({t: suffix, bar:false});
  fillTextParts(ctx, parts, x, y);
}

/* ====================== 다항식 합성곱 / 정확 PMF ====================== */
function gcd(a, b){ a=Math.abs(a); b=Math.abs(b); while(b){[a,b]=[b,a%b];} return a||1; }

function conv(a, b){
  const c = new Array(a.length + b.length - 1).fill(0);
  for(let i=0;i<a.length;i++){
    const ai = a[i]; if(!ai) continue;
    for(let j=0;j<b.length;j++) c[i+j] += ai * b[j];
  }
  return c;
}

function pmfSum(values, nn){
  /* 표본 합 S = X1+...+Xn 의 정확 분포: 단일 추출 pmf의 n중 합성곱 (power-by-square) */
  const m = values.length;
  let minv =  Infinity, maxv = -Infinity;
  values.forEach(v=>{ if(v<minv)minv=v; if(v>maxv)maxv=v; });
  const baseLen = maxv - minv + 1;
  const base = new Array(baseLen).fill(0);
  values.forEach(v => base[v - minv] += 1.0/m);

  let res = [1]; let shift = 0;
  let basePoly = base.slice(); let baseShift = minv;
  let k = nn;
  while(k > 0){
    if(k & 1){
      res = conv(res, basePoly);
      shift += baseShift;
    }
    if(k > 1){
      basePoly = conv(basePoly, basePoly);
      baseShift *= 2;
    }
    k >>= 1;
  }
  // 합 분포: sum=shift+i, prob=res[i]
  return {shift, probs: res};
}

/* X̄ = S/n 의 (값, 확률) 리스트 */
function pmfXbar(values, nn){
  const {shift, probs} = pmfSum(values, nn);
  const arr = [];
  for(let i=0;i<probs.length;i++){
    if(probs[i] > 1e-15){
      arr.push({sum: shift+i, xb: (shift+i)/nn, p: probs[i]});
    }
  }
  return arr;
}

/* ====================== 모집단 통계 ====================== */
function popStats(values){
  const m = values.reduce((a,b)=>a+b,0)/values.length;
  const v = values.reduce((s,x)=>s+(x-m)*(x-m),0)/values.length;
  return {mean:m, var:v, sd:Math.sqrt(v)};
}

function fmt(v, d=4){ if(isNaN(v)) return '--'; return Number(v.toFixed(d)).toString(); }
function isInt(v){ return Math.abs(v-Math.round(v))<1e-9; }
function fmtNum(v){ return isInt(v) ? Math.round(v)+'' : v.toFixed(3); }

/* ====================== 모집단 시각화 ====================== */
function drawBasket(){
  const wrap = document.querySelector('.basket');
  // 기존 ball 제거
  wrap.querySelectorAll('.ball').forEach(el=>el.remove());
  const N = pop.length;
  const W = wrap.clientWidth, H = wrap.clientHeight;
  const BSIZE = N <= 4 ? 56 : (N <= 6 ? 48 : 40);
  const PADX = 22, TOP_PAD = 36, BOT_PAD = 16;
  // 한 줄에 몇 개? 너비 기준
  const maxPerRow = Math.max(2, Math.floor((W - PADX*2 + 10) / (BSIZE + 8)));
  const perRow = Math.min(N, maxPerRow);
  const rows = Math.ceil(N / perRow);
  const usableH = H - TOP_PAD - BOT_PAD;
  const rowH = Math.min(BSIZE + 12, usableH / rows);
  for(let i=0;i<N;i++){
    const r = Math.floor(i / perRow), c = i % perRow;
    const colsInThisRow = (r === rows-1) ? (N - r*perRow) : perRow;
    const totalW = colsInThisRow*BSIZE + (colsInThisRow-1)*8;
    const startX = (W - totalW)/2;
    const x = startX + c*(BSIZE + 8);
    const y = TOP_PAD + r*rowH + (usableH/rows - BSIZE)/2;
    const el = document.createElement('div');
    el.className = 'ball';
    el.style.width = BSIZE+'px';
    el.style.height = BSIZE+'px';
    el.style.left = x+'px';
    el.style.top = y+'px';
    el.style.fontSize = (BSIZE*0.46)+'px';
    el.textContent = pop[i];
    el.dataset.idx = i;
    wrap.appendChild(el);
  }
  $('popSize').textContent = N;
}

function highlightBalls(idxList){
  const balls = document.querySelectorAll('.basket .ball');
  balls.forEach(b=>b.classList.remove('pick'));
  if(!idxList) return;
  // 중복 인덱스(복원추출)도 한 번씩 강조
  const set = new Set(idxList);
  balls.forEach(b=>{
    if(set.has(parseInt(b.dataset.idx))) b.classList.add('pick');
  });
}

/* ====================== 모집단 편집 UI ====================== */
function renderValInputs(){
  const wrap = $('valInputs');
  wrap.innerHTML = '';
  pop.forEach((v,i)=>{
    const lab = document.createElement('label');
    lab.innerHTML = `X<sub>${i+1}</sub>=<input type="number" data-i="${i}" value="${v}" step="1">`;
    wrap.appendChild(lab);
  });
  wrap.querySelectorAll('input').forEach(inp=>{
    inp.addEventListener('change', e=>{
      const idx = parseInt(e.target.dataset.i);
      let val = parseInt(e.target.value);
      if(isNaN(val)) val = 0;
      // 범위 제한
      if(val < -99) val = -99;
      if(val > 99)  val = 99;
      e.target.value = val;
      pop[idx] = val;
      preset = 'custom';
      updatePresetUI();
      onPopChanged();
    });
  });
}

function updatePresetUI(){
  document.querySelectorAll('.preset').forEach(b=>{
    b.classList.toggle('active', b.dataset.preset === preset);
  });
}

function applyPreset(name){
  preset = name;
  if(name === 'custom'){
    updatePresetUI();
    return;
  }
  pop = [...PRESETS[name]];
  $('mRange').value = pop.length;
  $('mVal').textContent = pop.length;
  updatePresetUI();
  renderValInputs();
  onPopChanged();
}

function changePopSize(newSize){
  // 슬라이더로 크기 변경 — 현재 값들을 유지하면서 길이 조정
  if(newSize > pop.length){
    while(pop.length < newSize){
      pop.push((pop.length+1)*2);  // 기본값
    }
  } else {
    pop = pop.slice(0, newSize);
  }
  // n의 최대값도 모집단 크기에 맞춰 안내(여기서는 그대로 유지)
  preset = 'custom';
  updatePresetUI();
  renderValInputs();
  onPopChanged();
}

/* ====================== 분포 차트 ====================== */
function drawChart(arr, stats){
  const cv = $('distChart');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL = 56, padR = 22, padT = 22, padB = 56;
  const plotW = W - padL - padR;
  const plotH = H - padT - padB;

  if(arr.length === 0){
    ctx.fillStyle='#64748b';
    ctx.font='15px sans-serif';
    ctx.textAlign='center';
    ctx.fillText('표본을 만들어주세요', W/2, H/2);
    return;
  }

  // X 범위: 모집단 min~max
  const minV = Math.min(...pop), maxV = Math.max(...pop);
  const spanV = (maxV - minV) || 1;
  const maxP = Math.max(...arr.map(d=>d.p));

  // 축
  ctx.strokeStyle='rgba(148,163,184,.45)';
  ctx.lineWidth=1.2;
  ctx.beginPath();
  ctx.moveTo(padL, padT); ctx.lineTo(padL, H-padB);
  ctx.lineTo(W-padR, H-padB);
  ctx.stroke();

  // y 가이드라인
  ctx.strokeStyle='rgba(148,163,184,.13)';
  ctx.fillStyle='#94a3b8';
  ctx.font='12px sans-serif';
  ctx.textAlign='right';
  ctx.textBaseline='middle';
  const yTicks = 5;
  for(let i=0;i<=yTicks;i++){
    const ratio = i/yTicks;
    const y = H - padB - ratio*plotH;
    if(i > 0){
      ctx.beginPath();
      ctx.setLineDash([3,3]);
      ctx.moveTo(padL, y); ctx.lineTo(W-padR, y);
      ctx.stroke();
      ctx.setLineDash([]);
    }
    ctx.fillText((ratio*maxP).toFixed(3), padL-7, y);
  }

  // 막대 폭 계산: 각 점의 X 위치는 (xb - minV)/spanV
  const barW = Math.max(6, Math.min(60, plotW / Math.max(arr.length, 6) * 0.7));

  // 막대 그리기
  arr.forEach(d=>{
    const xRatio = spanV === 0 ? 0.5 : (d.xb - minV)/spanV;
    const cx = padL + xRatio*plotW;
    const bh = (d.p / maxP) * plotH;
    const x0 = cx - barW/2;
    const y0 = H - padB - bh;
    const grad = ctx.createLinearGradient(0, y0, 0, H-padB);
    grad.addColorStop(0, '#38bdf8');
    grad.addColorStop(1, 'rgba(129,140,248,.55)');
    ctx.fillStyle = grad;
    // 둥근 위쪽 막대
    const r = 4;
    ctx.beginPath();
    ctx.moveTo(x0, y0+r);
    ctx.quadraticCurveTo(x0, y0, x0+r, y0);
    ctx.lineTo(x0+barW-r, y0);
    ctx.quadraticCurveTo(x0+barW, y0, x0+barW, y0+r);
    ctx.lineTo(x0+barW, H-padB);
    ctx.lineTo(x0, H-padB);
    ctx.closePath();
    ctx.fill();
    // 막대 위 확률 표시 (값이 충분히 클 때만)
    if(d.p / maxP > 0.1 && arr.length <= 18){
      ctx.fillStyle='#fde047';
      ctx.font='bold 11px sans-serif';
      ctx.textAlign='center'; ctx.textBaseline='bottom';
      ctx.fillText(d.p.toFixed(3), cx, y0-2);
    }
  });

  // 모평균 m 점선
  const m = stats.mean;
  const xm = spanV === 0 ? padL+plotW/2 : padL + (m-minV)/spanV * plotW;
  ctx.strokeStyle='#fb7185';
  ctx.setLineDash([6,5]);
  ctx.lineWidth=2.2;
  ctx.beginPath();
  ctx.moveTo(xm, padT); ctx.lineTo(xm, H-padB);
  ctx.stroke();
  ctx.setLineDash([]);
  // 라벨
  ctx.fillStyle='#fb7185';
  ctx.font='bold 13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  ctx.fillText('m='+fmt(m,3), xm, padT-4);

  // E(X̄) = m 표시 (실제 가중평균: 이론적으로 m과 같음, 검증)
  const Exb = arr.reduce((s,d)=>s + d.xb*d.p, 0);
  const xe = spanV === 0 ? padL+plotW/2 : padL + (Exb-minV)/spanV * plotW;
  ctx.strokeStyle='rgba(253,224,71,.85)';
  ctx.setLineDash([2,4]);
  ctx.lineWidth=2;
  ctx.beginPath();
  ctx.moveTo(xe, padT+18); ctx.lineTo(xe, H-padB);
  ctx.stroke();
  ctx.setLineDash([]);

  // x축 눈금: 모집단 모든 값 표시
  ctx.fillStyle='#94a3b8';
  ctx.font='12px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  // 균등 간격 (5~7 눈금)
  const ticks = [];
  if(spanV === 0){
    ticks.push(minV);
  } else {
    const tCount = Math.min(7, arr.length);
    for(let i=0;i<tCount;i++){
      const v = minV + (i/(tCount-1))*spanV;
      ticks.push(v);
    }
  }
  ticks.forEach(v=>{
    const xr = (v-minV)/(spanV||1);
    const xpx = padL + xr*plotW;
    ctx.beginPath();
    ctx.strokeStyle='rgba(148,163,184,.45)';
    ctx.moveTo(xpx, H-padB); ctx.lineTo(xpx, H-padB+4);
    ctx.stroke();
    ctx.fillText(fmtNum(v), xpx, H-padB+8);
  });

  // 축 제목
  ctx.fillStyle='#cbd5e1';
  ctx.font='bold 14px sans-serif';
  ctx.textAlign='center';
  ctx.textBaseline='alphabetic';
  fillXBar(ctx, W/2, H-8, '표본평균  ', '');
  ctx.save();
  ctx.translate(16, H/2);
  ctx.rotate(-Math.PI/2);
  ctx.textAlign='center';
  fillTextParts(ctx,
    [{t:'확률  P(', bar:false},
     {t:'X', bar:true},
     {t:' = ', bar:false},
     {t:'x', bar:true},
     {t:')', bar:false}],
    0, 0);
  ctx.restore();
}

/* ====================== 분포표 ====================== */
function renderDistTable(arr){
  const tbody = $('distTable').querySelector('tbody');
  let html = '';
  arr.forEach(d=>{
    // 분수 형태: sum/n (가능하면 약분)
    const g = gcd(d.sum, n);
    const num = d.sum/g, den = n/g;
    const fracStr = den === 1 ? `${num}` : `${num}/${den}`;
    const xbStr = isInt(d.xb) ? Math.round(d.xb)+'' : d.xb.toFixed(4);
    html += `<tr>
      <td class="xb-cell">${xbStr}</td>
      <td class="frac-cell">${fracStr}</td>
      <td class="p-cell">${d.p.toFixed(6)}</td>
    </tr>`;
  });
  tbody.innerHTML = html;
}

/* ====================== 예시 표본 ====================== */
function sampleOnce(nn){
  const idx=[], vals=[];
  const N = pop.length;
  for(let i=0;i<nn;i++){
    const k = Math.floor(Math.random()*N);
    idx.push(k); vals.push(pop[k]);
  }
  const sum = vals.reduce((a,b)=>a+b,0);
  return {idx, vals, sum, xb: sum/nn};
}

function renderExamples(){
  const list = $('exList');
  list.innerHTML = '';
  const samples = [];
  for(let i=0;i<5;i++) samples.push(sampleOnce(n));
  // 첫 표본의 인덱스로 모집단 하이라이트
  highlightBalls(samples[0].idx);

  samples.forEach((s,i)=>{
    const row = document.createElement('div');
    row.className = 'ex-item';
    const chips = s.vals.map((v,j)=>
      `<span class="ex-chip" style="animation-delay:${(i*0.04+j*0.03).toFixed(2)}s">${v}</span>`
    ).join('');
    const xbStr = isInt(s.xb) ? Math.round(s.xb)+'' : s.xb.toFixed(3);
    const g = gcd(s.sum, n);
    const fracStr = (n/g === 1) ? `${s.sum/g}` : `${s.sum/g}/${n/g}`;
    row.innerHTML = `
      <div class="ex-idx">${i+1}</div>
      <div class="ex-chips">${chips}</div>
      <div class="ex-xbar">
        <span class="sm"><span class="xb">X</span> = (${s.vals.join('+')})/${n}</span>
        ${xbStr} <span style="opacity:.7;font-size:.8rem">(${fracStr})</span>
      </div>
    `;
    list.appendChild(row);
  });
}

/* ====================== 갱신 파이프라인 ====================== */
function updateAll(){
  // 모집단 통계
  const ps = popStats(pop);
  $('popMean').textContent = fmt(ps.mean, 3);
  $('popVar').textContent  = fmt(ps.var, 3);
  $('popSd').textContent   = fmt(ps.sd, 3);
  $('cPopM').textContent   = fmt(ps.mean, 4);
  $('cPopV').textContent   = fmt(ps.var, 4);
  $('cPopS').textContent   = fmt(ps.sd, 4);

  // 표본평균의 분포
  // 너무 큰 경우 경고
  const N = pop.length;
  const totalCases = Math.pow(N, n);
  $('totalCases').textContent = totalCases.toLocaleString();
  const spread = Math.max(...pop) - Math.min(...pop);
  const warnEl = $('warnBox');
  // 다항식 합성곱은 spread*n+1 길이 → 너무 크면 위험
  if(spread * n > 800){
    warnEl.classList.add('show');
    warnEl.innerHTML = '⚠️ n과 모집단 값의 폭이 너무 큽니다. 계산이 느려질 수 있어요. n을 줄이거나 값의 폭을 줄여보세요.';
    if(spread * n > 2000){
      warnEl.innerHTML = '⚠️ n과 모집단 값의 폭이 너무 커서 정확 계산을 생략합니다. n을 줄여주세요.';
      drawChart([], ps);
      renderDistTable([]);
      $('distCnt').textContent = '--';
      $('cXbM').textContent = '--';
      $('cXbV').textContent = '--';
      $('cXbS').textContent = '--';
      return;
    }
  } else {
    warnEl.classList.remove('show');
  }

  const arr = pmfXbar(pop, n);
  $('distCnt').textContent = arr.length;
  drawChart(arr, ps);
  renderDistTable(arr);

  // 표본평균 비교값
  $('cXbM').textContent = fmt(ps.mean, 4);
  $('cXbV').textContent = fmt(ps.var/n, 4);
  $('cXbS').textContent = fmt(Math.sqrt(ps.var/n), 4);

  // 새 예시 표본
  renderExamples();
}

function onPopChanged(){
  drawBasket();
  updateAll();
}

/* ====================== 초기화 ====================== */
function init(){
  renderValInputs();
  drawBasket();
  updateAll();

  document.querySelectorAll('.preset').forEach(b=>{
    b.addEventListener('click', ()=> applyPreset(b.dataset.preset));
  });

  $('mRange').addEventListener('input', e=>{
    const sz = parseInt(e.target.value);
    $('mVal').textContent = sz;
    changePopSize(sz);
  });

  $('nRange').addEventListener('input', e=>{
    n = parseInt(e.target.value);
    $('nVal').textContent = n;
    updateAll();
  });

  $('btnResample').addEventListener('click', ()=>{
    renderExamples();
  });

  window.addEventListener('resize', ()=>{
    drawBasket();
    // 차트도 재그리기
    const ps = popStats(pop);
    const arr = pmfXbar(pop, n);
    drawChart(arr, ps);
  });
}
init();
</script>
</body>
</html>
"""


# ─────────────────────────────────────────────────────────────────────────────
# render()
# ─────────────────────────────────────────────────────────────────────────────
def render():
    st.subheader("📊 표본평균 X̄의 분포 탐험")
    st.caption(
        "모집단을 자유롭게 만들고, 표본 크기 **n**을 바꾸며 "
        "표본평균 **X̄**이 가질 수 있는 **모든 값**과 **각 값이 나올 확률**을 정확히 계산하여 살펴봅니다."
    )

    components.html(_HTML, height=2150, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
