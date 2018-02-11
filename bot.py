import discord
import requests
import json
from bs4 import BeautifulSoup
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('bot on')

@bot.command()
async def 배그(arg1 = 'null', arg2 = 'null', arg3 = 'null'): # arg1 = Nickname, arg2 = krjp/as/kakao... , arg3 = solo/duo/squad

        pubg_stats = {
            'rating':0, 'matches_cnt':0, 'win_matches_cnt':0,
            'topten_matches_cnt':0, 'kills_sum':0, 'kills_max':0,
            'assists_sum':0, 'headshot_kills_sum':0, 'deaths_sum':0,
            'longest_kill_max':0, 'rank_avg':0, 'damage_dealt_avg':0,
            'time_survived_avg':0
        }
        pubg_rank = {
            'your_rank':0,
            'all_player':0
        }
        pubg_text = {
            'rank':'', 'rating':'', 'win_rating':'',
            'top_ten':'', 'kd':'', 'avgdmg':'',
            'head_rate':''
        }
        pubg_to_text = {
            '솔':'1', '듀':'2', '스':'4', '솔로':'1', '듀오':'2', '스쿼드':'4'
        }
        
        if arg1 == 'null' or arg2 == 'null' or arg3 == 'null':
            await bot.say(u"```'!배그 [서버] [모드] [닉네임]'으로 명령어 사용```")
            return

        if arg1 == '아시아' or arg1 == '아':
            pubg_server = 'as'
        elif arg1 == '한본' or arg1 == '한':
            pubg_server = 'krjp'
        elif arg1 == '카카오' or arg1 == '카':
            pubg_server = 'kakao'
        else:
            await bot.say(u"```올바르지 않은 서버입니다. 서버:아시아/한본/카카오(아/한/카)```")
            return

        queues = ['솔', '듀', '스', '솔로', '듀오', '스쿼드']
        if arg2 in queues:
            pubg_queue = pubg_to_text[arg2]
        else:
            await bot.say(u"```올바르지 않은 모드입니다. 모드:솔로/듀오/스쿼드(솔/듀/스)```")
            return
      
        # argument process
        pubg_id = arg3
        pubg_link = "https://pubg.op.gg/user/{}?server={}".format(pubg_id,pubg_server)      
        soup = BeautifulSoup(requests.get(pubg_link).text,"html.parser")
        pubg_hash = soup.find("div", attrs={"data-user_id": True}) # check attribute


        if pubg_hash:
            pubg_hash = pubg_hash.attrs['data-user_id'] # Get user hash
            pubg_web_data = BeautifulSoup(requests.get("https://pubg.op.gg/api/users/{}/ranked-stats?season=2018-02&server={}&queue_size={}&mode=tpp".format(
                pubg_hash,pubg_server,pubg_queue)).text,"html.parser")
            json_data = json.loads(pubg_web_data.text)

            if not('message' in json_data):
                json_stats = json_data["stats"]
                pubg_rank['your_rank'] = json_data["ranks"]["rating"]
                pubg_rank['all_player'] = json_data["max_ranks"]["rating"]
                
                for i in pubg_stats.keys():
                    pubg_stats[i] = int(json_stats[i])

                pubg_text['rank'] = str(pubg_rank['your_rank']) + '위' + ' (Top ' + str(round(pubg_rank['your_rank']/pubg_rank['all_player']*100, 2)) + '%)'
                pubg_text['rating'] = str(pubg_stats['rating'])
                pubg_text['win_rating'] = str(round(pubg_stats['win_matches_cnt']/pubg_stats['matches_cnt']*100,2)) + '%'
                pubg_text['top_ten'] = str(round(pubg_stats['topten_matches_cnt']/pubg_stats['matches_cnt']*100,2)) + '%'
                if pubg_stats['deaths_sum'] > 0:
                    pubg_text['kd'] = str(round(pubg_stats['kills_sum']/pubg_stats['deaths_sum'],2))
                else:
                    pubg_text['kd'] = 'perfect'
                pubg_text['avgdmg'] = str(pubg_stats['damage_dealt_avg'])
                if pubg_stats['kills_sum'] > 0:
                    pubg_text['head_rate'] = str(round(pubg_stats['headshot_kills_sum']/pubg_stats['kills_sum']*100,2)) + '%'
                else:
                    pubg_text['head_rate'] = '0%'
                embed=discord.Embed(title='￼', color=0x838383)
                if arg2 == '솔' or arg2 == '솔로':
                    embed.set_author(name=(pubg_id.upper() + '#SOLO'))
                elif arg2 == '듀' or arg2 == '듀오':
                    embed.set_author(name=(pubg_id.upper() + '#DUO'))
                else:
                    embed.set_author(name=(pubg_id.upper() + '#SQUAD'))
                embed.add_field(name=u'랭킹', value=pubg_text['rank'], inline=False)
                embed.add_field(name=u'레이팅', value=pubg_text['rating'], inline=True)
                embed.add_field(name=u'승률', value=pubg_text['win_rating'], inline=True)
                embed.add_field(name=u'Top10', value=pubg_text['top_ten'], inline=True)
                embed.add_field(name=u'K/D', value=pubg_text['kd'], inline=True)
                embed.add_field(name=u'평균 딜량', value=pubg_text['avgdmg'], inline=True)
                embed.add_field(name=u'헤드샷', value=pubg_text['head_rate'], inline=True)
                await bot.say(embed=embed)
                print(pubg_link)
            else:
                await bot.say(u'```기록된 전적이 없습니다.```')
        else:
            await bot.say(u'```존재하지 않는 유저입니다.```')

bot.run('Mzk1OTIzNzE3MzYyMDI0NDQ5.DSaTvQ.YYHYSYMOWqiP92Y9sDxg56pujQM')
