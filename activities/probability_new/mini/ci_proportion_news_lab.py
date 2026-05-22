# activities/probability_new/mini/ci_proportion_news_lab.py
"""
모비율 신뢰구간 — 실제 뉴스 속 여론조사 해석

- 실제 뉴스/공공기관 통계 4가지 사례로 모비율의 신뢰구간을 직접 계산
  1) 한국갤럽 「한국인이 좋아하는 스포츠 스타」 — 손흥민 49% (n=1,777)
  2) 농림축산식품부 동물복지 국민의식조사 — 반려동물 양육 비율 (n=5,000)
  3) 통계청 2024 사회조사 — "결혼해야 한다" 응답 (n≈36,000)
  4) 문화체육관광부 국민독서실태조사 — 학생 종합독서율 (n=3,000)
- 단계별 애니메이션으로 p̂q̂/n → √(p̂q̂/n) → k·√(p̂q̂/n) → 신뢰구간 계산
- 수직선 위에 95%·99% 신뢰구간을 비교
- 4개 신뢰구간을 한눈에 비교하는 종합 차트 제공
"""
import streamlit as st
import streamlit.components.v1 as components
from reflection_utils import render_reflection_form

META = {
    "title": "📰 미니: 뉴스로 배우는 모비율 신뢰구간 — 실제 여론조사 해석",
    "description": "한국갤럽(좋아하는 스포츠 스타)·농림축산식품부(반려동물 양육)·통계청(결혼관)·"
                   "문화체육관광부(학생 독서율)의 실제 조사 자료 4건을 가지고 "
                   "신문 기사 속 표본비율로부터 모비율의 95%·99% 신뢰구간을 직접 계산하고, "
                   "기사에 표기된 \"표본오차 ±△%P\"의 의미를 수학적으로 해석합니다.",
    "order": 26,
}

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "모비율신뢰구간_뉴스해석"

_QUESTIONS = [
    {"type": "markdown",
     "text": "**📝 활동 성찰 — 뉴스로 배우는 모비율의 추정**"},
    {
        "key": "표본오차_의미",
        "label": "뉴스 기사 끝에 적힌 **\"95% 신뢰수준에 표본오차 ±△%P\"** 라는 문구가 "
                 "수업 시간에 배운 **신뢰구간 길이의 절반** `k·√(p̂q̂/n)` 과 어떻게 연결되는지 "
                 "본인의 말로 설명해 보세요.",
        "type": "text_area", "height": 110,
        "placeholder": "기사의 \"±△%P\"는 신뢰구간의 ___ 를 의미하고, "
                       "공식 `k·√(p̂q̂/n)` 에서 ___ 에 해당한다.",
    },
    {
        "key": "n과_표본오차",
        "label": "4가지 기사 중 **표본 크기 n** 이 가장 작은 사례(한국갤럽 1,777명)와 "
                 "가장 큰 사례(통계청 36,000명)의 신뢰구간 길이는 어떻게 달랐나요? "
                 "그 이유를 공식과 함께 설명해 보세요.",
        "type": "text_area", "height": 120,
        "placeholder": "n=1,777인 한국갤럽 조사의 신뢰구간은 ___, "
                       "n≈36,000인 통계청 조사의 신뢰구간은 ___. "
                       "이는 공식에서 분모의 √n 이 ___ 하기 때문이다.",
    },
    {
        "key": "신뢰도_95_99",
        "label": "같은 기사 데이터에 대해 신뢰도를 **95%(k=1.96)** 에서 **99%(k=2.58)** 로 올렸을 때 "
                 "신뢰구간이 어떻게 변했는지, 그리고 \"확신을 더 강하게 한다\"는 것이 "
                 "왜 \"폭이 넓어진다\"는 것과 같은 의미인지 적어 보세요.",
        "type": "text_area", "height": 120,
        "placeholder": "신뢰도를 99%로 높이면 k 값이 ___ 커지므로 신뢰구간의 폭이 ___. "
                       "더 강하게 확신하려면 ___ 한 범위를 잡아야 하기 때문이다.",
    },
    {
        "key": "기사해석_나만의말",
        "label": "이번 활동에서 다룬 4가지 기사 중 하나를 골라, "
                 "기사 본문에 적힌 표본비율(예: 49%, 28.6%, 52.5%, 95.8%) 을 "
                 "**\"진짜 모비율 p가 어디 있다고 추정할 수 있다\"** 라는 신뢰구간의 언어로 "
                 "본인이 직접 해석한 한 문장을 적어 보세요.",
        "type": "text_area", "height": 110,
        "placeholder": "예) 95% 신뢰수준에서 진짜 ___ 의 비율 p 는 약 ___ 와 ___ 사이에 있다고 "
                       "추정할 수 있다.",
    },
    {
        "key": "신뢰구간_오해",
        "label": "흔히 신문에서는 \"국민의 52.5% 가 결혼해야 한다고 답했다\" 처럼 "
                 "**한 숫자만** 강조하는 경우가 많아요. "
                 "이런 식의 표현이 **신뢰구간의 관점에서 어떤 점을 놓치게 만드는지** 적어 보세요.",
        "type": "text_area", "height": 110,
        "placeholder": "표본비율 한 숫자만 보면 ___ 을 알 수 없다. "
                       "실제로 진짜 모비율 p는 ___ 일 수 있기 때문이다.",
    },
    {
        "key": "비교_차트_관찰",
        "label": "활동 마지막의 \"4개 신뢰구간 비교\" 차트에서 어떤 조사가 가장 **좁은 신뢰구간**을 가졌고, "
                 "어떤 조사가 가장 **넓은 신뢰구간**을 가졌나요? "
                 "그 이유를 \"표본 크기 n\" 과 \"표본비율 p̂\" 두 관점에서 설명해 보세요.",
        "type": "text_area", "height": 130,
        "placeholder": "가장 좁은 신뢰구간은 ___ 조사였고, 가장 넓은 신뢰구간은 ___ 조사였다. "
                       "n이 클수록 ___ 하고, p̂이 1/2 에 가까울수록 ___ 하기 때문이다.",
    },
    {
        "key": "새롭게알게된점",
        "label": "💡 이 활동을 통해 새롭게 알게 된 점",
        "type": "text_area", "height": 90,
    },
    {
        "key": "느낀점",
        "label": "💬 활동을 마친 후 느낀 점 (뉴스를 볼 때 어떻게 달라질까?)",
        "type": "text_area", "height": 90,
    },
]


_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{
  font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
  background:linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#0f172a 100%);
  color:#e2e8f0;padding:14px 12px;min-height:100vh;
}

/* ============ 헤더 ============ */
.hdr{
  text-align:center;
  background:linear-gradient(135deg,rgba(56,189,248,.18),rgba(168,85,247,.18));
  border:2px solid rgba(56,189,248,.50);border-radius:18px;
  padding:14px 18px;margin-bottom:14px;
}
.hdr h1{font-size:1.65rem;font-weight:900;color:#bae6fd;margin-bottom:5px;letter-spacing:.3px}
.hdr p{font-size:1.08rem;color:#e2e8f0;line-height:1.6}
.hdr b{color:#fde047}

/* ============ 공식 카드 ============ */
.formula{
  background:rgba(15,23,42,.7);
  border:2px dashed rgba(251,191,36,.55);border-radius:14px;
  padding:14px 18px;margin-bottom:13px;
  display:flex;flex-wrap:wrap;justify-content:center;align-items:center;
  gap:18px;font-size:1.32rem;color:#fde68a;font-weight:800;
}
.formula .lab{color:#fbbf24;font-size:1.12rem}
.formula .eq{
  background:rgba(251,191,36,.10);border:1.5px solid rgba(251,191,36,.45);
  padding:7px 14px;border-radius:10px;letter-spacing:.5px;
}

/* ============ 패널 ============ */
.panel{
  background:rgba(15,23,42,.72);border:1.5px solid rgba(56,189,248,.32);
  border-radius:14px;padding:14px;margin-bottom:13px;
}
.panel h2{
  font-size:1.22rem;font-weight:900;color:#7dd3fc;margin-bottom:11px;
  display:flex;align-items:center;gap:9px;letter-spacing:.3px;
}
.panel h2 .badge{
  font-size:.88rem;color:#cbd5e1;background:rgba(56,189,248,.18);
  padding:3px 10px;border-radius:999px;font-weight:700;
}

/* ============ 탭 ============ */
.tab-row{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:13px}
.tab{
  padding:11px 18px;border-radius:14px;font-size:1.05rem;font-weight:800;
  border:2px solid transparent;cursor:pointer;color:#cbd5e1;
  background:linear-gradient(135deg,#475569,#334155);
  transition:all .15s ease;flex:1;min-width:165px;text-align:center;
  display:flex;flex-direction:column;align-items:center;gap:2px;
}
.tab .tab-emoji{font-size:1.6rem;line-height:1.2}
.tab .tab-name{font-size:1rem}
.tab small{font-size:.82rem;font-weight:600;opacity:.85;color:#cbd5e1}
.tab:hover{transform:translateY(-1px)}
.tab.active{
  background:linear-gradient(135deg,#0891b2,#0e7490);
  border-color:#67e8f9;box-shadow:0 4px 14px rgba(8,145,178,.55);color:#fff;
}
.tab.active small{color:#bae6fd}

/* ============ 뉴스 기사 카드 (신문 스타일) ============ */
.news-card{
  background:#f8fafc;color:#0f172a;
  border:3px solid #1e293b;border-radius:12px;
  padding:18px 22px;
  box-shadow:0 6px 18px rgba(0,0,0,.45);
  font-family:'Pretendard','Nanum Myeongjo','Apple SD Gothic Neo',serif;
  position:relative;
}
.news-card::before{
  content:"";position:absolute;top:-3px;left:18px;right:18px;height:5px;
  background:#0f172a;
}
.news-masthead{
  display:flex;justify-content:space-between;align-items:flex-end;
  border-bottom:2px solid #0f172a;padding-bottom:5px;margin-bottom:10px;
  font-family:'Pretendard',sans-serif;
}
.news-press{
  font-size:1.15rem;font-weight:900;color:#0f172a;letter-spacing:.5px;
}
.news-date{font-size:.95rem;color:#475569;font-weight:700}
.news-headline{
  font-size:1.45rem;font-weight:900;color:#0f172a;line-height:1.35;
  margin-bottom:10px;letter-spacing:-.2px;
}
.news-body{
  font-size:1.05rem;color:#1e293b;line-height:1.7;font-weight:500;
}
.news-body .hi{
  background:linear-gradient(180deg,transparent 55%,#fde047 55%,#fde047 95%,transparent 95%);
  padding:0 3px;font-weight:800;color:#0f172a;
}
.news-body .pcnt{color:#be185d;font-weight:900}
.news-meta{
  margin-top:11px;padding-top:9px;border-top:1.5px dashed #94a3b8;
  font-size:.92rem;color:#475569;font-family:'Pretendard',sans-serif;font-weight:600;
  line-height:1.55;
}
.news-meta b{color:#1e293b}

/* ============ 데이터 추출 카드 ============ */
.extract{
  display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:13px;
}
@media(max-width:720px){.extract{grid-template-columns:repeat(2,1fr)}}
.ext{
  background:rgba(56,189,248,.10);border:2px solid rgba(56,189,248,.42);
  border-radius:12px;padding:11px;text-align:center;
}
.ext .lab{font-size:.95rem;color:#7dd3fc;font-weight:800;margin-bottom:3px}
.ext .val{
  font-size:1.55rem;color:#bae6fd;font-weight:900;
  font-variant-numeric:tabular-nums;letter-spacing:.3px;
}
.ext.gold{background:rgba(251,191,36,.10);border-color:rgba(251,191,36,.42)}
.ext.gold .lab{color:#fde68a}
.ext.gold .val{color:#fde047}

/* ============ 컨트롤 ============ */
.ctl{
  display:flex;align-items:center;gap:14px;flex-wrap:wrap;
  background:rgba(168,85,247,.07);border:1.5px solid rgba(168,85,247,.32);
  border-radius:11px;padding:11px 14px;margin:10px 0;
}
.ctl-lab{font-size:1.05rem;font-weight:800;color:#c4b5fd;min-width:115px}
.k-btn{
  padding:9px 16px;border-radius:11px;font-size:1.02rem;font-weight:900;
  border:2px solid transparent;background:rgba(71,85,105,.6);color:#cbd5e1;
  cursor:pointer;transition:all .14s ease;letter-spacing:.3px;
}
.k-btn.active{
  background:linear-gradient(135deg,#a855f7,#7e22ce);color:#fff;
  border-color:#c4b5fd;box-shadow:0 3px 10px rgba(168,85,247,.5);
}
.btn-go{
  padding:11px 22px;border:none;border-radius:11px;font-weight:900;
  font-size:1.06rem;color:#fff;cursor:pointer;letter-spacing:.4px;
  background:linear-gradient(135deg,#22d3ee,#0e7490);
  box-shadow:0 3px 12px rgba(34,211,238,.45);transition:all .15s ease;
}
.btn-go:hover{transform:translateY(-1px);background:linear-gradient(135deg,#06b6d4,#155e75)}
.btn-go:active{transform:scale(.97)}

/* ============ 계산 스텝 카드 ============ */
.steps{
  display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:8px;
}
@media(max-width:900px){.steps{grid-template-columns:repeat(2,1fr)}}
.step{
  background:rgba(15,23,42,.6);border:2px solid rgba(148,163,184,.25);
  border-radius:12px;padding:11px;position:relative;
  opacity:0;transform:translateY(8px);
  transition:opacity .35s ease, transform .35s ease, border-color .35s ease;
}
.step.show{opacity:1;transform:translateY(0)}
.step.lit{border-color:rgba(251,191,36,.6);box-shadow:0 0 14px rgba(251,191,36,.20)}
.step .num{
  position:absolute;top:-10px;left:10px;
  width:24px;height:24px;border-radius:50%;
  background:#fbbf24;color:#0f172a;font-size:.85rem;font-weight:900;
  display:flex;align-items:center;justify-content:center;
}
.step .lab{
  font-size:.92rem;color:#fde68a;font-weight:800;margin-top:6px;margin-bottom:5px;
  letter-spacing:.3px;
}
.step .calc{
  font-size:1rem;color:#cbd5e1;line-height:1.5;font-weight:600;
  font-variant-numeric:tabular-nums;
}
.step .res{
  margin-top:6px;font-size:1.4rem;font-weight:900;color:#fde047;
  font-variant-numeric:tabular-nums;letter-spacing:.4px;
}

/* ============ 결과 강조 ============ */
.result-bar{
  margin-top:11px;padding:14px 18px;border-radius:14px;
  background:linear-gradient(135deg,rgba(34,211,238,.18),rgba(168,85,247,.18));
  border:2.5px solid rgba(34,211,238,.55);
  display:flex;flex-wrap:wrap;justify-content:space-around;align-items:center;
  gap:14px;font-size:1.15rem;color:#bae6fd;font-weight:800;
}
.result-bar .ci-text{
  font-size:1.55rem;color:#fef3c7;font-weight:900;
  font-variant-numeric:tabular-nums;letter-spacing:.4px;
}
.result-bar .conf-tag{
  background:rgba(168,85,247,.30);border:1.5px solid rgba(168,85,247,.6);
  padding:5px 14px;border-radius:999px;font-size:1.02rem;color:#e9d5ff;
}

/* ============ 수직선 ============ */
.numline-wrap{
  background:rgba(15,23,42,.55);border:1.5px solid rgba(148,163,184,.25);
  border-radius:12px;padding:11px;margin-top:11px;
}
#numlineCanvas{display:block;width:100%;height:230px;background:rgba(15,23,42,.4);border-radius:8px}

.compare-text{
  margin-top:10px;padding:11px 14px;border-radius:11px;
  background:rgba(34,197,94,.10);border:1.5px solid rgba(34,197,94,.4);
  font-size:1rem;color:#dcfce7;font-weight:600;line-height:1.6;
}
.compare-text b{color:#86efac}
.compare-text code{
  background:rgba(15,23,42,.5);padding:2px 7px;border-radius:5px;
  color:#fde047;font-size:.97em;
}

/* ============ 비교 차트 ============ */
.cmp-wrap{
  background:rgba(15,23,42,.6);border:2px solid rgba(168,85,247,.45);
  border-radius:14px;padding:13px;
}
#cmpCanvas{display:block;width:100%;height:340px;background:rgba(15,23,42,.4);border-radius:8px}

/* ============ 해석 카드 ============ */
.interp{
  background:linear-gradient(135deg,rgba(251,191,36,.10),rgba(244,114,182,.08));
  border:2px solid rgba(251,191,36,.45);border-radius:13px;
  padding:14px 18px;margin-top:12px;
  font-size:1.08rem;color:#fef3c7;line-height:1.75;font-weight:600;
}
.interp .ico{font-size:1.5rem}
.interp b{color:#fde047}
.interp .pop{color:#fbcfe8;font-weight:900}

/* ============ 인사이트 카드 ============ */
.insight{
  background:rgba(34,211,238,.10);border:2px solid rgba(34,211,238,.45);
  border-radius:13px;padding:13px 16px;margin-top:12px;
  font-size:1.04rem;color:#cffafe;line-height:1.7;
  display:flex;align-items:flex-start;gap:10px;font-weight:600;
}
.insight .ico{font-size:1.6rem;flex-shrink:0;line-height:1.2}
.insight b{color:#fde047}
.insight code{
  background:rgba(15,23,42,.6);padding:2px 6px;border-radius:5px;
  color:#fde047;font-size:.97em;letter-spacing:.3px;
}

/* 펄스 (결과 바) */
@keyframes pulse-blue{
  0%{box-shadow:0 0 0 0 rgba(34,211,238,.6)}
  100%{box-shadow:0 0 0 18px rgba(34,211,238,0)}
}
.result-bar.pulse{animation:pulse-blue .9s ease}

/* 탭 전환 페이드 */
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
.tab-content{animation:fadeIn .3s ease}

</style>
</head>
<body>

<div class="hdr">
  <h1>📰 뉴스로 배우는 모비율 신뢰구간 — 실제 여론조사를 해석해 보자!</h1>
  <p>한국갤럽·농림축산식품부·통계청·문화체육관광부의 <b>실제 조사 자료 4건</b>으로<br>
     기사 속 표본비율 <b>p̂</b> 에서 모비율 <b>p</b> 의 신뢰구간을 직접 계산하고 해석합니다.</p>
</div>

<div class="formula">
  <span class="lab">📐 모비율의 신뢰구간</span>
  <span class="eq">p̂ − k √( p̂q̂ / n ) ≤ p ≤ p̂ + k √( p̂q̂ / n )</span>
  <span class="lab">신뢰도 95% → k=1.96 &nbsp; 99% → k=2.58</span>
</div>

<!-- ① 탭: 4가지 기사 -->
<div class="panel">
  <h2>📑 사례 선택 <span class="badge">서로 다른 4개의 실제 조사</span></h2>
  <div class="tab-row" id="tabRow">
    <button class="tab active" data-key="sonny">
      <span class="tab-emoji">⚽</span>
      <span class="tab-name">손흥민 좋아요</span>
      <small>한국갤럽 · 2024.6</small>
    </button>
    <button class="tab" data-key="pet">
      <span class="tab-emoji">🐶</span>
      <span class="tab-name">반려동물 양육</span>
      <small>농림축산식품부 · 2024.12</small>
    </button>
    <button class="tab" data-key="marry">
      <span class="tab-emoji">💍</span>
      <span class="tab-name">결혼해야 한다</span>
      <small>통계청 · 2024.11</small>
    </button>
    <button class="tab" data-key="read">
      <span class="tab-emoji">📚</span>
      <span class="tab-name">학생 종합독서율</span>
      <small>문체부 · 2024.4</small>
    </button>
  </div>
</div>

<!-- ② 기사 카드 -->
<div class="panel tab-content" id="newsPanel">
  <h2>📰 기사 들여다보기 <span class="badge">실제 발표 자료</span></h2>
  <div class="news-card" id="newsCard">
    <!-- JS로 채워짐 -->
  </div>

  <div class="extract">
    <div class="ext"><div class="lab">표본 크기 n</div><div class="val" id="exN">--</div></div>
    <div class="ext gold"><div class="lab">표본비율 p̂</div><div class="val" id="exP">--</div></div>
    <div class="ext"><div class="lab">기사의 표본오차</div><div class="val" id="exMar">--</div></div>
    <div class="ext"><div class="lab">기사의 신뢰수준</div><div class="val" id="exConf">95%</div></div>
  </div>
</div>

<!-- ③ 신뢰도 설정 + 계산 -->
<div class="panel">
  <h2>🧮 신뢰구간 단계별 계산 <span class="badge">버튼을 눌러 한 단계씩!</span></h2>

  <div class="ctl">
    <span class="ctl-lab">신뢰도 선택</span>
    <button class="k-btn active" data-k="1.96">95% &nbsp;(k = 1.96)</button>
    <button class="k-btn" data-k="2.58">99% &nbsp;(k = 2.58)</button>
    <span style="flex:1"></span>
    <button class="btn-go" id="btnCalc">▶ 신뢰구간 단계별 계산하기</button>
  </div>

  <div class="steps" id="stepsBox">
    <div class="step" id="s1">
      <div class="num">1</div>
      <div class="lab">p̂ q̂ = p̂ · (1−p̂)</div>
      <div class="calc" id="c1">--</div>
      <div class="res" id="r1">--</div>
    </div>
    <div class="step" id="s2">
      <div class="num">2</div>
      <div class="lab">p̂ q̂ / n</div>
      <div class="calc" id="c2">--</div>
      <div class="res" id="r2">--</div>
    </div>
    <div class="step" id="s3">
      <div class="num">3</div>
      <div class="lab">√(p̂ q̂ / n)  =  표준편차 σ(p̂)</div>
      <div class="calc" id="c3">--</div>
      <div class="res" id="r3">--</div>
    </div>
    <div class="step" id="s4">
      <div class="num">4</div>
      <div class="lab">k · √(p̂ q̂ / n)  =  오차한계 (=구간 길이의 ½)</div>
      <div class="calc" id="c4">--</div>
      <div class="res" id="r4">--</div>
    </div>
  </div>

  <div class="result-bar" id="resultBar">
    <span>📍 모비율 <b style="color:#fde047">p</b> 의</span>
    <span class="conf-tag" id="confTag">95% 신뢰구간</span>
    <span class="ci-text" id="ciText">계산 버튼을 눌러 주세요</span>
  </div>

  <div class="numline-wrap">
    <canvas id="numlineCanvas" width="900" height="230"></canvas>
  </div>

  <div class="compare-text" id="cmpText">
    💬 ▶ 단계별 계산 버튼을 누르면 신뢰구간이 표시됩니다.
  </div>
</div>

<!-- ④ 해석 카드 -->
<div class="panel">
  <h2>📝 한 문장으로 해석하기 <span class="badge">신뢰구간을 일상 언어로</span></h2>
  <div class="interp" id="interp">
    <span class="ico">🗣️</span>
    <span id="interpText">먼저 신뢰구간을 계산해 주세요.</span>
  </div>
</div>

<!-- ⑤ 4개 비교 -->
<div class="panel">
  <h2>📊 4개 신뢰구간 한눈에 비교 <span class="badge">현재 신뢰도 기준</span></h2>
  <div class="cmp-wrap">
    <canvas id="cmpCanvas" width="900" height="340"></canvas>
  </div>
  <div class="insight">
    <span class="ico">💡</span>
    <span>
      4개 조사를 비교해 보면, 표본 크기 <code>n</code> 이 작을수록 신뢰구간의 폭이 <b>넓고</b>,
      클수록 신뢰구간이 <b>가늘어진다</b>는 걸 한눈에 볼 수 있어요. <br>
      또 같은 n 이라도 <code>p̂</code> 이 <b>½</b> 에 가까울수록 <code>p̂q̂</code> 이 커져
      신뢰구간이 더 넓어진다는 점도 함께 관찰해 보세요!
    </span>
  </div>
</div>

<script>
/* =============== 사례 데이터 (실제 조사 결과) =============== */
const CASES = {
  sonny: {
    icon: "⚽",
    color: "#60a5fa",
    color2: "#1d4ed8",
    press: "한국갤럽 「한국인이 좋아하는 스포츠 스타」 조사",
    date: "2024년 6월 13일 발표 (2024년 3월 22일~4월 5일 조사)",
    headline: "손흥민, 한국인이 좋아하는 스포츠 스타 49% — 압도적 1위",
    body: `한국갤럽이 발표한 「한국인이 좋아하는 스포츠 스타」 조사 결과,
           <span class="hi">손흥민</span> 선수를 가장 좋아하는 스포츠 스타로 꼽은 응답자가
           <span class="pcnt">49%</span> 로 압도적 1위를 차지했다. 김연아(10%)·박세리(5%)·
           류현진(4%) 등이 그 뒤를 이었다.`,
    survey_meta: `전국(제주 제외) 만 13세 이상 <b>1,777명</b> · 면접조사원 인터뷰(CAPI) ·
                  층화 집락 확률 비례 추출 · 응답률 27.7% ·
                  <b>표본오차 ±2.3%P (95% 신뢰수준)</b>`,
    n: 1777,
    phat: 0.49,
    target: "손흥민을 가장 좋아한다고 답한 사람",
    pop:    "전국(제주 제외) 만 13세 이상 국민",
    reported_margin: 2.3,
  },
  pet: {
    icon: "🐶",
    color: "#34d399",
    color2: "#059669",
    press: "농림축산식품부 보도자료",
    date: "2024년 12월 발표 (2024년 동물복지에 대한 국민의식조사)",
    headline: "한국 가구 28.6%, 반려동물과 함께 산다 — 역대 최고",
    body: `농림축산식품부가 발표한 「2024년 동물복지에 대한 국민의식조사」에 따르면,
           <span class="hi">반려동물을 기르고 있는 가구의 비율</span> 은
           <span class="pcnt">28.6%</span> 로 조사되었다. 이는 4년 전(27.7%) 보다 0.9%P 늘어난
           역대 최고치다.`,
    survey_meta: `전국 만 20~64세 일반 국민 <b>5,000명</b> · 온라인 패널 조사 ·
                  <b>표본오차 ±1.39%P (95% 신뢰수준)</b>`,
    n: 5000,
    phat: 0.286,
    target: "반려동물 양육 가구",
    pop:    "전국 만 20~64세 국민",
    reported_margin: 1.39,
  },
  marry: {
    icon: "💍",
    color: "#f472b6",
    color2: "#be185d",
    press: "통계청 「2024년 사회조사」",
    date: "2024년 11월 12일 발표",
    headline: "국민 52.5% \"결혼해야 한다\" — 8년 만에 최고치",
    body: `통계청이 발표한 「2024년 사회조사」 결과에 따르면, 만 13세 이상 국민 가운데
           <span class="hi">'결혼해야 한다'</span> 라고 응답한 비율이
           <span class="pcnt">52.5%</span> 로 집계되었다. 이는 2년 전(50.0%) 보다 2.5%P 증가한
           수치이며, 2016년 이후 8년 만에 가장 높은 수준이다.`,
    survey_meta: `전국 만 13세 이상 가구원 약 <b>36,000명</b> · 2024년 5월 15일부터 16일간
                  방문 면접조사 · <b>표본오차 ±0.5%P (95% 신뢰수준, 추정치)</b>`,
    n: 36000,
    phat: 0.525,
    target: "'결혼해야 한다' 응답자",
    pop:    "전국 만 13세 이상 국민",
    reported_margin: 0.52,
  },
  read: {
    icon: "📚",
    color: "#fbbf24",
    color2: "#b45309",
    press: "문화체육관광부 보도자료",
    date: "2024년 4월 18일 발표 (2023년 국민 독서실태조사)",
    headline: "초·중·고 학생 95.8%가 책을 읽는다",
    body: `문화체육관광부가 발표한 「2023년 국민 독서실태조사」에 따르면,
           초·중·고등학생의 <span class="hi">종합 독서율</span> (지난 1년간 종이책·전자책·
           오디오북 중 한 권 이상 읽은 학생의 비율) 이
           <span class="pcnt">95.8%</span> 로 나타났다. 연간 종합 독서량은 36권으로
           집계되었다.`,
    survey_meta: `전국 초·중·고등학생 <b>3,000명</b> · 학교 단위 표본추출 후 면접조사 ·
                  <b>표본오차 ±1.79%P (95% 신뢰수준, 최대치 기준)</b>`,
    n: 3000,
    phat: 0.958,
    target: "지난 1년간 책을 1권 이상 읽은 학생",
    pop:    "전국 초·중·고등학생",
    reported_margin: 1.79,
  }
};

/* =============== 상태 =============== */
let curKey = "sonny";
let k = 1.96;
let computed = null;  // {phat, n, k, half, lo, hi}

const $ = id => document.getElementById(id);
const fmt  = (v,d=4) => isFinite(v) ? Number(v.toFixed(d)).toString() : '--';
const fmtP = (v,d=2) => isFinite(v) ? (v*100).toFixed(d) + '%' : '--';

/* =============== 기사 카드 그리기 =============== */
function renderNews(){
  const c = CASES[curKey];
  $('newsCard').innerHTML =
    '<div class="news-masthead">'+
      '<span class="news-press">'+c.press+'</span>'+
      '<span class="news-date">'+c.date+'</span>'+
    '</div>'+
    '<div class="news-headline">'+c.icon+' '+c.headline+'</div>'+
    '<div class="news-body">'+c.body+'</div>'+
    '<div class="news-meta">📌 <b>조사 개요</b> &nbsp;'+ c.survey_meta +'</div>';

  $('exN').textContent  = c.n.toLocaleString();
  $('exP').textContent  = fmtP(c.phat,1);
  $('exMar').textContent = '±'+c.reported_margin+'%P';
  $('exConf').textContent = '95%';

  // 초기화
  computed = null;
  resetSteps();
  $('ciText').textContent = '계산 버튼을 눌러 주세요';
  $('confTag').textContent = (k===1.96?'95%':'99%')+' 신뢰구간';
  $('cmpText').innerHTML = '💬 ▶ 단계별 계산 버튼을 누르면 신뢰구간이 표시됩니다.';
  $('interpText').textContent = '먼저 신뢰구간을 계산해 주세요.';
  drawNumline();
  drawCompare();
}

/* =============== 스텝 리셋 =============== */
function resetSteps(){
  for(let i=1;i<=4;i++){
    const s = $('s'+i);
    s.classList.remove('show','lit');
    $('c'+i).textContent = '--';
    $('r'+i).textContent = '--';
  }
}

/* =============== 단계별 계산 (애니메이션) =============== */
function calculate(){
  const c = CASES[curKey];
  const p = c.phat, q = 1-c.phat, n = c.n;
  const pq = p*q;
  const pqn = pq/n;
  const sigma = Math.sqrt(pqn);
  const half = k*sigma;
  const lo = p - half, hi = p + half;
  computed = { phat:p, n, k, sigma, half, lo, hi };

  resetSteps();

  // 단계 1
  setTimeout(()=>{
    $('c1').innerHTML = 'p̂ = '+fmt(p,3)+' &nbsp;,&nbsp; q̂ = 1 − '+fmt(p,3)+' = '+fmt(q,3) +
                       '<br>p̂q̂ = '+fmt(p,3)+' × '+fmt(q,3);
    $('r1').textContent = '≈ '+fmt(pq,5);
    $('s1').classList.add('show','lit');
    setTimeout(()=>$('s1').classList.remove('lit'), 500);
  }, 100);

  // 단계 2
  setTimeout(()=>{
    $('c2').innerHTML = 'p̂q̂ / n = '+fmt(pq,5)+' ÷ '+n.toLocaleString();
    $('r2').textContent = '≈ '+pqn.toExponential(3);
    $('s2').classList.add('show','lit');
    setTimeout(()=>$('s2').classList.remove('lit'), 500);
  }, 700);

  // 단계 3
  setTimeout(()=>{
    $('c3').innerHTML = '√(p̂q̂/n) = √('+pqn.toExponential(3)+')';
    $('r3').textContent = '≈ '+fmt(sigma,5);
    $('s3').classList.add('show','lit');
    setTimeout(()=>$('s3').classList.remove('lit'), 500);
  }, 1300);

  // 단계 4
  setTimeout(()=>{
    $('c4').innerHTML = 'k × √(p̂q̂/n) = '+k.toFixed(2)+' × '+fmt(sigma,5);
    $('r4').textContent = '≈ '+fmt(half,5);
    $('s4').classList.add('show','lit');
    setTimeout(()=>$('s4').classList.remove('lit'), 500);
    // 결과 표시
    showResult();
  }, 1900);
}

/* =============== 결과 + 해석 =============== */
function showResult(){
  const c = CASES[curKey];
  const r = computed;
  const conf = (k===1.96?'95%':'99%');
  $('confTag').textContent = conf+' 신뢰구간';
  $('ciText').innerHTML =
    '[ '+fmt(r.lo,4)+' , '+fmt(r.hi,4)+' ] &nbsp; ' +
    '<span style="font-size:1.05rem;color:#bae6fd">' +
    '= '+fmtP(r.lo,2)+' ~ '+fmtP(r.hi,2)+'</span>';
  $('resultBar').classList.add('pulse');
  setTimeout(()=>$('resultBar').classList.remove('pulse'), 900);

  // 기사 표본오차와 비교
  const calcMargin = r.half*100;
  const reported = c.reported_margin;
  const diff = Math.abs(calcMargin - reported);
  let cmpMsg = '';
  if(k === 1.96){
    cmpMsg = '🔍 기사에 적힌 표본오차는 <b>±'+reported+'%P</b>, '+
             '우리가 계산한 95% 오차한계 <code>k·√(p̂q̂/n)</code> 는 <b>±'+
             calcMargin.toFixed(2)+'%P</b> 로 거의 ' +
             (diff < 0.5 ? '일치' : '비슷한 수준') + '!<br>'+
             '👉 신문 기사의 \"표본오차 ±△%P\"는 바로 우리가 배운 ' +
             '<code>k·√(p̂q̂/n)</code> 였어요. 기사들은 보통 <b>p̂=½</b> 을 가정하여 ' +
             '최대 오차로 표기합니다.';
  } else {
    cmpMsg = '🔍 신뢰도를 <b>99%</b> 로 올리면 오차한계가 <b>±'+calcMargin.toFixed(2) +
             '%P</b> 로 더 커집니다. (95%일 때는 약 ±'+(1.96/2.58*calcMargin).toFixed(2)+'%P)<br>'+
             '👉 \"더 강하게 확신\" 하려면 \"더 넓은 범위\" 를 잡아야 하는 것이지요.';
  }
  $('cmpText').innerHTML = cmpMsg;

  // 해석
  $('interpText').innerHTML =
    '신뢰도 <b>'+conf+'</b> 에서 ' +
    '<span class="pop">'+c.pop+'</span> 중 ' +
    '<b>'+c.target+'</b> 의 비율 <span class="pop">p</span> 는<br>'+
    '약 <b>'+fmtP(r.lo,2)+'</b> ~ <b>'+fmtP(r.hi,2)+'</b> 사이에 있다고 추정할 수 있다.';

  drawNumline();
  drawCompare();
}

/* =============== 수직선 그리기 =============== */
function drawNumline(){
  const cv = $('numlineCanvas');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const c = CASES[curKey];
  // 표시 영역 - p̂ 주변을 확대
  const center = c.phat;
  const halfWindow = Math.max(0.06, (computed ? computed.half : c.reported_margin/100)*4);
  let xMin = Math.max(0, center - halfWindow);
  let xMax = Math.min(1, center + halfWindow);
  if(xMax-xMin < 0.04){ xMin = Math.max(0, center-0.04); xMax = Math.min(1, center+0.04); }

  const padL=44, padR=44, padT=46, padB=70;
  const plotW = W-padL-padR, plotH = H-padT-padB;
  const yMid = padT + plotH/2;

  const X = v => padL + (v - xMin)/(xMax - xMin) * plotW;

  // 축선
  ctx.strokeStyle='rgba(148,163,184,.6)';
  ctx.lineWidth=2;
  ctx.beginPath();
  ctx.moveTo(padL, yMid); ctx.lineTo(W-padR, yMid);
  ctx.stroke();

  // 눈금
  const ticks = 9;
  ctx.strokeStyle='rgba(148,163,184,.4)';
  ctx.lineWidth=1;
  ctx.fillStyle='#cbd5e1';
  ctx.font='13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  for(let i=0;i<ticks;i++){
    const v = xMin + (i/(ticks-1))*(xMax-xMin);
    const x = X(v);
    ctx.beginPath();
    ctx.moveTo(x, yMid-7); ctx.lineTo(x, yMid+7);
    ctx.stroke();
    ctx.fillText((v*100).toFixed(1)+'%', x, yMid+12);
  }

  // 축 라벨
  ctx.fillStyle='#94a3b8';
  ctx.font='bold 13px sans-serif';
  ctx.fillText('모비율 p (퍼센트)', W/2, H-22);

  // p̂ 점
  const xc = X(c.phat);
  ctx.fillStyle='#fff';
  ctx.beginPath();
  ctx.arc(xc, yMid, 10, 0, Math.PI*2);
  ctx.fill();
  ctx.strokeStyle='#0f172a';
  ctx.lineWidth=2;
  ctx.stroke();
  ctx.fillStyle='#fde047';
  ctx.font='bold 16px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  ctx.fillText('p̂ = '+fmtP(c.phat,1), xc, yMid-22);

  if(!computed){
    ctx.fillStyle='#94a3b8';
    ctx.font='14px sans-serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText('단계별 계산 후 신뢰구간이 표시됩니다', W/2, padT+18);
    return;
  }

  // 신뢰구간 막대
  const x1 = X(Math.max(xMin, computed.lo));
  const x2 = X(Math.min(xMax, computed.hi));
  const grad = ctx.createLinearGradient(x1, 0, x2, 0);
  grad.addColorStop(0, 'rgba(34,211,238,.85)');
  grad.addColorStop(1, 'rgba(168,85,247,.85)');
  ctx.strokeStyle = grad;
  ctx.lineWidth = 22;
  ctx.lineCap='round';
  ctx.beginPath();
  ctx.moveTo(x1, yMid); ctx.lineTo(x2, yMid);
  ctx.stroke();
  ctx.lineCap='butt';

  // 양 끝 표시
  ctx.strokeStyle = '#67e8f9';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(x1, yMid-26); ctx.lineTo(x1, yMid+26);
  ctx.moveTo(x2, yMid-26); ctx.lineTo(x2, yMid+26);
  ctx.stroke();

  // 라벨
  ctx.fillStyle='#67e8f9';
  ctx.font='bold 14px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  ctx.fillText(fmtP(computed.lo,2), x1, yMid+50);
  ctx.fillText(fmtP(computed.hi,2), x2, yMid+50);

  // p̂ 점 다시 그리기 (CI 위에)
  ctx.fillStyle='#fff';
  ctx.beginPath();
  ctx.arc(xc, yMid, 10, 0, Math.PI*2);
  ctx.fill();
  ctx.strokeStyle='#0f172a';
  ctx.lineWidth=2;
  ctx.stroke();

  // 길이 표시 (위쪽 화살표)
  const arrY = padT + 8;
  ctx.strokeStyle='rgba(196,181,253,.7)';
  ctx.lineWidth=1.5;
  ctx.beginPath();
  ctx.moveTo(x1, arrY); ctx.lineTo(x2, arrY);
  ctx.moveTo(x1, arrY-6); ctx.lineTo(x1, arrY+6);
  ctx.moveTo(x2, arrY-6); ctx.lineTo(x2, arrY+6);
  ctx.stroke();
  ctx.fillStyle='#c4b5fd';
  ctx.font='bold 13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='alphabetic';
  ctx.fillText('구간 길이 ≈ '+(computed.half*2*100).toFixed(2)+'%P', (x1+x2)/2, arrY-9);
}

/* =============== 4개 비교 차트 =============== */
function drawCompare(){
  const cv = $('cmpCanvas');
  const ctx = cv.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const W = cv.clientWidth, H = cv.clientHeight;
  cv.width = W*dpr; cv.height = H*dpr;
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);

  const keys = ['sonny','pet','marry','read'];
  const padL=170, padR=40, padT=24, padB=46;
  const plotW = W-padL-padR, plotH = H-padT-padB;

  const xMin=0, xMax=1;
  const X = v => padL + (v-xMin)/(xMax-xMin)*plotW;

  // x축 눈금
  ctx.strokeStyle='rgba(148,163,184,.4)';
  ctx.lineWidth=1; ctx.setLineDash([3,3]);
  ctx.fillStyle='#cbd5e1';
  ctx.font='12px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  for(let i=0;i<=10;i++){
    const v = i/10;
    const x = X(v);
    ctx.beginPath();
    ctx.moveTo(x, padT); ctx.lineTo(x, padT+plotH);
    ctx.stroke();
    ctx.fillText((v*100).toFixed(0)+'%', x, padT+plotH+5);
  }
  ctx.setLineDash([]);

  ctx.fillStyle='#94a3b8';
  ctx.font='bold 13px sans-serif';
  ctx.fillText('모비율 p (퍼센트)', padL+plotW/2, H-16);

  // 행마다 그리기
  const rowH = plotH / keys.length;
  keys.forEach((kkey, i) => {
    const c = CASES[kkey];
    const y = padT + rowH*(i+0.5);
    const phat = c.phat;
    const q = 1-phat;
    const half = k*Math.sqrt(phat*q/c.n);
    const lo = phat-half, hi = phat+half;

    // y 가이드라인
    ctx.strokeStyle='rgba(148,163,184,.18)';
    ctx.lineWidth=1;
    ctx.beginPath();
    ctx.moveTo(padL, y); ctx.lineTo(padL+plotW, y);
    ctx.stroke();

    // 라벨
    ctx.fillStyle='#e2e8f0';
    ctx.font='bold 14px sans-serif';
    ctx.textAlign='right'; ctx.textBaseline='middle';
    ctx.fillText(c.icon+' '+c.target, padL-10, y-5);
    ctx.font='12px sans-serif';
    ctx.fillStyle='#94a3b8';
    ctx.fillText('n='+c.n.toLocaleString()+'  p̂='+fmtP(phat,1), padL-10, y+12);

    // CI 막대
    const x1 = X(lo), x2 = X(hi);
    ctx.strokeStyle = c.color;
    ctx.lineWidth = 14;
    ctx.lineCap='round';
    ctx.beginPath();
    ctx.moveTo(x1, y); ctx.lineTo(x2, y);
    ctx.stroke();
    ctx.lineCap='butt';

    // 끝 마커
    ctx.strokeStyle = c.color2;
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.moveTo(x1, y-18); ctx.lineTo(x1, y+18);
    ctx.moveTo(x2, y-18); ctx.lineTo(x2, y+18);
    ctx.stroke();

    // p̂ 점
    ctx.fillStyle = '#fff';
    ctx.beginPath();
    ctx.arc(X(phat), y, 6, 0, Math.PI*2);
    ctx.fill();
    ctx.strokeStyle='#0f172a';
    ctx.lineWidth=1.5;
    ctx.stroke();

    // 길이 라벨
    ctx.fillStyle = c.color;
    ctx.font='bold 12px sans-serif';
    ctx.textAlign='left'; ctx.textBaseline='middle';
    const lenTxt = '폭 ±'+(half*100).toFixed(2)+'%P';
    if(x2 + 110 < W-padR){
      ctx.fillText(lenTxt, x2+8, y);
    } else {
      ctx.textAlign='right';
      ctx.fillText(lenTxt, x1-8, y);
    }

    // 현재 선택된 케이스 강조
    if(kkey === curKey){
      ctx.strokeStyle='rgba(251,191,36,.85)';
      ctx.lineWidth=2; ctx.setLineDash([6,3]);
      ctx.strokeRect(padL-160, y-22, plotW+160, 44);
      ctx.setLineDash([]);
    }
  });

  // 제목
  ctx.fillStyle='#cbd5e1';
  ctx.font='bold 13px sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='top';
  ctx.fillText('현재 신뢰도: '+(k===1.96?'95% (k=1.96)':'99% (k=2.58)')+' · 노란 점선 = 현재 선택된 사례', W/2, 4);
}

/* =============== 이벤트 =============== */
document.querySelectorAll('.tab').forEach(b=>{
  b.addEventListener('click', ()=>{
    document.querySelectorAll('.tab').forEach(x=>x.classList.toggle('active', x===b));
    curKey = b.dataset.key;
    renderNews();
  });
});

document.querySelectorAll('.k-btn').forEach(b=>{
  b.addEventListener('click', ()=>{
    document.querySelectorAll('.k-btn').forEach(x=>x.classList.toggle('active', x===b));
    k = parseFloat(b.dataset.k);
    $('confTag').textContent = (k===1.96?'95%':'99%')+' 신뢰구간';
    // 계산이 되어 있으면 다시 계산
    if(computed){
      calculate();
    } else {
      drawCompare();
    }
  });
});

$('btnCalc').addEventListener('click', calculate);

window.addEventListener('resize', ()=>{
  drawNumline();
  drawCompare();
});

/* =============== 초기화 =============== */
renderNews();
</script>
</body>
</html>
"""


def render():
    st.subheader("📰 미니: 뉴스로 배우는 모비율 신뢰구간 — 실제 여론조사 해석")
    st.caption(
        "한국갤럽·농림축산식품부·통계청·문화체육관광부의 실제 조사 자료 4건으로 "
        "신문 기사 속 표본비율 p̂에서 모비율 p의 신뢰구간을 직접 단계별로 계산해 봅시다. "
        "기사 끝에 적힌 \"표본오차 ±△%P\"가 우리가 배운 k·√(p̂q̂/n) 과 어떻게 연결되는지 "
        "두 눈으로 확인할 수 있어요."
    )

    components.html(_HTML, height=2350, scrolling=True)

    st.divider()
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)
