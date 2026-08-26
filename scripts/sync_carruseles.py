#!/usr/bin/env python3
"""
Sincroniza los carruseles generados por la tarea automática de NC Contabilidades
(carpeta carruseles/<YYYY-MM-DD>/carrusel-N-tema/) hacia la carpeta de
Contenido Carrusel/Carrusel (Contenido Carrusel/Carrusel/<Mes Año>/<día>/C<n>/),
sin duplicar ni pisar nada.

Seguro de correr las veces que sea: para cada carrusel del repo, revisa si su
contenido (por hash del primer archivo) ya existe en CUALQUIER subcarpeta del
día correspondiente. Si no lo encuentra, lo copia a la primera carpeta "Cn"
libre que no exista todavía (así no choca con fotos u otro contenido que
Nicole haya guardado a mano en esa misma carpeta del día).
"""
import hashlib
import re
import shutil
import subprocess
from pathlib import Path

REPO = Path("/Users/danny/Contabilidad NC")
CARRUSELES = REPO / "carruseles"
PUBLICACIONES = REPO / "Contenido Carrusel" / "Carrusel"
LOG = REPO / "scripts" / "sync_carruseles.log"

MESES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def file_hash(path):
    return hashlib.md5(path.read_bytes()).hexdigest()


def first_image(folder):
    imgs = sorted(folder.glob("*.png")) or sorted(folder.glob("*.jpeg")) or sorted(folder.glob("*.jpg"))
    return imgs[0] if imgs else None


def already_saved(day_folder, signature):
    if not day_folder.exists():
        return False
    for sub in day_folder.iterdir():
        if not sub.is_dir():
            continue
        img = first_image(sub)
        if img and file_hash(img) == signature:
            return True
    return False


def next_free_slot(day_folder):
    n = 1
    while (day_folder / f"C{n}").exists():
        n += 1
    return day_folder / f"C{n}"


def main():
    log(f"--- corrida {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()} ---")

    result = subprocess.run(
        ["git", "pull", "origin", "main", "--no-rebase", "--no-edit"],
        cwd=REPO, capture_output=True, text=True,
    )
    log("git pull: " + result.stdout.strip().replace("\n", " | ") + result.stderr.strip().replace("\n", " | "))

    if not CARRUSELES.exists():
        log("No existe carpeta carruseles/, nada que hacer.")
        return

    copiados = 0
    for date_folder in sorted(CARRUSELES.iterdir()):
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", date_folder.name)
        if not m or not date_folder.is_dir():
            continue
        anio, mes_num, dia = m.groups()
        mes_nombre = MESES[int(mes_num) - 1]
        day_folder = PUBLICACIONES / f"{mes_nombre} {anio}" / str(int(dia))

        for carrusel_folder in sorted(date_folder.iterdir(), key=lambda p: p.name):
            if not carrusel_folder.is_dir():
                continue
            img = first_image(carrusel_folder)
            if not img:
                continue
            signature = file_hash(img)

            if already_saved(day_folder, signature):
                continue

            dest = next_free_slot(day_folder)
            dest.mkdir(parents=True, exist_ok=True)
            for f in carrusel_folder.glob("*.png"):
                shutil.copy2(f, dest / f.name)
            copiados += 1
            log(f"Copiado: {carrusel_folder} -> {dest}")

    log(f"Listo. Carruseles nuevos copiados: {copiados}")


if __name__ == "__main__":
    main()
