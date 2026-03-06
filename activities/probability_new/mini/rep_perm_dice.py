import streamlit as st
import streamlit.components.v1 as components
import requests
import datetime

_GAS_URL = "https://script.google.com/macros/s/AKfycbwJd7W3jYTucIALzqNJUyHvmnT3nqDCEmRZXAsBlBl3IWQYhuYqyvkI3B280chlr0g/exec"
_SHEET_NAME = "주사위던지기"

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
  body { font-family: system-ui, sans-serif; margin: 0; padding: 8px 12px 24px; background: #f8fafc; }
  .card { background: #fff; border: 1px solid #e5e7eb; border-radius: 14px; padding: 16px 20px; margin: 10px 0; }
  h3 { margin: 0 0 10px; font-size: 16px; }
  .ctrl label { font-size: 13px; color: #6b7280; font-weight: 600; }
  .val { display: inline-block; min-width: 28px; background: #eef2ff; border: 1px solid #c7d2fe;
         border-radius: 8px; padding: 2px 8px; font-weight: 700; font-size: 15px; text-align: center; }
  .formula { font-size: 22px; font-weight: 700; color: #1e40af; margin: 8px 0 4px; }
  .info-row { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; margin-top: 8px; }
  .kpi { border: 1px solid #e5e7eb; border-radius: 12px; padding: 8px 18px; text-align: center; }
  .kpi .num { font-size: 26px; font-weight: 800; color: #111827; }
  .kpi .lbl { font-size: 12px; color: #6b7280; }
  .tree-scroll { overflow: auto; max-height: 420px; border: 1px solid #e5e7eb;
                 border-radius: 10px; padding: 12px; background: #f9fafb; }
  .tree-node { display: flex; align-items: center; }
  .tree-line { width: 20px; height: 1px; background: #cbd5e1; flex-shrink: 0; }
  .tree-vline { width: 1px; background: #cbd5e1; }
  .dice { display: inline-flex; align-items: center; justify-content: center;
          width: 38px; height: 38px; border-radius: 6px; border: 2px solid #e5e7eb;
          font-size: 28px; background: #fff; flex-shrink: 0; }
  .leaf { background: #eff6ff; border-color: #bfdbfe; font-size: 12px; font-family: monospace;
          padding: 2px 6px; border-radius: 6px; margin-left: 4px; }
  .result-grid { display: flex; flex-wrap: wrap; gap: 5px; max-height: 300px; overflow-y: auto;
                 padding: 8px; border: 1px solid #e5e7eb; border-radius: 10px; background: #f9fafb; }
  .result-chip { background: #fff; border: 1px solid #e5e7eb; border-radius: 7px;
                 padding: 3px 7px; font-size: 13px; font-family: monospace; }
  .warn { color: #b45309; font-size: 13px; margin-top: 6px; }
  .tab-btns { display: flex; gap: 6px; margin-bottom: 10px; }
  .tab-btn { padding: 6px 14px; border-radius: 8px; border: 1px solid #d1d5db;
             background: #f9fafb; cursor: pointer; font-size: 13px; }
  .tab-btn.active { background: #2563eb; color: #fff; border-color: #1e40af; }
</style>
</head>
<body>

<div class="card">
  <h3>🎛 설정</h3>
  <div class="ctrl">
    <label>던지는 횟수 n = <span id="nVal" class="val">2</span></label><br>
    <input type="range" id="nRange" min="1" max="4" value="2" style="width:200px;margin-top:6px;">
  </div>
  <div class="formula" id="formula">6² = 36가지</div>
  <div style="font-size:13px;color:#6b7280;" id="sub"></div>
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
    <div style="font-size:13px;color:#6b7280;margin-bottom:6px;" id="listInfo"></div>
    <div class="result-grid" id="resultGrid"></div>
    <div class="warn" id="warn"></div>
  </div>

  <div id="tabTree" style="display:none;">
    <div style="font-size:13px;color:#6b7280;margin-bottom:6px;">
      n이 클수록 트리가 방대해지므로 n≤3 에서만 표시합니다.
    </div>
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
    nodeDiv.style.marginLeft = (depth * 32) + 'px';
    nodeDiv.style.marginBottom = '2px';
    nodeDiv.style.display = 'flex';
    nodeDiv.style.alignItems = 'center';
    nodeDiv.style.gap = '4px';

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

  // 목록
  const grid = document.getElementById('resultGrid');
  const warn = document.getElementById('warn');
  const info = document.getElementById('listInfo');
  grid.innerHTML = '';
  warn.textContent = '';

  const limit = Math.min(total, MAX);
  info.textContent = total <= MAX ? `(${total}가지 전체 표시)` : `(처음 ${MAX}개 표시)`;
  if (total > MAX) warn.textContent = `총 ${total.toLocaleString()}가지 중 처음 ${MAX}개만 표시합니다.`;

  let count = 0;
  for (const combo of cartesian6(n)) {
    if (count >= limit) break;
    const chip = document.createElement('span');
    chip.className = 'result-chip';
    chip.textContent = combo.map(v => FACES[v - 1]).join(' ');
    grid.appendChild(chip);
    count++;
  }

  // 트리
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
""", height=720)
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

        st.markdown("**📝 이 활동으로 해결할 수 있는 문제 3개 (문제와 답 모두 작성)**")
        q1 = st.text_area("문제 1", height=80)
        a1 = st.text_input("문제 1의 답")
        q2 = st.text_area("문제 2", height=80)
        a2 = st.text_input("문제 2의 답")
        q3 = st.text_area("문제 3", height=80)
        a3 = st.text_input("문제 3의 답")

        new_learning = st.text_area("💡 이 활동을 통해 새롭게 알게 된 점", height=100)
        feeling = st.text_area("💬 이 활동을 통해 느낀 점", height=100)

        submitted = st.form_submit_button("📤 제출하기", use_container_width=True, type="primary")

    if submitted:
        if not student_id or not name:
            st.warning("학번과 이름을 입력해주세요.")
        elif gas_url == "YOUR_GAS_WEB_APP_URL":
            st.error("⚠️ Google Sheets 연동 URL이 아직 설정되지 않았습니다. 선생님께 문의하세요.")
        else:
            payload = {
                "sheet":     sheet_name,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "학번":    student_id,
                "이름":    name,
                "문제1":   q1, "답1":  a1,
                "문제2":   q2, "답2":  a2,
                "문제3":   q3, "답3":  a3,
                "새롭게알게된점": new_learning,
                "느낀점":   feeling,
            }
            try:
                resp = requests.post(gas_url, json=payload, timeout=10)
                if resp.status_code == 200:
                    st.success(f"✅ {name}님의 활동 기록이 제출되었습니다!")
                    st.balloons()
                else:
                    st.error(f"제출 중 오류가 발생했습니다. (상태코드: {resp.status_code})")
            except Exception as e:
                st.error(f"제출 실패: {e}")
