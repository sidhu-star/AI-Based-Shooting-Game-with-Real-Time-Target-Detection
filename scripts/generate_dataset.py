from pathlib import Path
import random
import cv2
import numpy as np

ROOT = Path('dataset')
W, H = 640, 480
TRAIN, VAL = 240, 60

def make_image(index, split):
    image = np.zeros((H, W, 3), dtype=np.uint8)
    image[:] = tuple(random.randint(20, 55) for _ in range(3))
    cx = random.randint(70, W - 70)
    cy = random.randint(70, H - 70)
    r = random.randint(22, 55)
    cv2.circle(image, (cx, cy), r, (35, 35, 220), -1)
    cv2.circle(image, (cx, cy), max(5, r - 12), (235, 235, 235), -1)
    cv2.circle(image, (cx, cy), max(3, r - 25), (35, 35, 220), -1)
    noise = np.random.randint(0, 25, image.shape, dtype=np.uint8)
    image = cv2.add(image, noise)
    img_dir = ROOT / 'images' / split
    label_dir = ROOT / 'labels' / split
    img_dir.mkdir(parents=True, exist_ok=True)
    label_dir.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(img_dir / f'target_{index:04d}.jpg'), image)
    label_dir.joinpath(f'target_{index:04d}.txt').write_text(
        f'0 {cx/W:.6f} {cy/H:.6f} {2*r/W:.6f} {2*r/H:.6f}\n', encoding='utf-8')

if __name__ == '__main__':
    for i in range(TRAIN): make_image(i, 'train')
    for i in range(VAL): make_image(i, 'val')
    print(f'Generated {TRAIN} training and {VAL} validation images.')
