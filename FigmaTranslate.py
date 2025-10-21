#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量抓取 Figma 指定节点 JSON + 图片 + 截图
author : github.com/yourname
"""
import time
import requests
from urllib.parse import unquote
from FigmaUrl import  URLS1, TOKEN1, URLS2, TOKEN2, TaskStatus
import requests
import json
from typing import Optional, Dict, List, Tuple
from datetime import datetime

# ------------------------------
# 全局配置（根据你的服务实际情况修改）
# ------------------------------
BASE_URL = "http://localhost:7654"  # 你的 FastAPI 服务地址（IP+端口）
TIMEOUT = 10                       # 接口请求超时时间（秒）
USER_NAME = "qiuzhongya"


def create_task(figma_url: str, figma_token: str, app_name: str) -> Tuple[bool, Dict]:
    """
    调用 /d2c/task 接口，创建D2C任务
    :param figma_url: Figma 文件的URL（如 https://www.figma.com/file/xxx/xxx）
    :param figma_token: Figma 访问令牌（需有文件读取权限）
    :param app_name: 提交任务的用户名
    :return: (是否成功, 响应数据字典)
    """
    # 1. 接口参数校验（避免无效请求）
    if not figma_url.startswith("https://www.figma.com/"):
        return False, {"error": "Invalid Figma URL! Must start with 'https://www.figma.com/'"}
    if not figma_token.strip():
        return False, {"error": "Figma token cannot be empty!"}
    if not app_name.strip():
        return False, {"error": "User name cannot be empty!"}

    # 2. 构造请求
    url = f"{BASE_URL}/d2c/task"
    headers = {"Content-Type": "application/json"}  # 声明JSON格式请求体
    payload = {
        "figma_url": figma_url,
        "figma_token": figma_token,
        "app_name": app_name
    }

    # 3. 发送请求并处理响应
    try:
        response = requests.post(
            url=url,
            data=json.dumps(payload),  # 将字典转为JSON字符串
            headers=headers,
            timeout=TIMEOUT
        )
        response.raise_for_status()  # 自动捕获4xx/5xx状态码错误
        result = response.json()     # 解析JSON响应
        return True, result

    except requests.exceptions.RequestException as e:
        # 捕获网络异常（超时、连接失败等）或HTTP错误
        error_msg = f"Request failed: {str(e)}"
        if response:  # 若有响应，补充响应内容
            error_msg += f" | Response: {response.text[:200]}"  # 截取前200字符避免过长
        return False, {"error": error_msg}


def query_task(task_id: str) -> Tuple[bool, Dict]:
    """
    调用 /d2c/task 接口，查询单个任务详情
    :param task_id: 任务唯一标识（创建任务时返回的task_id）
    :param app_name: 任务所属用户名（需与创建时一致）
    :return: (是否成功, 响应数据字典)
    """
    # 1. 参数校验
    if not task_id.strip():
        return False, {"error": "Task ID cannot be empty!"}

    # 2. 构造请求（GET请求用params传参）
    url = f"{BASE_URL}/d2c/task"
    params = {
        "task_id": task_id
    }

    # 3. 发送请求并处理响应
    try:
        response = requests.get(
            url=url,
            params=params,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        result = response.json()
        return True, result

    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {str(e)}"
        if response:
            error_msg += f" | Response: {response.text[:200]}"
        return False, {"error": error_msg}


def query_tasks(app_name: str, offset: int = 0, limit: int = 200) -> Tuple[bool, Dict]:
    """
    调用 /d2c/tasks 接口，分页查询用户的所有任务
    :param app_name: 用户名
    :param offset: 起始位置（默认0，从第1个任务开始）
    :param limit: 每页数量（默认10，最大100，需符合服务端限制）
    :return: (是否成功, 响应数据字典)
    """
    # 1. 参数校验（符合服务端Query参数限制：offset≥0，1≤limit≤100）
    if not app_name.strip():
        return False, {"error": "User name cannot be empty!"}
    if offset < 0:
        return False, {"error": "Offset cannot be negative!"}
    if not (1 <= limit <= 2000):
        return False, {"error": "Limit must be between 1 and 2000!"}

    # 2. 构造请求
    url = f"{BASE_URL}/d2c/tasks"
    params = {
        "app_name": app_name,
        "offset": offset,
        "limit": limit
    }

    # 3. 发送请求并处理响应
    try:
        response = requests.get(
            url=url,
            params=params,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        result = response.json()
        # 补充分页信息（方便前端展示）
        result["current_page"] = (offset // limit) + 1 if limit != 0 else 1
        result["total_pages"] = (result.get("total_task_count", 0) + limit - 1) // limit
        return True, result

    except requests.exceptions.RequestException as e:
        error_msg = f"Request failed: {str(e)}"
        if response:
            error_msg += f" | Response: {response.text[:200]}"
        return False, {"error": error_msg}


def filter_tasks(tasks):
    """
    对任务列表进行筛选，保留figma_url相同情况下创建时间较晚的任务
    """
    unique_tasks = {}
    for task in tasks:
        figma_url = task["figma_url"]
        create_time = datetime.fromisoformat(task["create_time"].replace("Z", "+00:00"))
        if task["end_time"]:
            end_time = datetime.fromisoformat(task["end_time"].replace("Z", "+00:00"))
        else:
            end_time = None
        if figma_url not in unique_tasks:
            task["create_time"] =  create_time
            task["end_time"] =  end_time
            unique_tasks[figma_url] = task
        else:
            existing_task = unique_tasks[figma_url]
            existing_create_time = existing_task["create_time"]
            if create_time > existing_create_time:
                unique_tasks[figma_url] = task
    return sorted(list(unique_tasks.values()), key=lambda x: x["create_time"])



def update_sechdule_tasks(figmas, tasks):
    """
    对任务列表进行筛选，保留figma_url相同情况下创建时间较晚的任务
    """
    for task in tasks:
        figma_url = task["figma_url"]
        figma_info = figmas.get(figma_url)
        if figma_info:
            figma_info[1] = task["create_time"]
            if figma_info[0] != task["task_status"] and task["task_status"] == 3:
                query_info = query_task(task["task_id"])
                print(f"query task info {json.dumps(query_info)}")
            figma_info[0] = task["task_status"]
            figma_info[3] = task["end_time"]
    return figmas


def decoder_tasks_info():
    query_list_success, query_list_result = query_tasks(
        app_name=USER_NAME,
        offset=0,
        limit=1000  # 每页查5个任务
    )
    if query_list_success:
        print(f"Query tasks success! Result: {json.dumps(query_list_result, indent=2)}")
        tasks = filter_tasks(query_list_result["tasks"])
        running_task = sum(1 for task in tasks if task["task_status"] == 2)
        return running_task, tasks
    else:
        print(f"Query tasks failed! Error: {query_list_result['error']}")
        return 0, []


def sechdule_task(figma_tasks):
    running_task_cnt, tasks = decoder_tasks_info()
    remain_task_cnt = 0
    figma_tasks = update_sechdule_tasks(figma_tasks, tasks)
    for figma_info in figma_tasks.values():
        if figma_info[0] != 2 and figma_info[0] != 3:
            remain_task_cnt += 1
    sorted_figma_tasks = sorted(figma_tasks.items(), key=lambda item: item[1][1])
    candidate_task_url = None
    for k, v in sorted_figma_tasks:
        if v[0] in [4, 5, 6, 7]:
            candidate_task_url = k
            break
    clamdown = True
    if len(tasks) > 0:
        pre_create_task_time = tasks[-1]["create_time"]
        time_difference = datetime.now() - pre_create_task_time
        if time_difference.total_seconds() / 60 < 2:
             clamdown = False
    print(running_task_cnt, remain_task_cnt, clamdown, candidate_task_url)
    if running_task_cnt < 4 and remain_task_cnt > 0 and clamdown and candidate_task_url:
        create_success, create_result = create_task(candidate_task_url, figma_tasks[candidate_task_url][2], USER_NAME)
        if create_success:
            print(f"Create task success! Result: {json.dumps(create_result, indent=2)}")
    return figma_tasks   


if __name__ == "__main__":
    figma_tasks = {}
    for u in URLS1:
        if not u.strip():
            continue
        try:
            figma_tasks[u.strip()] = [TaskStatus.Unkonw, datetime.now(), TOKEN1, 0, datetime.now()]
            print(u.strip(), figma_tasks[u.strip()])
            time.sleep(0.1)
        except Exception as e:
            pass
    for u in URLS2:
        if not u.strip():
            continue
        try:
            figma_tasks[u.strip()] = [TaskStatus.Unkonw, datetime.now(), TOKEN2, 0, datetime.now()]
            print(u.strip(), figma_tasks[u.strip()])
            time.sleep(0.1)
        except Exception as e:
            pass
    translate_over = False
    while translate_over is False:
        figma_tasks = sechdule_task(figma_tasks)
        time.sleep(30)
        for k, v in figma_tasks.items():
            if v[0] != 3:
                break
        else:
            translate_over = True
    print("start show result:")
    for k, v in figma_tasks.items():
        print(k, v)
