# Gematría Cabalística Node para ComfyUI

Este Custom Node para ComfyUI toma un nombre (o cualquier texto), aplica la lógica matemática de la **gematría cabalística** utilizando el alfabeto latino, reduce el valor a un número místico del 1 al 22 (que mapea con los Sefirot y Senderos del Árbol de la Vida), y devuelve atributos y prompts listos para alimentar directamente a Stable Diffusion.

Es una herramienta ideal para crear arte generativo místico, lecturas de tarot visuales o avatares personalizados basados en la energía del nombre del usuario.

## 🚀 Instalación

Este nodo ha sido diseñado para ser **100% Plug & Play**. Utiliza únicamente la librería estándar de Python (`unicodedata` y `re`), por lo que **no necesitas instalar dependencias extra con pip**.

1. Abre tu terminal o línea de comandos.
2. Navega hasta el directorio de `custom_nodes` de tu instalación de ComfyUI:
   ```bash
   cd ruta/a/tu/ComfyUI/custom_nodes
   ```
3. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```
4. Reinicia ComfyUI.

## 🔮 Uso del Nodo

En la interfaz de ComfyUI, puedes encontrar el nodo de la siguiente manera:
- Haz doble clic en el espacio de trabajo y busca: `GematriaCabalisticaNode` o `Gematría Cabalística`.
- O navega por el menú contextual: `Add Node` -> `GipsyCabalistico` -> `Gematría Cabalística`.

### 📥 Entradas (Inputs)

- **`nombre_completo`** (`STRING`): El nombre, frase o palabra que deseas analizar.
  - *Inteligencia del nodo:* No te preocupes por el formato. El nodo limpia automáticamente el texto, eliminando mayúsculas, acentos, espacios y caracteres especiales para garantizar una suma matemática exacta.

### 📤 Salidas (Outputs)

- **`NUMERO`** (`INT`): Número entero entre 1 y 22. Es el resultado de la suma gemátrica y su posterior reducción mística.
  - *Nota Cabalística:* Si dejas el campo vacío o introduces caracteres que suman 0, el nodo te anclará al plano físico devolviendo **10 (Malkhut / El Reino)**.
- **`CONCEPTO`** (`STRING`): El nombre del Sefirá o Sendero asociado al número (Ej: `"Keter (Corona)"`, `"Sendero Aleph"`). Útil para mostrarlo en pantalla con nodos de texto.
- **`PROMPT_POSITIVO`** (`STRING`): Un prompt visual altamente detallado y estético, generado automáticamente en base a la energía del número resultante. Está diseñado para conectarse directamente al nodo de condicionamiento positivo de tu modelo base (ej. `CLIP Text Encode`).
- **`PROMPT_NEGATIVO`** (`STRING`): Un prompt negativo estático y genérico diseñado para asegurar una buena anatomía y calidad de imagen en Stable Diffusion (`"ugly, deformed, poorly drawn, text, watermark, bad anatomy, chaotic, low resolution"`). Se conecta al condicionamiento negativo.

## 🧠 Lógica Matemática y Reducción

El nodo sigue una lógica estricta y tradicional adaptada al alfabeto latino:

1. **Diccionario de Gematría:**
   Asigna los siguientes valores a las letras: `a=1, b=2, g=3, d=4, e=5, v=6, z=7, c=20, h=5, t=9, i=10, j=10, y=10, k=20, l=30, m=40, n=50, s=60, o=70, p=80, q=100, r=200, u=6, w=6, f=80, x=60`. Las letras que no están en este diccionario se valoran en 0.
2. **Suma:** Se suma el valor individual de cada letra de la palabra ingresada.
3. **Reducción Mística (Bucle):** Si la suma total es mayor a 22 (ya que existen 22 elementos en este sistema: 10 Sefirot y 12 Senderos aplicables), se suman los dígitos del número entre sí repetidamente hasta obtener un valor igual o menor a 22.
   - *Ejemplo:* Si el nombre suma `28`, la reducción será `2 + 8 = 10`.

## 🎨 Ejemplo de Workflow

1. Crea el nodo **Gematría Cabalística**.
2. Escribe tu nombre en el input `nombre_completo`.
3. Conecta el pin `PROMPT_POSITIVO` al input de texto de un **CLIP Text Encode (Prompt)**.
4. Conecta el pin `PROMPT_NEGATIVO` al input de texto de otro **CLIP Text Encode (Prompt)**.
5. Conecta los CLIP a tu **KSampler** de forma habitual.
6. ¡Genera la imagen y descubre el arte de la energía de tu nombre!
