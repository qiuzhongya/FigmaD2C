from enum import IntEnum
URLS1="""
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=1-460
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=1-1427
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=1-1767
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=102-974
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=102-1625
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-2240
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-6013
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-9206
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-13318
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-16582
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-17116
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-25745
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-25988
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-26118
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-26202
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-26224
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-26679
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-26962
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-26980
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-27062
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-27349
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-43733
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-43887
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-44118
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-44177
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-44343
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-44474
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-44609
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-44942
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-45053
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=104-45307
https://www.figma.com/design/s11IteQZ8jy9pjCjdAumvS/D2C-test-case?node-id=163-8283
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-9332
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-9226
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-9047
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-8989
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-8755
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-7691
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-7510
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-7421
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-7313
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-7223
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-7100
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-7043
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-6968
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-6773
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-6322
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-5822
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-4872
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-3545
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-3439
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-3333
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-3229
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-2910
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-2486
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-2280
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-2182
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-1888
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-1663
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-1466
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-1233
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-896
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-291
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-456
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=3-186
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=5-431
https://www.figma.com/design/daRLLtr7z3Z0zFbuFMUGHj/D2C-public-case?node-id=5-4
""".strip().splitlines()
#TOKEN1="##figd_FEXUWWAYwl4tDoYzDsxFw_##06v6s27kbfbt8nLiyC##".replace("##", "")
TOKEN1="##figd_OsT8uB9c4a3fQT_##pqbegQICCK4E1AFtnm_-X29cU##".replace("##", "")

URLS1 = [
    u.replace("Ushx6eAx3RflMMuStoPWFh", "s11IteQZ8jy9pjCjdAumvS")
    #u.replace("Ushx6eAx3RflMMuStoPWFh", "Ushx6eAx3RflMMuStoPWFh")
    for u in URLS1
]

URLS2="""
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=1-1767
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=1-1427
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=1-460
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=102-974
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=102-1625
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-2240
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-6013
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-9206
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-13318
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-17116
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-16850
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-26224
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-25745
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-26118
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-27062
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-26962
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-45307
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-45307
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-44942
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-44609
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-44474
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-44343
https://www.figma.com/design/wxUj4ZSmsRhSQXZ6p6K7O5/D2C-test-case-Byte?node-id=104-44177
""".strip().splitlines()
TOKEN2="##figd_ft_##nlKs1ZstlmrErpU7yXNI1NSb0o9Ag##-Jp4bVIL##".replace("##", "")


URLS3 = [
    u.replace("wxUj4ZSmsRhSQXZ6p6K7O5", "4mA2iRrJRgfNIFL1l66yVk")
     .replace("D2C-test-case-Byte", "D2C-test-case")
    for u in URLS2
]
#TOKEN_BYTE
TOKEN3="##figd_jJl4EiVnFY9iP_##KStuxg2UoprJeMYnA44YH-uMJy##".replace("##", "")

URLS4 = [
    u.replace("Ushx6eAx3RflMMuStoPWFh", "s11IteQZ8jy9pjCjdAumvS")
    for u in URLS1
]
TOKEN4="##figd_FEXUWWAYwl4tDoYzDsxFw_##06v6s27kbfbt8nLiyC##".replace("##", "")

class TaskStatus(IntEnum):
    Creating=0
    CreateFail=1
    Running=2
    Successed=3
    Stop=4       #user stop
    AdminStop=5  #admin stop
    Failed=6     #execute failed
    Unkonw=7  #query task not exist, query task not belong to query user

BASE_URL_IP = "http://localhost"
BASE_URL_PORT = 7654
