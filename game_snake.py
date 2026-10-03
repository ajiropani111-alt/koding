import pygame
import sys
import random

# Inisialisasi Pygame
pygame.init()

# Konfigurasi Ukuran Ubin (Tile Size)
UKURAN_UBIN = 40

# Peta Labirin (12 kolom x 10 baris)
# W = Dinding, . = Lantai, P = Pemain, K = Kunci, D = Pintu, E = Peti/Exit
PETA = [
    "WWWWWWWWWWWW",
    "WP..W......W",
    "W.W.W.WWWW.W",
    "W.W...W....W",
    "W.WWWWW.WW.W",
    "W.....W..K.W",
    "WWWW.W.WWWWW",
    "W....W.....W",
    "W.WWWWWW.D.W",
    "W........E.W",
    "WWWWWWWWWWWW"
]

LEBAR_LAYAR = len(PETA[0]) * UKURAN_UBIN
TINGGI_LAYAR = len(PETA) * UKURAN_UBIN

layar = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))
pygame.display.set_caption("Petualangan Labirin 2D")
jam = pygame.time.Clock()

# --- FUNGSI MENGGAMBAR SPRITE OTOMATIS DI MEMORI ---
def membuat_pemain():
    surf = pygame.Surface((UKURAN_UBIN, UKURAN_UBIN), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (255, 204, 0), [(8, 12), (2, 0), (14, 8)])
    pygame.draw.polygon(surf, (20, 20, 20), [(4, 4), (2, 0), (8, 6)])
    pygame.draw.polygon(surf, (255, 204, 0), [(32, 12), (38, 0), (26, 8)])
    pygame.draw.polygon(surf, (20, 20, 20), [(36, 4), (38, 0), (32, 6)])
    pygame.draw.ellipse(surf, (255, 204, 0), (6, 10, 28, 26))
    pygame.draw.circle(surf, (235, 50, 35), (11, 26), 4)
    pygame.draw.circle(surf, (235, 50, 35), (29, 26), 4)
    pygame.draw.circle(surf, (20, 20, 20), (14, 20), 3)
    pygame.draw.circle(surf, (255, 255, 255), (13, 19), 1)
    pygame.draw.circle(surf, (20, 20, 20), (26, 20), 3)
    pygame.draw.circle(surf, (255, 255, 255), (25, 19), 1)
    pygame.draw.polygon(surf, (20, 20, 20), [(19, 23), (21, 23), (20, 24)])
    pygame.draw.arc(surf, (20, 20, 20), (16, 23, 8, 5), 3.14, 0, 2)
    return surf

def membuat_dinding():
    surf = pygame.Surface((UKURAN_UBIN, UKURAN_UBIN))
    surf.fill((139, 69, 19))
    pygame.draw.rect(surf, (180, 100, 50), (2, 2, 16, 8))
    pygame.draw.rect(surf, (180, 100, 50), (21, 2, 16, 8))
    pygame.draw.rect(surf, (180, 100, 50), (2, 13, 35, 8))
    pygame.draw.rect(surf, (180, 100, 50), (2, 24, 16, 8))
    pygame.draw.rect(surf, (180, 100, 50), (21, 24, 16, 8))
    return surf

def membuat_lantai():
    surf = pygame.Surface((UKURAN_UBIN, UKURAN_UBIN))
    surf.fill((34, 139, 34))
    random.seed(123)
    for _ in range(25):
        x = random.randint(2, 36)
        y = random.randint(4, 36)
        pygame.draw.line(surf, (50, 205, 50), (x, y), (x + 1, y - 3), 1)
        pygame.draw.line(surf, (10, 90, 10), (x + 2, y), (x + 3, y - 2), 1)
    return surf

def membuat_kunci():
    surf = pygame.Surface((UKURAN_UBIN, UKURAN_UBIN), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 215, 0), (20, 14), 7, 3)
    pygame.draw.rect(surf, (255, 215, 0), (18, 20, 4, 14))
    pygame.draw.rect(surf, (255, 215, 0), (22, 25, 5, 3))
    pygame.draw.rect(surf, (255, 215, 0), (22, 30, 4, 3))
    return surf

def membuat_pintu():
    surf = pygame.Surface((UKURAN_UBIN, UKURAN_UBIN))
    surf.fill((34, 139, 34))
    pygame.draw.rect(surf, (101, 67, 33), (4, 2, 32, 36))
    pygame.draw.rect(surf, (160, 82, 45), (7, 5, 26, 30))
    pygame.draw.line(surf, (101, 67, 33), (15, 5), (15, 34), 1)
    pygame.draw.line(surf, (101, 67, 33), (24, 5), (24, 34), 1)
    pygame.draw.circle(surf, (255, 215, 0), (26, 20), 3)
    return surf

def membuat_peti():
    surf = pygame.Surface((UKURAN_UBIN, UKURAN_UBIN))
    surf.fill((34, 139, 34))
    pygame.draw.rect(surf, (139, 69, 19), (6, 12, 28, 22))
    pygame.draw.rect(surf, (218, 165, 32), (6, 12, 28, 22), 2)
    pygame.draw.line(surf, (218, 165, 32), (6, 20), (33, 20), 2)
    pygame.draw.rect(surf, (255, 215, 0), (18, 18, 4, 6))
    return surf

# Jika file PNG tidak ditemukan, otomatis menggambar sendiri
def load_atau_buat(filename, fungsi_buat):
    try:
        return pygame.transform.scale(pygame.image.load(filename), (UKURAN_UBIN, UKURAN_UBIN))
    except:
        return fungsi_buat()

img_pemain = load_atau_buat("pemain.png", membuat_pemain)
img_dinding = load_atau_buat("dinding.png", membuat_dinding)
img_lantai = load_atau_buat("lantai.png", membuat_lantai)
img_kunci = load_atau_buat("kunci.png", membuat_kunci)
img_pintu = load_atau_buat("pintu.png", membuat_pintu)
img_keluar = load_atau_buat("keluar.png", membuat_peti)

# Posisi & Status Awal
pos_pemain_x, pos_pemain_y = 1, 1
punya_kunci = False
pintu_terbuka = False
game_selesai = False

for y, baris in enumerate(PETA):
    for x, karakter in enumerate(baris):
        if karakter == 'P':
            pos_pemain_x, pos_pemain_y = x, y

def gambar_peta():
    for y, baris in enumerate(PETA):
        for x, karakter in enumerate(baris):
            pos_x = x * UKURAN_UBIN
            pos_y = y * UKURAN_UBIN
            
            layar.blit(img_lantai, (pos_x, pos_y))
            
            if karakter == 'W':
                layar.blit(img_dinding, (pos_x, pos_y))
            elif karakter == 'K' and not punya_kunci:
                layar.blit(img_kunci, (pos_x, pos_y))
            elif karakter == 'D' and not pintu_terbuka:
                layar.blit(img_pintu, (pos_x, pos_y))
            elif karakter == 'E':
                layar.blit(img_keluar, (pos_x, pos_y))

    layar.blit(img_pemain, (pos_pemain_x * UKURAN_UBIN, pos_pemain_y * UKURAN_UBIN))

# Loop Utama Game
berjalan = True
while berjalan:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            berjalan = False
            
        elif event.type == pygame.KEYDOWN and not game_selesai:
            dx, dy = 0, 0
            if event.key in (pygame.K_LEFT, pygame.K_a):
                dx = -1
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                dx = 1
            elif event.key in (pygame.K_UP, pygame.K_w):
                dy = -1
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                dy = 1

            target_x = pos_pemain_x + dx
            target_y = pos_pemain_y + dy
            target_karakter = PETA[target_y][target_x]

            if target_karakter != 'W':
                if target_karakter == 'D' and not pintu_terbuka:
                    if punya_kunci:
                        pintu_terbuka = True
                        pos_pemain_x, pos_pemain_y = target_x, target_y
                else:
                    pos_pemain_x, pos_pemain_y = target_x, target_y

                if target_karakter == 'K':
                    punya_kunci = True

                if target_karakter == 'E':
                    game_selesai = True

    gambar_peta()

    if game_selesai:
        font = pygame.font.SysFont("Arial", 32, bold=True)
        teks = font.render("KAMU MENANG!", True, (255, 255, 255))
        rect_teks = teks.get_rect(center=(LEBAR_LAYAR // 2, TINGGI_LAYAR // 2))
        
        s = pygame.Surface((LEBAR_LAYAR, 60))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        layar.blit(s, (0, TINGGI_LAYAR // 2 - 30))
        layar.blit(teks, rect_teks)

    pygame.display.flip()
    jam.tick(30)

pygame.quit()
sys.exit()