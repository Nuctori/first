import random
from Bullet import Bullet
class Player():
    def __init__(self,num,qq):

        self.num = num
        self.cmd = []
        self.qq = qq
        self.actpoint = 5
        self.havemove = False

        self.handcard = Card_list(self)

        if self.num == 100:
            self.x = 2
            self.y = 7
            self.text = "△"
            self.move = 1
        elif self.num == 101:
            self.x = 2
            self.y = 0
            self.text = "▼"
            self.move = -1
        else:
            raise TypeError("只支持2名玩家，参数为100，或者为101")

    def roundinit(self):
        self.actpoint = 5
        self.havemove = False
        self.cmd = []


    def up(self):
        if 0 <= self.y <= 7:
            self.y += -self.move

    def down(self):
        if 0 <= self.y <= 7:
            self.y += self.move

    def left(self):
        if 0 <= self.x < 4:
            self.x += 1
            
    def right(self):
        if 0 < self.x <= 4:
            self.x += -1

class Card_list():
    #手牌列表，最大上限9张
    def __init__(self,Player):
        self.Cards = []
        self.player = Player

    def getCard(self):
        if len(self.Cards) >= 9:
            return('手牌已到达最大数量（9张）')
        else:
            self.Cards.append(Draw(self.player))
            return('我的回合！抽卡！')

    def useCard(self,selectNum):
        card = self.Cards[int(selectNum)-1]
        
        itertime = 0
        for bullet in card[0]:
            bullet.active(self.player)
            
            if itertime == 1:
                bullet.ox += 1 
            elif  itertime == 2:
                bullet.ox -= 1 
            
            itertime += 1
        self.Cards.remove(card)
        return(card[0])

    def showCard(self):
        re = ''
        for Card in self.Cards:
            re += str(self.Cards.index(Card)+1) + ":" + Card[1] + '\r\n'
        return(re)

    def cost(self,selectNum):
        if len(self.Cards) >= int(selectNum)-1:
            card = self.Cards[int(selectNum)-1]  
        else: 
            return(0)
        return(card[2])




def Draw(Player):
    #输入玩家对象，随机生成弹幕卡一张，返回（弹幕类，卡牌描述文字，卡牌消耗）
    #要处理抽卡时就决定位置的问题，实例创建时就已经确定位置了
    direction_dict = {0:'右侧',1:'左侧'}
    angle_dict = {
    0:'正前方',1:'正前方',2:'正前方',3:'正前方',4:'正前方',
    12:'小角度',13:'小角度',14:'小角度',24:'中角度',
    36:'大角度', 45:'45度方向',}
    speed_list = [1,1,1,1,2,2,3]
    speed_dict = {1:'慢速弹',2:'中速弹',3:'快速弹'}
    quantity_list = [1,1,1,1,2,2,3]
    Bullet_list = [星弹,阴阳玉,大玉,小玉,菱弹]

    direction = random.choice(list(direction_dict))
    angle = random.choice(list(angle_dict))
    speed = random.choice(speed_list)
    quantity = random.choice(quantity_list)
    Bullet = random.choice(Bullet_list)

    
    card_cost = quantity + speed
    card_fun = Barrage(Bullet,Player,direction,angle,quantity,speed)
    #最后

    card_str = '{direction_str}{angle_str}发射：{quantity}个{Barrage}：{speed_str}【{cost}费】'.format(
    direction_str = direction_dict.get(direction),
    angle_str = angle_dict.get(angle),
    quantity = str(quantity),
    speed_str = speed_dict.get(speed),
    cost = card_cost,
    Barrage = Bullet.__name__
    
    )
    return(card_fun,card_str,card_cost)

def Barrage(Bullet,Player,direction=0,angle=0,quantity=1,speed=1): #能不能通过字典创建符卡呢
    # 输入玩家对象，角度，方向，返回弹幕对象列表
    shoot_list = []
    for i in range(quantity):
        shoot_list.append(Bullet(Player,direction,angle,speed))
    return shoot_list


class 星弹(Bullet):  
    #弹幕类
    def __init__(self,Player,direction,angle,speed):
        super().__init__(Player,direction,angle,speed)
        self.speed = speed
        self.num = 10

class 阴阳玉(Bullet):  
    #弹幕类
    def __init__(self,Player,direction,angle,speed):
        super().__init__(Player,direction,angle,speed)
        self.speed = speed
        self.num = 11

class 大玉(Bullet):  
    def __init__(self,Player,direction,angle,speed):
        super().__init__(Player,direction,angle,speed)
        self.speed = speed
        self.num = 12

class 小玉(Bullet):  
    #弹幕类
    def __init__(self,Player,direction,angle,speed):
        super().__init__(Player,direction,angle,speed)
        self.speed = speed
        self.num = 13

class 菱弹(Bullet):  
    #弹幕类
    def __init__(self,Player,direction,angle,speed):
        super().__init__(Player,direction,angle,speed)
        self.speed = speed
        self.num = 14

