# activities/probability/bertrand_paradox_p5.py
import streamlit as st
import streamlit.components.v1 as components
from utils import page_header

META = {
    "title": "베르트랑의 역설 (p5.js)",
    "description": "원 안에서 ‘무작위 현의 길이’가 정의에 따라 달라져 확률이 바뀌는 역설적 현상.",
    "order": 70,
}

def render():
    page_header("베르트랑의 역설 (p5.js)", "무작위 정의(방법)에 따라 ‘긴 현’의 확률이 달라진다", "🎲", top_rule=True)

    st.markdown(
        """
        **현의 길이가 내접 정삼각형의 한 변보다 ‘길다’**(longer than triangle side)일 확률을 세 가지 방법으로 비교합니다.  
        - **Method 1**: 원 위의 두 점을 균일하게 뽑아 연결 → 기대 확률 **1/3**  
        - **Method 2**: 임의의 반지름에서 중점을 균일하게 선택(반지름 거리 균일) → **1/2**  
        - **Method 3**: 원 내부에서 중점을 ‘면적 균일’로 선택 → **1/4**
        """
    )

    html = r'''
    <div id="bertrand-holder" style="width:100%;"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
    <script>
    // ====== p5.js: Bertrand's Paradox (responsive, Streamlit embed) ======
    let method = 1;
    let circleRadius = 200;
    let totalChords = 1000;
    let longerThanEquilateral = 0;
    let demoMode = false;
    let demoChord = null;
    let isLonger = false;
    let chordLayer;

    let runButton, demoButton, inputBox;
    let m1Button, m2Button, m3Button;

    // responsive canvas size
    let canvasW = 700, canvasH = 620;
    function fitSize() {
      const holder = document.getElementById('bertrand-holder');
      const w = (holder && holder.clientWidth) ? holder.clientWidth : (window.innerWidth - 32);
      canvasW = Math.min(w, 1000);
      canvasH = 620;
    }

    function setup() {
      fitSize();
      const c = createCanvas(canvasW, canvasH);
      c.parent('bertrand-holder');

      chordLayer = createGraphics(canvasW, canvasH);

      textFont('Arial');
      textStyle(NORMAL);

      // UI
      m1Button = createButton('Method 1');
      m2Button = createButton('Method 2');
      m3Button = createButton('Method 3');
      m1Button.mousePressed(()=>{method=1; runSimulation();});
      m2Button.mousePressed(()=>{method=2; runSimulation();});
      m3Button.mousePressed(()=>{method=3; runSimulation();});

      inputBox = createInput(totalChords.toString());

      runButton  = createButton('Run');
      demoButton = createButton('Show One');
      runButton.mousePressed(runSimulation);
      demoButton.mousePressed(showOneDemo);

      layoutControls();
      runSimulation();
    }

    function windowResized() {
      fitSize();
      resizeCanvas(canvasW, canvasH);
      // 그래픽 버퍼도 새 크기로 재생성 후 재그리기
      chordLayer = createGraphics(canvasW, canvasH);
      layoutControls();
      runSimulation();
    }

    function layoutControls() {
      const left = 20, top = 14, gap = 110;
      m1Button.position(left, top);
      m2Button.position(left + 120, top);
      m3Button.position(left + 240, top);

      inputBox.position(left + 380, top + 1);
      inputBox.size(90);

      runButton.position(left + 480, top);
      demoButton.position(left + 540, top);

      // 간단한 스타일
      [m1Button,m2Button,m3Button,runButton,demoButton].forEach(b=>{
        b.style('font-family','Arial');
        b.style('font-size','14px');
      });
      inputBox.style('font-family','Arial');
    }

    function showOneDemo() {
      demoChord = generateChord(method);
      isLonger = p5.Vector.dist(demoChord[0], demoChord[1]) > circleRadius * Math.sqrt(3);
      demoMode = true;
      redraw();
    }

    function draw() {
      background(255);

      // 안내
      fill(0); noStroke();
      textSize(14);
      textAlign(LEFT, TOP);
      text('1: Pick two random points on the circle.', 20, 60);
      text('2: Pick a random point on a radius (uniform along radius).', 20, 80);
      text('3: Pick a random midpoint uniformly in the disk.', 20, 100);

      const expected = (method===1? '1/3' : method===2? '1/2' : '1/4');
      text('Expected P(longer) = ' + expected, 20, 122);

      if (demoMode && demoChord) {
        image(chordLayer, 0, 0); // 기존 그림 유지
        drawSingleDemoChord();
      } else {
        image(chordLayer, 0, 0);
      }

      push();
      translate(width/2, height/2 + 70);
      // 데모가 아닐 때는 기준 도형(정삼각형+내접원) 보여주기
      if (!(demoMode && (method === 1 || method === 2))) {
        drawEquilateralTriangleWithIncircle();
      }
      noFill(); stroke(0);
      ellipse(0, 0, circleRadius*2, circleRadius*2);

      fill(0); noStroke();
      textAlign(CENTER);
      textSize(16);
      if (!demoMode) {
        const p = (totalChords>0)? (longerThanEquilateral/totalChords).toFixed(3) : '—';
        text(`Method ${method}: Probability = ${p}`, 0, circleRadius + 38);
      } else {
        text(`This chord is ${isLonger ? 'LONGER' : 'SHORTER'} than triangle side.`, 0, circleRadius + 38);
      }
      pop();
    }

    function runSimulation() {
      demoMode = false;
      totalChords = int(inputBox.value());
      longerThanEquilateral = 0;
      chordLayer.clear();

      chordLayer.push();
      chordLayer.translate(width/2, height/2 + 70);

      for (let i=0; i<totalChords; i++) {
        let chord = generateChord(method);
        let length = p5.Vector.dist(chord[0], chord[1]);
        const longer = length > circleRadius * Math.sqrt(3);
        chordLayer.stroke(longer ? color(255,0,0,60) : color(0,50));
        if (longer) longerThanEquilateral++;
        chordLayer.line(chord[0].x, chord[0].y, chord[1].x, chord[1].y);
      }
      chordLayer.pop();
      redraw();
    }

    function generateChord(method) {
      if (method === 1) {
        // 두 점을 원주에서 균일 선택
        let a1 = random(TWO_PI);
        let a2 = random(TWO_PI);
        return [
          createVector(Math.cos(a1)*circleRadius, Math.sin(a1)*circleRadius),
          createVector(Math.cos(a2)*circleRadius, Math.sin(a2)*circleRadius),
        ];
      } else if (method === 2) {
        // 반지름에서 거리 r을 균일 선택 (→ 기대 확률 1/2)
        let r = random(circleRadius);
        let ang = random(TWO_PI);
        let mid = createVector(Math.cos(ang)*r, Math.sin(ang)*r);
        let half = Math.sqrt(circleRadius*circleRadius - r*r);
        let dir = createVector(-Math.sin(ang), Math.cos(ang));
        return [
          p5.Vector.add(mid, p5.Vector.mult(dir, half)),
          p5.Vector.sub(mid, p5.Vector.mult(dir, half)),
        ];
      } else {
        // 원판에서 면적 균일 (r = R*sqrt(U)) (→ 기대 확률 1/4)
        let r = circleRadius * Math.sqrt(random(1));
        let ang = random(TWO_PI);
        let mid = createVector(Math.cos(ang)*r, Math.sin(ang)*r);
        let half = Math.sqrt(circleRadius*circleRadius - mid.magSq());
        let dir = createVector(-Math.sin(ang), Math.cos(ang));
        return [
          p5.Vector.add(mid, p5.Vector.mult(dir, half)),
          p5.Vector.sub(mid, p5.Vector.mult(dir, half)),
        ];
      }
    }

    function drawSingleDemoChord() {
      let p1 = demoChord[0], p2 = demoChord[1];
      push();
      translate(width/2, height/2 + 70);
      stroke(isLonger ? color(255, 0, 0) : color(0)); strokeWeight(2);
      line(p1.x, p1.y, p2.x, p2.y);
      strokeWeight(1);

      if (method === 1) {
        // 데모: p1, p2 각도를 이용해 기준 정삼각형 하나 표시
        let a1 = Math.atan2(p1.y, p1.x);
        let base = a1;
        let v1 = createVector(Math.cos(base)*circleRadius, Math.sin(base)*circleRadius);
        let v2 = createVector(Math.cos(base + TWO_PI/3)*circleRadius, Math.sin(base + TWO_PI/3)*circleRadius);
        let v3 = createVector(Math.cos(base + 2*TWO_PI/3)*circleRadius, Math.sin(base + 2*TWO_PI/3)*circleRadius);
        noFill(); stroke(0,150);
        beginShape(); vertex(v1.x,v1.y); vertex(v2.x,v2.y); vertex(v3.x,v3.y); endShape(CLOSE);
      } else if (method === 2) {
        drawTriangleUsingPerpendicularBisector(p1, p2);
      } else {
        // 방법 3: 중점 찍기
        let mid = p5.Vector.add(p1, p2).div(2);
        fill(0); noStroke(); ellipse(mid.x, mid.y, 8, 8);
      }
      pop();
    }

    function drawTriangleUsingPerpendicularBisector(p1, p2) {
      let mid = p5.Vector.add(p1, p2).div(2);
      let dir = p5.Vector.sub(p2, p1).normalize();
      let perp = createVector(-dir.y, dir.x);
      let d = Math.sqrt(circleRadius*circleRadius - mid.magSq());
      let inter1 = p5.Vector.add(mid, p5.Vector.mult(perp, d));
      let inter2 = p5.Vector.sub(mid, p5.Vector.mult(perp, d));
      let A = (inter1.mag() > inter2.mag()) ? inter1 : inter2;
      A.normalize().mult(circleRadius);
      let B = rotateAround(createVector(0,0), A, TWO_PI/3);
      let C = rotateAround(createVector(0,0), A, -TWO_PI/3);
      B.normalize().mult(circleRadius); C.normalize().mult(circleRadius);
      noFill(); stroke(0,150);
      beginShape(); vertex(A.x,A.y); vertex(B.x,B.y); vertex(C.x,C.y); endShape(CLOSE);
    }

    function rotateAround(center, point, ang) {
      let t = p5.Vector.sub(point, center);
      let x = t.x*Math.cos(ang) - t.y*Math.sin(ang);
      let y = t.x*Math.sin(ang) + t.y*Math.cos(ang);
      return createVector(x+center.x, y+center.y);
    }

    function drawEquilateralTriangleWithIncircle() {
      let r = circleRadius;
      let tri = [];
      for (let i=0;i<3;i++){
        let ang = -PI/2 + i*TWO_PI/3;
        tri.push(createVector(Math.cos(ang)*r, Math.sin(ang)*r));
      }
      stroke(0,150); fill(200,200,255,50);
      beginShape(); tri.forEach(p=>vertex(p.x,p.y)); endShape(CLOSE);
      let side = p5.Vector.dist(tri[0], tri[1]);
      let inR = (side*Math.sqrt(3))/6;
      let cx = (tri[0].x+tri[1].x+tri[2].x)/3;
      let cy = (tri[0].y+tri[1].y+tri[2].y)/3;
      noFill(); stroke(100,100,255);
      ellipse(cx, cy, inR*2, inR*2);
    }
    </script>
    '''
    components.html(html, height=660, scrolling=False)
