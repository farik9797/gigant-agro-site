#!/usr/bin/env python3
"""WebP-варианты для всех изображений, на которые ссылаются страницы. Результат: assets/img/opt/<имя>-<ширина>.webp"""
import os, re, glob, json
from PIL import Image
ROOT=os.path.dirname(os.path.abspath(__file__)); OPT=os.path.join(ROOT,'assets/img/opt'); os.makedirs(OPT,exist_ok=True)
WIDTHS_DEFAULT=[480,640,800,1200]; WIDTHS_HERO=[480,640,960,1440,1920]
HERO={'hero-gigant-1920.jpg','steppe-horses-1920.jpg','why-cow-fence.jpg','solar-line.jpg'}
SKIP={'favicon-64.png'}
used=set()
for f in glob.glob(os.path.join(ROOT,'pages/*.html'))+glob.glob(os.path.join(ROOT,'partials/*.html'))+[os.path.join(ROOT,'make_pages.py'),os.path.join(ROOT,'build.py')]:
    used|=set(re.findall(r'assets/img/([\w\-.]+\.(?:jpg|jpeg|png))', open(f,encoding='utf-8').read()))
manifest={}; before=after=0
for name in sorted(used-SKIP):
    src=os.path.join(ROOT,'assets/img',name)
    if not os.path.exists(src): print('  нет файла:',name); continue
    im=Image.open(src); im=im.convert('RGBA' if im.mode in('RGBA','LA','P') else 'RGB')
    base=os.path.splitext(name)[0]; widths=WIDTHS_HERO if name in HERO else WIDTHS_DEFAULT
    variants=[]
    for w in widths:
        if w>im.width and variants and im.width<variants[-1]['w']*1.15: break   # оригинал почти равен последнему варианту
        w=min(w,im.width); h=round(im.height*w/im.width)
        out=os.path.join(OPT,f'{base}-{w}.webp')
        im.resize((w,h),Image.LANCZOS).save(out,'WEBP',quality=74 if name in HERO else 78,method=6)
        variants.append({'w':w,'h':h,'file':f'assets/img/opt/{base}-{w}.webp','kb':os.path.getsize(out)//1024})
        if w==im.width: break
    manifest[name]={'width':im.width,'height':im.height,'variants':variants}
    before+=os.path.getsize(src); after+=max(v['kb'] for v in variants)*1024
json.dump(manifest,open(os.path.join(OPT,'manifest.json'),'w'),indent=1)
print(f'изображений: {len(manifest)}; оригиналы {before//1024} KB → крупнейшие WebP {after//1024} KB')
