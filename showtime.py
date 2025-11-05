# =====================================================
#   MATRIX AUTO DETECT v10.0 - CHẠY MỌI NƠI
#   PC → Pygame 3D | Termux → ASCII Terminal
#   Tự động phát hiện thiết bị + hệ điều hành
# =====================================================

import platform
import os
import sys
import time
import random
import threading
from queue import Queue

# ====================== PHÁT HIỆN THIẾT BỊ ======================
def detect_environment():
    system = platform.system().lower()
    machine = platform.machine().lower()
    is_termux = 'com.termux' in os.environ.get('PREFIX', '')
    is_android = 'android' in system or is_termux
    is_mobile = is_android or 'arm' in machine or 'aarch64' in machine
    has_gui = False

    try:
        import pygame
        pygame.init()
        pygame.display.set_mode((1,1))
        has_gui = True
        pygame.quit()
    except:
        has_gui = False

    return {
        'is_termux': is_termux,
        'is_android': is_android,
        'is_mobile': is_mobile,
        'has_gui': has_gui,
        'system': system
    }

env = detect_environment()

# ====================== MODE: TERMUX ASCII MATRIX ======================
def run_termux_matrix():
    print("\033[?25l")  # Ẩn con trỏ
    print("\033[2J\033[H")  # Xóa màn hình

    chars = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン01"
    width = os.get_terminal_size().columns
    height = os.get_terminal_size().lines - 1

    # Khởi tạo cột
    drops = [0] * width

    def update_drops():
        for i in range(width):
            if drops[i] == 0 or random.random() < 0.05:
                drops[i] = random.randint(1, height)
            else:
                drops[i] -= 1

    def draw():
        frame = [[' ' for _ in range(width)] for _ in range(height)]
        for x in range(width):
            y = drops[x]
            if y > 0:
                for dy in range(min(15, y)):
                    intensity = max(0, 255 - dy * 18)
                    if intensity > 200:
                        color = "\033[92m"  # Xanh sáng
                    elif intensity > 100:
                        color = "\033[32m"  # Xanh vừa
                    else:
                        color = "\033[90m"  # Xanh tối
                    char = random.choice(chars) if dy == 0 else frame[height - y + dy][x]
                    frame[height - y + dy][x] = f"{color}{char}\033[0m"
        return '\n'.join(''.join(row) for row in frame)

    # Progress bar giả lập hack
    hacking_status = {}
    progress_queue = Queue()

    def fake_hack_thread():
        tasks = [
            ("Scanning network...", 20),
            ("Brute force SSH...", 25),
            ("Injecting rootkit...", 18),
            ("Access granted!", 15),
        ]
        for name, steps in tasks:
            for i in range(steps):
                time.sleep(0.15)
                progress_queue.put(("update", name, i+1, steps))
            progress_queue.put(("complete", name))

    threading.Thread(target=fake_hack_thread, daemon=True).start()

    try:
        while True:
            update_drops()
            print(f"\033[H{draw()}")
            
            # Hiển thị progress bar
            while not progress_queue.empty():
                msg = progress_queue.get()
                if msg[0] == "complete":
                    hacking_status[msg[1]] = "DONE"
                elif msg[0] == "update":
                    name, cur, total = msg[1], msg[2], msg[3]
                    bar = "█" * cur + "░" * (total - cur)
                    print(f"\n\033[91m┌─ HACKING SYSTEM ─┐\033[0m")
                    print(f"│ {name}")
                    print(f"│ [{bar}] {cur}/{total}")
                    print(f"└{'─'*18}┘\033[0m")

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\033[?25h\033[0m")  # Hiện lại con trỏ
        print("Hacker logged out.")
        sys.exit()

# ====================== MODE: PC PYGAME 3D ======================
def run_pygame_matrix():
    # === TOÀN BỘ CODE PYGAME TỪ BẢN TRƯỚC (đã tối ưu) ===
    import pygame
    import numpy as np
    from pygame.locals import *

    pygame.init()
    WIDTH, HEIGHT = 1400, 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
    pygame.display.set_caption("MATRIX PRO MAX - PC MODE")
    clock = pygame.time.Clock()

    # Font & Màu
    FONT_BIG = pygame.font.SysFont('consolas', 28, bold=True)
    FONT_MED = pygame.font.SysFont('courier', 20, bold=True)
    chars = list("01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン")

    # 3D Drop class (gọn hơn)
    class Drop3D:
        def __init__(self, x, z=0):
            self.x, self.y, self.z = x, random.randint(-1000, -100), z
            self.speed = random.uniform(5, 25) * (1 + z/1000)
            self.length = random.randint(8, 25)
            self.chars = [random.choice(chars) for _ in range(self.length)]
            self.glow = 255

        def update(self):
            self.y += self.speed
            if self.y > HEIGHT + 200:
                self.y = random.randint(-500, -100)
                self.speed = random.uniform(5, 25) * (1 + self.z/1000)
                self.length = random.randint(8, 25)
                self.chars = [random.choice(chars) for _ in range(self.length)]
                self.glow = 255
            else:
                self.glow = max(100, self.glow - 2)

        def draw(self, surf):
            scale = 1 / (1 + self.z / 800)
            opacity = int(self.glow * scale)
            if opacity < 50: return
            for i, char in enumerate(self.chars):
                y_pos = self.y - i * 28 * scale
                if y_pos < -50 or y_pos > HEIGHT + 50: continue
                x_offset = self.x + np.sin(time.time() + i) * 10 * scale
                size = int(20 * scale)
                color = (0, min(255, opacity), 0)
                text = pygame.font.SysFont('courier', size, bold=True).render(char, True, color)
                surf.blit(text, (x_offset - text.get_width()//2, y_pos - text.get_height()//2))

    drops = [Drop3D(x + random.randint(-15,15), z) for x in range(0, WIDTH, 30) for z in [0, 300, 600]]
    fade = pygame.Surface((WIDTH, HEIGHT), SRCALPHA)
    fade.fill((0, 20, 0, 8))

    rainbow_phase = 0
    running = True
    while running:
        dt = clock.tick(60) / 1000
        rainbow_phase += dt * 3

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_F11:
                global screen, WIDTH, HEIGHT
                if screen.get_flags() & FULLSCREEN:
                    screen = pygame.display.set_mode((1400,900), RESIZABLE)
                else:
                    screen = pygame.display.set_mode((0,0), FULLSCREEN)
                WIDTH, HEIGHT = screen.get_size()

        screen.blit(fade, (0, 0))
        for drop in drops:
            drop.update()
            drop.draw(screen)

        title_color = (
            int(127 + 128 * np.sin(rainbow_phase)),
            int(127 + 128 * np.sin(rainbow_phase + 2)),
            int(127 + 128 * np.sin(rainbow_phase + 4))
        )
        title = FONT_BIG.render("MATRIX PRO MAX - PC", True, title_color)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 15))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# ====================== CHẠY CHẾ ĐỘ PHÙ HỢP ======================
if __name__ == "__main__":
    print(f"[+] Phát hiện: {platform.system()} | GUI: {env['has_gui']} | Termux: {env['is_termux']}")

    if env['is_termux'] or (env['is_mobile'] and not env['has_gui']):
        print("Điện thoại/Termux phát hiện → Chuyển sang chế độ ASCII!")
        run_termux_matrix()
    else:
        print("Máy tính phát hiện → Chạy Matrix 3D Pro Max!")
        try:
            run_pygame_matrix()
        except Exception as e:
            print(f"GUI lỗi: {e}\n→ Chuyển về chế độ ASCII!")
            run_termux_matrix()
