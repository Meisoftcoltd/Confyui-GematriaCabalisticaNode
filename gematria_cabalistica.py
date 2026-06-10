import unicodedata
import re

class GematriaCabalisticaNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "nombre_completo": ("STRING", {"multiline": False}),
            }
        }

    RETURN_TYPES = ("INT", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("NUMERO", "CONCEPTO", "PROMPT_POSITIVO", "PROMPT_NEGATIVO")
    FUNCTION = "calcular_gematria"
    CATEGORY = "GipsyCabalistico"

    def calcular_gematria(self, nombre_completo):
        # 1. Limpieza del input
        # Convertir a minúsculas
        texto = nombre_completo.lower()
        # Eliminar acentos
        texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
        # Eliminar espacios y caracteres especiales
        texto = re.sub(r'[^a-z]', '', texto)

        # 2. Diccionario de valores
        valores = {
            'a':1, 'b':2, 'g':3, 'd':4, 'e':5, 'v':6, 'z':7, 'c':20, 'h':5, 't':9,
            'i':10, 'j':10, 'y':10, 'k':20, 'l':30, 'm':40, 'n':50, 's':60, 'o':70,
            'p':80, 'q':100, 'r':200, 'u':6, 'w':6, 'f':80, 'x':60
        }

        # 3. Cálculo de suma
        suma = sum(valores.get(letra, 0) for letra in texto)

        # Manejo de caso especial
        if suma == 0:
            suma = 10
        else:
            # 4. Reducción mística
            while suma > 22:
                suma = sum(int(digito) for digito in str(suma))

        # 5. Diccionario de Salidas
        mapeo_salidas = {
            1: ("Keter (Corona)", "glowing white crown, pure blinding light, hyperdetailed celestial geometry, divine spark, gold accents, masterpiece"),
            2: ("Chochmah (Sabiduría)", "cosmic nebula, ancient silver stars, deep space, flowing energy, wisdom, mystical, 8k"),
            3: ("Binah (Entendimiento)", "deep indigo ocean, cosmic womb, dark mystical waters, ancient temple, profound shadows"),
            4: ("Chesed (Misericordia)", "majestic blue sky, expansive kingdom, throne of mercy, jupiter symbolism, grand architecture"),
            5: ("Gevurah (Rigor)", "sacred fire, glowing red ruby, ancient warrior armor, intense energy, sparks, mars symbolism"),
            6: ("Tiferet (Belleza)", "radiant golden sun, heart chakra, perfect balance, divine symmetry, glowing aura, beautiful mystical art"),
            7: ("Netzach (Victoria)", "emerald green nature, blooming mystical flowers, venus symbolism, passion, vibrant life force"),
            8: ("Hod (Esplendor)", "ancient scrolls, sacred geometry, glowing orange light, mercury symbolism, intricate logic pathways"),
            9: ("Yesod (Fundamento)", "mystical glowing purple moon, ethereal mist, crystal reflections, dreamlike atmosphere, subconscious"),
            10: ("Malkhut (El Reino)", "ancient glowing roots, physical earth, rich soil, tree of life grounding, earthly manifestation"),
            11: ("Sendero Aleph", "the fool tarot archetype, mystical cliff, pure potential, yellow bright background, fresh start"),
            12: ("Sendero Bet", "the magician archetype, glowing tools of creation, mystical altar, manipulating energy"),
            13: ("Sendero Gimel", "the high priestess, hidden knowledge, glowing blue crescent moon, veil of mysteries"),
            14: ("Sendero Dalet", "the empress, lush mystical forest, abundance, feminine divine energy, waterfalls"),
            15: ("Sendero He", "the emperor, solid red stone throne, authority, fiery background, structured power"),
            16: ("Sendero Vav", "the hierophant, ancient mystical teachings, sacred keys, glowing esoteric symbols"),
            17: ("Sendero Zain", "the lovers, twin flames glowing, perfect divine union, harmonious light"),
            18: ("Sendero Chet", "the chariot, moving mystical energy, overcoming obstacles, glowing armor"),
            19: ("Sendero Tet", "strength, glowing golden lion aura, gentle power, taming the beast"),
            20: ("Sendero Yod", "the hermit, solitary glowing lantern in darkness, mountaintop, inner wisdom"),
            21: ("Sendero Kaf", "wheel of fortune, spinning cosmic galaxy, fate, destiny, glowing celestial clock"),
            22: ("Sendero Lamed", "justice, glowing golden scales, truth, cosmic balance, sword of light")
        }

        # Obtener los atributos correspondientes al número final
        concepto, prompt_positivo = mapeo_salidas.get(suma, ("Desconocido", ""))
        prompt_negativo = "ugly, deformed, poorly drawn, text, watermark, bad anatomy, chaotic, low resolution"

        return (suma, concepto, prompt_positivo, prompt_negativo)
