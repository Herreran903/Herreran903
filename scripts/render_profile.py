"""Generate a self-contained animated SVG with only Python's standard library."""
import json, html, os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
config=json.loads((ROOT/'data/profile.json').read_text())
static=os.environ.get('STATIC')=='1'
esc=html.escape
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="680" viewBox="0 0 1200 680" role="img" aria-labelledby="title desc">',
'<title id="title">Nicolás Herrera — Systems Engineer</title><desc id="desc">Backend development and applied NLP. Learning RAG, LLM applications and robotics. All degree requirements completed, degree conferral expected December 2026.</desc>',
'<style>text{font-family:Menlo,Consolas,"Liberation Mono",monospace} @media(prefers-reduced-motion:reduce){.reveal{animation:none!important;opacity:1!important}.pulse{animation:none!important}.robot-motion{animation:none!important}}',
'@keyframes reveal{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:translateY(0)}} @keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}',
'@keyframes robotFloat{0%,100%{transform:translate(0,0) rotate(-1deg)}50%{transform:translate(2px,-7px) rotate(1deg)}} .robot-motion{transform-origin:270px 390px;animation:robotFloat 5s ease-in-out infinite}.reveal{animation:reveal .3s ease both}.pulse{animation:pulse 2s ease-in-out infinite}</style>',
'<rect x="1" y="1" width="1198" height="678" rx="18" fill="#101e25" stroke="#36535b" stroke-width="2"/>',
'<path d="M20 49H1180" stroke="#36535b"/>']
for x,c in [(25,'#cf8067'),(47,'#d9b778'),(69,'#7fa89a')]:parts.append(f'<circle cx="{x}" cy="25" r="5" fill="{c}"/>')
parts.append(f'<text x="100" y="30" font-size="14" fill="#9eb3b6">{esc(config["title"])}</text>')
parts.append('<defs><clipPath id="robotViewport"><rect x="12" y="58" width="535" height="600" rx="8"/></clipPath></defs><g clip-path="url(#robotViewport)"><g transform="translate(270 350)"><g>')
if not static:
    parts.append('<animateTransform attributeName="transform" type="scale" values="0.88;0.88;1.14;1.14;0.88;0.88" keyTimes="0;.15;.42;.65;.9;1" calcMode="spline" keySplines=".4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1;.4 0 .2 1" dur="8s" repeatCount="indefinite"/>')
parts.append('<g>')
if not static:
    parts.append('<animateTransform attributeName="transform" type="rotate" values="0;0;-3;2;0;0" keyTimes="0;.15;.42;.65;.9;1" dur="8s" repeatCount="indefinite"/>')
parts.append('<g transform="translate(-270 -350)">')
for i,row in enumerate((ROOT/'data/robot.txt').read_text().splitlines()):
 delay=i*.035
 attr='' if static else f'class="reveal" style="animation-delay:{delay:.3f}s"'
 parts.append(f'<text {attr} x="16" y="{112+i*13}" font-size="12" fill="#f1dfb7" xml:space="preserve">{esc(row)}</text>')
parts.append('</g></g></g></g></g>')
y=87
for i,(text,kind) in enumerate(config['rows']):
 if kind=='gap':y+=14;continue
 color='#87c6c3' if kind=='cmd' else '#f1dfb7' if kind=='title' else '#b9c9ce'
 attr='' if static else f'class="reveal" style="animation-delay:{.3+i*.07:.2f}s"'
 parts.append(f'<text {attr} x="565" y="{y}" font-size="{22 if kind=="title" else 16}" fill="{color}" xml:space="preserve">{esc(text)}</text>')
 y+=27 if kind=='title' else 25
assert y<=570, f'Content overflows availability indicator: {y}'
parts.extend(['<g '+('' if static else 'class="pulse"')+'><circle cx="576" cy="582" r="11" fill="none" stroke="#26784d" stroke-width="2"/><circle cx="576" cy="582" r="7" fill="none" stroke="#3dbf7d"/><circle cx="576" cy="582" r="3" fill="#66c99a"/></g>', '<text x="597" y="587" font-size="16" fill="#b9c9ce">Open to opportunities</text>','</svg>'])
out=ROOT/'assets/terminal-profile.svg';out.parent.mkdir(exist_ok=True);out.write_text(''.join(parts))
import xml.etree.ElementTree as ET
ET.parse(out)
print(f'Generated {out.name} ({out.stat().st_size} bytes)')

# GIF fallback: browsers consistently animate this format inside GitHub READMEs.
from PIL import Image, ImageDraw, ImageFont
import math
font_paths=['/System/Library/Fonts/Menlo.ttc','/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf']
font_path=next(p for p in font_paths if Path(p).exists())
f=ImageFont.truetype(font_path,16);title=ImageFont.truetype(font_path,22);af=ImageFont.truetype(font_path,12)
base=Image.new('RGB',(1200,680),'#101e25');d=ImageDraw.Draw(base)
d.rounded_rectangle((1,1,1198,678),18,outline='#36535b',width=2)
for x,c in [(25,'#cf8067'),(47,'#d9b778'),(69,'#7fa89a')]:d.ellipse((x-5,20,x+5,30),fill=c)
d.line((20,49,1180,49),fill='#36535b');d.text((100,17),config['title'],font=f,fill='#9eb3b6')
y=73
for text,kind in config['rows']:
 if kind=='gap':y+=14;continue
 d.text((565,y),text,font=title if kind=='title' else f,fill='#87c6c3' if kind=='cmd' else '#f1dfb7' if kind=='title' else '#b9c9ce');y+=27 if kind=='title' else 25
d.text((597,570),'Open to opportunities',font=f,fill='#b9c9ce')
robot=Image.new('RGBA',(540,600));rd=ImageDraw.Draw(robot)
for i,row in enumerate((ROOT/'data/robot.txt').read_text().splitlines()):rd.text((4,40+i*13),row,font=af,fill='#f1dfb7')
frames=[]
def ease(a):return a*a*(3-2*a)
for i in range(64):
 t=i/64
 if t<.15:z=0
 elif t<.42:z=ease((t-.15)/.27)
 elif t<.65:z=1
 elif t<.9:z=1-ease((t-.65)/.25)
 else:z=0
 scale=.88+.26*z;angle=(-3+5*max(0,min(1,(t-.42)/.23)))*z
 layer=robot.resize((round(540*scale),round(600*scale)),Image.Resampling.BICUBIC).rotate(angle,resample=Image.Resampling.BICUBIC,expand=True)
 window=Image.new('RGBA',(535,600));window.alpha_composite(layer,((535-layer.width)//2,(600-layer.height)//2))
 im=base.copy();im.paste(window,(12,58),window);di=ImageDraw.Draw(im);v=(1+math.cos(t*8*math.pi))/2
 di.ellipse((565,571,587,593),outline=(25,round(70+70*v),65),width=2);di.ellipse((573,579,579,585),fill='#66c99a');frames.append(im)
frames[0].save(ROOT/'assets/terminal-profile.gif',save_all=True,append_images=frames[1:],duration=125,loop=0,optimize=True,disposal=2)
print('Generated looping GIF fallback')
