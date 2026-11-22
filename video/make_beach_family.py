"""해변 가족 2분 일러스트 애니메이션 (1280x720, 24fps).
색감: 사용자 제공 캡처 4장에서 뽑은 팔레트(차가운 청회색 어둠 + 따뜻한 피부톤 + 백금 머리 + 불씨 주황).
실행: python3 make_beach_family.py out.mp4
"""
import math, subprocess, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, DUR = 1280, 720, 24, 120
N = FPS * DUR
OUT = sys.argv[1] if len(sys.argv) > 1 else "beach_family.mp4"
FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

# ---- 캡처에서 뽑은 팔레트 ----
INK   = (6, 6, 11)       # 가장 어두운 그림자
NIGHT = (18, 22, 28)     # 배경 청흑
SLATE = (33, 37, 44)
STEEL = (48, 55, 63)     # 청회색
UMBER = (69, 51, 47)     # 어두운 피부 그늘
SKIN  = (110, 87, 82)    # 피부 중간
ROSE  = (151, 134, 133)  # 피부 밝은 쪽
PLAT  = (205, 190, 190)  # 백금 머리/하이라이트
EMBER = (232, 150, 80)   # 불씨·노을 포인트
DARKH = (38, 30, 28)     # 짙은 갈색 머리

def mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)

# 장면별 하늘·바다 색 (모두 같은 팔레트 안에서 밝기만 이동)
SCENES = [
    # 제목, 부제, 하늘 위, 하늘 아래(수평선), 바다, 모래, 해 위치(0~1, None), 해 색
    dict(title="파도가 처음 데려온 사람들", sky=(NIGHT, mix(STEEL, ROSE, .35)), sea=SLATE, sand=mix(UMBER, STEEL, .4), sun=.62, glow=ROSE),
    dict(title="모닥불 앞의 약속",          sky=(INK, SLATE),                    sea=NIGHT, sand=mix(UMBER, INK, .45),   sun=None, glow=EMBER),
    dict(title="새벽에 온 두 생명",          sky=(SLATE, mix(ROSE, PLAT, .3)),   sea=STEEL, sand=mix(SKIN, STEEL, .45),  sun=.30, glow=PLAT),
    dict(title="바다와 함께 자라는 아이들",  sky=(STEEL, mix(PLAT, ROSE, .2)),   sea=mix(STEEL, ROSE, .25), sand=mix(SKIN, ROSE, .35), sun=.75, glow=PLAT),
    dict(title="여섯, 그리고 같은 바다",     sky=(NIGHT, mix(EMBER, ROSE, .45)), sea=mix(SLATE, UMBER, .35), sand=mix(UMBER, NIGHT, .3), sun=.42, glow=EMBER),
]
SCENE_LEN = DUR / len(SCENES)   # 24초
HZ = 410                        # 수평선 y

def font(sz): return ImageFont.truetype(FONT, sz)
F_TITLE, F_SMALL, F_END = font(40), font(22), font(54)

# ---- 공통 후처리: 비네팅 + 필름 그레인 ----
yy, xx = np.mgrid[0:H, 0:W]
VIG = (1 - 0.55 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) ** 1.2).clip(0.25, 1)[..., None]
RNG = np.random.default_rng(7)
GRAIN = [RNG.normal(0, 5, (H, W, 1)) for _ in range(6)]

def background(sc, t_local, k):
    """하늘·해·바다·모래 그리기."""
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    top, low = sc["sky"]
    for y in range(HZ):
        d.line([(0, y), (W, y)], fill=mix(top, low, (y / HZ) ** 1.4))
    # 해/달
    if sc["sun"] is not None:
        sx = int(W * sc["sun"]); sy = int(HZ - 60 + (k == 4) * t_local * 4.5)  # 마지막 장면은 해가 진다
        glow = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(glow)
        gd.ellipse([sx - 170, sy - 170, sx + 170, sy + 170], fill=90)
        glow = glow.filter(ImageFilter.GaussianBlur(70))
        im = Image.composite(Image.new("RGB", (W, H), sc["glow"]), im, glow)
        d = ImageDraw.Draw(im)
        d.ellipse([sx - 34, sy - 34, sx + 34, sy + 34], fill=mix(sc["glow"], PLAT, .5))
    # 바다
    for y in range(HZ, 560):
        f = (y - HZ) / 150
        d.line([(0, y), (W, y)], fill=mix(mix(low, sc["sea"], .6), sc["sea"], f))
    # 물결 반짝임
    for i in range(26):
        y = HZ + 8 + (i * 37) % 140
        x = (i * 211 + t_local * (12 + i % 5) * 6) % (W + 200) - 100
        a = 0.35 + 0.25 * math.sin(t_local * 1.7 + i)
        d.line([(x, y), (x + 40 + i % 4 * 15, y)], fill=mix(sc["sea"], sc["glow"], a * (1 - (y - HZ) / 180)), width=2)
    # 밀려오는 파도선 + 모래
    surge = 18 * math.sin(t_local * 2 * math.pi / 6)
    pts = [(x, 560 + surge + 8 * math.sin(x / 90 + t_local * 1.3)) for x in range(0, W + 20, 20)]
    d.polygon(pts + [(W, H), (0, H)], fill=sc["sand"])
    d.line(pts, fill=mix(PLAT, sc["sand"], .35), width=3)
    return im

def person(d, x, g, h, hair, cloth, phase=0.0, walking=False, long_hair=False, face=1, hold_baby=False, skin_mul=1.0):
    """역광 실루엣풍 인물. g = 발 위치 y, h = 키(px)."""
    s = h / 180
    bob = 3 * s * abs(math.sin(phase)) if walking else 1.2 * s * math.sin(phase * .5)
    sw = math.sin(phase) * 14 * s if walking else 0
    hip = g - 82 * s - bob
    sh = g - 145 * s - bob
    hd = g - 165 * s - bob
    skin = mix(UMBER, SKIN, skin_mul)
    # 다리
    for sgn in (-1, 1):
        d.line([(x + sgn * 6 * s, hip), (x + sgn * 6 * s + sgn * sw, g)], fill=mix(cloth, INK, .45), width=max(3, int(11 * s)))
    # 몸통
    d.rounded_rectangle([x - 20 * s, sh, x + 20 * s, hip + 6 * s], radius=int(12 * s), fill=cloth)
    # 팔
    if hold_baby:
        d.ellipse([x + face * 4 * s - 16 * s, sh + 18 * s, x + face * 4 * s + 18 * s, sh + 42 * s], fill=PLAT)   # 아기 담요
        d.ellipse([x + face * 12 * s - 6 * s, sh + 16 * s, x + face * 12 * s + 6 * s, sh + 28 * s], fill=ROSE)
        d.line([(x - 18 * s, sh + 8 * s), (x + face * 10 * s, sh + 38 * s)], fill=cloth, width=max(3, int(9 * s)))
    else:
        for sgn in (-1, 1):
            d.line([(x + sgn * 19 * s, sh + 6 * s), (x + sgn * 22 * s - sgn * sw * .8, hip + 8 * s)], fill=cloth, width=max(3, int(9 * s)))
    # 머리
    r = 16 * s
    if long_hair:
        d.rounded_rectangle([x - r - 3 * s, hd - r, x + r + 3 * s, hd + r + 30 * s], radius=int(10 * s), fill=hair)
    d.ellipse([x - r, hd - r, x + r, hd + r], fill=skin)
    d.chord([x - r - 1, hd - r - 3 * s, x + r + 1, hd + r * .6], 180, 360, fill=hair)
    # 역광 테두리(따뜻한 하이라이트)
    d.arc([x - r, hd - r, x + r, hd + r], 200 if face > 0 else -20, 300 if face > 0 else 80, fill=mix(ROSE, PLAT, .5), width=max(1, int(2 * s)))

def kid(d, x, g, h, hair, cloth, phase, running=True):
    person(d, x, g, h, hair, cloth, phase=phase, walking=running, long_hair=False, skin_mul=1.0)

# 네 어른 고정 설정 (커플 A: 백금머리 여자 + 짙은머리 남자 / 커플 B: 짙은 긴머리 여자 + 밝은 갈색머리 남자)
A_W = dict(hair=PLAT, cloth=mix(INK, SLATE, .5), long_hair=True)
A_M = dict(hair=DARKH, cloth=mix(UMBER, INK, .4))
B_W = dict(hair=mix(DARKH, UMBER, .5), cloth=mix(ROSE, UMBER, .45), long_hair=True)
B_M = dict(hair=mix(ROSE, UMBER, .3), cloth=mix(STEEL, INK, .2))

def embers(d, t, n=40, cx=640, base=600):
    for i in range(n):
        life = (t * 0.35 + i / n) % 1
        x = cx + 60 * math.sin(i * 12.9 + life * 6) + (i % 7 - 3) * 8
        y = base - life * 330
        c = mix(EMBER, NIGHT, life)
        rr = 2.5 * (1 - life) + .5
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=c)

def scene_frame(k, t):
    sc = SCENES[k]
    im = background(sc, t, k)
    d = ImageDraw.Draw(im)
    g1, g2 = 640, 660
    if k == 0:   # 두 커플이 양쪽에서 걸어와 만남
        p = ease(t / 14)
        ax = -120 + p * 520; bx = W + 120 - p * 520
        person(d, ax, g1, 170, phase=t * 5 * (p < 1), walking=p < 1, face=1, **A_W)
        person(d, ax - 55, g1 + 6, 182, phase=t * 5 * (p < 1) + 1, walking=p < 1, face=1, **A_M)
        person(d, bx, g1, 168, phase=t * 5 * (p < 1) + 2, walking=p < 1, face=-1, **B_W)
        person(d, bx + 55, g1 + 6, 184, phase=t * 5 * (p < 1) + 3, walking=p < 1, face=-1, **B_M)
    elif k == 1:  # 밤, 모닥불, 맞잡은 손
        cx = 640
        fl = 1 + .15 * math.sin(t * 13) + .1 * math.sin(t * 7.3)
        glow = Image.new("L", (W, H), 0); ImageDraw.Draw(glow).ellipse([cx - 260 * fl, 380, cx + 260 * fl, 820], fill=110)
        im = Image.composite(Image.new("RGB", (W, H), EMBER), im, glow.filter(ImageFilter.GaussianBlur(90)))
        d = ImageDraw.Draw(im)
        for i, xx_ in enumerate((-150, -95, 95, 150)):
            cfg = [A_M, A_W, B_W, B_M][i]
            person(d, cx + xx_, g1, [182, 170, 168, 184][i], phase=t + i, face=1 if xx_ < 0 else -1, skin_mul=1.25, **cfg)
        d.line([(cx - 128, g1 - 75), (cx - 117, g1 - 75)], fill=SKIN, width=6)
        d.line([(cx + 117, g1 - 75), (cx + 128, g1 - 75)], fill=SKIN, width=6)
        d.polygon([(cx - 26, g1 + 12), (cx, g1 - 46 * fl), (cx + 26, g1 + 12)], fill=EMBER)
        d.polygon([(cx - 12, g1 + 12), (cx, g1 - 22 * fl), (cx + 12, g1 + 12)], fill=PLAT)
        d.line([(cx - 34, g1 + 14), (cx + 34, g1 + 8)], fill=DARKH, width=7)
        embers(d, t, cx=cx, base=g1 - 10)
    elif k == 2:  # 새벽, 각 커플이 아기를 안고 있음
        person(d, 380, g1, 170, phase=t, face=1, hold_baby=True, **A_W)
        person(d, 325, g1 + 6, 182, phase=t + 1, face=1, **A_M)
        person(d, 900, g1, 168, phase=t + 2, face=-1, hold_baby=True, **B_W)
        person(d, 955, g1 + 6, 184, phase=t + 3, face=-1, **B_M)
        # 갈매기
        for i in range(3):
            bx = (t * 30 + i * 180) % (W + 200) - 100; by = 150 + i * 30 + 6 * math.sin(t * 2 + i)
            wv = 8 * math.sin(t * 6 + i)
            d.line([(bx - 14, by - wv), (bx, by), (bx + 14, by - wv)], fill=mix(INK, STEEL, .5), width=2)
    elif k == 3:  # 낮, 아이 둘이 물가를 달리고 부모는 지켜봄
        for i, (xx_, cfg, hh) in enumerate([(150, A_W, 170), (205, A_M, 182), (1080, B_W, 168), (1135, B_M, 184)]):
            person(d, xx_, g1 - 20, hh, phase=t + i, face=1 if xx_ < 640 else -1, **cfg)
        p = (t / 24)
        k1 = 360 + 520 * (0.5 - 0.5 * math.cos(p * 2 * math.pi * 1.5))
        k2 = k1 + 70 + 25 * math.sin(t * 1.3)
        kid(d, k1, g2, 100, PLAT, mix(ROSE, PLAT, .3), t * 9)
        kid(d, k2, g2 + 4, 92, DARKH, mix(STEEL, PLAT, .3), t * 9 + 1.5)
        # 연
        kx, ky = k2 + 160, 210 + 20 * math.sin(t * 1.1)
        d.line([(k2 + 18, g2 - 75), (kx, ky)], fill=mix(PLAT, STEEL, .4), width=1)
        d.polygon([(kx, ky - 24), (kx + 16, ky), (kx, ky + 24), (kx - 16, ky)], fill=EMBER)
        for j in range(4):
            d.ellipse([kx - 3 + j * 6 * math.sin(t * 3 + j), ky + 30 + j * 14, kx + 3 + j * 6 * math.sin(t * 3 + j), ky + 36 + j * 14], fill=ROSE)
    else:        # 노을, 여섯 식구가 나란히
        xs = [370, 430, 490, 790, 850, 910]
        cfgs = [A_M, None, A_W, B_W, None, B_M]
        for i, x in enumerate(xs):
            if cfgs[i] is None:
                kid(d, x, g1 + 4, 112, PLAT if i == 1 else DARKH, mix(ROSE, PLAT, .3) if i == 1 else mix(STEEL, PLAT, .3), t + i, running=False)
            else:
                person(d, x, g1, [182, 0, 170, 168, 0, 184][i], phase=t + i, face=1, skin_mul=1.15, **cfgs[i])
        d.line([(500, g1 - 70), (780, g1 - 70)], fill=mix(SKIN, EMBER, .2), width=0)
    return im, d

def overlay_text(im, k, t):
    d = ImageDraw.Draw(im, "RGBA")
    a = int(255 * min(ease((t - 1.0) / 1.2), ease((7.5 - t) / 1.2)))
    if a > 0:
        txt = SCENES[k]["title"]
        w = d.textlength(txt, font=F_TITLE)
        d.text(((W - w) / 2 + 1, 92), txt, font=F_TITLE, fill=(0, 0, 0, a // 2))
        d.text(((W - w) / 2, 90), txt, font=F_TITLE, fill=PLAT + (a,))
        sub = f"{k + 1} / 5"
        w2 = d.textlength(sub, font=F_SMALL)
        d.text(((W - w2) / 2, 145), sub, font=F_SMALL, fill=ROSE + (int(a * .8),))
    if k == 4 and t > 15:
        a2 = int(255 * ease((t - 15) / 2.5) * ease((23.6 - t) / 1.2))
        txt = "바다가 기억하는 가족"
        w = d.textlength(txt, font=F_END)
        d.text(((W - w) / 2, 250), txt, font=F_END, fill=PLAT + (a2,))

def finish(im, i):
    a = np.asarray(im).astype(np.float32)
    a = a * VIG + GRAIN[i % len(GRAIN)]
    # 시네마 레터박스
    a[:54] = 0; a[-54:] = 0
    return a.clip(0, 255).astype(np.uint8)

def render():
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-i", "audio.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
    XF = 1.5  # 장면 전환 겹침(초)
    for i in range(N):
        T = i / FPS
        k = min(int(T // SCENE_LEN), len(SCENES) - 1)
        t = T - k * SCENE_LEN
        im, _ = scene_frame(k, t)
        overlay_text(im, k, t)
        if t > SCENE_LEN - XF and k < len(SCENES) - 1:
            nxt, _ = scene_frame(k + 1, t - SCENE_LEN)
            im = Image.blend(im, nxt, ease((t - (SCENE_LEN - XF)) / XF))
        # 처음·끝 페이드
        fade = min(ease(T / 2.0), ease((DUR - T) / 2.5))
        if fade < 1:
            im = Image.blend(Image.new("RGB", (W, H)), im, fade)
        ff.stdin.write(finish(im, i).tobytes())
        if i % (FPS * 10) == 0:
            print(f"{T:.0f}s", flush=True)
    ff.stdin.close(); ff.wait()

def make_audio(path="audio.wav", sr=44100):
    n = sr * DUR; t = np.arange(n) / sr
    rng = np.random.default_rng(1)
    # 파도: 저역 통과한 잡음 + 6초 주기 밀물
    noise = rng.normal(0, 1, n)
    k = np.exp(-np.arange(400) / 60); k /= k.sum()
    surf = np.convolve(noise, k, mode="same")
    surf *= 0.35 + 0.65 * (0.5 + 0.5 * np.sin(2 * np.pi * t / 6)) ** 2
    # 잔잔한 화음 패드 (장면마다 화음 바뀜)
    chords = [[220, 277.2, 329.6], [196, 246.9, 293.7], [174.6, 220, 261.6], [196, 246.9, 329.6], [220, 277.2, 329.6, 440]]
    pad = np.zeros(n)
    seg = int(SCENE_LEN * sr)
    for ci, ch in enumerate(chords):
        s0, s1 = ci * seg, min(n, (ci + 1) * seg + sr * 2)
        tt = t[s0:s1] - t[s0]
        env = np.minimum(1, tt / 3) * np.minimum(1, (tt[-1] - tt) / 3 + 1e-9)
        for f in ch:
            pad[s0:s1] += env * np.sin(2 * np.pi * f * tt) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * tt + f))
    mixd = 0.55 * surf / np.abs(surf).max() + 0.18 * pad / len(chords[0])
    fade = np.minimum(1, t / 2) * np.minimum(1, (DUR - t) / 3)
    mixd = (mixd * fade / np.abs(mixd).max() * 0.8 * 32767).astype(np.int16)
    st = np.stack([mixd, np.roll(mixd, 300)], 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(st.tobytes())

if __name__ == "__main__":
    if "--still" in sys.argv:   # 장면별 미리보기 이미지
        for k in range(5):
            im, _ = scene_frame(k, 12); overlay_text(im, k, 4)
            Image.fromarray(finish(im, 0)).save(f"still_{k + 1}.png")
    else:
        make_audio(); render()
