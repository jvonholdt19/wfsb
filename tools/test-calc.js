const fs=require('fs');const M=require('../calcmath.js');
const src=fs.readFileSync('/tmp/live/site.js','utf8');
const fn=n=>{const i=src.indexOf('function '+n+'(');let d=0,j=src.indexOf('{',i);for(let k=j;k<src.length;k++){if(src[k]=='{')d++;if(src[k]=='}'&&--d==0)return src.slice(i,k+1);}};
let els={};global.document={getElementById:id=>els[id]};global.alert=m=>{throw new Error('alert:'+m)};
eval(['floor','dosum','checkNumber','computeForm','CalcA','cwCalc'].map(fn).join('\n')+';global.O={dosum,computeForm,CalcA,cwCalc}');
let pass=0,fail=0;const eq=(name,a,b)=>{const ok=Math.abs(a-b)<1e-9;ok?pass++:fail++;console.log((ok?'PASS ':'FAIL ')+name+'  original='+a+'  concept='+b);};
for(const [y,r,l] of [[30,8.0,100000],[15,6.5,250000],[30,3.25,175000],[10,12,5000]]){els.temps={IR:{value:r},YR:{value:y},LA:{value:l},AT:{value:0},AI:{value:0},PI:{}};O.dosum();eq(`mortgage ${y}y ${r}% $${l}`,+els.temps.PI.value,M.mortgage(y,r,l));}
for(const [p,n,i] of [[20000,60,6],[10000,36,0.05],[5000,12,9.99],[150000,360,7.25]]){const f={principal:{value:String(p)},payments:{value:String(n)},interest:{value:String(i)},payment:{}};O.computeForm(f);eq(`loan $${p} ${n}pmts ${i}%`,+f.payment.value,M.loan(p,n,i));}
for(const [p,m,per,i] of [[100,12,'m',5],[250,10,'y',3.5],[50,36,'m',2.25]]){els.calform={interest:{value:String(i)},months:{value:String(m)},payment:{value:String(p)},period:{options:[{selected:per=='m'},{selected:per=='y'}]},total:{}};O.CalcA();eq(`savings $${p}/mo ${m}${per} ${i}%`,+els.calform.total.value.slice(1),M.savings(p,m,per,i));}
const debt=(b,r,p,m)=>{els={cwBalance:{value:String(b)},cwRate:{value:String(r)},cwMonthlyAmount:{value:p==null?'':String(p)},cwDesiredMonths:{value:m==null?'':String(m)},cwResult:{}};O.cwCalc();return els.cwResult.innerHTML;};
for(const [b,r,m] of [[5000,18.9,24],[2500,21,12]]){const o=debt(b,r,null,m),x=M.debtByMonths(b,r,m);const c='It will cost $'+x.monthly.toFixed(2)+' a month to pay off this card and will cost you a total of $'+x.total.toFixed(2)+'.';const ok=o===c;ok?pass++:fail++;console.log((ok?'PASS ':'FAIL ')+`debt by months $${b} ${r}% ${m}mo: `+o);}
for(const [b,r,p] of [[5000,18.9,200],[2500,21,100]]){const o=debt(b,r,p,null),x=M.debtByPayment(b,r,p);const c='It will take '+x.months+' months to pay off this card and will cost you a total of $'+x.total.toFixed(2)+'.';const ok=o===c;ok?pass++:fail++;console.log((ok?'PASS ':'FAIL ')+`debt by payment $${b} ${r}% $${p}/mo: `+o);}
console.log(`${pass} passed, ${fail} failed`);
