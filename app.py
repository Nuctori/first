
import math

#角色位置 1-3 6-3
#玩家对象 四方向移动 卡组 行动值 当前坐标
#弹幕对象 发射坐标 当前坐标 角度 速度 威力
#每次回合结算，初始化地图 重新渲染所有坐标

player1 = 100 #定义玩家的号码
player2 = 101

class Player():
    def __init__(self,num):
        self.num = num

        if self.num == 100:
            self.x = 2
            self.y = 7
            self.text = "△"
        elif self.num == 101:
            self.x = 2
            self.y = 0
            self.text = "▼"
        else:
            raise TypeError("只支持2名玩家，参数为100，或者为101")

    def up(self):
        if 0 < self.y <= 7:
            self.y += -1

    def down(self):
        if 0 <= self.y < 7:
            self.y += 1

    def left(self):
        if 0 <= self.x < 4:
            self.x += 1
            print(self.x)
            
    def right(self):
        if 0 < self.x <= 4:
            self.x += -1


def X_list(angle):  #改写成生成器啊！！！
    relist = []
    for i in range(0,7):
        relist.append(int(math.sin(math.pi/180*angle) * i))
    return relist

        



# 弹幕继承子弹类  参数 发射玩家 发射方向 发射角度
class Bullet(): #弹幕需要记录发射者   
    def __init__(self,Player,direction,angle):
        self.player = Player.num

        self.x = Player.x
        self.y = Player.y 
        self.ox = Player.x
        self.oy = Player.y  
        self.ang = X_list(angle) # 弹幕的X轴偏移列表
        self.direction = direction

        # self.power = 1 #弹幕的伤害
        self.speed = 1 #弹幕速度BB
        self.num = 10
        self.round = 0

    def __next__(self): 
        #我来演示一下什么叫做垃圾代码

        #Y轴移动计算
        if self.player == player1: #如果是玩家1发射的弹幕
            if self.y == 0: #如果弹幕已经到达边界了
                return None #弹幕没了
            self.y -= 1 #弹幕往上射一格
        elif self.player == player2:
            if self.y == 7:
                return None
            self.y += 1

        #X轴移动计算   
        if self.direction == 0:
            self.x = self.ox + self.ang[self.round] #右侧偏移
        else:
            self.x = self.ox - self.ang[self.round] #左侧偏移

        self.round += 1
        return self.x,self.y

class 小玉(Bullet):
    def __init__(self,Player,direction,angle):
        super().__init__(Player,direction,angle)
        self.speed = 2
        self.num = 10
    

'''
星弹:10  
小玉:11  快速 少量伤害
中玉:12  中速 中等伤害
大玉:13  慢速 大量伤害
菱弹:14 
激光:15
'''



class Map(): #地图需要两份 一份显示玩家1弹幕 一份显示玩家2的弹幕
    def __init__(self,player,bullet_list=None):
        self.gamemap1 = [([0]*5)for i in range(8)]
        self.gamemap2 = [([0]*5)for i in range(8)]
        self.bullets = bullet_list


    def getMap(self):
        self.gamemap1[player[1].y][player[1].x] = player[1].num
        self.gamemap1[player[2].y][player[2].x] = player[2].num

        self.gamemap2[player[1].y][player[1].x] = player[1].num
        self.gamemap2[player[2].y][player[2].x] = player[2].num
        if self.bullets is not None:
            for Bullet in self.bullets:
                if Bullet.player == player1:
                    if self.gamemap1[Bullet.y][Bullet.x] == 0:
                        self.gamemap1[Bullet.y][Bullet.x] = Bullet.num
                    else:
                        self.gamemap1[Bullet.y][Bullet.x] = 55
                elif Bullet.player == player2:
                    if self.gamemap2[Bullet.y][Bullet.x] == 0:
                        self.gamemap2[Bullet.y][Bullet.x] = Bullet.num
                    else:
                        self.gamemap2[Bullet.y][Bullet.x] = 55
        return self.gamemap1,self.gamemap2



def rendermap(gamemap_tuple):
    i = 0
    str_map = []
    #传入二维列表地图，生成文本型地图
    for gamemap in gamemap_tuple:
        i += 1 
        ourprint = "玩家{}弹幕图".format(i)
        ourprint += "\n______________________"
        for line in gamemap:
            ourprint += "\n｜"
            for item in line:
                if item == 0:
                    ourprint += "　｜"
                if item == 100:
                    ourprint += "△ ｜"#玩家1
                if item == 101:
                    ourprint += "▼ ｜" #玩家2
                if item == 10:
                    ourprint += "☆ ｜" #星弹
                if item == 55:
                    ourprint += "※ ｜" #弹幕重叠
        ourprint += "\n￣￣￣￣￣￣￣￣￣￣￣"
        str_map.append(ourprint)
    return str_map

    
def bullet_move(bullet_list,player): #输入弹幕列表，输出弹幕列表中弹幕进行一次移动后的结果
    for bullet in bullet_list:
        for i in range(bullet.speed):
            bul = bullet.__next__()
            if bul == None:
                bullet_list.remove(bullet)  

            elif  bul[0] == player[2].x and bul[1] == player[2].y: #弹幕碰撞到玩家2检测
                if bullet.player == player1:
                    print("biu！玩家2疮了！")
            elif  bul[0] == player[1].x and bul[1] == player[1].y: #弹幕碰撞到玩家2检测
                if bullet.player == player2:
                    print("biu！玩家1疮了！")

def time_end(cmd1,cmd2,player): #结束双方回合，进行回合运算
    for i in range(1,3):
        player_str = 'player[{}]'.format(i)
        act = {
            "W":player_str + '.up()',
            "A":player_str + '.right()',
            "S":player_str + '.down()',
            "D":player_str + '.left()',
            "B":'bullet_list.append(小玉(Player='+ player_str +',direction=1,angle=0))',
        }

        if i == 1:
            eval(act[cmd1])
        else:
            eval(act[cmd2]) 

    bullet_move(bullet_list,player) 
    strmap = rendermap(Map(player,bullet_list).getMap())
    return(strmap)



if __name__ == "__main__":
    bullet_list = []
    player={
        1:Player(player1),
        2:Player(player2)
    }
    strmap = rendermap(Map(player,bullet_list).getMap())
    print("已完成地图初始化")

    cmd1 = None
    cmd2 = None
    i = 0

    tips= '''指令 W,A,S,D 控制角色移动，指令B释放弹幕'''
    print(tips)
    
    while True:
        allow_input = {"W","A","S","D","B"}
        print(strmap[1]) #玩家1操作时 显示玩家2发射的弹幕
        while True:
            cmd1 = input("玩家1请输入你的命令:")
            if cmd1 in allow_input:
                break         
            else:
                print('输入指令无效，请重新输入')
        print(strmap[0]) #玩家2操作时 显示玩家1发射的弹幕
        while True:
            cmd2 = input("玩家2请输入你的命令:")
            if cmd2 in allow_input:
                break         
            else:
                print('输入指令无效，请重新输入')
        
        strmap = time_end(cmd1,cmd2,player=player)

        i += 1
        print("第{}回合".format(i))





'''
游戏流程
玩家1 行动{b
    移动，发射弹幕
}
玩家2 行动{
    移动，发射弹幕
}


   
'''


