from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tienda.models import Categoria, Producto, Testimonio, Marca

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
        
        # Crear marca principal
        marca, created = Marca.objects.get_or_create(
            nombre='TapiSuave',
            defaults={
                'descripcion': 'Marca líder en colchones de alta calidad',
                'activa': True
            }
        )
        if created:
            self.stdout.write(f'✅ Marca: {marca.nombre}')
        
        # Crear categorías (usando nombre como filtro para evitar duplicados)
        categorias_data = [
            {'nombre': 'Colchones Individuales', 'slug': 'individuales'},
            {'nombre': 'Colchones Dobles', 'slug': 'dobles'},
            {'nombre': 'Colchones Queen', 'slug': 'queen'},
            {'nombre': 'Colchones King', 'slug': 'king'},
        ]
        
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],  # Usar nombre como filtro
                defaults={
                    'slug': cat_data['slug'],
                    'descripcion': f'Colchones {cat_data["nombre"].lower()}',
                    'activa': True
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
                    'categoria': 'Colchones Individuales',
                    'descripcion_corta': 'Colchón individual de alta calidad',
                    'descripcion': 'Colchón individual de alta calidad con tecnología de espuma viscoelástica para un descanso reparador.',
                    'precio': 299000,
                    'tamano': 'sencillo',
                    'firmeza': 'medio',
                    'altura': 20,
                    'material_principal': 'Espuma viscoelástica',
                    'garantia_anos': 5,
                    'peso': 15.5,
                    'stock': 10
                },
                {
                    'nombre': 'Colchón TapiSuave Premium Doble',
                    'slug': 'colchon-tapisuave-premium-doble',
                    'categoria': 'Colchones Dobles',
                    'descripcion_corta': 'Colchón doble premium con resortes',
                    'descripcion': 'Colchón doble premium con sistema de resortes independientes y capa de gel refrescante.',
                    'precio': 499000,
                    'tamano': 'doble',
                    'firmeza': 'medio',
                    'altura': 25,
                    'material_principal': 'Resortes independientes + Gel',
                    'garantia_anos': 7,
                    'peso': 25.0,
                    'stock': 8
                },
                {
                    'nombre': 'Colchón TapiSuave Deluxe Queen',
                    'slug': 'colchon-tapisuave-deluxe-queen',
                    'categoria': 'Colchones Queen',
                    'descripcion_corta': 'Colchón Queen con gel refrescante',
                    'descripcion': 'Colchón Queen size con tecnología de gel refrescante y soporte ergonómico avanzado.',
                    'precio': 699000,
                    'tamano': 'queen',
                    'firmeza': 'firme',
                    'altura': 30,
                    'material_principal': 'Gel refrescante + Memory foam',
                    'garantia_anos': 10,
                    'peso': 35.0,
                    'stock': 5
                },
                {
                    'nombre': 'Colchón TapiSuave Royal King',
                    'slug': 'colchon-tapisuave-royal-king',
                    'categoria': 'Colchones King',
                    'descripcion_corta': 'Colchón King de lujo premium',
                    'descripcion': 'Colchón King size de lujo con múltiples capas de confort y tecnología anti-ácaros.',
                    'precio': 899000,
                    'tamano': 'king',
                    'firmeza': 'medio',
                    'altura': 35,
                    'material_principal': 'Múltiples capas + Anti-ácaros',
                    'garantia_anos': 12,
                    'peso': 45.0,
                    'stock': 3
                },
            ]
            
            for prod_data in productos_data:
                categoria = Categoria.objects.get(nombre=prod_data['categoria'])
                producto = Producto.objects.create(
                    nombre=prod_data['nombre'],
                    slug=prod_data['slug'],
                    categoria=categoria,
                    marca=marca,
                    descripcion_corta=prod_data['descripcion_corta'],
                    descripcion=prod_data['descripcion'],
                    precio=prod_data['precio'],
                    tamano=prod_data['tamano'],
                    firmeza=prod_data['firmeza'],
                    altura=prod_data['altura'],
                    material_principal=prod_data['material_principal'],
                    garantia_anos=prod_data['garantia_anos'],
                    peso=prod_data['peso'],
                    stock=prod_data['stock'],
                    activo=True,
                    destacado=True
                )
                self.stdout.write(f'✅ Producto: {producto.nombre}')
        
        # Crear testimonios (usando los campos correctos del modelo)
        if not Testimonio.objects.exists():
            testimonios_data = [
                {
                    'nombre': 'María González',
                    'ciudad': 'Bogotá',
                    'comentario': 'Excelente calidad, duermo mucho mejor desde que compré mi colchón TapiSuave. La diferencia es notable.',
                    'calificacion': 5
                },
                {
                    'nombre': 'Carlos Rodríguez',
                    'ciudad': 'Medellín',
                    'comentario': 'La mejor inversión para mi descanso. El colchón es súper cómodo y la atención al cliente excelente.',
                    'calificacion': 5
                },
                {
                    'nombre': 'Ana Martínez',
                    'ciudad': 'Cali',
                    'comentario': 'Llevamos 2 años con nuestro colchón TapiSuave y sigue como nuevo. Totalmente recomendado.',
                    'calificacion': 5
                },
            ]
            
            for test_data in testimonios_data:
                Testimonio.objects.create(
                    nombre=test_data['nombre'],
                    ciudad=test_data['ciudad'],
                    comentario=test_data['comentario'],  # Campo correcto: 'comentario' no 'testimonio'
                    calificacion=test_data['calificacion'],
                    activo=True
                )
                self.stdout.write(f'✅ Testimonio: {test_data["nombre"]}')
        
        self.stdout.write('🎉 ¡Configuración completada exitosamente!')
        self.stdout.write('📝 Credenciales de admin:')
        self.stdout.write('   Usuario: jhon_martinez')
        self.stdout.write('   Contraseña: estefania1')