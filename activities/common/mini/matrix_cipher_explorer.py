# activities/common/mini/matrix_cipher_explorer.py
"""
행렬 암호 탐구
열쇠행렬 M을 이용한 암호 제작(B = A + M) 및 해독(A = B - M) — 행렬 덧셈/뺄셈 응용
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

_GAS_URL    = st.secrets["gas_url_common"]
_SHEET_NAME = "행렬암호탐구"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 '행렬 암호 탐구' 활동을 마치고 배운 내용을 정리해보세요**"},
    {"key": "enc_dec_role",
     "label": "1️⃣ 암호화에는 덧셈(B = A + M), 해독에는 뺄셈(A = B − M)을 쓰는 이유를 설명해보세요.",
     "type": "text_area", "height": 110},
    {"key": "key_importance",
     "label": "2️⃣ 열쇠행렬 M이 바뀌면 같은 단어도 다른 암호가 됩니다. 이것이 왜 중요한지 쓰세요.",
     "type": "text_area", "height": 100},
    {"key": "weakness",
     "label": "3️⃣ 이 암호 방식의 한계나 약점은 무엇일까요? 어떻게 보완할 수 있을지도 생각해보세요.",
     "type": "text_area", "height": 110},
    {"key": "새롭게알게된점",
     "label": "💡 이 활동을 통해 새롭게 알게 된 점",
     "type": "text_area", "height": 90},
    {"key": "느낀점",
     "label": "💬 이 활동을 하면서 느낀 점",
     "type": "text_area", "height": 90},
]

META = {
    "title":       "🔐 행렬 암호 탐구",
    "description": "열쇠행렬 M으로 영단어를 암호화하고 해독하는 활동 – 행렬 덧셈·뺄셈의 실생활 응용",
    "order":       8,
    "hidden":      False,
}

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>행렬 암호 탐구</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#06090f;color:#c0d4ec;
  padding:10px;min-height:100vh}

/* ── tabs ── */
.tab-bar{display:flex;gap:6px;margin-bottom:14px}
.tb{flex:1;padding:9px 4px;text-align:center;border-radius:10px;
  border:2px solid #152035;background:#0a1525;color:#3d5878;
  font-size:.8rem;font-weight:800;cursor:pointer;transition:all .2s;line-height:1.4}
.tb.on{background:linear-gradient(135deg,#1d4ed8,#7c3aed);color:#fff;
  border-color:transparent;box-shadow:0 3px 16px rgba(99,102,241,.35)}
.panel{display:none}.panel.on{display:block}

/* ── card shell ── */
.card{background:#0d1a2e;border:1px solid #1e3050;border-radius:14px;
  padding:16px;margin-bottom:12px}
.card-title{font-size:1rem;font-weight:900;color:#fbbf24;margin-bottom:12px}

/* ── matrix brackets (CSS-only) ── */
.mat-wrap{display:inline-flex;align-items:stretch;vertical-align:middle}
.mb-l,.mb-r{width:8px;flex-shrink:0}
.mb-l{border-top:3px solid currentColor;border-bottom:3px solid currentColor;
  border-left:3px solid currentColor;border-radius:4px 0 0 4px}
.mb-r{border-top:3px solid currentColor;border-bottom:3px solid currentColor;
  border-right:3px solid currentColor;border-radius:0 4px 4px 0}
.mg{display:grid;gap:5px;padding:6px 4px}
.mc{min-width:44px;height:38px;display:flex;align-items:center;justify-content:center;
  border-radius:6px;font-size:1.15rem;font-weight:700;
  font-family:'Courier New',monospace;border:1.5px solid #1e3050}
.mc.blue {background:rgba(59,130,246,.15);border-color:#3b82f6;color:#93c5fd}
.mc.purple{background:rgba(167,139,250,.15);border-color:#8b5cf6;color:#c4b5fd}
.mc.gold  {background:rgba(251,191,36,.15) ;border-color:#f59e0b;color:#fbbf24}
.mc.green {background:rgba(34,197,94,.15)  ;border-color:#22c55e;color:#4ade80}
.mc.input {background:#060c18;border-color:#1e3050;color:#e2e8f0}

/* ── alpha table ── */
.alpha-table{display:grid;grid-template-columns:repeat(13,1fr);gap:3px;margin:8px 0}
.ac{background:#060c18;border:1px solid #1a3050;border-radius:5px;padding:4px 2px;
  text-align:center;cursor:pointer;transition:all .2s}
.ac:hover,.ac.hi{background:#1d4ed8;border-color:#3b82f6}
.ac-let{font-size:.85rem;font-weight:800;color:#fbbf24}
.ac-num{font-size:.7rem;color:#64748b}
.ac.hi .ac-num{color:#fff}

/* ── hint/warn/success boxes ── */
.hint{background:rgba(56,189,248,.07);border-left:3px solid #38bdf8;
  border-radius:0 8px 8px 0;padding:8px 12px;font-size:.85rem;color:#7dd3fc;
  margin:10px 0;line-height:1.7}
.warn{background:rgba(248,113,113,.07);border-left:3px solid #f87171;
  border-radius:0 8px 8px 0;padding:8px 12px;font-size:.85rem;color:#fca5a5;margin:8px 0}
.ok  {background:rgba(34,197,94,.07)  ;border-left:3px solid #22c55e;
  border-radius:0 8px 8px 0;padding:8px 12px;font-size:.85rem;color:#4ade80;margin:8px 0}

/* ── buttons ── */
.btn{padding:9px 18px;border-radius:9px;border:none;cursor:pointer;
  font-size:.88rem;font-weight:800;transition:all .18s}
.btn:hover:not(:disabled){transform:translateY(-2px)}
.btn:disabled{opacity:.35;cursor:default}
.btn-blue  {background:linear-gradient(135deg,#1d4ed8,#3b82f6);color:#fff;
  box-shadow:0 3px 12px rgba(59,130,246,.3)}
.btn-purple{background:linear-gradient(135deg,#7c3aed,#a78bfa);color:#fff;
  box-shadow:0 3px 12px rgba(124,58,237,.3)}
.btn-green {background:linear-gradient(135deg,#059669,#10b981);color:#fff;
  box-shadow:0 3px 12px rgba(5,150,105,.3)}
.btn-gold  {background:linear-gradient(135deg,#d97706,#fbbf24);color:#000;
  box-shadow:0 3px 12px rgba(217,119,6,.25);font-size:.8rem}
.btn-ghost {background:#0d1a2e;color:#64748b;border:1px solid #1e3050}

/* ── word input ── */
.inp-word{background:#0a1525;border:2.5px solid #1e3050;border-radius:10px;
  color:#e2e8f0;font-size:1.8rem;font-weight:800;font-family:'Courier New',monospace;
  padding:12px 16px;text-align:center;width:200px;letter-spacing:.2em;
  text-transform:uppercase;outline:none;transition:border-color .2s}
.inp-word:focus{border-color:#3b82f6;box-shadow:0 0 14px rgba(59,130,246,.3)}
.inp-word::placeholder{color:#334155;letter-spacing:.05em}

/* ── matrix number inputs (decode) ── */
.inp-mc{background:#060c18;border:2.5px solid #1e3050;border-radius:8px;
  color:#c4b5fd;font-size:1.3rem;font-weight:700;font-family:'Courier New',monospace;
  padding:8px;text-align:center;width:60px;height:52px;outline:none;
  transition:border-color .2s;-moz-appearance:textfield}
.inp-mc:focus{border-color:#7c3aed;box-shadow:0 0 10px rgba(124,58,237,.3)}
.inp-mc::-webkit-inner-spin-button,.inp-mc::-webkit-outer-spin-button{-webkit-appearance:none}

/* ── big result word ── */
.big-word{font-size:3.2rem;font-weight:900;letter-spacing:.18em;text-align:center;
  padding:20px 10px;animation:pop .45s ease}
@keyframes pop{
  0%  {opacity:0;transform:scale(.7)}
  70% {transform:scale(1.1)}
  100%{opacity:1;transform:scale(1)}
}

/* ── char badges ── */
.char-badge{background:#0d1a2e;border:1.5px solid #1e3050;border-radius:10px;
  padding:10px 14px;text-align:center;min-width:60px}
.char-badge .ltr{font-size:2rem;font-weight:900;color:#fbbf24}
.char-badge .arr{font-size:.7rem;color:#475569;margin:3px 0}
.char-badge .num{font-size:1.4rem;font-weight:800;color:#93c5fd}

/* ── step block ── */
.step{background:#060c18;border-radius:10px;padding:13px;margin-bottom:10px}
.step-ttl{font-size:.78rem;font-weight:800;color:#fbbf24;margin-bottom:10px;
  letter-spacing:.03em}
.eq-row{display:flex;align-items:center;gap:10px;justify-content:center;
  flex-wrap:wrap;font-size:1.1rem;font-weight:800;color:#475569}
.op-sym{font-size:1.5rem;font-weight:900;color:#475569}

/* ── challenge ── */
.chall-card{background:#0a1525;border:2px solid #1e3050;border-radius:12px;
  padding:14px;margin-bottom:10px;transition:border-color .3s}
.chall-card.solved{border-color:#22c55e}
.chall-num{display:inline-block;background:linear-gradient(135deg,#1d4ed8,#7c3aed);
  color:#fff;font-size:.72rem;font-weight:800;padding:3px 10px;border-radius:6px;
  margin-bottom:10px}
.chall-inp{background:#060c18;border:2.5px solid #1e3050;border-radius:8px;
  color:#e2e8f0;font-size:1.2rem;font-weight:800;font-family:'Courier New',monospace;
  padding:8px 12px;text-align:center;width:110px;letter-spacing:.12em;
  text-transform:uppercase;outline:none;transition:border-color .2s}
.chall-inp:focus{border-color:#3b82f6}

/* ── progress dots ── */
.dots{display:flex;gap:7px;justify-content:center;margin:6px 0}
.dot{width:11px;height:11px;border-radius:50%;background:#1e3050;transition:all .35s}
.dot.done{background:#22c55e;box-shadow:0 0 6px #22c55e}
.dot.cur {background:#3b82f6;box-shadow:0 0 6px #3b82f6;animation:pulse .9s infinite}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.25)}}

/* ── finale banner ── */
.finale{background:#0d1a2e;border:2px solid #22c55e;border-radius:14px;
  text-align:center;padding:24px 16px;margin-top:10px}
.finale-icon{font-size:3.5rem;animation:bounce 1s infinite}
@keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}

/* ── particles ── */
.pt{position:fixed;pointer-events:none;border-radius:50%;z-index:9999;
  animation:ptf 1s ease-out forwards}
@keyframes ptf{
  0%  {opacity:1;transform:translate(0,0)scale(1)}
  100%{opacity:0;transform:translate(var(--tx),var(--ty))scale(0)}
}
@media(max-width:460px){
  .mc{min-width:36px;height:32px;font-size:1rem}
  .big-word{font-size:2.4rem}
  .inp-word{font-size:1.4rem;width:160px}
}
</style>
</head>
<body>

<!-- ════ TABS ════ -->
<div class="tab-bar">
  <div class="tb on"  id="tb-pri"  onclick="switchTab('pri')">📖 원리</div>
  <div class="tb"     id="tb-enc"  onclick="switchTab('enc')">✏️ 암호 만들기</div>
  <div class="tb"     id="tb-dec"  onclick="switchTab('dec')">🔓 해독하기</div>
  <div class="tb"     id="tb-chall"onclick="switchTab('chall')">🎯 도전!</div>
</div>

<!-- ════ PRINCIPLE ════ -->
<div class="panel on" id="panel-pri">

  <!-- alpha table -->
  <div class="card">
    <div class="card-title">🔡 알파벳 ↔ 숫자 대응표</div>
    <div class="alpha-table" id="alpha-table"></div>
    <div class="hint" style="margin-top:8px">글자를 클릭하면 해당 번호가 강조됩니다</div>
  </div>

  <!-- key matrix -->
  <div class="card">
    <div class="card-title">🔑 열쇠행렬 M</div>
    <div style="display:flex;align-items:center;gap:20px;flex-wrap:wrap;justify-content:center">
      <div style="text-align:center">
        <div style="font-size:1.15rem;font-weight:800;color:#fbbf24;margin-bottom:8px">M =</div>
        <div id="key-mat"></div>
      </div>
      <div style="flex:1;min-width:190px;background:#060c18;border-radius:10px;padding:12px">
        <div style="font-size:1rem;line-height:2.1;color:#94a3b8">
          📤 <strong style="color:#93c5fd">암호화</strong> : B = A + M<br>
          📥 <strong style="color:#f9a8d4">해독</strong>&nbsp;&nbsp;&nbsp; : A = B − M
        </div>
        <div style="font-size:.75rem;color:#475569;margin-top:8px">열쇠행렬 M을 알아야만 해독할 수 있어요!</div>
      </div>
    </div>
  </div>

  <!-- LOVE step-by-step -->
  <div class="card">
    <div class="card-title">📝 예시: 'LOVE' 암호화 단계별 풀이</div>
    <div id="love-steps"></div>
  </div>

  <div style="text-align:center;margin-bottom:6px">
    <button class="btn btn-blue" onclick="switchTab('enc')">✏️ 직접 해보기 ▶</button>
  </div>
</div>

<!-- ════ ENCODE ════ -->
<div class="panel" id="panel-enc">
  <div class="card">
    <div class="card-title">✏️ 나만의 암호 만들기</div>
    <div style="text-align:center;margin-bottom:16px">
      <div style="font-size:.88rem;color:#64748b;margin-bottom:10px">
        영어 4글자 단어를 입력하세요
      </div>
      <input class="inp-word" id="enc-inp" maxlength="4" placeholder="WORD"
        oninput="onEnc()">
      <div id="enc-cnt" style="font-size:.72rem;color:#475569;margin-top:6px">0 / 4 글자</div>
    </div>
    <div id="enc-result" style="display:none">
      <div class="step">
        <div class="step-ttl">① 각 문자 → 번호</div>
        <div id="enc-nums" style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap"></div>
      </div>
      <div class="step">
        <div class="step-ttl">② 번호 → 2×2 행렬 A</div>
        <div id="enc-matA" style="text-align:center"></div>
      </div>
      <div class="step">
        <div class="step-ttl">③ 암호 행렬 B = A + M</div>
        <div id="enc-calc" class="eq-row"></div>
      </div>
      <div class="ok" id="enc-ok"></div>
    </div>
  </div>
</div>

<!-- ════ DECODE ════ -->
<div class="panel" id="panel-dec">
  <div class="card">
    <div class="card-title">🔓 암호 행렬 B → 단어 찾기</div>
    <div class="hint">암호 행렬 B의 값을 입력하면 A = B − M으로 계산해 원래 단어를 알려드려요!</div>

    <!-- B input -->
    <div style="margin:14px 0;text-align:center">
      <div style="font-size:.8rem;font-weight:800;color:#64748b;margin-bottom:10px">
        암호 행렬 B 입력
      </div>
      <div style="display:inline-flex;align-items:stretch;gap:4px">
        <div class="mb-l" style="color:#8b5cf6"></div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px 2px">
          <input class="inp-mc" id="b11" type="number" placeholder="b₁₁">
          <input class="inp-mc" id="b12" type="number" placeholder="b₁₂">
          <input class="inp-mc" id="b21" type="number" placeholder="b₂₁">
          <input class="inp-mc" id="b22" type="number" placeholder="b₂₂">
        </div>
        <div class="mb-r" style="color:#8b5cf6"></div>
      </div>
    </div>

    <div style="text-align:center;margin-bottom:12px">
      <button class="btn btn-purple" onclick="doDec()">🔓 해독하기</button>
    </div>
    <div id="dec-result" style="display:none"></div>
  </div>

  <!-- examples -->
  <div class="card">
    <div class="card-title">💡 예시 문제로 해보기</div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px">
      <button class="btn btn-gold" onclick="loadEx(17,8,20,9)">
        B = [[17, 8], [20, 9]]
      </button>
      <button class="btn btn-gold" onclick="loadEx(13,8,11,9)">
        B = [[13, 8], [11, 9]]
      </button>
      <button class="btn btn-gold" onclick="loadEx(12,2,4,24)">
        B = [[12, 2], [4, 24]]
      </button>
    </div>
    <div style="font-size:.72rem;color:#475569">버튼을 누르면 자동으로 값이 채워집니다</div>
  </div>
</div>

<!-- ════ CHALLENGE ════ -->
<div class="panel" id="panel-chall">
  <div class="card">
    <div class="card-title">🎯 암호 해독 챌린지</div>
    <div class="hint">암호 행렬 B를 보고 A = B − M을 계산해 단어를 맞혀보세요!</div>
    <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;
      background:#060c18;border-radius:10px;padding:12px;margin-bottom:10px">
      <div style="font-size:.85rem;font-weight:800;color:#fbbf24">🔑 열쇠행렬 M =</div>
      <div id="chall-key-mat"></div>
      <div style="font-size:.82rem;color:#64748b">→ A = B − M 으로 해독</div>
    </div>
    <div class="dots" id="c-dots"></div>
    <div id="c-prog" style="font-size:.72rem;color:#64748b;text-align:center;margin-bottom:4px">
      0 / 5 해결
    </div>
  </div>
  <div id="chall-cards"></div>
  <div id="finale" style="display:none">
    <div class="finale">
      <div class="finale-icon">🏆</div>
      <div style="font-size:1.6rem;font-weight:900;color:#4ade80;margin:10px 0">모든 암호 해독 완료!</div>
      <div style="font-size:.9rem;color:#64748b">행렬 덧셈·뺄셈의 달인이 됐어요!</div>
    </div>
  </div>
</div>

<script>
/* ═══ KEY MATRIX ═══ */
const M = [[5,-7],[-2,4]];

/* ═══ MATRIX HELPERS ═══ */
function mAdd(A,B){return A.map((r,i)=>r.map((v,j)=>v+B[i][j]))}
function mSub(A,B){return A.map((r,i)=>r.map((v,j)=>v-B[i][j]))}
function n2l(n){return(n>=1&&n<=26)?String.fromCharCode(64+n):'?'}
function mat2word(m){return[m[0][0],m[0][1],m[1][0],m[1][1]].map(n2l).join('')}
function isValid(m){return[m[0][0],m[0][1],m[1][0],m[1][1]].every(n=>n>=1&&n<=26)}

/* ═══ MATRIX HTML ═══ */
function matHtml(data, cls='blue', cellW=44){
  const cols=data[0].length;
  const cells=data.map(row=>
    row.map(v=>`<div class="mc ${cls}" style="min-width:${cellW}px">${v}</div>`).join('')
  ).join('');
  return `<span class="mat-wrap" style="color:${cls2color(cls)}">
    <span class="mb-l"></span>
    <span class="mg" style="grid-template-columns:repeat(${cols},1fr)">${cells}</span>
    <span class="mb-r"></span>
  </span>`;
}
function cls2color(c){
  return{blue:'#93c5fd',purple:'#c4b5fd',gold:'#fbbf24',green:'#4ade80',input:'#c0d4ec'}[c]||'#e2e8f0';
}

/* ═══ ALPHA TABLE ═══ */
function buildAlpha(){
  const t=document.getElementById('alpha-table');
  const az='ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  t.innerHTML=az.map((l,i)=>`
    <div class="ac" id="ac-${i}" onclick="hiLetter(${i})">
      <div class="ac-let">${l}</div>
      <div class="ac-num">${i+1}</div>
    </div>`).join('');
}
let lastHi=-1;
function hiLetter(i){
  if(lastHi>=0) document.getElementById(`ac-${lastHi}`).classList.remove('hi');
  document.getElementById(`ac-${i}`).classList.add('hi');
  lastHi=i;
}

/* ═══ KEY MATRIX DISPLAY ═══ */
function buildKeyMat(){
  document.getElementById('key-mat').innerHTML=matHtml(M,'gold',44);
}

/* ═══ LOVE STEPS ═══ */
function buildLove(){
  const word='LOVE';
  const nums=word.split('').map(c=>c.charCodeAt(0)-64); // 12,15,22,5
  const A=[[nums[0],nums[1]],[nums[2],nums[3]]];
  const B=mAdd(A,M);
  document.getElementById('love-steps').innerHTML=`
    <div class="step">
      <div class="step-ttl">① 'L','O','V','E' → 번호로 변환</div>
      <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
        ${word.split('').map((c,i)=>`
          <div class="char-badge">
            <div class="ltr">${c}</div>
            <div class="arr">↓</div>
            <div class="num">${nums[i]}</div>
          </div>`).join('')}
      </div>
    </div>
    <div class="step">
      <div class="step-ttl">② 번호를 2×2 행렬 A로 배열 (행 순서대로)</div>
      <div class="eq-row">
        <span>A =</span>${matHtml(A,'blue')}
        <span style="font-size:.8rem;color:#475569">(첫행: L,O / 둘째행: V,E)</span>
      </div>
    </div>
    <div class="step">
      <div class="step-ttl">③ 암호 행렬 B = A + M 계산</div>
      <div class="eq-row">
        <span>B =</span>${matHtml(A,'blue')}
        <span class="op-sym">+</span>${matHtml(M,'gold')}
        <span class="op-sym">=</span>${matHtml(B,'green')}
      </div>
    </div>
    <div class="step">
      <div class="step-ttl">④ 해독: A = B − M으로 복원</div>
      <div class="eq-row">
        <span>A =</span>${matHtml(B,'green')}
        <span class="op-sym">−</span>${matHtml(M,'gold')}
        <span class="op-sym">=</span>${matHtml(A,'blue')}
        <span style="font-size:1.2rem;font-weight:900;color:#4ade80">→ LOVE ✓</span>
      </div>
    </div>`;
}

/* ═══ ENCODE ═══ */
function onEnc(){
  const raw=document.getElementById('enc-inp').value.toUpperCase().replace(/[^A-Z]/g,'');
  document.getElementById('enc-inp').value=raw;
  document.getElementById('enc-cnt').textContent=raw.length+' / 4 글자';
  const r=document.getElementById('enc-result');
  if(raw.length!==4){r.style.display='none';return;}

  const nums=raw.split('').map(c=>c.charCodeAt(0)-64);
  const A=[[nums[0],nums[1]],[nums[2],nums[3]]];
  const B=mAdd(A,M);

  document.getElementById('enc-nums').innerHTML=raw.split('').map((c,i)=>`
    <div class="char-badge">
      <div class="ltr">${c}</div>
      <div class="arr">↓</div>
      <div class="num">${nums[i]}</div>
    </div>`).join('');
  document.getElementById('enc-matA').innerHTML=
    `<div class="eq-row"><span>A =</span>${matHtml(A,'blue')}</div>`;
  document.getElementById('enc-calc').innerHTML=
    `<span>B =</span>${matHtml(A,'blue')}
     <span class="op-sym">+</span>${matHtml(M,'gold')}
     <span class="op-sym">=</span>${matHtml(B,'green')}`;
  document.getElementById('enc-ok').innerHTML=
    `<strong>암호화 완료!</strong> '${raw}'의 암호 행렬 B = `+
    `[[${B[0][0]}, ${B[0][1]}], [${B[1][0]}, ${B[1][1]}]]`;
  r.style.display='block';
}

/* ═══ DECODE ═══ */
function doDec(){
  const vals=['b11','b12','b21','b22'].map(id=>parseInt(document.getElementById(id).value));
  const r=document.getElementById('dec-result');
  r.style.display='block';
  if(vals.some(isNaN)){r.innerHTML='<div class="warn">⚠️ 네 칸을 모두 입력해주세요!</div>';return;}
  const Bmat=[[vals[0],vals[1]],[vals[2],vals[3]]];
  const Amat=mSub(Bmat,M);
  const word=mat2word(Amat);
  const ok=isValid(Amat);
  let html=`
    <div class="step" style="margin-bottom:10px">
      <div class="step-ttl">계산 과정: A = B − M</div>
      <div class="eq-row">
        <span>A =</span>${matHtml(Bmat,'purple')}
        <span class="op-sym">−</span>${matHtml(M,'gold')}
        <span class="op-sym">=</span>${matHtml(Amat,'blue')}
      </div>
    </div>`;
  if(ok){
    html+=`<div class="big-word" style="color:#4ade80">🎉 ${word}</div>`;
    burst();
  } else {
    html+=`<div class="warn">결과 값이 1~26 범위를 벗어났습니다. 입력값을 다시 확인해주세요.<br>
      A = [[${Amat[0][0]}, ${Amat[0][1]}], [${Amat[1][0]}, ${Amat[1][1]}]]</div>`;
  }
  r.innerHTML=html;
}
function loadEx(b11,b12,b21,b22){
  ['b11','b12','b21','b22'].forEach((id,i)=>{
    document.getElementById(id).value=[b11,b12,b21,b22][i];
  });
  doDec();
}

/* ═══ CHALLENGES ═══ */
const CHALLS=[
  {word:'HOME'},
  {word:'GIFT'},
  {word:'MOON'},
  {word:'COOL'},
  {word:'LION'},
];
// compute B for each
CHALLS.forEach(ch=>{
  const nums=ch.word.split('').map(c=>c.charCodeAt(0)-64);
  ch.A=[[nums[0],nums[1]],[nums[2],nums[3]]];
  ch.B=mAdd(ch.A,M);
});
let solved=CHALLS.map(()=>false);

function buildChall(){
  document.getElementById('chall-key-mat').innerHTML=matHtml(M,'gold',44);
  document.getElementById('c-dots').innerHTML=
    CHALLS.map((_,i)=>`<div class="dot" id="dot-${i}"></div>`).join('');
  updateDots();

  document.getElementById('chall-cards').innerHTML=CHALLS.map((ch,i)=>`
    <div class="chall-card" id="cc-${i}">
      <div class="chall-num">도전 ${i+1}</div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;flex-wrap:wrap">
        <span style="font-size:.9rem;color:#64748b">암호 행렬 B =</span>
        ${matHtml(ch.B,'purple',42)}
      </div>
      <div style="font-size:.8rem;color:#64748b;margin-bottom:10px">
        A = B − M을 계산해 단어를 맞혀보세요!
      </div>
      <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
        <input class="chall-inp" id="ci-${i}" maxlength="4" placeholder="????"
          onkeydown="if(event.key==='Enter')chkChall(${i})">
        <button class="btn btn-green" onclick="chkChall(${i})">확인!</button>
        <button class="btn btn-ghost" onclick="hintChall(${i})">💡 힌트</button>
      </div>
      <div id="cr-${i}" style="margin-top:8px"></div>
    </div>`).join('');
}

function chkChall(i){
  const inp=document.getElementById(`ci-${i}`).value.toUpperCase().trim();
  const r=document.getElementById(`cr-${i}`);
  if(inp.length!==4){r.innerHTML='<div class="warn" style="margin:0">⚠️ 4글자를 입력하세요!</div>';return;}
  if(inp===CHALLS[i].word){
    solved[i]=true;
    r.innerHTML=`<div class="ok" style="margin:0">🎉 정답! <strong>${inp}</strong> 맞습니다!</div>`;
    document.getElementById(`cc-${i}`).classList.add('solved');
    document.getElementById(`ci-${i}`).disabled=true;
    updateDots();
    burst();
    if(solved.every(Boolean)) setTimeout(()=>document.getElementById('finale').style.display='block',400);
  } else {
    r.innerHTML='<div class="warn" style="margin:0">❌ 틀렸어요. 다시 계산해보세요!</div>';
  }
}
function hintChall(i){
  const A=CHALLS[i].A;
  document.getElementById(`cr-${i}`).innerHTML=
    `<div class="hint" style="margin:4px 0;font-size:.8rem">
      힌트: A = ${matHtml(A,'blue',36)} → 각 숫자를 알파벳으로 바꿔보세요!
    </div>`;
}
function updateDots(){
  const n=solved.filter(Boolean).length;
  CHALLS.forEach((_,i)=>{
    const d=document.getElementById(`dot-${i}`);
    if(!d) return;
    d.className='dot '+(solved[i]?'done':i===n?'cur':'');
  });
  document.getElementById('c-prog').textContent=`${n} / ${CHALLS.length} 해결`;
}

/* ═══ PARTICLES ═══ */
function burst(){
  const cols=['#22c55e','#fbbf24','#38bdf8','#a78bfa','#f87171','#fb923c'];
  const cx=window.innerWidth/2, cy=window.innerHeight/3;
  for(let i=0;i<20;i++){
    const p=document.createElement('div'); p.className='pt';
    const a=Math.random()*Math.PI*2, d=60+Math.random()*130;
    p.style.cssText=`left:${cx}px;top:${cy}px;background:${cols[i%6]};`+
      `width:${5+Math.random()*6}px;height:${5+Math.random()*6}px;`+
      `--tx:${Math.cos(a)*d}px;--ty:${Math.sin(a)*d-60}px;`+
      `animation-delay:${Math.random()*.15}s`;
    document.body.appendChild(p);
    setTimeout(()=>p.remove(),1100);
  }
}

/* ═══ TABS ═══ */
function switchTab(tab){
  ['pri','enc','dec','chall'].forEach(t=>{
    document.getElementById('panel-'+t).classList.toggle('on',t===tab);
    document.getElementById('tb-'+t).classList.toggle('on',t===tab);
  });
}

/* ═══ INIT ═══ */
buildAlpha();
buildKeyMat();
buildLove();
buildChall();
</script>
</body>
</html>"""


def render():
    st.markdown("### 🔐 행렬 암호 탐구")
    st.caption("열쇠행렬 M으로 단어를 암호화하고 해독해보세요! B = A + M, A = B − M")
    components.html(_HTML, height=1750, scrolling=True)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
