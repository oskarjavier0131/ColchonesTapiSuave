from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
from cloudinary import CloudinaryImage

register = template.Library()

@register.simple_tag
def responsive_product_image(producto, size='detail', alt='', css_class='', lazy=True):
    """
    Genera imagen de producto responsiva con WebP + fallback
    
    Uso: {% responsive_product_image producto size='thumbnail' alt='Colchón' css_class='product-img' %}
    """
    if not producto.imagen_principal:
        # Mostrar un ícono en lugar de imagen rota
        return mark_safe(f'''
            <div class="placeholder-image d-flex align-items-center justify-content-center {css_class}" 
                 style="height: 200px; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px;">
                <div class="text-center text-muted">
                    <i class="fas fa-bed" style="font-size: 3rem; color: #6c757d;"></i>
                    <p class="mt-2 mb-0 small">Sin imagen</p>
                </div>
            </div>
        ''')
    
    # Obtener URLs según el tamaño solicitado
    size_mapping = {
        'thumbnail': {
            'webp': getattr(producto, f'imagen_thumbnail', None),
            'jpg': getattr(producto, f'imagen_thumbnail_jpg', None),
            'sizes': '(max-width: 576px) 150px, (max-width: 768px) 200px, 300px'
        },
        'card': {
            'webp': getattr(producto, f'imagen_card', None),
            'jpg': getattr(producto, f'imagen_detail_jpg', None),
            'sizes': '(max-width: 768px) 300px, 400px'
        },
        'detail': {
            'webp': getattr(producto, f'imagen_detail', None),
            'jpg': getattr(producto, f'imagen_detail_jpg', None),
            'sizes': '(max-width: 768px) 90vw, 800px'
        },
        'zoom': {
            'webp': getattr(producto, f'imagen_zoom', None),
            'jpg': producto.imagen_principal,
            'sizes': '(max-width: 1200px) 90vw, 1200px'
        }
    }
    
    config = size_mapping.get(size, size_mapping['detail'])
    lazy_attr = 'loading="lazy"' if lazy else ''
    
    webp_url = config['webp'].url if config['webp'] else ''
    jpg_url = config['jpg'].url if config['jpg'] else producto.imagen_principal.url
    sizes = config['sizes']
    
    html = f'''
    <picture class="{css_class}">
        <source srcset="{webp_url}" type="image/webp" sizes="{sizes}">
        <img src="{jpg_url}" alt="{alt}" class="img-fluid {css_class}" {lazy_attr}>
    </picture>
    '''
    
    return mark_safe(html)

@register.simple_tag
def product_gallery(producto):
    """
    Genera galería completa con todas las imágenes del producto
    """
    images = []
    
    # Imagen principal
    if producto.imagen_principal:
        images.append({
            'original': producto.imagen_principal.url,
            'zoom_webp': getattr(producto, 'imagen_zoom', producto.imagen_principal).url,
            'detail_webp': getattr(producto, 'imagen_detail', producto.imagen_principal).url,
            'thumb_webp': getattr(producto, 'imagen_thumbnail', producto.imagen_principal).url,
            'detail_jpg': getattr(producto, 'imagen_detail_jpg', producto.imagen_principal).url,
            'thumb_jpg': getattr(producto, 'imagen_thumbnail_jpg', producto.imagen_principal).url,
        })
    
    # Imágenes adicionales (2, 3, 4)
    for i in range(2, 5):
        img_field = getattr(producto, f'imagen_{i}', None)
        if img_field:
            images.append({
                'original': img_field.url,
                'zoom_webp': img_field.url,
                'detail_webp': img_field.url,
                'thumb_webp': img_field.url,
                'detail_jpg': img_field.url,
                'thumb_jpg': img_field.url,
            })
    
    return images

@register.filter
def webp_supported(request):
    """
    Detecta si el navegador soporta WebP
    """
    accept_header = request.META.get('HTTP_ACCEPT', '')
    return 'image/webp' in accept_header

@register.filter
def formato_peso_colombiano(value):
    """
    Formatea un número como peso colombiano con separadores de miles
    Ejemplo: 1500000 -> $1.500.000
    """
    try:
        # Convertir a entero para eliminar decimales
        numero = int(float(value))
        # Formatear con separadores de miles usando puntos
        formatted = f"{numero:,}".replace(',', '.')
        return f"${formatted}"
    except (ValueError, TypeError):
        return f"${value}"


@register.simple_tag
def cloudinary_image(image_field, transformation=None, **kwargs):
    """Genera imagen optimizada con Cloudinary"""
    if not image_field:
        return ''
    
    if not settings.DEBUG and hasattr(image_field, 'public_id'):
        # En producción con Cloudinary
        img = CloudinaryImage(image_field.public_id)
        if transformation:
            return img.build_url(transformation=transformation)
        return img.build_url()
    else:
        # En desarrollo o imagen local
        return image_field.url if image_field else ''