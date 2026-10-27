/* Formulas copied from the live site's script (dosum, computeForm, CalcA, cwCalc). */
(function(root){
function floor2(e){return Math.floor(e*Math.pow(10,2))/Math.pow(10,2);}
function mortgage(yr,ir,la){var t=ir/1200,n=1,a=1+t;for(var l=0;l<yr*12;l++)n=n*a;return floor2(la*t/(1-1/n));}
function loan(principal,payments,interest){var t=interest;if(t<1)t*=100;t/=1200;var n=1;for(var a=0;a<payments;a++)n=n*(1+t);return Math.ceil(100*(principal*n*t/(n-1)))/100;}
function savings(payment,num,period,interest){var n=period==='y'?num*12:num;var t=Math.pow(interest/100+1,.0833333)-1,l=t/(t+1),a=Math.pow(t+1,n)-1;a/=l;a*=payment;return Math.trunc(a*100)/100;}
function debtByMonths(bal,rate,months){var r=rate/100/12;var o=bal*r/(1-Math.pow(1+r,-months));o=Math.round(o*100)/100;return {monthly:o,total:o*months};}
function debtByPayment(bal,rate,pay){var r=rate/100/12,u=bal,s=0;if(r*bal>=pay)return null;while(u>0){s++;u=u*(1+r)-pay;}return {months:s,total:pay*s};}
var api={mortgage:mortgage,loan:loan,savings:savings,debtByMonths:debtByMonths,debtByPayment:debtByPayment};
if(typeof module!=='undefined')module.exports=api;else root.WFSCalc=api;
})(this);
