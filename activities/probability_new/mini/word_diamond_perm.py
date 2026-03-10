import streamlit as st
import streamlit.components.v1 as components
import requests
from reflection_utils import render_reflection_form
import datetime

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "단어다이아몬드순열"

_QUESTIONS = [
    {"type": 'markdown', "text": '**📝 이 활동으로 해결할 수 있는 문제 3개 (문제와 답 모두 작성)**'},
    {"key": '문제1', "label": '문제 1', "type": 'text_area', "height": 80},
    {"key": '답1', "label": '문제 1의 답', "type": 'text_input'},
    {"key": '문제2', "label": '문제 2', "type": 'text_area', "height": 80},
    {"key": '답2', "label": '문제 2의 답', "type": 'text_input'},
    {"key": '문제3', "label": '문제 3', "type": 'text_area', "height": 80},
    {"key": '답3', "label": '문제 3의 답', "type": 'text_input'},
    {"key": '새롭게알게된점', "label": '💡 이 활동을 통해 새롭게 알게 된 점', "type": 'text_area', "height": 100},
    {"key": '느낀점', "label": '💬 이 활동을 통해 느낀 점', "type": 'text_area', "height": 100},
]

META = {
    "title": "미니: 단어 다이아몬드와 같은 것이 있는 순열",
    "description": "홀수 글자 영어 단어를 다이아몬드 격자의 두 변에 배치하고, 위에서 아래로 이웃한 칸을 따라가며 단어를 읽는 경로의 수를 탐구합니다.",
    "order": 999999,
    "hidden": True,
}


def render():
    st.header("💎 단어 다이아몬드와 같은 것이 있는 순열")
    st.caption("홀수 글자 단어를 다이아몬드 격자 두 변에 배치하고, 위 꼭짓점에서 아래로 이웃한 칸을 하나씩 선택하여 원래 단어를 만드는 경우의 수를 탐구합니다.")

    components.html(_build_html(), height=1500, scrolling=True)
    _render_quiz()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


def _build_html() -> str:
    return r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[
    {left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}
  ],throwOnError:false})"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR',system-ui,sans-serif;background:linear-gradient(135deg,#06080f 0%,#0d1225 50%,#06080f 100%);min-height:100vh;padding:16px;color:#e2e8f0}

.card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:20px 24px;margin:14px 0;backdrop-filter:blur(10px);box-shadow:0 8px 32px rgba(0,0,0,.4)}
.card-title{font-size:15px;font-weight:700;color:#a78bfa;margin-bottom:14px;display:flex;align-items:center;gap:8px;letter-spacing:.02em}

/* ── INPUT ── */
.input-row{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.word-input{background:rgba(255,255,255,.07);border:2px solid rgba(167,139,250,.4);border-radius:14px;padding:12px 18px;font-size:22px;font-weight:700;font-family:'JetBrains Mono',monospace;color:#fff;letter-spacing:.12em;outline:none;width:300px;text-transform:uppercase;transition:.3s}
.word-input:focus{border-color:#a78bfa;box-shadow:0 0 0 4px rgba(167,139,250,.2)}
.gen-btn{background:linear-gradient(135deg,#7c3aed,#a78bfa);border:none;border-radius:14px;padding:13px 28px;font-size:15px;font-weight:700;color:#fff;cursor:pointer;transition:.2s;box-shadow:0 4px 20px rgba(124,58,237,.4)}
.gen-btn:hover{transform:translateY(-2px);box-shadow:0 6px 24px rgba(124,58,237,.6)}
.error-msg{color:#f87171;font-size:13px;font-weight:600;padding:8px 0;display:none}
.hint-tag{display:inline-block;background:rgba(251,191,36,.12);border:1px solid rgba(251,191,36,.3);border-radius:8px;padding:4px 12px;font-size:12px;color:#fbbf24;margin-top:8px}

/* ── DIAMOND SVG ── */
.diamond-wrap{overflow-x:auto;padding:10px 0;text-align:center}
svg.diamond{overflow:visible}
#pathDisplay{font-size:13px;color:#fde68a;font-family:'JetBrains Mono',monospace;font-weight:700;min-height:28px;margin-top:8px;letter-spacing:.08em;text-align:center}

/* ── PATH LEGEND ── */
.path-legend{display:flex;gap:20px;justify-content:center;margin:10px 0;flex-wrap:wrap}
.path-leg{display:flex;align-items:center;gap:8px;font-size:13px;color:#cbd5e1;font-weight:600}
.arrow-l{width:28px;height:18px;display:flex;align-items:center;justify-content:center;font-size:18px;color:#67e8f9}
.arrow-r{width:28px;height:18px;display:flex;align-items:center;justify-content:center;font-size:18px;color:#f472b6}

/* ── FORMULA ── */
.formula-box{background:rgba(124,58,237,.12);border:1px solid rgba(167,139,250,.3);border-radius:16px;padding:16px 22px;margin:14px 0;text-align:center}
.formula-main{font-size:26px;font-weight:900;color:#c4b5fd;margin-bottom:6px}
.formula-sub{font-size:13px;color:#94a3b8;line-height:1.8}
.kpi-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:14px;justify-content:center}
.kpi{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:12px 20px;text-align:center;min-width:110px}
.kpi .knum{font-size:30px;font-weight:900;color:#e2e8f0}
.kpi .klbl{font-size:11px;color:#94a3b8;margin-top:4px;font-weight:600;text-transform:uppercase;letter-spacing:.04em}

/* ── STEP ── */
.step-item{display:flex;gap:14px;margin-bottom:16px;align-items:flex-start}
.step-num{background:linear-gradient(135deg,#7c3aed,#a78bfa);border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:15px;flex-shrink:0;box-shadow:0 2px 12px rgba(124,58,237,.4);color:#fff}
.step-body{font-size:13px;color:#cbd5e1;line-height:1.8;flex:1}
.step-body strong{color:#a78bfa}
.hl{color:#fbbf24}
.hl2{color:#67e8f9}

/* ── PATH TABLE ── */
.ptable{width:100%;border-collapse:collapse;margin:10px 0;font-size:13px}
.ptable th{background:rgba(124,58,237,.25);color:#c4b5fd;padding:8px 12px;text-align:center;font-weight:700}
.ptable td{padding:7px 12px;text-align:center;border-bottom:1px solid rgba(255,255,255,.06);font-family:'JetBrains Mono',monospace;font-weight:600}
.ptable tr:hover td{background:rgba(167,139,250,.07)}

/* ── EXPLORE ── */
.all-paths-wrap{display:flex;flex-wrap:wrap;gap:6px;max-height:200px;overflow-y:auto;padding:8px 0}
.path-chip{background:rgba(255,255,255,.04);border:1px solid rgba(167,139,250,.2);border-radius:8px;padding:5px 10px;font-family:'JetBrains Mono',monospace;font-size:12px;cursor:pointer;transition:.2s;color:#c4b5fd}
.path-chip:hover{background:rgba(167,139,250,.18);border-color:#a78bfa;color:#fff}
.path-chip.active{background:linear-gradient(135deg,#7c3aed,#4f46e5);border-color:#a78bfa;color:#fff}

@media(max-width:500px){
  .word-input{width:220px;font-size:17px}
  .kpi .knum{font-size:22px}
  .formula-main{font-size:18px}
}
</style>
</head>
<body>

<!-- ══ 설명 카드 ══ -->
<div class="card">
  <div class="card-title">📖 활동 안내</div>
  <p style="font-size:13px;color:#cbd5e1;line-height:1.85;margin-bottom:10px">
    헝가리 수학자 <strong style="color:#a78bfa">폴리아(Pólya, 1887~1985)</strong>는 ABRACADABRA를 이용해 다음 문제를 냈습니다.<br>
    오른쪽 그림에서 가장 위에 있는 글자 <strong style="color:#fbbf24">A</strong>에서 시작하여
    아래로 내려가면서 <strong>바로 이웃한 글자를 하나씩 택하면</strong>
    <strong style="color:#67e8f9">ABRACADABRA</strong>라는 단어를 만들 수 있다.<br>
    이 단어를 만들 수 있는 경우의 수는 얼마인가?
  </p>
  <div style="background:rgba(103,232,249,.07);border:1px solid rgba(103,232,249,.2);border-radius:12px;padding:12px 16px;font-size:13px;color:#cbd5e1;line-height:1.8">
    🔑 <strong style="color:#67e8f9">핵심 아이디어</strong><br>
    단어 길이가 <strong>홀수 $n = 2k+1$</strong>일 때만 대칭 다이아몬드를 만들 수 있습니다.<br>
    왼쪽 변과 오른쪽 변 각각 $k$개의 칸에 단어 글자들이 배치되고,<br>
    맨 위 꼭짓점에서 맨 아래 꼭짓점까지 내려가는 동안
    매 단계에서 <span style="color:#67e8f9">왼쪽(↙)</span> 또는 <span style="color:#f472b6">오른쪽(↘)</span>을 선택합니다.<br>
    총 <strong style="color:#fbbf24">$2k$번</strong> 선택 중 정확히 <strong style="color:#67e8f9">$k$번 왼쪽</strong>,
    <strong style="color:#f472b6">$k$번 오른쪽</strong>을 선택해야 맨 아래에 도달하므로<br>
    경우의 수 = $\dfrac{(2k)!}{k! \times k!} = \binom{2k}{k}$
  </div>
</div>

<!-- ══ 입력 카드 ══ -->
<div class="card">
  <div class="card-title">⌨️ 탐구할 단어 입력</div>
  <p style="font-size:13px;color:#94a3b8;margin-bottom:12px;line-height:1.7">
    홀수 글자 영어 단어를 입력하세요. 짝수 글자 단어는 대칭 다이아몬드를 만들 수 없습니다.<br>
    <em style="color:#7dd3fc">예시: ABRACADABRA (11글자), LEVEL (5글자), RACECAR (7글자)</em>
  </p>
  <div class="input-row">
    <input class="word-input" id="wordInput" type="text" maxlength="21"
      placeholder="예) ABRACADABRA" value="ABRACADABRA" spellcheck="false" autocomplete="off">
    <button class="gen-btn" id="genBtn">💎 격자 생성</button>
  </div>
  <div class="error-msg" id="errMsg"></div>
  <div class="hint-tag" id="hintTag" style="display:none"></div>
</div>

<!-- ══ 다이아몬드 카드 ══ -->
<div class="card" id="diamondCard" style="display:none">
  <div class="card-title">💎 단어 다이아몬드 격자</div>
  <div class="path-legend">
    <div class="path-leg"><div class="arrow-l">↙</div> 왼쪽 이동</div>
    <div class="path-leg"><div class="arrow-r">↘</div> 오른쪽 이동</div>
  </div>
  <div class="diamond-wrap" id="diamondWrap"></div>
  <div id="pathDisplay"></div>
</div>

<!-- ══ 공식 카드 ══ -->
<div class="card" id="formulaCard" style="display:none">
  <div class="card-title">🔢 경우의 수 계산</div>
  <div class="formula-box">
    <div class="formula-main" id="formulaMain">—</div>
    <div class="formula-sub" id="formulaSub">—</div>
  </div>
  <div class="kpi-row" id="kpiRow"></div>
</div>

<!-- ══ 경로표 카드 ══ -->
<div class="card" id="pathTableCard" style="display:none">
  <div class="card-title">📊 선택 단계 분석표</div>
  <table class="ptable" id="ptable">
    <thead><tr><th>단계</th><th>선택</th><th>현재 위치의 글자</th><th>여기까지 경로 수</th></tr></thead>
    <tbody id="ptbody"></tbody>
  </table>
</div>

<!-- ══ 모든 경로 탐색 카드 ══ -->
<div class="card" id="exploreCard" style="display:none">
  <div class="card-title">🗺️ 모든 경로 탐색</div>
  <p style="font-size:12px;color:#94a3b8;margin-bottom:10px">경로 칩을 클릭하면 격자 위에서 해당 경로가 강조됩니다. (최대 252개까지 표시)</p>
  <div class="all-paths-wrap" id="allPathsWrap"></div>
</div>

<!-- ══ 풀이 단계 카드 ══ -->
<div class="card" id="explainCard" style="display:none">
  <div class="card-title">📖 풀이 단계</div>
  <div id="stepsContent"></div>
</div>

<script>
// ── BigInt 팩토리얼 ──
function factorial(n){let r=1n;for(let i=2n;i<=BigInt(n);i++)r*=i;return r;}
function C(n,k){if(k<0||k>n)return 0n;return factorial(n)/(factorial(k)*factorial(n-k));}
function fmt(big){return String(big).replace(/\B(?=(\d{3})+(?!\d))/g,',');}

// ── 다이아몬드 구조 ──
// 단어 길이 n = 2k+1
// 행 0: 1개 (첫 글자 W[0])
// 행 1: 2개 (W[1])
// ...
// 행 k: k+1개 (W[k]) ← 가장 넓은 중간 행
// 행 k+1: k개 (W[k+1])
// ...
// 행 2k: 1개 (W[2k]) ← 마지막 글자 (= W[0] 대칭)
//
// 연결 규칙:
//   확장 구간 (r < k): 셀 (r,c) → (r+1,c), (r+1,c+1)
//   수축 구간 (r >= k): 셀 (r,c), (r,c+1) → (r+1,c)  즉 (r,c) → (r+1,c-1) 아니면 (r+1,c)
// 수축 구간을 명확히:  행 r (r>=k) 의 셀 c → 행 r+1 의 셀 c (왼쪽)  또는 셀 c-1 (오른쪽?)
// 실제 대각선 방향: 왼쪽↙, 오른쪽↘
// 수축 구간에서 행 r 셀 c 의 자식:
//   왼쪽↙: 행 r+1, 셀 c-1  (가능하면)
//   오른쪽↘: 행 r+1, 셀 c  (가능하면)
// 단 수축구간에서 좌끝(c=0)은 오른쪽만, 우끝(c=rowCnt-1)은 왼쪽만 가능 → 실제론 항상 두 방향 가능

function rowCount(r, k) {
  return r <= k ? r + 1 : 2*k + 1 - r;
}
function rowCharIdx(r, k) {
  // 행 r 의 글자는 단어의 r번째 글자 (0-indexed)
  return r;
}

function buildDiamond(word) {
  const n = word.length; // 홀수
  const k = (n - 1) / 2;
  const rows = n; // 총 행 = 2k+1

  const CX = 48, CY = 44, R = 19;
  const maxCols = k + 1; // 가장 넓은 행의 열 수
  const totalW = (2*k+1)*CX + 40;
  const totalH = rows*CY + 40;

  // 셀 생성
  const cells = [];
  for (let r = 0; r < rows; r++) {
    const cnt = rowCount(r, k);
    const letter = word[r];
    const startX = totalW/2 - (cnt-1)*CX/2;
    for (let c = 0; c < cnt; c++) {
      cells.push({r, c, x: startX + c*CX, y: 20 + r*CY, letter, id:`n_${r}_${c}`});
    }
  }

  function getCell(r,c){return cells.find(cl=>cl.r===r&&cl.c===c)||null;}

  // 에지 생성 (방향 포함)
  // 확장: (r,c) → (r+1,c) [왼쪽↙], (r,c) → (r+1,c+1) [오른쪽↘]
  // 수축: (r,c) → (r+1,c-1) [왼쪽↙], (r,c) → (r+1,c) [오른쪽↘]
  const edges = [];
  for (let r = 0; r < rows-1; r++) {
    const cnt = rowCount(r, k);
    const isExpand = r < k;
    for (let c = 0; c < cnt; c++) {
      const from = getCell(r,c);
      if (isExpand) {
        // ↙ 왼쪽 → 아래 왼쪽 (같은 c)
        const toL = getCell(r+1, c);
        // ↘ 오른쪽 → 아래 오른쪽 (c+1)
        const toR = getCell(r+1, c+1);
        if (toL) edges.push({from, to:toL, dir:'L'});
        if (toR) edges.push({from, to:toR, dir:'R'});
      } else {
        // 수축: ↙ → (r+1, c-1)  ↘ → (r+1, c)
        const toL = getCell(r+1, c-1);
        const toR = getCell(r+1, c);
        if (toL) edges.push({from, to:toL, dir:'L'});
        if (toR) edges.push({from, to:toR, dir:'R'});
      }
    }
  }

  // DP: 각 셀까지 경로 수
  const dp = {};
  for (const cl of cells) {
    const key = `${cl.r}_${cl.c}`;
    if (cl.r === 0) { dp[key] = 1n; continue; }
    const parents = edges.filter(e=>e.to.r===cl.r&&e.to.c===cl.c).map(e=>e.from);
    let s = 0n;
    for (const p of parents) s += dp[`${p.r}_${p.c}`]||0n;
    dp[key] = s;
  }

  // 색상: 행(글자 위치)별로 색 지정 — 같은 글자면 같은 색
  const palette = [
    '#a78bfa','#67e8f9','#fbbf24','#f472b6','#34d399',
    '#fb923c','#818cf8','#e879f9','#4ade80','#f87171',
    '#38bdf8','#facc15','#c084fc','#86efac','#fda4af'
  ];
  const letterColor = {};
  let ci = 0;
  for (const ch of word) {
    if (!(ch in letterColor)) letterColor[ch] = palette[ci++ % palette.length];
  }

  // SVG
  let edgeSvg='', cellSvg='';
  for (const e of edges) {
    const col = e.dir==='L' ? 'rgba(103,232,249,.22)' : 'rgba(244,114,182,.22)';
    edgeSvg += `<line x1="${e.from.x}" y1="${e.from.y}" x2="${e.to.x}" y2="${e.to.y}"
      stroke="${col}" stroke-width="2" marker-end="url(#arr${e.dir})"/>`;
  }
  for (const cl of cells) {
    const col = letterColor[cl.letter]||'#a78bfa';
    const isTop = cl.r===0, isBot = cl.r===rows-1;
    const thick = isTop||isBot ? 2.5 : 1.5;
    const dpVal = dp[`${cl.r}_${cl.c}`]||0n;
    cellSvg += `
      <g class="cell" id="${cl.id}" transform="translate(${cl.x},${cl.y})"
         data-r="${cl.r}" data-c="${cl.c}" data-letter="${cl.letter}" data-dp="${dpVal}" style="cursor:pointer">
        <circle r="${R}" fill="${col}1a" stroke="${col}" stroke-width="${thick}"/>
        <text text-anchor="middle" dominant-baseline="central"
          font-family="'JetBrains Mono',monospace" font-size="14" font-weight="700" fill="${col}">${cl.letter}</text>
      </g>`;
  }

  const svg = `<svg class="diamond" width="${totalW}" height="${totalH}" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <marker id="arrL" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
        <path d="M0,0 L0,6 L6,3 z" fill="rgba(103,232,249,.5)"/></marker>
      <marker id="arrR" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
        <path d="M0,0 L0,6 L6,3 z" fill="rgba(244,114,182,.5)"/></marker>
    </defs>
    ${edgeSvg}${cellSvg}
  </svg>`;

  return {svg, cells, edges, dp, letterColor, k, totalW, totalH};
}

// ── 모든 경로 열거 (k ≤ 7 → 최대 C(14,7)=3432, 표시 상한 252) ──
function allPaths(k, edges, cells) {
  function getCell(r,c){return cells.find(cl=>cl.r===r&&cl.c===c);}
  const paths = [];
  function dfs(r, c, path) {
    if (r === 2*k) { paths.push(path.slice()); return; }
    if (paths.length >= 252) return;
    const from = getCell(r,c);
    const outs = edges.filter(e=>e.from.r===r&&e.from.c===c);
    for (const e of outs) {
      path.push(e.dir);
      dfs(e.to.r, e.to.c, path);
      path.pop();
    }
  }
  dfs(0,0,[]);
  return paths;
}

// ── 경로 하이라이트 ──
let currentHighlight = null;
function highlightPath(word, k, cells, edges, dirs) {
  // 원래 색 복원
  cells.forEach(cl => {
    const col = window._lcolor[cl.letter]||'#a78bfa';
    const g = document.getElementById(cl.id);
    if (!g) return;
    g.querySelector('circle').setAttribute('fill', col+'1a');
    g.querySelector('circle').setAttribute('stroke', col);
    g.querySelector('circle').setAttribute('stroke-width', cl.r===0||cl.r===word.length-1?'2.5':'1.5');
  });
  document.querySelectorAll('line.hl-edge').forEach(el=>el.remove());
  if (!dirs) return;

  // 경로 추적
  let r=0, c=0;
  const pathCells = [cells.find(cl=>cl.r===0&&cl.c===0)];
  for (const d of dirs) {
    const from = cells.find(cl=>cl.r===r&&cl.c===c);
    const edge = edges.find(e=>e.from.r===r&&e.from.c===c&&e.dir===d);
    if (!edge) break;
    r = edge.to.r; c = edge.to.c;
    pathCells.push(edge.to);
  }
  // 하이라이트
  pathCells.forEach(cl => {
    const col = '#fff';
    const g = document.getElementById(cl.id);
    if (!g) return;
    g.querySelector('circle').setAttribute('fill', 'rgba(167,139,250,.4)');
    g.querySelector('circle').setAttribute('stroke', '#fff');
    g.querySelector('circle').setAttribute('stroke-width', '3');
  });
  // 하이라이트 에지
  const svg = document.querySelector('svg.diamond');
  if (!svg) return;
  let cr=0, cc=0;
  for (const d of dirs) {
    const edge = edges.find(e=>e.from.r===cr&&e.from.c===cc&&e.dir===d);
    if (!edge) break;
    const line = document.createElementNS('http://www.w3.org/2000/svg','line');
    line.setAttribute('class','hl-edge');
    line.setAttribute('x1',edge.from.x); line.setAttribute('y1',edge.from.y);
    line.setAttribute('x2',edge.to.x);   line.setAttribute('y2',edge.to.y);
    line.setAttribute('stroke','#fff'); line.setAttribute('stroke-width','3');
    line.setAttribute('stroke-linecap','round');
    svg.insertBefore(line, svg.firstChild.nextSibling);
    cr=edge.to.r; cc=edge.to.c;
  }
}

// ── MAIN ──
function render() {
  const raw = document.getElementById('wordInput').value.trim().toUpperCase().replace(/[^A-Z]/g,'');
  const errEl = document.getElementById('errMsg');
  const hintTag = document.getElementById('hintTag');

  if (!raw || raw.length < 3) {
    errEl.textContent='영어 단어를 3글자 이상 입력해주세요.'; errEl.style.display='block'; return;
  }
  if (raw.length % 2 === 0) {
    errEl.textContent=`⚠️ "${raw}"은(는) ${raw.length}글자(짝수)입니다. 홀수 글자 단어를 입력해주세요. (예: LEVEL, RACECAR, ABRACADABRA)`;
    errEl.style.display='block'; return;
  }
  if (raw.length > 21) {
    errEl.textContent='21글자 이하로 입력해주세요.'; errEl.style.display='block'; return;
  }
  errEl.style.display='none';
  document.getElementById('wordInput').value = raw;

  const word = raw;
  const n = word.length;
  const k = (n-1)/2;
  hintTag.textContent = `n = ${n} (홀수) → k = ${k}, 총 선택 횟수 = 2k = ${2*k}`;
  hintTag.style.display = 'inline-block';

  const {svg, cells, edges, dp, letterColor, totalW, totalH} = buildDiamond(word);
  window._lcolor = letterColor;
  window._cells = cells;
  window._edges = edges;
  window._word  = word;
  window._k     = k;

  // ── 다이아몬드 ──
  document.getElementById('diamondCard').style.display='';
  const wrap = document.getElementById('diamondWrap');
  wrap.innerHTML = svg;

  // 셀 hover
  wrap.querySelectorAll('g.cell').forEach(g => {
    g.addEventListener('mouseenter', () => {
      const r=parseInt(g.dataset.r), dv=g.dataset.dp;
      document.getElementById('pathDisplay').textContent =
        `"${g.dataset.letter}" (${r+1}번째 글자) — 이 셀까지 오는 경로 수: ${Number(dv).toLocaleString()} 가지`;
    });
    g.addEventListener('mouseleave', () => { document.getElementById('pathDisplay').textContent=''; });
  });

  // ── 공식 ──
  document.getElementById('formulaCard').style.display='';
  const result = C(2*k, k);
  document.getElementById('formulaMain').innerHTML =
    `<span style="color:#fbbf24">$\\dfrac{(2 \\times ${k})!}{${k}! \\times ${k}!}$</span>` +
    ` = <span style="color:#34d399">${fmt(result)}</span>`;
  document.getElementById('formulaSub').innerHTML =
    `단어 길이 $n = ${n} = 2 \\times ${k} + 1$<br>` +
    `맨 위에서 맨 아래까지 총 <strong style="color:#fbbf24">$2k = ${2*k}$번</strong> 선택하며,` +
    ` 정확히 <span style="color:#67e8f9">왼쪽 ${k}번</span> + <span style="color:#f472b6">오른쪽 ${k}번</span> 이동해야 합니다.<br>` +
    `$\\displaystyle \\binom{${2*k}}{${k}} = \\frac{${2*k}!}{${k}! \\times ${k}!} = ${fmt(result)}$가지`;
  document.getElementById('kpiRow').innerHTML = `
    <div class="kpi"><div class="knum">${n}</div><div class="klbl">단어 글자 수 n</div></div>
    <div class="kpi"><div class="knum">${k}</div><div class="klbl">절반 k</div></div>
    <div class="kpi"><div class="knum">${2*k}</div><div class="klbl">총 선택 횟수 2k</div></div>
    <div class="kpi"><div class="knum" style="color:#34d399;font-size:${fmt(result).length>6?'18px':'28px'}">${fmt(result)}</div><div class="klbl">경우의 수 C(2k,k)</div></div>
  `;

  // ── 단계 분석표 ──
  document.getElementById('pathTableCard').style.display='';
  const tbodyEl = document.getElementById('ptbody');
  tbodyEl.innerHTML='';
  for (let step=1; step<=2*k; step++) {
    const charIdx = step; // 행 step 의 글자
    const letter = word[charIdx] || '';
    const dpAtRow = [];
    cells.filter(cl=>cl.r===step).forEach(cl=>{
      dpAtRow.push(Number(dp[`${cl.r}_${cl.c}`]||0n));
    });
    const rowSum = dpAtRow.reduce((a,b)=>a+b,0);
    tbodyEl.innerHTML += `<tr>
      <td style="color:#a78bfa">${step}</td>
      <td>↙&nbsp;or&nbsp;↘</td>
      <td style="color:${letterColor[letter]||'#e2e8f0'};font-weight:900">${letter}</td>
      <td style="color:#34d399">${rowSum.toLocaleString()}</td>
    </tr>`;
  }

  // ── 모든 경로 ──
  if (k <= 7) {
    document.getElementById('exploreCard').style.display='';
    const paths = allPaths(k, edges, cells);
    const pw = document.getElementById('allPathsWrap');
    pw.innerHTML='';
    paths.forEach((dirs,i)=>{
      const chip = document.createElement('div');
      chip.className='path-chip';
      chip.textContent = dirs.map(d=>d==='L'?'↙':'↘').join('');
      chip.title = `경로 ${i+1}: ${dirs.join('')}`;
      chip.addEventListener('click',()=>{
        document.querySelectorAll('.path-chip').forEach(c=>c.classList.remove('active'));
        chip.classList.add('active');
        highlightPath(word,k,cells,edges,dirs);
      });
      pw.appendChild(chip);
    });
    if (k>5) {
      const note = document.createElement('div');
      note.style.cssText='color:#64748b;font-size:11px;padding:4px 8px;width:100%';
      note.textContent=`(총 ${fmt(result)}가지 중 최대 252개만 표시)`;
      pw.appendChild(note);
    }
  } else {
    document.getElementById('exploreCard').style.display='none';
  }

  // ── 풀이 단계 ──
  document.getElementById('explainCard').style.display='';
  document.getElementById('stepsContent').innerHTML = `
    <div class="step-item">
      <div class="step-num">1</div>
      <div class="step-body">
        <strong>단어 길이 확인</strong><br>
        <span class="hl">"${word}"</span>는 총 <span class="hl">${n}글자</span>(홀수 ✓).<br>
        $n = ${n} = 2 \\times ${k} + 1$ 이므로 $k = ${k}$
      </div>
    </div>
    <div class="step-item">
      <div class="step-num">2</div>
      <div class="step-body">
        <strong>다이아몬드 격자 구조</strong><br>
        맨 위 꼭짓점(<span class="hl">${word[0]}</span>)에서 맨 아래 꼭짓점(<span class="hl">${word[n-1]}</span>)까지
        총 <span class="hl">${2*k}번</span> 이동합니다.<br>
        왼쪽 변: <span class="hl2">${word.substring(0,k+1)}</span>,
        오른쪽 변: <span class="hl2">${word[0]}${word.substring(k+1)}</span><br>
        각 이동은 <span style="color:#67e8f9">왼쪽(↙)</span> 또는 <span style="color:#f472b6">오른쪽(↘)</span> 두 가지만 가능합니다.
      </div>
    </div>
    <div class="step-item">
      <div class="step-num">3</div>
      <div class="step-body">
        <strong>왼쪽/오른쪽 선택의 조건</strong><br>
        맨 아래 꼭짓점에 도달하려면
        <span style="color:#67e8f9">왼쪽을 정확히 ${k}번</span>,
        <span style="color:#f472b6">오른쪽을 정확히 ${k}번</span> 선택해야 합니다.<br>
        이건 왼쪽(✓) ${k}개와 오른쪽(✗) ${k}개를 일렬로 나열하는 <strong>같은 것이 있는 순열</strong>과 같습니다.
      </div>
    </div>
    <div class="step-item">
      <div class="step-num">4</div>
      <div class="step-body">
        <strong>공식 적용</strong><br>
        $\\displaystyle \\frac{(${2*k})!}{${k}! \\times ${k}!} = \\binom{${2*k}}{${k}} = ${fmt(result)}$가지<br>
        격자 위에서 각 셀에 마우스를 올려 경로 수가 맞는지 확인해 보세요!
      </div>
    </div>
  `;

  // KaTeX 재렌더링
  if (typeof renderMathInElement !== 'undefined') {
    setTimeout(()=>renderMathInElement(document.body,{
      delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],
      throwOnError:false
    }),150);
  }
}

document.getElementById('genBtn').addEventListener('click', render);
document.getElementById('wordInput').addEventListener('keydown', e=>{if(e.key==='Enter')render();});
window.addEventListener('load', render);
</script>
</body>
</html>
"""

def _render_quiz():
    st.divider()
    st.subheader("🧩 확인 문제")
    st.caption("활동을 바탕으로 아래 문제를 풀어보세요. 답을 입력하고 **채점하기** 버튼을 눌러주세요.")

    QUIZ = [
        {
            "q": r"단어 **ABRACADABRA** (11글자)로 만든 다이아몬드 격자에서, 맨 위 꼭짓점 A에서 출발하여 아래로 이웃한 칸을 하나씩 선택하여 ABRACADABRA를 읽을 수 있는 경우의 수를 구하시오.",
            "a": "252",
            "hint": r"$n = 11 = 2 \times 5 + 1$ 이므로 $k = 5$. 왼쪽 5번, 오른쪽 5번 선택하는 순열의 수를 구하세요: $\dfrac{10!}{5! \times 5!}$",
            "sol": r"""왼쪽(↙) $5$번, 오른쪽(↘) $5$번을 일렬로 나열하는 **같은 것이 있는 순열**의 수와 같습니다.
$$\frac{(2 \times 5)!}{5! \times 5!} = \frac{10!}{5! \times 5!} = \binom{10}{5} = 252$$"""
        },
        {
            "q": r"단어 **LEVEL** (5글자)로 만든 다이아몬드 격자에서 LEVEL을 읽을 수 있는 경우의 수를 구하시오. (단, $n = 5 = 2 \times 2 + 1$이므로 $k = 2$)",
            "a": "6",
            "hint": r"왼쪽 $k=2$번, 오른쪽 $k=2$번 선택. $\dfrac{4!}{2! \times 2!}$를 계산하세요.",
            "sol": r"""$n = 5,\ k = 2$ 이므로 총 $2k = 4$번 이동합니다.
$$\frac{4!}{2! \times 2!} = \binom{4}{2} = 6$$"""
        },
        {
            "q": r"단어 **RACECAR** (7글자)로 만든 다이아몬드 격자에서 RACECAR를 읽을 수 있는 경우의 수를 구하시오. (단, $n = 7 = 2 \times 3 + 1$이므로 $k = 3$)",
            "a": "20",
            "hint": r"왼쪽 $k=3$번, 오른쪽 $k=3$번 선택. $\dfrac{6!}{3! \times 3!}$를 계산하세요.",
            "sol": r"""$n = 7,\ k = 3$ 이므로 총 $2k = 6$번 이동합니다.
$$\frac{6!}{3! \times 3!} = \binom{6}{3} = 20$$"""
        },
    ]

    for i, item in enumerate(QUIZ):
        with st.container():
            st.markdown(f"**문제 {i+1}.** {item['q']}")
            col1, col2 = st.columns([3, 1])
            with col1:
                user_ans = st.text_input(
                    f"답 입력 (문제 {i+1})",
                    key=f"wdp_q{i+1}",
                    label_visibility="collapsed",
                    placeholder="숫자로 입력하세요"
                )
            with col2:
                check = st.button("채점하기", key=f"wdp_check{i+1}", use_container_width=True)

            if check and user_ans.strip():
                user_stripped = user_ans.strip().replace(',', '').replace(' ', '')
                correct_stripped = str(item['a']).replace(',', '').replace(' ', '')
                if user_stripped == correct_stripped:
                    st.success("✅ 정답입니다!")
                else:
                    st.error(f"❌ 틀렸습니다. 정답은 **{item['a']}** 입니다.")
                with st.expander("💡 풀이 보기"):
                    st.markdown(item['sol'])
            elif check and not user_ans.strip():
                st.warning("답을 입력해주세요.")
        st.markdown("---")
