import os
import sys
from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

# ==========================================
# 1. CONFIGURACIÓN DE FONT FALLBACK EN MAC
# ==========================================
def get_font(size, bold=False):
    """
    Retorna una fuente TrueType instalada en macOS.
    Si no encuentra la fuente, retorna la fuente por defecto.
    """
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Courier New Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/System/Library/Fonts/Helvetica.dfont",
        "/Library/Fonts/Arial.ttf",
        "/Library/Fonts/Microsoft/Arial.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

# ==========================================
# 2. GENERACIÓN DE LA IMAGEN DEL STAGE PLOT
# ==========================================
def generate_stage_plot_image():
    # Dimensiones del lienzo (alta resolución para impresión)
    width, height = 2400, 1500
    img = Image.new("RGBA", (width, height), (18, 18, 20, 255)) # Zinc 900
    draw = ImageDraw.Draw(img)

    # Fuentes
    font_title = get_font(52, bold=True)
    font_subtitle = get_font(30, bold=False)
    font_section = get_font(28, bold=True)
    font_label_lg = get_font(22, bold=True)
    font_label_sm = get_font(18, bold=False)
    font_badge = get_font(20, bold=True)

    # ------------------------------------------
    # A. DIBUJAR PISO DEL ESCENARIO (PERSPECTIVA 3D)
    # ------------------------------------------
    # Líneas de perspectiva (verticales que convergen al fondo)
    stage_top_y = 180
    stage_bottom_y = 1420
    
    # Dibujar rejilla sutil
    for i in range(0, 13):
        # Punto inicial en el fondo, punto final al frente
        x_top = 400 + i * (1600 / 12)
        x_bottom = 100 + i * (2200 / 12)
        draw.line([(x_top, stage_top_y), (x_bottom, stage_bottom_y)], fill=(38, 38, 42, 100), width=2) # Zinc 800

    # Líneas de rejilla horizontales (separadas por perspectiva)
    h_lines = [180, 280, 410, 570, 770, 1020, 1320, 1420]
    for y in h_lines:
        # Calcular los bordes izquierdo y derecho del escenario en esta altura Y
        ratio = (y - stage_top_y) / (stage_bottom_y - stage_top_y)
        x_left = 400 - ratio * 300
        x_right = 2000 + ratio * 200
        draw.line([(x_left, y), (x_right, y)], fill=(38, 38, 42, 100), width=2)

    # Bordes físicos del escenario con brillo dorado LED
    # Borde de fondo (Upstage)
    draw.line([(400, stage_top_y), (2000, stage_top_y)], fill=(82, 82, 91, 255), width=4)
    # Borde lateral izquierdo (Stage Right / Público Izquierda)
    draw.line([(400, stage_top_y), (100, stage_bottom_y)], fill=(82, 82, 91, 255), width=4)
    # Borde lateral derecho (Stage Left / Público Derecha)
    draw.line([(2000, stage_top_y), (2300, stage_bottom_y)], fill=(82, 82, 91, 255), width=4)
    # Borde frontal (Downstage) - Línea LED de color dorado elegante
    draw.line([(100, stage_bottom_y), (2300, stage_bottom_y)], fill=(212, 175, 55, 255), width=6) # Oro

    # ------------------------------------------
    # B. DIBUJAR ETIQUETAS DE ORIENTACIÓN
    # ------------------------------------------
    # Público / Downstage
    draw.text((width // 2, 1460), "PÚBLICO / FRENTE DEL ESCENARIO (DOWNSTAGE)", fill=(212, 175, 55, 255), font=font_section, anchor="mm")
    # Fondo / Upstage
    draw.text((width // 2, 140), "FONDO DEL ESCENARIO (UPSTAGE)", fill=(161, 161, 170, 255), font=font_subtitle, anchor="mm")
    # Lado Izquierdo (Stage Right - para los músicos, derecha del público)
    draw.text((150, 160), "STAGE RIGHT\n(DERECHA ESCENARIO / IZQ. PÚBLICO)", fill=(161, 161, 170, 200), font=font_label_sm, anchor="lm")
    # Lado Derecho (Stage Left - para los músicos, izquierda del público)
    draw.text((2250, 160), "STAGE LEFT\n(IZQUIERDA ESCENARIO / DER. PÚBLICO)", fill=(161, 161, 170, 200), font=font_label_sm, anchor="rm")

    # Título principal en el escenario
    draw.text((width // 2, 60), "STAGE PLOT - PLANO DE DISTRIBUCIÓN DE ESCENARIO", fill=(255, 255, 255, 255), font=font_title, anchor="mm")
    draw.text((width // 2, 105), "CEREMONIA DE CLAUSURA CIEDI 2026", fill=(212, 175, 55, 255), font=font_subtitle, anchor="mm")

    # ------------------------------------------
    # C. FUNCIONES AUXILIARES PARA DIBUJAR ICONOS
    # ------------------------------------------
    
    def draw_badge(cx, cy, number, color=(245, 158, 11)):
        """Dibuja un círculo numérico para indicar el canal técnico."""
        r = 25
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(24, 24, 27, 255), outline=color, width=3)
        draw.text((cx, cy), str(number), fill=(255, 255, 255, 255), font=font_badge, anchor="mm")

    def draw_monitor(cx, cy, number, name):
        """Dibuja una cuña de monitoreo de piso."""
        # Altavoz trapezoidal de perfil
        points = [
            (cx - 70, cy + 35), # Abajo Izquierda
            (cx + 70, cy + 35), # Abajo Derecha
            (cx + 45, cy - 25), # Arriba Derecha
            (cx - 45, cy - 25)  # Arriba Izquierda
        ]
        draw.polygon(points, fill=(39, 39, 42, 255), outline=(113, 113, 122, 255), width=2)
        # Rejilla acústica (trapezoide interno)
        grille_points = [
            (cx - 60, cy + 25),
            (cx + 60, cy + 25),
            (cx + 38, cy - 18),
            (cx - 38, cy - 18)
        ]
        draw.polygon(grille_points, fill=(24, 24, 27, 255))
        # Bocina / Círculo interno
        draw.ellipse([(cx - 20, cy - 10), (cx + 20, cy + 20)], fill=(39, 39, 42, 255), outline=(63, 63, 70, 255), width=2)
        # Identificador del monitor (Círculo verde/azul brillante)
        draw_badge(cx, cy - 25, number, color=(16, 185, 129)) # Verde esmeralda para envíos
        # Nombre del monitor
        draw.text((cx, cy + 55), f"MONITOR {number}", fill=(255, 255, 255, 255), font=font_label_lg, anchor="mm")
        draw.text((cx, cy + 78), name, fill=(161, 161, 170, 255), font=font_label_sm, anchor="mm")

    def draw_mic_stand(cx, cy, number, is_wireless=False, name=""):
        """Dibuja un soporte de micrófono con indicador de canal."""
        # Base de micrófono (círculo exterior)
        r_base = 35
        base_color = (245, 158, 11, 255) if is_wireless else (14, 165, 233, 255) # Naranja/Oro para inalámbrico, Azul para cableado
        draw.ellipse([(cx - r_base, cy - r_base), (cx + r_base, cy + r_base)], fill=(39, 39, 42, 180), outline=base_color, width=3)
        
        # Icono de base de micrófono (tija y pinza simplificada)
        draw.line([(cx - 15, cy + 15), (cx + 15, cy - 15)], fill=(113, 113, 122, 255), width=3)
        draw.ellipse([(cx - 10, cy - 22), (cx + 10, cy - 6)], fill=(24, 24, 27, 255), outline=(161, 161, 170, 255), width=2)
        
        # Canal / Badge
        draw_badge(cx + 25, cy - 25, number, color=base_color)
        
        # Nombre del cantante / tipo
        label = f"Voz {number - 0}" # El número de voz coincide con el canal 1-10
        draw.text((cx, cy + 55), label, fill=(255, 255, 255, 255), font=font_label_lg, anchor="mm")
        type_str = "Inalámbrico" if is_wireless else "Cableado"
        draw.text((cx, cy + 75), type_str, fill=(161, 161, 170, 255), font=font_label_sm, anchor="mm")

    def draw_keyboard(cx, cy, number, name):
        """Dibuja un teclado de 61/88 teclas de forma estilizada."""
        # Chasis del teclado
        kw, kh = 180, 70
        draw.rounded_rectangle([(cx - kw//2, cy - kh//2), (cx + kw//2, cy + kh//2)], radius=8, fill=(30, 27, 75, 255), outline=(99, 102, 241, 255), width=3) # Indigo
        # Área de teclas (blanca)
        draw.rectangle([(cx - kw//2 + 8, cy + 10), (cx + kw//2 - 8, cy + kh//2 - 6)], fill=(255, 255, 255, 255))
        # Dibujar líneas de teclas negras
        key_x_start = cx - kw//2 + 14
        key_x_end = cx + kw//2 - 14
        step = (key_x_end - key_x_start) / 18
        for i in range(19):
            x = key_x_start + i * step
            # Línea de tecla blanca (delgada)
            draw.line([(x, cy + 10), (x, cy + kh//2 - 6)], fill=(200, 200, 200, 255), width=1)
            # Tecla negra (no en todas las posiciones)
            if i % 7 not in [2, 6] and i < 18:
                draw.rectangle([(x + step*0.6, cy + 10), (x + step*1.4, cy + 24)], fill=(0, 0, 0, 255))
                
        # Badge de canal
        draw_badge(cx + kw//2 - 10, cy - kh//2, number, color=(99, 102, 241))
        
        # Etiqueta
        draw.text((cx, cy - 55), name, fill=(255, 255, 255, 255), font=font_label_lg, anchor="mm")

    def draw_amplifier(cx, cy, label, color=(161, 161, 170)):
        """Dibuja un cabezal/amplificador de guitarra/bajo en el escenario."""
        aw, ah = 100, 60
        draw.rounded_rectangle([(cx - aw//2, cy - ah//2), (cx + aw//2, cy + ah//2)], radius=6, fill=(24, 24, 27, 255), outline=color, width=3)
        # Rejilla del parlante
        draw.rectangle([(cx - aw//2 + 8, cy - ah//2 + 8), (cx + aw//2 - 8, cy + ah//2 - 8)], fill=(39, 39, 42, 255))
        # Pequeño logo/texto AMP
        draw.text((cx, cy), label, fill=(161, 161, 170, 255), font=font_label_sm, anchor="mm")

    def draw_guitar(cx, cy, number, name, is_bass=False, is_extra=False):
        """Dibuja una guitarra/bajo y su amplificador/DI."""
        # Dibujar silueta estilizada de guitarra
        # Cuerpo
        draw.ellipse([(cx - 30, cy + 10), (cx + 30, cy + 50)], fill=(120, 53, 4, 255) if not is_bass else (153, 27, 27, 255), outline=(255, 255, 255, 100), width=1) # Madera o Rojo
        # Mástil
        draw.rectangle([(cx - 6, cy - 50), (cx + 6, cy + 10)], fill=(78, 53, 36, 255))
        # Pala (Clavijero)
        draw.ellipse([(cx - 10, cy - 60), (cx + 10, cy - 48)], fill=(120, 53, 4, 255) if not is_bass else (153, 27, 27, 255))
        
        # Si no es extra, lleva badge de canal técnico
        if not is_extra:
            draw_badge(cx + 35, cy - 35, number, color=(244, 63, 94) if not is_bass else (239, 68, 68)) # Color Coral/Rojo
            # Dibujar su amplificador justo detrás
            draw_amplifier(cx, cy - 90, "AMP" if not is_bass else "BASS AMP", color=(244, 63, 94) if not is_bass else (239, 68, 68))
        else:
            # Amplificador local Line 6 para las guitarras extra
            draw_amplifier(cx, cy - 90, "LINE 6", color=(113, 113, 122))
            
        # Etiquetas
        draw.text((cx, cy + 68), name, fill=(255, 255, 255, 255), font=font_label_lg, anchor="mm")
        if is_extra:
            draw.text((cx, cy + 90), "(Sin Consola)", fill=(161, 161, 170, 255), font=font_label_sm, anchor="mm")
        elif number == 29:
            draw.text((cx, cy + 90), "(Direct Box - DI)", fill=(161, 161, 170, 255), font=font_label_sm, anchor="mm")
        else:
            draw.text((cx, cy + 90), "(Línea + Mic PA)", fill=(161, 161, 170, 255), font=font_label_sm, anchor="mm")

    def draw_brass(cx, cy, number, name, is_trumpet=True):
        """Dibuja un instrumento de viento metal o madera (Trompeta / Saxo)."""
        # Círculo del músico
        r = 45
        draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(39, 39, 42, 255), outline=(234, 179, 8, 255), width=3) # Amarillo/Oro
        
        # Representación geométrica del viento
        if is_trumpet:
            # Trompeta: tubo horizontal largo y campana triangular a la izquierda
            draw.line([(cx - 25, cy - 5), (cx + 25, cy - 5)], fill=(234, 179, 8, 255), width=4)
            draw.line([(cx - 25, cy + 5), (cx + 25, cy + 5)], fill=(234, 179, 8, 255), width=4)
            draw.polygon([(cx - 25, cy - 15), (cx - 25, cy + 15), (cx - 40, cy)], fill=(234, 179, 8, 255))
        else:
            # Saxofón: tubo en forma de J o gancho dorado
            draw.arc([(cx - 25, cy), (cx + 5, cy + 30)], 0, 180, fill=(234, 179, 8, 255), width=6)
            draw.line([(cx + 5, cy - 25), (cx + 5, cy + 15)], fill=(234, 179, 8, 255), width=6)
            draw.polygon([(cx - 25, cy - 5), (cx - 38, cy + 10), (cx - 20, cy + 15)], fill=(234, 179, 8, 255))

        # Badge del canal
        draw_badge(cx + 35, cy - 35, number, color=(234, 179, 8))
        
        # Etiqueta
        draw.text((cx, cy + 65), name, fill=(255, 255, 255, 255), font=font_label_lg, anchor="mm")
        draw.text((cx, cy + 85), "Soporte Piso", fill=(161, 161, 170, 255), font=font_label_sm, anchor="mm")

    def draw_congas(cx, cy, number, name):
        """Dibuja un set de Congas (par de congas)."""
        # Dos tambores de conga (óvalos con perspectiva)
        # Conga 1 (Izquierda)
        draw.ellipse([(cx - 45, cy - 15), (cx - 5, cy + 45)], fill=(120, 53, 4, 255), outline=(161, 161, 170, 255), width=2)
        draw.ellipse([(cx - 40, cy - 12), (cx - 10, cy + 12)], fill=(254, 243, 199, 255)) # Parche color beige
        # Conga 2 (Derecha)
        draw.ellipse([(cx + 5, cy - 15), (cx + 45, cy + 45)], fill=(120, 53, 4, 255), outline=(161, 161, 170, 255), width=2)
        draw.ellipse([(cx + 10, cy - 12), (cx + 40, cy + 12)], fill=(254, 243, 199, 255)) # Parche color beige
        
        # Trípode soporte
        draw.line([(cx, cy + 15), (cx - 25, cy + 65)], fill=(113, 113, 122, 255), width=3)
        draw.line([(cx, cy + 15), (cx + 25, cy + 65)], fill=(113, 113, 122, 255), width=3)
        draw.line([(cx, cy + 15), (cx, cy + 75)], fill=(113, 113, 122, 255), width=3)

        # Badge
        draw_badge(cx + 50, cy - 30, number, color=(245, 158, 11))
        
        # Etiquetas
        draw.text((cx, cy + 95), name, fill=(255, 255, 255, 255), font=font_label_lg, anchor="mm")

    def draw_drums(cx, cy):
        """Dibuja un set de batería acústica completo con sus micrófonos."""
        # Área de batería (círculo de piso delimitador)
        draw.ellipse([(cx - 160, cy - 160), (cx + 160, cy + 160)], outline=(6, 182, 212, 100), width=2) # Círculo sutil cian
        
        # 1. Bombo (Kick - Canal 15)
        draw.ellipse([(cx - 50, cy - 50), (cx + 50, cy + 50)], fill=(24, 24, 27, 255), outline=(6, 182, 212, 255), width=4)
        draw_badge(cx, cy, 15, color=(6, 182, 212))
        draw.text((cx, cy + 65), "Bombo", fill=(255, 255, 255, 255), font=font_label_sm, anchor="mm")
        
        # 2. Caja (Snare - Canal 16)
        draw.ellipse([(cx - 105, cy + 15), (cx - 55, cy + 65)], fill=(39, 39, 42, 255), outline=(6, 182, 212, 255), width=2)
        draw_badge(cx - 80, cy + 40, 16, color=(6, 182, 212))
        draw.text((cx - 80, cy + 78), "Caja", fill=(255, 255, 255, 255), font=font_label_sm, anchor="mm")

        # 3. Hi-Hat (Canal 17)
        draw.ellipse([(cx - 145, cy - 25), (cx - 105, cy + 15)], fill=(234, 179, 8, 255), outline=(255, 255, 255, 150), width=1)
        draw_badge(cx - 125, cy - 5, 17, color=(6, 182, 212))
        draw.text((cx - 125, cy + 28), "Hi-Hat", fill=(255, 255, 255, 255), font=font_label_sm, anchor="mm")

        # 4. Tom 1 (Canal 18)
        draw.ellipse([(cx - 70, cy - 85), (cx - 20, cy - 35)], fill=(39, 39, 42, 255), outline=(6, 182, 212, 255), width=2)
        draw_badge(cx - 45, cy - 60, 18, color=(6, 182, 212))
        draw.text((cx - 45, cy - 100), "Tom 1", fill=(255, 255, 255, 255), font=font_label_sm, anchor="mm")

        # 5. Tom 2 (Canal 19)
        draw.ellipse([(cx + 20, cy - 85), (cx + 70, cy - 35)], fill=(39, 39, 42, 255), outline=(6, 182, 212, 255), width=2)
        draw_badge(cx + 45, cy - 60, 19, color=(6, 182, 212))
        draw.text((cx + 45, cy - 100), "Tom 2", fill=(255, 255, 255, 255), font=font_label_sm, anchor="mm")

        # 6. Overhead L (Ambiental - Canal 20)
        # Representado con una base aérea a la derecha del set
        draw.line([(cx + 110, cy - 75), (cx + 110, cy + 15)], fill=(161, 161, 170, 255), width=3)
        draw.ellipse([(cx + 100, cy - 90), (cx + 120, cy - 70)], fill=(24, 24, 27, 255), outline=(6, 182, 212, 255), width=2)
        draw_badge(cx + 110, cy - 80, 20, color=(6, 182, 212))
        draw.text((cx + 110, cy - 118), "OH L", fill=(255, 255, 255, 255), font=font_label_sm, anchor="mm")

        # Etiqueta general
        draw.text((cx, cy + 130), "BATERÍA ACÚSTICA", fill=(255, 255, 255, 255), font=font_label_lg, anchor="mm")

    # ------------------------------------------
    # D. INSERCIÓN DE COMPONENTES EN COORDENADAS
    # ------------------------------------------

    # 1. MONITORES (ENVÍOS AUXILIARES)
    # Monitor 2 (Izquierda adelante / Stage Right Front)
    draw_monitor(350, 1250, 2, "L-Frontal (Voces)")
    # Monitor 1 (Derecha adelante / Stage Left Front)
    draw_monitor(2050, 1250, 1, "R-Frontal (Voces)")
    # Monitor 4 (Izquierda lateral / Stage Right Lateral)
    draw_monitor(150, 800, 4, "L-Lateral (Sidefill)")
    # Monitor 3 (Derecha lateral / Stage Left Lateral)
    draw_monitor(2250, 800, 3, "R-Lateral (Sidefill)")
    # Monitor 5 (Fondo centro / Upstage Center) - Al lado de Congas
    draw_monitor(870, 220, 5, "Techo (Mezcla General)")

    # 2. EL CORO (VOCES 1 A 10)
    # Fila Delantera (Downstage): 5, 4, 3, 2, 1 (Izquierda a Derecha)
    front_vocals = [5, 4, 3, 2, 1]
    for idx, num in enumerate(front_vocals):
        x = 550 + idx * 325
        y = 1120
        # Voces 1-4 inalámbricos, Voz 5 con cable
        is_wireless = num in [1, 2, 3, 4]
        draw_mic_stand(x, y, num, is_wireless=is_wireless)

    # Fila Trasera (Mid-downstage): 10, 9, 8, 7, 6 (Izquierda a Derecha)
    back_vocals = [10, 9, 8, 7, 6]
    for idx, num in enumerate(back_vocals):
        x = 550 + idx * 325
        y = 960
        # Todas las voces 5-10 son cableadas (wireless=False)
        draw_mic_stand(x, y, num, is_wireless=False)

    # 3. VIENTOS (STAGE RIGHT / PÚBLICO IZQUIERDA)
    # Fila trasera: Sax 1 (11) y Sax 2 (12)
    draw_brass(330, 270, 11, "Saxofón 1", is_trumpet=False)
    draw_brass(540, 270, 12, "Saxofón 2", is_trumpet=False)
    # Fila delantera: Trompeta 1 (13) y Trompeta 2 (14)
    draw_brass(330, 490, 13, "Trompeta 1", is_trumpet=True)
    draw_brass(540, 490, 14, "Trompeta 2", is_trumpet=True)

    # 4. RITMO (BATERÍA Y CONGAS) - UPSTAGE CENTER
    draw_drums(1250, 390)
    draw_congas(920, 410, 21, "Congas L/R")

    # 5. STRING SECTION (GUITARRAS Y BAJO) - MIDSTAGE CENTER
    # Distribución simétrica de 7 instrumentos en el centro (4 extras y 3 principales)
    draw_guitar(690, 720, 0, "Guit. Acústica", is_extra=True)
    draw_guitar(840, 720, 0, "Guit. Acústica", is_extra=True)
    draw_guitar(1020, 720, 28, "Guitarra Eléctrica")
    draw_guitar(1200, 720, 30, "Bajo Eléctrico", is_bass=True)
    draw_guitar(1380, 720, 29, "Guitarra Elec-Acu.")
    draw_guitar(1560, 720, 0, "Guit. Acústica", is_extra=True)
    draw_guitar(1720, 720, 0, "Guit. Acústica", is_extra=True)

    # 6. TECLADOS (STAGE LEFT / PÚBLICO DERECHA) - 3 FILAS DE 2
    # Fila delantera (Downstage): Teclado 1 (22) y Teclado 2 (23)
    draw_keyboard(1930, 730, 22, "Teclado 1 (P.)")
    draw_keyboard(2190, 730, 23, "Teclado 2")
    # Fila intermedia (Midstage): Teclado 3 (24) y Teclado 4 (25)
    draw_keyboard(1930, 520, 24, "Teclado 3")
    draw_keyboard(2190, 520, 25, "Teclado 4")
    # Fila trasera (Upstage): Teclado 5 (26) y Teclado 6 (27)
    draw_keyboard(1930, 310, 26, "Teclado 5")
    draw_keyboard(2190, 310, 27, "Teclado 6")

    # Guardar la imagen generada
    os.makedirs("scratch", exist_ok=True)
    output_png = "scratch/stage_plot.png"
    img.save(output_png, "PNG")
    print(f"Stage Plot Image generated at {output_png}")
    return output_png

# ==========================================
# 3. CONSTRUCCIÓN DE PDF DE DOS PÁGINAS (LANDSCAPE)
# ==========================================
class TechRiderPDF(FPDF):
    def __init__(self):
        # Usamos orientación horizontal (Landscape) y unidad en milímetros (mm)
        super().__init__(orientation='L', unit='mm', format='Letter')
        self.set_margin(10)
        self.set_auto_page_break(auto=True, margin=10)

    def header(self):
        # Cabecera minimalista pero elegante
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "CIEDI - CEREMONIA DE CLAUSURA 2026  |  RIDER TÉCNICO DE SONIDO", ln=True, align="R")
        self.line(10, 15, 269, 15) # Línea divisoria
        self.ln(3)

    def footer(self):
        # Pie de página con numeración
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Página {self.page_no()} de {{nb}}", align="C")
        self.cell(0, 10, "Preparado por el Departamento de Artes - Música CIEDI", align="R")

def create_tech_rider_pdf(image_path):
    pdf = TechRiderPDF()
    pdf.alias_nb_pages()
    
    # ------------------------------------------
    # PÁGINA 1: EL STAGE PLOT (PLANO DE ESCENARIO)
    # ------------------------------------------
    pdf.add_page()
    pdf.set_y(15) # Justo debajo de la línea de cabecera
    
    # Insertar la imagen del Stage Plot a página casi completa
    # Tamaño Letter horizontal es aprox 279mm x 216mm. Con márgenes de 10mm nos queda 259mm x 196mm.
    # Usaremos 259mm de ancho y ajustaremos el alto proporcionalmente.
    pdf.image(image_path, x=10, y=17, w=259, h=162)
    
    # Nota al pie del plano
    pdf.set_y(180)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.multi_cell(0, 4, 
        "Nota: La disposición física de los micrófonos de coro representa la formación arqueada en dos filas (Voces 5, 4, 3, 2, 1 al frente; Voces 10, 9, 8, 7, 6 atrás).\n"
        "Las 4 guitarras electroacústicas adicionales (marcadas sin número de canal) se conectarán a dos amplificadores Line 6 en escenario y no se envían a la consola principal de P.A.",
        align="C"
    )

    # ------------------------------------------
    # PÁGINA 2: INPUT LIST Y MONITOREO
    # ------------------------------------------
    pdf.add_page()
    pdf.set_y(17)
    
    # Título de la sección
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(24, 24, 27)
    pdf.cell(0, 8, "RIDER TÉCNICO Y LISTA DE CANALES (INPUT LIST)", ln=True)
    
    # Detalles generales
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, "Docentes Responsables: Orlando Gómez, Oscar Villarreal, Joan Cabrera  |  Consola Requerida: Digital 32 Canales Mínimo (ej. Behringer X32 / Midas M32)", ln=True)
    pdf.ln(3)

    # Definir datos del Input List
    channels_data = [
        ("1", "Voz 1 - Inalámbrico", "Micrófono (UHF)", "-", "Coro fila delantera"),
        ("2", "Voz 2 - Inalámbrico", "Micrófono (UHF)", "-", "Coro fila delantera"),
        ("3", "Voz 3 - Inalámbrico", "Micrófono (UHF)", "-", "Coro fila delantera"),
        ("4", "Voz 4 - Inalámbrico", "Micrófono (UHF)", "-", "Coro fila delantera"),
        ("5", "Voz 5 - De mano", "Micrófono (Cable)", "-", "Coro fila delantera"),
        ("6", "Voz 6 - De mano", "Micrófono (Cable)", "-", "Coro fila trasera"),
        ("7", "Voz 7 - De mano", "Micrófono (Cable)", "-", "Coro fila trasera"),
        ("8", "Voz 8 - De mano", "Micrófono (Cable)", "-", "Coro fila trasera"),
        ("9", "Voz 9 - De mano", "Micrófono (Cable)", "-", "Coro fila trasera"),
        ("10", "Voz 10 - De mano", "Micrófono (Cable)", "-", "Coro fila trasera"),
        ("11", "Vientos - Saxofón 1", "Mic. Dinámico", "-", "Soporte de piso"),
        ("12", "Vientos - Saxofón 2", "Mic. Dinámico", "-", "Soporte de piso"),
        ("13", "Vientos - Trompeta 1", "Mic. Dinámico", "-", "Soporte de piso"),
        ("14", "Vientos - Trompeta 2", "Mic. Dinámico", "-", "Soporte de piso"),
        ("15", "Batería - Bombo", "Mic. Din. (B52)", "-", "Mic. interno"),
        ("16", "Batería - Caja", "Mic. Din. (SM57)", "-", "Mic. en caja"),
        ("17", "Batería - Hi hat", "Mic. Cond.", "-", "Condensador"),
        ("18", "Batería - Tom 1", "Mic. Clip (Din.)", "-", "Clip de tom"),
        ("19", "Batería - Tom 2", "Mic. Clip (Din.)", "-", "Clip de tom"),
        ("20", "Batería - Over Head L", "Mic. Cond.", "-", "Base aérea (Amb.)"),
        ("21", "Percusión - Congas L-R", "Mic. Dinámico x2", "-", "Soporte doble conga"),
        ("22", "Teclado 1 (Principal)", "-", "DI Activa", "Línea Principal"),
        ("23", "Teclado 2", "-", "DI Pasiva", "Línea balanceada"),
        ("24", "Teclado 3", "-", "DI Pasiva", "Línea balanceada"),
        ("25", "Teclado 4", "-", "DI Pasiva", "Línea balanceada"),
        ("26", "Teclado 5", "-", "DI Pasiva", "Línea balanceada"),
        ("27", "Teclado 6", "-", "DI Pasiva", "Línea balanceada"),
        ("28", "Guitarra Eléctrica", "Mic. Din. / Línea", "DI Pasiva", "Línea + Mic Amp"),
        ("29", "Guitarra Elec-Acu. 1", "-", "DI Pasiva", "DI a Consola"),
        ("30", "Bajo Eléctrico", "Línea / DI", "DI Activa", "Línea + Amp"),
        ("31", "Aux R", "-", "Línea", "Línea pistas/repro."),
        ("32", "Aux L", "-", "Línea", "Línea pistas/repro.")
    ]

    # Dibujar la tabla en el PDF de manera compacta pero elegante (2 columnas lado a lado para ahorrar espacio)
    # Ancho total disponible = 259mm
    # Dividiremos el espacio: Tabla de Canales 1-16 a la izquierda, Tabla de Canales 17-32 en el centro-derecha.
    col_w = [10, 45, 27, 23, 20] # Ancho de columnas: Canal(10), Instrumento(45), Mic(27), DI(23), Obs(20... reducido para encajar)
    # Ajustamos anchos para encajar dos tablas de 125mm de ancho cada una con un espacio en medio de 9mm
    t_width = 125
    col_w = [8, 45, 24, 18, 30] # 8 + 45 + 24 + 18 + 30 = 125mm
    
    # Dibujar encabezados para ambas columnas de tabla
    def draw_table_header(x_offset):
        pdf.set_x(x_offset)
        pdf.set_fill_color(31, 41, 55) # Gris oscuro #1f2937
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 7.5)
        
        pdf.cell(col_w[0], 5, "Ch", border=1, align="C", fill=True)
        pdf.cell(col_w[1], 5, "Instrumento / Voz", border=1, align="L", fill=True)
        pdf.cell(col_w[2], 5, "Micrófono", border=1, align="C", fill=True)
        pdf.cell(col_w[3], 5, "Caja Dir.", border=1, align="C", fill=True)
        pdf.cell(col_w[4], 5, "Observaciones", border=1, ln=False, align="L", fill=True)

    y_table_start = pdf.get_y()
    
    # Tabla Izquierda: Canales 1 a 16
    draw_table_header(10)
    pdf.ln(5)
    for i in range(16):
        ch, inst, mic, di, obs = channels_data[i]
        pdf.set_x(10)
        # Zebra striping
        if i % 2 == 0:
            pdf.set_fill_color(243, 244, 246) # Gris muy claro
        else:
            pdf.set_fill_color(255, 255, 255)
            
        pdf.set_text_color(30, 30, 30)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.cell(col_w[0], 4.5, ch, border=1, align="C", fill=True)
        pdf.cell(col_w[1], 4.5, inst[:27], border=1, align="L", fill=True)
        pdf.cell(col_w[2], 4.5, mic[:16], border=1, align="C", fill=True)
        pdf.cell(col_w[3], 4.5, di[:12], border=1, align="C", fill=True)
        pdf.cell(col_w[4], 4.5, obs[:22], border=1, ln=True, align="L", fill=True)

    # Tabla Derecha: Canales 17 a 32
    # Reposicionamos Y al inicio de la tabla
    pdf.set_y(y_table_start)
    draw_table_header(144) # 10mm margen + 125mm ancho tabla 1 + 9mm separación = 144mm
    pdf.ln(5)
    for i in range(16, 32):
        ch, inst, mic, di, obs = channels_data[i]
        pdf.set_x(144)
        if i % 2 == 0:
            pdf.set_fill_color(243, 244, 246)
        else:
            pdf.set_fill_color(255, 255, 255)
            
        pdf.set_text_color(30, 30, 30)
        pdf.set_font("Helvetica", "", 7.5)
        pdf.cell(col_w[0], 4.5, ch, border=1, align="C", fill=True)
        pdf.cell(col_w[1], 4.5, inst[:27], border=1, align="L", fill=True)
        pdf.cell(col_w[2], 4.5, mic[:16], border=1, align="C", fill=True)
        pdf.cell(col_w[3], 4.5, di[:12], border=1, align="C", fill=True)
        pdf.cell(col_w[4], 4.5, obs[:22], border=1, ln=True, align="L", fill=True)

    pdf.ln(3)

    # ------------------------------------------
    # E. SECCIÓN DE MONITOREO Y ENVÍOS (ABAJO IZQUIERDA) Y NOTAS (ABAJO DERECHA)
    # ------------------------------------------
    y_bottom_section = pdf.get_y()
    
    # 1. Tabla de Monitoreo (Ancho 125mm)
    pdf.set_x(10)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(24, 24, 27)
    pdf.cell(125, 5, "DISTRIBUCIÓN DE MONITORES (ENVÍOS AUXILIARES)", ln=True)
    pdf.ln(1)
    
    # Encabezado Monitoreo
    pdf.set_x(10)
    pdf.set_fill_color(16, 185, 129) # Verde esmeralda para monitores
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(15, 5, "Envío", border=1, align="C", fill=True)
    pdf.cell(30, 5, "Ubicación en Escenario", border=1, align="L", fill=True)
    pdf.cell(80, 5, "Detalle / Mezcla de Audio Sugerida", border=1, ln=True, align="L", fill=True)
    
    monitors_data = [
        ("Aux 1", "MON 1 (Downstage Right)", "Voces principales (Frente Derecha del público) y mezcla sutil de piano."),
        ("Aux 2", "MON 2 (Downstage Left)", "Voces principales (Frente Izquierda del público) y mezcla sutil de piano."),
        ("Aux 3", "MON 3 (Midstage Right Side)", "Side-fill derecho: Mezcla general balanceada con énfasis en sección de cuerdas."),
        ("Aux 4", "MON 4 (Midstage Left Side)", "Side-fill izquierdo: Mezcla general balanceada con énfasis en sección de viento."),
        ("Aux 5", "MON 5 (Upstage Center)", "Upstage Center (Techo/Atrás): Retorno para batería, congas, vientos y fila trasera de coro.")
    ]
    
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(30, 30, 30)
    for idx, (env, loc, det) in enumerate(monitors_data):
        pdf.set_x(10)
        if idx % 2 == 0:
            pdf.set_fill_color(240, 253, 250) # Verde menta muy claro
        else:
            pdf.set_fill_color(255, 255, 255)
        pdf.cell(15, 4.5, env, border=1, align="C", fill=True)
        pdf.cell(30, 4.5, loc, border=1, align="L", fill=True)
        pdf.cell(80, 4.5, det, border=1, ln=True, align="L", fill=True)

    # 2. Notas Técnicas (Ancho 125mm) - Colocada a la derecha de la de monitoreo
    pdf.set_y(y_bottom_section)
    pdf.set_x(144)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(24, 24, 27)
    pdf.cell(125, 5, "REQUERIMIENTOS Y NOTAS TÉCNICAS ADICIONALES", ln=True)
    pdf.ln(1)
    
    pdf.set_x(144)
    pdf.set_fill_color(254, 243, 199) # Fondo amarillo/oro sutil
    pdf.set_text_color(120, 53, 4) # Texto marrón oscuro
    pdf.set_font("Helvetica", "", 7.2)
    
    # Crear un bloque de texto multi-línea con borde decorativo
    notes_text = (
        "- GUITARRAS ADICIONALES: Hay 4 guitarras electroacústicas adicionales en escena que se "
        "conectarán directamente a 2 amplificadores LINE 6 provistos localmente. Estas guitarras "
        "NO van conectadas a la consola principal de sonido de P.A.\n\n"
        "- SISTEMA DE CORO: Consta de 10 cantantes. Los micrófonos 1 a 4 son inalámbricos UHF de mano "
        "en base de piso. Los micrófonos 5 a 10 son de mano con cable XLR en base de piso. Deben estar "
        "perfectamente numerados y etiquetados en la consola.\n\n"
        "- CAJAS DIRECTAS (DI): Se requieren 6 Cajas Directas pasivas para teclados 2-6 y guitarra 29, "
        "y 2 Cajas Directas activas de alta calidad para Teclado 1 (principal) y Bajo Eléctrico (canal 30).\n\n"
        "- ELECTRICIDAD: Puntos de corriente de 110V CA independientes (mínimo 4 tomas cada uno) en: "
        "Zona de teclados (derecha), Zona de guitarras (centro) y Zona de batería/vientos (fondo)."
    )
    
    # Usar multi_cell con coordenadas específicas para simular la caja de texto
    pdf.set_x(144)
    pdf.multi_cell(125, 3.8, notes_text, border=1, align="L", fill=True)

    # Guardar archivo PDF final
    output_pdf = "Rider_Tecnico_y_Stage_Plot_CIEDI.pdf"
    pdf.output(output_pdf)
    print(f"Professional Tech Rider PDF generated at {output_pdf}")
    return output_pdf

# ==========================================
# 4. ORQUESTADOR PRINCIPAL
# ==========================================
if __name__ == "__main__":
    print("Starting generation of CIEDI Sound Stage Plot & Technical Rider...")
    try:
        # Generar primero la imagen del Stage Plot
        img_path = generate_stage_plot_image()
        # Generar el PDF final incluyendo la imagen y las tablas
        pdf_path = create_tech_rider_pdf(img_path)
        print("Success! Process completed successfully.")
        print(f"Generated PDF: {os.path.abspath(pdf_path)}")
    except Exception as e:
        print(f"ERROR during generation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
