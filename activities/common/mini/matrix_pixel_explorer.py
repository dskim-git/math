# activities/common/mini/matrix_pixel_explorer.py
"""
사진 속 행렬 탐험
컴퓨터가 사진(그림 파일)을 행렬로 저장하는 원리를 픽셀 시각화와 인터랙션으로 직접 체험하는 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

# ── Google Sheets 연동 ───────────────────────────────────────────────────────
_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "행렬픽셀탐험"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 통해 알게 된 내용을 정리해 보세요**"},
    {"key": "저장원리",
     "label": "1️⃣ 컴퓨터가 사진(그림 파일)을 저장할 때 행렬을 어떻게 활용하는지 자신의 말로 설명해보세요.",
     "type": "text_area", "height": 100},
    {"key": "흑백컬러비교",
     "label": "2️⃣ 흑백 사진과 컬러 사진을 행렬로 저장할 때 어떤 차이점이 있는지 비교해보세요.",
     "type": "text_area", "height": 90},
    {"key": "사진보정수학",
     "label": "3️⃣ '사진 보정 실험실'에서 체험한 변환(반전·대칭·밝기·이진화) 중 하나를 골라, 행렬 성분이 어떻게 바뀌는지 수식을 포함해 설명해보세요.",
     "type": "text_area", "height": 100},
    {"key": "새롭게알게된점",
     "label": "💡 이 활동을 통해 새롭게 알게 된 점",
     "type": "text_area", "height": 90},
    {"key": "느낀점",
     "label": "💬 이 활동을 하면서 느낀 점",
     "type": "text_area", "height": 90},
]

META = {
    "title":       "📷 사진 속 행렬 탐험",
    "description": "컴퓨터가 사진을 행렬로 저장·보정하는 원리를 픽셀 시각화와 인터랙션으로 직접 체험하는 활동",
    "order":       0,
}

# ─────────────────────────────────────────────────────────────────────────────
_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>사진 속 행렬 탐험</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1a1a2e 100%);
  color:#e2e8f0;padding:7px 7px 2px;
  overflow:hidden;
}
/* Tabs */
.tabs{display:flex;gap:4px;margin-bottom:8px}
.tb{
  flex:1;padding:7px 3px;border-radius:8px;
  border:2px solid #1e293b;background:#1e293b;
  color:#64748b;font-weight:700;cursor:pointer;
  font-size:.73rem;text-align:center;transition:all .2s;
}
.tb.on{background:linear-gradient(135deg,#0ea5e9,#6366f1);color:#fff;border-color:transparent}
.tb:hover:not(.on){background:#273549;color:#e2e8f0}
.panel{display:none}.panel.on{display:block}
/* Card */
.card{
  background:#161e2e;border:1px solid #1e293b;
  border-radius:11px;padding:9px 11px;margin-bottom:7px;
}
.ct{font-size:.82rem;font-weight:800;color:#7dd3fc;margin-bottom:5px;display:flex;align-items:center;gap:5px}
.desc{font-size:.75rem;color:#94a3b8;line-height:1.58}
.ib{
  background:#0f172a;border:1px solid #334155;
  border-radius:7px;padding:6px 9px;
  font-size:.72rem;color:#94a3b8;line-height:1.55;margin-top:6px;
}
.hl{color:#f59e0b;font-weight:700}
.badge{
  display:inline-block;padding:1px 6px;border-radius:13px;
  font-size:.64rem;font-weight:700;
  background:#0ea5e920;color:#38bdf8;border:1px solid #0ea5e940;
}
/* Layout */
.row{display:flex;gap:10px;align-items:flex-start}
/* Pixel cells */
.pc{
  border-radius:2px;transition:transform .13s,box-shadow .13s;
  border:2px solid transparent;cursor:crosshair;
}
.pc:hover{transform:scale(1.14);box-shadow:0 0 6px #0ea5e9aa;border-color:#0ea5e9;position:relative;z-index:5}
.pc.sel{border-color:#f59e0b!important;box-shadow:0 0 8px #f59e0baa!important}
/* Matrix */
.mw{display:flex;align-items:center;gap:2px}
.mb{font-size:1.7rem;color:#7dd3fc;font-weight:100;line-height:1;user-select:none}
.mg{display:grid;gap:2px}
.mc{
  display:flex;align-items:center;justify-content:center;
  font-size:.6rem;font-weight:700;border-radius:3px;
  background:#1e293b;color:#94a3b8;
  transition:all .22s;border:1px solid #2d3748;height:21px;
}
.mc.sel{background:#f59e0b;color:#0f172a;transform:scale(1.08);box-shadow:0 0 5px #f59e0baa}
.mc.scanned{background:#0a2010;color:#4ade80;border-color:#166534}
.mc.proc{background:#312e81;color:#c7d2fe;border-color:#4f46e5}
/* Scan bar */
.sbw{background:#1e293b;border-radius:20px;height:5px;margin-top:6px;overflow:hidden}
.sb{height:5px;border-radius:20px;background:linear-gradient(90deg,#22c55e,#0ea5e9);width:0%;transition:width .09s}
/* Buttons */
.btn{
  padding:5px 9px;border-radius:7px;border:none;cursor:pointer;
  font-size:.71rem;font-weight:700;transition:all .14s;
}
.btn-p{background:linear-gradient(135deg,#0ea5e9,#6366f1);color:#fff}
.btn-s{background:#1e293b;color:#94a3b8;border:1px solid #334155}
.btn:hover{opacity:.83;transform:translateY(-1px)}
.btn:active{transform:translateY(0)}
.brow{display:flex;gap:5px;flex-wrap:wrap;margin-top:6px}
/* Channel btn */
.chb{
  padding:5px 9px;border-radius:7px;border:2px solid;
  cursor:pointer;font-size:.71rem;font-weight:700;transition:all .18s;
}
.chb.on{opacity:1}.chb:not(.on){opacity:.38}
.chb:hover{opacity:.88}
/* Art cell */
.ac{border-radius:2px;border:1px solid rgba(255,255,255,.07);cursor:pointer;transition:transform .09s}
.ac:hover{transform:scale(1.1)}
/* RGB mini */
.rgb-row{display:flex;gap:7px;align-items:flex-start;flex-wrap:wrap;margin-top:5px}
.rgb-blk{text-align:center}
.rgb-lbl{font-size:.68rem;font-weight:700;margin-bottom:3px}
.rgb-mat{font-size:.56rem;font-family:monospace;line-height:1.58;border-radius:6px;padding:4px 6px;border:1px solid}
.rgb-mat.r{background:rgba(239,68,68,.12);color:#fca5a5;border-color:#ef444450}
.rgb-mat.g{background:rgba(34,197,94,.12);color:#86efac;border-color:#22c55e50}
.rgb-mat.b{background:rgba(59,130,246,.12);color:#93c5fd;border-color:#3b82f650}
/* Processing */
.pbrow{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:7px}
.pb{
  padding:4px 8px;border-radius:7px;border:2px solid #334155;
  background:#1e293b;color:#94a3b8;cursor:pointer;
  font-size:.7rem;font-weight:700;transition:all .18s;
}
.pb.on{border-color:#a78bfa;color:#c4b5fd;background:#1e1b4b}
.pb:hover:not(.on){background:#273549;color:#e2e8f0}
.eqbox{
  font-size:.79rem;font-weight:700;
  background:#1e1b4b;border:1px solid #4338ca50;
  border-radius:8px;padding:5px 11px;
  color:#c7d2fe;margin-top:6px;
  font-family:'Courier New',monospace;
}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.3)}}
.pulse{animation:pulse .24s ease}
</style>
</head>
<body>

<div class="tabs">
  <button class="tb on" onclick="sw(0)">📷 픽셀&amp;행렬</button>
  <button class="tb" onclick="sw(1)">🎨 흑백 그리기</button>
  <button class="tb" onclick="sw(2)">🌈 컬러의 비밀</button>
  <button class="tb" onclick="sw(3)">🔧 사진 보정 실험실</button>
</div>

<!-- ═══ TAB 0: 픽셀 탐험기 ═══ -->
<div class="panel on" id="p0">
  <div class="card">
    <div class="ct">💡 컴퓨터는 사진을 어떻게 저장할까?</div>
    <p class="desc">흑백 사진의 각 픽셀은 <b>0(검정)~255(흰색)</b> 밝기값 하나로 저장돼요. 이 수들을 직사각형으로 배열하면 바로 <b>행렬</b>! 픽셀을 클릭하거나 스캔 애니메이션을 눌러보세요.</p>
  </div>
  <div class="card">
    <div class="row">
      <div>
        <div class="ct" style="font-size:.75rem">🖼️ 픽셀 이미지 <span class="badge">8×8</span></div>
        <div id="pg0" style="display:grid;grid-template-columns:repeat(8,32px);gap:2px"></div>
      </div>
      <div>
        <div class="ct" style="font-size:.75rem">📊 행렬 <span class="badge">8행 8열</span></div>
        <div class="mw">
          <div class="mb">[</div>
          <div id="mg0" class="mg" style="grid-template-columns:repeat(8,32px)"></div>
          <div class="mb">]</div>
        </div>
      </div>
    </div>
    <div id="ib0" class="ib">← 픽셀을 클릭하면 위치와 밝기값을 확인할 수 있어요!</div>
    <div class="sbw"><div id="sbar" class="sb"></div></div>
    <div class="brow">
      <button class="btn btn-p" id="scan-btn" onclick="scanAnim()">▶ 픽셀 스캔 애니메이션</button>
      <button class="btn btn-s" onclick="resetSel()">↺ 초기화</button>
    </div>
    <div class="ib" style="margin-top:5px">
      💡 이미지가 <span class="hl">8행×8열</span>이면 행렬도 <span class="hl">8행 8열</span> &nbsp;|&nbsp; 행렬의 <span class="hl">(i,j) 성분</span> = i행 j열 픽셀의 밝기값
    </div>
  </div>
</div>

<!-- ═══ TAB 1: 흑백 그리기 ═══ -->
<div class="panel" id="p1">
  <div class="card">
    <div class="ct">🎨 나만의 흑백 픽셀 아트</div>
    <p class="desc">격자를 클릭해서 밝기를 바꿔보세요! 오른쪽 <b>행렬이 실시간으로 바뀌는 것</b>을 확인하세요.</p>
  </div>
  <div class="card">
    <div class="row">
      <div>
        <div class="ct" style="font-size:.75rem">🖌️ 그리기 <span class="badge">8×8</span></div>
        <div id="pg1" style="display:grid;grid-template-columns:repeat(8,37px);gap:2px"></div>
        <div class="brow">
          <button class="btn btn-p" onclick="fillHeart()">❤️ 하트</button>
          <button class="btn btn-p" onclick="fillSmiley()">😊 스마일</button>
          <button class="btn btn-s" onclick="clearArt()">🗑️ 지우기</button>
        </div>
      </div>
      <div>
        <div class="ct" style="font-size:.75rem">📊 실시간 행렬 <span class="badge">8행 8열</span></div>
        <div class="mw">
          <div class="mb">[</div>
          <div id="mg1" class="mg" style="grid-template-columns:repeat(8,32px)"></div>
          <div class="mb">]</div>
        </div>
      </div>
    </div>
    <div class="ib" style="margin-top:6px">
      🎯 <span class="hl">0</span>=검정 &nbsp;|&nbsp; <span class="hl">255</span>=흰색 &nbsp;|&nbsp; 중간값=회색 &nbsp;|&nbsp; 클릭할 때마다 밝기 단계 변경
    </div>
  </div>
</div>

<!-- ═══ TAB 2: 컬러의 비밀 ═══ -->
<div class="panel" id="p2">
  <div class="card">
    <div class="ct">🌈 컬러 사진 = 행렬 3개!</div>
    <p class="desc">컬러 사진의 각 픽셀은 R·G·B 세 채널로 구성돼요. 각 채널은 하나의 행렬로 저장됩니다!</p>
  </div>
  <div class="card">
    <div style="display:flex;gap:4px;margin-bottom:8px;flex-wrap:wrap">
      <button class="chb on" data-c="o" onclick="setCh('o')" style="border-color:#475569;color:#e2e8f0">🌈 원본</button>
      <button class="chb" data-c="r" onclick="setCh('r')" style="border-color:#ef4444;color:#fca5a5;background:rgba(239,68,68,.15)">🔴 R채널</button>
      <button class="chb" data-c="g" onclick="setCh('g')" style="border-color:#22c55e;color:#86efac;background:rgba(34,197,94,.15)">🟢 G채널</button>
      <button class="chb" data-c="b" onclick="setCh('b')" style="border-color:#3b82f6;color:#93c5fd;background:rgba(59,130,246,.15)">🔵 B채널</button>
    </div>
    <div class="row">
      <div>
        <div class="ct" style="font-size:.75rem" id="ch-title">🌈 원본 <span class="badge">6×6</span></div>
        <div id="cg" style="display:grid;grid-template-columns:repeat(6,38px);gap:2px"></div>
      </div>
      <div>
        <div class="ct" style="font-size:.75rem">📊 행렬</div>
        <div id="ch-ph" style="font-size:.73rem;color:#475569;padding:6px 0;max-width:190px">← 채널 버튼을 누르면 행렬이 나타납니다!</div>
        <div id="ch-mw" class="mw" style="display:none">
          <div class="mb">[</div>
          <div id="cm" class="mg" style="grid-template-columns:repeat(6,38px)"></div>
          <div class="mb">]</div>
        </div>
      </div>
    </div>
    <div id="ch-info" class="ib" style="margin-top:6px">채널을 선택하면 해당 색상 성분의 행렬을 볼 수 있어요!</div>
  </div>
  <div class="card">
    <div class="ct">🔢 컬러 사진 = R행렬 + G행렬 + B행렬</div>
    <div class="rgb-row">
      <div class="rgb-blk"><div class="rgb-lbl" style="color:#fca5a5">🔴 R</div><div class="rgb-mat r" id="rm"></div></div>
      <div style="font-size:1.1rem;color:#7dd3fc;padding-top:18px">+</div>
      <div class="rgb-blk"><div class="rgb-lbl" style="color:#86efac">🟢 G</div><div class="rgb-mat g" id="gm"></div></div>
      <div style="font-size:1.1rem;color:#7dd3fc;padding-top:18px">+</div>
      <div class="rgb-blk"><div class="rgb-lbl" style="color:#93c5fd">🔵 B</div><div class="rgb-mat b" id="bm"></div></div>
      <div style="font-size:1.1rem;color:#7dd3fc;padding-top:18px">=</div>
      <div class="rgb-blk">
        <div class="rgb-lbl">🌈 컬러</div>
        <div id="preview" style="display:grid;grid-template-columns:repeat(6,19px);gap:1px"></div>
      </div>
    </div>
    <div class="ib" style="margin-top:5px">
      📱 <span class="hl">1920×1080</span> 컬러 사진 → <span class="hl">1080행 1920열</span> 행렬 3개 → 수 <span class="hl">6,220,800개</span>로 저장!
    </div>
  </div>
</div>

<!-- ═══ TAB 3: 사진 보정 실험실 ═══ -->
<div class="panel" id="p3">
  <div class="card">
    <div class="ct">🔧 행렬로 하는 사진 보정!</div>
    <p class="desc">사진 보정도 사실은 <b>행렬의 각 성분값을 수학적으로 바꾸는 것</b>이에요. 버튼을 눌러 이미지와 행렬이 어떻게 변하는지 확인해보세요!</p>
  </div>
  <div class="card">
    <div class="pbrow" id="pbrow">
      <button class="pb on" onclick="applyProc('orig')">🖼️ 원본</button>
      <button class="pb" onclick="applyProc('invert')">🔄 색상 반전</button>
      <button class="pb" onclick="applyProc('flipH')">↔️ 좌우 대칭</button>
      <button class="pb" onclick="applyProc('flipV')">↕️ 상하 대칭</button>
      <button class="pb" onclick="applyProc('bright+')">☀️ 밝기 높이기</button>
      <button class="pb" onclick="applyProc('bright-')">🌙 밝기 낮추기</button>
      <button class="pb" onclick="applyProc('thresh')">🎯 이진화</button>
    </div>
    <div class="row" style="align-items:flex-start">
      <div>
        <div class="ct" style="font-size:.75rem">🖼️ 원본 이미지</div>
        <div id="og" style="display:grid;grid-template-columns:repeat(6,35px);gap:2px"></div>
      </div>
      <div style="font-size:1.3rem;color:#7dd3fc;padding-top:24px">→</div>
      <div>
        <div class="ct" style="font-size:.75rem" id="proc-title">🖼️ 보정 이미지</div>
        <div id="pimg" style="display:grid;grid-template-columns:repeat(6,35px);gap:2px"></div>
      </div>
      <div>
        <div class="ct" style="font-size:.75rem">📊 보정 후 행렬 <span class="badge" id="diff-badge">변화 없음</span></div>
        <div class="mw">
          <div class="mb">[</div>
          <div id="pmg" class="mg" style="grid-template-columns:repeat(6,35px)"></div>
          <div class="mb">]</div>
        </div>
      </div>
    </div>
    <div class="eqbox" id="eqbox">← 보정 버튼을 누르면 수학 공식이 나타납니다</div>
    <div id="proc-ib" class="ib" style="margin-top:6px">위 버튼을 눌러 원본 사진을 변환해 보세요.</div>
  </div>
</div>

<script>
// ── 데이터 ───────────────────────────────────────────────────────────────────

// 8×8 하트 이미지 (흑백)
const IMG8=[
  [235,235,235,235,235,235,235,235],
  [235, 30, 30,235, 30, 30,235,235],
  [ 30, 30, 30, 30, 30, 30, 30,235],
  [ 30, 30, 30, 30, 30, 30, 30, 30],
  [235, 30, 30, 30, 30, 30, 30,235],
  [235,235, 30, 30, 30, 30,235,235],
  [235,235,235, 30, 30,235,235,235],
  [235,235,235,235,235,235,235,235],
];

// 8×8 art 그리드
const art8=Array.from({length:8},()=>Array(8).fill(255));
const LEVELS=[255,200,150,100,50,0];

// 6×6 컬러 이미지 (노을 그라디언트)
const CIMG=[
  [[230,90,50],[210,100,60],[180,120,80],[150,140,120],[100,130,180],[70,100,220]],
  [[220,100,55],[200,110,65],[170,130,85],[140,150,125],[90,140,185],[65,110,225]],
  [[205,115,65],[185,125,75],[160,140,95],[130,160,135],[85,150,195],[60,120,230]],
  [[185,128,75],[165,138,85],[145,152,108],[120,165,145],[80,160,200],[55,132,235]],
  [[165,138,88],[148,148,98],[130,162,118],[110,172,158],[75,168,208],[50,142,240]],
  [[145,148,98],[130,158,108],[115,168,128],[95,178,168],[70,172,215],[45,152,245]],
];

// 6×6 보정 실험용 이미지 (알파벳 F 모양 – 좌우 비대칭)
const PROC6=[
  [220,220,220,220,220, 20],
  [220, 20, 20, 20, 20, 20],
  [220,220,220,220, 20, 20],
  [220, 20, 20, 20, 20, 20],
  [220, 20, 20, 20, 20, 20],
  [220, 20, 20, 20, 20, 20],
];

// ── 탭 전환 ─────────────────────────────────────────────────────────────────
function sw(i){
  document.querySelectorAll('.tb').forEach((b,j)=>b.classList.toggle('on',i===j));
  document.querySelectorAll('.panel').forEach((p,j)=>p.classList.toggle('on',i===j));
}

// ═══════════════════ TAB 0 ═══════════════════
const pg0=document.getElementById('pg0');
const mg0=document.getElementById('mg0');
const ib0=document.getElementById('ib0');
const sbar=document.getElementById('sbar');

function buildTab0(){
  pg0.innerHTML=''; mg0.innerHTML='';
  for(let r=0;r<8;r++) for(let c=0;c<8;c++){
    const v=IMG8[r][c];
    const pc=document.createElement('div');
    pc.className='pc';
    pc.style.cssText=`width:32px;height:32px;background:rgb(${v},${v},${v})`;
    pc.addEventListener('click',()=>selPx(r,c));
    pg0.appendChild(pc);
    const mc=document.createElement('div');
    mc.className='mc'; mc.id=`m0-${r}-${c}`; mc.style.width='32px';
    mc.textContent=v; mg0.appendChild(mc);
  }
}

function selPx(r,c){
  if(scanning) return;
  pg0.querySelectorAll('.pc').forEach(e=>e.classList.remove('sel'));
  mg0.querySelectorAll('.mc').forEach(e=>e.classList.remove('sel'));
  pg0.children[r*8+c].classList.add('sel');
  const mc=document.getElementById(`m0-${r}-${c}`);
  mc.classList.add('sel','pulse');
  setTimeout(()=>mc.classList.remove('pulse'),350);
  const v=IMG8[r][c];
  const lbl=v<50?'검정':v<100?'매우 어두운 회색':v<180?'회색':v<240?'밝은 회색':'흰색';
  ib0.innerHTML=`📍 위치: <span class="hl">${r+1}행 ${c+1}열</span> &nbsp;|&nbsp; 밝기값: <span class="hl">${v}</span> &nbsp;|&nbsp; `+
    `<span style="display:inline-block;width:11px;height:11px;background:rgb(${v},${v},${v});border-radius:2px;vertical-align:middle;border:1px solid #475569"></span> `+
    `<span class="hl">${lbl}</span>`;
}

function resetSel(){
  if(scanning){clearTimeout(scanTimer);scanning=false;document.getElementById('scan-btn').textContent='▶ 픽셀 스캔 애니메이션';}
  pg0.querySelectorAll('.pc').forEach(e=>e.classList.remove('sel'));
  mg0.querySelectorAll('.mc').forEach(e=>{e.classList.remove('sel','scanned','pulse');e.style.color='';e.style.background='';});
  ib0.innerHTML='← 픽셀을 클릭하면 위치와 밝기값을 확인할 수 있어요!';
  sbar.style.width='0%';
}

let scanning=false,scanTimer=null,scanIdx=0;
function scanAnim(){
  if(scanning) return;
  scanning=true; scanIdx=0;
  pg0.querySelectorAll('.pc').forEach(e=>e.classList.remove('sel'));
  mg0.querySelectorAll('.mc').forEach(e=>{e.classList.remove('sel','scanned');e.style.color='';e.style.background='';});
  sbar.style.width='0%';
  document.getElementById('scan-btn').textContent='⏳ 스캔 중...';
  function step(){
    if(scanIdx>0) pg0.children[scanIdx-1].classList.remove('sel');
    if(scanIdx>=64){
      scanning=false;
      document.getElementById('scan-btn').textContent='▶ 다시 스캔';
      ib0.innerHTML='✅ 스캔 완료! <span class="hl">64개</span>의 픽셀 밝기값이 모두 행렬에 저장되었어요.';
      sbar.style.width='100%'; return;
    }
    const r=Math.floor(scanIdx/8),c=scanIdx%8,v=IMG8[r][c];
    pg0.children[scanIdx].classList.add('sel');
    const mc=document.getElementById(`m0-${r}-${c}`);
    mc.classList.add('scanned','pulse');
    setTimeout(()=>mc.classList.remove('pulse'),280);
    ib0.innerHTML=`🔍 스캔 중... <span class="hl">(${r+1}행, ${c+1}열)</span> → 밝기: <span class="hl">${v}</span>`;
    sbar.style.width=`${((scanIdx+1)/64*100).toFixed(0)}%`;
    scanIdx++;
    scanTimer=setTimeout(step,80);
  }
  step();
}
buildTab0();

// ═══════════════════ TAB 1 ═══════════════════
const pg1=document.getElementById('pg1');
const mg1=document.getElementById('mg1');

function buildTab1(){
  pg1.innerHTML=''; mg1.innerHTML='';
  for(let r=0;r<8;r++) for(let c=0;c<8;c++){
    const v=art8[r][c];
    const ac=document.createElement('div');
    ac.className='ac';
    ac.style.cssText=`width:37px;height:37px;background:rgb(${v},${v},${v})`;
    ac.addEventListener('click',()=>toggleArt(r,c));
    pg1.appendChild(ac);
    const mc=document.createElement('div');
    mc.className='mc'; mc.id=`m1-${r}-${c}`; mc.style.width='32px';
    mc.textContent=v; styleMC1(mc,v); mg1.appendChild(mc);
  }
}

function styleMC1(mc,v){
  mc.style.background=v<80?'#0a0f1e':'#1e293b';
  mc.style.color=v<80?'#64748b':v<180?'#94a3b8':'#e2e8f0';
}

function toggleArt(r,c){
  const nxt=LEVELS[(LEVELS.indexOf(art8[r][c])+1)%LEVELS.length];
  art8[r][c]=nxt;
  pg1.children[r*8+c].style.background=`rgb(${nxt},${nxt},${nxt})`;
  const mc=document.getElementById(`m1-${r}-${c}`);
  mc.textContent=nxt; mc.classList.add('pulse');
  setTimeout(()=>mc.classList.remove('pulse'),280);
  styleMC1(mc,nxt);
}

function setArtData(d){for(let r=0;r<8;r++) for(let c=0;c<8;c++) art8[r][c]=d[r][c]; buildTab1();}
function clearArt(){setArtData(Array.from({length:8},()=>Array(8).fill(255)));}
function fillHeart(){setArtData([
  [255,255,255,255,255,255,255,255],
  [255,  0,  0,255,  0,  0,255,255],
  [  0,  0,  0,  0,  0,  0,  0,255],
  [  0,  0,  0,  0,  0,  0,  0,  0],
  [255,  0,  0,  0,  0,  0,  0,255],
  [255,255,  0,  0,  0,  0,255,255],
  [255,255,255,  0,  0,255,255,255],
  [255,255,255,255,255,255,255,255],
]);}
function fillSmiley(){setArtData([
  [255,255,  0,  0,  0,  0,255,255],
  [255,  0,200,200,200,200,  0,255],
  [  0,200,  0,200,200,  0,200,  0],
  [  0,200,200,200,200,200,200,  0],
  [  0,200,  0,200,200,  0,200,  0],
  [  0,200,200,  0,  0,200,200,  0],
  [255,  0,200,200,200,200,  0,255],
  [255,255,  0,  0,  0,  0,255,255],
]);}
buildTab1();

// ═══════════════════ TAB 2 ═══════════════════
let curCh='o';
const CH_LBL={o:'🌈 원본',r:'🔴 R채널 (빨강)',g:'🟢 G채널 (초록)',b:'🔵 B채널 (파랑)'};
const CH_INFO={
  o:'원본의 각 픽셀은 R·G·B 세 값을 가져요. 채널 버튼을 눌러 각 성분을 확인하세요!',
  r:'<span class="hl">R 채널 행렬</span>: 빨간색 성분의 세기. 값이 클수록 붉은 빛이 강해요.',
  g:'<span class="hl">G 채널 행렬</span>: 초록색 성분의 세기. 값이 클수록 녹색 빛이 강해요.',
  b:'<span class="hl">B 채널 행렬</span>: 파란색 성분의 세기. 값이 클수록 파란 빛이 강해요.',
};
const CH_COL={r:'#fca5a5',g:'#86efac',b:'#93c5fd'};

function buildColorGrid(){
  document.getElementById('cg').innerHTML='';
  document.getElementById('cm').innerHTML='';
  document.getElementById('ch-title').innerHTML=CH_LBL[curCh]+' <span class="badge">6×6</span>';
  document.getElementById('ch-info').innerHTML=CH_INFO[curCh];
  const showMat=curCh!=='o';
  document.getElementById('ch-ph').style.display=showMat?'none':'block';
  document.getElementById('ch-mw').style.display=showMat?'flex':'none';
  for(let r=0;r<6;r++) for(let c=0;c<6;c++){
    const [rv,gv,bv]=CIMG[r][c];
    const pc=document.createElement('div');
    pc.style.cssText='width:38px;height:38px;border-radius:3px;transition:background .38s';
    pc.style.background=curCh==='o'?`rgb(${rv},${gv},${bv})`:
      curCh==='r'?`rgb(${rv},0,0)`:curCh==='g'?`rgb(0,${gv},0)`:`rgb(0,0,${bv})`;
    document.getElementById('cg').appendChild(pc);
    if(showMat){
      const val=curCh==='r'?rv:curCh==='g'?gv:bv;
      const mc=document.createElement('div');
      mc.className='mc'; mc.style.cssText=`width:38px;color:${CH_COL[curCh]}`;
      mc.textContent=val; document.getElementById('cm').appendChild(mc);
    }
  }
}

function setCh(ch){
  curCh=ch;
  document.querySelectorAll('.chb').forEach(b=>b.classList.toggle('on',b.dataset.c===ch));
  buildColorGrid();
}

function buildRGBMini(){
  ['r','g','b'].forEach((ch,ci)=>{
    document.getElementById(ch+'m').textContent=
      CIMG.map(row=>row.map(px=>String(px[ci]).padStart(3)).join(' ')).join('\n');
  });
  const prev=document.getElementById('preview');
  prev.innerHTML='';
  for(let r=0;r<6;r++) for(let c=0;c<6;c++){
    const [rv,gv,bv]=CIMG[r][c];
    const d=document.createElement('div');
    d.style.cssText=`width:19px;height:19px;background:rgb(${rv},${gv},${bv});border-radius:2px`;
    prev.appendChild(d);
  }
}
buildColorGrid(); buildRGBMini();

// ═══════════════════ TAB 3: 사진 보정 ═══════════════════
const PROC_DATA={
  orig:    {title:'🖼️ 보정 이미지 (원본)',    eq:'변환 없음  –  a(i,j) = 원본값',                                  info:'원본 이미지입니다. 변환 버튼을 눌러보세요!', changed:false},
  invert:  {title:'🔄 색상 반전',              eq:'반전  :  a(i,j)  →  255 − a(i,j)',                              info:'<b>색상 반전(Negative)</b>: 각 성분값을 255에서 빼요. 밝은 부분↔어두운 부분이 뒤바뀝니다!<br>사진 필름을 인화할 때 쓰이는 원리예요.', changed:true},
  flipH:   {title:'↔️ 좌우 대칭',              eq:'좌우 대칭  :  a(i,j)  →  a(i, n+1−j)',                         info:'<b>좌우 대칭(Horizontal Flip)</b>: 각 행 안에서 j열 성분을 (n+1−j)열 성분과 바꿔요.<br>셀카 사진 미러 효과가 이 원리입니다!', changed:true},
  flipV:   {title:'↕️ 상하 대칭',              eq:'상하 대칭  :  a(i,j)  →  a(m+1−i, j)',                         info:'<b>상하 대칭(Vertical Flip)</b>: i행 성분을 (m+1−i)행 성분과 바꿔요.<br>행 전체를 위아래로 뒤집는 것입니다!', changed:true},
  'bright+':{title:'☀️ 밝기 높이기',           eq:'밝기 +  :  a(i,j)  →  min( a(i,j) + 80, 255 )',               info:'<b>밝기 높이기</b>: 모든 성분에 상수 80을 더해요(최대 255). 이것이 바로 <b>행렬의 스칼라 덧셈</b>입니다!', changed:true},
  'bright-':{title:'🌙 밝기 낮추기',           eq:'밝기 −  :  a(i,j)  →  max( a(i,j) − 80, 0 )',                info:'<b>밝기 낮추기</b>: 모든 성분에서 상수 80을 빼요(최소 0). 행렬에서 상수를 빼는 것입니다!', changed:true},
  thresh:  {title:'🎯 이진화(Threshold)',       eq:'이진화  :  a(i,j) ≥ 128  →  255,  그 외  →  0',              info:'<b>이진화</b>: 128 이상이면 255(흰색), 미만이면 0(검정)으로 바꿔요.<br>QR코드·바코드가 이 방식으로 만들어집니다!', changed:true},
};

function applyProc(type){
  document.querySelectorAll('.pb').forEach(b=>{
    const fn=b.getAttribute('onclick');
    b.classList.toggle('on', fn===`applyProc('${type}')`);
  });
  const d=PROC_DATA[type];
  document.getElementById('proc-title').textContent=d.title;
  document.getElementById('eqbox').textContent=d.eq;
  document.getElementById('proc-ib').innerHTML=d.info;

  const processed=PROC6.map((row,r)=>row.map((v,c)=>{
    if(type==='orig')     return v;
    if(type==='invert')   return 255-v;
    if(type==='flipH')    return PROC6[r][5-c];
    if(type==='flipV')    return PROC6[5-r][c];
    if(type==='bright+')  return Math.min(v+80,255);
    if(type==='bright-')  return Math.max(v-80,0);
    if(type==='thresh')   return v>=128?255:0;
    return v;
  }));

  let changedCount=0;
  const pimg=document.getElementById('pimg');
  const pmg=document.getElementById('pmg');
  pimg.innerHTML=''; pmg.innerHTML='';
  for(let r=0;r<6;r++) for(let c=0;c<6;c++){
    const v=processed[r][c];
    const orig=PROC6[r][c];
    const changed=(v!==orig);
    if(changed) changedCount++;
    // 이미지 셀
    const dc=document.createElement('div');
    dc.style.cssText=`width:35px;height:35px;background:rgb(${v},${v},${v});`+
      `border-radius:2px;border:2px solid ${changed?'#f59e0b':'transparent'};transition:background .35s`;
    pimg.appendChild(dc);
    // 행렬 셀
    const mc=document.createElement('div');
    mc.className='mc'+(changed?' proc':'');
    mc.style.width='35px'; mc.textContent=v;
    pmg.appendChild(mc);
  }
  const badge=document.getElementById('diff-badge');
  badge.textContent=changedCount>0?`${changedCount}개 변화`:'변화 없음';
  badge.style.background=changedCount>0?'rgba(167,139,250,.25)':'rgba(14,165,233,.12)';
  badge.style.color=changedCount>0?'#c4b5fd':'#38bdf8';
  badge.style.borderColor=changedCount>0?'rgba(167,139,250,.4)':'rgba(14,165,233,.25)';
}

function buildProcOrig(){
  const og=document.getElementById('og');
  og.innerHTML='';
  for(let r=0;r<6;r++) for(let c=0;c<6;c++){
    const v=PROC6[r][c];
    const d=document.createElement('div');
    d.style.cssText=`width:35px;height:35px;background:rgb(${v},${v},${v});border-radius:2px`;
    og.appendChild(d);
  }
}
buildProcOrig();
applyProc('orig');
</script>
</body>
</html>
"""


def render():
    components.html(_HTML, height=780, scrolling=False)

    # ── 성찰 기록 폼 ────────────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
