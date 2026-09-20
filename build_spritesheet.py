from PIL import Image, ImageOps
from collections import deque

FRAME_W = 192
FRAME_H = 208
COLS = 8
ROWS = 9

src = Image.open("broccoli_base.png").convert("RGBA")

# 删除与边缘相连的白色背景，保留西兰花内部白色
w, h = src.size
px = src.load()

corners = [
    px[0, 0][:3],
    px[w - 1, 0][:3],
    px[0, h - 1][:3],
    px[w - 1, h - 1][:3],
]
bg = tuple(sum(c[i] for c in corners) // 4 for i in range(3))

def dist(a, b):
    return sum(abs(a[i] - b[i]) for i in range(3))

visited = set()
q = deque()

def add(x, y):
    if (x, y) in visited:
        return
    if 0 <= x < w and 0 <= y < h:
        if dist(px[x, y][:3], bg) < 75:
            visited.add((x, y))
            q.append((x, y))

for x in range(w):
    add(x, 0)
    add(x, h - 1)

for y in range(h):
    add(0, y)
    add(w - 1, y)

while q:
    x, y = q.popleft()
    add(x + 1, y)
    add(x - 1, y)
    add(x, y + 1)
    add(x, y - 1)

for x, y in visited:
    r, g, b, _ = px[x, y]
    px[x, y] = (r, g, b, 0)

bbox = src.getbbox()
if bbox:
    src = src.crop(bbox)

src.thumbnail((142, 165), Image.Resampling.LANCZOS)

sheet = Image.new("RGBA", (FRAME_W * COLS, FRAME_H * ROWS), (0, 0, 0, 0))

def make_frame(dx=0, dy=0, angle=0, sx=1.0, sy=1.0, flip=False):
    pet = src.copy()

    if flip:
        pet = ImageOps.mirror(pet)

    new_w = max(1, int(pet.width * sx))
    new_h = max(1, int(pet.height * sy))

    pet = pet.resize((new_w, new_h), Image.Resampling.LANCZOS)

    if angle:
        pet = pet.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

    frame = Image.new("RGBA", (FRAME_W, FRAME_H), (0, 0, 0, 0))
    x = (FRAME_W - pet.width) // 2 + dx
    y = (FRAME_H - pet.height) // 2 + dy
    frame.alpha_composite(pet, (x, y))
    return frame

animations = [
    # row 0 idle
    [
        (0,0,0,1,1,False),
        (0,-2,-1,1,1,False),
        (0,-3,0,1.01,.99,False),
        (0,-2,1,1,1,False),
        (0,0,0,1,1,False),
        (0,1,0,.99,1.01,False),
    ],
    # row 1 running-right
    [
        (0,2,-6,1.03,.97,False),
        (2,0,-3,1,1,False),
        (4,-2,1,.98,1.02,False),
        (5,0,5,1.02,.98,False),
        (4,2,4,1.03,.97,False),
        (2,0,0,1,1,False),
        (1,-2,-3,.99,1.02,False),
        (0,0,-6,1.02,.98,False),
    ],
    # row 2 running-left
    [
        (0,2,6,1.03,.97,True),
        (-2,0,3,1,1,True),
        (-4,-2,-1,.98,1.02,True),
        (-5,0,-5,1.02,.98,True),
        (-4,2,-4,1.03,.97,True),
        (-2,0,0,1,1,True),
        (-1,-2,3,.99,1.02,True),
        (0,0,6,1.02,.98,True),
    ],
    # row 3 waving
    [
        (0,0,-4,1,1,False),
        (0,-2,5,1,1,False),
        (0,0,-4,1,1,False),
        (0,-2,5,1,1,False),
    ],
    # row 4 jumping
    [
        (0,5,0,1.05,.94,False),
        (0,-6,-2,.98,1.03,False),
        (0,-15,0,.96,1.06,False),
        (0,-6,2,.98,1.03,False),
        (0,5,0,1.05,.94,False),
    ],
    # row 5 failed
    [
        (0,0,0,1,1,False),
        (0,2,4,1,1,False),
        (0,5,8,1,1,False),
        (0,8,13,1,1,False),
        (0,10,17,1,1,False),
        (0,8,13,1,1,False),
        (0,5,8,1,1,False),
        (0,2,4,1,1,False),
    ],
    # row 6 waiting
    [
        (0,0,0,1,1,False),
        (0,1,-1,1,1,False),
        (0,2,0,1,1,False),
        (0,1,1,1,1,False),
        (0,0,0,1,1,False),
        (0,1,0,1,1,False),
    ],
    # row 7 running
    [
        (0,2,-3,1.02,.98,False),
        (0,-1,0,1,1,False),
        (0,-3,3,.98,1.02,False),
        (0,-1,0,1,1,False),
        (0,2,-3,1.02,.98,False),
        (0,0,0,1,1,False),
    ],
    # row 8 review
    [
        (0,0,0,1,1,False),
        (1,-1,1,1,1,False),
        (0,-2,0,1,1.01,False),
        (-1,-1,-1,1,1,False),
        (0,0,0,1,1,False),
        (0,1,0,1,1,False),
    ]
]

for row, frames in enumerate(animations):
    rendered = [make_frame(*args) for args in frames]
    while len(rendered) < 8:
        rendered.append(rendered[-1].copy())

    for col in range(8):
        x = col * FRAME_W
        y = row * FRAME_H
        sheet.alpha_composite(rendered[col], (x, y))

sheet.save("spritesheet.webp", "WEBP", lossless=True, quality=100)

print("🥦 西兰花桌宠生成完成！")
print("spritesheet.webp size =", sheet.size)
