import random
import time
import streamlit as st

st.set_page_config(page_title="Reken Avontuur", page_icon="➕", layout="centered")
st.markdown("""
<style>
.stApp{background:linear-gradient(135deg,#eef7ff,#fff4dc 55%,#f4eaff)}
.block-container{max-width:900px;padding-top:1.3rem}.hero{background:linear-gradient(120deg,#00a896,#5b5ff0);color:white;padding:24px;border-radius:24px;text-align:center;box-shadow:0 12px 30px #5b5ff038}.hero h1{margin:0;font-size:2.35rem}.hero p{margin:.5rem 0 0}.card{background:#ffffffe8;padding:18px;border-radius:22px;box-shadow:0 8px 24px #1e293b1a;margin:12px 0}.question{font-size:3.1rem;font-weight:850;color:#30345f;text-align:center;margin:12px 0}.badge{display:inline-block;background:#fff3b0;padding:7px 11px;border-radius:999px;margin:4px;font-weight:700}.timer{font-size:1.2rem;font-weight:800;text-align:center;padding:10px;border-radius:14px;background:#fff3b0;color:#6b4f00;margin:8px 0}div.stButton>button,[data-testid="stFormSubmitButton"] button{border-radius:16px;font-weight:750;min-height:48px;border:0;background:#5b5ff0;color:white}[data-testid="stMetric"]{background:white;border-radius:18px;padding:10px;box-shadow:0 4px 14px #1e293b14}.fireworks{position:fixed;inset:0;pointer-events:none;z-index:9999;overflow:hidden}.firework{position:absolute;width:8px;height:8px;border-radius:50%;animation:burst 1.8s ease-out infinite;box-shadow:0 -70px #ff4d6d,49px -49px #ffd166,70px 0 #06d6a0,49px 49px #4cc9f0,0 70px #9b5de5,-49px 49px #ff9f1c,-70px 0 #f72585,-49px -49px #00f5d4}.f1{left:20%;top:35%}.f2{left:50%;top:22%;animation-delay:.55s}.f3{left:78%;top:38%;animation-delay:1.05s}@keyframes burst{0%{transform:scale(.05);opacity:1}65%{transform:scale(1.35);opacity:1}100%{transform:scale(1.8);opacity:0}}@media(max-width:600px){.hero h1{font-size:1.75rem}.question{font-size:2.6rem}.block-container{padding-left:.7rem;padding-right:.7rem}}
</style>
""",unsafe_allow_html=True)

D={"started":False,"finished":False,"score":0,"streak":0,"best":0,"lives":3,"answered":0,"correct":0,"wrong":0,"timed_out":0,"a":0,"b":0,"op":"+","answer":0,"choices":[],"feedback":"","locked":False,"xp":0,"badges":set(),"game_start":None,"finished_at":None,"deadline":None,"end_reason":""}
for k,v in D.items():
    if k not in st.session_state:st.session_state[k]=v.copy() if isinstance(v,set) else v

def reset_game():
    for k,v in D.items():st.session_state[k]=v.copy() if isinstance(v,set) else v

def make_sum():
    maximum=st.session_state.maximum
    kind=st.session_state.operation
    op=random.choice(["+","−"]) if kind=="Combinatie" else ("+" if kind=="Sommen" else "−")
    if op=="+":
        a=random.randint(0,maximum); b=random.randint(0,maximum-a); answer=a+b
    else:
        a=random.randint(0,maximum); b=random.randint(0,a); answer=a-b
    opts={answer}
    while len(opts)<4:
        opts.add(max(0,min(maximum,answer+random.choice([-10,-5,-3,-2,-1,1,2,3,5,10]))))
    st.session_state.a=a;st.session_state.b=b;st.session_state.op=op;st.session_state.answer=answer;st.session_state.choices=list(opts);random.shuffle(st.session_state.choices);st.session_state.feedback="";st.session_state.locked=False
    if st.session_state.level=="Met tijdsklok":st.session_state.deadline=time.time()+st.session_state.seconds_per_sum

def finish(reason):
    if not st.session_state.finished:
        st.session_state.finished=True;st.session_state.finished_at=time.time();st.session_state.end_reason=reason;st.session_state.deadline=None

def badges():
    if st.session_state.correct>=1:st.session_state.badges.add("🌟 Eerste ster")
    if st.session_state.streak>=5:st.session_state.badges.add("🔥 Reeks van 5")
    if st.session_state.correct>=10:st.session_state.badges.add("🧠 Rekenbrein")

def check(value):
    if st.session_state.locked or st.session_state.finished:return
    test=st.session_state.level=="Toetsniveau";st.session_state.locked=True;st.session_state.answered+=1
    if value==st.session_state.answer:
        st.session_state.correct+=1;st.session_state.streak+=1;st.session_state.best=max(st.session_state.best,st.session_state.streak)
        if not test:
            bonus=min(st.session_state.streak-1,5)*2;st.session_state.score+=10+bonus;st.session_state.xp+=20+bonus;st.session_state.feedback=f"✅ Juist! +{10+bonus} punten en +{20+bonus} XP";badges()
    else:
        st.session_state.wrong+=1;st.session_state.streak=0
        if not test:st.session_state.lives-=1;st.session_state.feedback=f"💡 Bijna! Het juiste antwoord is {st.session_state.answer}."
    if test:
        if st.session_state.answered>=100:finish("Alle 100 rekensommen zijn ingevuld.")
        else:make_sum()
    elif st.session_state.answered>=st.session_state.rounds or st.session_state.lives<=0:finish("De oefenreeks is voltooid.")

def timeout():
    st.session_state.answered+=1;st.session_state.timed_out+=1;st.session_state.streak=0
    if st.session_state.answered>=st.session_state.rounds:finish("De oefenreeks is voltooid.")
    else:make_sum()

def clock(x):
    x=max(0,int(x));return f"{x//60:02d}:{x%60:02d}"

def firework():st.markdown('<div class="fireworks"><span class="firework f1"></span><span class="firework f2"></span><span class="firework f3"></span></div>',unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>➕ Reken Avontuur ➖</h1><p>Oefen sommen en verschillen op jouw niveau.</p></div>',unsafe_allow_html=True)
with st.sidebar:
    st.header("🎮 Spelinstellingen")
    range_label=st.radio("Welke getallen wil je gebruiken?",["0–10","0–20","0–50","0–100"],disabled=st.session_state.started)
    maximum={"0–10":10,"0–20":20,"0–50":50,"0–100":100}[range_label]
    operation=st.radio("Welke bewerkingen?",["Sommen","Verschillen","Combinatie"],disabled=st.session_state.started)
    level=st.radio("Niveau",["Gewoon","Met tijdsklok","Toetsniveau"],disabled=st.session_state.started)
    if level!="Toetsniveau":
        answer_mode=st.radio("Hoe wil je antwoorden?",["Meerkeuze","Zelf invullen"],horizontal=True,disabled=st.session_state.started);rounds=st.slider("Aantal oefeningen",5,30,10,5,disabled=st.session_state.started)
    else:
        answer_mode="Zelf invullen";rounds=100;st.info("📝 Toets: 100 oefeningen, 10 minuten, alleen zelf invullen en geen tussentijdse feedback.")
    seconds=st.slider("Seconden per oefening",3,30,10,1,disabled=st.session_state.started) if level=="Met tijdsklok" else None
    if st.button("🔄 Nieuw spel",use_container_width=True):reset_game();st.rerun()
    st.caption("Er wordt geen klassement of persoonlijke informatie opgeslagen.")

if not st.session_state.started:
    st.markdown('<div class="card"><h3>🧮 Kies je uitdaging</h3><p>Kies je getallenbereik en oefen optellen, aftrekken of een combinatie. Verschillen hebben nooit een negatieve uitkomst en sommen blijven binnen het gekozen bereik.</p></div>',unsafe_allow_html=True)
    if st.button("🚀 Start avontuur",use_container_width=True):
        st.session_state.started=True;st.session_state.maximum=maximum;st.session_state.operation=operation;st.session_state.level=level;st.session_state.answer_mode=answer_mode;st.session_state.rounds=rounds;st.session_state.seconds_per_sum=seconds;st.session_state.game_start=time.time()
        if level=="Toetsniveau":st.session_state.test_deadline=time.time()+600
        make_sum();st.rerun()
else:
    @st.fragment(run_every=1)
    def game():
        if not st.session_state.finished:
            now=time.time()
            if st.session_state.level=="Toetsniveau" and now>=st.session_state.test_deadline:finish("De 10 minuten zijn verstreken.");st.rerun()
            if st.session_state.level=="Met tijdsklok" and now>=st.session_state.deadline:timeout();st.rerun()
        if st.session_state.finished:
            firework();pct=round(100*st.session_state.correct/max(1,st.session_state.answered),1);elapsed=st.session_state.finished_at-st.session_state.game_start;medal="🏆" if pct>=90 else "🌟" if pct>=70 else "💪"
            st.markdown(f'<div class="card" style="text-align:center"><div style="font-size:4rem">{medal}</div><h2>Resultaat</h2><p>{st.session_state.end_reason}</p><h1>{pct}%</h1><p>Benodigde tijd: <b>{clock(elapsed)}</b></p></div>',unsafe_allow_html=True)
            c1,c2,c3,c4=st.columns(4);c1.metric("✅ Juist",st.session_state.correct);c2.metric("❌ Fout",st.session_state.wrong);c3.metric("⏭️ Geen antwoord",st.session_state.timed_out);c4.metric("⏱️ Tijd",clock(elapsed))
            if st.session_state.level!="Toetsniveau":st.info(f"Score: {st.session_state.score} punten · Beste reeks: {st.session_state.best} · XP: {st.session_state.xp}")
            if st.button("🔁 Opnieuw spelen",use_container_width=True):reset_game();st.rerun()
            return
        if st.session_state.level=="Met tijdsklok":st.markdown(f'<div class="timer">⏱️ Nog {max(0,int(st.session_state.deadline-time.time()))} seconden</div>',unsafe_allow_html=True)
        elif st.session_state.level=="Toetsniveau":st.markdown(f'<div class="timer">⏱️ Toetstijd: {clock(st.session_state.test_deadline-time.time())}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="card"><div class="question">{st.session_state.a} {st.session_state.op} {st.session_state.b} = ?</div></div>',unsafe_allow_html=True)
        if st.session_state.answer_mode=="Meerkeuze":
            cols=st.columns(2)
            for i,ch in enumerate(st.session_state.choices):
                with cols[i%2]:st.button(str(ch),key=f"c{st.session_state.answered}_{ch}",use_container_width=True,on_click=check,args=(ch,),disabled=st.session_state.locked)
        else:
            with st.form(f"form_{st.session_state.answered}",clear_on_submit=True):
                value=st.number_input("Vul je antwoord in",min_value=0,max_value=st.session_state.maximum,step=1,value=None,placeholder="Typ hier je antwoord",disabled=st.session_state.locked)
                sent=st.form_submit_button("Bevestig antwoord ✅" if st.session_state.level=="Toetsniveau" else "Controleer antwoord ✅",use_container_width=True,disabled=st.session_state.locked)
                if sent:
                    if value is None:st.warning("Vul eerst een antwoord in.")
                    else:check(int(value));st.rerun()
        if st.session_state.level!="Toetsniveau" and st.session_state.feedback:
            (st.success if st.session_state.feedback.startswith("✅") else st.warning)(st.session_state.feedback)
            if st.button("Volgende oefening ➜",use_container_width=True):make_sum();st.rerun()
            if st.session_state.badges:st.markdown(" ".join(f'<span class="badge">{x}</span>' for x in sorted(st.session_state.badges)),unsafe_allow_html=True)
        st.divider()
        if st.session_state.level=="Toetsniveau":
            c1,c2,c3=st.columns(3);c1.metric("Vraag",f"{st.session_state.answered+1}/100");c2.metric("Ingevuld",st.session_state.answered);c3.metric("Resterend",100-st.session_state.answered);st.progress(st.session_state.answered/100)
        else:
            c1,c2,c3,c4=st.columns(4);c1.metric("⭐",st.session_state.score);c2.metric("🔥",st.session_state.streak);c3.metric("❤️",st.session_state.lives);c4.metric("⚡",st.session_state.xp);st.progress(st.session_state.answered/st.session_state.rounds,text=f"{st.session_state.answered}/{st.session_state.rounds}")
    game()
