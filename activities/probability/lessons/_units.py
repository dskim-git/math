# activities/probability/mini/circular_perm_anchor_p5.py
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "원순열: 한 자리(한 사람) 고정하면 (n−1)!",
    "description": "p5.js로 회전 중복을 시각화하고, 한 사람을 고정해 (n−1)!이 되는 이유를 직관적으로 보여주는 미니 액티비티.",
    "order": 9999,
    # "hidden": True,
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
    .badge{display:inline-block;padding:4px 8px;border-radius:10px;border:1px solid #cbd5e1;background:#f8fafc;font-size:12px;color:#0f172a}
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
      <li><b>좌/우회전</b>을 누르면, <b>바깥 원의 ‘1’</b>에서 <b>안쪽 원의 ‘1’(맨 위)</b>까지의 <b>원호</b>와
          해당 방향으로 <b>누적한 칸 수</b>를 표시합니다.</li>
    </ul>
  </div>
</div>

<script>
let n = 6;                 // 사람 수
let seating = [];          // 시계방향 좌석에 앉은 사람 라벨(1..n)
let W = 960, H = 560;

// 회전 힌트 표시 제어
let rotHintOn = false;     // 원호/문구 표시 여부
let rotDir = null;         // 'L' | 'R' (최근에 누른 방향)
let rotCount = 0;          // 해당 방향으로 누적 누른 횟수

function factorial(k){ let r=1; for(let i=2;i<=k;i++) r*=i; return r; }
function fyShuffle(a){
  for(let i=a.length-1;i>0;i--){
    const j=Math.floor(Math.random()*(i+1));
    [a[i],a[j]]=[a[j],a[i]];
  }
}
function rotateArray(a, k){ // k>0 오른쪽(시계), k<0 왼쪽(반시계)
  const m = ((k%a.length)+a.length)%a.length;
  return a.slice(-m).concat(a.slice(0,-m));
}
function canonicalByPerson1(a){
  const idx = a.indexOf(1);
  return rotateArray(a, a.length-idx); // 1이 index 0으로 오도록 시계 회전
}

function setup(){
  let c = createCanvas(W, H);
  c.parent("canvasHolder");
  textFont("Arial");
  resetSeating();
  updateKPI();

  byId("nSel").addEventListener("input", e=>{
    n = +e.target.value;
    byId("nVal").innerText = n;
    resetSeating();
    updateKPI();
  });

  byId("shuffleBtn").addEventListener("click", ()=>{
    fyShuffle(seating);
    // 섞으면 힌트 초기화
    rotHintOn = false; rotDir = null; rotCount = 0;
  });

  byId("rotL").addEventListener("click", ()=>{
    const prevDir = rotDir;
    seating = rotateArray(seating, -1);   // 반시계 1칸
    rotDir = 'L';
    rotCount = (prevDir==='L') ? (rotCount+1) : 1;
    rotHintOn = true;
    // 정렬되면 힌트 자동 숨김
    if (seating.indexOf(1) === 0){ rotHintOn=false; }
  });

  byId("rotR").addEventListener("click", ()=>{
    const prevDir = rotDir;
    seating = rotateArray(seating, +1);   // 시계 1칸
    rotDir = 'R';
    rotCount = (prevDir==='R') ? (rotCount+1) : 1;
    rotHintOn = true;
    // 정렬되면 힌트 자동 숨김
    if (seating.indexOf(1) === 0){ rotHintOn=false; }
  });
}

function resetSeating(){
  seating = [];
  for(let i=1;i<=n;i++) seating.push(i);
  rotHintOn = false; rotDir = null; rotCount = 0;
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
  const angStep = TWO_PI / seating.length;

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
  drawSeating(seating, R1, startAng, labelColor=color(30), diskColor=color(230), bold=false);

  // 안쪽 원: 정준형(1을 위로 고정)
  const canon = canonicalByPerson1(seating);
  stroke(210); strokeWeight(2); noFill();
  circle(0,0, 2*R2);
  drawSeating(canon, R2, startAng, labelColor=color(10,80,220), diskColor=color(180,210,255), bold=true);

  // 🔶 원호 힌트: 바깥의 1 → 안쪽의 1(맨 위) 까지
  const idx1 = seating.indexOf(1);
  const aligned = (idx1 === 0);
  if (rotHintOn && rotDir && rotCount>0 && !aligned){
    const aCur = startAng + angStep * idx1; // 바깥 1의 현재 각도
    const aTop = startAng;                  // 안쪽 1의 각도(맨 위)

    stroke(220,80,0); strokeWeight(2); noFill();

    if (rotDir === 'L'){
      // 좌회전(반시계): 현재 위치 → 위쪽 방향으로 CCW
      let s = aCur, e = aTop;
      if (e <= s) e += TWO_PI; // CCW 보장
      arc(0,0, R1*1.8, R1*1.8, s, e);

      // 화살촉(끝: 위쪽)
      const hx = (R1*0.9)*cos(aTop), hy = (R1*0.9)*sin(aTop);
      push();
      translate(hx, hy);
      rotate(aTop + PI/2); // CCW 접선
      fill(220,80,0); noStroke();
      triangle(0,0, -8,-12, 8,-12);
      pop();

      // 캡션
      noStroke(); fill(220,80,0);
      textAlign(CENTER, TOP); textSize(13);
      const mid = (s+e)/2;
      text(`좌회전 ${rotCount}칸`, (R1*0.9)*cos(mid), (R1*0.9)*sin(mid)+2);

    } else if (rotDir === 'R'){
      // 우회전(시계): 현재 위치에서 위쪽까지 CW == CCW로 위쪽→현재를 그리면 시각적으로 CW
      let s = aTop, e = aCur;
      if (e <= s) e += TWO_PI; // CCW 보장(위쪽→현재)
      arc(0,0, R1*1.8, R1*1.8, s, e);

      // 화살촉(끝: 위쪽, CW 접선)
      const hx = (R1*0.9)*cos(aTop), hy = (R1*0.9)*sin(aTop);
      push();
      translate(hx, hy);
      rotate(aTop - PI/2); // CW 접선
      fill(220,80,0); noStroke();
      triangle(0,0, -8,-12, 8,-12);
      pop();

      // 캡션
      noStroke(); fill(220,80,0);
      textAlign(CENTER, TOP); textSize(13);
      const mid = (s+e)/2;
      text(`우회전 ${rotCount}칸`, (R1*0.9)*cos(mid), (R1*0.9)*sin(mid)+2);
    }
  }

  pop();

  // 정렬 완료 뱃지
  if (seating.indexOf(1) === 0){
    noStroke(); fill(20,120,60);
    textAlign(CENTER, TOP); textSize(13);
    text("정렬 완료", width/2, height-28);
  }

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

  // 사람 1 강조(링)
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
- 무작위로 섞은 뒤, 좌/우 회전을 눌러 **바깥의 1 → 안쪽의 1(맨 위)** 에 도달하기까지의 **방향(원호)** 과 **누적 칸 수**를 관찰하게 하세요.  
- 이어서 **“사람 1번을 항상 맨 위”**로 고정한 안쪽 원(정준형)을 보며, 나머지 \(n-1\)명만 순서를 정하면 되므로 **\((n-1)!\)** 이 되는 이유를 연결합니다.
        """
    )
