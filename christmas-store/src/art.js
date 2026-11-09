const A={
ornament:(c='#B3202A',a='#C9A24B')=>`<svg viewBox="0 0 200 240"><path d="M100 8v26" stroke="${a}" stroke-width="3"/><circle cx="100" cy="8" r="6" fill="none" stroke="${a}" stroke-width="3"/><rect x="82" y="32" width="36" height="22" rx="4" fill="${a}"/><rect x="82" y="46" width="36" height="5" fill="rgba(0,0,0,.18)"/><circle cx="100" cy="140" r="88" fill="${c}"/><path d="M14 128c40 18 132 18 172 0" stroke="${a}" stroke-width="7" fill="none"/><path d="M18 160c40 18 124 18 164 0" stroke="${a}" stroke-width="4" fill="none" stroke-dasharray="2 10" stroke-linecap="round"/><ellipse cx="66" cy="96" rx="20" ry="30" fill="rgba(255,255,255,.28)" transform="rotate(30 66 96)"/></svg>`,
tree:(c='#16533F',a='#C9A24B')=>`<svg viewBox="0 0 200 240"><path d="M100 18l12 22 24 3-18 16 5 24-23-12-23 12 5-24-18-16 24-3z" fill="${a}"/><path d="M100 60l46 60h-22l40 52h-26l42 48H20l42-48H36l40-52H54z" fill="${c}"/><rect x="88" y="220" width="24" height="18" rx="3" fill="#6b4a2b"/><g fill="${a}"><circle cx="82" cy="112" r="6"/><circle cx="122" cy="150" r="6"/><circle cx="74" cy="182" r="6"/><circle cx="134" cy="198" r="6"/></g><g fill="#B3202A"><circle cx="112" cy="104" r="6"/><circle cx="90" cy="156" r="6"/><circle cx="110" cy="196" r="6"/></g></svg>`,
gift:(c='#B3202A',r='#C9A24B')=>`<svg viewBox="0 0 220 220"><path d="M110 58c-20-40-62-40-62-14 0 18 40 18 62 14zM110 58c20-40 62-40 62-14 0 18-40 18-62 14z" fill="none" stroke="${r}" stroke-width="10"/><rect x="24" y="58" width="172" height="40" rx="6" fill="${c}"/><rect x="38" y="96" width="144" height="110" rx="6" fill="${c}" filter="brightness(.88)"/><rect x="38" y="96" width="144" height="110" rx="6" fill="rgba(0,0,0,.12)"/><rect x="98" y="58" width="24" height="148" fill="${r}"/><rect x="24" y="90" width="172" height="8" fill="rgba(0,0,0,.15)"/></svg>`,
candle:(c='#FBF6EC',a='#B3202A')=>`<svg viewBox="0 0 200 240"><path d="M100 20c14 18 16 32 0 46-16-14-14-28 0-46z" fill="#F2B544"/><path d="M100 34c6 10 6 18 0 26-6-8-6-16 0-26z" fill="#fff6c8"/><rect x="98" y="62" width="4" height="12" fill="#333"/><rect x="62" y="74" width="76" height="140" rx="10" fill="${c}"/><rect x="62" y="120" width="76" height="34" fill="${a}"/><text x="100" y="143" text-anchor="middle" font-family="Playfair Display" font-weight="700" font-size="8.5" fill="#fff">TWINKLETREE</text><rect x="44" y="210" width="112" height="14" rx="7" fill="#C9A24B"/></svg>`,
stocking:(c='#B3202A',a='#FBF6EC')=>`<svg viewBox="0 0 200 240"><rect x="58" y="16" width="96" height="40" rx="10" fill="${a}"/><path d="M66 54h82v90c0 10 4 18 10 26l14 20c14 22-2 44-26 44H96c-30 0-50-26-38-52l8-16z" fill="${c}"/><path d="M66 100h82M66 120h82" stroke="#C9A24B" stroke-width="6"/><path d="M150 190c10 14 2 30-14 30h-26c4-18 22-30 40-30z" fill="${a}"/></svg>`,
wreath:(c='#16533F',a='#B3202A')=>`<svg viewBox="0 0 220 220"><circle cx="110" cy="110" r="74" fill="none" stroke="${c}" stroke-width="34"/><circle cx="110" cy="110" r="74" fill="none" stroke="#1d6a50" stroke-width="10" stroke-dasharray="6 14"/><g fill="${a}"><circle cx="60" cy="70" r="7"/><circle cx="160" cy="70" r="7"/><circle cx="48" cy="130" r="7"/><circle cx="172" cy="134" r="7"/><circle cx="110" cy="182" r="7"/></g><path d="M110 170l-26 36 26-10 26 10z" fill="${a}"/><circle cx="110" cy="172" r="12" fill="${a}"/><g fill="#C9A24B"><circle cx="80" cy="42" r="5"/><circle cx="140" cy="42" r="5"/><circle cx="182" cy="100" r="5"/><circle cx="38" cy="100" r="5"/></g></svg>`,
mark:(c='#C9A24B',t='#0F3D2E')=>`<svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="56" fill="${t}"/><path d="M60 18l5 10 11 1-8 7 2 11-10-5-10 5 2-11-8-7 11-1z" fill="${c}"/><path d="M60 46l16 18h-8l14 16h-9l15 16H32l15-16h-9l14-16h-8z" fill="${c}"/></svg>`,
};
document.querySelectorAll('[data-art]').forEach(el=>{const[k,...p]=el.dataset.art.split('|');el.insertAdjacentHTML('afterbegin',A[k](...p))});
document.querySelectorAll('[data-i]').forEach(el=>{
const I={truck:'<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
shield:'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
gift:'<rect x="3" y="8" width="18" height="5"/><rect x="5" y="13" width="14" height="8"/><path d="M12 8v13M12 8c-2-4-6-4-6-1.5S10 8 12 8zm0 0c2-4 6-4 6-1.5S14 8 12 8z"/>',
clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
lock:'<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>',
return:'<path d="M4 9h11a5 5 0 010 10H8"/><path d="M8 5L4 9l4 4"/>',
heart:'<path d="M12 20s-8-5-8-11a4.5 4.5 0 018-2.8A4.5 4.5 0 0120 9c0 6-8 11-8 11z"/>',
check:'<path d="M5 12.5l4.5 4.5L19 7.5"/>',
fire:'<path d="M12 3c1 4 5 5 5 10a5 5 0 01-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-4-1-6 1-9z"/>',
eye:'<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
bag:'<path d="M5 8h14l-1 13H6z"/><path d="M9 8V6a3 3 0 016 0v2"/>',
search:'<circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5"/>',
user:'<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4.5 4.5-6.5 8-6.5s7 2 8 6.5"/>',
star:'<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
pen:'<path d="M4 20l4-1L19 8l-3-3L5 16z"/>',
users:'<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-4 3.5-5.5 6.5-5.5s5.7 1.5 6.5 5.5"/><circle cx="17" cy="9" r="2.8"/><path d="M17 14.5c2.4 0 4 1.3 4.6 4.5"/>',
tag:'<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/>',
};
el.insertAdjacentHTML('afterbegin',`<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="${el.dataset.c||'currentColor'}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${I[el.dataset.i]}</svg>`)});
