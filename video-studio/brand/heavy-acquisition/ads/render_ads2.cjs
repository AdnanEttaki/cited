const { chromium } = require('playwright'); const fs=require('fs');
const icon=fs.readFileSync('../logo_icon.svg','utf8').replace(/<svg[^>]*>/,'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" style="width:100%;height:100%">');
const photo='data:image/jpeg;base64,'+fs.readFileSync('photo_clean.jpg').toString('base64');
const stripes='repeating-linear-gradient(-45deg,#FFCD11 0 22px,#111 22px 44px)';
function ad({w,h,head,sub,btn,tag,fs,pos}){const tall=h>1400;return `<style>*{margin:0;box-sizing:border-box}body{width:${w}px;height:${h}px;font-family:Inter,sans-serif;position:relative;overflow:hidden;background:#111}
.bg{position:absolute;inset:0;background:url('${photo}') center ${pos}/cover}
.top{position:absolute;left:0;right:0;top:0;height:${h*0.62}px;background:linear-gradient(180deg,rgba(17,17,17,.97) 0%,rgba(17,17,17,.88) 60%,rgba(17,17,17,0) 100%)}
.bot{position:absolute;left:0;right:0;bottom:0;height:${h*0.34}px;background:linear-gradient(0deg,rgba(17,17,17,.99) 0%,rgba(17,17,17,.94) 62%,rgba(17,17,17,0) 100%)}
.stripe{position:absolute;left:0;right:0;height:26px;background:${stripes}}
.tag{position:absolute;left:56px;top:${tall?84:70}px;background:#FFCD11;color:#111;font-weight:900;font-size:34px;letter-spacing:2px;padding:10px 22px;border-radius:8px;text-transform:uppercase}
h1{position:absolute;left:56px;right:40px;top:${tall?170:146}px;color:#fff;font-weight:900;font-size:${fs}px;line-height:.98;letter-spacing:-3px;text-transform:uppercase}
h1 em{font-style:normal;color:#FFCD11}
.sub{position:absolute;left:56px;right:56px;bottom:${tall?250:228}px;color:#fff;font-weight:800;font-size:54px;line-height:1.08;letter-spacing:-1px}
.btn{position:absolute;left:56px;bottom:${tall?96:84}px;background:#FFCD11;color:#111;font-weight:900;font-size:50px;padding:26px 62px;border-radius:14px;letter-spacing:1px}
.logo{position:absolute;right:56px;bottom:${tall?104:92}px;display:flex;align-items:center;gap:14px}
.logo .i{width:78px;height:78px}.logo .t{color:#fff;font-weight:900;font-size:34px;line-height:.95;letter-spacing:-.5px}.logo .t b{display:block;color:#FFCD11;font-size:15px;letter-spacing:5px;font-weight:800;margin-top:4px}
</style><div class="bg"></div><div class="top"></div><div class="bot"></div><div class="stripe" style="top:0"></div><div class="stripe" style="bottom:0"></div>
<div class="tag">${tag}</div><h1>${head}</h1><div class="sub">${sub}</div><div class="btn">${btn}</div><div class="logo"><div class="i">${icon}</div><div class="t">HEAVY<b>ACQUISITION</b></div></div>`;}
const tag='Excavation &amp; equipment owners';
const ads=[
 {n:'v1_question',tag,fs:112,pos:'55%',head:'Lack of <em>leads</em> limiting your business?',sub:'In 7 days, we build and launch your page, ads and follow-up.',btn:'BOOK MY CALL'},
 {n:'v2_machines',tag,fs:96,pos:'60%',head:'<em>5 machines</em> sitting. No website. No leads.',sub:'We fix that in 7 days. You just take the calls.',btn:'BOOK MY CALL'},
 {n:'v3_promise',tag,fs:112,pos:'55%',head:'<em>10 booked calls</em> in 90 days. Or you don&rsquo;t pay.',sub:'Live in 7 days. You just take the calls.',btn:'BOOK MY CALL'},
 {n:'v4_clicks',tag,fs:104,pos:'58%',head:'Paying for clicks? <em>Where do they land?</em>',sub:'Old site or Facebook page = lost leads. We fix it in 7 days.',btn:'BOOK MY CALL'}
];
(async()=>{const b=await chromium.launch();
for(const a of ads){for(const [sz,w,h] of [['4x5',1080,1350],['9x16',1080,1920]]){
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});await p.setContent(ad({w,h,...a}));await p.waitForTimeout(500);await p.screenshot({path:`${a.n}_${sz}.png`});await p.close();}}
await b.close();})();
