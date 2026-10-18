import numpy as np, wave
from scipy.signal import lfilter, butter, sosfilt
from common import *
SR=44100; N=int(SR*DUR)
rs=np.random.RandomState(3)
L=np.zeros(N,np.float32); Rr=np.zeros(N,np.float32)   # master
bus_pre=np.zeros((2,N),np.float32); bus_drop=np.zeros((2,N),np.float32); bus_sfx=np.zeros((2,N),np.float32)

def tt(d): return np.arange(int(d*SR))/SR
def hp(x,fc): return sosfilt(butter(2,fc/(SR/2),'high',output='sos'),x)
def lp(x,fc): return sosfilt(butter(2,fc/(SR/2),'low',output='sos'),x)
def bp(x,a,b): return sosfilt(butter(2,[a/(SR/2),b/(SR/2)],'band',output='sos'),x)
def add(bus,t0,sig,gain=1.0,pan=0.0):
    i=int(t0*SR)
    if i>=N or i+len(sig)<=0: return
    s=max(0,-i); e=min(len(sig),N-i)
    g1=gain*np.cos((pan+1)*np.pi/4); g2=gain*np.sin((pan+1)*np.pi/4)
    bus[0,i+s:i+e]+=sig[s:e]*g1; bus[1,i+s:i+e]+=sig[s:e]*g2

def kick(vol=1.0):
    t=tt(0.45); f=45+110*np.exp(-t*28); ph=2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph)*np.exp(-t*9)+0.4*np.sin(ph*2)*np.exp(-t*30))*vol
def clap():
    t=tt(0.22); n=hp(rs.randn(len(t)),900)
    env=np.exp(-t*22)+0.6*np.exp(-((t-0.012)*180)**2)+0.5*np.exp(-((t-0.024)*180)**2)
    return bp(n,900,6000)*env*0.9
def hat(op=False):
    t=tt(0.18 if op else 0.05); return hp(rs.randn(len(t)),7000)*np.exp(-t*(18 if op else 90))*0.5
def bass(f,d=0.35):
    t=tt(d); saw=2*((t*f)%1)-1; sq=np.sign(np.sin(2*np.pi*f*t))
    x=lp(0.6*saw+0.4*sq,900)
    env=np.minimum(1,t*200)*np.exp(-t*4)*(t<d-0.01)
    return x*env*0.9+0.5*np.sin(2*np.pi*f*t)*env
def pluck(f,d=0.16):
    t=tt(d); x=np.sign(np.sin(2*np.pi*f*t))*0.5+np.sin(2*np.pi*f*2*t)*0.2
    return lp(x,3500)*np.exp(-t*20)*0.5
def tick():
    t=tt(0.03); return np.sin(2*np.pi*2400*t)*np.exp(-t*220)*0.6
def whoosh(d=0.35,up=True):
    t=tt(d); n=rs.randn(len(t)); 
    env=(np.sin(np.pi*np.clip(t/d,0,1))**2)
    x=bp(n,500,7000)*env
    return x*0.8
def clang():
    t=tt(0.9); x=sum(a*np.sin(2*np.pi*f*t+p)*np.exp(-t*d) for f,a,d,p in [(740,1,6,0),(1190,.8,7,1),(1870,.6,9,2),(2630,.45,12,.5),(3410,.3,15,1.3)])
    x=x+hp(rs.randn(len(t)),2000)*np.exp(-t*60)*0.8
    return x*0.55
def thud(f0=95):
    t=tt(0.4); f=45+(f0-45)*np.exp(-t*20); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-t*11)
def buzzer(d=0.38):
    t=tt(d); x=np.sign(np.sin(2*np.pi*98*t))+0.6*np.sign(np.sin(2*np.pi*104*t))
    return lp(x,1800)*0.45*np.minimum(1,(d-t)*30)*np.minimum(1,t*80)
def sad():
    out=np.zeros(int(1.3*SR)); 
    for k,(f0,f1,s,dur) in enumerate([(311,294,0.0,0.3),(294,277,0.32,0.3),(277,262,0.64,0.3),(262,196,0.96,0.34)]):
        t=tt(dur); f=f0+(f1-f0)*(t/dur)+ (6*np.sin(2*np.pi*6*t) if k==3 else 0)
        ph=2*np.pi*np.cumsum(f)/SR; x=lp((2*((ph/(2*np.pi))%1)-1),1300)*np.minimum(1,t*60)*np.exp(-t*2.5)
        i=int(s*SR); out[i:i+len(x)]+=x*0.55
    return out
def sizzle(d=1.0):
    t=tt(d); n=np.zeros(len(t)); dens=60+500*(t/d)
    clicks=rs.rand(len(t))<(dens/SR)
    x=lfilter([1],[1,-0.5],clicks.astype(float)*rs.randn(len(t))*2.0)
    return hp(x,3000)*0.5+hp(rs.randn(len(t)),6000)*0.06*(t/d)
def drop808():
    t=tt(2.0); f=42+110*np.exp(-t*18); ph=2*np.pi*np.cumsum(f)/SR
    x=np.sin(ph)*np.exp(-t*1.7)*np.minimum(1,t*500)
    crash=hp(rs.randn(len(t)),5000)*np.exp(-t*2.8)*0.5
    imp=lp(rs.randn(len(t)),300)*np.exp(-t*20)*0.9
    return x*1.0+crash+imp
def swish_snd():
    t=tt(0.7); n=rs.randn(len(t))
    env=np.exp(-((t-0.06)/0.12)**2)*0.9+np.exp(-t*5)*0.25
    x=bp(n,1500,9000)*env + hp(rs.randn(len(t)),4000)*np.exp(-t*7)*0.25
    return x*0.8
def ding():
    t=tt(0.8); return (np.sin(2*np.pi*1318*t)+0.6*np.sin(2*np.pi*1760*t)+0.3*np.sin(2*np.pi*2637*t))*np.exp(-t*5)*0.35
def riser(d):
    t=tt(d); u=t/d
    n=hp(rs.randn(len(t)),3000)*(u**2.2)*0.55
    f=300*np.exp(np.log(3000/300)*u); ph=2*np.pi*np.cumsum(f)/SR
    s=np.sin(ph)*(u**2.5)*0.25
    return n+s
def heart(d):
    t=tt(d); out=np.zeros(len(t))
    per=0.9
    k=0
    while k*per<d:
        for off,g in ((0,1.0),(0.22,0.7)):
            i=int((k*per+off)*SR)
            tt_=tt(0.35); x=np.sin(2*np.pi*(52+30*np.exp(-tt_*30))*tt_)*np.exp(-tt_*12)*g
            e=min(len(out),i+len(x))
            if i<len(out): out[i:e]+=x[:e-i]
        k+=1
    return out*1.1
def tape_stop():
    t=tt(0.45); f=900*np.exp(-t*7.0)+40; ph=2*np.pi*np.cumsum(f)/SR
    return (np.sin(ph)+0.5*np.sign(np.sin(ph)))*np.exp(-t*5)*0.35

# ---------------- pre-drop groove (0..7)
BAR=2.0; STEP=BAR/16
steps=lambda bar,s:(bar*BAR+s*STEP)
bassline={0:(55,3),3:(55,2),6:(65.4,2),8:(55,2),10:(49,3),13:(55,2),14:(61.7,1)}
for bar in range(0,3):
    for s in (0,6,8,10): add(bus_pre,steps(bar,s),kick(0.9),0.9)
    for s in (4,12): add(bus_pre,steps(bar,s),clap(),0.35 if bar<1 else 0.5)
    for s in range(0,16,2): add(bus_pre,steps(bar,s),hat(s%8==6),0.28,pan=0.35)
    for s,(f,l) in bassline.items(): add(bus_pre,steps(bar,s),bass(f,l*STEP*1.1),0.8)
    for s in range(0,16,4): add(bus_pre,steps(bar,s)+STEP*2,tick(),0.5,pan=-0.3)
# partial bar 3 (6.0..7.0) – half bar drums stripped by pepper beat; handled below
# pepper beat 5.5-6.5: strip groove: remove bus_pre in that window then add sizzle/drone
i0,i1=int(5.5*SR),int(6.5*SR)
bus_pre[:,i0:i1]*=0.0
add(bus_sfx,5.5,sizzle(1.0),0.7)
drone=tt(1.0); dr=(np.sin(2*np.pi*55*drone)+0.5*np.sin(2*np.pi*82.5*drone))*np.minimum(1,drone*8)*0.35
add(bus_sfx,5.5,dr,0.8)
add(bus_sfx,5.5,whoosh(0.35),0.5); add(bus_sfx,5.5,thud(70),0.9)
# 6.5-7.0 launch: kick roll
for k in range(8): add(bus_pre,6.5+k*0.0625,kick(0.7+0.04*k),0.8)
# tape-stop cut of the pre bus at 7.0
fade=np.ones(N,np.float32); a=int(6.97*SR); b=int(7.08*SR); fade[a:b]=np.linspace(1,0,b-a); fade[b:]=0
bus_pre*=fade
add(bus_sfx,6.95,tape_stop(),0.8)

# ---------------- sfx for montage
add(bus_sfx,2.0,whoosh(0.3),0.55); add(bus_sfx,3.5,whoosh(0.3),0.55); add(bus_sfx,6.5,whoosh(0.3),0.6)
tc=2.0+(events(1,'rim')[0]-1.05)/0.5
add(bus_sfx,tc,clang(),1.0); add(bus_sfx,tc,thud(110),0.7)
add(bus_sfx,2.35,thud(80),0.9); add(bus_sfx,2.35,buzzer(),0.6)
add(bus_sfx,4.7,sad(),0.8)
add(bus_sfx,3.5+events(2,'floor')[0],thud(100),0.8)
add(bus_sfx,6.5,thud(60),1.0)
# ---------------- freeze 7.0-10.0
add(bus_sfx,7.0,heart(2.95),0.85)
add(bus_sfx,7.0,riser(2.9),0.9)
tin=tt(2.95); add(bus_sfx,7.0,np.sin(2*np.pi*2300*tin)*0.04*(tin/2.95),1.0)
# silence gap right before drop
i=int(9.93*SR); bus_sfx[:,i:int(10.0*SR)]*=0.0
# ---------------- drop 10.0 - 16
ts=time_of_tau3_swish()
add(bus_sfx,10.0,drop808(),1.0)
add(bus_sfx,ts,swish_snd(),1.0)
add(bus_sfx,ts,ding(),0.35)
add(bus_sfx,10.95,ding(),0.5)
add(bus_sfx,14.4,whoosh(0.35),0.5)
add(bus_sfx,12.0,whoosh(0.5),0.35)
lead_notes=[440,523.3,659.3,784,659.3,523.3,440,392]
bass_d={0:(55,3),3:(55,2),6:(65.4,2),8:(55,2),10:(49,3),13:(55,2),14:(61.7,1)}
kick_times=[]
for bar in range(5,8):   # bars at 10,12,14
    for s in (0,4,8,12): 
        t0=steps(bar,s)
        if t0>=10.0: 
            add(bus_drop,t0,kick(1.0),1.0); kick_times.append(t0)
    for s in (4,12): add(bus_drop,steps(bar,s),clap(),0.6)
    for s in range(0,16): add(bus_drop,steps(bar,s),hat(s%4==2),0.3 if s%2 else 0.22,pan=0.3 if s%2 else -0.3)
    for s,(f,l) in bass_d.items(): add(bus_drop,steps(bar,s),bass(f,l*STEP*1.1),0.85)
    for s in range(16):
        add(bus_drop,steps(bar,s),pluck(lead_notes[s%8]*(1 if bar%2==1 else 1.122) ),0.32,pan=-0.2 if s%2 else 0.2)
i0=int(10.0*SR); 
bus_drop[:,:i0]=0
# slow-mo replay lowpass feel 12.0-14.4
lpd=np.stack([lp(bus_drop[0],700),lp(bus_drop[1],700)])
m=np.zeros(N,np.float32); a=int(12.0*SR); b=int(14.4*SR); m[a:b]=1
m=np.convolve(m,np.ones(2000)/2000,'same')
bus_drop=bus_drop*(1-m)+lpd*m
# end loop dip
e0=int(15.75*SR); bus_drop[:,e0:]*=np.linspace(1,0.0,N-e0)
# sidechain duck on bass/lead is skipped; mix
mix=bus_pre*0.8+bus_drop*0.85+bus_sfx*0.9
mix=np.tanh(mix*1.25)/np.tanh(1.25)
peak=np.max(np.abs(mix)); mix=mix/peak*0.89
# tiny fade in/out
mix[:,:200]*=np.linspace(0,1,200); mix[:,-300:]*=np.linspace(1,0,300)
pcm=(np.clip(mix.T,-1,1)*32767).astype('<i2')
with wave.open('audio.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print('audio ok',N/SR,'peak',peak)
