# activities/probability_new/mini/buffon_needle_mini.py
"""
뷔퐁의 바늘 실험 미니활동 (개선판)
- 직선·V자·W자·원 등 다양한 형태로 시뮬레이션
- 원리 설명 탭(교차 조건·적분·뷔퐁 국수 정리) 포함
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🪡 뷔퐁의 바늘 실험",
    "description": "평행선에 바늘·V자·원 등을 던져 π를 추정. 원리 설명 탭과 다양한 모양 지원.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "뷔퐁의바늘미니"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 – 뷔퐁의 바늘 실험**"},
    {
        "key": "공식이해",
        "label": "교차 확률 공식 P = 2L/(π·d)가 어떻게 성립하는지 설명해 보세요. '원리 설명' 탭을 참고하여 적분 과정을 포함해서 설명하면 좋습니다.",
        "type": "text_area",
        "height": 130,
        "placeholder": "θ와 D가 각각 균일하게 분포할 때, 교차 조건 D ≤ (L/2)sinθ를 이용하면..."
    },
    {
        "key": "수렴관찰",
        "label": "시행 횟수를 늘릴수록 π 추정값이 어떻게 변했나요? 수렴 그래프에서 관찰한 경향을 설명하세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "처음에는 π 추정값이 크게 흔들리다가 횟수가 많아질수록..."
    },
    {
        "key": "형태비교",
        "label": "직선 바늘, V자형, W자형으로 각각 실험해보고 결과를 비교하세요. 총 호의 길이가 같을 때 π 추정 결과가 어떻게 달랐나요?",
        "type": "text_area",
        "height": 110,
        "placeholder": "직선 바늘: π ≈ __\nV자형: π ≈ __\nW자형: π ≈ __\n공통점/차이점: ..."
    },
    {
        "key": "뷔퐁국수",
        "label": "'뷔퐁의 국수 정리'에 따르면 어떤 형태라도 총 길이가 같으면 같은 기댓값을 가집니다. 이것이 신기한 이유와 이 정리의 의미를 설명하세요.",
        "type": "text_area",
        "height": 110,
        "placeholder": "형태가 달라도 π 추정에 사용할 수 있는 이유는..."
    },
    {
        "key": "몬테카를로",
        "label": "💡 무작위 실험으로 π 같은 수학 상수를 구하는 방법을 '몬테카를로 방법'이라고 합니다. 이 방법이 실제로 어디에 활용되는지 조사해서 써보세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "몬테카를로 방법은 ... 분야에서 활용된다."
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점", "label": "💬 느낀 점", "type": "text_area", "height": 90},
]

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>뷔퐁의 바늘 실험</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0a0f1e 0%,#0f2027 50%,#0a1628 100%);
  color:#e2e8f0;padding:12px 11px 22px;min-height:100vh;
}
/* ── 헤더 ── */
.hdr{text-align:center;padding:14px 16px 12px;
  background:linear-gradient(135deg,rgba(6,182,212,.15),rgba(99,102,241,.15));
  border:1px solid rgba(99,102,241,.3);border-radius:12px;margin-bottom:12px}
.hdr h1{font-size:1.3rem;color:#a78bfa;margin-bottom:4px}
.hdr p{font-size:0.8rem;color:#94a3b8;line-height:1.5}
/* ── 탭 ── */
.tab-bar{display:flex;gap:6px;margin-bottom:12px}
.tab-btn{
  padding:7px 18px;border-radius:7px;border:1px solid rgba(255,255,255,.15);
  background:transparent;color:#94a3b8;font-size:0.85rem;font-weight:600;cursor:pointer;
  transition:all .2s;
}
.tab-btn.on{background:rgba(167,139,250,.25);color:#a78bfa;border-color:#a78bfa}
/* ── 모양 선택 ── */
.shape-bar{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;
  padding:10px 12px;background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.08);border-radius:8px}
.shape-lbl{font-size:0.75rem;color:#64748b;align-self:center;margin-right:4px}
.sh-btn{
  padding:5px 12px;border-radius:5px;border:1px solid rgba(255,255,255,.15);
  background:transparent;color:#94a3b8;font-size:0.8rem;cursor:pointer;transition:all .15s;
}
.sh-btn.on{background:rgba(251,191,36,.2);color:#fbbf24;border-color:#fbbf24}
/* ── 메인 레이아웃 ── */
.main{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:10px}
.sim-wrap{flex:1 1 57%;min-width:260px}
.side-wrap{flex:1 1 33%;min-width:190px;display:flex;flex-direction:column;gap:8px}
canvas{border-radius:8px;border:1px solid rgba(99,102,241,.28);display:block;width:100%}
/* ── 통계 ── */
.sg{display:grid;grid-template-columns:1fr 1fr;gap:5px}
.sc{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.09);
    border-radius:8px;padding:7px 9px}
.sc.sp2{grid-column:span 2}
.sl{font-size:0.68rem;color:#94a3b8;margin-bottom:2px}
.sv{font-size:1.2rem;font-weight:700;line-height:1.2}
.sv.b{color:#60a5fa}.sv.r{color:#f87171}.sv.p{color:#c084fc}
.sv.g{font-size:1.35rem;color:#4ade80}
.sv.y{font-size:1.35rem;color:#fbbf24}
.sv.dim{color:#94a3b8}
.true-pi{background:rgba(251,191,36,.07);border:1px solid rgba(251,191,36,.2)}
/* ── 컨트롤 ── */
.ctrl{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
      border-radius:10px;padding:11px 13px;margin-bottom:9px}
.sr{display:flex;align-items:center;gap:8px;margin-bottom:9px}
.slbl{font-size:0.76rem;color:#94a3b8;min-width:80px}
input[type=range]{flex:1;accent-color:#a78bfa;cursor:pointer}
.snum{font-size:0.8rem;color:#e2e8f0;min-width:48px;text-align:right}
.spr{display:flex;align-items:center;gap:5px;flex-wrap:wrap;margin-bottom:9px}
.splbl{font-size:0.75rem;color:#94a3b8}
.spb{padding:3px 8px;border-radius:4px;border:1px solid rgba(255,255,255,.18);
     background:transparent;color:#94a3b8;font-size:0.76rem;cursor:pointer;transition:all .15s}
.spb.on{background:rgba(167,139,250,.22);color:#a78bfa;border-color:#a78bfa}
.br{display:flex;flex-wrap:wrap;gap:5px}
button.dp{padding:5px 11px;border-radius:5px;border:none;cursor:pointer;
  font-size:0.8rem;font-weight:600;
  background:linear-gradient(135deg,#3b82f6,#6366f1);color:#fff;transition:opacity .15s}
button.dp:hover{opacity:.85}
button.au{padding:5px 12px;border-radius:5px;border:none;cursor:pointer;
  font-size:0.8rem;font-weight:600;
  background:linear-gradient(135deg,#10b981,#059669);color:#fff}
button.st{padding:5px 10px;border-radius:5px;border:none;cursor:pointer;
  font-size:0.8rem;font-weight:600;background:#475569;color:#fff}
button.rs{padding:5px 10px;border-radius:5px;border:none;cursor:pointer;
  font-size:0.8rem;font-weight:600;
  background:linear-gradient(135deg,#ef4444,#dc2626);color:#fff}
/* ── 공식 박스 ── */
.fbox{background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.3);
      border-radius:9px;padding:10px 14px;text-align:center}
.ftit{font-size:0.75rem;color:#a78bfa;margin-bottom:5px}
.fmain{font-size:1rem;font-weight:700;color:#e2e8f0;font-family:'Courier New',monospace}
.fsub{font-size:0.78rem;color:#94a3b8;margin-top:4px}
/* ── 범례 ── */
.legend{display:flex;gap:12px;font-size:0.72rem;color:#94a3b8;margin-top:5px;flex-wrap:wrap}
.legend span{display:flex;align-items:center;gap:4px}
.ldot{width:14px;height:2.5px;border-radius:2px;display:inline-block}
/* ── 탭 컨텐츠 ── */
.tc{display:none}.tc.on{display:block}
/* ── 원리 탭 ── */
.thy{max-width:660px;margin:0 auto}
.tsec{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
      border-radius:10px;padding:14px 16px;margin-bottom:12px}
.tsec h3{font-size:0.95rem;color:#a78bfa;margin-bottom:10px;padding-bottom:6px;
         border-bottom:1px solid rgba(167,139,250,.2)}
.tsec p{font-size:0.82rem;color:#cbd5e1;line-height:1.65;margin-bottom:8px}
.tsec ul{font-size:0.82rem;color:#cbd5e1;padding-left:18px;line-height:1.7;margin-bottom:8px}
.tsec ul li{margin-bottom:3px}
.tformula{background:rgba(99,102,241,.12);border:1px solid rgba(99,102,241,.25);
           border-radius:7px;padding:9px 14px;margin:10px 0;
           font-family:'Courier New',monospace;font-size:0.9rem;color:#e2e8f0;text-align:center}
.tformula .tf-sub{font-size:0.78rem;color:#94a3b8;margin-top:4px;font-family:inherit}
.tcol{display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap}
.tcol .txt{flex:1 1 200px;font-size:0.82rem;color:#cbd5e1;line-height:1.65}
.tcol svg{flex:0 0 auto;max-width:220px}
.badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:0.72rem;
       font-weight:700;background:rgba(251,191,36,.2);color:#fbbf24;margin-bottom:6px}
.shape-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px;margin-top:10px}
.shape-card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
            border-radius:7px;padding:8px;text-align:center}
.shape-card .sc-name{font-size:0.75rem;color:#a78bfa;font-weight:700;margin-bottom:4px}
.shape-card .sc-formula{font-size:0.7rem;color:#94a3b8;font-family:'Courier New',monospace}
</style>
</head>
<body>

<div class="hdr">
  <h1>🪡 뷔퐁의 바늘 실험</h1>
  <p>평행선 위로 다양한 형태의 물체를 던져 π를 추정합니다.<br>
     원리 설명 탭에서 수학적 유도 과정도 확인해 보세요!</p>
</div>

<!-- 탭 바 -->
<div class="tab-bar">
  <button class="tab-btn on" onclick="switchTab('sim')">🔬 시뮬레이션</button>
  <button class="tab-btn" onclick="switchTab('theory')">📐 원리 설명</button>
</div>

<!-- ════════════ 시뮬레이션 탭 ════════════ -->
<div id="tab-sim" class="tc on">

  <!-- 모양 선택 -->
  <div class="shape-bar">
    <span class="shape-lbl">모양 선택:</span>
    <button class="sh-btn on" data-sh="straight" onclick="setShape('straight')">📏 직선 바늘</button>
    <button class="sh-btn" data-sh="v" onclick="setShape('v')">〈 V자형</button>
    <button class="sh-btn" data-sh="w" onclick="setShape('w')">𝖶 W자형</button>
  </div>

  <!-- 메인 -->
  <div class="main">
    <!-- 시뮬레이션 캔버스 -->
    <div class="sim-wrap">
      <canvas id="simC"></canvas>
      <div class="legend">
        <span><span class="ldot" style="background:#f87171"></span>교차 (hit)</span>
        <span><span class="ldot" style="background:#60a5fa"></span>비교차 (miss)</span>
        <span style="color:#475569">최신은 밝게 표시</span>
      </div>
    </div>
    <!-- 통계 + 그래프 -->
    <div class="side-wrap">
      <div class="sg">
        <div class="sc"><div class="sl">투척 횟수 (n)</div><div class="sv b" id="vN">0</div></div>
        <div class="sc"><div class="sl" id="hitsLabel">교차 횟수</div><div class="sv r" id="vH">0</div></div>
        <div class="sc"><div class="sl" id="rateLabel">교차율 (hits/n)</div><div class="sv p" id="vP">—</div></div>
        <div class="sc"><div class="sl" id="theoLabel">이론 교차율</div><div class="sv p" id="vT">—</div></div>
        <div class="sc sp2">
          <div class="sl">π 추정값 &nbsp;<span id="vEr" style="font-size:0.65rem;color:#64748b"></span></div>
          <div class="sv y" id="vPi">바늘을 던져보세요!</div>
        </div>
        <div class="sc sp2 true-pi">
          <div class="sl">실제 π</div>
          <div class="sv" style="color:#fbbf24;font-size:1rem">3.14159 26535 89793...</div>
        </div>
      </div>
      <canvas id="grC"></canvas>
    </div>
  </div>

  <!-- 컨트롤 -->
  <div class="ctrl">
    <div class="sr">
      <span class="slbl" id="sliderLabel">바늘 길이 L</span>
      <input type="range" id="sliderS" min="10" max="58" value="45" step="1">
      <span class="snum" id="lblS">45 px</span>
      <span style="font-size:0.72rem;color:#475569">(d = 65px)</span>
    </div>
    <div class="spr">
      <span class="splbl">속도:</span>
      <button class="spb" data-v="2" onclick="setSpd(2)">느리게</button>
      <button class="spb on" data-v="8" onclick="setSpd(8)">보통</button>
      <button class="spb" data-v="30" onclick="setSpd(30)">빠르게</button>
      <button class="spb" data-v="120" onclick="setSpd(120)">매우 빠르게</button>
    </div>
    <div class="br">
      <button class="dp" onclick="dropN(1)">+1개</button>
      <button class="dp" onclick="dropN(10)">+10개</button>
      <button class="dp" onclick="dropN(100)">+100개</button>
      <button class="dp" onclick="dropN(1000)">+1,000개</button>
      <button class="au" id="btnA" onclick="startAuto()">▶ 자동</button>
      <button class="st" id="btnS" style="display:none" onclick="stopAuto()">⏸ 정지</button>
      <button class="rs" onclick="resetSim()">↺ 초기화</button>
    </div>
  </div>

  <!-- 공식 -->
  <div class="fbox">
    <div class="ftit" id="fTitle">📐 직선 바늘 공식 (L ≤ d)</div>
    <div class="fmain" id="fMain">P(교차) = 2L / (π·d)</div>
    <div class="fsub" id="fSub">따라서 → π ≈ 2·L·n / (교차 횟수·d)</div>
  </div>

</div><!-- /tab-sim -->

<!-- ════════════ 원리 탭 ════════════ -->
<div id="tab-theory" class="tc">
<div class="thy">

  <!-- 단계 1 -->
  <div class="tsec">
    <h3>📌 단계 1: 실험 설정</h3>
    <div class="tcol">
      <div class="txt">
        <p>간격 <strong>d</strong>인 평행선 위에 길이 <strong>L(≤ d)</strong>인 바늘을 무작위로 던집니다. 이 때 두 확률 변수가 있습니다:</p>
        <ul>
          <li><strong style="color:#fbbf24">θ</strong> : 바늘과 평행선이 이루는 각도 (0 ~ π, 균일분포)</li>
          <li><strong style="color:#4ade80">D</strong> : 바늘 중심에서 가장 가까운 선까지의 거리 (0 ~ d/2, 균일분포)</li>
        </ul>
        <p>두 변수는 <strong>서로 독립</strong>이며, 교차 사건은 아래 조건으로 결정됩니다.</p>
      </div>
      <!-- SVG 다이어그램 1 -->
      <svg viewBox="0 0 210 130" style="max-width:210px;min-width:160px">
        <defs>
          <marker id="arr" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill="#94a3b8"/>
          </marker>
        </defs>
        <!-- 두 평행선 -->
        <line x1="10" y1="28" x2="200" y2="28" stroke="#94a3b8" stroke-width="2"/>
        <line x1="10" y1="108" x2="200" y2="108" stroke="#94a3b8" stroke-width="2"/>
        <text x="12" y="22" fill="#64748b" font-size="9">y = 0 (선)</text>
        <text x="12" y="120" fill="#64748b" font-size="9">y = d (선)</text>
        <!-- d 양방향 화살표 -->
        <line x1="196" y1="30" x2="196" y2="106" stroke="#94a3b8" stroke-width="1"
              marker-start="url(#arr)" marker-end="url(#arr)"/>
        <text x="200" y="72" fill="#94a3b8" font-size="10" font-weight="bold">d</text>
        <!-- 바늘 (교차 안 함) -->
        <line x1="55" y1="82" x2="125" y2="52" stroke="#60a5fa" stroke-width="2.5"/>
        <!-- 중심점 -->
        <circle cx="90" cy="67" r="2.5" fill="#60a5fa"/>
        <!-- D 수직 점선 (중심 → 위쪽 선) -->
        <line x1="90" y1="67" x2="90" y2="28" stroke="#4ade80" stroke-width="1.2" stroke-dasharray="3,2"
              marker-end="url(#arr)"/>
        <text x="94" y="50" fill="#4ade80" font-size="11" font-weight="bold">D</text>
        <!-- θ 호 -->
        <path d="M 105 67 A 15 15 0 0 0 116 59" fill="none" stroke="#fbbf24" stroke-width="1.5"/>
        <text x="118" y="68" fill="#fbbf24" font-size="11" font-weight="bold">θ</text>
        <!-- L/2 sin θ 표시 -->
        <line x1="125" y1="52" x2="125" y2="67" stroke="#f87171" stroke-width="1" stroke-dasharray="2,2"/>
        <text x="128" y="62" fill="#f87171" font-size="8">L/2·sinθ</text>
      </svg>
    </div>
  </div>

  <!-- 단계 2 -->
  <div class="tsec">
    <h3>📌 단계 2: 교차 조건</h3>
    <div class="tcol">
      <div class="txt">
        <p>바늘의 수직 방향 돌출 길이는 <strong>(L/2)·sinθ</strong>입니다.<br>
           바늘이 선과 교차하려면 중심에서 선까지의 거리 D가 이 돌출 길이보다 <strong>작거나 같아야</strong> 합니다.</p>
        <div class="tformula">D ≤ (L/2)·sin θ</div>
        <p>θ를 가로축, D를 세로축으로 나타내면, 교차가 일어나는 영역(파란색)은 사인 곡선 아래 부분입니다.</p>
      </div>
      <!-- SVG 다이어그램 2: D vs θ -->
      <svg viewBox="0 0 200 130" style="max-width:200px;min-width:150px">
        <!-- 축 -->
        <line x1="24" y1="10" x2="24" y2="110" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>
        <line x1="22" y1="108" x2="192" y2="108" stroke="#94a3b8" stroke-width="1.5" marker-end="url(#arr)"/>
        <!-- 축 레이블 -->
        <text x="8" y="64" fill="#4ade80" font-size="9" font-weight="bold">D</text>
        <text x="104" y="122" fill="#fbbf24" font-size="9" font-weight="bold">θ (0 ~ π)</text>
        <!-- d/2 수평선 -->
        <line x1="22" y1="30" x2="185" y2="30" stroke="#94a3b8" stroke-width="0.8" stroke-dasharray="3,2"/>
        <text x="4" y="33" fill="#94a3b8" font-size="8">d/2</text>
        <!-- 사인 곡선 (교차 영역 채우기) -->
        <path d="M24,108 Q 60,10 104,30 Q 148,50 184,108 Z"
              fill="rgba(96,165,250,0.25)" stroke="none"/>
        <path d="M24,108 Q 60,10 104,30 Q 148,50 184,108"
              fill="none" stroke="#60a5fa" stroke-width="2"/>
        <!-- 레이블 -->
        <text x="70" y="75" fill="#60a5fa" font-size="8">교차 영역</text>
        <text x="70" y="85" fill="#60a5fa" font-size="8">(D ≤ L/2·sinθ)</text>
        <!-- x축 π 표시 -->
        <line x1="184" y1="106" x2="184" y2="110" stroke="#94a3b8" stroke-width="1"/>
        <text x="181" y="120" fill="#94a3b8" font-size="9">π</text>
      </svg>
    </div>
  </div>

  <!-- 단계 3 -->
  <div class="tsec">
    <h3>📌 단계 3: 적분으로 확률 계산</h3>
    <p>θ와 D가 각각 [0, π]과 [0, d/2]에서 균일하게 분포하므로, 교차 확률은 전체 직사각형에 대한 사인 곡선 아래 면적의 비율입니다.</p>
    <div class="tformula">
      P(교차) = <span style="color:#60a5fa">∫₀^π (L/2)sinθ dθ</span> / (π × d/2)
      <div class="tf-sub">= [-(L/2)cosθ]₀^π / (πd/2) = L / (πd/2) = <strong style="color:#fbbf24">2L/(πd)</strong></div>
    </div>
    <p>교차가 일어난 횟수를 <strong>hits</strong>, 총 시행 횟수를 <strong>n</strong>이라 하면:</p>
    <div class="tformula">
      hits/n ≈ 2L/(πd) &nbsp;→&nbsp; <strong style="color:#fbbf24">π ≈ 2Ln / (hits·d)</strong>
    </div>
    <p style="color:#64748b;font-size:0.78rem">* 이 공식은 L ≤ d (짧은 바늘)인 경우에 정확하게 성립합니다.</p>
  </div>

  <!-- 단계 4: 뷔퐁의 국수 정리 -->
  <div class="tsec">
    <h3>📌 단계 4: 뷔퐁의 바늘 → 뷔퐁의 국수 (Buffon's Noodle)</h3>
    <div class="badge">확장 정리</div>
    <p>앞에서 다룬 <strong>뷔퐁의 바늘(Buffon's Needle)</strong>은 1777년 뷔퐁이 직선 바늘로 제시한 고전 문제입니다.
    이후 수학자들은 "바늘을 꼭 직선으로 제한할 필요가 있을까?"라는 질문을 던졌고,
    이를 임의의 곡선으로 일반화한 것이 <strong>뷔퐁의 국수 정리(Buffon's Noodle)</strong>입니다.
    마치 딱딱한 바늘 대신 구부러진 국수 면발을 던지는 것처럼요.</p>
    <p><strong>어떤 형태의 곡선이든</strong> 총 호의 길이가 L이면, 평행선 간격 d인 선에 던질 때 교차 횟수의 기댓값은 항상 같습니다!</p>
    <div class="tformula">
      E(교차 횟수) = 2L / (π·d) &nbsp;→&nbsp; π ≈ 2L·n / (total_crossings·d)
    </div>
    <p>따라서 직선 바늘이 아닌 V자형·W자형 등 어떤 모양으로도 π를 추정할 수 있습니다.</p>
    <div class="shape-grid">
      <div class="shape-card">
        <div class="sc-name">📏 직선 바늘</div>
        <svg viewBox="0 0 80 30" style="width:100%;max-width:80px;margin:4px auto;display:block">
          <line x1="10" y1="15" x2="70" y2="15" stroke="#60a5fa" stroke-width="2"/>
        </svg>
        <div class="sc-formula">arc = L<br>π ≈ 2Ln/hits·d</div>
      </div>
      <div class="shape-card">
        <div class="sc-name">〈 V자형</div>
        <svg viewBox="0 0 80 40" style="width:100%;max-width:80px;margin:4px auto;display:block">
          <line x1="40" y1="30" x2="10" y2="8" stroke="#fbbf24" stroke-width="2"/>
          <line x1="40" y1="30" x2="70" y2="8" stroke="#fbbf24" stroke-width="2"/>
        </svg>
        <div class="sc-formula">arc = 2×팔길이<br>π ≈ 2Ln/hits·d</div>
      </div>
      <div class="shape-card">
        <div class="sc-name">𝖶 W자형</div>
        <svg viewBox="0 0 80 30" style="width:100%;max-width:80px;margin:4px auto;display:block">
          <polyline points="5,5 22,25 40,5 58,25 75,5" fill="none" stroke="#f87171" stroke-width="2"/>
        </svg>
        <div class="sc-formula">arc = 4×마디길이<br>π ≈ 2Ln/hits·d</div>
      </div>
    </div>
    <div style="margin-top:10px;padding:8px 12px;background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);border-radius:7px;font-size:0.78rem;color:#fca5a5">
      ⚠️ <strong>원은 왜 포함하지 않나요?</strong><br>
      원의 둘레 = <strong>2πr</strong> — 여기에 이미 π가 포함됩니다.
      뷔퐁 국수 공식 E = 2L/(πd)에 대입하면 E = 4r/d 로 π가 소거되어,
      교차 데이터만으로는 독립적으로 π를 유도할 수 없습니다.
    </div>
  </div>

  <!-- 몬테카를로 -->
  <div class="tsec">
    <h3>💡 몬테카를로 방법</h3>
    <p>뷔퐁의 바늘 실험처럼 <strong>무작위 시행을 대량으로 반복</strong>하여 수학 상수나 확률을 추정하는 방법을 <strong style="color:#a78bfa">몬테카를로 방법(Monte Carlo Method)</strong>이라고 합니다.</p>
    <p>현대 컴퓨터를 이용한 몬테카를로 시뮬레이션은 물리학·금융·의학·AI 등 다양한 분야에서 활용됩니다.</p>
  </div>

</div><!-- /thy -->
</div><!-- /tab-theory -->

<script>
// ────────────────────────────────
//  상수 & 상태
// ────────────────────────────────
const D = 65;         // 선 간격 (px)
let size  = 45;       // 바늘 길이 or 반지름 (px)
let shape = 'straight';

let total = 0, crossings = 0;
let piHistory = [];
let autoRaf = null, autoSpd = 8;

const simC = document.getElementById('simC');
const simX = simC.getContext('2d');
const grC  = document.getElementById('grC');
const grX  = grC.getContext('2d');

// ────────────────────────────────
//  탭 전환
// ────────────────────────────────
function switchTab(id) {
  document.querySelectorAll('.tab-btn').forEach((b,i) =>
    b.classList.toggle('on', (i===0&&id==='sim')||(i===1&&id==='theory')));
  document.getElementById('tab-sim').classList.toggle('on', id==='sim');
  document.getElementById('tab-theory').classList.toggle('on', id==='theory');
}

// ────────────────────────────────
//  모양 선택
// ────────────────────────────────
const SHAPE_INFO = {
  straight: {
    sliderLabel: '바늘 길이 L',
    fTitle: '📐 직선 바늘 공식 (L ≤ d)',
    fMain:  'P(교차) = 2L / (π·d)',
    fSub:   '→ π ≈ 2·L·n / (교차 횟수·d)'
  },
  v: {
    sliderLabel: '팔 길이 (각 arm)',
    fTitle: '📐 V자형 – 뷔퐁의 국수 정리',
    fMain:  'E(교차) = 2·(2·arm) / (π·d)',
    fSub:   '→ π ≈ 2·(2·arm)·n / (교차 횟수·d)'
  },
  w: {
    sliderLabel: '마디 길이 (각 seg)',
    fTitle: '📐 W자형 – 뷔퐁의 국수 정리',
    fMain:  'E(교차) = 2·(4·seg) / (π·d)',
    fSub:   '→ π ≈ 2·(4·seg)·n / (교차 횟수·d)'
  },
};

function setShape(sh) {
  shape = sh;
  document.querySelectorAll('.sh-btn').forEach(b =>
    b.classList.toggle('on', b.dataset.sh === sh));
  const info = SHAPE_INFO[sh];
  document.getElementById('sliderLabel').textContent = info.sliderLabel;
  document.getElementById('fTitle').textContent = info.fTitle;
  document.getElementById('fMain').textContent  = info.fMain;
  document.getElementById('fSub').textContent   = info.fSub;

  const sl = document.getElementById('sliderS');
  size = +sl.value;
  document.getElementById('lblS').textContent = size + ' px';
  resetSim();
}

// ────────────────────────────────
//  시뮬레이션 로직
// ────────────────────────────────

/** 한 구간(y1→y2)이 몇 개의 수평선(y=D,2D,…)을 교차하는지 */
function segCross(y1, y2) {
  const mn = Math.min(y1, y2), mx = Math.max(y1, y2);
  if (mn === mx) return 0;
  const kmin = Math.ceil(mn / D + 1e-9);
  const kmax = Math.floor(mx / D - 1e-9);
  return Math.max(0, kmax - kmin + 1);
}

/** 원이 수평선과 교차하는 점의 수 */
function circleCross(cy, r) {
  let cnt = 0;
  const kmin = Math.ceil((cy - r) / D + 1e-9);
  const kmax = Math.floor((cy + r) / D - 1e-9);
  for (let k = kmin; k <= kmax; k++) {
    if (Math.abs(cy - k * D) < r) cnt += 2;
  }
  return cnt;
}

/** 한 번 던지기 → {segments|circle, crossCount, hit} */
function makeOneDrop() {
  const cx    = Math.random() * simC.width;
  const cy    = Math.random() * simC.height;
  const theta = Math.random() * Math.PI;
  const C = Math.cos(theta), S = Math.sin(theta);
  function rot(lx, ly) { return {x: cx + lx*C - ly*S, y: cy + lx*S + ly*C}; }

  let segs = [], isCircle = false, r = 0, cross = 0;

  if (shape === 'straight') {
    const p1 = rot(-size/2, 0), p2 = rot(size/2, 0);
    segs = [{x1:p1.x, y1:p1.y, x2:p2.x, y2:p2.y}];
    cross = segCross(p1.y, p2.y);

  } else if (shape === 'v') {
    const ha = Math.PI / 6; // 30° (so 60° between arms)
    const a1 = rot(size*Math.cos(ha),  -size*Math.sin(ha));
    const a2 = rot(-size*Math.cos(ha), -size*Math.sin(ha));
    segs = [
      {x1:cx, y1:cy, x2:a1.x, y2:a1.y},
      {x1:cx, y1:cy, x2:a2.x, y2:a2.y}
    ];
    cross = segCross(cy, a1.y) + segCross(cy, a2.y);

  } else if (shape === 'w') {
    // 4 segments of length `size` forming zigzag W
    const seg = size;
    const cs = Math.cos(Math.PI/4), ss = Math.sin(Math.PI/4);
    // local points (W upward)
    const lp = [
      {x:-2*seg*cs,  y: seg*ss*0.5},
      {x:-seg*cs,    y:-seg*ss*0.5},
      {x:0,          y: seg*ss*0.5},
      {x: seg*cs,    y:-seg*ss*0.5},
      {x: 2*seg*cs,  y: seg*ss*0.5}
    ];
    // centroid y offset
    const avgY = lp.reduce((a,p) => a+p.y, 0) / lp.length;
    segs = [];
    for (let i = 0; i < 4; i++) {
      const p1 = rot(lp[i].x, lp[i].y - avgY);
      const p2 = rot(lp[i+1].x, lp[i+1].y - avgY);
      segs.push({x1:p1.x, y1:p1.y, x2:p2.x, y2:p2.y});
      cross += segCross(p1.y, p2.y);
    }

  }

  return {cx, cy, segs, isCircle, r, cross, hit: cross > 0, theta};
}

let drops = []; // store for drawing

function dropN(n) {
  for (let i = 0; i < n; i++) {
    const d = makeOneDrop();
    drops.push(d);
    total++;
    crossings += d.cross;
    if (crossings > 0) piHistory.push(estimatePi());
  }
  render();
}

function estimatePi() {
  if (crossings === 0) return null;
  const arcLen = shape === 'straight' ? size : shape === 'v' ? 2*size : 4*size;
  return 2 * arcLen * total / (crossings * D);
}

function theoreticalRate() {
  const arcLen = shape === 'straight' ? size : shape === 'v' ? 2*size : 4*size;
  return 2 * arcLen / (Math.PI * D);
}

function setSpd(v) {
  autoSpd = v;
  document.querySelectorAll('.spb').forEach(b =>
    b.classList.toggle('on', +b.dataset.v === v));
}

function startAuto() {
  if (autoRaf) return;
  document.getElementById('btnA').style.display = 'none';
  document.getElementById('btnS').style.display = '';
  function loop() {
    dropN(autoSpd);
    autoRaf = requestAnimationFrame(loop);
  }
  autoRaf = requestAnimationFrame(loop);
}

function stopAuto() {
  if (autoRaf) { cancelAnimationFrame(autoRaf); autoRaf = null; }
  document.getElementById('btnA').style.display = '';
  document.getElementById('btnS').style.display = 'none';
}

function resetSim() {
  stopAuto();
  drops = []; total = 0; crossings = 0; piHistory = [];
  render();
}

// ────────────────────────────────
//  그리기: 시뮬레이션 캔버스
// ────────────────────────────────
function drawSim() {
  const W = simC.width, H = simC.height;
  const ctx = simX;

  ctx.fillStyle = '#0d1b2a';
  ctx.fillRect(0, 0, W, H);

  const n = drops.length;
  const fadeStart = Math.max(0, n - 800);

  // ── 평행선 (모든 모양 공통) ──
  for (let y = D; y < H; y += D) {
    ctx.strokeStyle = 'rgba(99,102,241,0.18)';
    ctx.lineWidth = 5;
    ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(W,y); ctx.stroke();
    ctx.strokeStyle = 'rgba(203,213,225,0.6)';
    ctx.lineWidth = 1.4;
    ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(W,y); ctx.stroke();
  }
  if (D < H) {
    ctx.fillStyle = 'rgba(100,116,139,0.7)';
    ctx.font = '10px sans-serif';
    ctx.fillText('d = ' + D + 'px', 4, D - 4);
  }

  // ── 투척물 그리기 ──
  for (let i = fadeStart; i < n; i++) {
    const dp = drops[i];
    const age = n - 1 - i;
    const alpha = age < 20 ? 1.0 : age < 150 ? 0.65 : 0.3;
    const lw = age < 4 ? 2.8 : 1.2;

    ctx.strokeStyle = dp.hit
      ? `rgba(248,113,113,${alpha})`
      : `rgba(96,165,250,${alpha})`;
    ctx.lineWidth = lw;

    if (dp.isCircle) {
      // 원 링 그리기
      ctx.beginPath();
      ctx.arc(dp.cx, dp.cy, dp.r, 0, 2*Math.PI);
      ctx.stroke();
    } else {
      for (const seg of dp.segs) {
        ctx.beginPath();
        ctx.moveTo(seg.x1, seg.y1);
        ctx.lineTo(seg.x2, seg.y2);
        ctx.stroke();
        if (age < 4) {
          ctx.fillStyle = dp.hit ? '#fca5a5' : '#93c5fd';
          ctx.beginPath(); ctx.arc(seg.x1, seg.y1, 2, 0, 2*Math.PI); ctx.fill();
          ctx.beginPath(); ctx.arc(seg.x2, seg.y2, 2, 0, 2*Math.PI); ctx.fill();
        }
      }
    }
  }

  // 투척 수 표시
  if (total > 0) {
    ctx.fillStyle = 'rgba(0,0,0,.55)';
    ctx.fillRect(W-126, 6, 120, 22);
    ctx.fillStyle = '#94a3b8';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText('n = ' + total.toLocaleString(), W-8, 21);
    ctx.textAlign = 'left';
  }
}

// ────────────────────────────────
//  그리기: π 수렴 그래프
// ────────────────────────────────
function drawGraph() {
  const ctx = grX;
  const W = grC.width, H = grC.height;
  const pad = {t:26, r:22, b:24, l:36};
  const gx = pad.l, gy = pad.t, gw = W-pad.l-pad.r, gh = H-pad.t-pad.b;

  ctx.fillStyle = '#0d1b2a';
  ctx.fillRect(0,0,W,H);

  ctx.fillStyle = '#94a3b8';
  ctx.font = 'bold 11px sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('π 수렴 그래프', W/2, 16);
  ctx.textAlign = 'left';

  if (piHistory.length < 2) {
    ctx.fillStyle = '#334155';
    ctx.font = '10px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('바늘을 던지면 그래프가 나타납니다', W/2, H/2+8);
    ctx.textAlign = 'left';
    return;
  }

  const minY = 2.0, maxY = 5.0;
  const yS = v => gy + gh - ((v-minY)/(maxY-minY))*gh;

  // 그리드
  ctx.strokeStyle = 'rgba(255,255,255,.07)';
  ctx.lineWidth = 1;
  [2,2.5,3,3.5,4,4.5,5].forEach(v => {
    const py = yS(v);
    ctx.beginPath(); ctx.moveTo(gx,py); ctx.lineTo(gx+gw,py); ctx.stroke();
  });

  // π 점선
  ctx.save();
  ctx.strokeStyle = 'rgba(251,191,36,.85)';
  ctx.lineWidth = 1.5;
  ctx.setLineDash([5,3]);
  const piY = yS(Math.PI);
  ctx.beginPath(); ctx.moveTo(gx,piY); ctx.lineTo(gx+gw,piY); ctx.stroke();
  ctx.restore();
  ctx.fillStyle = '#fbbf24';
  ctx.font = 'bold 10px sans-serif';
  ctx.fillText('π', gx+gw+3, piY+4);

  // 추정값 선
  ctx.strokeStyle = '#c084fc';
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  const hist = piHistory;
  const step = Math.max(1, Math.floor(hist.length/(gw*2)));
  for (let i = 0; i < hist.length; i += step) {
    const px = gx + (i/(hist.length-1))*gw;
    const pv = Math.min(maxY, Math.max(minY, hist[i]));
    const py = yS(pv);
    i===0 ? ctx.moveTo(px,py) : ctx.lineTo(px,py);
  }
  ctx.stroke();

  // 최신값 점
  const last = hist[hist.length-1];
  if (last >= minY && last <= maxY) {
    ctx.fillStyle = '#e879f9';
    ctx.beginPath(); ctx.arc(gx+gw, yS(last), 3, 0, 2*Math.PI); ctx.fill();
  }

  // 축
  ctx.strokeStyle = 'rgba(255,255,255,.25)';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(gx,gy); ctx.lineTo(gx,gy+gh); ctx.lineTo(gx+gw,gy+gh);
  ctx.stroke();

  // Y축 레이블
  ctx.fillStyle = '#64748b';
  ctx.font = '9px sans-serif';
  ctx.textAlign = 'right';
  [2,3,4,5].forEach(v => ctx.fillText(v, gx-3, yS(v)+3));
  ctx.textAlign = 'left';
}

// ────────────────────────────────
//  DOM 통계 업데이트
// ────────────────────────────────
function updateStats() {
  document.getElementById('vN').textContent = total.toLocaleString();
  document.getElementById('vH').textContent = crossings.toLocaleString();
  document.getElementById('vT').textContent = theoreticalRate().toFixed(5);

  if (total > 0) {
    document.getElementById('vP').textContent = (crossings/total).toFixed(5);
  }
  if (crossings > 0) {
    const pi = estimatePi();
    const el = document.getElementById('vPi');
    const diff = Math.abs(pi - Math.PI);
    const pctErr = (diff/Math.PI*100).toFixed(2);
    el.textContent = pi.toFixed(6);
    el.className = 'sv ' + (diff < 0.031 ? 'g' : diff < 0.16 ? 'y' : 'r');
    document.getElementById('vEr').textContent = '오차 ' + pctErr + '%';
  }
}

function render() {
  drawSim();
  drawGraph();
  updateStats();
}

// ────────────────────────────────
//  리사이즈
// ────────────────────────────────
function resizeAll() {
  const sw = simC.parentElement.clientWidth || 380;
  simC.width = sw; simC.height = Math.round(sw * 0.60);
  const gw = grC.parentElement.clientWidth || 200;
  grC.width = gw; grC.height = 175;
  render();
}

// ────────────────────────────────
//  슬라이더
// ────────────────────────────────
document.getElementById('sliderS').addEventListener('input', function() {
  size = +this.value;
  document.getElementById('lblS').textContent = size + ' px';
  resetSim();
});

window.addEventListener('resize', resizeAll);
resizeAll();
</script>
</body>
</html>
"""


def render():
    st.markdown("### 🪡 뷔퐁의 바늘 실험")
    st.markdown(
        "평행선 위로 다양한 형태의 물체를 던져 **π**를 추정합니다. "
        "**원리 설명** 탭에서 교차 조건과 적분 유도 과정을 확인하고, "
        "직선·V자·W자·원 등 여러 형태로 **뷔퐁의 국수 정리**를 체험해 보세요."
    )

    components.html(_HTML, height=1020, scrolling=True)

    st.markdown("---")
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
