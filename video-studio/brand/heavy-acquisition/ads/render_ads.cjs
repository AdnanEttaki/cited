const { chromium } = require('playwright'); const fs=require('fs');
const icon=fs.readFileSync('../logo_icon.svg','utf8').replace(/<svg[^>]*>/,'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" style="width:100%;height:100%">');
const photo='data:image/jpeg;base64,'+fs.readFileSync('photo_clean.jpg').toString('base64');
const stripes='repeating-linear-gradient(-45deg,#FFCD11 0 22px,#111 22px 44px)';
function ad({w,h,head,sub,btn}){return `<style>*{margin:0;box-sizing:border-box}body{width:${w}px;height:${h}px;font-family:Inter,sans-serif;position:relative;overflow:hidden;background:#111}
.bg{position:absolute;inset:0;background:url('${photo}') center ${h>1400?'62%':'55%'}/cover}
.top{position:absolute;left:0;right:0;top:0;height:${h*0.52}px;background:linear-gradient(180deg,rgba(17,17,17,.96) 0%,rgba(17,17,17,.86) 55%,rgba(17,17,17,0) 100%)}
.bot{position:absolute;left:0;right:0;bottom:0;height:${h*0.30}px;background:linear-gradient(0deg,rgba(17,17,17,.98) 0%,rgba(17,17,17,.92) 60%,rgba(17,17,17,0) 100%)}
.stripe{position:absolute;left:0;right:0;height:26px;background:${stripes}}
h1{position:absolute;left:60px;right:60px;top:${h>1400?110:130}px;color:#fff;font-weight:900;font-size:${h>1400?92:88}px;line-height:1.0;letter-spacing:-2px;text-transform:uppercase}
h1 em{font-style:normal;color:#FFCD11}
.sub{position:absolute;left:60px;right:60px;bottom:${h>1400?250:300}px;color:#fff;font-weight:800;font-size:46px;line-height:1.1;letter-spacing:-.5px}
.sub em{font-style:normal;color:#FFCD11}
.btn{position:absolute;left:60px;bottom:${h>1400?110:150}px;background:#FFCD11;color:#111;font-weight:900;font-size:40px;padding:24px 54px;border-radius:12px;letter-spacing:1px}
.logo{position:absolute;right:60px;bottom:${h>1400?118:158}px;display:flex;align-items:center;gap:14px}
.logo .i{width:66px;height:66px}.logo .t{color:#fff;font-weight:900;font-size:30px;line-height:.95;letter-spacing:-.5px}.logo .t b{display:block;color:#FFCD11;font-size:14px;letter-spacing:5px;font-weight:800;margin-top:4px}
</style><div class="bg"></div><div class="top"></div><div class="bot"></div><div class="stripe" style="top:0"></div><div class="stripe" style="bottom:0"></div>
<h1>${head}</h1><div class="sub">${sub}</div><div class="btn">${btn}</div><div class="logo"><div class="i">${icon}</div><div class="t">HEAVY<b>ACQUISITION</b></div></div>`;}
const ads=[
 {n:'ad1_question',head:'Is a <em>lack of leads</em> the thing limiting your excavation business?',sub:'In 7 days, we build and launch your page, your ads and your follow-up.',btn:'BOOK MY CALL'},
 {n:'ad3_promise',head:'<em>10 booked calls</em> in 90 days, or you don&rsquo;t pay.',sub:'Live in 7 days. You just take the calls.',btn:'BOOK MY CALL'}
];
(async()=>{const b=await chromium.launch();
for(const a of ads){for(const [sz,w,h] of [['4x5',1080,1350],['9x16',1080,1920]]){
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});await p.setContent(ad({w,h,...a}));await p.waitForTimeout(500);await p.screenshot({path:`${a.n}_${sz}.png`});await p.close();}}
await b.close();})();
