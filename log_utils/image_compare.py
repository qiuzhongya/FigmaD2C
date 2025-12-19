#!/usr/bin/env python3
"""
像素级对比前先高斯模糊，输出两种指标：
1. conv-diff : 模糊后相减，差异率
2. SSIM      : 结构相似性（已含卷积窗口）
"""
import cv2, numpy as np, argparse, sys
from skimage.metrics import structural_similarity as ssim

def load(path, size=None):
    im = cv2.imread(path, cv2.IMREAD_COLOR)
    if im is None:
        raise FileNotFoundError(path)
    if size:
        im = cv2.resize(im, size)
    return im

def gaussian(im, k=5, sigma=1.0):
    return cv2.GaussianBlur(im, (k, k), sigma)

def conv_diff(im1, im2, k=5, sigma=1.0, thresh=5):
    """返回差异率 0~1"""
    a = gaussian(im1, k, sigma)
    b = gaussian(im2, k, sigma)
    d = cv2.absdiff(a, b)
    gray = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
    return cv2.countNonZero(mask) / mask.size

def ssim_score(im1, im2):
    """返回 0~1，越大越相似"""
    return ssim(im1, im2, channel_axis=2)

# ---------- 统一入口 ----------
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('design')
    ap.add_argument('actual')
    ap.add_argument('--size', help='WxH, eg 375x812')
    ap.add_argument('--sigma', type=float, default=1.0)
    ap.add_argument('--thresh', type=int, default=5, help='0-255')
    ap.add_argument('--out', default='diff.png', help='差异热图')
    args = ap.parse_args(argv)          # 支持外部传入列表，方便单元测试

    size = tuple(map(int, args.size.split('x'))) if args.size else None
    a = load(args.design, size)
    b = load(args.actual, size)

    ratio = conv_diff(a, b, sigma=args.sigma, thresh=args.thresh)
    score = ssim_score(a, b)

    # 生成热图
    d = cv2.absdiff(gaussian(a), gaussian(b))
    cv2.imwrite(args.out, d)

    print(f'conv-diff={ratio:.3}')
    print(f'SSIM={score:.4f}')

    # CI 友好：非 0 退出码
    if ratio > 0.002 or score < 0.98:
        return ratio, score

if __name__ == '__main__':
    main()        # 真正调用
