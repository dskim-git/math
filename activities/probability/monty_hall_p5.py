# activities/probability/monty_hall_p5.py
from pathlib import Path
import base64
import streamlit as st
import streamlit.components.v1 as components

META = {
    "title": "몬티홀 시뮬레이터 (p5.js)",
    "description": "문을 고르고 공개 후, 유지/교체 전략의 승률을 직접 시뮬레이션해 보세요.",
    "order": 120,
}

def _img_to_data_uri(path: Path) -> str:
    """로컬 이미지를 data URI(base64)로 변환"""
    if not path.exists():
        return ""
    mime = "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"

def render():
    st.subheader("몬티홀 문제 시뮬레이터")
    st.caption("문 3개 중 하나에 자동차, 나머지 두 개에 염소. 한 문을 공개한 뒤 '유지' vs '교체' 전략의 승률을 비교해 보세요.")

    # ▶ 이미지: activities/probability/monty_hall_assets/{goat.png,car.png}
    here = Path(__file__).parent
    goat_uri = _img_to_data_uri(here / "monty_hall_assets" / "goat.png")
    car_uri  = _img_to_data_uri(here / "monty_hall_assets" / "car.png")
    if not goat_uri or not car_uri:
        st.warning("⚠️ 이미지가 없습니다. `activities/probability/monty_hall_assets/goat.png`, `car.png` 를 넣어주세요.")

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <script src="https://cdn.jsdelivr.net/npm/p5@1.9.0/lib/p5.min.js"></script>
  <style>
    html,body {{ margin:0; padding:0; overflow:hidden; font-family:sans-serif; }}
  </style>
</head>
<body>
<script>
let goatImg, carImg;

let chosenDoor = -1;
let carDoor;
let revealed = false;
let revealedDoor = -1;
let decisionMade = false;
let playerSwitched = false;
let showResult = false;

let switchWins = 0;
let stayWins = 0;
let simulations = 0;
let showStats = false;
let lastSim = "";

let isAutoPlay = false;
let autoSwitch = true;
let autoInterval = 30;
let autoTimer = 0;
let autoCount = 0;
let autoMax = 100;
let autoWinCount = 0;
let autoLossCount = 0;

let BUTTON_HEIGHT = 40;
let CANVAS_WIDTH = 900;
let CANVAS_HEIGHT = 820; // 텍스트 여유

let selectedSimCount = 0;
let strategySelection = false;

let doorOpenProgress = [0, 0, 0];
let doorRevealed = [false, false, false];

function preload() {{
  const goatURI = "{goat_uri}";
  const carURI  = "{car_uri}";
  if (goatURI) goatImg = loadImage(goatURI);
  if (carURI)  carImg  = loadImage(carURI);
}}

function setup() {{
  createCanvas(CANVAS_WIDTH, CANVAS_HEIGHT);
  textFont("sans-serif", 24);
  resetGame();
}}

function resetGame() {{
  chosenDoor = -1;
  carDoor = int(random(3));
  revealed = false;
  revealedDoor = -1;
  decisionMade = false;
  playerSwitched = false;
  showResult = false;
  showStats = false;
  selectedSimCount = 0;
  strategySelection = false;
  for (let i = 0; i < 3; i++) {{
    doorOpenProgress[i] = 0;
    doorRevealed[i] = false;
  }}
}}

function draw() {{
  background(255);
  textAlign(CENTER, CENTER);
  textSize(24);

  drawButton(width / 2 - 250, 30, "Reset");
  drawButton(width / 2 + 50, 30, isAutoPlay ? "Stop Auto" : "Auto Play");

  drawSimulationButtons();

  let startX = width / 2 - 325;
  for (let i = 0; i < 3; i++) {{
    let x = startX + i * 225;
    fill(i === chosenDoor ? color(180, 220, 255) : 240);
    rect(x, 160, 150, 250, 20);
    fill(0);
    text("Door " + (i + 1), x + 75, 430);

    if (doorRevealed[i]) {{
      doorOpenProgress[i] = min(1, doorOpenProgress[i] + 0.05);
      let img = (i === carDoor) ? carImg : goatImg;
      if (img) {{
        let imgScale = doorOpenProgress[i];
        let maxWidth = 100;
        let maxHeight = 100;
        imageMode(CENTER);
        image(img, x + 75, 285, maxWidth * imgScale, maxHeight * imgScale);
      }}
    }}
  }}

  if (showResult) {{
    fill(0);
    textSize(32);
    text((chosenDoor === carDoor) ? "🎉 You won a Car!" : "🐐 You got a Goat!", width / 2, 560);
    textSize(24);
  }}

  if (revealed && !decisionMade && !isAutoPlay) {{
    fill(200);
    rect(width / 2 - 200, 480, 150, 50);
    rect(width / 2 + 50, 480, 150, 50);
    fill(0);
    text("Stay", width / 2 - 125, 480 + BUTTON_HEIGHT / 2);
    text("Switch", width / 2 + 125, 480 + BUTTON_HEIGHT / 2);
  }}

  if (showStats) {{
    fill(0);
    text("Simulation (" + lastSim + "):", width / 2, 610);
    let wins = lastSim.includes("Switch") ? switchWins : stayWins;
    let winRate = (wins / simulations) * 100;
    text("Wins: " + wins + " / " + simulations + " (" + winRate.toFixed(2) + "%)", width / 2, 640);
  }}

  if (isAutoPlay) {{
    autoTimer++;
    if (autoTimer >= autoInterval) {{
      autoTimer = 0;
      playOneAutoGame(autoSwitch);
    }}
  }}

  if (autoCount > 0) {{
    fill(0);
    textSize(20);
    let currentRate = autoWinCount / autoCount * 100;
    text("AutoPlay: " + autoCount + " games", width / 2, 670);
    text("Wins: " + autoWinCount + " / Losses: " + autoLossCount + " (" + currentRate.toFixed(2) + "%)", width / 2, 695);
  }}
}}

function drawButton(x, y, label) {{
  fill(180);
  rect(x, y, 200, BUTTON_HEIGHT);
  fill(0);
  textSize(18);
  text(label, x + 100, y + BUTTON_HEIGHT / 2);
}}

function drawSimulationButtons() {{
  fill(200);
  rect(100, 90, 100, 40);
  rect(220, 90, 100, 40);
  rect(340, 90, 100, 40);
  rect(460, 90, 140, 40);
  fill(0);
  text("10", 150, 110);
  text("100", 270, 110);
  text("1000", 390, 110);
  text("10000", 530, 110);

  if (strategySelection) {{
    fill(180);
    rect(620, 90, 80, 40);
    rect(720, 90, 80, 40);
    fill(0);
    text("Stay", 660, 110);
    text("Switch", 760, 110);
  }}
}}

function mousePressed() {{
  if (chosenDoor === -1 && !isAutoPlay) {{
    let startX = width / 2 - 325;
    for (let i = 0; i < 3; i++) {{
      let x = startX + i * 225;
      if (mouseX > x && mouseX < x + 150 && mouseY > 160 && mouseY < 410) {{
        chosenDoor = i;
        revealGoatDoor();
      }}
    }}
  }}

  if (revealed && !decisionMade && !isAutoPlay) {{
    if (mouseX > width / 2 - 200 && mouseX < width / 2 - 50 && mouseY > 480 && mouseY < 530) {{
      decisionMade = true;
      playerSwitched = false;
      showResult = true;
      revealAllDoors();
    }} else if (mouseX > width / 2 + 50 && mouseX < width / 2 + 200 && mouseY > 480 && mouseY < 530) {{
      decisionMade = true;
      playerSwitched = true;
      for (let i = 0; i < 3; i++) {{
        if (i !== chosenDoor && i !== revealedDoor) {{
          chosenDoor = i;
          break;
        }}
      }}
      showResult = true;
      revealAllDoors();
    }}
  }}

  if (strategySelection && mouseY > 90 && mouseY < 130) {{
    if (mouseX > 620 && mouseX < 700) {{
      simulateGames(selectedSimCount, false);
      strategySelection = false;
      selectedSimCount = 0;
    }} else if (mouseX > 720 && mouseX < 800) {{
      simulateGames(selectedSimCount, true);
      strategySelection = false;
      selectedSimCount = 0;
    }}
  }}

  if (!strategySelection && mouseY > 90 && mouseY < 130) {{
    if (mouseX > 100 && mouseX < 200) selectedSimCount = 10;
    else if (mouseX > 220 && mouseX < 320) selectedSimCount = 100;
    else if (mouseX > 340 && mouseX < 440) selectedSimCount = 1000;
    else if (mouseX > 460 && mouseX < 600) selectedSimCount = 10000;
    if (selectedSimCount > 0) strategySelection = true;
  }}

  if (mouseY > 30 && mouseY < 70) {{
    if (mouseX > width / 2 - 250 && mouseX < width / 2 - 50) resetGame();
    else if (mouseX > width / 2 + 50 && mouseX < width / 2 + 250) {{
      isAutoPlay = !isAutoPlay;
      if (isAutoPlay) {{
        autoCount = 0;
        autoWinCount = 0;
        autoLossCount = 0;
        autoTimer = 0;
        autoSwitch = true;
        showStats = false;
        resetGame();
      }}
    }}
  }}
}}

function revealGoatDoor() {{
  revealed = true;
  for (let i = 0; i < 3; i++) {{
    if (i !== carDoor && i !== chosenDoor) {{
      revealedDoor = i;
      doorRevealed[i] = true;
      break;
    }}
  }}
}}

function revealAllDoors() {{
  for (let i = 0; i < 3; i++) {{
    doorRevealed[i] = true;
  }}
}}

function simulateGames(trials, switchMode) {{
  let wins = 0;
  for (let i = 0; i < trials; i++) {{
    let car = int(random(3));
    let choice = int(random(3));
    if (switchMode) {{
      for (let j = 0; j < 3; j++) {{
        if (j !== choice && j !== car) {{
          for (let k = 0; k < 3; k++) {{
            if (k !== choice && k !== j) {{
              choice = k;
              break;
            }}
          }}
          break;
        }}
      }}
    }}
    if (choice === car) wins++;
  }}
  if (switchMode) {{
    switchWins = wins;
    lastSim = "Switch";
  }} else {{
    stayWins = wins;
    lastSim = "Stay";
  }}
  simulations = trials;
  showStats = true;
}}

function playOneAutoGame(switchMode) {{
  chosenDoor = -1;
  carDoor = int(random(3));
  let choice = int(random(3));
  let reveal = -1;

  for (let i = 0; i < 3; i++) {{
    if (i !== choice && i !== carDoor) {{
      reveal = i;
      break;
    }}
  }}

  if (switchMode) {{
    for (let i = 0; i < 3; i++) {{
      if (i !== choice && i !== reveal) {{
        choice = i;
        break;
      }}
    }}
  }}

  let win = (choice === carDoor);
  if (win) autoWinCount++;
  else autoLossCount++;
  autoCount++;

  chosenDoor = choice;
  revealedDoor = reveal;
  revealed = true;
  decisionMade = true;
  playerSwitched = switchMode;
  showResult = true;
  revealAllDoors();

  if (autoCount >= autoMax) {{
    isAutoPlay = false;
    simulations = autoMax;
    lastSim = switchMode ? "Switch (Auto)" : "Stay (Auto)";
    switchWins = switchMode ? autoWinCount : 0;
    stayWins = switchMode ? 0 : autoWinCount;
    showStats = true;
  }}
}}
</script>
</body>
</html>
    """
    components.html(html, height=860, scrolling=False)
