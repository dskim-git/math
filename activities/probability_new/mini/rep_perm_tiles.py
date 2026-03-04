import streamlit as st
import streamlit.components.v1 as components
import requests
import datetime

_GAS_URL = "https://script.google.com/macros/s/AKfycbwJd7W3jYTucIALzqNJUyHvmnT3nqDCEmRZXAsBlBl3IWQYhuYqyvkI3B280chlr0g/exec"
_SHEET_NAME = "색깔타일"

META = {
    "title": "미니: 색깔 타일 배열기",
    "description": "k가지 색 타일을 n칸에 배열하는 kⁿ가지 경우를 시각적으로 탐색합니다.",
    "order": 999999,
    "hidden": True,
}

def render():
    st.header("🎨 색깔 타일 배열기")
    st.markdown("""
- $k$가지 색 타일을 **$n$칸에 나열**할 때 (같은 색 반복 허용), 경우의 수 = $k^n$
- 색의 수와 칸 수를 바꿔가며 규칙을 찾아보세요.
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
  .row { display: flex; gap: 32px; flex-wrap: wrap; align-items: center; }
  .ctrl label { font-size: 13px; color: #6b7280; font-weight: 600; }
  .val { display: inline-block; min-width: 28px; background: #eef2ff; border: 1px solid #c7d2fe;
         border-radius: 8px; padding: 2px 8px; font-weight: 700; font-size: 15px; text-align: center; }
  .formula { font-size: 22px; font-weight: 700; color: #1e40af; margin: 8px 0 4px; }
  .tiles-wrap { display: flex; flex-direction: column; gap: 4px; max-height: 400px;
                overflow-y: auto; padding: 8px; border: 1px solid #e5e7eb; border-radius: 10px;
                background: #f9fafb; }
  .row-tiles { display: flex; gap: 3px; align-items: center; }
  .tile { width: 28px; height: 28px; border-radius: 5px; border: 1px solid rgba(0,0,0,.1); flex-shrink: 0; }
  .idx { font-size: 11px; color: #9ca3af; min-width: 28px; text-align: right; margin-right: 4px; }
  .palette { display: flex; gap: 6px; flex-wrap: wrap; margin: 8px 0; }
  .swatch { width: 24px; height: 24px; border-radius: 5px; border: 1px solid rgba(0,0,0,.15); }
  .info-row { display: flex; gap: 16px; align-items: center; flex-wrap: wrap; margin-top: 8px; }
  .kpi { border: 1px solid #e5e7eb; border-radius: 12px; padding: 8px 18px; text-align: center; }
  .kpi .num { font-size: 26px; font-weight: 800; color: #111827; }
  .kpi .lbl { font-size: 12px; color: #6b7280; }
  .warn { color: #b45309; font-size: 13px; margin-top: 6px; }
</style>
</head>
<body>

<div class="card">
  <h3>🎛 설정</h3>
  <div class="row">
    <div class="ctrl">
      <label>색깔 수 k = <span id="kVal" class="val">3</span></label><br>
      <input type="range" id="kRange" min="2" max="6" value="3" style="width:180px;margin-top:4px;">
    </div>
    <div class="ctrl">
      <label>칸 수 n = <span id="nVal" class="val">3</span></label><br>
      <input type="range" id="nRange" min="1" max="5" value="3" style="width:180px;margin-top:4px;">
    </div>
  </div>

  <div>팔레트: <span id="palette" class="palette"></span></div>

  <div class="formula" id="formula"></div>
  <div style="font-size:13px;color:#6b7280;" id="sub"></div>

  <div class="info-row">
    <div class="kpi"><div class="num" id="totalNum">—</div><div class="lbl">총 경우의 수</div></div>
    <div class="kpi"><div class="num" id="formulaKpi">—</div><div class="lbl">공식 kⁿ</div></div>
  </div>
</div>

<div class="card">
  <h3>📋 전체 배열 <span id="listInfo" style="font-size:13px;color:#6b7280;"></span></h3>
  <div class="tiles-wrap" id="tilesWrap"></div>
  <div class="warn" id="warn"></div>
</div>

<script>
const COLORS = ['#ef4444','#3b82f6','#22c55e','#f59e0b','#a855f7','#ec4899'];
const NAMES  = ['빨강','파랑','초록','주황','보라','분홍'];
const MAX = 300;

const kRange = document.getElementById('kRange');
const nRange = document.getElementById('nRange');

function* cartesian(k, n) {
  if (n === 0) { yield []; return; }
  for (const rest of cartesian(k, n - 1))
    for (let i = 0; i < k; i++) yield [i, ...rest];
}

function superscript(n) {
  const sup = {'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵'};
  return String(n).split('').map(c => sup[c] || c).join('');
}

function update() {
  const k = parseInt(kRange.value);
  const n = parseInt(nRange.value);
  document.getElementById('kVal').textContent = k;
  document.getElementById('nVal').textContent = n;

  // palette
  const palette = document.getElementById('palette');
  palette.innerHTML = '';
  for (let i = 0; i < k; i++) {
    const s = document.createElement('div');
    s.className = 'swatch';
    s.style.background = COLORS[i];
    s.title = NAMES[i];
    palette.appendChild(s);
  }

  const total = Math.pow(k, n);
  document.getElementById('formula').textContent = `경우의 수: ${k}${superscript(n)} = ${total.toLocaleString()}가지`;
  document.getElementById('sub').textContent = `${k}가지 색 중 중복 허용하여 ${n}칸 배열 → ₍${k}₎Π₍${n}₎ = ${k}${superscript(n)} = ${total}`;
  document.getElementById('totalNum').textContent = total.toLocaleString();
  document.getElementById('formulaKpi').textContent = `${k}${superscript(n)}`;

  const wrap = document.getElementById('tilesWrap');
  wrap.innerHTML = '';
  const warn = document.getElementById('warn');
  const info = document.getElementById('listInfo');

  const limit = Math.min(total, MAX);
  if (total > MAX) {
    warn.textContent = `총 ${total.toLocaleString()}가지 중 처음 ${MAX}개만 표시합니다.`;
    info.textContent = `(처음 ${MAX}개)`;
  } else {
    warn.textContent = '';
    info.textContent = `(${total}가지 전체)`;
  }

  let count = 0;
  for (const combo of cartesian(k, n)) {
    if (count >= limit) break;
    const row = document.createElement('div');
    row.className = 'row-tiles';

    const idx = document.createElement('div');
    idx.className = 'idx';
    idx.textContent = count + 1;
    row.appendChild(idx);

    for (const ci of combo) {
      const tile = document.createElement('div');
      tile.className = 'tile';
      tile.style.background = COLORS[ci];
      tile.title = NAMES[ci];
      row.appendChild(tile);
    }
    wrap.appendChild(row);
    count++;
  }
}

kRange.addEventListener('input', update);
nRange.addEventListener('input', update);
update();
</script>
</body>
</html>
""", height=700)
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
                else:
                    st.error(f"제출 중 오류가 발생했습니다. (상태코드: {resp.status_code})")
            except Exception as e:
                st.error(f"제출 실패: {e}")
