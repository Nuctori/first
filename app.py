
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


class Bullet(Player): #弹幕需要记录发射者
    def __init__(self,Player):
        self.player = Player.num
        self.x = Player.x
        self.y = Player.y
        self.angle = 0
        self.power = 1
        self.num = 10

    def __next__(self): 
        #我来演示一下什么叫做垃圾代码
        if self.player == player1: #如果是玩家1发射的弹幕
            if self.y == 0: #如果弹幕已经到达边界了
                return None #弹幕没了
            self.y -= 1 #弹幕往上射一格
        elif self.player == player2:
            if self.y == 7:
                return None
            self.y += 1
        return self.x,self.y


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
        bul = bullet.__next__()
        if bul == None:
            bullet_list.remove(bullet)  

        elif  bul[0] == player[2].x and bul[1] == player[2].y: #弹幕碰撞到玩家2检测
            if bullet.player == player1:
                print("biu！玩家2疮了！")
        elif  bul[0] == player[1].x and bul[1] == player[1].y: #弹幕碰撞到玩家2检测
            if bullet.player == player2:
                print("biu！玩家1疮了！")

if __name__ == "__main__":
    bullet_list = []
    player={
        1:Player(player1),
        2:Player(player2)
    }
    strmap = rendermap(Map(player,bullet_list).getMap())
    print("已完成地图初始化")
    print(strmap)

    cmd1 = None
    cmd2 = None
    i = 0

    tips= '''
指令 W,A,S,D 控制角色移动，指令B释放弹幕

'''
    print(tips)
    while True:

        print(strmap[1]) #玩家1操作时 显示玩家2发射的弹幕
        while True:
            cmd = input("玩家1请输入你的命令:")
            if cmd == "W":
                player[1].up()
            elif cmd == "A":
                player[1].right()
            elif cmd == "S":
                player[1].down()
            elif cmd == "D":
                player[1].left()
            elif cmd == "B":
                bullet_list.append(Bullet(player[1]))
            else:
                print('输入指令无效，请重新输入')
                continue
            break
        print(strmap[0]) #玩家2操作时 显示玩家1发射的弹幕
        while True:
            cmd2 = input("玩家2请输入你的命令:")
            if cmd2 == "W":
                player[2].up()
            elif cmd2 == "A":
                player[2].right()
            elif cmd2 == "S":
                player[2].down()
            elif cmd2 == "D":
                player[2].left()
            elif cmd2 == "B":
                bullet_list.append(Bullet(player[2]))
            else:
                print('输入指令无效，请重新输入')
                continue
            break

        bullet_move(bullet_list,player) 
        strmap = rendermap(Map(player,bullet_list).getMap())
        i += 1
        print("第{}回合".format(i))



'''
游戏流程
玩家1 行动{
    移动，发射弹幕
}
玩家2 行动{
    移动，发射弹幕
}


   
'''


