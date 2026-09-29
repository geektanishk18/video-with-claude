import json, numpy as np, subprocess, re
SR=48000
T=json.load(open('timeline.json')); SEG={s['id']:s for s in T['segments']}; TOTAL=T['total']
def clean(w): return re.sub(r'[^a-z]','',w.lower())
def W(seg, word, n=1, end=False):
    k=0
    for w in SEG[seg]['words']:
        if clean(w[2])==word:
            k+=1
            if k==n: return w[1] if end else w[0]
    raise KeyError((seg,word))
# ---------- key visual/sound events (shared with Remotion) ----------
E={}
E['ding0']=0.0
E['another']=W('P1','another'); E['lead']=W('P1','lead')
E['really']=SEG['PR']['start']
E['actually']=SEG['P2']['start']; E['coming']=W('P2','coming'); E['everywhere']=W('P2','everywhere')
E['s1']=SEG['S1']['start']; E['manually']=W('S1','manually')
E['p3']=SEG['P3']['start']; E['qualify']=W('P3','qualify'); E['first']=W('P3','first')
E['s2']=SEG['S2']['start']; E['p4']=SEG['P4']['start']; E['s3']=SEG['S3']['start']
E['s4']=SEG['S4']['start']; E['s5']=SEG['S5']['start']; E['work']=W('S5','work')
E['s6']=SEG['S6']['start']; E['ai']=W('S6','ai'); E['handle']=W('S6','handle'); E['s6end']=SEG['S6']['end']
E['s7']=SEG['S7']['start']; E['understands']=W('S7','understands'); E['person']=W('S7','person'); E['actually2']=W('S7','actually'); E['wants']=W('S7','wants')
E['s8']=SEG['S8']['start']; E['against']=W('S8','against'); E['criteria']=W('S8','criteria')
E['s9']=SEG['S9']['start']; E['gives']=W('S9','gives'); E['score']=W('S9','score'); E['s9end']=SEG['S9']['end']
E['s10']=SEG['S10']['start']; E['treating']=W('S10','treating'); E['every10']=W('S10','every'); E['same']=W('S10','same')
E['s11']=SEG['S11']['start']; E['know']=W('S11','know'); E['which']=W('S11','which'); E['attention']=W('S11','attention')
E['s12']=SEG['S12']['start']; E['limited']=W('S12','limited'); E['industry']=W('S12','industry')
E['s13']=SEG['S13']['start']; E['define']=W('S13','define'); E['good']=W('S13','good'); E['s13end']=SEG['S13']['end']
E['s14']=SEG['S14']['start']; E['understands2']=W('S14','understands'); E['scores']=W('S14','scores'); E['match14']=W('S14','match'); E['best']=W('S14','best'); E['s14end']=SEG['S14']['end']
E['p5']=SEG['P5']['start']; E['s15']=SEG['S15']['start']; E['literally']=W('S15','literally')
E['p6']=SEG['P6']['start']; E['nice']=W('P6','nice'); E['p6end']=SEG['P6']['end']
E['total']=TOTAL
json.dump({k:round(v,3) for k,v in E.items()},open('events.json','w'),indent=1)

# ---------- synth ----------
rng=np.random.default_rng(7)
def env(n,a=0.005,r=0.2):
    t=np.arange(n)/SR; e=np.minimum(1,t/a)*np.exp(-t/r); return e
def tone(f,d,a=0.004,r=0.25,h=(1,.3,.1)):
    n=int(d*SR); t=np.arange(n)/SR; s=sum(amp*np.sin(2*np.pi*f*(i+1)*t) for i,amp in enumerate(h)); return s*env(n,a,r)
def noise(d): return rng.standard_normal(int(d*SR))
def lp(x,a): # one-pole lowpass
    y=np.zeros_like(x); acc=0
    for i in range(len(x)): acc+=a*(x[i]-acc); y[i]=acc
    return y
def bp_noise(d,f0,f1):
    n=int(d*SR); x=noise(d); X=np.fft.rfft(x); fr=np.fft.rfftfreq(n,1/SR)
    X[(fr<min(f0,f1))|(fr>max(f0,f1))]=0; return np.fft.irfft(X,n)
def sweep(d,f0,f1):
    n=int(d*SR); x=noise(d); out=np.zeros(n); seg=int(0.02*SR)
    for i in range(0,n,seg):
        f=f0+(f1-f0)*i/n; X=np.fft.rfft(x[i:i+seg]); fr=np.fft.rfftfreq(len(x[i:i+seg]),1/SR); X[(fr<f*0.6)|(fr>f*1.6)]=0; out[i:i+seg]=np.fft.irfft(X,len(x[i:i+seg]))
    t=np.linspace(0,1,n); return out*np.sin(np.pi*t)**1.5
SFX={
 'ding': lambda p=0: tone(1318.5*2**(p/12),0.6,r=0.18,h=(1,.25,.08))+0.6*tone(1975.5*2**(p/12),0.6,r=0.12),
 'pop': lambda p=0: tone(620*2**(p/12),0.12,a=0.002,r=0.03,h=(1,.5)),
 'click': lambda p=0: bp_noise(0.02,2500,7000)*env(int(0.02*SR),0.0005,0.004)*1.5,
 'key': lambda p=0: bp_noise(0.03,1500,5000)*env(int(0.03*SR),0.0005,0.006)*(0.8+0.4*rng.random()),
 'whoosh': lambda p=0: sweep(0.35,400,4000)*0.9,
 'whooshdown': lambda p=0: sweep(0.5,3000,300)*0.9,
 'drop': lambda p=0: (np.sin(2*np.pi*np.cumsum(np.linspace(90,38,int(1.2*SR)))/SR)*env(int(1.2*SR),0.003,0.45))*1.4+bp_noise(1.2,40,180)*env(int(1.2*SR),0.002,0.2)*0.5,
 'riser': lambda p=0: sweep(1.2,300,6000)*np.linspace(0.2,1,int(1.2*SR))*0.7,
 'confirm': lambda p=0: sum(tone(f,1.1,r=0.5,h=(1,.2)) for f in [523.25,659.25,783.99,1046.5])*0.35,
 'stamp': lambda p=0: bp_noise(0.18,60,900)*env(int(0.18*SR),0.001,0.05)*1.6+tone(110,0.18,r=0.06)*0.8,
 'slide': lambda p=0: bp_noise(0.18,800,3000)*np.sin(np.linspace(0,np.pi,int(0.18*SR)))*0.5,
 'tick': lambda p=0: tone(1800*2**(p/12),0.06,a=0.001,r=0.015,h=(1,)),
 'scribble': lambda p=0: bp_noise(0.9,1500,6000)*(0.5+0.5*np.abs(np.sin(np.linspace(0,40,int(0.9*SR)))))*0.35,
 'tap': lambda p=0: tone(880,0.15,a=0.001,r=0.04,h=(1,.6))*0.8,
 'thud': lambda p=0: tone(70,0.5,a=0.002,r=0.15,h=(1,.4))*1.2,
 'step': lambda p=0: bp_noise(0.08,100,1200)*env(int(0.08*SR),0.001,0.02)*1.1,
 'sip': lambda p=0: bp_noise(0.45,2000,8000)*np.sin(np.linspace(0,np.pi,int(0.45*SR)))**2*0.45,
 'chord': lambda p=0: sum(tone(f,3.2,a=0.02,r=1.4,h=(1,.15,.05)) for f in [220,277.18,329.63,440,554.37])*0.3,
 'blackclick': lambda p=0: bp_noise(0.03,1000,6000)*env(int(0.03*SR),0.0005,0.006)*2,
}
cues=[('ding',E['ding0'],0,1.0)]
for i in range(5): cues.append(('ding',E['another']+i*0.1,i*2,0.55))
cues.append(('ding',E['lead'],9,0.6))
for i,t in enumerate(np.linspace(SEG['P1']['end']+0.08,E['really']-0.08,6)): cues.append(('ding',t,(i%3)*3,0.45))
cues.append(('whoosh',E['actually']-0.05,0,0.8))
for i in range(6): cues.append(('pop',E['coming']+i*0.08,i,0.6))
for i in range(4): cues.append(('ding',E['everywhere']+i*0.06,i*4-2,0.5))
cues.append(('whoosh',E['s1']-0.1,0,0.7))
cues.append(('slide',E['p3']-0.05,0,0.9))
for i in range(7): cues.append(('key',E['qualify']+i*0.11,0,0.9))
cues+= [('ding',E['first'],5,0.7),('stamp',E['first'],0,0.5),('thud',E['s3']-0.02,0,0.8),('whooshdown',E['s3']+0.1,0,0.6),('scribble',E['work']-0.1,0,0.8),
        ('tap',E['s6'],0,0.8),('riser',E['handle']-1.2,0,0.6),('drop',E['handle'],0,1.0),('whoosh',E['s6end']+0.35,0,0.8),('whoosh',E['s7']-0.15,0,0.7)]
for i in range(18): cues.append(('key',E['s7']+0.1+i*0.07,0,0.5))
for k in ['person','actually2','wants']: cues.append(('whoosh',E[k],0,0.45))
cues.append(('slide',E['s8'],0,0.8))
for i in range(5): cues.append(('tick',E['criteria']+i*0.17,i*2,0.8))
cues.append(('whoosh',E['s9']-0.1,0,0.6))
n=int((E['score']-E['gives'])/0.09)
for i in range(n): cues.append(('tick',E['gives']+i*0.09,-12+i*0.5,0.35))
cues+= [('confirm',E['score'],0,0.9),('tick',E['treating'],7,0.4),('click',E['every10'],0,1),('slide',E['every10']+0.05,0,0.5),('click',E['same'],0,1)]
for i in range(4): cues.append(('slide',E['know']+i*0.07,0,0.6))
cues.append(('stamp',E['attention'],0,0.9))
for i in range(6): cues.append(('whoosh',E['limited']+i*0.28,0,0.35))
for i in range(8): cues.append(('key',E['define']+i*0.09,0,0.7))
cues.append(('confirm',E['good'],0,0.45))
for k in ['understands2','scores','match14','best']: cues.append(('tick',E[k],12,0.6))
cues+= [('confirm',E['best']+0.25,0,0.9),('whoosh',E['p5']-0.2,0,0.8)]
for i in range(3): cues.append(('step',E['s15']+0.1+i*0.38,0,0.8))
cues+= [('sip',E['nice']-0.15,0,1.0)]
N=int(TOTAL*SR)+SR
sfx=np.zeros(N)
for name,t,p,g in cues:
    s=SFX[name](p); i=int(max(0,t)*SR); j=min(N,i+len(s)); sfx[i:j]+=g*s[:j-i]
i0,i1=int(E['p4']*SR),int(E['handle']*SR); rt=bp_noise((i1-i0)/SR,80,900); sfx[i0:i0+len(rt)]+=rt*0.02
# ---------- funk bed 108 BPM ----------
bpm=108; st=60/bpm/4  # 16th
mus=np.zeros(N)
def add(buf,x,t,g=1.0):
    i=int(t*SR); j=min(N,i+len(x));
    if i<N and j>i: buf[i:j]+=g*x[:j-i]
def ks(f,d,damp=0.996,bright=1.0):
    n=int(d*SR); p=max(2,int(SR/f)); buf=rng.uniform(-1,1,p)*bright; out=np.zeros(n)
    for i in range(n):
        v=buf[i%p]; out[i]=v; buf[i%p]=damp*0.5*(v+buf[(i+1)%p])
    return out
def kick():
    n=int(0.32*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*np.cumsum(np.linspace(150,48,n))/SR)*np.exp(-t/0.08)*1.1+bp_noise(0.32,1000,4000)*np.exp(-t/0.004)*0.3
def snare(g=1):
    n=int(0.22*SR); t=np.arange(n)/SR; return (bp_noise(0.22,1200,8000)*np.exp(-t/0.06)*0.8+np.sin(2*np.pi*190*t)*np.exp(-t/0.05)*0.6)*g
def hat(open_=False):
    d=0.22 if open_ else 0.045; n=int(d*SR); t=np.arange(n)/SR; return bp_noise(d,7000,15000)*np.exp(-t/(0.08 if open_ else 0.012))*0.5
def crash():
    n=int(1.8*SR); t=np.arange(n)/SR; return bp_noise(1.8,4000,15000)*np.exp(-t/0.6)*0.5
def ep(freqs,d=0.35):  # FM electric piano stab
    n=int(d*SR); t=np.arange(n)/SR; o=np.zeros(n)
    for f in freqs: o+=np.sin(2*np.pi*f*t+1.2*np.exp(-t/0.12)*np.sin(2*np.pi*f*t))
    return o*np.exp(-t/0.16)*np.minimum(1,t/0.003)*0.14
def scratch(chord,ghost=False):
    if ghost: return bp_noise(0.05,1500,5000)*env(int(0.05*SR),0.001,0.01)*0.35
    o=sum(ks(f,0.12,0.985) for f in chord); t=np.arange(len(o))/SR; return o*np.exp(-t/0.04)*0.22
Kpat=[{0,3,8,10},{0,6,8,11}]; Spat={4,12}; Ghost={7,9,15}
E9=[164.81,207.65,293.66,369.99,493.88]; A9=[220,277.18,392,493.88,659.25]
Bpat={0:(0,0),3:(12,1),4:(3,0),6:(5,0),7:(7,0),8:(0,0),10:(10,0),11:(12,1),14:(3,0),15:(5,0)}  # semitones from root, pop
def groove(t0,t1,guitar=True,keys=True,drums=True,bass=True,intro=False):
    step=0; t=t0
    while t<t1-1e-6:
        bar=step//16; s=step%16; root=82.41 if (bar//2)%2==0 else 110.0; chord=E9 if root<100 else A9
        if drums and not (intro and bar==0 and s not in (0,4,8,12)):
            if s in Kpat[bar%2]: add(mus,kick(),t,0.9)
            if s in Spat: add(mus,snare(),t,0.7)
            if s in Ghost: add(mus,snare(0.25),t,0.7)
            add(mus,hat(s==14),t,0.35 if s%2==0 else 0.2)
        if bass and s in Bpat:
            semi,popn=Bpat[s]; f=root*2**(semi/12)
            add(mus,ks(f,0.3 if not popn else 0.18,0.993 if not popn else 0.98, 1.0)*(0.9 if not popn else 0.7),t,0.55)
        if guitar and not intro:
            if s in (2,6,10,14): add(mus,scratch(chord),t,1.0)
            elif s%2==1: add(mus,scratch(chord,True),t,1.0)
        if keys and not intro and s in (0,) and bar%2==0: add(mus,ep([f*2 for f in chord[1:4]],0.5),t,1.0)
        if keys and not intro and s==14 and bar%2==1: add(mus,ep([f*2 for f in chord[1:4]],0.3),t,1.0)
        t+=st; step+=1
bar=16*st
groove(0.5,E['p4'],intro=False)
add(mus,crash(),E['handle'],0.8)
groove(E['handle'],E['p5'])
groove(E['p5'],E['p6end']+0.15,guitar=False)
add(mus,ep([329.63,415.3,587.33,739.99],1.2),E['p6end']+0.2,1.4); add(mus,kick(),E['p6end']+0.2,0.9); add(mus,crash(),E['p6end']+0.2,0.5)
g=np.ones(N)
a_=int(E['p4']*SR); g[a_:a_+int(0.2*SR)]*=np.linspace(1,0,int(0.2*SR)); g[a_+int(0.2*SR):int(E['handle']*SR)]=0
mus*=g
# duck music under VO
vo=subprocess.run(['ffmpeg','-v','error','-i','master_vo.wav','-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
vo=np.frombuffer(vo,np.float32).astype(np.float64); vo=np.pad(vo,(0,max(0,N-len(vo))))[:N]
envv=np.sqrt(np.convolve(vo**2,np.ones(2400)/2400,'same')); duck=1-0.45*np.clip(envv/0.05,0,1)
duck=np.convolve(duck,np.ones(4800)/4800,'same'); mus*=duck
mix=vo*1.0+mus*0.42+sfx*0.28
mix=mix[:int(TOTAL*SR)]
mix/=max(1e-9,np.abs(mix).max())/0.9
mix.astype(np.float32).tofile('mix.f32')
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar',str(SR),'-ac','1','-i','mix.f32','-af','loudnorm=I=-14:TP=-1.2:LRA=9','-ar','48000','-ac','2','final_mix.wav'],check=True)
print('cues',len(cues),'events',len(E))
