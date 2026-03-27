# activities/probability_new/mini/statistical_prob_sim.py
"""
통계적 확률 시뮬레이터 – 윷놀이·비·타율
수학적 확률로는 정의할 수 없는 세 사례를 직접 시뮬레이션하며
통계적 확률의 개념과 계산 방법을 탐구합니다.
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "🎯 통계적 확률 탐험대",
    "description": "윷놀이·기상예보·야구 타율로 통계적 확률을 직접 시뮬레이션하며 탐구합니다.",
    "order": 999999,
    "hidden": True,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "통계적확률탐험대"

_QUESTIONS = [
    {"type": "markdown", "text": "**📝 활동 성찰 – 통계적 확률 탐험대**"},
    {
        "key": "왜통계적확률",
        "label": "윷놀이·비가 올 확률·야구 타율을 수학적 확률로 정의할 수 없는 이유를 각각 설명하세요.",
        "type": "text_area",
        "height": 120,
        "placeholder": "윷놀이: ...\n비가 올 확률: ...\n야구 타율: ..."
    },
    {
        "key": "대수의법칙",
        "label": "실험 횟수를 늘릴수록 상대도수가 어떻게 변했나요? 이것이 통계적 확률과 어떤 관련이 있는지 설명하세요.",
        "type": "text_area",
        "height": 100,
        "placeholder": "예) 처음에는 크게 흔들리다가 횟수가 많아질수록..."
    },
    {
        "key": "통계적확률정의",
        "label": "이 활동을 통해 알게 된 통계적 확률의 정의를 자신의 말로 써보세요.",
        "type": "text_area",
        "height": 90,
        "placeholder": "통계적 확률이란..."
    },
    {
        "key": "실생활예시",
        "label": "💡 세 사례 외에, 일상에서 통계적 확률을 사용하는 예를 2가지 이상 써보세요.",
        "type": "text_area",
        "height": 80,
        "placeholder": "예1: ...\n예2: ..."
    },
    {"key": "새롭게알게된점", "label": "💡 새롭게 알게 된 점", "type": "text_area", "height": 90},
    {
        "key": "느낀점",
        "label": "💬 느낀 점",
        "type": "text_area",
        "height": 90
    },
]

_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>통계적 확률 탐험대</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Segoe UI',system-ui,sans-serif;
  background:linear-gradient(135deg,#0a0f1e 0%,#0f2027 50%,#0a1628 100%);
  color:#e2e8f0;
  padding:14px 12px 28px;
  min-height:100vh;
}

/* ── 헤더 ── */
.hdr{
  text-align:center;
  padding:16px 18px 14px;
  background:linear-gradient(135deg,rgba(6,182,212,.15),rgba(99,102,241,.15));
  border:1px solid rgba(6,182,212,.3);
  border-radius:16px;
  margin-bottom:16px;
}
.hdr h1{font-size:1.3rem;color:#22d3ee;margin-bottom:6px;}
.hdr p{font-size:.8rem;color:#94a3b8;line-height:1.65;}

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
  font-size:.82rem;
  font-weight:600;
  transition:all .2s;
  color:#94a3b8;
  user-select:none;
}
.tab:hover{background:rgba(255,255,255,.08);transform:translateY(-2px);}
.tab.active{border-color:var(--tc);background:rgba(var(--tr),.15);color:var(--tc);}
.tab .tab-icon{font-size:1.5rem;display:block;margin-bottom:4px;}

/* ── 패널 ── */
.panel{display:none;}
.panel.active{display:block;animation:fadeIn .3s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px);}to{opacity:1;transform:none;}}

/* ── 설명 카드 ── */
.explain{
  border-radius:14px;
  padding:13px 15px;
  margin-bottom:14px;
  font-size:.82rem;
  line-height:1.7;
  border-left:4px solid;
}
.ex-yut {background:rgba(234,179,8,.08); border-color:#eab308;color:#fef3c7;}
.ex-rain{background:rgba(6,182,212,.08); border-color:#06b6d4;color:#cffafe;}
.ex-bat {background:rgba(34,197,94,.08);  border-color:#22c55e;color:#dcfce7;}
.explain h3{font-size:.92rem;font-weight:700;margin-bottom:7px;}
.explain .badge{
  display:inline-block;
  background:rgba(255,255,255,.12);
  border-radius:20px;
  padding:2px 9px;
  font-size:.72rem;
  font-weight:700;
  margin-right:5px;
  margin-bottom:4px;
}
.badge-no {background:rgba(239,68,68,.2);color:#fca5a5;}
.badge-yes{background:rgba(34,197,94,.2);color:#86efac;}

/* ── 컨트롤 ── */
.ctrl{
  display:flex;flex-wrap:wrap;align-items:center;gap:10px;
  background:rgba(255,255,255,.04);
  border:1px solid rgba(255,255,255,.07);
  border-radius:12px;
  padding:10px 14px;
  margin-bottom:12px;
}
.ctrl label{font-size:.78rem;color:#94a3b8;white-space:nowrap;}
input[type=range]{width:110px;accent-color:var(--tc,#06b6d4);cursor:pointer;}
.n-val{font-weight:700;color:var(--tc,#06b6d4);min-width:50px;font-size:.88rem;}
.stat-badge{
  margin-left:auto;
  background:rgba(255,255,255,.07);
  border-radius:8px;
  padding:4px 10px;
  font-size:.76rem;color:#64748b;
}
.stat-badge span{color:var(--tc,#06b6d4);font-weight:700;}
.btn{
  padding:8px 18px;border-radius:10px;border:none;
  cursor:pointer;font-weight:700;font-size:.85rem;
  transition:all .15s;white-space:nowrap;
  color:#fff;
}
.btn:hover{filter:brightness(1.15);}
.btn:active{transform:scale(.97);}
.btn-go  {background:linear-gradient(135deg,var(--tc,#06b6d4),var(--tc2,#6366f1));}
.btn-rst {background:rgba(255,255,255,.07);color:#94a3b8;font-size:.75rem;padding:6px 12px;}
.btn:disabled{opacity:.4;cursor:not-allowed;pointer-events:none;}

/* ── 결과 박스 ── */
.result-box{
  background:rgba(0,0,0,.3);
  border:1px solid rgba(255,255,255,.07);
  border-radius:14px;
  min-height:110px;
  display:flex;align-items:center;justify-content:center;
  flex-direction:column;gap:6px;
  margin-bottom:12px;
  overflow:hidden;position:relative;
}
.res-prompt{font-size:.85rem;color:#475569;padding:0 20px;text-align:center;}
.res-big{font-size:2.8rem;font-weight:900;animation:pop .3s cubic-bezier(.25,1.5,.5,1);}
.res-sub{font-size:.8rem;color:#94a3b8;}
@keyframes pop{
  0%{transform:scale(.2);opacity:0;}
  70%{transform:scale(1.15);}
  100%{transform:scale(1);opacity:1;}
}

/* ── 윷 애니메이션 ── */
.yut-throw{
  display:none;
  gap:8px;
  font-size:2.2rem;
  animation:spin .15s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg);}}

/* ── 막대 통계 ── */
.stats{
  background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.06);
  border-radius:14px;
  padding:13px 14px;
  margin-bottom:12px;
  display:none;
}
.stats-hdr{
  display:flex;justify-content:space-between;align-items:center;
  margin-bottom:10px;
}
.stats-title{font-size:.86rem;font-weight:700;color:var(--tc,#06b6d4);}
.bar-row{margin-bottom:9px;}
.bar-lbl{
  display:flex;justify-content:space-between;
  font-size:.75rem;color:#94a3b8;margin-bottom:3px;
}
.bar-track{
  background:rgba(255,255,255,.06);
  border-radius:6px;height:22px;position:relative;overflow:hidden;
}
.bar-fill{
  height:100%;border-radius:6px;
  transition:width .4s ease;
  display:flex;align-items:center;justify-content:flex-end;
  padding-right:6px;
  font-size:.7rem;font-weight:700;color:rgba(255,255,255,.9);
}
.bar-ref{
  position:absolute;top:0;bottom:0;width:2px;
  background:rgba(255,255,255,.5);
  pointer-events:none;z-index:2;
}
.ref-tip{
  position:absolute;top:1px;left:3px;
  font-size:.6rem;color:rgba(255,255,255,.4);
  white-space:nowrap;
}
.note{font-size:.68rem;color:#334155;text-align:right;margin-top:5px;}

/* ── 수렴 차트 ── */
.conv-wrap{
  background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.06);
  border-radius:14px;
  padding:12px 14px;
  margin-bottom:12px;
  display:none;
}
.conv-title{font-size:.82rem;font-weight:700;color:var(--tc,#06b6d4);margin-bottom:8px;}
canvas.conv-chart{width:100%;height:130px;display:block;border-radius:8px;}

/* ── 인사이트 ── */
.insight{
  border-radius:12px;padding:11px 14px;
  font-size:.8rem;line-height:1.65;
  border-left:4px solid;
  display:none;margin-bottom:8px;
  animation:fadeIn .4s ease;
}
.ins-key {background:rgba(6,182,212,.1);  border-color:#06b6d4;color:#a5f3fc;}
.ins-info{background:rgba(99,102,241,.1); border-color:#6366f1;color:#c7d2fe;}
.ins-tip {background:rgba(234,179,8,.1);  border-color:#eab308;color:#fef08a;}
.ins-title{font-weight:700;margin-bottom:4px;font-size:.86rem;}

/* ── 수식 칩 ── */
.formula{
  background:rgba(0,0,0,.35);
  border:1px solid rgba(255,255,255,.1);
  border-radius:10px;
  padding:10px 14px;
  font-size:.82rem;
  text-align:center;
  margin-bottom:12px;
  color:#e2e8f0;
}
.formula em{font-style:normal;color:var(--tc,#06b6d4);font-weight:700;}

/* ── 야구 결과 이모지 ── */
.ball-result{font-size:2.5rem;}
</style>
</head>
<body>

<!-- 헤더 -->
<div class="hdr">
  <h1>🎯 통계적 확률 탐험대</h1>
  <p>수학적 확률로는 계산할 수 없는 세 가지 사례를 직접 실험하며<br>
  <strong style="color:#22d3ee">통계적 확률</strong>이 무엇인지, 어떻게 구하는지 탐구해봐요!</p>
</div>

<!-- 탭 -->
<div class="tabs">
  <div class="tab active" id="tab-yut"   onclick="switchTab('yut')"
       style="--tc:#eab308;--tr:234,179,8">
    <span class="tab-icon">🪵</span>윷놀이
  </div>
  <div class="tab"        id="tab-rain"  onclick="switchTab('rain')"
       style="--tc:#06b6d4;--tr:6,182,212">
    <span class="tab-icon">🌧️</span>기상예보
  </div>
  <div class="tab"        id="tab-bat"   onclick="switchTab('bat')"
       style="--tc:#22c55e;--tr:34,197,94">
    <span class="tab-icon">⚾</span>야구 타율
  </div>
</div>

<!-- ════════ 윷놀이 패널 ════════ -->
<div class="panel active" id="panel-yut" style="--tc:#eab308;--tc2:#f97316;--tr:234,179,8">

  <div class="explain ex-yut">
    <h3>🪵 왜 윷은 수학적 확률로 계산할 수 없을까?</h3>
    <span class="badge badge-no">수학적 확률 ✗</span>
    <span class="badge badge-yes">통계적 확률 ✓</span>
    <p>윷가락은 <strong>반원기둥</strong> 모양입니다.
    평평한 면(배)과 볼록한 면(도/앞)의 넓이가 달라서
    앞뒤가 나올 확률이 서로 <em>다릅니다</em>.<br>
    근원사건이 동일한 확률을 갖지 않으므로
    수학적 확률(<em>동일가능성</em>)이 성립하지 않습니다.<br>
    → 실제로 윷을 많이 던져 얻은 <strong>상대도수</strong>로만 확률을 추정할 수 있어요!</p>
  </div>

  <div class="formula">
    통계적 확률 ≈ <em>도·개·걸·윷·모가 나온 횟수</em> ÷ <em>전체 던진 횟수</em>
  </div>

  <div class="ctrl">
    <label>한 번에 던지기</label>
    <input type="range" id="yut-n" min="1" max="500" value="1"
           oninput="document.getElementById('yut-nv').textContent=this.value+'회';yutN=+this.value">
    <span class="n-val" id="yut-nv">1회</span>
    <div class="stat-badge">누적: <span id="yut-total">0</span>회</div>
    <button class="btn btn-go"  id="yut-btn"  onclick="throwYut()">🪵 던져라!</button>
    <button class="btn btn-rst" onclick="resetYut()">↺ 초기화</button>
  </div>

  <div class="result-box" id="yut-res-box">
    <div class="res-prompt" id="yut-prompt">버튼을 눌러 윷을 던져보세요!</div>
    <div class="yut-throw" id="yut-anim">🪵🪵🪵🪵</div>
    <div class="res-big"   id="yut-big"   style="display:none;color:#eab308"></div>
    <div class="res-sub"   id="yut-sub"   style="display:none"></div>
  </div>

  <div class="stats" id="yut-stats">
    <div class="stats-hdr">
      <span class="stats-title">📊 누적 통계</span>
      <span style="font-size:.74rem;color:#64748b" id="yut-sc"></span>
    </div>
    <div id="yut-bars"></div>
  </div>

  <div class="conv-wrap" id="yut-conv">
    <div class="conv-title">📈 앞면(배) 상대도수의 수렴 과정</div>
    <canvas class="conv-chart" id="yut-canvas"></canvas>
    <div style="font-size:.7rem;color:#64748b;margin-top:5px">
      가로: 시행 횟수 &nbsp;|&nbsp; 세로: 윷가락 1개의 앞면 비율 (앞면 총수 ÷ 던진 막대 수) &nbsp;|&nbsp;
      <span style="color:rgba(255,255,255,.5)">━</span> 기준 60%
    </div>
  </div>

  <div class="insight ins-key" id="yut-insight" style="display:none">
    <div class="ins-title">💡 발견!</div>
    <div id="yut-ins-body"></div>
  </div>
</div>

<!-- ════════ 기상예보 패널 ════════ -->
<div class="panel" id="panel-rain" style="--tc:#06b6d4;--tc2:#6366f1;--tr:6,182,212">

  <div class="explain ex-rain">
    <h3>🌧️ 비가 올 확률을 왜 통계적 확률로 구할까?</h3>
    <span class="badge badge-no">수학적 확률 ✗</span>
    <span class="badge badge-yes">통계적 확률 ✓</span>
    <p>비가 오는 날씨는 기온·습도·기압 등 수많은 요인이 복합적으로 작용합니다.
    표본공간의 모든 근원사건(날씨 패턴)이 동일한 확률을 가진다고 볼 수 없어요.<br>
    → 기상청은 <strong>"오늘과 비슷한 기상 조건이 과거에 100번 있었을 때, 그 중 몇 번이나 비가 왔나?"</strong>를
    세어서 강수 확률을 계산합니다. 이것이 바로 통계적 확률!<br>
    <em>아래 시뮬레이션</em>에서 계절별 강수확률을 골라 직접 실험해보세요.</p>
  </div>

  <div class="formula">
    강수 확률(%) ≈ <em>비가 온 날의 수</em> ÷ <em>비슷한 기상조건의 날 수</em> × 100
  </div>

  <!-- 계절 선택 -->
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">
    <button class="btn btn-rst" id="rs-spring" onclick="setRain(40,'봄','🌸')"
            style="font-size:.8rem;padding:7px 13px">🌸 봄 (40%)</button>
    <button class="btn btn-rst" id="rs-summer" onclick="setRain(70,'여름','☀️')"
            style="font-size:.8rem;padding:7px 13px">☀️ 여름 (70%)</button>
    <button class="btn btn-rst" id="rs-autumn" onclick="setRain(25,'가을','🍂')"
            style="font-size:.8rem;padding:7px 13px">🍂 가을 (25%)</button>
    <button class="btn btn-rst" id="rs-winter" onclick="setRain(10,'겨울','❄️')"
            style="font-size:.8rem;padding:7px 13px">❄️ 겨울 (10%)</button>
  </div>

  <div class="ctrl">
    <label>하루씩 / 여러 날</label>
    <input type="range" id="rain-n" min="1" max="365" value="1"
           oninput="document.getElementById('rain-nv').textContent=this.value+'일';rainN=+this.value">
    <span class="n-val" id="rain-nv">1일</span>
    <div class="stat-badge">누적: <span id="rain-total">0</span>일</div>
    <button class="btn btn-go"  id="rain-btn"  onclick="doRain()" disabled>🌦️ 날씨 확인!</button>
    <button class="btn btn-rst" onclick="resetRain()">↺ 초기화</button>
  </div>

  <div class="result-box" id="rain-res-box">
    <div class="res-prompt" id="rain-prompt">먼저 계절을 선택하세요!</div>
    <div class="res-big" id="rain-big" style="display:none;color:#06b6d4"></div>
    <div class="res-sub" id="rain-sub" style="display:none"></div>
  </div>

  <div class="stats" id="rain-stats">
    <div class="stats-hdr">
      <span class="stats-title">📊 강수 통계</span>
      <span style="font-size:.74rem;color:#64748b" id="rain-sc"></span>
    </div>
    <div id="rain-bars"></div>
  </div>

  <div class="conv-wrap" id="rain-conv">
    <div class="conv-title">📈 강수 상대도수의 수렴 과정</div>
    <canvas class="conv-chart" id="rain-canvas"></canvas>
    <div style="font-size:.7rem;color:#64748b;margin-top:5px">
      가로: 날 수 &nbsp;|&nbsp; 세로: 강수 상대도수 &nbsp;|&nbsp;
      <span id="rain-ref-label" style="color:#06b6d4">━ 설정 확률</span>
    </div>
  </div>

  <div class="insight ins-info" id="rain-insight" style="display:none">
    <div class="ins-title">🌦️ 기상청의 예보 방식</div>
    <div id="rain-ins-body"></div>
  </div>
</div>

<!-- ════════ 야구 타율 패널 ════════ -->
<div class="panel" id="panel-bat" style="--tc:#22c55e;--tc2:#10b981;--tr:34,197,94">

  <div class="explain ex-bat">
    <h3>⚾ 야구 타율을 왜 수학적 확률로 구할 수 없을까?</h3>
    <span class="badge badge-no">수학적 확률 ✗</span>
    <span class="badge badge-yes">통계적 확률 ✓</span>
    <p>타자가 안타를 칠 확률은 투수의 구질, 컨디션, 구장 환경, 타자의 기술 등
    무한히 많은 변수에 의해 결정됩니다. 모든 타석이 동일한 조건이 아니므로
    <em>동일가능성</em>을 적용할 수 없어요.<br>
    → 대신 <strong>실제 타석 수와 안타 수</strong>를 세어 타율 = 안타/타수로 계산합니다.
    이것이 통계적 확률입니다!<br>
    아래에서 선수를 골라 타석에 들어서 보세요.</p>
  </div>

  <div class="formula">
    타율(통계적 확률) = <em>안타 수</em> ÷ <em>타수(타석 수)</em>
  </div>

  <!-- 선수 선택 -->
  <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px">
    <button class="btn btn-rst" onclick="setPlayer('이정후',0.349,'🦅')"
            style="font-size:.8rem;padding:7px 13px">🦅 이정후 (타율 .349)</button>
    <button class="btn btn-rst" onclick="setPlayer('류현진',0.180,'🎯')"
            style="font-size:.8rem;padding:7px 13px">🎯 투수 타자 (타율 .180)</button>
    <button class="btn btn-rst" onclick="setPlayer('슬럼프',0.200,'😰')"
            style="font-size:.8rem;padding:7px 13px">😰 슬럼프 타자 (타율 .200)</button>
    <button class="btn btn-rst" onclick="setPlayer('평균 선수',0.280,'⚾')"
            style="font-size:.8rem;padding:7px 13px">⚾ 평균 선수 (타율 .280)</button>
  </div>

  <div class="ctrl">
    <label>타석 수</label>
    <input type="range" id="bat-n" min="1" max="200" value="1"
           oninput="document.getElementById('bat-nv').textContent=this.value+'타석';batN=+this.value">
    <span class="n-val" id="bat-nv">1타석</span>
    <div class="stat-badge">누적: <span id="bat-total">0</span>타석</div>
    <button class="btn btn-go"  id="bat-btn"  onclick="doBat()" disabled>⚾ 타석!</button>
    <button class="btn btn-rst" onclick="resetBat()">↺ 초기화</button>
  </div>

  <div class="result-box" id="bat-res-box">
    <div class="res-prompt" id="bat-prompt">먼저 선수를 선택하세요!</div>
    <div class="res-big ball-result" id="bat-big" style="display:none"></div>
    <div class="res-sub" id="bat-sub" style="display:none"></div>
  </div>

  <div class="stats" id="bat-stats">
    <div class="stats-hdr">
      <span class="stats-title">📊 타격 통계</span>
      <span style="font-size:.74rem;color:#64748b" id="bat-sc"></span>
    </div>
    <div id="bat-bars"></div>
  </div>

  <div class="conv-wrap" id="bat-conv">
    <div class="conv-title">📈 타율(상대도수)의 수렴 과정</div>
    <canvas class="conv-chart" id="bat-canvas"></canvas>
    <div style="font-size:.7rem;color:#64748b;margin-top:5px">
      가로: 타석 수 &nbsp;|&nbsp; 세로: 타율 &nbsp;|&nbsp;
      <span id="bat-ref-label" style="color:#22c55e">━ 실제 타율</span>
    </div>
  </div>

  <div class="insight ins-tip" id="bat-insight" style="display:none">
    <div class="ins-title">⚾ 통계적 확률의 의미</div>
    <div id="bat-ins-body"></div>
  </div>
</div>

<script>
/* ═══════════════════════════════════════
   공통 유틸
═══════════════════════════════════════ */
function $(id){ return document.getElementById(id); }
function show(id){ $(id).style.display='block'; }
function hide(id){ $(id).style.display='none'; }

function switchTab(t){
  ['yut','rain','bat'].forEach(x=>{
    $('tab-'+x).classList.toggle('active',x===t);
    $('panel-'+x).classList.toggle('active',x===t);
  });
}

// 가중 랜덤
function pick(faces,probs){
  const r=Math.random(); let c=0;
  for(let i=0;i<probs.length;i++){ c+=probs[i]; if(r<c)return faces[i]; }
  return faces[faces.length-1];
}

// 막대 그래프 렌더
function renderBars(containerId, faces, counts, total, colors, refProbs, tc){
  const c=$(containerId);
  let html='';
  faces.forEach((f,i)=>{
    const cnt=counts[f]||0;
    const pct=total>0?cnt/total*100:0;
    const ref=refProbs?refProbs[i]*100:null;
    const col=colors[i]||tc||'#06b6d4';
    html+=`<div class="bar-row">
      <div class="bar-lbl">
        <span style="color:${col}">${f}</span>
        <span>${cnt}회 (${pct.toFixed(1)}%)</span>
      </div>
      <div class="bar-track">
        <div class="bar-fill" style="width:${Math.min(pct,100).toFixed(1)}%;background:${col}">
          ${pct>9?pct.toFixed(1)+'%':''}
        </div>
        ${ref!==null?`<div class="bar-ref" style="left:${Math.min(ref,100).toFixed(1)}%"><span class="ref-tip">기준</span></div>`:''}
      </div>
    </div>`;
  });
  if(refProbs) html+=`<div class="note">흰 선 = 기준(이론/설정) 확률</div>`;
  c.innerHTML=html;
}

// 꺾은선 차트
function drawChart(canvasId, data, refVal, tc, label){
  const cvs=$(canvasId);
  if(!cvs) return;
  const W=cvs.offsetWidth||320, H=130;
  cvs.width=W; cvs.height=H;
  const ctx=cvs.getContext('2d');
  ctx.clearRect(0,0,W,H);

  // 배경
  ctx.fillStyle='rgba(0,0,0,.25)';
  ctx.roundRect(0,0,W,H,8);
  ctx.fill();

  const pad={t:10,b:22,l:36,r:10};
  const iW=W-pad.l-pad.r, iH=H-pad.t-pad.b;

  // 기준선
  if(refVal!==null){
    const ry=pad.t+iH*(1-refVal);
    ctx.strokeStyle='rgba(255,255,255,.35)';
    ctx.setLineDash([4,4]);
    ctx.lineWidth=1.5;
    ctx.beginPath(); ctx.moveTo(pad.l,ry); ctx.lineTo(W-pad.r,ry); ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle='rgba(255,255,255,.45)';
    ctx.font='9px sans-serif';
    ctx.fillText((refVal*100).toFixed(0)+'%',2,ry+3);
  }

  if(data.length<2){ return; }

  // 그리드
  [0.25,0.5,0.75].forEach(v=>{
    const gy=pad.t+iH*(1-v);
    ctx.strokeStyle='rgba(255,255,255,.06)';
    ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(pad.l,gy); ctx.lineTo(W-pad.r,gy); ctx.stroke();
    ctx.fillStyle='rgba(255,255,255,.25)';
    ctx.font='9px sans-serif';
    ctx.fillText((v*100).toFixed(0)+'%',2,gy+3);
  });

  // 데이터 라인
  ctx.strokeStyle=tc||'#06b6d4';
  ctx.lineWidth=2;
  ctx.shadowColor=tc||'#06b6d4';
  ctx.shadowBlur=4;
  ctx.beginPath();
  data.forEach((v,i)=>{
    const x=pad.l+i/(data.length-1)*iW;
    const y=pad.t+iH*(1-Math.min(v,1));
    i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
  });
  ctx.stroke();
  ctx.shadowBlur=0;

  // 마지막 값 표시
  const last=data[data.length-1];
  const lx=W-pad.r, ly=pad.t+iH*(1-Math.min(last,1));
  ctx.beginPath();
  ctx.arc(lx,ly,4,0,Math.PI*2);
  ctx.fillStyle=tc||'#06b6d4';
  ctx.fill();
  ctx.fillStyle='white';
  ctx.font='bold 9px sans-serif';
  ctx.fillText((last*100).toFixed(1)+'%',lx-18,ly-6);
}

/* ═══════════════════════════════════════
   윷놀이
   실제 윷가락: 배(평평)=앞, 도/뒤=볼록
   실험 데이터 기반: 앞(배) ≈ 60%, 뒤(볼록) ≈ 40%
   → 도:1앞, 개:2앞, 걸:3앞, 윷:4앞, 모:4뒤
═══════════════════════════════════════ */
const YUT_OUTCOMES=['도','개','걸','윷','모'];
// 앞(배)=0.6, 뒤=0.4로 4개 독립 시행
function rollYutOnce(){
  let front=0;
  for(let i=0;i<4;i++) if(Math.random()<0.60) front++;
  const outcome=front===0?'모':front===1?'도':front===2?'개':front===3?'걸':'윷';
  return {outcome, front};
}
// 이론 분포 (p=0.6 이항)
const YUT_REF=[
  4*Math.pow(0.4,3)*0.6,        // 도: C(4,1)*0.6^1*0.4^3
  6*Math.pow(0.6,2)*Math.pow(0.4,2), // 개
  4*Math.pow(0.6,3)*0.4,        // 걸
  Math.pow(0.6,4),               // 윷
  Math.pow(0.4,4),               // 모
];
const YUT_EMOJIS=['🐕','🐶','🐈','🌙','⭕'];
const YUT_COLORS=['#fb923c','#fbbf24','#a3e635','#34d399','#60a5fa'];

let yutCounts={},yutTotal=0,yutFrontTotal=0,yutN=1,yutHistory=[],yutRolling=false;
YUT_OUTCOMES.forEach(o=>yutCounts[o]=0);

function throwYut(){
  if(yutRolling)return;
  yutRolling=true;
  $('yut-btn').disabled=true;
  hide('yut-prompt'); hide('yut-big'); hide('yut-sub');

  if(yutN<=5){
    // 애니메이션
    const a=$('yut-anim'); a.style.display='flex';
    setTimeout(()=>{
      a.style.display='none';
      let last='';
      for(let i=0;i<yutN;i++){
        const r=rollYutOnce(); last=r.outcome;
        yutCounts[last]++; yutFrontTotal+=r.front;
      }
      yutTotal+=yutN;

      const idx=YUT_OUTCOMES.indexOf(last);
      $('yut-big').textContent=YUT_EMOJIS[idx]+' '+last;
      $('yut-big').style.color=YUT_COLORS[idx];
      $('yut-big').style.display='block';
      $('yut-sub').textContent=yutN===1?`"${last}"(이)가 나왔습니다`:`${yutN}번 던졌습니다 (마지막: ${last})`;
      $('yut-sub').style.display='block';
      $('yut-total').textContent=yutTotal;
      updateYutStats(); yutRolling=false; $('yut-btn').disabled=false;
    },480);
  } else {
    hide('yut-anim');
    let last='';
    for(let i=0;i<yutN;i++){
      const r=rollYutOnce(); last=r.outcome;
      yutCounts[last]++; yutFrontTotal+=r.front;
    }
    yutTotal+=yutN;
    $('yut-big').textContent=`+${yutN}번!`;
    $('yut-big').style.color='#eab308';
    $('yut-big').style.display='block';
    $('yut-sub').textContent=`총 ${yutTotal}번 던졌습니다`;
    $('yut-sub').style.display='block';
    $('yut-total').textContent=yutTotal;
    updateYutStats(); yutRolling=false; $('yut-btn').disabled=false;
  }
}

function updateYutStats(){
  show('yut-stats');
  $('yut-sc').textContent=`총 ${yutTotal}번`;
  renderBars('yut-bars',YUT_OUTCOMES,yutCounts,yutTotal,YUT_COLORS,YUT_REF,'#eab308');

  // 수렴 차트: 개별 윷가락 앞면(배) 비율 = 앞면 총 개수 / (던진 횟수 × 4)
  const frontRate=yutFrontTotal/(yutTotal*4);
  yutHistory.push(frontRate);
  // 최대 200포인트
  const hist=yutHistory.length>200?yutHistory.filter((_,i)=>i%Math.ceil(yutHistory.length/200)===0):yutHistory;
  show('yut-conv');
  drawChart('yut-canvas',hist,0.60,'#eab308','앞면 상대도수');

  if(yutTotal>=50){
    $('yut-ins-body').innerHTML=
      `윷가락 1개의 앞면(배) 비율: <strong>${(frontRate*100).toFixed(1)}%</strong><br>` +
      `(총 ${yutTotal*4}개 던진 윷가락 중 앞면이 ${yutFrontTotal}개)<br>` +
      `던지는 횟수가 늘수록 이 값이 <strong>약 60%</strong>에 가까워집니다.<br>` +
      `이처럼 <em>시행 횟수를 늘릴수록 상대도수가 일정 값으로 수렴하는 성질</em>을 <strong>대수의 법칙</strong>이라 하며,<br>` +
      `이 수렴 값이 바로 <strong>통계적 확률</strong>입니다!`;
    show('yut-insight');
  }
}

function resetYut(){
  YUT_OUTCOMES.forEach(o=>yutCounts[o]=0);
  yutTotal=0; yutFrontTotal=0; yutHistory=[];
  $('yut-total').textContent='0';
  hide('yut-stats'); hide('yut-conv'); hide('yut-insight');
  hide('yut-big'); hide('yut-sub'); hide('yut-anim');
  show('yut-prompt');
}

/* ═══════════════════════════════════════
   기상예보
═══════════════════════════════════════ */
let rainProb=0.4, rainSeason='봄', rainIcon='🌸';
let rainCounts={'비':0,'맑음/흐림':0},rainTotal=0,rainN=1,rainHistory=[];
let rainActive=false;

function setRain(prob,season,icon){
  rainProb=prob/100; rainSeason=season; rainIcon=icon;
  resetRain();
  $('rain-btn').disabled=false;
  $('rain-prompt').textContent=`${icon} ${season} 강수확률 ${prob}%로 설정됨. 날씨를 확인해보세요!`;
  show('rain-prompt');
  $('rain-ref-label').innerHTML=`<span style="color:#06b6d4">━ 설정 강수확률 ${prob}%</span>`;
}

function doRain(){
  if(!rainActive && rainTotal===0) rainActive=true;
  hide('rain-prompt'); hide('rain-big'); hide('rain-sub');
  let lastRain=false;
  for(let i=0;i<rainN;i++){
    const r=Math.random()<rainProb;
    rainCounts[r?'비':'맑음/흐림']++;
    lastRain=r;
  }
  rainTotal+=rainN;

  if(rainN<=10){
    $('rain-big').textContent=lastRain?'🌧️':'☀️';
    $('rain-big').style.color=lastRain?'#60a5fa':'#fbbf24';
    $('rain-big').style.display='block';
    $('rain-sub').textContent=rainN===1
      ?(lastRain?'비가 왔습니다':'맑거나 흐린 날이었습니다')
      :`${rainN}일 확인 (마지막: ${lastRain?'비':'맑음'})`;
    $('rain-sub').style.display='block';
  } else {
    $('rain-big').textContent=`+${rainN}일`;
    $('rain-big').style.color='#06b6d4';
    $('rain-big').style.display='block';
    $('rain-sub').textContent=`총 ${rainTotal}일 누적`;
    $('rain-sub').style.display='block';
  }
  $('rain-total').textContent=rainTotal;
  updateRainStats();
}

function updateRainStats(){
  show('rain-stats');
  $('rain-sc').textContent=`총 ${rainTotal}일`;
  renderBars('rain-bars',['비','맑음/흐림'],rainCounts,rainTotal,
    ['#60a5fa','#fbbf24'],[rainProb,1-rainProb],'#06b6d4');

  const rRate=(rainCounts['비']||0)/rainTotal;
  rainHistory.push(rRate);
  const hist=rainHistory.length>200?rainHistory.filter((_,i)=>i%Math.ceil(rainHistory.length/200)===0):rainHistory;
  show('rain-conv');
  drawChart('rain-canvas',hist,rainProb,'#06b6d4','강수 상대도수');

  if(rainTotal>=30){
    $('rain-ins-body').innerHTML=
      `현재 강수 상대도수: <strong>${(rRate*100).toFixed(1)}%</strong><br>` +
      `기상청은 오늘과 <em>비슷한 기상 조건</em>이 과거에 있었던 날을 모두 모아,<br>` +
      `그 중 비가 온 날의 비율을 강수확률로 발표합니다.<br>` +
      `이 비율이 바로 <strong>통계적 확률</strong>이에요!<br>` +
      `실험을 계속 반복하면 상대도수가 <strong>${(rainProb*100).toFixed(0)}%</strong>로 수렴합니다.`;
    show('rain-insight');
  }
}

function resetRain(){
  rainCounts={'비':0,'맑음/흐림':0}; rainTotal=0; rainHistory=[]; rainActive=false;
  $('rain-total').textContent='0';
  hide('rain-stats'); hide('rain-conv'); hide('rain-insight');
  hide('rain-big'); hide('rain-sub');
  show('rain-prompt');
}

/* ═══════════════════════════════════════
   야구 타율
═══════════════════════════════════════ */
let batProb=0.349, playerName='이정후', playerIcon='🦅';
let batCounts={'안타':0,'아웃':0},batTotal=0,batN=1,batHistory=[];
let batActive=false;

const HIT_EMOJIS=['💥','🏃','🎉','👊'];
const OUT_EMOJIS=['😤','⚾','💨','👎'];

function setPlayer(name,avg,icon){
  playerName=name; batProb=avg; playerIcon=icon;
  resetBat();
  $('bat-btn').disabled=false;
  $('bat-prompt').textContent=`${icon} ${name} (타율 ${avg.toFixed(3)}) 선수 등장!`;
  show('bat-prompt');
  $('bat-ref-label').innerHTML=`<span style="color:#22c55e">━ 실제 타율 ${avg.toFixed(3)}</span>`;
}

function doBat(){
  hide('bat-prompt'); hide('bat-big'); hide('bat-sub');
  let lastHit=false;
  for(let i=0;i<batN;i++){
    const h=Math.random()<batProb;
    batCounts[h?'안타':'아웃']++;
    lastHit=h;
  }
  batTotal+=batN;

  if(batN<=10){
    const emoji=lastHit
      ? HIT_EMOJIS[Math.floor(Math.random()*HIT_EMOJIS.length)]
      : OUT_EMOJIS[Math.floor(Math.random()*OUT_EMOJIS.length)];
    $('bat-big').textContent=emoji;
    $('bat-big').style.display='block';
    $('bat-sub').textContent=batN===1
      ?(lastHit?`🎉 안타! ${playerName} 선수 출루!`:`😤 아웃! 다음 타석을 기약합니다.`)
      :`${batN}타석 완료 (마지막: ${lastHit?'안타':'아웃'})`;
    $('bat-sub').style.color=lastHit?'#86efac':'#fca5a5';
    $('bat-sub').style.display='block';
  } else {
    $('bat-big').textContent=`+${batN}타석`;
    $('bat-big').style.color='#22c55e';
    $('bat-big').style.display='block';
    $('bat-sub').textContent=`총 ${batTotal}타석 누적`;
    $('bat-sub').style.display='block';
  }
  $('bat-total').textContent=batTotal;
  updateBatStats();
}

function updateBatStats(){
  show('bat-stats');
  $('bat-sc').textContent=`총 ${batTotal}타석`;
  renderBars('bat-bars',['안타','아웃'],batCounts,batTotal,
    ['#22c55e','#f87171'],[batProb,1-batProb],'#22c55e');

  const hRate=(batCounts['안타']||0)/batTotal;
  batHistory.push(hRate);
  const hist=batHistory.length>200?batHistory.filter((_,i)=>i%Math.ceil(batHistory.length/200)===0):batHistory;
  show('bat-conv');
  drawChart('bat-canvas',hist,batProb,'#22c55e','타율');

  if(batTotal>=30){
    $('bat-ins-body').innerHTML=
      `현재 타율(통계적 확률): <strong>${hRate.toFixed(3)}</strong><br>` +
      `타석이 쌓일수록 이 값이 <strong>${batProb.toFixed(3)}</strong>에 수렴합니다.<br>` +
      `타율이 높은 타자가 한두 번 아웃되어도 실망할 필요 없는 이유가 여기 있어요!<br>` +
      `통계적 확률은 <em>시행 횟수가 충분히 많을 때</em> 의미 있는 값이 됩니다.`;
    show('bat-insight');
  }
}

function resetBat(){
  batCounts={'안타':0,'아웃':0}; batTotal=0; batHistory=[]; batActive=false;
  $('bat-total').textContent='0';
  hide('bat-stats'); hide('bat-conv'); hide('bat-insight');
  hide('bat-big'); hide('bat-sub');
  show('bat-prompt');
}
</script>
</body>
</html>"""


def render():
    st.subheader("🎯 통계적 확률 탐험대")
    st.caption("윷놀이·기상예보·야구 타율로 통계적 확률을 직접 시뮬레이션하며 탐구해봐요!")
    components.html(_HTML, height=1350, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
