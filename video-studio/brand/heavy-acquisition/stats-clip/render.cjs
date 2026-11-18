const { chromium } = require('playwright'); const fs=require('fs'); const {execSync}=require('child_process');
const icon=fs.readFileSync('../logo_icon.svg','utf8').replace(/<svg[^>]*>/,'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" style="width:100%;height:100%">').replace(/`/g,'');
const html=fs.readFileSync('clip.html','utf8').replace('__ICON__',icon);
fs.writeFileSync('clip_built.html',html);
const FPS=30,DUR=13;
(async()=>{const b=await chromium.launch();
for(const [name,w,h] of [['16x9',1920,1080],['9x16',1080,1920]]){
 const dir=`frames_${name}`;fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir);
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
 await p.goto('file://'+process.cwd()+'/clip_built.html');await p.waitForTimeout(400);
 for(let f=0;f<FPS*DUR;f++){await p.evaluate(t=>window.seek(t),f/FPS);await p.screenshot({path:`${dir}/f${String(f).padStart(4,'0')}.png`});}
 await p.close();
 execSync(`ffmpeg -v error -y -framerate ${FPS} -i ${dir}/f%04d.png -c:v libx264 -pix_fmt yuv420p -crf 17 -preset medium -movflags +faststart stats_clip_${name}.mp4`);
 fs.rmSync(dir,{recursive:true,force:true});
 console.log('done',name);
}
await b.close();})();
