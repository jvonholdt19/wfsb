import re,html
def txt(s): s=re.sub(r'<(script|form|style)[\s\S]*?</\1>','',s);s=re.sub(r'<[^>]+>',' ',s);return re.sub(r'\s+',' ',html.unescape(s)).strip()
ok=True
for f in ['home','about','locations','contact','online-banking','deposit-products','loan-products','other-products','order-checks','privacy-statement','speedbump']:
  l=open('/tmp/live/'+f+'.html').read();l=l[l.find('id="content">')+13:l.find('id="footer"')];l=l[:l.rfind('</div>')]
  c=txt(open(('index' if f=='home' else f)+'.html').read().split('<main')[1].split('</main>')[0])
  L=txt(l)
  if f=='speedbump': L=L.rsplit(' CANCEL',1)[0]
  # whole live text must appear contiguously in order; home allows the h1 to sit in the hero
  if f=='home':
    h1,body=L.split(' ',4)[:4],None
    parts=[txt(re.search(r'<h1>(.*?)</h1>',l,re.S).group(1)), txt(l.split('</h1>',1)[1])]
  else: parts=[L]
  res=all(p in c for p in parts); ok&=res
  print(f.ljust(18),'VERBATIM' if res else 'DIFF',sum(len(p) for p in parts),'chars')
print('ALL VERBATIM' if ok else 'PROBLEM')
