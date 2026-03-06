import streamlit as st
import streamlit.components.v1 as components
import requests
import datetime

META = {"title": "곱셈 공식 확장 탐구", "order": 20}

_GAS_URL    = "YOUR_COMMON1_GAS_WEB_APP_URL"
_SHEET_NAME = "곱셈공식확장"

_GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI',sans-serif;background:#0f172a;color:#e2e8f0;padding:14px;font-size:15px;}

/* ─ Header ─ */
.page-header{text-align:center;margin-bottom:14px;}
.page-header h2{font-size:1.35rem;color:#7dd3fc;margin-bottom:3px;}
.page-header p{font-size:.78rem;color:#64748b;}
.progress-bar{background:#1e293b;border-radius:8px;height:7px;overflow:hidden;margin:7px auto;max-width:380px;}
.progress-fill{background:linear-gradient(90deg,#06b6d4,#7c3aed);height:100%;transition:width .5s;}

/* ─ Stage Tabs ─ */
.stage-tabs{display:flex;gap:7px;justify-content:center;margin-bottom:14px;flex-wrap:wrap;}
.stage-tab{padding:7px 14px;border-radius:20px;border:2px solid #334155;background:#1e293b;
           color:#94a3b8;cursor:pointer;font-size:.82rem;transition:all .2s;user-select:none;}
.stage-tab.active{border-color:#06b6d4;background:#164e63;color:#7dd3fc;}
.stage-tab.done{border-color:#10b981;background:#064e3b;color:#6ee7b7;}
.stage-tab.done::before{content:'✓ ';}

/* ─ Stage panels ─ */
.stage{display:none;}
.stage.active{display:block;}

/* ─ Cards ─ */
.f-card{background:#1e293b;border:1px solid #334155;border-radius:11px;padding:12px 16px;margin-bottom:10px;}
.f-card .flabel{font-size:.72rem;color:#64748b;margin-bottom:5px;text-transform:uppercase;letter-spacing:.05em;}
.f-card .formula{font-size:1rem;color:#e2e8f0;font-family:Georgia,serif;}
.f-card.hl{border-color:#06b6d4;background:#0c2e3e;}
.f-card.purple{border-color:#7c3aed;background:#1b0e2d;}

/* ─ Pattern Table ─ */
.ptable{border-collapse:collapse;width:100%;margin-bottom:10px;font-size:.82rem;}
.ptable th{background:#1e3a5f;color:#7dd3fc;padding:5px 8px;text-align:center;}
.ptable td{background:#1e293b;border:1px solid #334155;padding:5px 8px;text-align:center;color:#cbd5e1;}
.ptable tr.discover td{background:#0c2e3e;color:#7dd3fc;font-weight:600;}
.ptable .qmark{color:#f59e0b;}

/* ─ Coef input row ─ */
.coef-row{display:flex;flex-wrap:wrap;gap:6px 4px;align-items:center;}
.coef-item{display:flex;align-items:center;gap:3px;}
.ci{width:38px;height:34px;background:#0f172a;border:2px solid #475569;border-radius:6px;
     color:#e2e8f0;text-align:center;font-size:.95rem;}
.ci.ok{border-color:#10b981;background:#022c22;}
.ci.ng{border-color:#ef4444;background:#2d0000;}
.ci:focus{outline:none;border-color:#06b6d4;}
.tlabel{font-size:.9rem;color:#cbd5e1;font-family:Georgia,serif;}
.sep{color:#475569;}

/* ─ Buttons ─ */
.btn{padding:7px 18px;border:none;border-radius:8px;cursor:pointer;font-size:.85rem;font-weight:600;transition:all .2s;}
.btn-cyan{background:#0891b2;color:#fff;}.btn-cyan:hover{background:#0e7490;}
.btn-green{background:#059669;color:#fff;}.btn-green:hover{background:#047857;}
.btn-gray{background:#334155;color:#94a3b8;}.btn-gray:hover{background:#475569;}
.btn:disabled{opacity:.45;cursor:not-allowed;}

/* ─ Feedback ─ */
.fb{min-height:26px;font-size:.85rem;padding:5px 10px;border-radius:7px;margin-top:8px;}
.fb.ok{background:#022c22;color:#6ee7b7;border:1px solid #10b981;}
.fb.ng{background:#2d0000;color:#fca5a5;border:1px solid #ef4444;}

/* ─ Pascal triangle ─ */
.pascal-outer{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:10px;}
.pascal-panel{flex:1;min-width:200px;}
.pascal-wrap{display:flex;flex-direction:column;align-items:center;gap:0;}
.prow{display:flex;align-items:center;gap:5px;margin:2px 0;opacity:0;transition:opacity .4s;}
.prow.vis{opacity:1;}
.pcell{width:42px;height:34px;background:#1e293b;border:1px solid #334155;border-radius:6px;
        display:flex;align-items:center;justify-content:center;font-size:.88rem;color:#e2e8f0;font-weight:600;}
.pcell.fresh{background:#164e63;border-color:#06b6d4;color:#7dd3fc;animation:pop .35s ease;}
.plabel{font-size:.72rem;color:#64748b;width:80px;text-align:right;margin-right:5px;font-family:Georgia,serif;}
@keyframes pop{0%{transform:scale(.4);opacity:0}60%{transform:scale(1.25)}100%{transform:scale(1);opacity:1}}

/* ─ Stage 3 term cards ─ */
.term-pool{display:flex;flex-wrap:wrap;gap:7px;padding:10px;background:#1e293b;border-radius:9px;margin-bottom:9px;}
.tc3{padding:7px 13px;background:#0f172a;border:2px solid #7c3aed;border-radius:7px;
     color:#c4b5fd;cursor:pointer;font-family:Georgia,serif;font-size:.93rem;transition:all .2s;user-select:none;}
.tc3:hover:not(.used){background:#2e1065;border-color:#a78bfa;}
.tc3.used{border-color:#374151;color:#4b5563;background:#111827;cursor:not-allowed;}

/* ─ Factor slots ─ */
.factor-disp{display:flex;align-items:center;gap:4px;flex-wrap:wrap;font-family:Georgia,serif;font-size:.97rem;
             color:#94a3b8;padding:8px 0;}
.fslot{min-width:54px;height:34px;background:#0f172a;border:2px dashed #475569;border-radius:6px;
        display:inline-flex;align-items:center;justify-content:center;color:#64748b;font-size:.82rem;
        cursor:pointer;margin:2px;transition:all .2s;}
.fslot.filled{border-style:solid;border-color:#7c3aed;color:#c4b5fd;background:#2e1065;}
.fslot.ok-slot{border-color:#10b981;background:#022c22;color:#6ee7b7;}
.fslot.ng-slot{border-color:#ef4444;background:#2d0000;color:#fca5a5;}

/* ─ misc ─ */
.chip{display:inline-block;padding:3px 10px;background:#1e293b;border-radius:20px;
       font-size:.78rem;color:#94a3b8;border:1px solid #334155;}
.chip .val{color:#fbbf24;font-weight:700;}
.snav{display:flex;justify-content:flex-end;margin-top:12px;gap:8px;}
#confetti{position:fixed;top:0;left:0;pointer-events:none;z-index:9999;}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
@media(max-width:600px){.grid2{grid-template-columns:1fr;}}

/* ─ Expand animation rows ─ */
.exp-row{display:flex;align-items:flex-start;gap:8px;padding:10px 12px;
         background:#1e293b;border:1px solid #334155;border-radius:9px;margin-bottom:4px;
         opacity:0;transform:translateY(-8px);transition:opacity .45s,transform .45s;flex-wrap:wrap;}
.exp-row.vis{opacity:1;transform:none;}
.exp-lhs{font-family:Georgia,serif;color:#7dd3fc;font-size:.97rem;min-width:125px;white-space:nowrap;}
.exp-eq{color:#64748b;padding:0 6px;font-size:.97rem;}
.exp-rhs{flex:1;min-width:0;}
.sq-part{color:#93c5fd;font-family:Georgia,serif;font-size:.9rem;}
.cr-sep{color:#64748b;margin:0 3px;}
.cr-part{color:#c4b5fd;font-family:Georgia,serif;font-size:.9rem;}
.exp-badges{display:flex;gap:5px;margin-top:5px;flex-wrap:wrap;}
.badge{font-size:.68rem;padding:2px 8px;border-radius:10px;}
.badge-sq{background:#1e3a5f;color:#93c5fd;border:1px solid #1d4ed8;}
.badge-cr{background:#2e1065;color:#c4b5fd;border:1px solid #7c3aed;}
.diff-row{display:flex;align-items:center;gap:6px;padding:9px 12px;
          background:#1e293b;border:1px solid #334155;border-radius:9px;margin-bottom:4px;
          opacity:0;transform:translateY(-8px);transition:opacity .45s,transform .45s;flex-wrap:wrap;}
.diff-row.vis{opacity:1;transform:none;}
.diff-lhs{font-family:Georgia,serif;color:#f87171;font-size:.95rem;min-width:52px;}
.diff-eq{color:#64748b;padding:0 4px;}
.diff-f1{font-family:Georgia,serif;color:#94a3b8;font-size:.95rem;}
.diff-f2{font-family:Georgia,serif;color:#a78bfa;font-size:.95rem;}
.diff-badge{font-size:.68rem;padding:2px 8px;border-radius:10px;background:#2e1065;
            color:#c4b5fd;border:1px solid #7c3aed;margin-left:4px;}
.add-zone{text-align:center;margin:3px 0 8px;position:relative;}
.add-zone::before{content:'';display:block;height:1px;
  background:linear-gradient(90deg,transparent,#334155,transparent);margin-bottom:6px;}
.btn-pulse{animation:abtn 1.6s infinite;}
@keyframes abtn{0%,100%{box-shadow:0 0 0 0 rgba(8,145,178,.55)}50%{box-shadow:0 0 0 7px rgba(8,145,178,0)}}
</style>
</head>
<body>
<canvas id="confetti"></canvas>

<!-- Header -->
<div class="page-header">
  <h2>🧮 곱셈 공식 확장 탐구</h2>
  <p>n을 늘려가며 패턴을 직접 발견하고, 더 일반적인 공식으로 확장해 보세요.</p>
  <div class="progress-bar"><div class="progress-fill" id="progFill" style="width:0%"></div></div>
  <div id="progLabel" style="font-size:.73rem;color:#64748b;margin-top:2px">0 / 3 스테이지 완료</div>
</div>

<!-- Stage Tabs -->
<div class="stage-tabs">
  <div class="stage-tab active" id="tab1" onclick="goStage(1)">① 합의 제곱 확장</div>
  <div class="stage-tab"        id="tab2" onclick="goStage(2)">② 이항 전개 계수</div>
  <div class="stage-tab"        id="tab3" onclick="goStage(3)">③ 차의 공식 패턴</div>
</div>

<!-- ════════════════════════════════ STAGE 1 ════════════════════════════════ -->
<div class="stage active" id="stage1">

  <div class="f-card" style="margin-bottom:10px">
    <div class="flabel">🔢 (변수 합)의 제곱 — 변수 개수 n을 늘려가며 탐구</div>
    <div style="font-size:.8rem;color:#64748b">버튼을 눌러 n을 늘리고, 전개식이 어떻게 달라지는지 확인하세요.</div>
  </div>

  <div class="exp-row vis" id="s1r2">
    <span class="exp-lhs">(a+b)²</span>
    <span class="exp-eq">=</span>
    <div class="exp-rhs">
      <span class="sq-part">a²+b²</span>
      <span class="cr-sep">+</span>
      <span class="cr-part">2ab</span>
      <div class="exp-badges">
        <span class="badge badge-sq">■ 제곱항 2개</span>
        <span class="badge badge-cr">◆ 교차항 1쌍</span>
      </div>
    </div>
  </div>

  <div class="add-zone" id="s1add3zone">
    <button class="btn btn-cyan btn-pulse" onclick="s1expand(3)">➕ n=3 확인하기</button>
  </div>

  <div class="exp-row" id="s1r3" style="display:none">
    <span class="exp-lhs">(a+b+c)²</span>
    <span class="exp-eq">=</span>
    <div class="exp-rhs">
      <span class="sq-part">a²+b²+c²</span>
      <span class="cr-sep">+</span>
      <span class="cr-part">2ab+2bc+2ca</span>
      <div class="exp-badges">
        <span class="badge badge-sq">■ 제곱항 3개</span>
        <span class="badge badge-cr">◆ 교차항 3쌍</span>
      </div>
    </div>
  </div>

  <div class="add-zone" id="s1add4zone" style="display:none">
    <button class="btn btn-cyan btn-pulse" onclick="s1expand(4)">➕ n=4 확인하기</button>
  </div>

  <div class="exp-row" id="s1r4" style="display:none">
    <span class="exp-lhs">(a+b+c+d)²</span>
    <span class="exp-eq">=</span>
    <div class="exp-rhs">
      <span class="sq-part">a²+b²+c²+d²</span>
      <span class="cr-sep">+</span>
      <span class="cr-part">2ab+2ac+2ad+2bc+2bd+2cd</span>
      <div class="exp-badges">
        <span class="badge badge-sq">■ 제곱항 4개</span>
        <span class="badge badge-cr">◆ 교차항 6쌍</span>
      </div>
    </div>
  </div>

  <div class="f-card" style="margin-top:6px">
    <div class="flabel">📊 발견한 패턴</div>
    <table class="ptable">
      <tr><th>변수 수 n</th><th>제곱항</th><th>교차항(이중곱)</th><th>전체 항 수</th></tr>
      <tr id="s1pt2"><td>2</td><td>2</td><td>1</td><td>3</td></tr>
      <tr id="s1pt3" style="display:none" class="discover"><td>3</td><td>3</td><td>3</td><td>6</td></tr>
      <tr id="s1pt4" style="display:none" class="discover"><td>4</td><td>4</td><td>6</td><td>10</td></tr>
    </table>
  </div>

  <div class="f-card hl" id="s1challenge" style="display:none">
    <div class="flabel">🎯 미션 : n=5일 때를 예측하세요</div>
    <div style="font-size:.83rem;color:#e2e8f0;margin-bottom:10px">
      (a+b+c+d+e)² 에서 — 발견한 패턴으로 n=5의 경우를 예측해 보세요.
    </div>
    <div style="display:flex;flex-wrap:wrap;gap:14px">
      <div>
        <div style="font-size:.78rem;color:#94a3b8;margin-bottom:4px">제곱항의 수 (□² 꼴)</div>
        <div class="coef-item"><input class="ci" id="s1m1" maxlength="2" placeholder="?"><span class="tlabel" style="margin-left:5px">개</span></div>
      </div>
      <div>
        <div style="font-size:.78rem;color:#94a3b8;margin-bottom:4px">교차항의 수 (이중곱 쌍)</div>
        <div class="coef-item"><input class="ci" id="s1m2" maxlength="2" placeholder="?"><span class="tlabel" style="margin-left:5px">쌍</span></div>
      </div>
      <div>
        <div style="font-size:.78rem;color:#94a3b8;margin-bottom:4px">전체 항의 수</div>
        <div class="coef-item"><input class="ci" id="s1m3" maxlength="2" placeholder="?"><span class="tlabel" style="margin-left:5px">개</span></div>
      </div>
    </div>
    <div style="margin-top:10px;display:flex;gap:8px">
      <button class="btn btn-gray" onclick="resetS1()">↺ 초기화</button>
      <button class="btn btn-cyan" onclick="checkS1()">✅ 확인</button>
    </div>
    <div class="fb" id="fb1"></div>
  </div>

  <div class="snav">
    <button class="btn btn-green" id="btnS1Next" style="display:none" onclick="goStage(2)">② 이항 전개 계수 →</button>
  </div>
</div>

<!-- ════════════════════════════════ STAGE 2 ════════════════════════════════ -->
<div class="stage" id="stage2">

  <div class="f-card" style="margin-bottom:10px">
    <div class="flabel">이항 전개 계수 — (a+b)ⁿ의 계수 패턴</div>
    <div class="formula" style="font-size:.92rem">
      (a+b)ⁿ 전개식의 <strong style="color:#7dd3fc">계수</strong>가 이항 전개 계수 삼각형의 n번째 행과 일치합니다.
    </div>
  </div>

  <div class="pascal-outer">
    <!-- Pascal triangle panel -->
    <div class="pascal-panel">
      <div class="f-card" style="padding:12px">
        <div class="flabel">� 이항 전개 계수
          <span id="pRowChip" style="color:#fbbf24;font-size:.75rem;margin-left:6px">(n=0~2)</span>
        </div>
        <div class="pascal-wrap" id="pascalWrap"></div>
        <div style="margin-top:10px;display:flex;gap:8px;align-items:center;flex-wrap:wrap">
          <button class="btn btn-cyan" id="btnPNext" onclick="addPRow()" style="font-size:.8rem;padding:5px 12px">➕ 다음 행 추가</button>
          <span class="chip">현재: n=<span class="val" id="curN">2</span></span>
        </div>
      </div>
    </div>

    <!-- (a+b)^4 challenge panel -->
    <div class="pascal-panel">
      <div class="f-card hl">
        <div class="flabel">🎯 미션 : (a+b)⁴ 의 계수를 입력하세요</div>
        <div style="font-family:Georgia,serif;font-size:.88rem;color:#94a3b8;margin:6px 0 10px">
          (a+b)⁴ = □a⁴ + □a³b + □a²b² + □ab³ + □b⁴
        </div>
        <div class="coef-row" style="flex-wrap:wrap;gap:6px">
          <div class="coef-item"><input class="ci" id="p0" maxlength="2" placeholder="?"><span class="tlabel">a⁴</span></div>
          <span class="sep">+</span>
          <div class="coef-item"><input class="ci" id="p1" maxlength="2" placeholder="?"><span class="tlabel">a³b</span></div>
          <span class="sep">+</span>
          <div class="coef-item"><input class="ci" id="p2" maxlength="2" placeholder="?"><span class="tlabel">a²b²</span></div>
          <span class="sep">+</span>
          <div class="coef-item"><input class="ci" id="p3" maxlength="2" placeholder="?"><span class="tlabel">ab³</span></div>
          <span class="sep">+</span>
          <div class="coef-item"><input class="ci" id="p4" maxlength="2" placeholder="?"><span class="tlabel">b⁴</span></div>
        </div>
        <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px">
          <button class="btn btn-gray"  onclick="resetS2()">↺ 초기화</button>
          <button class="btn btn-cyan"  onclick="checkS2()">✅ 정답 확인</button>
        </div>
        <div class="fb" id="fb2"></div>
      </div>
    </div>
  </div>

  <!-- General formula (shown on success) -->
  <div class="f-card" id="s2gen" style="display:none">
    <div class="flabel">📐 일반 공식 (이항정리 미리보기)</div>
    <div class="formula" style="font-size:.93rem">
      (a+b)ⁿ = C(n,0)aⁿ + C(n,1)aⁿ⁻¹b + ⋯ + C(n,n)bⁿ
    </div>
    <div style="font-size:.78rem;color:#64748b;margin-top:5px">
      C(n,k) = n! / (k!(n−k)!) 는 이항계수이며, 이항 전개 계수 삼각형의 각 원소와 같습니다.
    </div>
  </div>

  <div class="snav">
    <button class="btn btn-green" id="btnS2Next" style="display:none" onclick="goStage(3)">③ 차의 공식 패턴 →</button>
  </div>
</div>

<!-- ════════════════════════════════ STAGE 3 ════════════════════════════════ -->
<div class="stage" id="stage3">

  <div class="f-card" style="margin-bottom:10px">
    <div class="flabel">➖ aⁿ−bⁿ 인수분해 — n을 늘려가며 탐구</div>
    <div style="font-size:.8rem;color:#64748b">n이 커질수록 (a−b) 뒤에 오는 인수의 모양이 어떻게 확장되는지 확인하세요.</div>
  </div>

  <div class="diff-row vis" id="s3r2">
    <span class="diff-lhs">a²−b²</span>
    <span class="diff-eq">=</span>
    <span class="diff-f1">(a−b)</span>
    <span class="diff-f2">(a+b)</span>
    <span class="diff-badge">괄호 안 2항 · 각 항 차수 합=1</span>
  </div>

  <div class="add-zone" id="s3add3zone">
    <button class="btn btn-cyan btn-pulse" onclick="s3expand(3)">➕ n=3 확인하기</button>
  </div>

  <div class="diff-row" id="s3r3" style="display:none">
    <span class="diff-lhs">a³−b³</span>
    <span class="diff-eq">=</span>
    <span class="diff-f1">(a−b)</span>
    <span class="diff-f2">(a²+ab+b²)</span>
    <span class="diff-badge">괄호 안 3항 · 각 항 차수 합=2</span>
  </div>

  <div class="add-zone" id="s3add4zone" style="display:none">
    <button class="btn btn-cyan btn-pulse" onclick="s3expand(4)">➕ n=4 확인하기</button>
  </div>

  <div class="diff-row" id="s3r4" style="display:none">
    <span class="diff-lhs">a⁴−b⁴</span>
    <span class="diff-eq">=</span>
    <span class="diff-f1">(a−b)</span>
    <span class="diff-f2">(a³+a²b+ab²+b³)</span>
    <span class="diff-badge">괄호 안 4항 · 각 항 차수 합=3</span>
  </div>

  <div class="f-card" style="margin-top:6px">
    <div class="flabel">💡 패턴 정리</div>
    <div style="font-size:.83rem;color:#94a3b8;line-height:1.8">
      aⁿ−bⁿ = (a−b)(aⁿ⁻¹ + aⁿ⁻²b + ⋯ + abⁿ⁻² + bⁿ⁻¹)<br>
      → 괄호 안 : <strong style="color:#a78bfa">a</strong>의 지수 감소 · <strong style="color:#a78bfa">b</strong>의 지수 증가 · 각 항의 차수 합 = n−1
    </div>
  </div>

  <!-- 미션: a^5-b^5 (n=4 확인 후 잠금 해제) -->
  <div class="f-card purple" id="mA" style="display:none;margin-top:8px">
    <div class="flabel">🎯 미션 : (a−b)( ? ) = a⁵−b⁵</div>
    <div style="font-size:.82rem;color:#94a3b8;margin-bottom:8px">
      아래 카드 중 올바른 항을 <strong>차수 내림차순</strong>으로 클릭하여 5개의 슬롯을 채우세요.
      (슬롯 클릭 시 취소)
    </div>
    <div class="term-pool" id="poolA"></div>
    <div style="background:#0f172a;border-radius:8px;padding:10px;margin-bottom:8px">
      <div class="factor-disp">
        <span>(a−b)</span><span>(</span>
        <span id="sA0" class="fslot" onclick="clearSA(0)">?</span>
        <span class="sep">+</span>
        <span id="sA1" class="fslot" onclick="clearSA(1)">?</span>
        <span class="sep">+</span>
        <span id="sA2" class="fslot" onclick="clearSA(2)">?</span>
        <span class="sep">+</span>
        <span id="sA3" class="fslot" onclick="clearSA(3)">?</span>
        <span class="sep">+</span>
        <span id="sA4" class="fslot" onclick="clearSA(4)">?</span>
        <span>)</span>
        <span style="color:#94a3b8"> = a⁵−b⁵</span>
      </div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <button class="btn btn-gray" onclick="resetA()">↺ 초기화</button>
      <button class="btn btn-cyan" id="btnChkA" disabled onclick="checkA()">✅ 확인</button>
    </div>
    <div class="fb" id="fbA"></div>
  </div>

  <div class="f-card" id="s3gen" style="display:none;margin-top:8px">
    <div class="flabel">📐 일반 공식</div>
    <div class="formula" style="font-size:.93rem">
      (a−b)(aⁿ⁻¹ + aⁿ⁻²b + ⋯ + abⁿ⁻² + bⁿ⁻¹) = aⁿ − bⁿ
    </div>
    <div style="font-size:.78rem;color:#94a3b8;margin-top:5px">
      n이 홀수 : (a+b)(aⁿ⁻¹ − aⁿ⁻²b + ⋯ + bⁿ⁻¹) = aⁿ + bⁿ 도 성립
    </div>
  </div>

  <div class="snav">
    <span class="chip">총 점수: <span class="val" id="scoreLbl">0</span>점</span>
  </div>
</div>

<script>
// ─────────────────────────── Global state ────────────────────────────────────
const done = [false, false, false];
let score = 0;

// ─────────────────────────── Stage navigation ────────────────────────────────
function goStage(n) {
  [1,2,3].forEach(i => {
    document.getElementById('stage'+i).classList.toggle('active', i===n);
    const tab = document.getElementById('tab'+i);
    tab.classList.toggle('active', i===n && !done[i-1]);
  });
}

function markDone(n) {
  if (done[n-1]) return;
  done[n-1] = true;
  const tab = document.getElementById('tab'+n);
  tab.classList.remove('active');
  tab.classList.add('done');
  const cnt = done.filter(Boolean).length;
  document.getElementById('progFill').style.width = (cnt/3*100)+'%';
  document.getElementById('progLabel').textContent = cnt+' / 3 스테이지 완료';
  document.getElementById('scoreLbl').textContent = score;
  if (cnt === 3) launchConfetti();
}

function setFb(id, msg, cls) {
  const el = document.getElementById(id);
  el.innerHTML = msg;
  el.className = 'fb' + (cls ? ' '+cls : '');
}

// ─────────────────────────── Stage 1 ─────────────────────────────────────────
function s1expand(n) {
  document.getElementById('s1add'+n+'zone').style.display = 'none';
  const row = document.getElementById('s1r'+n);
  row.style.display = 'flex';
  setTimeout(() => row.classList.add('vis'), 30);
  document.getElementById('s1pt'+n).style.display = '';
  if (n === 3) document.getElementById('s1add4zone').style.display = 'block';
  if (n === 4) {
    document.getElementById('s1challenge').style.display = 'block';
    setTimeout(() => document.getElementById('s1challenge').scrollIntoView({behavior:'smooth',block:'nearest'}), 200);
  }
}

function checkS1() {
  const v1 = document.getElementById('s1m1').value.trim();
  const v2 = document.getElementById('s1m2').value.trim();
  const v3 = document.getElementById('s1m3').value.trim();
  const ok1 = v1==='5', ok2 = v2==='10', ok3 = v3==='15';
  ['s1m1','s1m2','s1m3'].forEach((id,i) => {
    const ok = [ok1,ok2,ok3][i];
    const v  = [v1,v2,v3][i];
    document.getElementById(id).classList.toggle('ok', ok);
    document.getElementById(id).classList.toggle('ng', v!=='' && !ok);
  });
  if (ok1 && ok2 && ok3) {
    setFb('fb1','🎉 정답! n=5: 제곱항 5개 + 교차항 10쌍 = 총 15항 ✨','ok');
    score += 30;
    document.getElementById('btnS1Next').style.display = 'inline-block';
    markDone(1);
    launchConfetti();
  } else {
    setFb('fb1','❌ 힌트: 제곱항은 n개, 교차항은 C(n,2)=n(n-1)/2쌍 이에요.','ng');
  }
}

function resetS1() {
  ['s1m1','s1m2','s1m3'].forEach(id => {
    const el = document.getElementById(id);
    el.value = '';
    el.classList.remove('ok','ng');
  });
  setFb('fb1','','');
}

// ─────────────────────────── Stage 2 : Pascal ────────────────────────────────
const PASCAL = [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1],[1,5,10,10,5,1],[1,6,15,20,15,6,1]];
let pShown = 3;

function initPascal() {
  const wrap = document.getElementById('pascalWrap');
  wrap.innerHTML = '';
  for (let r = 0; r < pShown; r++) appendPRow(r, false);
}

function appendPRow(r, isNew) {
  const wrap = document.getElementById('pascalWrap');
  const rowEl = document.createElement('div');
  rowEl.className = 'prow' + (isNew ? '' : ' vis');
  rowEl.id = 'prow'+r;

  const lbl = document.createElement('div');
  lbl.className = 'plabel';
  lbl.innerHTML = '(a+b)<sup>'+r+'</sup>';
  rowEl.appendChild(lbl);

  PASCAL[r].forEach(v => {
    const cell = document.createElement('div');
    cell.className = 'pcell' + (isNew ? ' fresh' : '');
    cell.textContent = v;
    rowEl.appendChild(cell);
  });
  wrap.appendChild(rowEl);
  if (isNew) setTimeout(() => rowEl.classList.add('vis'), 30);
}

function addPRow() {
  if (pShown >= PASCAL.length) return;
  appendPRow(pShown, true);
  document.getElementById('curN').textContent = pShown;
  document.getElementById('pRowChip').textContent = '(n=0~'+pShown+')';
  pShown++;
  if (pShown >= PASCAL.length) {
    document.getElementById('btnPNext').disabled = true;
    document.getElementById('btnPNext').textContent = '✅ 모두 표시됨';
  }
}

const ANS2 = ['1','4','6','4','1'];
function checkS2() {
  let allOk = true;
  ANS2.forEach((ans, i) => {
    const el = document.getElementById('p'+i);
    const ok = el.value.trim() === ans;
    el.classList.toggle('ok', ok);
    el.classList.toggle('ng', el.value.trim() !== '' && !ok);
    if (!ok) allOk = false;
  });
  if (allOk) {
    setFb('fb2','🎉 정답! (a+b)⁴ = a⁴+4a³b+6a²b²+4ab³+b⁴ ✨','ok');
    score += 30;
    document.getElementById('btnS2Next').style.display = 'inline-block';
    document.getElementById('s2gen').style.display = 'block';
    markDone(2);
    launchConfetti();
  } else {
    setFb('fb2','❌ 이항 전개 계수 n=4 행: 1 4 6 4 1 을 확인하세요.','ng');
  }
}

function resetS2() {
  ANS2.forEach((_, i) => {
    const el = document.getElementById('p'+i);
    el.value = '';
    el.classList.remove('ok','ng');
  });
  setFb('fb2','','');
}

// ─────────────────────────── Stage 3 ─────────────────────────────────────────
function s3expand(n) {
  document.getElementById('s3add'+n+'zone').style.display = 'none';
  const row = document.getElementById('s3r'+n);
  row.style.display = 'flex';
  setTimeout(() => row.classList.add('vis'), 30);
  if (n === 3) document.getElementById('s3add4zone').style.display = 'block';
  if (n === 4) {
    document.getElementById('mA').style.display = 'block';
    setTimeout(() => document.getElementById('mA').scrollIntoView({behavior:'smooth',block:'nearest'}), 200);
  }
}

const POOL_A_DEF = [
  {t:'a⁴',  ok:true},
  {t:'a³b', ok:true},
  {t:'a²b²',ok:true},
  {t:'ab³', ok:true},
  {t:'b⁴',  ok:true},
  {t:'a³b²',ok:false},
  {t:'a²b³',ok:false},
];
const CORRECT_A = ['a⁴','a³b','a²b²','ab³','b⁴'];

function shuffle(arr) { return [...arr].sort(() => Math.random()-.5); }

let pA = [], sA = [null,null,null,null,null];

function buildPool(poolId, items, clickFn) {
  const el = document.getElementById(poolId);
  el.innerHTML = '';
  items.forEach((item, i) => {
    const c = document.createElement('div');
    c.className = 'tc3';
    c.textContent = item.t;
    c.id = poolId+'_'+i;
    c.onclick = () => clickFn(i);
    el.appendChild(c);
  });
}

function refreshSlots(pfx, slots) {
  slots.forEach((v, i) => {
    const el = document.getElementById(pfx+i);
    if (v !== null) { el.textContent = v; el.classList.add('filled'); el.classList.remove('ok-slot','ng-slot'); }
    else            { el.textContent = '?'; el.classList.remove('filled','ok-slot','ng-slot'); }
  });
}

function firstEmpty(slots) { return slots.findIndex(s => s === null); }

function clickPA(i) {
  const item = pA[i];
  const card = document.getElementById('poolA_'+i);
  if (card.classList.contains('used')) return;
  const slot = firstEmpty(sA);
  if (slot === -1) return;
  sA[slot] = item.t;
  card.classList.add('used');
  refreshSlots('sA', sA);
  setFb('fbA','','');
  document.getElementById('btnChkA').disabled = sA.includes(null);
}
function clearSA(i) {
  if (sA[i] === null) return;
  const txt = sA[i]; sA[i] = null;
  let found = false;
  pA.forEach((item, ci) => {
    if (!found && item.t === txt) {
      const c = document.getElementById('poolA_'+ci);
      if (c && c.classList.contains('used')) { c.classList.remove('used'); found = true; }
    }
  });
  refreshSlots('sA', sA);
  document.getElementById('btnChkA').disabled = true;
  setFb('fbA','','');
}
function resetA() {
  sA = [null,null,null,null,null];
  pA.forEach((_,i) => document.getElementById('poolA_'+i).classList.remove('used'));
  refreshSlots('sA', sA);
  setFb('fbA','','');
  document.getElementById('btnChkA').disabled = true;
}
function checkA() {
  const ok = sA.every((v,i) => v === CORRECT_A[i]);
  sA.forEach((v,i) => {
    const el = document.getElementById('sA'+i);
    el.classList.toggle('ok-slot', v === CORRECT_A[i]);
    el.classList.toggle('ng-slot', v !== CORRECT_A[i]);
  });
  if (ok) {
    setFb('fbA','🎉 정답! (a−b)(a⁴+a³b+a²b²+ab³+b⁴) = a⁵−b⁵ ✨','ok');
    score += 40;
    document.getElementById('s3gen').style.display = 'block';
    markDone(3);
    launchConfetti();
  } else {
    setFb('fbA','❌ 슬롯을 클릭해서 제거하고 차수 내림차순으로 다시 배치하세요.','ng');
  }
}

// ─────────────────────────── Confetti ────────────────────────────────────────
function launchConfetti() {
  const canvas = document.getElementById('confetti');
  canvas.width = window.innerWidth; canvas.height = window.innerHeight;
  const ctx = canvas.getContext('2d');
  const pieces = Array.from({length:80}, () => ({
    x:Math.random()*canvas.width, y:Math.random()*canvas.height - canvas.height,
    r:Math.random()*4+2, dx:(Math.random()-.5)*3, dy:Math.random()*3+2,
    color:`hsl(${Math.random()*360},80%,60%)`, rot:Math.random()*360, drot:(Math.random()-.5)*6
  }));
  let frame = 0;
  function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    pieces.forEach(p => {
      ctx.save(); ctx.translate(p.x,p.y); ctx.rotate(p.rot*Math.PI/180);
      ctx.fillStyle=p.color; ctx.fillRect(-p.r,-p.r,p.r*2,p.r*2); ctx.restore();
      p.x+=p.dx; p.y+=p.dy; p.rot+=p.drot;
    });
    frame++;
    if(frame<100) requestAnimationFrame(draw);
    else ctx.clearRect(0,0,canvas.width,canvas.height);
  }
  draw();
}

// ─────────────────────────── Init ────────────────────────────────────────────
initPascal();
pA = shuffle(POOL_A_DEF);
buildPool('poolA', pA, clickPA);
refreshSlots('sA', sA);
</script>
</body>
</html>
"""


def render():
    st.header("🧮 곱셈 공식 확장 탐구")
    st.caption(
        "배운 곱셈 공식의 패턴을 직접 발견하고, 더 일반적인 형태로 확장해 보세요.  \n"
        "3개의 스테이지를 모두 클리어하면 완료입니다!"
    )
    components.html(_GAME_HTML, height=760, scrolling=True)
    _render_reflection_form(_SHEET_NAME, _GAS_URL)


def _render_reflection_form(sheet_name: str, gas_url: str):
    st.divider()
    st.subheader("✍️ 활동 후 성찰 기록")
    st.caption("아래 질문에 답하고 **제출하기** 버튼을 눌러주세요.")

    with st.form(f"reflection_{sheet_name}", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            student_id = st.text_input("학번")
        with c2:
            name = st.text_input("이름")

        st.markdown("**📝 이 활동과 관련된 문제 2개를 스스로 만들고 풀어보세요**")
        q1 = st.text_area("문제 1 (곱셈 공식 확장 관련)", height=70)
        a1 = st.text_input("문제 1의 정답")
        q2 = st.text_area("문제 2 (곱셈 공식 확장 관련)", height=70)
        a2 = st.text_input("문제 2의 정답")

        new_learning = st.text_area("💡 이 활동을 통해 새롭게 알게 된 점", height=90)
        feeling      = st.text_area("💬 이 활동을 하면서 느낀 점", height=90)

        submitted = st.form_submit_button("📤 제출하기", use_container_width=True, type="primary")

    if submitted:
        if not student_id or not name:
            st.warning("학번과 이름을 입력해주세요.")
        elif gas_url == "YOUR_COMMON1_GAS_WEB_APP_URL":
            st.error(
                "⚠️ Google Sheets 연동 URL이 아직 설정되지 않았습니다.  \n"
                "선생님이 Google Apps Script를 배포하고 `_GAS_URL`을 교체해야 합니다."
            )
        else:
            payload = {
                "sheet":        sheet_name,
                "timestamp":    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "학번":         student_id,
                "이름":         name,
                "문제1":        q1, "답1": a1,
                "문제2":        q2, "답2": a2,
                "새롭게알게된점": new_learning,
                "느낀점":        feeling,
            }
            try:
                resp = requests.post(gas_url, json=payload, timeout=10)
                if resp.status_code == 200:
                    st.success(f"✅ {name}님의 기록이 제출되었습니다!")
                    st.balloons()
                else:
                    st.error(f"제출 중 오류 (상태코드: {resp.status_code})")
            except Exception as e:
                st.error(f"네트워크 오류: {e}")
