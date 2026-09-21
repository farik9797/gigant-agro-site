(function(){
  const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // --- навигация: состояние при прокрутке + параллакс-гашение hero
  const nav=document.getElementById('nav'), hero=document.getElementById('heroContent');
  let ticking=false;
  const onScroll=()=>{ if(ticking) return; ticking=true; requestAnimationFrame(()=>{
    const y=window.scrollY; nav.classList.toggle('scrolled',y>24);
    if(hero&&!reduce){ const p=Math.min(y/700,1); hero.style.transform='translateY('+(y*0.18)+'px)'; hero.style.opacity=String(1-p*0.9); }
    ticking=false; }); };
  onScroll(); window.addEventListener('scroll',onScroll,{passive:true});

  // --- подвал: на мобильном колонки ссылок свёрнуты в аккордеон, на ПК открыты всегда
  (function(){
    var toggles=[].slice.call(document.querySelectorAll('.ft-toggle')); if(!toggles.length) return;
    var mq=window.matchMedia('(max-width: 767px)');
    var sync=function(){
      toggles.forEach(function(b){
        var panel=document.getElementById(b.getAttribute('aria-controls')); if(!panel) return;
        if(mq.matches){ var open=b.dataset.open==='1'; b.removeAttribute('tabindex'); b.setAttribute('aria-expanded',open?'true':'false'); panel.hidden=!open; }
        else { b.setAttribute('tabindex','-1'); b.removeAttribute('aria-expanded'); panel.hidden=false; }
      });
    };
    toggles.forEach(function(b){ b.addEventListener('click',function(){ if(!mq.matches) return; b.dataset.open=b.dataset.open==='1'?'0':'1'; sync(); }); });
    if(mq.addEventListener) mq.addEventListener('change',sync); else mq.addListener(sync);
    sync();
  })();

  // --- карточка товара: миниатюры переключают главное фото
  document.querySelectorAll('[data-gallery]').forEach(function(g){
    var main=g.querySelector('[data-gallery-main]'), thumbs=[].slice.call(g.querySelectorAll('[data-gallery-thumb]'));
    if(!main) return;
    thumbs.forEach(function(b){ b.addEventListener('click',function(){
      var im=b.querySelector('img'); if(im.srcset) main.srcset=im.srcset; main.src=im.currentSrc||im.src;
      main.alt=(b.getAttribute('aria-label')||'').replace(/^Фото \d+: /,'');
      thumbs.forEach(function(x){ x.setAttribute('aria-pressed', x===b?'true':'false'); });
    }); });
  });

  // --- слайдеры на мобильном: индикатор прокрутки
  [['catScroll','catProgress'],['kitScroll','kitProgress'],['relScroll','relProgress'],['flagScroll','flagProgress']].forEach(function(pair){
    var cs=document.getElementById(pair[0]), pg=document.getElementById(pair[1]);
    if(!cs||!pg) return;
    var upd=function(){
      if(cs.scrollWidth<=cs.clientWidth+1){ pg.style.width='100%'; pg.style.transform='none'; return; }
      var ratio=cs.clientWidth/cs.scrollWidth;
      pg.style.width=(ratio*100)+'%';
      pg.style.transform='translateX('+((cs.scrollLeft/cs.scrollWidth)/ratio*100)+'%)';
    };
    upd(); cs.addEventListener('scroll',upd,{passive:true}); window.addEventListener('resize',upd);
  });

  // --- бегущая строка: пауза
  const mq=document.querySelector('.marquee'), mqBtn=document.getElementById('marqueeToggle');
  if(mq&&mqBtn) mqBtn.addEventListener('click',()=>{const paused=mq.classList.toggle('paused'); mqBtn.setAttribute('aria-pressed',String(paused)); mqBtn.setAttribute('aria-label',paused?'Запустить бегущую строку':'Остановить бегущую строку'); mqBtn.querySelector('[data-ico="pause"]').hidden=paused; mqBtn.querySelector('[data-ico="play"]').hidden=!paused;});

  // --- мобильное меню
  const burger=document.getElementById('burger'), mobileMenu=document.getElementById('mobileMenu');
  if(burger&&mobileMenu){
  const setMenu=open=>{mobileMenu.hidden=!open;burger.setAttribute('aria-expanded',String(open)); if(open){mobileMenu.querySelector('a').focus();} else {burger.focus();}};
  burger.addEventListener('click',()=>setMenu(mobileMenu.hidden));
  mobileMenu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{mobileMenu.hidden=true;burger.setAttribute('aria-expanded','false');}));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!mobileMenu.hidden) setMenu(false);});
  document.addEventListener('click',e=>{if(!mobileMenu.hidden&&!mobileMenu.contains(e.target)&&!burger.contains(e.target)){mobileMenu.hidden=true;burger.setAttribute('aria-expanded','false');}});
  }

  // --- scroll reveal (контент видим без JS; JS только добавляет вход)
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target);}}),{threshold:0.12,rootMargin:'0px 0px -6% 0px'});
  document.querySelectorAll('.rv,.rv-stagger').forEach(el=>io.observe(el));
  // страховка: всё, что не попало в наблюдатель за 2,5 с, показать
  setTimeout(()=>document.querySelectorAll('.rv:not(.is-in),.rv-stagger:not(.is-in)').forEach(el=>{const r=el.getBoundingClientRect(); if(r.top<innerHeight) el.classList.add('is-in');}),2500);

  // --- группы чипов (одиночный выбор)
  function singleSelect(groupId,onChange){
    const g=document.getElementById(groupId); if(!g) return;
    g.addEventListener('click',e=>{const b=e.target.closest('button[data-v]'); if(!b) return;
      g.querySelectorAll('button[data-v]').forEach(x=>x.setAttribute('aria-pressed','false'));
      b.setAttribute('aria-pressed','true'); onChange&&onChange(b.dataset.v);});
  }
  const pick={animal:'krs',unit:'ha',power:'220'};
  singleSelect('pickAnimal',v=>pick.animal=v);
  singleSelect('pickPower',v=>pick.power=v);
  const unitGroup=document.getElementById('pickUnit');
  if(unitGroup) unitGroup.addEventListener('click',e=>{const b=e.target.closest('button[data-v]'); if(!b) return;
    unitGroup.querySelectorAll('button').forEach(x=>{x.setAttribute('aria-pressed','false');x.classList.remove('bg-ink','text-white');});
    b.setAttribute('aria-pressed','true'); b.classList.add('bg-ink','text-white'); pick.unit=b.dataset.v;
    document.getElementById('pickArea').value=pick.unit==='ha'?5:900;});
  document.querySelectorAll('[data-preset-power]').forEach(a=>a.addEventListener('click',()=>{
    const btn=document.querySelector('#pickPower button[data-v="'+a.dataset.presetPower+'"]'); btn&&btn.click();}));

  // --- правила подбора (стартовые, подтвердить у заказчика)
  const ANIMAL={krs:'КРС',horse:'лошади',sheep:'овцы и козы',pig:'свиньи',bird:'птица',wild:'защита от диких животных'};
  const POWER={'220':'220 В','12':'12\u00a0В аккумулятор','sun':'солнечная панель'};
  function recommend(a,ha,power){
    let r;
    if(a==='wild'||ha>6) r={model:'Bekci 25\u00a0Дж + комплектующие',price:'от 145 000 ₸',kit:'Прибор, проволока 1,6\u00a0мм, изоляторы и заземление под ваш периметр.',why:'Большой периметр или дикие животные — нужен запас мощности.'};
    else if(a==='sheep'&&ha<=1) r={model:'Комплект «Для овец», 1\u00a0га',price:'125 000 ₸',kit:'Генератор 4\u00a0Дж, шнур 2\u00a0×\u00a0500\u00a0м, аккумулятор 12\u00a0В, двое ворот, 100 изоляторов.',why:''};
    else if(a==='krs'&&ha<=5) r={model:'Комплект «Для КРС», 5\u00a0га',price:'145 000 ₸',kit:'Генератор 4\u00a0Дж, шнур 1000\u00a0м, аккумулятор 12\u00a0В 7\u00a0Ач, ворота, 100 изоляторов, табличка.',why:''};
    else if(a==='horse'&&ha<=6) r={model:'Комплект «Для лошадей», 6\u00a0га',price:'125 000 ₸',kit:'Генератор 2,5\u00a0Дж, шнур 1000\u00a0м, 100 изоляторов с саморезом, ворота, адаптер 220\u00a0В. Аккумулятор в подарок по акции.',why:''};
    else if(a==='pig'||a==='bird') r={model:'GIGANT 15\u00a0Дж + сетка или шнур',price:'от 105 000 ₸',kit:'Прибор, электросетка или шнур 6 жил, изоляторы — количество посчитаем по периметру.',why:''};
    else r={model:'GIGANT 15\u00a0Дж + комплектующие',price:'от 105 000 ₸',kit:'Прибор, проводник, изоляторы, заземление под ваш участок.',why:'Площадь больше стандартного комплекта — соберём под периметр.'};
    r.power=power==='sun'?'Питание: аккумулятор 12\u00a0В + солнечная панель и MPPT-контроллер — мощность панели подберём.':power==='12'?'Питание: аккумулятор 12\u00a0В (в готовых комплектах уже есть).':'Питание: от сети 220\u00a0В, адаптер в комплекте.';
    return r;
  }
  const pickGo=document.getElementById('pickGo');
  if(pickGo) pickGo.addEventListener('click',()=>{
    const val=parseFloat(document.getElementById('pickArea').value)||0;
    const ha=pick.unit==='ha'?val:Math.pow(val/4,2)/10000;
    const r=recommend(pick.animal,ha,pick.power);
    document.getElementById('resModel').textContent=r.model;
    document.getElementById('resKit').textContent=r.kit;
    document.getElementById('resPower').textContent=r.power;
    document.getElementById('resWhy').textContent=r.why;
    document.getElementById('resPrice').textContent=r.price;
    const areaTxt=pick.unit==='ha'?val+' га':val+' м периметра';
    const msg='Здравствуйте! Хочу подобрать электропастух. Животные: '+ANIMAL[pick.animal]+', '+areaTxt+', питание: '+POWER[pick.power]+'. Сайт предложил: '+r.model+'.';
    const ro=document.getElementById('resOrder'), tovar=r.model.replace(/\u00a0/g,' ');
    if(ro){ if(ro.getAttribute('href').charAt(0)==='#') ro.onclick=()=>setTovar(tovar); else ro.href='kontakty.html?tovar='+encodeURIComponent(tovar)+'#leadForm'; }
    document.getElementById('resWa').href='https://wa.me/77054285707?text='+encodeURIComponent(msg);
    const res=document.getElementById('pickResult'); res.classList.add('has-result'); document.getElementById('resEmpty').hidden=true; document.getElementById('resBody').hidden=false;
    if(window.innerWidth<1024) res.scrollIntoView({behavior:reduce?'auto':'smooth',block:'nearest'}); res.focus({preventScroll:true});
  });

  // --- табы по животным
  const tabs=document.getElementById('animalTabs');
  if(tabs) tabs.addEventListener('keydown',e=>{const list=[...tabs.querySelectorAll('[role="tab"]')]; const i=list.indexOf(document.activeElement); if(i<0) return;
    if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault(); const j=(i+(e.key==='ArrowRight'?1:-1)+list.length)%list.length; list[j].focus(); list[j].click();}});
  if(tabs) tabs.addEventListener('click',e=>{const b=e.target.closest('[role="tab"]'); if(!b) return;
    tabs.querySelectorAll('[role="tab"]').forEach(t=>{t.setAttribute('aria-selected','false');t.setAttribute('tabindex','-1');document.getElementById(t.getAttribute('aria-controls')).hidden=true;});
    b.setAttribute('aria-selected','true'); b.setAttribute('tabindex','0'); const p=document.getElementById(b.getAttribute('aria-controls')); p.hidden=false;
    p.classList.remove('tabpanel'); void p.offsetWidth; p.classList.add('tabpanel');});

  // --- чипы в форме (множественный выбор) → скрытое поле
  const fa=document.getElementById('formAnimals'), faVal=document.getElementById('formAnimalsValue');
  if(fa&&faVal) fa.addEventListener('click',e=>{const b=e.target.closest('button[data-v]'); if(!b) return;
    b.setAttribute('aria-pressed',b.getAttribute('aria-pressed')==='true'?'false':'true');
    faVal.value=[...fa.querySelectorAll('[aria-pressed="true"]')].map(x=>x.dataset.v).join(', ');});

  // товар из карточки: ?tovar=… или data-tovar у кнопки «Заказать»
  const tovarBox=document.getElementById('formTovar'), tovarVal=document.getElementById('formTovarValue');
  const setTovar=name=>{ if(!tovarBox||!tovarVal) return; tovarVal.value=name||''; tovarBox.hidden=!name; if(name) tovarBox.querySelector('[data-tovar-name]').textContent=name; };
  const qp=new URLSearchParams(location.search).get('tovar'); if(qp) setTovar(qp);
  document.querySelectorAll('[data-tovar]').forEach(a=>a.addEventListener('click',()=>setTovar(a.dataset.tovar)));
  const tovarClear=document.getElementById('formTovarClear'); if(tovarClear) tovarClear.addEventListener('click',()=>setTovar(''));

  // --- форма: инлайн-ошибки, заявка уходит менеджеру в WhatsApp (бэкенда нет, поэтому заявка не теряется)
  const form=document.getElementById('leadForm'), formOk=document.getElementById('formOk');
  if(form&&formOk){
  const setErr=(el,id,msg)=>{const err=document.getElementById(id); if(msg){el.setAttribute('aria-invalid','true'); err.textContent=msg; err.hidden=false;} else {el.removeAttribute('aria-invalid'); err.hidden=true;}};
  const validate=()=>{const f=form.elements; const digits=f.phone.value.replace(/\D/g,''); let first=null;
    [[f.name,'nameErr',f.name.value.trim()?'':'Укажите имя — так мы будем к вам обращаться.'],
     [f.phone,'phoneErr',digits.length>=10?'':'Введите номер телефона, например +7 705 000-00-00.'],
     [f.consent,'consentErr',f.consent.checked?'':'Нужно согласие на обработку данных.']
    ].forEach(([el,id,msg])=>{setErr(el,id,msg); if(msg&&!first) first=el;}); return first;};
  ['name','phone','consent'].forEach(n=>form.elements[n].addEventListener('input',()=>{if(form.elements[n].getAttribute('aria-invalid')) validate();}));


  form.addEventListener('submit',e=>{e.preventDefault(); const first=validate(); if(first){first.focus(); return;}
    const f=form.elements, lines=['Здравствуйте! Заявка с сайта GIGANT Agro.','Имя: '+f.name.value.trim(),'Телефон: '+f.phone.value.trim()];
    if(tovarVal&&tovarVal.value) lines.push('Товар: '+tovarVal.value);
    if(f.animals&&f.animals.value) lines.push('Животные: '+f.animals.value);
    if(f.area&&f.area.value) lines.push('Площадь: '+f.area.value+' га');
    if(f.power&&f.power.value) lines.push('Питание: '+f.power.value);
    const url='https://wa.me/77054285707?text='+encodeURIComponent(lines.join('\n'));
    const win=window.open(url,'_blank','noopener'); if(!win) location.href=url;
    formOk.hidden=false; formOk.focus({preventScroll:true});});
  }
})();
