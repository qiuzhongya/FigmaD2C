#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import os
import re
import json
import shutil
import subprocess
from typing import List, Dict, Any, Optional
from utils.tos_manager import upload_zip_to_tos

# ---------------- 正则 ----------------
LOG_HEAD   = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+ - \[TID:\d+\] - \w+ - ')
FIGMA_RE   = re.compile(r"Received Figma URL:\s*(?P<url>https?://[^\s]+).*?token:\s*(?P<token>\S+)")
COMP_RE    = re.compile(r"Compilation failed with error:")
LLM_RE     = re.compile(
    r'\{\s*["\']?(agent|tools)["\']?\s*:'     # LangChain 结构
    r'|'
    r'\[LLM\s+(?:INPUT|RAW\s+OUTPUT)\]'      # 我们自己的日志标记
)


# ---------------- 工具 ----------------
def split_blocks(text: str) -> List[str]:
    """按日志头切分成独立块"""
    lines = text.splitlines()
    buf, blocks = [], []
    for line in lines:
        if LOG_HEAD.match(line):
            if buf:
                blocks.append('\n'.join(buf))
            buf = [line]
        else:
            buf.append(line)
    if buf:
        blocks.append('\n'.join(buf))
    return blocks


def classify_block(block: str) -> Dict[str, Any]:
    """对单块日志分类"""
    payload = re.sub(LOG_HEAD, '', block).strip()
    if not payload:
        return {"type": "ignore"}

    # 1. Figma
    m = FIGMA_RE.search(payload)
    if m:
        return {"type": "figma", "url": m["url"], "token": m["token"]}

    # 2. 编译错误
    if COMP_RE.search(payload):
        return {"type": "compile_error", "detail": payload}

    # 3. LLM 交互
    if LLM_RE.search(payload):
        return {"type": "llm", "raw_block": payload}

    return {"type": "ignore"}


def handle_task_data(log_path: str, dump_json_path: str, stages: str) -> None:
    """主入口：读日志 -> 分类 -> 写 JSON"""
    text = open(log_path, encoding='utf-8', errors='ignore').read() if os.path.isfile(log_path) else ""
    dump_data = {
        "figma": {},
        "stage": stages,
        "compile_errors": [],
        "llm_blocks": [],
    }

    for block in split_blocks(text):
        rec = classify_block(block)
        t = rec.pop("type")
        if t == "figma":
            dump_data["figma"] = rec
        elif t == "compile_error":
            dump_data["compile_errors"].append(rec)
        elif t == "llm":
            dump_data["llm_blocks"].append(rec)

    os.makedirs(os.path.dirname(dump_json_path), exist_ok=True)
    with open(dump_json_path, 'w', encoding='utf-8') as f:
        json.dump(dump_data, f, ensure_ascii=False, indent=2)


def task_compress_upload(compress_dir: str, task_id: int, stages: str, figma_title: Optional[str] = None):
    workspace_dir = os.path.join(compress_dir, f"{task_id}")
    logfile = os.path.join(compress_dir, f"{task_id}.log")
    jsonfile = os.path.join(compress_dir, f"{task_id}", f"{task_id}.json")
    handle_task_data(logfile, jsonfile, stages)
    if os.path.isfile(logfile):            # 只移动文件
        shutil.copy(logfile, workspace_dir)   
    if figma_title:
        zip_name = f"{figma_title}_{task_id}.zip"
    else:
        zip_name = f"{task_id}.zip"
    try:
        subprocess.run(["zip", "-r", zip_name, f"{task_id}"], cwd=compress_dir, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise e
    output_zip_file_path = os.path.join(compress_dir, zip_name)
    upload_zip_to_tos(output_zip_file_path)


def main():
    base_dir      = "/tmp/d2c_task_output_master"
    task_id       = 1766504612015
    stages_str    = "2025-12-23 23:43:32 export_figma_json "

    log_path      = f"{base_dir}/{task_id}.log"
    dump_json_path= f"{base_dir}/D2C_test_case_1766504612015/{task_id}.json"

    handle_task_data(log_path, dump_json_path, stages_str)
    print(f"parse done -> {dump_json_path}")

if __name__ == '__main__':
    main()
