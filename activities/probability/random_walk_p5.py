# activities/probability/random_walk_p5.py
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "랜덤워크 (p5.js)",
    "description": "p5.js로 2D 랜덤워크를 시각화합니다. 경로/걸음 수를 조절해 보세요.",
    "order": 50,
    "hidden": False  # ← 보이고 싶으면 생략 또는 False. (mini 폴더에 넣으면 폴더 기준으로 숨김 처리됩니다)
}

def render():
    st.markdown("##### 2D 랜덤워크 (p5.js)")
    components.html(
        """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
    <style>
      body { margin:0; }
      .ui { font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; font-size:14px; margin-bottom:8px; }
      .ui > * { margin-right:8px; }
      #wrap { max-width: 900px; margin: 0 auto; }
    </style>
  </head>
  <body>
    <div id="wrap">
      <div class="ui">
        경로 개수: <input id="paths" type="number" min="1" max="200" value="20"/>
        걸음 수: <input id="steps" type="number" min="10" max="5000" value="500"/>
        속도(프레임당 걸음): <input id="speed" type="number" min="1" max="50" value="5"/>
        <button id="run">Run</button>
        <button id="reset">Reset</button>
      </div>
      <div id="sketch"></div>
    </div>

    <script>
      let walkers = [];
      let X = [], Y = [];
      let curStep = 0, maxSteps = 500, speed = 5;
      let running = false;
      let W = 900, H = 560;
      let nPaths = 20;

      function newRun() {
        nPaths = Math.max(1, Math.min(200, parseInt(document.getElementById('paths').value || '20')));
        maxSteps = Math.max(10, Math.min(5000, parseInt(document.getElementById('steps').value || '500')));
        speed = Math.max(1, Math.min(50, parseInt(document.getElementById('speed').value || '5')));

        X = Array.from({length: nPaths}, () => [0]);
        Y = Array.from({length: nPaths}, () => [0]);
        walkers = Array.from({length: nPaths}, () => ({x:0, y:0}));
        curStep = 0;
        running = true;
      }

      function resetAll() {
        X = []; Y = []; walkers = [];
        curStep = 0;
        running = false;
        clear();
        background(255);
        drawAxes();
      }

      document.getElementById('run').onclick = newRun;
      document.getElementById('reset').onclick = resetAll;

      function setup() {
        let cnv = createCanvas(W, H);
        cnv.parent(document.getElementById('sketch'));
        strokeWeight(1);
        background(255);
        drawAxes();
      }

      function drawAxes() {
        push();
        translate(W/2, H/2);
        stroke(220);
        line(-W/2, 0, W/2, 0);
        line(0, -H/2, 0, H/2);
        pop();
      }

      function draw() {
        if (!running) return;

        // 여러 걸음을 한 프레임에 진행
        for (let s = 0; s < speed && curStep < maxSteps; s++) {
          for (let i = 0; i < walkers.length; i++) {
            let ang = Math.random() * Math.PI * 2;
            walkers[i].x += Math.cos(ang);
            walkers[i].y += Math.sin(ang);
            X[i].push(walkers[i].x);
            Y[i].push(walkers[i].y);
          }
          curStep++;
        }

        // 그리기
        clear();
        background(255);
        drawAxes();

        push();
        translate(W/2, H/2);
        noFill();
        for (let i = 0; i < X.length; i++) {
          stroke(0, 120, 255, 90);
          beginShape();
          for (let k = 0; k < X[i].length; k++) {
            vertex(X[i][k], Y[i][k]);
          }
          endShape();
          // 끝점
          stroke(10, 10, 10);
          fill(10);
          circle(X[i][X[i].length-1], Y[i][Y[i].length-1], 3.5);
        }
        pop();

        if (curStep >= maxSteps) running = false;
      }
    </script>
  </body>
</html>
        """,
        height=620,
    )
