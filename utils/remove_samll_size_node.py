#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计 Figma JSON 中每个节点的直接子节点个数
"""
import json
import os
from pathlib import Path
import traceback
from typing import List, Dict
from copy import deepcopy
CACHE_DIR = Path("/tmp/d2c_json_cache")
REPORT_FILE = CACHE_DIR / "figma_child_count_report.json"

# 需要跳过的文件后缀
SKIP_SUFFIX = "_image_link_cache.json"

def verify_nodes(nodes1, nodes2):
    if len(nodes1) != len(nodes2):
        print(f"{len(nodes1)} length different for {len(nodes2)}")
        return False
    for i in range(len(nodes1)):
        if nodes1[i] != nodes2[i]:
            print(f"node {i} different for {nodes1[i]}, {nodes2[i]}")
            return False
    return True

def travel_parent_first(figma_json: dict):
    root_node = deepcopy(figma_json)
    nodes = []
    def walk(node):
        node_id = node.get("id", None)
        if node_id:
            nodes.append(node_id)
        else:
            return
        children = node.get("children", [])
        for child in children:
            walk(child)
        return
    walk(root_node)
    return nodes

def travel_parent_last(figma_json: dict):
    root_node = deepcopy(figma_json)
    nodes = []
    def walk(node):
        node_id = node.get("id", None)
        if node_id:
            children = node.get("children", [])
            for child in children:
                walk(child)
            nodes.append(node_id)
        else:
            return
        return
    walk(root_node)
    return nodes

def remove_samll_size_tree(figma_json: dict):
    LAYOUT_KEYS = {
        "id", "name", "type", "componentId",
        "absoluteBoundingBox", "layoutMode", "primaryAxisAlignItems",
        "counterAxisAlignItems", "constraints", "layoutGrow", "layoutAlign",
        "paddingTop", "paddingLeft", "paddingRight", "paddingBottom",
        "layoutSizingVertical", "layoutSizingHorizontal", "clipsContent"
    }

    root_node = deepcopy(figma_json)
    abb = root_node.get("absoluteBoundingBox") or {}    # 同样防一手
    view_size = int(abb.get("width", 0)) * int(abb.get("height", 0))
    split_size = view_size // 10

    def walk(node: dict) -> dict:
        node_abb = node.get("absoluteBoundingBox") or {}  # 关键防御
        node_size = int(node_abb.get("width", 0)) * int(node_abb.get("height", 0))

        slim = {k: node[k] for k in LAYOUT_KEYS if k in node}
        if "children" in node:
            slim["children"] = [walk(child) for child in node["children"]]

        if node_size < split_size:
            return slim

        full = {**node, **slim}
        full["children"] = slim.get("children", [])
        return full

    return walk(root_node)

def main():
    if not CACHE_DIR.is_dir():
        print(f"目录不存在: {CACHE_DIR}")
        return

    for json_file in CACHE_DIR.glob("*.json"):
        if json_file.name.endswith(SKIP_SUFFIX):
            continue
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            document = data.get("document", {})
            light_json = remove_samll_size_tree(document)
            first_light_nodes = travel_parent_first(light_json)
            first_figma_nodes = travel_parent_first(document)
            last_light_nodes = travel_parent_last(light_json)
            last_figma_nodes = travel_parent_last(document)
            verify_nodes(first_light_nodes, first_figma_nodes)
            verify_nodes(last_light_nodes, last_figma_nodes)
            print(f"[OK] {json_file.name:<40} {len(first_light_nodes)}, {len(last_light_nodes)}, {len(first_light_nodes) == len(last_light_nodes)}节点")
        except Exception:
            # 关键改动：用 traceback 打印完整堆栈
            print(f"[ERR] {json_file.name} 读取/解析失败:")
            traceback.print_exc()


if __name__ == "__main__":
    main()
