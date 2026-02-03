#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计 Figma JSON 中每个节点的直接子节点个数
"""
import json
import os
from pathlib import Path
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

def build_dsl_tree(figma_json: dict):
    root_node = deepcopy(figma_json)
    def walk(node):
        coder_tree = {}
        LAYOUT_KEYS = ["id", "name", "type", "componentId", 
                       "absoluteBoundingBox", "layoutMode", "primaryAxisAlignItems", "counterAxisAlignItems", "constraints", 
                       "layoutGrow", "layoutAlign", "paddingTop", "paddingLeft", "paddingRight", "paddingBottom",
                       "layoutSizingVertical", "layoutSizingHorizontal", "clipsContent"]
        coder_tree.update({k: node[k] for k in LAYOUT_KEYS if k in node})
        coder_tree["children"] = []
        children = node.get("children", [])
        for child in children:
            sub_coder_tree = walk(child)
            coder_tree["children"].append(sub_coder_tree)
        return coder_tree
    coder_tree = walk(root_node)
    return coder_tree

def main():
    if not CACHE_DIR.is_dir():
        print(f"目录不存在: {CACHE_DIR}")
        return

    all_records = []
    for json_file in CACHE_DIR.glob("*.json"):
        if json_file.name.endswith(SKIP_SUFFIX):
            continue
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            document = data.get("document", {})
            dsl_tree = build_dsl_tree(document)
            first_dsl_nodes = travel_parent_first(dsl_tree)
            first_figma_nodes = travel_parent_first(document)
            last_dsl_nodes = travel_parent_last(dsl_tree)
            last_figma_nodes = travel_parent_last(document)
            verify_nodes(first_dsl_nodes, first_figma_nodes)
            verify_nodes(last_dsl_nodes, last_figma_nodes)



            # 在 main() 里替换原来的 print
            print(f"[OK] {json_file.name:<40} {len(first_dsl_nodes)}, {len(last_dsl_nodes)}, {len(first_dsl_nodes) == len(last_dsl_nodes)}节点")        
        except Exception as e:
            print(f"[ERR] {json_file.name} 读取/解析失败: {e}")


if __name__ == "__main__":
    main()
