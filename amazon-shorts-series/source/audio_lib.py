import numpy as np, wave
from scipy.signal import lfilter, butter, sosfilt
DUR=17.0
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


BPM=130.0; B=60/BPM; G0=12.0-24*B
def bt(k): return G0+k*B
def crickets(d):
    out=np.zeros(int(d*SR))
    for _ in range(int(d*7)):
        t0=rs.uniform(0,d-0.2); f=rs.uniform(3800,4600); n=int(0.07*SR); tt_=np.arange(n)/SR
        chirp=np.sin(2*np.pi*f*tt_)*np.exp(-tt_*35)*(0.5+0.5*np.sign(np.sin(2*np.pi*55*tt_)))
        i=int(t0*SR); out[i:i+n]+=chirp[:len(out)-i]*0.05
    return out
def footstep(g=1.0):
    t=tt(0.14); n=bp(rs.randn(len(t)),200,1400)*np.exp(-t*40)*0.5
    th=np.sin(2*np.pi*(80+60*np.exp(-t*50))*t)*np.exp(-t*30)*0.6
    return (n+th)*g
def crackle(d):
    t=tt(d); x=np.zeros(len(t))
    for _ in range(int(d*90)):
        i=rs.randint(0,len(t)-300); n=rs.randint(30,260)
        x[i:i+n]+=rs.randn(n)*np.exp(-np.arange(n)/rs.uniform(15,60))*rs.uniform(0.2,0.9)
    return hp(x,1500)*0.5*np.minimum(1,t*20)*np.minimum(1,(d-t)*6)
def ping(f=1500):
    t=tt(0.9); return np.sin(2*np.pi*f*t)*np.exp(-t*4.5)*0.4+np.sin(2*np.pi*f*2*t)*np.exp(-t*8)*0.15
def paper():
    t=tt(0.3); return bp(rs.randn(len(t)),1500,8000)*np.sin(np.pi*np.clip(t/0.3,0,1))**2*0.5
def creak():
    t=tt(0.9); f=140+60*np.sin(2*np.pi*3.3*t)+80*t; ph=2*np.pi*np.cumsum(f)/SR
    return lp(np.sign(np.sin(ph))*0.5+rs.randn(len(t))*0.1,900)*np.sin(np.pi*np.clip(t/0.9,0,1))*0.5
