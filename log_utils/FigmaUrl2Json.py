#!/usr/bin/env python3
import json, pathlib, re, requests, sys

# ========== 可改参数 ==========
TOKEN = "##figd_iVEgBkhonbyLncHXTKctKE-##YCcs66rmh3uN8vHe-##".replace("##", "")   # 你的真实 token
URLS = """https://www.figma.com/design/2G4texS7ZHyza7LXewwr6k/Complex_Homepage?node-id=0-1&p=f&t=Zw43Q54TdiPKD9aq-0
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
https://www.figma.com/design/8DKAG9lieGCgJDVbZ1F4nJ/D2C-test-case?node-id=1-1427&t=j2Vy8TeiYNJdnYCN-4""".strip().split()

OUT_DIR = pathlib.Path("json")
OUT_DIR.mkdir(exist_ok=True)

# 正则提取关键字段
pat = re.compile(r'https://www\.figma\.com/design/([^/]+)/([^/?]+)\?.*node-id=([\d\-]+)')

def file_name(match: re.Match) -> str:
    file_key, title, node = match.groups()
    # 把标题里的空格/特殊符号统一换成下划线
    safe_title = re.sub(r'\W+', '_', title)
    return f"{safe_title}_node-id_{node}.json"

def download(url: str, token: str, save_path: pathlib.Path):
    m = pat.search(url)
    if not m:
        print(f'skip: {url}')
        return
    file_key, _, node_id = m.groups()
    api = f"https://api.figma.com/v1/files/{file_key}/nodes?ids={node_id}"
    headers = {'X-Figma-Token': token}
    resp = requests.get(api, headers=headers, timeout=60)
    resp.raise_for_status()
    save_path.write_text(resp.text, encoding='utf8')
    print(f'saved: {save_path}')

def main():
    for u in URLS:
        try:
            download(u, TOKEN, OUT_DIR / file_name(pat.search(u)))
        except Exception as e:
            print(f'fail: {u}  {e}', file=sys.stderr)

if __name__ == '__main__':
    main()
