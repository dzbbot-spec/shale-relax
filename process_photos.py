"""
Обработка фото для мини-аппа Шале Релакс.
Делает: обрезка до 1200x800 (горизонтальные) или 800x1200 (вертикальные),
студийная цветокоррекция, сохранение в processed/
"""
import os
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

INPUT_DIRS = [
    "/Users/annakucenko/shale-relax/mini-app/public/photos/снаружи",
    "/Users/annakucenko/shale-relax/mini-app/public/photos/внутри",
]

OUTPUT_BASE = "/Users/annakucenko/shale-relax/mini-app/public/photos/processed"

TARGET_LANDSCAPE = (1200, 800)
TARGET_PORTRAIT = (800, 1200)
QUALITY = 88


def process_photo(input_path: Path, output_path: Path):
    img = Image.open(input_path)

    # Убираем EXIF-ориентацию
    try:
        from PIL import ImageOps
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass

    w, h = img.size
    is_landscape = w >= h
    target_w, target_h = TARGET_LANDSCAPE if is_landscape else TARGET_PORTRAIT

    # Умная обрезка — кроп по центру с сохранением соотношения
    target_ratio = target_w / target_h
    current_ratio = w / h

    if current_ratio > target_ratio:
        # Слишком широкое — режем по бокам
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        # Слишком высокое — режем сверху/снизу (чуть выше центра)
        new_h = int(w / target_ratio)
        top = int((h - new_h) * 0.4)
        img = img.crop((0, top, w, top + new_h))

    # Ресайз
    img = img.resize((target_w, target_h), Image.LANCZOS)

    # Студийная цветокоррекция
    # Яркость +15%
    img = ImageEnhance.Brightness(img).enhance(1.15)
    # Контраст +20%
    img = ImageEnhance.Contrast(img).enhance(1.20)
    # Насыщенность -10% (приглушить как на референсе)
    img = ImageEnhance.Color(img).enhance(0.90)
    # Резкость +15%
    img = ImageEnhance.Sharpness(img).enhance(1.15)

    # Сохраняем
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "JPEG", quality=QUALITY, optimize=True)
    print(f"  {'L' if is_landscape else 'P'} {input_path.name} → {target_w}x{target_h}")


def main():
    print("Обработка фото для Шале Релакс...\n")
    total = 0

    for input_dir in INPUT_DIRS:
        folder_name = Path(input_dir).name
        output_dir = Path(OUTPUT_BASE) / folder_name
        print(f"Папка: {folder_name}")

        for f in sorted(Path(input_dir).glob("*.jp*g")):
            if f.name.startswith("."):
                continue
            output_path = output_dir / f.name
            try:
                process_photo(f, output_path)
                total += 1
            except Exception as e:
                print(f"  ОШИБКА {f.name}: {e}")

        print()

    print(f"Готово! Обработано {total} фото.")
    print(f"Результат: {OUTPUT_BASE}")


if __name__ == "__main__":
    main()
