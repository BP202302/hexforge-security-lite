from __future__ import annotations

import math
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / ".pydeps-video"))

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from moviepy import AudioFileClip, ImageSequenceClip


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "dist"
FRAMES = OUT / "frames"
W, H = 720, 1280
FPS = 20
DURATION = 32


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


F_TITLE = font(58, True)
F_BIG = font(74, True)
F_MED = font(42, True)
F_SMALL = font(28, False)
F_TINY = font(22, False)


SCENES = [
    (0, 4.8, "BERLIN", "A validator heartbeat under the city lights", "Solana Summit Germany 2026"),
    (4.8, 9.8, "THE ROOM", "builders, artists, institutions, first-timers", "one chain, many accents"),
    (9.8, 15.0, "THE SIGNAL", "ideas moved faster than slides", "payments, DePIN, agents, apps"),
    (15.0, 21.0, "THE MOMENT", "not a conference recap", "a proof that community can feel physical"),
    (21.0, 27.0, "THE TAKEAWAY", "crypto wins when it stops sounding distant", "and starts sounding local"),
    (27.0, 32.0, "SEE YOU ONCHAIN", "@SuperteamDE", "Berlin gave the network a pulse"),
]


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * max(0.0, min(1.0, t))


def text_center(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1]), text, font=fnt, fill=fill)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def scene_at(t: float):
    for start, end, *copy in SCENES:
        if start <= t < end:
            return start, end, copy
    return SCENES[-1][0], SCENES[-1][1], list(SCENES[-1][2:])


def draw_grid(draw: ImageDraw.ImageDraw, t: float):
    horizon = int(H * 0.53)
    vanishing = (W // 2 + int(math.sin(t * 0.7) * 35), horizon)
    for i in range(-8, 9):
        x = W // 2 + i * 72
        draw.line((x, H, *vanishing), fill=(53, 240, 196, 85), width=2)
    for n in range(24):
        y = int(lerp(H, horizon, (n / 24) ** 1.9))
        alpha = int(55 + n * 4)
        draw.line((0, y, W, y), fill=(255, 205, 87, alpha), width=2)


def draw_particles(draw: ImageDraw.ImageDraw, t: float):
    rng = np.random.default_rng(20260613)
    for i in range(105):
        base_x = rng.uniform(0, W)
        speed = rng.uniform(18, 80)
        y = (rng.uniform(-H, H) + t * speed) % H
        x = base_x + math.sin(t * rng.uniform(0.2, 1.3) + i) * 18
        r = rng.uniform(1.2, 3.8)
        col = (255, 255, 255, int(rng.uniform(35, 115)))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=col)


def draw_frame(idx: int):
    t = idx / FPS
    start, end, copy = scene_at(t)
    local = (t - start) / (end - start)
    title, subtitle, kicker = copy

    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    xx = np.linspace(0, 1, W, dtype=np.float32)[None, :]
    wave = np.sin(xx * 12 + t * 0.9) * 10
    teal = 22 + 42 * yy + 18 * np.sin(t + yy * 6)
    mag = 20 + 35 * (1 - yy)
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    arr[:, :, 0] = np.clip(12 + teal / 3 + wave, 0, 255)
    arr[:, :, 1] = np.clip(10 + mag / 4 + wave * 0.15, 0, 255)
    arr[:, :, 2] = np.clip(35 + teal + xx * 12, 0, 255)
    arr[:, :, 3] = 255
    bg = Image.fromarray(arr, "RGBA")

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow, "RGBA")
    pulse = 0.5 + 0.5 * math.sin(t * 2.1)
    gd.ellipse((-170, 80, 450, 700), fill=(42, 236, 198, int(36 + pulse * 35)))
    gd.ellipse((330, 210, 930, 880), fill=(255, 75, 126, int(32 + pulse * 28)))
    gd.ellipse((120, 730, 610, 1220), fill=(255, 202, 86, int(22 + pulse * 20)))
    bg = Image.alpha_composite(bg, glow.filter(ImageFilter.GaussianBlur(48)))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay, "RGBA")
    draw_grid(od, t)
    draw_particles(od, t)

    # Berlin signal tower / block skyline, deliberately abstract rather than stock footage.
    base_y = 655
    for i, x in enumerate(range(-40, W + 80, 72)):
        h = 80 + int(54 * math.sin(i * 1.7 + t * 0.4))
        od.rounded_rectangle((x, base_y - h, x + 46, base_y), radius=4, fill=(8, 7, 18, 210))
        for wy in range(base_y - h + 12, base_y - 8, 22):
            od.rectangle((x + 12, wy, x + 20, wy + 6), fill=(255, 207, 92, 125))
    od.line((W // 2, 190, W // 2, 660), fill=(244, 54, 93, 160), width=8)
    od.ellipse((W // 2 - 26, 170, W // 2 + 26, 222), outline=(244, 54, 93, 190), width=5)

    bg = Image.alpha_composite(bg, overlay)
    d = ImageDraw.Draw(bg, "RGBA")

    intro = min(1, local / 0.18)
    outro = min(1, (1 - local) / 0.15)
    alpha = int(255 * min(intro, outro))
    y_offset = int(lerp(70, 0, intro))

    d.rounded_rectangle((52, 82, W - 52, 168), radius=18, fill=(255, 255, 255, 24))
    d.text((76, 108), "SOLANA SUMMIT GERMANY", font=F_TINY, fill=(240, 255, 245, 190))
    d.text((76, 135), "13 JUNE 2026 / BERLIN", font=F_TINY, fill=(255, 219, 105, 210))

    text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    td = ImageDraw.Draw(text_layer, "RGBA")
    text_center(td, (W // 2, 330 + y_offset), title, F_BIG if len(title) < 11 else F_TITLE, (255, 255, 255, alpha))
    y = 442 + y_offset
    for line in wrap(td, subtitle, F_MED, W - 110):
        text_center(td, (W // 2, y), line, F_MED, (255, 233, 176, alpha))
        y += 52
    for line in wrap(td, kicker, F_SMALL, W - 120):
        text_center(td, (W // 2, y + 26), line, F_SMALL, (187, 255, 236, alpha))
        y += 37

    # Rhythmic data-caption at the bottom.
    bars = 24
    for i in range(bars):
        bh = int(12 + 46 * abs(math.sin(t * 2.8 + i * 0.65)))
        x = 70 + i * 24
        td.rounded_rectangle((x, H - 132 - bh, x + 9, H - 132), radius=5, fill=(53, 240, 196, int(alpha * 0.65)))
    td.text((70, H - 105), "community highlights / AI animation / original audio", font=F_TINY, fill=(255, 255, 255, int(alpha * 0.72)))
    td.text((70, H - 76), "submitted asset package: GitHub + social-ready caption", font=F_TINY, fill=(255, 255, 255, int(alpha * 0.58)))

    bg = Image.alpha_composite(bg, text_layer)
    return bg.convert("RGB")


def make_audio(path: Path):
    sr = 44100
    n = int(sr * DURATION)
    t = np.arange(n) / sr
    bpm = 112
    beat = 60 / bpm
    audio = np.zeros(n, dtype=np.float32)
    # Warm synth bed.
    for freq, amp in [(55, 0.16), (82.41, 0.08), (110, 0.045)]:
        audio += amp * np.sin(2 * np.pi * freq * t + 0.12 * np.sin(2 * np.pi * 0.17 * t))
    # Plucky arpeggio.
    notes = [220, 277.18, 329.63, 440, 554.37, 659.25, 554.37, 440]
    for i in range(int(DURATION / (beat / 2))):
        start = int(i * beat / 2 * sr)
        length = int(0.18 * sr)
        if start + length >= n:
            break
        env = np.exp(-np.linspace(0, 5.5, length))
        tone = np.sin(2 * np.pi * notes[i % len(notes)] * np.arange(length) / sr)
        audio[start:start + length] += 0.12 * env * tone
    # Kick and crisp click.
    for i in range(int(DURATION / beat) + 1):
        start = int(i * beat * sr)
        length = int(0.13 * sr)
        if start + length < n:
            tt = np.arange(length) / sr
            kick = np.sin(2 * np.pi * (115 - 70 * tt / tt[-1]) * tt) * np.exp(-tt * 28)
            audio[start:start + length] += 0.38 * kick
        click_start = start + int(0.5 * beat * sr)
        length = int(0.035 * sr)
        if click_start + length < n:
            noise = np.random.default_rng(i).normal(0, 1, length)
            audio[click_start:click_start + length] += 0.035 * noise * np.exp(-np.linspace(0, 5, length))
    audio *= 0.92 / max(0.92, float(np.max(np.abs(audio))))
    pcm = (audio * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)
        wav.writeframes(pcm.tobytes())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    FRAMES.mkdir(parents=True, exist_ok=True)
    frame_paths = []
    for idx in range(DURATION * FPS):
        p = FRAMES / f"frame_{idx:04d}.png"
        draw_frame(idx).save(p, quality=92)
        frame_paths.append(str(p))
    audio = OUT / "solana-summit-germany-original-audio.wav"
    make_audio(audio)
    clip = ImageSequenceClip(frame_paths, fps=FPS)
    clip = clip.with_audio(AudioFileClip(str(audio)))
    clip.write_videofile(
        str(OUT / "solana-summit-germany-berlin-signal.mp4"),
        codec="libx264",
        audio_codec="aac",
        fps=FPS,
        preset="medium",
        bitrate="4200k",
        threads=4,
    )
    draw_frame(36).save(OUT / "thumbnail.png", quality=95)


if __name__ == "__main__":
    main()
