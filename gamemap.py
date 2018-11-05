player1 = 100 #定义玩家的号码
player2 = 101

bullet_style = {10:'☆',11:'☯',12:'○',13:'•',14:'♦',55:'※'}
class Map(): 
    #地图需要两份 一份显示玩家1弹幕 一份显示玩家2的弹幕
    def __init__(self,players,bullet_list=None):
        self.gamemap1 = [([0]*5)for i in range(8)]
        self.gamemap2 = [([0]*5)for i in range(8)]
        self.bullets = bullet_list
        self.players = players


    def getMap(self):
        self.gamemap1[self.players[0].y][self.players[0].x] = self.players[0].num
        self.gamemap1[self.players[1].y][self.players[1].x] = self.players[1].num

        self.gamemap2[self.players[0].y][self.players[0].x] = self.players[0].num
        self.gamemap2[self.players[1].y][self.players[1].x] = self.players[1].num
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


    def getrendermap(self):
        self.getMap()
        #传入二维列表地图，生成文本型地图
        gamemap_tuple = (self.gamemap1,self.gamemap2)
        def mainrender(line,i):
            ourprint =""
            ourprint += "\n｜"
            for item in line:
                if item == 0:
                    ourprint += "  ｜"
                elif item == 100:
                    if i == 2:
                        ourprint += "△｜"#玩家1
                    else:
                        ourprint += "▽｜"#玩家1
                elif item == 101:
                    if i == 2:
                        ourprint += "▼｜" #玩家2
                    else:
                        ourprint += "▲｜"#玩家1
                else:
                    ourprint += bullet_style[item] + "｜" #渲染弹幕

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