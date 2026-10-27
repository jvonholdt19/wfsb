(function(){var D={fdic:'https://www.fdic.gov',hud:'https://www.hud.gov',mainstreet:'https://orders.mainstreetinc.com/consumerreorder?useheader=yes&cid=2046'};
var k=new URLSearchParams(location.search).get('to'),ok=document.getElementById('sb-ok'),c=document.getElementById('sb-cancel');
if(D.hasOwnProperty(k)){ok.href=D[k];ok.target='_blank';}
c.addEventListener('click',function(e){if(history.length>1){e.preventDefault();history.back();}});})();
