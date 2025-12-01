import os
import re
from datetime import datetime
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Font

base_dir = "/tmp/d2c_task_output/"

# ---------- 工具函数 ----------
def is_valid_folder(name):
    return not name.isdigit() and any(c.isalpha() for c in name)

def find_log_file(fpath, fname):
    preferred = os.path.join(fpath, f"{fname}.log")
    if os.path.isfile(preferred):
        return preferred
    for f in os.listdir(fpath):
        if f.endswith(".log"):
            return os.path.join(fpath, f)
    return None

def calc_duration(log_path):
    with open(log_path, "r", encoding="utf-8") as fh:
        lines = [L for L in fh if L.strip()]
    if len(lines) < 2:
        return 0
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})"
    first, last = re.search(pattern, lines[0]), re.search(pattern, lines[-1])
    if not (first and last):
        return 0
    fmt = "%Y-%m-%d %H:%M:%S,%f"
    t1 = datetime.strptime(first.group(1), fmt)
    t2 = datetime.strptime(last.group(1), fmt)
    return (t2 - t1).total_seconds()

def format_duration(sec):
    sec = int(sec)
    if sec < 60:
        return f"{sec}秒"
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}小时{m}分{s}秒" if h else f"{m}分{s}秒"

def find_images(fpath):
    img_dir = os.path.join(fpath, "app/src/test/snapshots/images/")
    if not os.path.exists(img_dir):
        return None, None
    a = b = None
    for f in os.listdir(img_dir):
        if f.startswith("com.example.myapplication"):
            a = os.path.join(img_dir, f)
        elif f.startswith("figma_screenshot"):
            b = os.path.join(img_dir, f)
        if a and b:
            break
    return a, b


image_width = 160
image_height = image_width * 2.2
# ---------- 主函数 ----------
def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Snapshots"

    folders = sorted(
        [f for f in os.listdir(base_dir)
         if os.path.isdir(os.path.join(base_dir, f)) and is_valid_folder(f)],
        key=str.lower
    )
    total = 0
    for f in folders:
        log = find_log_file(os.path.join(base_dir, f), f)
        total += calc_duration(log) if log else 0
    avg = total / len(folders) if folders else 0

    ws.append(["Folder Name", "D2C Image", "Figma Screenshot",
               f"Duration (avg {format_duration(avg)})", "Log File"])
    for col, w in enumerate([30, 30, 30, 20, 60], 1):
        ws.column_dimensions[chr(64 + col)].width = w

    row = 2
    for folder in folders:
        fpath = os.path.join(base_dir, folder)
        log_file = find_log_file(fpath, folder)
        dur = calc_duration(log_file) if log_file else 0
        img1, img2 = find_images(fpath)
        if img1 and img2:
            ws.cell(row=row, column=1, value=folder)
            for col, ip in enumerate([img1, img2], 2):
                img = XLImage(ip)
                img.width, img.height = image_width, image_height
                ws.add_image(img, f"{chr(64 + col)}{row}")
            ws.cell(row=row, column=4, value=format_duration(dur))
            if log_file:
                cell = ws.cell(row=row, column=5, value=os.path.basename(log_file))
                cell.hyperlink = log_file
                cell.font = Font(color="0000FF", underline="single")
            else:
                ws.cell(row=row, column=5, value="N/A")
            ws.row_dimensions[row].height = 280
            row += 1

    out_xlsx = f"d2c_{datetime.now().strftime('%Y%m%d-%H')}_report.xlsx"
    wb.save(out_xlsx)
    print(f"✅ 报告已保存为 {out_xlsx}，平均时间：{format_duration(avg)}")

if __name__ == "__main__":
    main()
