# activities/probability/mini/circular_perm_anchor_p5.py
import streamlit as st
import streamlit.components.v1 as components
import math

META = {
    "title": "원순열: 한 자리(한 사람) 고정하면 (n−1)!",
    "description": "p5.js로 회전 중복을 시각화하고, 한 사람을 고정해 (n−1)!이 되는 이유를 직관적으로 보여주는 미니 액티비티.",
    "order": 9999,  # 미니는 보통 숨김이지만, 보이게 하고 싶으면 order 조정
    # "hidden": True,  # 미니로 숨기려면 주석 해제
}

def render():
    st.header("🔁 원순열: ‘한 자리(한 사람) 고정’의 의미 (p5.js)")

    st.markdown(
        """
- **목표**: 원형 자리 배치에서 회전은 같은 배치로 본다 → **중복을 없애려면 한 사람(혹은 한 자리 기준)을 고정**하면 된다.  
- **핵심 결과**: 서로 다른 원배치 수 = **(n−1)!**  

아래 인터랙티브 그림에서 사람 **1번**을 항상 **맨 위 고정**(앵커)으로 두고, 나머지 사람의 순서만 바꿔 보세요.
    """
    )

    st.latex(r"\text{서로 다른 원배치 수} \;=\; \frac{n!}{n}\;=\;(n-1)!")

    components.html(
        """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <script src="https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.min.js"></script>
  <style>
    :root { --fg:#0f172a; --muted:#64748b; --ink:#111827;}
    body{margin:0;font-family:system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;}
    #wrap{max-width:1000px;margin:0 auto;padding:8px 10px 24px 10px;}
    .ui{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0 12px 0;}
    .ui label{font-size:14px;color:var(--muted);}
    .chip{background:#eef2ff;border:1px solid #c7d2fe;border-radius:12px;padding:4px 8px;font-size:13px;}
    .btn{padding:6px 10px;border-radius:8px;border:1px solid #cbd5e1;background:white;cursor:pointer}
    .btn:hover{background:#f8fafc}
    .btn:active{transform:translateY(1px)}
    .hstack{display:flex;gap:8px;align-items:center}
    .card{border:1px solid #e5e7eb;border-radius:12px;padding:10px;margin-top:10px}
    .note{font-size:13px;color:var(--muted)}
    canvas{border-radius:12px;border:1px solid #e5e7eb}
    .kpi{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px}
    .kpi .box{border:1px solid #e5e7eb;border-radius:12px;padding:10px;text-align:center}
    .kpi .val{font-size:22px;font-weight:700;color:var(--ink)}
    .kpi .lab{font-size:12px;color:var(--muted)}
  </style>
</head>
<body>
<div id="wrap">
  <div class="ui">
    <div class="hstack">
      <label>사람 수 n</label>
      <input id="nSel" type="range" min="3" max="12" value="6" />
      <span id="nVal" class="chip">6</span>
    </div>
    <div class="hstack">
      <button class="btn" id="shuffleBtn">무작위 섞기</button>
      <button class="btn" id="rotL">좌회전</button>
      <button class="btn" id="rotR">우회전</button>
    </div>
  </div>

  <div id="canvasHolder"></div>

  <div class="kpi">
    <div class="box">
      <div class="val" id="linCnt">720</div>
      <div class="lab">선형 배치 수 <span class="note">(n!)</span></div>
    </div>
    <div class="box">
      <div class="val" id="cirCnt">120</div>
      <div class="lab">서로 다른 원배치 수 <span class="note">((n−1)!)</span></div>
    </div>
  </div>

  <div class="card note">
    ◻︎ 시각화 방법  
    <ul>
      <li>바깥 원: 임의(무작위)로 섞은 현재 배치 (시작 좌석은 위쪽으로 표시)</li>
      <li>안쪽 원(색이 진함): 회전 중복을 제거한 <b>정준형(canonical)</b>—<b>사람 1번</b>이 항상 위쪽 고정</li>
      <li>회전 화살표는 현재 배치를 정준형으로 만들기 위해 회전한 각도를 의미(좌/우회전 눌렀을 때 표시)</li>
    </ul>
  </div>
</div>

<script>
let n = 6;                 // 사람 수
let seating = [];          // 시계방향 좌석에 앉은 사람 라벨(1..n)
let W = 960, H = 560;

// ✅ 회전 힌트(화살표/“회전 n칸”)를 표시할지 여부
let showRotationHint = false;

function factorial(k){ let r=1; for(let i=2;i<=k;i++) r*=i; return r; }

// Fisher–Yates 셔플(제자리)
function fyShuffle(a){ 
  for(let i=a.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    [a[i],a[j]]=[a[j],a[i]];
  }
}

function rotateArray(a, k){ // k>0 오른쪽 회전
  const m = ((k%a.length)+a.length)%a.length;
  return a.slice(-m).concat(a.slice(0,-m));
}

// 정준형(사람 1번을 항상 위쪽 인덱스 0으로 회전)
function canonicalByPerson1(a){
  const idx = a.indexOf(1);
  return rotateArray(a, a.length-idx); // 1이 index 0으로 오도록 오른쪽 회전
}

function setup(){
  let c = createCanvas(W, H);
  c.parent("canvasHolder");
  textFont("Arial");
  resetSeating();
  updateKPI();

  // UI 연결
  byId("nSel").addEventListener("input", e=>{
    n = +e.target.value;
    byId("nVal").innerText = n;
    resetSeating();
    updateKPI();
    showRotationHint = false;  // n 변경 시 힌트 숨김
  });

  // ✅ 무작위 섞기: 현재 배열만 섞고, 회전 힌트는 숨김
  byId("shuffleBtn").addEventListener("click", ()=>{
    fyShuffle(seating);
    showRotationHint = false;  // 섞기 후 화살표 비표시
  });

  // 좌/우 회전: 이때만 회전 힌트 표시
  byId("rotL").addEventListener("click", ()=>{
    seating = rotateArray(seating, 1);
    showRotationHint = true;
  });
  byId("rotR").addEventListener("click", ()=>{
    seating = rotateArray(seating, -1);
    showRotationHint = true;
  });
}

function resetSeating(){
  seating = [];
  for(let i=1;i<=n;i++) seating.push(i);
}

function updateKPI(){
  byId("linCnt").innerText = factorial(n).toLocaleString();
  byId("cirCnt").innerText = factorial(n-1).toLocaleString();
}

function draw(){
  background(255);
  drawRings();
}

function drawRings(){
  push();
  translate(width/2, height/2);
  noFill();

  const R1 = 210;   // 바깥 원
  const R2 = 140;   // 안쪽 원
  const startAng = -HALF_PI;   // 위쪽이 index 0

  // 기준 좌석(시작점) 마커
  stroke(160); strokeWeight(2);
  line(0, -R1-10, 0, -R1+8);
  fill(0); noStroke();
  textAlign(CENTER, BOTTOM);
  textSize(12);
  text("시작 좌석", 0, -R1-14);

  // 바깥 원: 현재 배치
  stroke(220); strokeWeight(2); noFill();
  circle(0,0, 2*R1);

  // 좌석 눈금 & 라벨
  drawSeating(seating, R1, startAng, labelColor=color(30), diskColor=color(230), bold=false);

  // 정준형(사람1을 위로 고정) — 라벨만 진하게
  const canon = canonicalByPerson1(seating);
  stroke(210); strokeWeight(2); noFill();
  circle(0,0, 2*R2);
  drawSeating(canon, R2, startAng, labelColor=color(10,80,220), diskColor=color(180,210,255), bold=true);

  // ✅ 회전 화살표(현재→정준형): 좌/우회전 버튼을 눌렀을 때만 보여준다
  if (showRotationHint){
    const idx1 = seating.indexOf(1);
    let rotStep = (n - idx1) % n;       // 오른쪽 회전 스텝
    if(rotStep!==0){
      stroke(220,80,0); strokeWeight(2); noFill();
      const a0 = startAng;
      const a1 = startAng + TWO_PI*(rotStep/n);
      arc(0,0, R1*1.8, R1*1.8, a0, a1);
      // 화살촉
      const hx = (R1*0.9)*cos(a1), hy = (R1*0.9)*sin(a1);
      push();
      translate(hx, hy);
      rotate(a1 + PI/2);
      fill(220,80,0); noStroke();
      triangle(0,0, -8,-12, 8,-12);
      pop();

      noStroke(); fill(220,80,0);
      textAlign(CENTER, TOP);
      textSize(13);
      text(`회전 ${rotStep}칸`, (R1*0.9)*cos((a0+a1)/2), (R1*0.9)*sin((a0+a1)/2)+2);
    }
  }

  pop();

  // 캡션
  noStroke(); fill(60);
  textAlign(CENTER, TOP);
  textSize(14);
  text("바깥 원: 현재 배치  ·  안쪽 원: 사람 1을 위로 고정한 정준형(회전 중복 제거)", width/2, height-30);
}

function drawSeating(arr, R, startAng, labelColor, diskColor, bold){
  const angStep = TWO_PI / arr.length;
  textAlign(CENTER, CENTER);
  for(let i=0;i<arr.length;i++){
    const a = startAng + angStep*i;
    const x = R*cos(a), y = R*sin(a);

    // 좌석 표시
    stroke(200); strokeWeight(1);
    line(x, y, 0.92*x, 0.92*y);

    // 사람(원)
    noStroke(); fill(diskColor);
    const r = (bold? 20:16);
    circle(x, y, r*2);

    // 라벨
    fill(labelColor); textSize(bold? 16: 14);
    text(arr[i], x, y+1);
  }

  // 사람 1을 강조(링)
  const idx1 = arr.indexOf(1);
  if(idx1 >= 0){
    const a1 = startAng + angStep*idx1;
    const x1 = R*cos(a1), y1 = R*sin(a1);
    noFill(); stroke(0,120,255); strokeWeight(2.2);
    circle(x1, y1, (bold? 26:22)*2);
  }
}

function byId(id){ return document.getElementById(id); }
</script>
</body>
</html>
        """,
        height=720,
    )

    st.markdown(
        """
**수업 아이디어**  
- 먼저 무작위 배치를 여러 번 섞어 본 뒤, 회전만 다르고 본질은 같은 배치가 많다는 걸 관찰시킵니다.  
- 그 다음 **“사람 1번을 항상 맨 위에”** 고정해서 중복을 없애면, 나머지 \(n-1\)명만 순서를 정하면 되므로 **\((n-1)!\)** 이 됨을 자연스럽게 연결하세요.
        """
    )
