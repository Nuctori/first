import random
from Player import Player
from Bullet import Bullet

#角色位置 1-3 6-3
#玩家对象 四方向移动 卡组 行动值 当前坐标
#弹幕对象 发射坐标 当前坐标 角度 速度 威力
#每次回合结算，初始化地图 重新渲染所有坐标
#现在先分拆函数  玩家类 子弹类   符卡类 地图类
player1 = 100 #定义玩家的号码
player2 = 101
    
'''
星弹:10  
小玉:11  快速 少量伤害
中玉:12  中速 中等伤害
大玉:13  慢速 大量伤害
菱弹:14 
激光:15
'''

class Map(): 
    #地图需要两份 一份显示玩家1弹幕 一份显示玩家2的弹幕
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
                if Bullet.y > 7 or  Bullet.x > 4:#再嵌套下去的话，圈复杂度爆炸！！！
                    continue
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
    #传入二维列表地图，生成文本型地图
    def mainrender(line,i):
        ourprint =""
        ourprint += "\n｜"
        for item in line:
            if item == 0:
                ourprint += "　｜"
            if item == 100:
                if i == 2:
                    ourprint += "△ ｜"#玩家1
                else:
                    ourprint += "▽ ｜"#玩家1
            if item == 101:
                if i == 2:
                    ourprint += "▼ ｜" #玩家2
                else:
                    ourprint += "▲ ｜"#玩家1


            if item == 10:
                ourprint += "☆ ｜" #星弹
            if item == 55:
                ourprint += "※ ｜" #弹幕重叠
        return ourprint

    i = 0
    str_map = []
    ourprint = ""
    
    for gamemap in gamemap_tuple:
        i += 1 
        ourprint = "玩家{}弹幕图".format(i)
        ourprint += "\n______________________"

        if i == 1:
            for line in reversed(gamemap):
                ourprint += mainrender(line,i)
            ourprint += "\n￣￣￣￣￣￣￣￣￣￣￣"
            str_map.append(ourprint)
        else:    
            for line in gamemap:
                ourprint += mainrender(line,i)
            ourprint += "\n￣￣￣￣￣￣￣￣￣￣￣"
            str_map.append(ourprint)
    return str_map

    
def bullet_move(bullet_list,player): 

    #输入弹幕列表，让弹幕列表中子弹移动一步，输出弹幕列表中弹幕进行一次移动后的结果
    for bullet in bullet_list:
        for i in range(bullet.speed):
            bul = bullet.__next__() #？？
            if bul == None:
                bullet_list.remove(bullet)  

            elif  bul[0] == player[2].x and bul[1] == player[2].y: #弹幕碰撞到玩家1检测
                if bullet.player == player1:
                    print("biu！玩家2疮了！")
            elif  bul[0] == player[1].x and bul[1] == player[1].y: #弹幕碰撞到玩家2检测
                if bullet.player == player2:
                    print("biu！玩家1疮了！")


def time_end(cmds,player):
    i = 0  #一股C味
     #结束双方回合，进行回合运算，输入命令和玩家字典，给玩家对象和命令对象迭代
    for cmd in cmds:
        i += 1
        move = {"W":player[i].up, "A":player[i].right, "S":player[i].down,"D":player[i].left}
        for cmditem in cmd:
            if cmditem.isdigit():
                bullet_list.extend(player[i].handcard.useCard(cmditem)) 
            elif isinstance(cmditem,str):
                move[cmditem]()

    bullet_move(bullet_list,player) 
    strmap = rendermap(Map(player,bullet_list).getMap())
    return(strmap)

 

'''
'回合开始，执行抽卡函数，手牌，上限为8的数组，将卡片放入数组，根据输入序号，取出卡片 
'任务列表，一个队列，输入指令后 扣除行动点，指令进队 
'回合结算，取出队列指令，一条一条执行
'计算耗费，弹幕初始耗费，加速度耗费
'''


if __name__ == "__main__":
    bullet_list = []
    player={
        1:Player(player1),
        2:Player(player2)
    }
    strmap = rendermap(Map(player,bullet_list).getMap())
    print("已完成地图初始化")

    
    i = 0
    gameround = 0

    tips= '''指令 W,A,S,D 控制角色移动，指令B释放弹幕'''
    print(tips)
    while True:
        cmds = [[],[]]
        allow_input = {
        " ","W","A","S","D","E",
        "1","2","3","4","5","6","7","8","9"}
        #玩家1操作时 显示玩家2发射的弹幕
        for i in range(1,3):
            actpoint = 5
            havemove = False

            if i == 2:
                print(strmap[1])
            else:
                print(strmap[0])

            while True:
                cmd = input("玩家{}请输入你的命令:".format(i))
                if cmd in allow_input:
                    if cmd == " ":
                        if actpoint < 1:
                            print("行动点不足")
                        else:
                            actpoint -= 1
                            player[i].handcard.getCard()
                            player[i].handcard.showCard()
                    elif "WASD".find(cmd) != -1:
                        if actpoint < 1:
                            print("行动点不足")
                        elif havemove:
                            print("本回合你已经移动过了")
                        else:
                            actpoint -= 1
                            havemove = True
                            cmds[i-1].append(cmd.upper())
                    elif "123456789".find(cmd) != -1:
                        cost = player[i].handcard.cost(cmd)
                        if actpoint >= cost:
                            actpoint -= player[i].handcard.cost(cmd)
                            cmds[i-1].append(cmd)
                        else:
                            print('行动点不足')
                    else:
                        break
                else:
                    print('输入指令无效，请重新输入')
        
        strmap = time_end(cmds,player=player)
        gameround += 1
        print("第{}回合".format(gameround))
