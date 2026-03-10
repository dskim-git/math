import streamlit as st
import streamlit.components.v1 as components
import requests
from reflection_utils import render_reflection_form
import datetime

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "삼색기순열"

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
    "title": "미니: 삼색기와 같은 것이 있는 순열",
    "description": "파란·흰·빨간 3색으로 만드는 삼색기를 통해 같은 것이 있는 순열을 탐구합니다.",
    "order": 999999,
    "hidden": True,
}

def render():
    st.header("🏳️ 삼색기와 같은 것이 있는 순열")
    st.markdown("""
- 삼색기는 **3가지 색**을 3개의 칸에 하나씩 칠하거나, 일부 색이 반복될 때 만들어집니다.
- 아래 활동에서 삼색기를 직접 만들고 가능한 경우의 수를 탐구해 보세요.
""")

    components.html(r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/topojson-client@3/dist/topojson-client.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}],throwOnError:false})"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a0a1a 0%,#0d1b2a 50%,#0a0a1a 100%);min-height:100vh;padding:16px 16px 60px;color:#e2e8f0}
.card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:20px 24px;margin:12px 0;backdrop-filter:blur(10px)}
.card-title{font-size:15px;font-weight:700;color:#67e8f9;margin-bottom:14px;display:flex;align-items:center;gap:8px;letter-spacing:.02em}
h3{color:#f0f0f0;font-size:14px;margin-bottom:10px;}

/* ===================== MAP ===================== */
#map-wrap{width:100%;border-radius:14px;border:1px solid rgba(255,255,255,0.15);position:relative;overflow:hidden;background:#0d1b2a}
#map-svg{width:100%;height:auto;display:block}
#map-svg .land{fill:#1e3a5f;stroke:#2a5298;stroke-width:.3}
#map-svg .graticule{fill:none;stroke:rgba(255,255,255,.06);stroke-width:.2}
.map-pin{cursor:pointer;transition:.15s}
.map-pin circle{transition:.15s}
.map-pin:hover circle{r:7;opacity:1}
.map-tooltip{position:absolute;background:rgba(10,10,26,.95);border:1px solid rgba(255,255,255,.2);border-radius:10px;padding:8px 12px;font-size:12px;color:#e2e8f0;pointer-events:none;display:none;white-space:nowrap;z-index:30}
.map-legend{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.map-legend-item{display:flex;align-items:center;gap:6px;font-size:11px;color:#94a3b8;cursor:pointer;padding:4px 8px;border-radius:8px;border:1px solid rgba(255,255,255,.08);transition:.15s}
.map-legend-item:hover{background:rgba(255,255,255,.07);color:#e2e8f0}
.map-legend-item .dot-pin{width:12px;height:12px;border-radius:50%;border:2px solid #fff}

/* ===================== FLAGS LIST ===================== */
.flags-grid{display:flex;flex-wrap:wrap;gap:12px;padding:6px 0}
.flag-card{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:12px 10px;width:100px;min-width:90px;text-align:center;transition:.2s;cursor:default;flex-shrink:0}
.flag-card:hover{background:rgba(103,232,249,.08);border-color:rgba(103,232,249,.3);transform:translateY(-2px)}
.flag-card .flag-vis{display:flex;border-radius:6px;overflow:hidden;height:40px;margin:0 auto 8px;width:72px;box-shadow:0 2px 10px rgba(0,0,0,.5)}
.flag-card .flag-vis .stripe{flex:1}
.flag-card .country-name{font-size:11px;font-weight:600;color:#cbd5e1;line-height:1.4;word-break:keep-all}
.flag-card .perm-label{font-size:10px;color:#64748b;margin-top:3px}
.flag-card.horiz .flag-vis{flex-direction:column;width:60px;height:48px}

/* ===================== ACTIVITY ===================== */
.activity-desc{background:rgba(14,165,233,.08);border-left:3px solid #0ea5e9;border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:14px;font-size:13px;color:#cbd5e1;line-height:1.7}
.act-tabs{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap}
.act-tab{padding:8px 16px;border-radius:10px;border:1px solid rgba(255,255,255,.15);background:transparent;color:#94a3b8;font-size:13px;font-weight:600;cursor:pointer;transition:.2s}
.act-tab.active{background:linear-gradient(135deg,#0ea5e9,#06b6d4);color:#fff;border-color:transparent;box-shadow:0 4px 15px rgba(14,165,233,.4)}
.act-tab:hover:not(.active){background:rgba(255,255,255,.07);color:#e2e8f0}

/* --- Act 1: 순열 빌더 --- */
.flag-builder{display:flex;gap:6px;margin:14px 0;align-items:center;flex-wrap:wrap}
.builder-stripe{width:60px;height:80px;border-radius:8px;border:2px dashed rgba(255,255,255,.25);display:flex;align-items:center;justify-content:center;font-size:22px;cursor:pointer;transition:.2s;position:relative}
.builder-stripe.filled{border-style:solid;box-shadow:0 2px 12px rgba(0,0,0,.4)}
.builder-stripe:hover{transform:scale(1.06)}
.color-palette{display:flex;gap:8px;margin:10px 0;flex-wrap:wrap}
.pal-btn{width:40px;height:40px;border-radius:50%;border:3px solid rgba(255,255,255,.2);cursor:pointer;transition:.2s;position:relative}
.pal-btn:hover,.pal-btn.selected{border-color:#fff;transform:scale(1.15);box-shadow:0 0 15px rgba(255,255,255,.4)}
.pal-btn .col-label{position:absolute;bottom:-18px;left:50%;transform:translateX(-50%);font-size:10px;color:#94a3b8;white-space:nowrap;font-weight:600}
.reset-btn{background:rgba(239,68,68,.15);border:1px solid rgba(239,68,68,.4);color:#fca5a5;border-radius:10px;padding:8px 16px;cursor:pointer;font-weight:600;font-size:13px;transition:.2s}
.reset-btn:hover{background:rgba(239,68,68,.3)}
.result-box{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:14px;margin-top:10px;min-height:60px}
.result-tag{display:inline-flex;align-items:center;gap:4px;background:rgba(103,232,249,.12);border:1px solid rgba(103,232,249,.3);border-radius:8px;padding:4px 10px;margin:3px;font-size:12px;font-weight:600;color:#67e8f9}
.perms-found{font-size:13px;color:#94a3b8;margin-bottom:8px}

/* --- Act 2: 경우의 수 탐구 --- */
.explore-section{margin:10px 0}
.constraint-row{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin:10px 0}
.constraint-row label{font-size:13px;color:#94a3b8;font-weight:600}
.cnt-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(0,0,0,.3);border:1px solid rgba(255,255,255,.12);border-radius:10px;padding:6px 14px}
.cnt-btn{width:28px;height:28px;border-radius:8px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.07);color:#e2e8f0;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.1s;font-weight:700}
.cnt-btn:hover{background:rgba(255,255,255,.15)}
.cnt-num{font-size:18px;font-weight:800;min-width:24px;text-align:center;color:#e2e8f0}
.formula-box{background:rgba(14,165,233,.1);border:1px solid rgba(14,165,233,.25);border-radius:14px;padding:14px 20px;margin:14px 0;text-align:center}
.formula{font-size:28px;font-weight:800;color:#67e8f9;margin-bottom:4px}
.formula-sub{font-size:13px;color:#94a3b8}
.all-flags-grid{display:flex;flex-wrap:wrap;gap:8px;max-height:280px;overflow-y:auto;padding:8px}
.mini-flag-card{display:flex;gap:1px;border-radius:6px;overflow:hidden;height:34px;width:60px;cursor:default;box-shadow:0 1px 6px rgba(0,0,0,.5);transition:.15s;flex-shrink:0}
.mini-flag-card:hover{transform:scale(1.15);box-shadow:0 4px 14px rgba(0,0,0,.7)}
.mini-flag-card.horiz-flag{flex-direction:column;width:50px;height:40px}

/* --- Act 3: 동형 비교 --- */
.compare-grid{display:flex;flex-wrap:wrap;gap:14px}
.compare-group{flex:1;min-width:160px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:14px}
.compare-group h4{font-size:13px;font-weight:700;color:#67e8f9;margin-bottom:10px}
.formula-chip{background:rgba(103,232,249,.1);border:1px solid rgba(103,232,249,.25);border-radius:8px;padding:6px 12px;font-size:14px;font-weight:700;color:#67e8f9;text-align:center;margin-bottom:10px}

::-webkit-scrollbar{width:5px;height:5px}::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}::-webkit-scrollbar-thumb{background:rgba(14,165,233,.4);border-radius:3px}
</style>
</head>
<body>

<!-- ===== SECTION 1: MAP ===== -->
<div class="card">
  <div class="card-title">🗺️ 세계의 삼색기 국가</div>
  <div id="map-wrap" style="position:relative;min-height:320px;border-radius:14px;border:1px solid rgba(255,255,255,0.1);overflow:hidden">
    <svg id="map-svg" style="width:100%;display:block"></svg>
    <div class="map-tooltip" id="map-tooltip"></div>
    <div id="map-loading" style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#94a3b8;font-size:13px">🔄 지도 로딩 중...</div>
  </div>
  <div class="map-legend" id="map-legend"></div>
</div>

<!-- ===== SECTION 2: FLAG GALLERY ===== -->
<div class="card">
  <div class="card-title">🏳️ 국가별 삼색기 모음</div>
  <div style="display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap">
    <button class="act-tab active" id="tab-vert" onclick="setLayout('vert')">세로 줄무늬</button>
    <button class="act-tab" id="tab-horiz" onclick="setLayout('horiz')">가로 줄무늬</button>
    <button class="act-tab" id="tab-all" onclick="setLayout('all')">전체 보기</button>
  </div>
  <div class="flags-grid" id="flags-grid"></div>
</div>

<!-- ===== SECTION 3: ACTIVITY ===== -->
<div class="card">
  <div class="card-title">🎨 삼색기 경우의 수 탐구 활동</div>
  <div class="activity-desc">
    파란색(🔵), 흰색(⚪), 빨간색(🔴) 3가지 색을 각각 <strong>1개씩</strong> 사용하여<br>
    3칸짜리 삼색기를 만들 때 가능한 경우를 모두 탐구해 봅시다.
  </div>

  <div class="act-tabs">
    <button class="act-tab active" onclick="showAct(1,this)">활동 ① 직접 만들기</button>
    <button class="act-tab" onclick="showAct(2,this)">활동 ② 경우의 수 탐구</button>
    <button class="act-tab" onclick="showAct(3,this)">활동 ③ 흰색→빨간색으로 바꾸기</button>
  </div>

  <!-- ACT 1 -->
  <div id="act1">
    <div style="font-size:13px;color:#94a3b8;margin-bottom:10px">색을 선택한 후 아래 칸을 클릭해 칠해보세요.</div>
    <div class="color-palette" id="palette"></div>
    <div style="margin-top:16px;font-size:13px;color:#cbd5e1;font-weight:600;margin-bottom:8px">📐 삼색기 만들기</div>
    <div class="flag-builder" id="builder"></div>
    <button class="reset-btn" onclick="resetBuilder()">↺ 초기화</button>
    <div class="result-box" id="result-box">
      <div style="font-size:12px;color:#64748b">색을 칸에 모두 칠하면 결과가 표시됩니다</div>
    </div>
    <div style="margin-top:16px;font-size:13px;color:#67e8f9;font-weight:700;margin-bottom:8px">✅ 지금까지 만든 경우:</div>
    <div id="made-flags" style="display:flex;flex-wrap:wrap;gap:8px"></div>
    <div id="made-count" style="font-size:13px;color:#94a3b8;margin-top:8px"></div>
  </div>

  <!-- ACT 2 -->
  <div id="act2" style="display:none">
    <div class="activity-desc" style="margin-bottom:14px">
      각 색의 사용 개수를 바꾸며 <strong>같은 것이 있는 순열</strong> 공식을 확인해보세요.<br>
      공식: $\dfrac{n!}{p!\, q!\, r!}$ (전체 $n$개, 같은 것이 각각 $p$, $q$, $r$개)
    </div>
    <div class="constraint-row">
      <span style="font-size:13px;font-weight:700;color:#e2e8f0">파란색</span>
      <div class="cnt-badge">
        <button class="cnt-btn" onclick="changeCnt('b',-1)">−</button>
        <span class="cnt-num" id="cnt-b">1</span>
        <button class="cnt-btn" onclick="changeCnt('b',+1)">+</button>
      </div>
      <span style="font-size:13px;font-weight:700;color:#e2e8f0">흰색</span>
      <div class="cnt-badge">
        <button class="cnt-btn" onclick="changeCnt('w',-1)">−</button>
        <span class="cnt-num" id="cnt-w">1</span>
        <button class="cnt-btn" onclick="changeCnt('w',+1)">+</button>
      </div>
      <span style="font-size:13px;font-weight:700;color:#e2e8f0">빨간색</span>
      <div class="cnt-badge">
        <button class="cnt-btn" onclick="changeCnt('r',-1)">−</button>
        <span class="cnt-num" id="cnt-r">1</span>
        <button class="cnt-btn" onclick="changeCnt('r',+1)">+</button>
      </div>
    </div>
    <div class="formula-box" id="formula-box2">
      <div class="formula" id="formula2">...</div>
      <div class="formula-sub" id="formula-sub2">...</div>
    </div>
    <div style="font-size:13px;font-weight:700;color:#67e8f9;margin-bottom:6px">모든 경우 시각화:</div>
    <div class="all-flags-grid" id="all-flags-grid"></div>
  </div>

  <!-- ACT 3 -->
  <div id="act3" style="display:none">
    <div class="activity-desc">
      활동 ①에서 만든 <strong>6가지</strong> 삼색기(파·흰·빨 각 1개씩)에서<br>
      <strong>흰색 칸을 모두 빨간색으로 바꾸면</strong> 서로 다른 경우는 몇 가지일까요?<br>
      아래에서 직접 확인해 보세요. (파란·빨간·빨간 색 배열 → $\dfrac{3!}{2!} = 3$가지)
    </div>
    <div class="compare-grid">
      <div class="compare-group">
        <h4>변환 전: 파·흰·빨 각 1개 (6가지)</h4>
        <div class="formula-chip">3! = 6</div>
        <div id="before-flags" style="display:flex;flex-wrap:wrap;gap:8px"></div>
      </div>
      <div style="display:flex;flex-direction:column;justify-content:center;align-items:center;gap:8px;padding:0 4px;color:#94a3b8;font-size:18px">
        <div>⇒</div>
        <div style="font-size:11px;text-align:center;color:#64748b">흰색→<br>빨간색</div>
      </div>
      <div class="compare-group">
        <h4>변환 후: 파·빨·빨 (서로 다른 3가지)</h4>
        <div class="formula-chip">3!/2! = 3</div>
        <div id="after-flags" style="display:flex;flex-wrap:wrap;gap:8px"></div>
      </div>
    </div>
    <div class="formula-box" style="margin-top:16px">
      <div class="formula">$\dfrac{3!}{2!} = 3$가지</div>
      <div class="formula-sub">파란색 1개, 빨간색 2개를 나열: 같은 것이 있는 순열</div>
    </div>
  </div>
</div>

<script>
// ======================== DATA ========================
const COLORS = {
  b:  {hex:'#0047AB', name:'파란색',  short:'파'},
  w:  {hex:'#FFFFFF', name:'흰색',    short:'흰'},
  r:  {hex:'#CF142B', name:'빨간색',  short:'빨'},
  y:  {hex:'#FFCD00', name:'노란색',  short:'노'},
  g:  {hex:'#009A44', name:'초록색',  short:'초'},
  k:  {hex:'#000000', name:'검정색',  short:'검'},
  o:  {hex:'#FF8200', name:'주황색',  short:'주'},
  lb: {hex:'#00A3E0', name:'하늘색',  short:'하'},
};

// 순수 삼색기 목록 — 나무위키 「삼색기」 항목 기준, 문장·별·국장 없는 국기만 포함
// orientation: 'v'(세로 줄무늬) or 'h'(가로 줄무늬)  c:[]: 왼→오 또는 위→아래 색 순서
const FLAGS = [
  // ---세로 줄무늬---
  {name:'프랑스',      code:'fr', c:['b','w','r'],  o:'v', lat:46.2, lng:2.2},
  {name:'이탈리아',    code:'it', c:['g','w','r'],  o:'v', lat:41.9, lng:12.5},
  {name:'아일랜드',    code:'ie', c:['g','w','o'],  o:'v', lat:53.3, lng:-7.9},
  {name:'코트디부아르', code:'ci', c:['o','w','g'],  o:'v', lat:7.5,  lng:-5.5},
  {name:'벨기에',     code:'be', c:['k','y','r'],  o:'v', lat:50.8, lng:4.4},
  {name:'루마니아',    code:'ro', c:['b','y','r'],  o:'v', lat:44.4, lng:26.1},
  {name:'차드',       code:'td', c:['b','y','r'],  o:'v', lat:15.5, lng:18.6},
  {name:'말리',       code:'ml', c:['g','y','r'],  o:'v', lat:17.6, lng:-4.0},
  {name:'기니',       code:'gn', c:['r','y','g'],  o:'v', lat:11.0, lng:-10.9},
  // ---가로 줄무늬---
  {name:'독일',       code:'de', c:['k','r','y'],  o:'h', lat:51.2, lng:10.5},
  {name:'룩셈부르크',  code:'lu', c:['r','w','lb'], o:'h', lat:49.8, lng:6.1},
  {name:'네덜란드',    code:'nl', c:['r','w','b'],  o:'h', lat:52.1, lng:5.3},
  {name:'러시아',     code:'ru', c:['w','b','r'],  o:'h', lat:61.5, lng:90.0},
  {name:'헝가리',     code:'hu', c:['r','w','g'],  o:'h', lat:47.2, lng:19.5},
  {name:'불가리아',    code:'bg', c:['w','g','r'],  o:'h', lat:42.7, lng:25.5},
  {name:'리투아니아',  code:'lt', c:['y','g','r'],  o:'h', lat:55.2, lng:23.9},
  {name:'에스토니아',  code:'ee', c:['b','k','w'],  o:'h', lat:58.6, lng:25.0},
  {name:'아르메니아',  code:'am', c:['r','b','o'],  o:'h', lat:40.2, lng:44.5},
  {name:'예멘',       code:'ye', c:['r','w','k'],  o:'h', lat:15.6, lng:48.5},
  {name:'볼리비아',    code:'bo', c:['r','y','g'],  o:'h', lat:-16.5,lng:-64.0},
  {name:'콜롬비아',    code:'co', c:['y','b','r'],  o:'h', lat:4.6,  lng:-74.1},
  {name:'시에라리온',  code:'sl', c:['g','w','b'],  o:'h', lat:8.5,  lng:-11.8},
  {name:'가봉',       code:'ga', c:['g','y','b'],  o:'h', lat:-0.8, lng:11.6},
];

// ======================== MAP ========================
async function buildMap() {
  const wrap = document.getElementById('map-wrap');
  const tooltip = document.getElementById('map-tooltip');
  const loading = document.getElementById('map-loading');
  const w = wrap.clientWidth || 800;
  const h = Math.round(w * 0.5);

  const svgEl = document.getElementById('map-svg');
  svgEl.setAttribute('width', w);
  svgEl.setAttribute('height', h);

  const svg = d3.select('#map-svg');
  svg.append('rect').attr('width', w).attr('height', h).attr('fill', '#0a1832');

  const projection = d3.geoNaturalEarth1()
    .scale(w / 6.3)
    .translate([w / 2, h / 2]);
  const pathGen = d3.geoPath().projection(projection);

  // 거르교선
  svg.append('path')
    .datum(d3.geoGraticule()())
    .attr('fill', 'none')
    .attr('stroke', 'rgba(255,255,255,.07)')
    .attr('stroke-width', .3)
    .attr('d', pathGen);

  try {
    const world = await d3.json('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json');
    if (loading) loading.remove();

    svg.append('g')
      .selectAll('path')
      .data(topojson.feature(world, world.objects.countries).features)
      .join('path')
      .attr('fill', '#1e3a5f')
      .attr('stroke', '#2d5a9e')
      .attr('stroke-width', .3)
      .attr('d', pathGen);

    svg.append('path')
      .datum(topojson.mesh(world, world.objects.countries, (a, b) => a !== b))
      .attr('fill', 'none')
      .attr('stroke', '#3a6ba8')
      .attr('stroke-width', .2)
      .attr('d', pathGen);

    FLAGS.forEach(f => {
      const coords = projection([f.lng, f.lat]);
      if (!coords) return;
      const [cx, cy] = coords;
      if (cx < 0 || cx > w || cy < 0 || cy > h) return;

      const g = svg.append('g')
        .attr('class', 'map-pin')
        .attr('transform', `translate(${cx.toFixed(1)},${cy.toFixed(1)})`);

      g.append('circle')
        .attr('r', 5)
        .attr('fill', COLORS[f.c[0]].hex)
        .attr('stroke', '#fff')
        .attr('stroke-width', 1.5)
        .attr('opacity', .92)
        .style('cursor', 'pointer');

      g.on('mouseenter', function(event) {
        const [mx, my] = d3.pointer(event, wrap);
        const stripes = f.c.map(c =>
          `<span style="display:inline-block;width:13px;height:18px;background:${COLORS[c].hex};border-radius:3px;margin:0 1px;border:1px solid rgba(255,255,255,.2)"></span>`
        ).join('');
        tooltip.innerHTML = `
          <div style="display:flex;gap:2px;align-items:center;margin-bottom:5px">${stripes}</div>
          <div style="font-weight:700;font-size:13px">${f.name}</div>
          <div style="font-size:10px;color:#94a3b8;margin-top:2px">${f.c.map(c=>COLORS[c].short).join('·')} · ${f.o==='v'?'세로':'가로'} 줄무늬</div>
        `;
        let left = mx + 12;
        let top = my - 74;
        if (left + 175 > w) left = mx - 187;
        if (top < 4) top = my + 14;
        tooltip.style.left = left + 'px';
        tooltip.style.top = top + 'px';
        tooltip.style.display = 'block';
        d3.select(this).select('circle').attr('r', 8);
      })
      .on('mouseleave', function() {
        tooltip.style.display = 'none';
        d3.select(this).select('circle').attr('r', 5);
      });
    });
  } catch(e) {
    if (loading) loading.textContent = '❌ 지도 데이터를 불러오지 못했습니다.';
  }
}

// ======================== FLAGS GALLERY ========================
let currentLayout = 'vert';

function setLayout(mode) {
  currentLayout = mode;
  ['vert','horiz','all'].forEach(m => {
    document.getElementById('tab-'+m).classList.toggle('active', m===mode);
  });
  buildFlagsGrid();
}

function buildFlagsGrid() {
  const grid = document.getElementById('flags-grid');
  grid.innerHTML = '';
  const data = currentLayout === 'vert' ? FLAGS.filter(f=>f.o==='v')
             : currentLayout === 'horiz' ? FLAGS.filter(f=>f.o==='h')
             : FLAGS;

  data.forEach(f => {
    const card = document.createElement('div');
    card.className = 'flag-card';
    const perm = f.c.map(c=>COLORS[c].short).join('·');
    const orient = f.o === 'v' ? '세로' : '가로';
    card.innerHTML = `
      <img src="https://flagcdn.com/w80/${f.code}.png"
           style="width:70px;height:auto;border-radius:5px;display:block;margin:0 auto 8px;box-shadow:0 2px 8px rgba(0,0,0,.5)"
           alt="${f.name}" loading="lazy">
      <div class="country-name">${f.name}</div>
      <div class="perm-label">${perm} · ${orient}</div>
    `;
    grid.appendChild(card);
  });
}

// ======================== ACT 1: Builder ========================
const PALETTE_COLORS = ['b','w','r'];
let selectedColor = 'b';
let builderState = [null, null, null];
const madeSet = new Set();
const madeList = [];

function buildPalette() {
  const p = document.getElementById('palette');
  p.innerHTML = '';
  PALETTE_COLORS.forEach(c => {
    const btn = document.createElement('button');
    btn.className = 'pal-btn' + (c === selectedColor ? ' selected' : '');
    btn.style.background = COLORS[c].hex;
    btn.style.outline = (c === 'w') ? '1px solid rgba(255,255,255,.3)' : 'none';
    btn.id = 'pal-'+c;
    btn.innerHTML = `<span class="col-label">${COLORS[c].short}</span>`;
    btn.onclick = () => {
      selectedColor = c;
      document.querySelectorAll('.pal-btn').forEach(b=>b.classList.remove('selected'));
      btn.classList.add('selected');
    };
    p.appendChild(btn);
  });
}

function buildBuilderStripes() {
  const wrap = document.getElementById('builder');
  wrap.innerHTML = '';
  for (let i = 0; i < 3; i++) {
    const stripe = document.createElement('div');
    stripe.className = 'builder-stripe' + (builderState[i] ? ' filled' : '');
    if (builderState[i]) {
      stripe.style.background = COLORS[builderState[i]].hex;
      stripe.style.borderColor = COLORS[builderState[i]].hex;
      if (builderState[i] === 'w') stripe.style.borderColor = 'rgba(255,255,255,.5)';
      stripe.title = COLORS[builderState[i]].name;
      stripe.innerHTML = '';
    } else {
      stripe.innerHTML = '<span style="font-size:28px;color:rgba(255,255,255,.2)">' + (i+1) + '</span>';
    }
    stripe.onclick = () => {
      builderState[i] = selectedColor;
      buildBuilderStripes();
      checkBuilderResult();
    };
    wrap.appendChild(stripe);
  }
}

function checkBuilderResult() {
  if (builderState.includes(null)) {
    document.getElementById('result-box').innerHTML = '<div style="font-size:12px;color:#64748b">색을 칸에 모두 칠하면 결과가 표시됩니다</div>';
    return;
  }
  const key = builderState.join('-');
  const names = builderState.map(c=>COLORS[c].short).join('·');
  const colors = builderState.map(c=>COLORS[c].hex);

  const hasDup = new Set(builderState).size < builderState.length;
  const msgColor = hasDup ? '#f59e0b' : '#4ade80';
  const msg = hasDup ? '⚠️ 중복 색이 있는 경우' : '✅ 모두 다른 색 (3! = 6가지 중 하나)';

  document.getElementById('result-box').innerHTML = `
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
      <div style="display:flex;height:50px;width:90px;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.5)">
        ${builderState.map(c=>`<div style="flex:1;background:${COLORS[c].hex}"></div>`).join('')}
      </div>
      <div>
        <div style="font-size:14px;font-weight:700;color:#e2e8f0">${names}</div>
        <div style="font-size:12px;color:${msgColor};margin-top:3px">${msg}</div>
      </div>
    </div>
  `;

  // Add to made list (only unique, all-different)
  if (!hasDup && !madeSet.has(key)) {
    madeSet.add(key);
    madeList.push([...builderState]);
    updateMadeFlags();
  }
}

function updateMadeFlags() {
  const wrap = document.getElementById('made-flags');
  wrap.innerHTML = '';
  madeList.forEach(st => {
    const card = document.createElement('div');
    card.style.cssText = 'display:flex;flex-direction:column;align-items:center;gap:4px';
    const flag = document.createElement('div');
    flag.style.cssText = 'display:flex;height:44px;width:72px;border-radius:8px;overflow:hidden;box-shadow:0 2px 10px rgba(0,0,0,.5)';
    flag.innerHTML = st.map(c=>`<div style="flex:1;background:${COLORS[c].hex}"></div>`).join('');
    const lbl = document.createElement('div');
    lbl.style.cssText = 'font-size:10px;color:#94a3b8;font-weight:600';
    lbl.textContent = st.map(c=>COLORS[c].short).join('·');
    card.appendChild(flag);
    card.appendChild(lbl);
    wrap.appendChild(card);
  });
  const cnt = document.getElementById('made-count');
  const total = 6;
  cnt.textContent = `${madeList.length}/${total}가지 발견 (전체 3! = 6가지)`;
  if (madeList.length >= total) {
    cnt.innerHTML = `<span style="color:#4ade80;font-weight:700">🎉 모두 발견! 전체 3! = 6가지를 완성했습니다!</span>`;
  }
}

function resetBuilder() {
  builderState = [null, null, null];
  buildBuilderStripes();
  document.getElementById('result-box').innerHTML = '<div style="font-size:12px;color:#64748b">색을 칸에 모두 칠하면 결과가 표시됩니다</div>';
}

// ======================== ACT 2: Explore ========================
let cnts = {b:1, w:1, r:1};

function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n-1);
}

function changeCnt(col, delta) {
  cnts[col] = Math.max(0, Math.min(4, cnts[col] + delta));
  document.getElementById('cnt-'+col).textContent = cnts[col];
  updateAct2();
}

function permutations(arr) {
  if (arr.length <= 1) return [arr];
  const result = new Set();
  arr.forEach((el, i) => {
    const rest = arr.filter((_,j)=>j!==i);
    permutations(rest).forEach(p => {
      result.add([el,...p].join(','));
    });
  });
  return [...result].map(s=>s.split(','));
}

function updateAct2() {
  const b = cnts.b, w = cnts.w, r = cnts.r;
  const n = b + w + r;
  if (n === 0) {
    document.getElementById('formula2').textContent = '-';
    document.getElementById('formula-sub2').textContent = '개수를 1 이상으로 설정하세요.';
    document.getElementById('all-flags-grid').innerHTML = '';
    return;
  }

  const num = factorial(n);
  const den = factorial(b) * factorial(w) * factorial(r);
  const result = num / den;

  let denStr = '';
  if (b>1) denStr += `${factorial(b)}`;
  if (w>1) denStr += (denStr?'×':'')+`${factorial(w)}`;
  if (r>1) denStr += (denStr?'×':'')+`${factorial(r)}`;
  denStr = denStr || '1';

  const numStr = `${n}!` + (n<=6 ? ` = ${num}` : '');
  document.getElementById('formula2').textContent = `${n}! / (${factorial(b)}×${factorial(w)}×${factorial(r)}) = ${result}가지`;
  document.getElementById('formula-sub2').textContent =
    `파란색 ${b}개, 흰색 ${w}개, 빨간색 ${r}개 → 전체 ${n}개를 나열: ${result}가지`;

  // Generate all permutations
  const arr = [
    ...Array(b).fill('b'),
    ...Array(w).fill('w'),
    ...Array(r).fill('r')
  ];
  const perms = (result <= 120) ? permutations(arr) : [];

  const grid = document.getElementById('all-flags-grid');
  grid.innerHTML = '';
  if (result > 120) {
    grid.innerHTML = `<div style="font-size:12px;color:#64748b">경우의 수가 너무 많아 시각화를 생략합니다 (${result}가지)</div>`;
    return;
  }
  perms.forEach(perm => {
    const card = document.createElement('div');
    card.className = 'mini-flag-card';
    card.title = perm.map(c=>COLORS[c].short).join('·');
    perm.forEach(c => {
      const stripe = document.createElement('div');
      stripe.style.cssText = `flex:1;background:${COLORS[c].hex}`;
      card.appendChild(stripe);
    });
    grid.appendChild(card);
  });
}

// ======================== ACT 3: Transform ========================
function buildAct3() {
  const arr = ['b','w','r'];
  const allPerms = permutations(arr);

  // Before
  const before = document.getElementById('before-flags');
  before.innerHTML = '';
  allPerms.forEach(perm => {
    const wrap = document.createElement('div');
    wrap.style.cssText = 'display:flex;flex-direction:column;align-items:center;gap:3px';
    const flag = document.createElement('div');
    flag.style.cssText = 'display:flex;height:40px;width:66px;border-radius:7px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.5)';
    flag.innerHTML = perm.map(c=>`<div style="flex:1;background:${COLORS[c].hex}"></div>`).join('');
    const lbl = document.createElement('div');
    lbl.style.cssText = 'font-size:10px;color:#94a3b8';
    lbl.textContent = perm.map(c=>COLORS[c].short).join('·');
    wrap.appendChild(flag);
    wrap.appendChild(lbl);
    before.appendChild(wrap);
  });

  // After: replace 'w' with 'r'
  const afterSeen = new Set();
  const afterPerms = [];
  allPerms.forEach(perm => {
    const transformed = perm.map(c => c === 'w' ? 'r' : c);
    const key = transformed.join('-');
    if (!afterSeen.has(key)) {
      afterSeen.add(key);
      afterPerms.push(transformed);
    }
  });

  const after = document.getElementById('after-flags');
  after.innerHTML = '';
  afterPerms.forEach(perm => {
    const wrap = document.createElement('div');
    wrap.style.cssText = 'display:flex;flex-direction:column;align-items:center;gap:3px';
    const flag = document.createElement('div');
    flag.style.cssText = 'display:flex;height:40px;width:66px;border-radius:7px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.5)';
    flag.innerHTML = perm.map(c=>`<div style="flex:1;background:${COLORS[c].hex}"></div>`).join('');
    const lbl = document.createElement('div');
    lbl.style.cssText = 'font-size:10px;color:#94a3b8';
    lbl.textContent = perm.map(c=>COLORS[c].short).join('·');
    wrap.appendChild(flag);
    wrap.appendChild(lbl);
    after.appendChild(wrap);
  });
}

// ======================== TAB SWITCH ========================
function showAct(n, btn) {
  [1,2,3].forEach(i => {
    document.getElementById('act'+i).style.display = i===n ? '' : 'none';
  });
  document.querySelectorAll('.act-tab').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  if (n === 2) updateAct2();
  if (n === 3) buildAct3();
}

// ======================== INIT ========================
buildMap();
buildFlagsGrid();
buildPalette();
buildBuilderStripes();
</script>
</body>
</html>
""", height=1950, scrolling=True)

    _render_quiz(_SHEET_NAME)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


def _render_quiz(sheet_name: str):
    st.divider()
    st.subheader("🧩 확인 문제")
    st.caption("활동을 바탕으로 아래 문제를 풀어보세요. 답을 입력하고 **채점하기** 버튼을 눌러주세요.")

    QUIZ = [
        {
            "q": "파란색, 흰색, 빨간색을 각각 1개씩 사용하여 3칸짜리 가로 줄무늬 삼색기를 만들 때, 서로 다른 경우는 몇 가지인지 구하시오.",
            "a": "6",
            "hint": "3가지 서로 다른 색을 일렬로 나열하는 순열입니다.",
            "sol": "3가지 서로 다른 색을 나열하는 경우의 수 → $3! = 6$가지입니다."
        },
        {
            "q": "파란색 1개, 빨간색 2개를 사용하여 3칸짜리 삼색기를 만들 때, 서로 다른 경우는 몇 가지인지 구하시오.",
            "a": "3",
            "hint": "같은 것이 있는 순열 공식 $\\dfrac{n!}{p!\\,q!}$를 사용하세요.",
            "sol": "$\\dfrac{3!}{1!\\cdot 2!} = \\dfrac{6}{2} = 3$가지\n\n(파·빨·빨, 빨·파·빨, 빨·빨·파)"
        },
        {
            "q": "파란색 1개, 흰색 2개, 빨간색 1개를 모두 사용하여 4칸짜리 가로 줄무늬 국기를 만들 때, 서로 다른 경우는 모두 몇 가지인지 구하시오.",
            "a": "12",
            "hint": "전체 4개, 흰색이 2개 같으므로 $\\dfrac{4!}{1!\\cdot 2!\\cdot 1!}$를 계산하세요.",
            "sol": "$\\dfrac{4!}{1!\\cdot 2!\\cdot 1!} = \\dfrac{24}{2} = 12$가지"
        },
    ]

    for i, item in enumerate(QUIZ):
        with st.container():
            st.markdown(f"**문제 {i+1}.** {item['q']}")
            col1, col2 = st.columns([3, 1])
            with col1:
                user_ans = st.text_input(
                    f"답 입력 (문제 {i+1})",
                    key=f"flag_q{i+1}",
                    label_visibility="collapsed",
                    placeholder="답을 입력하세요"
                )
            with col2:
                check = st.button("채점하기", key=f"flag_check{i+1}", use_container_width=True)

            if check and user_ans.strip():
                user_stripped = user_ans.strip().replace(',', '').replace(' ', '')
                correct_stripped = str(item['a']).replace(',', '').replace(' ', '')
                is_correct = user_stripped == correct_stripped
                if is_correct:
                    st.success("✅ 정답입니다!")
                else:
                    st.error(f"❌ 틀렸습니다. 정답은 **{item['a']}** 입니다.")
                with st.expander("💡 풀이 보기"):
                    st.markdown(item['sol'])
            elif check and not user_ans.strip():
                st.warning("답을 입력해주세요.")
        st.markdown("---")
