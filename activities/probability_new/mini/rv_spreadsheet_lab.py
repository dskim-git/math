# activities/probability_new/mini/rv_spreadsheet_lab.py
"""
스프레드시트로 확률변수 분석
Y=aX+b 수식 입력부터 기댓값·분산·표준편차까지 전 과정을 엑셀 수식으로 체험.
"""
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title":       "📊 스프레드시트로 확률변수 분석",
    "description": "Y=aX+b 수식 입력부터 기댓값·분산·표준편차까지 엑셀 수식으로 직접 계산합니다.",
    "order":       55,
    "hidden":      True,
}

_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>스프레드시트로 확률변수 분석</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#e2e8f0;padding:14px 10px;min-height:600px}
.hero{text-align:center;background:linear-gradient(135deg,rgba(59,130,246,.15),rgba(139,92,246,.1));
      border:1px solid rgba(59,130,246,.3);border-radius:16px;padding:16px;margin-bottom:14px}
.hero h1{font-size:17px;font-weight:900;color:#60a5fa}
.hero p{font-size:11.5px;color:#94a3b8;margin-top:4px}
.prob-selector{display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap}
.prob-btn{padding:8px 14px;border-radius:10px;border:2px solid #1e3a5f;
          background:#141c2b;color:#7a8ea8;cursor:pointer;font-size:12.5px;font-weight:700;transition:all .2s}
.prob-btn.active{background:#1e3a5f;border-color:#3b82f6;color:#93c5fd}
.prob-btn:hover:not(.active){background:#1a2540;color:#93c5fd}
.prob-desc{background:#141c2b;border:1px solid #1e3a5f;border-radius:12px;
           padding:10px 14px;margin-bottom:12px;font-size:13px;line-height:1.7}
.prob-formula{font-size:15px;font-weight:800;color:#60a5fa;font-style:italic}
.prob-info{color:#94a3b8;margin-top:3px;font-size:12px}
.tabs{display:flex;gap:6px;margin-bottom:14px}
.tab-btn{padding:8px 18px;border-radius:10px;border:2px solid #1e293b;
         background:#141c2b;color:#7a8ea8;cursor:pointer;font-size:13px;font-weight:700;transition:all .2s}
.tab-btn.active{background:#172554;border-color:#3b82f6;color:#93c5fd}
.tab-panel{display:none}.tab-panel.active{display:block}
.card{background:#161e2e;border:1px solid #1e293b;border-radius:14px;padding:16px 18px;margin-bottom:12px}
.card-title{font-size:14px;font-weight:800;color:#60a5fa;margin-bottom:10px;display:flex;align-items:center;gap:7px}
.step-card{background:#0d1629;border:1px solid #1e3a5f;border-radius:12px;padding:14px 16px;margin-bottom:10px}
.step-header{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.step-num-circle{width:30px;height:30px;border-radius:50%;background:#172554;border:2px solid #3b82f6;
                 color:#60a5fa;font-size:14px;font-weight:800;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.step-title-txt{font-size:13.5px;font-weight:800;color:#e2e8f0}
.step-body{font-size:12.5px;color:#94a3b8;line-height:1.85;padding-left:40px}
.fbadge{font-family:'Courier New',monospace;background:#0f2a10;color:#86efac;
        padding:2px 7px;border-radius:5px;font-size:12px;border:1px solid #166534;display:inline-block}
.nbadge{background:#1c1a07;color:#fbbf24;padding:1px 6px;border-radius:4px;font-size:11px;font-weight:700}
.formula-note{margin-top:6px;padding:8px 12px;background:#0a1a0a;border-radius:8px;
              border:1px solid #166534;font-size:12.5px;color:#4ade80;line-height:1.6}
.msheet{border-collapse:collapse;font-size:11px;margin:8px 0 0 40px;width:calc(100% - 40px)}
.msheet .mh{background:#0f2340;color:#7dd3fc;padding:4px 8px;border:1px solid #1e3a5f;text-align:center;font-weight:700}
.msheet .mr{background:#0f2340;color:#7dd3fc;padding:4px 8px;border:1px solid #1e3a5f;text-align:center;font-weight:700;min-width:24px}
.msheet .mg{background:#0d2040;color:#93c5fd;padding:4px 8px;border:1px solid #1e3a5f;text-align:center}
.msheet .ml{background:#1a1a2e;color:#fbbf24;padding:4px 8px;border:1px solid #1e3a5f;text-align:center;font-weight:700;font-size:10px}
.msheet .mf{background:#0a1a14;color:#86efac;padding:4px 8px;border:1.5px dashed #166534;text-align:center;font-family:monospace;font-size:10px}
.msheet .mc{background:#052e16;color:#4ade80;padding:4px 8px;border:1px solid #166534;text-align:center;font-weight:700}
.msheet .ms{background:#1a0a2e;color:#c084fc;padding:4px 8px;border:1px solid #6b21a8;text-align:center;font-weight:700}
.msheet .mres{background:#1c1505;color:#fbbf24;padding:4px 8px;border:1px solid #b45309;text-align:center;font-weight:700}
.msheet .me{background:#0b1629;padding:4px 8px;border:1px solid #1e293b}
.step-prog{display:flex;align-items:center;gap:3px;margin-bottom:12px;flex-wrap:wrap}
.sdot{width:24px;height:24px;border-radius:50%;border:2px solid #1e293b;background:#141c2b;
      color:#4b5563;font-size:9px;font-weight:700;display:flex;align-items:center;justify-content:center;transition:all .3s;flex-shrink:0}
.sdot.cur{background:#172554;border-color:#3b82f6;color:#60a5fa;box-shadow:0 0 10px rgba(59,130,246,.4)}
.sdot.done{background:#14532d;border-color:#16a34a;color:#4ade80}
.sline{flex:1;height:2px;background:#1e293b;border-radius:2px;min-width:3px}
.sline.done{background:#16a34a}
.legend{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 10px;font-size:11px}
.legend-item{display:flex;align-items:center;gap:5px;color:#94a3b8}
.ldot{width:12px;height:12px;border-radius:3px;flex-shrink:0}
/* Two-column layout */
.sheets-row{display:flex;gap:14px;flex-wrap:wrap;margin:10px 0}
.sheets-col{flex:1;min-width:270px}
.col-title{font-size:11.5px;font-weight:700;color:#94a3b8;margin-bottom:6px;text-align:center;
           background:#0d1629;border-radius:6px;padding:4px 8px;border:1px solid #1e293b}
.sheet-wrap{overflow-x:auto}
.stbl{border-collapse:collapse;font-size:12px;width:100%}
.stbl th{background:#0f2340;color:#7dd3fc;padding:6px 5px;border:1px solid #1e3a5f;text-align:center;font-weight:700;min-width:50px}
.stbl .rnum{background:#0f2340;color:#7dd3fc;padding:6px 3px;border:1px solid #1e3a5f;text-align:center;font-weight:700;font-size:10px;min-width:16px}
.stbl td{border:1px solid #1e293b;height:36px;vertical-align:middle}
.clbl{background:#1a1a2e;color:#fbbf24;text-align:center;font-weight:800;font-size:10.5px;padding:0 4px}
.cgiv{background:#0d2040;color:#93c5fd;text-align:center;font-weight:700;padding:0 4px;font-size:12px}
.csumlbl{background:#1a0a2e;color:#c084fc;text-align:center;font-weight:800;font-size:10.5px;padding:0 4px}
.cemp{background:#0b1629;padding:0 3px}
.cftgt{background:#041510;border:1px solid #1e293b!important;padding:2px;position:relative}
.cftgt.active-step{outline:2px solid #22c55e;outline-offset:-2px;animation:pulseG 1.6s ease-in-out infinite}
.cftgt.filled{background:#041a12}
@keyframes pulseG{0%,100%{outline-color:#22c55e}50%{outline-color:#4ade80;box-shadow:inset 0 0 8px rgba(34,197,94,.2)}}
.cfdisplay{width:100%;height:100%;min-height:30px;display:flex;align-items:center;justify-content:center;
           color:#4ade80;font-family:'Courier New',monospace;font-size:10px;font-weight:700;padding:2px;text-align:center}
.ccomp{background:#052e16;color:#4ade80;text-align:center;font-weight:700;font-family:monospace;font-size:12px;padding:0 4px}
.csum{background:#1a0a2e;color:#c084fc;text-align:center;font-weight:800;font-family:monospace;font-size:13px;padding:0 4px;border:1px solid #6b21a8!important}
.crre{background:#0b1629;border:1.5px dashed #374151!important;padding:0 4px}
.crre.active-step{outline:2px solid #fbbf24;outline-offset:-2px;animation:pulseY 1.6s ease-in-out infinite}
@keyframes pulseY{0%,100%{outline-color:#fbbf24}50%{outline-color:#f59e0b;box-shadow:inset 0 0 8px rgba(251,191,36,.2)}}
.cres{background:#1c1505;color:#fbbf24;text-align:center;font-weight:800;font-family:monospace;font-size:13px;padding:0 4px;border:1px solid #b45309!important}
/* Formula record table */
.frtbl{border-collapse:collapse;font-size:10px;width:100%}
.frtbl th{background:#0c1525;color:#4a6080;padding:5px 4px;border:1px solid #161e2e;text-align:center;font-weight:700;min-width:44px}
.frtbl .frnum{background:#0c1525;color:#4a6080;padding:5px 2px;border:1px solid #161e2e;text-align:center;font-weight:700;font-size:9px;min-width:14px}
.frtbl td{border:1px solid #161e2e;height:32px;vertical-align:middle}
.frtbl .fllbl{background:#111825;color:#6a7ea0;text-align:center;font-weight:700;font-size:9px;padding:0 2px}
.frc{padding:2px 2px;text-align:center;font-family:'Courier New',monospace;font-size:9px;color:#222d3a;background:#080e18;transition:background .35s,color .35s}
.frc.fr-given{background:#071428;color:#6aaccf;font-weight:700}
.frc.fr-formula{background:#061210;color:#45b86a;border:1px dashed #145030!important;font-weight:700}
.frc.fr-sum{background:#0e0620;color:#8854b8;font-weight:800;border:1px solid #4a1880!important}
.frc.fr-result{background:#110800;color:#c09015;font-weight:800;border:1px solid #7a3800!important}
.sinstr{background:#0f2330;border:1.5px solid #0369a1;border-radius:12px;padding:12px 14px;margin-bottom:10px;font-size:13px;line-height:1.85}
.snbadge{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;background:#0369a1;color:#fff;
         border-radius:50%;font-size:11px;font-weight:800;margin-right:6px;flex-shrink:0;vertical-align:middle}
.tcell{font-family:monospace;background:#1a2a3a;color:#93c5fd;padding:1px 6px;border-radius:4px}
.tform{font-family:'Courier New',monospace;background:#0a1a14;color:#86efac;padding:2px 7px;border-radius:5px;font-size:13px;border:1px solid #166534}
.fbar-wrap{display:flex;gap:8px;align-items:center;margin-bottom:10px;flex-wrap:wrap}
.fbar-lbl{font-family:monospace;background:#0f2340;color:#7dd3fc;padding:6px 10px;border-radius:6px;font-size:13px;font-weight:700;border:1px solid #1e3a5f;white-space:nowrap}
#finput{flex:1;min-width:160px;background:#0b1629;border:2px solid #22c55e;border-radius:8px;
        color:#86efac;font-family:'Courier New',monospace;font-size:14px;padding:8px 12px;outline:none}
#finput::placeholder{color:#1e3a2a}
#finput:focus{border-color:#4ade80;background:#041510}
#finput.err{border-color:#ef4444;color:#fca5a5}
#finput.ok{border-color:#4ade80}
.actrow{display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap}
.btn{padding:9px 18px;border:none;border-radius:8px;font-size:13px;font-weight:700;cursor:pointer;transition:.2s;display:flex;align-items:center;gap:5px}
.btn:disabled{opacity:.35;cursor:not-allowed}
.bchk{background:#16a34a;color:#fff}.bchk:hover:not(:disabled){background:#15803d}
.bfill{background:#0369a1;color:#fff}.bfill:hover:not(:disabled){background:#0284c7}
.bsum{background:#7c3aed;color:#fff}.bsum:hover:not(:disabled){background:#6d28d9}
.brst{background:#1e293b;color:#94a3b8}.brst:hover{background:#263547}
.bhint{background:#92400e;color:#fcd34d}.bhint:hover{background:#b45309}
.fb{min-height:26px;font-size:13px;font-weight:700;padding:7px 12px;border-radius:8px;margin-bottom:8px}
.fb.ok{background:#052e16;color:#4ade80;border:1px solid #166534}
.fb.ng{background:#2d0a0a;color:#f87171;border:1px solid #7f1d1d}
.fb.info{background:#0c1a40;color:#93c5fd;border:1px solid #1e3a5f}
.complt{display:none;text-align:center;background:linear-gradient(135deg,rgba(251,191,36,.12),rgba(34,197,94,.08));
        border:2px solid #fbbf24;border-radius:16px;padding:20px;margin-top:12px}
.complt h2{font-size:22px;color:#fbbf24;margin-bottom:6px}
.rgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:12px 0}
.rbox{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:10px;padding:12px 8px;text-align:center}
.rlbl{font-size:11px;color:#94a3b8;margin-bottom:3px}
.rval{font-size:22px;font-weight:900;color:#fbbf24}
@keyframes cfall{0%{transform:translateY(-20px) rotate(0);opacity:1}100%{transform:translateY(100vh) rotate(720deg);opacity:0}}
.cpce{position:fixed;width:8px;height:8px;border-radius:2px;animation:cfall linear forwards;pointer-events:none;z-index:9999}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}
</style>
</head>
<body>
<div class="hero">
  <h1>📊 스프레드시트로 확률변수 분석</h1>
  <p>엑셀 수식을 단계별로 입력하여 확률변수의 기댓값·분산·표준편차를 직접 구해보세요</p>
</div>
<div class="prob-selector" id="prob-selector">
  <button class="prob-btn active" onclick="selProb(0,this)">📌 문제 1 : Y = 3X+2</button>
  <button class="prob-btn" onclick="selProb(1,this)">📌 문제 2 : Y = 2X−1</button>
  <button class="prob-btn" onclick="selProb(2,this)">📌 문제 3 : Y = 2X+3</button>
</div>
<div class="prob-desc">
  <div class="prob-formula" id="pd-formula">Y = 3X + 2</div>
  <div class="prob-info" id="pd-info">X의 값 : 2, 4, 6, 8 &nbsp;|&nbsp; P(Y) = {0.4, 0.3, 0.2, 0.1}</div>
</div>
<div class="tabs">
  <button class="tab-btn active" onclick="swTab('guide',this)">📋 단계 설명</button>
  <button class="tab-btn" onclick="swTab('practice',this)">🧮 직접 해보기</button>
</div>

<!-- GUIDE TAB -->
<div id="tab-guide" class="tab-panel active">
<div class="card">
  <div class="card-title">📋 스프레드시트로 확률변수의 평균·분산·표준편차 구하는 방법</div>
  <div id="guide-content"></div>
</div>
</div><!-- /tab-guide -->
<!-- PRACTICE TAB -->
<div id="tab-practice" class="tab-panel">
  <div class="step-prog" id="sprog">
    <div class="sdot cur" id="sd0">1</div><div class="sline" id="sl01"></div>
    <div class="sdot"     id="sd1">2</div><div class="sline" id="sl12"></div>
    <div class="sdot"     id="sd2">3</div><div class="sline" id="sl23"></div>
    <div class="sdot"     id="sd3">4</div><div class="sline" id="sl34"></div>
    <div class="sdot"     id="sd4">5</div><div class="sline" id="sl45"></div>
    <div class="sdot"     id="sd5">6</div><div class="sline" id="sl56"></div>
    <div class="sdot"     id="sd6">7</div><div class="sline" id="sl67"></div>
    <div class="sdot"     id="sd7">8</div><div class="sline" id="sl78"></div>
    <div class="sdot"     id="sd8">9</div><div class="sline" id="sl89"></div>
    <div class="sdot"     id="sd9">10</div>
  </div>
  <div class="legend">
    <div class="legend-item"><div class="ldot" style="background:#0d2040;border:1px solid #1e3a5f"></div>주어진 데이터</div>
    <div class="legend-item"><div class="ldot" style="background:#041510;border:1.5px dashed #22c55e"></div>수식 입력 셀</div>
    <div class="legend-item"><div class="ldot" style="background:#052e16;border:1px solid #166534"></div>계산된 값</div>
    <div class="legend-item"><div class="ldot" style="background:#1a0a2e;border:1px solid #6b21a8"></div>합계 (Σ)</div>
    <div class="legend-item"><div class="ldot" style="background:#1c1505;border:1px solid #b45309"></div>결과 (V, σ)</div>
  </div>
  <div class="sheets-row">
    <div class="sheets-col">
      <div class="col-title">🧮 직접 입력하기</div>
      <div class="sheet-wrap">
      <table class="stbl" id="main-sheet">
        <tr><th></th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th></tr>
        <tr>
          <td class="rnum">1</td><td class="clbl">X</td>
          <td class="cgiv" id="r1b"></td><td class="cgiv" id="r1c"></td>
          <td class="cgiv" id="r1d"></td><td class="cgiv" id="r1e"></td>
          <td class="cemp"></td>
        </tr>
        <tr>
          <td class="rnum">2</td><td class="clbl">Y</td>
          <td class="cftgt" id="r2b"><div class="cfdisplay" id="d2b">?</div></td>
          <td class="cftgt" id="r2c"><div class="cfdisplay" id="d2c">—</div></td>
          <td class="cftgt" id="r2d"><div class="cfdisplay" id="d2d">—</div></td>
          <td class="cftgt" id="r2e"><div class="cfdisplay" id="d2e">—</div></td>
          <td class="cemp"></td>
        </tr>
        <tr>
          <td class="rnum">3</td><td class="clbl">P(Y)</td>
          <td class="cgiv" id="r3b"></td><td class="cgiv" id="r3c"></td>
          <td class="cgiv" id="r3d"></td><td class="cgiv" id="r3e"></td>
          <td class="csumlbl">합계</td>
        </tr>
        <tr>
          <td class="rnum">4</td><td class="clbl" style="font-size:10px">Y·P(Y)</td>
          <td class="cftgt" id="r4b"><div class="cfdisplay" id="d4b">?</div></td>
          <td class="cftgt" id="r4c"><div class="cfdisplay" id="d4c">—</div></td>
          <td class="cftgt" id="r4d"><div class="cfdisplay" id="d4d">—</div></td>
          <td class="cftgt" id="r4e"><div class="cfdisplay" id="d4e">—</div></td>
          <td class="crre"  id="r4f"></td>
        </tr>
        <tr>
          <td class="rnum">5</td><td class="clbl" style="font-size:9px">Y²·P(Y)</td>
          <td class="cftgt" id="r5b"><div class="cfdisplay" id="d5b">?</div></td>
          <td class="cftgt" id="r5c"><div class="cfdisplay" id="d5c">—</div></td>
          <td class="cftgt" id="r5d"><div class="cfdisplay" id="d5d">—</div></td>
          <td class="cftgt" id="r5e"><div class="cfdisplay" id="d5e">—</div></td>
          <td class="crre"  id="r5f"></td>
        </tr>
        <tr><td class="rnum">6</td><td class="cemp"></td><td class="cemp"></td><td class="cemp"></td><td class="cemp"></td><td class="cemp"></td><td class="cemp"></td></tr>
        <tr><td class="rnum">7</td><td class="cemp"></td><td class="cemp"></td><td class="cemp"></td><td class="cemp"></td><td class="clbl">V(Y)</td><td class="crre" id="r7f"></td></tr>
        <tr><td class="rnum">8</td><td class="cemp"></td><td class="cemp"></td><td class="cemp"></td><td class="cemp"></td><td class="clbl">σ(Y)</td><td class="crre" id="r8f"></td></tr>
      </table>
      </div>
    </div>
    <div class="sheets-col">
      <div class="col-title">📝 수식 기록 (내가 입력한 수식)</div>
      <div class="sheet-wrap">
      <table class="frtbl">
        <tr><th></th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th></tr>
        <tr><td class="frnum">1</td><td class="fllbl">X</td>
            <td class="frc" id="fr_r1b">—</td><td class="frc" id="fr_r1c">—</td>
            <td class="frc" id="fr_r1d">—</td><td class="frc" id="fr_r1e">—</td><td class="frc"></td></tr>
        <tr><td class="frnum">2</td><td class="fllbl">Y</td>
            <td class="frc" id="fr_r2b">—</td><td class="frc" id="fr_r2c">—</td>
            <td class="frc" id="fr_r2d">—</td><td class="frc" id="fr_r2e">—</td><td class="frc"></td></tr>
        <tr><td class="frnum">3</td><td class="fllbl">P(Y)</td>
            <td class="frc" id="fr_r3b">—</td><td class="frc" id="fr_r3c">—</td>
            <td class="frc" id="fr_r3d">—</td><td class="frc" id="fr_r3e">—</td>
            <td class="fllbl" style="font-size:8px">합계</td></tr>
        <tr><td class="frnum">4</td><td class="fllbl" style="font-size:9px">Y·P</td>
            <td class="frc" id="fr_r4b">—</td><td class="frc" id="fr_r4c">—</td>
            <td class="frc" id="fr_r4d">—</td><td class="frc" id="fr_r4e">—</td>
            <td class="frc" id="fr_r4f">—</td></tr>
        <tr><td class="frnum">5</td><td class="fllbl" style="font-size:8px">Y²·P</td>
            <td class="frc" id="fr_r5b">—</td><td class="frc" id="fr_r5c">—</td>
            <td class="frc" id="fr_r5d">—</td><td class="frc" id="fr_r5e">—</td>
            <td class="frc" id="fr_r5f">—</td></tr>
        <tr><td class="frnum">6</td><td class="fllbl"></td><td class="frc"></td><td class="frc"></td><td class="frc"></td><td class="frc"></td><td class="frc"></td></tr>
        <tr><td class="frnum">7</td><td class="fllbl"></td><td class="frc"></td><td class="frc"></td><td class="frc"></td><td class="fllbl">V(Y)</td><td class="frc" id="fr_r7f">—</td></tr>
        <tr><td class="frnum">8</td><td class="fllbl"></td><td class="frc"></td><td class="frc"></td><td class="frc"></td><td class="fllbl">σ(Y)</td><td class="frc" id="fr_r8f">—</td></tr>
      </table>
      </div>
    </div>
  </div><!-- /sheets-row -->

  <div class="sinstr" id="sinstr"></div>
  <div class="fbar-wrap" id="fbar-wrap">
    <div class="fbar-lbl" id="fbar-lbl">B2</div>
    <input type="text" id="finput" placeholder="수식을 입력하세요 (예: =3*B1+2)"
           autocomplete="off" autocorrect="off" spellcheck="false">
    <button class="btn bchk" onclick="chkFormula()">✓ 확인</button>
    <button class="btn bhint" onclick="showHint()">💡 힌트</button>
  </div>
  <div class="actrow">
    <button class="btn bfill" id="fill-btn" onclick="doFill()" disabled>▶ 채우기 핸들로 드래그</button>
    <button class="btn bsum"  id="sum-btn"  onclick="doSum()"  disabled>Σ 합계 구하기</button>
    <button class="btn brst"  onclick="resetPractice()">↺ 처음부터</button>
  </div>
  <div class="fb info" id="feedback">← 수식을 입력하고 확인 버튼을 누르세요</div>
  <div class="complt" id="complt">
    <div style="font-size:34px;margin-bottom:6px">🎉</div>
    <h2>완성!</h2>
    <p style="font-size:13px;color:#94a3b8;margin-bottom:10px">스프레드시트로 확률변수의 통계량을 모두 구했습니다!</p>
    <div class="rgrid">
      <div class="rbox"><div class="rlbl">기댓값 E(Y)</div><div class="rval" id="res-ey">—</div></div>
      <div class="rbox"><div class="rlbl">분산 V(Y)</div><div class="rval" id="res-vy">—</div></div>
      <div class="rbox"><div class="rlbl">표준편차 σ(Y)</div><div class="rval" id="res-sy">—</div></div>
    </div>
    <div style="font-size:12px;color:#94a3b8">다른 문제도 도전해 보세요! 🚀</div>
  </div>
</div><!-- /tab-practice -->
<script>
const PROBS=[
  {formula:"Y = 3X + 2",info:"X의 값 : 2, 4, 6, 8  |  P(Y) = {0.4, 0.3, 0.2, 0.1}",
   X:[2,4,6,8],Y:[8,14,20,26],P:[0.4,0.3,0.2,0.1],
   B2formula:"=3*B1+2",hintB2:"Y = 3X+2 이므로 =3*B1+2",
   YP:[3.2,4.2,4.0,2.6],Y2P:[25.6,58.8,80.0,67.6],EY:14,EY2:232,VY:36,sY:6},
  {formula:"Y = 2X − 1",info:"X의 값 : 1, 2, 3, 4  |  P(Y) = {0.3, 0.3, 0.2, 0.2}",
   X:[1,2,3,4],Y:[1,3,5,7],P:[0.3,0.3,0.2,0.2],
   B2formula:"=2*B1-1",hintB2:"Y = 2X−1 이므로 =2*B1-1",
   YP:[0.3,0.9,1.0,1.4],Y2P:[0.3,2.7,5.0,9.8],EY:3.6,EY2:17.8,VY:4.84,sY:2.2},
  {formula:"Y = 2X + 3",info:"X의 값 : 1, 2, 3, 4  |  P(Y) = {0.1, 0.3, 0.4, 0.2}",
   X:[1,2,3,4],Y:[5,7,9,11],P:[0.1,0.3,0.4,0.2],
   B2formula:"=2*B1+3",hintB2:"Y = 2X+3 이므로 =2*B1+3",
   YP:[0.5,2.1,3.6,2.2],Y2P:[2.5,14.7,32.4,24.2],EY:8.4,EY2:73.8,VY:3.24,sY:1.8}
];
const STEPS=[
  {type:'formula',cell:'B2'},{type:'fill',row:2},
  {type:'formula',cell:'B4'},{type:'fill',row:4},{type:'sum',row:4},
  {type:'formula',cell:'B5'},{type:'fill',row:5},{type:'sum',row:5},
  {type:'formula',cell:'F7'},{type:'formula',cell:'F8'}
];
let curProb=0,curStep=0;

function renderGuide(p){
  const fillFormulas=['B','C','D','E'].map(col=>p.B2formula.replace(/B/g,col));
  const eySquared=Math.round(p.EY*p.EY*10000)/10000;
  document.getElementById('guide-content').innerHTML=`
  <div class="step-card">
    <div class="step-header"><div class="step-num-circle">(1)</div>
      <div class="step-title-txt">1행(X)과 3행(P(Y))에 주어진 값 입력</div></div>
    <div class="step-body">
      1행에 확률변수 X 값을, 3행에 P(Y) 값을 입력합니다.<br>
      <span class="nbadge">${p.formula}, X ∈ {${p.X.join(',')}}, P(Y) = {${p.P.join(', ')}}</span>
      <table class="msheet" style="margin-top:8px">
        <tr><th class="mh"></th><th class="mh">A</th><th class="mh">B</th><th class="mh">C</th><th class="mh">D</th><th class="mh">E</th></tr>
        <tr><td class="mr">1</td><td class="ml">X</td>${p.X.map(v=>`<td class="mg">${v}</td>`).join('')}</tr>
        <tr><td class="mr">3</td><td class="ml">P(Y)</td>${p.P.map(v=>`<td class="mg">${v}</td>`).join('')}</tr>
      </table>
    </div>
  </div>
  <div class="step-card">
    <div class="step-header"><div class="step-num-circle">(2)</div>
      <div class="step-title-txt">셀 B2에 <span class="fbadge">${p.B2formula}</span> 입력 → 채우기 핸들로 E2까지</div></div>
    <div class="step-body">
      ${p.formula} 이므로 셀 B2에 <span class="fbadge">${p.B2formula}</span> 를 입력하고 E2까지 채우기 핸들을 드래그합니다.
      <table class="msheet" style="margin-top:8px">
        <tr><th class="mh"></th><th class="mh">A</th><th class="mh">B</th><th class="mh">C</th><th class="mh">D</th><th class="mh">E</th></tr>
        <tr><td class="mr">2</td><td class="ml">Y</td>${fillFormulas.map(f=>`<td class="mf">${f}</td>`).join('')}</tr>
        <tr><td class="mr"></td><td class="me"></td>${p.Y.map(v=>`<td class="mc">${v}</td>`).join('')}</tr>
      </table>
      <div style="margin-top:5px;font-size:11.5px;color:#7dd3fc">
        ✦ B2 수식을 드래그하면 B1→C1→D1→E1로 자동 변경됩니다.
      </div>
    </div>
  </div>
  <div class="step-card">
    <div class="step-header"><div class="step-num-circle">(3)</div>
      <div class="step-title-txt">셀 B4에 <span class="fbadge">=B2*B3</span> → 채우기 핸들 → Σ → E(Y)</div></div>
    <div class="step-body">
      B4에 <span class="fbadge">=B2*B3</span> 입력 후 E4까지 채우기 핸들, Σ 클릭 → F4에 E(Y) = ${p.EY}
      <table class="msheet" style="margin-top:8px">
        <tr><th class="mh"></th><th class="mh">A</th><th class="mh">B</th><th class="mh">C</th><th class="mh">D</th><th class="mh">E</th><th class="mh">F</th></tr>
        <tr><td class="mr">4</td><td class="ml" style="font-size:10px">Y·P(Y)</td>
            <td class="mf">=B2*B3</td><td class="mf">=C2*C3</td><td class="mf">=D2*D3</td><td class="mf">=E2*E3</td>
            <td class="ms">${p.EY}</td></tr>
      </table>
    </div>
  </div>
  <div class="step-card">
    <div class="step-header"><div class="step-num-circle">(4)</div>
      <div class="step-title-txt">셀 B5에 <span class="fbadge">=B2^2*B3</span> → 채우기 핸들 → Σ → E(Y²)</div></div>
    <div class="step-body">
      B5에 <span class="fbadge">=B2^2*B3</span> 입력 후 같은 방법으로 F5에 E(Y²) = ${p.EY2}
      <table class="msheet" style="margin-top:8px">
        <tr><th class="mh"></th><th class="mh">A</th><th class="mh">B</th><th class="mh">C</th><th class="mh">D</th><th class="mh">E</th><th class="mh">F</th></tr>
        <tr><td class="mr">5</td><td class="ml" style="font-size:9px">Y²·P(Y)</td>
            <td class="mf">=B2^2*B3</td><td class="mf">=C2^2*C3</td><td class="mf">=D2^2*D3</td><td class="mf">=E2^2*E3</td>
            <td class="ms">${p.EY2}</td></tr>
      </table>
    </div>
  </div>
  <div class="step-card">
    <div class="step-header"><div class="step-num-circle">(5)</div>
      <div class="step-title-txt">F7에 <span class="fbadge">=F5-F4^2</span>, F8에 <span class="fbadge">=SQRT(F7)</span></div></div>
    <div class="step-body">
      분산 V(Y) = E(Y²) − {E(Y)}² 와 표준편차 σ(Y) = √V(Y) 를 셀 수식으로 입력합니다.
      <table class="msheet" style="margin-top:8px">
        <tr><th class="mh"></th><th class="mh">E</th><th class="mh">F</th></tr>
        <tr><td class="mr">7</td><td class="ml">V(Y)</td><td class="mf">=F5-F4^2</td></tr>
        <tr><td class="mr">8</td><td class="ml">σ(Y)</td><td class="mf">=SQRT(F7)</td></tr>
      </table>
      <div class="formula-note">
        📐 V(Y) = E(Y²) − {E(Y)}² = F5 − (F4)² = ${p.EY2} − ${eySquared} = <strong>${p.VY}</strong><br>
        📐 σ(Y) = √V(Y) = SQRT(F7) = √${p.VY} = <strong>${p.sY}</strong>
      </div>
    </div>
  </div>`;
}
function swTab(name,btn){
  document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('tab-'+name).classList.add('active');
}
function selProb(idx,btn){
  curProb=idx;
  document.querySelectorAll('.prob-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  const p=PROBS[idx];
  document.getElementById('pd-formula').textContent=p.formula;
  document.getElementById('pd-info').textContent=p.info;
  fillSheetData(p);
  renderGuide(p);
  resetPractice();
}
function fillSheetData(p){
  const cols=['b','c','d','e'];
  cols.forEach((c,i)=>{
    document.getElementById(`r1${c}`).textContent=p.X[i];
    document.getElementById(`r3${c}`).textContent=p.P[i];
    setFR('fr_r1'+c,p.X[i],'given');
    setFR('fr_r3'+c,p.P[i],'given');
  });
}
function setFR(id,text,type){
  const el=document.getElementById(id);
  if(!el)return;
  el.className='frc'+(type?' fr-'+type:'');
  el.textContent=text;
}
function resetFormulaRecord(){
  const cols=['b','c','d','e'];
  cols.forEach(c=>{setFR('fr_r2'+c,'—','');setFR('fr_r4'+c,'—','');setFR('fr_r5'+c,'—','');});
  ['fr_r4f','fr_r5f','fr_r7f','fr_r8f'].forEach(id=>setFR(id,'—',''));
}
function resetPractice(){
  curStep=0;
  const cols=['b','c','d','e'];
  [2,4,5].forEach(rn=>cols.forEach(c=>{
    const el=document.getElementById(`r${rn}${c}`);
    el.className='cftgt';
    el.innerHTML=`<div class="cfdisplay" id="d${rn}${c}">${c==='b'?'?':'—'}</div>`;
  }));
  ['r4f','r5f','r7f','r8f'].forEach(id=>{const el=document.getElementById(id);el.className='crre';el.textContent='';});
  const fi=document.getElementById('finput');fi.value='';fi.className='';
  document.getElementById('fill-btn').disabled=true;
  document.getElementById('sum-btn').disabled=true;
  document.getElementById('fill-btn').textContent='▶ 채우기 핸들로 드래그';
  document.getElementById('complt').style.display='none';
  document.getElementById('fbar-wrap').style.display='flex';
  document.getElementById('sinstr').style.display='';
  resetFormulaRecord();
  setFeedback('info','← 수식을 입력하고 확인 버튼을 누르세요');
  updateStepUI();
}
function updateStepUI(){
  if(curStep>=STEPS.length){showCompletion();return;}
  const step=STEPS[curStep],p=PROBS[curProb];
  const sinstr=document.getElementById('sinstr');
  const fbar=document.getElementById('fbar-wrap');
  const fillBtn=document.getElementById('fill-btn');
  const sumBtn=document.getElementById('sum-btn');
  document.querySelectorAll('.cftgt').forEach(el=>el.classList.remove('active-step'));
  document.querySelectorAll('.crre').forEach(el=>el.classList.remove('active-step'));
  for(let i=0;i<STEPS.length;i++){
    const d=document.getElementById(`sd${i}`);
    if(i<curStep){d.className='sdot done';d.textContent='✓';}
    else if(i===curStep){d.className='sdot cur';d.textContent=i+1;}
    else{d.className='sdot';d.textContent=i+1;}
  }
  for(let i=0;i<STEPS.length-1;i++)
    document.getElementById(`sl${i}${i+1}`).className='sline'+(i<curStep?' done':'');
  if(step.type==='formula'){
    fbar.style.display='flex';fillBtn.disabled=true;sumBtn.disabled=true;
    const fi=document.getElementById('finput');fi.value='';fi.className='';
    document.getElementById('fbar-lbl').textContent=step.cell;
    setTimeout(()=>fi.focus(),80);
    const cellMap={'B2':'r2b','B4':'r4b','B5':'r5b','F7':'r7f','F8':'r8f'};
    const cel=document.getElementById(cellMap[step.cell]);
    if(cel)cel.classList.add('active-step');
    const im={
      'B2':`<span class="snbadge">(2)</span> 셀 <span class="tcell">B2</span> 에 Y와 X의 관계를 수식으로 입력하세요.
            <div style="font-size:11.5px;color:#7dd3fc;margin-top:5px">
            ✦ ${p.formula} 이므로 B1(X값)을 사용한 수식을 입력합니다.
            &nbsp;<span style="color:#fbbf24">(예: Y = aX+b → =a*B1+b)</span></div>`,
      'B4':`<span class="snbadge">(3)</span> 셀 <span class="tcell">B4</span> 에 수식 <span class="tform">=B2*B3</span> 를 입력하세요.
            <div style="font-size:11.5px;color:#7dd3fc;margin-top:5px">✦ Y×확률 P(Y) → Y·P(Y) 의 첫 번째 값</div>`,
      'B5':`<span class="snbadge">(4)</span> 셀 <span class="tcell">B5</span> 에 수식 <span class="tform">=B2^2*B3</span> 를 입력하세요.
            <div style="font-size:11.5px;color:#7dd3fc;margin-top:5px">✦ Y²×확률 P(Y) &nbsp;<span style="color:#fbbf24">( ^2 는 제곱 )</span></div>`,
      'F7':`<span class="snbadge">(5)</span> 셀 <span class="tcell">F7</span> 에 수식 <span class="tform">=F5-F4^2</span> 를 입력하세요.
            <div style="font-size:11.5px;color:#7dd3fc;margin-top:5px">✦ 분산 V(Y) = E(Y²)−{E(Y)}² = <span style="color:#c084fc">F5</span>−(<span style="color:#c084fc">F4</span>)²</div>`,
      'F8':`<span class="snbadge">(5)</span> 셀 <span class="tcell">F8</span> 에 수식 <span class="tform">=SQRT(F7)</span> 를 입력하세요.
            <div style="font-size:11.5px;color:#7dd3fc;margin-top:5px">✦ 표준편차 σ(Y) = √V(Y) = SQRT(F7)</div>`
    };
    sinstr.innerHTML=im[step.cell]||'';
    setFeedback('info','← 수식을 입력하고 확인 버튼을 누르세요');
  }else if(step.type==='fill'){
    fbar.style.display='none';fillBtn.disabled=false;sumBtn.disabled=true;
    const sb=step.row===2?'(2)':step.row===4?'(3)':'(4)';
    fillBtn.textContent=`▶ 채우기 핸들로 E${step.row}까지 드래그`;
    sinstr.innerHTML=`<span class="snbadge">${sb}</span>
      '채우기 핸들'로 <span class="tcell">B${step.row}</span> 수식을 <span class="tcell">E${step.row}</span> 까지 드래그하세요.
      <div style="font-size:11.5px;color:#7dd3fc;margin-top:5px">✦ 드래그하면 B→C→D→E로 자동 변경됩니다.</div>`;
    setFeedback('info','← 아래 채우기 핸들 버튼을 클릭하세요');
  }else if(step.type==='sum'){
    fbar.style.display='none';fillBtn.disabled=true;sumBtn.disabled=false;
    const sb=step.row===4?'(3)':'(4)';
    const rl=step.row===4?'Y·P(Y)':'Y²·P(Y)',cl=step.row===4?'F4':'F5';
    sinstr.innerHTML=`<span class="snbadge">${sb}</span>
      <strong>Σ</strong> 버튼으로 ${rl} 의 합계를 구하세요.
      <div style="font-size:11.5px;color:#7dd3fc;margin-top:5px">
      ✦ B${step.row}:E${step.row} 의 합이 <span class="tcell">${cl}</span> 에 기록됩니다.</div>`;
    setFeedback('info','← 아래 Σ 합계 구하기 버튼을 클릭하세요');
  }
}
function norm(s){return s.replace(/\s/g,'').toUpperCase();}
function chkFormula(){
  const step=STEPS[curStep];if(step.type!=='formula')return;
  const fi=document.getElementById('finput');const val=fi.value.trim();const p=PROBS[curProb];
  const exp={'B2':p.B2formula,'B4':'=B2*B3','B5':'=B2^2*B3','F7':'=F5-F4^2','F8':'=SQRT(F7)'};
  if(norm(val)===norm(exp[step.cell])){
    fi.className='ok';
    if(step.cell==='B2'){
      document.getElementById('d2b').textContent=p.B2formula;
      document.getElementById('r2b').classList.add('filled');
      setFR('fr_r2b',p.B2formula,'formula');
      setFeedback('ok',`✓ 정확해요! B2 = ${p.Y[0]}  채우기 핸들로 E2까지 드래그하세요.`);
    }else if(step.cell==='B4'){
      document.getElementById('d4b').textContent='=B2*B3';
      document.getElementById('r4b').classList.add('filled');
      setFR('fr_r4b','=B2*B3','formula');
      setFeedback('ok','✓ 정확해요! 채우기 핸들로 E4까지 드래그하세요.');
    }else if(step.cell==='B5'){
      document.getElementById('d5b').textContent='=B2^2*B3';
      document.getElementById('r5b').classList.add('filled');
      setFR('fr_r5b','=B2^2*B3','formula');
      setFeedback('ok','✓ 정확해요! 채우기 핸들로 E5까지 드래그하세요.');
    }else if(step.cell==='F7'){
      document.getElementById('r7f').className='cres';
      document.getElementById('r7f').textContent=p.VY;
      setFR('fr_r7f','=F5-F4^2','result');
      setFeedback('ok',`✓ V(Y) = ${p.VY}  분산을 구했습니다! 이제 표준편차를 구하세요.`);
    }else if(step.cell==='F8'){
      document.getElementById('r8f').className='cres';
      document.getElementById('r8f').textContent=p.sY;
      setFR('fr_r8f','=SQRT(F7)','result');
      setFeedback('ok',`✓ σ(Y) = ${p.sY}  표준편차까지 구했습니다! 🎊`);
    }
    curStep++;setTimeout(updateStepUI,600);
  }else{
    fi.className='err';fi.style.animation='none';fi.offsetHeight;fi.style.animation='shake .4s ease';
    if(!val.startsWith('=')){setFeedback('ng','❌ 수식은 = 기호로 시작해야 합니다.');}
    else if(step.cell==='B5'&&norm(val).includes('B2*B3')&&!norm(val).includes('^2')){
      setFeedback('ng','❌ 제곱을 잊었어요! Y² 는 B2^2 으로 표현합니다: =B2^2*B3');
    }else{setFeedback('ng','❌ 수식이 다릅니다. 힌트 버튼을 눌러보세요.');}
  }
}
function doFill(){
  const step=STEPS[curStep];if(step.type!=='fill')return;
  const rn=step.row,p=PROBS[curProb];
  const COLS=['C','D','E'],lc=['c','d','e'];
  const srcFmt=rn===2?p.B2formula:(rn===4?'=B2*B3':'=B2^2*B3');
  COLS.forEach((C,i)=>{
    const formula=srcFmt.replace(/B/g,C);
    document.getElementById(`r${rn}${lc[i]}`).classList.add('filled');
    document.getElementById(`d${rn}${lc[i]}`).textContent=formula;
    setFR(`fr_r${rn}${lc[i]}`,formula,'formula');
  });
  if(rn===2)setFeedback('ok',`✓ Y 값 채우기 완료! (${p.Y.join(', ')})  이제 B4 수식을 입력하세요.`);
  else setFeedback('ok','✓ 채우기 완료! Σ 합계 구하기 버튼을 클릭하세요.');
  curStep++;setTimeout(updateStepUI,400);
}
function doSum(){
  const step=STEPS[curStep];if(step.type!=='sum')return;
  const p=PROBS[curProb],rn=step.row,lc=['b','c','d','e'];
  if(rn===4){
    lc.forEach((c,i)=>{const el=document.getElementById(`r4${c}`);el.className='ccomp';el.innerHTML='';el.textContent=p.YP[i];});
    document.getElementById('r4f').className='csum';document.getElementById('r4f').textContent=p.EY;
    setFR('fr_r4f','Σ='+p.EY,'sum');
    setFeedback('ok',`✓ E(Y) = ${p.EY}  기댓값(평균)을 구했습니다! 🎊`);
  }else{
    lc.forEach((c,i)=>{const el=document.getElementById(`r5${c}`);el.className='ccomp';el.innerHTML='';el.textContent=p.Y2P[i];});
    document.getElementById('r5f').className='csum';document.getElementById('r5f').textContent=p.EY2;
    setFR('fr_r5f','Σ='+p.EY2,'sum');
    setFeedback('ok',`✓ E(Y²) = ${p.EY2}  이제 분산 수식을 입력하세요!`);
  }
  curStep++;setTimeout(updateStepUI,400);
}
function showHint(){
  const step=STEPS[curStep];if(step.type!=='formula')return;
  const p=PROBS[curProb];
  const h={'B2':`💡 힌트: ${p.hintB2}`,'B4':'💡 B4 = Y×P(Y) → =B2*B3',
           'B5':'💡 B5 = Y²×P(Y) → =B2^2*B3  ( ^는 거듭제곱 )',
           'F7':'💡 V(Y) = E(Y²)−{E(Y)}² = F5−F4² → =F5-F4^2',
           'F8':'💡 σ(Y) = √V(Y) = SQRT(분산) → =SQRT(F7)'};
  setFeedback('info',h[step.cell]||'');
}
function showCompletion(){
  const p=PROBS[curProb];
  for(let i=0;i<STEPS.length;i++){const d=document.getElementById(`sd${i}`);d.className='sdot done';d.textContent='✓';}
  for(let i=0;i<STEPS.length-1;i++)document.getElementById(`sl${i}${i+1}`).className='sline done';
  document.getElementById('fbar-wrap').style.display='none';
  document.getElementById('sinstr').style.display='none';
  document.getElementById('res-ey').textContent=p.EY;
  document.getElementById('res-vy').textContent=p.VY;
  document.getElementById('res-sy').textContent=p.sY;
  document.getElementById('complt').style.display='block';
  setFeedback('ok','🎉 모든 단계 완성! 스프레드시트로 평균·분산·표준편차를 모두 구했습니다!');
  launchConfetti();
}
function setFeedback(cls,msg){const el=document.getElementById('feedback');el.className='fb '+cls;el.textContent=msg;}
function launchConfetti(){
  const cols=['#fbbf24','#4ade80','#60a5fa','#c084fc','#f87171','#34d399'];
  for(let i=0;i<35;i++){
    setTimeout(()=>{
      const el=document.createElement('div');el.className='cpce';
      el.style.left=Math.random()*100+'vw';el.style.top='-10px';
      el.style.background=cols[Math.floor(Math.random()*cols.length)];
      el.style.animationDuration=(1.4+Math.random()*1.6)+'s';
      el.style.transform=`rotate(${Math.random()*360}deg)`;
      document.body.appendChild(el);setTimeout(()=>el.remove(),3500);
    },i*75);
  }
}
document.getElementById('finput').addEventListener('keydown',e=>{if(e.key==='Enter')chkFormula();});
selProb(0,document.querySelector('.prob-btn.active'));
</script>
</body>
</html>
"""


def render():
    components.html(_HTML, height=1700, scrolling=True)
