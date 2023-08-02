<!--
 * @Author         : EmiyaGm
 * @Date           : 2023-8-2 10:37:25
 * @Description    : None
 * @GitHub         : https://github.com/emiyagm
-->

<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot-plugin-status

_✨ NoneBot 命运方舟国服流浪商人刷新时间查看 自动播报稀有及其以上卡牌刷新 插件 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/emiyagm/nonebot-plugin-loastark-wandering-trader/main/LICENSE">
    <img src="https://img.shields.io/github/license/emiyagm/nonebot-plugin-loastark-wandering-trader.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-loastark-wandering-trader">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-loastark-wandering-trader.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="python">
</p>

## 使用方式

通用:

- 发送 Command `下一个商人` 获取某个服务器流浪商人刷新时间列表
- 每隔x分钟会自动通报稀有度在蓝色以上的卡片刷新位置

## 配置项

配置方式：直接在 NoneBot 全局配置文件中添加以下配置项即可。

### TRADER__USER_IDS

- 类型：`list`
- 默认值：`[]`
- 说明：需要发送通知的QQ号（需要是好友）

### TRADER__GROUP_IDS

- 类型：`list`
- 默认值：`[]`
- 说明：需要发送通知的群号（需要在群里）

### TRADER__TIME

- 类型: `int`
- 默认: `1`
- 说明: 检测流浪商人位置结果间隔时间

### TRADER__SERVER_ID

- 类型: `int`
- 默认: `14`
- 说明：服务器对应的id（参考如下）：
  - 先锋服务器（亚克拉西亚）: 1
  - 先锋服务器（先锋体验服）: 2
  - 卢佩恩（卢特兰）: 3
  - 卢佩恩（安忆谷）: 4
  - 卢佩恩（妮娜芙）: 5
  - 卢佩恩（卡丹）: 6
  - 卢佩恩（希里安）: 7
  - 卢佩恩（摩可可）: 12
  - 卢佩恩（塞卡）: 13
  - 卢佩恩（艾弗格雷斯）: 14
  - 卢佩恩（纳西尼尔）: 15
  - 卢佩恩（凯萨尔）: 16
  - 卢佩恩（洛恒戴尔）: 17
  - 卢佩恩（库克赛顿）: 19
  - 卡杰洛斯（贝隆）: 23
  - 卡杰洛斯（巴尔坦）: 24
  - 卡杰洛斯（贝拉）: 25
  - 卡杰洛斯（阿尔古斯）: 26
  - 卡杰洛斯（艾达琳）: 27
  - 卡杰洛斯（特里希温）: 28
  - 卡杰洛斯（凯因）: 29
  - 卡杰洛斯（卡隆）: 30
  - 普罗提温（托托克）: 31
  - 普罗提温（阿布莱修德）: 32
  - 普罗提温（艾伦）: 33
  - 普罗提温（阿贾娜）: 34
  - 普罗提温（萨沙）: 35
  - 普罗提温（卡门）: 36
  - 普罗提温（阿黛尔）: 37
  - 普罗提温（霸者之剑）: 38

配置文件示例（默认模板）

```dotenv
TRADER__USER_IDS=[12345678,87654321]
TRADER__GROUP_IDS=[12345678,87654321]
TRADER__TIME=1
TRADER__SERVER_ID=14
```