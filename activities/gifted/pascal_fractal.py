import streamlit as st
import streamlit.components.v1 as components

META = {
    "title":       "미니: 파스칼 삼각형에서 찾아보는 프랙털",
    "description": "이항계수를 mod m로 색칠하여 시에르핀스키 삼각형 등 프랙털 패턴을 탐구합니다.",
    "order":       26,
    "hidden":      True,
}

# ──────────────────────────────────────────────
# 퀴즈 데이터
# ──────────────────────────────────────────────
_QUIZ = [
    {
        "q": "파스칼 삼각형의 각 원소를 **mod 2** (2로 나눈 나머지)로 색칠할 때 나타나는 프랙털 도형은?",
        "choices": ["코흐 눈송이", "망델브로트 집합", "시에르핀스키 삼각형", "칸토어 집합"],
        "answer": 2,
        "explain": "mod 2로 색칠하면 홀수 위치가 3등분 삼각형 구조로 반복되며 **시에르핀스키 삼각형**이 나타납니다.",
    },
    {
        "q": "mod 3으로 색칠할 때 관찰되는 패턴은?",
        "choices": [
            "완전히 랜덤한 점들",
            "세 개의 자기유사 삼각형이 반복되는 카펫 패턴",
            "직선 줄무늬",
            "원 모양의 패턴",
        ],
        "answer": 1,
        "explain": "mod 3에서는 **시에르핀스키 삼각형이 3색**으로 나뉩니다. 각 수준마다 self-similar한 삼각형 구조가 세 배씩 분기됩니다.",
    },
    {
        "q": "프랙털(fractal)의 핵심 특성은?",
        "choices": [
            "단순한 직선 구조",
            "확대할수록 형태가 사라짐",
            "자기 유사성(self-similarity): 일부를 확대하면 전체와 닮은 패턴이 반복됨",
            "오직 컴퓨터로만 만들 수 있는 형태",
        ],
        "answer": 2,
        "explain": "프랙털의 핵심은 **자기 유사성(self-similarity)**입니다. 화면을 확대해도 비슷한 패턴이 반복되는 구조를 가집니다. 파스칼 삼각형의 mod 색칠 패턴이 바로 이 성질을 가집니다.",
    },
]

# ──────────────────────────────────────────────
# p5.js HTML
# ──────────────────────────────────────────────
_CANVAS_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:linear-gradient(135deg,#0a1628 0%,#0f2027 50%,#0a1628 100%);
    min-height:100vh;font-family:'Segoe UI',system-ui,sans-serif;color:#e2e8f0;}
  .wrap{padding:16px;display:flex;flex-direction:column;gap:14px}
  .card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);
    border-radius:20px;padding:18px 22px;backdrop-filter:blur(10px)}
  .card-title{font-size:14px;font-weight:700;color:#fbbf24;margin-bottom:14px;
    display:flex;align-items:center;gap:8px;letter-spacing:.02em}
  .ctrl-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
  .ctrl label{font-size:11px;color:#94a3b8;font-weight:600;letter-spacing:.04em;
    text-transform:uppercase;display:block;margin-bottom:6px}
  .ctrl input[type=range]{width:100%;-webkit-appearance:none;height:6px;border-radius:3px;
    background:linear-gradient(90deg,#f59e0b,#ef4444);outline:none;display:block}
  .ctrl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;
    border-radius:50%;background:#fff;border:3px solid #f59e0b;cursor:pointer;
    box-shadow:0 0 10px rgba(245,158,11,.6)}
  .val{display:inline-block;min-width:34px;background:linear-gradient(135deg,#f59e0b,#ef4444);
    border-radius:10px;padding:3px 10px;font-weight:800;font-size:16px;text-align:center;
    color:#fff;box-shadow:0 2px 10px rgba(245,158,11,.4)}
  .preset-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
  .preset-btn{padding:6px 14px;border-radius:10px;border:1px solid rgba(255,255,255,.15);
    background:rgba(255,255,255,.05);cursor:pointer;font-size:12px;font-weight:600;
    color:#94a3b8;transition:.2s}
  .preset-btn:hover,.preset-btn.active{background:rgba(245,158,11,.2);color:#fbbf24;
    border-color:rgba(245,158,11,.4)}
  .info-row{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px}
  .kpi{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
    border-radius:14px;padding:10px 20px;text-align:center;flex:1;min-width:100px}
  .kpi .num{font-size:28px;font-weight:900;color:#e2e8f0}
  .kpi .lbl{font-size:10px;color:#94a3b8;margin-top:3px;font-weight:600;
    letter-spacing:.04em;text-transform:uppercase}
  #canvas-wrap{border-radius:16px;overflow:hidden;box-shadow:0 4px 30px rgba(0,0,0,.4)}
  canvas{display:block}
  .obs-box{background:rgba(99,102,241,.08);border:1px solid rgba(99,102,241,.25);
    border-radius:14px;padding:14px 18px;font-size:13px;line-height:1.7;color:#c7d2fe}
  .obs-box b{color:#a5b4fc}
  ::-webkit-scrollbar{width:5px}
  ::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
  ::-webkit-scrollbar-thumb{background:rgba(245,158,11,.4);border-radius:3px}
  .custom-select{position:relative;width:100%}
  .selected-option{background:rgba(255,255,255,.06);color:#e2e8f0;border:1px solid rgba(255,255,255,.15);
    border-radius:8px;padding:7px 12px;font-size:13px;cursor:pointer;display:flex;
    justify-content:space-between;align-items:center;user-select:none;transition:.2s}
  .selected-option:hover{background:rgba(255,255,255,.1);border-color:rgba(255,255,255,.3)}
  .options-list{display:none;position:absolute;top:calc(100% + 4px);left:0;right:0;z-index:200;
    background:#1a2740;border:1px solid rgba(255,255,255,.15);border-radius:8px;
    overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,.6)}
  .option{padding:9px 14px;font-size:13px;color:#e2e8f0;cursor:pointer;transition:.2s}
  .option:hover{background:rgba(245,158,11,.18);color:#fbbf24}
  .option.active{background:rgba(245,158,11,.12);color:#fbbf24;font-weight:700}
  .arrow{font-size:10px;transition:transform .2s;color:#94a3b8}
  .custom-select.open .arrow{transform:rotate(180deg)}
</style>
</head>
<body>
<div class="wrap">

  <!-- 컨트롤 카드 -->
  <div class="card">
    <div class="card-title">⚙️ 설정</div>
    <div class="ctrl-grid">
      <div class="ctrl">
        <label>🎯 modulo m = <span id="modVal" class="val">2</span></label>
        <input type="range" id="modRange" min="2" max="12" value="2">
      </div>
      <div class="ctrl">
        <label>🎨 나머지 r = <span id="remVal" class="val">0</span></label>
        <input type="range" id="remRange" min="0" max="1" value="0">
      </div>
      <div class="ctrl">
        <label>🔍 확대 배율 = <span id="scaleVal" class="val">4</span></label>
        <input type="range" id="scaleRange" min="1" max="20" step="0.5" value="4">
      </div>
      <div class="ctrl" style="display:flex;flex-direction:column;justify-content:flex-end">
        <label>🎨 색상 테마</label>
        <div class="custom-select" id="themeSelect">
          <div class="selected-option" onclick="toggleDropdown(event)">
            <span id="selectedLabel">파란 점선 (기본)</span>
            <span class="arrow">▾</span>
          </div>
          <div class="options-list" id="optionsList">
            <div class="option active" onclick="selectTheme('blue','파란 점선 (기본)',this)">파란 점선 (기본)</div>
            <div class="option" onclick="selectTheme('gold','황금 &amp; 회색',this)">황금 &amp; 회색</div>
            <div class="option" onclick="selectTheme('rainbow','무지개 (mod별 색)',this)">무지개 (mod별 색)</div>
            <div class="option" onclick="selectTheme('neon','네온 그린',this)">네온 그린</div>
          </div>
        </div>
      </div>
    </div>
    <div style="margin-top:10px">
      <div style="font-size:11px;color:#94a3b8;font-weight:600;letter-spacing:.04em;
        text-transform:uppercase;margin-bottom:6px">⚡ 프리셋</div>
      <div class="preset-row">
        <button class="preset-btn active" onclick="applyPreset(2,0)">mod 2 — 시에르핀스키</button>
        <button class="preset-btn" onclick="applyPreset(3,0)">mod 3</button>
        <button class="preset-btn" onclick="applyPreset(5,0)">mod 5</button>
        <button class="preset-btn" onclick="applyPreset(7,0)">mod 7 (소수)</button>
        <button class="preset-btn" onclick="applyPreset(4,0)">mod 4 (합성수)</button>
      </div>
    </div>
    <div class="info-row">
      <div class="kpi"><div class="num" id="kpiMod">2</div><div class="lbl">modulo</div></div>
      <div class="kpi"><div class="num" id="kpiRem">0</div><div class="lbl">나머지(r)</div></div>
      <div class="kpi"><div class="num" id="kpiRows">—</div><div class="lbl">표시 행 수</div></div>
      <div class="kpi"><div class="num" id="kpiDots">—</div><div class="lbl">칠해진 원소</div></div>
    </div>
  </div>

  <!-- 캔버스 -->
  <div id="canvas-wrap"></div>

  <!-- 관찰 포인트 -->
  <div class="card">
    <div class="card-title">🔬 관찰 포인트</div>
    <div class="obs-box" id="obsBox">
      <b>mod 2, r=0 (짝수)</b>: 0만 남으면 빈 삼각형 &nbsp;|&nbsp;
      <b>mod 2, r=1 (홀수)</b>: <b>시에르핀스키 삼각형</b>이 나타납니다!<br>
      확대를 줄이면(배율↑) 더 많은 행을 한 눈에, 늘리면 숫자까지 확인 가능합니다.
    </div>
  </div>
</div>

<script>
// ── 설정 상태 ───────────────────────────────────
let cfg = { mod: 2, rem: 0, scale: 4, theme: 'blue' };
let totalDots = 0, visRows = 0;

// ── 색상 팔레트 ───────────────────────────────────
const THEMES = {
  blue:    (v,m,r) => v === r ? [0,102,204] : [230,230,230],
  gold:    (v,m,r) => v === r ? [245,158,11] : [30,30,50],
  rainbow: (v,m,r) => {
    const hues = [0,30,60,120,180,240,270,300,330,350,15,45];
    const h = hues[v % hues.length];
    return hslToRgb(h/360, 0.7, 0.55);
  },
  neon:    (v,m,r) => v === r ? [57,255,20] : [10,20,10],
};

function hslToRgb(h,s,l){
  let r,g,b;
  if(s===0){r=g=b=l}else{
    const q=l<0.5?l*(1+s):l+s-l*s, p=2*l-q;
    r=hue2rgb(p,q,h+1/3); g=hue2rgb(p,q,h); b=hue2rgb(p,q,h-1/3);
  }
  return [Math.round(r*255),Math.round(g*255),Math.round(b*255)];
}
function hue2rgb(p,q,t){
  if(t<0)t+=1; if(t>1)t-=1;
  if(t<1/6)return p+(q-p)*6*t;
  if(t<1/2)return q;
  if(t<2/3)return p+(q-p)*(2/3-t)*6;
  return p;
}

// ── DOM 참조 ───────────────────────────────────
const modRange   = document.getElementById('modRange');
const remRange   = document.getElementById('remRange');
const scaleRange = document.getElementById('scaleRange');

// ── 컨트롤 이벤트 ───────────────────────────────────
modRange.addEventListener('input', () => {
  cfg.mod = parseInt(modRange.value);
  if(cfg.rem >= cfg.mod) cfg.rem = 0;
  remRange.max = cfg.mod - 1;
  remRange.value = cfg.rem;
  syncUI(); redraw();
});
remRange.addEventListener('input', () => {
  cfg.rem = parseInt(remRange.value); syncUI(); redraw();
});
scaleRange.addEventListener('input', () => {
  cfg.scale = parseFloat(scaleRange.value); syncUI(); redraw();
});
function toggleDropdown(e) {
  e.stopPropagation();
  const sel = document.getElementById('themeSelect');
  const list = document.getElementById('optionsList');
  const isOpen = list.style.display === 'block';
  list.style.display = isOpen ? 'none' : 'block';
  sel.classList.toggle('open', !isOpen);
}
function selectTheme(value, label, el) {
  cfg.theme = value;
  document.getElementById('selectedLabel').textContent = label;
  document.getElementById('optionsList').style.display = 'none';
  document.getElementById('themeSelect').classList.remove('open');
  document.querySelectorAll('.option').forEach(o => o.classList.remove('active'));
  el.classList.add('active');
  redraw();
}
document.addEventListener('click', () => {
  document.getElementById('optionsList').style.display = 'none';
  document.getElementById('themeSelect').classList.remove('open');
});

function applyPreset(m, r) {
  cfg.mod = m; cfg.rem = r;
  modRange.value = m; remRange.max = m-1; remRange.value = r;
  syncUI(); redraw();
  document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
}

function syncUI() {
  document.getElementById('modVal').textContent  = cfg.mod;
  document.getElementById('remVal').textContent  = cfg.rem;
  document.getElementById('scaleVal').textContent = cfg.scale;
  remRange.max = cfg.mod - 1;
  document.getElementById('kpiMod').textContent = cfg.mod;
  document.getElementById('kpiRem').textContent = cfg.rem;
  updateObs();
}

const OBS_MAP = {
  '2_0': '짝수 원소만 색칠 → 대부분 빈 공간. <b>홀수(r=1)</b>로 바꿔보세요!',
  '2_1': '<b>시에르핀스키 삼각형(Sierpiński triangle)</b>! 홀수인 이항계수만 색칠하면 자기유사 삼각형이 나타납니다. 뤼카 정리로 설명됩니다.',
  '3_0': 'mod 3에서 r=0: 3의 배수인 원소 위치. 삼각형 안에 작은 삼각형 빈 공간이 반복됩니다.',
  '3_1': 'mod 3, r=1: 세 가지 나머지 중 하나. 프랙털 서브삼각형 구조를 확인하세요.',
  '3_2': 'mod 3, r=2: 나머지가 2인 원소들도 프랙털 패턴을 형성합니다.',
  '__prime': '소수 mod일 때 규칙적 격자 패턴(뤼카 정리). 합성수 mod일 때보다 패턴이 선명합니다.',
  '__composite': '합성수 mod: 소수 mod보다 패턴이 불규칙적입니다. <b>mod 4 vs mod 5</b>를 비교해보세요!',
};
const PRIMES = new Set([2,3,5,7,11]);

function updateObs(){
  const key = `${cfg.mod}_${cfg.rem}`;
  let txt = OBS_MAP[key] || '';
  if(!txt) txt = PRIMES.has(cfg.mod) ? OBS_MAP['__prime'] : OBS_MAP['__composite'];
  document.getElementById('obsBox').innerHTML = txt;
}

// ── p5.js 스케치 ───────────────────────────────────
let p5Instance = null;

function redraw() {
  if(p5Instance) p5Instance.remove();
  const wrap = document.getElementById('canvas-wrap');
  wrap.innerHTML = '';

  p5Instance = new p5(function(p){
    const BASE = 60;
    let tri = [];

    p.setup = function(){
      const w = wrap.clientWidth || 700;
      p.createCanvas(w, 660).parent(wrap);
      p.noStroke();
      buildTri();
      p.noLoop();
    };

    function buildTri(){
      const spacing = BASE / cfg.scale;
      const rows = Math.floor((p.height - 20) / spacing);
      tri = [];
      totalDots = 0;
      visRows = rows;
      for(let n=0;n<rows;n++){
        tri[n]=[];
        for(let k=0;k<=n;k++){
          const v = (k===0||k===n) ? 1n : tri[n-1][k-1]+tri[n-1][k];
          tri[n][k] = v;
          const rem = Number(v % BigInt(cfg.mod));
          if(rem === cfg.rem) totalDots++;
        }
      }
      document.getElementById('kpiRows').textContent = rows;
      document.getElementById('kpiDots').textContent = totalDots.toLocaleString();
    }

    p.draw = function(){
      p.background(10, 22, 40);
      const spacing = BASE / cfg.scale;
      const palFn = THEMES[cfg.theme] || THEMES.blue;
      const textMode = spacing >= 20;
      if(textMode){ p.textAlign(p.CENTER, p.CENTER); }

      for(let n=0;n<tri.length;n++){
        for(let k=0;k<=n;k++){
          const v = tri[n][k];
          const rem = Number(v % BigInt(cfg.mod));
          const [r,g,b] = palFn(rem, cfg.mod, cfg.rem);
          const x = p.width/2 + (k - n/2)*spacing;
          const y = n*spacing + 14;
          p.fill(r,g,b);
          p.ellipse(x, y, spacing*0.65);
          if(textMode){
            p.fill(255);
            p.textSize(spacing*0.28);
            p.text(v.toString(), x, y);
          }
        }
      }
    };
  });
}

// 초기 실행
syncUI();
redraw();

// 창 크기 변경 시 재렌더
window.addEventListener('resize', () => { redraw(); });
</script>
</body>
</html>
"""

# ──────────────────────────────────────────────
# render()
# ──────────────────────────────────────────────

def render():
    st.header("🔺 파스칼 삼각형에서 찾아보는 프랙털")
    st.markdown(
        "파스칼 삼각형의 각 항을 **mod m** (m으로 나눈 나머지)로 색칠하면 "
        "놀라운 **프랙털 패턴**이 나타납니다.  \n"
        "아래 시뮬레이터에서 **modulo 값**과 **나머지**를 자유롭게 바꾸며 탐구해보세요!"
    )

    components.html(_CANVAS_HTML, height=1300, scrolling=False)

    st.markdown("---")

    # ── 탐구 활동 ──────────────────────────────
    st.subheader("🧪 탐구 활동")

    with st.expander("📐 탐구 1: 시에르핀스키 삼각형과 이항계수", expanded=True):
        st.markdown("""
**시에르핀스키 삼각형**은 자기유사성(self-similarity)을 가진 가장 유명한 프랙털 중 하나입니다.

① 위 시뮬레이터에서 `mod = 2`, `r = 1` 로 설정해보세요.
② 홀수인 이항계수(${}_{n}C_{k}$)만 색칠되며 시에르핀스키 삼각형이 나타납니다.
③ **확대 배율**을 낮춰 더 많은 행을 보세요 — 패턴이 무한히 반복됨을 확인하세요.

> **핵심 원리 (뤼카 정리)**: 소수 $p$에 대해 ${}_{n}C_{k} \\equiv \\prod_{i} {}_{n_i}C_{k_i} \\pmod{p}$
> 여기서 $n_i, k_i$는 $n, k$의 $p$진법 각 자리수입니다.
> $k$의 어느 자리가 $n$의 대응 자리보다 크면 ${}_{n}C_{k} \\equiv 0$이 됩니다.
""")

    with st.expander("🔢 탐구 2: 소수 mod vs 합성수 mod 비교"):
        st.markdown("""
| 설정 | 패턴 특성 |
|------|-----------|
| **mod 2 (소수)** | 매우 규칙적인 시에르핀스키 삼각형 |
| **mod 3 (소수)** | 3색 자기유사 삼각형 패턴 |
| **mod 5 (소수)** | 5배 분기되는 정교한 격자 |
| **mod 4 (합성수)** | mod 2·2 이어서 패턴이 불규칙 |
| **mod 6 (합성수)** | mod 2·3 혼합 → 복잡한 패턴 |

① 소수 mod와 합성수 mod를 번갈아 설정하며 패턴을 비교해보세요.
② 소수 mod일 때 왜 더 규칙적인 패턴이 나올까요? **뤼카 정리**와 연결해서 생각해보세요.
""")

    with st.expander("🌀 탐구 3: 프랙털 차원 느껴보기"):
        st.markdown("""
프랙털은 **비정수 차원**(Hausdorff dimension)을 가집니다.
시에르핀스키 삼각형의 차원 $D$는:

$$D = \\frac{\\ln 3}{\\ln 2} \\approx 1.585$$

(2차원도 아니고 1차원도 아닌 "1.585차원"!)

① 시뮬레이터에서 배율을 줄여가며 배율이 2배 될 때마다 점의 수가 대략 몇 배가 되는지 세어보세요.
② 만약 3배 많아진다면 $D = \\log_2 3 \\approx 1.585$ 임을 확인할 수 있습니다.
③ mod 3일 때의 패턴에서도 비슷하게 계산해보면? *(힌트: $\\frac{\\ln 6}{\\ln 3}$)*
""")

    st.markdown("---")

    # ── 퀴즈 ──────────────────────────────────
    st.subheader("📝 확인 퀴즈")
    st.caption("각 문항을 풀고 확인 버튼을 눌러보세요.")

    for i, q in enumerate(_QUIZ):
        with st.container():
            st.markdown(f"**Q{i+1}. {q['q']}**")
            sel_key = f"gifted_pascal_fractal_quiz_sel_{i}"
            chk_key = f"gifted_pascal_fractal_quiz_chk_{i}"

            sel = st.radio(
                label="선택",
                options=q["choices"],
                key=sel_key,
                label_visibility="collapsed",
            )
            if st.button("✅ 확인", key=chk_key):
                if q["choices"].index(sel) == q["answer"]:
                    st.success(f"정답! 🎉  \n{q['explain']}")
                else:
                    correct = q["choices"][q["answer"]]
                    st.error(f"아쉽게도 틀렸습니다.  \n**정답**: {correct}  \n{q['explain']}")
            st.markdown("---")
