import streamlit as st
import streamlit.components.v1 as components
import requests
from reflection_utils import render_reflection_form
import datetime

META = {"title": "대수막대로 곱셈 공식 탐구", "order": 25}

_GAS_URL = st.secrets["gas_url_common"]
_SHEET_NAME = "대수막대곱셈공식"

_QUESTIONS = [
    {"key": '문제1', "label": '문제 1', "type": 'text_area', "height": 70},
    {"key": '답1', "label": '문제 1 답', "type": 'text_area', "height": 70},
    {"key": '문제2', "label": '문제 2', "type": 'text_area', "height": 70},
    {"key": '답2', "label": '문제 2 답', "type": 'text_area', "height": 70},
    {"key": '새롭게알게된점', "label": '새롭게 알게 된 점', "type": 'text_area', "height": 80},
    {"key": '느낀점', "label": '느낀 점', "type": 'text_area', "height": 80},
]

_GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]})"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR','Segoe UI',sans-serif;background:#0b1120;color:#e2e8f0;padding:12px;font-size:15px;min-height:100vh}
.ftabs{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:16px}
.ftab{padding:7px 14px;border-radius:20px;border:2px solid #1e293b;background:#1a2236;color:#64748b;cursor:pointer;font-size:.78rem;transition:all .2s;user-select:none}
.ftab:hover{border-color:#334155;color:#94a3b8}
.ftab.active{border-color:#06b6d4;background:#0c2e3e;color:#a5f3fc;font-weight:700}
.ftab.done{border-color:#10b981!important;background:#032017!important;color:#6ee7b7!important}
.ftab.done::before{content:'\2713 '}
.panel{display:none}.panel.active{display:block}
.card{background:#111827;border:1px solid #1e293b;border-radius:14px;padding:16px;margin-bottom:14px}
.card-title{font-size:1rem;font-weight:700;color:#7dd3fc;margin-bottom:12px}
.formula-box{background:#0c1830;border:1px solid #1e3a5f;border-radius:10px;padding:12px 18px;font-size:1.1rem;text-align:center;margin-bottom:14px}
.tile-workspace{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap;margin-bottom:14px}
.tile-pool{background:#0f172a;border:2px dashed #334155;border-radius:12px;padding:10px;min-width:150px;min-height:80px}
.tile-pool-title{font-size:.75rem;color:#64748b;margin-bottom:8px;font-weight:600}
.tile-pool .tiles-row{display:flex;flex-wrap:wrap;gap:6px}
.tile{padding:6px 10px;border-radius:8px;font-size:.78rem;font-weight:700;cursor:grab;user-select:none;transition:all .15s;display:inline-flex;align-items:center;justify-content:center;border:2px solid transparent;min-width:44px;text-align:center}
.tile:active{cursor:grabbing;transform:scale(1.1)}
.tile.dragging{opacity:.5}
.tile-x2{background:#1e3a5f;border-color:#3b82f6;color:#bfdbfe}
.tile-abx{background:#1c3a2e;border-color:#10b981;color:#6ee7b7}
.tile-b2{background:#2d1b4e;border-color:#8b5cf6;color:#c4b5fd}
.tile-neg{opacity:.7}
.tile-unit{background:#2d2a1b;border-color:#f59e0b;color:#fde68a}
.grid-cell{width:48px;height:48px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:.7rem;color:#fff;font-weight:700;cursor:pointer;transition:all .15s}
.grid-cell.empty{background:#0f172a;border:2px dashed #334155}
.grid-cell.empty:hover{border-color:#06b6d4;background:#0c2a3a}
.grid-cell.placed{cursor:default}
.placed.tile-x2{background:#1e3a5f;border:2px solid #60a5fa}
.placed.tile-abx{background:#1c3a2e;border:2px solid #34d399}
.placed.tile-b2{background:#2d1b4e;border:2px solid #a78bfa}
.placed.tile-neg{opacity:.75}
.placed.tile-unit{background:#2d2a1b;border:2px solid #fbbf24}
.hint-btn,.check-btn,.reset-btn{padding:7px 18px;border:none;border-radius:8px;cursor:pointer;font-size:.82rem;font-weight:600;transition:all .2s;margin-right:6px;margin-bottom:6px}
.check-btn{background:#0e7490;color:#fff}.check-btn:hover{background:#0891b2}
.hint-btn{background:#1c3a2e;color:#6ee7b7;border:1px solid #10b981}
.reset-btn{background:#2d1b1b;color:#fca5a5;border:1px solid #dc2626}
.msg-box{padding:12px 16px;border-radius:10px;font-size:.9rem;margin-top:10px;display:none}
.msg-box.show{display:block}
.msg-success{background:#032017;border:1px solid #10b981;color:#6ee7b7}
.msg-error{background:#1b0808;border:1px solid #dc2626;color:#fca5a5}
.msg-hint{background:#1c2a3e;border:1px solid #3b82f6;color:#93c5fd}
.prog-bar-wrap{margin-bottom:14px}
.prog-track{height:6px;background:#1e293b;border-radius:99px;overflow:hidden;margin-top:4px}
.prog-fill{height:100%;background:linear-gradient(90deg,#06b6d4,#7c3aed);border-radius:99px;transition:width .5s}
.prog-lbl{font-size:.72rem;color:#64748b;display:flex;justify-content:space-between;margin-top:2px}
.scene{width:260px;height:260px;perspective:800px;margin:0 auto;cursor:grab}
.scene:active{cursor:grabbing}
.cube-wrap{width:260px;height:260px;position:relative;transform-style:preserve-3d;transform-origin:130px 130px 0}
.cube-block{position:absolute;width:0;height:0;transform-style:preserve-3d}
.face{position:absolute;display:flex;align-items:center;justify-content:center;font-size:.65rem;font-weight:700;backface-visibility:visible;opacity:.88;border-radius:3px}
.cube-controls{display:flex;gap:8px;justify-content:center;margin-top:10px;flex-wrap:wrap}
.cube-controls button{padding:5px 12px;border-radius:6px;border:1px solid #334155;background:#1a2236;color:#94a3b8;cursor:pointer;font-size:.75rem}
.cube-controls button:hover{background:#0c2e3e;color:#a5f3fc}
.parts-list{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.part-badge{padding:5px 12px;border-radius:6px;font-size:.78rem;font-weight:700;cursor:pointer;transition:all .2s;border:1px solid transparent;color:#fff}
.part-badge:hover{filter:brightness(1.3)}
@media(max-width:600px){.tile-workspace{flex-direction:column}.scene{width:200px;height:200px}}
</style>
</head>
<body>

<div class="prog-bar-wrap">
  <div class="prog-lbl"><span>진행도</span><span id="prog-text">0 / 8 완료</span></div>
  <div class="prog-track"><div class="prog-fill" id="prog-fill" style="width:0%"></div></div>
</div>

<div class="ftabs" id="ftabs">
  <div class="ftab active" onclick="showTab(0)" id="tab0">① $(a+b)^2$</div>
  <div class="ftab" onclick="showTab(1)" id="tab1">② $(a-b)^2$</div>
  <div class="ftab" onclick="showTab(2)" id="tab2">③ $(a+b)(a-b)$</div>
  <div class="ftab" onclick="showTab(3)" id="tab3">④ $(x+a)(x+b)$</div>
  <div class="ftab" onclick="showTab(4)" id="tab4">⑤ $(ax+b)(cx+d)$</div>
  <div class="ftab" onclick="showTab(5)" id="tab5">⑥ $(a+b+c)^2$</div>
  <div class="ftab" onclick="showTab(6)" id="tab6">⑦ $(a+b)^3$ 3D</div>
  <div class="ftab" onclick="showTab(7)" id="tab7">⑧ $a^3+b^3$ 3D</div>
</div>

<!-- Panel 0 -->
<div class="panel active" id="panel0">
  <div class="card">
    <div class="card-title">중학교 복습 ① — $(a+b)^2$ 탐구</div>
    <div class="formula-box">$(a+b)^2 = (a+b)(a+b) = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">왼쪽 타일 창고에서 타일을 <b>드래그</b>하여 격자에 끌어다 놓으세요. 놓인 타일을 <b>클릭</b>하면 제거됩니다.</p>
    <div class="tile-workspace" id="ws0"></div>
    <div><button class="check-btn" onclick="checkGrid(0)">✔ 확인</button><button class="hint-btn" onclick="showHint(0)">힌트</button><button class="reset-btn" onclick="resetGrid(0)">↺ 초기화</button></div>
    <div class="msg-box" id="msg0"></div>
  </div>
</div>
<!-- Panel 1 -->
<div class="panel" id="panel1">
  <div class="card">
    <div class="card-title">중학교 복습 ② — $(a-b)^2$ 탐구</div>
    <div class="formula-box">$(a-b)^2 = a^2 - 2ab + b^2$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:10px">
      한 변의 길이가 $a$인 정사각형($a^2$)에서 시작합니다.<br>
      오른쪽 세로 띠(폭 $b$, 높이 $a$)와 아래쪽 가로 띠(폭 $a$, 높이 $b$)를 각각 떼어내면 $ab$씩 두 번 빠집니다.<br>
      그런데 오른쪽 아래 모서리 $b^2$은 두 띠에 모두 포함되어 있으므로 <b>한 번 더해</b>줍니다.<br>
      남은 왼쪽 위 $(a{-}b){\times}(a{-}b)$ 정사각형이 바로 $(a-b)^2$입니다.
    </p>
    <div id="aminus-b-svg" style="margin-bottom:14px"></div>
    <div style="background:#0c1830;border:1px solid #1e3a5f;border-radius:10px;padding:12px 18px;font-size:.95rem;margin-bottom:12px">
      <div style="color:#7dd3fc;font-weight:700;margin-bottom:8px">넓이로 유도하기</div>
      <div id="ab2-step1" style="margin-bottom:6px;cursor:pointer;padding:6px 10px;border-radius:6px;border:1px solid #1e293b" onclick="highlightAB2(1)">
        ① 한 변 $a$인 정사각형 <span id="s1-badge" style="background:#1e3a5f;border:1px solid #3b82f6;border-radius:4px;padding:2px 8px;font-size:.85rem">$a^2$</span> 에서 시작
      </div>
      <div id="ab2-step2" style="margin-bottom:6px;cursor:pointer;padding:6px 10px;border-radius:6px;border:1px solid #1e293b" onclick="highlightAB2(2)">
        ② 오른쪽 세로 띠(폭 $b$, 높이 $a$) <span style="background:#1c3a2e;border:1px solid #10b981;border-radius:4px;padding:2px 8px;font-size:.85rem">$-ab$</span> 제거 → $a^2 - ab$
      </div>
      <div id="ab2-step3" style="margin-bottom:6px;cursor:pointer;padding:6px 10px;border-radius:6px;border:1px solid #1e293b" onclick="highlightAB2(3)">
        ③ 아래쪽 가로 띠(폭 $a$, 높이 $b$) <span style="background:#1c3a2e;border:1px solid #10b981;border-radius:4px;padding:2px 8px;font-size:.85rem">$-ab$</span> 제거 → $a^2 - 2ab$
      </div>
      <div id="ab2-step4" style="cursor:pointer;padding:6px 10px;border-radius:6px;border:1px solid #1e293b" onclick="highlightAB2(4)">
        ④ 두 번 빠진 모서리 <span style="background:#2d1b4e;border:1px solid #8b5cf6;border-radius:4px;padding:2px 8px;font-size:.85rem">$b^2$</span> 보충 → $(a-b)^2 = a^2 - 2ab + b^2$
      </div>
    </div>
    <div><button class="check-btn" onclick="checkAB2()">✔ 공식 확인</button><button class="hint-btn" onclick="highlightAB2(0)">전체 보기</button></div>
    <div class="msg-box" id="msg1"></div>
  </div>
</div>
<!-- Panel 2 -->
<div class="panel" id="panel2">
  <div class="card">
    <div class="card-title">중학교 복습 ③ — $(a+b)(a-b)$ 탐구</div>
    <div class="formula-box">$(a+b)(a-b) = a^2 - b^2$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:10px">
      한 변의 길이가 $a$인 정사각형($a^2$)에서 오른쪽 아래 $b{\times}b$ 정사각형($b^2$)을 제거하면 L자 도형이 남습니다.<br>
      L자 도형을 가로선으로 자른 뒤 아래쪽 조각을 90° 회전하여 오른쪽에 붙이면,<br>
      가로 $(a+b)$, 세로 $(a-b)$인 직사각형 — 즉 $(a+b)(a-b) = a^2-b^2$이 됩니다.
    </p>
    <div id="aplusb-aminus-svg" style="margin-bottom:14px"></div>
    <div style="background:#0c1830;border:1px solid #1e3a5f;border-radius:10px;padding:12px 18px;font-size:.95rem;margin-bottom:12px">
      <div style="color:#7dd3fc;font-weight:700;margin-bottom:8px">넓이로 유도하기</div>
      <div id="ab-diff-step1" style="margin-bottom:6px;cursor:pointer;padding:6px 10px;border-radius:6px;border:1px solid #1e293b" onclick="highlightDiff(1)">
        ① 한 변 $a$인 정사각형 <span style="background:#1e3a5f;border:1px solid #3b82f6;border-radius:4px;padding:2px 8px;font-size:.85rem">$a^2$</span> 에서 시작
      </div>
      <div id="ab-diff-step2" style="margin-bottom:6px;cursor:pointer;padding:6px 10px;border-radius:6px;border:1px solid #1e293b" onclick="highlightDiff(2)">
        ② 오른쪽 아래 <span style="background:#2d1b4e;border:1px solid #8b5cf6;border-radius:4px;padding:2px 8px;font-size:.85rem">$b^2$</span> 제거 → L자형, 가로선으로 분할
      </div>
      <div id="ab-diff-step3" style="cursor:pointer;padding:6px 10px;border-radius:6px;border:1px solid #1e293b" onclick="highlightDiff(3)">
        ③ 아래쪽 조각 90° 회전하여 붙이기 → 가로 $(a+b)$, 세로 $(a-b)$ 직사각형
      </div>
    </div>
    <div><button class="check-btn" onclick="checkDiff()">✔ 공식 확인</button><button class="hint-btn" onclick="highlightDiff(0)">전체 보기</button></div>
    <div class="msg-box" id="msg2"></div>
  </div>
</div>
<!-- Panel 3 -->
<div class="panel" id="panel3">
  <div class="card">
    <div class="card-title">중학교 복습 ④ — $(x+a)(x+b)$ 탐구</div>
    <div class="formula-box">$(x+a)(x+b) = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">가로 $(x+a)$, 세로 $(x+b)$인 직사각형을 채워보세요.</p>
    <div class="tile-workspace" id="ws3"></div>
    <div><button class="check-btn" onclick="checkGrid(3)">✔ 확인</button><button class="hint-btn" onclick="showHint(3)">힌트</button><button class="reset-btn" onclick="resetGrid(3)">↺ 초기화</button></div>
    <div class="msg-box" id="msg3"></div>
  </div>
</div>
<!-- Panel 4 -->
<div class="panel" id="panel4">
  <div class="card">
    <div class="card-title">중학교 복습 ⑤ — $(ax+b)(cx+d)$ 탐구</div>
    <div class="formula-box">$(ax+b)(cx+d) = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">가로 $(ax+b)$, 세로 $(cx+d)$인 직사각형을 채워보세요.</p>
    <div class="tile-workspace" id="ws4"></div>
    <div><button class="check-btn" onclick="checkGrid(4)">✔ 확인</button><button class="hint-btn" onclick="showHint(4)">힌트</button><button class="reset-btn" onclick="resetGrid(4)">↺ 초기화</button></div>
    <div class="msg-box" id="msg4"></div>
  </div>
</div>
<!-- Panel 5 -->
<div class="panel" id="panel5">
  <div class="card">
    <div class="card-title">새 공식 ① — $(a+b+c)^2$ 탐구</div>
    <div class="formula-box">$(a+b+c)^2 = (a+b+c)(a+b+c) = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">가로·세로 모두 $(a+b+c)$인 3×3 정사각형을 채워보세요.</p>
    <div class="tile-workspace" id="ws5"></div>
    <div><button class="check-btn" onclick="checkGrid(5)">✔ 확인</button><button class="hint-btn" onclick="showHint(5)">힌트</button><button class="reset-btn" onclick="resetGrid(5)">↺ 초기화</button></div>
    <div class="msg-box" id="msg5"></div>
  </div>
</div>
<!-- Panel 6 -->
<div class="panel" id="panel6">
  <div class="card">
    <div class="card-title">입체 신공식 ② — $(a+b)^3$ 탐구</div>
    <div class="formula-box">$(a+b)^3 = \;?$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:12px">한 변이 $(a+b)$인 정육면체를 8개 조각으로 나눠보세요. 드래그로 회전, 조각 클릭하면 강조됩니다.</p>
    <div style="display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start">
      <div style="flex:0 0 240px">
        <div style="font-size:.85rem;color:#7dd3fc;font-weight:700;margin-bottom:8px">8개 조각 (클릭하면 강조)</div>
        <div class="parts-list" id="parts6"></div>
        <div class="msg-box" id="msg6" style="margin-top:12px"></div>
        <div style="margin-top:12px">
          <button class="check-btn" onclick="checkCube(6)">✔ 공식 확인</button>
          <button class="reset-btn" onclick="resetCubeHL(6)">↺ 강조 해제</button>
        </div>
      </div>
      <div>
        <div class="scene" id="scene6"><div class="cube-wrap" id="cubeWrap6"></div></div>
        <div class="cube-controls">
          <button onclick="rotateCube(6,-30,0)">◀</button>
          <button onclick="rotateCube(6,30,0)">▶</button>
          <button onclick="rotateCube(6,0,-30)">▲</button>
          <button onclick="rotateCube(6,0,30)">▼</button>
          <button onclick="resetCubeRot(6)">↺</button>
        </div>
      </div>
    </div>
  </div>
</div>
<!-- Panel 7 -->
<div class="panel" id="panel7">
  <div class="card">
    <div class="card-title">입체 신공식 ③ — $a^3+b^3$ 인수분해 탐구</div>
    <div class="formula-box">$a^3 + b^3 = (a+b)(a^2-ab+b^2)$</div>
    <p style="font-size:.82rem;color:#94a3b8;margin-bottom:10px">
      한 변의 길이가 $(a+b)$인 정육면체$(=(a+b)^3)$에서 시작합니다.<br>
      $3a^2b$ 조각 3개와 $3ab^2$ 조각 3개를 차례로 제거하면 $a^3$과 $b^3$만 남습니다.<br>
      이를 인수분해하면 $a^3+b^3 = (a+b)(a^2-ab+b^2)$이 됩니다.
    </p>
    <div style="background:#0c1830;border:1px solid #1e3a5f;border-radius:10px;padding:12px 18px;font-size:.95rem;margin-bottom:12px">
      <div style="color:#7dd3fc;font-weight:700;margin-bottom:8px">$a^3+b^3$ 유도하기</div>
      <div id="c7-step1" style="margin-bottom:6px;cursor:pointer;padding:6px 10px;border-radius:6px;border:1px solid #1e293b" onclick="stepHL7(1)">
        ① 한 변 $(a+b)$인 정육면체 <span style="background:#1e3a5f;border:1px solid #3b82f6;border-radius:4px;padding:2px 8px;font-size:.85rem">$(a+b)^3$</span> 전체 = $a^3+3a^2b+3ab^2+b^3$
      </div>
      <div id="c7-step2" style="margin-bottom:6px;cursor:pointer;padding:6px 10px;border-radius:6px;border:1px solid #1e293b" onclick="stepHL7(2)">
        ② <span style="background:#1c3a2e;border:1px solid #10b981;border-radius:4px;padding:2px 8px;font-size:.85rem">$a^2b$</span> 조각 3개 제거 → $a^3+3ab^2+b^3$
      </div>
      <div id="c7-step3" style="margin-bottom:6px;cursor:pointer;padding:6px 10px;border-radius:6px;border:1px solid #1e293b" onclick="stepHL7(3)">
        ③ <span style="background:#2d1b4e;border:1px solid #8b5cf6;border-radius:4px;padding:2px 8px;font-size:.85rem">$ab^2$</span> 조각 3개 제거 → $a^3+b^3$
      </div>
      <div id="c7-step4" style="cursor:pointer;padding:6px 10px;border-radius:6px;border:1px solid #1e293b" onclick="stepHL7(4)">
        ④ 남은 <span style="background:#1e3a5f;border:1px solid #3b82f6;border-radius:4px;padding:2px 8px;font-size:.85rem">$a^3$</span>과 <span style="background:#2d2a1b;border:1px solid #f59e0b;border-radius:4px;padding:2px 8px;font-size:.85rem">$b^3$</span> 만 남음<br>
        <div style="margin-top:8px;padding:8px 12px;background:#0a1628;border-radius:6px;font-size:.82rem;line-height:1.9">
          $a^3+b^3$<br>
          $= (a+b)^3 - 3a^2b - 3ab^2$<br>
          $= (a+b)^3 - 3ab(a+b)$<br>
          $= (a+b)\bigl[(a+b)^2 - 3ab\bigr]$<br>
          $= (a+b)(a^2+2ab+b^2-3ab)$<br>
          $= \boldsymbol{(a+b)(a^2-ab+b^2)}$
        </div>
      </div>
    </div>
    <div style="display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start">
      <div style="flex:0 0 240px">
        <div style="font-size:.85rem;color:#7dd3fc;font-weight:700;margin-bottom:8px">조각 목록 (클릭시 강조)</div>
        <div class="parts-list" id="parts7"></div>
        <div class="msg-box" id="msg7" style="margin-top:12px"></div>
        <div style="margin-top:12px">
          <button class="check-btn" onclick="checkCube(7)">✔ 공식 확인</button>
          <button class="reset-btn" onclick="resetCubeHL(7)">↺ 강조 해제</button>
        </div>
      </div>
      <div>
        <div class="scene" id="scene7"><div class="cube-wrap" id="cubeWrap7"></div></div>
        <div class="cube-controls">
          <button onclick="rotateCube(7,-30,0)">◀</button>
          <button onclick="rotateCube(7,30,0)">▶</button>
          <button onclick="rotateCube(7,0,-30)">▲</button>
          <button onclick="rotateCube(7,0,30)">▼</button>
          <button onclick="resetCubeRot(7)">↺</button>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
// ── 공식 데이터 ──
const FDATA = [
  {cols:2,rows:2,cL:['a','b'],rL:['a','b'],
   pool:[{type:'tile-x2',tex:'a^2',cnt:1},{type:'tile-abx',tex:'ab',cnt:2},{type:'tile-b2',tex:'b^2',cnt:1}],
   ans:[['tile-x2','tile-abx'],['tile-abx','tile-b2']],
   result:'(a+b)^2 = a^2 + 2ab + b^2',
   hint:'좌상: a², 우상: ab, 좌하: ab, 우하: b²'},
  {cols:2,rows:2,cL:['a','(-b)'],rL:['a','(-b)'],
   pool:[{type:'tile-x2',tex:'a^2',cnt:1},{type:'tile-abx tile-neg',tex:'-ab',cnt:2},{type:'tile-b2',tex:'b^2',cnt:1}],
   ans:[['tile-x2','tile-abx tile-neg'],['tile-abx tile-neg','tile-b2']],
   result:'(a-b)^2 = a^2 - 2ab + b^2',
   hint:'(-b)×a = -ab, a×(-b) = -ab. (-b)×(-b) = b² (양수!)'},
  {cols:2,rows:2,cL:['a','b'],rL:['a','(-b)'],
   pool:[{type:'tile-x2',tex:'a^2',cnt:1},{type:'tile-abx',tex:'ab',cnt:1},{type:'tile-abx tile-neg',tex:'-ab',cnt:1},{type:'tile-b2 tile-neg',tex:'-b^2',cnt:1}],
   ans:[['tile-x2','tile-abx'],['tile-abx tile-neg','tile-b2 tile-neg']],
   result:'(a+b)(a-b) = a^2 - b^2',
   hint:'ab와 -ab가 서로 상쇄돼서 a²-b²만 남아요!'},
  {cols:2,rows:2,cL:['x','a'],rL:['x','b'],
   pool:[{type:'tile-x2',tex:'x^2',cnt:1},{type:'tile-abx',tex:'ax',cnt:1},{type:'tile-abx',tex:'bx',cnt:1},{type:'tile-unit',tex:'ab',cnt:1}],
   ans:[['tile-x2','tile-abx'],['tile-abx','tile-unit']],
   result:'(x+a)(x+b) = x^2 + (a+b)x + ab',
   hint:'좌상: x², 우상: ax, 좌하: bx, 우하: ab'},
  {cols:2,rows:2,cL:['ax','b'],rL:['cx','d'],
   pool:[{type:'tile-x2',tex:'acx^2',cnt:1},{type:'tile-abx',tex:'adx',cnt:1},{type:'tile-abx',tex:'bcx',cnt:1},{type:'tile-unit',tex:'bd',cnt:1}],
   ans:[['tile-x2','tile-abx'],['tile-abx','tile-unit']],
   result:'(ax+b)(cx+d) = acx^2 + (ad+bc)x + bd',
   hint:'(cx)(ax)=acx², d·ax=adx, (cx)b=bcx, d·b=bd'},
  {cols:3,rows:3,cL:['a','b','c'],rL:['a','b','c'],
   pool:[{type:'tile-x2',tex:'a^2',cnt:1},{type:'tile-x2',tex:'b^2',cnt:1},{type:'tile-x2',tex:'c^2',cnt:1},
         {type:'tile-abx',tex:'ab',cnt:2},{type:'tile-abx',tex:'bc',cnt:2},{type:'tile-b2',tex:'ca',cnt:2}],
   ans:[['tile-x2','tile-abx','tile-b2'],['tile-abx','tile-x2','tile-abx'],['tile-b2','tile-abx','tile-x2']],
   result:'(a+b+c)^2 = a^2+b^2+c^2+2ab+2bc+2ca',
   hint:'대각선: a², b², c². 나머지는 두 변수의 곱 (각 2개씩)'},
];

// ── 상태 ──
const gS = {}, pC = {};

function initState(fi) {
  const f = FDATA[fi];
  if (!gS[fi]) {
    gS[fi] = Array.from({length:f.rows}, () => new Array(f.cols).fill(null));
    pC[fi] = f.pool.map(p => p.cnt);
  }
}

// ── 격자 빌드 ──
function buildGrid(fi) {
  const f = FDATA[fi]; initState(fi);
  const ws = document.getElementById('ws' + fi); ws.innerHTML = '';
  // 타일 창고
  const poolDiv = document.createElement('div'); poolDiv.className = 'tile-pool';
  poolDiv.innerHTML = '<div class="tile-pool-title">타일 창고</div><div class="tiles-row" id="pr' + fi + '"></div>';
  ws.appendChild(poolDiv);
  // 격자
  const table = document.createElement('div');
  table.style.cssText = 'display:inline-grid;gap:3px;grid-template-columns:auto ' + ('48px '.repeat(f.cols)).trim();
  const corner = document.createElement('div'); corner.style.cssText = 'width:36px;height:36px'; table.appendChild(corner);
  f.cL.forEach(l => {
    const d = document.createElement('div');
    d.style.cssText = 'width:48px;height:36px;display:flex;align-items:center;justify-content:center;color:#fbbf24;font-weight:700;font-size:.82rem';
    d.innerHTML = katex.renderToString(l, {throwOnError:false}); table.appendChild(d);
  });
  for (let r = 0; r < f.rows; r++) {
    const rl = document.createElement('div');
    rl.style.cssText = 'width:36px;display:flex;align-items:center;justify-content:center;color:#fbbf24;font-weight:700;font-size:.82rem';
    rl.innerHTML = katex.renderToString(f.rL[r], {throwOnError:false}); table.appendChild(rl);
    for (let c = 0; c < f.cols; c++) {
      const cell = document.createElement('div'); cell.id = 'cell-' + fi + '-' + r + '-' + c;
      cell.dataset.fi = fi; cell.dataset.r = r; cell.dataset.c = c;
      const placed = gS[fi][r][c];
      if (placed) setCellPlaced(cell, fi, r, c, placed); else cell.className = 'grid-cell empty';
      cell.addEventListener('dragover', e => { e.preventDefault(); if (!gS[fi][r][c]) cell.style.borderColor = '#06b6d4'; });
      cell.addEventListener('dragleave', () => { if (!gS[fi][r][c]) cell.style.borderColor = ''; });
      cell.addEventListener('drop', e => { e.preventDefault(); cell.style.borderColor = ''; doDropOnCell(fi, r, c, JSON.parse(e.dataTransfer.getData('text/plain'))); });
      cell.addEventListener('click', () => { if (gS[fi][r][c]) removeFromCell(fi, r, c); });
      table.appendChild(cell);
    }
  }
  ws.appendChild(table);
  renderPool(fi);
}

function renderPool(fi) {
  const f = FDATA[fi]; const row = document.getElementById('pr' + fi);
  if (!row) return; row.innerHTML = '';
  f.pool.forEach((item, pi) => {
    const rem = pC[fi][pi];
    for (let i = 0; i < rem; i++) {
      const tile = document.createElement('div'); tile.className = 'tile ' + item.type;
      tile.innerHTML = katex.renderToString(item.tex, {throwOnError:false});
      tile.draggable = true; tile.dataset.pi = pi; tile.dataset.fi = fi; tile.dataset.type = item.type;
      tile.addEventListener('dragstart', e => { tile.classList.add('dragging'); e.dataTransfer.setData('text/plain', JSON.stringify({pi, fi, type:item.type, tex:item.tex})); });
      tile.addEventListener('dragend', () => tile.classList.remove('dragging'));
      tile.addEventListener('touchstart', touchStart, {passive:false});
      row.appendChild(tile);
    }
    if (rem === 0) {
      const ph = document.createElement('div'); ph.className = 'tile ' + item.type; ph.style.opacity = '.18';
      ph.innerHTML = katex.renderToString(item.tex, {throwOnError:false}); row.appendChild(ph);
    }
  });
}

function doDropOnCell(fi, r, c, data) {
  if (gS[fi][r][c]) returnToPool(fi, gS[fi][r][c]);
  pC[fi][data.pi]--; gS[fi][r][c] = data.type;
  const cell = document.getElementById('cell-' + fi + '-' + r + '-' + c);
  setCellPlaced(cell, fi, r, c, data.type); renderPool(fi);
}

function setCellPlaced(cell, fi, r, c, type) {
  cell.className = 'grid-cell placed ' + type;
  const item = FDATA[fi].pool.find(p => p.type === type);
  cell.innerHTML = katex.renderToString(item ? item.tex : '?', {throwOnError:false});
  cell.title = '클릭해서 제거';
}

function removeFromCell(fi, r, c) {
  returnToPool(fi, gS[fi][r][c]); gS[fi][r][c] = null;
  const cell = document.getElementById('cell-' + fi + '-' + r + '-' + c);
  cell.className = 'grid-cell empty'; cell.innerHTML = ''; cell.title = ''; renderPool(fi);
}

function returnToPool(fi, type) {
  const idx = FDATA[fi].pool.findIndex(p => p.type === type); if (idx !== -1) pC[fi][idx]++;
}

// ── 확인 / 힌트 / 초기화 ──
function checkGrid(fi) {
  const f = FDATA[fi]; let allFilled = true, allOk = true;
  for (let r = 0; r < f.rows; r++) for (let c = 0; c < f.cols; c++) {
    const placed = gS[fi][r][c], exp = f.ans[r][c];
    const cell = document.getElementById('cell-' + fi + '-' + r + '-' + c);
    if (!placed) { allFilled = false; continue; }
    if (placed === exp) cell.style.outline = '2px solid #10b981';
    else { cell.style.outline = '2px solid #ef4444'; allOk = false; }
  }
  const msg = document.getElementById('msg' + fi); msg.className = 'msg-box show';
  if (!allFilled) { msg.className = 'msg-box msg-hint show'; msg.innerHTML = '⚠ 빈 칸이 있어요!'; return; }
  if (allOk) {
    msg.className = 'msg-box msg-success show';
    msg.innerHTML = '정답! ' + katex.renderToString(f.result, {throwOnError:false});
    document.getElementById('tab' + fi).classList.add('done'); updateProg();
  } else {
    msg.className = 'msg-box msg-error show';
    msg.innerHTML = '✗ 틀린 칸이 있어요 (빨간 테두리 확인)';
  }
}

function showHint(fi) {
  const msg = document.getElementById('msg' + fi); msg.className = 'msg-box msg-hint show';
  msg.innerHTML = '💡 ' + FDATA[fi].hint;
}

function resetGrid(fi) {
  const f = FDATA[fi]; gS[fi] = Array.from({length:f.rows}, () => new Array(f.cols).fill(null)); pC[fi] = f.pool.map(p => p.cnt);
  buildGrid(fi); document.getElementById('msg' + fi).className = 'msg-box';
}

// ── 3D 정육면체 ──
const CUBE_PARTS = {
  6: [{key:'a3', label:'a^3', color:'#1e3a5f', border:'#3b82f6', count:1},
      {key:'a2b',label:'a^2b',color:'#1c3a2e', border:'#10b981', count:3},
      {key:'ab2',label:'ab^2',color:'#2d1b4e', border:'#8b5cf6', count:3},
      {key:'b3', label:'b^3', color:'#2d2a1b', border:'#f59e0b', count:1}],
  7: [{key:'a3', label:'a^3', color:'#1e3a5f', border:'#3b82f6', count:1, keep:true},
      {key:'a2b',label:'a^2b',color:'#1c3a2e',border:'#10b981', count:3, keep:false},
      {key:'ab2',label:'ab^2',color:'#2d1b4e',border:'#8b5cf6', count:3, keep:false},
      {key:'b3', label:'b^3', color:'#2d2a1b', border:'#f59e0b', count:1, keep:true}],
};
const cubeRot = {6:{x:30,y:-20}, 7:{x:30,y:-20}};

function buildCube(idx, wrapId) {
  const wrap = document.getElementById(wrapId); wrap.innerHTML = '';
  const A = 76, B = 44, dims = [A,B], offs = [0,A], total = A+B;
  const parts = CUBE_PARTS[idx];
  for (let ix = 0; ix < 2; ix++) for (let iy = 0; iy < 2; iy++) for (let iz = 0; iz < 2; iz++) {
    const bc = ix + iy + iz; const part = parts[bc];
    const bk = document.createElement('div'); bk.className = 'cube-block'; bk.dataset.key = part.key;
    const w=dims[ix], h=dims[iy], d=dims[iz], ox=offs[ix], oy=offs[iy], oz=offs[iz], cx=total/2, cy=total/2, cz=total/2;
    bk.style.cssText = 'position:absolute;width:0;height:0;transform-style:preserve-3d;left:' + cx + 'px;top:' + cy + 'px;transform:translate3d(' + (ox-cx) + 'px,' + (oy-cy) + 'px,' + (oz-cz) + 'px)';
    bk.addEventListener('click', () => hlPart(idx, part.key));
    [{fw:w,fh:h,tx:0,ty:0,tz:d/2,rx:0,ry:0,lbl:true},
     {fw:w,fh:h,tx:0,ty:0,tz:-d/2,rx:0,ry:180,lbl:true},
     {fw:d,fh:h,tx:-w/2,ty:0,tz:0,rx:0,ry:-90,lbl:true},
     {fw:d,fh:h,tx:w/2,ty:0,tz:0,rx:0,ry:90,lbl:true},
     {fw:w,fh:d,tx:0,ty:-h/2,tz:0,rx:-90,ry:0,lbl:true},
     {fw:w,fh:d,tx:0,ty:h/2,tz:0,rx:90,ry:0,lbl:true}].forEach(fd => {
      const face = document.createElement('div'); face.className = 'face';
      face.style.cssText = 'width:' + fd.fw + 'px;height:' + fd.fh + 'px;margin-left:' + (-fd.fw/2) + 'px;margin-top:' + (-fd.fh/2) + 'px;background:' + part.color + ';border:1px solid ' + part.border + ';transform:translate3d(' + fd.tx + 'px,' + fd.ty + 'px,' + fd.tz + 'px) rotateY(' + fd.ry + 'deg) rotateX(' + fd.rx + 'deg)';
      if (fd.lbl) face.innerHTML = katex.renderToString(part.label, {throwOnError:false});
      bk.appendChild(face);
    });
    wrap.appendChild(bk);
  }
  applyCubeRot(idx);
}

function applyCubeRot(idx) { const w = document.getElementById('cubeWrap' + idx); const r = cubeRot[idx]; w.style.transform = 'rotateX(' + r.x + 'deg) rotateY(' + r.y + 'deg)'; }
function rotateCube(idx, dy, dx) { cubeRot[idx].y += dy; cubeRot[idx].x += dx; applyCubeRot(idx); }
function resetCubeRot(idx) { cubeRot[idx] = {x:30, y:-20}; applyCubeRot(idx); }

let dragPtr = null;
function initDrag(sceneId, idx) {
  const el = document.getElementById(sceneId);
  el.addEventListener('pointerdown', e => { dragPtr = {x:e.clientX, y:e.clientY}; el.setPointerCapture(e.pointerId); });
  el.addEventListener('pointermove', e => { if (!dragPtr) return; cubeRot[idx].y += (e.clientX - dragPtr.x) * 0.6; cubeRot[idx].x += (e.clientY - dragPtr.y) * 0.4; dragPtr = {x:e.clientX, y:e.clientY}; applyCubeRot(idx); });
  el.addEventListener('pointerup', () => { dragPtr = null; });
}

function hlPart(idx, key) { document.querySelectorAll('#cubeWrap' + idx + ' .cube-block').forEach(b => { b.style.filter = b.dataset.key === key ? 'brightness(2) drop-shadow(0 0 8px #fff)' : 'brightness(.35)'; }); }
function resetCubeHL(idx) {
  document.querySelectorAll('#cubeWrap' + idx + ' .cube-block').forEach(b => b.style.filter = '');
  document.getElementById('msg' + idx).className = 'msg-box';
  if (idx === 7) {
    [1,2,3,4].forEach(s => {
      const el = document.getElementById('c7-step' + s);
      if(el) { el.style.background = ''; el.style.borderColor = '#1e293b'; }
    });
  }
}

function buildPartBadges(idx) {
  const con = document.getElementById('parts' + idx); con.innerHTML = '';
  CUBE_PARTS[idx].forEach(p => {
    const badge = document.createElement('div'); badge.className = 'part-badge';
    badge.style.cssText = 'background:' + p.color + ';border-color:' + p.border;
    badge.innerHTML = katex.renderToString(p.label, {throwOnError:false});
    if (p.count > 1) badge.innerHTML += ' <small style="opacity:.7">×' + p.count + '</small>';
    if (idx === 7 && p.keep === false) badge.style.opacity = '.55';
    badge.addEventListener('click', () => hlPart(idx, p.key));
    con.appendChild(badge);
  });
  if (idx === 7) {
    const note = document.createElement('div'); note.style.cssText = 'font-size:.75rem;color:#94a3b8;margin-top:8px';
    note.textContent = '연한 조각은 상쇄되므로 a³+b³만 남아요.'; con.appendChild(note);
  }
}

function checkCube(idx) {
  const r = {6:'(a+b)^3=a^3+3a^2b+3ab^2+b^3', 7:'a^3+b^3=(a+b)(a^2-ab+b^2)'};
  const n = {6:'8조각: a³(×1)+a²b(×3)+ab²(×3)+b³(×1)', 7:'a²b와 ab²항들이 상쇄되어 a³+b³=(a+b)(a²-ab+b²)'};
  const msg = document.getElementById('msg' + idx);
  msg.className = 'msg-box msg-success show';
  msg.innerHTML = '정답! ' + katex.renderToString(r[idx], {throwOnError:false}) + '<br><small style="color:#6ee7b7;font-size:.75rem">' + n[idx] + '</small>';
  document.getElementById('tab' + idx).classList.add('done'); updateProg();
}

// ── 터치 드래그 ──
let tData = null, tGhost = null;
function touchStart(e) {
  const t = e.currentTarget;
  tData = {pi:+t.dataset.pi, fi:+t.dataset.fi, type:t.dataset.type, tex:FDATA[+t.dataset.fi].pool[+t.dataset.pi].tex};
  e.preventDefault();
}
document.addEventListener('touchmove', e => {
  if (!tData) return; e.preventDefault();
  if (!tGhost) { tGhost = document.createElement('div'); tGhost.style.cssText = 'position:fixed;pointer-events:none;z-index:999;background:#1e3a5f;border-radius:8px;padding:8px;color:#fff;font-size:.8rem;opacity:.85'; tGhost.textContent = '★'; document.body.appendChild(tGhost); }
  tGhost.style.left = (e.touches[0].clientX + 12) + 'px'; tGhost.style.top = (e.touches[0].clientY + 12) + 'px';
}, {passive:false});
document.addEventListener('touchend', e => {
  if (tGhost) { tGhost.remove(); tGhost = null; }
  if (!tData) return;
  const t = e.changedTouches[0]; const el = document.elementFromPoint(t.clientX, t.clientY);
  if (el && el.classList.contains('grid-cell')) { const fi = +el.dataset.fi, r = +el.dataset.r, c = +el.dataset.c; doDropOnCell(fi, r, c, tData); }
  tData = null;
}, {passive:false});

// ── (a-b)² SVG 시각화 ──
function buildAB2Svg() {
  const A = 160, B = 55, pad = 28;
  const aB = A - B; // 105 px = a-b
  const W = A + pad * 2 + 50, H = A + pad * 2 + 42;
  const ox = pad + 24, oy = pad;

  const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
  svg.setAttribute('width', W); svg.setAttribute('height', H);
  svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  svg.style.display = 'block'; svg.style.margin = '0 auto';

  function rect(x,y,w,h,fill,stroke,id,op) {
    const r = document.createElementNS('http://www.w3.org/2000/svg','rect');
    r.setAttribute('x',x); r.setAttribute('y',y);
    r.setAttribute('width',w); r.setAttribute('height',h);
    r.setAttribute('fill',fill); r.setAttribute('stroke',stroke);
    r.setAttribute('stroke-width','2');
    if(id) r.setAttribute('id',id);
    if(op !== undefined) r.setAttribute('opacity',op);
    return r;
  }
  function text(x,y,t,color,size,anchor) {
    const el = document.createElementNS('http://www.w3.org/2000/svg','text');
    el.setAttribute('x',x); el.setAttribute('y',y);
    el.setAttribute('fill', color||'#e2e8f0');
    el.setAttribute('font-size', size||13);
    el.setAttribute('font-family','Noto Sans KR,sans-serif');
    el.setAttribute('text-anchor', anchor||'middle');
    el.setAttribute('dominant-baseline','middle');
    el.textContent = t; return el;
  }
  function line(x1,y1,x2,y2,color,dash) {
    const l = document.createElementNS('http://www.w3.org/2000/svg','line');
    l.setAttribute('x1',x1);l.setAttribute('y1',y1);
    l.setAttribute('x2',x2);l.setAttribute('y2',y2);
    l.setAttribute('stroke',color||'#475569');
    l.setAttribute('stroke-width','1.5');
    if(dash) l.setAttribute('stroke-dasharray','5,3');
    return l;
  }
  function rotText(x,y,t,color) {
    const g = document.createElementNS('http://www.w3.org/2000/svg','g');
    g.setAttribute('transform','translate('+x+','+y+') rotate(-90)');
    const el = document.createElementNS('http://www.w3.org/2000/svg','text');
    el.setAttribute('text-anchor','middle'); el.setAttribute('dominant-baseline','middle');
    el.setAttribute('fill',color||'#e2e8f0'); el.setAttribute('font-size',12);
    el.setAttribute('font-family','Noto Sans KR,sans-serif');
    el.textContent = t; g.appendChild(el); return g;
  }

  const C_TL = '#1e3a5f', C_AB = '#1c3a2e', C_B2 = '#2d1b4e';
  const S_TL = '#3b82f6', S_AB = '#10b981', S_B2 = '#8b5cf6';

  // 4개 영역: a×a 정사각형을 (a-b)/b 분할선으로 나눔
  // 전체 a×a 배경 [파랑] — a² 전체를 파란색으로 표시
  svg.appendChild(rect(ox, oy, A, A, C_TL, S_TL, 'r-bg', 1));
  // 오른쪽위 b×(a-b) — 오른쪽 띠의 위 부분 [초록]
  svg.appendChild(rect(ox+aB, oy, B, aB, C_AB, S_AB, 'r-tr', 0));
  // 왼쪽아래 (a-b)×b — 아래쪽 띠의 왼 부분 [초록]
  svg.appendChild(rect(ox, oy+aB, aB, B, C_AB, S_AB, 'r-bl', 0));
  // 오른쪽아래 b×b — 두 띠 겹침 모서리 [보라]
  svg.appendChild(rect(ox+aB, oy+aB, B, B, C_B2, S_B2, 'r-br', 0));

  // 분할선 (항상 표시)
  svg.appendChild(line(ox+aB, oy, ox+aB, oy+A, '#475569', true));
  svg.appendChild(line(ox, oy+aB, ox+A, oy+aB, '#475569', true));

  // 축 레이블 (가로)
  svg.appendChild(text(ox+aB/2, oy+A+16, 'a-b', '#fbbf24', 12));
  svg.appendChild(text(ox+aB+B/2, oy+A+16, 'b', '#a78bfa', 12));
  svg.appendChild(text(ox+A/2, oy+A+30, '\u2190 a \u2192', '#64748b', 11));
  // 축 레이블 (세로)
  svg.appendChild(rotText(ox-16, oy+aB/2, 'a-b', '#fbbf24'));
  svg.appendChild(rotText(ox-16, oy+aB+B/2, 'b', '#a78bfa'));

  // 내부 레이블 (단계별 표시)
  const lTL = text(ox+aB/2, oy+aB/2, '(a-b)\u00B2', '#93c5fd', 13);
  lTL.setAttribute('id','l-tl'); lTL.setAttribute('opacity',0); svg.appendChild(lTL);
  const lBR = text(ox+aB+B/2, oy+aB+B/2, 'b\u00B2', '#c4b5fd', 12);
  lBR.setAttribute('id','l-br'); lBR.setAttribute('opacity',0); svg.appendChild(lBR);

  // 오른쪽 세로 띠 외곽선 (b×A 전체): 단계 2
  const ovRight = rect(ox+aB, oy, B, A, 'none', '#10b981', 'ov-right', 0);
  ovRight.setAttribute('stroke-dasharray','6,3'); ovRight.setAttribute('stroke-width','2.5');
  svg.appendChild(ovRight);
  const lblRight = text(ox+aB+B/2, oy+A/2, '-ab', '#6ee7b7', 12);
  lblRight.setAttribute('id','lbl-right'); lblRight.setAttribute('opacity',0); svg.appendChild(lblRight);

  // 아래쪽 가로 띠 외곽선 (A×b 전체): 단계 3
  const ovBot = rect(ox, oy+aB, A, B, 'none', '#10b981', 'ov-bot', 0);
  ovBot.setAttribute('stroke-dasharray','6,3'); ovBot.setAttribute('stroke-width','2.5');
  svg.appendChild(ovBot);
  const lblBot = text(ox+A/2, oy+aB+B/2, '-ab', '#6ee7b7', 12);
  lblBot.setAttribute('id','lbl-bot'); lblBot.setAttribute('opacity',0); svg.appendChild(lblBot);

  // b² 모서리 강조 (겹침): 단계 4
  const ovCorner = rect(ox+aB, oy+aB, B, B, 'none', '#f59e0b', 'ov-corner', 0);
  ovCorner.setAttribute('stroke-width','3'); svg.appendChild(ovCorner);
  const lblCorner = text(ox+aB+B+22, oy+aB+B/2, '+b\u00B2', '#fde68a', 12);
  lblCorner.setAttribute('id','lbl-corner'); lblCorner.setAttribute('opacity',0); svg.appendChild(lblCorner);
  // 화살표 (모서리 → "+b²" 레이블)
  const arCorner = document.createElementNS('http://www.w3.org/2000/svg','line');
  arCorner.setAttribute('x1',ox+aB+B); arCorner.setAttribute('y1',oy+aB+B/2);
  arCorner.setAttribute('x2',ox+aB+B+10); arCorner.setAttribute('y2',oy+aB+B/2);
  arCorner.setAttribute('stroke','#f59e0b'); arCorner.setAttribute('stroke-width','1.5');
  arCorner.setAttribute('id','ar-corner'); arCorner.setAttribute('opacity',0); svg.appendChild(arCorner);

  // (a-b)² 답 강조 테두리: 단계 1~
  const ovAns = rect(ox, oy, aB, aB, 'none', '#f59e0b', 'ov-ans', 0);
  ovAns.setAttribute('stroke-width','3'); svg.appendChild(ovAns);

  document.getElementById('aminus-b-svg').appendChild(svg);
}

function setOpacity(id, val) { const el = document.getElementById(id); if(el) el.setAttribute('opacity', val); }

function highlightAB2(step) {
  // 0=전체, 1=a² 시작, 2=오른쪽 띠 -ab, 3=아래 띠 -ab, 4=b² 보충
  // r-bg (전체 a×a 파랑)는 항상 표시
  setOpacity('r-tr', step >= 2 ? 0.85 : 0);
  setOpacity('r-bl', step >= 3 ? 0.85 : 0);
  setOpacity('r-br', step >= 2 ? 1 : 0);
  setOpacity('l-tl', step >= 1 ? 1 : 0);
  setOpacity('l-br', step >= 2 ? 1 : 0);
  setOpacity('ov-right', step >= 2 ? 1 : 0);
  setOpacity('lbl-right', step >= 2 ? 1 : 0);
  setOpacity('ov-bot', step >= 3 ? 1 : 0);
  setOpacity('lbl-bot', step >= 3 ? 1 : 0);
  setOpacity('ov-corner', step >= 4 ? 1 : 0);
  setOpacity('lbl-corner', step >= 4 ? 1 : 0);
  setOpacity('ar-corner', step >= 4 ? 1 : 0);
  setOpacity('ov-ans', step >= 1 ? 1 : 0);
  [1,2,3,4].forEach(s => {
    const el = document.getElementById('ab2-step' + s);
    if(el) el.style.background = (s === step || step === 0) ? '#0c2e3e' : '';
    if(el) el.style.borderColor = (s === step || step === 0) ? '#06b6d4' : '#1e293b';
  });
  if(step === 0) {
    setOpacity('r-tr',0.85); setOpacity('r-bl',0.85); setOpacity('r-br',1);
    setOpacity('l-br',1); setOpacity('l-tl',1);
    setOpacity('ov-right',1); setOpacity('lbl-right',1);
    setOpacity('ov-bot',1); setOpacity('lbl-bot',1);
    setOpacity('ov-corner',1); setOpacity('lbl-corner',1); setOpacity('ar-corner',1);
    setOpacity('ov-ans',1);
  }
}

function checkAB2() {
  const msg = document.getElementById('msg1');
  msg.className = 'msg-box msg-success show';
  msg.innerHTML = '정답! ' + katex.renderToString('(a-b)^2 = a^2 - 2ab + b^2', {throwOnError:false})
    + '<br><small style="color:#6ee7b7;font-size:.78rem">a² 에서 ab×2를 빼고, 중복으로 빠진 b²을 한 번 더해주면 (a-b)²이 됩니다.</small>';
  document.getElementById('tab1').classList.add('done'); updateProg();
}

// ── (a+b)(a-b) SVG 시각화 ──
function buildDiffSvg() {
  const A = 130, B = 42, pad = 28;
  const aB = A - B; // 88 = a-b
  const gap = 52; // 두 도형 사이 간격
  const rx = pad + 20 + A + gap; // 오른쪽 직사각형 시작 x
  const W = rx + (A + B) + pad + 10, H = A + pad * 2 + 36;
  const ox = pad + 20, oy = pad;

  const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
  svg.setAttribute('width', W); svg.setAttribute('height', H);
  svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
  svg.style.display = 'block'; svg.style.margin = '0 auto';

  function rect(x,y,w,h,fill,stroke,id,op) {
    const r = document.createElementNS('http://www.w3.org/2000/svg','rect');
    r.setAttribute('x',x);r.setAttribute('y',y);
    r.setAttribute('width',w);r.setAttribute('height',h);
    r.setAttribute('fill',fill);r.setAttribute('stroke',stroke);
    r.setAttribute('stroke-width','2');
    if(id) r.setAttribute('id',id);
    if(op!==undefined) r.setAttribute('opacity',op);
    return r;
  }
  function text(x,y,t,color,size,anchor) {
    const el = document.createElementNS('http://www.w3.org/2000/svg','text');
    el.setAttribute('x',x);el.setAttribute('y',y);
    el.setAttribute('fill',color||'#e2e8f0');
    el.setAttribute('font-size',size||13);
    el.setAttribute('font-family','Noto Sans KR,sans-serif');
    el.setAttribute('text-anchor',anchor||'middle');
    el.setAttribute('dominant-baseline','middle');
    el.textContent=t; return el;
  }
  function line(x1,y1,x2,y2,color,dash) {
    const l = document.createElementNS('http://www.w3.org/2000/svg','line');
    l.setAttribute('x1',x1);l.setAttribute('y1',y1);
    l.setAttribute('x2',x2);l.setAttribute('y2',y2);
    l.setAttribute('stroke',color||'#475569');
    l.setAttribute('stroke-width','1.5');
    if(dash) l.setAttribute('stroke-dasharray','5,3');
    return l;
  }
  function rotText(x,y,t,color) {
    const g = document.createElementNS('http://www.w3.org/2000/svg','g');
    g.setAttribute('transform','translate('+x+','+y+') rotate(-90)');
    const el = document.createElementNS('http://www.w3.org/2000/svg','text');
    el.setAttribute('text-anchor','middle');el.setAttribute('dominant-baseline','middle');
    el.setAttribute('fill',color||'#e2e8f0');el.setAttribute('font-size',12);
    el.setAttribute('font-family','Noto Sans KR,sans-serif');
    el.textContent=t; g.appendChild(el); return g;
  }
  function arrow(x1,y1,x2,y2,color) {
    const g = document.createElementNS('http://www.w3.org/2000/svg','g');
    const l = document.createElementNS('http://www.w3.org/2000/svg','line');
    l.setAttribute('x1',x1);l.setAttribute('y1',y1);
    l.setAttribute('x2',x2);l.setAttribute('y2',y2);
    l.setAttribute('stroke',color||'#f59e0b');l.setAttribute('stroke-width','2');
    g.appendChild(l);
    const angle = Math.atan2(y2-y1,x2-x1)*180/Math.PI;
    const mk = document.createElementNS('http://www.w3.org/2000/svg','polygon');
    mk.setAttribute('points','0,-4 8,0 0,4');
    mk.setAttribute('fill',color||'#f59e0b');
    mk.setAttribute('transform','translate('+x2+','+y2+') rotate('+angle+')');
    g.appendChild(mk); return g;
  }

  const C_TOP = '#1e3a5f', C_BL = '#1c3a2e', C_BR = '#2d1b4e';
  const S_TOP = '#3b82f6', S_BL = '#10b981', S_BR = '#8b5cf6';

  // ── 왼쪽: a×a 정사각형 ──
  // 전체 a×a 배경 [파랑] — a² 전체를 파란색으로 표시
  svg.appendChild(rect(ox, oy, A, A, C_TOP, S_TOP, 'd-bg', 1));
  // 왼쪽아래: (a-b) × b [초록] — 잘라서 회전할 조각 (step2에서 표시)
  svg.appendChild(rect(ox, oy+aB, aB, B, C_BL, S_BL, 'd-bl', 0));
  // 오른쪽아래: b × b [보라] — 제거되는 b² 영역
  svg.appendChild(rect(ox+aB, oy+aB, B, B, C_BR, S_BR, 'd-br', 0));

  // 분할선 (항상 표시)
  svg.appendChild(line(ox+aB, oy+aB, ox+A, oy+aB, '#475569', true)); // 오른쪽 아래 가로
  svg.appendChild(line(ox+aB, oy, ox+aB, oy+A, '#475569', true));    // 세로

  // 왼쪽 도형 축 레이블
  svg.appendChild(text(ox+A/2,  oy+A+16, 'a', '#fbbf24', 12));
  svg.appendChild(rotText(ox-16, oy+aB/2, 'a-b', '#fbbf24'));
  svg.appendChild(rotText(ox-16, oy+aB+B/2, 'b', '#a78bfa'));
  svg.appendChild(text(ox+aB/2, oy+A+16, 'a-b', '#fbbf24', 11));
  svg.appendChild(text(ox+aB+B/2, oy+A+16, 'b', '#a78bfa', 11));

  // 내부 레이블
  const lTop = text(ox+A/2, oy+aB/2, 'a(a-b)', '#93c5fd', 11);
  lTop.setAttribute('id','d-ltop'); lTop.setAttribute('opacity',0); svg.appendChild(lTop);
  const lBL = text(ox+aB/2, oy+aB+B/2, '(a-b)b', '#6ee7b7', 11);
  lBL.setAttribute('id','d-lbl'); lBL.setAttribute('opacity',0); svg.appendChild(lBL);
  const lBR = text(ox+aB+B/2, oy+aB+B/2, 'b\u00B2', '#c4b5fd', 11);
  lBR.setAttribute('id','d-lbr'); lBR.setAttribute('opacity',0); svg.appendChild(lBR);

  // b² 강조 테두리
  const brHL = rect(ox+aB, oy+aB, B, B, 'none', '#f59e0b', 'd-brhl', 0);
  brHL.setAttribute('stroke-width','2.5'); svg.appendChild(brHL);

  // L자형 강조 외곽선
  const Lpoly = document.createElementNS('http://www.w3.org/2000/svg','polygon');
  Lpoly.setAttribute('points',
    ox+','+(oy)+' '+(ox+A)+','+(oy)+' '+(ox+A)+','+(oy+aB)+' '+
    (ox+aB)+','+(oy+aB)+' '+(ox+aB)+','+(oy+A)+' '+ox+','+(oy+A));
  Lpoly.setAttribute('fill','none'); Lpoly.setAttribute('stroke','#f59e0b');
  Lpoly.setAttribute('stroke-width','2'); Lpoly.setAttribute('id','d-Lpoly'); Lpoly.setAttribute('opacity',0);
  svg.appendChild(Lpoly);

  // 가로 분할선 (자르는 선): 왼쪽 부분만
  const cutLine = line(ox, oy+aB, ox+aB, oy+aB, '#a3e635', false);
  cutLine.setAttribute('id','d-cut'); cutLine.setAttribute('opacity',0);
  cutLine.setAttribute('stroke-width','2'); cutLine.setAttribute('stroke-dasharray','8,4');
  svg.appendChild(cutLine);
  const cutLbl = text(ox+aB/2, oy+aB-10, '\u2702 자르기', '#a3e635', 10);
  cutLbl.setAttribute('id','d-cutlbl'); cutLbl.setAttribute('opacity',0); svg.appendChild(cutLbl);

  // 화살표: 왼→오
  const arEl = arrow(ox+A+8, oy+A/2, rx-8, oy+aB/2, '#f59e0b');
  arEl.setAttribute('id','d-arrow'); arEl.setAttribute('opacity',0); svg.appendChild(arEl);
  const arLbl = text(ox+A+gap/2, oy+A/2-12, '90\u00B0 회전\n후 재배열', '#f59e0b', 10);
  arLbl.setAttribute('id','d-arrlbl'); arLbl.setAttribute('opacity',0); svg.appendChild(arLbl);

  // ── 오른쪽: (a+b)×(a-b) 직사각형 ──
  const ry = oy + B/2;
  // 왼쪽 부분: a×(a-b) [파랑]
  svg.appendChild(rect(rx, ry, A, aB, C_TOP, S_TOP, 'd-rtop', 0));
  // 오른쪽 부분: b×(a-b) [초록, 회전된 아래쪽 조각]
  svg.appendChild(rect(rx+A, ry, B, aB, C_BL, S_BL, 'd-rright', 0));
  // 결과 강조 테두리
  const resHL = rect(rx, ry, A+B, aB, 'none', '#f59e0b', 'd-resHL', 0);
  resHL.setAttribute('stroke-width','2.5'); svg.appendChild(resHL);
  // 결과 레이블
  const lRes = text(rx+(A+B)/2, ry+aB/2, '(a+b)(a-b)', '#6ee7b7', 11);
  lRes.setAttribute('id','d-lres'); lRes.setAttribute('opacity',0); svg.appendChild(lRes);
  // 오른쪽 축 레이블
  svg.appendChild(text(rx+A/2, ry+aB+16, 'a', '#fbbf24', 11));
  svg.appendChild(text(rx+A+B/2, ry+aB+16, 'b', '#a78bfa', 11));
  svg.appendChild(text(rx+(A+B)/2, ry+aB+28, '\u2190 a+b \u2192', '#64748b', 11));
  svg.appendChild(rotText(rx-14, ry+aB/2, 'a-b', '#fbbf24'));

  document.getElementById('aplusb-aminus-svg').appendChild(svg);
}

function setOpacityD(id, val) { const el = document.getElementById(id); if(el) el.setAttribute('opacity', val); }

function highlightDiff(step) {
  // 1=a² 시작, 2=b² 제거+L자+분할선, 3=재배열 직사각형
  // d-bg (전체 a×a 파랑)는 항상 표시
  setOpacityD('d-bl', step >= 2 ? 1 : 0);
  setOpacityD('d-br', step >= 2 ? 1 : 0);
  setOpacityD('d-lbr', step >= 2 ? 1 : 0);
  setOpacityD('d-brhl', step >= 2 ? 1 : 0);
  setOpacityD('d-Lpoly', step >= 2 ? 1 : 0);
  setOpacityD('d-cut', step >= 2 ? 1 : 0);
  setOpacityD('d-cutlbl', step >= 2 ? 1 : 0);
  setOpacityD('d-ltop', step >= 2 ? 1 : 0);
  setOpacityD('d-lbl', step >= 2 ? 1 : 0);
  setOpacityD('d-arrow', step >= 3 ? 1 : 0);
  setOpacityD('d-arrlbl', step >= 3 ? 1 : 0);
  setOpacityD('d-rtop', step >= 3 ? 1 : 0);
  setOpacityD('d-rright', step >= 3 ? 1 : 0);
  setOpacityD('d-resHL', step >= 3 ? 1 : 0);
  setOpacityD('d-lres', step >= 3 ? 1 : 0);
  [1,2,3].forEach(s => {
    const el = document.getElementById('ab-diff-step' + s);
    if(el) el.style.background = (s === step || step === 0) ? '#0c2e3e' : '';
    if(el) el.style.borderColor = (s === step || step === 0) ? '#06b6d4' : '#1e293b';
  });
  if(step === 0) {
    setOpacityD('d-bl',1); setOpacityD('d-br',1); setOpacityD('d-lbr',1);
    setOpacityD('d-brhl',1); setOpacityD('d-Lpoly',1);
    setOpacityD('d-cut',1); setOpacityD('d-cutlbl',1);
    setOpacityD('d-ltop',1); setOpacityD('d-lbl',1);
    setOpacityD('d-arrow',1); setOpacityD('d-arrlbl',1);
    setOpacityD('d-rtop',1); setOpacityD('d-rright',1);
    setOpacityD('d-resHL',1); setOpacityD('d-lres',1);
  }
}

// ── a³+b³ 단계별 강조 ──
function stepHL7(step) {
  const blocks = document.querySelectorAll('#cubeWrap7 .cube-block');
  blocks.forEach(b => {
    const key = b.dataset.key;
    let f = '';
    if (step === 1) {
      f = ''; // 전체 정상
    } else if (step === 2) {
      f = key === 'a2b' ? 'brightness(2.2) drop-shadow(0 0 8px #10b981)' : 'brightness(.25)';
    } else if (step === 3) {
      f = key === 'ab2' ? 'brightness(2.2) drop-shadow(0 0 8px #8b5cf6)' : 'brightness(.25)';
    } else if (step === 4) {
      f = (key === 'a3' || key === 'b3') ? 'brightness(2.2) drop-shadow(0 0 10px #fff)' : 'brightness(.1)';
    }
    b.style.filter = f;
  });
  [1,2,3,4].forEach(s => {
    const el = document.getElementById('c7-step' + s);
    if(el) el.style.background = s === step ? '#0c2e3e' : '';
    if(el) el.style.borderColor = s === step ? '#06b6d4' : '#1e293b';
  });
}

function checkDiff() {
  const msg = document.getElementById('msg2');
  msg.className = 'msg-box msg-success show';
  msg.innerHTML = '정답! ' + katex.renderToString('(a+b)(a-b) = a^2 - b^2', {throwOnError:false})
    + '<br><small style="color:#6ee7b7;font-size:.78rem">a²에서 b²을 뺀 L자형을 자른 뒤 아래 조각을 90° 회전하여 붙이면 가로 (a+b), 세로 (a-b)인 직사각형이 됩니다.</small>';
  document.getElementById('tab2').classList.add('done'); updateProg();
}

// ── 탭 & 진행도 ──
function showTab(idx) {
  document.querySelectorAll('.ftab').forEach((t, i) => t.classList.toggle('active', i === idx));
  document.querySelectorAll('.panel').forEach((p, i) => p.classList.toggle('active', i === idx));
}
function updateProg() {
  const done = document.querySelectorAll('.ftab.done').length;
  document.getElementById('prog-fill').style.width = (done / 8 * 100) + '%';
  document.getElementById('prog-text').textContent = done + ' / 8 완료';
}

window.addEventListener('load', () => {
  buildGrid(0); buildGrid(3); buildGrid(4); buildGrid(5);
  buildAB2Svg();
  buildDiffSvg();
  buildCube(6, 'cubeWrap6'); buildCube(7, 'cubeWrap7');
  buildPartBadges(6); buildPartBadges(7);
  initDrag('scene6', 6); initDrag('scene7', 7);
  renderMathInElement(document.getElementById('ftabs'), {delimiters:[{left:'$', right:'$', display:false}]});
});
</script>
</body>
</html>"""


def render():
    st.markdown("## 대수막대로 곱셈 공식 탐구")
    st.caption(
        "대수막대를 직접 드래그해서 격자를 채우세요. "
        "중학교 복습 5개 + 새 공식 3개 = 전 8개!"
    )
    components.html(_GAME_HTML, height=920, scrolling=True)
    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
