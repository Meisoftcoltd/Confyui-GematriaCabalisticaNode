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
                "concepto": ("STRING", {"default": "Sendero Aleph, El Loco"}), # CONCEPTO PURO DEL PRIMER NODO
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
            parts = md_text.split('###')
            sections = []
            for p in parts[1:]: # Ignoramos parts[0] que es el "# REPORTE VIBRACIONAL..."
                lines = p.split('\n', 1)
                content = lines[1].replace('**', '').strip() if len(lines) > 1 else p.strip()
                sections.append(content)
            return sections

        sec1 = extract_sections(md1) + [""] * 4
        sec2 = extract_sections(md2) + [""] * 4
        sec3 = extract_sections(md3) + [""] * 4
        sec4 = extract_sections(md4) + [""] * 3

        # ---------------------------------------------------------
        # 3. BASE DE DATOS DEL TAROT Y SIGNOS (100% DINÁMICO)
        # ---------------------------------------------------------
        # Formato: "Sendero": ("Letra Hebrea", "Número Tarot", "Conexión")
        tarot_db = {
            "Aleph": ("א", "0", "Kether a Chokmah"), "Bet": ("ב", "I", "Kether a Binah"),
            "Gimel": ("ג", "II", "Kether a Tiferet"), "Dalet": ("ד", "III", "Chokmah a Binah"),
            "He": ("ה", "IV", "Chokmah a Tiferet"), "Vav": ("ו", "V", "Chokmah a Chesed"),
            "Zain": ("ז", "VI", "Binah a Tiferet"), "Chet": ("ח", "VII", "Binah a Gevurah"),
            "Tet": ("ט", "VIII", "Chesed a Gevurah"), "Yod": ("י", "IX", "Chesed a Tiferet"),
            "Kaf": ("כ", "X", "Chesed a Netzach"), "Lamed": ("ל", "XI", "Gevurah a Tiferet"),
            "Mem": ("מ", "XII", "Gevurah a Hod"), "Nun": ("נ", "XIII", "Tiferet a Netzach"),
            "Samej": ("ס", "XIV", "Tiferet a Yesod"), "Ayin": ("ע", "XV", "Tiferet a Hod"),
            "Pe": ("פ", "XVI", "Netzach a Hod"), "Tzadi": ("צ", "XVII", "Netzach a Yesod"),
            "Kof": ("ק", "XVIII", "Netzach a Malkhut"), "Resh": ("ר", "XIX", "Hod a Yesod"),
            "Shin": ("ש", "XX", "Hod a Malkhut"), "Tav": ("ת", "XXI", "Yesod a Malkhut")
        }

        # Extraer Sendero y Arquetipo directo del input del nodo base (ej. "Sendero Aleph, El loco")
        concept_parts = [p.strip() for p in concepto.split(',')]
        sendero_str = concept_parts[0] if len(concept_parts) > 0 else "Aleph"
        arquetipo_str = concept_parts[1].title() if len(concept_parts) > 1 else "El Loco"
        sendero_name = sendero_str.replace("Sendero", "").replace("sendero", "").strip().title()

        # Buscar en DB
        letra, num_tarot, conexion = tarot_db.get(sendero_name, ("-", "-", "-"))

        # Conversor simple a romanos para el número maestro
        def to_roman(n):
            romans = {11: 'XI', 22: 'XXII', 33: 'XXXIII'}
            return romans.get(n, str(n))

        # Extractor robusto de signos del zodiaco
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

        html = html.replace("{{NUMERO_GRANDE}}", str(numero_cabalistico))
        html = html.replace("{{NUMERO_ROMANO}}", to_roman(numero_cabalistico))
        html = html.replace("{{ETIQUETA_NUMERO}}", f"Frecuencia · {numero_cabalistico}")
        html = html.replace("{{ETIQUETA_SENDERO}}", f"Sendero {sendero_name}")
        html = html.replace("{{ETIQUETA_ARQUETIPO}}", arquetipo_str)
        html = html.replace("{{NOMBRE_LETRA_HEBREA}}", letra)
        html = html.replace("{{NUMERO_SENDERO}}", num_tarot)
        html = html.replace("{{NOMBRE_ARQUETIPO}}", arquetipo_str)
        html = html.replace("{{CONEXION_SEFIROT}}", conexion)

        for tag, valor in signos.items():
            html = html.replace(tag, valor)

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