#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1. 强制覆盖：/tmp/d2c_json_cache/  ->  /Users/bytedance/code/d2c_json_cache/
2. 增量补回：/Users/bytedance/code/d2c_json_cache/  ->  /tmp/d2c_json_cache/
"""
import shutil
from pathlib import Path

TMP  = Path("/tmp/d2c_json_cache")
BACK = Path("/Users/bytedance/code/d2c_json_cache")

def force_copy(src: Path, dst: Path):
    """无条件覆盖"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

def missing_copy(src: Path, dst: Path):
    """只复制缺失文件"""
    if dst.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

def prepare_json_cache():
    TMP.mkdir(parents=True, exist_ok=True)
    BACK.mkdir(parents=True, exist_ok=True)

    # 1. 强制覆盖
    print("=== 强制覆盖：TMP -> BACK")
    for f in TMP.rglob("*"):
        if f.is_file():
            force_copy(f, BACK / f.relative_to(TMP))
    print("=== 强制覆盖 完成")

    # 2. 增量补回
    print("=== 增量补回：BACK -> TMP")
    for f in BACK.rglob("*"):
        if f.is_file():
            missing_copy(f, TMP / f.relative_to(BACK))
    print("=== 增量补回 完成")
