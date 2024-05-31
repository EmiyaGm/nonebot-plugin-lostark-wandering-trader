from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot import on_keyword, require, get_bot, get_bots, get_driver
from httpx import Response, AsyncClient
import datetime
import time
from .config import Config
from display_at import get_display_at

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

card_data = []

rapport_data = []

location_data = []

get_driver = get_driver()

@get_driver.on_startup
async def _():
    global card_data
    global rapport_data
    global location_data
    card_data = await get_cards()
    rapport_data = await get_rapports()
    location_data = await get_locations()

scheduler_time = 1
if plugin_config.get('time', 1) >= 60:
    scheduler_time = 59
else:
    scheduler_time = plugin_config.get('time', 1)

@scheduler.scheduled_job("cron", minute=f"*/{scheduler_time}", id="check_trader")
async def check_trader():
    global notice_data
    global card_data
    global rapport_data
    global location_data
    bots = get_bots().values()
    if len(notice_data) == 0:
        for bot in bots:
            notice_data.append([])
    for index,bot in enumerate(bots):
        
        display_at = get_display_at()
        
        response = ''

        if display_at is None:
            result = []
        else:
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
                    # card = item.get('_card', {})
                    cardIds = item.get('cardId', '').split(",")
                    rapportIds = item.get('rapportId', '').split(",")
                    locationId = item.get('locationId', '')
                    card_array = []
                    rapport_array = []
                    for origin_card in card_data:
                        id = origin_card.get('id', '')
                        if id in cardIds:
                            card_array.append(origin_card)
                    for origin_rapport in rapport_data:
                        id = origin_rapport.get('id', '')
                        if id in rapportIds:
                            rapport_array.append(origin_rapport)
                    # rapport = item.get('_rapport', {})
                    rarity_array = []
                    send_type_array = []
                    if len(plugin_config.get('send_type', [])) == 0:
                        send_type_array = ['Card', 'Rapport']
                    else:
                        send_type_array = plugin_config.get('send_type', [])
                    if len(plugin_config.get('rarity', [])) == 0:
                        rarity_array = ['Epic', 'Legendary', 'Rare']
                    else:
                        rarity_array = plugin_config.get('rarity', [])
                    location = {}
                    for origin_location in location_data:
                        id = origin_location.get('id', '')
                        if id == locationId:
                            location = origin_location
                    image = location.get('snapshot', '')
                    lname = location.get('name', '')
                    member = item.get('_member', {})
                    username = member.get('username', '未知人士')
                    location_confirm = False
                    if len(card_array) == 0:
                        confirm = False
                    else:
                        for card in card_array:
                            rarity = card.get('rarity', '')
                            confirm = False
                            for rItem in rarity_array:
                                if rItem == rarity and "Card" in send_type_array:
                                    confirm = True
                            send_cards = plugin_config.get('cards', [])
                            cname = card.get('name', '')
                            if len(send_cards) != 0:
                                confirm = False
                                if cname in send_cards:
                                    confirm = True
                            if confirm:
                                response = lname + f' 出{cname}了！' + f'稀有度为{rarity}' + f' 提报人: {username}'
                                location_confirm = True
                                try:
                                    for qq in plugin_config.get('user_ids', []):
                                        await bot.call_api('send_private_msg', **{
                                            'user_id': qq,
                                            'message': response
                                        })
                                except:
                                    pass
                                try:
                                    for group in plugin_config.get('group_ids', []):
                                        await bot.call_api('send_group_msg', **{
                                            'group_id': group,
                                            'message': response
                                        })
                                except:
                                    pass
                                time.sleep(1)
                    if len(rapport_array) == 0:
                        rapport_confirm = False
                    else:
                        for rapport in rapport_array:
                            rapport_confirm = False
                            if rapport.get('rarity') == 'Legendary' and "Rapport" in send_type_array:
                                rapport_confirm = True
                            if rapport_confirm:
                                rname = rapport.get('name', '')
                                response = lname + f' 出{rname}了！' + '稀有度为传说' + f' 提报人: {username}'
                                location_confirm = True
                                try:
                                    for qq in plugin_config.get('user_ids', []):
                                        await bot.call_api('send_private_msg', **{
                                            'user_id': qq,
                                            'message': response
                                        })
                                except:
                                    pass
                                try:
                                    for group in plugin_config.get('group_ids', []):
                                        await bot.call_api('send_group_msg', **{
                                            'group_id': group,
                                            'message': response
                                        })
                                except:
                                    pass
                                time.sleep(1)
                    location_image = plugin_config.get('location_image', True)
                    if location_confirm and location_image:
                        try:
                            for qq in plugin_config.get('user_ids', []):
                                await bot.call_api('send_private_msg', **{
                                    'user_id': qq,
                                    'message': MessageSegment.image(f"https://www.emrpg.com/{image}")
                                })
                        except:
                            pass
                        try:
                            for group in plugin_config.get('group_ids', []):
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
            

trader = on_keyword({"商人情况"}, priority=1)

favor = on_keyword({"好感度"}, priority=1)

async def get_locations():
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
            res = await client.get("https://emrpg.com/plugin.php?page=0&perPage=0&fromServer=lostarkcn&uri=merchants/locations&id=tj_emrpg", headers=headers)
            result = res.json().get('data' , {}).get('list', [])
        except:
            result = []
        return result

async def get_rapports():
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
            res = await client.get("https://emrpg.com/plugin.php?page=0&perPage=0&fromServer=lostarkcn&uri=merchants/rapports&id=tj_emrpg", headers=headers)
            result = res.json().get('data' , {}).get('list', [])
        except:
            result = []
        return result

async def get_cards():
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
            res = await client.get("https://emrpg.com/plugin.php?page=0&perPage=0&fromServer=lostarkcn&uri=merchants/cards&id=tj_emrpg", headers=headers)
            result = res.json().get('data' , {}).get('list', [])
        except:
            result = []
        return result

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
            res = await client.get(f"https://www.emrpg.com/plugin.php?displayAt={displayAt}&fromServer=lostarkcn&serverId={plugin_config.get('server_id')}&uri=merchants/active&_pipes=withMember&id=tj_emrpg", headers=headers)
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


async def get_npc_friendship():
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
            res = await client.get(f"https://emrpg.com/plugin.php?uri=games/lostark/gameData/npcFriendship&_pipes=withContinent&id=tj_emrpg", headers=headers)
            result = res.json().get('data' , [])
        except:
            result = []
        return result

async def get_npc_friendship_reward(primaryKey):
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
            res = await client.get(f"https://emrpg.com/plugin.php?uri=games/lostark/gameData/npcFriendship/reward&_pipes=withContinent&id=tj_emrpg&primaryKey={primaryKey}", headers=headers)
            result = res.json().get('data' , {})
        except:
            result = {}
        return result

@trader.handle()
async def _(matcher: Matcher, event: MessageEvent):
    now = datetime.datetime.now()
    hour = str(now.hour)
    date = datetime.datetime.now().date().isoformat()

    
    result = await get_data()
    if len(result) != 0:
        response = ''
        for index,item in enumerate(result):
            now = datetime.datetime.now()
            display_start_at = int(item.get('displayStartAt', 0))
            display_end_at = int(item.get('displayEndAt', 0))
            display_start_at_new = datetime.datetime.fromtimestamp(display_start_at)
            display_end_at_new = datetime.datetime.fromtimestamp(display_end_at)
            response = response + item.get('region', '未知地区') + '的' + item.get('name', '未知商人') + '出现时间为：' + display_start_at_new.__format__( '%Y-%m-%d %H:%M:%S') + ' - ' + display_end_at_new.__format__( '%Y-%m-%d %H:%M:%S') + '\n'
        response = response + 'by: EmiyaGm'
    else:
        response = '商人正在备货中...'
    await trader.finish(response)


@favor.handle()
async def _(matcher: Matcher, event: MessageEvent):
    npc = ""
    if args := event.get_plaintext().split("好感度"):
        npc = args[0].strip() or args[1].strip()
        if not npc:
            await favor.finish("请确定需要查询好感度的NPC名称")
        else:
            result = await get_npc_friendship()
            if len(result) != 0:
                response = ''
                for index,item in enumerate(result):
                    if npc == item.get('NpcName', ''):
                        primaryKey = item.get('PrimaryKey', 0)
                if not primaryKey:
                    response = "暂无NPC数据..."
                else:
                    reward = await get_npc_friendship_reward(primaryKey)
                    if len(reward.get(primaryKey, {}).keys()) != 0:
                        reward_data = reward.get(primaryKey, {})
                        if len(reward_data.get('stuffs', [])) != 0:
                            response = response + reward_data.get('stuffs')[0] + 'x' + str(reward_data.get('ItemAmount1', 0)) + '\n'
                        response = response + 'by: EmiyaGm'
            else:
                response = '暂无NPC数据...'
            await favor.finish(response)
        