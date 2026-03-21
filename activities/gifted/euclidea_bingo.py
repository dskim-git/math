META = {
    "title": "미니: 작도 게임(빙고)",
    "description": "작도 빙고 게임. 5×5 빙고판에서 문제를 선택하고 팀별 점수를 관리하세요.",
    "order": 42,
    "hidden": True,
}

# ─────────────────────────────────────────────────────────────────
#  실시간 동기화 설정 (Firebase Realtime Database)
#
#  설정 방법:
#  1. https://console.firebase.google.com 에서 프로젝트 생성
#  2. Realtime Database 활성화 (테스트 모드로 시작)
#  3. 데이터베이스 URL 복사 (예: https://xxx-default-rtdb.firebaseio.com)
#  4. 아래 FIREBASE_DB_URL 에 붙여넣기
#
#  설정하지 않으면: 교사 단독 조작 모드로만 동작
# ─────────────────────────────────────────────────────────────────
FIREBASE_DB_URL = "https://mathlab-bingo-default-rtdb.asia-southeast1.firebasedatabase.app/"   # 예: "https://my-project-default-rtdb.firebaseio.com"

# ─────────────────────────────────────────────────────────────────
#  문제별 GeoGebra URL (학생 화면에 표시)
#  예: GEOGEBRA_URLS = {1: "https://www.geogebra.org/m/xxxxx", ...}
#  비어 있으면 GeoGebra Classic 기본 화면 표시
# ─────────────────────────────────────────────────────────────────
GEOGEBRA_CALC_URLS = {
    1:  "https://www.geogebra.org/calculator/ga8pkmee",
    2:  "https://www.geogebra.org/calculator/ep7wjv4f",
    3:  "https://www.geogebra.org/calculator/segp6e92",
    4:  "https://www.geogebra.org/calculator/x7xmayph",
    5:  "https://www.geogebra.org/calculator/cacmctnz",
    6:  "https://www.geogebra.org/calculator/byu9dcq3",
    7:  "https://www.geogebra.org/calculator/kbb4musk",
    8:  "https://www.geogebra.org/calculator/zn7ygwrr",
    9:  "https://www.geogebra.org/calculator/xgycthvh",
    10: "https://www.geogebra.org/calculator/ckbdj36s",
    11: "https://www.geogebra.org/calculator/wvzvn7cp",
    12: "https://www.geogebra.org/calculator/ytgu62dp",
    13: "https://www.geogebra.org/calculator/hrjv42r8",
    14: "https://www.geogebra.org/calculator/eszrzhgu",
    15: "https://www.geogebra.org/calculator/eqgakujy",
    16: "https://www.geogebra.org/calculator/vhnahfmd",
    17: "https://www.geogebra.org/calculator/msrr3zvu",
    18: "https://www.geogebra.org/calculator/h99jdexn",
    19: "https://www.geogebra.org/calculator/uzrvbykv",
    20: "https://www.geogebra.org/calculator/rca2tyje",
    21: "https://www.geogebra.org/calculator/zdepjgnt",
    22: "https://www.geogebra.org/calculator/mahcyjng",
    23: "https://www.geogebra.org/calculator/aaccjjxn",
    24: "https://www.geogebra.org/calculator/zt9ekaw9",
    25: "https://www.geogebra.org/calculator/gfjjqazq",
}

GEOGEBRA_URLS = {
    1:  "https://www.geogebra.org/material/iframe/id/ga8pkmee/width/1912/height/858/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false",
    2:  "https://www.geogebra.org/material/iframe/id/ep7wjv4f/width/1912/height/858/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false",
    3:  "https://www.geogebra.org/material/iframe/id/segp6e92/width/1912/height/858/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false",
    4:  "https://www.geogebra.org/material/iframe/id/x7xmayph/width/1912/height/858/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false",
    5:  "https://www.geogebra.org/material/iframe/id/cacmctnz/width/1912/height/858/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false",
    6:  "https://www.geogebra.org/material/iframe/id/byu9dcq3/width/1912/height/858/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false",
    7:  "https://www.geogebra.org/material/iframe/id/kbb4musk/width/1912/height/858/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false",
    8:  "https://www.geogebra.org/material/iframe/id/zn7ygwrr/width/1912/height/858/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false",
    9:  "https://www.geogebra.org/material/iframe/id/xgycthvh/width/1912/height/858/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false",
    10: "https://www.geogebra.org/material/iframe/id/ckbdj36s/width/1912/height/858/border/888888/sfsb/true/smb/false/stb/false/stbh/false/ai/false/asb/false/sri/false/rc/false/ld/false/sdz/false/ctl/false",
}

import streamlit.components.v1 as components
import json as _json
import importlib.util as _ilu, os as _os

# ── 커스텀 작도 캔버스 모듈 로드 ──────────────────────────────
_canvas_spec = _ilu.spec_from_file_location(
    "_geo_canvas",
    _os.path.join(_os.path.dirname(__file__), "_geo_canvas.py"))
_canvas_mod = _ilu.module_from_spec(_canvas_spec)
_canvas_spec.loader.exec_module(_canvas_mod)
_GEO_CSS          = _canvas_mod.GEO_CSS
_GEO_HTML         = _canvas_mod.GEO_HTML
_GEO_JS_TEMPLATE  = _canvas_mod.GEO_JS_TEMPLATE
_CANVAS_PROBLEMS  = _canvas_mod.PROBLEMS_CONFIG

_TEMPLATE = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{background:#0a1628;color:#e2e8f0;font-family:'Segoe UI','Noto Sans KR',system-ui,sans-serif;line-height:1.5;font-size:14px;}
#app{max-width:1100px;margin:0 auto;padding:10px 14px 30px;}

/* ── role banner ── */
.role-banner{display:flex;align-items:center;gap:8px;padding:7px 12px;border-radius:8px;margin-bottom:10px;font-size:0.8rem;font-weight:700;}
.role-banner.teacher{background:rgba(251,191,36,0.12);border:1px solid rgba(251,191,36,0.3);color:#fbbf24;}
.role-banner.student{background:rgba(56,189,248,0.10);border:1px solid rgba(56,189,248,0.25);color:#38bdf8;}
.sync-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;background:#334155;}
.sync-dot.on{background:#4ade80;box-shadow:0 0 6px #4ade8088;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}

/* ── ctrl ── */
.ctrl-row{display:flex;align-items:center;gap:8px;margin-bottom:12px;flex-wrap:wrap;}
.ctrl-btn{padding:6px 14px;border-radius:7px;border:1.5px solid #334155;background:#1e293b;color:#94a3b8;cursor:pointer;font-size:0.8rem;font-weight:700;transition:all .15s;}
.ctrl-btn:hover{border-color:#64748b;color:#f8fafc;}
.ctrl-btn.danger{border-color:#dc2626;color:#fca5a5;}
.ctrl-btn.danger:hover{background:#7f1d1d;}
.ctrl-btn.class-on{border-color:#16a34a;background:#14532d;color:#4ade80;}
.ctrl-btn.class-on:hover{background:#15803d;border-color:#4ade80;}
.ctrl-btn.class-off{border-color:#64748b;color:#94a3b8;}
.confirm-box{background:#1e293b;border:1.5px solid #dc2626;border-radius:9px;padding:10px 14px;display:none;align-items:center;gap:10px;}
.confirm-box p{color:#fca5a5;font-size:0.82rem;}

/* ── main layout ── */
.main-layout{display:flex;gap:18px;align-items:flex-start;}
.bingo-wrap{flex:0 0 auto;}
.side-wrap{flex:1;min-width:175px;}

/* ── bingo table ── */
.bingo-tbl{border-collapse:separate;border-spacing:5px;background:#0f1f38;border-radius:14px;padding:10px;border:2px solid #0e7490;}

/* ── cell ── */
.bingo-cell{
  width:94px;height:104px;
  background:#0a1628;border:2px solid #155e75;
  border-radius:9px;cursor:pointer;
  vertical-align:top;padding:5px 5px 4px;
  transition:all .2s;user-select:none;
}
.bingo-cell.teacher-only{cursor:pointer;}
.bingo-cell.no-click{cursor:default;pointer-events:none;}
.bingo-cell:not(.no-click):hover{border-color:#22d3ee;background:#1e3a5f;}
.bingo-cell.owned{border-width:2.5px;}
.bingo-cell.perm{box-shadow:0 0 14px #fbbf2455;}

.c-top{display:flex;justify-content:space-between;align-items:flex-start;height:18px;overflow:hidden;}
.c-num{font-size:0.6rem;font-weight:700;color:#475569;flex-shrink:0;}
.c-owner-tag{font-size:0.56rem;font-weight:800;padding:1px 4px;border-radius:3px;white-space:nowrap;}
.c-mid{display:flex;flex-direction:column;align-items:center;justify-content:center;height:58px;}
.vL{font-size:1.22rem;font-weight:900;color:#38bdf8;line-height:1.15;}
.vE{font-size:1.0rem;font-weight:700;color:#94a3b8;line-height:1.15;}
.bingo-cell.owned .vL,.bingo-cell.owned .vE{color:#f1f5f9;}
.c-conds{display:flex;gap:2px;justify-content:center;align-items:center;height:18px;}
.cd{font-size:0.6rem;font-weight:800;padding:2px 5px;border-radius:4px;
  background:#1e293b;color:#334155;border:1px solid #334155;}
.cd.on{color:#f8fafc;border-color:transparent;}

/* ── team cards ── */
.team-card{border-radius:10px;padding:10px 12px;margin-bottom:9px;border:2px solid rgba(255,255,255,0.1);}
.tc-hd{display:flex;align-items:center;justify-content:space-between;margin-bottom:3px;}
.tc-name{font-size:1rem;font-weight:900;}
.tc-score{font-size:1.5rem;font-weight:900;}
.tc-score-lbl{font-size:0.65rem;color:#94a3b8;}
.tc-det{font-size:0.68rem;color:#64748b;margin-top:3px;}

/* ── bingo lines ── */
.bingo-box{background:#0f1f38;border-radius:9px;padding:9px 11px;margin-top:8px;border:1px solid #1e3a5f;}
.bingo-box-t{font-size:0.7rem;color:#64748b;margin-bottom:5px;}
.bingo-tags{display:flex;gap:4px;flex-wrap:wrap;}
.bingo-tag{padding:2px 8px;border-radius:5px;font-size:0.7rem;font-weight:800;}

/* ══════ PROBLEM PAGE ══════ */
#pg-problem{display:none;}

.prob-meta-line{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:8px;font-size:0.9rem;font-weight:700;}
.prob-meta-line .mn{color:#f8fafc;font-size:1.05rem;}
.prob-meta-line .ml{color:#38bdf8;}
.prob-meta-line .me{color:#c4b5fd;}

.gg-btn{display:inline-flex;align-items:center;gap:5px;padding:5px 12px;border-radius:7px;border:1.5px solid #166534;background:#14532d;color:#4ade80;cursor:pointer;font-size:0.78rem;font-weight:800;text-decoration:none;transition:all .15s;margin-left:auto;}
.gg-btn:hover{background:#15803d;border-color:#4ade80;color:#f0fdf4;}

.back-btn{display:inline-flex;align-items:center;gap:6px;padding:7px 16px;border-radius:8px;border:1.5px solid #334155;background:#1e293b;color:#94a3b8;cursor:pointer;font-size:0.82rem;font-weight:700;margin-bottom:14px;transition:all .15s;}
.back-btn:hover{border-color:#64748b;color:#f8fafc;}

.prob-layout{display:flex;gap:14px;align-items:flex-start;}
@media(max-width:720px){.prob-layout{flex-direction:column;}}
.prob-left{flex:1.3;min-width:0;}
.prob-right{flex:1;min-width:0;}

.sec-box{background:#0f1f38;border-radius:10px;padding:12px;margin-bottom:12px;border:1px solid #1e3a5f;}
.sec-title{font-size:0.76rem;font-weight:800;color:#475569;margin-bottom:9px;text-transform:uppercase;letter-spacing:.05em;}

table.tool-tbl{width:100%;border-collapse:collapse;}
table.tool-tbl th{background:#0a1628;color:#64748b;font-size:0.7rem;font-weight:700;padding:5px 8px;text-align:center;border:1px solid #1e3a5f;}
table.tool-tbl td{padding:6px 8px;text-align:center;border:1px solid #0a1628;font-size:0.82rem;}
table.tool-tbl tr:nth-child(odd) td{background:#0f1f38;}
table.tool-tbl tr:nth-child(even) td{background:#0a1628;}
table.tool-tbl td:first-child{text-align:left;font-weight:700;color:#e2e8f0;}
.bl{display:inline-block;padding:2px 7px;border-radius:5px;background:#1e3a5f;color:#7dd3fc;font-weight:800;font-size:0.75rem;border:1px solid #0ea5e9;}
.be{display:inline-block;padding:2px 7px;border-radius:5px;background:#1a1040;color:#c4b5fd;font-weight:800;font-size:0.75rem;border:1px solid #8b5cf6;}

/* condition rows (teacher only) */
.cond-row{display:flex;align-items:center;gap:5px;margin-bottom:9px;flex-wrap:wrap;}
.cond-lbl{font-size:0.76rem;font-weight:800;min-width:62px;}
.cond-lbl.L{color:#38bdf8;}
.cond-lbl.E{color:#c4b5fd;}
.cond-lbl.V{color:#fde68a;}
.cond-opt{padding:4px 9px;border-radius:6px;border:1.5px solid #334155;background:#0a1628;color:#475569;cursor:pointer;font-size:0.74rem;font-weight:700;transition:all .15s;}
.cond-opt:hover{border-color:#475569;color:#94a3b8;}
.cond-opt.sel{color:#f8fafc;}

.owner-box{border-radius:8px;border:1.5px solid #334155;padding:10px 12px;font-size:0.84rem;margin-top:2px;}
.score-guide{font-size:0.76rem;color:#64748b;line-height:1.9;}

/* ── Geometry canvas (injected) ── */
__GEO_CSS__

/* waiting overlay for student bingo board */
.student-hint{
  background:rgba(56,189,248,0.07);border:1px dashed rgba(56,189,248,0.2);
  border-radius:9px;padding:10px 14px;margin-bottom:10px;
  font-size:0.8rem;color:#38bdf8;text-align:center;
}
</style>
</head>
<body>
<div id="app">

<!-- role banner -->
<div class="role-banner" id="role-banner">
  <span class="sync-dot" id="sync-dot"></span>
  <span id="role-text">연결 확인 중...</span>
</div>

<!-- ═══════════════════════════
     BINGO PAGE
═══════════════════════════ -->
<div id="pg-bingo">
  <!-- Teacher-only controls -->
  <div class="ctrl-row" id="teacher-ctrl">
    <button class="ctrl-btn class-on" id="sync-toggle-btn" onclick="toggleSync()">🎓 수업 모드 ON</button>
    <button class="ctrl-btn danger" onclick="confirmReset()">🗑 전체 초기화</button>
    <div class="confirm-box" id="confirm-box">
      <p>정말 모든 진행 상황을 초기화할까요?</p>
      <button class="ctrl-btn danger" onclick="doReset()">초기화</button>
      <button class="ctrl-btn" onclick="cancelReset()">취소</button>
    </div>
  </div>

  <!-- Student hint -->
  <div class="student-hint" id="student-hint" style="display:none">
    📡 선생님이 문제를 선택하면 자동으로 이동합니다.
  </div>

  <div class="main-layout">
    <div class="bingo-wrap">
      <table class="bingo-tbl" id="bingo-tbl"></table>
    </div>
    <div class="side-wrap">
      <div id="team-cards"></div>
      <div class="bingo-box">
        <div class="bingo-box-t">🎊 빙고 현황</div>
        <div class="bingo-tags" id="bingo-tags">
          <span style="font-size:0.73rem;color:#334155">아직 빙고 없음</span>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ═══════════════════════════
     PROBLEM PAGE
═══════════════════════════ -->
<div id="pg-problem">

  <div class="prob-meta-line">
    <span class="mn" id="p-num">문제 #1</span>
    <span style="color:#334155">·</span>
    <span>목표&nbsp;<span class="ml" id="p-tgt-L">?L</span></span>
    <span style="color:#334155">·</span>
    <span><span class="me" id="p-tgt-E">?E</span></span>
    <a class="gg-btn" id="gg-link" href="#" target="_blank" rel="noopener">
      🔗 GeoGebra에서 풀기
    </a>
  </div>

  <!-- Teacher: back button -->
  <div id="teacher-back">
    <button class="back-btn" onclick="showBingo()">← 빙고판으로 돌아가기</button>
  </div>

  <div class="prob-layout">

    <!-- LEFT: hint + tool table -->
    <div class="prob-left">
      <!-- Teacher hint -->
      <div class="sec-box" id="teacher-hint-box">
        <div class="sec-title">📋 진행 방법</div>
        <div style="font-size:0.8rem;color:#64748b;line-height:1.7;">
          Euclidea 앱에서 이 번호의 문제를 푸세요.<br>
          <span style="color:#38bdf8;font-weight:700">목표 L값</span> 달성 → L 조건,&nbsp;
          <span style="color:#c4b5fd;font-weight:700">목표 E값</span> 달성 → E 조건.<br>
          더 적은 수로 풀면 <span style="color:#fde68a;font-weight:700">V 조건</span> 보너스!<br>
          <span style="color:#475569;font-size:0.76rem;">마지막으로 조건을 달성한 조가 해당 칸을 소유합니다.</span>
        </div>
      </div>

      <div class="sec-box">
        <div class="sec-title">📐 도구별 L값 · E값</div>
        <table class="tool-tbl">
          <thead><tr><th>도구</th><th>L값</th><th>E값</th></tr></thead>
          <tbody>
            <tr><td>점</td><td><span class="bl">0L</span></td><td><span class="be">0E</span></td></tr>
            <tr><td>선</td><td><span class="bl">1L</span></td><td><span class="be">1E</span></td></tr>
            <tr><td>원</td><td><span class="bl">1L</span></td><td><span class="be">1E</span></td></tr>
            <tr><td>수직 이등분선</td><td><span class="bl">1L</span></td><td><span class="be">3E</span></td></tr>
            <tr><td>수선</td><td><span class="bl">1L</span></td><td><span class="be">3E</span></td></tr>
            <tr><td>각의 이등분선</td><td><span class="bl">1L</span></td><td><span class="be">4E</span></td></tr>
            <tr><td>평행선</td><td><span class="bl">1L</span></td><td><span class="be">4E</span></td></tr>
            <tr><td>교차</td><td><span class="bl">0L</span></td><td><span class="be">0E</span></td></tr>
          </tbody>
        </table>
      </div>

    </div>

    <!-- RIGHT: condition assignment (teacher only) or score info (student) -->
    <div class="prob-right">

      <!-- Teacher: condition assignment -->
      <div id="teacher-cond-box">
        <div class="sec-box">
          <div class="sec-title">✅ 조건 달성 기록</div>
          <p style="font-size:0.75rem;color:#475569;margin-bottom:12px;">
            각 조건을 달성한 조를 선택하세요.<br>마지막으로 선택한 조가 칸을 소유합니다.
          </p>
          <div class="cond-row">
            <span class="cond-lbl L">L 조건</span>
            <button class="cond-opt" id="cL-0" onclick="setCond('L',null)">미달성</button>
            <button class="cond-opt" id="cL-1" onclick="setCond('L',1)">1조</button>
            <button class="cond-opt" id="cL-2" onclick="setCond('L',2)">2조</button>
            <button class="cond-opt" id="cL-3" onclick="setCond('L',3)">3조</button>
            <button class="cond-opt" id="cL-4" onclick="setCond('L',4)">4조</button>
          </div>
          <div class="cond-row">
            <span class="cond-lbl E">E 조건</span>
            <button class="cond-opt" id="cE-0" onclick="setCond('E',null)">미달성</button>
            <button class="cond-opt" id="cE-1" onclick="setCond('E',1)">1조</button>
            <button class="cond-opt" id="cE-2" onclick="setCond('E',2)">2조</button>
            <button class="cond-opt" id="cE-3" onclick="setCond('E',3)">3조</button>
            <button class="cond-opt" id="cE-4" onclick="setCond('E',4)">4조</button>
          </div>
          <div class="cond-row">
            <span class="cond-lbl V">🌟 V 조건</span>
            <button class="cond-opt" id="cV-0" onclick="setCond('V',null)">미달성</button>
            <button class="cond-opt" id="cV-1" onclick="setCond('V',1)">1조</button>
            <button class="cond-opt" id="cV-2" onclick="setCond('V',2)">2조</button>
            <button class="cond-opt" id="cV-3" onclick="setCond('V',3)">3조</button>
            <button class="cond-opt" id="cV-4" onclick="setCond('V',4)">4조</button>
          </div>
          <div class="owner-box" id="owner-box">
            <span style="color:#334155">아직 달성된 조건이 없습니다.</span>
          </div>
        </div>
        <div class="sec-box">
          <div class="sec-title">📊 점수 기준</div>
          <div class="score-guide">
            <div><span style="color:#38bdf8">L·E·V 조건</span> 각 +10점</div>
            <div>빙고 1줄 완성 → +50점</div>
            <div style="margin-top:4px;color:#334155;font-size:0.7rem;">* L+E+V 모두 달성 시 영구 소유 🔒</div>
          </div>
        </div>
      </div>

      <!-- Student: condition status + current scores -->
      <div id="student-score-box" style="display:none;">
        <div class="sec-box">
          <div class="sec-title">✅ 조건 달성 현황</div>
          <div id="student-cond-status"></div>
        </div>
        <div class="sec-box">
          <div class="sec-title">📊 현재 점수</div>
          <div id="student-team-scores"></div>
        </div>
      </div>

    </div>
  </div>

  <!-- 커스텀 작도 캔버스 (injected) -->
  __GEO_HTML__

</div>

</div><!-- #app -->

<script>
'use strict';

// ═══════════════ CONFIG (injected by Python) ═══════════════
const IS_TEACHER  = __IS_TEACHER__;
const FB_URL      = '__FIREBASE_DB_URL__';
const FB_ENABLED  = FB_URL !== '' && FB_URL.startsWith('http');
const FB_PATH     = FB_URL.replace(/\/$/, '') + '/euclidea_bingo';
const GG_URLS     = __GEOGEBRA_CALC_URLS__;

// ═══════════════ DATA ═══════════════
const GRID = [
  [1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]
];
const PROBLEMS = {
  1:{L:4,E:8},  2:{L:3,E:5},  3:{L:2,E:4},  4:{L:3,E:3},  5:{L:5,E:7},
  6:{L:6,E:7},  7:{L:4,E:10}, 8:{L:3,E:6},  9:{L:2,E:5},  10:{L:6,E:11},
  11:{L:6,E:7}, 12:{L:2,E:6}, 13:{L:3,E:6}, 14:{L:3,E:3}, 15:{L:6,E:10},
  16:{L:3,E:5}, 17:{L:2,E:3}, 18:{L:5,E:6}, 19:{L:3,E:6}, 20:{L:3,E:5},
  21:{L:7,E:10},22:{L:3,E:5}, 23:{L:4,E:6}, 24:{L:3,E:3}, 25:{L:7,E:8},
};
const TEAMS = {
  1:{name:'1조',color:'#f87171',bg:'rgba(248,113,113,0.18)',border:'#f87171'},
  2:{name:'2조',color:'#38bdf8',bg:'rgba(56,189,248,0.18)',border:'#38bdf8'},
  3:{name:'3조',color:'#4ade80',bg:'rgba(74,222,128,0.18)',border:'#4ade80'},
  4:{name:'4조',color:'#c084fc',bg:'rgba(192,132,252,0.18)',border:'#c084fc'},
};

// ═══════════════ STATE ═══════════════
// probs[num] = { L:tid|null, E:tid|null, V:tid|null, owner:tid|null }
const LS_KEY = 'euclidea_bingo_v3';

function loadState() {
  if (!IS_TEACHER) return { probs:{} };  // students never use localStorage
  try {
    const s = JSON.parse(localStorage.getItem(LS_KEY));
    if (s && s.probs) return s;
  } catch(e) {}
  return { probs:{} };
}
function saveState() {
  if (IS_TEACHER) {
    localStorage.setItem(LS_KEY, JSON.stringify(state));
    if (FB_ENABLED) pushProbs();
  }
}

let state   = loadState();
let curProb = null;
let currentPage = 'bingo';

// ═══════════════ HELPERS ═══════════════
function getProb(num) {
  if (!state.probs[num]) state.probs[num] = {L:null,E:null,V:null,owner:null};
  return state.probs[num];
}
function getOwner(num) { return state.probs[num]?.owner ?? null; }
function isPerm(num) {
  const p = state.probs[num];
  return !!(p && p.L!==null && p.E!==null && p.V!==null);
}
function calcScore(tid) {
  let s = 0;
  Object.values(state.probs).forEach(p => {
    if(p.L===tid) s+=10; if(p.E===tid) s+=10; if(p.V===tid) s+=10;
  });
  getBingoLines().filter(l=>l.team===tid).forEach(()=>s+=50);
  return s;
}
function getBingoLines() {
  const lines=[];
  GRID.forEach((row,r)=>{
    const os=row.map(n=>getOwner(n));
    if(os[0]!==null&&os.every(o=>o===os[0])) lines.push({team:os[0],type:`${r+1}행`});
  });
  for(let c=0;c<5;c++){
    const os=GRID.map(row=>getOwner(row[c]));
    if(os[0]!==null&&os.every(o=>o===os[0])) lines.push({team:os[0],type:`${c+1}열`});
  }
  {const os=GRID.map((row,i)=>getOwner(row[i]));
   if(os[0]!==null&&os.every(o=>o===os[0])) lines.push({team:os[0],type:'↘대각선'});}
  {const os=GRID.map((row,i)=>getOwner(row[4-i]));
   if(os[0]!==null&&os.every(o=>o===os[0])) lines.push({team:os[0],type:'↗대각선'});}
  return lines;
}

// ═══════════════ BUILD GRID ═══════════════
function buildGrid() {
  const tbl = document.getElementById('bingo-tbl');
  tbl.innerHTML = '';
  GRID.forEach(row => {
    const tr = document.createElement('tr');
    row.forEach(num => {
      const td   = document.createElement('td');
      const p    = state.probs[num] || {L:null,E:null,V:null,owner:null};
      const ownr = getOwner(num);
      const perm = isPerm(num);
      const ot   = ownr ? TEAMS[ownr] : null;

      td.className = 'bingo-cell'
        + ((IS_TEACHER || _freeMode) ? ' teacher-only' : ' no-click')
        + (ownr?' owned':'') + (perm?' perm':'');

      if (ot) {
        td.style.background  = ot.bg;
        td.style.borderColor = ot.color;
        td.style.boxShadow   = perm
          ? `0 0 14px #fbbf2455,0 0 6px ${ot.color}44`
          : `0 0 8px ${ot.color}33`;
      }

      const dot = (letter) => {
        const team = p[letter];
        if (team !== null && team !== undefined && TEAMS[team]) {
          const t = TEAMS[team];
          return `<span class="cd on" style="background:${t.bg};color:${t.color};border-color:${t.border}">${letter}</span>`;
        }
        return `<span class="cd">${letter}</span>`;
      };

      td.innerHTML = `
        <div class="c-top">
          <span class="c-num">${num}</span>
          ${ot?`<span class="c-owner-tag" style="background:${ot.bg};color:${ot.color}">${ot.name}${perm?'🔒':''}</span>`:''}
        </div>
        <div class="c-mid"><span class="vL">${PROBLEMS[num].L}L</span><span class="vE">${PROBLEMS[num].E}E</span></div>
        <div class="c-conds">${dot('L')}${dot('E')}${dot('V')}</div>`;

      if (IS_TEACHER || _freeMode) td.onclick = () => showProblem(num, false);
      tr.appendChild(td);
    });
    tbl.appendChild(tr);
  });
}

function buildTeamCards() {
  const c = document.getElementById('team-cards');
  c.innerHTML = '';
  Object.entries(TEAMS).forEach(([id,t]) => {
    const tid  = parseInt(id);
    const score = calcScore(tid);
    const condCount = Object.values(state.probs).reduce((acc,p)=>{
      if(p.L===tid)acc++; if(p.E===tid)acc++; if(p.V===tid)acc++; return acc;
    },0);
    const ownedCells = Object.keys(state.probs).filter(n=>getOwner(parseInt(n))===tid).length;
    const bingoCount = getBingoLines().filter(l=>l.team===tid).length;
    const div=document.createElement('div');
    div.className='team-card';
    div.style.background=t.bg; div.style.borderColor=t.border;
    div.innerHTML=`
      <div class="tc-hd">
        <span class="tc-name" style="color:${t.color}">${t.name}</span>
        <div><span class="tc-score" style="color:${t.color}">${score}</span><span class="tc-score-lbl">점</span></div>
      </div>
      <div class="tc-det">조건 ${condCount}개 · 소유 ${ownedCells}칸${bingoCount>0?` · 🎊빙고 ${bingoCount}줄`:''}</div>`;
    c.appendChild(div);
  });
}

function updateBingoTags() {
  const lines=getBingoLines();
  const el=document.getElementById('bingo-tags');
  if(!lines.length){el.innerHTML='<span style="font-size:0.73rem;color:#334155">아직 빙고 없음</span>';return;}
  el.innerHTML=lines.map(l=>{
    const t=TEAMS[l.team];
    return `<span class="bingo-tag" style="background:${t.bg};color:${t.color};border:1px solid ${t.border}">🎊 ${t.name} ${l.type}</span>`;
  }).join('');
}

// ═══════════════ PAGES ═══════════════
function showBingo(pushNav=true) {
  currentPage = 'bingo';
  document.getElementById('pg-bingo').style.display   = 'block';
  document.getElementById('pg-problem').style.display = 'none';
  buildGrid(); buildTeamCards(); updateBingoTags();
  if (IS_TEACHER && FB_ENABLED && pushNav) fbPushNav(0);
}

function showProblem(num, pushNav=true) {
  currentPage = 'problem';
  curProb = num;
  document.getElementById('pg-bingo').style.display   = 'none';
  document.getElementById('pg-problem').style.display = 'block';

  const p = PROBLEMS[num];
  document.getElementById('p-num').textContent   = `문제 #${num}`;
  document.getElementById('p-tgt-L').textContent = `${p.L}L`;
  document.getElementById('p-tgt-E').textContent = `${p.E}E`;
  const ggLink = document.getElementById('gg-link');
  if (ggLink) ggLink.href = GG_URLS[num] || '#';

  if (IS_TEACHER) {
    refreshCondButtons();
    refreshOwnerBox();
  } else {
    updateStudentScores();
  }
  initCanvas(num);

  if (IS_TEACHER && FB_ENABLED && pushNav) fbPushNav(num);
  window.scrollTo(0, 0);
}


function updateStudentScores() {
  // Condition status for current problem
  const cs = document.getElementById('student-cond-status');
  if (cs && curProb) {
    const p = state.probs[curProb] || {L:null,E:null,V:null};
    const condInfo = [
      {k:'L', label:'L 조건', color:'#38bdf8'},
      {k:'E', label:'E 조건', color:'#c4b5fd'},
      {k:'V', label:'🌟 V 조건', color:'#fde68a'},
    ];
    cs.innerHTML = condInfo.map(({k,label,color})=>{
      const tid = p[k];
      const t   = tid ? TEAMS[tid] : null;
      return `<div style="display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid #1e3a5f;">
        <span style="font-weight:700;color:${color}">${label}</span>
        ${t
          ? `<span style="font-weight:800;color:${t.color}">${t.name} ✓</span>`
          : `<span style="color:#334155">미달성</span>`}
      </div>`;
    }).join('');
  }

  // Team scores
  const box = document.getElementById('student-team-scores');
  box.innerHTML = '';
  Object.entries(TEAMS).forEach(([id,t])=>{
    const tid=parseInt(id);
    const score=calcScore(tid);
    const div=document.createElement('div');
    div.style.cssText=`display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid #1e3a5f;`;
    div.innerHTML=`<span style="font-weight:700;color:${t.color}">${t.name}</span><span style="font-size:1.1rem;font-weight:900;color:${t.color}">${score}점</span>`;
    box.appendChild(div);
  });
}

// ═══════════════ CONDITION BUTTONS (teacher) ═══════════════
function refreshCondButtons() {
  const p = getProb(curProb);
  ['L','E','V'].forEach(cond => {
    const cur = p[cond];
    styleOpt(document.getElementById(`c${cond}-0`), cur===null, null);
    [1,2,3,4].forEach(tid => styleOpt(document.getElementById(`c${cond}-${tid}`), cur===tid, TEAMS[tid]));
  });
}
function styleOpt(btn, active, team) {
  if(!btn) return;
  if(active && team){
    btn.className='cond-opt sel';
    btn.style.cssText=`background:${team.bg};border-color:${team.border};color:${team.color};box-shadow:0 0 6px ${team.border}55`;
  } else if(active){
    btn.className='cond-opt sel';
    btn.style.cssText='background:#1e293b;border-color:#64748b;color:#94a3b8;';
  } else {
    btn.className='cond-opt'; btn.style.cssText='';
  }
}
function setCond(cond, teamId) {
  const p = getProb(curProb);
  p[cond] = teamId;
  if(teamId!==null) p.owner=teamId;
  else if(p.L===null&&p.E===null&&p.V===null) p.owner=null;
  saveState(); refreshCondButtons(); refreshOwnerBox();
}
function refreshOwnerBox() {
  const box=document.getElementById('owner-box');
  const p=state.probs[curProb];
  const ownr=getOwner(curProb);
  const perm=isPerm(curProb);
  if(!ownr){box.style.cssText='border-color:#334155;';box.innerHTML='<span style="color:#334155">아직 달성된 조건이 없습니다.</span>';return;}
  const ot=TEAMS[ownr];
  const parts=[];
  if(p&&p.L!==null) parts.push(`<span style="color:#38bdf8;font-weight:700">L:${TEAMS[p.L].name}</span>`);
  if(p&&p.E!==null) parts.push(`<span style="color:#c4b5fd;font-weight:700">E:${TEAMS[p.E].name}</span>`);
  if(p&&p.V!==null) parts.push(`<span style="color:#fde68a;font-weight:700">V:${TEAMS[p.V].name}</span>`);
  if(perm){
    box.style.cssText='border-color:#fbbf24;background:#1c1a08;';
    box.innerHTML=`<div>🔒 <span style="color:${ot.color};font-weight:900">${ot.name}</span> <span style="color:#fbbf24;font-weight:700">영구 소유</span></div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:6px">${parts.join('')}</div>`;
  } else {
    box.style.cssText=`border-color:${ot.border};background:${ot.bg};`;
    box.innerHTML=`<div><span style="color:${ot.color};font-weight:900">${ot.name}</span> <span style="color:#94a3b8;font-size:0.82rem">임시 소유</span></div>
      <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:6px">${parts.join('')}</div>`;
  }
}

// ═══════════════ RESET ═══════════════
function confirmReset(){document.getElementById('confirm-box').style.display='flex';}
function cancelReset(){document.getElementById('confirm-box').style.display='none';}
function doReset(){
  state={probs:{}};saveState();
  if(IS_TEACHER&&FB_ENABLED) fbPushAll();
  document.getElementById('confirm-box').style.display='none';
  showBingo();
}

// ═══════════════ FIREBASE SYNC ═══════════════
// Teacher → Firebase (REST API, no SDK needed)

// 수업 모드 ON/OFF 토글 (admin 전용)
let _classMode = true;  // true = 수업 모드, false = 자유 탐구

async function fbPushSync(enabled) {
  if (!FB_ENABLED || !IS_TEACHER) return;
  try {
    await fetch(`${FB_PATH}/sync.json`, {
      method: 'PUT', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(enabled)
    });
  } catch(e) { console.warn('FB sync push failed', e); }
}

function toggleSync() {
  _classMode = !_classMode;
  const btn = document.getElementById('sync-toggle-btn');
  if (_classMode) {
    btn.className = 'ctrl-btn class-on';
    btn.textContent = '🎓 수업 모드 ON';
  } else {
    btn.className = 'ctrl-btn class-off';
    btn.textContent = '🏠 자유 탐구 모드';
  }
  fbPushSync(_classMode);
}

async function fbPushNav(num) {
  if(!FB_ENABLED||!IS_TEACHER) return;
  try {
    await fetch(`${FB_PATH}/nav.json`,{
      method:'PUT', headers:{'Content-Type':'application/json'},
      body: JSON.stringify(num)  // null = bingo board, number = problem num
    });
  } catch(e){ console.warn('FB nav push failed',e); }
}
async function pushProbs() {
  if(!FB_ENABLED||!IS_TEACHER) return;
  try {
    await fetch(`${FB_PATH}/probs.json`,{
      method:'PUT', headers:{'Content-Type':'application/json'},
      body: JSON.stringify(state.probs)
    });
  } catch(e){ console.warn('FB probs push failed',e); }
}
async function fbPushAll() {
  if(!FB_ENABLED||!IS_TEACHER) return;
  try {
    await fetch(`${FB_PATH}.json`,{
      method:'PUT', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({nav:null, probs:{}})
    });
  } catch(e){}
}

// Student ← Firebase (Server-Sent Events — persistent connection, auto-reconnect)
let _lastNav  = -1;   // -1 = uninitialized, 0 = bingo, 1~25 = problem
let _fbStream = null;
let _freeMode = false; // true = 자유 탐구 모드 (학생이 독립적으로 탐구)

// ── 학생 UI: 수업모드 ↔ 자유탐구 모드 표시 전환 ──
function _updateStudentSyncUI(classMode) {
  const text = document.getElementById('role-text');
  const hint = document.getElementById('student-hint');
  const back = document.getElementById('teacher-back');
  if (classMode) {
    if (text) text.textContent = '학생 모드 — 교사 화면에 자동 연결됨';
    if (hint) hint.textContent = '📡 선생님이 문제를 선택하면 자동으로 이동합니다.';
    if (back) back.style.display = 'none';
  } else {
    if (text) text.textContent = '🏠 자유 탐구 모드 — 문제 칸을 눌러 자유롭게 탐구하세요';
    if (hint) hint.textContent = '🏠 자유 탐구 모드 — 문제 칸을 눌러 자유롭게 탐구하세요';
    if (back) back.style.display = 'block';
  }
}

// ── 공통: Firebase 데이터를 받아서 UI에 반영 ──
function _applyFbData(data) {
  if (!data) return;

  // sync 플래그 처리 (학생 전용)
  if (!IS_TEACHER && data.sync !== undefined) {
    const newFreeMode = (data.sync === false);
    if (newFreeMode !== _freeMode) {
      _freeMode = newFreeMode;
      _updateStudentSyncUI(!_freeMode);
      buildGrid(); // 클릭 가능 여부 갱신
    }
  }

  if (data.probs) {
    state.probs = data.probs;
    if (currentPage === 'bingo') {
      buildGrid(); buildTeamCards(); updateBingoTags();
    } else if (currentPage === 'problem') {
      updateStudentScores();
    }
  }

  // 자유 탐구 모드에서는 auto-navigate 안 함
  if (_freeMode) return;

  const nav = (data.nav === undefined) ? 0 : (data.nav ?? 0);
  if (nav !== _lastNav) {
    _lastNav = nav;
    if (nav === 0) {
      showBingo(false);
    } else if (typeof nav === 'number' && nav > 0) {
      showProblem(nav, false);
    }
  }
}

// ── 연결 상태 표시 ──
function _fbSetStatus(connected) {
  const dot  = document.getElementById('sync-dot');
  const text = document.getElementById('role-text');
  if (!dot || !text) return;
  if (connected) {
    dot.classList.add('on');
    dot.style.background = '';
    text.textContent = '학생 모드 — 교사 화면에 자동 연결됨';
  } else {
    dot.classList.remove('on');
    dot.style.background = '#ef4444';
    text.textContent = '학생 모드 — 연결 끊김 (자동 재연결 중...)';
  }
}

// ── SSE 스트리밍 시작 (타임아웃 없음, 브라우저가 자동 재연결) ──
function startFbStream() {
  if (!FB_ENABLED || IS_TEACHER) return;
  if (_fbStream) { _fbStream.close(); _fbStream = null; }

  _fbStream = new EventSource(`${FB_PATH}.json`);

  _fbStream.addEventListener('put', (e) => {
    try {
      const msg = JSON.parse(e.data);
      const path = msg.path, val = msg.data;
      if (path === '/') {
        _applyFbData(val);
      } else if (path === '/nav') {
        const nav = val ?? 0;
        if (nav !== _lastNav) {
          _lastNav = nav;
          if (nav === 0) showBingo(false);
          else if (typeof nav === 'number' && nav > 0) showProblem(nav, false);
        }
      } else if (path === '/probs') {
        state.probs = val || {};
        if (currentPage === 'bingo') { buildGrid(); buildTeamCards(); updateBingoTags(); }
        else if (currentPage === 'problem') { updateStudentScores(); }
      } else if (path === '/sync' && !IS_TEACHER) {
        const newFreeMode = (val === false);
        if (newFreeMode !== _freeMode) {
          _freeMode = newFreeMode;
          _updateStudentSyncUI(!_freeMode);
          buildGrid();
        }
      }
    } catch(err) { console.warn('FB SSE parse error', err); }
  });

  _fbStream.addEventListener('patch', (e) => {
    try {
      const msg = JSON.parse(e.data);
      if (msg.path === '/') _applyFbData(msg.data);
    } catch(err) {}
  });

  // Firebase가 인증 거부 시 'cancel' 이벤트 전송
  _fbStream.addEventListener('cancel', () => _fbSetStatus(false));

  _fbStream.onopen  = () => _fbSetStatus(true);
  _fbStream.onerror = () => _fbSetStatus(false);
  // EventSource는 끊기면 자동으로 재연결 — 수동 retry 불필요
}

// ═══════════════ ROLE-BASED UI INIT ═══════════════
function applyRole() {
  const banner   = document.getElementById('role-banner');
  const roleText = document.getElementById('role-text');
  const syncDot  = document.getElementById('sync-dot');

  if (IS_TEACHER) {
    banner.className = 'role-banner teacher';
    roleText.textContent = FB_ENABLED
      ? '교사 모드 — Firebase 실시간 동기화 활성화'
      : '교사 모드 — 오프라인 (Firebase 미설정)';
    if (FB_ENABLED) {
      syncDot.classList.add('on');
      // 현재 Firebase의 sync 상태를 읽어서 버튼 초기화
      fetch(`${FB_PATH}/sync.json`)
        .then(r => r.json())
        .then(val => {
          _classMode = (val !== false); // null/true → 수업 모드, false → 자유 탐구
          const btn = document.getElementById('sync-toggle-btn');
          if (btn) {
            btn.className = _classMode ? 'ctrl-btn class-on' : 'ctrl-btn class-off';
            btn.textContent = _classMode ? '🎓 수업 모드 ON' : '🏠 자유 탐구 모드';
          }
        })
        .catch(() => {});
    }

    // teacher-only UI
    document.getElementById('teacher-ctrl').style.display  = 'flex';
    document.getElementById('teacher-back').style.display  = 'block';
    document.getElementById('teacher-hint-box').style.display = 'block';
    document.getElementById('teacher-cond-box').style.display = 'block';
    document.getElementById('student-hint').style.display  = 'none';
    document.getElementById('student-score-box').style.display = 'none';

  } else {
    banner.className = 'role-banner student';
    roleText.textContent = FB_ENABLED
      ? '학생 모드 — 연결 중...'
      : '학생 모드 — 오프라인 (실시간 연결 없음)';
    // syncDot은 연결 성공(onopen) 시 _fbSetStatus(true)가 켜줌

    // student UI
    document.getElementById('teacher-ctrl').style.display  = 'none';
    document.getElementById('teacher-back').style.display  = 'none';
    document.getElementById('teacher-hint-box').style.display = 'none';
    document.getElementById('teacher-cond-box').style.display = 'none';
    document.getElementById('student-hint').style.display  = 'block';
    document.getElementById('student-score-box').style.display = 'block';

    // SSE 스트리밍 시작 (타임아웃 없음, 자동 재연결)
    if (FB_ENABLED) {
      startFbStream();
      // 탭이 숨겨졌다가 다시 보일 때 스트림이 닫혔으면 재시작
      document.addEventListener('visibilitychange', () => {
        if (!document.hidden && _fbStream &&
            _fbStream.readyState === EventSource.CLOSED) {
          startFbStream();
        }
      });
    }
  }
}

// ═══════════════ INIT ═══════════════
applyRole();
showBingo(false);  // don't push nav on initial load

// ═══════════════ GEOMETRY CANVAS (injected) ═══════════════
__GEO_JS__
</script>
</body>
</html>
"""


def render():
    import streamlit as st

    user_type = st.session_state.get("_user_type", "student")
    dev_mode  = st.session_state.get("_dev_mode", False)
    is_teacher = (user_type == "admin") or dev_mode

    _geo_js = _GEO_JS_TEMPLATE.replace(
        "__CANVAS_PROBLEMS__", _json.dumps(_CANVAS_PROBLEMS))

    html = (_TEMPLATE
        .replace("__IS_TEACHER__",    "true" if is_teacher else "false")
        .replace("__FIREBASE_DB_URL__", FIREBASE_DB_URL)
        .replace("__GEOGEBRA_CALC_URLS__", _json.dumps(GEOGEBRA_CALC_URLS))
        .replace("__GEOGEBRA_URLS__", _json.dumps(GEOGEBRA_URLS))
        .replace("__GEO_CSS__",  _GEO_CSS)
        .replace("__GEO_HTML__", _GEO_HTML)
        .replace("__GEO_JS__",   _geo_js))

    st.header("🎯 작도 게임(빙고)")
    if not is_teacher:
        st.caption("📡 선생님이 문제를 선택하면 자동으로 이동합니다.")
    else:
        st.caption("문제 칸 클릭 → 조건 기록 → 빙고판으로 돌아가기")

    components.html(html, height=2000, scrolling=True)
