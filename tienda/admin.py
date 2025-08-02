from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Marca, Producto, ImagenProducto, Testimonio, Contacto, Newsletter

admin.site.site_header = 'ColchonesTapiSuave - Administración'
admin.site.site_title = 'TapiSuave Admin'
admin.site.index_title = 'Panel de Administración'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'orden', 'productos_count']
    list_filter = ['activa']
    search_fields = ['nombre']
    prepopulated_fields = {'slug': ('nombre',)}
    
    def productos_count(self, obj):
        return obj.productos.count()
    productos_count.short_description = 'Productos'

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'productos_count']
    list_filter = ['activa']
    search_fields = ['nombre']
    
    def productos_count(self, obj):
        return obj.productos.count()
    productos_count.short_description = 'Productos'

class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'marca', 'tamano', 'precio_display', 'stock', 'destacado', 'activo']
    list_filter = ['categoria', 'marca', 'tamano', 'firmeza', 'destacado', 'activo']
    search_fields = ['nombre', 'descripcion_corta']
    prepopulated_fields = {'slug': ('nombre', 'tamano')}
    inlines = [ImagenProductoInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'slug', 'categoria', 'marca', 'descripcion_corta', 'descripcion')
        }),
        ('Características', {
            'fields': ('tamano', 'firmeza', 'altura', 'material_principal', 'garantia_anos', 'peso')
        }),
        ('Precios y Stock', {
            'fields': ('precio', 'precio_descuento', 'stock')
        }),
        ('Imágenes', {
            'fields': ('imagen_principal', 'imagen_2', 'imagen_3', 'imagen_4')
        }),
        ('Configuración', {
            'fields': ('destacado', 'activo')
        }),
    )
    
    def precio_display(self, obj):
        if obj.precio_descuento:
            return format_html(
                '<span style="text-decoration: line-through;">${}</span> <span style="color: red; font-weight: bold;">${}</span>',
                obj.precio, obj.precio_descuento
            )
        return f'${obj.precio}'
    precio_display.short_description = 'Precio'

@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ciudad', 'calificacion', 'producto', 'fecha', 'activo']
    list_filter = ['calificacion', 'activo', 'fecha']
    search_fields = ['nombre', 'ciudad', 'comentario']

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'asunto', 'fecha_creacion', 'respondido']
    list_filter = ['asunto', 'respondido', 'fecha_creacion']
    search_fields = ['nombre', 'email', 'mensaje']
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('nombre', 'email', 'telefono', 'ciudad')
        }),
        ('Mensaje', {
            'fields': ('asunto', 'mensaje', 'acepto_terminos', 'fecha_creacion')
        }),
        ('Estado', {
            'fields': ('respondido', 'fecha_respuesta')
        }),
    )
    
    def has_delete_permission(self, request, obj=None):
        # Solo permitir eliminar mensajes respondidos
        if obj:
            return obj.respondido
        return True

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'nombre', 'activo', 'fecha_suscripcion']
    list_filter = ['activo', 'fecha_suscripcion']
    search_fields = ['email', 'nombre']
    readonly_fields = ['fecha_suscripcion']
    
    actions = ['desactivar_suscriptores', 'activar_suscriptores']
    
    def desactivar_suscriptores(self, request, queryset):
        queryset.update(activo=False)
        self.message_user(request, f'{queryset.count()} suscriptores desactivados.')
    desactivar_suscriptores.short_description = 'Desactivar suscriptores seleccionados'
    
    def activar_suscriptores(self, request, queryset):
        queryset.update(activo=True)
        self.message_user(request, f'{queryset.count()} suscriptores activados.')
    activar_suscriptores.short_description = 'Activar suscriptores seleccionados'