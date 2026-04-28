import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "미니: 세상의 확률분포 한눈에 보기",
    "description": "이산·연속 확률분포의 이름과 실생활 예시를 카드로 탐색합니다.",
    "order": 999,
    "hidden": True,
}

_HTML = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a1628 0%,#0f2027 50%,#0a1628 100%);min-height:100vh;padding:20px;color:#e2e8f0}

.page-title{text-align:center;margin-bottom:6px}
.page-title h1{font-size:22px;font-weight:800;color:#fff;letter-spacing:-.01em}
.page-title p{font-size:13px;color:#94a3b8;margin-top:6px;line-height:1.6}

.highlight-box{background:linear-gradient(135deg,rgba(99,102,241,.15),rgba(168,85,247,.1));border:1px solid rgba(99,102,241,.3);border-radius:16px;padding:14px 20px;margin:14px 0;text-align:center}
.highlight-box span{font-size:13px;color:#a5b4fc;line-height:1.7}
.highlight-box strong{color:#818cf8}

.tabs{display:flex;gap:10px;margin:18px 0 16px;justify-content:center}
.tab-btn{padding:10px 28px;border-radius:12px;border:1.5px solid rgba(255,255,255,.12);background:rgba(255,255,255,.04);cursor:pointer;font-size:14px;font-weight:700;color:#94a3b8;transition:all .25s;letter-spacing:.01em}
.tab-btn:hover{background:rgba(255,255,255,.08)}
.tab-btn.active.discrete{background:linear-gradient(135deg,rgba(245,158,11,.25),rgba(234,88,12,.15));color:#fbbf24;border-color:rgba(245,158,11,.5);box-shadow:0 0 20px rgba(245,158,11,.2)}
.tab-btn.active.continuous{background:linear-gradient(135deg,rgba(16,185,129,.25),rgba(6,182,212,.15));color:#34d399;border-color:rgba(16,185,129,.5);box-shadow:0 0 20px rgba(16,185,129,.2)}

.section-label{font-size:12px;color:#64748b;font-weight:600;letter-spacing:.08em;text-transform:uppercase;margin-bottom:12px;text-align:center}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}

.card{border-radius:18px;border:1.5px solid rgba(255,255,255,.08);background:rgba(255,255,255,.04);padding:0;cursor:pointer;transition:all .28s;overflow:hidden;position:relative}
.card:hover{transform:translateY(-4px);box-shadow:0 12px 36px rgba(0,0,0,.4)}
.card.open{border-color:rgba(255,255,255,.2)}

.card-header{padding:16px 18px 14px;display:flex;align-items:flex-start;gap:10px}
.card-icon{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0}
.card-header-text{flex:1;min-width:0}
.card-name{font-size:15px;font-weight:800;color:#f1f5f9;line-height:1.2;margin-bottom:4px}
.card-name-en{font-size:11px;color:#64748b;font-weight:500}
.badge-row{display:flex;gap:5px;margin-top:6px;flex-wrap:wrap}
.badge{display:inline-block;font-size:10px;font-weight:700;padding:2px 8px;border-radius:6px;letter-spacing:.03em}
.badge-textbook{background:rgba(245,158,11,.2);color:#fbbf24;border:1px solid rgba(245,158,11,.35)}
.badge-discrete{background:rgba(245,158,11,.1);color:#f59e0b;border:1px solid rgba(245,158,11,.2)}
.badge-continuous{background:rgba(16,185,129,.1);color:#34d399;border:1px solid rgba(16,185,129,.2)}
.badge-standard{background:rgba(99,102,241,.2);color:#a5b4fc;border:1px solid rgba(99,102,241,.35)}

.chevron{position:absolute;top:18px;right:16px;font-size:14px;color:#475569;transition:transform .25s}
.card.open .chevron{transform:rotate(180deg)}

.card-body{max-height:0;overflow:hidden;transition:max-height .35s ease,padding .25s}
.card.open .card-body{max-height:300px}

.card-content{padding:0 18px 16px}
.desc{font-size:12.5px;color:#cbd5e1;line-height:1.65;margin-bottom:12px;padding:10px 12px;background:rgba(255,255,255,.03);border-radius:10px;border-left:3px solid}
.examples-title{font-size:11px;color:#64748b;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:8px}
.example-item{display:flex;align-items:flex-start;gap:7px;margin-bottom:7px}
.ex-num{min-width:20px;height:20px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:800;flex-shrink:0}
.ex-text{font-size:12.5px;color:#94a3b8;line-height:1.55}

.tab-panel{display:none}
.tab-panel.active{display:block}

::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:rgba(0,0,0,.2);border-radius:3px}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.15);border-radius:3px}
</style>
</head>
<body>

<div class="page-title">
  <h1>🌐 세상의 확률분포 한눈에 보기</h1>
  <p>수학자들이 발견한 다양한 확률분포를 만나보세요.<br>카드를 클릭하면 상세 설명과 실생활 예시를 볼 수 있어요.</p>
</div>

<div class="highlight-box">
  <span>우리가 배우는 확률분포는 전체 중 극히 일부예요. 고등학교에서는 이 중<br>
  <strong>이항분포</strong>와 <strong>정규분포(표준정규분포 포함)</strong>를 집중적으로 다룹니다. ⭐</span>
</div>

<div class="tabs">
  <button class="tab-btn active discrete" onclick="switchTab('discrete')">⚂ 이산확률분포 (8종)</button>
  <button class="tab-btn continuous" onclick="switchTab('continuous')">〰 연속확률분포 (9종)</button>
</div>

<!-- 이산확률분포 -->
<div id="panel-discrete" class="tab-panel active">
  <div class="section-label">이산확률변수 — 셀 수 있는 값을 갖는 확률분포</div>
  <div class="grid" id="grid-discrete"></div>
</div>

<!-- 연속확률분포 -->
<div id="panel-continuous" class="tab-panel">
  <div class="section-label">연속확률변수 — 구간 내 어떤 값도 가질 수 있는 확률분포</div>
  <div class="grid" id="grid-continuous"></div>
</div>

<script>
const DISCRETE = [
  {
    icon: "🎯",
    name: "베르누이분포",
    nameEn: "Bernoulli Distribution",
    badges: ["이산"],
    color: "#f59e0b",
    borderColor: "rgba(245,158,11,.4)",
    iconBg: "rgba(245,158,11,.15)",
    numBg: "rgba(245,158,11,.25)",
    numColor: "#fbbf24",
    desc: "성공 또는 실패, 딱 두 가지 결과만 있는 단 한 번의 시행에서 '성공 횟수'의 확률분포입니다.",
    examples: [
      "동전을 한 번 던져 앞면이 나오는지 여부",
      "자유투 한 번에서 성공할지 실패할지"
    ]
  },
  {
    icon: "📊",
    name: "이항분포",
    nameEn: "Binomial Distribution",
    badges: ["이산", "교과서 ⭐"],
    isTextbook: true,
    color: "#f59e0b",
    borderColor: "rgba(245,158,11,.6)",
    iconBg: "rgba(245,158,11,.2)",
    numBg: "rgba(245,158,11,.3)",
    numColor: "#fbbf24",
    desc: "독립적인 베르누이 시행을 n번 반복했을 때, 성공 횟수의 확률분포입니다. 이항분포의 핵심!",
    examples: [
      "동전을 10번 던졌을 때 앞면이 나오는 횟수",
      "시험 20문항을 모두 찍었을 때 맞히는 문항 수"
    ]
  },
  {
    icon: "🎲",
    name: "다항분포",
    nameEn: "Multinomial Distribution",
    badges: ["이산"],
    color: "#f97316",
    borderColor: "rgba(249,115,22,.4)",
    iconBg: "rgba(249,115,22,.15)",
    numBg: "rgba(249,115,22,.25)",
    numColor: "#fb923c",
    desc: "결과가 3가지 이상인 시행을 n번 반복했을 때, 각 결과가 나오는 횟수의 확률분포입니다. 이항분포를 여러 결과로 확장한 것!",
    examples: [
      "주사위를 30번 던졌을 때 각 눈(1~6)이 나오는 횟수",
      "설문에서 '매우좋음/좋음/보통/나쁨/매우나쁨' 응답 분포"
    ]
  },
  {
    icon: "⚖️",
    name: "이산균등분포",
    nameEn: "Discrete Uniform Distribution",
    badges: ["이산"],
    color: "#eab308",
    borderColor: "rgba(234,179,8,.4)",
    iconBg: "rgba(234,179,8,.15)",
    numBg: "rgba(234,179,8,.25)",
    numColor: "#facc15",
    desc: "유한한 값들이 모두 똑같은 확률을 가지는 가장 단순한 이산확률분포입니다.",
    examples: [
      "주사위를 한 번 던져 나오는 수 (1~6이 모두 1/6 확률)",
      "1부터 45까지 중 로또 번호 하나를 뽑을 때"
    ]
  },
  {
    icon: "⚡",
    name: "포아송분포",
    nameEn: "Poisson Distribution",
    badges: ["이산"],
    color: "#d97706",
    borderColor: "rgba(217,119,6,.4)",
    iconBg: "rgba(217,119,6,.15)",
    numBg: "rgba(217,119,6,.25)",
    numColor: "#fbbf24",
    desc: "일정한 시간이나 공간 안에서 드물게 발생하는 사건의 횟수를 나타내는 확률분포입니다.",
    examples: [
      "하루 동안 특정 교차로에서 발생하는 교통사고 건수",
      "1시간 동안 병원 응급실에 방문하는 환자 수"
    ]
  },
  {
    icon: "🔁",
    name: "기하분포",
    nameEn: "Geometric Distribution",
    badges: ["이산"],
    color: "#b45309",
    borderColor: "rgba(180,83,9,.4)",
    iconBg: "rgba(180,83,9,.15)",
    numBg: "rgba(180,83,9,.25)",
    numColor: "#d97706",
    desc: "처음으로 성공할 때까지 시행해야 하는 횟수의 확률분포입니다. '몇 번 만에 처음 성공할까?'",
    examples: [
      "자유투를 처음으로 성공할 때까지 시도한 횟수",
      "불량품이 처음 발생할 때까지 생산한 제품 수"
    ]
  },
  {
    icon: "🔢",
    name: "음이항분포",
    nameEn: "Negative Binomial Distribution",
    badges: ["이산"],
    color: "#92400e",
    borderColor: "rgba(146,64,14,.4)",
    iconBg: "rgba(146,64,14,.15)",
    numBg: "rgba(146,64,14,.25)",
    numColor: "#b45309",
    desc: "r번째 성공이 일어날 때까지 시행해야 하는 총 횟수의 확률분포입니다. 기하분포를 r번으로 확장!",
    examples: [
      "야구에서 3번째 아웃을 잡을 때까지의 타석 수",
      "불량품이 5번째로 나올 때까지 검사한 제품 수"
    ]
  },
  {
    icon: "🃏",
    name: "초기하분포",
    nameEn: "Hypergeometric Distribution",
    badges: ["이산"],
    color: "#78350f",
    borderColor: "rgba(120,53,15,.4)",
    iconBg: "rgba(120,53,15,.15)",
    numBg: "rgba(120,53,15,.25)",
    numColor: "#92400e",
    desc: "비복원추출에서 N개 중 n개를 뽑았을 때, 원하는 것이 k개 뽑힐 확률을 나타내는 확률분포입니다.",
    examples: [
      "30명의 학생 중 12명이 여학생일 때, 5명을 무작위로 선발했을 때의 여학생 수",
      "52장의 카드 중 5장을 뽑았을 때 스페이드가 나오는 장 수"
    ]
  }
];

const CONTINUOUS = [
  {
    icon: "📏",
    name: "균등분포",
    nameEn: "Continuous Uniform Distribution",
    badges: ["연속"],
    color: "#10b981",
    borderColor: "rgba(16,185,129,.4)",
    iconBg: "rgba(16,185,129,.15)",
    numBg: "rgba(16,185,129,.25)",
    numColor: "#34d399",
    desc: "정해진 구간 안의 모든 값이 동일한 확률로 나타나는 가장 단순한 연속확률분포입니다.",
    examples: [
      "버스가 0~10분 사이에 도착할 때, 정확히 몇 분에 도착할지",
      "원판을 돌려 멈추는 각도(0°~360°)"
    ]
  },
  {
    icon: "🔔",
    name: "정규분포",
    nameEn: "Normal Distribution",
    badges: ["연속", "교과서 ⭐"],
    isTextbook: true,
    color: "#10b981",
    borderColor: "rgba(16,185,129,.6)",
    iconBg: "rgba(16,185,129,.2)",
    numBg: "rgba(16,185,129,.3)",
    numColor: "#34d399",
    desc: "평균을 중심으로 좌우 대칭인 종 모양의 연속확률분포입니다. 자연과 사회 현상에서 가장 자주 나타납니다.",
    examples: [
      "같은 학년 학생들의 키 분포",
      "공장에서 생산된 과자의 무게 분포"
    ]
  },
  {
    icon: "⭐",
    name: "표준정규분포",
    nameEn: "Standard Normal Distribution",
    badges: ["연속", "교과서 ⭐"],
    isTextbook: true,
    color: "#059669",
    borderColor: "rgba(5,150,105,.6)",
    iconBg: "rgba(5,150,105,.2)",
    numBg: "rgba(5,150,105,.3)",
    numColor: "#6ee7b7",
    desc: "평균이 0, 표준편차가 1인 특별한 정규분포입니다. 모든 정규분포는 이것으로 변환해 확률을 구합니다.",
    examples: [
      "Z점수(표준점수)로 변환된 수능 원점수",
      "정규분포를 따르는 어떤 데이터든 표준화하면 이 분포가 됨"
    ]
  },
  {
    icon: "⏱️",
    name: "지수분포",
    nameEn: "Exponential Distribution",
    badges: ["연속"],
    color: "#06b6d4",
    borderColor: "rgba(6,182,212,.4)",
    iconBg: "rgba(6,182,212,.15)",
    numBg: "rgba(6,182,212,.25)",
    numColor: "#67e8f9",
    desc: "다음 사건이 발생하기까지 기다려야 하는 시간의 확률분포입니다. 포아송분포의 '쌍둥이'!",
    examples: [
      "기계가 고장난 후 다음 고장까지의 시간",
      "버스 정류장에서 다음 버스를 기다리는 시간"
    ]
  },
  {
    icon: "🎯",
    name: "베타분포",
    nameEn: "Beta Distribution",
    badges: ["연속"],
    color: "#8b5cf6",
    borderColor: "rgba(139,92,246,.4)",
    iconBg: "rgba(139,92,246,.15)",
    numBg: "rgba(139,92,246,.25)",
    numColor: "#c4b5fd",
    desc: "0과 1 사이의 비율이나 확률 그 자체를 모델링하는 확률분포입니다.",
    examples: [
      "야구 선수의 타율(성공 비율) 추정",
      "어떤 광고 클릭률이 얼마나 될지 불확실성 표현"
    ]
  },
  {
    icon: "⏳",
    name: "감마분포",
    nameEn: "Gamma Distribution",
    badges: ["연속"],
    color: "#7c3aed",
    borderColor: "rgba(124,58,237,.4)",
    iconBg: "rgba(124,58,237,.15)",
    numBg: "rgba(124,58,237,.25)",
    numColor: "#a78bfa",
    desc: "r번째 사건이 발생하기까지의 대기 시간의 확률분포입니다. 지수분포를 r번으로 확장한 것!",
    examples: [
      "3번째 고객이 도착할 때까지의 시간",
      "보험 청구 금액의 분포 모델링"
    ]
  },
  {
    icon: "🔬",
    name: "카이제곱분포",
    nameEn: "Chi-squared Distribution",
    badges: ["연속"],
    color: "#db2777",
    borderColor: "rgba(219,39,119,.4)",
    iconBg: "rgba(219,39,119,.15)",
    numBg: "rgba(219,39,119,.25)",
    numColor: "#f9a8d4",
    desc: "표준정규분포를 따르는 값들을 제곱해서 합산한 확률분포입니다. 통계 검정에서 자주 쓰입니다.",
    examples: [
      "설문조사에서 관찰 빈도와 기대 빈도 차이 검정(χ² 검정)",
      "두 범주형 변수 사이의 연관성 검정"
    ]
  },
  {
    icon: "🧪",
    name: "스튜던트 t분포",
    nameEn: "Student's t-Distribution",
    badges: ["연속"],
    color: "#0891b2",
    borderColor: "rgba(8,145,178,.4)",
    iconBg: "rgba(8,145,178,.15)",
    numBg: "rgba(8,145,178,.25)",
    numColor: "#67e8f9",
    desc: "표본의 크기가 작을 때 모평균을 추정하는 데 쓰이는 확률분포입니다. 샘플 수가 많아질수록 정규분포에 가까워집니다.",
    examples: [
      "소수의 실험 참가자로 신약 효과 검증",
      "두 학급의 시험 평균 점수 차이를 소규모 표본으로 비교"
    ]
  },
  {
    icon: "📐",
    name: "F분포",
    nameEn: "F Distribution",
    badges: ["연속"],
    color: "#0e7490",
    borderColor: "rgba(14,116,144,.4)",
    iconBg: "rgba(14,116,144,.15)",
    numBg: "rgba(14,116,144,.25)",
    numColor: "#22d3ee",
    desc: "두 집단의 분산을 비교할 때 사용하는 확률분포입니다. 세 집단 이상의 평균 차이를 한꺼번에 검정할 때도 씁니다.",
    examples: [
      "두 공장 제품의 무게 변동성(균일성) 비교",
      "세 반 이상의 수학 점수 평균 차이 분석(분산분석, ANOVA)"
    ]
  }
];

function makeCard(dist, type) {
  const div = document.createElement('div');
  div.className = 'card';
  div.style.setProperty('--card-color', dist.color);

  const badgesHtml = dist.badges.map(b => {
    if (b.includes('교과서')) return `<span class="badge badge-textbook">${b}</span>`;
    if (b === '이산') return `<span class="badge badge-discrete">${b}</span>`;
    return `<span class="badge badge-continuous">${b}</span>`;
  }).join('');

  const examplesHtml = dist.examples.map((ex, i) => `
    <div class="example-item">
      <div class="ex-num" style="background:${dist.numBg};color:${dist.numColor}">${i+1}</div>
      <div class="ex-text">${ex}</div>
    </div>
  `).join('');

  div.innerHTML = `
    <div class="card-header">
      <div class="card-icon" style="background:${dist.iconBg}">${dist.icon}</div>
      <div class="card-header-text">
        <div class="card-name">${dist.name}</div>
        <div class="card-name-en">${dist.nameEn}</div>
        <div class="badge-row">${badgesHtml}</div>
      </div>
    </div>
    <div class="chevron">▼</div>
    <div class="card-body">
      <div class="card-content">
        <div class="desc" style="border-left-color:${dist.borderColor}">${dist.desc}</div>
        <div class="examples-title">📌 실생활 예시</div>
        ${examplesHtml}
      </div>
    </div>
  `;

  if (dist.isTextbook) {
    div.style.borderColor = dist.borderColor;
    div.style.boxShadow = `0 0 16px rgba(${dist.isTextbook && type === 'continuous' ? '16,185,129' : '245,158,11'},.18)`;
  }

  div.addEventListener('click', () => {
    div.classList.toggle('open');
  });

  return div;
}

function buildGrids() {
  const gD = document.getElementById('grid-discrete');
  DISCRETE.forEach(d => gD.appendChild(makeCard(d, 'discrete')));
  const gC = document.getElementById('grid-continuous');
  CONTINUOUS.forEach(d => gC.appendChild(makeCard(d, 'continuous')));
}

function switchTab(type) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.getElementById('panel-' + type).classList.add('active');
  const btn = document.querySelector(`.tab-btn.${type}`);
  btn.classList.add('active');
}

buildGrids();
</script>
</body>
</html>
"""


def render():
    st.header("🌐 세상의 확률분포 한눈에 보기")
    st.caption("수학자들이 발견한 다양한 확률분포를 카드로 탐색해 보세요. 카드를 클릭하면 설명과 예시가 펼쳐집니다.")
    components.html(_HTML, height=1200, scrolling=True)
