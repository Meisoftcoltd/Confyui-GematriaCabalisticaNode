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
                "imagen": ("IMAGE",), # Entrada para la imagen generada por SDXL/Flux
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

    def assemble_html(self, nombre, imagen, md1, md2, md3, md4):
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
        # 2. PARSEO DE TEXTOS CON REGEX (Extracción limpia)
        # ---------------------------------------------------------
        def extract_sections(md_text):
            # Busca estrictamente todo lo que hay DESPUÉS de una línea con '###'
            # y se detiene antes del siguiente '###' o el final del documento.
            # Esto elimina automáticamente los títulos duplicados y el formato roto.
            matches = re.findall(r'###[^\n]*\n(.*?)(?=###|$)', md_text, re.DOTALL)
            return [m.replace('**', '').strip() for m in matches]

        sec1 = extract_sections(md1) + [""] * 4
        sec2 = extract_sections(md2) + [""] * 4
        sec3 = extract_sections(md3) + [""] * 4
        sec4 = extract_sections(md4) + [""] * 3

        # ---------------------------------------------------------
        # 3. EXTRACCIÓN INTELIGENTE DE VARIABLES
        # ---------------------------------------------------------
        def get_regex_val(pattern, text, fallback="-"):
            match = re.search(pattern, text, re.IGNORECASE)
            return match.group(1).strip() if match else fallback

        signos = {
            "{{SIGNO_KETER}}": get_regex_val(r"Keter \(Neptuno\):\s*\*?([a-zA-Z]+)", md2, "-"),
            "{{SIGNO_CHOCHMAH}}": get_regex_val(r"Chochmah \(Urano\):\s*\*?([a-zA-Z]+)", md2, "-"),
            "{{SIGNO_BINAH}}": get_regex_val(r"Binah \(Saturno\):\s*\*?([a-zA-Z]+)", md2, "-"),
            "{{SIGNO_CHESED}}": get_regex_val(r"Chesed \(Júpiter\):\s*\*?([a-zA-Z]+)", md2, "-"),
            "{{SIGNO_GEVURAH}}": get_regex_val(r"Gevurah \(Marte\):\s*\*?([a-zA-Z]+)", md2, "-"),
            "{{SIGNO_TIFERET}}": get_regex_val(r"Tiferet \(Sol\):\s*\*?([a-zA-Z]+)", md2, "-"),
            "{{SIGNO_NETZACH}}": get_regex_val(r"Netzach \(Venus\):\s*\*?([a-zA-Z]+)", md2, "-"),
            "{{SIGNO_HOD}}": get_regex_val(r"Hod \(Mercurio\):\s*\*?([a-zA-Z]+)", md2, "-"),
            "{{SIGNO_YESOD}}": get_regex_val(r"Yesod \(Luna\):\s*\*?([a-zA-Z]+)", md2, "-"),
            "{{SIGNO_MALKHUT}}": get_regex_val(r"Malkhut \(Ascendente\):\s*\*?([a-zA-Z]+)", md2, "-"),
        }

        numero_base = get_regex_val(r"frecuencia del número\s*(\d+)", md1, "No detectado")
        arquetipo = get_regex_val(r"El Arquetipo asociado es\s*([a-zA-Z\s]+)\.", md1, "No detectado")
        sendero = get_regex_val(r"El Sendero\s*([a-zA-Z]+)\s*es", md1, "No detectado")

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
        html = html.replace("{{NUMERO_GRANDE}}", numero_base)
        html = html.replace("{{NUMERO_ROMANO}}", "XI" if numero_base == "11" else ("XXII" if numero_base == "22" else "-"))
        html = html.replace("{{ETIQUETA_NUMERO}}", f"Número Maestro · {numero_base}" if numero_base != "No detectado" else "-")
        html = html.replace("{{ETIQUETA_SENDERO}}", f"Sendero {sendero}" if sendero != "No detectado" else "-")
        html = html.replace("{{ETIQUETA_ARQUETIPO}}", arquetipo)
        html = html.replace("{{NOMBRE_LETRA_HEBREA}}", "א" if sendero == "Aleph" else "-")
        html = html.replace("{{NUMERO_SENDERO}}", "0")
        html = html.replace("{{NOMBRE_ARQUETIPO}}", arquetipo)
        html = html.replace("{{CONEXION_SEFIROT}}", "La Corona a la Sabiduría")

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