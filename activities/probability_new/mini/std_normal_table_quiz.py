import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "표준정규분포표연습"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 — 표준정규분포표 활용**"},
    {
        "key": "어려운유형",
        "label": "🤔 어떤 유형의 문제(Z값→확률 또는 확률→Z값)가 더 어려웠나요? 왜 그랬는지 설명해 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "대칭성활용",
        "label": "⚖️ 표준정규분포의 대칭성(−z와 z의 관계)이 확률 계산에서 어떻게 활용되는지 예를 들어 설명해 보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "표읽기전략",
        "label": "🔍 표준정규분포표를 빠르고 정확하게 읽기 위해 사용한 나만의 전략이나 방법을 적어보세요.",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 새롭게 알게 된 점",
        "type": "text_area",
        "height": 90,
    },
    {
        "key": "느낀점",
        "label": "💬 느낀 점",
        "type": "text_area",
        "height": 90,
    },
]

META = {
    "title": "미니: 표준정규분포표 활용 퀴즈",
    "description": "표준정규분포표를 보며 Z값→확률, 확률→Z값을 직접 계산하는 인터랙티브 퀴즈",
    "order": 999999,
    "hidden": True,
}

_HTML = r"""<!doctype html>
<html><head><meta charset="utf-8"><style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0d1b2a 0%,#162032 50%,#0d1b2a 100%);min-height:100vh;padding:14px;color:#e2e8f0}

/* ── Nav ── */
.nav{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap}
.nbtn{padding:9px 16px;border-radius:12px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.04);cursor:pointer;font-size:13px;font-weight:600;color:#94a3b8;transition:all .2s;white-space:nowrap}
.nbtn.active{background:rgba(99,179,237,.2);color:#90cdf4;border-color:rgba(99,179,237,.35)}
.nbtn:hover:not(.active){background:rgba(255,255,255,.08);color:#e2e8f0}

/* ── Card ── */
.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.09);border-radius:18px;padding:18px 22px;margin-bottom:14px}
.card-title{font-size:14px;font-weight:700;color:#90cdf4;margin-bottom:12px;display:flex;align-items:center;gap:8px}

/* ── Page ── */
.page{display:none}.page.active{display:block}

/* ── Table ── */
.tbl-wrap{overflow-x:auto;border-radius:10px}

/* ── Ref details (collapsible table in quiz tabs) ── */
.ref-details{margin-bottom:14px;border-radius:14px;overflow:hidden;border:1px solid rgba(99,179,237,.2)}
.ref-details summary{padding:11px 18px;cursor:pointer;font-size:13px;font-weight:600;color:#90cdf4;background:rgba(99,179,237,.1);user-select:none;list-style:none;display:flex;align-items:center;gap:8px}
.ref-details summary::-webkit-details-marker{display:none}
.ref-details summary::before{content:'▶';font-size:10px;transition:transform .2s;display:inline-block}
.ref-details[open] summary::before{transform:rotate(90deg)}
.ref-details .inner{padding:12px;background:rgba(255,255,255,.03)}
table{border-collapse:collapse;font-size:11px;min-width:620px}
thead th{background:rgba(99,179,237,.18);color:#90cdf4;padding:5px 9px;border:1px solid rgba(255,255,255,.09);font-weight:700;position:sticky;top:0;z-index:2}
thead th:first-child{position:sticky;left:0;z-index:3}
tbody td{padding:4px 9px;border:1px solid rgba(255,255,255,.06);text-align:center;cursor:pointer;transition:background .12s;color:#cbd5e0;font-family:monospace;font-size:11px}
tbody td:hover{background:rgba(99,179,237,.22);color:#90cdf4}
tbody td.zh{background:rgba(99,179,237,.13);color:#90cdf4;font-weight:700;position:sticky;left:0;z-index:1}
tbody td.hr{background:rgba(99,179,237,.07)}
tbody td.hc{background:rgba(99,179,237,.07)}
tbody td.hcell{background:rgba(16,185,129,.38)!important;color:#fff!important;font-weight:700}

/* ── Search ── */
.srow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.zinput{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:10px;padding:7px 12px;color:#e2e8f0;font-size:14px;width:170px;outline:none;transition:border .2s}
.zinput:focus{border-color:rgba(99,179,237,.5)}
.zchip{background:rgba(99,179,237,.15);border:1px solid rgba(99,179,237,.3);border-radius:20px;padding:5px 14px;font-size:13px;color:#90cdf4;font-weight:600}
.chip-row{display:flex;gap:8px;flex-wrap:wrap}
.chip{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:8px;padding:5px 10px;font-size:12px;cursor:pointer;transition:all .2s;font-family:monospace;color:#94a3b8}
.chip:hover{background:rgba(99,179,237,.2);color:#90cdf4;border-color:rgba(99,179,237,.3)}

/* ── Formula box ── */
.fbox{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:12px;padding:12px 16px}
.frow{font-size:13px;line-height:2.1;color:#cbd5e0}
.fkey{color:#90cdf4;font-weight:700}

/* ── Quiz header ── */
.qhead{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;padding:12px 18px;background:rgba(255,255,255,.04);border-radius:14px;margin-bottom:14px}
.sbox{text-align:center}.snum{font-size:26px;font-weight:900}.slbl{font-size:10px;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:.04em;margin-top:2px}
.dots{display:flex;gap:6px;align-items:center}
.dot{width:11px;height:11px;border-radius:50%;background:rgba(255,255,255,.12);transition:background .3s}
.dot.ok{background:#10b981}.dot.ng{background:#ef4444}

/* ── Problem card ── */
.qcard{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:16px 18px;margin-bottom:12px}
.qnum{font-size:11px;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px}
.qformula{font-size:19px;color:#fbbf24;font-family:Georgia,serif;font-weight:700;margin-bottom:12px;line-height:1.4}
.arow{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.ainput{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.13);border-radius:10px;padding:7px 12px;color:#e2e8f0;font-size:14px;width:150px;outline:none;transition:border .2s;font-family:monospace}
.ainput:focus{border-color:rgba(99,179,237,.5)}
.ainput.ok{border-color:rgba(16,185,129,.6);background:rgba(16,185,129,.08)}
.ainput.ng{border-color:rgba(239,68,68,.5);background:rgba(239,68,68,.06)}
.btn{padding:7px 15px;border-radius:10px;border:none;cursor:pointer;font-size:13px;font-weight:600;transition:all .2s}
.bcheck{background:linear-gradient(135deg,#3b82f6,#1d4ed8);color:#fff}
.bcheck:hover{transform:translateY(-1px);box-shadow:0 4px 10px rgba(59,130,246,.35)}
.bhint{background:rgba(245,158,11,.15);color:#fbbf24;border:1px solid rgba(245,158,11,.25)}
.bhint:hover{background:rgba(245,158,11,.25)}
.bnew{background:linear-gradient(135deg,#10b981,#059669);color:#fff}
.bnew:hover{transform:translateY(-1px);box-shadow:0 4px 10px rgba(16,185,129,.35)}
.fb{margin-top:8px;padding:9px 13px;border-radius:10px;font-size:13px;line-height:1.7;display:none}
.fb.ok{background:rgba(16,185,129,.12);border:1px solid rgba(16,185,129,.25);color:#6ee7b7}
.fb.ng{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);color:#fca5a5}
.hbox{margin-top:8px;padding:9px 13px;border-radius:10px;font-size:13px;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.2);color:#fcd34d;display:none;line-height:1.6}
.final-banner{text-align:center;padding:14px;font-size:15px;font-weight:700;color:#fbbf24;border-radius:14px;background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.2);margin-top:12px}

@keyframes pop{0%{transform:scale(.85);opacity:0}60%{transform:scale(1.06)}100%{transform:scale(1);opacity:1}}
.pop{animation:pop .3s ease-out}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.2);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(99,179,237,.35);border-radius:3px}
</style></head>
<body>

<div class="nav">
  <button class="nbtn active" onclick="showPage(this,'tbl')">📋 표준정규분포표</button>
  <button class="nbtn" onclick="showPage(this,'z2p')">🔢 Z → 확률 퀴즈</button>
  <button class="nbtn" onclick="showPage(this,'p2z')">🎯 확률 → Z값 퀴즈</button>
</div>

<!-- ════════ PAGE 1: TABLE ════════ -->
<div id="pg-tbl" class="page active">
  <div class="card">
    <div class="card-title">📊 표준정규분포표 <span style="font-size:11px;color:#64748b;font-weight:400;margin-left:6px">p(0 ≤ Z ≤ z)</span></div>
    <p style="font-size:12px;color:#94a3b8;margin-bottom:10px">z값을 입력하거나 표의 셀을 클릭하면 해당 확률을 바로 확인할 수 있습니다.</p>
    <div class="srow">
      <input type="number" id="zIn" class="zinput" placeholder="z 입력 (예: 1.96)" step="0.01" min="0" max="3.09" oninput="searchZ(this.value)">
      <div id="zOut" class="zchip" style="display:none"></div>
    </div>
    <div class="tbl-wrap" id="tblWrap"></div>
  </div>
  <div class="card">
    <div class="card-title">⭐ 자주 사용하는 z값</div>
    <div class="chip-row" id="keyChips"></div>
  </div>
  <div class="card">
    <div class="card-title">📐 확률 계산 공식 정리</div>
    <div class="fbox">
      <div class="frow">📌 <span class="fkey">p(0 ≤ Z ≤ z)</span> &nbsp;→ 표에서 직접 읽기</div>
      <div class="frow">📌 <span class="fkey">p(Z ≤ z)</span> = 0.5 + p(0 ≤ Z ≤ z)</div>
      <div class="frow">📌 <span class="fkey">p(Z ≥ z)</span> = 0.5 − p(0 ≤ Z ≤ z) &nbsp;(z > 0)</div>
      <div class="frow">📌 <span class="fkey">p(−z ≤ Z ≤ 0)</span> = p(0 ≤ Z ≤ z) &nbsp;&nbsp;(대칭성 이용)</div>
      <div class="frow">📌 <span class="fkey">p(−z ≤ Z ≤ z)</span> = 2 × p(0 ≤ Z ≤ z)</div>
      <div class="frow">📌 <span class="fkey">p(a ≤ Z ≤ b)</span> = p(0 ≤ Z ≤ b) − p(0 ≤ Z ≤ a) &nbsp;(0 ≤ a ≤ b)</div>
      <div class="frow">📌 <span class="fkey">p(−a ≤ Z ≤ b)</span> = p(0 ≤ Z ≤ a) + p(0 ≤ Z ≤ b) &nbsp;(a, b > 0)</div>
    </div>
  </div>
</div>

<!-- ════════ PAGE 2: Z→P ════════ -->
<div id="pg-z2p" class="page">
  <details class="ref-details">
    <summary>📋 표준정규분포표 참고 (클릭하여 열기/닫기)</summary>
    <div class="inner"><div class="tbl-wrap" id="tblWrap2"></div></div>
  </details>
  <div class="qhead">
    <div style="display:flex;gap:16px;align-items:center">
      <div class="sbox"><div class="snum" id="z2p-ok" style="color:#10b981">0</div><div class="slbl">정답</div></div>
      <div style="color:#334155;font-size:20px">/</div>
      <div class="sbox"><div class="snum" id="z2p-tr" style="color:#90cdf4">0</div><div class="slbl">시도</div></div>
      <div class="dots" id="z2p-dots"></div>
    </div>
    <button class="btn bnew" onclick="loadZ2P()">🔀 새 문제 세트</button>
  </div>
  <div id="z2p-probs"></div>
</div>

<!-- ════════ PAGE 3: P→Z ════════ -->
<div id="pg-p2z" class="page">
  <details class="ref-details">
    <summary>📋 표준정규분포표 참고 (클릭하여 열기/닫기)</summary>
    <div class="inner"><div class="tbl-wrap" id="tblWrap3"></div></div>
  </details>
  <div class="qhead">
    <div style="display:flex;gap:16px;align-items:center">
      <div class="sbox"><div class="snum" id="p2z-ok" style="color:#10b981">0</div><div class="slbl">정답</div></div>
      <div style="color:#334155;font-size:20px">/</div>
      <div class="sbox"><div class="snum" id="p2z-tr" style="color:#90cdf4">0</div><div class="slbl">시도</div></div>
      <div class="dots" id="p2z-dots"></div>
    </div>
    <button class="btn bnew" onclick="loadP2Z()">🔀 새 문제 세트</button>
  </div>
  <div id="p2z-probs"></div>
</div>

<script>
// ── ERF approximation (Abramowitz & Stegun) ──────────────────────────
function erf(x){
  const s=x<0?-1:1; x=Math.abs(x);
  const t=1/(1+0.3275911*x);
  const y=1-(((((1.061405429*t-1.453152027)*t+1.421413741)*t-0.284496736)*t+0.254829592)*t)*Math.exp(-x*x);
  return s*y;
}
function p0z(z){ return z<0?-p0z(-z):erf(z/Math.sqrt(2))/2; }
function f4(v){ return (Math.round(v*10000)/10000).toFixed(4); }

// ── TABLE ────────────────────────────────────────────────────────────
const KEY_Z=[
  {z:1.00,lbl:'z=1.00'},
  {z:1.28,lbl:'z=1.28'},
  {z:1.50,lbl:'z=1.50'},
  {z:1.65,lbl:'z=1.65'},
  {z:1.96,lbl:'z=1.96 ★'},
  {z:2.00,lbl:'z=2.00 ★'},
  {z:2.33,lbl:'z=2.33'},
  {z:2.58,lbl:'z=2.58'},
  {z:3.00,lbl:'z=3.00'},
];

function buildTable(wrapId, interactive){
  const w=document.getElementById(wrapId);
  let h='<table><thead><tr><th style="min-width:42px">z</th>';
  for(let c=0;c<=9;c++) h+=`<th>.0${c}</th>`;
  h+='</tr></thead><tbody>';
  for(let r=0;r<=30;r++){
    const zr=(r/10).toFixed(1);
    h+=`<tr><td class="zh">${zr}</td>`;
    for(let c=0;c<=9;c++){
      const z=r/10+c/100;
      if(interactive){
        h+=`<td onclick="clickCell(${z.toFixed(2)})" data-r="${r}" data-c="${c}" data-z="${z.toFixed(2)}">${f4(p0z(z))}</td>`;
      } else {
        h+=`<td>${f4(p0z(z))}</td>`;
      }
    }
    h+='</tr>';
  }
  h+='</tbody></table>';
  w.innerHTML=h;
}

function doChip(z){
  document.getElementById('zIn').value=z;
  searchZ(z);
}

function clearHL(){
  document.querySelectorAll('#tblWrap td').forEach(td=>td.classList.remove('hr','hc','hcell'));
}
function hlCell(z){
  clearHL();
  const zr=Math.round(z*100)/100;
  const r=Math.round(Math.floor(zr*10+1e-9));
  const c=Math.round((zr-r/10)*100+1e-9);
  if(r<0||r>30||c<0||c>9) return;
  document.querySelectorAll('#tblWrap td[data-r]').forEach(td=>{
    const tr=parseInt(td.dataset.r), tc=parseInt(td.dataset.c);
    if(tr===r&&tc===c) td.classList.add('hcell');
    else if(tr===r) td.classList.add('hr');
    else if(tc===c) td.classList.add('hc');
  });
  const cell=document.querySelector(`#tblWrap td[data-z="${zr.toFixed(2)}"]`);
  if(cell) cell.scrollIntoView({block:'nearest',inline:'nearest'});
}
function searchZ(v){
  const z=parseFloat(v);
  const out=document.getElementById('zOut');
  if(isNaN(z)||z<0||z>3.09){out.style.display='none';clearHL();return;}
  out.style.display='inline-block';
  out.textContent=`p(0 ≤ Z ≤ ${z.toFixed(2)}) = ${f4(p0z(z))}`;
  hlCell(z);
}
function clickCell(z){
  document.getElementById('zIn').value=z;
  searchZ(z);
}

// ── PAGE SWITCH ───────────────────────────────────────────────────────
function showPage(btn,id){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nbtn').forEach(b=>b.classList.remove('active'));
  document.getElementById('pg-'+id).classList.add('active');
  btn.classList.add('active');
}

// ── QUIZ DATA ─────────────────────────────────────────────────────────
const Z2P=[
  {q:'p(0 ≤ Z ≤ 1.00)',ans:'0.3413',
   hint:'표에서 z = 1.0 행, 0.00 열의 값을 읽으세요.',
   sol:'표에서 z = 1.00 → <b>p = 0.3413</b>'},
  {q:'p(0 ≤ Z ≤ 1.50)',ans:'0.4332',
   hint:'표에서 z = 1.5 행, 0.00 열의 값을 읽으세요.',
   sol:'표에서 z = 1.50 → <b>p = 0.4332</b>'},
  {q:'p(0 ≤ Z ≤ 1.96)',ans:'0.4750',
   hint:'표에서 z = 1.9 행, 0.06 열의 값을 읽으세요.',
   sol:'표에서 z = 1.96 → <b>p = 0.4750</b>'},
  {q:'p(0 ≤ Z ≤ 2.00)',ans:'0.4772',
   hint:'표에서 z = 2.0 행, 0.00 열의 값을 읽으세요.',
   sol:'표에서 z = 2.00 → <b>p = 0.4772</b>'},
  {q:'p(0 ≤ Z ≤ 2.58)',ans:'0.4951',
   hint:'표에서 z = 2.5 행, 0.08 열의 값을 읽으세요.',
   sol:'표에서 z = 2.58 → <b>p = 0.4951</b>'},
  {q:'p(−1.00 ≤ Z ≤ 1.00)',ans:'0.6826',
   hint:'대칭성: p(−z ≤ Z ≤ z) = 2 × p(0 ≤ Z ≤ z)',
   sol:'2 × p(0≤Z≤1.00) = 2 × 0.3413 = <b>0.6826</b>'},
  {q:'p(−2.00 ≤ Z ≤ 2.00)',ans:'0.9544',
   hint:'대칭성: p(−z ≤ Z ≤ z) = 2 × p(0 ≤ Z ≤ z)',
   sol:'2 × p(0≤Z≤2.00) = 2 × 0.4772 = <b>0.9544</b>'},
  {q:'p(−1.96 ≤ Z ≤ 1.96)',ans:'0.9500',
   hint:'대칭성: p(−z ≤ Z ≤ z) = 2 × p(0 ≤ Z ≤ z)',
   sol:'2 × p(0≤Z≤1.96) = 2 × 0.4750 = <b>0.9500</b>'},
  {q:'p(Z ≥ 1.96)',ans:'0.0250',
   hint:'p(Z ≥ z) = 0.5 − p(0 ≤ Z ≤ z)',
   sol:'0.5 − 0.4750 = <b>0.0250</b>'},
  {q:'p(Z ≥ 1.50)',ans:'0.0668',
   hint:'p(Z ≥ z) = 0.5 − p(0 ≤ Z ≤ z)',
   sol:'0.5 − 0.4332 = <b>0.0668</b>'},
  {q:'p(Z ≥ 2.00)',ans:'0.0228',
   hint:'p(Z ≥ z) = 0.5 − p(0 ≤ Z ≤ z)',
   sol:'0.5 − 0.4772 = <b>0.0228</b>'},
  {q:'p(Z ≤ 2.00)',ans:'0.9772',
   hint:'p(Z ≤ z) = 0.5 + p(0 ≤ Z ≤ z)',
   sol:'0.5 + 0.4772 = <b>0.9772</b>'},
  {q:'p(Z ≤ 1.50)',ans:'0.9332',
   hint:'p(Z ≤ z) = 0.5 + p(0 ≤ Z ≤ z)',
   sol:'0.5 + 0.4332 = <b>0.9332</b>'},
  {q:'p(Z ≤ 1.96)',ans:'0.9750',
   hint:'p(Z ≤ z) = 0.5 + p(0 ≤ Z ≤ z)',
   sol:'0.5 + 0.4750 = <b>0.9750</b>'},
  {q:'p(1.00 ≤ Z ≤ 2.00)',ans:'0.1359',
   hint:'p(a ≤ Z ≤ b) = p(0≤Z≤b) − p(0≤Z≤a)',
   sol:'0.4772 − 0.3413 = <b>0.1359</b>'},
  {q:'p(1.50 ≤ Z ≤ 2.50)',ans:'0.0606',
   hint:'p(a ≤ Z ≤ b) = p(0≤Z≤b) − p(0≤Z≤a). z=2.50: p=0.4938',
   sol:'0.4938 − 0.4332 = <b>0.0606</b>'},
  {q:'p(−1.50 ≤ Z ≤ 0)',ans:'0.4332',
   hint:'대칭성: p(−z ≤ Z ≤ 0) = p(0 ≤ Z ≤ z)',
   sol:'p(0≤Z≤1.50) = <b>0.4332</b>'},
  {q:'p(−1.96 ≤ Z ≤ 1.50)',ans:'0.9082',
   hint:'p(−a ≤ Z ≤ b) = p(0≤Z≤a) + p(0≤Z≤b)  (a, b > 0)',
   sol:'0.4750 + 0.4332 = <b>0.9082</b>'},
  {q:'p(−2.00 ≤ Z ≤ 1.00)',ans:'0.8185',
   hint:'p(−a ≤ Z ≤ b) = p(0≤Z≤a) + p(0≤Z≤b)  (a, b > 0)',
   sol:'0.4772 + 0.3413 = <b>0.8185</b>'},
];

const P2Z=[
  {q:'p(0 ≤ Z ≤ <em>a</em>) = 0.3413일 때, <em>a</em>의 값은?',ans:'1.00',
   hint:'표에서 0.3413에 해당하는 z값을 찾으세요.',
   sol:'표에서 p = 0.3413 → <b>a = 1.00</b>'},
  {q:'p(0 ≤ Z ≤ <em>a</em>) = 0.4332일 때, <em>a</em>의 값은?',ans:'1.50',
   hint:'표에서 0.4332에 해당하는 z값을 찾으세요.',
   sol:'표에서 p = 0.4332 → <b>a = 1.50</b>'},
  {q:'p(0 ≤ Z ≤ <em>a</em>) = 0.4750일 때, <em>a</em>의 값은?',ans:'1.96',
   hint:'표에서 0.4750에 해당하는 z값을 찾으세요.',
   sol:'표에서 p = 0.4750 → <b>a = 1.96</b>'},
  {q:'p(0 ≤ Z ≤ <em>a</em>) = 0.4772일 때, <em>a</em>의 값은?',ans:'2.00',
   hint:'표에서 0.4772에 해당하는 z값을 찾으세요.',
   sol:'표에서 p = 0.4772 → <b>a = 2.00</b>'},
  {q:'p(−<em>a</em> ≤ Z ≤ <em>a</em>) = 0.6826일 때, <em>a</em>의 값은?',ans:'1.00',
   hint:'p(−a≤Z≤a) = 2×p(0≤Z≤a). 먼저 0.6826÷2를 구하세요.',
   sol:'p(0≤Z≤a) = 0.6826÷2 = 0.3413 → 표에서 <b>a = 1.00</b>'},
  {q:'p(−<em>a</em> ≤ Z ≤ <em>a</em>) = 0.9500일 때, <em>a</em>의 값은?',ans:'1.96',
   hint:'p(−a≤Z≤a) = 2×p(0≤Z≤a). 먼저 0.9500÷2를 구하세요.',
   sol:'p(0≤Z≤a) = 0.9500÷2 = 0.4750 → 표에서 <b>a = 1.96</b>'},
  {q:'p(−<em>a</em> ≤ Z ≤ <em>a</em>) = 0.9544일 때, <em>a</em>의 값은?',ans:'2.00',
   hint:'p(−a≤Z≤a) = 2×p(0≤Z≤a). 먼저 0.9544÷2를 구하세요.',
   sol:'p(0≤Z≤a) = 0.9544÷2 = 0.4772 → 표에서 <b>a = 2.00</b>'},
  {q:'p(Z ≥ <em>a</em>) = 0.0250일 때, <em>a</em>의 값은? (단, a > 0)',ans:'1.96',
   hint:'p(Z≥a) = 0.5 − p(0≤Z≤a)이므로, p(0≤Z≤a) = 0.5 − 0.0250을 먼저 계산하세요.',
   sol:'p(0≤Z≤a) = 0.5−0.0250 = 0.4750 → 표에서 <b>a = 1.96</b>'},
  {q:'p(Z ≥ <em>a</em>) = 0.0228일 때, <em>a</em>의 값은? (단, a > 0)',ans:'2.00',
   hint:'p(Z≥a) = 0.5 − p(0≤Z≤a)이므로, p(0≤Z≤a) = 0.5 − 0.0228을 먼저 계산하세요.',
   sol:'p(0≤Z≤a) = 0.5−0.0228 = 0.4772 → 표에서 <b>a = 2.00</b>'},
  {q:'p(Z ≥ <em>a</em>) = 0.0668일 때, <em>a</em>의 값은? (단, a > 0)',ans:'1.50',
   hint:'p(Z≥a) = 0.5 − p(0≤Z≤a)이므로, p(0≤Z≤a) = 0.5 − 0.0668을 먼저 계산하세요.',
   sol:'p(0≤Z≤a) = 0.5−0.0668 = 0.4332 → 표에서 <b>a = 1.50</b>'},
  {q:'p(Z ≤ <em>a</em>) = 0.9332일 때, <em>a</em>의 값은?',ans:'1.50',
   hint:'p(Z≤a) = 0.5 + p(0≤Z≤a). p(0≤Z≤a) = 0.9332 − 0.5를 구하세요.',
   sol:'p(0≤Z≤a) = 0.9332−0.5 = 0.4332 → 표에서 <b>a = 1.50</b>'},
  {q:'p(Z ≤ <em>a</em>) = 0.9750일 때, <em>a</em>의 값은?',ans:'1.96',
   hint:'p(Z≤a) = 0.5 + p(0≤Z≤a). p(0≤Z≤a) = 0.9750 − 0.5를 구하세요.',
   sol:'p(0≤Z≤a) = 0.9750−0.5 = 0.4750 → 표에서 <b>a = 1.96</b>'},
  {q:'p(Z ≤ <em>a</em>) = 0.9772일 때, <em>a</em>의 값은?',ans:'2.00',
   hint:'p(Z≤a) = 0.5 + p(0≤Z≤a). p(0≤Z≤a) = 0.9772 − 0.5를 구하세요.',
   sol:'p(0≤Z≤a) = 0.9772−0.5 = 0.4772 → 표에서 <b>a = 2.00</b>'},
];

// ── QUIZ ENGINE ───────────────────────────────────────────────────────
function shuffle(a){ return a.map(x=>({x,r:Math.random()})).sort((a,b)=>a.r-b.r).map(x=>x.x); }

let ST={
  z2p:{sel:[],tried:0,correct:0,status:[]},
  p2z:{sel:[],tried:0,correct:0,status:[]}
};

function renderDots(id,n,status){
  const el=document.getElementById(id);
  el.innerHTML='';
  for(let i=0;i<n;i++){
    const d=document.createElement('div');
    d.className='dot'+(status[i]==='ok'?' ok':(status[i]==='ng'?' ng':''));
    el.appendChild(d);
  }
}

function renderProblems(containerId,problems,pfx){
  const c=document.getElementById(containerId);
  c.innerHTML='';
  const note=document.createElement('p');
  note.style.cssText='font-size:12px;color:#64748b;margin-bottom:12px';
  note.textContent='※ 답은 소수점 포함하여 입력하세요. 예) 0.3413  또는  1.96';
  c.appendChild(note);
  problems.forEach((p,i)=>{
    const div=document.createElement('div');
    div.className='qcard'; div.id=`${pfx}-q${i}`;
    div.innerHTML=`
      <div class="qnum">문제 ${i+1}</div>
      <div class="qformula">${p.q} = ?</div>
      <div class="arow">
        <input type="text" class="ainput" id="${pfx}-a${i}" placeholder="답 입력"
               onkeydown="if(event.key==='Enter')checkAns('${pfx}',${i})">
        <button class="btn bcheck" onclick="checkAns('${pfx}',${i})">채점</button>
        <button class="btn bhint" onclick="toggleHint('${pfx}',${i})">💡 힌트</button>
      </div>
      <div class="hbox" id="${pfx}-h${i}">${p.hint}</div>
      <div class="fb" id="${pfx}-f${i}"></div>`;
    c.appendChild(div);
  });
}

function loadZ2P(){
  ST.z2p={sel:shuffle(Z2P).slice(0,5),tried:0,correct:0,status:Array(5).fill('')};
  document.getElementById('z2p-ok').textContent=0;
  document.getElementById('z2p-tr').textContent=0;
  renderDots('z2p-dots',5,ST.z2p.status);
  renderProblems('z2p-probs',ST.z2p.sel,'z2p');
}
function loadP2Z(){
  ST.p2z={sel:shuffle(P2Z).slice(0,5),tried:0,correct:0,status:Array(5).fill('')};
  document.getElementById('p2z-ok').textContent=0;
  document.getElementById('p2z-tr').textContent=0;
  renderDots('p2z-dots',5,ST.p2z.status);
  renderProblems('p2z-probs',ST.p2z.sel,'p2z');
}

function toggleHint(pfx,i){
  const h=document.getElementById(`${pfx}-h${i}`);
  h.style.display=(h.style.display==='block'?'none':'block');
}

function checkAns(pfx,i){
  const st=pfx==='z2p'?ST.z2p:ST.p2z;
  if(st.status[i]!=='') return;
  const prob=st.sel[i];
  const inp=document.getElementById(`${pfx}-a${i}`);
  const fb=document.getElementById(`${pfx}-f${i}`);
  const user=inp.value.trim().replace(/,/g,'');
  if(!user){inp.focus();return;}
  const isOk=Math.abs(parseFloat(user)-parseFloat(prob.ans))<1e-9;
  st.tried++;
  if(isOk){
    st.correct++;st.status[i]='ok';
    inp.classList.add('ok');
    fb.className='fb ok pop';
    fb.innerHTML=`✅ 정답! &nbsp; ${prob.sol}`;
  } else {
    st.status[i]='ng';
    inp.classList.add('ng');
    fb.className='fb ng pop';
    fb.innerHTML=`❌ 틀렸어요. 정답: <b>${prob.ans}</b><br>${prob.sol}`;
  }
  fb.style.display='block';
  inp.disabled=true;
  document.getElementById(`${pfx}-ok`).textContent=st.correct;
  document.getElementById(`${pfx}-tr`).textContent=st.tried;
  renderDots(`${pfx}-dots`,5,st.status);
  if(st.tried===5){
    const msgs=['🎉 완벽! 5문제 전부 정답!','👏 훌륭해요! 4개 정답!','📚 절반 이상! 다시 도전해보세요.','📖 조금 더 연습이 필요해요.','📖 다시 공식을 살펴봐요!'];
    const idx=5-st.correct;
    const banner=document.createElement('div');
    banner.className='final-banner pop';
    banner.textContent=idx===0?msgs[0]:idx===1?msgs[1]:idx<=2?msgs[2]:idx<=3?msgs[3]:msgs[4];
    document.getElementById(`${pfx}-probs`).appendChild(banner);
    banner.scrollIntoView({behavior:'smooth',block:'nearest'});
  }
}

// ── INIT ──────────────────────────────────────────────────────────────
buildTable('tblWrap', true);
// build key chips after tblWrap is ready
(()=>{const cr=document.getElementById('keyChips');cr.innerHTML=KEY_Z.map(k=>`<span class="chip" onclick="doChip(${k.z})">${k.lbl} : p = ${f4(p0z(k.z))}</span>`).join('');})();
buildTable('tblWrap2', false);
buildTable('tblWrap3', false);
loadZ2P();
loadP2Z();
</script>
</body></html>"""


def render():
    st.header("📊 표준정규분포표 활용 연습")
    st.markdown(
        """
        표준정규분포 $Z \\sim N(0, 1)$ 에서 $p(0 \\le Z \\le z)$ 값을 담은 표를 활용하여
        다양한 범위의 **확률 계산**과 **역방향 추론(확률 → Z값)** 을 직접 연습해 보세요.
        """
    )
    components.html(_HTML, height=1800)

    # ── 성찰 기록 폼 ──────────────────────────────────────────────────────
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
