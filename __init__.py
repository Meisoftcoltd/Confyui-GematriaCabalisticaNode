from .gematria_cabalistica import GematriaCabalisticaNode
from .html_assembler import GematriaHTMLAssembler

NODE_CLASS_MAPPINGS = {
    "GematriaCabalisticaNode": GematriaCabalisticaNode,
    "GematriaHTMLAssembler": GematriaHTMLAssembler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GematriaCabalisticaNode": "Gematría Cabalística (Input)",
    "GematriaHTMLAssembler": "Ensamblador HTML Gematría"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
