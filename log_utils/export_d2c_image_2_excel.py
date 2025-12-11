import os, re, subprocess
from datetime import datetime
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Font, Alignment

base_dir = "/tmp/d2c_task_output/"
COMPARE_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_compare.py")

# ---------- 工具函数（保持不变） ----------
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

# ---------- 新增：一次性扫描 token ----------
def calc_tokens(log_path):
    """
    返回 (input_tokens, output_tokens, total_tokens)
    日志里可能有多条，累加即可
    """
    inp = out = total = 0
    if not log_path or not os.path.isfile(log_path):
        return 0, 0, 0
    with open(log_path, encoding="utf-8") as fh:
        for line in fh:
            # 匹配单引号或双引号
            m_in  = re.search(r"['\"]input_tokens['\"]\s*:\s*(\d+)", line)
            m_out = re.search(r"['\"]output_tokens['\"]\s*:\s*(\d+)", line)
            m_tot = re.search(r"['\"]total_tokens['\"]\s*:\s*(\d+)", line)
            if m_in:  inp  += int(m_in.group(1))
            if m_out: out  += int(m_out.group(1))
            if m_tot: total = max(total, int(m_tot.group(1)))  # 一般只有一行 total
    # 若日志里没给出 total，再自己算
    if total == 0:
        total = inp + out
    return inp, out, total

def format_tokens(inp, out, total):
    return f"input: {inp}\n, out: {out}\n,toatl: {total}\n"


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

# ---------- 新增：调用 compare.py 拿到 ratio & score ----------
import subprocess, os, sys, shlex

COMPARE_PY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_compare.py")

def compare_images(design: str, actual: str):
    """
    返回 (ratio, score) 字符串；失败返回 ('N/A','N/A')
    """
    if not os.path.isfile(design) or not os.path.isfile(actual):
        print(f"[compare] 图片不存在：{design} 或 {actual}")
        return "N/A", "N/A"

    cmd = [sys.executable, COMPARE_PY,
           design, actual, "--size", "375x812"]   # 统一分辨率
    try:
        # 捕获 stdout+stderr，方便调试
        completed = subprocess.run(
            cmd, capture_output=True, text=True, check=True)
        ratio = score = "N/A"
        for line in completed.stdout.splitlines():
            if line.startswith("conv-diff="):
                ratio = line.split("=", 1)[1].strip()
            elif line.startswith("SSIM="):
                score = line.split("=", 1)[1].strip()
        print(f"[compare] ratio={ratio}, score={score}")
        return ratio, score

    except subprocess.CalledProcessError as e:
        # exit 1/2 都会走到这里
        print(f"[compare] 失败！exit={e.returncode}")
        print(f"cmd : {' '.join(shlex.quote(c) for c in cmd)}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return "N/A", "N/A"
    except Exception as e:
        print(f"[compare] 其他异常: {e}")
        return "N/A", "N/A"

image_width = 160
image_height = int(image_width * 2.2)

# ---------- 主函数 ----------
def main():
    wb = Workbook()
    ws = wb.active
    ws.title = datetime.now().strftime('%Y%m%d-%H')

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
    inp_sum = out_sum = tot_sum = 0
    # 1. 表头追加两列
    ws.append(["Folder Name", "D2C Image", "Figma Screenshot",
               f"Duration (avg {format_duration(avg)})", f"token (avg{format_tokens(inp_sum, out_sum, tot_sum)})",
               "Conv-Diff(<0.002)", "SSIM(>0.98)"])

    ws.column_dimensions['E'].alignment = Alignment(wrap_text=True, vertical='top')
    # 2. 列宽 +2
    for col, w in enumerate([30, 30, 30, 20, 20, 15, 15], 1):
        ws.column_dimensions[chr(64 + col)].width = w

    row = 2
    
    for folder in folders:
        fpath = os.path.join(base_dir, folder)
        log_file = find_log_file(fpath, folder)
        dur = calc_duration(log_file) if log_file else 0
        inp, out, tot = calc_tokens(log_file)
        img1, img2 = find_images(fpath)
        inp_sum += inp
        out_sum += out
        tot_sum += tot
        if img1 and img2:
            ws.cell(row=row, column=1, value=folder)
            # 插图
            for col, ip in enumerate([img1, img2], 2):
                img = XLImage(ip)
                img.width, img.height = image_width, image_height
                ws.add_image(img, f"{chr(64 + col)}{row}")
            ws.cell(row=row, column=4, value=format_duration(dur))
            ws.cell(row=row, column=5, value=format_tokens(inp, out, tot))               

            # 3. 新增：ratio & score
            ratio, score = compare_images(img2, img1)   # 参数顺序按需要调
            ws.cell(row=row, column=6, value=ratio)
            ws.cell(row=row, column=7, value=score)

            ws.row_dimensions[row].height = 280
            row += 1
            ws.cell(row=row - 1, column=5).alignment = Alignment(wrap_text=True, vertical='bottom')
            ws.cell(row=row - 1, column=1).alignment = Alignment(wrap_text=True, vertical='bottom')
    header_row = 1
    tok_cell = ws.cell(row=header_row, column=5,
            value=f"Token (avg {format_tokens(inp_sum/(row - 1), out_sum/(row - 1), tot_sum/(row - 1))})")
    tok_cell.alignment = Alignment(wrap_text=True)
    out_xlsx = f"d2c_{datetime.now().strftime('%Y%m%d-%H')}_report.xlsx"
    wb.save(out_xlsx)
    print(f"✅ 报告已保存 为 {out_xlsx}，平均时间：{format_duration(avg)}")

if __name__ == "__main__":
    import sys
    main()
