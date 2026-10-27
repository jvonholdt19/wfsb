# Rebuilds pages from the live site's #content (verbatim text), sanitized for the strict CSP.
import re, html
from html.parser import HTMLParser
from urllib.parse import unquote
L='/tmp/live/'; OUT='/workspace/wfs-concept/'
KEEP_ATTR={'href','colspan','rowspan','id'}
DROP_WITH_CONTENT={'script','form','style'}
VOID={'br','hr','img','input'}
SB_OK={'www.fdic.gov':'https://www.fdic.gov','www.hud.gov':'https://www.hud.gov','orders.mainstreetinc.com/consumerreorder?useheader=yes&cid=2046':'https://orders.mainstreetinc.com/consumerreorder?useheader=yes&cid=2046'}
def maplink(h):
  if h.startswith('#'): return h
  if h.startswith('/speedbump'):
    link=unquote(re.search(r'link=([^&]*)',h).group(1));key=link.lower()
    k={'www.fdic.gov':'fdic','www.hud.gov':'hud'}.get(key,'mainstreet' if 'mainstreetinc' in key else None)
    return 'speedbump.html?to='+k
  if h=='/': return 'index.html'
  if h.startswith('/pdf/'): return 'https://www.worthingtonfederalsavings.com'+h
  if h.startswith('/'): return h[1:]+'.html'
  return h
class San(HTMLParser):
  def __init__(s): super().__init__(convert_charrefs=False); s.o=[]; s.skip=0
  def handle_starttag(s,t,a):
    if s.skip or t in DROP_WITH_CONTENT:
      if t in DROP_WITH_CONTENT and t not in VOID: s.skip+=1
      return
    if t in ('img','input'): return
    attrs=[]
    for k,v in a:
      if t=='a' and k=='name': attrs.append(('id',v))
      elif k in KEEP_ATTR: attrs.append((k,maplink(v) if k=='href' else v))
    if t=='a' and any(k=='href' and v.startswith('http') for k,v in attrs): attrs.append(('rel','noopener'))
    s.o.append('<'+t+''.join(f' {k}="{html.escape(v)}"' for k,v in attrs)+'>')
  def handle_startendtag(s,t,a): s.handle_starttag(t,a)
  def handle_endtag(s,t):
    if t in DROP_WITH_CONTENT:
      if s.skip: s.skip-=1
      return
    if s.skip or t in VOID: return
    s.o.append(f'</{t}>')
  def handle_data(s,d):
    if not s.skip: s.o.append(d)
  def handle_entityref(s,n):
    if not s.skip: s.o.append(f'&{n};')
  def handle_charref(s,n):
    if not s.skip: s.o.append(f'&#{n};')
def content(name):
  s=open(L+name+'.html').read(); i=s.find('id="content">')+len('id="content">'); j=s.find('id="footer"')
  body=s[i:j]; body=body[:body.rfind('</div>')]
  p=San(); p.feed(body); out=''.join(p.o)
  return re.sub(r'<p>\s*</p>','',out).strip()

src=open(OUT+'index.html').read()
footer=re.search(r'<footer>.*?</footer>',src,re.S).group(0)
footer=re.sub(r'<div class="comp">.*?</div>','<div class="comp"><a href="speedbump.html?to=fdic">Member FDIC</a><a href="speedbump.html?to=hud">Equal Housing Lender</a></div>',footer,flags=re.S)
footer=re.sub(r'<p><a href="privacy-statement.html">.*?</p>','<p><a href="index.html">Links</a> | <a href="privacy-statement.html">Privacy Statement</a> | <a href="speedbump.html?to=mainstreet">Reorder Checks</a> | <a href="accessibility.html">Accessibility Statement</a></p>',footer,flags=re.S)
footer=footer.replace('Compliance text placeholders — official FDIC and Equal Housing Lender notices go here on the live site.','Concept note: FDIC and Equal Housing Lender badges are text placeholders; the official artwork goes here on the live site.')
footer=re.sub(r'<p class="credits">.*?</p>','<p class="credits">Photos via Wikimedia Commons: Worthington City Hall by Myotus (CC BY 4.0); Jackson by AlexiusHoratius (CC BY-SA 3.0); house by Myotus (CC BY-SA 4.0); smartphone by Océanos y dados (CC0); prairie photos by Mike Budd/U.S. Fish and Wildlife Service (public domain). Images resized. Fonts: Fraunces &amp; Inter (SIL OFL 1.1).</p>',footer,flags=re.S)
PRIMARY=[('index.html','Home'),('online-banking.html','Online Banking'),('deposit-products.html','Deposit Products'),('loan-products.html','Loan Products'),('other-products.html','Other Products &amp; Services')]
UTIL=[('about.html','About'),('locations.html','Locations'),('contact.html','Contact'),('calculators.html','Calculators'),('order-checks.html','Order Checks')]
def head(title,cur):
  ac=lambda h:' aria-current="page"' if h==cur else ''
  pn=''.join(f'<a href="{h}"{ac(h)}>{t}</a>' for h,t in PRIMARY); un=''.join(f'<a href="{h}"{ac(h)}>{t}</a>' for h,t in UTIL)
  return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{title} — Worthington Federal Savings Bank (Design Concept)</title>
<link rel="preload" href="fonts/fraunces-700.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="style.css"></head><body>
<div class="concept" role="note">Design concept prepared by NWIM Project Management for Worthington Federal Savings — not the official bank website.</div>
<nav class="util" aria-label="Secondary"><div class="wrap">{un}</div></nav>
<header><div class="wrap"><a class="mark" href="index.html"><svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true"><rect width="34" height="34" rx="8" fill="#0d2c40"/><text x="17" y="23" text-anchor="middle" font-family="Georgia,serif" font-size="17" font-weight="700" fill="#e9b25c">W</text></svg><span>Worthington Federal<small>Savings Bank</small></span></a>
<button class="menu-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="site-menu">Menu</button>
<nav class="primary" id="site-menu" aria-label="Main">{pn}<div class="menu-util">{un}</div></nav></div></header>'''
def page(fn,title,body,scripts=()):
  sc=''.join(f'<script src="{x}"></script>' for x in ('nav.js',)+tuple(scripts))
  open(OUT+fn,'w').write(head(title,fn)+'\n<main id="top">'+body+'</main>\n'+footer+'\n'+sc+'</body></html>\n')
def split_h1(c):
  m=re.match(r'\s*<h1>(.*?)</h1>(.*)',c,re.S); return m.group(1).strip(),m.group(2)
def inner(c,cls=''):
  h1,rest=split_h1(c)
  return f'<div class="page-hero"><div class="wrap"><h1>{h1}</h1></div></div><section><div class="wrap copy {cls}">{rest}</div></section>'

# HOME (rich design; all claims quoted from the bank's own pages)
h1,rest=split_h1(content('home'))
hero=re.search(r'<form class="card" id="login".*?</form>',src,re.S).group(0).replace('<button type="submit">Log in</button>','<button type="submit">Login</button>')
quick=open('/tmp/quick.html').read()
for a,b in [('Personal banking','Deposit Products'),('>Loans<','>Loan Products<'),('Online &amp; Mobile banking','Online Banking'),('Locations &amp; hours','Locations')]: quick=quick.replace(a,b)
ICON_LOAN='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3"/></svg>'
ICON_HEART='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21l-8-8a5 5 0 017-7l1 1 1-1a5 5 0 017 7z"/></svg>'
ICON_HOUSE='<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V9l7-5 7 5v12M10 21v-6h4v6"/></svg>'
CTA='''<div class="cta"><div class="wrap"><div><h2>Visit us at any of our three locations</h2><p>Please contact us or visit one of our locations for more information on any of the loan products listed above.</p></div><div><a class="btn" href="contact.html">Contact</a><a class="btn ghost" href="locations.html">Locations</a></div></div></div>'''
CTA_SIMPLE='''<div class="cta"><div class="wrap"><div><h2>Visit us at any of our three locations</h2></div><div><a class="btn" href="contact.html">Contact</a><a class="btn ghost" href="locations.html">Locations</a></div></div></div>'''
cards=f'''<section id="personal"><div class="wrap"><div class="center"><h2>How can we help?</h2></div><div class="cards">
<article class="pcard"><img src="images/personal.webp" alt="Yellow prairie coneflowers against a Minnesota prairie sunset" width="900" height="600" loading="lazy"><div><h3>Personal banking</h3><ul><li>Checking</li><li>Savings</li><li>Certificate of Deposit</li><li>IRA</li></ul><a href="deposit-products.html">Deposit Products →</a></div></article>
<article class="pcard"><img src="images/home.webp" alt="A brown two-story house with a red front door and an enclosed porch" width="900" height="563" loading="lazy"><div><h3>Loans</h3><p>We do not sell our mortgages to a third party. Therefore, when you have a question, you have a local person to contact.</p><a href="loan-products.html">Loan Products →</a></div></article>
<article class="pcard"><img src="images/phone.webp" alt="A person using a smartphone" width="900" height="563" loading="lazy"><div><h3>Online &amp; Mobile banking</h3><p>Our Online Banking gives you 24 hour, 7 days a week access to your checking, savings, money market, certificate of deposit, and loan accounts from your home, office computer or on your electronic device.</p><a href="online-banking.html">Online Banking →</a></div></article>
</div></div></section>'''
why=f'''<section class="why" aria-labelledby="wh"><div class="wrap"><div class="center"><h2 id="wh">Why bank local</h2></div><div class="grid3">
<div class="pt"><span class="ic" aria-hidden="true">{ICON_LOAN}</span><h3>Loans serviced locally</h3><p>We do not sell our mortgages to a third party. Therefore, when you have a question, you have a local person to contact.</p></div>
<div class="pt"><span class="ic" aria-hidden="true">{ICON_HEART}</span><h3>Friendly, knowledgeable staff</h3><p>The one thing that hasn’t changed is the friendly, knowledgeable staff you’ve come to know.</p></div>
<div class="pt"><span class="ic" aria-hidden="true">{ICON_HOUSE}</span><h3>Since 1935</h3><p>On March 30th, 1935, the first loan went on the books and was in the amount of $800.00. This was the beginning of our service to Worthington and the surrounding communities.</p></div></div></div></section>'''
merger='''<section class="merger" id="jackson"><div class="wrap split"><img src="images/jackson.webp" alt="Downtown street in Jackson, Minnesota (town photo, not the bank)" width="1200" height="601" loading="lazy"><div>
<h2>Welcome, Jackson Federal customers</h2><p>On August 27, 2025, Jackson Federal Savings and Loan Association merged with Worthington Federal Savings Bank. The complete merger happened on March 16th, 2026, so our customers now have the ability to conduct their banking business at any of our three locations.</p>
<ol class="timeline"><li><b>August 27, 2025</b></li><li><b>March 16th, 2026</b></li></ol>
<a class="btn" href="locations.html">Locations</a></div></div></section>'''
locs='''<section id="locations"><div class="wrap"><div class="center"><h2>Office Locations &amp; Hours</h2></div><div class="cards">
<article class="loc"><img src="images/worthington.webp" alt="Worthington City Hall, Worthington, Minnesota (town photo, not the bank)" width="900" height="506" loading="lazy"><div class="b"><h3>WORTHINGTON LOCATION</h3><p>PO Box 339, 418 11th Street<br>Worthington, MN 56187<br>Phone <a href="tel:5073722131">507-372-2131</a><br>Toll Free <a href="tel:8009146023">800-914-6023</a></p><p><strong>LOBBY HOURS OF OPERATION</strong><br>Monday-Friday 8:30-4:00</p><p><strong>DRIVE UP HOURS OF OPERATION</strong><br>Monday-Thursday 8:30-4:00<br>Friday 8:30-5:00</p><p>Drive Up ATM Available 24/7</p></div></article>
<article class="loc"><img src="images/lakefield.webp" alt="Blooming Minnesota prairie with purple blazing star and goldenrod (scenic photo, not the bank)" width="900" height="506" loading="lazy"><div class="b"><h3>LAKEFIELD LOCATION</h3><p>PO Box 157, 313 Main Street<br>Lakefield, MN 56150<br>Phone <a href="tel:5076626680">507-662-6680</a></p><p><strong>HOURS OF OPERATION</strong><br>Monday-Friday 9:00-4:00</p></div></article>
<article class="loc"><img src="images/jackson.webp" alt="Downtown Jackson, Minnesota (town photo, not the bank)" width="900" height="506" loading="lazy"><div class="b"><h3>JACKSON LOCATION</h3><p>414 2nd Avenue, PO Box 46<br>Jackson, MN 56143<br>Phone <a href="tel:5078474714">507-847-4714</a></p><p><strong>HOURS OF OPERATION</strong><br>Monday-Friday 8:30-4:00</p><p>ATM Available 24/7 in the Entryway</p></div></article>
</div><p class="center"><a href="locations.html">Full location details →</a></p></div></section>'''
herotxt=f'<div><p class="eyebrow">Worthington · Lakefield · Jackson</p><h1>{h1}</h1><p class="lead">We are proud to be a part of our communities, and to participate in the growth and prosperity of our region.</p><ul class="pills"><li>Three locations</li><li>24 Hour Online Banking</li><li>Mobile Deposit</li></ul></div>'
welcome=f'<section class="pt-welcome"><div class="wrap copy narrow">{rest}</div></section>'
page('index.html','Home',f'<div class="hero"><div class="wrap">{herotxt}{hero}</div></div>{quick}{welcome}{cards}{why}{merger}{CTA_SIMPLE}{locs}',('demo.js',))
for fn,t in [('about','About'),('online-banking','Online Banking'),('deposit-products','Deposit Products'),('loan-products','Loan Products'),('other-products','Other Products & Services'),('order-checks','Order Checks'),('locations','Locations'),('privacy-statement','Privacy Statement')]:
  extra=CTA_SIMPLE if fn in ('deposit-products','loan-products','online-banking','other-products','about') else ''
  if fn=='about': extra=merger.replace('<h2>Welcome, Jackson Federal customers</h2>','<h2>Welcome, Jackson Federal customers</h2>')+extra
  page(fn+'.html',t,inner(content(fn),'privacy' if fn=='privacy-statement' else '')+extra)
c=content('contact')
page('contact.html','Contact',inner(c)+'<section class="pt0"><div class="wrap"><p class="note">Concept note: the live Contact page has a Name / Email / Comments form here. It is omitted in this concept so nothing can be submitted.</p></div></section>')
# SPEEDBUMP (verbatim notice; OK/CANCEL via speedbump.js, whitelisted destinations only)
sb=content('speedbump'); sb=re.sub(r'<table.*?</table>','',sb,flags=re.S)
page('speedbump.html','Notice',f'<section><div class="wrap copy narrow">{sb}<p class="sb-btns"><a id="sb-ok" class="btn" href="index.html" rel="noopener">OK</a> <a id="sb-cancel" class="btn ghost" href="index.html">CANCEL</a></p></div></section>',('speedbump.js',))
page('accessibility.html','Accessibility Statement','<div class="page-hero"><div class="wrap"><h1>Accessibility Statement</h1></div></div><section><div class="wrap"><p class="note">Concept note: the live site has no accessibility statement page. The bank’s own statement goes here.</p></div></section>')
# CALCULATOR
calc=open(OUT+'tools/calculator.html').read()
page('calculators.html','Calculators',calc,('calculators.js',))
print('ok')
