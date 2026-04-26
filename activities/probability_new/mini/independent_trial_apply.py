import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "독립시행실생활"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 독립시행 실생활 탐구 – 성찰 질문**"},
    {
        "key": "독립시행이유",
        "label": "탐구한 4가지 상황(자유투·한국시리즈·양궁·날씨) 중 하나를 골라, 그것이 '독립시행'이라고 할 수 있는 이유를 설명하세요.",
        "type": "text_area",
        "height": 100,
    },
    {
        "key": "공식분해",
        "label": "공식 nCr × p^r × (1-p)^(n-r) 에서 ① nCr  ② p^r  ③ (1-p)^(n-r) 이 각각 무엇을 뜻하는지 자신의 말로 설명하세요.",
        "type": "text_area",
        "height": 110,
    },
    {
        "key": "나만의예시",
        "label": "일상생활에서 독립시행을 적용할 수 있는 나만의 상황을 만들고, 구체적인 확률을 직접 계산해 보세요.",
        "type": "text_area",
        "height": 120,
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점",        "label": "💬 느낀 점",           "type": "text_area", "height": 90},
]

META = {
    "title":       "🎯 독립시행 실생활 탐구",
    "description": "농구·야구·양궁·날씨 속 독립시행 확률을 탐구하며 공식을 익힙니다.",
    "order":       999999,
    "hidden":      True,
}

_HTML = r"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a1628 0%,#0f2027 50%,#0a1628 100%);min-height:100vh;padding:14px 14px 24px;color:#e2e8f0}

/* ── Tab navigation ─────────────────────────── */
.tab-nav{display:flex;gap:7px;margin-bottom:14px;flex-wrap:wrap}
.tab-btn{padding:9px 18px;border-radius:12px;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.04);cursor:pointer;font-size:13px;font-weight:700;color:#94a3b8;transition:.2s;white-space:nowrap}
.tab-btn:hover{background:rgba(255,255,255,.09)}
.tab-btn.active{background:rgba(99,102,241,.25);color:#a5b4fc;border-color:rgba(99,102,241,.5)}
.tab-pane{display:none}.tab-pane.active{display:block}

/* ── Cards ──────────────────────────────────── */
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:18px 22px;backdrop-filter:blur(10px)}
.prob-box{background:rgba(99,102,241,.1);border:1px solid rgba(99,102,241,.3);border-radius:14px;padding:13px 18px;margin-bottom:14px}
.prob-title{font-size:17px;font-weight:800;color:#a5b4fc;margin-bottom:5px}
.prob-text{font-size:14px;color:#cbd5e1;line-height:1.65}

/* ── Controls ───────────────────────────────── */
.ctrl-row{display:flex;gap:18px;flex-wrap:wrap;align-items:flex-end;margin-bottom:14px}
.ctrl-item{display:flex;flex-direction:column;gap:5px}
.ctrl-label{font-size:11px;color:#94a3b8;font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.vb{display:inline-block;min-width:44px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:8px;padding:2px 10px;font-weight:800;font-size:14px;text-align:center;color:#fff;box-shadow:0 2px 10px rgba(99,102,241,.4);margin-left:4px}
input[type=range]{-webkit-appearance:none;height:6px;border-radius:3px;background:linear-gradient(90deg,#6366f1,#8b5cf6);outline:none;width:155px;cursor:pointer}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:#fff;border:3px solid #6366f1;cursor:pointer;box-shadow:0 0 8px rgba(99,102,241,.5)}

/* ── Formula box ────────────────────────────── */
.fbox{background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.3);border-radius:14px;padding:13px 20px;margin-bottom:12px;text-align:center}
.fexpr{font-size:16px;font-weight:700;color:#34d399;font-family:monospace;margin-bottom:5px;line-height:1.6}
.fans{font-size:24px;font-weight:900;color:#10b981;margin:4px 0}
.fnote{font-size:12px;color:#6ee7b7;margin-top:3px}

/* ── Bar chart ──────────────────────────────── */
.chart-wrap{overflow-x:auto;padding:2px 0}
.chart{display:flex;align-items:flex-end;gap:8px;height:240px;padding-bottom:36px}
.bc{display:flex;flex-direction:column;align-items:center;gap:3px;cursor:pointer}
.bar{width:54px;border-radius:6px 6px 0 0;background:linear-gradient(180deg,#6366f1,#4f46e5);transition:all .3s;min-height:4px}
.bar.hl{background:linear-gradient(180deg,#f59e0b,#d97706)}
.bar:hover{filter:brightness(1.3)}
.blbl{font-size:13px;color:#94a3b8;margin-top:3px}
.bpct{font-size:11px;color:#64748b}

/* ── Emoji grid ─────────────────────────────── */
.eg{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0}
.ei{font-size:42px;width:68px;height:68px;display:flex;align-items:center;justify-content:center;border-radius:14px;border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.04);transition:.25s}
.ei.suc{background:rgba(16,185,129,.2);border-color:rgba(16,185,129,.4)}
.ei.fail{background:rgba(239,68,68,.14);border-color:rgba(239,68,68,.3)}

/* ── Baseball bracket ───────────────────────── */
.brk{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}
.gc{width:90px;height:90px;border-radius:16px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:14px;font-weight:700;gap:5px;border:2px solid rgba(255,255,255,.1);background:rgba(255,255,255,.04)}
.gc .gi{font-size:28px}
.gc.aw{border-color:rgba(59,130,246,.55);background:rgba(59,130,246,.16)}
.gc.bw{border-color:rgba(239,68,68,.45);background:rgba(239,68,68,.13)}
.gc.pd{opacity:.55}
.kpi-row{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}
.kpi{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:14px 28px;text-align:center;min-width:140px}
.kpi .num{font-size:30px;font-weight:900}
.kpi .lbl{font-size:11px;color:#94a3b8;margin-top:4px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.chip{display:inline-block;background:rgba(99,102,241,.15);border:1px solid rgba(99,102,241,.3);border-radius:8px;padding:5px 12px;font-size:13px;font-family:monospace;color:#a5b4fc;margin:4px 3px}

/* ── Weather ────────────────────────────────── */
.wr{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}
.wday{width:80px;border-radius:14px;padding:12px 6px;display:flex;flex-direction:column;align-items:center;gap:5px;border:2px solid rgba(255,255,255,.1);background:rgba(255,255,255,.04);cursor:pointer;transition:.2s;font-size:13px;font-weight:600;color:#94a3b8}
.wday .wi{font-size:40px}
.wday.rain{border-color:rgba(99,102,241,.55);background:rgba(99,102,241,.18)}
.wday.sun{border-color:rgba(245,158,11,.45);background:rgba(245,158,11,.13)}

::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(99,102,241,.4);border-radius:3px}
</style>
</head>
<body>

<!-- ── Tab nav ──────────────────────────────────── -->
<div class="tab-nav">
  <button class="tab-btn active" id="btn0" onclick="showTab(0)">🏀 자유투</button>
  <button class="tab-btn" id="btn1" onclick="showTab(1)">⚾ 한국시리즈</button>
  <button class="tab-btn" id="btn2" onclick="showTab(2)">🎯 양궁</button>
  <button class="tab-btn" id="btn3" onclick="showTab(3)">🌦️ 날씨</button>
</div>

<!-- ════════════════════════════════════════════════
     TAB 0 : 농구 자유투
     ════════════════════════════════════════════════ -->
<div class="tab-pane active" id="tab0">
<div class="card">
  <div class="prob-box">
    <div class="prob-title">🏀 농구 자유투</div>
    <div class="prob-text" id="pt0">…</div>
  </div>
  <div class="ctrl-row">
    <div class="ctrl-item">
      <span class="ctrl-label">성공 확률 p = <span class="vb" id="pv0">0.60</span></span>
      <input type="range" id="ps0" min="10" max="90" value="60" step="5" oninput="upd0()">
    </div>
    <div class="ctrl-item">
      <span class="ctrl-label">시도 횟수 n = <span class="vb" id="nv0">5</span></span>
      <input type="range" id="ns0" min="1" max="10" value="5" oninput="upd0()">
    </div>
    <div class="ctrl-item">
      <span class="ctrl-label">목표 r = <span class="vb" id="rv0">3</span></span>
      <input type="range" id="rs0" min="0" max="10" value="3" oninput="upd0()">
    </div>
  </div>
  <div class="eg" id="eg0"></div>
  <div class="fbox">
    <div class="fexpr" id="fe0">…</div>
    <div class="fans" id="fa0">…</div>
    <div class="fnote" id="fn0">…</div>
  </div>
  <div style="font-size:11px;color:#64748b;margin-bottom:6px">📊 r별 확률 분포 &nbsp;(막대 클릭 → r 변경)</div>
  <div class="chart-wrap"><div class="chart" id="ch0"></div></div>
</div>
</div>

<!-- ════════════════════════════════════════════════
     TAB 1 : 야구 한국시리즈
     ════════════════════════════════════════════════ -->
<div class="tab-pane" id="tab1">
<div class="card">
  <div class="prob-box">
    <div class="prob-title">⚾ 프로야구 한국시리즈 (7전 4선승제)</div>
    <div class="prob-text">현재까지 <strong style="color:#60a5fa">A팀 2승 1패</strong>. 각 경기에서 A팀의 승률이 p일 때, A팀이 우승할 확률을 구해 보자.</div>
  </div>
  <div class="ctrl-row">
    <div class="ctrl-item">
      <span class="ctrl-label">A팀 경기당 승률 p = <span class="vb" id="pv1">0.50</span></span>
      <input type="range" id="ps1" min="10" max="90" value="50" step="5" oninput="upd1()">
    </div>
  </div>
  <div class="brk" id="brk1"></div>
  <div class="kpi-row" id="kpi1"></div>
  <div class="fbox">
    <div class="fexpr" id="fe1" style="font-size:13px;line-height:1.8">…</div>
    <div class="fans" id="fa1">…</div>
  </div>
  <div style="font-size:11px;color:#64748b;margin-bottom:6px">🗺️ A팀 우승 경로별 확률</div>
  <div id="paths1"></div>
</div>
</div>

<!-- ════════════════════════════════════════════════
     TAB 2 : 양궁
     ════════════════════════════════════════════════ -->
<div class="tab-pane" id="tab2">
<div class="card">
  <div class="prob-box">
    <div class="prob-title">🎯 양궁 명중 확률 탐구</div>
    <div class="prob-text" id="pt2">…</div>
  </div>
  <div class="ctrl-row">
    <div class="ctrl-item">
      <span class="ctrl-label">명중 확률 p = <span class="vb" id="pv2">0.70</span></span>
      <input type="range" id="ps2" min="10" max="90" value="70" step="5" oninput="upd2()">
    </div>
    <div class="ctrl-item">
      <span class="ctrl-label">화살 수 n = <span class="vb" id="nv2">6</span></span>
      <input type="range" id="ns2" min="2" max="12" value="6" oninput="upd2()">
    </div>
  </div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-start">
    <canvas id="arc2" width="480" height="360" style="border-radius:14px;flex-shrink:0;border:1px solid rgba(255,255,255,.08);width:480px;max-width:100%"></canvas>
    <div style="flex:1;min-width:190px">
      <div class="fbox" style="margin-bottom:0">
        <div style="font-size:11px;color:#6ee7b7;margin-bottom:5px">선택된 r의 확률</div>
        <div class="fexpr" id="fe2">…</div>
        <div class="fans" id="fa2">…</div>
      </div>
    </div>
  </div>
  <div style="font-size:11px;color:#64748b;margin:10px 0 6px">📊 전체 확률 분포 &nbsp;(막대 클릭 → 과녁 시각화 변경)</div>
  <div class="chart-wrap"><div class="chart" id="ch2"></div></div>
</div>
</div>

<!-- ════════════════════════════════════════════════
     TAB 3 : 날씨
     ════════════════════════════════════════════════ -->
<div class="tab-pane" id="tab3">
<div class="card">
  <div class="prob-box">
    <div class="prob-title">🌦️ 일주일 날씨 예보</div>
    <div class="prob-text" id="pt3">…</div>
  </div>
  <div class="ctrl-row">
    <div class="ctrl-item">
      <span class="ctrl-label">하루 비올 확률 p = <span class="vb" id="pv3">0.40</span></span>
      <input type="range" id="ps3" min="10" max="90" value="40" step="5" oninput="upd3()">
    </div>
    <div class="ctrl-item">
      <span class="ctrl-label">비 오는 날 수 r = <span class="vb" id="rv3">3</span></span>
      <input type="range" id="rs3" min="0" max="7" value="3" oninput="upd3()">
    </div>
  </div>
  <div class="wr" id="wr3"></div>
  <div class="fbox">
    <div class="fexpr" id="fe3">…</div>
    <div class="fans" id="fa3">…</div>
    <div class="fnote" id="fn3">…</div>
  </div>
  <div style="font-size:11px;color:#64748b;margin-bottom:6px">📊 비 오는 날 수별 확률 분포 &nbsp;(막대 클릭)</div>
  <div class="chart-wrap"><div class="chart" id="ch3"></div></div>
</div>
</div>

<script>
// ── Math helpers ─────────────────────────────────────────────
function C(n,r){if(r<0||r>n)return 0;if(r===0||r===n)return 1;let x=1,k=Math.min(r,n-r);for(let i=0;i<k;i++)x=x*(n-i)/(i+1);return Math.round(x)}
function BP(n,r,p){if(r<0||r>n)return 0;return C(n,r)*Math.pow(p,r)*Math.pow(1-p,n-r)}
function pct(v){return(v*100).toFixed(2)+'%'}
function sr(seed){const x=Math.sin(seed*9301+49297)%1;return Math.abs(x)}  // seeded random

// ── Tab manager ──────────────────────────────────────────────
function showTab(i){
  document.querySelectorAll('.tab-pane').forEach((el,j)=>el.classList.toggle('active',j===i));
  document.querySelectorAll('.tab-btn').forEach((el,j)=>el.classList.toggle('active',j===i));
  if(i===2)setTimeout(drawArc2,30);
}

// ── Bar chart helper ─────────────────────────────────────────
function mkChart(id,probs,hl,cb){
  const c=document.getElementById(id);c.innerHTML='';
  const mx=Math.max(...probs,0.001);
  probs.forEach((p,r)=>{
    const h=Math.max(Math.round(p/mx*92),3);
    const g=document.createElement('div');g.className='bc';
    const b=document.createElement('div');
    b.className='bar'+(r===hl?' hl':'');b.style.height=h+'px';
    b.title=`r=${r}: ${pct(p)}`;
    if(cb)b.onclick=()=>cb(r);
    const lbl=document.createElement('div');lbl.className='blbl';lbl.textContent=r;
    const pv=document.createElement('div');pv.className='bpct';pv.textContent=(p*100).toFixed(1)+'%';
    g.appendChild(b);g.appendChild(lbl);g.appendChild(pv);
    c.appendChild(g);
  });
}

// ═══════════════════════════════════════════════
// TAB 0 : 농구 자유투
// ═══════════════════════════════════════════════
function upd0(){
  const p=+document.getElementById('ps0').value/100;
  const n=+document.getElementById('ns0').value;
  let r=+document.getElementById('rs0').value;
  if(r>n){r=n;document.getElementById('rs0').value=r;}
  document.getElementById('rs0').max=n;

  document.getElementById('pv0').textContent=p.toFixed(2);
  document.getElementById('nv0').textContent=n;
  document.getElementById('rv0').textContent=r;
  document.getElementById('pt0').textContent=
    `자유투 성공 확률이 ${p.toFixed(2)}인 선수가 ${n}번 자유투를 시도할 때, 정확히 ${r}번 성공할 확률은?`;

  // emoji grid
  const eg=document.getElementById('eg0');eg.innerHTML='';
  for(let i=0;i<n;i++){
    const d=document.createElement('div');
    d.className='ei '+(i<r?'suc':'fail');
    d.textContent=i<r?'🏀':'✖️';
    eg.appendChild(d);
  }

  const prob=BP(n,r,p), cn=C(n,r);
  document.getElementById('fe0').innerHTML=
    `<sub>${n}</sub>C<sub>${r}</sub> &times; ${p.toFixed(2)}<sup>${r}</sup> &times; ${(1-p).toFixed(2)}<sup>${n-r}</sup>`;
  document.getElementById('fa0').textContent=
    `= ${cn} × ${Math.pow(p,r).toFixed(4)} × ${Math.pow(1-p,n-r).toFixed(4)}`;
  document.getElementById('fn0').textContent=`≈ ${pct(prob)}`;

  const probs=[];for(let i=0;i<=n;i++)probs.push(BP(n,i,p));
  mkChart('ch0',probs,r,(ri)=>{document.getElementById('rs0').value=ri;upd0();});
}

// ═══════════════════════════════════════════════
// TAB 1 : 야구 한국시리즈
// ═══════════════════════════════════════════════
function upd1(){
  const p=+document.getElementById('ps1').value/100;
  document.getElementById('pv1').textContent=p.toFixed(2);

  // Bracket (3 played: A-win, B-win, A-win; 4 pending)
  const brk=document.getElementById('brk1');brk.innerHTML='';
  [
    {lbl:'1차전',cls:'aw',icon:'🔵'},
    {lbl:'2차전',cls:'bw',icon:'🔴'},
    {lbl:'3차전',cls:'aw',icon:'🔵'},
    {lbl:'4차전',cls:'pd',icon:'❓'},
    {lbl:'5차전',cls:'pd',icon:'❓'},
    {lbl:'6차전',cls:'pd',icon:'❓'},
    {lbl:'7차전',cls:'pd',icon:'❓'},
  ].forEach(g=>{
    const el=document.createElement('div');el.className='gc '+g.cls;
    el.innerHTML=`<span class="gi">${g.icon}</span><span>${g.lbl}</span>`;
    brk.appendChild(el);
  });

  // A needs 2 more wins, B needs 3 more wins
  // P(A wins in exactly r more games) = C(r-1, 1) * p^2 * (1-p)^(r-2)
  const aN=2, bN=3;
  let pA=0;
  const paths=[];
  for(let r=aN;r<=aN+bN-1;r++){
    const bW=r-aN;
    const pp=C(r-1,aN-1)*Math.pow(p,aN)*Math.pow(1-p,bW);
    pA+=pp;
    paths.push({r,bW,pp,cn:C(r-1,aN-1)});
  }

  document.getElementById('kpi1').innerHTML=
    `<div class="kpi"><div class="num" style="color:#60a5fa">${pct(pA)}</div><div class="lbl">A팀 우승 확률</div></div>
     <div class="kpi"><div class="num" style="color:#f87171">${pct(1-pA)}</div><div class="lbl">B팀 우승 확률</div></div>`;

  const parts=paths.map(({r,bW})=>
    `C(${r-1},1)&middot;p<sup>2</sup>&middot;(1-p)<sup>${bW}</sup>`).join(' + ');
  document.getElementById('fe1').innerHTML=`P(A우승) = ${parts}`;
  document.getElementById('fa1').textContent=
    `= ${paths.map(x=>pct(x.pp)).join(' + ')} = ${pct(pA)}`;

  const pd=document.getElementById('paths1');pd.innerHTML='';
  paths.forEach(({r,bW,pp,cn})=>{
    const d=document.createElement('div');d.style.marginBottom='5px';
    const remain=r-aN; // = bW
    d.innerHTML=`<span class="chip">${r}게임째 A 우승 &nbsp;│&nbsp; 나머지 ${remain}패 포함 &nbsp;│&nbsp; C(${r-1},1) = ${cn}가지 &nbsp;│&nbsp; ${pct(pp)}</span>`;
    pd.appendChild(d);
  });
}

// ═══════════════════════════════════════════════
// TAB 2 : 양궁
// ═══════════════════════════════════════════════
let arcHl=4; // highlighted r for archery

function drawArc2(){
  const cv=document.getElementById('arc2');if(!cv)return;
  const ctx=cv.getContext('2d');
  const cx=240,cy=180,maxR=155;
  ctx.clearRect(0,0,480,360);

  // Draw rings (outer→inner)
  const rings=[
    {r:maxR,  c:'#1e3a5f'},
    {r:maxR*.8,c:'#1e40af'},
    {r:maxR*.6,c:'#b91c1c'},
    {r:maxR*.4,c:'#dc2626'},
    {r:maxR*.22,c:'#1d4ed8'},
    {r:maxR*.08,c:'#fbbf24'},
  ];
  rings.forEach(({r,c})=>{
    ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);
    ctx.fillStyle=c;ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,.18)';ctx.lineWidth=1;ctx.stroke();
  });
  // crosshair
  ctx.strokeStyle='rgba(255,255,255,.15)';ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(cx-maxR,cy);ctx.lineTo(cx+maxR,cy);ctx.stroke();
  ctx.beginPath();ctx.moveTo(cx,cy-maxR);ctx.lineTo(cx,cy+maxR);ctx.stroke();

  const n=+document.getElementById('ns2').value;
  const r=arcHl;

  for(let i=0;i<n;i++){
    const hit=i<r;
    const angle=sr(i*7+1)*Math.PI*2;
    const dist=hit? sr(i*13+3)*56+10 : sr(i*17+5)*64+80;
    const xp=cx+dist*Math.cos(angle);
    const yp=cy+dist*Math.sin(angle);
    const xc=Math.max(8,Math.min(472,xp));
    const yc=Math.max(8,Math.min(352,yp));
    // arrow tail
    ctx.beginPath();ctx.moveTo(xc,yc);ctx.lineTo(xc,yc-22);
    ctx.strokeStyle=hit?'#6ee7b7':'#fca5a5';ctx.lineWidth=3;ctx.stroke();
    // arrowhead
    ctx.beginPath();ctx.arc(xc,yc,7,0,Math.PI*2);
    ctx.fillStyle=hit?'#34d399':'rgba(239,68,68,.85)';ctx.fill();
    ctx.strokeStyle=hit?'#059669':'#991b1b';ctx.lineWidth=2;ctx.stroke();
  }
}

function setArcR(ri){
  const n=+document.getElementById('ns2').value;
  const p=+document.getElementById('ps2').value/100;
  arcHl=ri;
  document.getElementById('fe2').innerHTML=
    `r = ${ri}번 명중 &nbsp;&nbsp; <sub>${n}</sub>C<sub>${ri}</sub> &times; ${p.toFixed(2)}<sup>${ri}</sup> &times; ${(1-p).toFixed(2)}<sup>${n-ri}</sup>`;
  document.getElementById('fa2').textContent=pct(BP(n,ri,p));
  const probs=[];for(let i=0;i<=n;i++)probs.push(BP(n,i,p));
  mkChart('ch2',probs,ri,setArcR);
  drawArc2();
}

function upd2(){
  const p=+document.getElementById('ps2').value/100;
  const n=+document.getElementById('ns2').value;
  document.getElementById('pv2').textContent=p.toFixed(2);
  document.getElementById('nv2').textContent=n;
  document.getElementById('pt2').textContent=
    `명중 확률이 ${p.toFixed(2)}인 선수가 ${n}발을 쏩니다. 각 경우의 확률 분포를 탐구해 보세요.`;
  const probs=[];for(let i=0;i<=n;i++)probs.push(BP(n,i,p));
  const mxR=probs.indexOf(Math.max(...probs));
  arcHl=mxR;
  document.getElementById('fe2').innerHTML=
    `r = ${mxR}번 명중 &nbsp;&nbsp; <sub>${n}</sub>C<sub>${mxR}</sub> &times; ${p.toFixed(2)}<sup>${mxR}</sup> &times; ${(1-p).toFixed(2)}<sup>${n-mxR}</sup>`;
  document.getElementById('fa2').textContent=pct(probs[mxR]);
  mkChart('ch2',probs,mxR,setArcR);
  drawArc2();
}

// ═══════════════════════════════════════════════
// TAB 3 : 날씨
// ═══════════════════════════════════════════════
const WK=['월','화','수','목','금','토','일'];

function upd3(){
  const p=+document.getElementById('ps3').value/100;
  const r=+document.getElementById('rs3').value;
  const n=7;
  document.getElementById('pv3').textContent=p.toFixed(2);
  document.getElementById('rv3').textContent=r;
  document.getElementById('pt3').textContent=
    `하루 비올 확률이 ${p.toFixed(2)}인 지역에서, 7일 중 정확히 ${r}일 비올 확률은?`;

  const wr=document.getElementById('wr3');wr.innerHTML='';
  for(let i=0;i<n;i++){
    const d=document.createElement('div');
    d.className='wday '+(i<r?'rain':'sun');
    d.innerHTML=`<span class="wi">${i<r?'🌧️':'☀️'}</span><span>${WK[i]}</span>`;
    wr.appendChild(d);
  }

  const prob=BP(n,r,p), cn=C(n,r);
  document.getElementById('fe3').innerHTML=
    `<sub>7</sub>C<sub>${r}</sub> &times; ${p.toFixed(2)}<sup>${r}</sup> &times; ${(1-p).toFixed(2)}<sup>${7-r}</sup>`;
  document.getElementById('fa3').textContent=
    `= ${cn} × ${Math.pow(p,r).toFixed(4)} × ${Math.pow(1-p,n-r).toFixed(4)}`;
  document.getElementById('fn3').textContent=`≈ ${pct(prob)}`;

  const probs=[];for(let i=0;i<=n;i++)probs.push(BP(n,i,p));
  mkChart('ch3',probs,r,(ri)=>{document.getElementById('rs3').value=ri;upd3();});
}

// ── Init ─────────────────────────────────────────────────────
upd0(); upd1(); upd2(); upd3();
</script>
</body>
</html>
"""


def render():
    st.header("🎯 독립시행, 실생활에서 찾기")
    st.caption("각 탭의 슬라이더를 움직여 독립시행 확률 공식을 탐구해 보세요.")
    components.html(_HTML, height=950)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
