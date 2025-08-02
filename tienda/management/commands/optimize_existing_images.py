from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from tienda.models import Producto
from tienda.utils import compress_image
import os
from PIL import Image

class Command(BaseCommand):
    help = 'Optimiza todas las imágenes existentes en el sistema'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Forzar re-procesamiento de todas las imágenes',
        )
        
        parser.add_argument(
            '--format',
            type=str,
            choices=['webp', 'jpeg', 'both'],
            default='both',
            help='Formato de salida (webp, jpeg, both)',
        )
        
        parser.add_argument(
            '--quality',
            type=int,
            default=85,
            help='Calidad de compresión (1-100)',
        )
    
    def handle(self, *args, **options):
        force = options['force']
        format_output = options['format']
        quality = options['quality']
        
        self.stdout.write(self.style.SUCCESS('🚀 Iniciando optimización de imágenes...'))
        
        # Obtener productos con imágenes
        productos = Producto.objects.exclude(imagen_principal='')
        total = productos.count()
        
        if total == 0:
            self.stdout.write(self.style.WARNING('No se encontraron productos con imágenes.'))
            return
        
        self.stdout.write(f'📊 Encontrados {total} productos para procesar...')
        
        stats = {
            'processed': 0,
            'errors': 0,
            'total_size_before': 0,
            'total_size_after': 0,
        }
        
        for i, producto in enumerate(productos, 1):
            try:
                self.stdout.write(f'🔄 [{i}/{total}] Procesando: {producto.nombre}')
                
                # Procesar imagen principal
                if producto.imagen_principal:
                    result = self.process_product_image(producto, quality, format_output)
                    stats['processed'] += 1
                    stats['total_size_before'] += result['size_before']
                    stats['total_size_after'] += result['size_after']
                
                # Procesar imágenes adicionales
                for img_num in range(2, 5):
                    img_field = getattr(producto, f'imagen_{img_num}', None)
                    if img_field:
                        self.process_additional_image(img_field, quality, format_output)
                
                self.stdout.write(f'  ✅ Completado')
                
            except Exception as e:
                stats['errors'] += 1
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Error: {str(e)}')
                )
        
        # Mostrar estadísticas finales
        self.show_final_stats(stats)
    
    def process_product_image(self, producto, quality, format_output):
        """Procesa la imagen principal de un producto"""
        original_path = producto.imagen_principal.path
        original_size = os.path.getsize(original_path)
        
        # Generar versiones optimizadas
        sizes = {
            'thumbnail': (300, 300),
            'detail': (800, 600),
            'zoom': (1200, 900),
        }
        
        total_size_after = 0
        
        for size_name, dimensions in sizes.items():
            if format_output in ['webp', 'both']:
                webp_file = compress_image(
                    producto.imagen_principal, 
                    dimensions, 
                    quality, 
                    'WEBP'
                )
                total_size_after += len(webp_file.read())
                webp_file.seek(0)
            
            if format_output in ['jpeg', 'both']:
                jpg_file = compress_image(
                    producto.imagen_principal, 
                    dimensions, 
                    quality, 
                    'JPEG'
                )
                total_size_after += len(jpg_file.read())
                jpg_file.seek(0)
        
        return {
            'size_before': original_size,
            'size_after': total_size_after
        }
    
    def process_additional_image(self, image_field, quality, format_output):
        """Procesa imágenes adicionales"""
        try:
            if format_output in ['webp', 'both']:
                compress_image(image_field, (800, 600), quality, 'WEBP')
            
            if format_output in ['jpeg', 'both']:
                compress_image(image_field, (800, 600), quality, 'JPEG')
                
        except Exception as e:
            self.stdout.write(f'    ⚠️ Error procesando imagen adicional: {e}')
    
    def show_final_stats(self, stats):
        """Muestra estadísticas finales"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('📊 ESTADÍSTICAS FINALES'))
        self.stdout.write('='*50)
        
        self.stdout.write(f"✅ Productos procesados: {stats['processed']}")
        self.stdout.write(f"❌ Errores: {stats['errors']}")
        
        if stats['total_size_before'] > 0:
            size_before_mb = stats['total_size_before'] / (1024 * 1024)
            size_after_mb = stats['total_size_after'] / (1024 * 1024)
            reduction = ((stats['total_size_before'] - stats['total_size_after']) / stats['total_size_before']) * 100
            
            self.stdout.write(f"📦 Tamaño original: {size_before_mb:.1f} MB")
            self.stdout.write(f"📦 Tamaño optimizado: {size_after_mb:.1f} MB")
            self.stdout.write(self.style.SUCCESS(f"💾 Reducción: {reduction:.1f}%"))
        
        self.stdout.write('\n🎉 ¡Optimización completada!')