import time, math, csv
from pathlib import Path
import cv2, pygame, numpy as np
from ultralytics import YOLO
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CAMERA_INDEX, YOLO_MODEL, CONFIDENCE_THRESHOLD, GAME_DURATION, LEVELS, LEADERBOARD_FILE

class Game:
    def __init__(self):
        pygame.init()
        try: pygame.mixer.init()
        except pygame.error: pass
        self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("AI Target Arena - YOLO Live Detection")
        self.clock=pygame.time.Clock()
        self.font=pygame.font.SysFont("Segoe UI",22,bold=True)
        self.big=pygame.font.SysFont("Segoe UI",46,bold=True)
        self.small=pygame.font.SysFont("Segoe UI",17)
        self.cap=cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,640); self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,480)
        if not self.cap.isOpened(): raise RuntimeError("Webcam could not be opened.")
        self.model=YOLO(YOLO_MODEL)
        self.running=True; self.started=False; self.finished=False
        self.level=1; self.score=0; self.hits=0; self.misses=0; self.combo=0; self.best_combo=0
        self.target=(450,390); self.start_time=0; self.detections=[]; self.fps=0; self.flash=""; self.flash_until=0

    def tone(self,freq,duration=90):
        try:
            sr=44100; n=int(sr*duration/1000); t=np.arange(n)/sr
            a=(np.sin(2*np.pi*freq*t)*32767*.15).astype(np.int16)
            pygame.sndarray.make_sound(np.column_stack((a,a))).play()
        except Exception: pass

    def new_target(self):
        r=LEVELS[self.level]["size"]
        self.target=(np.random.randint(r+25,890-r-25),np.random.randint(130+r,730-r))

    def start(self):
        self.started=True; self.finished=False; self.level=1
        self.score=0; self.hits=0; self.misses=0; self.combo=0; self.best_combo=0
        self.start_time=time.time(); self.new_target()

    def accuracy(self):
        total=self.hits+self.misses
        return self.hits/total*100 if total else 0

    def action(self,x,y):
        if not self.started or self.finished: return
        tx,ty=self.target; r=LEVELS[self.level]["size"]
        if (x-tx)**2+(y-ty)**2<=r*r:
            self.hits+=1; self.combo+=1; self.best_combo=max(self.best_combo,self.combo)
            mult=1+min(self.combo//5,4)*.25
            earned=int(LEVELS[self.level]["points"]*mult); self.score+=earned
            self.flash=f"+{earned}"; self.flash_until=time.time()+.6; self.tone(880); self.new_target()
            if self.hits>=LEVELS[self.level]["hits"]:
                if self.level<4:
                    self.level+=1; self.hits=0; self.flash=f"LEVEL {self.level}"
                    self.flash_until=time.time()+1; self.tone(990,140); self.new_target()
                else: self.finish()
        else:
            self.misses+=1; self.combo=0; self.flash="MISS"; self.flash_until=time.time()+.4; self.tone(220,120)

    def finish(self):
        if self.finished: return
        self.finished=True; self.tone(220,220)
        p=Path(LEADERBOARD_FILE); exists=p.exists()
        with p.open("a",newline="",encoding="utf8") as f:
            w=csv.writer(f)
            if not exists: w.writerow(["player","score","level","hits","misses","accuracy","date"])
            w.writerow(["Player",self.score,self.level,self.hits,self.misses,f"{self.accuracy():.1f}",time.strftime("%Y-%m-%d %H:%M")])

    def draw_text(self,s,font,x,y,c=(235,238,245)):
        self.screen.blit(font.render(str(s),True,c),(x,y))

    def run(self):
        self.start(); prev=time.time()
        while self.running:
            for e in pygame.event.get():
                if e.type==pygame.QUIT: self.running=False
                elif e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_ESCAPE: self.running=False
                    elif e.key==pygame.K_RETURN and (not self.started or self.finished): self.start()
                elif e.type==pygame.MOUSEBUTTONDOWN and e.button==1: self.action(*pygame.mouse.get_pos())

            ok,fr=self.cap.read()
            if ok:
                fr=cv2.flip(fr,1)
                result=self.model.predict(fr,conf=CONFIDENCE_THRESHOLD,verbose=False)[0]
                self.detections=[]
                if result.boxes is not None:
                    for b in result.boxes:
                        x1,y1,x2,y2=map(int,b.xyxy[0].tolist()); conf=float(b.conf[0])
                        label=result.names[int(b.cls[0])]
                        self.detections.append((x1,y1,x2,y2,label,conf))
                preview=cv2.cvtColor(cv2.resize(fr,(900,675)),cv2.COLOR_BGR2RGB)
                surface=pygame.surfarray.make_surface(preview.swapaxes(0,1))
            else: surface=None

            now=time.time(); self.fps=1/max(now-prev,1e-6); prev=now
            if self.started and not self.finished and now-self.start_time>=GAME_DURATION: self.finish()

            self.screen.fill((10,13,19))
            pygame.draw.rect(self.screen,(17,20,28),(0,0,1200,82))
            self.draw_text("TARGET ARENA",self.font,28,27)
            self.draw_text(f"LEVEL {self.level}",self.font,430,27,(110,210,255))
            self.draw_text(f"SCORE {self.score}",self.font,600,27,(255,210,90))
            left=max(0,int(GAME_DURATION-(now-self.start_time))) if self.started and not self.finished else 0
            self.draw_text(f"TIME {left:02d}",self.font,850,27,(120,235,160))

            if surface: self.screen.blit(surface,(0,82))
            for x1,y1,x2,y2,label,conf in self.detections:
                rect=(int(x1*900/640),int(y1*675/480)+82,int((x2-x1)*900/640),int((y2-y1)*675/480))
                pygame.draw.rect(self.screen,(80,230,140),rect,2)
                self.draw_text(f"{label} {conf:.0%}",self.small,rect[0],rect[1],(80,230,140))

            tx,ty=self.target; r=LEVELS[self.level]["size"]
            pygame.draw.circle(self.screen,(225,55,65),(tx,ty),r)
            pygame.draw.circle(self.screen,(245,245,245),(tx,ty),max(5,r-12))
            pygame.draw.circle(self.screen,(225,55,65),(tx,ty),max(3,r-24))

            mx,my=pygame.mouse.get_pos()
            pygame.draw.circle(self.screen,(255,255,255),(mx,my),18,2)
            pygame.draw.line(self.screen,(255,255,255),(mx-28,my),(mx+28,my),2)
            pygame.draw.line(self.screen,(255,255,255),(mx,my-28),(mx,my+28),2)

            pygame.draw.rect(self.screen,(25,29,40),(930,105,245,600),border_radius=16)
            self.draw_text("LIVE STATUS",self.font,955,130)
            vals=[("HITS",self.hits),("MISSES",self.misses),("ACCURACY",f"{self.accuracy():.1f}%"),("COMBO",f"x{self.combo}"),("YOLO TARGETS",len(self.detections)),("FPS",int(self.fps))]
            y=185
            for a,b in vals:
                self.draw_text(a,self.small,955,y,(155,165,185)); self.draw_text(b,self.font,955,y+23); y+=78

            if not self.started: self.draw_text("PRESS ENTER TO START",self.big,330,355)
            elif self.finished:
                self.draw_text("GAME OVER",self.big,370,345)
                self.draw_text("Press ENTER to play again",self.font,455,405)
            elif time.time()<self.flash_until: self.draw_text(self.flash,self.big,380,105,(255,225,90))

            pygame.display.flip(); self.clock.tick(FPS)

    def close(self):
        self.cap.release(); pygame.quit()
