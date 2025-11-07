from PIL import Image, ImageDraw, ImageFont
import base64
import json

# Configuracion del ESl
# TODO: Ajustar esto a la resolucion y tamaño del ESl real en un .env
WIDTH = 384
HEIGHT = 184
ESL_MAC = "0012383B268CE5B0"

PRODUCTO_NOMBRE = "Colgante Murano"
PRODUCTO_TAMANIO = "30cm"
PRODUCTO_PRECIO = 17500

# Preparacion de la imagen
# Crear una imagen con fondo blanco 
img = Image.new('RGBA', (WIDTH, HEIGHT), color='white')
d = ImageDraw.Draw(img)

# Se puede ajustar el path o usar fuentes personalizadas
font_bold = ImageFont.load_default().font_variant(size=24)       # Nombre
font_regular = ImageFont.load_default().font_variant(size=18)    # Tamaño y oferta
font_price = ImageFont.load_default().font_variant(size=28)      # Precio

# Dibujar elementos

# 1. Nombre del producto
# TODO: Ajustar las coordenadas segun el diseño del ESl
d.text((10, 5), PRODUCTO_NOMBRE, fill=(0, 0, 0, 255), font=font_bold)

# 2. Tamaño (negro)
# TODO: Ajustar las coordenadas (x, y)
d.text((10, 40), PRODUCTO_TAMANIO, fill=(0, 0, 0, 255), font=font_regular)

# 3. Texto "OFERTA" (negro)
# TODO: Ajustar las coordenadas (x, y)
d.text((10, 75), "OFERTA", fill=(0, 0, 0, 255), font=font_regular)

# 4. Recuadro rojo para el precio
# Coordenadas (x1, y1, x2, y2) para el rectángulo.
# TODO: Ajusta estas coordenadas para el tamaño y posición del recuadro rojo
red_box_coords = (WIDTH - 120, HEIGHT - 50, WIDTH - 10, HEIGHT - 10) # Ejemplo
d.rectangle(red_box_coords, fill=(255, 0, 0, 255)) # Rojo opaco

# 5. Precio dentro del recuadro (blanco)
price_text = f"${PRODUCTO_PRECIO:,}".replace(",", ".") # Formateo con separador de miles

# --- Corrección: d.textsize() está obsoleto. Usar d.textbbox() ---
# Obtenemos el bounding box del texto (x1, y1, x2, y2)
# Usamos (0,0) como ancla de referencia para el cálculo
try:
    # Versión moderna de Pillow
    bbox = d.textbbox((0, 0), price_text, font=font_price)
    text_width = bbox[2] - bbox[0]  # right - left
    text_height = bbox[3] - bbox[1] # bottom - top
    # Ajustes basados en el offset del bounding box
    x_offset = bbox[0]
    y_offset = bbox[1]
except AttributeError:
    # Versión antigua de Pillow (por si acaso)
    text_width, text_height = d.textsize(price_text, font=font_price)
    x_offset = 0
    y_offset = 0

# Centrar el texto en el recuadro rojo
box_width = red_box_coords[2] - red_box_coords[0]
box_height = red_box_coords[3] - red_box_coords[1]

# Calculamos el (x, y) de la esquina superior izquierda del texto
text_x = red_box_coords[0] + (box_width - text_width) / 2
text_y = red_box_coords[1] + (box_height - text_height) / 2

# Ajustamos la posición x/y basada en el offset (left, top) del bounding box
# Esto es necesario porque textbbox() no siempre empieza en (0,0)
text_x = text_x - x_offset
text_y = text_y - y_offset

d.text((text_x, text_y), price_text, fill=(255, 255, 255, 255), font=font_price)

# Convertir la imagen a ARGB 32bit y despues a base64
# La antena espera ARGB. Pillow trabaja en RGBA, pero la conversion final lo maneja bien
# Se puede probar a guardar como BMP si el PNG da problemas, pero PNG es mas comun para Base64

from io import BytesIO
img_bytes_io = BytesIO()
img.save(img_bytes_io, format='PNG')   # Probar con 'BMP' si hay problemas
img_bytes = img_bytes_io.getvalue()

base64_str = base64.b64encode(img_bytes).decode('utf-8')

# Preparar el comando MQTT JSON
mqtt_command = {
  "queueId": 1002, # Un nuevo ID para esta operación
  "deviceType": 1,
  "deviceMac": ESL_MAC,
  "deviceVersion": "4.2.E", # Dejar este valor, si falla probar con otro
  "refreshAction": 3,
  "refreshArea": 1,
  "content": [
    {
      "dataType": 3,
      "dataRef": base64_str
    }
  ]
}

with open("refresco_precio.json", "w") as f:
    json.dump(mqtt_command, f, indent=2)

print(f"JSON del comando guardado en refresco_precio.json para MAC: {ESL_MAC}")
print("¡Ahora puedes publicarlo con mosquitto_pub!")

# Guarda la imagen generada para ver cómo se ve
img.save("precio_generado.png")
print("Imagen generada (precio_generado.png) guardada para revisión visual.")