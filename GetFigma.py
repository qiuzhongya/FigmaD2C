#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量抓取 Figma 指定节点 JSON + 图片 + 截图
author : github.com/yourname
"""

import os
import re
import sys
import json
import time
import requests
from urllib.parse import unquote
from FigmaUrl import URLS1, TOKEN1, URLS2, TOKEN2

# ---------- 配置 ----------


BASE_HEADERS = {"X-Figma-Token": TOKEN}
API_ROOT     = "https://api.figma.com/v1"
WAIT         = 0.5  # 每次 API 间隔，防止限速
# ---------------------------


# ---------- 工具 ----------
def parse_url(url: str):
    """提取 file_key 与 node_id"""
    # file_key
    m = re.search(r"figma\.com/design/([a-zA-Z0-9]+)", url)
    if not m:
        raise ValueError("无法解析 file_key: " + url)
    file_key = m.group(1)
    # node-id
    m = re.search(r"[?&]node-id=([^&]+)", url)
    node_id = unquote(m.group(1)) if m else "0-1"
    return file_key, node_id

def safe_name(s: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", s)

def mkdir(d):
    os.makedirs(d, exist_ok=True)

def download(url: str, dst: str):
    """通用下载函数"""
    if not url:
        return
    r = requests.get(url, stream=True, headers=BASE_HEADERS)
    r.raise_for_status()
    with open(dst, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    print("  saved ->", dst)

# ---------- 主逻辑 ----------
def handle_one(url: str):
    file_key, node_id = parse_url(url)
    # 取文件名
    name = safe_name(url.split("/")[4])
    folder = f"{name}_{node_id}"
    mkdir(folder)

    # 1. 获取节点 JSON
    json_path = os.path.join(folder, f"{folder}.json")
    if not os.path.exists(json_path):
        print(f"[JSON] {folder}")
        api = f"{API_ROOT}/files/{file_key}/nodes?ids={node_id}"
        r = requests.get(api, headers=BASE_HEADERS)
        if r.status_code != 200:
            print(" ! 获取 JSON 失败", r.status_code, r.text[:200])
            return
        data = r.json()
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        time.sleep(WAIT)
    else:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

    # 2. 下载 JSON 中所有图片（fills / exportSettings 等）
    print(f"[Images] {folder}")
    images = set()
    def walk(obj):
        if isinstance(obj, dict):
            if obj.get("type") == "IMAGE" and "imageHash" in obj:
                images.add(obj["imageHash"])
            if "fills" in obj:
                for f in obj["fills"]:
                    if f.get("type") == "IMAGE" and "imageHash" in f:
                        images.add(f["imageHash"])
            if "exportSettings" in obj:
                for ex in obj["exportSettings"]:
                    if "imageHash" in ex:
                        images.add(ex["imageHash"])
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
    walk(data)

    if images:
        # 批量换 URL
        hash_list = ",".join(images)
        r = requests.get(f"{API_ROOT}/images/{file_key}?ids={hash_list}&format=png",
                         headers=BASE_HEADERS)
        if r.status_code == 200:
            mapping = r.json()["images"]
            for h, u in mapping.items():
                if u:
                    download(u, os.path.join(folder, f"{h}.png"))
                    time.sleep(0.2)
        else:
            print(" ! 批量 images 接口失败", r.text[:200])

    # 3. 截图
    screenshot = os.path.join(folder, "screenshot.png")
    if not os.path.exists(screenshot):
        print(f"[Screenshot] {folder}")
        r = requests.get(f"{API_ROOT}/images/{file_key}?ids={node_id}&format=png&scale=2",
                         headers=BASE_HEADERS)
        if r.status_code == 200:
            url = r.json()["images"].get(node_id)
            if url:
                download(url, screenshot)
        else:
            print(" ! 截图接口失败", r.text[:200])

# ---------- 入口 ----------
if __name__ == "__main__":
    for u in URLS:
        if not u.strip():
            continue
        try:
            handle_one(u.strip())
        except Exception as e:
            print(" ! 处理失败", u, e)
    print("全部完成 ✅")
