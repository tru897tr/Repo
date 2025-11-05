# =====================================================
#   MATRIX AUTO v11.0 - SIÊU MƯỢT, KHÔNG LỖI
#   + Hiệu ứng loading "Đang xác định thiết bị..."
#   + Tự động chuyển chế độ
#   + Không lỗi import *
# =====================================================

import os
import sys
import time
import random
import threading
import platform
from queue import Queue

# ====================== HIỆU ỨNG LOADING NGẦU ======================
def loading_animation(text, duration=3):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r\033[92m{chars[i % len(chars)]}\033[0m \033[1;36m{text}\033[0m")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print(f"\r\033[92m✔\033[0m \033[1;36m{text} DONE!\033[0m")

# ====================== PHÁT HIỆN THIẾT BỊ ======================
def detect_environment():
    print("\n" + "="*50)
    loading_animation("Đang quét hệ điều hành...", 1.5)
    loading_animation("Phát hiện CPU & kiến trúc...", 1.5)
    loading_animation("Kiểm tra môi trường GUI...", 2)

    system = platform.system().lower()
    machine = platform.machine().lower()
    is_termux = 'com.termux' in os.environ.get('PREFIX', '')
    is_android = 'android' in system or is_termux
    is_mobile = is_android or 'arm' in machine or 'aarch64' in machine

    has_gui = False
    try:
        import pygame
        pygame.init()
        pygame.display.set_mode((1,1), pygame.NOFRAME)
        pygame.quit()
        has_gui = True
    except:
        has_gui = False

    env = {
        'is_termux': is_termux,
        'is_android': is_android,
        'is_mobile': is_mobile,
        'has_gui': has_gui,
        'system': system
    }

    # In kết quả ngầu
    print("\n\033[1;33m╔════════════════ KẾT QUẢ PHÁT HIỆN ════════════════╗\033[0m")
    print(f"║ Hệ điều hành : \033[1;36m{platform.system():<15}\033[0m                  ║")
    print(f"║ Thiết bị     : \033[1;36m{'ĐIỆN THOẠI' if is_mobile else 'MÁY TÍNH':<15}\033[0m              ║")
    print(f"║ Termux       : \033[1;36m{'CÓ' if is_termux else 'KHÔNG':<15}\033[0m                 ║")
    print(f"║ GUI (pygame) : \033[1;36m{'SẴN SÀNG' if has_gui else 'KHÔNG HỖ TRỢ':<15}\033[0m            ║")
    print("\033[1;33m╚═══════════════════════════════════════════════════╝\033[0m\n")
    time.sleep(1)

    return env

# ====================== CHẾ ĐỘ TERMUX: ASCII MATRIX ======================
def run_ascii_matrix():
    os.system('clear') if os.name == 'posix' else os.system('cls')
    print("\033[?25l")  # Ẩn con trỏ
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    
    try:
        width = os.get_terminal_size().columns
        height = os.get_terminal_size().lines - 3
    except:
        width, height = 80, 24

    drops = [0] * width
    progress_queue = Queue()
    hacking_status = {}

    def fake_hack():
        tasks = [
            ("Scanning ports...", 18),
            ("Cracking password...", 22),
            ("Bypassing firewall...", 20),
            ("Access granted!", 15),
        ]
        for name, steps in tasks:
            for i in range(steps):
                time.sleep(0.12)
                progress_queue.put(("update", name, i+1, steps))
            progress_queue.put(("done", name))

    threading.Thread(target=fake_hack, daemon=True).start()

    try:
        while True:
            # Cập nhật giọt
            for i in range(width):
                if drops[i] <= 0 or random.random() < 0.075:
                    drops[i] = random.randint(5, height)
                drops[i] -= 1

            # Vẽ khung
            frame = [[' ' for _ in range(width)] for _ in range(height)]
            for x in range(width):
                y = height - drops[x]
                if y >= 0:
                    trail = min(15, drops[x])
                    for dy in range(trail):
                        intensity = max(0, 255 - dy * 17)
                        if intensity > 200:
                            color = "\033[92m"  # sáng
                        elif intensity > 100:
                            color = "\033[32m"  # trung
                        else:
                            color = "\033[90m"  # tối
                        char = random.choice(chars) if dy == 0 else frame[y + dy][x]
                        frame[y + dy][x] = f"{color}{char}\033[0m"

            # In màn hình
            output = '\n'.join(''.join(row) for row in frame)
            print(f"\033[H{output}")

            # Progress bar
            lines = []
            while not progress_queue.empty():
                msg = progress_queue.get()
                if msg[0] == "update":
                    name, cur, total = msg[1], msg[2], msg[3]
                    bar = "█" * cur + "░" * (total - cur)
                    lines.append(f"\033[91m┃ {name}")
                    lines.append(f"┃ [{bar}] {cur}/{total}")
                elif msg[0] == "done":
                    hacking_status[msg[1]] = "DONE"

            if lines:
                print("\n\033[91m┌─ HACKING IN PROGRESS ─┐\033[0m")
                for line in lines[-4:]:
                    print(line)
                print("└" + "─" * 22 + "┘\033[0m")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\033[?25h\033[0m")
        print("\n\033[91mHacker disconnected. Trace erased.\033[0m")
        sys.exit()

# ====================== CHẾ ĐỘ PC: PYGAME 3D ======================
# Import pygame ở đây để tránh lỗi khi không có GUI
try:
    import pygame
    import numpy as np
    from pygame.locals import *
    PYGAME_AVAILABLE = True
except:
    PYGAME_AVAILABLE = False

def run_pygame_matrix():
    if not PYGAME_AVAILABLE:
        print("Pygame không khả dụng!")
        return

    pygame.init()
    WIDTH, HEIGHT = 1400, 900
    screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
    pygame.display.set_caption("MATRIX PRO - PC MODE")
    clock = pygame.time.Clock()

    FONT_BIG = pygame.font.SysFont('consolas', 30, bold=True)
    chars = list("01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン")

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
                if -50 < y_pos < HEIGHT + 50:
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
            if event.type == KEYDOWN:
                if event.key == K_F11:
                    global WIDTH, HEIGHT
                    flags = screen.get_flags()
                    if flags & FULLSCREEN:
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
        title = FONT_BIG.render("MATRIX PRO - PC MODE", True, title_color)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 15))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# ====================== CHẠY CHƯƠNG TRÌNH ======================
if __name__ == "__main__":
    env = detect_environment()

    if env['is_termux'] or (env['is_mobile'] and not env['has_gui']):
        print("\033[91mChuyển sang chế độ TERMUX ASCII MATRIX...\033[0m")
        time.sleep(1.5)
        run_ascii_matrix()
    else:
        print("\033[92mKhởi chạy MATRIX 3D PRO trên PC...\033[0m")
        time.sleep(1.5)
        run_pygame_matrix()
