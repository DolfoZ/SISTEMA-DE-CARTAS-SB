from PIL import Image
import sys, os

src = "TESON-MENDEZ.png"
dst = "icon.ico"

if not os.path.exists(src):
    print(f"No se encontro {src}, continuando sin icono.")
    sys.exit(0)

try:
    img = Image.open(src).convert("RGBA")
    sizes = [(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)]
    imgs  = [img.resize(s, Image.LANCZOS) for s in sizes]
    imgs[0].save(dst, format="ICO", sizes=sizes, append_images=imgs[1:])
    print(f"Icono generado: {dst}")
except Exception as e:
    print(f"Advertencia: {e}")
    sys.exit(0)
