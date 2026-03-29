# activities/probability_new/mini/bertrand_paradox_mini.py
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🔮 베르트랑의 역설",
    "description": "무작위의 정의에 따라 확률이 달라지는 역설! 원 안의 현을 세 가지 방법으로 뽑아 확률을 비교합니다.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "베르트랑의역설"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 – 베르트랑의 역설**"},
    {
        "key": "역설설명",
        "label": "세 가지 방법에서 확률이 각각 1/3, 1/2, 1/4로 다르게 나온 이유를 '무작위'의 정의와 관련지어 설명해보세요.",
        "type": "text_area",
        "height": 130,
        "placeholder": "방법마다 '무작위'를 다르게 정의했기 때문에... 방법 1에서는 원호 위에서 균일하게, 방법 2에서는...",
    },
    {
        "key": "어떤방법이맞나",
        "label": "세 가지 방법 중 어느 것이 가장 '자연스러운' 무작위라고 생각하나요? 이유도 함께 써보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "방법 (1/2/3)이 가장 자연스럽다고 생각합니다. 왜냐하면...",
    },
    {
        "key": "중점분포관찰",
        "label": "시뮬레이션 탭에서 '중점 보기'를 켜고 세 방법의 중점 분포를 비교해보세요. 어떤 차이가 보이나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "방법 1의 중점은 원의 가장자리 쪽에 쏠리고..., 방법 3의 중점은 고르게...",
    },
    {
        "key": "통계적확률연결",
        "label": "이 역설이 '통계적 확률'과 어떤 관련이 있을까요? 실험 방법이 다를 때 통계적 확률이 달라지는 상황을 생각해보세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "통계적 확률은 실험의 방법에 따라 달라질 수 있습니다. 예를 들어...",
    },
    {
        "key": "실생활연결",
        "label": "💡 '무작위 추출 방법'이 결과에 영향을 주는 실생활 상황을 써보세요. (예: 여론조사, 실험 설계 등)",
        "type": "text_area",
        "height": 100,
        "placeholder": "여론조사에서 표본을 어떻게 뽑느냐에 따라...",
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점", "label": "💬 느낀 점", "type": "text_area", "height": 90},
]

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>베르트랑의 역설</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0a0f1e 0%,#0f2027 50%,#0a1628 100%);
  color:#e2e8f0;padding:10px;}
.hdr{text-align:center;padding:11px 14px 9px;
  background:linear-gradient(135deg,rgba(167,139,250,.15),rgba(99,102,241,.15));
  border:1px solid rgba(167,139,250,.3);border-radius:12px;margin-bottom:9px;}
.hdr h1{font-size:1.2rem;color:#a78bfa;margin-bottom:3px}
.hdr p{font-size:0.75rem;color:#94a3b8;line-height:1.5}
.hdr strong{color:#e2e8f0}
.tab-bar{display:flex;gap:4px;margin-bottom:9px;overflow-x:auto}
.tab-btn{padding:5px 11px;border-radius:7px;border:1px solid rgba(255,255,255,.15);
  background:transparent;color:#94a3b8;font-size:0.74rem;font-weight:600;
  cursor:pointer;transition:all .2s;white-space:nowrap;flex-shrink:0;}
.tab-btn.on{background:rgba(167,139,250,.25);color:#a78bfa;border-color:#a78bfa}
.tab-panel{display:none}.tab-panel.on{display:block}

/* Method tab */
.mcv{width:320px;height:320px;display:block;margin:0 auto;border-radius:10px;}
.step-nav{display:flex;align-items:center;gap:6px;justify-content:center;margin:8px 0 6px;}
.nbtn{padding:4px 12px;border-radius:6px;border:1px solid rgba(255,255,255,.18);
  background:rgba(167,139,250,.2);color:#c4b5fd;font-size:0.74rem;font-weight:600;cursor:pointer;transition:.15s;}
.nbtn:hover{background:rgba(167,139,250,.38)}
.nbtn:disabled{opacity:.35;cursor:default}
.nbtn.reset{background:rgba(52,211,153,.15);color:#6ee7b7;border-color:rgba(52,211,153,.3)}
.nbtn.reset:hover{background:rgba(52,211,153,.3)}
.scnt{font-size:0.72rem;color:#64748b;min-width:40px;text-align:center}
.scard{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:10px;padding:9px 13px;min-height:120px;}
.stitle{font-size:0.8rem;color:#a78bfa;font-weight:700;margin-bottom:4px}
.stext{font-size:0.74rem;color:#94a3b8;line-height:1.55;white-space:pre-line}
.sform{margin-top:7px;padding:4px 10px;border-radius:6px;
  background:rgba(0,0,0,.35);font-size:0.77rem;color:#c4b5fd;text-align:center;display:block;}

/* Sim tab */
.ctrl{display:flex;align-items:center;gap:6px;flex-wrap:wrap;
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:10px;padding:7px 11px;margin-bottom:8px;}
.ctrl label{font-size:0.73rem;color:#94a3b8}
#nSlider{width:88px;accent-color:#a78bfa}
.ndisp{font-size:0.73rem;color:#a78bfa;font-weight:700;min-width:28px}
.btn{padding:4px 10px;border-radius:6px;border:1px solid rgba(255,255,255,.18);
  background:rgba(167,139,250,.2);color:#c4b5fd;font-size:0.73rem;font-weight:600;cursor:pointer;transition:.15s;}
.btn:hover{background:rgba(167,139,250,.38)}
.btn.cyan{background:rgba(6,182,212,.18);color:#67e8f9;border-color:rgba(6,182,212,.3)}
.btn.cyan:hover{background:rgba(6,182,212,.3)}
.btn.red{background:rgba(239,68,68,.14);color:#fca5a5;border-color:rgba(239,68,68,.3)}
.btn.red:hover{background:rgba(239,68,68,.25)}
.chklbl{display:flex;align-items:center;gap:4px;font-size:0.73rem;color:#94a3b8;cursor:pointer}
.chklbl input{accent-color:#a78bfa}
.cvs{display:flex;gap:6px}
.cvw{flex:1;min-width:0;background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:6px;text-align:center;}
.cvw h3{font-size:0.74rem;margin-bottom:2px}
.cvw .cdesc{font-size:0.64rem;color:#94a3b8;margin-bottom:5px;line-height:1.3;min-height:22px}
.cvw canvas{width:100%;height:auto;border-radius:6px;display:block}
.pbox{margin-top:5px;padding:4px 6px;border-radius:7px;
  background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.06);}
.plbl{font-size:0.61rem;color:#64748b}
.pval{font-size:0.88rem;font-weight:700;margin:1px 0}
.pthy{font-size:0.6rem;color:#475569}
.legend{display:flex;gap:10px;justify-content:center;
  font-size:0.66rem;color:#94a3b8;margin-top:6px;flex-wrap:wrap;}
.ldot{width:10px;height:3px;border-radius:2px;display:inline-block;vertical-align:middle;margin-right:2px}

/* Summary tab */
.ybox{background:linear-gradient(135deg,rgba(251,191,36,.08),rgba(245,158,11,.08));
  border:1px solid rgba(251,191,36,.22);border-radius:10px;
  padding:11px 13px;font-size:0.76rem;line-height:1.6;color:#fde68a;margin-bottom:10px;}
.ybox h4{color:#fbbf24;margin-bottom:4px;font-size:0.86rem}
.scards{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:9px}
.sc{flex:1;min-width:170px;background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:10px;}
.sc h4{font-size:0.77rem;margin-bottom:5px}
.sc p{font-size:0.71rem;color:#94a3b8;line-height:1.5}
.scf{margin-top:6px;padding:4px 8px;border-radius:6px;
  background:rgba(0,0,0,.3);font-size:0.76rem;color:#c4b5fd;text-align:center;}
.purpbox{background:linear-gradient(135deg,rgba(167,139,250,.1),rgba(99,102,241,.1));
  border:1px solid rgba(167,139,250,.25);border-radius:10px;padding:10px 13px;
  font-size:0.75rem;line-height:1.6;}
.purpbox h4{color:#a78bfa;margin-bottom:4px;font-size:0.84rem}
.chips{display:flex;gap:5px;margin-top:7px;flex-wrap:wrap}
.chip{padding:3px 9px;border-radius:14px;font-size:0.69rem;font-weight:700}
</style>
</head>
<body>

<div class="hdr">
  <h1>🔮 베르트랑의 역설</h1>
  <p><strong>원의 내접 정삼각형의 한 변보다 긴 현을 무작위로 그을 확률은?</strong><br>
  1/3? 1/2? 1/4? — 셋 모두 맞습니다. "무작위"의 정의에 따라 답이 달라집니다!</p>
</div>

<div class="tab-bar">
  <button class="tab-btn on"  onclick="T(this,'m0')">🟣 방법 1</button>
  <button class="tab-btn"     onclick="T(this,'m1')">🔵 방법 2</button>
  <button class="tab-btn"     onclick="T(this,'m2')">🟢 방법 3</button>
  <button class="tab-btn"     onclick="T(this,'sim')">🎲 시뮬레이션</button>
  <button class="tab-btn"     onclick="T(this,'sum')">📌 정리</button>
</div>

<!-- ── 방법 1 ── -->
<div id="tab-m0" class="tab-panel on">
  <canvas id="mc0" class="mcv" width="320" height="320"></canvas>
  <div class="step-nav">
    <button class="nbtn" id="pb0" onclick="prev(0)">← 이전</button>
    <span class="scnt" id="sc0">1 / 5</span>
    <button class="nbtn" id="nb0" onclick="next(0)">다음 →</button>
    <button class="nbtn reset" onclick="reset(0)">🔀 새로 시도</button>
  </div>
  <div class="scard">
    <div class="stitle" id="st0"></div>
    <div class="stext"  id="sx0"></div>
    <span class="sform" id="sf0"></span>
  </div>
</div>

<!-- ── 방법 2 ── -->
<div id="tab-m1" class="tab-panel">
  <canvas id="mc1" class="mcv" width="320" height="320"></canvas>
  <div class="step-nav">
    <button class="nbtn" id="pb1" onclick="prev(1)">← 이전</button>
    <span class="scnt" id="sc1">1 / 5</span>
    <button class="nbtn" id="nb1" onclick="next(1)">다음 →</button>
    <button class="nbtn reset" onclick="reset(1)">🔀 새로 시도</button>
  </div>
  <div class="scard">
    <div class="stitle" id="st1"></div>
    <div class="stext"  id="sx1"></div>
    <span class="sform" id="sf1"></span>
  </div>
</div>

<!-- ── 방법 3 ── -->
<div id="tab-m2" class="tab-panel">
  <canvas id="mc2" class="mcv" width="320" height="320"></canvas>
  <div class="step-nav">
    <button class="nbtn" id="pb2" onclick="prev(2)">← 이전</button>
    <span class="scnt" id="sc2">1 / 4</span>
    <button class="nbtn" id="nb2" onclick="next(2)">다음 →</button>
    <button class="nbtn reset" onclick="reset(2)">🔀 새로 시도</button>
  </div>
  <div class="scard">
    <div class="stitle" id="st2"></div>
    <div class="stext"  id="sx2"></div>
    <span class="sform" id="sf2"></span>
  </div>
</div>

<!-- ── 시뮬레이션 ── -->
<div id="tab-sim" class="tab-panel">
  <div class="ctrl">
    <label>시행 수</label>
    <input type="range" id="nSlider" min="100" max="2000" step="100" value="600"
           oninput="document.getElementById('nd').textContent=this.value">
    <span class="ndisp" id="nd">600</span>
    <button class="btn" onclick="runAll()">▶ 실행</button>
    <button class="btn cyan" id="animBtn" onclick="toggleAnim()">🎞 애니메이션</button>
    <button class="btn red" onclick="clearAll()">🗑 지우기</button>
    <label class="chklbl"><input type="checkbox" id="showMid" onchange="redrawSim()">중점 보기</label>
  </div>
  <div class="cvs">
    <div class="cvw">
      <h3 style="color:#a78bfa">🟣 방법 1</h3>
      <p class="cdesc">두 점 선택</p>
      <canvas id="sc0c" width="155" height="155"></canvas>
      <div class="pbox"><div class="plbl">실험 확률</div>
        <div class="pval" id="pv0" style="color:#a78bfa">—</div>
        <div class="pthy">이론: 1/3 ≈ 0.333</div></div>
    </div>
    <div class="cvw">
      <h3 style="color:#06b6d4">🔵 방법 2</h3>
      <p class="cdesc">지름 위 점</p>
      <canvas id="sc1c" width="155" height="155"></canvas>
      <div class="pbox"><div class="plbl">실험 확률</div>
        <div class="pval" id="pv1" style="color:#06b6d4">—</div>
        <div class="pthy">이론: 1/2 = 0.500</div></div>
    </div>
    <div class="cvw">
      <h3 style="color:#34d399">🟢 방법 3</h3>
      <p class="cdesc">원 내부 점</p>
      <canvas id="sc2c" width="155" height="155"></canvas>
      <div class="pbox"><div class="plbl">실험 확률</div>
        <div class="pval" id="pv2" style="color:#34d399">—</div>
        <div class="pthy">이론: 1/4 = 0.250</div></div>
    </div>
  </div>
  <div class="legend">
    <span><span class="ldot" style="background:#ef4444"></span>긴 현 (> R√3)</span>
    <span><span class="ldot" style="background:#475569"></span>짧은 현</span>
    <span><span class="ldot" style="background:#ef444466;border:1px dashed #ef4444"></span>내접원 경계 (R/2)</span>
  </div>
</div>

<!-- ── 정리 ── -->
<div id="tab-sum" class="tab-panel">
  <div class="ybox">
    <h4>⚡ 베르트랑의 역설이란?</h4>
    1889년 조제프 베르트랑이 제기한 문제입니다.<br>
    <strong>같은 질문에 세 가지 방법이 모두 수학적으로 올바르지만, 서로 다른 확률을 줍니다.</strong><br>
    역설의 원인: "무작위"의 정의가 달라지면 확률 공간이 달라집니다.<br>
    교훈: <strong>확률을 말할 때는 반드시 확률 공간(표본 공간 + 분포)을 명확히 해야 합니다.</strong>
  </div>
  <div class="scards">
    <div class="sc">
      <h4 style="color:#a78bfa">🟣 방법 1 — 원호 균일</h4>
      <p>A 선택 → A를 꼭짓점으로 하는 삼각형 결정<br>
      B가 '유리한 호'(120°) 안에 있으면 긴 현<br>
      유리한 호 120° = 전체 360°의 1/3</p>
      <div class="scf">P₁ = 120°/360° = 1/3 ≈ 0.333</div>
    </div>
    <div class="sc">
      <h4 style="color:#06b6d4">🔵 방법 2 — 지름 균일 선택</h4>
      <p>P, Q를 꼭짓점으로 하는 두 내접 정삼각형의<br>
      맞은편 변이 지름을 1:2:1로 분할<br>
      중간 구간(= R)에 M이 있으면 긴 현<br>
      구간 비율: 1/4 + 1/2 + 1/4 = 2R</p>
      <div class="scf">P₂ = R / 2R = 1/2 = 0.500</div>
    </div>
    <div class="sc">
      <h4 style="color:#34d399">🟢 방법 3 — 면적 균일</h4>
      <p>원 내부의 점을 면적에 대해 균일하게 선택<br>
      |OM| &lt; R/2이면 긴 현<br>
      중점: 원판 전체에 균일 분포</p>
      <div class="scf">P₃ = 1/4 = 0.250</div>
    </div>
  </div>
  <div class="purpbox">
    <h4>🔑 핵심 통찰: 중점 분포가 다르다!</h4>
    어떤 방법이든 <strong>현이 길다 ⟺ 중점이 내접원(반지름 R/2) 안에 있다</strong>는 조건은 같습니다.<br>
    차이는 <strong>중점이 어떻게 분포하느냐</strong>입니다. 시뮬레이션에서 '중점 보기'로 확인해보세요!
    <div class="chips">
      <span class="chip" style="background:rgba(167,139,250,.2);color:#a78bfa">방법1 → 가장자리 쏠림</span>
      <span class="chip" style="background:rgba(6,182,212,.2);color:#06b6d4">방법2 → 지름 균일</span>
      <span class="chip" style="background:rgba(52,211,153,.2);color:#34d399">방법3 → 면적 균일</span>
    </div>
  </div>
</div>

<script>
// ── 상수 ──
const MR=115, MCX=160, MCY=160;       // method canvas
const SR=72,  SCX=77,  SCY=77;        // sim canvas
const MSIDE=MR*Math.sqrt(3), SSIDE=SR*Math.sqrt(3);

// ── 단계 텍스트 ──
const STEPS=[
  [ // 방법 1 (5단계)
    {t:"원 그리기",
     x:"반지름 R인 원을 그립니다.\n빨간 점선은 내접원(반지름 R/2)입니다.\n\n목표: 내접 정삼각형의 한 변(길이 R√3)보다\n긴 현을 그을 확률은?",
     f:"P(현 길이 > R√3) = ?"},
    {t:"점 A 선택 → 정삼각형 결정",
     x:"원 위의 점 A를 균일하게 선택합니다.\nA를 한 꼭짓점으로 하는 정삼각형을 그립니다.\n나머지 두 꼭짓점 B₁, B₂가 결정됩니다.",
     f:"A에서 B₁, B₂까지 거리 = R√3 (정삼각형 한 변)"},
    {t:"긴 현이 되는 조건",
     x:"B가 호 B₁B₂ (A를 포함하지 않는 초록 호) 안에 있으면\n현 AB의 길이 > R√3이 됩니다!\n\n이 '유리한 호'는 원 전체(360°)의 1/3 = 120°입니다.",
     f:"유리한 호(초록) = 120° = 전체의 1/3"},
    {t:"점 B 선택 → 현 완성",
     x:"B를 원 위에서 균일하게 선택합니다.\nB가 초록 호 안에 있으면 → 긴 현 🔴\nB가 초록 호 밖에 있으면 → 짧은 현 ⚫",
     f:"B가 유리한 호 안  ⟺  긴 현"},
    {t:"확률 계산",
     x:"B는 원 위 어디에나 균일하게 선택됩니다.\n유리한 호(초록, 1) : 불리한 호(회색, 1+1) = 1 : 2\n\n따라서 확률 = 1/(1+2) = 1/3",
     f:"P₁ = 120° / 360° = 1/3 ≈ 0.333"},
  ],
  [ // 방법 2 (5단계)
    {t:"원 그리기",
     x:"반지름 R인 원을 그립니다.\n빨간 점선은 내접원(반지름 R/2)입니다.\n\n목표: 내접 정삼각형의 한 변(길이 R√3)보다\n긴 현을 그을 확률은?",
     f:"P(현 길이 > R√3) = ?"},
    {t:"지름 P-Q 그리기",
     x:"원의 중심을 지나는 지름 P-Q를 그립니다.\n이 지름 위에서 점 M을 균일하게 선택할 것입니다.",
     f:"지름의 길이 = 2R"},
    {t:"경계 현 그리기 (삼각형의 변)",
     x:"P를 꼭짓점으로 하는 내접 정삼각형과\nQ를 꼭짓점으로 하는 내접 정삼각형을 그립니다.\n\n두 삼각형의 맞은편 변은 지름과 수직이며,\n각각 중심으로부터 R/2 거리에 위치합니다.\n\n→ 두 변 사이(녹색 구간): 긴 현  ·  두 변 바깥(회색 구간): 짧은 현",
     f:"두 경계 현의 길이 = R√3 (내접 정삼각형의 변 길이)"},
    {t:"점 M 선택 → 현 완성",
     x:"지름 P-Q 위에서 점 M을 균일하게 선택합니다.\nM에서 지름과 수직인 현을 그립니다.\n\n• M이 두 변 사이(녹색 구간)에 있으면 → 긴 현 🔴\n• M이 두 변 바깥(회색 구간)에 있으면 → 짧은 현 ⚫",
     f:"M이 녹색 구간 내  ⟺  긴 현"},
    {t:"확률 계산",
     x:"지름 P-Q의 전체 길이 = 2R\n두 경계 변 사이(녹색 구간)의 길이 = R\n\n따라서 확률 = 녹색 구간 / 전체 지름 = R / 2R",
     f:"P₂ = R / 2R = 1/2 = 0.500"},
  ],
  [ // 방법 3 (4단계)
    {t:"원과 내접 정삼각형",
     x:"같은 원입니다. 이번엔 원 내부의 점으로 현을 정의합니다.",
     f:"P(현 길이 > R√3) = ?"},
    {t:"원 내부 점 M 선택",
     x:"원 내부에서 점 M을 면적에 대해 균일하게 선택합니다.\n어느 넓이 영역이나 동일한 확률을 가집니다.\n(단순히 r을 균일하게 뽑으면 안 됩니다!)",
     f:"M ~ Uniform distribution on disk"},
    {t:"현 완성 + 조건 확인",
     x:"M을 중점으로 하는 현을 그립니다 (OM에 수직).\n현의 길이 = 2√(R²−|OM|²)\n\n긴 현 조건: |OM| < R/2  →  M이 내접원 안!",
     f:"|OM| < R/2  ⟺  현 길이 > R√3"},
    {t:"확률 계산",
     x:"M이 원판 전체에 균일하므로,\n확률 = 내접원 넓이 / 원 넓이 = 넓이의 비율!",
     f:"P₃ = π(R/2)² / πR² = 1/4 = 0.250"},
  ],
];
const MAXSTEP=[5,5,4];

// ── Method 상태 ──
let mStep=[1,1,1];
let mData=[null,null,null];
const M_CVS=[0,1,2].map(i=>document.getElementById('mc'+i));
const M_CTX=M_CVS.map(c=>c.getContext('2d'));

function initData(m){
  if(m===0){
    mData[m]={a1:Math.random()*2*Math.PI, a2:Math.random()*2*Math.PI};
  } else if(m===1){
    mData[m]={mx:(Math.random()*2-1)*MR};
  } else {
    const ang=Math.random()*2*Math.PI;
    const d=MR*Math.sqrt(Math.random());
    mData[m]={ang, d};
  }
}

// ── 베이스 그리기 (원 + 내접원 점선만; 삼각형은 각 메서드에서 동적으로) ──
function drawBase(ctx, r, cx, cy){
  ctx.fillStyle='#0b1220';
  ctx.fillRect(0,0,ctx.canvas.width,ctx.canvas.height);
  ctx.save(); ctx.translate(cx,cy);
  // 내접원 (반지름 r/2, 빨간 점선)
  ctx.setLineDash([4,4]); ctx.strokeStyle='rgba(239,68,68,0.38)'; ctx.lineWidth=1.5;
  ctx.beginPath(); ctx.arc(0,0,r/2,0,2*Math.PI); ctx.stroke();
  // 원
  ctx.setLineDash([]); ctx.strokeStyle='rgba(226,232,240,0.6)'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.arc(0,0,r,0,2*Math.PI); ctx.stroke();
  ctx.restore();
}

function glow(ctx,x,y,r,col){
  const rgb=hexRgb(col);
  ctx.fillStyle=`rgba(${rgb},0.22)`;
  ctx.beginPath(); ctx.arc(x,y,r*2.3,0,2*Math.PI); ctx.fill();
  ctx.fillStyle=col;
  ctx.beginPath(); ctx.arc(x,y,r,0,2*Math.PI); ctx.fill();
}
function hexRgb(h){
  const r=parseInt(h.slice(1,3),16),g=parseInt(h.slice(3,5),16),b=parseInt(h.slice(5,7),16);
  return `${r},${g},${b}`;
}
function lbl(ctx,x,y,text,col){
  ctx.font='bold 11px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
  const w=ctx.measureText(text).width+6;
  ctx.fillStyle='rgba(0,0,0,0.7)'; ctx.fillRect(x-w/2,y-7,w,14);
  ctx.fillStyle=col; ctx.fillText(text,x,y);
}

// ── 방법별 단계 그리기 ──
function drawM0(ctx,step){
  const {a1,a2}=mData[0];
  const p1=[MR*Math.cos(a1),MR*Math.sin(a1)];
  const p2=[MR*Math.cos(a2),MR*Math.sin(a2)];
  const isLong=Math.hypot(p2[0]-p1[0],p2[1]-p1[1])>MSIDE;
  // A를 꼭짓점으로 하는 삼각형의 나머지 두 꼭짓점
  const v1a=a1+2*Math.PI/3, v2a=a1+4*Math.PI/3;
  const tv1=[MR*Math.cos(v1a),MR*Math.sin(v1a)];
  const tv2=[MR*Math.cos(v2a),MR*Math.sin(v2a)];

  drawBase(ctx,MR,MCX,MCY);
  ctx.save(); ctx.translate(MCX,MCY);

  // step 1: 원만 (base에서 이미 그림)

  if(step>=2){
    // A점 + A를 꼭짓점으로 하는 정삼각형
    ctx.strokeStyle='rgba(99,102,241,0.6)'; ctx.lineWidth=1.5; ctx.setLineDash([]);
    ctx.beginPath(); ctx.moveTo(p1[0],p1[1]); ctx.lineTo(tv1[0],tv1[1]); ctx.lineTo(tv2[0],tv2[1]); ctx.closePath(); ctx.stroke();
    // 나머지 꼭짓점 B₁, B₂
    glow(ctx,tv1[0],tv1[1],4,'#818cf8');
    glow(ctx,tv2[0],tv2[1],4,'#818cf8');
    lbl(ctx,tv1[0]+radOff(tv1,0),tv1[1]+radOff(tv1,1),'B₁','#a5b4fc');
    lbl(ctx,tv2[0]+radOff(tv2,0),tv2[1]+radOff(tv2,1),'B₂','#a5b4fc');
    // A점
    glow(ctx,p1[0],p1[1],6,'#fbbf24');
    lbl(ctx,p1[0]+radOff(p1,0),p1[1]+radOff(p1,1),'A','#fbbf24');
  }

  if(step>=3){
    // 유리한 호: B₁ → B₂ (A를 포함하지 않는 120° 호) 강조
    ctx.strokeStyle='rgba(52,211,153,0.9)'; ctx.lineWidth=6; ctx.setLineDash([]);
    ctx.beginPath(); ctx.arc(0,0,MR,v1a,v2a); ctx.stroke();
    // 호 라벨
    const mAng=a1+Math.PI;
    ctx.fillStyle='#34d399'; ctx.font='bold 10px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('유리한 호',(MR+20)*Math.cos(mAng),(MR+20)*Math.sin(mAng));
    ctx.fillText('(120°)',(MR+20)*Math.cos(mAng),(MR+20)*Math.sin(mAng)+13);
  }

  if(step>=4){
    // B점 + 현
    glow(ctx,p2[0],p2[1],6,isLong?'#ef4444':'#94a3b8');
    lbl(ctx,p2[0]+radOff(p2,0),p2[1]+radOff(p2,1),'B',isLong?'#fca5a5':'#94a3b8');
    ctx.strokeStyle=isLong?'rgba(239,68,68,0.22)':'rgba(148,163,184,0.18)';
    ctx.lineWidth=7; ctx.setLineDash([]);
    ctx.beginPath(); ctx.moveTo(p1[0],p1[1]); ctx.lineTo(p2[0],p2[1]); ctx.stroke();
    ctx.strokeStyle=isLong?'#ef4444':'#94a3b8'; ctx.lineWidth=2.5;
    ctx.beginPath(); ctx.moveTo(p1[0],p1[1]); ctx.lineTo(p2[0],p2[1]); ctx.stroke();
    ctx.fillStyle=isLong?'#ef4444':'#94a3b8'; ctx.font='bold 12px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(isLong?'✓ 긴 현!':'✗ 짧은 현',0,MR+18);
  }

  if(step>=5){
    // 확률 시각화: 안쪽 작은 원 위에 세 호를 1:1:1로 표시
    const arcR=MR*0.36;
    // 불리한 두 호 (A~B₁, B₂~A) → 회색
    ctx.strokeStyle='rgba(148,163,184,0.45)'; ctx.lineWidth=5;
    ctx.beginPath(); ctx.arc(0,0,arcR,a1,v1a);       ctx.stroke(); // A→B₁
    ctx.beginPath(); ctx.arc(0,0,arcR,v2a,a1+2*Math.PI); ctx.stroke(); // B₂→A
    // 유리한 호 (B₁~B₂) → 초록
    ctx.strokeStyle='rgba(52,211,153,0.75)'; ctx.lineWidth=5;
    ctx.beginPath(); ctx.arc(0,0,arcR,v1a,v2a); ctx.stroke();
    // 호 비율 레이블
    ctx.font='bold 10px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillStyle='#6ee7b7';
    ctx.fillText('1',(arcR+13)*Math.cos(a1+Math.PI),(arcR+13)*Math.sin(a1+Math.PI));
    ctx.fillStyle='#94a3b8';
    ctx.fillText('1',(arcR+13)*Math.cos(a1+Math.PI/3),(arcR+13)*Math.sin(a1+Math.PI/3));
    ctx.fillText('1',(arcR+13)*Math.cos(a1+5*Math.PI/3),(arcR+13)*Math.sin(a1+5*Math.PI/3));
  }
  ctx.restore();
}

function radOff(p,axis){
  const len=Math.hypot(p[0],p[1])||1;
  return (p[axis]/len)*17;
}

function drawM1(ctx,step){
  const {mx}=mData[1];
  const isLong=Math.abs(mx)<MR/2;
  const h=MR*Math.sqrt(3)/2;  // 내접 정삼각형 변의 반높이
  const half=Math.sqrt(Math.max(0,MR*MR-mx*mx));  // 수직 현의 반길이
  drawBase(ctx,MR,MCX,MCY);
  ctx.save(); ctx.translate(MCX,MCY);

  // step 2+: 수평 지름 P-Q
  if(step>=2){
    ctx.strokeStyle='rgba(248,113,113,0.7)'; ctx.lineWidth=2; ctx.setLineDash([]);
    ctx.beginPath(); ctx.moveTo(-MR,0); ctx.lineTo(MR,0); ctx.stroke();
    // 화살표 (Q 방향)
    ctx.beginPath();
    ctx.moveTo(MR,0); ctx.lineTo(MR-10,-5); ctx.moveTo(MR,0); ctx.lineTo(MR-10,5);
    ctx.stroke();
    glow(ctx,-MR,0,5,'#fbbf24'); glow(ctx,MR,0,5,'#fbbf24');
    lbl(ctx,-MR-16,0,'P','#fbbf24'); lbl(ctx,MR+16,0,'Q','#fbbf24');
  }

  // step 3+: 두 내접 정삼각형 + 경계 현 + 구간 색상
  if(step>=3){
    // P(-MR,0)을 꼭짓점으로 하는 정삼각형 (점선)
    ctx.strokeStyle='rgba(99,102,241,0.32)'; ctx.lineWidth=1.2; ctx.setLineDash([5,4]);
    ctx.beginPath();
    ctx.moveTo(-MR,0); ctx.lineTo(MR/2,h); ctx.lineTo(MR/2,-h); ctx.closePath();
    ctx.stroke();
    // Q(MR,0)을 꼭짓점으로 하는 정삼각형 (점선)
    ctx.beginPath();
    ctx.moveTo(MR,0); ctx.lineTo(-MR/2,h); ctx.lineTo(-MR/2,-h); ctx.closePath();
    ctx.stroke();
    ctx.setLineDash([]);

    // 왼쪽 경계 현 x=-MR/2 (파란색 실선)
    ctx.strokeStyle='rgba(6,182,212,0.9)'; ctx.lineWidth=2.5;
    ctx.beginPath(); ctx.moveTo(-MR/2,-h); ctx.lineTo(-MR/2,h); ctx.stroke();
    // 오른쪽 경계 현 x=+MR/2 (파란색 실선)
    ctx.beginPath(); ctx.moveTo(MR/2,-h); ctx.lineTo(MR/2,h); ctx.stroke();

    // 지름 위 세 구간 색상 표시 (경계 현 위에 덮기)
    // 왼쪽 바깥 구간: P ~ 왼쪽 경계 (회색)
    ctx.strokeStyle='rgba(148,163,184,0.65)'; ctx.lineWidth=5;
    ctx.beginPath(); ctx.moveTo(-MR,0); ctx.lineTo(-MR/2,0); ctx.stroke();
    // 중간 구간: 두 경계 사이 (초록)
    ctx.strokeStyle='rgba(52,211,153,0.85)'; ctx.lineWidth=5;
    ctx.beginPath(); ctx.moveTo(-MR/2,0); ctx.lineTo(MR/2,0); ctx.stroke();
    // 오른쪽 바깥 구간: 오른쪽 경계 ~ Q (회색)
    ctx.strokeStyle='rgba(148,163,184,0.65)'; ctx.lineWidth=5;
    ctx.beginPath(); ctx.moveTo(MR/2,0); ctx.lineTo(MR,0); ctx.stroke();

    // 구간 라벨
    ctx.font='bold 9px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillStyle='#6ee7b7'; ctx.fillText('R (1/2)',0,15);
    ctx.fillStyle='#94a3b8';
    ctx.fillText('R/2',-MR*0.75,15); ctx.fillText('R/2',MR*0.75,15);
    // 경계 현 거리 라벨
    ctx.fillStyle='#67e8f9'; ctx.font='9px sans-serif';
    ctx.fillText('R/2',-MR/2,-h-9); ctx.fillText('R/2',MR/2,-h-9);
  }

  // step 4+: 점 M 선택 + 수직 현
  if(step>=4){
    // 수직 현
    ctx.strokeStyle=isLong?'rgba(239,68,68,0.22)':'rgba(148,163,184,0.18)';
    ctx.lineWidth=7; ctx.setLineDash([]);
    ctx.beginPath(); ctx.moveTo(mx,-half); ctx.lineTo(mx,half); ctx.stroke();
    ctx.strokeStyle=isLong?'#ef4444':'#94a3b8'; ctx.lineWidth=2.5;
    ctx.beginPath(); ctx.moveTo(mx,-half); ctx.lineTo(mx,half); ctx.stroke();
    // 직각 표시
    const s=8;
    ctx.strokeStyle='rgba(255,255,255,0.28)'; ctx.lineWidth=1;
    ctx.beginPath();
    ctx.moveTo(mx+s,0); ctx.lineTo(mx+s,s); ctx.lineTo(mx,s); ctx.stroke();
    // M 점
    glow(ctx,mx,0,6,'#06b6d4');
    lbl(ctx,mx+(mx>0?14:-14),-15,'M','#67e8f9');
    // 결과 텍스트
    ctx.fillStyle=isLong?'#ef4444':'#94a3b8';
    ctx.font='bold 12px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(isLong?'✓ 중간 구간 → 긴 현!':'✗ 바깥 구간 → 짧은 현',0,MR+18);
  }

  // step 5+: 확률 시각화 바
  if(step>=5){
    const barY=MR*0.82, bW=MR*0.82;
    ctx.strokeStyle='rgba(148,163,184,0.55)'; ctx.lineWidth=6;
    ctx.beginPath(); ctx.moveTo(-bW,-barY); ctx.lineTo(-bW/2,-barY); ctx.stroke();
    ctx.strokeStyle='rgba(52,211,153,0.8)';
    ctx.beginPath(); ctx.moveTo(-bW/2,-barY); ctx.lineTo(bW/2,-barY); ctx.stroke();
    ctx.strokeStyle='rgba(148,163,184,0.55)';
    ctx.beginPath(); ctx.moveTo(bW/2,-barY); ctx.lineTo(bW,-barY); ctx.stroke();
    ctx.font='bold 10px sans-serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillStyle='#6ee7b7'; ctx.fillText('1/2',0,-barY-11);
    ctx.fillStyle='#94a3b8';
    ctx.fillText('1/4',-bW*0.75,-barY-11); ctx.fillText('1/4',bW*0.75,-barY-11);
  }

  ctx.restore();
}

function drawM2(ctx,step){
  const {ang,d}=mData[2];
  const mid=[d*Math.cos(ang),d*Math.sin(ang)];
  const half=Math.sqrt(Math.max(0,MR*MR-d*d));
  const dx=-Math.sin(ang),dy=Math.cos(ang);
  const p1=[mid[0]+dx*half,mid[1]+dy*half];
  const p2=[mid[0]-dx*half,mid[1]-dy*half];
  const isLong=d<MR/2;
  drawBase(ctx,MR,MCX,MCY);
  ctx.save(); ctx.translate(MCX,MCY);
  if(step>=2){
    ctx.fillStyle='rgba(52,211,153,0.04)'; ctx.beginPath(); ctx.arc(0,0,MR,0,2*Math.PI); ctx.fill();
    glow(ctx,mid[0],mid[1],6,'#34d399');
    lbl(ctx,mid[0]+12,mid[1]-12,'M','#6ee7b7');
    ctx.strokeStyle='rgba(52,211,153,0.32)'; ctx.lineWidth=1; ctx.setLineDash([3,3]);
    ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(mid[0],mid[1]); ctx.stroke(); ctx.setLineDash([]);
  }
  if(step>=3){
    ctx.strokeStyle=isLong?'rgba(239,68,68,0.22)':'rgba(148,163,184,0.18)';
    ctx.lineWidth=7; ctx.setLineDash([]);
    ctx.beginPath(); ctx.moveTo(p1[0],p1[1]); ctx.lineTo(p2[0],p2[1]); ctx.stroke();
    ctx.strokeStyle=isLong?'#ef4444':'#94a3b8'; ctx.lineWidth=2.5;
    ctx.beginPath(); ctx.moveTo(p1[0],p1[1]); ctx.lineTo(p2[0],p2[1]); ctx.stroke();
    if(d>8){const s=8,nx=Math.cos(ang),ny=Math.sin(ang);
      ctx.strokeStyle='rgba(255,255,255,0.28)'; ctx.lineWidth=1;
      ctx.beginPath();
      ctx.moveTo(mid[0]+nx*s,mid[1]+ny*s);
      ctx.lineTo(mid[0]+nx*s+dx*s,mid[1]+ny*s+dy*s);
      ctx.lineTo(mid[0]+dx*s,mid[1]+dy*s); ctx.stroke();}
    ctx.strokeStyle=isLong?'rgba(239,68,68,0.75)':'rgba(148,163,184,0.5)';
    ctx.lineWidth=2; ctx.setLineDash([3,3]);
    ctx.beginPath(); ctx.arc(0,0,MR/2,0,2*Math.PI); ctx.stroke(); ctx.setLineDash([]);
    if(isLong){ctx.fillStyle='rgba(239,68,68,0.07)'; ctx.beginPath(); ctx.arc(0,0,MR/2,0,2*Math.PI); ctx.fill();}
  }
  if(step>=4){
    ctx.fillStyle=isLong?'#ef4444':'#94a3b8'; ctx.font='bold 12px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(isLong?'✓ |OM| < R/2 → 긴 현!':'✗ |OM| ≥ R/2 → 짧은 현',0,MR+18);
  }
  ctx.restore();
}

const DRAWFN=[drawM0,drawM1,drawM2];

function updateMethod(m){
  const s=STEPS[m][mStep[m]-1];
  document.getElementById('st'+m).textContent=s.t;
  document.getElementById('sx'+m).textContent=s.x;
  document.getElementById('sf'+m).textContent=s.f;
  document.getElementById('sc'+m).textContent=`${mStep[m]} / ${MAXSTEP[m]}`;
  document.getElementById('pb'+m).disabled=(mStep[m]<=1);
  document.getElementById('nb'+m).disabled=(mStep[m]>=MAXSTEP[m]);
  DRAWFN[m](M_CTX[m],mStep[m]);
}

function next(m){if(mStep[m]<MAXSTEP[m]){mStep[m]++;updateMethod(m);}}
function prev(m){if(mStep[m]>1){mStep[m]--;updateMethod(m);}}
function reset(m){initData(m);mStep[m]=1;updateMethod(m);}

// ── 시뮬레이션 ──
const S_CVS=[0,1,2].map(i=>document.getElementById('sc'+i+'c'));
const S_CTX=S_CVS.map(c=>c.getContext('2d'));
let sData=[{l:0,t:0,ch:[]},{l:0,t:0,ch:[]},{l:0,t:0,ch:[]}];
let animRun=false, animId=null;

function genChord(m){
  let p1,p2,mid;
  if(m===0){
    const a1=Math.random()*2*Math.PI, a2=Math.random()*2*Math.PI;
    p1=[SR*Math.cos(a1),SR*Math.sin(a1)]; p2=[SR*Math.cos(a2),SR*Math.sin(a2)];
    mid=[(p1[0]+p2[0])/2,(p1[1]+p2[1])/2];
  } else {
    const ang=Math.random()*2*Math.PI;
    const d=(m===1)?Math.random()*SR:SR*Math.sqrt(Math.random());
    mid=[d*Math.cos(ang),d*Math.sin(ang)];
    const half=Math.sqrt(Math.max(0,SR*SR-d*d));
    const dx=-Math.sin(ang),dy=Math.cos(ang);
    p1=[mid[0]+dx*half,mid[1]+dy*half]; p2=[mid[0]-dx*half,mid[1]-dy*half];
  }
  const isLong=Math.hypot(p2[0]-p1[0],p2[1]-p1[1])>SSIDE;
  return {p1,p2,mid,isLong};
}

function drawSim(i){
  const ctx=S_CTX[i]; const d=sData[i];
  const showMid=document.getElementById('showMid').checked;
  drawBase(ctx,SR,SCX,SCY);
  ctx.save(); ctx.translate(SCX,SCY);
  for(const ch of d.ch){
    if(showMid){
      ctx.fillStyle=ch.isLong?'rgba(239,68,68,0.75)':'rgba(148,163,184,0.38)';
      ctx.beginPath(); ctx.arc(ch.mid[0],ch.mid[1],1.5,0,2*Math.PI); ctx.fill();
    } else {
      ctx.strokeStyle=ch.isLong?'rgba(239,68,68,0.42)':'rgba(100,116,139,0.22)';
      ctx.lineWidth=0.7; ctx.setLineDash([]);
      ctx.beginPath(); ctx.moveTo(ch.p1[0],ch.p1[1]); ctx.lineTo(ch.p2[0],ch.p2[1]); ctx.stroke();
    }
  }
  ctx.restore();
  const el=document.getElementById('pv'+i);
  if(d.t===0){el.textContent='—';return;}
  el.textContent=`${(d.l/d.t).toFixed(3)}  (${d.l}/${d.t})`;
}
function redrawSim(){S_CTX.forEach((_,i)=>drawSim(i));}

function addCh(i,ch){sData[i].ch.push(ch);sData[i].t++;if(ch.isLong)sData[i].l++;}

function runAll(){
  stopAnim();
  const n=+document.getElementById('nSlider').value;
  sData=[{l:0,t:0,ch:[]},{l:0,t:0,ch:[]},{l:0,t:0,ch:[]}];
  for(let j=0;j<n;j++){addCh(0,genChord(0));addCh(1,genChord(1));addCh(2,genChord(2));}
  redrawSim();
}
function clearAll(){
  stopAnim();
  sData=[{l:0,t:0,ch:[]},{l:0,t:0,ch:[]},{l:0,t:0,ch:[]}];
  redrawSim();
}
function toggleAnim(){animRun?stopAnim():startAnim();}
function startAnim(){
  sData=[{l:0,t:0,ch:[]},{l:0,t:0,ch:[]},{l:0,t:0,ch:[]}];
  animRun=true; document.getElementById('animBtn').textContent='⏹ 멈추기';
  let step=0; const maxN=+document.getElementById('nSlider').value;
  const batch=Math.max(1,Math.ceil(maxN/100));
  function frame(){
    if(!animRun)return;
    for(let k=0;k<batch;k++){addCh(0,genChord(0));addCh(1,genChord(1));addCh(2,genChord(2));step++;}
    redrawSim();
    if(step<maxN)animId=setTimeout(frame,16); else stopAnim();
  }
  frame();
}
function stopAnim(){
  animRun=false; clearTimeout(animId);
  document.getElementById('animBtn').textContent='🎞 애니메이션';
}

// ── 탭 전환 ──
function T(btn,name){
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('on'));
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('on'));
  document.getElementById('tab-'+name).classList.add('on');
  btn.classList.add('on');
}

// ── 초기화 ──
[0,1,2].forEach(m=>{initData(m);updateMethod(m);});
S_CTX.forEach((_,i)=>drawSim(i));
</script>
</body>
</html>
"""


def render():
    components.html(_HTML, height=770, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
