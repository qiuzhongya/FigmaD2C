#!/usr/bin/env python3
# batch_clean_visible.py
import json
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

SRC_DIR = Path('/tmp/d2c_json_cache')
DST_DIR = Path('/tmp/d2c_json_cache_tmp')

def is_outside_parent(child_abb: Dict, parent_abb: Dict) -> bool:
    """
    检查子节点是否完全在父节点边界外部
    """
    if not child_abb or not parent_abb:
        return False
    
    # 提取边界值
    child_left = child_abb.get("x", 0)
    child_top = child_abb.get("y", 0)
    child_right = child_left + child_abb.get("width", 0)
    child_bottom = child_top + child_abb.get("height", 0)
    
    parent_left = parent_abb.get("x", 0)
    parent_top = parent_abb.get("y", 0)
    parent_right = parent_left + parent_abb.get("width", 0)
    parent_bottom = parent_top + parent_abb.get("height", 0)
    
    # 检查是否完全在父节点外部（四种情况）
    if child_left >= parent_right: return True
    if child_right <= parent_left: return True
    if child_top >= parent_bottom: return True
    if child_bottom <= parent_top: return True
    
    return False


def process_node(node: Dict, view_abb: tuple[int], parent_abb: Optional[Dict]) -> Optional[Dict]:
    """
    递归处理节点。
    如果节点需要被删除，返回 None。
    如果节点保留，返回清洗后的新节点字典（包含处理过的 children）。
    """
    node_id = node.get("id")
    abb = node.get("absoluteBoundingBox", {})    
    # 条件 A: 完全在父节点外部
    if parent_abb and abb:
        if is_outside_parent(abb, parent_abb):
            print(f"remove outside parent node: {node_id}, "
                    f"child: ({abb.get('x')}, {abb.get('y')}, {abb.get('width')}x{abb.get('height')}), "
                    f"parent: ({parent_abb.get('x')}, {parent_abb.get('y')}, {parent_abb.get('width')}x{parent_abb.get('height')})")
            return None  # 直接丢弃该节点及其子树
    
    # 条件 B: 不可见
    if node.get('visible') is False:
        print(f"remove invisible node: {node_id}")
        return None
        
    # 条件 C: 透明度极低
    if node.get('opacity') is not None and node.get('opacity') < 0.01:
        print(f"remove opacity node: {node_id}")
        return None
    
    if abb:
        if abb.get("width", 0) == 0 or abb.get("height", 0) == 0:
            print(f"remove size 0 node: {node_id}, width: {abb.get('width')}, height: {abb.get('height')}")
            return None
        
        if not parent_abb:
            if abb.get("y", 0) >= view_abb[3]:
                print(f"remove screen down node: {node_id}")
                return None
            if abb.get("y", 0) + abb.get("height", 0) <= view_abb[2]:
                print(f"remove screen up node: {node_id}")
                return None
            if abb.get("x", 0) >= view_abb[1]:
                print(f"remove screen right node: {node_id}")
                return None

            if abb.get("x", 0) + abb.get("width", 0) <= view_abb[0]:
                print(f"remove screen left node: {node_id}")
                return None
            
    new_node = {k: v for k, v in node.items() if k != 'children'}
    
    # --- 3. 递归处理子节点 ---
    children = node.get("children", [])
    if children:
        new_children = []
        for child in children:
            # 递归调用，传入当前节点的 abb 作为父边界
            processed_child = process_node(child, view_abb, abb)
            if processed_child is not None:
                new_children.append(processed_child)
        new_node['children'] = new_children

    return new_node
 

def pre_process_figma_json(figma_json: Any) -> Any:
    document = figma_json.get("document", {})
    view_abb = document.get("absoluteBoundingBox", {})

    if not view_abb:
        return
    view_x1 = view_abb.get("x", 0)
    view_x2 = view_abb.get("x", 0) + view_abb.get("width", 0)
    view_y1 = view_abb.get("y", 0)
    view_y2= view_abb.get("y", 0) + view_abb.get("height", 0)
    

    cleaned_document = process_node(document, (view_x1, view_x2, view_y1, view_y2), None)
    
    if cleaned_document is None:
        print("Warning: Root document was removed!")
        figma_json["document"] = {}
    else:
        figma_json["document"] = cleaned_document
        
    return figma_json

def main():
    DST_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for src_file in SRC_DIR.iterdir():
        if not src_file.is_file():
            continue
        if src_file.name.find('image_link_cache') > 0:
            continue
        
        dst_file = DST_DIR / src_file.name
        print(f'处理 {src_file.name} ...')
        
        try:
            with src_file.open('r', encoding='utf-8') as f:
                data = json.load(f)
            
            cleaned_data = pre_process_figma_json(data)
            
            with dst_file.open('w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
            count += 1
        except Exception as e:
            print(f"❌ 处理文件 {src_file.name} 时出错: {e}")

    print(f'✅ 全部处理完成，共 {count} 个文件 -> {DST_DIR}')

if __name__ == '__main__':
    main()
