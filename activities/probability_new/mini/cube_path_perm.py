import streamlit as st
import streamlit.components.v1 as components
import requests
import datetime

_GAS_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbwJd7W3jYTucIALzqNJUyHvmnT3nqDCEmRZXAsBlBl3IWQYhuYqyvkI3B280chlr0g/exec"
)
_SHEET_NAME = "정육면체경로순열"

META = {
    "title": "미니: 정육면체 최단경로와 같은 것이 있는 순열",
    "subject": "probability_new",
    "chapter": "같은 것이 있는 순열",
    "keywords": ["정육면체", "최단경로", "같은 것이 있는 순열", "포함-배제"],
    "hidden": True,
}


def render():
    st.header("🎲 정육면체 최단경로 탐구")
    st.caption("같은 것이 있는 순열 — 정육면체의 모서리를 따라 이동하는 최단경로의 수를 구해봅니다.")
    components.html(_build_html(), height=1100, scrolling=True)
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
        else:
            payload = {
                "sheet": sheet_name,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "학번": student_id,
                "이름": name,
                "문제1": q1, "답1": a1,
                "문제2": q2, "답2": a2,
                "문제3": q3, "답3": a3,
                "새롭게알게된점": new_learning,
                "느낀점": feeling,
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


def _build_html() -> str:
    return r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.10/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[
    {left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}
  ]})"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR',system-ui,sans-serif;background:#0e1117;color:#e0e0e0;padding:14px 10px;}

.tab-bar{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px;}
.tab-btn{padding:9px 16px;border:1px solid #3a4060;border-radius:8px;background:#1a1f35;
  color:#9ba8c5;cursor:pointer;font-size:13px;font-weight:600;transition:all .2s;}
.tab-btn.active{background:#2c4a8c;border-color:#4c8bf5;color:#fff;}
.tab-panel{display:none;}
.tab-panel.active{display:block;}

.card{background:#161a27;border:1px solid #252b42;border-radius:14px;padding:18px;margin-bottom:14px;}
h3{color:#82aaff;margin-bottom:10px;font-size:15px;font-weight:700;}
h4{color:#c3d2f5;margin-bottom:8px;font-size:13.5px;font-weight:600;}
p,li{font-size:13px;line-height:1.75;color:#c0c8de;}
ul{padding-left:18px;margin-top:4px;}

.formula-box{background:rgba(14,165,233,.08);border:1px solid rgba(14,165,233,.22);
  border-radius:12px;padding:14px 20px;margin:12px 0;text-align:center;}
.f-main{font-size:20px;font-weight:800;color:#67e8f9;margin-bottom:4px;}
.f-sub{font-size:12px;color:#7a8ea8;}

table.step{width:100%;border-collapse:collapse;font-size:13px;margin:10px 0;}
table.step th,table.step td{border:1px solid #252b42;padding:8px 10px;text-align:center;vertical-align:middle;}
table.step th{background:#1a2240;color:#82aaff;font-weight:700;}
table.step td{background:#10131e;color:#c5cfe8;}
table.step td.ans-cell{color:#6bcb77;font-weight:700;font-size:15px;}
table.step td.sub{font-size:11px;color:#7a8ea8;}
table.step input.blank-step{
  width:62px;height:28px;border:2px solid #4c8bf5;border-radius:6px;
  background:#0a0e1a;color:#e8f0ff;text-align:center;font-size:13px;font-weight:700;outline:none;
}
table.step input.blank-step.correct{border-color:#4caf50;background:#0d220d;color:#81c784;}
table.step input.blank-step.wrong{border-color:#ef5350;background:#220d0d;color:#ef9a9a;}

.answer-box{background:#0d1f0d;border:1px solid #2a5a2a;border-radius:10px;
  padding:12px 20px;margin-top:10px;text-align:center;}
.answer-box .ans{font-size:20px;font-weight:800;color:#6bcb77;}

.hl{color:#ffd166;font-weight:700;}
.note{font-size:11.5px;color:#6a7a9a;margin-top:4px;}
.note2{font-size:12px;color:#7a8ea8;margin:6px 0;}

.sub-bar{display:flex;gap:6px;margin-bottom:12px;}
.sub-btn{padding:6px 14px;border:1px solid #3a4060;border-radius:6px;
  background:#111629;color:#8a98b8;cursor:pointer;font-size:12px;font-weight:600;transition:all .2s;}
.sub-btn.active{background:#1e3a70;border-color:#4c8bf5;color:#fff;}
.sub-panel{display:none;}
.sub-panel.active{display:block;}

/* 큐브 캔버스 래퍼 */
.cube-wrap{position:relative;display:inline-block;}
canvas.cube-canvas{display:block;background:transparent;}

/* 꼭짓점 빈칸 — canvas 위 절대 위치 */
input.vblank{
  position:absolute;
  width:40px;height:22px;
  border:2px solid #4c8bf5;border-radius:5px;
  background:#0a0e1a;color:#e8f0ff;
  text-align:center;font-size:12px;font-weight:700;
  outline:none;transition:border-color .2s,background .2s;
  padding:0;
}
input.vblank:focus{border-color:#82aaff;background:#0d1228;}
input.vblank.correct{border-color:#4caf50;background:#0d220d;color:#81c784;}
input.vblank.wrong{border-color:#ef5350;background:#220d0d;color:#ef9a9a;}
input.vblank.readonly{
  background:#0a0e1a;border-color:#2a3560;color:#5a7aae;
  pointer-events:none;
}

.check-btn{padding:8px 22px;border-radius:8px;border:none;
  background:#2c5282;color:#fff;font-size:13px;font-weight:700;cursor:pointer;margin-right:8px;}
.check-btn:hover{background:#3a6db3;}
.reset-btn{padding:8px 16px;border-radius:8px;border:none;
  background:#2a1f0a;color:#e0c090;font-size:12px;cursor:pointer;}
.result-msg{font-size:13px;margin-top:8px;min-height:20px;}

/* 내외부 탭 — 간단 정육면체 그림 */
canvas.info-canvas{display:block;background:transparent;margin:0 auto;}
</style>
</head>
<body>

<div class="tab-bar">
  <button class="tab-btn active" id="btn-tab-all"  onclick="showTab('all')">① 내·외부 모두 사용</button>
  <button class="tab-btn"       id="btn-tab-outer" onclick="showTab('outer')">② 외부만 사용</button>
  <button class="tab-btn"       id="btn-tab-sum"   onclick="showTab('sum')">③ 합의 법칙</button>
</div>

<!-- ══════════════════════════════════════════════
     탭 ①: 내·외부 모두
══════════════════════════════════════════════ -->
<div id="tab-all" class="tab-panel active">
  <div class="card">
    <h3>내·외부 모서리를 모두 사용하는 경우</h3>
    <p>작은 정육면체 27개를 이어 붙인 큰 정육면체의 모든 모서리를 도로로 사용합니다.</p>
    <p style="margin-top:6px">꼭짓점 A에서 대각 꼭짓점 G까지 이동할 때: <span class="hl">가로(x) n번 + 세로(y) n번 + 높이(z) n번</span> 이동</p>
  </div>

  <div class="sub-bar">
    <button class="sub-btn active" id="btn-all-2" onclick="showAllSub(2)">2×2×2</button>
    <button class="sub-btn"       id="btn-all-3" onclick="showAllSub(3)">3×3×3</button>
  </div>

  <div id="all-2" class="sub-panel active">
    <div class="card">
      <h4>2×2×2 정육면체 — 내·외부 모두 사용</h4>
      <canvas id="all-info-2" class="info-canvas" width="340" height="300"></canvas>
      <div class="formula-box" style="margin-top:12px;">
        <div class="f-main">$$\frac{6!}{2!\,2!\,2!} = 90 \text{ 가지}$$</div>
        <div class="f-sub">가로 2번 · 세로 2번 · 높이 2번 이동 (같은 것이 있는 순열)</div>
      </div>
    </div>
  </div>

  <div id="all-3" class="sub-panel">
    <div class="card">
      <h4>3×3×3 정육면체 — 내·외부 모두 사용</h4>
      <canvas id="all-info-3" class="info-canvas" width="380" height="340"></canvas>
      <div class="formula-box" style="margin-top:12px;">
        <div class="f-main">$$\frac{9!}{3!\,3!\,3!} = 1680 \text{ 가지}$$</div>
        <div class="f-sub">가로 3번 · 세로 3번 · 높이 3번 이동 (같은 것이 있는 순열)</div>
      </div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════
     탭 ②: 외부만 사용
══════════════════════════════════════════════ -->
<div id="tab-outer" class="tab-panel">
  <div class="sub-bar">
    <button class="sub-btn active" id="btn-outer-2" onclick="showOuterSub(2)">2×2×2</button>
    <button class="sub-btn"       id="btn-outer-3" onclick="showOuterSub(3)">3×3×3</button>
  </div>

  <!-- 외부 2×2×2 -->
  <div id="outer-2" class="sub-panel active">
    <div class="card">
      <h3>2×2×2 — 외부 모서리만 사용 (포함-배제)</h3>
      <p>꼭짓점 A에서 G까지 <span class="hl">겉면 모서리만</span> 이용하는 최단경로의 수</p>
      <p class="note2">최단거리 = 6칸 (가로 2 + 세로 2 + 높이 2)</p>
      <!-- 교과서 그림 -->
      <canvas id="outer-fig-2" class="info-canvas" width="340" height="300" style="margin-top:10px;"></canvas>
    </div>
    <div class="card">
      <h4>🔍 풀이 단계 — 빈칸을 채워보세요</h4>
      <table class="step" id="outer-2-table">
        <tr><th>단계</th><th>설명</th><th>계산식</th><th>결과</th></tr>
        <tr>
          <td><span class="hl">Ⅰ단계</span></td>
          <td>지나는 두 면의 쌍 선택<br><span class="sub">(밑·앞·오른쪽 중 2개 선택)</span></td>
          <td>$3 \times 2$</td>
          <td><input class="blank-step" type="number" data-ans="6" placeholder="?">가지</td>
        </tr>
        <tr>
          <td><span class="hl">Ⅱ단계</span></td>
          <td>그 두 면 위의 경로 수<br><span class="sub">(한 방향 2번, 다른 방향 4번)</span></td>
          <td>$\dfrac{6!}{2!\times4!}$</td>
          <td><input class="blank-step" type="number" data-ans="15" placeholder="?">가지</td>
        </tr>
        <tr>
          <td>Ⅰ×Ⅱ</td>
          <td>곱의 법칙으로 합산</td>
          <td><input class="blank-step" type="number" data-ans="6" placeholder="?"> $\times$ <input class="blank-step" type="number" data-ans="15" placeholder="?"></td>
          <td><input class="blank-step" type="number" data-ans="90" placeholder="?">가지</td>
        </tr>
        <tr>
          <td><span class="hl">Ⅲ 중복</span></td>
          <td>세 면 모두 지나는 경로 (빼기)</td>
          <td>$18 + 18$</td>
          <td><input class="blank-step" type="number" data-ans="36" placeholder="?">가지</td>
        </tr>
        <tr>
          <td class="ans-cell">최종 답</td>
          <td>포함-배제 원리</td>
          <td><input class="blank-step" type="number" data-ans="90" placeholder="?"> $-$ <input class="blank-step" type="number" data-ans="36" placeholder="?"></td>
          <td><input class="blank-step" type="number" data-ans="54" placeholder="?">가지</td>
        </tr>
      </table>
      <div style="margin-top:10px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
        <button class="check-btn" onclick="checkOuterTable(2)">✓ 정답 확인</button>
        <button class="reset-btn" onclick="resetOuterTable(2)">↺ 초기화</button>
        <span id="outer-2-result" class="result-msg"></span>
      </div>
    </div>
  </div>

  <!-- 외부 3×3×3 -->
  <div id="outer-3" class="sub-panel">
    <div class="card">
      <h3>3×3×3 — 외부 모서리만 사용 (포함-배제)</h3>
      <p>꼭짓점 A에서 B까지 <span class="hl">겉면 모서리만</span> 이용하는 최단경로의 수</p>
      <p class="note2">최단거리 = 9칸 (가로 3 + 세로 3 + 높이 3)</p>
      <canvas id="outer-fig-3" class="info-canvas" width="380" height="340" style="margin-top:10px;"></canvas>
    </div>
    <div class="card">
      <h4>🔍 풀이 단계 — 빈칸을 채워보세요</h4>
      <table class="step" id="outer-3-table">
        <tr><th>단계</th><th>설명</th><th>계산식</th><th>결과</th></tr>
        <tr>
          <td><span class="hl">Ⅰ단계</span></td>
          <td>지나는 두 면의 쌍 선택</td>
          <td>$3 \times 2$</td>
          <td><input class="blank-step" type="number" data-ans="6" placeholder="?">가지</td>
        </tr>
        <tr>
          <td><span class="hl">Ⅱ단계</span></td>
          <td>그 두 면 위의 경로 수<br><span class="sub">(한 방향 3번, 다른 방향 6번)</span></td>
          <td>$\dfrac{9!}{3!\times6!}$</td>
          <td><input class="blank-step" type="number" data-ans="84" placeholder="?">가지</td>
        </tr>
        <tr>
          <td>Ⅰ×Ⅱ</td>
          <td>곱의 법칙으로 합산</td>
          <td><input class="blank-step" type="number" data-ans="6" placeholder="?"> $\times$ <input class="blank-step" type="number" data-ans="84" placeholder="?"></td>
          <td><input class="blank-step" type="number" data-ans="504" placeholder="?">가지</td>
        </tr>
        <tr>
          <td><span class="hl">Ⅲ 중복</span></td>
          <td>세 면 모두 지나는 경로</td>
          <td>$\left\{\dfrac{6!}{3!\times3!}\times1\right\}\times3\times2$</td>
          <td><input class="blank-step" type="number" data-ans="120" placeholder="?">가지</td>
        </tr>
        <tr>
          <td class="ans-cell">최종 답</td>
          <td>포함-배제 원리</td>
          <td><input class="blank-step" type="number" data-ans="504" placeholder="?"> $-$ <input class="blank-step" type="number" data-ans="120" placeholder="?"></td>
          <td><input class="blank-step" type="number" data-ans="384" placeholder="?">가지</td>
        </tr>
      </table>
      <div style="margin-top:10px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
        <button class="check-btn" onclick="checkOuterTable(3)">✓ 정답 확인</button>
        <button class="reset-btn" onclick="resetOuterTable(3)">↺ 초기화</button>
        <span id="outer-3-result" class="result-msg"></span>
      </div>
    </div>
  </div>
</div>

<!-- ══════════════════════════════════════════════
     탭 ③: 합의 법칙
══════════════════════════════════════════════ -->
<div id="tab-sum" class="tab-panel">
  <div class="card">
    <h3>③ 합의 법칙으로 구하기</h3>
    <p>각 꼭짓점까지 가는 최단경로의 수를 직접 채워보세요.</p>
    <p class="note2">이웃한 꼭짓점의 값을 더하면 다음 꼭짓점의 값을 구할 수 있습니다.</p>
  </div>
  <div class="sub-bar">
    <button class="sub-btn active" id="btn-sum-2" onclick="showSumSub(2)">2×2×2</button>
    <button class="sub-btn"       id="btn-sum-3" onclick="showSumSub(3)">3×3×3</button>
  </div>

  <div id="sum-2" class="sub-panel active">
    <div class="card">
      <h4>2×2×2 — 외부 꼭짓점별 경로 수 채우기</h4>
      <p class="note2">A(왼쪽 아래 앞)에서 G(오른쪽 위 뒤)까지의 외부 최단경로</p>
      <div class="cube-wrap" id="sum2-wrap">
        <canvas id="sum2-canvas" class="cube-canvas" width="480" height="420"></canvas>
      </div>
      <div style="margin-top:12px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
        <button class="check-btn" onclick="checkSumAnswers(2)">✓ 정답 확인</button>
        <button class="reset-btn" onclick="resetSumAnswers(2)">↺ 초기화</button>
        <span id="sum-2-result" class="result-msg"></span>
      </div>
    </div>
  </div>

  <div id="sum-3" class="sub-panel">
    <div class="card">
      <h4>3×3×3 — 외부 꼭짓점별 경로 수 채우기</h4>
      <p class="note2">A(왼쪽 아래 앞)에서 B(오른쪽 위 뒤)까지의 외부 최단경로</p>
      <div class="cube-wrap" id="sum3-wrap">
        <canvas id="sum3-canvas" class="cube-canvas" width="560" height="500"></canvas>
      </div>
      <div style="margin-top:12px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
        <button class="check-btn" onclick="checkSumAnswers(3)">✓ 정답 확인</button>
        <button class="reset-btn" onclick="resetSumAnswers(3)">↺ 초기화</button>
        <span id="sum-3-result" class="result-msg"></span>
      </div>
    </div>
  </div>
</div>

<!-- ══ JS ══ -->
<script>
// ─────────────────────────────────────────────
// 탭 전환
// ─────────────────────────────────────────────
function showTab(id) {
  ['all','outer','sum'].forEach(t=>{
    document.getElementById('tab-'+t).classList.toggle('active',t===id);
    document.getElementById('btn-tab-'+t).classList.toggle('active',t===id);
  });
  if(id==='all'){
    setTimeout(()=>{drawInfoCube(2,'all-info-2');drawInfoCube(3,'all-info-3');},60);
  }
  if(id==='outer'){
    setTimeout(()=>{drawInfoCube(2,'outer-fig-2');drawInfoCube(3,'outer-fig-3');},60);
    if(window.renderMathInElement){
      setTimeout(()=>renderMathInElement(document.getElementById('tab-outer'),{
        delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]
      }),200);
    }
  }
  if(id==='sum'){
    setTimeout(()=>drawSumCube(2),60);
  }
}
function showAllSub(n){
  [2,3].forEach(m=>{
    document.getElementById('all-'+m).classList.toggle('active',m===n);
    document.getElementById('btn-all-'+m).classList.toggle('active',m===n);
  });
  setTimeout(()=>drawInfoCube(n,'all-info-'+n),60);
}
function showOuterSub(n){
  [2,3].forEach(m=>{
    document.getElementById('outer-'+m).classList.toggle('active',m===n);
    document.getElementById('btn-outer-'+m).classList.toggle('active',m===n);
  });
  setTimeout(()=>{
    drawInfoCube(n,'outer-fig-'+n);
    if(window.renderMathInElement)
      renderMathInElement(document.getElementById('outer-'+n+'-table'),{
        delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]
      });
  },60);
}
function showSumSub(n){
  [2,3].forEach(m=>{
    document.getElementById('sum-'+m).classList.toggle('active',m===n);
    document.getElementById('btn-sum-'+m).classList.toggle('active',m===n);
  });
  setTimeout(()=>drawSumCube(n),60);
}

// ─────────────────────────────────────────────
// 투영 함수 — 교과서와 동일한 사각투시
// ─────────────────────────────────────────────
// 교과서: 왼쪽 아래 앞이 A, 오른쪽 위 뒤가 G
// 축 설정: x→오른쪽, y→위, z→안쪽(사선)
// proj(x,y,z) = (ox + x*ux + z*wx, oy - y*uy + z*wy)
function makeProj(canvas, n){
  const W=canvas.width, H=canvas.height;
  // 스케일: n에 따라 셀 크기 조정
  const cell = n===2 ? Math.min(W,H)*0.22 : Math.min(W,H)*0.17;
  // z방향 사선: 오른쪽 위로
  const wx = cell*0.55, wy = -cell*0.40;
  // 왼쪽 아래(A)를 기준점으로
  const ox = W*0.14;
  const oy = H*0.82;
  return (x,y,z)=>[ox + x*cell + z*wx, oy - y*cell + z*wy];
}

// ─────────────────────────────────────────────
// 정육면체 배경 그리기 (내·외부 info + outer fig 공용)
// ─────────────────────────────────────────────
function drawInfoCube(n, canvasId){
  const canvas=document.getElementById(canvasId);
  if(!canvas) return;
  const ctx=canvas.getContext('2d');
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const p=makeProj(canvas,n);

  // 면 채우기 순서: 앞면(왼)→ 아래면 → 왼쪽면 → 위면 → 오른면 → 뒷면(오)
  // 3면이 보이도록: 앞(z=0,pink/green), 위(y=n,blue), 오른(x=n,brown)
  // 교과서 색상 근사
  function face(pts,col,stroke){
    ctx.beginPath();
    ctx.moveTo(pts[0][0],pts[0][1]);
    for(let i=1;i<pts.length;i++) ctx.lineTo(pts[i][0],pts[i][1]);
    ctx.closePath();
    ctx.fillStyle=col; ctx.fill();
    ctx.strokeStyle=stroke||'rgba(255,255,255,0.5)';
    ctx.lineWidth=1.5; ctx.setLineDash([]); ctx.stroke();
  }

  // 앞면 z=0: x=0~n, y=0~n (분홍/초록)
  // 교과서에서 앞 왼쪽 면 = 핑크/연두, 앞 오른쪽 = 노랑
  // 단순화: 앞면 전체를 옅은 초록으로
  face([p(0,0,0),p(n,0,0),p(n,n,0),p(0,n,0)],
       'rgba(100,160,120,0.55)');
  // 내부 격자 — 앞면
  for(let i=1;i<n;i++){
    ctx.beginPath();
    ctx.moveTo(...p(i,0,0)); ctx.lineTo(...p(i,n,0));
    ctx.strokeStyle='rgba(255,255,255,0.25)'; ctx.lineWidth=0.9; ctx.setLineDash([4,4]); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(...p(0,i,0)); ctx.lineTo(...p(n,i,0));
    ctx.stroke();
  }
  ctx.setLineDash([]);

  // 위면 y=n: x=0~n, z=0~n (파랑)
  face([p(0,n,0),p(n,n,0),p(n,n,n),p(0,n,n)],
       'rgba(60,100,190,0.65)');
  for(let i=1;i<n;i++){
    ctx.beginPath();
    ctx.moveTo(...p(i,n,0)); ctx.lineTo(...p(i,n,n));
    ctx.strokeStyle='rgba(255,255,255,0.25)'; ctx.lineWidth=0.9; ctx.setLineDash([4,4]); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(...p(0,n,i)); ctx.lineTo(...p(n,n,i));
    ctx.stroke();
  }
  ctx.setLineDash([]);

  // 오른면 x=n: z=0~n, y=0~n (갈색/노랑)
  face([p(n,0,0),p(n,n,0),p(n,n,n),p(n,0,n)],
       'rgba(160,110,50,0.60)');
  for(let i=1;i<n;i++){
    ctx.beginPath();
    ctx.moveTo(...p(n,i,0)); ctx.lineTo(...p(n,i,n));
    ctx.strokeStyle='rgba(255,255,255,0.25)'; ctx.lineWidth=0.9; ctx.setLineDash([4,4]); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(...p(n,0,i)); ctx.lineTo(...p(n,n,i));
    ctx.stroke();
  }
  ctx.setLineDash([]);

  // 겉 테두리 강조
  ctx.strokeStyle='rgba(255,255,255,0.75)'; ctx.lineWidth=1.8; ctx.setLineDash([]);
  // 앞면 테두리
  ctx.beginPath(); ctx.moveTo(...p(0,0,0)); ctx.lineTo(...p(n,0,0)); ctx.lineTo(...p(n,n,0)); ctx.lineTo(...p(0,n,0)); ctx.closePath(); ctx.stroke();
  // 위면 테두리
  ctx.beginPath(); ctx.moveTo(...p(0,n,0)); ctx.lineTo(...p(n,n,0)); ctx.lineTo(...p(n,n,n)); ctx.lineTo(...p(0,n,n)); ctx.closePath(); ctx.stroke();
  // 오른면 테두리
  ctx.beginPath(); ctx.moveTo(...p(n,0,0)); ctx.lineTo(...p(n,n,0)); ctx.lineTo(...p(n,n,n)); ctx.lineTo(...p(n,0,n)); ctx.closePath(); ctx.stroke();

  // 숨겨진 모서리 점선
  ctx.strokeStyle='rgba(255,255,255,0.25)'; ctx.lineWidth=1; ctx.setLineDash([4,4]);
  ctx.beginPath(); ctx.moveTo(...p(0,0,0)); ctx.lineTo(...p(0,0,n)); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(...p(0,0,n)); ctx.lineTo(...p(n,0,n)); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(...p(0,0,n)); ctx.lineTo(...p(0,n,n)); ctx.stroke();
  ctx.setLineDash([]);

  // 보이는 모서리 실선
  ctx.strokeStyle='rgba(255,255,255,0.85)'; ctx.lineWidth=1.8;
  [[p(0,n,n),p(n,n,n)],[p(n,0,n),p(n,n,n)],[p(n,0,0),p(n,0,n)],[p(0,n,0),p(0,n,n)]].forEach(([a,b])=>{
    ctx.beginPath(); ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]); ctx.stroke();
  });

  // 꼭짓점 레이블
  ctx.font=`bold ${n===2?14:13}px sans-serif`;
  ctx.fillStyle='#ff8888';
  const [ax,ay]=p(0,0,0);
  ctx.fillText('A', ax-16, ay+5);
  ctx.fillStyle='#88ff88';
  const [gx,gy]=p(n,n,n);
  ctx.fillText(n===2?'G':'B', gx+5, gy-4);
}

// ─────────────────────────────────────────────
// DP — 외부 모서리
// ─────────────────────────────────────────────
function isOuter(x,y,z,n){return x===0||x===n||y===0||y===n||z===0||z===n;}
function vidx(x,y,z,n){return z*(n+1)*(n+1)+y*(n+1)+x;}

function computeOuterDP(n){
  const sz=(n+1)*(n+1)*(n+1);
  const dp=new Array(sz).fill(0);
  dp[vidx(0,0,0,n)]=1;
  for(let z=0;z<=n;z++) for(let y=0;y<=n;y++) for(let x=0;x<=n;x++){
    const v=dp[vidx(x,y,z,n)]; if(!v) continue;
    [[1,0,0],[0,1,0],[0,0,1]].forEach(([dx,dy,dz])=>{
      const nx=x+dx,ny=y+dy,nz=z+dz;
      if(nx>n||ny>n||nz>n) return;
      // 외부 모서리만: 두 끝점 모두 외부
      if(isOuter(x,y,z,n)&&isOuter(nx,ny,nz,n))
        dp[vidx(nx,ny,nz,n)]+=v;
    });
  }
  return dp;
}

// ─────────────────────────────────────────────
// 합의 법칙 캔버스
// 보이는 3면의 꼭짓점에만 빈칸 배치
// ─────────────────────────────────────────────
// 보이는 꼭짓점: 앞면(z=0), 위면(y=n), 오른면(x=n)
// 단, 겹치는 꼭짓점은 한 번만

const sumInputs = {};  // n → [{el,ans,x,y,z}]

function visibleVerts(n){
  const seen=new Set();
  const list=[];
  function add(x,y,z){
    const k=`${x},${y},${z}`;
    if(seen.has(k)) return;
    seen.add(k);
    list.push({x,y,z});
  }
  // 앞면 z=0
  for(let y=0;y<=n;y++) for(let x=0;x<=n;x++) add(x,y,0);
  // 위면 y=n (z >0 만)
  for(let z=1;z<=n;z++) for(let x=0;x<=n;x++) add(x,n,z);
  // 오른면 x=n (z>0, y<n 만)
  for(let z=1;z<=n;z++) for(let y=0;y<n;y++) add(n,y,z);
  return list;
}

function drawSumCube(n){
  const canvas=document.getElementById('sum'+n+'-canvas');
  if(!canvas) return;
  const ctx=canvas.getContext('2d');
  ctx.clearRect(0,0,canvas.width,canvas.height);

  const p=makeProj(canvas,n);

  // 면 그리기 (앞→위→오른 순서, 동일 로직)
  function face(pts,col){
    ctx.beginPath();
    ctx.moveTo(pts[0][0],pts[0][1]);
    for(let i=1;i<pts.length;i++) ctx.lineTo(pts[i][0],pts[i][1]);
    ctx.closePath();
    ctx.fillStyle=col; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.45)'; ctx.lineWidth=1.5; ctx.setLineDash([]); ctx.stroke();
  }

  // 앞면
  face([p(0,0,0),p(n,0,0),p(n,n,0),p(0,n,0)],'rgba(100,160,120,0.50)');
  for(let i=1;i<n;i++){
    ctx.beginPath(); ctx.moveTo(...p(i,0,0)); ctx.lineTo(...p(i,n,0));
    ctx.strokeStyle='rgba(255,255,255,0.20)'; ctx.lineWidth=0.8; ctx.setLineDash([4,4]); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(...p(0,i,0)); ctx.lineTo(...p(n,i,0)); ctx.stroke();
  }
  ctx.setLineDash([]);
  // 위면
  face([p(0,n,0),p(n,n,0),p(n,n,n),p(0,n,n)],'rgba(60,100,190,0.60)');
  for(let i=1;i<n;i++){
    ctx.beginPath(); ctx.moveTo(...p(i,n,0)); ctx.lineTo(...p(i,n,n));
    ctx.strokeStyle='rgba(255,255,255,0.20)'; ctx.lineWidth=0.8; ctx.setLineDash([4,4]); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(...p(0,n,i)); ctx.lineTo(...p(n,n,i)); ctx.stroke();
  }
  ctx.setLineDash([]);
  // 오른면
  face([p(n,0,0),p(n,n,0),p(n,n,n),p(n,0,n)],'rgba(160,110,50,0.55)');
  for(let i=1;i<n;i++){
    ctx.beginPath(); ctx.moveTo(...p(n,i,0)); ctx.lineTo(...p(n,i,n));
    ctx.strokeStyle='rgba(255,255,255,0.20)'; ctx.lineWidth=0.8; ctx.setLineDash([4,4]); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(...p(n,0,i)); ctx.lineTo(...p(n,n,i)); ctx.stroke();
  }
  ctx.setLineDash([]);

  // 숨겨진 모서리 점선
  ctx.strokeStyle='rgba(255,255,255,0.20)'; ctx.lineWidth=1; ctx.setLineDash([4,4]);
  ctx.beginPath(); ctx.moveTo(...p(0,0,0)); ctx.lineTo(...p(0,0,n)); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(...p(0,0,n)); ctx.lineTo(...p(n,0,n)); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(...p(0,0,n)); ctx.lineTo(...p(0,n,n)); ctx.stroke();
  ctx.setLineDash([]);
  // 보이는 나머지 모서리
  ctx.strokeStyle='rgba(255,255,255,0.75)'; ctx.lineWidth=1.8;
  [[p(0,n,n),p(n,n,n)],[p(n,0,n),p(n,n,n)],[p(n,0,0),p(n,0,n)],[p(0,n,0),p(0,n,n)]].forEach(([a,b])=>{
    ctx.beginPath(); ctx.moveTo(a[0],a[1]); ctx.lineTo(b[0],b[1]); ctx.stroke();
  });

  // A, G/B 레이블
  ctx.font=`bold 14px sans-serif`;
  ctx.fillStyle='#ff8888';
  const [ax,ay]=p(0,0,0); ctx.fillText('A',ax-17,ay+5);
  ctx.fillStyle='#88ff88';
  const [gx,gy]=p(n,n,n); ctx.fillText(n===2?'G':'B',gx+5,gy-5);

  // input 배치
  placeSumInputs(n, canvas, p);
}

function placeSumInputs(n, canvas, p){
  const wrap=document.getElementById('sum'+n+'-wrap');
  // 기존 input 제거
  wrap.querySelectorAll('input.vblank').forEach(e=>e.remove());

  const dp=computeOuterDP(n);
  const verts=visibleVerts(n);
  sumInputs[n]=[];

  verts.forEach(({x,y,z})=>{
    if(!isOuter(x,y,z,n)) return;
    const ans=dp[vidx(x,y,z,n)];
    const [px,py]=p(x,y,z);
    const isStart=(x===0&&y===0&&z===0);

    const inp=document.createElement('input');
    inp.type='number';
    inp.min='0';
    inp.className='vblank';
    if(isStart){ inp.value='1'; inp.classList.add('readonly'); }
    else { inp.dataset.ans=ans; inp.placeholder='?'; }

    // 꼭짓점 기준으로 약간 오른쪽 위에 배치 (겹치지 않도록 오프셋)
    inp.style.left=(px+3)+'px';
    inp.style.top=(py-28)+'px';

    wrap.appendChild(inp);
    if(!isStart) sumInputs[n].push({el:inp,ans,x,y,z});
  });
}

function checkSumAnswers(n){
  if(!sumInputs[n]||!sumInputs[n].length) return;
  let ok=0,fail=0;
  sumInputs[n].forEach(({el,ans})=>{
    el.classList.remove('correct','wrong');
    const v=parseInt(el.value);
    if(isNaN(v)||el.value==='') return;
    if(v===ans){el.classList.add('correct');ok++;}
    else{el.classList.add('wrong');fail++;}
  });
  const res=document.getElementById('sum-'+n+'-result');
  if(fail===0&&ok>0)
    res.innerHTML=`<span style="color:#6bcb77">🎉 모두 정답! (${ok}개)</span>`;
  else
    res.innerHTML=`<span style="color:#ffd166">정답 ${ok} / 오답 ${fail}</span>`;
}
function resetSumAnswers(n){
  if(!sumInputs[n]) return;
  sumInputs[n].forEach(({el})=>{
    el.value=''; el.classList.remove('correct','wrong');
  });
  document.getElementById('sum-'+n+'-result').innerHTML='';
}

// ─────────────────────────────────────────────
// 외부 풀이 단계 빈칸 확인
// ─────────────────────────────────────────────
function checkOuterTable(n){
  const table=document.getElementById('outer-'+n+'-table');
  const inputs=table.querySelectorAll('input.blank-step');
  let ok=0,fail=0;
  inputs.forEach(inp=>{
    inp.classList.remove('correct','wrong');
    const v=parseInt(inp.value);
    const ans=parseInt(inp.dataset.ans);
    if(isNaN(v)||inp.value==='') return;
    if(v===ans){inp.classList.add('correct');ok++;}
    else{inp.classList.add('wrong');fail++;}
  });
  const res=document.getElementById('outer-'+n+'-result');
  if(fail===0&&ok>0)
    res.innerHTML=`<span style="color:#6bcb77">🎉 모두 정답! (${ok}개)</span>`;
  else
    res.innerHTML=`<span style="color:#ffd166">정답 ${ok} / 오답 ${fail}</span>`;
}
function resetOuterTable(n){
  const table=document.getElementById('outer-'+n+'-table');
  table.querySelectorAll('input.blank-step').forEach(inp=>{
    inp.value=''; inp.classList.remove('correct','wrong');
  });
  document.getElementById('outer-'+n+'-result').innerHTML='';
}

// ─────────────────────────────────────────────
// 초기화
// ─────────────────────────────────────────────
window.addEventListener('load',()=>{
  // ① 탭 초기 렌더
  drawInfoCube(2,'all-info-2');
  // ③ 탭 초기 캔버스 (탭 전환 때 다시 그려짐)
  // KaTeX
  if(window.renderMathInElement)
    setTimeout(()=>renderMathInElement(document.body,{
      delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]
    }),300);
});
</script>
</body>
</html>
"""


if __name__ == "__main__":
    render()
