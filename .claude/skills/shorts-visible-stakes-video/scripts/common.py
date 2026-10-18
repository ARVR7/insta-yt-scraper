import numpy as np, math
W,H=1080,1920; FPS=30; DUR=16.0
G=2400.0; R=48.0; FLOOR=1560.0
RIMC=(780.0,820.0); RIMHW=105.0; RIM_Y=820.0
BOARD_X=920.0; BOARD_Y0=540.0; BOARD_Y1=880.0
START=(90.0,1720.0)

def launch(target,T):
    vx=(target[0]-START[0])/T
    vy=(target[1]-START[1]-0.5*G*T*T)/T
    return vx,vy

def simulate(v0,dur=6.0,dt=1/1200.):
    n=int(dur/dt)+1
    X=np.zeros(n);Y=np.zeros(n);A=np.zeros(n)
    x,y=START;vx,vy=v0;a=0.0
    ev=[]
    edges=[(RIMC[0]-RIMHW,RIM_Y+6),(RIMC[0]+RIMHW,RIM_Y+6)]
    above=True
    for i in range(n):
        X[i]=x;Y[i]=y;A[i]=a
        vy+=G*dt; x+=vx*dt; y+=vy*dt
        a+=(4.0+vx/R*0.25)*dt
        if RIM_Y<y<RIM_Y+170 and abs(x-RIMC[0])<RIMHW and vy>0:
            vx*=0.9965; vy*=0.9993
        t=i*dt
        for ex,ey in edges:
            dx,dy=x-ex,y-ey; d=math.hypot(dx,dy)
            if d<R+7 and d>1e-6:
                nx,ny=dx/d,dy/d
                dn=vx*nx+vy*ny
                if dn<0:
                    vx-=1.55*dn*nx; vy-=1.55*dn*ny
                    x=ex+nx*(R+7); y=ey+ny*(R+7)
                    ev.append(('rim',t))
        if x+R>BOARD_X and BOARD_Y0<y<BOARD_Y1 and vx>0:
            vx=-vx*0.6; x=BOARD_X-R; ev.append(('board',t))
        if y+R>FLOOR and vy>0 and y<FLOOR+300 and not (x<200 and t<0.5):
            # floor only counts once ball is above ground plane (launch comes from foreground)
            pass
        if above and y>RIM_Y and abs(x-RIMC[0])<RIMHW and y<RIM_Y+60 and t>0.5:
            ev.append(('swish',t)); above=False
    return X,Y,A,ev

# foreground launch: floor collision only after ball has risen above the floor line once
def simulate2(v0,dur=6.0,dt=1/1200.):
    n=int(dur/dt)+1
    X=np.zeros(n);Y=np.zeros(n);A=np.zeros(n)
    x,y=START;vx,vy=v0;a=0.0
    ev=[]
    edges=[(RIMC[0]-RIMHW,RIM_Y+6),(RIMC[0]+RIMHW,RIM_Y+6)]
    swished=False; airborne=False
    for i in range(n):
        X[i]=x;Y[i]=y;A[i]=a
        t=i*dt
        vy+=G*dt; x+=vx*dt; y+=vy*dt
        a+=(4.0+vx/R*0.25)*dt
        if y+R<FLOOR-30: airborne=True
        if RIM_Y<y<RIM_Y+170 and abs(x-RIMC[0])<RIMHW and vy>0:
            vx*=0.9965; vy*=0.9993
        for ex,ey in edges:
            dx,dy=x-ex,y-ey; d=math.hypot(dx,dy)
            if d<R+7 and d>1e-6:
                nx,ny=dx/d,dy/d; dn=vx*nx+vy*ny
                if dn<0:
                    vx-=1.55*dn*nx; vy-=1.55*dn*ny
                    x=ex+nx*(R+7); y=ey+ny*(R+7); ev.append(('rim',t))
        if x+R>BOARD_X and BOARD_Y0<y<BOARD_Y1 and vx>0:
            vx=-vx*0.6; x=BOARD_X-R; ev.append(('board',t))
        if airborne and y+R>FLOOR and vy>0:
            y=FLOOR-R; 
            if abs(vy)>200: ev.append(('floor',t))
            vy=-vy*0.5; vx*=0.85
        if (not swished) and RIM_Y+8<y<RIM_Y+60 and abs(x-RIMC[0])<RIMHW and t>0.5 and not any(e[0]=='rim' for e in ev):
            ev.append(('swish',t)); swished=True
    return X,Y,A,ev,dt

V1=launch((631,793),1.1)
V2=launch((540,820),1.15)
V3=launch((780,820),1.15)
SIMS={1:simulate2(V1),2:simulate2(V2),3:simulate2(V3)}

def ball(att,tau):
    X,Y,A,ev,dt=SIMS[att]
    f=max(0.0,tau)/dt
    i=int(f); i=min(i,len(X)-2); fr=f-i
    return (X[i]*(1-fr)+X[i+1]*fr, Y[i]*(1-fr)+Y[i+1]*fr, A[i]*(1-fr)+A[i+1]*fr)

def events(att,kind):
    return [t for k,t in SIMS[att][3] if k==kind]

# ---------- timeline ----------
def smooth(u):
    u=min(1.0,max(0.0,u)); return u*u*(3-2*u)

TAU_FREEZE=1.07
def slow_tau(u):
    # integral of rate r(u)=0.18+0.82*smooth((u-0.7)/0.5), u seconds after unfreeze
    if u<=0: return TAU_FREEZE
    s=np.linspace(0,u,max(2,int(u*400)))
    r=0.25+0.75*np.array([smooth((x-0.6)/0.5) for x in s])
    return TAU_FREEZE+float(np.trapezoid(r,s))

def ball_clock(t):
    """returns (att,tau) for scene ball at wall time t"""
    if t<2.0: return 1,0.30+0.375*t
    if t<3.5: return 1,1.05+0.5*(t-2.0)
    if t<5.5: return 2,(t-3.5)
    if t<6.5: return 2,2.0
    if t<7.0: return 3,(t-6.5)
    if t<10.0: return 3,TAU_FREEZE
    if t<12.0: return 3,slow_tau(t-10.0)
    if t<14.4: return 3,0.95+(t-12.0)*0.27
    return 3,2.4+(t-14.4)

def time_of_tau3_swish():
    ts=events(3,'swish')[0]
    for k in range(0,4000):
        t=10+k/1000.
        if slow_tau(t-10)>=ts: return t
    return 10.3

TIMER_PTS=[(0,15.0),(2.0,13.0),(3.5,8.6),(5.5,3.4),(6.5,1.2),(7.0,1.2),(10.0,1.2)]
def timer_val(t):
    if t>=10.0:
        ts=time_of_tau3_swish()
        return 0.71 if t>=ts else 1.2-(1.2-0.71)*((t-10.0)/(ts-10.0))
    ts=[p[0] for p in TIMER_PTS]; vs=[p[1] for p in TIMER_PTS]
    return float(np.interp(t,ts,vs))

if __name__=='__main__':
    for a in (1,2,3):
        print(a,SIMS[a][3][:8])
    print('swish wall time',time_of_tau3_swish())
    for tt in (0,1,2,2.3,3.0,4,5,6.9,10,10.3,11,12,14):
        print(tt,ball_clock(tt),[round(v) for v in ball(*ball_clock(tt))],timer_val(tt))
