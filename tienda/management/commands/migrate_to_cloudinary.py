from django.core.management.base import BaseCommand
from tienda.models import Producto
import cloudinary.uploader
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Migra imágenes existentes a Cloudinary'
    
    def handle(self, *args, **options):
        if settings.DEBUG:
            self.stdout.write(
                self.style.ERROR('Este comando solo funciona en producción')
            )
            return
            
        productos = Producto.objects.filter(imagen_principal__isnull=False)
        
        for producto in productos:
            try:
                # Subir imagen principal
                if producto.imagen_principal:
                    result = cloudinary.uploader.upload(
                        producto.imagen_principal.path,
                        folder="productos",
                        public_id=f"producto_{producto.id}_principal"
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'✅ {producto.nombre}: {result["url"]}')
                    )
                    
                # Subir imágenes adicionales
                for i, imagen in enumerate(producto.imagenes_adicionales.all()):
                    if imagen.imagen:
                        result = cloudinary.uploader.upload(
                            imagen.imagen.path,
                            folder="productos",
                            public_id=f"producto_{producto.id}_adicional_{i}"
                        )
                        self.stdout.write(
                            self.style.SUCCESS(f'✅ Imagen adicional {i}: {result["url"]}')
                        )
                        
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error con {producto.nombre}: {str(e)}')
                )