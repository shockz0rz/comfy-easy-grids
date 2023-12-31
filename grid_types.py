from dataclasses import dataclass
from PIL import ImageFont

# from ImagesGrid
@dataclass
class Annotation():
    column_texts: list[str]
    row_texts: list[str]
    font: ImageFont.FreeTypeFont
