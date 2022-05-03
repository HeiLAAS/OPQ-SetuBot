import re
from typing import Union

from botoy import FriendMsg, GroupMsg, S
from botoy import async_decorators as deco

from .model import GetSetuConfig
from .setu import Setu

__doc__ = "色图姬"

setuPattern = "来(.*?)[点丶、个份张幅](.*?)的?([rR]18)?[色瑟涩䔼😍🐍][图圖🤮]"
digitalConversionDict = {
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}


async def check_and_processing(
    ctx: Union[GroupMsg, FriendMsg]
) -> Union[GetSetuConfig, None]:

    send = S.bind(ctx)
    info = getattr(ctx, "_match")
    config = GetSetuConfig()
    if info[1] != "":
        if info[1] in digitalConversionDict.keys():
            config.toGetNum = int(digitalConversionDict[info[1]])
        else:
            if info[1].isdigit():
                config.toGetNum = int(info[1])
            else:
                await send.atext("能不能用阿拉伯数字?")
                # logger.info('非数字')
                return None
    else:  # 未指定数量,默认1
        config.toGetNum = 1
    config.tags = [i for i in set(re.split(r"[,， ]", info[2])) if i != ""]
    if info[3]:  # r18关键字
        config.level = 1
    return config


@deco.ignore_botself
@deco.on_regexp(setuPattern)
async def main(ctx):
    if config := await check_and_processing(ctx):
        await Setu(ctx, config).main()


async def receive_group_msg(ctx):
    await main(ctx)


async def receive_friend_msg(ctx):
    await main(ctx)
