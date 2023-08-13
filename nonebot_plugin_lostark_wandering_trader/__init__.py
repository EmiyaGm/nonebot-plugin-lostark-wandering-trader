from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot import on_keyword, require, get_bot, get_bots, get_driver
from httpx import Response, AsyncClient
import datetime
import time
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="命运方舟流浪商人卡牌刷新提示",
    description="国服命运方舟流浪商人稀有史诗传说卡牌刷新提示",
    usage="nb plugin install nonebot_plugin_lostark_wandering_trader",
    type="application",
    homepage="https://github.com/EmiyaGm/nonebot-plugin-lostark-wandering-trader",
    config=Config,
    extra={},
    supported_adapters={"~onebot.v11"},
)

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

try:
    plugin_config = Config.parse_obj(get_driver().config).trader.dict()
except:
    plugin_config = {
        'user_ids': [],
        'group_ids': [],
        'time': 1,
        'server_id': 6,
        'rarity': [],
        'send_type': []
    }
    
notice_data = []

@scheduler.scheduled_job("cron", minute=f"*/{plugin_config.get('time')}", id="check_trader")
async def check_trader():
    global notice_data
    bots = get_bots().values()
    if len(notice_data) == 0:
        for bot in bots:
            notice_data.append([])
    for index,bot in enumerate(bots):
        now = datetime.datetime.now()

        hour = now.hour

        date = datetime.datetime.now().date().isoformat()
        
        show_time_array = [datetime.datetime.strptime( date + ' ' + '04:00:00', '%Y-%m-%d %H:%M:%S'), datetime.datetime.strptime( date + ' ' + '10:00:00', '%Y-%m-%d %H:%M:%S'), datetime.datetime.strptime( date + ' ' + '16:00:00', '%Y-%m-%d %H:%M:%S'), datetime.datetime.strptime( date + ' ' + '22:00:00', '%Y-%m-%d %H:%M:%S'),]
        # time_start = datetime.datetime.strptime( date + ' ' + hour + ':30:00', '%Y-%m-%d %H:%M:%S')
        # time_one = datetime.datetime.strptime( date + ' ' + hour + ':35:00', '%Y-%m-%d %H:%M:%S')
        # time_two = datetime.datetime.strptime( date + ' ' + hour + ':55:00', '%Y-%m-%d %H:%M:%S')
        
        if hour >= 4 and hour <= 9:
            display_at = show_time_array[0]
        
        if hour >= 10 and hour <= 15:
            display_at = show_time_array[1]
            
        if hour >= 16 and hour <= 21:
            display_at = show_time_array[2]
        
        if hour >= 22 or hour <= 3:
            display_at = show_time_array[3]

        response = ''
        
        result = await get_detail(int(display_at.timestamp()))
        if len(result) != 0:
            for item in result:
                can_notice = True
                for notice in notice_data[index]:
                    nid = notice.get('locationId', '')
                    id = item.get('locationId', '')
                    if nid == id:
                        can_notice = False
                if can_notice:
                    card = item.get('_card', {})
                    rapport = item.get('_rapport', {})
                    rarity_array = []
                    send_type_array = []
                    if len(plugin_config.get('send_type')) == 0:
                        send_type_array = ['Card', 'Rapport']
                    else:
                        send_type_array = plugin_config.get('send_type')
                    if len(plugin_config.get('rarity')) == 0:
                        rarity_array = ['Epic', 'Legendary', 'Rare']
                    else:
                        rarity_array = plugin_config.get('rarity')
                    location = item.get('_location', {})
                    image = location.get('snapshot', '')
                    lname = location.get('name', '')
                    member = item.get('_member', {})
                    username = member.get('username', '未知人士')
                    if card is None:
                        confirm = False
                    else:
                        rarity = card.get('rarity', '')
                        confirm = False
                        for rItem in rarity_array:
                            if rItem == rarity and "Card" in send_type_array:
                                confirm = True
                        if confirm:
                            cname = card.get('name', '')
                            response = lname + f' 出{cname}了！' + f'稀有度为{rarity}' + f' 提报人: {username}'
                            try:
                                for qq in plugin_config.get('user_ids'):
                                    await bot.call_api('send_private_msg', **{
                                        'user_id': qq,
                                        'message': response
                                    })
                            except:
                                pass
                            try:
                                for group in plugin_config.get('group_ids'):
                                    await bot.call_api('send_group_msg', **{
                                        'group_id': group,
                                        'message': response
                                    })
                            except:
                                pass
                            time.sleep(1)
                    rapport_confirm = False
                    if rapport is None:
                        rapport_confirm = False
                    else:
                        if rapport.get('rarity') == 'Legendary' and "Rapport" in send_type_array:
                            rapport_confirm = True
                        if rapport_confirm:
                            rname = rapport.get('name', '')
                            response = lname + f' 出{rname}了！' + '稀有度为传说' + f' 提报人: {username}'
                            try:
                                for qq in plugin_config.get('user_ids'):
                                    await bot.call_api('send_private_msg', **{
                                        'user_id': qq,
                                        'message': response
                                    })
                            except:
                                pass
                            try:
                                for group in plugin_config.get('group_ids'):
                                    await bot.call_api('send_group_msg', **{
                                        'group_id': group,
                                        'message': response
                                    })
                            except:
                                pass
                            time.sleep(1)
                    if confirm or rapport_confirm:
                        try:
                            for qq in plugin_config.get('user_ids'):
                                await bot.call_api('send_private_msg', **{
                                    'user_id': qq,
                                    'message': MessageSegment.image(f"https://www.emrpg.com/{image}")
                                })
                        except:
                            pass
                        try:
                            for group in plugin_config.get('group_ids'):
                                await bot.call_api('send_group_msg', **{
                                    'group_id': group,
                                    'message': MessageSegment.image(f"https://www.emrpg.com/{image}")
                                })
                        except:
                            pass
                        time.sleep(1)
            notice_data[index] = result
        else:
            notice_data[index] = []
            

trader = on_keyword({"下一个商人"}, priority=1)

async def get_detail(displayAt):
     async with AsyncClient() as client:
        headers = {
        'X-Ajax': '1',
        'Cookie': 'acw_tc=707c9fc716906220300653664e550e283e11113d450a6e9e21bb7af38e99ab; UBtd_671d_saltkey=l3nfa1If; UBtd_671d_lastvisit=1690618430; UBtd_671d_sid=w61IJF; UBtd_671d_lastact=1690623811%09plugin.php%09; UBtd_671d_sid=O3zbk8; UBtd_671d_lastact=1690799529%09plugin.php%09',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'www.emrpg.com',
        'Connection': 'keep-alive'
        }
        result = []
        try:
            res = await client.get(f"https://www.emrpg.com/plugin.php?displayAt={displayAt}&fromServer=lostarkcn&serverId={plugin_config.get('server_id')}&uri=merchants/active&_pipes=withCard,withRapport,withLocation,withMember&id=tj_emrpg", headers=headers)
            result = res.json().get('data' , [])
        except:
            result = []
        return result

async def get_data():
    async with AsyncClient() as client:
        headers = {
        'X-Ajax': '1',
        'Cookie': 'acw_tc=707c9fc716906220300653664e550e283e11113d450a6e9e21bb7af38e99ab; UBtd_671d_saltkey=l3nfa1If; UBtd_671d_lastvisit=1690618430; UBtd_671d_sid=Z6bM50; UBtd_671d_sendmail=1; UBtd_671d_lastact=1690622038%09plugin.php%09; UBtd_671d_saltkey=AMcqaqQh; UBtd_671d_lastvisit=1690616006; UBtd_671d_sid=PeEjTE; UBtd_671d_lastact=1690622255%09plugin.php%09; acw_tc=76b20f6b16906221102315601e4147a5e05cf53f9b496a18f9a8670e71ca6d',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'www.emrpg.com',
        'Connection': 'keep-alive'
        }
        result = []
        try:
            res = await client.get(f"https://www.emrpg.com/plugin.php?fromServer=lostarkcn&serverId={plugin_config.get('server_id')}&uri=merchants/list&id=tj_emrpg", headers=headers)
            result = res.json().get('data' , [])
        except:
            result = []
        return result


@trader.handle()
async def _(matcher: Matcher, event: MessageEvent):
    now = datetime.datetime.now()
    hour = str(now.hour)
    date = datetime.datetime.now().date().isoformat()
    time_start = datetime.datetime.strptime( date + ' ' + hour + ':30:00', '%Y-%m-%d %H:%M:%S')
    time_two = datetime.datetime.strptime( date + ' ' + hour + ':55:00', '%Y-%m-%d %H:%M:%S')
    if now < time_two and now > time_start:
        response = '商人正在出现'
    else:
        result = await get_data()
        if len(result) != 0:
            response = ''
            for index,item in enumerate(result):
                now = datetime.datetime.now()
                # now_str = now.strftime('%H:%M:%S')
                times = item.get('times', [])
                for time in times:
                    date = datetime.datetime.now().date().isoformat()
                    time_obj = datetime.datetime.strptime( date + ' ' + time, '%Y-%m-%d %H:%M:%S')
                    if now.__lt__(time_obj):
                        response = response + item.get('region', '未知地区') + '的' + item.get('name', '未知商人') + '，即将在 ' + time_obj.strftime('%H:%M:%S')  + ' 时出现' + '\n'
                        break
                # if index != len(result) - 1:
                #     response = response + item.get('region', '未知地区') + '的' + item.get('name', '未知商人') + '\n'
                # else:
                #     response = response + item.get('region', '未知地区') + '的' + item.get('name', '未知商人')
            response = response + 'by: EmiyaGm'
        else:
            response = '暂无数据'
    await trader.finish(response)
