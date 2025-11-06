import cv2
import numpy as np
import pyautogui
import time
import argparse

pyautogui.FAILSAFE = True 

def rdp(points, epsilon):
    if len(points) < 3:
        return points
    def perp(a, b, c):
        a = np.array(a); b = np.array(b); c = np.array(c)
        if np.allclose(a, b):
            return np.linalg.norm(c - a)
        return np.abs(np.cross(b - a, a - c)) / np.linalg.norm(b - a)
    stack = [(0, len(points) - 1)]
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    while stack:
        s, e = stack.pop()
        maxd = 0.0; idx = None
        for i in range(s + 1, e):
            d = perp(points[s], points[e], points[i])
            if d > maxd:
                maxd = d; idx = i
        if maxd > epsilon and idx is not None:
            keep[idx] = True
            stack.append((s, idx)); stack.append((idx, e))
    return [points[i] for i, k in enumerate(keep) if k]

def get_paths_from_image(img_path, resize_max=800, canny1=25, canny2=75, simplify_eps=2.5):
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"File {img_path} not found or could not be opened.")
    h0, w0 = img.shape[:2]
    scale = 1.0
    if max(h0, w0) > resize_max:
        scale = resize_max / max(h0, w0)
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(blur, canny1, canny2)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    paths = []
    for cnt in contours:
        pts = [(int(p[0][0]), int(p[0][1])) for p in cnt]
        if len(pts) < 5:
            continue
        simplified = rdp(pts, simplify_eps)
        if len(simplified) >= 2:
            paths.append(simplified)
    paths.sort(key=lambda p: -len(p))
    return paths, (img.shape[1], img.shape[0]), scale

def scale_and_map_paths(paths, src_size, dst_tl, dst_br):
    sw, sh = src_size
    x0, y0 = dst_tl; x1, y1 = dst_br
    dw = x1 - x0; dh = y1 - y0
    src_ratio = sw / sh
    dst_ratio = dw / dh
    if src_ratio > dst_ratio:
        scale = dw / sw
        new_h = sh * scale
        offset_x = x0
        offset_y = y0 + (dh - new_h) / 2
    else:
        scale = dh / sh
        new_w = sw * scale
        offset_x = x0 + (dw - new_w) / 2
        offset_y = y0
    mapped = []
    for path in paths:
        newp = []
        for (px, py) in path:
            mx = offset_x + px * scale
            my = offset_y + py * scale
            newp.append((int(mx), int(my)))
        mapped.append(newp)
    return mapped

def draw_paths(paths, speed=0.002, pause_between_paths=0.25):
    print("Starting to draw. Stop by moving your mouse to the upper left or right corner.")
    time.sleep(1.0)
    for i, path in enumerate(paths):
        if len(path) < 2:
            continue
        x0, y0 = path[0]
        pyautogui.moveTo(x0, y0, duration=0.15)
        pyautogui.mouseDown()
        for (x, y) in path[1:]:
            pyautogui.moveTo(x, y, duration=speed)
        pyautogui.mouseUp()
        time.sleep(pause_between_paths)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', required=True)
    parser.add_argument('--speed', type=float, default=0.003, help='duration of movement between points (seconds)')
    parser.add_argument('--simplify', type=float, default=2.5, help='epsilon for simplicity (larger -> fewer points)')
    parser.add_argument('--calibrate', action='store_true', help='click two corners of the canvas manually')
    args = parser.parse_args()

    print("Processing the image...")
    paths, src_size, scale = get_paths_from_image(args.image, simplify_eps=args.simplify)
    print(f"Found {len(paths)} paths. Image size: {src_size}, input scaling: {scale:.3f}")

    dst_tl = None; dst_br = None
    if args.calibrate or dst_tl is None:
        print("Calibration mode: first click the upper-left corner of the canvas (ENTER to save), then the lower-right corner (ENTER).")
        input("Place your cursor over the upper left corner of the canvas and press Enter...")
        p1 = pyautogui.position()
        print("Saved:", p1)
        input("Place your cursor over the lower right corner of the canvas and press Enter...")
        p2 = pyautogui.position()
        print("Saved:", p2)
        dst_tl = (p1.x, p1.y)
        dst_br = (p2.x, p2.y)

    mapped = scale_and_map_paths(paths, src_size, dst_tl, dst_br)
    print("Your mapping is ready. Prepare your Emulator window and hold your mouse still for a moment.")
    time.sleep(1.0)
    draw_paths(mapped, speed=args.speed)
    print("Completed.")

if __name__ == '__main__':
    main()
