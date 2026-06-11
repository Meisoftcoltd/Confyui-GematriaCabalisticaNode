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
    CATEGORY = "GematriaCabalistica"

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
            1: ("Keter (Corona)", "corona blanca brillante, luz cegadora pura, geometría celestial hiperdetallada, chispa divina, detalles en oro, obra maestra"),
            2: ("Chochmah (Sabiduría)", "nebulosa cósmica, estrellas plateadas antiguas, espacio profundo, energía fluyente, sabiduría, místico, 8k"),
            3: ("Binah (Entendimiento)", "océano índigo profundo, matriz cósmica, aguas místicas oscuras, templo antiguo, sombras profundas"),
            4: ("Chesed (Misericordia)", "cielo azul majestuoso, reino expansivo, trono de misericordia, simbolismo de júpiter, gran arquitectura"),
            5: ("Gevurah (Rigor)", "fuego sagrado, rubí rojo brillante, armadura de guerrero antiguo, energía intensa, chispas, simbolismo de marte"),
            6: ("Tiferet (Belleza)", "sol dorado radiante, chakra del corazón, equilibrio perfecto, simetría divina, aura brillante, hermoso arte místico"),
            7: ("Netzach (Victoria)", "naturaleza verde esmeralda, flores místicas floreciendo, simbolismo de venus, pasión, fuerza vital vibrante"),
            8: ("Hod (Esplendor)", "pergaminos antiguos, geometría sagrada, luz naranja brillante, simbolismo de mercurio, intrincados caminos lógicos"),
            9: ("Yesod (Fundamento)", "luna púrpura brillante mística, niebla etérea, reflejos de cristal, atmósfera onírica, subconsciente"),
            10: ("Malkhut (El Reino)", "raíces antiguas brillantes, tierra física, suelo rico, enraizamiento del árbol de la vida, manifestación terrenal"),
            11: ("Sendero Aleph", "arquetipo del tarot del loco, acantilado místico, potencial puro, fondo amarillo brillante, nuevo comienzo"),
            12: ("Sendero Bet", "arquetipo del mago, herramientas brillantes de creación, altar místico, manipulando energía"),
            13: ("Sendero Gimel", "la suma sacerdotisa, conocimiento oculto, luna creciente azul brillante, velo de misterios"),
            14: ("Sendero Dalet", "la emperatriz, exuberante bosque místico, abundancia, energía divina femenina, cascadas"),
            15: ("Sendero He", "el emperador, trono de piedra roja sólida, autoridad, fondo ardiente, poder estructurado"),
            16: ("Sendero Vav", "el hierofante, antiguas enseñanzas místicas, llaves sagradas, símbolos esotéricos brillantes"),
            17: ("Sendero Zain", "los amantes, llamas gemelas brillantes, unión divina perfecta, luz armoniosa"),
            18: ("Sendero Chet", "el carro, energía mística en movimiento, superando obstáculos, armadura brillante"),
            19: ("Sendero Tet", "fuerza, aura de león dorado brillante, poder suave, domando a la bestia"),
            20: ("Sendero Yod", "el ermitaño, linterna solitaria brillante en la oscuridad, cima de la montaña, sabiduría interior"),
            21: ("Sendero Kaf", "rueda de la fortuna, galaxia cósmica giratoria, destino, suerte, reloj celestial brillante"),
            22: ("Sendero Lamed", "justicia, balanzas doradas brillantes, verdad, equilibrio cósmico, espada de luz")
        }

        # Obtener los atributos correspondientes al número final
        concepto, prompt_positivo = mapeo_salidas.get(suma, ("Desconocido", ""))
        prompt_negativo = "feo, deformado, mal dibujado, texto, marca de agua, mala anatomía, caótico, baja resolución"

        return (suma, concepto, prompt_positivo, prompt_negativo)
