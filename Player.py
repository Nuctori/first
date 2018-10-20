import random
from Bullet import Bullet
class Player():
    def __init__(self,num):

        self.num = num
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
            print('手牌已到达最大数量（9张）')
        else:
            self.Cards.append(Draw(self.player))

    def useCard(self,selectNum):
        card = self.Cards[int(selectNum)-1]
        self.Cards.remove(card)
        return(card[0])

    def showCard(self):
        for Card in self.Cards:
            print(self.Cards.index(Card)+1,":",Card[1])

    def cost(self,selectNum):
        card = self.Cards[int(selectNum)-1]
        return(card[2])




def Draw(Player):
    #输入玩家对象，随机生成弹幕卡一张，返回（弹幕类，卡牌描述文字，卡牌消耗）
    direction_dict = {0:'右侧',1:'左侧'}
    angle_dict = {
    0:'正前方',1:'正前方',2:'正前方',3:'正前方',4:'正前方',
    12:'小角度',13:'小角度',14:'小角度',24:'中角度',
    36:'大角度', 45:'45度方向',}
    speed_list = [0,0,0,0,1,1,2]
    speed_dict = {0:'慢速弹',1:'中速弹',2:'快速弹'}

    direction = random.choice(list(direction_dict))
    angle = random.choice(list(angle_dict))
    speed = random.choice(speed_list)
    speed = 1
    
    card_cost = 2 + speed
    card_fun = 两个小玉(Player,direction,angle)
    card_str = '{direction_str}{angle_str}发射：小玉：{speed_str}【{cost}费】'.format(
    direction_str = direction_dict.get(direction),
    angle_str = angle_dict.get(angle),
    speed_str = speed_dict.get(speed),
    cost = card_cost 
    
    )
    return(card_fun,card_str,card_cost)


def 两个小玉(Player,direction=0,angle=0): #能不能通过字典创建符卡呢
    # 输入玩家对象，角度，方向，返回弹幕对象列表
    shoot1 = 小玉(Player,direction,angle) 
    shoot2 = 小玉(Player,direction,angle)
    shoot2.x += 1
    shoot2.ox += 1
    shoot_list = [shoot1,shoot2]
    return shoot_list

class 小玉(Bullet):  
    #弹幕类
    def __init__(self,Player,direction,angle):
        super().__init__(Player,direction,angle)
        self.speed = 1
        self.num = 10
