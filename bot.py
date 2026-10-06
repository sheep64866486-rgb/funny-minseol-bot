import asyncio
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
import edge_tts

OUT = Path("output")
OUT.mkdir(exist_ok=True)

jokes = [
    "알람을 다섯 개 맞춘 이유? 다섯 번 무시하려고.",
    "통장 잔고는 3천 원인데 배달앱은 왜 켜져 있지?",
    "다이어트는 내일부터. 문제는 내일도 내일이라는 것.",
    "10분만 누워있으려고 했는데 눈 뜨니까 세 시간이 지났어.",
    "월급이 들어왔다. 그리고 카드값이 인사하러 왔다.",
]

text = random.choice(jokes)

async def make_voice():
    voice = edge_tts.Communicate(
        text=text,
        voice="ko-KR-HyunsuMultilingualNeural",
        rate="+10%"
    )
    await voice.save("voice.mp3")

def make_image():
    img = Image.new("RGB", (1080, 1920), "black")
    draw = ImageDraw.Draw(img)

    font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    font = ImageFont.truetype(font_path, 70)

    words = text.split()
    lines = []
    line = ""

    for word in words:
        test = (line + " " + word).strip()
        if len(test) > 13:
            if line:
                lines.append(line)
            line = word
        else:
            line = test

    if line:
        lines.append(line)

    final_text = "\n".join(lines)

    box = draw.multiline_textbbox(
        (0, 0),
        final_text,
        font=font,
        spacing=25,
        align="center"
    )

    w = box[2] - box[0]
    h = box[3] - box[1]

    draw.multiline_text(
        ((1080 - w) / 2, (1920 - h) / 2),
        final_text,
        font=font,
        fill="white",
        spacing=25,
        align="center"
    )

    img.save("background.png")

def make_video():
    subprocess.run([
        "ffmpeg",
        "-y",
        "-loop", "1",
        "-i", "background.png",
        "-i", "voice.mp3",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-vf", "scale=1080:1920",
        str(OUT / "funny_minseol.mp4")
    ], check=True)

asyncio.run(make_voice())
make_image()
make_video()

print("웃긴민설 영상 제작 완료")
