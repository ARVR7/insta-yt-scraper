import sys
from audio_lib import *
part=int(sys.argv[1])
CFG={
 1:dict(bed='night',foot=True,ev=[(2.0,'whoosh',.6),(2.0,'thud',1.0),(8.8,'whoosh',.5),(8.8,'thud',1.0)],ticks=(12.0,14.5,70)),
 2:dict(bed='night',foot=False,ev=[(2.4,'ping',.5),(3.8,'ping',.5),(5.2,'ping',.5),(6.6,'ping',.5),(8.0,'ping',.5),(12.0,'clang',1.0),(12.0,'thud',1.0)],ticks=None),
 3:dict(bed='night',foot=False,ev=[(6.2,'ding',.5),(6.9,'ding',.5),(7.6,'ding',.5),(8.3,'ding',.5),(12.0,'riser1',.8),(13.3,'whoosh',.7),(13.3,'thud',.7)],ticks=None),
 4:dict(bed='night',foot=False,ev=[(12.0,'clang',1.0),(12.0,'paper',.7)],ticks=(2.0,10.0,16)),
 5:dict(bed='camp',foot=False,ev=[(5.6,'thud',.7),(9.0,'tape',.8)],ticks=None),
 6:dict(bed='news',foot=False,ev=[(1.6,'paper',.8),(3.6,'paper',.8),(5.6,'paper',.8),(7.6,'paper',.8),(9.0,'paper',.8),(12.0,'thud',1.0),(12.0,'paper',.8),(12.6,'thud',1.0)],ticks=(1.0,10.0,60)),
 7:dict(bed='night',foot=True,ev=[(3.0,'thud',1.0),(3.0,'buzzer',.5),(5.26,'thud',1.0),(5.26,'buzzer',.5),(7.42,'thud',1.0),(7.42,'buzzer',.5),(12.6,'thud',1.0)],ticks=(2.0,9.5,100)),
 8:dict(bed='lab',foot=False,ev=[(1.5,'creak',.8),(2.3,'ding',.4),(12.0,'clang',1.0),(12.0,'thud',1.0)],ticks=None),
 9:dict(bed='lab',foot=False,ev=[(2.0,'whoosh',.6),(3.0,'whoosh',.6),(4.0,'whoosh',.6),(5.0,'whoosh',.6),(12.0,'whoosh',.8)],ticks=None),
 10:dict(bed='lab',foot=False,ev=[(2.0,'ping',.5),(4.0,'ping',.5),(6.0,'ping',.5),(8.0,'ping',.5),(12.0,'riser1',.6)],ticks=None),
}[part]
def ev(name):
    return {'whoosh':lambda:whoosh(0.5),'thud':lambda:thud(60),'ding':ding,'clang':clang,'buzzer':lambda:buzzer(0.5),'ping':ping,'paper':paper,
            'creak':creak,'tape':tape_stop,'riser1':lambda:riser(1.2),'tick':tick}[name]()
# bed
td=tt(12.0); drone=(np.sin(2*np.pi*55*td)+0.5*np.sin(2*np.pi*55.7*td)+0.25*np.sin(2*np.pi*82.4*td))*np.minimum(1,td/1.5)*0.2
add(bus_pre,0.0,drone,0.8)
if cfg_bed:=CFG['bed']:
    if cfg_bed=='night':
        cr=crickets(10.0); cr[int(8.6*SR):]*=np.linspace(1,0,len(cr)-int(8.6*SR)); add(bus_pre,0.0,cr,1.0)
    elif cfg_bed=='camp':
        c=crackle(9.5); c[int(8.0*SR):]*=np.linspace(1,0,len(c)-int(8.0*SR)); add(bus_pre,0.0,c,0.8)
    elif cfg_bed=='news':
        for k in range(24): add(bus_pre,0.3+k*0.42+rs.uniform(0,0.05),tick(),0.25)
    elif cfg_bed=='lab':
        add(bus_pre,0.0,np.sin(2*np.pi*110*tt(10.0))*0.05*np.linspace(0.3,1,len(tt(10.0))),1.0)
k0=int(np.ceil((0.4-G0)/B))
for k in range(k0,int((10.0-G0)/B)+1):
    t0=bt(k)
    if t0<0.2 or t0>=9.95: continue
    if CFG['foot']: add(bus_sfx,t0,footstep(0.7),0.8,pan=-0.25 if k%2 else 0.25)
    if t0>=4.6:
        A=min(1,(t0-4.6)/4.0); add(bus_pre,t0,kick(0.35+0.5*A),0.9)
    if t0>=6.0: add(bus_pre,t0+B/2,hat(False),0.25,pan=0.3)
    if t0>=8.0 and k%2==1: add(bus_pre,t0,clap(),0.3)
    if k%4==0 and t0>=3.0: add(bus_pre,t0,bass([55,58.27,55,49][(k//4)%4],B*3.6),0.6)
add(bus_sfx,7.5,riser(2.45),0.8)
fade=np.ones(N,np.float32); a=int(9.9*SR); b=int(10.05*SR); fade[a:b]=np.linspace(1,0,b-a); fade[b:]=0
bus_pre*=fade
add(bus_sfx,10.0,tape_stop(),0.7)
add(bus_sfx,10.05,heart(1.85),0.9)
tin=tt(1.85); add(bus_sfx,10.05,np.sin(2*np.pi*2100*tin)*0.035*(tin/1.85),1.0)
add(bus_sfx,11.0,ding(),0.35); add(bus_sfx,11.0,thud(60),0.6)
for (t0,name,g) in CFG['ev']: add(bus_sfx,t0,ev(name),g)
if CFG['ticks']:
    a_,b_,n_=CFG['ticks']
    for v in np.linspace(0,1,n_): add(bus_sfx,a_+(b_-a_)*(1-(1-v)**(1/3)),tick(),0.28)
if part in (7,): add(bus_sfx,12.0,whoosh(0.9),0.5)
i=int(11.93*SR); bus_sfx[:,i:int(12.0*SR)]*=0.0
add(bus_sfx,12.0,drop808(),1.0)
add(bus_sfx,12.0,whoosh(0.9),0.5)
# cliffhanger sting: slam + buzzer + low rumble, extra hit on the last line
add(bus_sfx,14.0,thud(50),1.0); add(bus_sfx,14.0,buzzer(0.5),0.35)
add(bus_sfx,14.25,thud(60),0.8); add(bus_sfx,14.5,thud(45),1.0); add(bus_sfx,14.5,clang(),0.5)
add(bus_sfx,14.0,riser(0.5),0.5)
add(bus_sfx,15.8,ding(),0.4)
bassd={0:(55,3),3:(55,2),6:(65.4,2),8:(55,2),10:(49,3),13:(55,2),14:(58.27,1)}
BAR=4*B; ST=BAR/16; lead=[220,261.6,329.6,392,329.6,261.6,220,196]
bar=0
while 12.0+bar*BAR<17.0:
    b0=12.0+bar*BAR
    for s in (0,8): add(bus_drop,b0+s*ST,kick(0.9),0.9)
    for s in (4,12): add(bus_drop,b0+s*ST,clap(),0.4)
    for s in range(0,16,2): add(bus_drop,b0+s*ST,hat(s%8==6),0.22,pan=0.3 if (s//2)%2 else -0.3)
    for s,(f,l) in bassd.items(): add(bus_drop,b0+s*ST,bass(f,l*ST*1.1),0.75)
    for s in range(0,16,2): add(bus_drop,b0+s*ST,pluck(lead[(s//2)%8]*(1 if bar%2==0 else 1.122)),0.26,pan=-0.2 if (s//2)%2 else 0.2)
    bar+=1
bus_drop[:,:int(12.0*SR)]=0
lpd=np.stack([lp(bus_drop[0],900),lp(bus_drop[1],900)]); m=np.zeros(N,np.float32); m[int(12.0*SR):int(14.0*SR)]=1; m=np.convolve(m,np.ones(3000)/3000,'same')
bus_drop=bus_drop*(1-m)+lpd*m
e0=int(16.55*SR); bus_drop[:,e0:]*=np.linspace(1,0.0,N-e0)
mix=bus_pre*0.8+bus_drop*0.85+bus_sfx*0.9
mix=np.tanh(mix*1.25)/np.tanh(1.25)
peak=np.max(np.abs(mix)); mix=mix/peak*0.89
mix[:,:200]*=np.linspace(0,1,200); mix[:,-300:]*=np.linspace(1,0,300)
pcm=(np.clip(mix.T,-1,1)*32767).astype('<i2')
with wave.open(f'audio_p{part}.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('audio ok',part,'peak',round(float(peak),2))
