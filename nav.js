(function(){var b=document.getElementById('menu-btn'),m=document.getElementById('site-menu');if(!b||!m)return;
function set(o){b.setAttribute('aria-expanded',String(o));m.classList.toggle('open',o);b.textContent=o?'Close':'Menu';}
b.addEventListener('click',function(){set(b.getAttribute('aria-expanded')!=='true');});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&b.getAttribute('aria-expanded')==='true'){set(false);b.focus();}});
m.addEventListener('click',function(e){if(e.target.closest('a'))set(false);});
window.addEventListener('resize',function(){if(window.innerWidth>=880)set(false);});})();
