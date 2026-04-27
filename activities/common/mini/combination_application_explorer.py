# activities/common/mini/combination_application_explorer.py
"""
조합 활용 탐구 — 평행사변형·부분집합·원 위의 삼각형 3가지 상황에서
조합으로 개수를 구하는 원리를 인터랙티브하게 탐구하는 미니 활동
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "조합활용탐구"

META = {
    "title":       "🔺 조합 활용 탐구",
    "description": "평행사변형·부분집합·원 위의 삼각형 3가지 상황에서 조합으로 개수를 구하는 원리를 탐구합니다.",
    "order":       341,
    "hidden":      False,
}

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동을 마치고 아래 성찰 질문에 답해 보세요**"},
    {
        "key":    "평행사변형원리",
        "label":  "① 평행사변형의 개수를 구할 때 왜 ₘC₂ × ₙC₂를 사용할까요? 가로 평행선 2개와 사선 평행선 2개를 선택하는 것이 평행사변형을 결정하는 이유를 설명해보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "부분집합원리",
        "label":  "② {x₁, x₂, …, xₙ}에서 모든 부분집합의 개수가 2ⁿ인 이유를 ₙC₀+ₙC₁+⋯+ₙCₙ=2ⁿ과 연결하여 설명해보세요.",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "삼각형원리",
        "label":  "③ 원 위의 n개의 점으로 만들 수 있는 삼각형의 개수가 ₙC₃인 이유를 설명해보세요. 왜 점 3개를 고르면 항상 삼각형 하나가 결정될까요?",
        "type":   "text_area",
        "height": 110,
    },
    {
        "key":    "공통점",
        "label":  "④ 세 가지 상황(평행사변형, 부분집합, 삼각형)에서 조합을 사용하는 공통된 이유는 무엇인가요? 순열이 아닌 조합을 쓰는 까닭은?",
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

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Nanum Gothic',sans-serif;background:#12122a;color:#eee;padding:14px;}
.tabs{display:flex;gap:8px;margin-bottom:18px;flex-wrap:wrap;}
.tab-btn{
  padding:11px 18px;border:none;border-radius:28px;cursor:pointer;
  font-size:14px;font-weight:bold;transition:all .3s;
  background:#22224a;color:#99a;
}
.tab-btn.active{
  background:linear-gradient(135deg,#7c6fff,#3ecef7);
  color:#fff;box-shadow:0 4px 18px rgba(120,100,255,.45);
}
.tab-btn:hover:not(.active){background:#2d2d5e;color:#ccc;}
.tab-content{display:none;}
.tab-content.active{display:block;}

.card{background:#1a1a3e;border-radius:14px;padding:18px;margin-bottom:14px;}
.title-section{
  background:linear-gradient(135deg,#1a1a3e,#0f305a);
  border-left:5px solid #7c6fff;
  padding:12px 16px;border-radius:0 10px 10px 0;margin-bottom:16px;
}
.title-section h2{font-size:18px;color:#7c6fff;margin-bottom:4px;}
.title-section p{font-size:13px;color:#aab;}

.formula-box{
  background:linear-gradient(135deg,#1e1e4e,#16163e);
  border:2px solid #7c6fff;border-radius:12px;
  padding:14px;text-align:center;font-size:18px;
  margin:14px 0;font-weight:bold;line-height:1.7;
}
.formula-box .val{color:#FFD700;font-size:26px;}

.slider-row{display:flex;align-items:center;gap:12px;margin:10px 0;}
.slider-label{width:150px;font-size:14px;color:#ccd;}
input[type=range]{flex:1;accent-color:#7c6fff;cursor:pointer;height:6px;}
.slider-val{
  width:34px;text-align:center;font-weight:bold;
  color:#7c6fff;font-size:20px;
}

canvas{display:block;margin:0 auto;border-radius:12px;background:#0d0d22;max-width:100%;}

.btn{
  padding:10px 22px;border:none;border-radius:26px;cursor:pointer;
  font-size:14px;font-weight:bold;transition:all .2s;margin:5px;
}
.btn-p{background:linear-gradient(135deg,#7c6fff,#3ecef7);color:#fff;}
.btn-s{background:#22224a;color:#aab;border:1px solid #445;}
.btn:hover{transform:scale(1.05);}
.btn:active{transform:scale(.97);}

.info-text{font-size:13px;color:#99a;text-align:center;margin:8px 0;line-height:1.6;}
.hl{color:#FFD700;font-weight:bold;}

.step-counter{font-size:13px;color:#99a;text-align:center;margin:6px 0;min-height:18px;}
.progress-bar{height:6px;background:#22224a;border-radius:3px;margin:6px 0;overflow:hidden;}
.progress-fill{height:100%;background:linear-gradient(to right,#7c6fff,#3ecef7);border-radius:3px;transition:width .35s;}

/* ── Tab 1: Subset ── */
.elem-wrap{display:flex;justify-content:center;flex-wrap:wrap;gap:10px;margin:16px 0;}
.elem-circle{
  display:inline-flex;align-items:center;justify-content:center;
  width:52px;height:52px;border-radius:50%;font-size:20px;font-weight:bold;
  transition:all .35s;border:3px solid transparent;cursor:default;
}
.subset-grid{
  display:flex;flex-wrap:wrap;gap:8px;margin-top:10px;
  max-height:220px;overflow-y:auto;padding:8px;
  background:#10102e;border-radius:10px;
}
.sitem{
  background:#22224a;border-radius:8px;padding:6px 13px;
  font-size:13px;border:2px solid transparent;transition:all .3s;
}
.sitem.on{border-color:#FFD700;background:#33336e;color:#FFD700;}

.kbar-wrap{display:flex;align-items:flex-end;justify-content:center;gap:14px;height:120px;margin:14px 0;}
.kbar-item{display:flex;flex-direction:column;align-items:center;gap:3px;}
.kbar{
  width:44px;border-radius:6px 6px 0 0;min-height:4px;
  background:linear-gradient(to top,#7c6fff,#3ecef7);transition:height .5s;
}
.kbar.kactive{background:linear-gradient(to top,#FFD700,#FF6B6B);}
.kbar-lbl{font-size:11px;color:#99a;}
.kbar-cnt{font-size:12px;color:#7c6fff;font-weight:bold;}
.kbar-item.kactive .kbar-cnt{color:#FFD700;}
.kbar-item.kactive .kbar-lbl{color:#FFD700;}

/* ── Tab 2: Triangle ── */
.tri-info{display:flex;justify-content:space-around;flex-wrap:wrap;gap:8px;margin:12px 0;}
.icard{background:#22224a;border-radius:12px;padding:10px 18px;text-align:center;min-width:110px;}
.icard .num{font-size:30px;font-weight:bold;color:#7c6fff;}
.icard .lbl{font-size:11px;color:#99a;margin-top:3px;}
</style>
</head>
<body>

<div class="tabs">
  <button class="tab-btn active" onclick="showTab(0)">① 평행사변형 만들기</button>
  <button class="tab-btn" onclick="showTab(1)">② 부분집합 탐험</button>
  <button class="tab-btn" onclick="showTab(2)">③ 원 위의 삼각형</button>
</div>

<!-- ══════════════════ TAB 0 : PARALLELOGRAM ══════════════════ -->
<div id="tab0" class="tab-content active">
  <div class="title-section">
    <h2>📐 평행사변형의 개수를 조합으로!</h2>
    <p>m개의 가로 평행선과 n개의 사선 평행선으로 만들어지는 평행사변형의 개수 = <strong>ₘC₂ × ₙC₂</strong></p>
  </div>

  <div class="card">
    <div class="slider-row">
      <span class="slider-label">가로 평행선 m =</span>
      <input type="range" id="slM" min="2" max="6" value="3" oninput="updatePara()">
      <span class="slider-val" id="vM">3</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">사선 평행선 n =</span>
      <input type="range" id="slN" min="2" max="6" value="5" oninput="updatePara()">
      <span class="slider-val" id="vN">5</span>
    </div>
  </div>

  <canvas id="paraCanvas" width="560" height="400"></canvas>

  <div class="formula-box" id="paraFormula">
    ₃C₂ × ₅C₂ = 3 × 10 = <span class="val" id="totalPara">30</span> 개
  </div>

  <div style="text-align:center;margin:10px 0;">
    <button class="btn btn-p" onclick="showRandom()">🎲 랜덤 평행사변형!</button>
    <button class="btn btn-p" id="btnAuto" onclick="toggleAuto()">▶ 자동 탐색</button>
    <button class="btn btn-s" onclick="resetPara()">↺ 초기화</button>
  </div>
  <div class="step-counter" id="paraStep"></div>
  <div class="progress-bar" id="paraProg" style="display:none">
    <div class="progress-fill" id="paraFill" style="width:0%"></div>
  </div>
  <div class="info-text">
    💡 가로 평행선 2개를 선택하는 방법 <span class="hl">ₘC₂</span>가지,
    사선 평행선 2개를 선택하는 방법 <span class="hl">ₙC₂</span>가지.
    두 선택의 곱이 평행사변형의 총 개수입니다!
  </div>
</div>

<!-- ══════════════════ TAB 1 : SUBSETS ══════════════════ -->
<div id="tab1" class="tab-content">
  <div class="title-section">
    <h2>🧩 부분집합의 개수를 조합으로!</h2>
    <p>n개의 원소를 가진 집합에서 k개짜리 부분집합의 개수 = <strong>ₙCₖ</strong>,  모든 부분집합의 합 = <strong>2ⁿ</strong></p>
  </div>

  <div class="card">
    <div class="slider-row">
      <span class="slider-label">원소의 개수 n =</span>
      <input type="range" id="slSubN" min="3" max="5" value="4" oninput="updateSub()">
      <span class="slider-val" id="vSubN">4</span>
    </div>
    <div class="slider-row">
      <span class="slider-label">부분집합 크기 k =</span>
      <input type="range" id="slK" min="0" max="4" value="2" oninput="updateSub()">
      <span class="slider-val" id="vK">2</span>
    </div>
  </div>

  <div class="elem-wrap" id="elemWrap"></div>

  <div class="formula-box">
    집합 <span id="setDisp" class="hl">{a, b, c, d}</span>에서<br>
    <span id="fSubN">₄</span>C<span id="fSubK">₂</span> = <span class="val" id="subCnt">6</span> 개의 부분집합
  </div>

  <div style="text-align:center;margin:10px 0;">
    <button class="btn btn-p" onclick="nextSub()">▶ 다음 부분집합</button>
    <button class="btn btn-p" onclick="allSub()">🔍 모두 표시</button>
    <button class="btn btn-s" onclick="resetSub()">↺ 초기화</button>
  </div>

  <div class="subset-grid" id="subGrid"></div>

  <div class="card" style="margin-top:14px;">
    <div style="font-size:14px;color:#3ecef7;font-weight:bold;margin-bottom:8px;">
      모든 k에 대한 ₙCₖ — 합산하면 2ⁿ!
    </div>
    <div class="kbar-wrap" id="kbars"></div>
    <div style="text-align:center;font-size:15px;margin-top:6px;">
      ₙC₀ + ₙC₁ + ₙC₂ + ⋯ + ₙCₙ = <span class="val" id="pow2n">16</span> = 2<sup id="powN">4</sup>
    </div>
  </div>
</div>

<!-- ══════════════════ TAB 2 : TRIANGLES ══════════════════ -->
<div id="tab2" class="tab-content">
  <div class="title-section">
    <h2>🔺 원 위의 점으로 만드는 삼각형!</h2>
    <p>원 위에 서로 다른 n개의 점이 있을 때, 3개의 점을 선택하면 삼각형 하나가 결정됩니다. 삼각형의 개수 = <strong>ₙC₃</strong></p>
  </div>

  <div class="card">
    <div class="slider-row">
      <span class="slider-label">점의 개수 n =</span>
      <input type="range" id="slCN" min="4" max="8" value="5" oninput="updateCirc()">
      <span class="slider-val" id="vCN">5</span>
    </div>
  </div>

  <canvas id="circCanvas" width="560" height="460"></canvas>

  <div class="tri-info">
    <div class="icard">
      <div class="num" id="cN">5</div><div class="lbl">점의 개수 (n)</div>
    </div>
    <div class="icard">
      <div class="num" id="nc3">10</div><div class="lbl">ₙC₃ (삼각형 총수)</div>
    </div>
    <div class="icard">
      <div class="num" id="triIdx">0</div><div class="lbl">현재 번호</div>
    </div>
  </div>

  <div class="formula-box">
    <span id="triF">₅</span>C₃ = <span class="val" id="triTotal">10</span> 개의 삼각형
  </div>

  <div style="text-align:center;margin:10px 0;">
    <button class="btn btn-p" onclick="nextTri()">▶ 다음 삼각형</button>
    <button class="btn btn-p" id="btnAll" onclick="toggleAll()">🌈 모두 보기</button>
    <button class="btn btn-s" onclick="resetCirc()">↺ 초기화</button>
  </div>
  <div class="step-counter" id="triStep"></div>
  <div class="progress-bar" id="triProg" style="display:none">
    <div class="progress-fill" id="triFill" style="width:0%"></div>
  </div>
  <div class="info-text">
    💡 원 위의 서로 다른 n개의 점에서 3개를 선택하면 항상 삼각형 하나가 결정됩니다.
    (어떤 3점도 일직선 위에 놓이지 않으므로)
  </div>
</div>

<script>
// ── 공통 유틸 ──────────────────────────────────────────────────────────────
function C(n, r) {
  if (r < 0 || r > n) return 0;
  if (r === 0 || r === n) return 1;
  if (r > n - r) r = n - r;
  let v = 1;
  for (let i = 0; i < r; i++) v = v * (n - i) / (i + 1);
  return Math.round(v);
}
const SUB = ['₀','₁','₂','₃','₄','₅','₆','₇','₈','₉'];
function sub(n) { return String(n).split('').map(d => SUB[+d]).join(''); }

function sendHeight(){
  const h = document.body.scrollHeight + 30;
  window.parent.postMessage({type:'streamlit:setFrameHeight', height:h}, '*');
}
function showTab(i) {
  document.querySelectorAll('.tab-content').forEach((el,j)=>el.classList.toggle('active',i===j));
  document.querySelectorAll('.tab-btn').forEach((el,j)=>el.classList.toggle('active',i===j));
  setTimeout(sendHeight, 80);
}

// ══════════════════════════════════════════════════════════════════════════
// TAB 0 — PARALLELOGRAM
// ══════════════════════════════════════════════════════════════════════════
const pCvs = document.getElementById('paraCanvas');
const pCtx = pCvs.getContext('2d');
const SLOPE = 1.75;   // dy/dx in screen coords (down-right)
let pM=3, pN=5, pSelH=[], pSelD=[], pCombos=[], pIdx=0, pTimer=null;

function hLines(m,H){ const a=[],mg=H*.14; for(let i=0;i<m;i++) a.push(mg+(H-2*mg)*i/(m-1)); return a; }
function dLines(n,W,H){
  const a=[], yMax=H*.86, xEnd=W-yMax/SLOPE-8;
  for(let i=0;i<n;i++) a.push(60+(xEnd-60)*i/(n-1));
  return a;
}
function ix(y,x0){ return y/SLOPE+x0; }  // x at given y for diagonal line with x-intercept x0

function buildCombos(){
  pCombos=[];
  for(let i=0;i<pM-1;i++) for(let j=i+1;j<pM;j++)
    for(let a=0;a<pN-1;a++) for(let b=a+1;b<pN;b++)
      pCombos.push([[i,j],[a,b]]);
}

function drawPara(selH,selD){
  const W=pCvs.width, H=pCvs.height;
  pCtx.clearRect(0,0,W,H);
  const hl=hLines(pM,H), dl=dLines(pN,W,H);

  // shaded parallelogram (draw first, under lines)
  if(selH.length===2 && selD.length===2){
    const h1=hl[selH[0]],h2=hl[selH[1]],d1=dl[selD[0]],d2=dl[selD[1]];
    const p1={x:ix(h1,d1),y:h1},p2={x:ix(h1,d2),y:h1};
    const p3={x:ix(h2,d2),y:h2},p4={x:ix(h2,d1),y:h2};
    pCtx.beginPath();
    pCtx.fillStyle='rgba(255,220,50,.3)';
    pCtx.moveTo(p1.x,p1.y);[p2,p3,p4].forEach(p=>pCtx.lineTo(p.x,p.y));
    pCtx.closePath(); pCtx.fill();
    pCtx.beginPath();
    pCtx.strokeStyle='#FFD700'; pCtx.lineWidth=2.5;
    pCtx.moveTo(p1.x,p1.y);[p2,p3,p4].forEach(p=>pCtx.lineTo(p.x,p.y));
    pCtx.closePath(); pCtx.stroke();
    [p1,p2,p3,p4].forEach(p=>{
      pCtx.beginPath(); pCtx.fillStyle='#FFD700';
      pCtx.arc(p.x,p.y,6,0,Math.PI*2); pCtx.fill();
    });
  }

  // diagonal lines
  for(let i=0;i<pN;i++){
    const sel=selD.includes(i);
    pCtx.beginPath();
    pCtx.strokeStyle=sel?'#FF7070':'rgba(200,90,90,.55)';
    pCtx.lineWidth=sel?3:1.5;
    pCtx.moveTo(ix(-10,dl[i]),-10); pCtx.lineTo(ix(H+10,dl[i]),H+10);
    pCtx.stroke();
    if(sel){
      pCtx.fillStyle='#FF8888'; pCtx.font='bold 13px sans-serif';
      pCtx.fillText('n'+(i+1), ix(18,dl[i])-6, 28);
    }
  }

  // horizontal lines
  for(let i=0;i<pM;i++){
    const sel=selH.includes(i);
    pCtx.beginPath();
    pCtx.strokeStyle=sel?'#4ECDC4':'rgba(80,190,120,.55)';
    pCtx.lineWidth=sel?3:1.5;
    pCtx.moveTo(0,hl[i]); pCtx.lineTo(W,hl[i]);
    pCtx.stroke();
    if(sel){
      pCtx.fillStyle='#4ECDC4'; pCtx.font='bold 13px sans-serif';
      pCtx.fillText('m'+(i+1), 8, hl[i]-7);
    }
  }

  // intersection dots
  hl.forEach((hy,hi)=> dl.forEach((dx,di)=>{
    const x=ix(hy,dx);
    if(x<0||x>W) return;
    const on=selH.includes(hi)&&selD.includes(di);
    pCtx.beginPath();
    pCtx.fillStyle=on?'#FFD700':'rgba(140,140,200,.45)';
    pCtx.arc(x,hy,on?6:3,0,Math.PI*2); pCtx.fill();
  }));
}

function updatePara(){
  pM=+document.getElementById('slM').value;
  pN=+document.getElementById('slN').value;
  document.getElementById('vM').textContent=pM;
  document.getElementById('vN').textContent=pN;
  const mc2=C(pM,2), nc2=C(pN,2);
  document.getElementById('paraFormula').innerHTML=
    `${sub(pM)}C₂ × ${sub(pN)}C₂ = ${mc2} × ${nc2} = <span class="val" id="totalPara">${mc2*nc2}</span> 개`;
  stopAuto(); pSelH=[]; pSelD=[];
  buildCombos(); drawPara([],[]);
  document.getElementById('paraStep').textContent='';
}

function showRandom(){
  stopAuto();
  const [h,d]=pCombos[Math.floor(Math.random()*pCombos.length)];
  pSelH=h; pSelD=d; drawPara(h,d);
  document.getElementById('paraStep').textContent=
    `선택: 가로선 m${h[0]+1}, m${h[1]+1}  ×  사선 n${d[0]+1}, n${d[1]+1}`;
}

function toggleAuto(){
  if(pTimer){ stopAuto(); return; }
  pIdx=0;
  document.getElementById('btnAuto').textContent='⏸ 정지';
  document.getElementById('paraProg').style.display='block';
  autoStep();
}
function autoStep(){
  if(pIdx>=pCombos.length){ stopAuto(); return; }
  const [h,d]=pCombos[pIdx];
  drawPara(h,d);
  document.getElementById('paraStep').textContent=
    `${pIdx+1} / ${pCombos.length}:  m${h[0]+1},m${h[1]+1} × n${d[0]+1},n${d[1]+1}`;
  document.getElementById('paraFill').style.width=((pIdx+1)/pCombos.length*100)+'%';
  pIdx++;
  pTimer=setTimeout(autoStep,550);
}
function stopAuto(){
  clearTimeout(pTimer); pTimer=null;
  document.getElementById('btnAuto').textContent='▶ 자동 탐색';
  document.getElementById('paraProg').style.display='none';
}
function resetPara(){ stopAuto(); pSelH=[]; pSelD=[]; drawPara([],[]); document.getElementById('paraStep').textContent=''; }

// ══════════════════════════════════════════════════════════════════════════
// TAB 1 — SUBSETS
// ══════════════════════════════════════════════════════════════════════════
const ENAMES=['a','b','c','d','e'];
const ECOLORS=['#FF6B6B','#4ECDC4','#FFD700','#7c6fff','#45B7D1'];
let sN=4, sK=2, sCombos=[], sCur=0;

function combs(arr,k){
  if(k===0) return [[]];
  if(!arr.length) return [];
  const [f,...r]=arr;
  return [...combs(r,k-1).map(c=>[f,...c]), ...combs(r,k)];
}

function updateSub(){
  sN=+document.getElementById('slSubN').value;
  const ks=document.getElementById('slK');
  ks.max=sN; sK=Math.min(+ks.value,sN); ks.value=sK;
  document.getElementById('vSubN').textContent=sN;
  document.getElementById('vK').textContent=sK;

  const elems=ENAMES.slice(0,sN);
  document.getElementById('setDisp').textContent='{'+elems.join(', ')+'}';
  document.getElementById('fSubN').textContent=sub(sN);
  document.getElementById('fSubK').textContent=sub(sK);
  document.getElementById('subCnt').textContent=C(sN,sK);
  document.getElementById('pow2n').textContent=Math.pow(2,sN);
  document.getElementById('powN').textContent=sN;

  // elements display
  document.getElementById('elemWrap').innerHTML=elems.map((e,i)=>
    `<span class="elem-circle" id="ec${i}" style="background:${ECOLORS[i]}33;border-color:${ECOLORS[i]}">${e}</span>`
  ).join('');

  sCombos=combs(Array.from({length:sN},(_,i)=>i), sK);
  sCur=0;
  renderSubGrid();
  renderKBars();
  hlElems([]);
}

function hlElems(idxs){
  ENAMES.slice(0,sN).forEach((_,i)=>{
    const el=document.getElementById('ec'+i); if(!el)return;
    if(idxs.includes(i)){
      el.style.background=ECOLORS[i]+'cc';
      el.style.transform='scale(1.25)';
      el.style.boxShadow=`0 0 18px ${ECOLORS[i]}`;
    } else {
      el.style.background=ECOLORS[i]+'33';
      el.style.transform='scale(1)';
      el.style.boxShadow='none';
    }
  });
}

function renderSubGrid(){
  const elems=ENAMES.slice(0,sN);
  document.getElementById('subGrid').innerHTML=sCombos.map((s,i)=>{
    const lbl=s.length===0?'∅':'{'+s.map(j=>elems[j]).join(', ')+'}';
    return `<div class="sitem" id="si${i}">${lbl}</div>`;
  }).join('');
}

function nextSub(){
  if(!sCombos.length) return;
  document.querySelectorAll('.sitem').forEach(el=>el.classList.remove('on'));
  const c=sCombos[sCur], el=document.getElementById('si'+sCur);
  if(el){ el.classList.add('on'); el.scrollIntoView({behavior:'smooth',block:'nearest'}); }
  hlElems(c);
  sCur=(sCur+1)%sCombos.length;
}
function allSub(){
  document.querySelectorAll('.sitem').forEach(el=>el.classList.add('on'));
  hlElems(Array.from({length:sN},(_,i)=>i));
}
function resetSub(){
  sCur=0;
  document.querySelectorAll('.sitem').forEach(el=>el.classList.remove('on'));
  hlElems([]);
}

function renderKBars(){
  const maxC=Math.max(...Array.from({length:sN+1},(_,k)=>C(sN,k)));
  let html='';
  for(let k=0;k<=sN;k++){
    const cnt=C(sN,k), h=Math.max(4,(cnt/maxC)*85), act=k===sK?'kactive':'';
    html+=`<div class="kbar-item ${act}">
      <div class="kbar-cnt">${cnt}</div>
      <div class="kbar ${act}" style="height:${h}px"></div>
      <div class="kbar-lbl">k=${k}</div>
    </div>`;
  }
  document.getElementById('kbars').innerHTML=html;
}

// ══════════════════════════════════════════════════════════════════════════
// TAB 2 — TRIANGLES ON CIRCLE
// ══════════════════════════════════════════════════════════════════════════
const tCvs=document.getElementById('circCanvas');
const tCtx=tCvs.getContext('2d');
let cN=5, cTris=[], cIdx=0, cAll=false;

const TCOLS=[
  '#FF6B6B','#4ECDC4','#FFD700','#7c6fff','#45B7D1',
  '#FF8E53','#A8E6CF','#FF6EB4','#88D8B0','#FFCB47',
  '#B088FF','#FF8888','#88FFCC','#FFD088','#88BBFF',
  '#FF88AA','#AAFFCC','#FFAA88','#88AAFF','#CCFF88',
  '#FF6677','#77FFAA','#FFAA77','#7766FF','#AAFF77',
  '#FF9988','#88FFBB','#FFBB88','#8899FF','#BBFF88',
  '#FFAA99','#99FFCC','#FFCCAA','#99AAFF','#CCFFAA',
  '#FFB3B3','#B3FFE6','#FFE6B3','#B3C6FF','#E6FFB3',
  '#FF99CC','#99FFEE','#FFEECC','#99BBFF','#EEFFCC',
  '#FFCCDD','#CCFFE8','#FFE8CC','#CCDDFF','#E8FFCC',
];

function circPts(n,W,H){
  const cx=W/2,cy=H/2,r=Math.min(W,H)*.38,pts=[];
  for(let i=0;i<n;i++){
    const a=2*Math.PI*i/n - Math.PI/2;
    pts.push({x:cx+r*Math.cos(a),y:cy+r*Math.sin(a)});
  }
  return pts;
}

function buildTris(n){
  const t=[];
  for(let i=0;i<n-2;i++) for(let j=i+1;j<n-1;j++) for(let k=j+1;k<n;k++) t.push([i,j,k]);
  return t;
}

function drawCirc(bgTris, curTri){
  const W=tCvs.width,H=tCvs.height;
  tCtx.clearRect(0,0,W,H);
  const pts=circPts(cN,W,H), cx=W/2,cy=H/2,r=Math.min(W,H)*.38;

  // circle outline
  tCtx.beginPath(); tCtx.arc(cx,cy,r,0,Math.PI*2);
  tCtx.strokeStyle='rgba(100,100,200,.35)'; tCtx.lineWidth=1.5; tCtx.stroke();

  // all triangles (background)
  if(bgTris.length>1){
    bgTris.forEach((tri,i)=>{
      const [a,b,c]=tri, col=TCOLS[i%TCOLS.length];
      tCtx.beginPath();
      tCtx.moveTo(pts[a].x,pts[a].y);
      tCtx.lineTo(pts[b].x,pts[b].y);
      tCtx.lineTo(pts[c].x,pts[c].y);
      tCtx.closePath();
      tCtx.fillStyle=col+'28'; tCtx.fill();
      tCtx.strokeStyle=col+'88'; tCtx.lineWidth=1; tCtx.stroke();
    });
  }

  // current triangle
  if(curTri!==null){
    const [a,b,c]=curTri;
    tCtx.beginPath();
    tCtx.moveTo(pts[a].x,pts[a].y);
    tCtx.lineTo(pts[b].x,pts[b].y);
    tCtx.lineTo(pts[c].x,pts[c].y);
    tCtx.closePath();
    tCtx.fillStyle='rgba(255,215,0,.32)'; tCtx.fill();
    tCtx.strokeStyle='#FFD700'; tCtx.lineWidth=3; tCtx.stroke();
  }

  // points & labels
  pts.forEach((p,i)=>{
    const inT=curTri&&curTri.includes(i);
    tCtx.beginPath();
    tCtx.fillStyle=inT?'#FFD700':'#7c6fff';
    tCtx.arc(p.x,p.y,inT?9:7,0,Math.PI*2); tCtx.fill();
    tCtx.beginPath();
    tCtx.strokeStyle=inT?'#fff':'#3ecef7'; tCtx.lineWidth=2;
    tCtx.arc(p.x,p.y,inT?9:7,0,Math.PI*2); tCtx.stroke();

    const a=2*Math.PI*i/cN - Math.PI/2, off=22;
    tCtx.fillStyle=inT?'#FFD700':'#dde';
    tCtx.font=`bold ${inT?15:13}px sans-serif`;
    tCtx.textAlign='center'; tCtx.textBaseline='middle';
    tCtx.fillText('P'+(i+1), cx+(r+off)*Math.cos(a), cy+(r+off)*Math.sin(a));
  });
}

function updateCirc(){
  cN=+document.getElementById('slCN').value;
  document.getElementById('vCN').textContent=cN;
  document.getElementById('cN').textContent=cN;
  const nc3=C(cN,3);
  document.getElementById('nc3').textContent=nc3;
  document.getElementById('triF').textContent=sub(cN);
  document.getElementById('triTotal').textContent=nc3;
  document.getElementById('triIdx').textContent='0';
  cTris=buildTris(cN); cIdx=0; cAll=false;
  document.getElementById('btnAll').textContent='🌈 모두 보기';
  document.getElementById('triProg').style.display='none';
  document.getElementById('triStep').textContent='';
  drawCirc([],null);
}

function nextTri(){
  if(!cTris.length) return;
  cAll=false; document.getElementById('btnAll').textContent='🌈 모두 보기';
  const tri=cTris[cIdx];
  drawCirc([],tri);
  document.getElementById('triStep').textContent=
    `${cIdx+1} / ${cTris.length}:  삼각형 P${tri[0]+1}−P${tri[1]+1}−P${tri[2]+1}`;
  document.getElementById('triIdx').textContent=cIdx+1;
  document.getElementById('triProg').style.display='block';
  document.getElementById('triFill').style.width=((cIdx+1)/cTris.length*100)+'%';
  cIdx=(cIdx+1)%cTris.length;
}

function toggleAll(){
  cAll=!cAll;
  if(cAll){
    drawCirc(cTris,null);
    document.getElementById('btnAll').textContent='🔲 초기화';
    document.getElementById('triStep').textContent='총 '+cTris.length+'개 삼각형 모두 표시!';
    document.getElementById('triProg').style.display='block';
    document.getElementById('triFill').style.width='100%';
    document.getElementById('triIdx').textContent=cTris.length;
  } else { resetCirc(); }
}

function resetCirc(){
  cIdx=0; cAll=false;
  document.getElementById('btnAll').textContent='🌈 모두 보기';
  document.getElementById('triStep').textContent='';
  document.getElementById('triProg').style.display='none';
  document.getElementById('triIdx').textContent='0';
  drawCirc([],null);
}

// ── 초기화 ──────────────────────────────────────────────────────────────
buildCombos(); updatePara();
updateSub();
updateCirc();
window.addEventListener('load', ()=>setTimeout(sendHeight, 150));
</script>
</body>
</html>
"""

def render():
    components.html(_HTML, height=1100, scrolling=False)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
