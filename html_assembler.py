import os
import re
import base64
import torch
import numpy as np
from io import BytesIO
from PIL import Image

class GematriaHTMLAssembler:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "nombre": ("STRING", {"default": "Nombre Apellido Apellido"}),
                "numero_cabalistico": ("INT", {"default": 11}), # NÚMERO PURO DEL PRIMER NODO
                "concepto": ("STRING", {"default": "Sendero Aleph"}), # (Se mantiene por compatibilidad de cables)
                "imagen": ("IMAGE",),
                "md1": ("STRING", {"multiline": True, "default": ""}),
                "md2": ("STRING", {"multiline": True, "default": ""}),
                "md3": ("STRING", {"multiline": True, "default": ""}),
                "md4": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("html_output",)
    FUNCTION = "assemble_html"
    CATEGORY = "GematriaCabalistica"

    def assemble_html(self, nombre, numero_cabalistico, concepto, imagen, md1, md2, md3, md4):
        # ---------------------------------------------------------
        # 1. CONVERSIÓN DE IMAGEN TENSOR A BASE64
        # ---------------------------------------------------------
        img_tensor = imagen[0].cpu().numpy()
        img_array = np.clip(255. * img_tensor, 0, 255).astype(np.uint8)
        img_pil = Image.fromarray(img_array)

        buffered = BytesIO()
        img_pil.save(buffered, format="JPEG", quality=85)
        img_base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        imagen_base64 = f"data:image/jpeg;base64,{img_base64_str}"

        # ---------------------------------------------------------
        # 2. PARSEO DE TEXTOS (Ignora el título principal y corta por ###)
        # ---------------------------------------------------------
        def extract_sections(md_text):
            matches = re.findall(r'###[^\n]*\n(.*?)(?=###|$)', md_text, re.DOTALL)
            return [m.replace('**', '').strip() for m in matches]

        sec1 = extract_sections(md1) + [""] * 4
        sec2 = extract_sections(md2) + [""] * 4
        sec3 = extract_sections(md3) + [""] * 4
        sec4 = extract_sections(md4) + [""] * 3

        # ---------------------------------------------------------
        # 3. BASE DE DATOS MAESTRA DEL TAROT (100% DINÁMICO POR NÚMERO)
        # ---------------------------------------------------------
        tarot_db = {
            1: ("Aleph", "א", "0", "El Loco", "Kether a Chokmah"),
            2: ("Bet", "ב", "I", "El Mago", "Kether a Binah"),
            3: ("Gimel", "ג", "II", "La Sacerdotisa", "Kether a Tiferet"),
            4: ("Dalet", "ד", "III", "La Emperatriz", "Chokmah a Binah"),
            5: ("He", "ה", "IV", "El Emperador", "Chokmah a Tiferet"),
            6: ("Vav", "ו", "V", "El Hierofante", "Chokmah a Chesed"),
            7: ("Zain", "ז", "VI", "Los Amantes", "Binah a Tiferet"),
            8: ("Chet", "ח", "VII", "El Carro", "Binah a Gevurah"),
            9: ("Tet", "ט", "VIII", "La Fuerza", "Chesed a Gevurah"),
            10: ("Yod", "י", "IX", "El Ermitaño", "Chesed a Tiferet"),
            11: ("Kaf", "כ", "X", "La Rueda de la Fortuna", "Chesed a Netzach"),
            12: ("Lamed", "ל", "XI", "La Justicia", "Gevurah a Tiferet"),
            13: ("Mem", "מ", "XII", "El Colgado", "Gevurah a Hod"),
            14: ("Nun", "נ", "XIII", "La Muerte", "Tiferet a Netzach"),
            15: ("Samej", "ס", "XIV", "La Templanza", "Tiferet a Yesod"),
            16: ("Ayin", "ע", "XV", "El Diablo", "Tiferet a Hod"),
            17: ("Pe", "פ", "XVI", "La Torre", "Netzach a Hod"),
            18: ("Tzadi", "צ", "XVII", "La Estrella", "Netzach a Yesod"),
            19: ("Kof", "ק", "XVIII", "La Luna", "Netzach a Malkhut"),
            20: ("Resh", "ר", "XIX", "El Sol", "Hod a Yesod"),
            21: ("Shin", "ש", "XX", "El Juicio", "Hod a Malkhut"),
            22: ("Tav", "ת", "XXI", "El Mundo", "Yesod a Malkhut")
        }

        tarot_data = tarot_db.get(numero_cabalistico, ("Desconocido", "-", "-", "Desconocido", "-"))
        sendero_name = tarot_data[0]
        letra_char = tarot_data[1]
        num_tarot = tarot_data[2]
        arquetipo_str = tarot_data[3]
        conexion = tarot_data[4]

        def to_roman(n):
            romans = {11: 'XI', 22: 'XXII', 33: 'XXXIII'}
            return romans.get(n, str(n))

        def extract_signo(esfera, text):
            zodiac = ["Aries", "Tauro", "Géminis", "Geminis", "Cáncer", "Cancer", "Leo", "Virgo", "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis"]
            for line in text.split('\n'):
                if esfera.lower() in line.lower():
                    for sign in zodiac:
                        if sign.lower() in line.lower():
                            return sign.capitalize()
            return "-"

        signos = {
            "{{SIGNO_KETER}}": extract_signo("Keter", md2), "{{SIGNO_CHOCHMAH}}": extract_signo("Chochmah", md2),
            "{{SIGNO_BINAH}}": extract_signo("Binah", md2), "{{SIGNO_CHESED}}": extract_signo("Chesed", md2),
            "{{SIGNO_GEVURAH}}": extract_signo("Gevurah", md2), "{{SIGNO_TIFERET}}": extract_signo("Tiferet", md2),
            "{{SIGNO_NETZACH}}": extract_signo("Netzach", md2), "{{SIGNO_HOD}}": extract_signo("Hod", md2),
            "{{SIGNO_YESOD}}": extract_signo("Yesod", md2), "{{SIGNO_MALKHUT}}": extract_signo("Malkhut", md2),
        }

        # ---------------------------------------------------------
        # 4. CARGA DE PLANTILLA E INYECCIÓN
        # ---------------------------------------------------------
        template_path = os.path.join(os.path.dirname(__file__), "template.html")

        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                html = file.read()
        except FileNotFoundError:
            return ("Error: No se encontró el archivo template.html",)

        html = html.replace("{{NOMBRE}}", nombre)
        html = html.replace("{{IMAGEN_CARTA_BASE64}}", imagen_base64)

        # Datos del Tarot inyectados en la portada y carta
        html = html.replace("{{NUMERO_GRANDE}}", str(numero_cabalistico))
        html = html.replace("{{NUMERO_ROMANO}}", to_roman(numero_cabalistico))
        html = html.replace("{{ETIQUETA_NUMERO}}", f"Frecuencia · {numero_cabalistico}")

        # Aquí se inyectan las 3 cosas juntas para la portada (Letra Hebrea, Latín, Nombre Sendero)
        html = html.replace("{{ETIQUETA_SENDERO}}", f"{letra_char} · {sendero_name} · Sendero {sendero_name}")
        html = html.replace("{{ETIQUETA_ARQUETIPO}}", arquetipo_str)

        html = html.replace("{{NOMBRE_LETRA_LATIN}}", sendero_name)
        html = html.replace("{{LETRA_HEBREA_CHAR}}", letra_char)
        html = html.replace("{{NUMERO_SENDERO}}", num_tarot)
        html = html.replace("{{NOMBRE_ARQUETIPO}}", arquetipo_str)
        html = html.replace("{{CONEXION_SEFIROT}}", conexion)

        # Signos
        for tag, valor in signos.items():
            html = html.replace(tag, valor)

        # Textos IA
        html = html.replace("{{TEXTO_SEC_1}}", sec1[0])
        html = html.replace("{{TEXTO_SEC_2}}", sec1[1])
        html = html.replace("{{TEXTO_SEC_3}}", sec1[2])
        html = html.replace("{{TEXTO_SEC_4}}", sec1[3])

        html = html.replace("{{TEXTO_SEC_6}}", sec2[1])
        html = html.replace("{{TEXTO_SEC_7}}", sec2[2])
        html = html.replace("{{TEXTO_SEC_8}}", sec2[3])

        html = html.replace("{{TEXTO_SEC_9}}", sec3[0])
        html = html.replace("{{TEXTO_SEC_10}}", sec3[1])
        html = html.replace("{{TEXTO_SEC_11}}", sec3[2])
        html = html.replace("{{TEXTO_SEC_12}}", sec3[3])

        html = html.replace("{{VEREDICTO_1}}", sec4[0])
        html = html.replace("{{VEREDICTO_2}}", sec4[1])
        html = html.replace("{{VEREDICTO_3}}", sec4[2])

        return (html,)
