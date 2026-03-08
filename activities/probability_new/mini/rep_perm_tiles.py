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
  *{box-sizing:border-box;margin:0;padding:0}
  body{font-family:'Segoe UI',system-ui,sans-serif;background:linear-gradient(135deg,#0f172a 0%,#1a0a2e 50%,#0f172a 100%);min-height:100vh;padding:16px;color:#e2e8f0}
  .card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:20px 24px;margin:12px 0;backdrop-filter:blur(10px)}
  .card-title{font-size:15px;font-weight:700;color:#c4b5fd;margin-bottom:14px;display:flex;align-items:center;gap:8px;letter-spacing:.02em}
  .row{display:flex;gap:32px;flex-wrap:wrap;align-items:center}
  .ctrl label{font-size:12px;color:#94a3b8;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
  .ctrl input[type=range]{width:180px;-webkit-appearance:none;height:6px;border-radius:3px;background:linear-gradient(90deg,#a855f7,#ec4899);outline:none;margin-top:8px;display:block}
  .ctrl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#fff;border:3px solid #a855f7;cursor:pointer;box-shadow:0 0 10px rgba(168,85,247,.6)}
  .val{display:inline-block;min-width:36px;background:linear-gradient(135deg,#a855f7,#ec4899);border-radius:10px;padding:3px 10px;font-weight:800;font-size:17px;text-align:center;color:#fff;box-shadow:0 2px 12px rgba(168,85,247,.5)}
  .formula-box{background:rgba(168,85,247,.1);border:1px solid rgba(168,85,247,.25);border-radius:14px;padding:14px 20px;margin:14px 0;text-align:center}
  .formula{font-size:26px;font-weight:800;color:#c4b5fd;margin-bottom:4px}
  .sub{font-size:13px;color:#94a3b8}
  .palette{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0}
  .swatch{width:32px;height:32px;border-radius:8px;border:2px solid rgba(255,255,255,.15);cursor:pointer;transition:.2s;box-shadow:0 2px 8px rgba(0,0,0,.3)}
  .swatch:hover{transform:scale(1.15)}
  .info-row{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:4px}
  .kpi{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:12px 24px;text-align:center;min-width:110px}
  .kpi .num{font-size:32px;font-weight:900;color:#e2e8f0}
  .kpi .lbl{font-size:11px;color:#94a3b8;margin-top:4px;font-weight:600;letter-spacing:.04em;text-transform:uppercase}
  .tiles-wrap{display:flex;flex-direction:column;gap:5px;max-height:380px;overflow-y:auto;padding:10px}
  .row-tiles{display:flex;gap:4px;align-items:center}
  .tile{width:32px;height:32px;border-radius:7px;border:2px solid rgba(255,255,255,.1);flex-shrink:0;transition:.2s;box-shadow:0 2px 6px rgba(0,0,0,.3)}
  .tile:hover{transform:scale(1.15);border-color:rgba(255,255,255,.4)}
  .idx{font-size:10px;color:#64748b;min-width:28px;text-align:right;margin-right:6px}
  .warn{color:#fbbf24;font-size:13px;margin-top:8px}
  ::-webkit-scrollbar{width:5px;height:5px}
  ::-webkit-scrollbar-track{background:rgba(0,0,0,.3);border-radius:3px}
  ::-webkit-scrollbar-thumb{background:rgba(168,85,247,.4);border-radius:3px}
</style>
</head>
<body>

<div class="card">
  <div class="card-title">⚙️ 설정</div>
  <div class="row">
    <div class="ctrl">
      <label>색깔 수 k = <span id="kVal" class="val">3</span></label>
      <input type="range" id="kRange" min="2" max="6" value="3">
    </div>
    <div class="ctrl">
      <label>칸 수 n = <span id="nVal" class="val">3</span></label>
      <input type="range" id="nRange" min="1" max="5" value="3">
    </div>
  </div>
  <div style="font-size:12px;color:#94a3b8;font-weight:600;letter-spacing:.04em;text-transform:uppercase;margin:10px 0 6px">팔레트</div>
  <div id="palette" class="palette"></div>
  <div class="formula-box">
    <div class="formula" id="formula">3³ = 27가지</div>
    <div class="sub" id="sub">3가지 색 중 중복 허용하여 3칸 배열 → ₃Π₃ = 3³ = 27</div>
  </div>
  <div class="info-row">
    <div class="kpi"><div class="num" id="totalNum">—</div><div class="lbl">총 경우의 수</div></div>
    <div class="kpi"><div class="num" id="formulaKpi">—</div><div class="lbl">공식 kⁿ</div></div>
  </div>
</div>

<div class="card">
  <div class="card-title">🎨 전체 배열 <span id="listInfo" style="font-size:12px;color:#64748b;font-weight:400"></span></div>
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

  const palette = document.getElementById('palette');
  palette.innerHTML = '';
  for (let i = 0; i < k; i++) {
    const s = document.createElement('div');
    s.className = 'swatch';
    s.style.background = COLORS[i];
    s.style.boxShadow = `0 2px 12px ${COLORS[i]}88`;
    s.title = NAMES[i];
    palette.appendChild(s);
  }

  const total = Math.pow(k, n);
  document.getElementById('formula').textContent = `${k}${superscript(n)} = ${total.toLocaleString()}가지`;
  document.getElementById('sub').textContent = `${k}가지 색 중 중복 허용하여 ${n}칸 배열 → ₍${k}₎Π₍${n}₎ = ${k}${superscript(n)} = ${total}`;
  document.getElementById('totalNum').textContent = total.toLocaleString();
  document.getElementById('formulaKpi').textContent = `${k}${superscript(n)}`;

  const wrap = document.getElementById('tilesWrap');
  wrap.innerHTML = '';
  const warn = document.getElementById('warn');
  const info = document.getElementById('listInfo');

  const limit = Math.min(total, MAX);
  if (total > MAX) {
    warn.textContent = `⚠ 총 ${total.toLocaleString()}가지 중 처음 ${MAX}개만 표시합니다.`;
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
      tile.style.boxShadow = `0 2px 8px ${COLORS[ci]}66`;
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
""", height=720)
    _render_quiz(_SHEET_NAME)
    _render_reflection_form(_SHEET_NAME, _GAS_URL)


def _render_quiz(sheet_name: str):
    st.divider()
    st.subheader("🧩 확인 문제")
    st.caption("활동을 바탕으로 아래 문제를 풀어보세요. 답을 입력하고 **채점하기** 버튼을 눌러주세요.")

    QUIZ = [
        {
            "q": "빨강, 파랑, 초록, 노랑 4가지 색 타일을 5칸에 배열할 때 (같은 색 반복 허용), 첫 번째 칸과 마지막 칸의 색이 서로 같아야 한다면 가능한 배열은 모두 몇 가지인지 구하시오.",
            "a": "256",
            "hint": "첫 번째 칸 4가지, 마지막 칸 1가지(첫 칸과 같으므로), 나머지 3칸 각 4가지입니다.",
            "sol": "첫 번째 칸: 4가지, 2·3·4번째 칸: 각 4가지, 마지막 칸: 첫 칸과 같아야 하므로 1가지\n\n$4 \\times 4^3 \\times 1 = 4^4 = 256$가지입니다."
        },
        {
            "q": "빨강(R), 파랑(B), 초록(G) 3가지 색 타일을 4칸에 배열할 때, 빨간색 타일이 한 개도 없는 배열의 수를 구하시오.",
            "a": "16",
            "hint": "빨간색을 제외하면 2가지 색만 사용합니다.",
            "sol": "빨간색 없이 파랑·초록 2가지만 사용 → $2^4 = 16$가지입니다."
        },
        {
            "q": "3가지 색(빨강, 파랑, 초록) 타일을 4칸에 배열할 때, 인접한 두 칸의 색이 절대 같지 않으려면 몇 가지 배열이 가능한지 구하시오. (예: 빨-파-빨-파는 가능, 빨-빨-파-초는 불가)",
            "a": "24",
            "hint": "첫 번째 칸 3가지, 이후 각 칸은 바로 이전 칸과 달라야 하므로 2가지씩 선택합니다.",
            "sol": "첫 번째 칸: 3가지, 두 번째 칸: 첫 칸과 달라야 하므로 2가지, 세 번째 칸: 두 번째와 달라야 하므로 2가지, 네 번째 칸: 세 번째와 달라야 하므로 2가지\n\n$3 \\times 2 \\times 2 \\times 2 = 3 \\times 2^3 = 24$가지입니다."
        },
    ]

    for i, item in enumerate(QUIZ):
        with st.container():
            st.markdown(f"**문제 {i+1}.** {item['q']}")
            col1, col2 = st.columns([3, 1])
            with col1:
                user_ans = st.text_input(f"답 입력 (문제 {i+1})", key=f"tile_q{i+1}", label_visibility="collapsed", placeholder="답을 입력하세요")
            with col2:
                check = st.button("채점하기", key=f"tile_check{i+1}", use_container_width=True)

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
