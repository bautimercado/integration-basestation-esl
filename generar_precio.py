from PIL import Image, ImageDraw, ImageFont
import base64
import json
import io

WIDTH = 384   # width de la etiqueta (propiedad width)
HEIGHT = 184  # height de la etiqueta (propiedad height)

# Rutas a las fuentes (ajustar según el host)
FONT_PATH_TITLE = "/mnt/c/Windows/Fonts/arial.ttf"
FONT_PATH_TEXT  = "/mnt/c/Windows/Fonts/arial.ttf"
FONT_PATH_PRICE = "/mnt/c/Windows/Fonts/arialbd.ttf"

# 1) Crear imagen base
img = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 255))
draw = ImageDraw.Draw(img)

# 2) Fuentes
try:
    font_title = ImageFont.truetype(FONT_PATH_TITLE, 36)
    font_text  = ImageFont.truetype(FONT_PATH_TEXT, 26)
    font_price = ImageFont.truetype(FONT_PATH_PRICE, 40)
except:
    font_title = ImageFont.load_default()
    font_text = ImageFont.load_default()
    font_price = ImageFont.load_default()

# 3) Dibujar contenido (usá solo blanco / negro / rojo puro)
draw.text((10, 10), "Capitan del Espacio", fill=(0, 0, 0, 255), font=font_title)
draw.text((10, 60), "30cm",            fill=(0, 0, 0, 255), font=font_text)
draw.text((10, 100), "OFERTA",         fill=(0, 0, 0, 255), font=font_text)

# Caja de precio bien roja
draw.rectangle([(170, 90), (370, 150)], fill=(255, 0, 0, 255))
draw.text((180, 100), "$18500", fill=(255, 255, 255, 255), font=font_price)

# 4) Asegurar formato RGBA
img = img.convert("RGBA")
img = img.rotate(90, expand=True)

# 5) Obtener buffer ARGB crudo (sin cabecera)
#rgba = img.tobytes()  # R, G, B, A por pixel
#argb_bytes = bytearray()

buf = io.BytesIO()
img.save(buf, format="PNG")
rgba_bytes = buf.getvalue()

#for i in range(0, len(rgba), 4):
#    r, g, b, a = rgba[i:i+4]
#    argb_bytes += bytes([a, r, g, b])  # A, R, G, B

# Sanity check: tamaño exacto WIDTH * HEIGHT * 4
#expected = WIDTH * HEIGHT * 4
#print("len(argb_bytes) =", len(argb_bytes), "expected =", expected)

# 6) Base64 de los bytes crudos
b64_data = base64.b64encode(rgba_bytes).decode("utf-8")

with open("preview.b64.txt", "w") as f:
    f.write(b64_data)

# 7) Armar comando MQTT
mqtt_command = {
    "queueId": 1008,
    "deviceType": 1,
    "deviceMac": "0012383B268CE5B0",
    # Mejor usar la versión real que reportó la etiqueta:
    "deviceVersion": "4.3.15",
    "refreshAction": 3,
    "refreshArea": 1,
    "content": [
        {
            "dataType": 3,
            "dataRef": b64_data
        }
    ]
}

with open("mqtt_command.json", "w") as f:
    json.dump(mqtt_command, f, indent=2)

print("mqtt_command.json generado.")
