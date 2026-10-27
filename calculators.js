(function(){
var C=window.WFSCalc;
var money=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'});
function $(id){return document.getElementById(id);}
function num(id){var v=$(id).value.replace(/[,\s$]/g,'');if(v===''||!/^\d*\.?\d+$|^\d+\.$/.test(v))return NaN;return parseFloat(v);}
function bad(out,msg,field){out.textContent=msg;if(field){$(field).setAttribute('aria-invalid','true');$(field).focus();}}
function clear(f){f.querySelectorAll('[aria-invalid]').forEach(function(x){x.removeAttribute('aria-invalid');});}
function range(out,id,label,v,lo,hi){if(isNaN(v)){bad(out,label+' field has invalid data: '+$(id).value,id);return false;}if(v<lo||v>hi){bad(out,label+' field has invalid data: '+$(id).value+' not in the range '+lo+' to '+hi,id);return false;}return true;}
var run={
 mortgage:function(){var o=$('m-out'),yr=num('m-yr'),ir=num('m-ir'),la=num('m-la');
  if(!range(o,'m-yr','Years',yr,1,50)||!range(o,'m-ir','Interest',ir,.001,99)||!range(o,'m-la','Loan Amount',la,1,99999999))return;o.textContent=money.format(C.mortgage(yr,ir,la));},
 loan:function(){var o=$('l-out'),p=num('l-p'),n=num('l-n'),i=num('l-i');
  if(!range(o,'l-p','Principal',p,100,9999999)||!range(o,'l-n','Number of Payments',n,1,480)||!range(o,'l-i','Interest',i,.001,99))return;
  if(i<1)$('l-i').value=String(i*100);o.textContent=money.format(C.loan(p,n,i));},
 savings:function(){var o=$('s-out'),p=num('s-pay'),m=num('s-mo'),i=num('s-int');
  if(isNaN(p)||isNaN(m)||isNaN(i)){bad(o,'Please fill in all of the required fields.');return;}o.textContent=money.format(C.savings(p,m,$('s-per').value,i));},
 debt:function(){var o=$('d-out'),b=num('d-bal'),r=num('d-rate'),hasP=$('d-pay').value.trim()!=='',hasM=$('d-months').value.trim()!=='';
  if(isNaN(b)){bad(o,'Please enter your credit card balance.','d-bal');return;}
  if(isNaN(r)){bad(o,"Please enter your credit card's interest rate.",'d-rate');return;}
  if(hasP===hasM){bad(o,'Please enter either a payment amount or desired months.');return;}
  if(hasM){var m=num('d-months');if(isNaN(m)||m<1){bad(o,'Please enter either a payment amount or desired months.','d-months');return;}
   var x=C.debtByMonths(b,r,m);o.textContent='It will cost $'+x.monthly.toFixed(2)+' a month to pay off this card and will cost you a total of $'+x.total.toFixed(2)+'.';}
  else{var p=num('d-pay');if(isNaN(p)||p<=0){bad(o,'Please enter either a payment amount or desired months.','d-pay');return;}
   var y=C.debtByPayment(b,r,p);if(!y){bad(o,'Your monthly payment is less than the monthly interest charged by this card.','d-pay');return;}
   o.textContent='It will take '+y.months+' months to pay off this card and will cost you a total of $'+y.total.toFixed(2)+'.';}}
};
document.querySelectorAll('form.cform').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();clear(f);run[f.getAttribute('data-calc')]();});});
var pick=$('calc-pick');
function show(){document.querySelectorAll('form.cform').forEach(function(f){f.hidden=f.getAttribute('data-calc')!==pick.value;});}
pick.addEventListener('change',show);
var q=new URLSearchParams(location.search).get('calc');if(q&&run[q]){pick.value=q;}show();
if(new URLSearchParams(location.search).get('demo')==='1'){var f=document.querySelector('form.cform:not([hidden])');f.requestSubmit();}
})();
