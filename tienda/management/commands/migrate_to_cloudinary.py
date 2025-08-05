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
                self.style.WARNING('Este comando funciona mejor en producción')
            )
        
        productos = Producto.objects.filter(imagen_principal__isnull=False)
        total = productos.count()
        
        self.stdout.write(f'Migrando {total} imágenes a Cloudinary...')
        
        for i, producto in enumerate(productos, 1):
            try:
                if producto.imagen_principal:
                    public_id = f"productos/producto_{producto.id}_principal"
                    
                    # Subir a Cloudinary
                    if hasattr(producto.imagen_principal, 'path') and os.path.exists(producto.imagen_principal.path):
                        result = cloudinary.uploader.upload(
                            producto.imagen_principal.path,
                            public_id=public_id,
                            folder="productos",
                            resource_type="image"
                        )
                    else:
                        result = cloudinary.uploader.upload(
                            producto.imagen_principal.url,
                            public_id=public_id,
                            folder="productos",
                            resource_type="image"
                        )
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ {i}/{total} - {producto.nombre}: {result["secure_url"]}'
                        )
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ {i}/{total} - Error con {producto.nombre}: {str(e)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS('🎉 Migración completada!')
        )