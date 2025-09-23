# activities/probability/random_walk_p5.py
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "랜덤워크 (p5.js)",
    "description": "p5.js로 2D 랜덤워크를 시각화합니다. 경로/걸음/속도/줌/점 크기 조절 가능.",
    "order": 50,
    "hidden": False,  # mini 폴더가 아니라면 False
}

def render():
    st.markdown("### 2D 랜덤워크 (p5.js)")
    components.html(
        """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.min.js"></script>
    <style>
      body { margin:0; }
      #wrap{ max-width: 1100px; margin: 0 auto; padding: 8px 10px 14px; }
      .ui { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
            font-size: 14px; margin-bottom: 10px; display:flex; flex-wrap:wrap; gap:8px; align-items: center; }
      .ui label{ margin-right: 4px; }
      .ui input[type="number"]{ width: 90px; }
      .pill{ background:#f3f4f6; border:1px solid #e5e7eb; padding:6px 10px; border-radius:8px; }
      .btn{ cursor:pointer; border:1px solid #d1d5db; background:#fff; border-radius:8px; padding:6px 12px; }
      .btn:active{ transform: translateY(1px); }
      #status{ font-size:13px; color:#374151; margin-left:auto; }
      canvas{ display:block; }
    </style>
  </head>
  <body>
    <div id="wrap">
      <div class="ui">
        <span class="pill">경로: <input id="paths" type="number" min="1" max="200" value="20"></span>
        <span class="pill">걸음: <input id="steps" type="number" min="10" max="20000" value="800"></span>
        <span class="pill">속도(스텝/프레임): <input id="speed" type="number" min="1" max="2000" value="50"></span>
        <span class="pill">줌: <input id="zoom" type="number" min="0.2" max="10" step="0.1" value="1.0"></span>
        <span class="pill">점 크기: <input id="dot" type="number" min="1" max="10" value="2"></span>
        <button id="reset" class="btn">리셋</button>
        <button id="rerun" class="btn">다시 그리기</button>
        <span id="status"></span>
      </div>
      <div id="sketch-holder"></div>
      <noscript>p5.js 실행을 위해 브라우저의 자바스크립트를 허용해 주세요.</noscript>
      <div id="fallback" style="display:none; color:#b91c1c; margin-top:8px;">
        p5.js가 로드되지 않았습니다. 네트워크/차단 플러그인을 확인해 주세요.
      </div>
    </div>

    <script>
      // p5 로드 체크
      if (!window.p5) {
        document.getElementById('fallback').style.display = 'block';
      }

      // 인스턴스 모드로 충돌 방지
      const s = (p) => {
        let W = 1000, H = 640;         // 캔버스 기본 크기 (Streamlit iframe 높이에 맞춤)
        let paths = 20, steps = 800, speed = 50, zoom = 1.0, dot = 2;
        let pos = [], stepLeft = 0, running = true;

        function readUI() {
          const get = (id, f) => f(document.getElementById(id).value);
          paths = Math.max(1, Math.min(200, get('paths', Number)));
          steps = Math.max(10, Math.min(20000, get('steps', Number)));
          speed = Math.max(1, Math.min(2000, get('speed', Number)));
          zoom  = Math.max(0.2, Math.min(10, get('zoom', Number)));
          dot   = Math.max(1, Math.min(10, get('dot', Number)));
        }

        function init() {
          readUI();
          pos = new Array(paths).fill(0).map(_ => ({x:0, y:0, trail:[]}));
          stepLeft = steps;
          running = true;
          p.background(255);
        }

        p.setup = () => {
          // parent 너비를 기준으로 조금 여백을 두고 캔버스 생성
          const holder = document.getElementById('sketch-holder');
          const parentW = holder.clientWidth || 1000;
          W = Math.min(1000, parentW);
          H = 640; // iframe 높이와 맞춤 (아래 components.html height 참고)
          const cnv = p.createCanvas(W, H);
          cnv.parent('sketch-holder');
          p.pixelDensity(1);
          init();

          // 버튼/입력 핸들러
          document.getElementById('reset').onclick = () => { init(); };
          document.getElementById('rerun').onclick = () => { readUI(); running = true; };
          ['paths','steps','speed','zoom','dot'].forEach(id => {
            document.getElementById(id).addEventListener('change', () => { readUI(); });
          });
        };

        p.windowResized = () => {
          const holder = document.getElementById('sketch-holder');
          const parentW = holder.clientWidth || 1000;
          W = Math.min(1000, parentW);
          p.resizeCanvas(W, H);
        };

        p.draw = () => {
          // 연한 배경으로 잔상 줄이기
          p.fill(255, 255, 255, 20);
          p.noStroke();
          p.rect(0, 0, W, H);

          // 원점 중앙
          p.push();
          p.translate(W/2, H/2);
          p.scale(zoom);

          // 다중 경로 업데이트
          p.stroke(0, 0, 0, 120);
          p.strokeWeight(dot);
          for (let i = 0; i < paths; i++) {
            const w = pos[i];
            // speed 만큼 한 프레임에 여러 스텝 수행
            let iter = Math.min(speed, stepLeft);
            while (iter-- > 0 && running) {
              const ang = Math.random() * Math.PI * 2;
              w.x += Math.cos(ang);
              w.y += Math.sin(ang);
              w.trail.push({x:w.x, y:w.y});
              if (w.trail.length > 2000) w.trail.shift();
              stepLeft--;
              if (stepLeft <= 0) running = false;
            }
            // 경로 그리기
            p.noFill();
            p.beginShape();
            for (const t of w.trail) p.vertex(t.x, t.y);
            p.endShape();
            // 현재 위치 점
            p.point(w.x, w.y);
          }
          p.pop();

          // 상태
          const done = steps - stepLeft;
          document.getElementById('status').textContent =
            `진행: ${done}/${steps}  · 경로 ${paths}개  · 줌 ${zoom.toFixed(2)}  · 점 ${dot}`;
        };
      };

      new p5(s, document.body);
    </script>
  </body>
</html>
        """,
        height=700,   # ← 캔버스가 보이도록 충분한 높이
        scrolling=True
    )
