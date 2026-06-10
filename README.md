# Gematría Cabalística Node para ComfyUI

Este Custom Node para ComfyUI toma un nombre, aplica la lógica matemática de la gematría cabalística utilizando el alfabeto latino, reduce el valor a un número del 1 al 22 (mapeando Sefirot y Senderos del Árbol de la Vida) y devuelve atributos y prompts listos para alimentar Stable Diffusion.

## Instalación

1. Ve a tu directorio de `custom_nodes` en ComfyUI:
   ```bash
   cd ComfyUI/custom_nodes
   ```
2. Clona este repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   ```
3. Reinicia ComfyUI.

*(Nota: Este nodo utiliza únicamente la librería estándar de Python (`unicodedata`, `re`), por lo que no requiere instalar dependencias extra con `pip`).*

## Uso

El nodo se encuentra en la categoría **GipsyCabalistico** con el nombre **Gematría Cabalística**.

### Entradas (Inputs)
- **nombre_completo** (`STRING`): El nombre o texto a evaluar.
  - *El nodo limpiará automáticamente el texto (quita acentos, convierte a minúsculas y elimina espacios/caracteres especiales).*

### Salidas (Outputs)
- **NUMERO** (`INT`): Número entero entre 1 y 22 resultante de la suma de las letras y la reducción mística. (Si la suma es 0, devolverá 10 por defecto, correspondiente a Malkhut).
- **CONCEPTO** (`STRING`): Nombre del Sefirá o Sendero asociado al número resultante (Ej. "Keter (Corona)").
- **PROMPT_POSITIVO** (`STRING`): Prompt visual místico generado automáticamente en base al Sefirá o Sendero correspondiente, ideal para conectar a un nodo de condicionamiento positivo de Stable Diffusion.
- **PROMPT_NEGATIVO** (`STRING`): Prompt negativo genérico de calidad estático ("ugly, deformed, poorly drawn, text, watermark, bad anatomy, chaotic, low resolution").

## Lógica Matemática
- Se utiliza el diccionario de gematría: `a=1, b=2, g=3, d=4, e=5, v=6, z=7, c=20, h=5, t=9, i=10, j=10, y=10, k=20, l=30, m=40, n=50, s=60, o=70, p=80, q=100, r=200, u=6, w=6, f=80, x=60`. Letras no listadas valen 0.
- La suma total se reduce místicamente sumando los dígitos repetidamente hasta que el número final sea menor o igual a 22.
