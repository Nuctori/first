import random
from Player import Player
from Bullet import Bullet
from gamemap import Map


player1 = 100 
player2 = 101
    



    
def bullet_move(bullet_list,player): 
    #输入弹幕列表，让弹幕列表中子弹移动一步，输出弹幕列表中弹幕进行一次移动后的结果
    for bullet in bullet_list:
        for i in range(bullet.speed):
            bul = bullet.__next__() #？？
            if bul == None:
                bullet_list.remove(bullet)  

            elif  bul[0] == player[1].x and bul[1] == player[1].y: #弹幕碰撞到玩家1检测
                if bullet.player == player1:
                    return("biu！玩家2疮了！")
                    
            elif  bul[0] == player[0].x and bul[1] == player[0].y: #弹幕碰撞到玩家2检测
                if bullet.player == player2:
                    return("biu！玩家1疮了！")
                    


def time_end(players,game):
    i = 0  
    #一股C味
    #结束双方回合，进行回合运算，输入命令和玩家字典，给玩家对象和命令对象迭代
    for player in players:
        move = {"W":player.up, "A":player.right, "S":player.down,"D":player.left}
        for cmditem in player.cmd:
            if cmditem.isdigit():
                game.bullet_list.extend(player.handcard.useCard(cmditem)) 
            elif isinstance(cmditem,str):
                move[cmditem]()
        i += 1

    result = bullet_move(game.bullet_list,players)
    if result is not None:
        return(result)
    game.strmap = Map(players,game.bullet_list).getrendermap()
    return(game.strmap)

class Game():
    #封装关于游戏的主要数据（弹幕 玩家 地图 回合数）
    def __init__(self,player):
        self.bullet_list = []
        self.player = player
        self.strmap = Map(player,self.bullet_list).getrendermap()
        self.gameround = 0

    def getmap(self,Player):
        #输入玩家对象，取出字符串地图
        i = 0
        for player in self.player:
            if Player == player:
                if i == 1:
                    return(self.strmap[0],self.strmap[1]) 
                else:
                    return(self.strmap[1],self.strmap[0]) 
            i += 1

    #完善player类 封装，不使用公共数组
    def sendorder(self,Player,cmd):
        # 给 player对象 过滤并且 发送指令，输入玩家对象，指令，返回提示文本
        allow_input = {
        " ","W","A","S","D","E","C",
        "1","2","3","4","5","6","7","8","9"}
        if cmd in allow_input:
            if cmd == " ":
                if Player.actpoint < 1:
                    return("行动点不足")
                else:
                    Player.actpoint -= 1 
                    Player.handcard.getCard()
                    return(Player.handcard.showCard())
            elif cmd == "C":
                return(Player.handcard.showCard())
            elif "WASD".find(cmd) != -1:
                move = {'W':'上','A':'左','S':'下','D':'右'}
                if Player.actpoint < 1:
                    return("行动点不足,剩余行动点{}".format(Player.actpoint))
                elif Player.havemove:
                    return("本回合你已经移动过了")
                else:
                    Player.actpoint -= 1
                    Player.havemove = True
                    Player.cmd.append(cmd)
                    return("你向{}移动了一步".format(move[cmd]))
            elif "123456789".find(cmd) != -1:

                cost = Player.handcard.cost(cmd)
                if cost == 0:
                    return('没有选定手牌')
                elif cmd in Player.cmd:
                    return('您已使用这张手牌')
                elif Player.actpoint >= cost:
                    Player.actpoint -= Player.handcard.cost(cmd)
                    Player.cmd.append(cmd)
                    return('已使用手牌')
                else:
                    return('行动点不足')
            else:
                pass
        else:
            return('输入指令无效，请重新输入')
        

def handle_sock(sock,addr,Player,Game):
    #监听玩家客户端发送过来的指令，进行操作 输入：套接字，端口，玩家对象，游戏对象。循环进行游戏
    import time
    while True:
        cmd = sock.recv(1024)
        cmd = cmd.decode('utf-8')
        cmd = cmd.upper()
        wait = False
        if cmd != 'E':
            
            msg = Game.sendorder(Player,cmd)
            msg += '\r\n当前你还拥有{}点行动点\r\n'.format(Player.actpoint)
            msg += '<input>'
            sock.send(msg.encode('utf-8'))

        else:    
            msg = '请等待...'
            sock.send(msg.encode('utf-8'))
            allgame[Game] += 1
            while allgame[Game] != 2:
                wait = True
                time.sleep(1)
            if wait:
                allgame[Game] = 0

            else:
                Game.gameround += 1
                result = time_end(players=players,game=Game)
                if isinstance(result,str):
                    msg = result
                    sock.send(msg.encode('utf-8'))
                    sock.close()
                    break

                
            Player.roundinit()
            strmap = Game.getmap(Player)
            msg = strmap[0]+'\r\n\r\n'
            msg += strmap[1]
            msg += '\r\n当前你还拥有{}点行动点\r\n'.format(Player.actpoint)
            msg += '<input>'
            sock.send(msg.encode('utf-8'))

'''
抽卡器
只抽出类 不抽出实例，使用时候再创建实例
'''

allgame = {}
if __name__ == "__main__":

    import socket
    import sys
    import threading

    serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 4148
    serversocket.bind((host,port))
    serversocket.listen(20)
    players = []
    room = {}
    clientsocket_list = []
    newgame = None


    while True:
        clientsocket,addr = serversocket.accept()
        print(str(addr))



        if clientsocket not in clientsocket_list:
            clientsocket_list.append(clientsocket)

        if not players:
            players.append(Player(player1,addr))
            msg = '已进入游戏，请等待另一位玩家。\r\n'
            clientsocket.send(msg.encode('utf-8'))
        elif not newgame:
            players.append(Player(player2,addr))
            newgame = Game(players)
            i=0

            for client in clientsocket_list:
                allgame[newgame] = 0
                client_thread = threading.Thread(target=handle_sock,args=(client,addr,players[i],newgame))
                client_thread.start()

                msg = '玩家已经到齐，游戏开始\r\n'
                strmap = newgame.getmap(players[i])
                msg += strmap[0]+'\r\n\r\n'
                msg += strmap[1]
                msg += '\r\n当前你还拥有{}点行动点\r\n'.format(players[i].actpoint)
                msg += '<input>'
                client.send(msg.encode('utf-8'))
                i += 1
                msg= ""  

