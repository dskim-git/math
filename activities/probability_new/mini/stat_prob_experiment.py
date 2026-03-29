# activities/probability_new/mini/stat_prob_experiment.py
"""
통계적 확률 실험실 – 동전·주사위·카드
수학적 확률을 알고 있는 시행에서 실제로 실험을 반복하며
통계적 확률이 수학적 확률에 가까워지는 과정을 탐구합니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🎲 통계적 확률 실험실",
    "description": "동전·주사위·카드 시행을 반복하며 통계적 확률이 수학적 확률에 수렴하는 과정을 탐구합니다.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "통계적확률실험실"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 – 통계적 확률 실험실**"},
    {
        "key": "수학적확률비교",
        "label": "실험을 1000번 했을 때 얻은 통계적 확률과 수학적 확률을 비교하세요. 둘이 같았나요, 달랐나요? 왜 그렇다고 생각하나요?",
        "type": "text_area",
        "height": 120,
        "placeholder": "수학적 확률은 __이고, 실험에서 구한 통계적 확률은 __였다. 그 이유는..."
    },
    {
        "key": "수렴과정",
        "label": "그래프를 보면 상대도수가 어떻게 변화했나요? 횟수가 늘어날수록 어떤 경향이 나타났는지 설명하세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "초반에는 크게 흔들리다가..."
    },
    {
        "key": "대수의법칙",
        "label": "시행 횟수를 늘릴수록 통계적 확률이 수학적 확률에 가까워지는 현상을 '큰 수의 법칙'이라고 합니다. 이 활동에서 큰 수의 법칙을 확인했나요? 어떤 시행에서 가장 잘 나타났나요?",
        "type": "text_area",
        "height": 100,
        "placeholder": "가장 잘 나타난 시행: ...\n이유: ..."
    },
    {
        "key": "통계적확률의미",
        "label": "수학적 확률로도 구할 수 있는데 왜 통계적 확률을 사용하는 것이 의미 있을까요?",
        "type": "text_area",
        "height": 90,
        "placeholder": "통계적 확률은..."
    },
    {
        "key": "흥미로운시행",
        "label": "💡 세 가지 시행 중 가장 흥미로웠던 것과 그 이유를 써보세요.",
        "type": "text_area",
        "height": 80,
        "placeholder": "가장 흥미로운 시행: ...\n이유: ..."
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {"key": "느낀점", "label": "💬 느낀 점", "type": "text_area", "height": 90},
]

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>통계적 확률 실험실</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0d1117 0%,#161b22 50%,#0d1117 100%);
  color:#e2e8f0;
  padding:14px 12px 28px;
  min-height:100vh;
}

/* ── 헤더 ── */
.hdr{
  text-align:center;
  padding:18px 18px 14px;
  background:linear-gradient(135deg,rgba(16,185,129,.15),rgba(59,130,246,.15));
  border:1px solid rgba(16,185,129,.3);
  border-radius:16px;
  margin-bottom:16px;
}
.hdr h1{font-size:1.35rem;color:#34d399;margin-bottom:6px;}
.hdr p{font-size:.82rem;color:#94a3b8;line-height:1.65;}

/* ── 탭 ── */
.tabs{display:flex;gap:6px;margin-bottom:14px;flex-wrap:wrap;}
.tab{
  flex:1;min-width:90px;
  padding:10px 8px;
  border-radius:12px;
  border:2px solid rgba(255,255,255,.1);
  background:rgba(255,255,255,.04);
  cursor:pointer;
  text-align:center;
  font-size:.85rem;
  font-weight:600;
  transition:all .2s;
  color:#94a3b8;
}
.tab:hover{border-color:rgba(52,211,153,.4);color:#34d399;}
.tab.active{
  border-color:#34d399;
  background:rgba(52,211,153,.15);
  color:#34d399;
}
.tab .icon{font-size:1.4rem;display:block;margin-bottom:3px;}

/* ── 패널 ── */
.panel{display:none;animation:fadeIn .3s ease;}
.panel.active{display:block;}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}

/* ── 카드 ── */
.card{
  background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.1);
  border-radius:14px;
  padding:14px 14px 12px;
  margin-bottom:12px;
}
.card-title{font-size:.85rem;font-weight:700;color:#a3e635;margin-bottom:10px;}

/* ── 선택 UI ── */
.select-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;align-items:center;}
.select-row label{font-size:.8rem;color:#94a3b8;white-space:nowrap;}
select{
  flex:1;min-width:120px;
  background:#1e293b;border:1px solid rgba(255,255,255,.15);
  color:#e2e8f0;border-radius:8px;padding:6px 8px;font-size:.82rem;
}

/* ── 수학적 확률 배지 ── */
.math-prob{
  display:inline-flex;align-items:center;gap:6px;
  background:rgba(99,102,241,.2);border:1px solid rgba(99,102,241,.4);
  border-radius:8px;padding:6px 12px;font-size:.82rem;margin-bottom:10px;
}
.math-prob span{color:#818cf8;font-weight:700;}

/* ── 버튼 행 ── */
.btn-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;}
.btn{
  flex:1;min-width:80px;
  padding:9px 10px;border-radius:10px;border:none;cursor:pointer;
  font-weight:700;font-size:.82rem;transition:all .18s;
}
.btn-run{background:linear-gradient(135deg,#059669,#10b981);color:#fff;}
.btn-run:hover{filter:brightness(1.1);}
.btn-run:disabled{opacity:.45;cursor:not-allowed;}
.btn-reset{background:rgba(239,68,68,.15);border:1px solid rgba(239,68,68,.3);color:#fca5a5;}
.btn-reset:hover{background:rgba(239,68,68,.25);}
.btn-speed{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.15);color:#cbd5e1;font-size:.76rem;}
.btn-speed.active{background:rgba(251,191,36,.15);border-color:rgba(251,191,36,.4);color:#fbbf24;}

/* ── 결과 표시 ── */
.result-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px;}
.stat-box{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
  border-radius:10px;padding:10px;text-align:center;
}
.stat-box .val{font-size:1.4rem;font-weight:800;color:#34d399;}
.stat-box .lbl{font-size:.72rem;color:#64748b;margin-top:2px;}

/* ── 최신 결과 뱃지 ── */
.last-result{
  text-align:center;font-size:2.5rem;
  padding:8px 0 6px;
  min-height:60px;
  animation:pop .25s ease;
}
@keyframes pop{from{transform:scale(1.4)}to{transform:scale(1)}}

/* ── 표 ── */
.tbl-wrap{overflow-x:auto;margin-bottom:10px;}
table{width:100%;border-collapse:collapse;font-size:.75rem;min-width:500px;}
th{
  background:rgba(52,211,153,.12);color:#6ee7b7;
  padding:6px 4px;text-align:center;
  border-bottom:1px solid rgba(52,211,153,.2);white-space:nowrap;
}
td{padding:5px 4px;text-align:center;border-bottom:1px solid rgba(255,255,255,.05);}
td.success{color:#34d399;font-weight:700;}
td.ratio{color:#fbbf24;}
td.math{color:#818cf8;}

/* ── 캔버스 ── */
canvas{
  width:100%;height:220px;display:block;
  border-radius:10px;background:#0d1117;
  border:1px solid rgba(255,255,255,.08);
}

/* ── 개별 결과 목록 ── */
.log-wrap{
  max-height:120px;overflow-y:auto;
  display:flex;flex-wrap:wrap;gap:4px;
  scrollbar-width:thin;scrollbar-color:#334155 transparent;
}
.log-item{
  font-size:.75rem;padding:2px 7px;
  border-radius:20px;white-space:nowrap;
}
.log-hit{background:rgba(52,211,153,.15);color:#6ee7b7;border:1px solid rgba(52,211,153,.2);}
.log-miss{background:rgba(255,255,255,.04);color:#64748b;border:1px solid rgba(255,255,255,.07);}

/* ── 수렴 메시지 ── */
.converge-msg{
  text-align:center;padding:8px;font-size:.82rem;
  color:#fbbf24;background:rgba(251,191,36,.1);
  border:1px solid rgba(251,191,36,.25);border-radius:8px;
  margin-top:6px;display:none;
}
</style>
</head>
<body>

<div class="hdr">
  <h1>🔬 통계적 확률 실험실</h1>
  <p>시행을 반복하며 <strong>상대도수</strong>가 <strong>수학적 확률</strong>에 가까워지는 과정을 직접 확인해보세요!</p>
</div>

<!-- 탭 -->
<div class="tabs">
  <div class="tab active" onclick="switchTab('coin')"><span class="icon">🪙</span>동전</div>
  <div class="tab" onclick="switchTab('dice')"><span class="icon">🎲</span>주사위</div>
  <div class="tab" onclick="switchTab('card')"><span class="icon">🃏</span>카드</div>
</div>

<!-- ════════════════ 동전 패널 ════════════════ -->
<div id="panel-coin" class="panel active">
  <div class="card">
    <div class="card-title">🪙 동전 던지기</div>
    <div class="select-row">
      <label>관찰할 면:</label>
      <select id="coin-event" onchange="coinSetup()">
        <option value="head">앞면 (H)</option>
        <option value="tail">뒷면 (T)</option>
      </select>
    </div>
    <div class="math-prob" id="coin-math-prob">수학적 확률: <span>1/2 = 0.500</span></div>
    <div class="btn-row">
      <button class="btn btn-run" id="coin-btn1" onclick="runSim('coin',1)">1번</button>
      <button class="btn btn-run" id="coin-btn10" onclick="runSim('coin',10)">10번</button>
      <button class="btn btn-run" id="coin-btn100" onclick="runSim('coin',100)">100번</button>
      <button class="btn btn-run" id="coin-btnAuto" onclick="autoRun('coin')">▶ 자동</button>
      <button class="btn btn-reset" onclick="resetSim('coin')">초기화</button>
    </div>
    <div class="btn-row">
      <button class="btn btn-speed" id="coin-s1" onclick="setSpeed('coin',1)" >느리게</button>
      <button class="btn btn-speed active" id="coin-s2" onclick="setSpeed('coin',2)">보통</button>
      <button class="btn btn-speed" id="coin-s3" onclick="setSpeed('coin',3)">빠르게</button>
    </div>
    <div class="last-result" id="coin-last">－</div>
    <div class="result-grid">
      <div class="stat-box"><div class="val" id="coin-total">0</div><div class="lbl">전체 횟수</div></div>
      <div class="stat-box"><div class="val" id="coin-hit">0</div><div class="lbl">사건 발생 횟수</div></div>
      <div class="stat-box"><div class="val" id="coin-ratio">0.000</div><div class="lbl">상대도수 (통계적 확률)</div></div>
      <div class="stat-box"><div class="val" id="coin-diff" style="color:#fbbf24">—</div><div class="lbl">수학적 확률과의 차이</div></div>
    </div>
    <div class="converge-msg" id="coin-converge">📈 상대도수가 수학적 확률에 매우 가까워졌어요!</div>
  </div>
  <div class="card">
    <div class="card-title">📊 상대도수 변화 그래프</div>
    <canvas id="coin-canvas"></canvas>
  </div>
  <div class="card">
    <div class="card-title">📋 구간별 결과 표 (100번 단위)</div>
    <div class="tbl-wrap"><table id="coin-table">
      <thead><tr><th>던진 횟수</th><th>100</th><th>200</th><th>300</th><th>400</th><th>500</th><th>600</th><th>700</th><th>800</th><th>900</th><th>1000</th></tr></thead>
      <tbody>
        <tr><td>사건 발생 횟수</td><td id="ct-h-1">—</td><td id="ct-h-2">—</td><td id="ct-h-3">—</td><td id="ct-h-4">—</td><td id="ct-h-5">—</td><td id="ct-h-6">—</td><td id="ct-h-7">—</td><td id="ct-h-8">—</td><td id="ct-h-9">—</td><td id="ct-h-10">—</td></tr>
        <tr><td>상대도수</td><td id="ct-r-1" class="ratio">—</td><td id="ct-r-2" class="ratio">—</td><td id="ct-r-3" class="ratio">—</td><td id="ct-r-4" class="ratio">—</td><td id="ct-r-5" class="ratio">—</td><td id="ct-r-6" class="ratio">—</td><td id="ct-r-7" class="ratio">—</td><td id="ct-r-8" class="ratio">—</td><td id="ct-r-9" class="ratio">—</td><td id="ct-r-10" class="ratio">—</td></tr>
      </tbody>
    </table></div>
    <div style="font-size:.72rem;color:#475569;text-align:right;margin-top:4px;">상대도수는 소수 셋째 자리까지 표시</div>
  </div>
  <div class="card">
    <div class="card-title">📜 개별 결과 로그</div>
    <div class="log-wrap" id="coin-log"></div>
  </div>
</div>

<!-- ════════════════ 주사위 패널 ════════════════ -->
<div id="panel-dice" class="panel">
  <div class="card">
    <div class="card-title">🎲 주사위 던지기</div>
    <div class="select-row">
      <label>사건 선택:</label>
      <select id="dice-event" onchange="diceSetup()">
        <option value="1">눈이 1</option>
        <option value="2">눈이 2</option>
        <option value="3">눈이 3</option>
        <option value="4">눈이 4</option>
        <option value="5">눈이 5</option>
        <option value="6">눈이 6</option>
        <option value="even">짝수 눈 (2,4,6)</option>
        <option value="odd">홀수 눈 (1,3,5)</option>
        <option value="lte3">3 이하 (1,2,3)</option>
        <option value="gte4">4 이상 (4,5,6)</option>
      </select>
    </div>
    <div class="math-prob" id="dice-math-prob">수학적 확률: <span>1/6 ≈ 0.167</span></div>
    <div class="btn-row">
      <button class="btn btn-run" onclick="runSim('dice',1)">1번</button>
      <button class="btn btn-run" onclick="runSim('dice',10)">10번</button>
      <button class="btn btn-run" onclick="runSim('dice',100)">100번</button>
      <button class="btn btn-run" id="dice-btnAuto" onclick="autoRun('dice')">▶ 자동</button>
      <button class="btn btn-reset" onclick="resetSim('dice')">초기화</button>
    </div>
    <div class="btn-row">
      <button class="btn btn-speed" id="dice-s1" onclick="setSpeed('dice',1)">느리게</button>
      <button class="btn btn-speed active" id="dice-s2" onclick="setSpeed('dice',2)">보통</button>
      <button class="btn btn-speed" id="dice-s3" onclick="setSpeed('dice',3)">빠르게</button>
    </div>
    <div class="last-result" id="dice-last">－</div>
    <div class="result-grid">
      <div class="stat-box"><div class="val" id="dice-total">0</div><div class="lbl">전체 횟수</div></div>
      <div class="stat-box"><div class="val" id="dice-hit">0</div><div class="lbl">사건 발생 횟수</div></div>
      <div class="stat-box"><div class="val" id="dice-ratio">0.000</div><div class="lbl">상대도수 (통계적 확률)</div></div>
      <div class="stat-box"><div class="val" id="dice-diff" style="color:#fbbf24">—</div><div class="lbl">수학적 확률과의 차이</div></div>
    </div>
    <div class="converge-msg" id="dice-converge">📈 상대도수가 수학적 확률에 매우 가까워졌어요!</div>
  </div>
  <div class="card">
    <div class="card-title">📊 상대도수 변화 그래프</div>
    <canvas id="dice-canvas"></canvas>
  </div>
  <div class="card">
    <div class="card-title">📋 구간별 결과 표 (100번 단위)</div>
    <div class="tbl-wrap"><table id="dice-table">
      <thead><tr><th>던진 횟수</th><th>100</th><th>200</th><th>300</th><th>400</th><th>500</th><th>600</th><th>700</th><th>800</th><th>900</th><th>1000</th></tr></thead>
      <tbody>
        <tr><td>사건 발생 횟수</td><td id="dt-h-1">—</td><td id="dt-h-2">—</td><td id="dt-h-3">—</td><td id="dt-h-4">—</td><td id="dt-h-5">—</td><td id="dt-h-6">—</td><td id="dt-h-7">—</td><td id="dt-h-8">—</td><td id="dt-h-9">—</td><td id="dt-h-10">—</td></tr>
        <tr><td>상대도수</td><td id="dt-r-1" class="ratio">—</td><td id="dt-r-2" class="ratio">—</td><td id="dt-r-3" class="ratio">—</td><td id="dt-r-4" class="ratio">—</td><td id="dt-r-5" class="ratio">—</td><td id="dt-r-6" class="ratio">—</td><td id="dt-r-7" class="ratio">—</td><td id="dt-r-8" class="ratio">—</td><td id="dt-r-9" class="ratio">—</td><td id="dt-r-10" class="ratio">—</td></tr>
      </tbody>
    </table></div>
    <div style="font-size:.72rem;color:#475569;text-align:right;margin-top:4px;">상대도수는 소수 셋째 자리까지 표시</div>
  </div>
  <div class="card">
    <div class="card-title">📜 개별 결과 로그</div>
    <div class="log-wrap" id="dice-log"></div>
  </div>
</div>

<!-- ════════════════ 카드 패널 ════════════════ -->
<div id="panel-card" class="panel">
  <div class="card">
    <div class="card-title">🃏 트럼프 카드 한 장 뽑기 (52장, 복원추출)</div>
    <div class="select-row">
      <label>사건 선택:</label>
      <select id="card-event" onchange="cardSetup()">
        <option value="heart">하트 ♥ (13장)</option>
        <option value="spade">스페이드 ♠ (13장)</option>
        <option value="diamond">다이아 ♦ (13장)</option>
        <option value="club">클럽 ♣ (13장)</option>
        <option value="red">빨간 카드 ♥♦ (26장)</option>
        <option value="black">검은 카드 ♠♣ (26장)</option>
        <option value="ace">에이스 A (4장)</option>
        <option value="face">페이스 카드 J/Q/K (12장)</option>
      </select>
    </div>
    <div class="math-prob" id="card-math-prob">수학적 확률: <span>13/52 = 1/4 = 0.250</span></div>
    <div class="btn-row">
      <button class="btn btn-run" onclick="runSim('card',1)">1번</button>
      <button class="btn btn-run" onclick="runSim('card',10)">10번</button>
      <button class="btn btn-run" onclick="runSim('card',100)">100번</button>
      <button class="btn btn-run" id="card-btnAuto" onclick="autoRun('card')">▶ 자동</button>
      <button class="btn btn-reset" onclick="resetSim('card')">초기화</button>
    </div>
    <div class="btn-row">
      <button class="btn btn-speed" id="card-s1" onclick="setSpeed('card',1)">느리게</button>
      <button class="btn btn-speed active" id="card-s2" onclick="setSpeed('card',2)">보통</button>
      <button class="btn btn-speed" id="card-s3" onclick="setSpeed('card',3)">빠르게</button>
    </div>
    <div class="last-result" id="card-last">－</div>
    <div class="result-grid">
      <div class="stat-box"><div class="val" id="card-total">0</div><div class="lbl">전체 횟수</div></div>
      <div class="stat-box"><div class="val" id="card-hit">0</div><div class="lbl">사건 발생 횟수</div></div>
      <div class="stat-box"><div class="val" id="card-ratio">0.000</div><div class="lbl">상대도수 (통계적 확률)</div></div>
      <div class="stat-box"><div class="val" id="card-diff" style="color:#fbbf24">—</div><div class="lbl">수학적 확률과의 차이</div></div>
    </div>
    <div class="converge-msg" id="card-converge">📈 상대도수가 수학적 확률에 매우 가까워졌어요!</div>
  </div>
  <div class="card">
    <div class="card-title">📊 상대도수 변화 그래프</div>
    <canvas id="card-canvas"></canvas>
  </div>
  <div class="card">
    <div class="card-title">📋 구간별 결과 표 (100번 단위)</div>
    <div class="tbl-wrap"><table id="card-table">
      <thead><tr><th>뽑은 횟수</th><th>100</th><th>200</th><th>300</th><th>400</th><th>500</th><th>600</th><th>700</th><th>800</th><th>900</th><th>1000</th></tr></thead>
      <tbody>
        <tr><td>사건 발생 횟수</td><td id="cat-h-1">—</td><td id="cat-h-2">—</td><td id="cat-h-3">—</td><td id="cat-h-4">—</td><td id="cat-h-5">—</td><td id="cat-h-6">—</td><td id="cat-h-7">—</td><td id="cat-h-8">—</td><td id="cat-h-9">—</td><td id="cat-h-10">—</td></tr>
        <tr><td>상대도수</td><td id="cat-r-1" class="ratio">—</td><td id="cat-r-2" class="ratio">—</td><td id="cat-r-3" class="ratio">—</td><td id="cat-r-4" class="ratio">—</td><td id="cat-r-5" class="ratio">—</td><td id="cat-r-6" class="ratio">—</td><td id="cat-r-7" class="ratio">—</td><td id="cat-r-8" class="ratio">—</td><td id="cat-r-9" class="ratio">—</td><td id="cat-r-10" class="ratio">—</td></tr>
      </tbody>
    </table></div>
    <div style="font-size:.72rem;color:#475569;text-align:right;margin-top:4px;">상대도수는 소수 셋째 자리까지 표시</div>
  </div>
  <div class="card">
    <div class="card-title">📜 개별 결과 로그</div>
    <div class="log-wrap" id="card-log"></div>
  </div>
</div>

<script>
// ══════════════════════════════════════════════
//  상태
// ══════════════════════════════════════════════
const TABS = ['coin','dice','card'];
const state = {};
const speeds = {1:600, 2:180, 3:30};  // ms per tick in auto mode

TABS.forEach(t => {
  state[t] = {
    total: 0, hit: 0,
    history: [],     // 매 시행 상대도수
    snapshots: {},   // 100단위 스냅샷
    mathProb: 0.5,
    mathProbStr: '1/2 = 0.500',
    speed: 2,
    autoTimer: null,
    running: false,
    logItems: [],
  };
});

// ══════════════════════════════════════════════
//  설정 – 수학적 확률 계산
// ══════════════════════════════════════════════
function coinSetup(){
  const ev = document.getElementById('coin-event').value;
  const s = state.coin;
  s.mathProb = 0.5;
  s.mathProbStr = '1/2 = 0.500';
  document.getElementById('coin-math-prob').innerHTML =
    '수학적 확률: <span>' + s.mathProbStr + '</span>';
}

function diceSetup(){
  const ev = document.getElementById('dice-event').value;
  const s = state.dice;
  const map = {
    '1':'1/6 ≈ 0.167','2':'1/6 ≈ 0.167','3':'1/6 ≈ 0.167',
    '4':'1/6 ≈ 0.167','5':'1/6 ≈ 0.167','6':'1/6 ≈ 0.167',
    'even':'3/6 = 1/2 = 0.500','odd':'3/6 = 1/2 = 0.500',
    'lte3':'3/6 = 1/2 = 0.500','gte4':'3/6 = 1/2 = 0.500',
  };
  const prob = {'1':1/6,'2':1/6,'3':1/6,'4':1/6,'5':1/6,'6':1/6,
                'even':1/2,'odd':1/2,'lte3':1/2,'gte4':1/2};
  s.mathProb = prob[ev];
  s.mathProbStr = map[ev];
  document.getElementById('dice-math-prob').innerHTML =
    '수학적 확률: <span>' + s.mathProbStr + '</span>';
}

function cardSetup(){
  const ev = document.getElementById('card-event').value;
  const s = state.card;
  const map = {
    'heart':'13/52 = 1/4 = 0.250','spade':'13/52 = 1/4 = 0.250',
    'diamond':'13/52 = 1/4 = 0.250','club':'13/52 = 1/4 = 0.250',
    'red':'26/52 = 1/2 = 0.500','black':'26/52 = 1/2 = 0.500',
    'ace':'4/52 = 1/13 ≈ 0.077','face':'12/52 = 3/13 ≈ 0.231',
  };
  const prob = {
    'heart':13/52,'spade':13/52,'diamond':13/52,'club':13/52,
    'red':26/52,'black':26/52,'ace':4/52,'face':12/52,
  };
  s.mathProb = prob[ev];
  s.mathProbStr = map[ev];
  document.getElementById('card-math-prob').innerHTML =
    '수학적 확률: <span>' + s.mathProbStr + '</span>';
}

// ══════════════════════════════════════════════
//  시행 – 한 번 결과 생성
// ══════════════════════════════════════════════
function doOneTrial(tab){
  const s = state[tab];
  let result, isHit, label;

  if(tab === 'coin'){
    const ev = document.getElementById('coin-event').value;
    const r = Math.random() < 0.5 ? 'head' : 'tail';
    isHit = r === ev;
    result = r === 'head' ? '앞 🪙' : '뒤 🪙';
    label = r === 'head' ? '앞' : '뒤';
  } else if(tab === 'dice'){
    const ev = document.getElementById('dice-event').value;
    const r = Math.floor(Math.random()*6)+1;
    const faces = ['⚀','⚁','⚂','⚃','⚄','⚅'];
    result = faces[r-1] + ' ' + r;
    label = String(r);
    if(ev==='even') isHit = r%2===0;
    else if(ev==='odd') isHit = r%2===1;
    else if(ev==='lte3') isHit = r<=3;
    else if(ev==='gte4') isHit = r>=4;
    else isHit = String(r)===ev;
  } else {
    const ev = document.getElementById('card-event').value;
    const suits = ['♥','♦','♠','♣'];
    const vals  = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'];
    const si = Math.floor(Math.random()*4);
    const vi = Math.floor(Math.random()*13);
    const suit = suits[si]; const val = vals[vi];
    result = suit + val;
    label = result;
    if(ev==='heart') isHit = si===0;
    else if(ev==='diamond') isHit = si===1;
    else if(ev==='spade') isHit = si===2;
    else if(ev==='club') isHit = si===3;
    else if(ev==='red') isHit = si<=1;
    else if(ev==='black') isHit = si>=2;
    else if(ev==='ace') isHit = vi===0;
    else if(ev==='face') isHit = vi>=10;
  }

  s.total++;
  if(isHit) s.hit++;
  const ratio = s.hit / s.total;
  s.history.push(ratio);

  // 스냅샷 (100단위)
  if(s.total % 100 === 0 && s.total <= 1000){
    s.snapshots[s.total] = {hit: s.hit, ratio};
    updateTable(tab);
  }

  // 로그
  s.logItems.unshift({label, isHit});
  if(s.logItems.length > 200) s.logItems.pop();

  return {result, isHit, ratio};
}

// ══════════════════════════════════════════════
//  runSim – n번 실행
// ══════════════════════════════════════════════
function runSim(tab, n){
  const s = state[tab];
  if(s.running) return;
  for(let i=0;i<n;i++) doOneTrial(tab);
  updateUI(tab);
}

// ══════════════════════════════════════════════
//  autoRun – 1000번까지 자동
// ══════════════════════════════════════════════
function autoRun(tab){
  const s = state[tab];
  if(s.running){
    // 정지
    clearInterval(s.autoTimer);
    s.running = false;
    document.getElementById(tab+'-btnAuto').textContent = '▶ 자동';
    return;
  }
  s.running = true;
  document.getElementById(tab+'-btnAuto').textContent = '⏹ 정지';

  const ms = speeds[s.speed];
  const batchSize = s.speed === 3 ? 10 : 1;

  s.autoTimer = setInterval(()=>{
    if(s.total >= 1000){
      clearInterval(s.autoTimer);
      s.running = false;
      document.getElementById(tab+'-btnAuto').textContent = '▶ 자동';
      updateUI(tab);
      return;
    }
    for(let i=0;i<batchSize && s.total<1000;i++) doOneTrial(tab);
    updateUI(tab);
  }, ms);
}

// ══════════════════════════════════════════════
//  resetSim
// ══════════════════════════════════════════════
function resetSim(tab){
  const s = state[tab];
  if(s.autoTimer) clearInterval(s.autoTimer);
  s.total=0; s.hit=0; s.history=[]; s.snapshots={}; s.logItems=[]; s.running=false;
  document.getElementById(tab+'-btnAuto').textContent='▶ 자동';

  // 표 초기화
  const prefix = {coin:'ct',dice:'dt',card:'cat'}[tab];
  for(let i=1;i<=10;i++){
    document.getElementById(prefix+'-h-'+i).textContent='—';
    document.getElementById(prefix+'-r-'+i).textContent='—';
  }
  document.getElementById(tab+'-last').textContent='－';
  document.getElementById(tab+'-total').textContent='0';
  document.getElementById(tab+'-hit').textContent='0';
  document.getElementById(tab+'-ratio').textContent='0.000';
  document.getElementById(tab+'-diff').textContent='—';
  document.getElementById(tab+'-log').innerHTML='';
  document.getElementById(tab+'-converge').style.display='none';
  drawGraph(tab);
}

function setSpeed(tab, sp){
  state[tab].speed = sp;
  [1,2,3].forEach(i=>{
    const el = document.getElementById(tab+'-s'+i);
    el.classList.toggle('active', i===sp);
  });
  // 실행 중이면 재시작
  if(state[tab].running){
    clearInterval(state[tab].autoTimer);
    state[tab].running = false;
    document.getElementById(tab+'-btnAuto').textContent='▶ 자동';
    autoRun(tab);
  }
}

// ══════════════════════════════════════════════
//  updateUI
// ══════════════════════════════════════════════
function updateUI(tab){
  const s = state[tab];
  const ratio = s.total > 0 ? s.hit/s.total : 0;
  const diff  = s.total > 0 ? Math.abs(ratio - s.mathProb) : null;

  // 최신 결과 (마지막 로그 아이템)
  if(s.logItems.length>0){
    const it = s.logItems[0];
    const el = document.getElementById(tab+'-last');
    el.textContent = it.label + (it.isHit ? ' ✅' : ' ❌');
    el.style.color = it.isHit ? '#34d399' : '#f87171';
  }

  document.getElementById(tab+'-total').textContent = s.total;
  document.getElementById(tab+'-hit').textContent   = s.hit;
  document.getElementById(tab+'-ratio').textContent = ratio.toFixed(3);

  const diffEl = document.getElementById(tab+'-diff');
  if(diff !== null){
    diffEl.textContent = diff.toFixed(3);
    diffEl.style.color = diff < 0.02 ? '#34d399' : diff < 0.05 ? '#fbbf24' : '#f87171';
  }

  // 수렴 메시지
  const convEl = document.getElementById(tab+'-converge');
  convEl.style.display = (s.total >= 500 && diff !== null && diff < 0.02) ? 'block' : 'none';

  // 로그
  const logEl = document.getElementById(tab+'-log');
  logEl.innerHTML = s.logItems.slice(0,100).map(it=>{
    return `<span class="log-item ${it.isHit?'log-hit':'log-miss'}">${it.label}</span>`;
  }).join('');

  drawGraph(tab);
}

// ══════════════════════════════════════════════
//  표 업데이트
// ══════════════════════════════════════════════
function updateTable(tab){
  const s = state[tab];
  const prefix = {coin:'ct',dice:'dt',card:'cat'}[tab];
  const n = s.total;  // 스냅샷 시점
  const idx = n / 100;
  const snap = s.snapshots[n];
  if(!snap) return;
  document.getElementById(prefix+'-h-'+idx).textContent = snap.hit;
  const rEl = document.getElementById(prefix+'-r-'+idx);
  rEl.textContent = snap.ratio.toFixed(3);
}

// ══════════════════════════════════════════════
//  그래프 그리기
// ══════════════════════════════════════════════
function drawGraph(tab){
  const canvas = document.getElementById(tab+'-canvas');
  const ctx = canvas.getContext('2d');
  const W = canvas.offsetWidth || 400;
  const H = 220;
  canvas.width = W; canvas.height = H;

  const s = state[tab];
  const hist = s.history;
  const mp = s.mathProb;

  // 배경
  ctx.fillStyle = '#0d1117';
  ctx.fillRect(0,0,W,H);

  const pad = {l:42,r:16,t:14,b:32};
  const gW = W - pad.l - pad.r;
  const gH = H - pad.t - pad.b;

  // 그리드
  ctx.strokeStyle = 'rgba(255,255,255,.06)';
  ctx.lineWidth = 1;
  [0,.2,.4,.6,.8,1.0].forEach(v=>{
    const y = pad.t + gH*(1-v);
    ctx.beginPath(); ctx.moveTo(pad.l,y); ctx.lineTo(pad.l+gW,y); ctx.stroke();
    ctx.fillStyle='#475569'; ctx.font='10px sans-serif'; ctx.textAlign='right';
    ctx.fillText(v.toFixed(1), pad.l-4, y+3.5);
  });

  // X축 레이블
  ctx.fillStyle='#475569'; ctx.font='10px sans-serif'; ctx.textAlign='center';
  [200,400,600,800,1000].forEach(n=>{
    const x = pad.l + (n/1000)*gW;
    ctx.fillText(n, x, H-pad.b+14);
  });
  ctx.fillText('횟수', W/2, H-2);

  // 수학적 확률 기준선
  const mpY = pad.t + gH*(1-mp);
  ctx.strokeStyle='rgba(239,68,68,.7)';
  ctx.lineWidth=2;
  ctx.setLineDash([6,4]);
  ctx.beginPath(); ctx.moveTo(pad.l,mpY); ctx.lineTo(pad.l+gW,mpY); ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle='#f87171'; ctx.font='bold 10px sans-serif'; ctx.textAlign='left';
  ctx.fillText('p='+mp.toFixed(3), pad.l+4, mpY-4);

  if(hist.length < 2) return;

  // 상대도수 선
  ctx.strokeStyle='rgba(52,211,153,.9)';
  ctx.lineWidth=1.8;
  ctx.beginPath();
  hist.forEach((v,i)=>{
    const x = pad.l + ((i+1)/1000)*gW;
    const y = pad.t + gH*(1-v);
    i===0 ? ctx.moveTo(x,y) : ctx.lineTo(x,y);
  });
  ctx.stroke();

  // 현재 점
  if(hist.length>0){
    const lv = hist[hist.length-1];
    const lx = pad.l + (hist.length/1000)*gW;
    const ly = pad.t + gH*(1-lv);
    ctx.fillStyle='#34d399';
    ctx.beginPath(); ctx.arc(lx,ly,4,0,Math.PI*2); ctx.fill();
  }

  // 범례
  ctx.font='10px sans-serif';
  ctx.fillStyle='rgba(52,211,153,.9)'; ctx.fillRect(pad.l+8, pad.t+6, 14, 3);
  ctx.fillStyle='#94a3b8'; ctx.textAlign='left';
  ctx.fillText('상대도수', pad.l+26, pad.t+10);
  ctx.fillStyle='rgba(239,68,68,.7)'; ctx.fillRect(pad.l+90, pad.t+6, 14, 3);
  ctx.fillStyle='#94a3b8';
  ctx.fillText('수학적 확률', pad.l+108, pad.t+10);
}

// ══════════════════════════════════════════════
//  탭 전환
// ══════════════════════════════════════════════
function switchTab(tab){
  TABS.forEach(t=>{
    document.getElementById('panel-'+t).classList.toggle('active', t===tab);
  });
  document.querySelectorAll('.tab').forEach((el,i)=>{
    el.classList.toggle('active', TABS[i]===tab);
  });
  drawGraph(tab);
}

// ══════════════════════════════════════════════
//  초기화
// ══════════════════════════════════════════════
coinSetup(); diceSetup(); cardSetup();
TABS.forEach(t => drawGraph(t));
</script>
</body>
</html>
"""


def render():
    st.markdown("### 🔬 통계적 확률 실험실")
    st.markdown(
        "동전·주사위·카드 시행을 반복하며 **상대도수(통계적 확률)**가 "
        "**수학적 확률**에 가까워지는 과정을 직접 확인해 보세요."
    )

    components.html(_HTML, height=1400, scrolling=True)

    st.markdown("---")
    st.markdown(
        "#### 🌐 통그라미로 더 탐구하기",
    )
    st.markdown(
        "통계청에서 만든 **통그라미** 사이트에서 수학적 확률과 통계적 확률의 관계를 "
        "인터랙티브하게 추가 탐구할 수 있어요.",
    )
    st.link_button(
        "📊 통그라미 열기",
        "https://tong.kostat.go.kr/tongramy_web/main.do?menuSn=163#",
        use_container_width=True,
    )

    st.markdown("---")
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
