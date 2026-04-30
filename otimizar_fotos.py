"""Otimiza as fotos usadas no site (gera WebP 1600/800 + JPG fallback).

Move os originais para fotos/originais/ e sobrescreve fotos/ com versões leves.
Roda uma vez: `python otimizar_fotos.py`
"""
from pathlib import Path
import shutil
import sys

from PIL import Image, ImageOps

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RAIZ = Path(__file__).parent
FOTOS = RAIZ / "fotos"
BACKUP = FOTOS / "originais"

# (arquivo_original, gerar_jpg_fallback)
ALVOS = [
    ("IMG_6078.jpg", True),
    ("IMG_6082.jpg", True),
    ("IMG_6095.jpg", True),
    ("IMG_6083.jpg", True),
    ("IMG_6120.jpg", True),
    ("IMG_6094.jpg", True),   # og:image
    ("fotocomcatarina.png", True),
    ("fotodentista.png", True),
]

LARGURA_GRANDE = 1600
LARGURA_PEQUENA = 800
QUALIDADE = 82


def humano(n_bytes: int) -> str:
    for unidade in ("B", "KB", "MB", "GB"):
        if n_bytes < 1024:
            return f"{n_bytes:.1f} {unidade}"
        n_bytes /= 1024
    return f"{n_bytes:.1f} TB"


def redimensionar(img: Image.Image, largura: int) -> Image.Image:
    if img.width <= largura:
        return img.copy()
    nova_altura = round(img.height * largura / img.width)
    return img.resize((largura, nova_altura), Image.LANCZOS)


def processar(nome: str, gerar_jpg: bool) -> tuple[int, int, tuple[int, int]]:
    caminho_backup = BACKUP / nome
    if not caminho_backup.exists():
        raise FileNotFoundError(f"Backup não encontrado: {caminho_backup}")

    tamanho_original = caminho_backup.stat().st_size

    img = Image.open(caminho_backup)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    if img.mode == "RGBA":
        fundo = Image.new("RGB", img.size, (255, 255, 255))
        fundo.paste(img, mask=img.split()[-1])
        img = fundo

    stem = Path(nome).stem
    dimensoes_grande = None
    tamanho_total = 0

    # WebP 1600
    grande = redimensionar(img, LARGURA_GRANDE)
    dimensoes_grande = grande.size
    saida_webp = FOTOS / f"{stem}.webp"
    grande.save(saida_webp, "WEBP", quality=QUALIDADE, method=6)
    tamanho_total += saida_webp.stat().st_size

    # WebP 800
    pequena = redimensionar(img, LARGURA_PEQUENA)
    saida_webp_p = FOTOS / f"{stem}-800.webp"
    pequena.save(saida_webp_p, "WEBP", quality=QUALIDADE, method=6)
    tamanho_total += saida_webp_p.stat().st_size

    # JPG fallback
    if gerar_jpg:
        saida_jpg = FOTOS / f"{stem}.jpg"
        grande.save(saida_jpg, "JPEG", quality=QUALIDADE, optimize=True, progressive=True)
        tamanho_total += saida_jpg.stat().st_size

    # Se origem era PNG, remove o PNG da pasta fotos/ (ele só existe no backup)
    png_orig = FOTOS / nome
    if png_orig.suffix.lower() == ".png" and png_orig.exists():
        png_orig.unlink()

    return tamanho_original, tamanho_total, dimensoes_grande


def main() -> int:
    if not FOTOS.exists():
        print(f"Pasta não encontrada: {FOTOS}", file=sys.stderr)
        return 1

    BACKUP.mkdir(exist_ok=True)

    # Move originais para backup (todos os arquivos da pasta, exceto a própria pasta originais)
    print("→ Fazendo backup dos originais...")
    movidos = 0
    for arquivo in FOTOS.iterdir():
        if arquivo.is_dir():
            continue
        destino = BACKUP / arquivo.name
        if not destino.exists():
            shutil.move(str(arquivo), str(destino))
            movidos += 1
    print(f"  {movidos} arquivo(s) movido(s) para {BACKUP.relative_to(RAIZ)}")

    print("\n→ Processando imagens usadas no site...\n")
    total_antes = 0
    total_depois = 0
    print(f"{'Arquivo':<28} {'Antes':>10}  →  {'Depois':>10}   {'Redução':>8}   {'Dimensões':>14}")
    print("-" * 90)
    for nome, gerar_jpg in ALVOS:
        try:
            antes, depois, dims = processar(nome, gerar_jpg)
        except FileNotFoundError as e:
            print(f"  AVISO: {e}")
            continue
        total_antes += antes
        total_depois += depois
        reducao = (1 - depois / antes) * 100 if antes else 0
        print(f"{nome:<28} {humano(antes):>10}  →  {humano(depois):>10}   {reducao:>6.1f}%   {dims[0]}x{dims[1]:>4}")

    print("-" * 90)
    if total_antes:
        reducao_total = (1 - total_depois / total_antes) * 100
        print(f"{'TOTAL':<28} {humano(total_antes):>10}  →  {humano(total_depois):>10}   {reducao_total:>6.1f}%")

    print("\n✓ Pronto. Originais preservados em fotos/originais/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
