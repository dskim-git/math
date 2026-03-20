import base64
import os

import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 성삼위일체 — 인물 사이의 실제 거리 추정",
    "description": "마사초의 「성삼위일체」 원작과 1점 투시도 분석 그림을 나란히 보며 자 도구로 직접 측정하고 실제 크기를 환산합니다.",
    "order": 37,
    "hidden": True,
}

_TEMPLATE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{background:#0f172a;color:#e2e8f0;font-family:'Segoe UI','Noto Sans KR',system-ui,sans-serif;font-size:13px;line-height:1.5;}
#app{max-width:1500px;margin:0 auto;padding:10px 10px 24px;}

.page-title{font-size:0.95rem;font-weight:900;color:#f8fafc;margin-bottom:3px;}
.page-sub{font-size:0.72rem;color:#64748b;margin-bottom:10px;}

/* ── two-column ── */
.two-col{display:flex;gap:10px;align-items:flex-start;overflow-x:auto;}
@media(max-width:640px){.two-col{flex-direction:column;}}

/* ── panel ── */
.cvs-panel{flex:1;min-width:0;background:#1e293b;border:1px solid #334155;border-radius:10px;overflow:hidden;}
.cvs-panel.left{flex:0 0 360px;}
.cvs-panel:not(.left){min-width:520px;flex:1;}
.panel-hd{font-size:0.68rem;font-weight:800;color:#94a3b8;letter-spacing:.04em;padding:5px 10px;background:#0f172a;border-bottom:1px solid #334155;}

/* ── toolbar ── */
.toolbar{background:#0f172a;border-bottom:1px solid #334155;padding:5px 8px;display:flex;align-items:center;gap:5px;flex-wrap:wrap;}
.tg{display:flex;align-items:center;gap:3px;}
.vsep{width:1px;height:18px;background:#334155;flex-shrink:0;}
.tb-btn{padding:3px 8px;border-radius:5px;border:1.5px solid #334155;background:#1e293b;color:#94a3b8;cursor:pointer;font-size:0.68rem;font-weight:700;white-space:nowrap;transition:all .15s;}
.tb-btn.active{background:#78350f;color:#fde68a;border-color:#f59e0b;}
.tb-btn.ruler-active{background:#1e3a5f;color:#bfdbfe;border-color:#3b82f6;}
.tb-btn.text-active{background:#1a1040;color:#c4b5fd;border-color:#a855f7;}
.tb-btn:hover:not(.active):not(.ruler-active):not(.text-active){border-color:#475569;color:#cbd5e1;}
.tl-lbl{font-size:0.63rem;color:#475569;white-space:nowrap;}
.cswatch{width:15px;height:15px;border-radius:3px;cursor:pointer;border:2px solid transparent;transition:all .1s;flex-shrink:0;}
.cswatch.on{border-color:#f8fafc;transform:scale(1.25);}
input[type=range]{width:50px;accent-color:#38bdf8;cursor:pointer;}
#thkL,#thkR{font-size:0.68rem;color:#fbbf24;font-weight:700;min-width:10px;}
.act-btn{padding:3px 7px;border-radius:4px;border:1.5px solid #334155;background:#0f172a;color:#94a3b8;cursor:pointer;font-size:0.68rem;font-weight:700;transition:all .15s;}
.act-btn:hover{border-color:#f43f5e;color:#fecdd3;}

/* ── ruler tip ── */
.ruler-tip{display:none;padding:4px 10px;background:#1e3a5f;border-bottom:1px solid #334155;font-size:0.68rem;color:#93c5fd;}
.ruler-tip b{color:#bfdbfe;}
.rc-row{display:flex;align-items:center;gap:4px;margin-top:3px;flex-wrap:wrap;}
.rswatch{width:15px;height:15px;border-radius:3px;cursor:pointer;border:2px solid transparent;flex-shrink:0;transition:all .1s;}
.rswatch.on{border-color:#f8fafc;transform:scale(1.25);}

/* ── text tip ── */
.text-tip{display:none;padding:4px 10px;background:#1a1040;border-bottom:1px solid #334155;font-size:0.68rem;color:#c4b5fd;}
.text-tip .fs-row{display:flex;align-items:center;gap:6px;margin-top:3px;}
.fs-btn{padding:2px 8px;border-radius:4px;border:1px solid #6d28d9;background:#2e1065;color:#c4b5fd;cursor:pointer;font-size:0.67rem;font-weight:700;}
.fs-btn.on{background:#6d28d9;color:#ede9fe;}

/* ── canvas outer ── */
.cvs-outer{position:relative;background:#000;overflow-x:hidden;line-height:0;}
canvas{display:block;touch-action:none;}

/* ── text float input ── */
.text-float{position:absolute;background:rgba(0,0,0,0.8);border:1.5px dashed #a855f7;border-radius:4px;padding:2px 5px;font-size:18px;font-weight:700;color:#fbbf24;outline:none;width:80px;min-width:20px;z-index:20;display:none;}

/* ── lm bar ── */
.lm-bar{background:#0f172a;border-top:1px solid #1e3a5f;padding:4px 10px;display:flex;align-items:center;gap:6px;flex-wrap:wrap;}
.lm-lbl{font-size:0.66rem;color:#475569;}
.lm-val{font-size:0.85rem;font-weight:900;color:#fbbf24;min-width:60px;}
.lm-sub{font-size:0.63rem;color:#334155;}

/* ── converter ── */
.converter{background:#1e293b;border:1px solid #334155;border-radius:0 0 10px 10px;border-top:none;padding:10px 12px;}
.conv-title{font-size:0.78rem;font-weight:800;color:#7dd3fc;margin-bottom:6px;}
.conv-info{font-size:0.72rem;color:#64748b;margin-bottom:8px;}
.conv-grid{display:flex;flex-wrap:wrap;gap:6px;align-items:center;}
.conv-label{font-size:0.72rem;color:#94a3b8;white-space:nowrap;}
.conv-inp{width:80px;padding:4px 7px;border-radius:6px;border:1.5px solid #334155;background:#0f172a;color:#f8fafc;font-size:0.82rem;font-weight:700;text-align:center;outline:none;}
.conv-inp:focus{border-color:#3b82f6;}
.conv-unit{font-size:0.7rem;color:#475569;}
.conv-btn{padding:5px 13px;border-radius:7px;border:none;background:#0369a1;color:#e0f2fe;font-size:0.75rem;font-weight:800;cursor:pointer;}
.conv-btn:hover{background:#0284c7;}
.conv-auto{padding:4px 9px;border-radius:6px;border:1px solid #334155;background:#1e293b;color:#64748b;font-size:0.67rem;font-weight:700;cursor:pointer;}
.conv-auto:hover{border-color:#475569;color:#cbd5e1;}
.conv-result-box{background:#022c22;border:1.5px solid #14b8a6;border-radius:8px;padding:6px 12px;font-size:0.82rem;color:#34d399;}
.conv-result-box strong{font-size:1.1rem;color:#a7f3d0;}
.conv-formula{font-size:0.67rem;color:#334155;margin-top:6px;}
.conv-dir-row{display:flex;gap:6px;margin-bottom:8px;}
.conv-dir-btn{padding:4px 10px;border-radius:6px;border:1.5px solid #334155;background:#1e293b;color:#64748b;font-size:0.72rem;font-weight:700;cursor:pointer;}
.conv-dir-btn.active{background:#0c4a6e;color:#7dd3fc;border-color:#0369a1;}
</style>
</head>
<body>
<div id="app">

<div class="page-title">🖼 성삼위일체 — 원작 &amp; 분석 다이어그램</div>
<div class="page-sub">두 그림에서 자 도구로 직접 측정 · 선 그리기 · 텍스트 입력. 원본 그림 아래에서 실제 크기 환산.</div>

<div class="two-col">

  <!-- ══════════ LEFT: original painting ══════════ -->
  <div class="cvs-panel left">
    <div class="panel-hd">📷 원본 그림 — 성삼위일체 (317 cm × 667 cm)</div>

    <div class="toolbar" id="tbL">
      <div class="tg">
        <button class="tb-btn" id="btnLineL" onclick="setToolL('line')">📏 선</button>
        <button class="tb-btn ruler-active" id="btnRulerL" onclick="setToolL('ruler')">📐 자</button>
        <button class="tb-btn" id="btnFreeL" onclick="setToolL('free')">✏️</button>
        <button class="tb-btn text-active" id="btnTextL" onclick="setToolL('text')" style="background:#2e1065;color:#c4b5fd;border-color:#a855f7;">T 텍스트</button>
        <button class="tb-btn" id="btnEraserL" onclick="setToolL('eraser')">🧹</button>
      </div>
      <div class="vsep"></div>
      <div class="tg">
        <span class="tl-lbl">색</span>
        <div class="cswatch on" style="background:#ef4444" data-c="#ef4444" onclick="setColorL(this)"></div>
        <div class="cswatch" style="background:#facc15" data-c="#facc15" onclick="setColorL(this)"></div>
        <div class="cswatch" style="background:#4ade80" data-c="#4ade80" onclick="setColorL(this)"></div>
        <div class="cswatch" style="background:#38bdf8" data-c="#38bdf8" onclick="setColorL(this)"></div>
        <div class="cswatch" style="background:#c084fc" data-c="#c084fc" onclick="setColorL(this)"></div>
        <div class="cswatch" style="background:#f8fafc" data-c="#f8fafc" onclick="setColorL(this)"></div>
        <div class="cswatch" style="background:#fbbf24" data-c="#fbbf24" onclick="setColorL(this)"></div>
      </div>
      <div class="vsep"></div>
      <div class="tg">
        <span class="tl-lbl">두께</span>
        <input type="range" id="thkSliderL" min="1" max="10" value="2" oninput="SL.thick=+this.value;document.getElementById('thkL').textContent=SL.thick;">
        <span id="thkL">2</span>
      </div>
      <div class="vsep"></div>
      <div class="tg">
        <button class="act-btn" onclick="undoL()">↩</button>
        <button class="act-btn" onclick="clearL()">🗑</button>
      </div>
    </div>

    <div class="ruler-tip" id="rtL">
      📐 <b>자</b>: 드래그 배치, 끝점 드래그로 조정, 우클릭 삭제.
      <div class="rc-row">
        <span style="font-size:0.62rem;color:#64748b">자 색</span>
        <div class="rswatch on" style="background:#fbbf24" data-rc="#fbbf24" onclick="setRulerColorL(this)"></div>
        <div class="rswatch" style="background:#f8fafc" data-rc="#f8fafc" onclick="setRulerColorL(this)"></div>
        <div class="rswatch" style="background:#f43f5e" data-rc="#f43f5e" onclick="setRulerColorL(this)"></div>
        <div class="rswatch" style="background:#34d399" data-rc="#34d399" onclick="setRulerColorL(this)"></div>
        <div class="rswatch" style="background:#60a5fa" data-rc="#60a5fa" onclick="setRulerColorL(this)"></div>
        <div class="rswatch" style="background:#e879f9" data-rc="#e879f9" onclick="setRulerColorL(this)"></div>
      </div>
    </div>

    <div class="text-tip" id="ttL">
      T <b>텍스트</b>: 캔버스 위를 클릭한 뒤 입력 → Enter로 확정, Esc로 취소.
      <div class="fs-row">
        <span style="font-size:0.62rem;color:#64748b">글자 크기</span>
        <button class="fs-btn" onclick="SL.fontSize=14;setFsSel('L',14)">소</button>
        <button class="fs-btn on" onclick="SL.fontSize=22;setFsSel('L',22)">중</button>
        <button class="fs-btn" onclick="SL.fontSize=32;setFsSel('L',32)">대</button>
        <button class="fs-btn" onclick="SL.fontSize=44;setFsSel('L',44)">특대</button>
      </div>
    </div>

    <div class="cvs-outer" id="outerL">
      <canvas id="cvsL" style="cursor:crosshair;"></canvas>
      <input class="text-float" id="textFloatL" type="text">
    </div>

    <div class="lm-bar">
      <span class="lm-lbl">📐 최근 측정:</span>
      <span class="lm-val" id="lmL">— px</span>
      <span class="lm-sub">자 도구로 선분을 그으면 픽셀 수 표시</span>
    </div>
  </div>

  <!-- ══════════ RIGHT: analysis diagram ══════════ -->
  <div class="cvs-panel">
    <div class="panel-hd">🔬 1점 투시도 분석 다이어그램</div>

    <div class="toolbar" id="tbR">
      <div class="tg">
        <button class="tb-btn" id="btnLineR" onclick="setToolR('line')">📏 선</button>
        <button class="tb-btn ruler-active" id="btnRulerR" onclick="setToolR('ruler')">📐 자</button>
        <button class="tb-btn" id="btnFreeR" onclick="setToolR('free')">✏️</button>
        <button class="tb-btn text-active" id="btnTextR" onclick="setToolR('text')" style="background:#2e1065;color:#c4b5fd;border-color:#a855f7;">T 텍스트</button>
        <button class="tb-btn" id="btnEraserR" onclick="setToolR('eraser')">🧹</button>
      </div>
      <div class="vsep"></div>
      <div class="tg">
        <span class="tl-lbl">색</span>
        <div class="cswatch on" style="background:#ef4444" data-c="#ef4444" onclick="setColorR(this)"></div>
        <div class="cswatch" style="background:#facc15" data-c="#facc15" onclick="setColorR(this)"></div>
        <div class="cswatch" style="background:#4ade80" data-c="#4ade80" onclick="setColorR(this)"></div>
        <div class="cswatch" style="background:#38bdf8" data-c="#38bdf8" onclick="setColorR(this)"></div>
        <div class="cswatch" style="background:#c084fc" data-c="#c084fc" onclick="setColorR(this)"></div>
        <div class="cswatch" style="background:#f8fafc" data-c="#f8fafc" onclick="setColorR(this)"></div>
        <div class="cswatch" style="background:#fbbf24" data-c="#fbbf24" onclick="setColorR(this)"></div>
      </div>
      <div class="vsep"></div>
      <div class="tg">
        <span class="tl-lbl">두께</span>
        <input type="range" id="thkSliderR" min="1" max="10" value="2" oninput="SR.thick=+this.value;document.getElementById('thkR').textContent=SR.thick;">
        <span id="thkR">2</span>
      </div>
      <div class="vsep"></div>
      <div class="tg">
        <button class="act-btn" onclick="undoR()">↩</button>
        <button class="act-btn" onclick="clearR()">🗑</button>
      </div>
    </div>

    <div class="ruler-tip" id="rtR">
      📐 <b>자</b>: 드래그 배치, 끝점 드래그로 조정, 우클릭 삭제.
      <div class="rc-row">
        <span style="font-size:0.62rem;color:#64748b">자 색</span>
        <div class="rswatch on" style="background:#fbbf24" data-rc="#fbbf24" onclick="setRulerColorR(this)"></div>
        <div class="rswatch" style="background:#f8fafc" data-rc="#f8fafc" onclick="setRulerColorR(this)"></div>
        <div class="rswatch" style="background:#f43f5e" data-rc="#f43f5e" onclick="setRulerColorR(this)"></div>
        <div class="rswatch" style="background:#34d399" data-rc="#34d399" onclick="setRulerColorR(this)"></div>
        <div class="rswatch" style="background:#60a5fa" data-rc="#60a5fa" onclick="setRulerColorR(this)"></div>
        <div class="rswatch" style="background:#e879f9" data-rc="#e879f9" onclick="setRulerColorR(this)"></div>
      </div>
    </div>

    <div class="text-tip" id="ttR">
      T <b>텍스트</b>: 캔버스 위를 클릭한 뒤 입력 → Enter로 확정, Esc로 취소.
      <div class="fs-row">
        <span style="font-size:0.62rem;color:#64748b">글자 크기</span>
        <button class="fs-btn" onclick="SR.fontSize=14;setFsSel('R',14)">소</button>
        <button class="fs-btn on" onclick="SR.fontSize=22;setFsSel('R',22)">중</button>
        <button class="fs-btn" onclick="SR.fontSize=32;setFsSel('R',32)">대</button>
        <button class="fs-btn" onclick="SR.fontSize=44;setFsSel('R',44)">특대</button>
      </div>
    </div>

    <div class="cvs-outer" id="outerR">
      <canvas id="cvsR" style="cursor:crosshair;"></canvas>
      <input class="text-float" id="textFloatR" type="text">
    </div>

    <div class="lm-bar">
      <span class="lm-lbl">📐 최근 측정:</span>
      <span class="lm-val" id="lmR">— px</span>
      <span class="lm-sub">자 도구로 선분을 그으면 픽셀 수 표시</span>
    </div>

    <!-- ── CONVERTER ── -->
    <div class="converter">
      <div class="conv-title">📏 실제 크기 환산</div>
      <div class="conv-info">원본 작품: 가로 <b style="color:#60a5fa">317 cm</b> × 세로 <b style="color:#60a5fa">667 cm</b></div>
      <div class="conv-dir-row">
        <button class="conv-dir-btn active" id="btnDirW" onclick="setConvDir('w')">↔ 가로 기준</button>
        <button class="conv-dir-btn" id="btnDirH" onclick="setConvDir('h')">↕ 세로 기준</button>
      </div>
      <div class="conv-grid">
        <span class="conv-label">화면 속 그림 <span id="convDirLbl">가로</span></span>
        <input class="conv-inp" type="number" id="convW" placeholder="px">
        <span class="conv-unit">px</span>
        <button class="conv-auto" onclick="autoFillW()">↺ 자동</button>
        <div style="flex-basis:100%;height:0;"></div>
        <span class="conv-label">측정한 선분</span>
        <input class="conv-inp" type="number" id="convPx" placeholder="px">
        <span class="conv-unit">px</span>
        <button class="conv-auto" onclick="copyLastMeas()">← 최근 측정</button>
        <div style="flex-basis:100%;height:0;"></div>
        <button class="conv-btn" onclick="doConvert()">계산하기 →</button>
        <div class="conv-result-box" id="convResultBox" style="display:none">
          실제 길이: <strong id="convResult">—</strong> cm
        </div>
      </div>
      <div class="conv-formula" id="convFormula">공식: 실제 길이 = 측정값(px) × 317 ÷ 화면 그림 가로(px)</div>
    </div>
  </div>

</div><!-- two-col -->
</div><!-- app -->

<script>
(function(){
'use strict';

/* ══════════════════════════════════════════════════════
   Shared drawing utilities
══════════════════════════════════════════════════════ */
function d2(ax,ay,bx,by){return Math.sqrt((ax-bx)**2+(ay-by)**2);}
function dSeg(px,py,ax,ay,bx,by){
  const dx=bx-ax,dy=by-ay,l2=dx*dx+dy*dy;
  if(l2<1)return d2(px,py,ax,ay);
  const t=Math.max(0,Math.min(1,((px-ax)*dx+(py-ay)*dy)/l2));
  return d2(px,py,ax+t*dx,ay+t*dy);
}
function hitStroke(st,x,y){
  const r=Math.max(8,st.thick/2+5);
  if(st.type==='text'){const fs=st.fs||22;const w=st._w||(st.text.length*fs*0.58);return x>=st.x-4&&x<=st.x+w+8&&y>=st.y-4&&y<=st.y+fs+6;}
  if(!st.pts||st.pts.length<2) return false;
  if(st.type==='line'){const p=st.pts,last=p[p.length-1];return dSeg(x,y,p[0].x,p[0].y,last.x,last.y)<=r;}
  for(let i=1;i<st.pts.length;i++) if(dSeg(x,y,st.pts[i-1].x,st.pts[i-1].y,st.pts[i].x,st.pts[i].y)<=r) return true;
  return false;
}
function findHitStroke(arr,x,y){for(let i=arr.length-1;i>=0;i--) if(hitStroke(arr[i],x,y)) return i; return -1;}

function drawStroke(c,st){
  if(st.type==='text'){
    c.save();
    c.font=`bold ${st.fs||22}px "Noto Sans KR","Segoe UI",sans-serif`;
    c.fillStyle=st.color||'#fbbf24';
    c.textBaseline='top';
    // shadow for readability
    c.shadowColor='rgba(0,0,0,0.9)';c.shadowBlur=4;
    c.fillText(st.text,st.x,st.y);
    if(!st._w)st._w=c.measureText(st.text).width;
    c.restore();
    return;
  }
  if(!st.pts||st.pts.length<2)return;
  c.save();c.strokeStyle=st.color;c.lineWidth=st.thick;
  c.lineCap='round';c.lineJoin='round';c.beginPath();
  if(st.type==='line'){c.moveTo(st.pts[0].x,st.pts[0].y);c.lineTo(st.pts[st.pts.length-1].x,st.pts[st.pts.length-1].y);}
  else{c.moveTo(st.pts[0].x,st.pts[0].y);for(let i=1;i<st.pts.length;i++)c.lineTo(st.pts[i].x,st.pts[i].y);}
  c.stroke();c.restore();
}

function drawRuler(c,r,sel){
  const dx=r.x2-r.x1,dy=r.y2-r.y1,len=Math.sqrt(dx*dx+dy*dy);
  if(len<3)return;
  const ang=Math.atan2(dy,dx),col=r.color||'#fbbf24';
  c.save();c.translate(r.x1,r.y1);c.rotate(ang);
  c.shadowColor='rgba(0,0,0,0.85)';c.shadowBlur=5;c.lineCap='square';
  c.strokeStyle='rgba(0,0,0,0.7)';c.lineWidth=7;c.beginPath();c.moveTo(0,0);c.lineTo(len,0);c.stroke();
  c.strokeStyle=col;c.lineWidth=4;c.beginPath();c.moveTo(0,0);c.lineTo(len,0);c.stroke();
  [0,len].forEach(tx=>{
    c.strokeStyle='rgba(0,0,0,0.7)';c.lineWidth=5;c.beginPath();c.moveTo(tx,-11);c.lineTo(tx,11);c.stroke();
    c.strokeStyle=col;c.lineWidth=2.5;c.beginPath();c.moveTo(tx,-11);c.lineTo(tx,11);c.stroke();
  });
  c.shadowBlur=0;
  for(let t=0;t<=len;t+=20){
    const h=t%100===0?8:t%50===0?5:3;
    c.strokeStyle='rgba(0,0,0,0.6)';c.lineWidth=2;c.beginPath();c.moveTo(t,0);c.lineTo(t,h);c.stroke();
    c.strokeStyle=col;c.lineWidth=1.5;c.beginPath();c.moveTo(t,0);c.lineTo(t,h);c.stroke();
  }
  c.save();
  const flip=Math.abs(ang)>Math.PI/2;
  c.translate(len/2,0);if(flip)c.rotate(Math.PI);
  const lbl=Math.round(len)+' px';
  c.font='bold 13px "Segoe UI",sans-serif';const tw=c.measureText(lbl).width;
  c.fillStyle='rgba(0,0,0,0.85)';c.beginPath();c.roundRect(-tw/2-6,-29,tw+12,18,4);c.fill();
  c.fillStyle=col;c.textAlign='center';c.textBaseline='alphabetic';c.fillText(lbl,0,-14);
  c.restore();c.restore();
  [[r.x1,r.y1],[r.x2,r.y2]].forEach(([x,y])=>{
    c.beginPath();c.arc(x,y,7,0,Math.PI*2);c.fillStyle='rgba(0,0,0,0.6)';c.fill();
    c.beginPath();c.arc(x,y,5,0,Math.PI*2);c.fillStyle=sel?'#f97316':col;c.fill();
    c.beginPath();c.arc(x,y,5,0,Math.PI*2);c.strokeStyle='#f8fafc';c.lineWidth=1.5;c.stroke();
  });
}

/* ══════════════════════════════════════════════════════
   Canvas tool factory
══════════════════════════════════════════════════════ */
function makeCanvas(cvsId,outerId,lmId,floatId,side){
  const cvs=document.getElementById(cvsId);
  const ctx=cvs.getContext('2d');
  const outer=document.getElementById(outerId);
  const lmEl=document.getElementById(lmId);
  const floatInp=document.getElementById(floatId);

  const S={
    tool:'ruler',color:'#ef4444',thick:2,rulerColor:'#fbbf24',fontSize:22,
    drawing:false,sx:0,sy:0,freeStroke:null,
    strokes:[],rulers:[],rulerDrag:null,selectedRuler:-1,
    selectedText:-1,textDrag:null,
    bgImg:null,imgW:0,imgH:0,
  };
  let lastPx=null;
  let textPendingCvs=null; // canvas coords for pending text

  function pxC(e){
    const r=cvs.getBoundingClientRect(),sx=cvs.width/r.width,sy=cvs.height/r.height;
    const pt=e.touches?e.touches[0]:e;
    return{x:(pt.clientX-r.left)*sx,y:(pt.clientY-r.top)*sy};
  }
  function hitR(x,y){
    for(let i=S.rulers.length-1;i>=0;i--){
      const r=S.rulers[i];
      if(d2(x,y,r.x1,r.y1)<10)return{idx:i,ep:'1'};
      if(d2(x,y,r.x2,r.y2)<10)return{idx:i,ep:'2'};
      if(dSeg(x,y,r.x1,r.y1,r.x2,r.y2)<8)return{idx:i,ep:'b'};
    }
    return null;
  }
  function hitText(x,y){
    for(let i=S.strokes.length-1;i>=0;i--){
      const st=S.strokes[i];
      if(st.type!=='text')continue;
      const fs=st.fs||22;
      const w=st._w||(st.text.length*fs*0.58);
      if(x>=st.x-4&&x<=st.x+w+8&&y>=st.y-4&&y<=st.y+fs+6)return i;
    }
    return -1;
  }
  function redraw(preS,preR){
    ctx.clearRect(0,0,cvs.width,cvs.height);
    ctx.fillStyle='#0f172a';ctx.fillRect(0,0,cvs.width,cvs.height);
    if(S.bgImg)ctx.drawImage(S.bgImg,0,0,S.imgW,S.imgH);
    S.strokes.forEach((st,i)=>{
      drawStroke(ctx,st);
      if(st.type==='text'&&i===S.selectedText){
        const fs=st.fs||22;const w=st._w||(st.text.length*fs*0.58);
        ctx.save();ctx.strokeStyle='#a855f7';ctx.lineWidth=1.5;ctx.setLineDash([4,3]);
        ctx.strokeRect(st.x-3,st.y-3,w+6,fs+6);ctx.restore();
      }
    });
    if(preS){ctx.globalAlpha=0.72;drawStroke(ctx,preS);ctx.globalAlpha=1;}
    S.rulers.forEach((r,i)=>drawRuler(ctx,r,i===S.selectedRuler));
    if(preR){ctx.globalAlpha=0.8;drawRuler(ctx,preR,false);ctx.globalAlpha=1;}
    if(S.rulers.length){
      const r=S.rulers[S.rulers.length-1];
      lastPx=Math.round(d2(r.x1,r.y1,r.x2,r.y2));
      lmEl.textContent=lastPx+' px';
    }else{lastPx=null;lmEl.textContent='— px';}
  }

  // ── text float input ──
  function showTextFloat(cx,cy){
    // position the float input in CSS coords (relative to outer)
    const outerRect=outer.getBoundingClientRect();
    const cvsRect=cvs.getBoundingClientRect();
    const dispX=(cx/cvs.width)*cvsRect.width + (cvsRect.left-outerRect.left);
    const scrollTop=outer.scrollTop||0;
    const dispY=(cy/cvs.height)*cvsRect.height + (cvsRect.top-outerRect.top) + scrollTop;
    floatInp.style.left=dispX+'px';
    floatInp.style.top=dispY+'px';
    floatInp.style.fontSize=(S.fontSize)+'px';
    floatInp.style.color=S.color;
    floatInp.style.borderColor=S.color;
    floatInp.style.display='block';
    floatInp.value='';
    textPendingCvs={x:cx,y:cy};
    setTimeout(()=>floatInp.focus(),10);
  }
  function commitText(){
    const txt=floatInp.value.trim();
    floatInp.style.display='none';
    if(!txt||!textPendingCvs)return;
    S.strokes.push({type:'text',x:textPendingCvs.x,y:textPendingCvs.y,text:txt,color:S.color,fs:S.fontSize});
    textPendingCvs=null;
    redraw();
  }
  floatInp.addEventListener('keydown',e=>{
    if(e.key==='Enter'){e.preventDefault();commitText();}
    if(e.key==='Escape'){floatInp.style.display='none';textPendingCvs=null;}
  });
  floatInp.addEventListener('blur',()=>{
    if(floatInp.value.trim())commitText();
    else{floatInp.style.display='none';textPendingCvs=null;}
  });

  // ── pointer events ──
  cvs.addEventListener('pointerdown',e=>{
    e.preventDefault();
    const{x,y}=pxC(e);
    if(S.tool==='text'){
      const tidx=hitText(x,y);
      if(tidx>=0){
        S.selectedText=tidx;
        const st=S.strokes[tidx];
        S.textDrag={idx:tidx,ox:x,oy:y,tx0:st.x,ty0:st.y};
        cvs.setPointerCapture(e.pointerId);redraw();
      }else{S.selectedText=-1;showTextFloat(x,y);}
      return;
    }
    if(S.tool==='ruler'){
      const hit=hitR(x,y);
      if(hit){
        S.selectedRuler=hit.idx;
        const r=S.rulers[hit.idx];
        S.rulerDrag={ep:hit.ep,idx:hit.idx,ox:x,oy:y,ox1:r.x1,oy1:r.y1,ox2:r.x2,oy2:r.y2};
      }else{S.selectedRuler=-1;S.rulerDrag={ep:'new',x1:x,y1:y};}
      cvs.setPointerCapture(e.pointerId);redraw();return;
    }
    S.selectedRuler=-1;S.drawing=true;S.sx=x;S.sy=y;
    if(S.tool==='eraser'){
      // find closest stroke or ruler and remove
      if(S.rulers.length){
        const hit=hitR(x,y);
        if(hit){S.rulers.splice(hit.idx,1);if(S.selectedRuler>=hit.idx)S.selectedRuler--;S.drawing=false;redraw();return;}
      }
      const si=findHitStroke(S.strokes,x,y);
      if(si!==-1){S.strokes.splice(si,1);redraw();}
      S.drawing=false;return;
    }
    if(S.tool==='free'){S.freeStroke={type:'free',color:S.color,thick:S.thick,pts:[{x,y}]};S.strokes.push(S.freeStroke);}
    cvs.setPointerCapture(e.pointerId);
  });
  cvs.addEventListener('pointermove',e=>{
    const{x,y}=pxC(e);
    if(S.tool==='text'&&S.textDrag){
      const st=S.strokes[S.textDrag.idx];
      st.x=S.textDrag.tx0+(x-S.textDrag.ox);
      st.y=S.textDrag.ty0+(y-S.textDrag.oy);
      st._w=undefined; // invalidate width cache on move (position changed, not size)
      redraw();return;
    }
    if(S.tool==='ruler'){
      if(S.rulerDrag){
        const d=S.rulerDrag;
        if(d.ep==='new'){redraw(null,{x1:d.x1,y1:d.y1,x2:x,y2:y,color:S.rulerColor});}
        else{
          const r=S.rulers[d.idx],dx=x-d.ox,dy=y-d.oy;
          if(d.ep==='1'){r.x1=d.ox1+dx;r.y1=d.oy1+dy;}
          else if(d.ep==='2'){r.x2=d.ox2+dx;r.y2=d.oy2+dy;}
          else{r.x1=d.ox1+dx;r.y1=d.oy1+dy;r.x2=d.ox2+dx;r.y2=d.oy2+dy;}
          redraw();
        }
      }else{
        const hit=hitR(x,y);
        cvs.style.cursor=hit?(hit.ep==='1'||hit.ep==='2'?'grab':'move'):'crosshair';
      }
      return;
    }
    if(!S.drawing)return;e.preventDefault();
    if(S.tool==='line')redraw({type:'line',color:S.color,thick:S.thick,pts:[{x:S.sx,y:S.sy},{x,y}]});
    else if(S.tool==='free'&&S.freeStroke){S.freeStroke.pts.push({x,y});redraw();}
  });
  cvs.addEventListener('pointerup',e=>{
    const{x,y}=pxC(e);
    if(S.tool==='text'&&S.textDrag){S.textDrag=null;return;}
    if(S.tool==='ruler'){
      if(S.rulerDrag){
        const d=S.rulerDrag;
        if(d.ep==='new'&&d2(d.x1,d.y1,x,y)>8)S.rulers.push({x1:d.x1,y1:d.y1,x2:x,y2:y,color:S.rulerColor});
        S.rulerDrag=null;redraw();
      }
      return;
    }
    if(!S.drawing)return;S.drawing=false;
    if(S.tool==='line'){
      const ddx=x-S.sx,ddy=y-S.sy;
      if(ddx*ddx+ddy*ddy>25)S.strokes.push({type:'line',color:S.color,thick:S.thick,pts:[{x:S.sx,y:S.sy},{x,y}]});
      redraw();
    }
    S.freeStroke=null;
  });
  cvs.addEventListener('pointerleave',()=>{if(S.drawing&&S.tool==='line'){S.drawing=false;redraw();}});
  cvs.addEventListener('contextmenu',e=>{
    e.preventDefault();const{x,y}=pxC(e);const hit=hitR(x,y);
    if(hit){S.rulers.splice(hit.idx,1);if(S.selectedRuler>=0&&S.selectedRuler>=hit.idx)S.selectedRuler--;redraw();}
  });

  // ── load image ──
  function loadImg(b64,mime){
    const img=new Image();
    img.onload=()=>{
      S.bgImg=img;
      const w=outer.clientWidth||400;
      S.imgW=w;S.imgH=Math.round(w*img.naturalHeight/img.naturalWidth);
      cvs.width=w;cvs.height=S.imgH;
      cvs.style.width=w+'px';cvs.style.height=S.imgH+'px';
      redraw();
    };
    img.src=`data:${mime};base64,${b64}`;
  }

  // ── resize observer ──
  new ResizeObserver(()=>{
    if(!S.bgImg)return;
    const nw=outer.clientWidth;if(!nw||nw===S.imgW)return;
    const sc=nw/S.imgW;
    S.rulers.forEach(r=>{r.x1*=sc;r.y1*=sc;r.x2*=sc;r.y2*=sc;});
    S.strokes.forEach(st=>{
      if(st.pts)st.pts.forEach(p=>{p.x*=sc;p.y*=sc;});
      if(st.type==='text'){st.x*=sc;st.y*=sc;st.fs=Math.round((st.fs||22)*sc);st._w=undefined;}
    });
    S.imgW=nw;S.imgH=Math.round(S.bgImg.naturalHeight*nw/S.bgImg.naturalWidth);
    cvs.width=nw;cvs.height=S.imgH;
    cvs.style.width=nw+'px';cvs.style.height=S.imgH+'px';
    redraw();
  }).observe(outer);

  return{
    S,cvs,outer,
    loadImg,redraw,
    getLastPx:()=>lastPx,
    getImgW:()=>S.imgW,
    getImgH:()=>S.imgH,
    undo(){
      if(S.tool==='ruler'&&S.rulers.length){S.rulers.pop();S.selectedRuler=-1;}
      else if(S.strokes.length)S.strokes.pop();
      redraw();
    },
    clear(){S.strokes=[];S.rulers=[];S.selectedRuler=-1;redraw();},
  };
}

/* ══════════════════════════════════════════════════════
   Instantiate two canvases
══════════════════════════════════════════════════════ */
const CL=makeCanvas('cvsL','outerL','lmL','textFloatL','L');
const CR=makeCanvas('cvsR','outerR','lmR','textFloatR','R');
const SL=CL.S, SR=CR.S;

/* ── Tool wiring ── */
function updateToolBtns(side){
  const S=side==='L'?SL:SR;
  const pfx='btn'+side;
  const ids={line:pfx+'LineL'||pfx+'Line',ruler:pfx+'Ruler',free:pfx+'Free',text:pfx+'Text',eraser:pfx+'Eraser'};
  // reset all
  ['Line','Ruler','Free','Text','Eraser'].forEach(t=>{
    const el=document.getElementById('btn'+t+side);
    if(!el)return;
    el.classList.remove('active','ruler-active','text-active');
    // restore default styling
    if(t==='Ruler'&&S.tool==='ruler'){el.classList.add('ruler-active');}
    else if(t==='Text'&&S.tool==='text'){el.classList.add('text-active');}
    else if(S.tool===t.toLowerCase()){el.classList.add('active');}
  });
  document.getElementById('rt'+side).style.display=S.tool==='ruler'?'block':'none';
  document.getElementById('tt'+side).style.display=S.tool==='text'?'block':'none';
  const cursor=S.tool==='eraser'?'cell':'crosshair';
  document.getElementById('cvs'+side).style.cursor=cursor;
}
window.setToolL=t=>{SL.tool=t;updateToolBtns('L');};
window.setToolR=t=>{SR.tool=t;updateToolBtns('R');};
window.setColorL=el=>{document.querySelectorAll('#tbL .cswatch').forEach(s=>s.classList.remove('on'));el.classList.add('on');SL.color=el.dataset.c;};
window.setColorR=el=>{document.querySelectorAll('#tbR .cswatch').forEach(s=>s.classList.remove('on'));el.classList.add('on');SR.color=el.dataset.c;};
window.setRulerColorL=el=>{document.querySelectorAll('#rtL .rswatch').forEach(s=>s.classList.remove('on'));el.classList.add('on');SL.rulerColor=el.dataset.rc;if(SL.selectedRuler>=0){SL.rulers[SL.selectedRuler].color=SL.rulerColor;CL.redraw();}};
window.setRulerColorR=el=>{document.querySelectorAll('#rtR .rswatch').forEach(s=>s.classList.remove('on'));el.classList.add('on');SR.rulerColor=el.dataset.rc;if(SR.selectedRuler>=0){SR.rulers[SR.selectedRuler].color=SR.rulerColor;CR.redraw();}};
window.undoL=()=>CL.undo();
window.undoR=()=>CR.undo();
window.clearL=()=>CL.clear();
window.clearR=()=>CR.clear();
window.setFsSel=(side,sz)=>{
  document.querySelectorAll('#tt'+side+' .fs-btn').forEach(b=>b.classList.remove('on'));
  event.target.classList.add('on');
};

/* ── Initial tool button state ── */
updateToolBtns('L');
updateToolBtns('R');
// Set initial: ruler active for both
document.getElementById('btnRulerL').classList.add('ruler-active');
document.getElementById('btnRulerR').classList.add('ruler-active');
// Text buttons keep their purple style
document.getElementById('btnTextL').style.cssText='background:#2e1065;color:#c4b5fd;border:1.5px solid #a855f7;';
document.getElementById('btnTextR').style.cssText='background:#2e1065;color:#c4b5fd;border:1.5px solid #a855f7;';

/* ══════════════════════════════════════════════════════
   Load images
══════════════════════════════════════════════════════ */
CL.loadImg('PLACEHOLDER_TRINITY','image/jpeg');
CR.loadImg('PLACEHOLDER_DIAGRAM','image/jpeg');

/* ══════════════════════════════════════════════════════
   Converter
══════════════════════════════════════════════════════ */
let convDir='w';
window.setConvDir=function(dir){
  convDir=dir;
  document.getElementById('btnDirW').classList.toggle('active',dir==='w');
  document.getElementById('btnDirH').classList.toggle('active',dir==='h');
  document.getElementById('convDirLbl').textContent=dir==='w'?'가로':'세로';
  document.getElementById('convFormula').textContent=dir==='w'
    ?'공식: 실제 길이 = 측정값(px) × 317 ÷ 화면 그림 가로(px)'
    :'공식: 실제 길이 = 측정값(px) × 667 ÷ 화면 그림 세로(px)';
  document.getElementById('convW').value='';
  document.getElementById('convResultBox').style.display='none';
};
window.autoFillW=function(){
  const v=convDir==='w'?CL.getImgW():CL.getImgH();
  if(v)document.getElementById('convW').value=v;
};
window.copyLastMeas=function(){
  const px=CL.getLastPx()??CR.getLastPx();
  if(px===null){alert('자 도구로 먼저 측정해주세요.');return;}
  document.getElementById('convPx').value=px;
};
window.doConvert=function(){
  const W=parseFloat(document.getElementById('convW').value);
  const L=parseFloat(document.getElementById('convPx').value);
  const box=document.getElementById('convResultBox');
  const res=document.getElementById('convResult');
  if(!W||!L||W<=0||L<=0){box.style.display='block';box.style.borderColor='#ef4444';box.style.color='#fca5a5';res.textContent='입력값을 확인하세요';return;}
  const real=convDir==='w'?L*317/W:L*667/W;
  box.style.display='block';
  box.style.borderColor='#14b8a6';box.style.color='#34d399';
  res.textContent=real.toFixed(1);
};

// Auto-fill width after image loads (slight delay)
setTimeout(()=>{if(CL.getImgW())document.getElementById('convW').value=CL.getImgW();},800);

})();
</script>
</body>
</html>
"""


def _b64(fname: str) -> str:
    root = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "gifted_art")
    )
    with open(os.path.join(root, fname), "rb") as f:
        return base64.b64encode(f.read()).decode()


def render():
    st.header("🖼 성삼위일체 — 원작 & 분석 다이어그램")
    st.caption("두 그림에서 선 그리기 · 자 측정 · 텍스트 입력 | 원본 그림 아래 실제 크기 환산")

    try:
        trinity_b64 = _b64("trinity.jpg")
        diagram_b64 = _b64("trinity3D.jpg")
    except Exception as e:
        st.error(f"이미지 파일을 찾을 수 없습니다: {e}")
        return

    html = _TEMPLATE.replace("PLACEHOLDER_TRINITY", trinity_b64).replace("PLACEHOLDER_DIAGRAM", diagram_b64)
    components.html(html, height=1500, scrolling=True)
