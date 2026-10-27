(function(){var b=document.getElementById('menu-btn'),m=document.getElementById('site-menu');if(!b||!m)return;
b.addEventListener('click',function(){var o=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',String(!o));m.classList.toggle('open',!o);});})();
