
let W,H;
const pts=Array.from({length:60},()=>({x:Math.random()*1920,y:Math.random()*1200,
  r:Math.random()*1.4+.3,s:Math.random()*.25+.08,o:Math.random()*.5+.1,d:Math.random()>.5?1:-1}));

function initBgCanvas(){
  const cv=document.getElementById('bg-cv');
  if(!cv){return;}
  const cx=cv.getContext('2d');
  if(!cx){return;}
  function rsz(){W=cv.width=window.innerWidth;H=cv.height=window.innerHeight;}
  rsz();
  window.addEventListener('resize',rsz);
  (function fr(){
    cx.clearRect(0,0,W,H);
    pts.forEach(p=>{p.o+=.004*p.d;if(p.o>.6||p.o<.05)p.d*=-1;p.y+=p.s;
      cx.beginPath();cx.arc(p.x%W,p.y%H,p.r,0,Math.PI*2);cx.fillStyle='rgba(200,180,255,'+p.o+')';cx.fill();
    });
    requestAnimationFrame(fr);
  })();
}

const visited=new Set([1]);
function updateProg(){
  const pb=document.getElementById('pb-fill');
  const pt=document.getElementById('prog-text');
  if(pb){pb.style.width=Math.round(visited.size/3*100)+'%';}
  if(pt){pt.textContent=visited.size+' / 3 파트';}
}

function openVideo(url){
  window.open(url, '_blank', 'noopener,noreferrer');
}

let tl2done=false;
function showPart(n){
  document.querySelectorAll('.part').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t=>t.classList.remove('active'));
  const part=document.getElementById('part'+n);
  const tab=document.querySelectorAll('.nav-tab')[n-1];
  if(part){part.classList.add('active');}
  if(tab){tab.classList.add('active');}
  visited.add(n);updateProg();
  if(n===2&&!tl2done)setTimeout(animTL,200);
  try{window.scrollTo({top:0,behavior:'smooth'});}catch(e){}
}
function animTL(){tl2done=true;document.querySelectorAll('#tl2 .ts').forEach((s,i)=>setTimeout(()=>s.classList.add('vis'),i*220));}

function selChar(pid,cid,card){
  const n=pid.replace('p','');
  document.querySelectorAll('#part'+n+' .cc').forEach(c=>c.classList.remove('sel'));
  card.classList.add('sel');
  document.querySelectorAll('#part'+n+' .cd').forEach(d=>d.classList.remove('show'));
  const panel=document.getElementById(pid+'-'+cid);
  if(panel){panel.classList.add('show');panel.scrollIntoView({behavior:'smooth',block:'nearest'});}
}

let battleDone=false;
function runBattle(){
  if(battleDone)return;battleDone=true;
  const btn=document.getElementById('battle-btn');
  btn.disabled=true;btn.textContent='⚔️ 대결 중…';
  let step=0;
  const iv=setInterval(()=>{step++;const tb=document.getElementById('tartag-badge');tb.style.opacity='1';tb.textContent=step+' / 30 🏅';
    if(step>=30){clearInterval(iv);document.getElementById('fior-badge').style.opacity='1';
      document.getElementById('battle-result').style.display='block';
      document.getElementById('battle-result').innerHTML='🏆 타르탈리아 완승! <strong>30 : 0</strong>';
      document.getElementById('btl-desc').style.display='block';btn.textContent='✅ 완료';}
  },60);
}

function bindQuiz(){
  document.querySelectorAll('.opt').forEach(btn=>{
    btn.addEventListener('click',function(){
      const qid=this.dataset.qid;
      document.querySelectorAll('.opt[data-qid="'+qid+'"]').forEach(b=>b.classList.remove('correct','wrong'));
      this.classList.add(this.dataset.ans==='c'?'correct':'wrong');
      const fb=document.getElementById('fb-'+qid);
      if(fb){fb.innerHTML=this.dataset.fb;fb.className='qfb show '+(this.dataset.ans==='c'?'ok':'fail');}
    });
  });
}

const gLetter=`"친구에게,

나는 5차 이상의 방정식을 왜 대수적으로 풀 수 없는가에 대해
완전히 새로운 이론을 발견했습니다.
시간이 없다… 시간이 없다…
이 편지를 가우스와 야코비에게 전해 달라.

— Évariste Galois, 1832년 5월 29일 새벽"`;
let typeIv=null,typeIdx=0;
function typeGaloisLetter(){
  const el=document.getElementById('letter-text');
  if(typeIv){clearInterval(typeIv);el.innerHTML='';typeIdx=0;}
  const txt=gLetter;
  typeIv=setInterval(()=>{if(typeIdx>=txt.length){clearInterval(typeIv);return;}typeIdx++;el.innerHTML=txt.slice(0,typeIdx).replace(/\n/g,'<br>');},28);
}

// 초기화 중 일부가 실패해도 클릭 기능은 유지되도록 분리
try{bindQuiz();}catch(e){console.error(e);}
try{updateProg();}catch(e){console.error(e);}
try{initBgCanvas();}catch(e){console.error(e);}
