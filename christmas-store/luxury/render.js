const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const j of process.argv.slice(2)){const [f,w]=j.split(':');
const p=await b.newPage({viewport:{width:+w,height:900},deviceScaleFactor:2});
await p.goto('file://'+__dirname+'/src/'+f+'.html',{waitUntil:'networkidle'});
await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
await p.screenshot({path:__dirname+'/images/'+f+'.png',fullPage:true});console.log('rendered',f);}
await b.close();})();
