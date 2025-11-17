from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile
from io import BytesIO
import random
import os
from django.conf import settings

def gerar_avatar_inicial(letra):
    letra = letra.upper()

    cor = random.choice(["#4a90e2", "#50e3c2", "#e94e77", "#f5a623", "#7ed321"])

    img = Image.new("RGB", (300, 300), cor)
    draw = ImageDraw.Draw(img)

    # Caminho da fonte
    font_path = os.path.join(
        settings.BASE_DIR,
        "BibliotecaEstrela",
        "static",
        "fonts",
        "Roboto-Bold.ttf"
    )

    font = ImageFont.truetype(font_path, 150)

    # --- CENTRALIZAÇÃO PERFEITA ---
    bbox = draw.textbbox((0, 0), letra, font=font)

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (300 - text_width) / 2
    y = (235 - text_height) / 2  # Calculo real da altura

    draw.text((x, y), letra, fill="white", font=font)

    # Converter para arquivo
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    file_png = ContentFile(buffer.getvalue())

    return file_png
