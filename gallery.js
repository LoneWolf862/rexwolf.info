const images=[
 {src:'assets/images/full/rubik-wolf.webp',title:'Cube Break',caption:'Rex relaxing with a Rubik’s cube.'},
 {src:'assets/images/full/rex-portrait.webp',title:'Portrait',caption:'Rex wearing glasses.'},
 {src:'assets/images/full/music-wolf.webp',title:'Lost in the Music',caption:'Headphones on, world off.'},
 {src:'assets/images/full/arcade-wolf.webp',title:'Arcade Night',caption:'Retro games and bass guitar.'}
];
let current=0; let touchStart=0;
const box=document.querySelector('.lightbox'), img=document.querySelector('#lightbox-image'), title=document.querySelector('#lightbox-title'), caption=document.querySelector('#lightbox-caption'), counter=document.querySelector('#lightbox-counter'), dl=document.querySelector('#download-link');
function render(){const item=images[current];img.src=item.src;img.alt=item.title;title.textContent=item.title;caption.textContent=item.caption;counter.textContent=`${current+1} / ${images.length}`;dl.href=item.src;dl.download=item.src.split('/').pop();}
function openAt(i){current=i;render();box.classList.add('open');box.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';document.querySelector('.close-btn').focus();}
function close(){box.classList.remove('open');box.setAttribute('aria-hidden','true');document.body.style.overflow='';}
function move(d){current=(current+d+images.length)%images.length;render();}
document.querySelectorAll('.gallery-card').forEach(b=>b.addEventListener('click',()=>openAt(Number(b.dataset.index))));
document.querySelector('.close-btn').addEventListener('click',close);document.querySelector('.prev').addEventListener('click',()=>move(-1));document.querySelector('.next').addEventListener('click',()=>move(1));
box.addEventListener('click',e=>{if(e.target===box)close();});
document.addEventListener('keydown',e=>{if(!box.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')move(-1);if(e.key==='ArrowRight')move(1);});
box.addEventListener('touchstart',e=>touchStart=e.changedTouches[0].clientX,{passive:true});box.addEventListener('touchend',e=>{const delta=e.changedTouches[0].clientX-touchStart;if(Math.abs(delta)>55)move(delta>0?-1:1);},{passive:true});
