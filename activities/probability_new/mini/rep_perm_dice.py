import streamlit as st
import streamlit.components.v1 as components
import requests
from reflection_utils import render_reflection_form
import datetime

_GAS_URL = st.secrets["gas_url_probability_new"]
_SHEET_NAME = "주사위던지기"

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
    "title": "미니: 주사위 연속 던지기와 중복순열",
    "description": "주사위를 n번 던질 때 나오는 6ⁿ가지 결과를 트리 형태로 탐색합니다.",
    "order": 999999,
    "hidden": True,
}

def render():
    st.header("🎲 주사위 연속 던지기와 중복순열")
    st.markdown("""
- 주사위를 $n$번 던질 때, 매 시행마다 1~6 중 하나가 나옵니다. (중복 허용)
- 전체 경우의 수 = $6^n$ → **중복순열** $\\_{6}\\Pi_{n} = 6^n$
- 아래에서 던지는 횟수를 바꾸며 트리를 확인해 보세요.
""")

    components.html("""
<!doctype html>
<html>
<head>
<meta charset="utf-8"/>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0a1628 0%,#0f2027 50%,#0a1628 100%);min-height:100vh;padding:16px;color:#e2e8f0}
  .card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:20px 24px;margin:12px 0;backdrop-filter:blur(10px)}
  .card-title{font-size:15px;font-weight:700;color:#fbbf24;margin-bottom:14px;display:flex;align-items:center;gap:8px;letter-spacing:.02em}
  .ctrl label{font-size:12px;color:#94a3b8;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
  .ctrl input[type=range]{width:200px;-webkit-appearance:none;height:6px;border-radius:3px;background:linear-gradient(90deg,#f59e0b,#ef4444);outline:none;margin-top:8px;display:block}
  .ctrl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#fff;border:3px solid #f59e0b;cursor:pointer;box-shadow:0 0 10px rgba(245,158,11,.6)}
  .val{display:inline-block;min-width:36px;background:linear-gradient(135deg,#f59e0b,#ef4444);border-radius:10px;padding:3px 10px;font-weight:800;font-size:17px;text-align:center;color:#fff;box-shadow:0 2px 12px rgba(245,158,11,.5)}
  .formula-box{background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.25);border-radius:14px;padding:14px 20px;margin:14px 0;text-align:center}
  .formula{font-size:26px;font-weight:800;color:#fbbf24;margin-bottom:4px}
  .sub{font-size:13px;color:#94a3b8}
  .info-row{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:4px}
  .kpi{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:12px 24px;text-align:center;min-width:110px}
  .kpi .num{font-size:32px;font-weight:900;color:#e2e8f0}
  .kpi .lbl{font-size:11px;color:#94a3b8;margin-top:4px;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
  .tab-btns{display:flex;gap:8px;margin-bottom:12px}
  .tab-btn{padding:7px 18px;border-radius:10px;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.04);cursor:pointer;font-size:13px;font-weight:600;color:#94a3b8;transition:.2s}
  .tab-btn.active{background:rgba(245,158,11,.2);color:#fbbf24;border-color:rgba(245,158,11,.4)}
  .result-grid{display:flex;flex-wrap:wrap;gap:6px;max-height:280px;overflow-y:auto;padding:8px}
  .result-chip{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:8px;padding:5px 9px;font-size:14px;font-family:monospace;color:#e2e8f0;cursor:pointer;transition:.2s}
  .result-chip:hover{background:rgba(245,158,11,.15);border-color:rgba(245,158,11,.3);transform:scale(1.05)}
  .warn{color:#fbbf24;font-size:13px;margin-top:8px}
  .tree-scroll{overflow:auto;max-height:400px;padding:4px}
  .tree-node{display:flex;align-items:center;gap:6px;margin:3px 0}
  .dice{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:8px;border:2px solid rgba(255,255,255,.15);font-size:28px;background:rgba(255,255,255,.06);flex-shrink:0;transition:.2s;cursor:pointer}
  .dice:hover{background:rgba(245,158,11,.2);border-color:rgba(245,158,11,.4);transform:scale(1.1)}
  .leaf{background:rgba(99,102,241,.2);border:1px solid rgba(99,102,241,.3);font-size:11px;font-family:monospace;padding:3px 7px;border-radius:6px;color:#a5b4fc}
  ::-webkit-scrollbar{width:5px;height:5px}
  ::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
  ::-webkit-scrollbar-thumb{background:rgba(245,158,11,.4);border-radius:3px}
</style>
</head>
<body>

<div class="card">
  <div class="card-title">⚙️ 설정</div>
  <div class="ctrl">
    <label>던지는 횟수 n = <span id="nVal" class="val">2</span></label>
    <input type="range" id="nRange" min="1" max="4" value="2">
  </div>
  <div class="formula-box">
    <div class="formula" id="formula">6² = 36가지</div>
    <div class="sub" id="sub">주사위 2번 던지기 → 매번 6가지 → ₆Π₂ = 6² = 36</div>
  </div>
  <div class="info-row">
    <div class="kpi"><div class="num" id="totalNum">36</div><div class="lbl">총 경우의 수</div></div>
    <div class="kpi"><div class="num" id="formulaKpi">6²</div><div class="lbl">공식 6ⁿ</div></div>
  </div>
</div>

<div class="card">
  <div class="tab-btns">
    <button class="tab-btn active" id="btnList" onclick="showTab('list')">📋 목록</button>
    <button class="tab-btn" id="btnTree" onclick="showTab('tree')">🌳 트리 (n≤3)</button>
  </div>

  <div id="tabList">
    <div style="font-size:12px;color:#64748b;margin-bottom:8px;" id="listInfo"></div>
    <div class="result-grid" id="resultGrid"></div>
    <div class="warn" id="warn"></div>
  </div>

  <div id="tabTree" style="display:none;">
    <div style="font-size:13px;color:#64748b;margin-bottom:8px;">n이 클수록 트리가 방대해지므로 n≤3 에서만 표시합니다.</div>
    <div class="tree-scroll" id="treeWrap"></div>
  </div>
</div>

<script>
const FACES = ['⚀','⚁','⚂','⚃','⚄','⚅'];
const MAX = 500;
let currentTab = 'list';

const nRange = document.getElementById('nRange');

function superscript(n) {
  const sup = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴'};
  return String(n).split('').map(c => sup[c] || c).join('');
}
function* cartesian6(n) {
  if (n === 0) { yield []; return; }
  for (const rest of cartesian6(n - 1))
    for (let i = 1; i <= 6; i++) yield [i, ...rest];
}

function showTab(t) {
  currentTab = t;
  document.getElementById('tabList').style.display = t === 'list' ? '' : 'none';
  document.getElementById('tabTree').style.display = t === 'tree' ? '' : 'none';
  document.getElementById('btnList').className = 'tab-btn' + (t === 'list' ? ' active' : '');
  document.getElementById('btnTree').className = 'tab-btn' + (t === 'tree' ? ' active' : '');
}

function buildTree(prefix, depth, maxDepth, container) {
  if (depth === maxDepth) return;
  for (let f = 1; f <= 6; f++) {
    const nodeDiv = document.createElement('div');
    nodeDiv.className = 'tree-node';
    nodeDiv.style.marginLeft = (depth * 38) + 'px';

    const dice = document.createElement('span');
    dice.className = 'dice';
    dice.textContent = FACES[f - 1];
    nodeDiv.appendChild(dice);

    if (depth === maxDepth - 1) {
      const lbl = document.createElement('span');
      lbl.className = 'leaf';
      lbl.textContent = [...prefix, f].join('-');
      nodeDiv.appendChild(lbl);
    }
    container.appendChild(nodeDiv);
    buildTree([...prefix, f], depth + 1, maxDepth, container);
  }
}

function update() {
  const n = parseInt(nRange.value);
  document.getElementById('nVal').textContent = n;
  const total = Math.pow(6, n);

  document.getElementById('formula').textContent = `6${superscript(n)} = ${total.toLocaleString()}가지`;
  document.getElementById('sub').textContent =
    `주사위 ${n}번 던지기 → 매번 6가지 → ₆Π${n} = 6${superscript(n)} = ${total.toLocaleString()}`;
  document.getElementById('totalNum').textContent = total.toLocaleString();
  document.getElementById('formulaKpi').textContent = `6${superscript(n)}`;

  const grid = document.getElementById('resultGrid');
  const warn = document.getElementById('warn');
  const info = document.getElementById('listInfo');
  grid.innerHTML = '';
  warn.textContent = '';

  const limit = Math.min(total, MAX);
  info.textContent = total <= MAX ? `${total}가지 전체 표시` : `처음 ${MAX}개 표시`;
  if (total > MAX) warn.textContent = `⚠ 총 ${total.toLocaleString()}가지 중 처음 ${MAX}개만 표시합니다.`;

  let count = 0;
  for (const combo of cartesian6(n)) {
    if (count >= limit) break;
    const chip = document.createElement('span');
    chip.className = 'result-chip';
    chip.textContent = combo.map(v => FACES[v - 1]).join(' ');
    grid.appendChild(chip);
    count++;
  }

  const treeWrap = document.getElementById('treeWrap');
  treeWrap.innerHTML = '';
  if (n <= 3) {
    buildTree([], 0, n, treeWrap);
  } else {
    treeWrap.textContent = 'n > 3이면 트리가 너무 커져 표시하지 않습니다. 목록 탭을 이용하세요.';
  }
}

nRange.addEventListener('input', update);
update();
</script>
</body>
</html>
""", height=740)
    _render_quiz(_SHEET_NAME)
    render_reflection_form(_SHEET_NAME, _GAS_URL, _QUESTIONS)


def _render_quiz(sheet_name: str):
    st.divider()
    st.subheader("🧩 확인 문제")
    st.caption("활동을 바탕으로 아래 문제를 풀어보세요. 답을 입력하고 **채점하기** 버튼을 눌러주세요.")

    QUIZ = [
        {
            "q": "주사위를 3번 던질 때, 나온 세 수의 합이 3이 되는 경우의 수를 구하시오. (예: (1,1,1)만 가능)",
            "a": "1",
            "hint": "세 수의 합이 3이 되려면 각 수는 1 이상이므로, 세 수가 모두 1인 경우뿐입니다.",
            "sol": "세 수의 합이 3이고 각 수가 1~6의 자연수이므로 $(1, 1, 1)$의 1가지뿐입니다.\n\n(합이 3인 경우: $1+1+1=3$, 다른 조합은 불가)"
        },
        {
            "q": "주사위 2개를 동시에 던질 때, 두 눈의 곱이 홀수인 경우의 수를 구하시오.",
            "a": "9",
            "hint": "곱이 홀수이려면 두 눈 모두 홀수여야 합니다. 주사위에서 홀수는 1, 3, 5입니다.",
            "sol": "곱이 홀수 ↔ 두 수 모두 홀수\n\n주사위의 홀수: 1, 3, 5 → 3가지\n\n두 눈 모두 홀수인 경우: $3 \\times 3 = 9$가지입니다."
        },
        {
            "q": "주사위를 4번 던져서 나온 4개의 수의 곱이 짝수가 되는 경우의 수를 구하시오.",
            "a": "1215",
            "hint": "여사건(4개 모두 홀수)을 이용하면 편리합니다.",
            "sol": "전체 경우의 수: $6^4 = 1296$\n\n여사건(곱이 홀수 = 4개 모두 홀수): 홀수는 1, 3, 5로 3가지 → $3^4 = 81$\n\n곱이 짝수인 경우: $1296 - 81 = 1215$가지"
        },
    ]

    for i, item in enumerate(QUIZ):
        with st.container():
            st.markdown(f"**문제 {i+1}.** {item['q']}")
            col1, col2 = st.columns([3, 1])
            with col1:
                user_ans = st.text_input(f"답 입력 (문제 {i+1})", key=f"dice_q{i+1}", label_visibility="collapsed", placeholder="답을 입력하세요")
            with col2:
                check = st.button("채점하기", key=f"dice_check{i+1}", use_container_width=True)

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
