from enum import IntEnum

URLS1="""
https://www.figma.com/design/2G4texS7ZHyza7LXewwr6k/Complex_Homepage?node-id=0-1&p=f&t=Zw43Q54TdiPKD9aq-0
https://www.figma.com/design/ZPdXR2vN5xUpsCn1zpVVyM/Complex_Exchange?node-id=1-95&t=RYaZ117V4qnop5rn-0
https://www.figma.com/design/NDhYpgHZiCs8euNGEt4s7m/D2C-figma-demo?node-id=1-465&t=6c12q9vIPu42nUqq-0
https://www.figma.com/design/dsFPmq1EPsxVdv0MXnwgzf/Complex_Apperance?node-id=1-160&t=oux2bk0emfNiY1RH-0
https://www.figma.com/design/627KPjRbo6Jnifwyzp08cl/Complex_HP?node-id=0-1&p=f&t=U3Jnap1Y6rbXH4OA-0
https://www.figma.com/design/IkwTz62d4UNgRiYZmjocLU/Complex_Notification?node-id=1-116&t=GJGearGENwGYaWlc-0
https://www.figma.com/design/InaLeJPia0Iu9meuO4NKdK/Mediun_Album?node-id=0-1&p=f&t=gwV6MMFIfea00RgD-0
https://www.figma.com/design/9FYcJ44Kr3AEBGDXhcIIaF/Mediun_Chat1?node-id=1-167&t=SQdccGIpl5vWnVtJ-0
https://www.figma.com/design/9FYcJ44Kr3AEBGDXhcIIaF/Mediun_Chat1?node-id=1-2&t=SQdccGIpl5vWnVtJ-0
https://www.figma.com/design/0LhWBitl0cZNsMJb2kfqiE/Mediun_Comment?node-id=0-1&p=f&t=f9z8SE1jKdHLrhX3-0
https://www.figma.com/design/vhzHK1fqWw1g4ZJjORAJs3/Mediun_Delivery?node-id=0-1&p=f&t=DQIErDBeEkjl06ll-0
https://www.figma.com/design/XQ2C4SWYFIJdIrr6wTgiWV/Mediun_DoctorHome?node-id=0-1&p=f&t=PyhpOwXJ75X9lr9t-0
https://www.figma.com/design/Ap70zqm4dXmo8u9u8tfCGR/Mediun_Filter?node-id=1-106&t=kqkC2HhfhBXhnglV-0
https://www.figma.com/design/kEFOpBA9EsOL7NJIcdHJDB/Mediun_Homepage?node-id=1-102&t=Rp5mWWzDgjhIdHym-0
https://www.figma.com/design/CP80TPBxJhPIYZe7wrVKu6/Medium_Order?node-id=0-8&t=LHSOloa7sns7WpBf-0
https://www.figma.com/design/4VPgbnqRBmEgAyFrz75nNZ/Mediun_Schedule?node-id=0-1&p=f&t=MDCzFXi2duxjOoeX-0
https://www.figma.com/design/LOFMYHVnT9GxGzLlZKA2gd/Mediun_Setting?node-id=0-1&p=f&t=kUxypaSShE7q9N8v-0
https://www.figma.com/design/Ow4utpAm3ddSJGwckw4iRJ/Complex_Instagram?node-id=2-1536&t=5w7tuukKvVgORcPJ-0
https://www.figma.com/design/Ow4utpAm3ddSJGwckw4iRJ/Complex_Instagram?node-id=2-1517&t=5w7tuukKvVgORcPJ-0
https://www.figma.com/design/478XmVzfFPKRObw4cdSy5X/Simple_AddCard?node-id=4-160&t=oBZXLMp0GbKuHEO4-0
https://www.figma.com/design/478XmVzfFPKRObw4cdSy5X/Simple_AddCard?node-id=4-192&t=oBZXLMp0GbKuHEO4-0
https://www.figma.com/design/478XmVzfFPKRObw4cdSy5X/Simple_AddCard?node-id=1-104&t=oBZXLMp0GbKuHEO4-0
https://www.figma.com/design/4Sm9aXkTvWfJNUmbdFZkbT/Simple_Chat1?node-id=0-1&p=f&t=dRnhZ5rzGDbsvMYC-0
https://www.figma.com/design/MSOgbPRtOVHx93gnXY8sSs/Simple_Chat2?node-id=0-1&p=f&t=FkLjzr8tDSWk6C1m-0
https://www.figma.com/design/RICuRI2XnLG4SHmLFAKTKl/Simple_Food2?node-id=0-1&p=f&t=sVFI5nzC4RiVwgPx-0
https://www.figma.com/design/cGBdSZDe25qIgEYLQJmv9L/Simple_Food1?node-id=0-1&p=f&t=PLgZ4EmauHQi5QUK-0
https://www.figma.com/design/OHgbyRpbe88pLXAdYlOud8/Simple_Login1?node-id=2-173&t=SwJusOm4ojzz9anm-0
https://www.figma.com/design/lSkkwzFhKvnm9bei6OI4Qn/Simple_Login2?node-id=0-1&p=f&t=7d7RiWD6mMDeTvDx-0
https://www.figma.com/design/0cLfTR7SOMPucq5IZJ0PQ1/Simple_Notification?node-id=0-1&p=f&t=QT21HG65pztKiJWe-0
https://www.figma.com/design/29KUiCbxonpXUNONFHndIz/Simple_Payment?node-id=0-1&p=f&t=03u2DBQHnnKyoa19-0
https://www.figma.com/design/A3J2NZ987MkeFdehHOL3lF/Simple_Profile?node-id=0-20&t=rSgby724fY84Bavy-0
https://www.figma.com/design/qj4XMB3bXhQfLG6QjmvN1W/Simple_Sharing?node-id=0-1&p=f&t=3RJXv5UUmHAXuGGh-0
https://www.figma.com/design/zw8e35BtXmY5jOznBJeWYD/Simple_Shop_1?node-id=1-75&t=VFppg3zRDPo5E6vG-0
https://www.figma.com/design/zw8e35BtXmY5jOznBJeWYD/Simple_Shop_1?node-id=1-214&t=VFppg3zRDPo5E6vG-0
https://www.figma.com/design/tWC3cYnPvWh68HDhVNJRNh/Simple_Singup?node-id=1-209&t=KVhYlhL2Vxq3PfAg-0
""".strip().splitlines()
TOKEN1="##figd_NOvj1PfYuUFr2L-##S_gEZuXf7H519MjWk3uAQjmWO##".replace("##", "")


URLS2="""
https://www.figma.com/design/T5UGp5w1e4Re7Y1ePsLoqB/D2C-Benchmark?node-id=69-2157&t=OxJmcfPw7ZZZmavD-4
https://www.figma.com/design/T5UGp5w1e4Re7Y1ePsLoqB/D2C-Benchmark?node-id=69-1623&t=OxJmcfPw7ZZZmavD-4
https://www.figma.com/design/T5UGp5w1e4Re7Y1ePsLoqB/D2C-Benchmark?node-id=1-166&t=kMsYMoAYmqy1S6Cm-4
https://www.figma.com/design/T5UGp5w1e4Re7Y1ePsLoqB/D2C-Benchmark?node-id=1-1428&t=kMsYMoAYmqy1S6Cm-4
https://www.figma.com/design/T5UGp5w1e4Re7Y1ePsLoqB/D2C-Benchmark?node-id=1-2351&t=kMsYMoAYmqy1S6Cm-4
https://www.figma.com/design/T5UGp5w1e4Re7Y1ePsLoqB/D2C-Benchmark?node-id=1-8346&t=kMsYMoAYmqy1S6Cm-4
https://www.figma.com/design/T5UGp5w1e4Re7Y1ePsLoqB/D2C-Benchmark?node-id=1-9171&t=kMsYMoAYmqy1S6Cm-4
https://www.figma.com/design/T5UGp5w1e4Re7Y1ePsLoqB/D2C-Benchmark?node-id=2-3727&t=kMsYMoAYmqy1S6Cm-4
""".strip().splitlines()
TOKEN2="##figd_jJl4EiVnFY9iP_##KStuxg2UoprJeMYnA44YH-uMJy##".replace("##", "")


class TaskStatus(IntEnum):
    Creating=0
    CreateFail=1
    Running=2
    Successed=3
    Stop=4       #user stop
    AdminStop=5  #admin stop
    Failed=6     #execute failed
    Unkonw=7  #query task not exist, query task not belong to query user