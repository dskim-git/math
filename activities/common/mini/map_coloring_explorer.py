# activities/common/mini/map_coloring_explorer.py
"""
지도 색칠 경우의 수 탐구 - 도형과 지도를 직접 클릭하여 색칠하며
인접 영역을 서로 다른 색으로 칠하는 경우의 수와 4색 정리를 탐구하는 인터랙티브 미니 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "지도색칠경우의수"

META = {
    "title":       "🗺️ 지도 색칠 경우의 수",
    "description": "도형과 지도를 직접 색칠하며 인접 영역을 다른 색으로 칠하는 경우의 수와 4색 정리를 탐구합니다.",
    "order":       345,
    "hidden":      False,
}

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 성찰 질문에 답해 보세요**"},
    {
        "key":    "색칠방법수",
        "label":  "① 4개의 영역(A,B,C,D)을 4가지 색으로 인접한 영역이 서로 다르게 칠하는 경우의 수가 84인 이유를 단계별로 설명해보세요. 합의 법칙과 곱의 법칙이 어디에 사용됐나요?",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "색최솟값",
        "label":  "② 서울 25개 자치구 또는 미국 50개 주 지도를 색칠해보며 인접한 구역을 모두 다른 색으로 칠하기 위해 최소 몇 가지 색이 필요했나요? 실험 결과를 적어보세요.",
        "type":   "text_area",
        "height": 90,
    },
    {
        "key":    "4색정리연결",
        "label":  "③ 4색 정리란 무엇인지 자신의 말로 설명하고, 지도 색칠 활동과 4색 정리가 어떻게 연결되는지 설명해보세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "조건영향",
        "label":  "④ '인접한 영역은 서로 다른 색으로 칠한다'는 조건이 없다면 경우의 수는 어떻게 달라질까요? 조건이 경우의 수에 미치는 영향을 설명해보세요.",
        "type":   "text_area",
        "height": 90,
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
<meta charset="UTF-8">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Nanum Gothic',sans-serif;background:#0f1123;color:#eee;padding:14px;}
.tabs{display:flex;gap:8px;margin-bottom:18px;flex-wrap:wrap;}
.tab-btn{padding:10px 16px;border:none;border-radius:28px;cursor:pointer;font-size:13px;font-weight:bold;transition:all .3s;background:#1c1c3e;color:#99a;}
.tab-btn.active{background:linear-gradient(135deg,#7c6fff,#3ecef7);color:#fff;box-shadow:0 4px 18px rgba(120,100,255,.45);}
.tab-btn:hover:not(.active){background:#2a2a50;color:#ccc;}
.tab-content{display:none;}.tab-content.active{display:block;}
.card{background:#1a1a3e;border-radius:14px;padding:18px;margin-bottom:14px;}
.title-bar{background:linear-gradient(135deg,#1a1a3e,#0f305a);border-left:5px solid #7c6fff;padding:12px 16px;border-radius:0 10px 10px 0;margin-bottom:16px;}
.title-bar h2{font-size:18px;color:#7c6fff;margin-bottom:4px;}
.title-bar p{font-size:13px;color:#aab;}
.palette{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 12px;align-items:center;}
.swatch{width:40px;height:40px;border-radius:50%;cursor:pointer;border:3px solid transparent;transition:all .2s;flex-shrink:0;}
.swatch.sel{border-color:#fff;transform:scale(1.2);box-shadow:0 0 14px rgba(255,255,255,.6);}
.erase-btn{width:40px;height:40px;border-radius:50%;cursor:pointer;background:#222244;border:3px solid #555;font-size:16px;display:flex;align-items:center;justify-content:center;transition:all .2s;}
.erase-btn.sel{border-color:#fff;transform:scale(1.2);}
.status-bar{padding:10px 14px;border-radius:8px;font-size:13px;font-weight:bold;margin:8px 0;min-height:38px;}
.s-neutral{background:#1c2040;color:#99a;}
.s-ok{background:linear-gradient(135deg,#1a4a2e,#1e5c38);color:#7fef9f;border:1px solid #3fdf6f;}
.s-err{background:linear-gradient(135deg,#4a1a1a,#5c1e1e);color:#ef7f7f;border:1px solid #df3f3f;}
.btn{padding:9px 16px;border:none;border-radius:8px;cursor:pointer;font-size:13px;font-weight:bold;transition:all .2s;margin-right:6px;margin-bottom:4px;}
.btn-p{background:linear-gradient(135deg,#7c6fff,#3ecef7);color:#fff;}
.btn-s{background:#2d2d5e;color:#ccd;}
.btn:hover{opacity:.85;transform:translateY(-1px);}
#tip{position:fixed;background:#222244;border:1px solid #7c6fff;border-radius:8px;padding:6px 12px;font-size:12px;pointer-events:none;display:none;z-index:9999;color:#eef;}
.celebrate{display:none;text-align:center;font-size:20px;padding:14px;border-radius:12px;margin:8px 0;background:linear-gradient(135deg,#1e4a2e,#2e6a3e);border:2px solid #3fef6f;animation:pulse 1s ease-in-out infinite;}
.celebrate.show{display:block;}
@keyframes pulse{0%,100%{transform:scale(1);}50%{transform:scale(1.02);}}
.region{cursor:pointer;transition:opacity .15s;stroke:#ffffff22;stroke-width:1;fill:#2a2a55;}
.region:hover{opacity:.75;}
.region.bad{stroke:#ff4444!important;stroke-width:3!important;animation:blink .5s ease-in-out 3;}
@keyframes blink{0%,100%{opacity:1;}50%{opacity:.4;}}
.step-list{list-style:none;counter-reset:step;}
.step-list li{counter-increment:step;display:flex;align-items:flex-start;gap:10px;padding:10px 0;border-bottom:1px solid #2a2a55;font-size:13px;line-height:1.6;}
.step-list li::before{content:counter(step);width:26px;height:26px;border-radius:50%;background:linear-gradient(135deg,#7c6fff,#3ecef7);color:#fff;font-weight:bold;font-size:13px;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.step-v{font-size:22px;font-weight:bold;color:#FFD700;}
.fbox{background:#12122a;border:2px solid #7c6fff;border-radius:12px;padding:14px;text-align:center;font-size:15px;margin:10px 0;font-weight:bold;line-height:1.9;}
.fbig{font-size:26px;color:#FFD700;}
.nctrl{display:flex;align-items:center;gap:10px;margin:8px 0 14px;font-size:14px;}
.nc-btn{width:32px;height:32px;border-radius:50%;border:2px solid #7c6fff;background:#1c1c3e;color:#7c6fff;font-size:16px;font-weight:bold;cursor:pointer;transition:all .2s;}
.nc-btn:hover{background:#7c6fff;color:#fff;}
.nc-val{font-size:22px;font-weight:bold;color:#FFD700;width:50px;text-align:center;}
.leaf-map{height:540px;border-radius:10px;overflow:hidden;}
.leaflet-container{background:#12122a!important;}
.leaflet-tooltip-dark{background:rgba(0,0,0,.75)!important;border:1px solid #7c6fff!important;color:#eef!important;font-size:11px!important;font-weight:bold!important;padding:2px 7px!important;border-radius:5px!important;white-space:nowrap!important;}
.leaflet-tooltip-dark::before{display:none!important;}
.leaflet-control-zoom a{background:#1c1c3e!important;color:#aab!important;border-color:#3a3a6e!important;}
.leaflet-control-attribution{background:rgba(15,17,35,.8)!important;color:#556!important;font-size:9px!important;}
.th-card{background:linear-gradient(135deg,#1a1a3e,#12122a);border:1px solid #3a3a6e;border-radius:14px;padding:20px;margin-bottom:14px;}
.th-card h3{color:#7c6fff;font-size:16px;margin-bottom:10px;}
.th-card p,.th-card li{color:#bbc;font-size:14px;line-height:1.8;}
.th-card ul{padding-left:20px;margin:8px 0;}
.hi-box{background:linear-gradient(135deg,#1e3a5e,#1a2a4e);border:2px solid #3ecef7;border-radius:12px;padding:16px;margin:12px 0;text-align:center;}
.hi-box p{color:#eef;font-size:15px;line-height:1.8;font-weight:bold;}
</style>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
</head>
<body>
<div class="tabs">
  <button class="tab-btn active" onclick="showTab(0)">🔵 4영역 원 색칠</button>
  <button class="tab-btn" onclick="showTab(1)">⬠ 5영역 도형 색칠</button>
  <button class="tab-btn" onclick="showTab(2)">🏙️ 서울 25개 자치구</button>
  <button class="tab-btn" onclick="showTab(3)">🇺🇸 미국 50개 주</button>
  <button class="tab-btn" onclick="showTab(4)">🎨 4색 정리</button>
</div>
<div id="tip"></div>
<!-- ===== TAB 0: 4-region circle ===== -->
<div class="tab-content active">
  <div class="title-bar">
    <h2>🔵 원을 4가지 색으로 칠하는 경우의 수</h2>
    <p>원을 4개의 영역 A, B, C, D로 나누었을 때 인접한 영역이 서로 다른 색이 되도록 색칠하는 경우의 수를 구해 봅시다.</p>
  </div>
  <div class="card">
    <div style="font-size:13px;color:#aab;margin-bottom:6px;">🎨 색상을 선택하고 영역을 클릭하여 색칠하세요</div>
    <div class="palette" id="t0-palette"></div>
    <div>
      <button class="btn btn-s" onclick="resetTab(0)">🔄 초기화</button>
      <button class="btn btn-p" onclick="checkTab(0)">✅ 확인</button>
      <button class="btn btn-p" onclick="autoColor(0)">⚡ 자동 색칠</button>
    </div>
    <div class="status-bar s-neutral" id="t0-status">🖌️ 색을 고른 뒤 영역을 클릭하여 색칠하세요</div>
    <div class="celebrate" id="t0-celebrate">🎉 완성! 인접한 영역이 모두 다른 색으로 칠해졌어요! 🎉</div>
  </div>
  <div class="card" style="text-align:center;">
    <svg viewBox="0 0 420 420" style="width:min(420px,90vw);height:auto;display:block;margin:0 auto;">
      <path id="t0-A" class="region" onclick="paint(0,'A')" d="M 210,210 L 210,30 A 180,180 0 0,0 30,210 Z"/>
      <path id="t0-D" class="region" onclick="paint(0,'D')" d="M 210,210 L 390,210 A 180,180 0 0,0 210,30 Z"/>
      <path id="t0-B" class="region" onclick="paint(0,'B')" d="M 210,210 L 30,210 A 180,180 0 0,0 210,390 Z"/>
      <path id="t0-C" class="region" onclick="paint(0,'C')" d="M 210,210 L 210,390 A 180,180 0 0,0 390,210 Z"/>
      <line x1="210" y1="30" x2="210" y2="390" stroke="#444466" stroke-width="2"/>
      <line x1="30" y1="210" x2="390" y2="210" stroke="#444466" stroke-width="2"/>
      <circle cx="210" cy="210" r="180" fill="none" stroke="#7c6fff" stroke-width="2.5"/>
      <text x="110" y="200" fill="#fff" font-size="30" font-weight="bold" text-anchor="middle" pointer-events="none">A</text>
      <text x="310" y="200" fill="#fff" font-size="30" font-weight="bold" text-anchor="middle" pointer-events="none">D</text>
      <text x="110" y="320" fill="#fff" font-size="30" font-weight="bold" text-anchor="middle" pointer-events="none">B</text>
      <text x="310" y="320" fill="#fff" font-size="30" font-weight="bold" text-anchor="middle" pointer-events="none">C</text>
      <text x="210" y="218" fill="#7c6fff88" font-size="11" text-anchor="middle" pointer-events="none">중심</text>
    </svg>
    <div style="font-size:12px;color:#778;margin-top:8px;">인접 관계: A↔B, A↔D, B↔C, C↔D &nbsp;|&nbsp; 비인접(대각): A↔C, B↔D</div>
  </div>
  <div class="card">
    <div style="font-size:14px;font-weight:bold;color:#aab;margin-bottom:12px;">📐 단계별 풀이</div>
    <ul class="step-list">
      <li>
        <div><b>영역 A</b>에 칠할 색의 수: <span class="step-v">4</span>가지</div>
      </li>
      <li>
        <div><b>영역 B</b> (A와 인접 → B ≠ A): <span class="step-v">3</span>가지</div>
      </li>
      <li>
        <div>
          <b>영역 C</b> (B와만 인접, A와는 비인접 → C ≠ B)를 경우로 나눕니다.<br>
          <div style="margin-top:6px;padding:8px 12px;border-left:3px solid #7c6fff;background:#12122a;border-radius:0 8px 8px 0;">
            <div>✦ <b>C = A인 경우</b>: 1가지 → D (A·C와 다름, A=C이므로 D ≠ A): <b>3</b>가지 → 소계 <span class="step-v">1×3 = 3</span></div>
            <div style="margin-top:4px;">✦ <b>C ≠ A이고 C ≠ B인 경우</b>: 2가지 → D (A와도 C와도 다름): <b>2</b>가지 → 소계 <span class="step-v">2×2 = 4</span></div>
          </div>
          <div style="margin-top:6px;">C, D 단계 합 (합의 법칙): <span class="step-v">3 + 4 = 7</span>가지</div>
        </div>
      </li>
      <li>
        <div><b>전체 경우의 수</b> (곱의 법칙):</div>
      </li>
    </ul>
    <div class="fbox">
      A의 경우 × B의 경우 × (C·D 합의 법칙)<br>
      = 4 × 3 × (3+4) = 4 × 3 × 7 = <span class="fbig">84가지</span>
    </div>
  </div>
</div>
<!-- ===== TAB 1: 5-region figure ===== -->
<div class="tab-content">
  <div class="title-bar">
    <h2>⬠ 5개의 영역을 색칠하는 경우의 수</h2>
    <p>5개의 영역 A, B, C, D, E가 있을 때 인접한 영역이 서로 다른 색이 되도록 색칠해 보세요. 최소 몇 가지 색이 필요할까요?</p>
  </div>
  <div class="card">
    <div style="font-size:13px;color:#aab;margin-bottom:6px;">🎨 색상을 선택하고 영역을 클릭하여 색칠하세요</div>
    <div class="palette" id="t1-palette"></div>
    <div>
      <button class="btn btn-s" onclick="resetTab(1)">🔄 초기화</button>
      <button class="btn btn-p" onclick="checkTab(1)">✅ 확인</button>
      <button class="btn btn-p" onclick="autoColor(1)">⚡ 자동 색칠</button>
    </div>
    <div class="status-bar s-neutral" id="t1-status">🖌️ 색을 고른 뒤 영역을 클릭하여 색칠하세요</div>
    <div class="celebrate" id="t1-celebrate">🎉 완성! 최소 몇 가지 색으로 색칠할 수 있었나요? 🎉</div>
  </div>
  <div class="card" style="text-align:center;">
    <svg viewBox="0 0 550 390" style="width:min(550px,95vw);height:auto;display:block;margin:0 auto;">
      <!-- A: left rectangle -->
      <rect id="t1-A" class="region" x="20" y="20" width="165" height="295" rx="4" onclick="paint(1,'A')"/>
      <!-- C: upper-right (with oval hole via evenodd) -->
      <path id="t1-C" class="region" fill-rule="evenodd" onclick="paint(1,'C')"
            d="M 185,20 L 530,20 L 530,205 L 185,205 Z M 457,205 A 108,72 0 1,0 243,205 A 108,72 0 1,0 457,205 Z"/>
      <!-- B: lower-right -->
      <rect id="t1-B" class="region" x="185" y="205" width="345" height="110" rx="4" onclick="paint(1,'B')"/>
      <!-- D: oval (straddling C-B boundary at y=205) -->
      <ellipse id="t1-D" class="region" cx="350" cy="205" rx="108" ry="72" onclick="paint(1,'D')"/>
      <!-- E: bottom strip (full width) -->
      <rect id="t1-E" class="region" x="20" y="315" width="510" height="60" rx="4" onclick="paint(1,'E')"/>
      <!-- Dividing lines (visual guides) -->
      <line x1="185" y1="20" x2="185" y2="315" stroke="#444466" stroke-width="2"/>
      <line x1="20" y1="315" x2="530" y2="315" stroke="#444466" stroke-width="2"/>
      <!-- Labels -->
      <text x="103" y="170" fill="#fff" font-size="32" font-weight="bold" text-anchor="middle" pointer-events="none">A</text>
      <text x="490" y="45" fill="#fff" font-size="26" font-weight="bold" text-anchor="middle" pointer-events="none">C</text>
      <text x="350" y="210" fill="#fff" font-size="26" font-weight="bold" text-anchor="middle" pointer-events="none">D</text>
      <text x="450" y="265" fill="#fff" font-size="26" font-weight="bold" text-anchor="middle" pointer-events="none">B</text>
      <text x="275" y="352" fill="#fff" font-size="22" font-weight="bold" text-anchor="middle" pointer-events="none">E</text>
    </svg>
    <div style="font-size:12px;color:#778;margin-top:8px;">
      인접 관계: A↔B, A↔C, A↔E, B↔C, B↔D, B↔E, C↔D
    </div>
  </div>
  <div class="card">
    <div style="font-size:14px;font-weight:bold;color:#aab;margin-bottom:10px;">💡 탐구 포인트</div>
    <ul style="list-style:none;display:flex;flex-direction:column;gap:8px;font-size:13px;color:#bbc;line-height:1.7;">
      <li>🔷 A, B, C는 서로 모두 인접하므로 최소 <b style="color:#FFD700">3가지</b> 색이 필요합니다.</li>
      <li>🔷 D는 B와 C에만 인접, E는 A와 B에만 인접합니다.</li>
      <li>🔷 색의 수를 바꿔가며 실험해보세요! 최소 몇 가지 색으로 완성할 수 있나요?</li>
      <li>🔷 같은 색을 여러 영역에 써도 되지만, <b style="color:#FF6B6B">인접한 두 영역은 반드시 다른 색</b>이어야 합니다.</li>
    </ul>
  </div>
</div>
<!-- ===== TAB 2: Seoul map ===== -->
<div class="tab-content">
  <div class="title-bar">
    <h2>🏙️ 서울 25개 자치구 지도 색칠</h2>
    <p>서울특별시 25개 자치구를 직접 색칠해 보세요. 인접한 자치구는 서로 다른 색으로 칠해야 합니다. 몇 가지 색으로 완성할 수 있을까요?</p>
  </div>
  <div class="card">
    <div style="font-size:13px;color:#aab;margin-bottom:6px;">🎨 색상 개수 설정 후 색칠하세요</div>
    <div class="nctrl">
      <span class="color-num-label">색 개수:</span>
      <button class="nc-btn" onclick="updateNColors(2,-1)">−</button>
      <span class="nc-val" id="t2-ncolors">4</span>
      <button class="nc-btn" onclick="updateNColors(2,1)">+</button>
      <span style="font-size:12px;color:#778;">(최소 몇 가지 색으로 완성할 수 있나요?)</span>
    </div>
    <div class="palette" id="t2-palette"></div>
    <div>
      <button class="btn btn-s" onclick="resetTab(2)">🔄 초기화</button>
      <button class="btn btn-p" onclick="checkTab(2)">✅ 확인</button>
      <button class="btn btn-p" onclick="autoColor(2)">⚡ 자동 색칠</button>
    </div>
    <div class="status-bar s-neutral" id="t2-status">🖌️ 색을 고른 뒤 자치구를 클릭하여 색칠하세요</div>
    <div class="celebrate" id="t2-celebrate">🎉 완성! 서울 25개 자치구를 인접 규칙에 맞게 색칠했어요! 🎉</div>
  </div>
  <div class="card" style="padding:6px;">
    <div id="seoulMap" class="leaf-map"></div>
    <div style="font-size:11px;color:#667;margin-top:6px;padding:4px;">※ 대한민국 통계청 행정구역 경계 데이터 기반 (southkorea/seoul-maps). 지도를 드래그/확대·축소할 수 있습니다.</div>
  </div>
</div>
<!-- ===== TAB 3: USA grid ===== -->
<div class="tab-content">
  <div class="title-bar">
    <h2>🇺🇸 미국 50개 주 지도 색칠</h2>
    <p>미국 50개 주를 직접 색칠해 보세요. 인접한 주는 서로 다른 색으로 칠해야 합니다. 몇 가지 색으로 완성할 수 있을까요? (알래스카·하와이 포함)</p>
  </div>
  <div class="card">
    <div style="font-size:13px;color:#aab;margin-bottom:6px;">🎨 색상 개수 설정 후 주를 클릭하여 색칠하세요</div>
    <div class="nctrl">
      <span class="color-num-label">색 개수:</span>
      <button class="nc-btn" onclick="updateNColors(3,-1)">−</button>
      <span class="nc-val" id="t3-ncolors">4</span>
      <button class="nc-btn" onclick="updateNColors(3,1)">+</button>
      <span style="font-size:12px;color:#778;">(4색 정리: 평면 지도는 항상 4가지 색으로 충분!)</span>
    </div>
    <div class="palette" id="t3-palette"></div>
    <div>
      <button class="btn btn-s" onclick="resetTab(3)">🔄 초기화</button>
      <button class="btn btn-p" onclick="checkTab(3)">✅ 확인</button>
      <button class="btn btn-p" onclick="autoColor(3)">⚡ 자동 색칠</button>
    </div>
    <div class="status-bar s-neutral" id="t3-status">🖌️ 색을 고른 뒤 주를 클릭하여 색칠하세요</div>
    <div class="celebrate" id="t3-celebrate">🎉 완성! 미국 50개 주를 인접 규칙에 맞게 색칠했어요! 🎉</div>
  </div>
  <div class="card" style="padding:6px;">
    <div id="usaMap" class="leaf-map"></div>
    <div style="font-size:11px;color:#667;margin-top:6px;padding:4px;">※ 알래스카·하와이 포함. 지도를 드래그·확대·축소할 수 있습니다.</div>
  </div>
</div>
<!-- ===== TAB 4: 4-color theorem ===== -->
<div class="tab-content">
  <div class="title-bar">
    <h2>🎨 4색 정리 (Four Color Theorem)</h2>
    <p>평면 위의 어떤 지도도 단 4가지 색만으로 인접한 나라(영역)를 서로 다른 색으로 칠할 수 있다는 수학적 정리를 탐구합니다.</p>
  </div>

  <div class="th-card">
    <h3>🔑 4색 정리란?</h3>
    <p>
      <b style="color:#FFD700">4색 정리</b>는 "평면 위에 그려진 어떤 지도에서도, 서로 인접한 영역이 항상 다른 색이 되도록
      칠하기 위해 필요한 최소 색의 수는 4가지 이하이다"라는 정리입니다.
    </p>
    <ul style="margin-top:10px;">
      <li>1852년 프란시스 거스리(Francis Guthrie)가 처음 이 문제를 제기했습니다.</li>
      <li>120년 이상 증명되지 못했던 난제로, 수학자들을 오랫동안 괴롭혔습니다.</li>
      <li>1976년 아펠(Appel)과 하켄(Haken)이 컴퓨터를 이용해 최초로 증명했습니다.</li>
      <li>이는 역사상 최초의 <b style="color:#3ecef7">컴퓨터 보조 증명</b>으로, 수학계에 큰 논쟁을 일으켰습니다.</li>
    </ul>
  </div>

  <div class="hi-box">
    <p>🗺️ 어떤 복잡한 지도라도<br><span style="font-size:22px;color:#FFD700">단 4가지 색</span>으로 인접한 영역이 서로 다르게 색칠할 수 있습니다!</p>
  </div>

  <div class="th-card">
    <h3>🧩 4색이 반드시 필요한 경우</h3>
    <p>아래 지도는 4개의 영역이 <b>서로 모두 인접</b>합니다 (완전 그래프 K₄).<br>
    반드시 4가지 색이 필요합니다. 직접 색칠해 보세요!</p>
    <div style="font-size:13px;color:#aab;margin:10px 0 6px;">🎨 색상을 선택하고 영역을 클릭하여 색칠하세요</div>
    <div class="palette" id="t4-palette"></div>
    <div>
      <button class="btn btn-s" onclick="resetTab(4)">🔄 초기화</button>
      <button class="btn btn-p" onclick="checkTab(4)">✅ 확인</button>
      <button class="btn btn-p" onclick="autoColor(4)">⚡ 자동 색칠</button>
      <button class="btn btn-s" onclick="showDemo4()">💡 왜 3색으로 불가능할까?</button>
    </div>
    <div class="status-bar s-neutral" id="t4-status">🖌️ 4개 영역이 서로 모두 인접 — 최소 4색이 필요합니다!</div>
    <div class="celebrate" id="t4-celebrate">🎉 4색으로 완성! 이 지도는 3색으로는 불가능합니다. 4색 정리를 체험했어요! 🎉</div>
    <div style="text-align:center;margin-top:12px;">
      <svg viewBox="0 0 500 400" style="width:min(480px,95vw);height:auto;display:block;margin:0 auto;">
        <!-- K4 planar map: outer rect minus triangle = F4, 3 inner triangles -->
        <!-- Outer boundary box -->
        <rect x="0" y="0" width="500" height="400" fill="#12122a" rx="8"/>
        <!-- F4: outer region (rect minus outer triangle, evenodd) -->
        <path id="t4-F4" class="region" fill-rule="evenodd" onclick="paint(4,'F4')"
              d="M 5,5 L 495,5 L 495,395 L 5,395 Z M 250,35 L 75,365 L 425,365 Z"/>
        <!-- F1: left inner triangle -->
        <polygon id="t4-F1" class="region" points="250,35 250,220 75,365" onclick="paint(4,'F1')"/>
        <!-- F2: right inner triangle -->
        <polygon id="t4-F2" class="region" points="250,35 425,365 250,220" onclick="paint(4,'F2')"/>
        <!-- F3: bottom inner triangle -->
        <polygon id="t4-F3" class="region" points="250,220 75,365 425,365" onclick="paint(4,'F3')"/>
        <!-- Edges of the outer triangle (visual guide) -->
        <polygon points="250,35 75,365 425,365" fill="none" stroke="#7c6fff" stroke-width="2"/>
        <!-- Inner edges -->
        <line x1="250" y1="35" x2="250" y2="220" stroke="#7c6fff" stroke-width="1.5"/>
        <line x1="75" y1="365" x2="250" y2="220" stroke="#7c6fff" stroke-width="1.5"/>
        <line x1="425" y1="365" x2="250" y2="220" stroke="#7c6fff" stroke-width="1.5"/>
        <!-- Labels -->
        <text x="50" y="30" fill="#eef" font-size="16" font-weight="bold" text-anchor="middle" pointer-events="none">F4</text>
        <text x="185" y="230" fill="#eef" font-size="16" font-weight="bold" text-anchor="middle" pointer-events="none">F1</text>
        <text x="315" y="230" fill="#eef" font-size="16" font-weight="bold" text-anchor="middle" pointer-events="none">F2</text>
        <text x="250" y="330" fill="#eef" font-size="16" font-weight="bold" text-anchor="middle" pointer-events="none">F3</text>
        <!-- Adjacency labels -->
        <text x="250" y="390" fill="#7c6fff88" font-size="10" text-anchor="middle" pointer-events="none">F1·F2·F3·F4 모두 서로 인접</text>
      </svg>
    </div>
    <div id="demo4-msg" style="display:none;background:#1c1c3e;border-radius:10px;padding:12px;margin-top:10px;font-size:13px;color:#bbc;line-height:1.8;">
      🔍 <b style="color:#FFD700">3가지 색으로 시도하면?</b><br>
      F1, F2, F3은 서로 모두 인접하므로 3가지 다른 색(예: 빨강, 청록, 하늘)이 필요합니다.<br>
      F4는 F1·F2·F3 모두와 인접하므로 이미 사용된 3가지 색 이외의 색, 즉 <b style="color:#FF6B6B">4번째 색</b>이 반드시 필요합니다!
    </div>
  </div>

  <div class="th-card">
    <h3>📊 4색 정리와 그래프 이론</h3>
    <ul>
      <li>지도의 각 영역을 <b>꼭짓점(vertex)</b>, 인접 관계를 <b>변(edge)</b>으로 나타내면 <b style="color:#3ecef7">그래프</b>가 됩니다.</li>
      <li>지도 색칠 문제는 그래프의 <b style="color:#FFD700">채색 수(chromatic number)</b>를 구하는 문제입니다.</li>
      <li>4색 정리는 "평면 그래프의 채색 수는 항상 4 이하"임을 의미합니다.</li>
      <li>하지만 3차원 공간의 지도나 구멍이 있는 면(토러스 등)에서는 더 많은 색이 필요할 수 있습니다.</li>
    </ul>
  </div>

  <div class="th-card">
    <h3>🌍 실생활 속의 4색 정리</h3>
    <ul>
      <li>📡 <b>이동통신 주파수 배치</b>: 인접 기지국이 같은 주파수를 쓰지 않도록 최소 주파수 종류를 결정</li>
      <li>📅 <b>시간표 작성</b>: 같은 시간에 같은 자원을 쓰면 안 되는 작업 스케줄링</li>
      <li>🧬 <b>유전자 지도</b>: DNA 서열 분석에서 겹치는 구간 배치</li>
      <li>🎨 <b>인쇄 기술</b>: 인쇄판 수를 최소화하는 색상 배치</li>
    </ul>
  </div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const COLORS=['#FF6B6B','#4ECDC4','#45B7D1','#FFA726','#9CCC65','#CE93D8','#FFD54F','#78909C'];
const CNAMES=['빨강','청록','하늘','주황','초록','보라','노랑','회색'];
const DEFAULT_FILL='#2a2a55';

// Adjacency data
const ADJ={
  0:{A:['B','D'],B:['A','C'],C:['B','D'],D:['A','C']},
  1:{A:['B','C','E'],B:['A','C','D','E'],C:['A','B','D'],D:['B','C'],E:['A','B']},
  2:{
    '도봉':['강북','노원'],'노원':['도봉','강북','성북','중랑'],
    '강북':['도봉','노원','성북','은평','서대문'],
    '성북':['강북','노원','중랑','동대문','종로'],
    '중랑':['노원','성북','동대문','광진'],
    '은평':['강북','서대문','마포'],
    '서대문':['강북','은평','종로','마포','용산'],
    '종로':['성북','서대문','동대문','중구','용산','마포'],
    '중구':['종로','동대문','성동','용산'],
    '동대문':['성북','중랑','광진','종로','중구','성동'],
    '광진':['중랑','동대문','성동','강동'],
    '마포':['은평','서대문','종로','용산','영등포','강서'],
    '용산':['서대문','종로','중구','마포','동작','영등포'],
    '성동':['동대문','광진','강동','중구','서초'],
    '강동':['광진','성동','강남','송파'],
    '강서':['마포','양천','영등포'],
    '양천':['강서','영등포','구로'],
    '영등포':['강서','양천','마포','용산','동작','구로'],
    '구로':['양천','영등포','금천','동작'],
    '동작':['영등포','용산','서초','관악','구로','금천'],
    '금천':['구로','관악','동작'],
    '관악':['금천','동작','서초'],
    '서초':['동작','관악','강남','성동'],
    '강남':['서초','성동','강동','송파'],
    '송파':['강남','강동']
  },
  3:{
    'AL':['FL','GA','MS','TN'],'AK':[],'AZ':['CA','CO','NM','NV','UT'],
    'AR':['LA','MO','MS','OK','TN','TX'],'CA':['AZ','NV','OR'],
    'CO':['AZ','KS','NE','NM','OK','UT','WY'],'CT':['MA','NY','RI'],
    'DE':['MD','NJ','PA'],'FL':['AL','GA'],'GA':['AL','FL','NC','SC','TN'],'HI':[],
    'ID':['MT','NV','OR','UT','WA','WY'],'IL':['IA','IN','KY','MO','WI'],
    'IN':['IL','KY','MI','OH'],'IA':['IL','MN','MO','NE','SD','WI'],
    'KS':['CO','MO','NE','OK'],'KY':['IL','IN','MO','OH','TN','VA','WV'],
    'LA':['AR','MS','TX'],'ME':['NH'],
    'MD':['DE','PA','VA','WV'],'MA':['CT','NH','NY','RI','VT'],
    'MI':['IN','OH','WI'],'MN':['IA','ND','SD','WI'],
    'MS':['AL','AR','LA','TN'],'MO':['AR','IA','IL','KS','KY','NE','OK','TN'],
    'MT':['ID','ND','SD','WY'],'NE':['CO','IA','KS','MO','SD','WY'],
    'NV':['AZ','CA','ID','OR','UT'],'NH':['MA','ME','VT'],
    'NJ':['DE','NY','PA'],'NM':['AZ','CO','OK','TX','UT'],
    'NY':['CT','MA','NJ','PA','VT'],'NC':['GA','SC','TN','VA'],
    'ND':['MN','MT','SD'],'OH':['IN','KY','MI','PA','WV'],
    'OK':['AR','CO','KS','MO','NM','TX'],'OR':['CA','ID','NV','WA'],
    'PA':['DE','MD','NJ','NY','OH','WV'],'RI':['CT','MA'],
    'SC':['GA','NC'],'SD':['IA','MN','MT','ND','NE','WY'],
    'TN':['AL','AR','GA','KY','MS','MO','NC','VA'],'TX':['AR','LA','NM','OK'],
    'UT':['AZ','CO','ID','NV','NM','WY'],'VT':['MA','NH','NY'],
    'VA':['KY','MD','NC','TN','WV'],'WA':['ID','OR'],
    'WV':['KY','MD','OH','PA','VA'],'WI':['IA','IL','MI','MN'],
    'WY':['CO','ID','MT','NE','SD','UT']
  },
  4:{F1:['F2','F3','F4'],F2:['F1','F3','F4'],F3:['F1','F2','F4'],F4:['F1','F2','F3']}
};

// State name → abbreviation lookup (for GeoJSON property fallback)
const STATE_ABBR={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA',
  'Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA',
  'Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA',
  'Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD',
  'Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS',
  'Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH',
  'New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC',
  'North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA',
  'Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN',
  'Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA',
  'West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'};

const N_COLORS=[4,4,4,4,4];
const CS=[{},{},{},{},{}];
const SEL=[0,0,0,0,0];

// Leaflet instances (tabs 2 & 3)
const LEAF_MAPS=[null,null,null,null,null];
const LEAF_LAYERS=[{},{},{},{},{}];
const LEAF_INITED=[false,false,false,false,false];

// ── core helpers ───────────────────────────────────────────────────────────
function isLight(hex){
  const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);
  return(r*0.299+g*0.587+b*0.114)>155;
}

function applyRegionStyle(t,rid,colorIdx,bad){
  const color=colorIdx>=0?COLORS[colorIdx]:null;
  if(t===2||t===3){
    const layer=LEAF_LAYERS[t][rid];
    if(!layer)return;
    layer.setStyle({
      fillColor:color||DEFAULT_FILL,
      fillOpacity:color?0.82:0.55,
      color:bad?'#ff4444':'#ffffff55',
      weight:bad?2.5:0.8
    });
  }else{
    const el=document.getElementById('t'+t+'-'+rid);
    if(!el)return;
    if(el.tagName==='DIV'){el.style.background=color||'';el.style.color=color?(isLight(color)?'#222':'#fff'):'';}
    else el.style.fill=color||'';
    el.classList.toggle('bad',!!bad);
  }
}

// ── palette ───────────────────────────────────────────────────────────────
function initPalette(t){
  const el=document.getElementById('t'+t+'-palette');
  if(!el)return;
  el.innerHTML='';
  for(let i=0;i<N_COLORS[t];i++){
    const s=document.createElement('div');
    s.className='swatch'+(SEL[t]===i?' sel':'');
    s.style.background=COLORS[i];s.title=CNAMES[i];
    s.onclick=()=>{SEL[t]=i;initPalette(t);};
    el.appendChild(s);
  }
  const e=document.createElement('div');
  e.className='erase-btn'+(SEL[t]===-1?' sel':'');
  e.title='지우기';e.textContent='🧹';
  e.onclick=()=>{SEL[t]=-1;initPalette(t);};
  el.appendChild(e);
}

// ── paint / check / reset / auto ──────────────────────────────────────────
function paint(t,rid){
  if(SEL[t]===-1)delete CS[t][rid];
  else CS[t][rid]=SEL[t];
  applyRegionStyle(t,rid,CS[t][rid]??-1,false);
  checkTabSilent(t);
}
function checkTabSilent(t){return checkTab(t,true);}

function checkTab(t,silent=false){
  const adj=ADJ[t],cs=CS[t];
  const regions=Object.keys(adj);
  const bad=new Set();
  for(const[r,nb]of Object.entries(adj))
    for(const n of nb)
      if(cs[r]!==undefined&&cs[n]!==undefined&&cs[r]===cs[n]){bad.add(r);bad.add(n);}
  regions.forEach(r=>applyRegionStyle(t,r,cs[r]??-1,bad.has(r)));
  const allDone=regions.every(r=>cs[r]!==undefined);
  const st=document.getElementById('t'+t+'-status'),ce=document.getElementById('t'+t+'-celebrate');
  if(allDone&&bad.size===0){
    if(st){st.className='status-bar s-ok';st.textContent='🎉 완성! 모든 인접 영역이 서로 다른 색입니다!';}
    if(ce)ce.classList.add('show');
  }else{
    if(ce)ce.classList.remove('show');
    if(!silent||bad.size>0){
      if(st){
        st.className='status-bar '+(bad.size>0?'s-err':'s-neutral');
        st.textContent=bad.size>0?'⚠️ 인접 구역 '+bad.size+'곳이 같은 색입니다!':
          '🖌️ '+regions.filter(r=>cs[r]!==undefined).length+'/'+regions.length+' 구역 색칠됨';
      }
    }
  }
  return bad.size===0&&allDone;
}

function resetTab(t){
  CS[t]={};
  Object.keys(ADJ[t]).forEach(r=>applyRegionStyle(t,r,-1,false));
  const st=document.getElementById('t'+t+'-status');
  if(st){st.className='status-bar s-neutral';st.textContent='🖌️ 색을 고른 뒤 영역을 클릭하여 색칠하세요';}
  const ce=document.getElementById('t'+t+'-celebrate');
  if(ce)ce.classList.remove('show');
}

function autoColor(t){
  CS[t]={};
  const adj=ADJ[t];
  const sorted=[...Object.keys(adj)].sort((a,b)=>adj[b].length-adj[a].length);
  for(const r of sorted){
    const used=new Set((adj[r]||[]).map(n=>CS[t][n]).filter(c=>c!==undefined));
    let c=0;while(used.has(c))c++;
    if(c<N_COLORS[t]){CS[t][r]=c;applyRegionStyle(t,r,c,false);}
  }
  checkTab(t,false);
}

function updateNColors(t,d){
  const n=Math.max(2,Math.min(8,N_COLORS[t]+d));
  N_COLORS[t]=n;
  const el=document.getElementById('t'+t+'-ncolors');
  if(el)el.textContent=n;
  resetTab(t);initPalette(t);
}

// ── SVG tooltip (tabs 0 & 1) ──────────────────────────────────────────────
function showTip(e,text){
  const t=document.getElementById('tip');
  t.textContent=text;t.style.display='block';
  t.style.left=(e.clientX+12)+'px';t.style.top=(e.clientY-4)+'px';
}
function hideTip(){document.getElementById('tip').style.display='none';}

// ── Leaflet map utilities ─────────────────────────────────────────────────
function leafStyle(){
  return{fillColor:DEFAULT_FILL,fillOpacity:0.55,color:'#ffffff55',weight:0.8};
}

function normalizeSeoulName(name){
  if(!name)return'';
  // "강남구"→"강남", but "중구"(len=2) stays "중구"
  if(name.endsWith('구')&&name.length>2)return name.slice(0,-1);
  return name;
}

function initSeoulMap(){
  if(LEAF_INITED[2])return;
  LEAF_INITED[2]=true;
  const map=L.map('seoulMap',{zoomControl:true,scrollWheelZoom:false});
  LEAF_MAPS[2]=map;
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png',{
    attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> © <a href="https://carto.com/">CARTO</a>',
    maxZoom:19
  }).addTo(map);
  const loadingEl=document.getElementById('seoulMap');
  if(loadingEl)loadingEl.style.cursor='wait';
  fetch('https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json')
    .then(r=>r.json())
    .then(data=>{
      if(loadingEl)loadingEl.style.cursor='';
      const geoLayer=L.geoJSON(data,{
        style:leafStyle(),
        onEachFeature:(feature,featureLayer)=>{
          const props=feature.properties||{};
          const rawName=props.SIG_KOR_NM||props.sig_kor_nm||props.NAME_2||props.name||'';
          const rid=normalizeSeoulName(rawName);
          if(rid&&ADJ[2][rid]!==undefined){
            LEAF_LAYERS[2][rid]=featureLayer;
            featureLayer.on('click',()=>paint(2,rid));
            featureLayer.bindTooltip(rid,{
              sticky:true,className:'leaflet-tooltip-dark',direction:'top',offset:[0,-4]
            });
          }
        }
      }).addTo(map);
      map.fitBounds(geoLayer.getBounds());
    })
    .catch(()=>{
      if(loadingEl)loadingEl.innerHTML='<div style="color:#f77;text-align:center;padding:20px;">지도 데이터를 불러올 수 없습니다. 인터넷 연결을 확인해 주세요.</div>';
    });
}

function initUSAMap(){
  if(LEAF_INITED[3])return;
  LEAF_INITED[3]=true;
  const map=L.map('usaMap',{zoomControl:true,scrollWheelZoom:false,center:[38,-96],zoom:4});
  LEAF_MAPS[3]=map;
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png',{
    attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> © <a href="https://carto.com/">CARTO</a>',
    maxZoom:19
  }).addTo(map);
  const loadingEl=document.getElementById('usaMap');
  fetch('https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/us-states.json')
    .then(r=>r.json())
    .then(data=>{
      const geoLayer=L.geoJSON(data,{
        style:leafStyle(),
        onEachFeature:(feature,featureLayer)=>{
          // feature.id is the 2-letter state abbreviation in folium's GeoJSON
          let rid=typeof feature.id==='string'&&feature.id.length===2?feature.id:null;
          if(!rid){
            const name=(feature.properties&&(feature.properties.name||feature.properties.NAME))||'';
            rid=STATE_ABBR[name]||null;
          }
          if(rid&&ADJ[3][rid]!==undefined){
            LEAF_LAYERS[3][rid]=featureLayer;
            featureLayer.on('click',()=>paint(3,rid));
            const fullName=(feature.properties&&(feature.properties.name||feature.properties.NAME))||rid;
            featureLayer.bindTooltip(rid+' — '+fullName,{
              sticky:true,className:'leaflet-tooltip-dark',direction:'top',offset:[0,-4]
            });
          }
        }
      }).addTo(map);
      // 미국 본토(48개 주) 위주로 표시
      map.fitBounds([[24.4,-124.8],[49.4,-66.9]]);
    })
    .catch(()=>{
      if(loadingEl)loadingEl.innerHTML='<div style="color:#f77;text-align:center;padding:20px;">지도 데이터를 불러올 수 없습니다. 인터넷 연결을 확인해 주세요.</div>';
    });
}

// ── tab switching ──────────────────────────────────────────────────────────
function showTab(n){
  document.querySelectorAll('.tab-content').forEach((el,i)=>el.classList.toggle('active',i===n));
  document.querySelectorAll('.tab-btn').forEach((el,i)=>el.classList.toggle('active',i===n));
  if(n===2){
    setTimeout(()=>{
      initSeoulMap();
      if(LEAF_MAPS[2])LEAF_MAPS[2].invalidateSize();
    },120);
  }else if(n===3){
    setTimeout(()=>{
      initUSAMap();
      if(LEAF_MAPS[3])LEAF_MAPS[3].invalidateSize();
    },120);
  }
}

function showDemo4(){
  const el=document.getElementById('demo4-msg');
  if(el)el.style.display=el.style.display==='none'?'block':'none';
}

function sendHeight(){
  const h=document.documentElement.scrollHeight;
  window.parent.postMessage({type:'streamlit:setFrameHeight',height:h+20},'*');
}

// Init
for(let t=0;t<=4;t++)initPalette(t);
window.addEventListener('load',()=>setTimeout(sendHeight,300));
document.querySelectorAll('.tab-btn').forEach(b=>b.addEventListener('click',()=>setTimeout(sendHeight,200)));
</script>
</body>
</html>
"""

def render():
    components.html(_HTML, height=1700, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
