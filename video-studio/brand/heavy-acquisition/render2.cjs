const { chromium } = require('playwright'); const fs=require('fs');
const icon = fs.readFileSync('logo_icon.svg','utf8').replace(/<svg[^>]*>/,'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" style="width:100%;height:100%">');
(async()=>{const b=await chromium.launch();
async function shot(html,w,h,out,scale=2){const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:scale});await p.setContent(html);await p.waitForTimeout(300);await p.screenshot({path:out});await p.close();}
const css=`*{margin:0;box-sizing:border-box}body{font-family:Inter,sans-serif}`;
await shot(`<style>${css}body{width:600px;height:600px;background:#111;display:flex;align-items:center;justify-content:center}</style><div style="width:420px;height:420px">${icon}</div>`,600,600,'logo_icon.png');
const lock=(dark)=>`<div style="display:flex;align-items:center;gap:36px"><div style="width:190px;height:190px">${icon}</div><div><div style="font-weight:900;font-size:118px;letter-spacing:-3px;line-height:.9;color:${dark?'#fff':'#111'}">HEAVY</div><div style="font-weight:800;font-size:46px;letter-spacing:14px;line-height:1.2;color:${dark?'#FFCD11':'#111'};${dark?'':'background:#FFCD11;display:inline-block;padding:0 14px;margin-left:-14px'}">ACQUISITION</div></div></div>`;
await shot(`<style>${css}body{width:1000px;height:400px;background:#111;display:flex;align-items:center;justify-content:center}</style>${lock(true)}`,1000,400,'logo_horizontal_dark.png');
await shot(`<style>${css}body{width:1000px;height:400px;background:#fff;display:flex;align-items:center;justify-content:center}</style>${lock(false)}`,1000,400,'logo_horizontal_light.png');
// BANNER 1640x624
const stripes=`repeating-linear-gradient(-45deg,#FFCD11 0 28px,#111 28px 56px)`;
await shot(`<style>${css}body{width:1640px;height:624px;background:#111;position:relative;overflow:hidden;color:#fff}
.stripe{position:absolute;left:0;right:0;height:38px;background:${stripes}}
.top{top:0}.bot{bottom:0}
.wrap{position:absolute;left:0;right:0;top:38px;bottom:38px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.logo{display:flex;align-items:center;gap:18px;margin-bottom:34px}
.logo .i{width:84px;height:84px}
.logo .t1{font-weight:900;font-size:50px;letter-spacing:-1px;line-height:.9;text-align:left}
.logo .t2{font-weight:800;font-size:19px;letter-spacing:6px;color:#FFCD11;text-align:left;margin-top:4px}
h1{font-weight:900;font-size:92px;letter-spacing:-2px;line-height:1;text-transform:uppercase}
h1 span{color:#FFCD11}
p{margin-top:24px;font-weight:600;font-size:30px;color:#d8d8d8;letter-spacing:.5px}
</style><div class="stripe top"></div><div class="stripe bot"></div><div class="wrap"><div class="logo"><div class="i">${icon}</div><div><div class="t1">HEAVY</div><div class="t2">ACQUISITION</div></div></div><h1>Serious buyers.<br><span>Booked calls.</span></h1><p>The lead system for equipment dealers and excavation companies.</p></div>`,1640,624,'banner_1640x624.png',1);
// PALETTE SHEET
const sw=(n,h,u,txt)=>`<div style="flex:1;display:flex;flex-direction:column"><div style="height:210px;background:${h};border:2px solid ${h=='#FFFFFF'||h=='#F4F4F2'?'#cfcfcf':h};border-radius:14px 14px 0 0"></div><div style="padding:16px 18px;background:#fff;border:2px solid #e3e3e3;border-top:0;border-radius:0 0 14px 14px;color:#111"><div style="font-weight:900;font-size:22px">${n}</div><div style="font-weight:700;font-size:20px;margin:2px 0 6px;font-family:monospace">${h}</div><div style="font-size:15px;color:#555;line-height:1.3">${u}</div></div></div>`;
await shot(`<style>${css}body{width:1600px;height:1090px;background:#f4f4f2;padding:60px;color:#111}</style>
<div style="display:flex;align-items:center;gap:20px;margin-bottom:40px"><div style="width:84px;height:84px">${icon}</div><div><div style="font-weight:900;font-size:44px;letter-spacing:-1px;line-height:1">HEAVY ACQUISITION</div><div style="font-weight:700;font-size:20px;color:#555;letter-spacing:3px">BRAND PALETTE</div></div></div>
<div style="font-weight:800;font-size:18px;letter-spacing:3px;color:#777;margin-bottom:14px">CORE</div>
<div style="display:flex;gap:22px;margin-bottom:38px">${sw('Hazard Yellow','#FFCD11','Buttons, highlights, logo mark')}${sw('Steel Black','#111111','Backgrounds, headlines, logo')}${sw('Safety White','#FFFFFF','Text on black, clean sections')}</div>
<div style="font-weight:800;font-size:18px;letter-spacing:3px;color:#777;margin-bottom:14px">SUPPORTING</div>
<div style="display:flex;gap:22px">${sw('Graphite','#2A2A2A','Cards and panels on black')}${sw('Concrete Gray','#8A8D8F','Secondary text, lines, icons')}${sw('Off-White','#F4F4F2','Light page background')}</div>
<div style="margin-top:34px;font-size:18px;color:#444;line-height:1.5"><b>Ratio:</b> ~60% black and white, ~30% gray and off-white, ~10% yellow only for what you want clicked. &nbsp; <b>Contrast:</b> black text on yellow &#10003; &nbsp;|&nbsp; yellow text on white &#10007; (use yellow on black). &nbsp; <b>Type:</b> Inter Black (capitals) for headlines, Inter for body.</div>`,1600,1090,'brand_palette.png',1);
await b.close();})();
