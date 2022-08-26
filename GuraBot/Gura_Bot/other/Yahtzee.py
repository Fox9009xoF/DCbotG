import discord
from discord.ext import commands
from ImportOther.importO import Cog_extention
import json
import random

with open('C:\\Users\\10121\\Desktop\\DiscordBot\\GuraBot\\Gura_Bot\\setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

players = [] #所有玩家
p = 0 #輪到的玩家編號
is_start = False
dice = [0, 0, 0, 0, 0]
reserve = []
roll_chance = 3
scores = [] #所有玩家分數

class Yahtzee(Cog_extention):
    
    @commands.command()
    async def join(self, ctx):
        global players, is_start

        if is_start == False:
            name = ctx.message.author.display_name
            
            if name in players:
                await ctx.send("不可重複加入")
            else:
                players.append(name)
                await ctx.send(f"{name} 已加入遊戲, 目前玩家人數: {len(players)}")
                await ctx.send("若玩家都已加入遊戲, 使用`!start`開始遊戲")
            
        else:
            await ctx.send("遊戲已經開始, 無法中途加入")
    
    @commands.command()
    async def leave(self, ctx):
        global players, is_start

        if is_start == False:
            name = ctx.message.author.display_name

            if name not in players:
                await ctx.send("尚未加入遊戲")
            else:
                for i in range(0, len(players)):
                    if players[i] == name:
                        await ctx.send(f"{name} 已退出遊戲")
                        del players[i]
                        break
        else:
            await ctx.send("遊戲已經開始, 無法退出遊戲(別想逃啊~)")
    
    @commands.command()
    async def start(self, ctx):
        global players, is_start, scores, p

        name = ctx.message.author.display_name

        if name in players:
            if len(players) != 0:
                if is_start == False:
                    is_start = True
                    await ctx.send(f"遊戲開始, {players[p]} 的回合")
                    scores = [["\_\_\_"]*12 for _ in range(len(players))]
                    
                    for i in range(len(players)):
                        scores[i].append(0)

                    print(scores)
                else:
                    await ctx.send("遊戲已經開始")
            else:
                await ctx.send("玩家人數不足")
        else:
            await ctx.send("加入遊戲才能宣布開始")
    
    @commands.command()
    async def roll(self, ctx):
        global roll_chance, is_start, players, p, dice, reserve
        if is_start == True:

            if ctx.message.author.display_name == players[p]:

                if roll_chance != 0:
                    for i in range(len(dice)):
                        dice[i] = random.randint(1, 6)
                    dice.sort()
                    await ctx.send(f"擲出 {dice}")

                    if len(reserve) != 0:
                        await ctx.send(f"目前已保留 {reserve}")
                    
                    if roll_chance != 1:
                        await ctx.send("請使用`!reserve`指定要留下的骰子")
                    else:
                        pass

                    roll_chance -= 1
                    await ctx.send(f"還有{roll_chance}次擲骰機會")

                    if roll_chance <= 0:
                        await ctx.send("請使用`!count`指令選填分數")

                else:
                    await ctx.send("你沒有機會了，使用`!count`指令選填分數")
            else:
                await ctx.send(f"現在是 {players[p]} 的回合")
        else:
            await ctx.send("遊戲還沒開始, 使用`!start`開始遊戲")
    
    @commands.command()
    async def reserve(self, ctx, msg):
        global is_start, dice

        if is_start == True:
            if ctx.message.author.display_name == players[p]:
                if 0 not in dice:
                    queue = msg.split('/')

                    for i in range(len(queue)):
                        for j in range(len(dice)):

                            if int(queue[i]) == int(dice[j]):
                                reserve.append(int(queue[i]))
                                reserve.sort()
                                queue[i] = 0
                                dice[j] = 0
                    
                    for i in range(reserve.count(0)):
                        reserve.remove(0)

                    await ctx.send(f"已保留 {reserve}")
                    queue = []
                    for i in range(dice.count(0)):
                        dice.remove(0)
                else:
                    await ctx.send("還沒擲骰子無法保存")
            else:
                await ctx.send(f"現在是 {players[p]} 的回合")
        else:
            await ctx.send("遊戲還沒開始, 使用`!start`開始遊戲")
    
    @commands.command()
    async def desert(self, ctx, msg):
        global reserve, is_start, dice

        if is_start == True:
            if ctx.message.author.display_name == players[p]:
                queue = msg.split('/')
                a = []

                if len(reserve) != 0:
                    for i in range(len(queue)):
                        for j in range(len(reserve)):

                            if int(queue[i]) == int(reserve[j]):
                                a.append(int(queue[i]))
                                dice.append(int(queue[i]))
                                queue[i] = 0
                                reserve[j] = 0

                    for i in range(reserve.count(0)):
                        reserve.remove(0)
                    
                    a.sort()
                    await ctx.send(f"已捨棄 {a}, 已保留 {reserve}")
                    queue = []
                    a = []

                else:
                    await ctx.send("沒有已保存的骰子")
            else:
                await ctx.send(f"現在是 {players[p]} 的回合")
        else:
            await ctx.send("遊戲還沒開始, 使用`!start`開始遊戲")
    
    @commands.command()
    async def count(self, ctx, msg):
        global is_start, players, p, dice, reserve, scores, roll_chance
        
        reserve.extend(dice)
        reserve.sort()

        if is_start == True:
            test = 0

            if ctx.message.author.display_name == players[p]:
            
                if msg == "Ones" or msg == "ones":
                    if scores[p][0] == "\_\_\_":
                        c = reserve.count(1)
                        scores[p][0] = int(1*c)
                        await ctx.send(f"Ones {scores[p][0]}分")
                    else:
                        await ctx.send("你已經填過 Ones 了")

                elif msg == "Twos" or msg == "twos":
                    if scores[p][1] == "\_\_\_":
                        c = reserve.count(2)
                        scores[p][1] = int(2*c)
                        await ctx.send(f"Twos {scores[p][1]}分")
                    else:
                        await ctx.send("你已經填過 Twos 了")

                elif msg == "Threes" or msg == "threes":
                    if scores[p][2] == "\_\_\_":
                        c = reserve.count(3)
                        scores[p][2] = int(3*c)
                        await ctx.send(f"Threes {scores[p][2]}分")
                    else:
                        await ctx.send("你已經填過 Threes 了")
                
                elif msg == "Fours" or msg == "fours":
                    if scores[p][3] == "\_\_\_":
                        c = reserve.count(4)
                        scores[p][3] = int(4*c)
                        await ctx.send(f"Fours {scores[p][3]}分")
                    else:
                        await ctx.send("你已經填過 Fours 了")
                
                elif msg == "Fives" or msg == "fives":
                    if scores[p][4] == "\_\_\_":
                        c = reserve.count(5)
                        scores[p][4] = int(5*c)
                        await ctx.send(f"Fives {scores[p][4]}分")
                    else:
                        await ctx.send("你已經填過 Fives 了")
                
                elif msg == "Sixes" or msg == "sixes":
                    if scores[p][5] == "\_\_\_":
                        c = reserve.count(6)
                        scores[p][5] = int(6*c)
                        await ctx.send(f"Sixes {scores[p][5]}分")
                    else:
                        await ctx.send("你已經填過 Sixes 了")
                
                elif msg == "Choice" or msg == "choice":
                    if scores[p][6] == "\_\_\_":
                        scores[p][6] = int(sum(reserve))
                        await ctx.send(f"Choice {scores[p][6]}分")
                    else:
                        await ctx.send("你已經填過 Choice 了")
                
                elif msg == "Fourdice" or msg == "fourdice":
                    if scores[p][7] == "\_\_\_":
                        if reserve[0] == reserve[3] or reserve[1] == reserve[4]:
                            scores[p][7] = int(sum(reserve))
                        else:
                            scores[p][7] = 0
                        
                        await ctx.send(f"Fourdice {scores[p][7]}分")
                    else:
                        await ctx.send("你已經填過 Fourdice 了")
                
                elif msg == "Fullhouse" or msg == "fullhouse":
                    
                    if scores[p][8] == "\_\_\_":
                        if reserve[0] == reserve[1] and reserve[2] == reserve[4]:
                            scores[p][8] = int(sum(reserve))
                        elif reserve[0] == reserve[2] and reserve[3] == reserve[4]:
                            scores[p][8] = int(sum(reserve))
                        else:
                            scores[p][8] = 0
                        
                        await ctx.send(f"Fullhouse {scores[p][8]}分")
                    else:
                        await ctx.send("你已經填過 Fullhouse 了")
                
                elif msg == "S" or msg == "s" or msg == "S. Straight":
                    
                    if scores[p][9] == "\_\_\_":
                        if 1 in reserve and 2 in reserve and 3 in reserve and 4 in reserve:
                            scores[p][9] = 15
                        elif 2 in reserve and 3 in reserve and 4 in reserve and 5 in reserve:
                            scores[p][9] = 15
                        elif 3 in reserve and 4 in reserve and 5 in reserve and 6 in reserve:
                            scores[p][9] = 15
                        else:
                            scores[p][9] = 0
                        
                        await ctx.send(f"S. Straight {scores[p][9]}分")
                    else:
                        await ctx.send("你已經填過 S. Straight 了")
                
                elif msg == "B" or msg == "b" or msg == "B. Straight":
                    
                    if scores[p][10] == "\_\_\_":
                        if 1 in reserve and 2 in reserve and 3 in reserve and 4 in reserve and 5 in reserve:
                            scores[p][10] = 25
                        elif 2 in reserve and 3 in reserve and 4 in reserve and 5 in reserve and 6 in reserve:
                            scores[p][10] = 25
                        else:
                            scores[p][10] = 0
                        
                        await ctx.send(f"B. Straight {scores[p][10]}分")
                    else:
                        await ctx.send("你已經填過 B. Straight 了")    
                
                elif msg == "Yahtzee" or msg == "yahtzee":
                    
                    if scores[p][11] == "\_\_\_":
                        if reserve[0] == reserve[4]:
                            scores[p][11] = 50
                            await ctx.send("YAHTZEE!")
                        else:
                            scores[p][11] = 0
                        
                        await ctx.send(f"YAHTZEE {scores[p][11]}分")
                    else:
                        await ctx.send("還想填 Yahtzee 呀")
                
                else:
                    await ctx.send("沒有這個分數項目, 請重新輸入")
                    test += 1

                sums = 0
                
                if scores[p][12] == 0:
                    for j in range(0, 6):
                        if type(scores[p][j]) == int:
                            sums += scores[p][j]
                    if sums >= 65:
                        await ctx.send(f"恭喜 {players[p]} Bonus +35分")
                        scores[p][12] = 35
                
                if test == 0:
                    p += 1
                    if p == len(players):
                        p = 0
                    
                    if scores[-1].count("\_\_\_") != 0:
                        await ctx.send(f"換 {players[p]} 擲骰")
                        roll_chance = 3
                        dice = [0, 0, 0, 0, 0]
                        reserve = []
                    else:
                        await ctx.send(f"遊戲結束，使用`!result`查看結果")
            else:
                await ctx.send(f"現在是 {players[p]} 的回合")
        else:
            await ctx.send("遊戲還沒開始, 使用`!start`開始遊戲")

    @commands.command()
    async def score(self, ctx, name):

        if is_start == True:

            if name in players:
                num = players.index(name)
                sums = 0

                await ctx.send(f"{players[num]} 的分數版:\nOnes: {scores[num][0]}分\nTwos: {scores[num][1]}分\nThrees: {scores[num][2]}分\nFours: {scores[num][3]}分\nFives: {scores[num][4]}分\nSixes: {scores[num][5]}分\nBonus: {scores[num][12]}分\nChoice: {scores[num][6]}分\nFourdice: {scores[num][7]}分\nFullhouse: {scores[num][8]}分\nS. Straight: {scores[num][9]}分\nB. Straight: {scores[num][10]}分\nYahtzee: {scores[num][11]}分")
                
                for i in scores[num]:
                    if i != "\_\_\_":
                        sums += i
                
                await ctx.send(f"總分: {sums}分")

            else:
                await ctx.send("這個人沒有參加遊戲")

        else:
            await ctx.send("遊戲還沒開始, 使用`!start`開始遊戲")
    
    @commands.command()
    async def result(self, ctx):
        global scores, players, is_start, dice, reserve, roll_chance

        rl = [] #勝利者

        if is_start == True:
            if "\_\_\_" not in scores:
                
                await ctx.send("遊戲結束，統計結果")

                for i in range(len(players)):
                    scores[i] = sum(scores[i])
                
                for m in range(len(scores)):
                    await ctx.send(f"{players[m]}: {scores[m]}分")
                    
                if scores.count(max(scores)) == 1:
                    nums = scores.index(max(scores))
                    await ctx.send(f"{players[nums]} 的勝利!({scores[nums]}分)")

                else:
                    for k in range(len(scores)):
                        if scores[k] == max(scores):
                            rl.append(k)
                    
                    for l in range(len(rl)):
                        rl[l] = players[rl[l]]
                    
                    await ctx.send(f"{rl} 的勝利!({max(scores)})")
                
                players = []
                p = 0 
                is_start = False
                dice = [0, 0, 0, 0, 0]
                reserve = []
                roll_chance = 3
                scores = []
                await ctx.send("遊戲已重置")
            
            else:
                await ctx.send(f"遊戲還沒結束，現在是 {players[p]} 的回合")

        else:
            await ctx.send("遊戲還沒開始, 使用`!start`開始遊戲")
    
    @commands.command()
    async def plist(self, ctx):
        await ctx.send(f"目前玩家: {players}")

    @commands.command()
    async def reset(self, ctx):
        global scores, players, is_start, dice, reserve, roll_chance, p

        if is_start == True:
            players = []
            p = 0 
            is_start = False
            dice = [0, 0, 0, 0, 0]
            reserve = []
            roll_chance = 3
            scores = []
            await ctx.send("遊戲已重置")
        else:
            await ctx.send("遊戲還沒開始, 無法重置")

def setup(bot):
    bot.add_cog(Yahtzee(bot))

