from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True)
    activa = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['orden', 'nombre']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='marcas/', blank=True)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TAMANOS_CHOICES = [
        ('sencillo', 'Sencillo (90x190)'),
        ('semi', 'Semidoble (120x190)'),
        ('doble', 'Doble (140x190)'),
        ('queen', 'Queen (160x190)'),
        ('king', 'King (200x200)'),
    ]
    
    FIRMEZA_CHOICES = [
        ('suave', 'Suave'),
        ('medio', 'Medio'),
        ('firme', 'Firme'),
        ('extra_firme', 'Extra Firme'),
    ]
    
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name='productos')
    descripcion_corta = models.CharField(max_length=300)
    descripcion = RichTextField()
    
    # Características específicas de colchones
    tamano = models.CharField(max_length=20, choices=TAMANOS_CHOICES)
    firmeza = models.CharField(max_length=20, choices=FIRMEZA_CHOICES)
    altura = models.PositiveIntegerField(help_text="Altura en centímetros")
    material_principal = models.CharField(max_length=100)
    garantia_anos = models.PositiveIntegerField(default=1)
    
    # Precios y stock
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    precio_descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    
    # Imágenes
    imagen_principal = models.ImageField(upload_to='productos/')
    imagen_2 = models.ImageField(upload_to='productos/', blank=True)
    imagen_3 = models.ImageField(upload_to='productos/', blank=True)
    imagen_4 = models.ImageField(upload_to='productos/', blank=True)
    
    # Configuración
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso en kg")
    
    # Fechas
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name_plural = "Productos"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.nombre}-{self.tamano}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('producto_detalle', kwargs={'slug': self.slug})
    
    def get_precio_final(self):
        return self.precio_descuento if self.precio_descuento else self.precio
    
    def get_descuento_porcentaje(self):
        if self.precio_descuento and self.precio_descuento < self.precio:
            return round(((self.precio - self.precio_descuento) / self.precio) * 100)
        return 0
    
    def get_ahorro(self):
        if self.precio_descuento:
            return self.precio - self.precio_descuento
        return 0
    
    def __str__(self):
        return f"{self.nombre} - {self.tamano}"

class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes_adicionales')
    imagen = models.ImageField(upload_to='productos/adicionales/')
    descripcion = models.CharField(max_length=100, blank=True)
    orden = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['orden']

class Testimonio(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    comentario = models.TextField()
    calificacion = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='testimonios', blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha']

class Contacto(models.Model):
    ASUNTOS_CHOICES = [
        ('consulta_producto', 'Consulta sobre Productos'),
        ('cotizacion', 'Solicitar Cotización'),
        ('garantia', 'Temas de Garantía'),
        ('envio', 'Información de Envío'),
        ('soporte', 'Soporte Técnico'),
        ('otro', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    asunto = models.CharField(max_length=20, choices=ASUNTOS_CHOICES)
    mensaje = models.TextField()
    acepto_terminos = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    respondido = models.BooleanField(default=False)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.nombre} - {self.get_asunto_display()}"

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100, blank=True)
    activo = models.BooleanField(default=True)
    fecha_suscripcion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Suscriptores Newsletter"
        ordering = ['-fecha_suscripcion']
    
    def __str__(self):
        return self.email
                