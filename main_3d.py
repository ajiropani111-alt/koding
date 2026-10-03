from ursina import *
from PIL import Image
import os
import random
import math

# --- 1. TEKSTUR WARNA SOLID OTOMATIS ---
os.makedirs('textures_temp', exist_ok=True)

def buat_gambar_warna(nama_file, rgb_tuple):
    path = os.path.join('textures_temp', nama_file)
    if not os.path.exists(path):
        img = Image.new('RGB', (16, 16), color=rgb_tuple)
        img.save(path)
    return path

tex_rumput  = buat_gambar_warna('rumput.png', (45, 120, 45))
tex_tanah   = buat_gambar_warna('tanah.png', (130, 90, 50))
tex_batang  = buat_gambar_warna('batang.png', (90, 50, 20))
tex_daun    = buat_gambar_warna('daun.png', (20, 90, 20))
tex_hitam   = buat_gambar_warna('hitam.png', (20, 20, 25))
tex_putih   = buat_gambar_warna('putih.png', (240, 240, 240))
tex_kulit   = buat_gambar_warna('kulit.png', (230, 180, 150))
tex_ikat    = buat_gambar_warna('ikat.png', (50, 60, 80))
tex_besi    = buat_gambar_warna('besi.png', (180, 190, 200))

# Warna Baju Karakter
tex_naruto_o = buat_gambar_warna('n_oranye.png', (255, 120, 0))
tex_naruto_k = buat_gambar_warna('n_kuning.png', (255, 215, 0))
tex_sasuke_b = buat_gambar_warna('s_biru.png', (40, 50, 120))
tex_sakura_p = buat_gambar_warna('s_pink.png', (230, 80, 120))
tex_kakashi_h= buat_gambar_warna('k_hijau.png', (40, 80, 50))
tex_kakashi_r= buat_gambar_warna('k_rambut.png', (210, 210, 215))
tex_akatsuki = buat_gambar_warna('akatsuki.png', (30, 30, 35))
tex_merah    = buat_gambar_warna('merah.png', (200, 30, 30))
tex_jurus    = buat_gambar_warna('jurus.png', (0, 230, 255))
tex_rumah    = buat_gambar_warna('rumah.png', (180, 140, 100))
tex_atap     = buat_gambar_warna('atap.png', (160, 40, 40))

# --- 2. INISIALISASI GAME ENGINE ---
app = Ursina()

window.title = "Petualangan Ninja 3D - Tampilan Top-Down (Dari Atas)"
window.fps_counter.enabled = False
window.color = color.rgb(255, 150, 90)

# --- 3. LINGKUNGAN DESA & HUTAN KONOHA ---
lantai = Entity(model='plane', scale=(100, 1, 100), position=(0, 0, 0), texture=tex_rumput, collider='box')
jalan  = Entity(model='plane', scale=(14, 1, 100), position=(0, 0.01, 0), texture=tex_tanah)
Entity(model='wireframe_cube', scale=(100, 10, 100), position=(0, 5, 0), texture=tex_hitam)

# Bangunan Rumah Desa
for z_pos in [-35, -15, 15, 35]:
    r_kiri = Entity(model='cube', scale=(8, 6, 10), position=(-18, 3, z_pos), texture=tex_rumah, collider='box')
    Entity(model='cone', scale=(10, 4, 12), position=(-18, 8, z_pos), texture=tex_atap)
    
    r_kanan = Entity(model='cube', scale=(8, 6, 10), position=(18, 3, z_pos), texture=tex_rumah, collider='box')
    Entity(model='cone', scale=(10, 4, 12), position=(18, 8, z_pos), texture=tex_atap)

# Pohon Hutan Konoha
for _ in range(30):
    px = random.choice([random.randint(-45, -25), random.randint(25, 45)])
    pz = random.randint(-45, 45)
    pohon = Entity(model='cylinder', scale=(1.4, 9, 1.4), position=(px, 4.5, pz), texture=tex_batang, collider='box')
    Entity(parent=pohon, model='sphere', scale=(4, 0.9, 4), position=(0, 0.4, 0), texture=tex_daun)

# --- 4. MEMBUAT KARAKTER NINJA DETAIL ---
def buat_karakter_detail(pos, tex_baju, tex_celana, tex_rambut, tex_rompi=None, nama=""):
    induk = Entity(position=pos, collider='box')
    induk.collider = BoxCollider(induk, center=Vec3(0, 1, 0), size=Vec3(0.8, 1.8, 0.8))
    
    # Kaki Kiri & Kanan
    kaki_kiri = Entity(parent=induk, model='cube', scale=(0.3, 0.7, 0.3), position=(-0.2, 0.35, 0), texture=tex_celana)
    kaki_kanan = Entity(parent=induk, model='cube', scale=(0.3, 0.7, 0.3), position=(0.2, 0.35, 0), texture=tex_celana)
    
    # Badan
    Entity(parent=induk, model='cube', scale=(0.7, 0.6, 0.4), position=(0, 1.0, 0), texture=tex_baju)
    if tex_rompi:
        Entity(parent=induk, model='cube', scale=(0.75, 0.55, 0.45), position=(0, 1.0, 0), texture=tex_rompi)
        
    # Tangan Kiri & Kanan
    tangan_kiri = Entity(parent=induk, model='cube', scale=(0.22, 0.65, 0.22), position=(-0.48, 1.0, 0), texture=tex_baju)
    tangan_kanan = Entity(parent=induk, model='cube', scale=(0.22, 0.65, 0.22), position=(0.48, 1.0, 0), texture=tex_baju)
    
    # Kepala
    kepala = Entity(parent=induk, model='cube', scale=(0.55, 0.45, 0.5), position=(0, 1.55, 0), texture=tex_kulit)
    Entity(parent=kepala, model='cube', scale=(1.05, 0.4, 1.05), position=(0, 0.3, 0), texture=tex_rambut)
    
    # Ikat Kepala Konoha
    ikat = Entity(parent=kepala, model='cube', scale=(1.02, 0.25, 1.02), position=(0, 0.05, 0), texture=tex_ikat)
    Entity(parent=ikat, model='cube', scale=(0.3, 0.15, 0.1), position=(0, 0, 0.5), texture=tex_besi)
    
    if nama:
        Text(text=nama, parent=induk, position=(0, 2.2, 0), scale=5, billboard=True, color=color.yellow)
        
    induk.kaki_kiri = kaki_kiri
    induk.kaki_kanan = kaki_kanan
    induk.tangan_kiri = tangan_kiri
    induk.tangan_kanan = tangan_kanan
    
    induk.waktu_ubah_arah = 0
    induk.kecepatan_npc = random.uniform(2, 4)
    induk.waktu_ayun = random.uniform(0, 10)
    
    return induk

# --- 5. KARAKTER PLAYER & TEMAN TIM 7 ---
player = buat_karakter_detail((0, 0, -25), tex_naruto_o, tex_naruto_o, tex_naruto_k)

sasuke  = buat_karakter_detail((-4, 0, -20), tex_sasuke_b, tex_putih, tex_hitam, nama="Sasuke")
sakura  = buat_karakter_detail((4, 0, -20), tex_sakura_p, tex_hitam, tex_sakura_p, nama="Sakura")
kakashi = buat_karakter_detail((0, 0, -17), tex_hitam, tex_hitam, tex_kakashi_r, tex_rompi=tex_kakashi_h, nama="Kakashi Sensei")

daftar_teman = [sasuke, sakura, kakashi]

# --- 6. MUSUH NINJA AKATSUKI ---
musuh_list = []
for i in range(8):
    mx = random.choice([random.randint(-40, -10), random.randint(10, 40)])
    mz = random.randint(-20, 40)
    
    musuh = buat_karakter_detail((mx, 0, mz), tex_akatsuki, tex_akatsuki, tex_hitam)
    Entity(parent=musuh, model='cube', scale=(0.4, 0.3, 0.42), position=(0, 1.0, 0), texture=tex_merah)
    musuh_list.append(musuh)

# --- 7. KONTROL KAMERA TOP-DOWN (DARI ATAS) ---
camera.parent = player
# Posisi tinggi di atas player (Y = 18), mundur sedikit di belakang (Z = -6)
camera.position = (0, 18, -6)
# Rotasi menunduk 70 derajat menghadap tanah
camera.rotation_x = 70

# UI Misi
teks_skor = Text(text=f"Musuh Tersisa: {len(musuh_list)}", position=(-0.45, 0.45), scale=1.5, color=color.yellow)
teks_info = Text(
    text="W/A/S/D: Jalan | Klik Kiri: Serang Rasengan | Klik Kanan: Shuriken | ESC: Keluar", 
    position=(-0.45, 0.4), 
    scale=1, 
    color=color.white
)

proyektil_list = []

# --- 8. FUNGSI PERGERAKAN NPC ---
def gerakkan_npc(npc):
    npc.waktu_ubah_arah -= time.dt
    if npc.waktu_ubah_arah <= 0:
        npc.rotation_y = random.uniform(0, 360)
        npc.waktu_ubah_arah = random.uniform(2, 6)
        
    npc.position += npc.forward * npc.kecepatan_npc * time.dt
    
    if abs(npc.x) > 42 or abs(npc.z) > 42:
        npc.rotation_y += 180
        
    npc.waktu_ayun += time.dt * 8
    sudut_ayun = math.sin(npc.waktu_ayun) * 25
    
    npc.tangan_kiri.rotation_x = sudut_ayun
    npc.tangan_kanan.rotation_x = -sudut_ayun
    npc.kaki_kiri.rotation_x = -sudut_ayun
    npc.kaki_kanan.rotation_x = sudut_ayun

# --- 9. LOGIKA PERMAINAN ---
waktu_jalan = 0

def update():
    global waktu_jalan
    kecepatan = 9 * time.dt
    sedang_jalan = False
    
    for t in daftar_teman:
        gerakkan_npc(t)
        
    for m in musuh_list:
        gerakkan_npc(m)

    # Input Kontrol Player
    if held_keys['w'] or held_keys['up arrow']:
        player.position += player.forward * kecepatan
        sedang_jalan = True
    if held_keys['s'] or held_keys['down arrow']:
        player.position -= player.forward * kecepatan
        sedang_jalan = True
    if held_keys['a'] or held_keys['left arrow']:
        player.rotation_y -= 120 * time.dt
    if held_keys['d'] or held_keys['right arrow']:
        player.rotation_y += 120 * time.dt

    # Animasi Jalan Naruto
    if sedang_jalan:
        waktu_jalan += time.dt * 12
        sudut_ayun = math.sin(waktu_jalan) * 35
        
        player.tangan_kiri.rotation_x = sudut_ayun
        player.tangan_kanan.rotation_x = -sudut_ayun
        player.kaki_kiri.rotation_x = -sudut_ayun
        player.kaki_kanan.rotation_x = sudut_ayun
    else:
        player.tangan_kiri.rotation_x = lerp(player.tangan_kiri.rotation_x, 0, 0.2)
        player.tangan_kanan.rotation_x = lerp(player.tangan_kanan.rotation_x, 0, 0.2)
        player.kaki_kiri.rotation_x = lerp(player.kaki_kiri.rotation_x, 0, 0.2)
        player.kaki_kanan.rotation_x = lerp(player.kaki_kanan.rotation_x, 0, 0.2)

    # Pergerakan Proyektil
    for p in proyektil_list[:]:
        p.position += p.forward * p.kecepatan * time.dt
        p.rotation_z += 25
        
        hit_info = p.intersects()
        if hit_info.hit:
            if hit_info.entity in musuh_list:
                hit_info.entity.animate_rotation((90, 0, 0), duration=0.2)
                hit_info.entity.animate_scale((0, 0, 0), duration=0.4)
                musuh_list.remove(hit_info.entity)
                destroy(hit_info.entity, delay=0.4)
                
                teks_skor.text = f"Musuh Tersisa: {len(musuh_list)}"
                
                if len(musuh_list) == 0:
                    teks_skor.text = "DESA KONOHA AMAN! TIM 7 BERHASIL!"
                    teks_skor.color = color.gold
            
            proyektil_list.remove(p)
            destroy(p)
        
        elif distance(p.position, player.position) > 50:
            proyektil_list.remove(p)
            destroy(p)

def input(key):
    if key == 'left mouse down':
        player.tangan_kanan.animate_rotation_x(-70, duration=0.1)
        player.tangan_kanan.animate_rotation_x(0, duration=0.2, delay=0.2)
        
        r = Entity(
            model='sphere',
            scale=0.6,
            position=player.world_position + Vec3(0, 1.2, 0) + player.forward * 1.5,
            rotation=player.world_rotation,
            texture=tex_jurus
        )
        r.kecepatan = 25
        proyektil_list.append(r)

    if key == 'right mouse down':
        player.tangan_kiri.animate_rotation_x(-60, duration=0.1)
        player.tangan_kiri.animate_rotation_x(0, duration=0.2, delay=0.2)
        
        s = Entity(
            model='cube',
            scale=(0.4, 0.02, 0.4),
            position=player.world_position + Vec3(0, 1.2, 0) + player.forward * 1.5,
            rotation=player.world_rotation,
            texture=tex_hitam
        )
        s.kecepatan = 38
        proyektil_list.append(s)

    if key == 'escape':
        application.quit()

app.run()