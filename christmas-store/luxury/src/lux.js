function rng(s){return()=>{s=(s*9301+49297)%233280;return s/233280}}
function heart(x,y){x*=1.25;y=-(y)*1.25+.25;return Math.pow(x*x+y*y-1,3)-x*x*y*y*y<=0}
function star(x,y){const v=[];for(let i=0;i<10;i++){const a=-Math.PI/2+i*Math.PI/5,r=i%2?.42:1;v.push([r*Math.cos(a),r*Math.sin(a)])}let c=false;for(let i=0,j=9;i<10;j=i++){const[xi,yi]=v[i],[xj,yj]=v[j];if(((yi>y)!=(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi))c=!c}return c}
function flake(x,y){const a=Math.atan2(y,x),r=Math.hypot(x,y);const arm=Math.abs(Math.sin(3*a));return (arm<.2&&r<1)||(r<.22)||(Math.abs(r-.6)<.08&&arm<.5)}
const P={
 warm:(nx,ny,R)=>{const b=.55+.45*R();return `rgba(255,${190+Math.floor(30*R())},${110+Math.floor(40*R())},${b})`},
 aurora:(nx,ny,R)=>`hsl(${(170+ny*140+nx*40)%360},90%,${58+R()*12}%)`,
 heart:(nx,ny,R)=>heart(nx*2.1,(ny-.58)*3.2)?`hsl(352,90%,${55+R()*10}%)`:`rgba(255,210,150,${.25+R()*.25})`,
 star:(nx,ny,R)=>star(nx*2,(ny-.6)*2.6)?`hsl(44,100%,${62+R()*12}%)`:`hsl(205,70%,${30+R()*14}%)`,
 snow:(nx,ny,R)=>flake(nx*2.1,(ny-.58)*3)?`rgba(255,255,255,${.8+R()*.2})`:`hsl(210,85%,${40+R()*14}%)`,
 candy:(nx,ny,R)=>(Math.floor((nx*6+ny*9)))%2?`hsl(355,85%,${50+R()*10}%)`:`rgba(255,250,240,${.75+R()*.25})`,
 forest:(nx,ny,R)=>R()<.12?`hsl(${R()<.5?0:44},95%,60%)`:`hsl(140,70%,${35+R()*18}%)`,
};
function ledTree(p='warm',rows=26,seed=7){const R=rng(seed);let s='',W=400,H=520,top=60,bot=470;
 for(let r=0;r<rows;r++){const ny=r/(rows-1),y=top+ny*(bot-top),half=(30+ny*170),n=Math.max(1,Math.round(half/7.2));
  for(let i=-n;i<=n;i++){const x=200+i*(half/n)+(R()-.5)*3,nx=(x-200)/200;const c=P[p](nx,ny,R);s+=`<circle cx="${x.toFixed(1)}" cy="${(y+(R()-.5)*3).toFixed(1)}" r="2.9" fill="${c}"/>`}}
 const id='g'+Math.floor(R()*1e6);
 return `<svg viewBox="0 0 ${W} ${H}"><defs><filter id="${id}" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter><radialGradient id="h${id}" cx="50%" cy="60%" r="50%"><stop offset="0" stop-color="#ffcf8a" stop-opacity=".18"/><stop offset="1" stop-color="#ffcf8a" stop-opacity="0"/></radialGradient></defs>
 <ellipse cx="200" cy="300" rx="210" ry="250" fill="url(#h${id})"/>
 <path d="M200 18l7 15 16 2-12 11 3 16-14-8-14 8 3-16-12-11 16-2z" fill="#F5D58A" filter="url(#${id})"/>
 <g filter="url(#${id})">${s}</g><rect x="188" y="474" width="24" height="30" fill="#2a1d14"/><ellipse cx="200" cy="506" rx="120" ry="8" fill="rgba(255,200,130,.08)"/></svg>`}
document.querySelectorAll('[data-tree]').forEach((el,k)=>{const[p,r]=el.dataset.tree.split('|');el.innerHTML=ledTree(p,+(r||26),k*13+5)});
const I={truck:'<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="17.5" r="1.6"/><circle cx="17" cy="17.5" r="1.6"/>',shield:'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',return:'<path d="M4 9h11a5 5 0 010 10H8"/><path d="M8 5L4 9l4 4"/>',lock:'<rect x="5" y="11" width="14" height="10" rx="1"/><path d="M8 11V8a4 4 0 018 0v3"/>',phone:'<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18.5h2"/>',spark:'<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>',clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',gift:'<rect x="3" y="8" width="18" height="5"/><rect x="5" y="13" width="14" height="8"/><path d="M12 8v13M12 8c-2-4-6-4-6-1.5S10 8 12 8zm0 0c2-4 6-4 6-1.5S14 8 12 8z"/>',plug:'<path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 01-12 0zM12 17v4"/>',bag:'<path d="M5 8h14l-1 13H6z"/><path d="M9 8V6a3 3 0 016 0v2"/>',check:'<path d="M5 12.5l4.5 4.5L19 7.5"/>',plus:'<path d="M12 5v14M5 12h14"/>',minus:'<path d="M5 12h14"/>',music:'<path d="M9 18V5l11-2v13"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="17.5" cy="16" r="2.5"/>',timer:'<circle cx="12" cy="13" r="8"/><path d="M12 9v4M9 2h6"/>',search:'<circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5"/>',user:'<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4.5 4.5-6.5 8-6.5s7 2 8 6.5"/>'};
document.querySelectorAll('[data-i]').forEach(el=>el.insertAdjacentHTML('afterbegin',`<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="${el.dataset.c||'currentColor'}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">${I[el.dataset.i]}</svg>`));
