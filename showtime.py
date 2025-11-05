import time, sys, os
from colorama import Fore, Style, init
from pyfiglet import Figlet
import random

init(autoreset=True)

# Tạo hiệu ứng gõ chữ
def type_effect(text, color=Fore.CYAN, delay=0.04):
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Tạo banner ASCII ngầu
def show_banner(text, font="slant", color=Fore.MAGENTA):
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = Figlet(font=font)
    print(color + banner.renderText(text) + Style.RESET_ALL)

# Hiệu ứng "loading"
def loading_bar(text="Đang khởi động...", length=20, delay=0.1):
    type_effect(text, Fore.YELLOW)
    for i in range(length + 1):
        bar = '█' * i + '-' * (length - i)
        sys.stdout.write(f'\r[{bar}] {int(i/length*100)}%')
        sys.stdout.flush()
        time.sleep(delay)
    print("\n")

# ---------- BẮT ĐẦU CHƯƠNG TRÌNH ----------
show_banner("Showtime", "standard", Fore.BLUE)
loading_bar("Chuẩn bị bài thuyết trình...")

intro_lines = [
    "Xin chào mọi người 👋",
    "Hôm nay, tôi sẽ mang đến cho các bạn một điều thật đặc biệt...",
    "Một hành trình của công nghệ, sáng tạo và đam mê 💡🔥",
]

for line in intro_lines:
    type_effect(line, random.choice([Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA]), 0.05)
    time.sleep(0.5)

show_banner("Let's Begin!", "starwars", Fore.RED)
time.sleep(1)

# PHẦN CHÍNH
slides = [
    ("Chủ đề", "Công nghệ tạo nên sự khác biệt 💻"),
    ("Điểm nổi bật", "Kết hợp sáng tạo, tư duy và đột phá 🚀"),
    ("Thông điệp", "Hãy dám nghĩ, dám làm, và dám bứt phá! 💥")
]

for title, content in slides:
    show_banner(title, "banner3-D", Fore.CYAN)
    type_effect(content, Fore.WHITE, 0.05)
    time.sleep(2)

# KẾT THÚC
show_banner("THANK YOU!", "slant", Fore.YELLOW)
type_effect("Hãy để ý tưởng của bạn tỏa sáng 🌟", Fore.LIGHTGREEN_EX)
type_effect("— End of Presentation —", Fore.LIGHTBLACK_EX)
