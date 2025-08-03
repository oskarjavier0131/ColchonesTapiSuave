from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tienda.models import Categoria, Producto, Testimonio

class Command(BaseCommand):
    help = 'Configurar datos iniciales para producción'
    
    def handle(self, *args, **options):
        self.stdout.write('🚀 Configurando datos iniciales...')
        
        # Crear superusuario con tus credenciales
        if not User.objects.filter(username='jhon_martinez').exists():
            User.objects.create_superuser(
                username='jhon_martinez',
                email='jhon.martinez@colchonestapisuave.com',
                password='estefania1'
            )
            self.stdout.write('✅ Superusuario creado: jhon_martinez / estefania1')
        
        # Crear categorías
        categorias_data = [
            {'nombre': 'Colchones Individuales', 'slug': 'individuales'},
            {'nombre': 'Colchones Dobles', 'slug': 'dobles'},
            {'nombre': 'Colchones Queen', 'slug': 'queen'},
            {'nombre': 'Colchones King', 'slug': 'king'},
        ]
        
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'nombre': cat_data['nombre'],
                    'descripcion': f'Colchones {cat_data["nombre"].lower()}'
                }
            )
            if created:
                self.stdout.write(f'✅ Categoría: {categoria.nombre}')
        
        # Crear productos de ejemplo
        if not Producto.objects.exists():
            productos_data = [
                {
                    'nombre': 'Colchón TapiSuave Classic Individual',
                    'slug': 'colchon-tapisuave-classic-individual',
                    'categoria': 'individuales',
                    'precio': 299000,
                    'descripcion': 'Colchón individual de alta calidad con tecnología de espuma viscoelástica para un descanso reparador.',
                    'garantia_anos': 5,
                },
                {
                    'nombre': 'Colchón TapiSuave Premium Doble',
                    'slug': 'colchon-tapisuave-premium-doble',
                    'categoria': 'dobles',
                    'precio': 499000,
                    'descripcion': 'Colchón doble premium con sistema de resortes independientes y capa de gel refrescante.',
                    'garantia_anos': 7,
                },
                {
                    'nombre': 'Colchón TapiSuave Deluxe Queen',
                    'slug': 'colchon-tapisuave-deluxe-queen',
                    'categoria': 'queen',
                    'precio': 699000,
                    'descripcion': 'Colchón Queen size con tecnología de gel refrescante y soporte ergonómico avanzado.',
                    'garantia_anos': 10,
                },
                {
                    'nombre': 'Colchón TapiSuave Royal King',
                    'slug': 'colchon-tapisuave-royal-king',
                    'categoria': 'king',
                    'precio': 899000,
                    'descripcion': 'Colchón King size de lujo con múltiples capas de confort y tecnología anti-ácaros.',
                    'garantia_anos': 12,
                },
            ]
            
            for prod_data in productos_data:
                categoria = Categoria.objects.get(slug=prod_data['categoria'])
                producto = Producto.objects.create(
                    nombre=prod_data['nombre'],
                    slug=prod_data['slug'],
                    categoria=categoria,
                    precio=prod_data['precio'],
                    descripcion=prod_data['descripcion'],
                    garantia_anos=prod_data['garantia_anos'],
                    activo=True,
                    destacado=True
                )
                self.stdout.write(f'✅ Producto: {producto.nombre}')
        
        # Crear testimonios
        if not Testimonio.objects.exists():
            testimonios_data = [
                {
                    'nombre': 'María González',
                    'testimonio': 'Excelente calidad, duermo mucho mejor desde que compré mi colchón TapiSuave. La diferencia es notable.',
                    'calificacion': 5
                },
                {
                    'nombre': 'Carlos Rodríguez',
                    'testimonio': 'La mejor inversión para mi descanso. El colchón es súper cómodo y la atención al cliente excelente.',
                    'calificacion': 5
                },
                {
                    'nombre': 'Ana Martínez',
                    'testimonio': 'Llevamos 2 años con nuestro colchón TapiSuave y sigue como nuevo. Totalmente recomendado.',
                    'calificacion': 5
                },
            ]
            
            for test_data in testimonios_data:
                Testimonio.objects.create(
                    nombre=test_data['nombre'],
                    testimonio=test_data['testimonio'],
                    calificacion=test_data['calificacion'],
                    activo=True
                )
                self.stdout.write(f'✅ Testimonio: {test_data["nombre"]}')
        
        self.stdout.write('🎉 ¡Configuración completada exitosamente!')
        self.stdout.write('📝 Credenciales de admin:')
        self.stdout.write('   Usuario: jhon_martinez')
        self.stdout.write('   Contraseña: estefania1')