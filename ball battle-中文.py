import pygame,random,_thread,time,sys
from math import *
from pygame.locals import *
from mylib import *
from numpy import arctan

#初始化，常量和变量
#初始化
pygame.init()
screen=pygame.display.set_mode((900,600))
pygame.display.set_caption("球球人机作战")
#字体和文字常量
myfont=pygame.font.Font("C:/Windows/Fonts/Simhei.ttf",20)
title_font=pygame.font.Font("C:/Windows/Fonts/STXINWEI.TTF",40)
myfs=pygame.font.Font("C:/Windows/Fonts/Simhei.ttf",15)
rank_title=myfs.render("排行榜",True,(255,125,0))
#颜色常量
GRAY100=100,100,100
GRAY150=150,150,150
GRAY200=200,200,200
BLACK=0,0,0
GREEN1=0,200,0
WHITE=255,255,255
BLUE1=44,53,255
RED=255,0,0
#自动球名字
nicknames=[ 
    "Happy",
    "大家好",
    "→_→",
    "今橙",
    "高级玩家",
    "BuggyPlayer",
    "飞阳",
    "Python",
    "Java",
    "C",
    "Visual",
    "Basic",
    "人机",
    "Pygame"
]
#变量
show_dest=True #显示玩家移动方向
show_ab_dest=False #显示自动球移动方向
width=3000
height=3000
playerx=width/2 #playerx,playery这两个变量不常用，还是保留吧
playery=height/2
showhelp=True
bonuscount=500

#各种类
class Ball(): #移动的球的父类（不包括不移动的食物）
    def __init__(self,x,y,angle,radius):
        self.radius=radius
        self.mass=sq(radius)
        self.mass=self.radius*self.radius
        self.x=x
        self.y=y
        self.angle=angle
        self.speed=0.2
        self.x_in=0 #根据角度决定移动时x和y增加或减少
        self.y_in=0
        self.a1=0 #∠1
        self.color=20,20,20
        self.a=0
        self.b=0
        self.c=0
        self.tbcount=0 #touch boundary count
        self.name=""
        self.type=""
        self.chasing=False
    def reinit(self):
        self.x=random.randint(0,width)
        self.y=random.randint(0,height)
        self.mass=900
        self.radius=30
    def touch_boundary(self):
        pass
    def update(self):   
        if self.x<self.radius:  #防过界和反弹
            self.x=self.radius
            if self.chasing==False and self.type=="AIPlayer":
                self.angle=360-self.angle
        if self.y<self.radius:
            self.y=self.radius
            if self.chasing==False and self.type=="AIPlayer":
                self.angle=180-self.angle
        if self.x>width-self.radius:
            self.x=width-self.radius
            if self.chasing==False and self.type=="AIPlayer":
                self.angle=360-self.angle
        if self.y>height-self.radius:
            self.y=height-self.radius
            if self.chasing==False and self.type=="AIPlayer":
                self.angle=180-self.angle
        if self.angle>=360: #角度处理（0≤angle<360）
            self.angle-=360
        if self.angle<0:
            self.angle+=360
        if self.angle==0 or self.angle==180: #角度处理（根据移动方向转换自身角度和三角函数角度）
            self.x_in=0
        elif self.angle==90 or self.angle==270:
            self.y_in=0
        if self.angle>0 and self.angle<90:
            self.x_in=1
            self.y_in=-1
            self.a1=90-self.angle
        elif self.angle>90 and self.angle<180:
            self.x_in=1
            self.y_in=1
            self.a1=self.angle-90
        elif self.angle>180 and self.angle<270:
            self.x_in=-1
            self.y_in=1
            self.a1=270-self.angle
        elif self.angle>270 and self.angle<360:
            self.x_in=-1
            self.y_in=-1
            self.a1=self.angle-270
        a=abs(cos(radians(self.a1))*self.speed) #三角函数计算和移动
        b=abs(sin(radians(self.a1))*self.speed)
        self.x+=a*self.x_in
        self.y+=b*self.y_in
        self.a=a
        self.b=b
        self.mass-=0.0001*self.mass #适当减少体重
        self.radius=int(sqrt(self.mass)) #根据质量计算半径
class AIPlayer(Ball): #自动球
    def __init__(self,x,y,name=""):
        super().__init__(x,y,random.randint(1,360)+0.1,30)
        self.type="AIPlayer"
        self.masstag1=myfs.render("",True,BLACK)
        self.color=random.randint(0,255),random.randint(0,255),random.randint(0,255)
        if name=="":
            try: #防止名单中名字不够用
                n=random.randint(0,len(nicknames)-1)
                self.name=nicknames[n]
                del nicknames[n]
            except:
                self.name="用户"+str(random.randint(0,100))
        else:
            self.name=name
        self.nametag=myfont.render(self.name,True,BLACK)
        self.nametag1=myfs.render(self.name,True,BLACK)
        self.masstag=myfont.render(str(self.mass),True,BLACK)
    def update(self):
        super().update()
        self.radius=sqrt(self.mass)
        self.masstag=myfont.render(str(int(self.mass)),True,BLACK)
        self.masstag1=myfs.render(str(int(self.mass)),True,BLACK)
        self.speed=2+500/self.mass
    def display(self):
        x=self.x-(player.x-450)
        y=self.y-(player.y-300)
        pygame.draw.circle(screen,self.color,(int(x),int(y)),int(self.radius))
        screen.blit(self.nametag,(int(x)-self.radius,int(y)-30))
        screen.blit(self.masstag,(int(x)-self.radius,int(y)))
        if show_ab_dest:
            pygame.draw.line(screen,(0,0,0),(int(x),int(y)),(int(x)+self.a*100*self.x_in,int(y)+self.b*100*self.y_in))
class Player(Ball): #玩家
    def __init__(self):
        super().__init__(playerx,playery,0.1,30)
        self.type="Player"
        self.name="玩家"
        self.color=0,0,255
        self.speed=1
        self.nametag=myfont.render("玩家",True,BLACK)
        self.nametag1=myfs.render("玩家",True,BLACK)
        self.masstag=myfont.render("0",True,BLACK)
        self.masstag1=myfs.render("",True,BLACK)
        self.autospeed=True
    def update(self):
        super().update()
        self.masstag=myfont.render(str(int(self.mass)),True,BLACK)
        self.masstag1=myfs.render(str(int(self.mass)),True,BLACK)
        if self.autospeed:
            self.speed=2+500/self.mass
        else:
            self.speed-=1
            if self.speed<3+500/self.mass:
                self.autospeed=True
    def display(self):
        pygame.draw.circle(screen,self.color,(450,300),int(self.radius))
        if show_dest:
            pygame.draw.line(screen,(0,0,0),(450,300),(450+self.a*100*self.x_in,300+self.b*100*self.y_in))
        screen.blit(self.nametag,(450-self.radius,270))
        screen.blit(self.masstag,(450-self.radius,300))
class PlayerPart(Ball):
    def __init__(self,angle,mass):
        self.color=player.color
        self.mass=mass
        self.radius=sqrt(mass)
        self.type="PlayerPart"
        self.name="玩家"
        self.speed=50/player.speed
        self.angle=angle
        self.autospeed=True
        self.x=player.x+2
        self.y=player.y-2
        self.masstag=myfont.render(str(int(self.mass)),True,BLACK)
        self.masstag1=myfs.render(str(int(self.mass)),True,BLACK)
        self.nametag=player.nametag
        self.nametag1=player.nametag1
        self.chasing=False
    def update(self):
        super().update()
        self.speed=2+500/self.mass
        self.masstag=myfont.render(str(int(self.mass)),True,BLACK)
        self.masstag1=myfs.render(str(int(self.mass)),True,BLACK)
    def display(self):
        x=self.x-(player.x-450)
        y=self.y-(player.y-300)
        pygame.draw.circle(screen,self.color,(int(x),int(y)),int(self.radius))
        screen.blit(self.nametag,(int(x)-self.radius,int(y)-30))
        screen.blit(self.masstag,(int(x)-self.radius,int(y)))
        if show_ab_dest:
            pygame.draw.line(screen,(0,0,0),(int(x),int(y)),(int(x)+self.a*100*self.x_in,int(y)+self.b*100*self.y_in))
    
        
class SmallFood(): #小食物（不会移动的）
    def __init__(self):
        self.x=random.randint(0,width)
        self.y=random.randint(0,height)
        self.color=random.randint(0,255),random.randint(0,255),random.randint(0,255)
    def display(self):
        x=self.x-(player.x-450)
        y=self.y-(player.y-300)
        pygame.draw.circle(screen,self.color,(int(x),int(y)),5)
    def update(self):
        for p in balls:
            distance=sqrt(sq(p.x-self.x)+sq(p.y-self.y))
            if distance<p.radius-5:
                p.mass+=100
                self.x=random.randint(0,width)
                self.y=random.randint(0,height)
        
#数学函数
def get_distance(ball1,ball2):
    return sqrt(sq(ball1.x-ball2.x)+sq(ball1.y-ball2.y))
def sq(num): #平方
    return num*num
def get_01(num): #正数返回1，0返回0，负数返回-1
    if num<0:
        return -1
    elif num==0:
        return 0
    elif num>0:
        return 1

#显示球吃球信息
kill_info=[] #球吃球信息列表
killer=False #是否需要显示球吃球信息
def kill_info_display_timer_thread(): #球吃球信息显示计时
    global killer
    while True:
        time.sleep(2)
        if len(kill_info)!=0:
            del kill_info[0]
        else:
            break
    killer=False
def display_kill(ball1,ball2):
    global killer
    if ball1.type in ["PlayerPart","Player"] and ball2.type in ["PlayerPart","Player"]:
        return
    str1=ball1.name+" 吃了 "+ball2.name
    kill_info.append(title_font.render(str1,True,RED))
    if killer:
        return #防止线程同一时间被多次调用
    killer=True
    _thread.start_new_thread(kill_info_display_timer_thread,())

#创建和初始化对象
smallfoods=[] #小食物列表
for i in range(bonuscount):
    smallfoods.append(SmallFood())
if "auto" in sys.argv:
    player=AIPlayer(1000,1000) 
else:
    player=Player()
balls=[AIPlayer(1100,1100,"我的好朋友"),player]
for i in range(13): #添加球
    balls.append(AIPlayer(random.randint(0,width),random.randint(0,height)))

#显示帮助
helptext=[
    myfont.render("球球人机作战 - V0.0.3",True,GREEN1),
    myfont.render("用←→箭旋调整运动方向，用W,A,S,D键快速切换球上下左右运动方向；",True,BLACK),
    myfont.render("按Tab显示/隐藏玩家运动方向指示线；",True,BLACK),
    myfont.render("按O显示/隐藏其他球运动方向指示线；",True,BLACK),
    myfont.render("按空格键分身。",True,BLACK),
    myfont.render("",True,BLACK),
    myfont.render("更新内容：增加玩家分身功能",True,BLACK),
    myfont.render("",True,BLACK),
    myfont.render("此程序作者：BuggyPlayer  更新日期：2020年5月2日",True,BLACK)
]
def cancelhelp():
    global showhelp
    time.sleep(5)
    showhelp=False
_thread.start_new_thread(cancelhelp,())

#游戏核心运行
def game_thread():
    while True:
        try:
            loop()
        except:
            pass
def set_angle(ball1,ball2):
    if ball1.type=="Player":
        return
    elif ball1.type=="PlayerPart":
        if ball1.autospeed==False:
            return
        ball2=player
    distx=ball1.x-ball2.x
    disty=ball1.y-ball2.y
    a1=abs((arctan(disty/distx))/pi*180)
    in_x=get_01(-distx)
    in_y=get_01(-disty)
    if in_x==1 and in_y==-1:
        ball1.angle=90-a1
    elif in_x==1 and in_y==1:
        ball1.angle=a1+90
    elif in_x==-1 and in_y==1:
        ball1.angle=270-a1
    elif in_x==-1 and in_y==-1:
        ball1.angle=a1+270
    ball1.in_x=in_x
    ball1.in_y=in_y
def ball_die(eater,failer,eindex,findex):
    global balls
    display_kill(eater,failer)
    if eater.type=="PlayerPart" and failer.type=="Player":
        failer.mass+=eater.mass
        del balls[eindex]
    elif eater.type in ["PlayerPart","Player"] and failer.type=="PlayerPart":
        eater.mass+=failer.mass
        del balls[findex]
    elif eater.type=="AIPlayer" and failer.type=="Player":
        for i in range(len(balls)):
            if balls[i].type=="PlayerPart":
                player.mass=balls[i].mass
                player.x=balls[i].x
                player.y=balls[i].y
                del balls[i]
                return
        failer.reinit()
    elif eater.type=="AIPlayer" and failer.type=="PlayerPart":
        eater.mass+=failer.mass
        del balls[findex]
    else:
        eater.mass+=failer.mass
        failer.reinit()
def loop():
    for p in balls: #更新球
        p.update()
        if p.radius>0.5*width:
            p.reinit()
    try:
        balls.sort(key=lambda x:x.mass,reverse=True)
    except:
        pass
    for i in range(len(balls)-1):
        set_angle(balls[i],balls[i+1])
        balls[i].chasing=True
    balls[len(balls)-1].chasing=False
    if balls[len(balls)-1].type=="PlayerPart":
        set_angle(balls[len(balls)-1],player)
        balls[len(balls)-1].chasing=True
    for i in range(len(balls)):
        for j in range(len(balls)):
            if i==j:
                continue
            if get_distance(balls[i],balls[j])<abs(balls[i].radius-balls[j].radius): #球吃球
                if balls[i].radius>balls[j].radius:
                    ball_die(balls[i],balls[j],i,j)
                elif balls[i].radius<balls[j].radius:
                    ball_die(balls[j],balls[i],j,i)
    for b in smallfoods:
        b.update()
_thread.start_new_thread(game_thread,())

#游戏UI
while True:
    for event in pygame.event.get(): #事件处理
        if event.type==QUIT:
            sys.exit()
        elif event.type==KEYDOWN:
            if event.key==K_TAB:
                if show_dest:
                    show_dest=False
                else:
                    show_dest=True
            elif event.key==K_o:
                if show_ab_dest:
                    show_ab_dest=False
                else:
                    show_ab_dest=True
            elif event.key==K_w:
                player.angle=0.1
            elif event.key==K_d:
                player.angle=90.1
            elif event.key==K_s:
                player.angle=180.1
            elif event.key==K_a:
                player.angle=270.1
            elif event.key==K_r:
                kill_info=[]
            elif event.key==K_SPACE and player.mass>500:
                balls.append(PlayerPart(player.angle,player.mass/2))
                player.mass=player.mass/2
                player.autospeed=False
                player.speed=50/player.speed
    pressed_keys=pygame.key.get_pressed()
    if pressed_keys[K_LEFT]:
        player.angle-=1
    if pressed_keys[K_RIGHT]:
        player.angle+=1
    screen.fill(WHITE) #从此往下：绘制画面
    for b in smallfoods:
        if get_distance(b,player)<550:
            b.display()
    for i in range(31): #绘制竖线
        xtemp=int((player.x-450)/30)*30-player.x+450
        pygame.draw.line(screen,GRAY150,(xtemp+i*30,0),(xtemp+i*30,600))
        if player.x-450+i*20 in [0,width]:
            pygame.draw.line(screen,BLACK,(xtemp+i*30,0),(xtemp+i*30,600),3)
    for i in range(21): #绘制横线
        ytemp=int((player.y-300)/30)*30-player.y+300
        pygame.draw.line(screen,GRAY150,(0,ytemp+i*30),(900,ytemp+i*30))
        if player.y-300+i*20 in [0,height]:
            pygame.draw.line(screen,BLACK,(0,ytemp+i*30),(900,ytemp+i*30),3)
    for j in range(len(balls)): #显示球
        i=len(balls)-j-1
        try:
            if get_distance(balls[i],player)-balls[i].radius<550:
                balls[i].display()
        except:
            pass
    for i in range(len(kill_info)): #显示球吃球信息
        try:
            screen.blit(kill_info[i],(140,i*50+40))
        except:
            pass
    pygame.draw.rect(screen,BLUE1,(15,15,110,110))
    pygame.draw.rect(screen,GRAY100,(20,20,100,100)) #显示小地图背景
    for p in balls: #在小地图上显示球
        pygame.draw.circle(screen,(255,100,0),(20+int(p.x*(100/width)),int(20+p.y*(100/width))),5)
    pygame.draw.circle(screen,(255,250,0),(20+int(player.x*(100/width)),int(20+player.y*(100/width))),5)
    screen.blit(rank_title,(780,10))
    for i in range(len(balls)):
        try:
            screen.blit(balls[i].nametag1,(730,30+20*i))
            screen.blit(balls[i].masstag1,(830,30+20*i))
        except:
            pass
    if showhelp:
        pygame.draw.rect(screen,GRAY200,(100,100,700,400))
        for i in range(len(helptext)):
            screen.blit(helptext[i],(110,110+30*i))
    pygame.display.update()