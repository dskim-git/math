# activities/probability_new/mini/sampling_mean_relation_lab.py
"""
모평균과 표본평균의 관계 — 표본평균 분포 시각 탐험 미니활동
- 3가지 모집단(학생 키 / 수학 점수 / 줄넘기 횟수)에서 m개의 표본을 임의(복원)추출
- 모집단 가로 수직선에 표본 위치 빨간 점/막대로 강조
- 표본평균 X̄들을 히스토그램으로 누적, N(μ, σ²)와 N(μ, σ²/n)의 두 정규곡선과 비교
- 모집단(이론) / 표본평균(이론) / 표본평균(경험) 3 통계 비교 카드
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🌟 미니: 모평균 ↔ 표본평균 — 두 정규곡선 비교 실험실",
    "description": "모집단에서 표본을 여러 번 추출해 X̄들의 분포를 모집단 N(μ,σ²)와 표본평균의 분포 N(μ,σ²/n) 두 정규곡선과 함께 비교합니다.",
    "order": 9,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "표본평균관계탐험"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 모평균과 표본평균의 관계**"},
    {
        "key": "두_곡선_차이",
        "label": "그래프에 함께 그려진 **두 정규곡선** N(μ, σ²)과 N(μ, σ²/n)은 어떻게 달랐나요? "
                 "어느 쪽이 더 좁고 뾰족한 모양이었나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "모집단 곡선 N(μ, σ²)은 ___이고, 표본평균 곡선 N(μ, σ²/n)은 ___ ...",
    },
    {
        "key": "n_바뀌면",
        "label": "표본 크기 **n**을 작게(예: n=4) 했을 때와 크게(예: n=40) 했을 때, "
                 "표본평균 X̄들의 분포(점/막대)는 어떻게 다르게 보였나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "n이 작을 때는 X̄ 점들이 ___, n이 클 때는 ___ ...",
    },
    {
        "key": "m_바뀌면",
        "label": "표본의 개수 **m**(표본을 몇 번 뽑는지)을 늘릴수록 히스토그램은 어떤 변화를 보였나요? "
                 "곡선 N(μ, σ²/n)과 어떻게 닮아갔나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "m을 늘릴수록 히스토그램이 점점 ___ 곡선과 ___ ...",
    },
    {
        "key": "경험_이론_차이",
        "label": "비교 표에서 **표본평균(이론)**과 **표본평균(경험)** 값을 비교해 보았을 때, "
                 "두 값은 얼마나 잘 일치했나요? 왜 그런 결과가 나왔다고 생각하나요?",
        "type": "text_area",
        "height": 100,
        "placeholder": "이론값(σ²/n, σ/√n)과 경험값이 ___ 했다. 왜냐하면 ___ ...",
    },
    {
        "key": "비정규_모집단",
        "label": "모집단이 종 모양(정규분포 비슷)이 **아닌 경우**(예: 줄넘기 횟수처럼 한쪽으로 치우친 분포)에도 "
                 "X̄의 분포는 어떻게 보였나요? 거기서 무엇을 발견했나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "줄넘기 분포처럼 치우친 모집단이어도 X̄의 분포는 ___ 모양이었고, "
                       "이를 보고 ___ 라는 사실을 알 수 있었다.",
    },
    {
        "key": "표본평균_의미",
        "label": "이 활동을 통해 **모평균 μ**와 **표본평균 X̄**의 관계를 어떻게 설명할 수 있나요?",
        "type": "text_area",
        "height": 100,
        "placeholder": "모평균은 ___이고, 표본평균은 ___. 따라서 표본평균은 모평균을 ___ ...",
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
# HTML — 모집단 ↔ 표본평균 두 정규곡선 비교 실험실
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
  background:linear-gradient(135deg,rgba(56,189,248,.2),rgba(245,158,11,.2));
  border:2px solid rgba(245,158,11,.5);border-radius:18px;
  padding:14px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.5rem;font-weight:900;color:#fbbf24;margin-bottom:4px;letter-spacing:.3px}
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

/* ============ 프리셋 ============ */
.preset-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:11px}
.preset{
  padding:9px 15px;border-radius:999px;font-size:.98rem;font-weight:800;
  border:2px solid transparent;cursor:pointer;color:#fff;
  background:linear-gradient(135deg,#475569,#334155);
  transition:all .14s ease;
}
.preset:hover{transform:translateY(-1px)}
.preset.active{
  background:linear-gradient(135deg,#f59e0b,#b45309);
  border-color:#fde047;box-shadow:0 4px 12px rgba(245,158,11,.45);color:#fff;
}

/* ============ 모집단 수직선 ============ */
.popline-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(56,189,248,.3);
  border-radius:12px;padding:11px;
}
.popline-info{
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;
  font-size:.92rem;color:#cbd5e1;font-weight:700;margin-bottom:6px;
}
.popline-info b{color:#fbbf24}
#popLine{
  display:block;width:100%;height:170px;
  background:rgba(15,23,42,.4);border-radius:8px;
}

/* ============ 모집단 통계 카드 ============ */
.pop-stats-row{
  display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:11px;
}
@media(max-width:780px){.pop-stats-row{grid-template-columns:repeat(2,1fr)}}
.psc{
  background:rgba(245,158,11,.08);border:1.5px solid rgba(245,158,11,.4);
  border-radius:11px;padding:10px;text-align:center;
}
.psc .lab{font-size:.92rem;color:#fbbf24;font-weight:800;margin-bottom:3px;letter-spacing:.3px}
.psc .val{font-size:1.35rem;color:#fef3c7;font-weight:900}
.psc .sub{font-size:.78rem;color:#94a3b8;margin-top:2px}

/* ============ 표본 설정 ============ */
.ctl-row{
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  background:rgba(34,197,94,.08);border:1.5px solid rgba(34,197,94,.35);
  border-radius:11px;padding:10px;margin-bottom:9px;
}
.ctl-lab{font-size:1rem;font-weight:800;color:#86efac;min-width:120px}
.ctl-range{flex:1;min-width:130px;accent-color:#22c55e;height:6px}
.ctl-val{
  font-size:1.4rem;font-weight:900;color:#fde047;min-width:54px;
  background:rgba(15,23,42,.7);padding:2px 12px;border-radius:8px;text-align:center;
}
.btn-row{display:flex;gap:9px;flex-wrap:wrap;margin-top:5px}
.btn{
  padding:11px 16px;border:none;border-radius:11px;
  font-size:1rem;font-weight:900;color:#fff;cursor:pointer;
  transition:all .15s ease;letter-spacing:.3px;
}
.btn:active{transform:scale(.96)}
.btn-pri{background:linear-gradient(135deg,#22c55e,#15803d);box-shadow:0 3px 10px rgba(34,197,94,.4);flex:1;min-width:160px}
.btn-pri:hover{background:linear-gradient(135deg,#16a34a,#14532d);transform:translateY(-1px)}
.btn-sec{background:linear-gradient(135deg,#3b82f6,#1d4ed8);box-shadow:0 3px 10px rgba(59,130,246,.4)}
.btn-sec:hover{background:linear-gradient(135deg,#2563eb,#1e40af);transform:translateY(-1px)}
.btn-ghost{background:rgba(71,85,105,.65);border:1.5px solid rgba(148,163,184,.3)}
.btn-ghost:hover{background:rgba(71,85,105,.9)}

/* ============ 표본 표 ============ */
.samp-grid{
  display:grid;grid-template-columns:1fr 1fr;gap:11px;
}
@media(max-width:880px){.samp-grid{grid-template-columns:1fr}}

.samp-table-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(99,102,241,.25);
  border-radius:11px;overflow:hidden;
}
.samp-table-head{
  display:flex;justify-content:space-between;align-items:center;
  background:rgba(99,102,241,.18);padding:8px 11px;
  font-size:.95rem;color:#c4b5fd;font-weight:900;letter-spacing:.3px;
}
.samp-table-inner{max-height:260px;overflow:auto}
table.stab{
  width:100%;border-collapse:collapse;font-size:.96rem;color:#e2e8f0;text-align:center;
}
table.stab thead th{
  position:sticky;top:0;z-index:2;
  background:rgba(15,23,42,.95);color:#a5b4fc;font-weight:900;
  padding:7px 6px;border-bottom:2px solid rgba(99,102,241,.4);
}
table.stab tbody td{
  padding:6px 6px;border-bottom:1px solid rgba(99,102,241,.12);
  cursor:pointer;
}
table.stab tbody tr:nth-child(even){background:rgba(30,41,59,.4)}
table.stab tbody tr:hover{background:rgba(56,189,248,.16)}
table.stab tbody tr.selected{
  background:rgba(244,63,94,.22) !important;
  outline:2px solid rgba(244,63,94,.55);outline-offset:-2px;
}
table.stab td.xbar-cell{color:#fde047;font-weight:900}
table.stab td.idx-cell{color:#94a3b8;font-weight:800}

.samp-detail{
  background:rgba(244,63,94,.08);border:1.5px solid rgba(244,63,94,.4);
  border-radius:11px;padding:11px;
}
.sd-head{
  font-size:1rem;color:#fb7185;font-weight:900;
  display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;
  letter-spacing:.3px;
}
.sd-xbar{
  color:#fde047;font-weight:900;
  background:rgba(15,23,42,.55);padding:3px 11px;border-radius:8px;font-size:.98rem;
}
.sd-chips{display:flex;flex-wrap:wrap;gap:5px;max-height:200px;overflow:auto}
.sd-chip{
  display:inline-flex;align-items:center;justify-content:center;
  min-width:34px;height:30px;padding:0 7px;border-radius:8px;
  background:radial-gradient(135deg,#fecaca,#dc2626);
  color:#fff;font-weight:900;font-size:.92rem;
  border:1.5px solid #fca5a5;
  box-shadow:0 2px 4px rgba(244,63,94,.35);
  animation:popIn .25s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes popIn{from{opacity:0;transform:scale(.4)}to{opacity:1;transform:scale(1)}}
.sd-empty{color:#94a3b8;font-style:italic;font-size:.95rem;padding:8px;text-align:center}

/* ============ 정규곡선 차트 ============ */
.chart-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(56,189,248,.3);
  border-radius:12px;padding:12px;
}
#normChart{
  display:block;width:100%;height:360px;
  background:rgba(15,23,42,.5);border-radius:8px;
}
.legend{
  display:flex;flex-wrap:wrap;gap:14px;justify-content:center;
  font-size:.95rem;color:#cbd5e1;font-weight:700;margin-top:10px;
}
.lg{display:flex;align-items:center;gap:6px}
.lg .swatch{display:inline-block;width:22px;height:4px;border-radius:2px}
.lg .dot{display:inline-block;width:9px;height:9px;border-radius:50%}

/* ============ 통계 비교 표 ============ */
.cmp-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(168,85,247,.4);
  border-radius:12px;overflow:hidden;
}
table.ctab{
  width:100%;border-collapse:collapse;font-size:1rem;color:#e2e8f0;text-align:center;
}
table.ctab thead th{
  background:rgba(168,85,247,.22);color:#e9d5ff;font-weight:900;
  padding:9px 8px;border-bottom:2px solid rgba(168,85,247,.5);font-size:1rem;
}
table.ctab tbody td{
  padding:11px 8px;border-bottom:1px solid rgba(168,85,247,.18);
  font-size:1.05rem;
}
table.ctab tbody tr:nth-child(odd){background:rgba(30,41,59,.45)}
table.ctab tbody th{
  background:rgba(168,85,247,.14);color:#c4b5fd;font-weight:900;
  text-align:left;padding:11px 13px;letter-spacing:.3px;
}
table.ctab .vcell{color:#fef3c7;font-weight:900}
table.ctab .theory{color:#7dd3fc}
table.ctab .empir{color:#86efac}

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

</style>
</head>
<body>

<div class="hdr">
  <h1>🌟 모평균과 표본평균의 관계</h1>
  <p>모집단에서 표본을 여러 번 뽑아 <span class="xb">X</span>들이 그리는 분포를
     <b>두 정규곡선</b> N(μ, σ²) ↔ N(μ, σ²/n)과 함께 비교해 봐요!</p>
</div>

<!-- ① 모집단 -->
<div class="panel">
  <h2>🎒 모집단 선택 <span class="badge">실생활 데이터 3가지</span></h2>

  <div class="preset-row" id="presetRow">
    <button class="preset active" data-key="heights">📏 학생 키 (cm) · N≈종모양</button>
    <button class="preset" data-key="scores">📝 수학 시험 점수 · N≈종모양</button>
    <button class="preset" data-key="jumprope">🪢 1분 줄넘기 횟수 · 비대칭</button>
  </div>

  <div class="popline-wrap">
    <div class="popline-info">
      <span>📊 모집단 (가로 수직선 위 회색 점) · <b>크기 N = <span id="popN">--</span></b></span>
      <span>🟥 빨간 점/막대 = 선택된 표본의 위치</span>
    </div>
    <canvas id="popLine" width="900" height="170"></canvas>
  </div>

  <div class="pop-stats-row">
    <div class="psc">
      <div class="lab">모집단 크기 N</div>
      <div class="val" id="kN">--</div>
    </div>
    <div class="psc">
      <div class="lab">모평균 μ</div>
      <div class="val" id="kMu">--</div>
    </div>
    <div class="psc">
      <div class="lab">모분산 σ²</div>
      <div class="val" id="kVar">--</div>
    </div>
    <div class="psc">
      <div class="lab">모표준편차 σ</div>
      <div class="val" id="kSd">--</div>
    </div>
  </div>
</div>

<!-- ② 표본 설정 -->
<div class="panel">
  <h2>🎲 표본 추출 설정 <span class="badge">크기 n인 표본을 m번 뽑습니다</span></h2>

  <div class="ctl-row">
    <span class="ctl-lab">표본 크기 n</span>
    <input type="range" min="2" max="60" value="10" class="ctl-range" id="nRange">
    <span class="ctl-val" id="nVal">10</span>
  </div>
  <div class="ctl-row">
    <span class="ctl-lab">표본 개수 m</span>
    <input type="range" min="5" max="200" value="50" class="ctl-range" id="mRange">
    <span class="ctl-val" id="mVal">50</span>
  </div>

  <div class="btn-row">
    <button class="btn btn-pri" id="btnDraw">🎲 새로 표본 추출</button>
    <button class="btn btn-sec" id="btnAdd">➕ 표본 m개 더 추가</button>
    <button class="btn btn-ghost" id="btnClear">🔄 초기화</button>
  </div>
</div>

<!-- ③ 표본 표 + 선택 표본 상세 -->
<div class="panel">
  <h2>📋 추출된 표본들 <span class="badge">행을 클릭하면 강조됩니다</span></h2>

  <div class="samp-grid">
    <div class="samp-table-wrap">
      <div class="samp-table-head">
        <span>표본 목록</span>
        <span style="font-size:.85rem;color:#cbd5e1;font-weight:700">누적 <span id="totSamp" style="color:#fde047;font-weight:900">0</span>개</span>
      </div>
      <div class="samp-table-inner">
        <table class="stab" id="sampTable">
          <thead>
            <tr><th>표본#</th><th>크기 n</th><th>표본평균 <span class="xb">X</span></th><th>표본표준편차 S</th></tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
    </div>

    <div class="samp-detail">
      <div class="sd-head">
        <span>📦 선택한 표본 #<span id="selIdx">--</span></span>
        <span class="sd-xbar"><span class="xb">X</span> = <span id="selXbar">--</span></span>
      </div>
      <div class="sd-chips" id="selChips">
        <div class="sd-empty">왼쪽 표에서 표본을 선택해 보세요</div>
      </div>
    </div>
  </div>
</div>

<!-- ④ 정규곡선 차트 -->
<div class="panel">
  <h2>📈 정규곡선 비교: N(μ, σ²) vs N(μ, σ²/n)</h2>

  <div class="chart-wrap">
    <canvas id="normChart" width="980" height="360"></canvas>
    <div class="legend">
      <span class="lg"><span class="swatch" style="background:#38bdf8"></span> 모집단 N(μ, σ²)</span>
      <span class="lg"><span class="swatch" style="background:#f59e0b"></span> 표본평균 N(μ, σ²/n)</span>
      <span class="lg"><span class="dot" style="background:rgba(0,0,0,.4);outline:1px solid #475569"></span> 표본평균 <span class="xb">X</span>들 (점)</span>
      <span class="lg"><span class="dot" style="background:#f43f5e"></span> 선택된 표본의 <span class="xb">X</span></span>
      <span class="lg"><span class="swatch" style="background:rgba(56,189,248,.35)"></span> <span class="xb">X</span> 히스토그램</span>
    </div>
  </div>

  <div class="insight">
    <span class="ico">💡</span>
    <span>
      모집단 곡선보다 <span class="xb">X</span>의 곡선이 <b>훨씬 좁고 뾰족</b>해요.
      n이 커질수록 <span class="xb">X</span> 점들이 모평균 μ 주위에 <b>더 촘촘히</b> 모이고,
      모집단이 종 모양이 아니어도 <span class="xb">X</span>의 분포는 점점 종 모양에 가까워져요!
    </span>
  </div>
</div>

<!-- ⑤ 통계 비교 표 -->
<div class="panel">
  <h2>📊 모수 vs 표본평균 — 이론과 경험 비교</h2>
  <div class="cmp-wrap">
    <table class="ctab">
      <thead>
        <tr>
          <th style="text-align:left;padding-left:13px">항목</th>
          <th>평균 (μ)</th>
          <th>분산 (σ²)</th>
          <th>표준편차 (σ)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>🎒 모집단 (이론)</th>
          <td class="vcell"  id="cMu">--</td>
          <td class="vcell"  id="cVar">--</td>
          <td class="vcell"  id="cSd">--</td>
        </tr>
        <tr>
          <th>🎯 표본평균 (이론)</th>
          <td class="theory" id="tMu">--</td>
          <td class="theory" id="tVar">--</td>
          <td class="theory" id="tSd">--</td>
        </tr>
        <tr>
          <th>🌟 표본평균 (경험)</th>
          <td class="empir"  id="eMu">--</td>
          <td class="empir"  id="eVar">--</td>
          <td class="empir"  id="eSd">--</td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="insight">
    <span class="ico">🔍</span>
    <span>
      m(표본 개수)을 늘릴수록 <b>표본평균(경험)</b> 행이 <b>표본평균(이론)</b> 행에 가까워져요.
      이론: E(<span class="xb">X</span>)=μ, V(<span class="xb">X</span>)=σ²/n.
    </span>
  </div>
</div>

<script>
/* ====================== 시드 RNG (재현 가능) ====================== */
function mulberry32(seed){
  let s = seed >>> 0;
  return function(){
    s = (s + 0x6D2B79F5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function boxMuller(rng){
  let u = 0, v = 0;
  while(u === 0) u = rng();
  while(v === 0) v = rng();
  return Math.sqrt(-2*Math.log(u)) * Math.cos(2*Math.PI*v);
}

/* ====================== 모집단 데이터 ====================== */
function makeHeights(){
  // 학생 키(cm): N=160, μ≈168, σ≈6 (대략 정규)
  const rng = mulberry32(20251);
  const arr = [];
  for(let i=0;i<160;i++){
    let v = 168 + boxMuller(rng) * 6.2;
    v = Math.max(150, Math.min(188, v));
    arr.push(Math.round(v*10)/10);  // 소수 한 자리
  }
  return arr;
}
function makeScores(){
  // 수학 시험 점수(0~100): N=160, 약간 좁은 정규
  const rng = mulberry32(73821);
  const arr = [];
  for(let i=0;i<160;i++){
    let v = 72 + boxMuller(rng) * 14;
    v = Math.max(15, Math.min(100, v));
    arr.push(Math.round(v));  // 정수
  }
  return arr;
}
function makeJumprope(){
  // 1분 줄넘기 횟수: 비대칭(오른쪽 꼬리), 평균 약 90, range 40~220
  const rng = mulberry32(91234);
  const arr = [];
  for(let i=0;i<160;i++){
    // 감마풍: 두 개의 지수합으로 근사
    const shape = 4;
    let v = 0;
    for(let k=0;k<shape;k++){
      v += -Math.log(1 - rng()) * 22;
    }
    v = v + 28;  // 베이스라인
    v = Math.max(30, Math.min(240, v));
    arr.push(Math.round(v));
  }
  return arr;
}
const POPULATIONS = {
  heights:  {label: "학생 키 (cm)",       data: makeHeights(),  unit: "cm",   showInt:false},
  scores:   {label: "수학 시험 점수 (점)", data: makeScores(),   unit: "점",   showInt:true},
  jumprope: {label: "1분 줄넘기 횟수",     data: makeJumprope(), unit: "회",   showInt:true},
};

/* ====================== 상태 ====================== */
let currentKey = "heights";
let n = 10;
let m = 50;
let samples = [];      // [{vals, idx, mean, sd}]
let selectedIdx = 0;   // 표본 표에서 선택된 인덱스
let drawRng = mulberry32(Date.now() & 0xFFFFFFFF);  // 추출용 RNG

const $ = id => document.getElementById(id);
function fmt(v, d=3){ if(isNaN(v)) return '--'; return Number(v.toFixed(d)).toString(); }

/* ====================== Canvas — X 위에 가로선(X̄) 그리기 헬퍼 ======================
 * canvas에서 X+combining macron(U+0304)은 폰트에 따라 깨질 수 있어,
 * X 글자를 그린 뒤 그 위에 사각형으로 직접 가로선을 칠합니다.
 * parts: [{t:"문자열", bar:true|false}, ...]
 */
function fillTextParts(ctx, parts, x, y){
  // 현재 textAlign 기준으로 시작 x 계산
  let totalW = 0;
  parts.forEach(p => totalW += ctx.measureText(p.t).width);
  let cursor;
  const align = ctx.textAlign;
  if(align === 'center')      cursor = x - totalW/2;
  else if(align === 'right')  cursor = x - totalW;
  else                        cursor = x;
  // 글꼴 크기 추출 (예: "bold 14px sans-serif" → 14)
  const fm = (ctx.font.match(/(\d+(?:\.\d+)?)px/) || [0,'12'])[1];
  const fpx = parseFloat(fm);
  const oldAlign = ctx.textAlign;
  const oldBaseline = ctx.textBaseline;
  ctx.textAlign = 'left';
  parts.forEach(p => {
    const w = ctx.measureText(p.t).width;
    ctx.fillText(p.t, cursor, y);
    if(p.bar && w > 0){
      // baseline에 맞춰 글자의 윗 위치 계산
      let top;
      if(oldBaseline === 'top')                  top = y - 1;
      else if(oldBaseline === 'middle')          top = y - fpx*0.55;
      else if(oldBaseline === 'bottom')          top = y - fpx*1.0 - 1;
      else /* alphabetic / hanging / ideographic */ top = y - fpx*0.92;
      const barH = Math.max(1.5, fpx*0.09);
      const oldFill = ctx.fillStyle;
      ctx.fillRect(cursor+1, top, w-2, barH);
      ctx.fillStyle = oldFill;
    }
    cursor += w;
  });
  ctx.textAlign = oldAlign;
}
/* 간편 단축: prefix + X̄ + suffix 한 줄을 그림 */
function fillXBar(ctx, x, y, prefix, suffix){
  const parts = [];
  if(prefix) parts.push({t: prefix, bar:false});
  parts.push({t: 'X', bar:true});
  if(suffix) parts.push({t: suffix, bar:false});
  fillTextParts(ctx, parts, x, y);
}

/* ====================== 통계 ====================== */
function popStats(values){
  const mean = values.reduce((a,b)=>a+b,0)/values.length;
  const v = values.reduce((s,x)=>s+(x-mean)*(x-mean),0)/values.length;
  return {mean, var:v, sd:Math.sqrt(v), min:Math.min(...values), max:Math.max(...values)};
}
function sampleStats(values){
  const n = values.length;
  const mean = values.reduce((a,b)=>a+b,0)/n;
  if(n <= 1) return {mean, sd:0};
  const v = values.reduce((s,x)=>s+(x-mean)*(x-mean),0)/(n-1);
  return {mean, sd:Math.sqrt(v)};
}

/* ====================== 표본 추출 ====================== */
function drawOneSample(values, nn){
  const N = values.length;
  const idx = new Array(nn), vals = new Array(nn);
  for(let i=0;i<nn;i++){
    const k = Math.floor(drawRng()*N);
    idx[i] = k;
    vals[i] = values[k];
  }
  const stats = sampleStats(vals);
  return {idx, vals, mean: stats.mean, sd: stats.sd};
}
function drawSamples(values, nn, mm){
  const out = new Array(mm);
  for(let i=0;i<mm;i++) out[i] = drawOneSample(values, nn);
  return out;
}

/* ====================== 모집단 수직선 ====================== */
function drawPopLine(){
  const cv = $('popLine');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const data = POPULATIONS[currentKey].data;
  const ps = popStats(data);
  const padL = 48, padR = 30, padT = 30, padB = 50;
  const lo = ps.min, hi = ps.max;
  const span = hi - lo || 1;
  const yAxis = H - padB - 30;

  // 축
  ctx.strokeStyle = 'rgba(148,163,184,.6)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(padL, yAxis); ctx.lineTo(W-padR, yAxis);
  ctx.stroke();

  // 양끝 라벨
  ctx.fillStyle = '#cbd5e1';
  ctx.font = 'bold 13px sans-serif';
  ctx.textAlign = 'left'; ctx.textBaseline = 'top';
  ctx.fillText(POPULATIONS[currentKey].showInt ? Math.round(lo)+'' : lo.toFixed(1), padL, yAxis+8);
  ctx.textAlign = 'right';
  ctx.fillText(POPULATIONS[currentKey].showInt ? Math.round(hi)+'' : hi.toFixed(1), W-padR, yAxis+8);

  // 중간 눈금
  const ticks = 5;
  ctx.textAlign = 'center';
  ctx.fillStyle = '#94a3b8';
  ctx.font = '12px sans-serif';
  ctx.strokeStyle = 'rgba(148,163,184,.4)';
  for(let i=1;i<ticks;i++){
    const v = lo + i*span/ticks;
    const x = padL + (v-lo)/span * (W-padL-padR);
    ctx.beginPath();
    ctx.moveTo(x, yAxis-4); ctx.lineTo(x, yAxis+4);
    ctx.stroke();
    ctx.fillText(POPULATIONS[currentKey].showInt ? Math.round(v)+'' : v.toFixed(0), x, yAxis+8);
  }

  // 모평균 μ 점선
  const xMu = padL + (ps.mean - lo)/span * (W-padL-padR);
  ctx.strokeStyle = '#fbbf24';
  ctx.setLineDash([5,4]);
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(xMu, padT-4); ctx.lineTo(xMu, yAxis);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 12px sans-serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
  ctx.fillText('μ='+fmt(ps.mean,2), xMu, padT-6);

  // 선택된 표본 인덱스 set
  const sel = (samples.length > 0 && samples[selectedIdx]) ? new Set(samples[selectedIdx].idx) : null;

  // 모든 점 그리기 — 선택 표본은 빨강+막대
  // Jitter (deterministic from index hash to avoid flicker)
  const half = 22;
  for(let i=0;i<data.length;i++){
    const v = data[i];
    const x = padL + (v-lo)/span * (W-padL-padR);
    // pseudo-random y offset based on i
    const jr = ((i*2654435761)>>>0) / 4294967296;
    const jy = (jr - 0.5) * 14;
    if(sel && sel.has(i)){
      // 빨간 막대 + 점
      ctx.strokeStyle = 'rgba(244,63,94,.95)';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(x, yAxis - half); ctx.lineTo(x, yAxis + half);
      ctx.stroke();
      ctx.fillStyle = '#f43f5e';
      ctx.beginPath();
      ctx.arc(x, yAxis + jy, 5, 0, Math.PI*2);
      ctx.fill();
    } else {
      ctx.fillStyle = 'rgba(148,163,184,.55)';
      ctx.beginPath();
      ctx.arc(x, yAxis + jy, 3.2, 0, Math.PI*2);
      ctx.fill();
    }
  }

  // 단위 표시
  ctx.fillStyle = '#cbd5e1';
  ctx.font = 'bold 12px sans-serif';
  ctx.textAlign = 'right';
  ctx.fillText(POPULATIONS[currentKey].unit, W-padR-2, padT-6);
}

/* ====================== 정규곡선 + 히스토그램 ====================== */
function pdf(x, mu, sd){
  if(sd <= 0) return 0;
  return (1/(sd*Math.sqrt(2*Math.PI))) * Math.exp(-0.5*Math.pow((x-mu)/sd, 2));
}

function drawNormChart(){
  const cv = $('normChart');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const padL = 56, padR = 22, padT = 22, padB = 60;
  const plotW = W - padL - padR;
  const plotH = H - padT - padB;

  const data = POPULATIONS[currentKey].data;
  const ps = popStats(data);
  const mu = ps.mean, sd = ps.sd;
  const sdBar = sd / Math.sqrt(n);

  // x 범위: 모집단의 ±4σ와 X̄ 범위 모두 포함
  const xMin = Math.min(mu - 4*sd, mu - 5*sdBar, ps.min);
  const xMax = Math.max(mu + 4*sd, mu + 5*sdBar, ps.max);
  const xSpan = xMax - xMin;

  // 곡선의 최대 y (둘 중 큰 쪽)
  const maxPdfPop = pdf(mu, mu, sd);
  const maxPdfBar = pdf(mu, mu, sdBar);
  let yMaxPdf = Math.max(maxPdfPop, maxPdfBar);

  // 표본평균 히스토그램
  let hist = null, histMaxDensity = 0;
  if(samples.length > 0){
    const means = samples.map(s=>s.mean);
    const nbins = Math.max(10, Math.min(30, Math.ceil(Math.sqrt(samples.length))+5));
    const binW = xSpan / nbins;
    const bins = new Array(nbins).fill(0);
    means.forEach(v=>{
      let k = Math.floor((v - xMin)/binW);
      if(k < 0) k = 0; if(k >= nbins) k = nbins-1;
      bins[k]++;
    });
    // 밀도로 환산
    const dens = bins.map(c => c / (samples.length * binW));
    histMaxDensity = Math.max(...dens);
    yMaxPdf = Math.max(yMaxPdf, histMaxDensity);
    hist = {nbins, binW, dens};
  }

  const Y = y => padT + plotH - (y / yMaxPdf) * plotH;
  const X = x => padL + ((x - xMin) / xSpan) * plotW;

  // 가이드 그리드
  ctx.strokeStyle = 'rgba(148,163,184,.13)';
  ctx.setLineDash([3,3]);
  ctx.lineWidth = 1;
  for(let i=1;i<=4;i++){
    const y = padT + (i/4)*plotH;
    ctx.beginPath();
    ctx.moveTo(padL, y); ctx.lineTo(W-padR, y);
    ctx.stroke();
  }
  ctx.setLineDash([]);

  // 히스토그램 (먼저, 곡선이 위에 보이게)
  if(hist){
    ctx.fillStyle = 'rgba(56,189,248,.32)';
    ctx.strokeStyle = 'rgba(56,189,248,.6)';
    ctx.lineWidth = 1;
    for(let i=0;i<hist.nbins;i++){
      const x0 = X(xMin + i*hist.binW);
      const x1 = X(xMin + (i+1)*hist.binW);
      const y0 = Y(hist.dens[i]);
      const y1 = Y(0);
      ctx.beginPath();
      ctx.rect(x0+1, y0, x1-x0-2, y1-y0);
      ctx.fill(); ctx.stroke();
    }
  }

  // 모집단 곡선 N(μ, σ²) — 파랑
  ctx.strokeStyle = '#38bdf8';
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  for(let i=0;i<=400;i++){
    const x = xMin + (i/400)*xSpan;
    const y = pdf(x, mu, sd);
    if(i === 0) ctx.moveTo(X(x), Y(y));
    else ctx.lineTo(X(x), Y(y));
  }
  ctx.stroke();

  // 표본평균 곡선 N(μ, σ²/n) — 주황
  ctx.strokeStyle = '#f59e0b';
  ctx.lineWidth = 2.8;
  ctx.beginPath();
  for(let i=0;i<=400;i++){
    const x = xMin + (i/400)*xSpan;
    const y = pdf(x, mu, sdBar);
    if(i === 0) ctx.moveTo(X(x), Y(y));
    else ctx.lineTo(X(x), Y(y));
  }
  ctx.stroke();

  // μ 점선
  const xMu = X(mu);
  ctx.strokeStyle = 'rgba(251,191,36,.9)';
  ctx.setLineDash([5,4]);
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(xMu, padT); ctx.lineTo(xMu, padT+plotH);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 14px sans-serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'alphabetic';
  ctx.fillText('μ='+fmt(mu,2), xMu, padT-5);

  // 축
  ctx.strokeStyle = 'rgba(148,163,184,.5)';
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.moveTo(padL, padT+plotH); ctx.lineTo(W-padR, padT+plotH);
  ctx.moveTo(padL, padT); ctx.lineTo(padL, padT+plotH);
  ctx.stroke();

  // x 눈금
  ctx.fillStyle = '#94a3b8';
  ctx.font = '12px sans-serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  const xTicks = 7;
  for(let i=0;i<=xTicks;i++){
    const xv = xMin + (i/xTicks)*xSpan;
    const xpx = X(xv);
    ctx.beginPath();
    ctx.strokeStyle = 'rgba(148,163,184,.45)';
    ctx.moveTo(xpx, padT+plotH); ctx.lineTo(xpx, padT+plotH+4);
    ctx.stroke();
    ctx.fillText(POPULATIONS[currentKey].showInt ? Math.round(xv)+'' : xv.toFixed(1), xpx, padT+plotH+8);
  }

  // 표본평균 점들 (작게, 가로 베이스라인 위)
  if(samples.length > 0){
    const yDots = padT + plotH - 14;
    ctx.fillStyle = 'rgba(0,0,0,.5)';
    samples.forEach((s,i)=>{
      if(i === selectedIdx) return;
      const x = X(s.mean);
      const jy = (((i*2654435761) >>> 0)/4294967296 - 0.5) * 12;
      ctx.beginPath();
      ctx.arc(x, yDots + jy, 3, 0, Math.PI*2);
      ctx.fill();
    });
    // 선택 표본 점은 더 크고 빨강
    if(samples[selectedIdx]){
      const sx = X(samples[selectedIdx].mean);
      ctx.fillStyle = '#f43f5e';
      ctx.beginPath();
      ctx.arc(sx, yDots, 7, 0, Math.PI*2);
      ctx.fill();
      // 라벨
      ctx.fillStyle = '#fda4af';
      ctx.font = 'bold 13px sans-serif';
      ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
      fillXBar(ctx, sx, yDots-9, '', '='+fmt(samples[selectedIdx].mean,2));
    }
  }

  // 축 제목
  ctx.fillStyle = '#cbd5e1';
  ctx.font = 'bold 13px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('값 ('+POPULATIONS[currentKey].unit+')', W/2, H-10);
  ctx.save();
  ctx.translate(15, H/2);
  ctx.rotate(-Math.PI/2);
  ctx.fillText('확률밀도', 0, 0);
  ctx.restore();
}

/* ====================== UI 업데이트 ====================== */
function updatePopStats(){
  const data = POPULATIONS[currentKey].data;
  const ps = popStats(data);
  const isInt = POPULATIONS[currentKey].showInt;
  $('popN').textContent = data.length;
  $('kN').textContent = data.length;
  $('kMu').textContent  = isInt ? fmt(ps.mean,2) : fmt(ps.mean,2);
  $('kVar').textContent = fmt(ps.var,2);
  $('kSd').textContent  = fmt(ps.sd,2);

  // 비교 표 모집단(이론) 행
  $('cMu').textContent  = fmt(ps.mean,3);
  $('cVar').textContent = fmt(ps.var,3);
  $('cSd').textContent  = fmt(ps.sd,3);
}

function updateTheoryStats(){
  const data = POPULATIONS[currentKey].data;
  const ps = popStats(data);
  $('tMu').textContent  = fmt(ps.mean,3);
  $('tVar').textContent = fmt(ps.var/n, 3);
  $('tSd').textContent  = fmt(ps.sd/Math.sqrt(n), 3);
}

function updateEmpiricalStats(){
  if(samples.length === 0){
    $('eMu').textContent = '--';
    $('eVar').textContent = '--';
    $('eSd').textContent = '--';
    return;
  }
  const means = samples.map(s=>s.mean);
  const mu = means.reduce((a,b)=>a+b,0)/means.length;
  let v = 0;
  if(means.length > 1){
    v = means.reduce((s,x)=>s+(x-mu)*(x-mu),0)/(means.length-1);
  }
  $('eMu').textContent  = fmt(mu, 3);
  $('eVar').textContent = means.length > 1 ? fmt(v, 3) : '--';
  $('eSd').textContent  = means.length > 1 ? fmt(Math.sqrt(v), 3) : '--';
}

function renderSampleTable(){
  const tbody = $('sampTable').querySelector('tbody');
  if(samples.length === 0){
    tbody.innerHTML = '<tr><td colspan="4" style="padding:18px;color:#64748b;font-style:italic">표본을 추출해 보세요</td></tr>';
    $('totSamp').textContent = '0';
    return;
  }
  $('totSamp').textContent = samples.length;
  let html = '';
  samples.forEach((s,i)=>{
    const cls = (i === selectedIdx) ? ' class="selected"' : '';
    html += `<tr${cls} data-i="${i}">
      <td class="idx-cell">#${i+1}</td>
      <td>${s.vals.length}</td>
      <td class="xbar-cell">${fmt(s.mean, 3)}</td>
      <td>${fmt(s.sd, 3)}</td>
    </tr>`;
  });
  tbody.innerHTML = html;
  tbody.querySelectorAll('tr').forEach(tr=>{
    tr.addEventListener('click', ()=>{
      const i = parseInt(tr.dataset.i);
      if(isNaN(i)) return;
      selectedIdx = i;
      renderSampleTable();
      renderSelDetail();
      drawPopLine();
      drawNormChart();
    });
  });
  // 선택된 행으로 자동 스크롤
  const selTr = tbody.querySelector('tr.selected');
  if(selTr) selTr.scrollIntoView({block:'nearest', behavior:'smooth'});
}

function renderSelDetail(){
  const det = $('selChips');
  if(samples.length === 0 || !samples[selectedIdx]){
    det.innerHTML = '<div class="sd-empty">왼쪽 표에서 표본을 선택해 보세요</div>';
    $('selIdx').textContent = '--';
    $('selXbar').textContent = '--';
    return;
  }
  const s = samples[selectedIdx];
  $('selIdx').textContent = (selectedIdx+1);
  $('selXbar').textContent = fmt(s.mean, 3);
  det.innerHTML = s.vals.map((v,i)=>
    `<span class="sd-chip" style="animation-delay:${(i*0.015).toFixed(2)}s">${POPULATIONS[currentKey].showInt ? Math.round(v) : v}</span>`
  ).join('');
}

/* ====================== 액션 ====================== */
function doDraw(){
  const data = POPULATIONS[currentKey].data;
  samples = drawSamples(data, n, m);
  selectedIdx = 0;
  updateTheoryStats();
  updateEmpiricalStats();
  renderSampleTable();
  renderSelDetail();
  drawPopLine();
  drawNormChart();
}
function doAdd(){
  if(samples.length === 0){ doDraw(); return; }
  const data = POPULATIONS[currentKey].data;
  // 같은 n으로만 추가
  const newOnes = drawSamples(data, n, m);
  samples = samples.concat(newOnes);
  updateEmpiricalStats();
  renderSampleTable();
  drawNormChart();
}
function doClear(){
  samples = [];
  selectedIdx = 0;
  updateEmpiricalStats();
  renderSampleTable();
  renderSelDetail();
  drawPopLine();
  drawNormChart();
}
function selectPreset(key){
  currentKey = key;
  document.querySelectorAll('.preset').forEach(b=>{
    b.classList.toggle('active', b.dataset.key === key);
  });
  samples = [];
  selectedIdx = 0;
  updatePopStats();
  updateTheoryStats();
  updateEmpiricalStats();
  renderSampleTable();
  renderSelDetail();
  drawPopLine();
  drawNormChart();
}

/* ====================== 초기화 ====================== */
function init(){
  updatePopStats();
  updateTheoryStats();
  drawPopLine();
  drawNormChart();
  renderSampleTable();
  // 초기 표본
  doDraw();

  document.querySelectorAll('.preset').forEach(b=>{
    b.addEventListener('click', ()=>selectPreset(b.dataset.key));
  });
  $('nRange').addEventListener('input', e=>{
    n = parseInt(e.target.value);
    $('nVal').textContent = n;
    updateTheoryStats();
    drawNormChart();  // 곡선 즉시 갱신
  });
  $('mRange').addEventListener('input', e=>{
    m = parseInt(e.target.value);
    $('mVal').textContent = m;
  });
  $('btnDraw').addEventListener('click', doDraw);
  $('btnAdd').addEventListener('click', doAdd);
  $('btnClear').addEventListener('click', doClear);

  window.addEventListener('resize', ()=>{
    drawPopLine();
    drawNormChart();
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
    st.subheader("🌟 모평균과 표본평균의 관계 — 두 정규곡선 비교 실험실")
    st.caption(
        "모집단(학생 키 / 시험 점수 / 줄넘기 횟수)에서 표본 m개를 직접 뽑아 "
        "표본평균들의 분포를 **두 정규곡선** N(μ, σ²) ↔ N(μ, σ²/n)와 함께 비교해 봅니다."
    )

    components.html(_HTML, height=2200, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
