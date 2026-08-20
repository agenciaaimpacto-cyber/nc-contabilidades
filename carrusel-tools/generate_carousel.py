#!/usr/bin/env python3
"""
Genera un carrusel de imagenes (1080x1350, estilo NC Contabilidades: fondo
azul marino oscuro, texto blanco/naranjo bold) a partir de un archivo JSON
de slides.

Uso:
  python3 generate_carousel.py slides.json output_dir/

Formato de slides.json:
{
  "slides": [
    {"type": "hook", "tag": "SABIAS QUE...", "text": "El **27%** de impuesto a las empresas podria bajar a **23%**"},
    {"type": "text", "lines": ["Es un proyecto de ley", "**aun en tramitacion.**"], "sub": "Todavia no es ley vigente."},
    {"type": "stat", "number": "20", "unit": "sept", "text": "es el plazo para declarar el **F29 de agosto** por Internet"},
    {"type": "proof", "tag": "SII", "text": "El plazo del F29 se traslada al **dia habil siguiente** si cae en fin de semana o feriado", "source": "Fuente: SII, Calendario Tributario"},
    {"type": "cta", "text": "Quieres tu contabilidad **al dia?**", "button": "Escribeme por WhatsApp ->", "sub": "Revisamos tu caso sin costo."}
  ]
}

Marcado: **palabra** = resaltado en naranjo. El resto va en blanco (o gris para
subtitulos). No uses tildes fuera de UTF-8 raro; el script soporta UTF-8 normal.
"""
import json
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
PAD = 90
BG = (11, 36, 64)          # navy-dark
ORANGE = (245, 130, 31)    # orange
WHITE = (250, 250, 248)    # paper
DIM = (200, 210, 222)
GRAY_LABEL = (142, 163, 189)
GRAY_SOURCE = (120, 142, 168)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(SCRIPT_DIR, "fonts")
BLACK_FONT_PATH = os.path.join(FONT_DIR, "ArchivoBlack-Regular.ttf")
VAR_FONT_PATH = os.path.join(FONT_DIR, "Archivo-Variable.ttf")

TOKEN_RE = re.compile(r"\*\*(.+?)\*\*|(\S+)")


def load_black(size):
    return ImageFont.truetype(BLACK_FONT_PATH, size)


def load_variable(size, weight=600, width=100):
    f = ImageFont.truetype(VAR_FONT_PATH, size)
    try:
        f.set_variation_by_axes([width, weight])
    except Exception:
        pass
    return f


def tokenize(text, base_color):
    """'hola **mundo** feliz' -> [('hola', base_color), ('mundo', ORANGE), ('feliz', base_color)]"""
    tokens = []
    for m in TOKEN_RE.finditer(text):
        if m.group(1) is not None:
            for w in m.group(1).split():
                tokens.append((w, ORANGE))
        else:
            tokens.append((m.group(2), base_color))
    return tokens


def wrap_and_draw(draw, xy, text, font, max_width, line_height, base_color,
                   align="left", center_x=None):
    tokens = tokenize(text, base_color)
    space_w = draw.textlength(" ", font=font)
    lines = []
    current, current_w = [], 0
    for word, color in tokens:
        w = draw.textlength(word, font=font)
        added = w if not current else space_w + w
        if current and current_w + added > max_width:
            lines.append(current)
            current, current_w = [], 0
            added = w
        current.append((word, color, w))
        current_w += added
    if current:
        lines.append(current)

    x0, y = xy
    for line in lines:
        line_w = sum(w for _, _, w in line) + space_w * (len(line) - 1)
        if align == "center":
            x = (center_x if center_x is not None else W / 2) - line_w / 2
        else:
            x = x0
        for word, color, w in line:
            draw.text((x, y), word, font=font, fill=color)
            x += w + space_w
        y += line_height
    return y


def brand_label(draw, side="right"):
    f = load_variable(24, weight=700)
    txt = "NC CONTABILIDADES"
    if side == "right":
        w = draw.textlength(txt, font=f)
        draw.text((W - PAD - w, 60), txt, font=f, fill=GRAY_LABEL)
    else:
        draw.text((PAD, 60), txt, font=f, fill=GRAY_LABEL)


def swipe_hint(draw):
    f = load_variable(24, weight=700)
    txt = "DESLIZA ->"
    w = draw.textlength(txt, font=f)
    draw.text((W - PAD - w, H - 90), txt, font=f, fill=GRAY_LABEL)


def new_canvas():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def render_hook(slide):
    img, d = new_canvas()
    brand_label(d)
    y = 300
    if slide.get("tag"):
        f = load_variable(28, weight=700)
        d.text((PAD, y), slide["tag"].upper(), font=f, fill=ORANGE)
        y += 70
    f = load_black(76)
    wrap_and_draw(d, (PAD, y), slide["text"], f, W - 2 * PAD, 92, WHITE)
    swipe_hint(d)
    return img


def render_text(slide):
    img, d = new_canvas()
    brand_label(d)
    y = 480
    f = load_black(62)
    for line in slide.get("lines", []):
        y = wrap_and_draw(d, (PAD, y), line, f, W - 2 * PAD, 76, WHITE)
        y += 6
    if slide.get("sub"):
        fs = load_variable(34, weight=500)
        wrap_and_draw(d, (PAD, y + 24), slide["sub"], fs, W - 2 * PAD, 46, DIM)
    swipe_hint(d)
    return img


def render_stat(slide):
    img, d = new_canvas()
    brand_label(d)
    fnum = load_black(220)
    y = 480
    d.text((PAD, y), slide["number"], font=fnum, fill=ORANGE)
    if slide.get("unit"):
        numw = d.textlength(slide["number"], font=fnum)
        funit = load_black(100)
        d.text((PAD + numw + 10, y + 100), slide["unit"], font=funit, fill=ORANGE)
    y += 280
    fs = load_variable(40, weight=700)
    wrap_and_draw(d, (PAD, y), slide["text"], fs, W - 2 * PAD, 52, WHITE)
    swipe_hint(d)
    return img


def render_proof(slide):
    img, d = new_canvas()
    brand_label(d)
    y = 300
    if slide.get("tag"):
        f = load_variable(28, weight=700)
        d.text((PAD, y), slide["tag"].upper(), font=f, fill=ORANGE)
        y += 70
    f = load_black(64)
    y = wrap_and_draw(d, (PAD, y), slide["text"], f, W - 2 * PAD, 80, WHITE)
    if slide.get("source"):
        fs = load_variable(20, weight=500)
        d.text((PAD, H - 90), slide["source"], font=fs, fill=GRAY_SOURCE)
    return img


def render_cta(slide):
    img, d = new_canvas()
    brand_label(d, side="left")
    f = load_black(58)
    y = wrap_and_draw(d, (PAD, 300), slide["text"], f, W - 2 * PAD, 74, WHITE,
                       align="center", center_x=W / 2)
    if slide.get("button"):
        fb = load_black(36)
        btn_text = slide["button"]
        tw = d.textlength(btn_text, font=fb)
        box_w, box_h = tw + 88, 100
        box_x = (W - box_w) / 2
        box_y = y + 60
        d.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h],
                             radius=10, fill=ORANGE)
        d.text((box_x + 44, box_y + 28), btn_text, font=fb, fill=BG)
        y = box_y + box_h + 40
    if slide.get("sub"):
        fs = load_variable(30, weight=500)
        wrap_and_draw(d, (PAD, y + 20), slide["sub"], fs, W - 2 * PAD, 40, DIM,
                       align="center", center_x=W / 2)
    return img


RENDERERS = {
    "hook": render_hook,
    "text": render_text,
    "stat": render_stat,
    "proof": render_proof,
    "cta": render_cta,
}


def main():
    if len(sys.argv) != 3:
        print("Uso: generate_carousel.py slides.json output_dir/")
        sys.exit(1)
    slides_path, out_dir = sys.argv[1], sys.argv[2]
    with open(slides_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    os.makedirs(out_dir, exist_ok=True)
    for i, slide in enumerate(data["slides"], start=1):
        renderer = RENDERERS.get(slide["type"])
        if not renderer:
            print(f"Tipo de slide desconocido: {slide['type']}")
            sys.exit(1)
        img = renderer(slide)
        out_path = os.path.join(out_dir, f"slide-{i}.png")
        img.save(out_path, "PNG")
        print(f"Guardado {out_path}")


if __name__ == "__main__":
    main()
