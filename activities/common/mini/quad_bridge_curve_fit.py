# activities/common/mini/quad_bridge_curve_fit.py
"""
다리 사진에서 이차함수 찾기
실제 다리 사진(선암사 무지개다리·대전 엑스포교·금문교)에
이차함수 y=a(x-h)²+k 그래프를 겹쳐 계수를 찾는 인터랙티브 미니활동
이차함수 최대·최소 단원 연계: 꼭짓점(최댓값/최솟값)을 실생활과 연결
"""
import base64
import io
import os

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image as PILImage

from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "다리이차함수찾기"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 성찰 질문에 답해 보세요**"},
    {
        "key":    "꼭짓점의미",
        "label":  "① 이차함수 y=a(x-h)²+k에서 꼭짓점 (h, k)는 아치교와 현수교 각각에서 어떤 물리적 의미를 가지나요? 두 경우를 구분하여 설명하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "a부호역할",
        "label":  "② 계수 a가 양수일 때와 음수일 때 그래프 모양이 어떻게 달라지나요? 이것이 최대·최솟값의 존재와 어떻게 연결되는지 다리의 예를 들어 설명하세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "대칭축활용",
        "label":  "③ 대칭축 x=h가 실제 다리 구조에서 무엇을 의미하는지 설명하고, 다리를 설계할 때 대칭축 정보가 왜 유용한지 생각해 보세요.",
        "type":   "text_area",
        "height": 100,
    },
    {
        "key":    "실생활계산",
        "label":  "④ 찾은 이차함수 식을 이용하면 다리의 어떤 정보(최고 높이, 교각 간 거리, 수면과의 여유 등)를 계산할 수 있을까요? 구체적으로 적어보세요.",
        "type":   "text_area",
        "height": 100,
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

META = {
    "title":       "🌉 다리에서 이차함수 찾기",
    "description": "실제 다리 사진(선암사 무지개다리·대전 엑스포교·금문교)에 이차함수 그래프를 직접 맞추며 꼭짓점(최대·최솟값)과 대칭축을 실생활과 연결하는 인터랙티브 탐구 활동입니다.",
    "order":       242,
    "hidden":      False,
}


def _b64(filename: str) -> str:
    """Load image, resize to canvas dimensions, return base64 JPEG string."""
    path = os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "commonmath", filename)
    )
    with PILImage.open(path) as img:
        img = img.convert("RGB")
        img.thumbnail((660, 380), PILImage.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=78)
        return base64.b64encode(buf.getvalue()).decode()


_HTML_TMPL = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Malgun Gothic','Apple SD Gothic Neo',system-ui,sans-serif;
  background:linear-gradient(155deg,#060917 0%,#0e1630 60%,#080f1c 100%);
  color:#e2e8ff;
  padding:8px 10px 16px;
  overflow-y:auto;
}

/* ── 탭 ── */
.tabs{display:flex;gap:3px;border-bottom:2px solid #1e3060;margin-bottom:0}
.tab-btn{
  padding:6px 11px;border:none;border-radius:8px 8px 0 0;
  background:#0a1020;color:#556688;cursor:pointer;font-size:.78rem;
  font-family:inherit;transition:all .2s;border-bottom:2px solid transparent;margin-bottom:-2px;
}
.tab-btn:hover{background:#131e38;color:#99aacc}
.tab-btn.active{background:#151f3a;color:#ffd700;border-bottom:2px solid #ffd700;font-weight:700}

/* ── 패널 ── */
.tab-panel{display:none}
.tab-panel.active{display:block}

/* ── 안내 단계 ── */
.guide-steps{
  display:flex;gap:5px;margin:6px 0 5px;flex-wrap:wrap;
}
.step{
  flex:1;min-width:130px;background:#050d20;border-radius:7px;
  padding:4px 9px;border-left:3px solid #1d4ed8;font-size:.76rem;color:#93c5fd;
}
.step b{color:#ffd700;}

/* ── 다리 정보 바 ── */
.bridge-info{
  display:flex;align-items:center;gap:8px;
  padding:5px 9px;background:#0c1428;border-radius:7px;
  margin:5px 0 4px;border:1px solid #1a2a50;font-size:.79rem;
}
.badge{
  background:#1e3a8a;color:#93c5fd;border-radius:4px;
  padding:2px 7px;font-weight:700;white-space:nowrap;flex-shrink:0;
}
.badge.cable{background:#065f46;color:#6ee7b7;}
.badge.user{background:#3b1f6e;color:#c4b5fd;}

/* ── 캔버스 ── */
.canvas-wrap{
  position:relative;width:660px;height:370px;
  border:2px solid #1e3060;border-radius:9px;overflow:hidden;
  background:#000;margin:0 auto;
}
canvas{display:block;}

/* ── 수식 표시 ── */
.eq-display{
  text-align:center;padding:4px;font-size:1.05rem;
  font-weight:700;color:#ffd700;min-height:28px;letter-spacing:.3px;
}

/* ── 슬라이더 ── */
.slider-section{
  background:#0c1428;border-radius:9px;padding:8px 12px;
  margin-top:5px;border:1px solid #1a2a50;
}
.slider-row{
  display:flex;align-items:center;gap:7px;margin:4px 0;font-size:.82rem;
}
.slider-label{width:30px;font-weight:700;color:#93c5fd;text-align:right;flex-shrink:0}
.slider-val{width:48px;text-align:right;color:#ffd700;font-weight:700;flex-shrink:0;font-size:.88rem;}
.slider-desc{color:#4a6080;font-size:.76rem;flex:1}
input[type=range]{flex:1;min-width:180px;height:5px;cursor:pointer;accent-color:#3b82f6;}

/* ── 정보 카드 ── */
.info-cards{display:flex;gap:6px;margin-top:6px;flex-wrap:wrap;}
.info-card{
  flex:1;min-width:130px;background:#0c1428;border-radius:7px;
  padding:5px 9px;border:1px solid #1a2a50;font-size:.78rem;text-align:center;
}
.info-card .label{color:#4a6080;margin-bottom:2px;font-size:.74rem;}
.info-card .value{color:#ffd700;font-weight:700;font-size:.9rem;}

/* ── 버튼 ── */
.btn-row{display:flex;gap:6px;margin-top:6px;flex-wrap:wrap;}
.btn{
  padding:6px 12px;border:none;border-radius:7px;cursor:pointer;
  font-family:inherit;font-size:.78rem;font-weight:600;transition:all .15s;
}
.btn-hint{background:#713f12;color:#fde68a;}
.btn-hint:hover{background:#92400e;}
.btn-reset{background:#1e293b;color:#94a3b8;}
.btn-reset:hover{background:#334155;}

/* ── 힌트 박스 ── */
.hint-box{
  display:none;margin-top:6px;padding:7px 11px;
  background:#1a1000;border:1px solid #92400e;border-radius:7px;
  font-size:.79rem;color:#fde68a;line-height:1.65;
}
.hint-box.show{display:block;}

/* ── 업로드 구역 ── */
.upload-zone{
  border:2px dashed #1e3060;border-radius:9px;padding:22px;
  text-align:center;margin:8px 0 0;color:#4a6080;cursor:pointer;transition:all .2s;
}
.upload-zone:hover{border-color:#3b82f6;color:#93c5fd;background:#050d20;}
.upload-zone input[type=file]{display:none;}

/* ── 좌표 범위 슬라이더 분리 ── */
.range-divider{
  margin-top:7px;padding-top:7px;border-top:1px solid #1a2a50;
}
.range-label{font-size:.74rem;color:#4a6080;margin-bottom:3px;}
</style>
</head>
<body>

<!-- 헤더 -->
<div style="display:flex;align-items:center;gap:10px;margin-bottom:5px;">
  <span style="font-size:1.1rem;font-weight:700;color:#93c5fd;">🌉 다리에서 이차함수 찾기</span>
  <span style="font-size:.77rem;color:#4a6080;">슬라이더로 그래프를 조정해 다리 곡선에 맞춰 보세요!</span>
</div>

<!-- 안내 단계 -->
<div class="guide-steps">
  <div class="step"><b>①</b> 사진 속 곡선을 관찰한다</div>
  <div class="step"><b>②</b> <b>a</b> 로 곡선 방향·폭 설정</div>
  <div class="step"><b>③</b> <b>h</b> 로 대칭축 좌우 이동</div>
  <div class="step"><b>④</b> <b>k</b> 로 꼭짓점 높이 조정</div>
  <div class="step"><b>⑤</b> 곡선이 일치하면 식 확인!</div>
</div>

<!-- 탭 -->
<div class="tabs">
  <button class="tab-btn active" onclick="showTab(0)">① 선암사 무지개다리</button>
  <button class="tab-btn" onclick="showTab(1)">② 대전 엑스포교</button>
  <button class="tab-btn" onclick="showTab(2)">③ 샌프란시스코 금문교</button>
  <button class="tab-btn" onclick="showTab(3)">📸 내 사진으로!</button>
</div>

<!-- ═══ 탭 0: 선암사 ═══ -->
<div id="panel0" class="tab-panel active">
  <div class="bridge-info">
    <span class="badge">아치교 ▼</span>
    <span><b>선암사 무지개다리</b> · 전남 순천 · 돌로 쌓은 반원형 아치 — <em>아치는 아래로 볼록 (a &lt; 0), 꼭짓점 = 최댓값(아치 최고점)</em></span>
  </div>
  <div class="canvas-wrap"><canvas id="cv0" width="660" height="370"></canvas></div>
  <div class="eq-display" id="eq0"></div>
  <div class="slider-section">
    <div class="slider-row">
      <span class="slider-label">a</span>
      <input type="range" id="a0" min="-3" max="0.5" step="0.05" value="-0.35">
      <span class="slider-val" id="av0"></span>
      <span class="slider-desc">곡선 방향·폭 (음수 → 아치 ▼, 절댓값 클수록 좁음)</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">h</span>
      <input type="range" id="h0" min="-2" max="12" step="0.1" value="5">
      <span class="slider-val" id="hv0"></span>
      <span class="slider-desc">대칭축 위치 — 꼭짓점 x좌표</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">k</span>
      <input type="range" id="k0" min="-2" max="8" step="0.1" value="3.8">
      <span class="slider-val" id="kv0"></span>
      <span class="slider-desc">꼭짓점 높이 — 아치의 <b>최댓값</b></span>
    </div>
  </div>
  <div class="info-cards">
    <div class="info-card"><div class="label">꼭짓점</div><div class="value" id="vtx0"></div></div>
    <div class="info-card"><div class="label">대칭축</div><div class="value" id="axis0"></div></div>
    <div class="info-card"><div class="label">최댓값 (아치 최고점)</div><div class="value" id="mm0"></div></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-hint" onclick="toggleHint(0)">💡 힌트</button>
    <button class="btn btn-reset" onclick="resetSliders(0)">↺ 초기화</button>
  </div>
  <div class="hint-box" id="hint0">
    🔍 <b>힌트:</b> 선암사 무지개다리는 반원에 가까운 아치 구조입니다.<br>
    • <b>a &lt; 0</b> — 아래로 볼록(최댓값)이어야 아치 모양이 됩니다.<br>
    • 다리가 좌우 대칭이므로 <b>h ≈ 5</b>로 시작하고, 아치 최고점 높이로 <b>k</b>를 조정하세요.<br>
    • |a|가 클수록 아치가 좁고 가파릅니다.
  </div>
</div>

<!-- ═══ 탭 1: 엑스포교 ═══ -->
<div id="panel1" class="tab-panel">
  <div class="bridge-info">
    <span class="badge">아치교 ▼</span>
    <span><b>대전 엑스포교</b> · 대전 · 강철 아치 구조 — <em>아치는 아래로 볼록 (a &lt; 0), 꼭짓점 = 최댓값(아치 최고점)</em></span>
  </div>
  <div class="canvas-wrap"><canvas id="cv1" width="660" height="370"></canvas></div>
  <div class="eq-display" id="eq1"></div>
  <div class="slider-section">
    <div class="slider-row">
      <span class="slider-label">a</span>
      <input type="range" id="a1" min="-3" max="0.5" step="0.05" value="-0.4">
      <span class="slider-val" id="av1"></span>
      <span class="slider-desc">곡선 방향·폭 (음수 → 아치 ▼)</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">h</span>
      <input type="range" id="h1" min="-2" max="12" step="0.1" value="5">
      <span class="slider-val" id="hv1"></span>
      <span class="slider-desc">대칭축 위치 — 꼭짓점 x좌표</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">k</span>
      <input type="range" id="k1" min="-2" max="9" step="0.1" value="4.5">
      <span class="slider-val" id="kv1"></span>
      <span class="slider-desc">꼭짓점 높이 — 아치의 <b>최댓값</b></span>
    </div>
  </div>
  <div class="info-cards">
    <div class="info-card"><div class="label">꼭짓점</div><div class="value" id="vtx1"></div></div>
    <div class="info-card"><div class="label">대칭축</div><div class="value" id="axis1"></div></div>
    <div class="info-card"><div class="label">최댓값 (아치 최고점)</div><div class="value" id="mm1"></div></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-hint" onclick="toggleHint(1)">💡 힌트</button>
    <button class="btn btn-reset" onclick="resetSliders(1)">↺ 초기화</button>
  </div>
  <div class="hint-box" id="hint1">
    🔍 <b>힌트:</b> 대전 엑스포교는 강철로 만든 아치 구조입니다.<br>
    • 아치 최고점을 꼭짓점(h, k)으로 설정하세요.<br>
    • 양 교각 발판이 x축과 만나는 지점을 찾으면 아치 폭을 알 수 있습니다.<br>
    • 그 두 점의 중간값이 대칭축 h가 됩니다.
  </div>
</div>

<!-- ═══ 탭 2: 금문교 ═══ -->
<div id="panel2" class="tab-panel">
  <div class="bridge-info">
    <span class="badge cable">현수교 ▲</span>
    <span><b>샌프란시스코 금문교</b> · 미국 캘리포니아 · 케이블이 아래로 처지는 현수교 — <em>케이블은 위로 볼록 (a &gt; 0), 꼭짓점 = 최솟값(케이블 최저점)</em></span>
  </div>
  <div class="canvas-wrap"><canvas id="cv2" width="660" height="370"></canvas></div>
  <div class="eq-display" id="eq2"></div>
  <div class="slider-section">
    <div class="slider-row">
      <span class="slider-label">a</span>
      <input type="range" id="a2" min="-0.5" max="3" step="0.01" value="0.1">
      <span class="slider-val" id="av2"></span>
      <span class="slider-desc">곡선 방향·폭 (양수 → 케이블 ▲, 작을수록 완만)</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">h</span>
      <input type="range" id="h2" min="-2" max="12" step="0.1" value="5">
      <span class="slider-val" id="hv2"></span>
      <span class="slider-desc">대칭축 위치 — 케이블 최저점 x좌표</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">k</span>
      <input type="range" id="k2" min="-1" max="7" step="0.1" value="0.8">
      <span class="slider-val" id="kv2"></span>
      <span class="slider-desc">꼭짓점 높이 — 케이블의 <b>최솟값</b></span>
    </div>
  </div>
  <div class="info-cards">
    <div class="info-card"><div class="label">꼭짓점</div><div class="value" id="vtx2"></div></div>
    <div class="info-card"><div class="label">대칭축</div><div class="value" id="axis2"></div></div>
    <div class="info-card"><div class="label">최솟값 (케이블 최저점)</div><div class="value" id="mm2"></div></div>
  </div>
  <div class="btn-row">
    <button class="btn btn-hint" onclick="toggleHint(2)">💡 힌트</button>
    <button class="btn btn-reset" onclick="resetSliders(2)">↺ 초기화</button>
  </div>
  <div class="hint-box" id="hint2">
    🔍 <b>힌트:</b> 금문교의 메인 케이블은 두 탑 사이에서 아래로 처집니다.<br>
    • <b>a &gt; 0</b> (양수) — 위로 볼록(최솟값)이어야 케이블 모양이 됩니다.<br>
    • 케이블 최저점(중간 아래처짐)이 꼭짓점(h, k)이며, 이것이 <b>최솟값</b>입니다.<br>
    • 두 탑의 x좌표 중간값이 대칭축 h가 됩니다.
  </div>
</div>

<!-- ═══ 탭 3: 내 사진 ═══ -->
<div id="panel3" class="tab-panel">
  <div class="bridge-info">
    <span class="badge user">직접 탐구</span>
    <span>이차곡선이 보이는 <b>내 사진</b>을 올려 이차함수를 직접 찾아보세요!</span>
  </div>

  <div class="upload-zone" id="uploadZone">
    <input type="file" id="fileInput" accept="image/*">
    <div onclick="document.getElementById('fileInput').click()" style="cursor:pointer;">
      <div style="font-size:2rem;margin-bottom:5px;">📷</div>
      <div style="font-size:.88rem;font-weight:600;color:#93c5fd;">클릭하거나 사진을 드래그해서 올리세요</div>
      <div style="font-size:.76rem;margin-top:3px;">다리, 분수, 무지개, 포물선 모양 물체 등 이차곡선을 찾아보세요!</div>
    </div>
  </div>

  <div class="canvas-wrap" id="userCanvasWrap" style="display:none;">
    <canvas id="cv3" width="660" height="370"></canvas>
  </div>
  <div class="eq-display" id="eq3"></div>

  <div class="slider-section" id="userSliders" style="display:none;">
    <div class="slider-row">
      <span class="slider-label">a</span>
      <input type="range" id="a3" min="-3" max="3" step="0.05" value="-0.3">
      <span class="slider-val" id="av3"></span>
      <span class="slider-desc">곡선 방향·폭</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">h</span>
      <input type="range" id="h3" min="-2" max="12" step="0.1" value="5">
      <span class="slider-val" id="hv3"></span>
      <span class="slider-desc">대칭축 위치</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">k</span>
      <input type="range" id="k3" min="-3" max="10" step="0.1" value="3">
      <span class="slider-val" id="kv3"></span>
      <span class="slider-desc">꼭짓점 높이</span>
    </div>
    <div class="range-divider">
      <div class="range-label">📏 좌표 범위 조정 (사진에 맞게 설정하세요)</div>
      <div class="slider-row">
        <span class="slider-label" style="width:50px;font-size:.74rem;">x 최대</span>
        <input type="range" id="xmax3" min="5" max="30" step="1" value="10">
        <span class="slider-val" id="xmaxv3"></span>
        <span class="slider-desc">x축 범위</span>
      </div>
      <div class="slider-row">
        <span class="slider-label" style="width:50px;font-size:.74rem;">y 최대</span>
        <input type="range" id="ymax3" min="3" max="20" step="1" value="7">
        <span class="slider-val" id="ymaxv3"></span>
        <span class="slider-desc">y축 범위</span>
      </div>
    </div>
  </div>

  <div class="info-cards" id="userInfoCards" style="display:none;">
    <div class="info-card"><div class="label">꼭짓점</div><div class="value" id="vtx3"></div></div>
    <div class="info-card"><div class="label">대칭축</div><div class="value" id="axis3"></div></div>
    <div class="info-card"><div class="label">최대/최솟값</div><div class="value" id="mm3"></div></div>
  </div>
  <div class="btn-row" id="userBtnRow" style="display:none;">
    <button class="btn btn-reset" onclick="resetSliders(3)">↺ 초기화</button>
    <button class="btn" style="background:#1e293b;color:#94a3b8;"
            onclick="document.getElementById('fileInput').click()">🔄 다른 사진 선택</button>
  </div>
</div>

<script>
// ── 다리 설정 ──────────────────────────────────────────────
const CFG = [
  // 선암사 무지개다리 (arch)
  { xMin:0, xMax:10, yMin:-1.2, yMax:6,
    initA:-0.35, initH:5, initK:3.8,
    isArch:true, color:'#ff6b6b' },
  // 대전 엑스포교 (arch)
  { xMin:0, xMax:10, yMin:-1.2, yMax:7,
    initA:-0.4,  initH:5, initK:4.5,
    isArch:true, color:'#f59e0b' },
  // 금문교 (cable)
  { xMin:0, xMax:10, yMin:-0.8, yMax:8,
    initA:0.1,   initH:5, initK:0.8,
    isArch:false, color:'#60a5fa' },
];

// ── 이미지 ─────────────────────────────────────────────────
const IMGS = [new Image(), new Image(), new Image()];
IMGS[0].src = 'data:image/jpeg;base64,__IMG1__';
IMGS[1].src = 'data:image/jpeg;base64,__IMG2__';
IMGS[2].src = 'data:image/jpeg;base64,__IMG3__';

let currentTab = 0;
let userImg = null;
let uXMax = 10, uYMax = 7;

// ── 탭 전환 ───────────────────────────────────────────────
function showTab(idx) {
  document.querySelectorAll('.tab-panel').forEach((p,i) =>
    p.classList.toggle('active', i===idx));
  document.querySelectorAll('.tab-btn').forEach((b,i) =>
    b.classList.toggle('active', i===idx));
  currentTab = idx;
  idx < 3 ? drawBridge(idx) : drawUser();
}

// ── 좌표 변환 ─────────────────────────────────────────────
function toPx(x, y, xMin, xMax, yMin, yMax, W, H) {
  return [(x-xMin)/(xMax-xMin)*W, H-(y-yMin)/(yMax-yMin)*H];
}

// ── 격자 그리기 ────────────────────────────────────────────
function drawGrid(ctx, W, H, xMin, xMax, yMin, yMax) {
  // 격자선
  ctx.lineWidth = 0.7;
  ctx.strokeStyle = 'rgba(100,150,255,0.22)';
  for (let x = Math.ceil(xMin); x <= Math.floor(xMax); x++) {
    const [px] = toPx(x,0,xMin,xMax,yMin,yMax,W,H);
    ctx.beginPath(); ctx.moveTo(px,0); ctx.lineTo(px,H); ctx.stroke();
  }
  for (let y = Math.ceil(yMin); y <= Math.floor(yMax); y++) {
    const [,py] = toPx(0,y,xMin,xMax,yMin,yMax,W,H);
    ctx.beginPath(); ctx.moveTo(0,py); ctx.lineTo(W,py); ctx.stroke();
  }
  // 축
  ctx.strokeStyle = 'rgba(160,210,255,0.65)';
  ctx.lineWidth = 1.5;
  if (yMin<=0 && yMax>=0) {
    const [,py0]=toPx(0,0,xMin,xMax,yMin,yMax,W,H);
    ctx.beginPath(); ctx.moveTo(0,py0); ctx.lineTo(W,py0); ctx.stroke();
  }
  if (xMin<=0 && xMax>=0) {
    const [px0]=toPx(0,0,xMin,xMax,yMin,yMax,W,H);
    ctx.beginPath(); ctx.moveTo(px0,0); ctx.lineTo(px0,H); ctx.stroke();
  }
  // 눈금 레이블
  ctx.fillStyle = 'rgba(180,210,255,0.75)';
  ctx.font = '10px Malgun Gothic,sans-serif';
  const [px0lab,py0lab] = toPx(0,0,xMin,xMax,yMin,yMax,W,H);
  const labelY = Math.min(Math.max(py0lab+14, 14), H-3);
  ctx.textAlign = 'center';
  for (let x=Math.ceil(xMin); x<=Math.floor(xMax); x++) {
    if (x===0) continue;
    const [px] = toPx(x,0,xMin,xMax,yMin,yMax,W,H);
    ctx.fillText(x, px, labelY);
  }
  ctx.textAlign = 'right';
  const labelX = Math.min(Math.max(px0lab-4, 16), W-4);
  for (let y=Math.ceil(yMin); y<=Math.floor(yMax); y++) {
    if (y===0) continue;
    const [,py] = toPx(0,y,xMin,xMax,yMin,yMax,W,H);
    ctx.fillText(y, labelX, py+4);
  }
  ctx.textAlign = 'right';
  ctx.fillText('O', Math.min(px0lab-3,W-4), Math.min(py0lab+13,H-3));
}

// ── 포물선 그리기 ──────────────────────────────────────────
function drawParabola(ctx, W, H, xMin, xMax, yMin, yMax, a, h, k, color, lw) {
  if (a===0) return;
  ctx.beginPath(); ctx.strokeStyle=color; ctx.lineWidth=lw;
  ctx.shadowColor=color; ctx.shadowBlur=10;
  let go=false;
  for (let px=-2; px<=W+2; px++) {
    const x = xMin+(px/W)*(xMax-xMin);
    const y = a*(x-h)*(x-h)+k;
    const [cx,cy] = toPx(x,y,xMin,xMax,yMin,yMax,W,H);
    if (cy>=-30 && cy<=H+30) {
      go ? ctx.lineTo(cx,cy) : (ctx.moveTo(cx,cy), go=true);
    } else { if(go){ctx.stroke();ctx.beginPath();go=false;} }
  }
  if(go) ctx.stroke();
  ctx.shadowBlur=0;
}

// ── 꼭짓점 점 ─────────────────────────────────────────────
function drawVtxDot(ctx, W, H, xMin, xMax, yMin, yMax, h, k, color) {
  const [cx,cy] = toPx(h,k,xMin,xMax,yMin,yMax,W,H);
  if (cx<-10||cx>W+10||cy<-10||cy>H+10) return;
  ctx.beginPath(); ctx.arc(cx,cy,7,0,2*Math.PI);
  ctx.fillStyle=color; ctx.fill();
  ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke();
  // 꼭짓점 좌표 레이블
  ctx.fillStyle='rgba(255,255,255,0.85)';
  ctx.font='bold 10px Malgun Gothic,sans-serif';
  ctx.textAlign='left';
  const lx = cx+10, ly = cy < 20 ? cy+16 : cy-10;
  ctx.fillText(`(${fmt(h)}, ${fmt(k)})`, Math.min(lx,W-70), ly);
}

// ── 대칭축 점선 ────────────────────────────────────────────
function drawSymAxis(ctx, W, H, xMin, xMax, yMin, yMax, h, color) {
  const [cx] = toPx(h,0,xMin,xMax,yMin,yMax,W,H);
  ctx.beginPath(); ctx.strokeStyle=color; ctx.lineWidth=1.2;
  ctx.setLineDash([5,4]);
  ctx.moveTo(cx,0); ctx.lineTo(cx,H); ctx.stroke();
  ctx.setLineDash([]);
}

// ── 숫자 포맷 ─────────────────────────────────────────────
function fmt(n){ return (+n.toFixed(2)).toString(); }

// ── 수식 업데이트 ─────────────────────────────────────────
function updateEq(idx, a, h, k) {
  const aStr = fmt(a);
  const hAbs = fmt(Math.abs(h));
  const hPart = h>0 ? `x − ${hAbs}` : h<0 ? `x + ${hAbs}` : 'x';
  const kPart = k>=0 ? `+ ${fmt(k)}` : `− ${fmt(-k)}`;
  let eq = `y = ${aStr}(${hPart})² ${kPart}`;
  if(h===0 && k===0) eq = `y = ${aStr}x²`;
  else if(h===0) eq = `y = ${aStr}x² ${kPart}`;
  else if(k===0) eq = `y = ${aStr}(${hPart})²`;
  document.getElementById(`eq${idx}`).textContent = eq;
}

// ── 정보 카드 업데이트 ────────────────────────────────────
function updateInfo(idx, a, h, k, isArch) {
  document.getElementById(`vtx${idx}`).textContent  = `(${fmt(h)}, ${fmt(k)})`;
  document.getElementById(`axis${idx}`).textContent = `x = ${fmt(h)}`;
  const label = (isArch !== undefined ? isArch : a<0) ? '최댓값' : '최솟값';
  document.getElementById(`mm${idx}`).textContent   = `${label}: ${fmt(k)}`;
}

// ── 다리 캔버스 그리기 ────────────────────────────────────
function drawBridge(idx) {
  const canvas = document.getElementById(`cv${idx}`);
  const ctx = canvas.getContext('2d');
  const W=canvas.width, H=canvas.height;
  const c = CFG[idx];
  const a = +document.getElementById(`a${idx}`).value;
  const h = +document.getElementById(`h${idx}`).value;
  const k = +document.getElementById(`k${idx}`).value;

  ctx.clearRect(0,0,W,H);

  // 이미지
  if (IMGS[idx].complete && IMGS[idx].naturalWidth>0) {
    ctx.drawImage(IMGS[idx],0,0,W,H);
  } else {
    ctx.fillStyle='#0a1428'; ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#334'; ctx.font='14px sans-serif'; ctx.textAlign='center';
    ctx.fillText('이미지 로딩 중…',W/2,H/2);
  }
  // 오버레이
  ctx.fillStyle='rgba(0,0,0,0.25)'; ctx.fillRect(0,0,W,H);

  drawGrid(ctx,W,H,c.xMin,c.xMax,c.yMin,c.yMax);
  drawSymAxis(ctx,W,H,c.xMin,c.xMax,c.yMin,c.yMax,h,c.color+'88');
  drawParabola(ctx,W,H,c.xMin,c.xMax,c.yMin,c.yMax,a,h,k,c.color,3.2);
  drawVtxDot(ctx,W,H,c.xMin,c.xMax,c.yMin,c.yMax,h,k,c.color);

  updateEq(idx,a,h,k);
  updateInfo(idx,a,h,k,c.isArch);
  document.getElementById(`av${idx}`).textContent = fmt(a);
  document.getElementById(`hv${idx}`).textContent = fmt(h);
  document.getElementById(`kv${idx}`).textContent = fmt(k);
}

// ── 사용자 캔버스 그리기 ──────────────────────────────────
function drawUser() {
  const canvas = document.getElementById('cv3');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W=canvas.width, H=canvas.height;
  const a = +document.getElementById('a3').value;
  const h = +document.getElementById('h3').value;
  const k = +document.getElementById('k3').value;
  const xMax = uXMax, yMax = uYMax;
  const xMin=0, yMin=-yMax*0.12;

  ctx.clearRect(0,0,W,H);
  if (userImg) {
    ctx.drawImage(userImg,0,0,W,H);
    ctx.fillStyle='rgba(0,0,0,0.25)'; ctx.fillRect(0,0,W,H);
  } else {
    ctx.fillStyle='#0a1428'; ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#335'; ctx.font='13px sans-serif'; ctx.textAlign='center';
    ctx.fillText('사진을 올리면 여기에 표시됩니다',W/2,H/2);
  }

  drawGrid(ctx,W,H,xMin,xMax,yMin,yMax);
  drawSymAxis(ctx,W,H,xMin,xMax,yMin,yMax,h,'#f59e0b88');
  drawParabola(ctx,W,H,xMin,xMax,yMin,yMax,a,h,k,'#f59e0b',3.2);
  drawVtxDot(ctx,W,H,xMin,xMax,yMin,yMax,h,k,'#f59e0b');

  updateEq(3,a,h,k);
  updateInfo(3,a,h,k,undefined);
  document.getElementById('av3').textContent = fmt(a);
  document.getElementById('hv3').textContent = fmt(h);
  document.getElementById('kv3').textContent = fmt(k);
  document.getElementById('xmaxv3').textContent = fmt(xMax);
  document.getElementById('ymaxv3').textContent = fmt(yMax);
}

// ── 슬라이더 이벤트 연결 ──────────────────────────────────
[0,1,2].forEach(i => {
  ['a','h','k'].forEach(s => {
    document.getElementById(`${s}${i}`).addEventListener('input',()=>drawBridge(i));
  });
});
['a','h','k'].forEach(s =>
  document.getElementById(`${s}3`).addEventListener('input',drawUser));
document.getElementById('xmax3').addEventListener('input',function(){
  uXMax=+this.value; drawUser();
});
document.getElementById('ymax3').addEventListener('input',function(){
  uYMax=+this.value; drawUser();
});

// ── 힌트 토글 ─────────────────────────────────────────────
function toggleHint(idx) {
  document.getElementById(`hint${idx}`).classList.toggle('show');
}

// ── 초기화 ────────────────────────────────────────────────
function resetSliders(idx) {
  if (idx < 3) {
    const c = CFG[idx];
    document.getElementById(`a${idx}`).value = c.initA;
    document.getElementById(`h${idx}`).value = c.initH;
    document.getElementById(`k${idx}`).value = c.initK;
    document.getElementById(`hint${idx}`).classList.remove('show');
    drawBridge(idx);
  } else {
    document.getElementById('a3').value = -0.3;
    document.getElementById('h3').value = 5;
    document.getElementById('k3').value = 3;
    document.getElementById('xmax3').value = 10; uXMax=10;
    document.getElementById('ymax3').value = 7;  uYMax=7;
    drawUser();
  }
}

// ── 파일 업로드 ───────────────────────────────────────────
function loadFile(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    const img = new Image();
    img.onload = () => {
      userImg = img;
      document.getElementById('uploadZone').style.display = 'none';
      document.getElementById('userCanvasWrap').style.display = 'block';
      document.getElementById('userSliders').style.display = 'block';
      document.getElementById('userInfoCards').style.display = 'flex';
      document.getElementById('userBtnRow').style.display = 'flex';
      drawUser();
    };
    img.src = e.target.result;
  };
  reader.readAsDataURL(file);
}

document.getElementById('fileInput').addEventListener('change', e => {
  if (e.target.files[0]) loadFile(e.target.files[0]);
});
const zone = document.getElementById('uploadZone');
zone.addEventListener('dragover', e => { e.preventDefault(); zone.style.borderColor='#3b82f6'; });
zone.addEventListener('dragleave', () => { zone.style.borderColor=''; });
zone.addEventListener('drop', e => {
  e.preventDefault(); zone.style.borderColor='';
  if (e.dataTransfer.files[0]) loadFile(e.dataTransfer.files[0]);
});

// ── 이미지 로딩 후 재그리기 ──────────────────────────────
IMGS.forEach((img,i) => { img.onload = () => { if(currentTab===i) drawBridge(i); }; });

// ── 초기 렌더 ─────────────────────────────────────────────
window.addEventListener('load', () => {
  drawBridge(0);
  drawUser();
});
setTimeout(() => drawBridge(currentTab), 400);
setTimeout(() => drawBridge(currentTab), 1200);
</script>
</body>
</html>"""


def render():
    st.markdown("### 🌉 다리에서 이차함수 찾기")
    st.markdown(
        "실제 다리 사진에 이차함수 **y = a(x−h)² + k** 그래프를 겹쳐 곡선을 맞춰 보세요. "
        "꼭짓점이 아치의 **최댓값**, 케이블의 **최솟값**과 어떻게 연결되는지 탐구합니다."
    )

    b1 = _b64("arch bridge1.jpg")
    b2 = _b64("arch bridge2.jpg")
    b3 = _b64("arch bridge3.jpg")

    html = (_HTML_TMPL
            .replace("__IMG1__", b1)
            .replace("__IMG2__", b2)
            .replace("__IMG3__", b3))

    components.html(html, height=840, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
