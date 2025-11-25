#!/usr/bin/env python3
import os
import re
from datetime import datetime
from pathlib import Path

LOG_DIR = Path('/tmp/d2c_task_output')
TIME_RE = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})')

def duration_minutes(file_path: Path):
    """返回单个 log 的耗时（分钟），无法解析返回 None"""
    times = TIME_RE.findall(file_path.read_text(encoding='utf8', errors='ignore'))
    if len(times) < 2:
        return None
    t1 = datetime.strptime(times[0],  '%Y-%m-%d %H:%M:%S,%f')
    t2 = datetime.strptime(times[-1], '%Y-%m-%d %H:%M:%S,%f')
    return (t2 - t1).total_seconds() / 60

def main():
    for logfile in sorted(LOG_DIR.glob('*.log')):
        mins = duration_minutes(logfile)
        print(f'{logfile.name:<25}  {mins:.2f} min' if mins else f'{logfile.name:<25}  -- invalid')

if __name__ == '__main__':
    main()
