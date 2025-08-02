from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFit, ResizeToFill, Adjust
from pilkit.processors import Transpose, SmartCrop

# Configuraciones específicas para colchones
@register.generator('producto:thumbnail')
class ProductoThumbnail(ImageSpec):
    """Miniatura cuadrada para grids de productos"""
    processors = [
        Transpose(),  # Corrige orientación EXIF
        ResizeToFill(300, 300),  # Cuadrado perfecto
        Adjust(sharpness=1.1),  # Ligero enfoque
    ]
    format = 'WEBP'
    options = {'quality': 85, 'method': 6}  # Método 6 = mejor compresión

@register.generator('producto:card')
class ProductoCard(ImageSpec):
    """Para tarjetas de producto en móvil"""
    processors = [
        Transpose(),
        ResizeToFit(400, 300),
    ]
    format = 'WEBP'
    options = {'quality': 80}

@register.generator('producto:detail')
class ProductoDetail(ImageSpec):
    """Para página de detalle del producto"""
    processors = [
        Transpose(),
        ResizeToFit(800, 600),
    ]
    format = 'WEBP'
    options = {'quality': 90}

@register.generator('producto:zoom')
class ProductoZoom(ImageSpec):
    """Para zoom y galería completa"""
    processors = [
        Transpose(),
        ResizeToFit(1200, 900),
    ]
    format = 'WEBP'
    options = {'quality': 95}

@register.generator('producto:hero')
class ProductoHero(ImageSpec):
    """Para banners hero en homepage"""
    processors = [
        Transpose(),
        ResizeToFit(1920, 800),
    ]
    format = 'WEBP'
    options = {'quality': 85}

# Fallbacks JPEG para navegadores antiguos
@register.generator('producto:thumbnail_jpg')
class ProductoThumbnailJPG(ImageSpec):
    processors = [Transpose(), ResizeToFill(300, 300)]
    format = 'JPEG'
    options = {'quality': 85, 'optimize': True}

@register.generator('producto:detail_jpg')
class ProductoDetailJPG(ImageSpec):
    processors = [Transpose(), ResizeToFit(800, 600)]
    format = 'JPEG'
    options = {'quality': 90, 'optimize': True}