from enum import IntEnum

URLS1="""
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=110094-7248
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=1-1767
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=1-1427
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=1-460
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=102-974
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=102-1625
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-2240
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-6013
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-9206
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-13318
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-17116
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-16582
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-25745
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-26224
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-26118
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-26202
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-26679
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-26962
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-26980
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-27062
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-27349
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-44177
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-44343
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-44474
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-44609
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-44942
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-45307
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-43887
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=104-151746
https://www.figma.com/design/NDhYpgHZiCs8euNGEt4s7m/D2C-figma-demo?node-id=1-465
https://www.figma.com/design/2G4texS7ZHyza7LXewwr6k/Complex_Homepage?node-id=0-1&p=f
https://www.figma.com/design/ZPdXR2vN5xUpsCn1zpVVyM/Complex_Exchange?node-id=1-95
https://www.figma.com/design/dsFPmq1EPsxVdv0MXnwgzf/Complex_Apperance?node-id=1-160
https://www.figma.com/design/627KPjRbo6Jnifwyzp08cl/Complex_HP?node-id=0-1&p=f
https://www.figma.com/design/IkwTz62d4UNgRiYZmjocLU/Complex_Notification?node-id=1-116
https://www.figma.com/design/InaLeJPia0Iu9meuO4NKdK/Mediun_Album?node-id=0-1&p=f
https://www.figma.com/design/9FYcJ44Kr3AEBGDXhcIIaF/Mediun_Chat1?node-id=1-167
https://www.figma.com/design/9FYcJ44Kr3AEBGDXhcIIaF/Mediun_Chat1?node-id=1-2
https://www.figma.com/design/0LhWBitl0cZNsMJb2kfqiE/Mediun_Comment?node-id=0-1&p=f
https://www.figma.com/design/vhzHK1fqWw1g4ZJjORAJs3/Mediun_Delivery?node-id=0-1&p=f
https://www.figma.com/design/XQ2C4SWYFIJdIrr6wTgiWV/Mediun_DoctorHome?node-id=0-1&p=f
https://www.figma.com/design/Ap70zqm4dXmo8u9u8tfCGR/Mediun_Filter?node-id=1-106
https://www.figma.com/design/kEFOpBA9EsOL7NJIcdHJDB/Mediun_Homepage?node-id=1-102
https://www.figma.com/design/CP80TPBxJhPIYZe7wrVKu6/Medium_Order?node-id=0-8
https://www.figma.com/design/4VPgbnqRBmEgAyFrz75nNZ/Mediun_Schedule?node-id=0-1&p=f
https://www.figma.com/design/LOFMYHVnT9GxGzLlZKA2gd/Mediun_Setting?node-id=0-1&p=f
https://www.figma.com/design/Ow4utpAm3ddSJGwckw4iRJ/Complex_Instagram?node-id=2-1536
https://www.figma.com/design/Ow4utpAm3ddSJGwckw4iRJ/Complex_Instagram?node-id=2-1517
https://www.figma.com/design/478XmVzfFPKRObw4cdSy5X/Simple_AddCard?node-id=4-160
https://www.figma.com/design/478XmVzfFPKRObw4cdSy5X/Simple_AddCard?node-id=4-192
https://www.figma.com/design/478XmVzfFPKRObw4cdSy5X/Simple_AddCard?node-id=1-104
https://www.figma.com/design/4Sm9aXkTvWfJNUmbdFZkbT/Simple_Chat1?node-id=0-1&p=f
https://www.figma.com/design/MSOgbPRtOVHx93gnXY8sSs/Simple_Chat2?node-id=0-1&p=f
https://www.figma.com/design/RICuRI2XnLG4SHmLFAKTKl/Simple_Food2?node-id=0-1&p=f
https://www.figma.com/design/cGBdSZDe25qIgEYLQJmv9L/Simple_Food1?node-id=0-1&p=f
https://www.figma.com/design/OHgbyRpbe88pLXAdYlOud8/Simple_Login1?node-id=2-173
https://www.figma.com/design/lSkkwzFhKvnm9bei6OI4Qn/Simple_Login2?node-id=0-1&p=f
https://www.figma.com/design/0cLfTR7SOMPucq5IZJ0PQ1/Simple_Notification?node-id=0-1&p=f
https://www.figma.com/design/29KUiCbxonpXUNONFHndIz/Simple_Payment?node-id=0-1&p=f
https://www.figma.com/design/A3J2NZ987MkeFdehHOL3lF/Simple_Profile?node-id=0-20
https://www.figma.com/design/qj4XMB3bXhQfLG6QjmvN1W/Simple_Sharing?node-id=0-1&p=f
https://www.figma.com/design/zw8e35BtXmY5jOznBJeWYD/Simple_Shop_1?node-id=1-75
https://www.figma.com/design/zw8e35BtXmY5jOznBJeWYD/Simple_Shop_1?node-id=1-214
https://www.figma.com/design/tWC3cYnPvWh68HDhVNJRNh/Simple_Singup?node-id=1-209
""".strip().splitlines()
TOKEN1="##figd_NOvj1PfYuUFr2L-##S_gEZuXf7H519MjWk3uAQjmWO##".replace("##", "")
TOKEN1="##figd_##iVEgBkhonbyLncHXTKctKE##-YCcs66rmh3uN8vHe-##".replace("##", "")

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

class TaskStatus(IntEnum):
    Creating=0
    CreateFail=1
    Running=2
    Successed=3
    Stop=4       #user stop
    AdminStop=5  #admin stop
    Failed=6     #execute failed
    Unkonw=7  #query task not exist, query task not belong to query user
