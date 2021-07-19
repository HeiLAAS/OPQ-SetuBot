import re
from botoy import GroupMsg
from botoy.sugar import Text, Picture
from botoy import decorators as deco

__doc__ = """把B站小程序转成链接"""

dont_Send_miniProgram_Base64PIC = r"""
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
RQFFFFAUUUUH/9k=
"""

@deco.these_msgtypes("XmlMsg")
@deco.ignore_botself
def receive_group_msg(ctx: GroupMsg):
    if len(ctx.Content) > 200:
        if info := re.findall(r'(https://b23\.tv/.*?)\?', ctx.Content):
            # S.image(Dont_Send_miniProgram_Base64PIC)
            Text(info[0])
            Picture(pic_base64=dont_Send_miniProgram_Base64PIC)
            # S.text(info[0])
