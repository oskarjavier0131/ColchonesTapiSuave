from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()

@register.simple_tag
def responsive_product_image(producto, size='detail', alt='', css_class='', lazy=True):
    """
    Genera imagen de producto responsiva con WebP + fallback
    
    Uso: {% responsive_product_image producto size='thumbnail' alt='Colchón' css_class='product-img' %}
    """
    if not producto.imagen_principal:
        # Placeholder si no hay imagen
        placeholder_webp = f"{settings.STATIC_URL}images/placeholders/product-placeholder.webp"
        placeholder_jpg = f"{settings.STATIC_URL}images/placeholders/product-placeholder.jpg"
        
        return mark_safe(f'''
            <picture class="{css_class}">
                <source srcset="{placeholder_webp}" type="image/webp">
                <img src="{placeholder_jpg}" alt="{alt}" class="img-fluid {css_class}" loading="lazy">
            </picture>
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