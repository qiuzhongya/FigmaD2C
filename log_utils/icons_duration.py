#!/usr/bin/env python3
import datetime, pathlib, re, sys

LOG_DIR = pathlib.Path('/tmp/d2c_task_output')
START   = '--- EXPORTING FIGMA ICONS ---'
END     = 'Finished running: export_figma_icons'
TIME_RE = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})')

def duration(p: pathlib.Path):
    t1 = t2 = None
    for line in p.read_text(encoding='utf8', errors='ignore').splitlines():
        if START in line:
            t1 = datetime.datetime.strptime(TIME_RE.search(line).group(1), '%Y-%m-%d %H:%M:%S,%f')
        if END in line and t1:
            t2 = datetime.datetime.strptime(TIME_RE.search(line).group(1), '%Y-%m-%d %H:%M:%S,%f')
            break
    return (t2 - t1).total_seconds() / 60 if t1 and t2 else None

for log in sorted(LOG_DIR.glob('*.log')):
    mins = duration(log)
    print(f'{log.name:<30} {mins:.2f} min' if mins else f'{log.name:<30} -- invalid')
