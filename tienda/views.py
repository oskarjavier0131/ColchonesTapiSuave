from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import Producto, Categoria, Testimonio, Contacto, Newsletter
from .forms import ContactoForm, NewsletterForm

def inicio(request):
    productos_destacados = Producto.objects.filter(destacado=True, activo=True)[:8]
    testimonios = Testimonio.objects.filter(activo=True)[:6]
    
    # Manejar suscripción al newsletter
    if request.method == 'POST' and 'newsletter_email' in request.POST:
        newsletter_form = NewsletterForm(request.POST)
        if newsletter_form.is_valid():
            try:
                newsletter_form.save()
                messages.success(request, '¡Gracias por suscribirte a nuestro newsletter!')
            except:
                messages.warning(request, 'Este email ya está suscrito a nuestro newsletter.')
        else:
            messages.error(request, 'Por favor verifica el email ingresado.')
        return redirect('inicio')
    
    context = {
        'productos_destacados': productos_destacados,
        'testimonios': testimonios,
        'newsletter_form': NewsletterForm(),
    }
    return render(request, 'tienda/inicio.html', context)

def productos_lista(request):
    productos = Producto.objects.filter(activo=True)
    
    # Filtros
    categoria_slug = request.GET.get('categoria')
    busqueda = request.GET.get('q')
    orden = request.GET.get('orden', 'nombre')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    tamano = request.GET.get('tamano')
    firmeza = request.GET.get('firmeza')
    
    if categoria_slug:
        productos = productos.filter(categoria__slug=categoria_slug)
    
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion_corta__icontains=busqueda) |
            Q(marca__nombre__icontains=busqueda) |
            Q(material_principal__icontains=busqueda)
        )
    
    if precio_min:
        try:
            precio_min = float(precio_min)
            productos = productos.filter(precio__gte=precio_min)
        except ValueError:
            pass
    
    if precio_max:
        try:
            precio_max = float(precio_max)
            productos = productos.filter(precio__lte=precio_max)
        except ValueError:
            pass
    
    if tamano:
        productos = productos.filter(tamano=tamano)
    
    if firmeza:
        productos = productos.filter(firmeza=firmeza)
    
    # Ordenamiento
    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'nombre':
        productos = productos.order_by('nombre')
    elif orden == 'destacados':
        productos = productos.order_by('-destacado', 'nombre')
    
    # Paginación
    paginator = Paginator(productos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener opciones para filtros
    tamanos_disponibles = Producto.TAMANOS_CHOICES
    firmezas_disponibles = Producto.FIRMEZA_CHOICES
    
    context = {
        'page_obj': page_obj,
        'categoria_actual': categoria_slug,
        'busqueda': busqueda,
        'orden': orden,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'tamano_actual': tamano,
        'firmeza_actual': firmeza,
        'tamanos_disponibles': tamanos_disponibles,
        'firmezas_disponibles': firmezas_disponibles,
    }
    return render(request, 'tienda/productos_lista.html', context)

def producto_detalle(request, slug):
    producto = get_object_or_404(Producto, slug=slug, activo=True)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria, 
        activo=True
    ).exclude(id=producto.id)[:4]
    
    # Testimonios específicos del producto
    testimonios_producto = Testimonio.objects.filter(
        producto=producto, 
        activo=True
    )[:3]
    
    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
        'testimonios_producto': testimonios_producto,
    }
    return render(request, 'tienda/producto_detalle.html', context)

def sobre_nosotros(request):
    # Estadísticas de la empresa
    stats = {
        'productos_total': Producto.objects.filter(activo=True).count(),
        'categorias_total': Categoria.objects.filter(activa=True).count(),
        'testimonios_total': Testimonio.objects.filter(activo=True).count(),
    }
    
    context = {
        'stats': stats,
    }
    return render(request, 'tienda/sobre_nosotros.html', context)

def contacto(request):
    form = ContactoForm()
    
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto_obj = form.save()
            
            # Enviar email de notificación (opcional)
            try:
                send_mail(
                    subject=f'Nuevo mensaje de contacto - {contacto_obj.get_asunto_display()}',
                    message=f'''
                    Nuevo mensaje de contacto recibido:
                    
                    Nombre: {contacto_obj.nombre}
                    Email: {contacto_obj.email}
                    Teléfono: {contacto_obj.telefono}
                    Ciudad: {contacto_obj.ciudad}
                    Asunto: {contacto_obj.get_asunto_display()}
                    
                    Mensaje:
                    {contacto_obj.mensaje}
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['info@colchonestapisuave.com.co'],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, '¡Mensaje enviado exitosamente! Te contactaremos pronto.')
            return redirect('contacto')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    
    context = {
        'form': form,
    }
    return render(request, 'tienda/contacto.html', context)

# Vista AJAX para búsqueda rápida
def busqueda_ajax(request):
    query = request.GET.get('q', '')
    if len(query) >= 2:
        productos = Producto.objects.filter(
            Q(nombre__icontains=query) |
            Q(descripcion_corta__icontains=query),
            activo=True
        )[:5]
        
        results = []
        for producto in productos:
            results.append({
                'id': producto.id,
                'nombre': producto.nombre,
                'precio': str(producto.get_precio_final()),
                'imagen': producto.imagen_principal.url if producto.imagen_principal else '',
                'url': producto.get_absolute_url(),
            })
        
        return JsonResponse({'results': results})
    
    return JsonResponse({'results': []})