# activities/common/mini/gelosia_div.py
"""갤로시아 나눗셈 (Gelosia Division) 탐구"""
import datetime
import streamlit as st
import streamlit.components.v1 as components
import requests

_GAS_URL    = "https://script.google.com/macros/s/AKfycbySLDnSYGfQmqrtpuMyIju5hiEf7Lesp6bnWzplm3oZD4WHXESl1XJmsXT_EVcKOJI/exec"
_SHEET_NAME = "갤로시아나눗셈"

META = {
    "title":       "➗ 갤로시아 나눗셈 탐구",
    "description": "격자(갤로시아) 방식으로 다항식 나눗셈의 몫과 나머지를 직접 구하는 활동",
    "order":       32,
    "hidden":      True,
}

_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>갤로시아 나눗셈 탐구</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#e2e8f0;
     padding:14px 10px;min-height:600px}
.card{background:#161e2e;border:1px solid #1e293b;border-radius:14px;padding:18px 20px;margin-bottom:14px}
.card-title{font-size:15px;font-weight:800;color:#a78bfa;margin-bottom:10px}
.hint-box{background:#1a0e2a;border:1px solid #6d28d9;border-radius:10px;
          padding:12px 16px;margin-bottom:12px;font-size:13px;color:#ddd6fe;line-height:1.9}
.prob-selector{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:14px}
.prob-btn{padding:7px 16px;border-radius:8px;border:2px solid #1e293b;background:#141c2b;
          color:#7a8ea8;cursor:pointer;font-size:12.5px;font-weight:700;transition:all .2s}
.prob-btn.active{background:#2e1065;border-color:#7c3aed;color:#c4b5fd}
.prob-btn.solved{border-color:#0ea5e9;background:#0c2a3e;color:#7dd3fc}

/* ── 갤로시아 나눗셈 격자 ── */
/* 전체 레이아웃:
   [왼쪽 레이블] [격자] [오른쪽 레이블]
   위쪽에 몫 레이블(초록), 아래에 합산 레이블
*/
.gdiv-wrap{margin:10px 0;overflow-x:auto}
.gdiv-layout{display:inline-flex;flex-direction:column;align-items:flex-start;gap:0}

/* 위쪽: 왼쪽공백 + 몫레이블들 */
.gdiv-top-row{display:flex;align-items:flex-end;padding-bottom:4px}
.gdiv-top-spacer{display:inline-block} /* 왼쪽 레이블 너비만큼 */
.gdiv-quot-lbl{text-align:center;font-size:16px;font-weight:800;color:#4ade80}

/* 중간: 왼쪽레이블 + 격자 + 오른쪽레이블 */
.gdiv-mid-row{display:flex;align-items:stretch}
.gdiv-left-labels{display:flex;flex-direction:column;justify-content:space-around;
                   align-items:flex-end;padding-right:8px}
.gdiv-ll{font-size:16px;font-weight:800;color:#7dd3fc}
.gdiv-right-labels{display:flex;flex-direction:column;justify-content:space-around;
                    align-items:flex-start;padding-left:8px}
.gdiv-rl{font-size:16px;font-weight:800;color:#7dd3fc}
.gdiv-grid{display:inline-grid;border:3px solid #3b82f6}

/* 각 셀 */
.gd-cell{position:relative;width:90px;height:72px;border:1px solid #3b82f6;
          overflow:hidden;background:#0a0e1a}
/* \ 방향 대각선: 왼쪽위→오른쪽아래 */
.gd-cell .diag-line{position:absolute;top:0;left:0;width:0;height:0;border-style:solid;
  border-width:0 0 72px 90px;
  border-color:transparent transparent transparent #1e293b;pointer-events:none}
/* 셀 값: 중앙 배치 (fixed 숫자, 학생이 채우는 input 모두) */
.gd-cell .cell-val{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-size:15px;font-weight:700;color:#e2e8f0;z-index:2;white-space:nowrap}
.gd-cell input.cell-inp{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:44px;height:30px;background:#0f172a;border:2px solid #334155;border-radius:5px;
  color:#e2e8f0;text-align:center;font-size:14px;font-weight:700;z-index:2;outline:none}
.gd-cell input.cell-inp.quot-inp{color:#4ade80;border-color:#166534}
.gd-cell input.cell-inp.rem-inp{color:#f97316;border-color:#7c2d12}
.gd-cell input.ok{border-color:#22c55e!important;background:#052e16!important}
.gd-cell input.ng{border-color:#ef4444!important;background:#2d0a0a!important}

/* 아래: 왼쪽공백 + 합산값들 */
.gdiv-bot-row{display:flex;align-items:flex-start;padding-top:4px}
.gdiv-bot-slot{text-align:center}
.gdiv-bot-lbl{font-size:16px;font-weight:800;color:#94a3b8}
.gdiv-bot-inp{width:48px;padding:5px 2px;border:2px solid #334155;border-radius:6px;
              background:#0f172a;color:#e2e8f0;font-size:14px;font-weight:700;
              text-align:center;outline:none;transition:.2s}
.gdiv-bot-inp:focus{border-color:#a78bfa}
.gdiv-bot-inp.ok{border-color:#22c55e!important;background:#052e16!important;color:#4ade80!important}
.gdiv-bot-inp.ng{border-color:#ef4444!important;background:#2d0a0a!important;color:#f87171!important}

/* 범례 */
.legend{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:14px;font-size:12.5px}
.legend-item{display:flex;align-items:center;gap:6px}
.legend-dot{width:12px;height:12px;border-radius:3px}

.check-btn{padding:10px 28px;border:none;border-radius:9px;background:#7c3aed;
           color:#fff;font-size:14px;font-weight:700;cursor:pointer;transition:.2s;margin-top:12px}
.check-btn:hover{background:#6d28d9}
.check-btn.all-ok{background:#1d4ed8}
.feedback{margin-top:8px;font-size:13px;font-weight:700;min-height:20px}
.feedback.ok{color:#4ade80}.feedback.ng{color:#f87171}
.prog-wrap{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.prog-track{flex:1;height:7px;background:#1e293b;border-radius:99px;overflow:hidden}
.prog-bar{height:100%;background:linear-gradient(90deg,#7c3aed,#0ea5e9);transition:width .4s;border-radius:99px}
.score-badge{background:#2e1065;color:#c4b5fd;border-radius:99px;padding:3px 12px;font-size:12px;font-weight:700}
.intro-box{background:#0f102a;border:1px solid #3730a3;border-radius:12px;padding:16px 18px;margin-bottom:16px}
.intro-box h3{font-size:14px;font-weight:700;color:#a78bfa;margin-bottom:8px}
.intro-box p,.intro-box li{font-size:13px;color:#c4b5fd;line-height:1.9}
.intro-box ul{padding-left:18px}
.hl-orange{color:#fb923c;font-weight:700}.hl-green{color:#4ade80;font-weight:700}
.hl-blue{color:#60a5fa;font-weight:700}.hl-yellow{color:#fbbf24;font-weight:700}
.hl-purple{color:#c4b5fd;font-weight:700}
.result-box{margin-top:12px;padding:14px;background:#0c0a20;border:1px solid #4c1d95;border-radius:10px;display:none}
.result-box p{font-size:13.5px;color:#ddd6fe;line-height:2}
@media(max-width:500px){
  .gd-cell{width:68px;height:58px}
  .gd-cell .diag-line{border-width:0 0 58px 68px}
  .gdiv-quot-lbl,.gdiv-bot-slot,.gdiv-bot-inp{width:68px}
  .gd-cell input.cell-inp{width:34px;height:24px;font-size:12px}
}
</style>
</head>
<body>

<div style="text-align:center;margin-bottom:16px">
  <div style="font-size:1.4rem;font-weight:800;color:#c4b5fd;margin-bottom:4px">
    ➗ 갤로시아 나눗셈 탐구
  </div>
  <div style="font-size:12.5px;color:#64748b">
    격자 방식으로 다항식 나눗셈의 몫과 나머지를 직접 구해보세요
  </div>
</div>

<div class="prog-wrap">
  <div class="prog-track"><div class="prog-bar" id="progBar" style="width:0%"></div></div>
  <div class="score-badge">해결 <span id="progTxt">0 / 0</span></div>
</div>

<div class="intro-box">
  <h3>🔹 갤로시아 나눗셈 격자 구조</h3>
  <p><strong>직사각형 크기:</strong>
    행 수 = 나누는 식의 차수 + 1,
    열 수 = 피제식의 항 수 (= 몫의 차수 + 나머지의 차수 + 2)</p>
  <ul>
    <li><span class="hl-yellow">피제식(나누려는 식)의 계수</span>를 직사각형의
        <strong>왼쪽 변·아랫쪽 변</strong>을 따라 반시계방향으로 배치합니다.
        (맨 위 행의 왼쪽은 비워둡니다)</li>
    <li><span class="hl-blue">오른쪽 변</span>: 나누는 식의 계수 B[0], B[1], …</li>
    <li><span class="hl-green">위쪽 레이블(초록)</span>: 몫의 계수 — 학생이 직접 구합니다.</li>
    <li>각 셀 [행 r][열 c] = B[r] × q[c]</li>
    <li>대각선(↘) 합 = 왼쪽·아랫쪽에 표시된 피제식의 각 항 계수</li>
    <li><span class="hl-orange">마지막 열(주황)</span>: 나머지 계수</li>
  </ul>
</div>

<div class="card">
  <div class="card-title">✏️ 문제 선택</div>
  <div class="prob-selector" id="polyProbSel"></div>
</div>

<div class="card" id="polyProbCard">
  <div class="card-title" id="polyProbTitle">문제</div>
  <div class="hint-box" id="polyHint"></div>

  <div class="legend">
    <div class="legend-item">
      <div class="legend-dot" style="background:#fbbf24"></div>
      <span style="color:#fbbf24">노랑(왼쪽·아래) = 피제식 계수 (주어진 값)</span>
    </div>
    <div class="legend-item">
      <div class="legend-dot" style="background:#7dd3fc"></div>
      <span style="color:#7dd3fc">파랑(오른쪽) = 나누는 식 계수 (주어진 값)</span>
    </div>
    <div class="legend-item">
      <div class="legend-dot" style="background:#4ade80"></div>
      <span style="color:#4ade80">초록(위) = 몫의 계수 (학생 입력)</span>
    </div>
    <div class="legend-item">
      <div class="legend-dot" style="background:#e2e8f0"></div>
      <span style="color:#94a3b8">흰색(격자) = B[r]×q[c] (학생 입력)</span>
    </div>
    <div class="legend-item">
      <div class="legend-dot" style="background:#f97316"></div>
      <span style="color:#f97316">주황(나머지 열) = 나머지 계수 (학생 입력)</span>
    </div>
  </div>

  <div id="polyGridWrap"></div>
  <button class="check-btn" id="polyCheckBtn" onclick="checkPoly()">✅ 채점하기</button>
  <div class="feedback" id="polyFeedback"></div>
  <div class="result-box" id="polyResult"><p id="polyResultText"></p></div>
</div>

<script>
// ──────────────────────────────────────────────
// 갤로시아 나눗셈 알고리즘
//
// A = 피제식 계수 [a0, a1, ..., an]  (최고차→상수)
// B = 나누는 식 계수 [b0, b1, ..., bm]  (최고차→상수)
//
// 격자: nRows = B.length (= 나누는 식 차수+1)
//        nCols = A.length (= 피제식 항 수)
//        quotLen = nCols - nRows  (몫 항 수)
//
// 레이블 배치 (반시계 방향):
//   왼쪽 변(위→아래): B[0], B[1], ..., B[nRows-1]
//   위쪽 레이블(좌→우): q[0], q[1], ..., q[quotLen-1]  (학생이 구함)
//   오른쪽 변 = 왼쪽 변과 동일 (표시 생략 또는 동일 표시)
//
// 셀 값:
//   cell[r][c] = B[r] * q[c]   (r=0..nRows-1, c=0..quotLen-1)
//   마지막 nRows-1 개 열은 나머지 열 → 셀값은 계산 불필요 (비워둠)
//
// 대각선 합산 검증:
//   대각선 d (0-indexed, ↘방향):
//     셀 [r][c]는 대각선 d = r + c 에 속함
//   각 대각선 d의 합 = A[d]  (피제식 계수)
//   d=0: cell[0][0] = B[0]*q[0] = A[0]  → q[0] = A[0]/B[0]
//   d=1: cell[0][1] + cell[1][0] = B[0]*q[1] + B[1]*q[0] = A[1]
//        → q[1] = (A[1] - B[1]*q[0]) / B[0]
//   d=c (일반): B[0]*q[c] = A[c] - Σ_{r=1}^{min(c,nRows-1)} B[r]*q[c-r]
//
// 아래 합산 = 각 열 c에 해당하는 대각선 합 표시
//   아래 합산[c] = Σ_{r=0}^{nRows-1} cell[r][c-...] = A[c+...] 관련값
//   실제로: 아래에 표시되는 값은 피제식의 계수 A[nRows-1], A[nRows], ..., A[nCols-1]
//           (격자 왼쪽 아래 모서리에서 시작하는 대각선 합산)
//   → 아래 합산 위치 c (0~nCols-1):
//       c에 해당하는 대각선(r+c=nRows-1+c) 중 격자 안에 있는 셀들의 합
//       단 간단하게: 아래 표시값[c] = A[nRows-1+c]  (검증용으로만 사용)
//
// ──────────────────────────────────────────────

function fmtN(v){
  const r=Math.round(v*1e9)/1e9, ri=Math.round(r);
  return Math.abs(r-ri)<1e-7 ? ri : parseFloat(r.toFixed(4));
}

function computeDivision(A, B){
  const nCols=A.length, nRows=B.length, quotLen=nCols-nRows+1;
  const q=new Array(nCols).fill(0);

  // 몫 계수 계산 (조립제법 방식)
  for(let c=0;c<quotLen;c++){
    let s=A[c];
    for(let r=1;r<nRows;r++){
      if(c-r>=0) s -= B[r]*q[c-r];
    }
    q[c]=fmtN(s/B[0]);
  }

  // 셀 값: cell[r][c] = B[r]*q[c]  (c < quotLen인 경우만)
  // 나머지 계수: 마지막 nRows열의 cell[0][c] 값
  const cells=[];
  for(let r=0;r<nRows;r++){
    const row=[];
    for(let c=0;c<nCols;c++){
      if(c<quotLen) row.push(fmtN(B[r]*q[c]));
      else row.push(null); // 나머지 열은 셀값 없음
    }
    cells.push(row);
  }

  // 나머지 계수 계산
  // 아래 합산(대각선 합) = A[c]에 해당하는 값
  // 나머지 열(c>=quotLen)에서:
  //   remCoeff[c-quotLen] = A[c] - Σ_{r=1}^{nRows-1} cells[r][c-r] (if c-r<quotLen)
  const remCoeffs=[];
  for(let c=quotLen;c<nCols;c++){
    let s=A[c];
    for(let r=1;r<nRows;r++){
      const cc=c-r;
      if(cc>=0 && cc<quotLen) s -= cells[r][cc];
    }
    remCoeffs.push(fmtN(s));
  }

  // 아래 합산 표시값: 격자 아래쪽에 나타나는 A 계수들
  // 각 열 c의 대각선 합(r+c=일정)에서 격자 맨 아래 행의 셀이 속하는 대각선
  // 실제로 아래 표시: 격자 왼쪽 아래 코너부터 오른쪽으로
  // 이미지에서: -3, 1, 4  = A[1], A[2], A[3]
  // → 아래 표시값[i] = A[nRows-1 + i]  (i=0..nCols-nRows = quotLen)
  // 즉 quotLen+1 개 (나머지 포함해서 A[nRows-1] .. A[nCols-1])
  // 아래 합산: A[nRows-1], A[nRows], ..., A[nCols-1] → quotLen개
  const diagSums=[];
  for(let i=0;i<quotLen;i++) diagSums.push(A[nRows-1+i]);

  return {q: q.slice(0,quotLen), cells, remCoeffs, diagSums, quotLen, nCols, nRows};
}

const POLY_PROBS = [
  {
    label:'① (2x³−3x²+x+4) ÷ (2x+3)',
    A:[2,-3,1,4], B:[2,3],
    dividendStr:'2x³ − 3x² + x + 4', divisorStr:'2x + 3',
    title:'(2x³ − 3x² + x + 4) ÷ (2x + 3)'
  },
  {
    label:'② (x³ − x² − 5x − 3) ÷ (x + 1)',
    A:[1,-1,-5,-3], B:[1,1],
    dividendStr:'x³ − x² − 5x − 3', divisorStr:'x + 1',
    title:'(x³ − x² − 5x − 3) ÷ (x + 1)'
  },
  {
    label:'③ (x³ − 5x + 6) ÷ (x − 2)',
    A:[1,0,-5,6], B:[1,-2],
    dividendStr:'x³ − 5x + 6', divisorStr:'x − 2',
    title:'(x³ − 5x + 6) ÷ (x − 2)'
  },
  {
    label:'④ (2x³ + x² − 5x + 3) ÷ (x − 1)',
    A:[2,1,-5,3], B:[1,-1],
    dividendStr:'2x³ + x² − 5x + 3', divisorStr:'x − 1',
    title:'(2x³ + x² − 5x + 3) ÷ (x − 1)'
  },
  {
    label:'⑤ (x³ + 2x² − 4x + 6) ÷ (x² + x − 2)',
    A:[1,2,-4,6], B:[1,1,-2],
    dividendStr:'x³ + 2x² − 4x + 6', divisorStr:'x² + x − 2',
    title:'(x³ + 2x² − 4x + 6) ÷ (x² + x − 2)'
  },
  {
    label:'⑥ (2x⁴ + x³ − 3x + 1) ÷ (2x − 1)',
    A:[2,1,0,-3,1], B:[2,-1],
    dividendStr:'2x⁴ + x³ − 3x + 1', divisorStr:'2x − 1',
    title:'(2x⁴ + x³ − 3x + 1) ÷ (2x − 1)'
  },
];

const solved=new Set();
let curProb=0;

function updateProgress(){
  const total=POLY_PROBS.length, done=solved.size;
  document.getElementById('progBar').style.width=(done/total*100)+'%';
  document.getElementById('progTxt').textContent=done+' / '+total;
}

function buildSel(){
  const sel=document.getElementById('polyProbSel'); sel.innerHTML='';
  POLY_PROBS.forEach((p,i)=>{
    const btn=document.createElement('button');
    btn.className='prob-btn'+(i===curProb?' active':'')+( solved.has(i)?' solved':'');
    btn.textContent=p.label+(solved.has(i)?' ✅':'');
    btn.onclick=()=>loadProb(i);
    sel.appendChild(btn);
  });
}

function fmtSign(v){
  if(v===0) return '0';
  return v>0 ? '+'+v : ''+v;
}

function loadProb(idx){
  curProb=idx; buildSel();
  const p=POLY_PROBS[idx];
  document.getElementById('polyProbTitle').textContent='✏️ '+p.title;
  const data=computeDivision(p.A, p.B);
  const {quotLen, nCols, nRows}=data;
  const remLen=nRows-1; // 나머지 차수 = 나누는 식 차수 - 1 (단 余항수)
  const diagCount=quotLen+1; // 아래 표시 개수

  document.getElementById('polyHint').innerHTML=
    '<strong>피제식:</strong> <span class="hl-yellow">'+p.dividendStr+'</span>'+
    ' &nbsp; <strong>나누는 식:</strong> <span class="hl-purple">'+p.divisorStr+'</span><br>'+
    '격자: <span class="hl-blue">'+nRows+'행 × '+nCols+'열</span>'+
    ' (행수=나누는 식 차수+1='+nRows+', 열수=피제식 항수='+nCols+')<br>'+
    '피제식 계수 <span class="hl-yellow">['+p.A.join(', ')+']</span>를 왼쪽·아래에 배치,'+
    ' 나누는 식 계수 <span class="hl-purple">['+p.B.join(', ')+']</span>는 오른쪽에 표시됩니다.<br>'+
    '<span class="hl-green">위쪽(초록)</span>: 몫의 계수 '+quotLen+'개를 직접 구하세요.'+
    ' <span class="hl-orange">마지막 '+(nRows-1)+'열(주황)</span>: 나머지 계수.<br>'+
    '각 <strong>셀 = B[행] × q[열]</strong>, 대각선(↘) 합 = 왼쪽·아래의 피제식 계수';

  renderGrid(p, data);
  document.getElementById('polyFeedback').textContent='';
  document.getElementById('polyFeedback').className='feedback';
  document.getElementById('polyResult').style.display='none';
  document.getElementById('polyCheckBtn').className='check-btn';
  document.getElementById('polyCheckBtn').disabled=false;
}

function renderGrid(p, data){
  const {q, cells, remCoeffs, diagSums, quotLen, nCols, nRows}=data;
  const CW=90; // cell width
  const LL=36; // left label width
  const RL=36; // right label width

  // ── 위 레이블(몫 + 나머지): 총 nCols개 슬롯
  // 위 레이블: quotLen개는 초록(몫), 나머지 nRows개는 빈칸
  let html='<div class="gdiv-wrap"><div class="gdiv-layout">';

  // 1. 위쪽 행: spacer + 몫/나머지 레이블
  html+='<div class="gdiv-top-row">';
  html+='<div class="gdiv-top-spacer" style="width:'+LL+'px"></div>';
  for(let c=0;c<nCols;c++){
    const isRem=c>=quotLen;
    html+='<div class="gdiv-quot-lbl" style="width:'+CW+'px;color:'+(isRem?'#f97316':'#4ade80')+'">';
    if(!isRem){
      // 몫: 학생이 입력
      html+='<input class="cell-inp quot-inp" style="width:48px;height:30px;top:auto;left:auto;position:static;transform:none;display:block;margin:0 auto"'+
            ' data-type="quot" data-col="'+c+'" data-ans="'+q[c]+'" type="number" placeholder="?">';
    } else {
      // 나머지: 마지막 nRows열 중 행0의 셀에 나머지가 들어감
      // → 여기서는 나머지 레이블 입력칸(행0 위에)은 두지 않고 셀 자체에서 처리
      html+='<span style="font-size:11px;color:#475569">나머지</span>';
    }
    html+='</div>';
  }
  html+='</div>'; // top-row

  // 2. 중간 행: 왼쪽레이블 + 격자 + 오른쪽레이블
  html+='<div class="gdiv-mid-row">';

  // 왼쪽 레이블: 피제식 계수를 반시계 방향으로 배치
  // row 0(맨 위): 비워둠
  // row r>0: A[nRows-1-r] (아래일수록 A[0], 위로 갈수록 A[1], ...)
  html+='<div class="gdiv-left-labels" style="width:'+LL+'px">';
  for(let r=0;r<nRows;r++){
    const leftVal = r===0 ? '' : p.A[nRows-1-r];
    html+='<div class="gdiv-ll" style="height:72px;line-height:72px;color:#fbbf24">'+leftVal+'</div>';
  }
  html+='</div>';

  // 격자
  html+='<div class="gdiv-grid" style="grid-template-columns:repeat('+nCols+','+CW+'px);grid-template-rows:repeat('+nRows+',72px)">';
  for(let r=0;r<nRows;r++){
    for(let c=0;c<nCols;c++){
      const isRem=c>=quotLen;
      html+='<div class="gd-cell'+(isRem?' rem-col':'')+'">';
      html+='<div class="diag-line"></div>';
      if(!isRem){
        // 몫 열: 셀값 = B[r]*q[c], 학생이 입력
        html+='<input class="cell-inp" data-type="cell" data-r="'+r+'" data-c="'+c+'" data-ans="'+cells[r][c]+'" type="number" placeholder="?">';
      } else {
        // 나머지 열: 행0에만 입력 (나머지 계수)
        if(r===0){
          const remIdx=c-quotLen;
          html+='<input class="cell-inp rem-inp" data-type="rem" data-c="'+remIdx+'" data-ans="'+remCoeffs[remIdx]+'" type="number" placeholder="?">';
        }
        // 나머지 열의 다른 행은 비어있음
      }
      html+='</div>';
    }
  }
  html+='</div>'; // grid

  // 오른쪽 레이블: B[0], B[1], ...
  html+='<div class="gdiv-right-labels" style="width:'+RL+'px">';
  for(let r=0;r<nRows;r++){
    html+='<div class="gdiv-rl" style="height:72px;line-height:72px">'+p.B[r]+'</div>';
  }
  html+='</div>';

  html+='</div>'; // mid-row

  // 3. 아래 합산 행: spacer + 합산값들
  // 아래에는 대각선 합산값 (= 피제식 계수) 입력칸
  // 위치: 격자 맨 왼쪽 아래 모서리를 기준으로 오른쪽으로 quotLen+1개
  // 즉 열 위치: 0 ~ quotLen (격자 위치와 동일하게 정렬)
  // 단 첫 번째 대각선 합은 격자 왼쪽 바깥에 배치 (col=-1 해당)
  // 이미지에서: -3(col0 왼쪽), 1(col1), 4(col2) = A[1], A[2], A[3]
  // → 아래 합산은 col -1, 0, 1, ..., nCols-nRows 위치에 배치
  // 구현: spacer(LL + 0*CW) + diagSums[0]부터

  // 아래 레이블: 피제식 계수 A[nRows-1..nCols-1] = diagSums (정적 표시)
  html+='<div class="gdiv-bot-row">';
  html+='<div style="width:'+LL+'px"></div>';
  for(let i=0;i<diagSums.length;i++){
    html+='<div class="gdiv-bot-slot" style="width:'+CW+'px">';
    html+='<div style="display:flex;justify-content:center">';
    html+='<div class="gdiv-bot-lbl" style="color:#fbbf24;font-size:16px;font-weight:800;padding:6px 0">'+diagSums[i]+'</div>';
    html+='</div></div>';
  }
  html+='</div>'; // bot-row

  html+='</div></div>'; // layout, wrap
  document.getElementById('polyGridWrap').innerHTML=html;
}

function checkPoly(){
  const allInps=document.querySelectorAll('#polyGridWrap input');
  let allOk=true, wrong=0;
  allInps.forEach(inp=>{
    const ans=parseFloat(inp.dataset.ans), val=parseFloat(inp.value);
    if(isNaN(val)||Math.abs(val-ans)>0.01){inp.classList.add('ng');inp.classList.remove('ok');allOk=false;wrong++;}
    else{inp.classList.add('ok');inp.classList.remove('ng');}
  });

  const p=POLY_PROBS[curProb];
  const data=computeDivision(p.A, p.B);

  function polyToStr(coeffs, startDeg){
    let s='';
    coeffs.forEach((c,i)=>{
      if(c===0) return;
      const deg=startDeg-i, ac=(Math.abs(c)===1&&deg>0)?'':''+Math.abs(c);
      const sign=c<0?'−':'+ ', xp=deg>1?'x<sup>'+deg+'</sup>':deg===1?'x':'';
      s+=sign+ac+xp+' ';
    });
    return s.replace(/^\+ /,'').trim()||'0';
  }

  const fb=document.getElementById('polyFeedback');
  if(allOk){
    fb.textContent='🎉 모두 정답입니다!'; fb.className='feedback ok';
    document.getElementById('polyCheckBtn').className='check-btn all-ok';
    document.getElementById('polyCheckBtn').disabled=true;
    document.getElementById('polyResult').style.display='block';
    const qs=polyToStr(data.q, data.q.length-1);
    const rs=polyToStr(data.remCoeffs, data.remCoeffs.length-1);
    document.getElementById('polyResultText').innerHTML=
      '몫: <strong style="color:#4ade80;font-size:16px">'+qs+'</strong><br>'+
      '나머지: <strong style="color:#f97316;font-size:16px">'+rs+'</strong><br>'+
      '갤로시아 격자 나눗셈 완성! ✅';
    solved.add(curProb); buildSel(); updateProgress();
  } else {
    fb.textContent='❌ 틀린 칸이 '+wrong+'개 있습니다. 다시 확인해보세요.';
    fb.className='feedback ng';
  }
}

window.onload=()=>{ buildSel(); loadProb(0); updateProgress(); };
</script>
</body>
</html>
"""


def render():
    st.title("➗ 갤로시아 나눗셈 탐구")
    st.markdown(
        "격자(갤로시아) 방식으로 **다항식 나눗셈**의 몫과 나머지를 "
        "단계적으로 구해보는 활동입니다."
    )
    components.html(_HTML, height=1600, scrolling=False)
    _render_reflection_form(_SHEET_NAME, _GAS_URL)


def _render_reflection_form(sheet_name: str, gas_url: str):
    st.divider()
    st.subheader("✍️ 활동 후 성찰 기록")
    st.caption("아래 질문에 답하고 **제출하기** 버튼을 눌러 선생님께 전달해 주세요.")

    with st.form(f"reflection_{sheet_name}", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            student_id = st.text_input("학번")
        with c2:
            name = st.text_input("이름")

        st.markdown("**📝 다항식 버전 나눗셈 한 문제를 직접 풀고 과정을 기록해보세요**")
        q_poly = st.text_area(
            "선택한 다항식 나눗셈 문제",
            placeholder="예) (2x³−3x²+x+4) ÷ (2x+3)",
            height=56
        )
        a_poly = st.text_input("격자를 채우고 얻은 몫 다항식과 나머지")

        st.markdown("**💬 갤로시아 나눗셈과 조립제법의 공통점·차이점을 적어보세요**")
        comparison = st.text_area("갤로시아 나눗셈 vs 조립제법 비교", height=90)
        new_learning = st.text_area("💡 이 활동을 통해 새롭게 알게 된 점", height=90)
        feeling = st.text_area("💬 이 활동을 하면서 느낀 점", height=80)

        submitted = st.form_submit_button("📤 제출하기", use_container_width=True, type="primary")

    if submitted:
        if not student_id or not name:
            st.warning("학번과 이름을 입력해주세요.")
        else:
            payload = {
                "sheet":          sheet_name,
                "timestamp":      datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "학번":           student_id,
                "이름":           name,
                "다항식문제":     q_poly,
                "다항식답":       a_poly,
                "비교분석":       comparison,
                "새롭게알게된점": new_learning,
                "느낀점":         feeling,
            }
            try:
                resp = requests.post(gas_url, json=payload, timeout=10)
                if resp.status_code == 200:
                    st.success(f"✅ {name}님의 기록이 제출되었습니다!")
                    st.balloons()
                else:
                    st.error(f"제출 중 오류가 발생했습니다. (상태코드: {resp.status_code})")
            except Exception as e:
                st.error(f"네트워크 오류: {e}")
