import math

player1 = 100 #定义玩家的号码
player2 = 101
# 弹幕继承子弹类  参数 发射玩家 发射方向 发射角度
class Bullet(): #弹幕需要记录发射者   
    def __init__(self,Player,direction,angle,speed=1):
        self.player = Player.num

        self.x = Player.x
        self.y = Player.y 
        self.ox = Player.x
        self.oy = Player.y  
        self.ang = X_list(angle) # 弹幕的X轴偏移列表
        self.direction = direction

        # self.power = 1 #弹幕的伤害
        self.speed = speed #弹幕速度BB
        self.num = 10
        self.round = 0

    def active(self,Player):
        self.x = Player.x
        self.y = Player.y 
        self.ox = Player.x
        self.oy = Player.y 

    def __next__(self): 
        #我来演示一下什么叫做垃圾代码

        #Y轴移动计算
        if self.player == player1: #如果是玩家1发射的弹幕
            if self.y == 0 : #如果弹幕已经到达边界了
                return None #弹幕没了
            self.y -= 1 #弹幕往上射一格
        elif self.player == player2:
            if self.y == 7:
                return None
            self.y += 1

        #X轴移动计算   
        if self.direction == 0:
            if self.x < 4: 
                self.x = self.ox + self.ang[self.round] #右侧偏移
            else:
                return None
                    
        else:
            if self.x > 0: 
                self.x = self.ox - self.ang[self.round] #左侧偏移
            else:
                return None
        self.round += 1
        return self.x,self.y


def X_list(angle):  #改写成生成器啊！！！
    relist = []
    for i in range(0,7):
        relist.append(int(math.sin(math.pi/180*angle) * i))
    return relist