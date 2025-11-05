# ================================================
#   MATRIX PRO MAX ULTRA v9.9.9 - by GROK HACKER
#   Features: Multi-thread, Progress Bar, 3D Rain,
#             Fake Hacking, RGB Glow, Sound, Auto-Resize
# ================================================

import pygame
import random
import sys
import threading
import time
import numpy as np
from pygame.locals import *
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.console import Console
from queue import Queue

# ====================== CONFIG ======================
WIDTH, HEIGHT = 1400, 900
FULLSCREEN = False
FPS = 60
GLOW_INTENSITY = 255
ENABLE_SOUND = True
ENABLE_3D = True
ENABLE_HACKING_SIM = True
# ====================================================

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
if FULLSCREEN:
    screen = pygame.display.set_mode((0, 0), FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("MATRIX PRO MAX ULTRA v9.9.9")
clock = pygame.time.Clock()

# Font
FONT_BIG = pygame.font.SysFont('consolas', 28, bold=True)
FONT_MED = pygame.font.SysFont('courier', 20, bold=True)
FONT_SMALL = pygame.font.SysFont('courier', 16)

# Màu
GREEN = (0, 255, 100)
CYAN = (0, 255, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
PURPLE = (200, 0, 255)
WHITE = (255, 255, 255)

# Ký tự Matrix
MATRIX_CHARS = list("01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン")

# Âm thanh (tải file free từ web nếu muốn)
try:
    if ENABLE_SOUND:
        pygame.mixer.init()
        pygame.mixer.music.load("matrix_theme.mp3")  # Tự thêm file
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
except:
    ENABLE_SOUND = False

# ====================== PROGRESS BAR THREAD ======================
console = Console()
progress_queue = Queue()

def fake_hacking_task():
    tasks = [
        ("Breaching firewall", 15),
        ("Decrypting AES-256", 20),
        ("Injecting payload", 18),
        ("Bypassing AI defense", 25),
        ("Accessing mainframe", 22),
        ("Downloading secrets", 30),
        ("Erasing traces", 15),
    ]
    with Progress(
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=40),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        console=console
    ) as progress:
        for name, total in tasks:
            task = progress.add_task(name, total=total)
            for _ in range(total):
                time.sleep(0.1)
                progress.update(task, advance=1)
                progress_queue.put(("update", name, total))
            progress_queue.put(("complete", name))

# ====================== 3D MATRIX RAIN ======================
class Drop3D:
    def __init__(self, x, z_depth=0):
        self.x = x
        self.y = random.randint(-1000, -100)
        self.z = z_depth
        self.speed = random.uniform(5, 25) * (1 + z_depth / 10)
        self.length = random.randint(8, 25)
        self.chars = [random.choice(MATRIX_CHARS) for _ in range(self.length)]
        self.glow = 255
        self.angle = 0

    def update(self):
        self.y += self.speed
        self.angle += 0.05
        if self.y > HEIGHT + 200:
            self.y = random.randint(-500, -100)
            self.speed = random.uniform(5, 25) * (1 + self.z / 10)
            self.length = random.randint(8, 25)
            self.chars = [random.choice(MATRIX_CHARS) for _ in range(self.length)]
            self.glow = 255
        else:
            self.glow = max(100, self.glow - 2)

    def draw(self, surface):
        scale = 1 / (1 + self.z / 800)
        opacity = int(self.glow * scale)
        if opacity < 50: return

        for i, char in enumerate(self.chars):
            y_pos = self.y - i * 28 * scale
            if y_pos < -50 or y_pos > HEIGHT + 50: continue

            # 3D perspective
            x_offset = self.x + np.sin(self.angle + i) * 10 * scale
            size = int(20 * scale)

            # Glow effect
            glow_surf = pygame.Surface((size*3, size*3), SRCALPHA)
            for g in range(5, 0, -1):
                alpha = max(0, opacity // g)
                color = (0, min(255, alpha), 0)
                pygame.draw.circle(glow_surf, (*color, alpha//3), (size*1.5, size*1.5), g*3)

            # Render char
            font = pygame.font.SysFont('courier', size, bold=True)
            text = font.render(char, True, (0, opacity, 0))
            text_pos = (x_offset - text.get_width()//2, y_pos - text.get_height()//2)

            surface.blit(glow_surf, (x_offset - size*1.5, y_pos - size*1.5), special_flags=BLEND_ADD)
            surface.blit(text, text_pos)

# Tạo mưa 3D
drops = []
for x in range(0, WIDTH, 30):
    for layer in range(3):
        drops.append(Drop3D(x + random.randint(-15, 15), z_depth=layer * 300))

# Fade surface
fade = pygame.Surface((WIDTH, HEIGHT), SRCALPHA)
fade.fill((0, 20, 0, 8))

# ====================== MAIN LOOP ======================
hacking_thread = threading.Thread(target=fake_hacking_task, daemon=True)
hacking_thread.start()

hacking_status = {}
show_progress = True
rainbow_phase = 0

running = True
while running:
    dt = clock.tick(FPS) / 1000
    rainbow_phase += dt * 3

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_F11:
                FULLSCREEN = not FULLSCREEN
                if FULLSCREEN:
                    screen = pygame.display.set_mode((0,0), FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((1400,900), RESIZABLE)
                WIDTH, HEIGHT = screen.get_size()
            if event.key == K_SPACE:
                show_progress = not show_progress

    # Hiệu ứng fade
    screen.blit(fade, (0, 0))

    # Cập nhật & vẽ mưa 3D
    for drop in drops:
        drop.update()
        drop.draw(screen)

    # Rainbow title
    title_color = (
        int(127 + 128 * np.sin(rainbow_phase)),
        int(127 + 128 * np.sin(rainbow_phase + 2)),
        int(127 + 128 * np.sin(rainbow_phase + 4))
    )
    title = FONT_BIG.render("MATRIX PRO MAX ULTRA", True, title_color)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 15))

    # Hiển thị thông tin hệ thống
    info = FONT_SMALL.render(f"FPS: {clock.get_fps():.1f} | Drops: {len(drops)} | 3D: ON | Sound: {'ON' if ENABLE_SOUND else 'OFF'}", True, CYAN)
    screen.blit(info, (10, HEIGHT - 30))

    # Progress bar từ thread
    while not progress_queue.empty():
        msg = progress_queue.get()
        if msg[0] == "complete":
            hacking_status[msg[1]] = "DONE"

    if show_progress and ENABLE_HACKING_SIM:
        y = 80
        for task_name, status in list(hacking_status.items())[-5:]:
            color = GREEN if status == "DONE" else YELLOW
            txt = FONT_MED.render(f"[{status}] {task_name}", True, color)
            screen.blit(txt, (50, y))
            y += 35

    # Thêm hiệu ứng scanline
    for i in range(0, HEIGHT, 4):
        if random.random() < 0.02:
            pygame.draw.line(screen, (0, 50, 0, 50), (0, i), (WIDTH, i), 1)

    pygame.display.flip()

# Cleanup
pygame.quit()
sys.exit()
