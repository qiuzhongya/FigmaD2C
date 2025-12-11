import os
import json
from typing import Any, Dict, Optional, List

# ------------- 缓存工具 -------------
def json_cache_path(file_key: str, node_id: str) -> str:
    """本地缓存文件路径"""
    cache_dir = "/tmp/d2c_json_cache"
    os.makedirs(cache_dir, exist_ok=True)
    # 与 Figma 内部 ID 格式保持一致
    sanitized_node = node_id.replace("-", ":")
    return os.path.join(cache_dir, f"{file_key}_{sanitized_node}.json")


def read_json_cache(file_key: str, node_id: str) -> Optional[Dict[str, Any]]:
    """返回缓存的 dict，失败或不存在返回 None"""
    path = json_cache_path(file_key, node_id)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            print("read json cache")
            return json.load(f)   # 直接反序列化成 dict
    except Exception:
        return None


def write_json_cache(file_key: str, node_id: str, data: Dict[str, Any]) -> None:
    """把 dict 落盘，失败不抛异常"""
    path = json_cache_path(file_key, node_id)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        # 这里可以接日志系统
        pass

'''
def fetch_image_links(file_key: str,
                      node_ids: List[str],
                      token: str) -> Dict[str, str]:
    cached = read_image_json_cache(file_key, node_ids)
    if cached is not None:
        return cached
    url = f"https://api.figma.com/v1/images/{file_key}"
    params = {"ids": ",".join(node_ids), "format": "png", "scale": 3}
    headers = {"X-Figma-Token": token}
    resp = requests.get(url, headers=headers, params=params, timeout=30)

    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", 60))
        tlogger().error(f"Rate limited (429) -> retry_after={retry_after}")
        raise Exception(f"Figma API rate limited (429) -> retry_after={retry_after}")
    if resp.status_code != 200:
        tlogger().info(f"Get image urls failed, code={resp.status_code}, text={resp.text}")
        return {}
    images: Dict[str, str] = resp.json().get("images", {})
    write_image_json_cache(file_key, images)
    return images


def parse_figma_file(node_id: str, figma_token: str, figma_file_key: str):
    cached = read_json_cache(figma_file_key, node_id)
    if cached is not None:
        return cached
    url = f"https://api.figma.com/v1/files/{figma_file_key}/nodes?ids={node_id}"
    headers = {
        "X-FIGMA-TOKEN": figma_token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 60))
        print(f"Rate limited (429) on {url} -> retry_after={retry_after}")
        raise Exception(f"Figma Api rate limited (429) on {url} -> retry_after={retry_after}")
    if not response.ok:
        tlogger().info("parse figma file failed: ", response.text)
        raise Exception("parse figma file to json failed")
    node_data = response.json()['nodes'][node_id.replace("-", ":")]
    write_json_cache(figma_file_key, node_id, node_data)
    return response.json()['nodes'][node_id.replace("-", ":")]
'''


# ------------- 缓存工具 -------------
def image_json_cache_path(file_key: str) -> str:
    return f"/tmp/d2c_json_cache/{file_key}_image_link_cache.json"


def read_image_json_cache(file_key: str,
                          needed_nodes: List[str]) -> Optional[Dict[str, str]]:
    """返回 images 字段 dict；缓存必须包含所有 needed_nodes 才算命中"""
    path = image_json_cache_path(file_key)
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            images: Dict[str, str] = json.load(f).get("images", {})
        if all(n in images for n in needed_nodes):
            print("read image download link cache")
            return images
    except Exception:
        pass
    return None


def write_image_json_cache(file_key: str, new_images: Dict[str, str]) -> None:
    """增量合并并落盘；失败不抛"""
    path = image_json_cache_path(file_key)
    try:
        # 读旧缓存
        old = {}
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                old = json.load(f).get("images", {})
        # 合并
        old.update(new_images)
        # 写回
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"images": old}, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
