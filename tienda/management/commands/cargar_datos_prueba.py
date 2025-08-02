from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from tienda.models import Categoria, Marca, Producto, Testimonio, Contacto, Newsletter
import random
from datetime import datetime, timedelta
import sys

class Command(BaseCommand):
    help = 'Carga datos de prueba para ColchonesTapiSuave'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Elimina todos los datos existentes antes de cargar',
        )

    def handle(self, *args, **options):
        self.stdout.write("🚀 Iniciando carga de datos de prueba para ColchonesTapiSuave...")
        self.stdout.write("="*60)

        # Limpiar datos existentes si se especifica
        if options['limpiar']:
            self.stdout.write("🗑️ Limpiando datos existentes...")
            Testimonio.objects.all().delete()
            Newsletter.objects.all().delete()
            Contacto.objects.all().delete()
            Producto.objects.all().delete()
            Marca.objects.all().delete()
            Categoria.objects.all().delete()
            self.stdout.write("   ✅ Datos eliminados")

        try:
            # 1. Crear categorías
            self.crear_categorias()
            
            # 2. Crear marcas
            self.crear_marcas()
            
            # 3. Crear productos
            self.crear_productos()
            
            # 4. Crear testimonios
            self.crear_testimonios()
            
            # 5. Crear contactos
            self.crear_contactos()
            
            # 6. Crear newsletter
            self.crear_newsletter()
            
            # 7. Mostrar resumen
            self.mostrar_resumen()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error durante la carga: {str(e)}')
            )
            sys.exit(1)

    def crear_categorias(self):
        self.stdout.write("📂 Creando categorías...")
        
        categorias_data = [
            {
                'nombre': 'Colchones Matrimoniales',
                'descripcion': 'Colchones para parejas que buscan comodidad y espacio. Tamaños Queen y King.',
                'orden': 1
            },
            {
                'nombre': 'Colchones Individuales',
                'descripcion': 'Perfectos para habitaciones individuales. Tamaños sencillo y semidoble.',
                'orden': 2
            },
            {
                'nombre': 'Colchones Premium',
                'descripcion': 'Nuestra línea de lujo con materiales premium y tecnología avanzada.',
                'orden': 3
            },
            {
                'nombre': 'Colchones Ortopédicos',
                'descripcion': 'Diseñados especialmente para el cuidado de la columna vertebral.',
                'orden': 4
            },
        ]

        self.categorias = {}
        for cat_data in categorias_data:
            categoria, created = Categoria.objects.get_or_create(
                nombre=cat_data['nombre'],
                defaults={
                    'descripcion': cat_data['descripcion'],
                    'orden': cat_data['orden'],
                    'activa': True,
                }
            )
            self.categorias[cat_data['nombre']] = categoria
            status = "✅ Creada" if created else "ℹ️ Ya existe"
            self.stdout.write(f"   {status}: {categoria.nombre}")

    def crear_marcas(self):
        self.stdout.write("\n🏷️ Creando marcas...")
        
        marcas_data = [
            {
                'nombre': 'TapiSuave',
                'descripcion': 'Nuestra marca principal de colchones de calidad superior.',
            },
            {
                'nombre': 'DreamComfort',
                'descripcion': 'Línea premium para el descanso perfecto.',
            },
            {
                'nombre': 'OrthoRest',
                'descripcion': 'Especialistas en colchones ortopédicos y terapéuticos.',
            },
            {
                'nombre': 'EcoSleep',
                'descripcion': 'Colchones ecológicos fabricados con materiales naturales.',
            },
        ]

        self.marcas = {}
        for marca_data in marcas_data:
            marca, created = Marca.objects.get_or_create(
                nombre=marca_data['nombre'],
                defaults={
                    'descripcion': marca_data['descripcion'],
                    'activa': True,
                }
            )
            self.marcas[marca_data['nombre']] = marca
            status = "✅ Creada" if created else "ℹ️ Ya existe"
            self.stdout.write(f"   {status}: {marca.nombre}")

    def crear_productos(self):
        self.stdout.write("\n🛏️ Creando productos...")
        
        productos_data = [
            # Colchones Matrimoniales
            {
                'nombre': 'Colchón King TapiSuave Premium',
                'categoria': 'Colchones Matrimoniales',
                'marca': 'TapiSuave',
                'descripcion_corta': 'Colchón King Size de lujo con memory foam y tecnología de enfriamiento.',
                'descripcion': '''
                <h3>Colchón King TapiSuave Premium</h3>
                <p>Experimenta el máximo confort con nuestro colchón King Size Premium. Fabricado con materiales de la más alta calidad, incluye:</p>
                <ul>
                    <li><strong>Memory Foam de Alta Densidad:</strong> Se adapta perfectamente a tu cuerpo</li>
                    <li><strong>Tecnología de Enfriamiento:</strong> Mantiene la temperatura ideal durante la noche</li>
                    <li><strong>Base de Resortes Ensacados:</strong> Soporte independiente para cada área del cuerpo</li>
                    <li><strong>Funda Hipoalergénica:</strong> Protege contra ácaros y bacterias</li>
                </ul>
                <p>Ideal para parejas que buscan el máximo lujo y confort en su descanso.</p>
                ''',
                'tamano': 'king',
                'firmeza': 'medio',
                'altura': 30,
                'material_principal': 'Memory Foam Premium',
                'garantia_anos': 10,
                'precio': 2500000,
                'precio_descuento': 1999000,
                'stock': 15,
                'peso': 45.5,
                'destacado': True,
            },
            {
                'nombre': 'Colchón Queen DreamComfort Deluxe',
                'categoria': 'Colchones Matrimoniales',
                'marca': 'DreamComfort',
                'descripcion_corta': 'Colchón Queen con tecnología de soporte zonal y materiales premium.',
                'descripcion': '''
                <h3>Colchón Queen DreamComfort Deluxe</h3>
                <p>Diseñado para brindar el soporte perfecto donde más lo necesitas:</p>
                <ul>
                    <li><strong>Soporte Zonal:</strong> Diferentes zonas de firmeza para cabeza, torso y piernas</li>
                    <li><strong>Látex Natural:</strong> Material transpirable y duradero</li>
                    <li><strong>Gel RefreshCool:</strong> Tecnología de enfriamiento avanzada</li>
                    <li><strong>Certificación Eco-Tex:</strong> Libre de químicos nocivos</li>
                </ul>
                ''',
                'tamano': 'queen',
                'firmeza': 'firme',
                'altura': 28,
                'material_principal': 'Látex Natural con Gel',
                'garantia_anos': 8,
                'precio': 1800000,
                'precio_descuento': 1440000,
                'stock': 22,
                'peso': 38.0,
                'destacado': True,
            },
            {
                'nombre': 'Colchón Doble TapiSuave Classic',
                'categoria': 'Colchones Matrimoniales',
                'marca': 'TapiSuave',
                'descripcion_corta': 'Nuestro bestseller. Calidad comprobada y precio accesible.',
                'descripcion': '''
                <h3>Colchón Doble TapiSuave Classic</h3>
                <p>El favorito de nuestros clientes por más de 10 años:</p>
                <ul>
                    <li><strong>Resortes Bonnell:</strong> Sistema tradicional de probada durabilidad</li>
                    <li><strong>Acolchado Suave:</strong> Capa de confort superior</li>
                    <li><strong>Borde Wire:</strong> Refuerzo perimetral para mayor durabilidad</li>
                    <li><strong>Garantía Extendida:</strong> Respaldado por años de experiencia</li>
                </ul>
                ''',
                'tamano': 'doble',
                'firmeza': 'medio',
                'altura': 24,
                'material_principal': 'Resortes Bonnell + Espuma',
                'garantia_anos': 6,
                'precio': 980000,
                'precio_descuento': 784000,
                'stock': 40,
                'peso': 32.0,
                'destacado': True,
            },
            
            # Colchones Individuales
            {
                'nombre': 'Colchón Semidoble Comfort Plus',
                'categoria': 'Colchones Individuales',
                'marca': 'TapiSuave',
                'descripcion_corta': 'Ideal para habitaciones juveniles y de huéspedes. Excelente relación calidad-precio.',
                'descripcion': '''
                <h3>Colchón Semidoble Comfort Plus</h3>
                <p>Perfecto para espacios medianos, combina comodidad y durabilidad:</p>
                <ul>
                    <li><strong>Espuma de Alta Densidad:</strong> Soporte firme y duradero</li>
                    <li><strong>Pillow Top:</strong> Capa adicional de confort</li>
                    <li><strong>Borde Reforzado:</strong> Mayor durabilidad en los bordes</li>
                    <li><strong>Funda Desmontable:</strong> Fácil limpieza y mantenimiento</li>
                </ul>
                ''',
                'tamano': 'semi',
                'firmeza': 'medio',
                'altura': 25,
                'material_principal': 'Espuma HR + Pillow Top',
                'garantia_anos': 5,
                'precio': 899000,
                'precio_descuento': None,
                'stock': 35,
                'peso': 25.0,
                'destacado': False,
            },
            {
                'nombre': 'Colchón Sencillo EcoSleep Natural',
                'categoria': 'Colchones Individuales',
                'marca': 'EcoSleep',
                'descripcion_corta': 'Colchón ecológico fabricado con materiales 100% naturales y sostenibles.',
                'descripcion': '''
                <h3>Colchón Sencillo EcoSleep Natural</h3>
                <p>Cuida del planeta mientras cuidas tu descanso:</p>
                <ul>
                    <li><strong>Fibra de Coco:</strong> Material natural y transpirable</li>
                    <li><strong>Látex 100% Natural:</strong> Extraído de árboles de caucho</li>
                    <li><strong>Algodón Orgánico:</strong> Funda certificada GOTS</li>
                    <li><strong>Sin Químicos:</strong> Libre de pegamentos y tratamientos tóxicos</li>
                </ul>
                ''',
                'tamano': 'sencillo',
                'firmeza': 'firme',
                'altura': 22,
                'material_principal': 'Látex Natural + Fibra de Coco',
                'garantia_anos': 7,
                'precio': 750000,
                'precio_descuento': 675000,
                'stock': 28,
                'peso': 18.5,
                'destacado': True,
            },
            {
                'nombre': 'Colchón Sencillo Basic Comfort',
                'categoria': 'Colchones Individuales',
                'marca': 'TapiSuave',
                'descripcion_corta': 'Opción económica sin comprometer la calidad. Ideal para habitaciones auxiliares.',
                'descripcion': '''
                <h3>Colchón Sencillo Basic Comfort</h3>
                <p>Calidad TapiSuave al mejor precio:</p>
                <ul>
                    <li><strong>Espuma de Densidad Balanceada:</strong> Confort y soporte adecuados</li>
                    <li><strong>Funda Intercambiable:</strong> Facilita la limpieza</li>
                    <li><strong>Diseño Compacto:</strong> Perfecto para espacios pequeños</li>
                    <li><strong>Fabricación Nacional:</strong> Producto 100% colombiano</li>
                </ul>
                ''',
                'tamano': 'sencillo',
                'firmeza': 'firme',
                'altura': 20,
                'material_principal': 'Espuma HR Densidad Media',
                'garantia_anos': 3,
                'precio': 450000,
                'precio_descuento': None,
                'stock': 50,
                'peso': 15.0,
                'destacado': False,
            },
            
            # Colchones Premium
            {
                'nombre': 'Colchón King DreamComfort Luxury',
                'categoria': 'Colchones Premium',
                'marca': 'DreamComfort',
                'descripcion_corta': 'La experiencia de lujo definitiva. Tecnología de punta y materiales exclusivos.',
                'descripcion': '''
                <h3>Colchón King DreamComfort Luxury</h3>
                <p>El summum del lujo en descanso. Cada detalle ha sido pensado para tu comodidad:</p>
                <ul>
                    <li><strong>Memory Foam Viscoelástico:</strong> 7cm de capa superior premium</li>
                    <li><strong>Micro Resortes Titanium:</strong> 2000 resortes ensacados de titanio</li>
                    <li><strong>Bamboo Charcoal:</strong> Propiedades antibacteriales naturales</li>
                    <li><strong>Cashmere Cover:</strong> Funda de lana de cashmere ultra suave</li>
                    <li><strong>Edge Support Pro:</strong> Soporte reforzado en todo el perímetro</li>
                </ul>
                <p><em>Incluye base dividida y almohadas de regalo.</em></p>
                ''',
                'tamano': 'king',
                'firmeza': 'medio',
                'altura': 35,
                'material_principal': 'Memory Foam + Titanium Springs',
                'garantia_anos': 15,
                'precio': 4500000,
                'precio_descuento': 3600000,
                'stock': 8,
                'peso': 55.0,
                'destacado': True,
            },
            {
                'nombre': 'Colchón King EcoSleep Bamboo',
                'categoria': 'Colchones Premium',
                'marca': 'EcoSleep',
                'descripcion_corta': 'Lujo sostenible con fibras de bamboo y materiales ecológicos.',
                'descripcion': '''
                <h3>Colchón King EcoSleep Bamboo</h3>
                <p>Lujo y sostenibilidad en perfecta armonía:</p>
                <ul>
                    <li><strong>Fibra de Bamboo:</strong> Naturalmente antibacterial</li>
                    <li><strong>Latex Orgánico:</strong> Certificado FSC</li>
                    <li><strong>Carbón Activado:</strong> Absorbe humedad y olores</li>
                    <li><strong>Packaging Reciclable:</strong> Compromiso total con el medio ambiente</li>
                </ul>
                ''',
                'tamano': 'king',
                'firmeza': 'medio',
                'altura': 30,
                'material_principal': 'Bamboo + Látex Orgánico',
                'garantia_anos': 9,
                'precio': 3500000,
                'precio_descuento': 2800000,
                'stock': 10,
                'peso': 48.0,
                'destacado': True,
            },
            
            # Colchones Ortopédicos
            {
                'nombre': 'Colchón Queen OrthoRest Terapéutico',
                'categoria': 'Colchones Ortopédicos',
                'marca': 'OrthoRest',
                'descripcion_corta': 'Diseñado por especialistas para el cuidado de la columna vertebral.',
                'descripcion': '''
                <h3>Colchón Queen OrthoRest Terapéutico</h3>
                <p>Desarrollado en colaboración con fisioterapeutas y especialistas en columna:</p>
                <ul>
                    <li><strong>Soporte Lumbar Reforzado:</strong> Zona central con mayor firmeza</li>
                    <li><strong>Alineación Espinal:</strong> Mantiene la curvatura natural de la espalda</li>
                    <li><strong>Memory Foam Médico:</strong> Alivia puntos de presión</li>
                    <li><strong>Certificación Médica:</strong> Recomendado por ortopedistas</li>
                </ul>
                ''',
                'tamano': 'queen',
                'firmeza': 'extra_firme',
                'altura': 28,
                'material_principal': 'Espuma Ortopédica HR',
                'garantia_anos': 10,
                'precio': 2100000,
                'precio_descuento': 1890000,
                'stock': 18,
                'peso': 40.0,
                'destacado': True,
            },
            {
                'nombre': 'Colchón Queen Premium OrthoRest Pro',
                'categoria': 'Colchones Ortopédicos',
                'marca': 'OrthoRest',
                'descripcion_corta': 'Tecnología avanzada para problemas de espalda. Recomendado por especialistas.',
                'descripcion': '''
                <h3>Colchón Queen Premium OrthoRest Pro</h3>
                <p>Solución profesional para problemas de espalda:</p>
                <ul>
                    <li><strong>7 Zonas Diferenciadas:</strong> Soporte específico para cada parte del cuerpo</li>
                    <li><strong>Memory Foam Termorregulador:</strong> Se adapta a tu temperatura corporal</li>
                    <li><strong>Capa Visco-Gel:</strong> Máximo alivio de puntos de presión</li>
                    <li><strong>Certificación Médica Plus:</strong> Estudios clínicos que avalan su eficacia</li>
                </ul>
                ''',
                'tamano': 'queen',
                'firmeza': 'extra_firme',
                'altura': 33,
                'material_principal': 'Memory Foam Médico + Gel',
                'garantia_anos': 12,
                'precio': 2800000,
                'precio_descuento': 2240000,
                'stock': 14,
                'peso': 44.0,
                'destacado': True,
            }
        ]

        productos_creados = 0
        productos_actualizados = 0
        
        for prod_data in productos_data:
            categoria = self.categorias[prod_data['categoria']]
            marca = self.marcas[prod_data['marca']]
            
            producto, created = Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults={
                    'categoria': categoria,
                    'marca': marca,
                    'descripcion_corta': prod_data['descripcion_corta'],
                    'descripcion': prod_data['descripcion'],
                    'tamano': prod_data['tamano'],
                    'firmeza': prod_data['firmeza'],
                    'altura': prod_data['altura'],
                    'material_principal': prod_data['material_principal'],
                    'garantia_anos': prod_data['garantia_anos'],
                    'precio': prod_data['precio'],
                    'precio_descuento': prod_data['precio_descuento'],
                    'stock': prod_data['stock'],
                    'peso': prod_data['peso'],
                    'destacado': prod_data['destacado'],
                    'activo': True,
                }
            )
            
            if created:
                productos_creados += 1
                status = "✅ Creado"
                if producto.destacado:
                    status += " ⭐"
                if producto.precio_descuento:
                    status += " 🏷️"
            else:
                productos_actualizados += 1
                status = "ℹ️ Ya existe"
            
            self.stdout.write(f"   {status}: {producto.nombre}")
        
        self.stdout.write(f"   📊 Total: {productos_creados} creados, {productos_actualizados} ya existían")

    def crear_testimonios(self):
        self.stdout.write("\n💬 Creando testimonios...")
        
        testimonios_data = [
            {
                'nombre': 'María González',
                'ciudad': 'Bogotá',
                'comentario': 'Increíble la diferencia que hizo el colchón TapiSuave en mi descanso. Ya no me levanto con dolor de espalda y duermo toda la noche sin interrupciones. Lo recomiendo 100%.',
                'calificacion': 5,
                'producto': 'Colchón King TapiSuave Premium'
            },
            {
                'nombre': 'Carlos Rodríguez',
                'ciudad': 'Medellín',
                'comentario': 'Excelente servicio al cliente y el colchón llegó en perfecto estado. La calidad es notable y el precio muy competitivo. Mi esposa y yo estamos encantados.',
                'calificacion': 5,
                'producto': 'Colchón Queen DreamComfort Deluxe'
            },
            {
                'nombre': 'Ana Patricia Herrera',
                'ciudad': 'Cali',
                'comentario': 'Compré el colchón para mi hijo adolescente y ha sido una excelente inversión. Su postura ha mejorado notablemente y duerme mucho mejor.',
                'calificacion': 4,
                'producto': 'Colchón Semidoble Comfort Plus'
            },
            {
                'nombre': 'Roberto Martínez',
                'ciudad': 'Barranquilla',
                'comentario': 'Como persona con problemas de columna, este colchón ha sido una bendición. El soporte es perfecto y he notado una gran mejora en mis dolores.',
                'calificacion': 5,
                'producto': 'Colchón Queen OrthoRest Terapéutico'
            },
            {
                'nombre': 'Lucía Fernández',
                'ciudad': 'Bucaramanga',
                'comentario': 'Me encanta que sea un producto ecológico sin sacrificar comodidad. Se siente genial saber que estoy cuidando el planeta mientras duermo bien.',
                'calificacion': 4,
                'producto': 'Colchón King EcoSleep Bamboo'
            },
            {
                'nombre': 'Diego Vargas',
                'ciudad': 'Pereira',
                'comentario': 'Relación calidad-precio excelente. Es mi segundo colchón TapiSuave y la calidad sigue siendo la misma. Durabilidad garantizada.',
                'calificacion': 4,
                'producto': 'Colchón Doble TapiSuave Classic'
            },
        ]

        testimonios_creados = 0
        for testimonio_data in testimonios_data:
            # Buscar el producto asociado
            try:
                producto = Producto.objects.get(nombre=testimonio_data['producto'])
            except Producto.DoesNotExist:
                producto = None
            
            # Generar fecha aleatoria en los últimos 6 meses
            fecha_base = datetime.now() - timedelta(days=180)
            fecha_random = fecha_base + timedelta(days=random.randint(0, 180))
            
            testimonio, created = Testimonio.objects.get_or_create(
                nombre=testimonio_data['nombre'],
                comentario=testimonio_data['comentario'],
                defaults={
                    'ciudad': testimonio_data['ciudad'],
                    'calificacion': testimonio_data['calificacion'],
                    'producto': producto,
                    'fecha': fecha_random,
                    'activo': True,
                }
            )
            
            if created:
                testimonios_creados += 1
                status = "✅ Creado"
            else:
                status = "ℹ️ Ya existe"
            
            self.stdout.write(f"   {status}: {testimonio.nombre} - {testimonio.calificacion}⭐")
        
        self.stdout.write(f"   📊 Total: {testimonios_creados} creados")

    def crear_contactos(self):
        self.stdout.write("\n📧 Creando contactos de prueba...")
        
        contactos_data = [
            {
                'nombre': 'Jennifer López',
                'email': 'jennifer.lopez@email.com',
                'telefono': '3201234567',
                'ciudad': 'Bogotá',
                'asunto': 'consulta_producto',
                'mensaje': 'Hola, estoy interesada en conocer más sobre los colchones ortopédicos. Tengo problemas de lumbalgia y necesito una recomendación específica.',
                'respondido': False
            },
            {
                'nombre': 'Alexander García',
                'email': 'alex.garcia@empresa.com',
                'telefono': '3156789012',
                'ciudad': 'Medellín',
                'asunto': 'cotizacion',
                'mensaje': 'Buenos días, necesito cotización para equipar un hotel de 50 habitaciones. Por favor envíenme información sobre descuentos por volumen.',
                'respondido': True
            },
            {
                'nombre': 'Miguel Torres',
                'email': 'miguel.torres@hotmail.com',
                'telefono': '3124567890',
                'ciudad': 'Barranquilla',
                'asunto': 'envio',
                'mensaje': 'Quiero saber si realizan envíos a zonas rurales. Vivo a 45 minutos del centro de Barranquilla.',
                'respondido': False
            }
        ]

        contactos_creados = 0
        for contacto_data in contactos_data:
            # Generar fecha aleatoria en el último mes
            fecha_base = datetime.now() - timedelta(days=30)
            fecha_random = fecha_base + timedelta(days=random.randint(0, 30))
            
            contacto, created = Contacto.objects.get_or_create(
                email=contacto_data['email'],
                defaults={
                    'nombre': contacto_data['nombre'],
                    'telefono': contacto_data['telefono'],
                    'ciudad': contacto_data['ciudad'],
                    'asunto': contacto_data['asunto'],
                    'mensaje': contacto_data['mensaje'],
                    'acepto_terminos': True,
                    'fecha_creacion': fecha_random,
                    'respondido': contacto_data['respondido'],
                }
            )
            
            if created:
                contactos_creados += 1
                status = "✅ Creado"
            else:
                status = "ℹ️ Ya existe"
            
            self.stdout.write(f"   {status}: {contacto.nombre} - {contacto.get_asunto_display()}")
        
        self.stdout.write(f"   📊 Total: {contactos_creados} creados")

    def crear_newsletter(self):
        self.stdout.write("\n📰 Creando suscriptores newsletter...")
        
        newsletters_data = [
            {'email': 'cliente1@gmail.com', 'nombre': 'Andrea Sánchez'},
            {'email': 'cliente2@hotmail.com', 'nombre': 'José Mendoza'},
            {'email': 'cliente3@yahoo.com', 'nombre': 'Laura Peña'},
            {'email': 'cliente4@outlook.com', 'nombre': 'Carlos Restrepo'},
            {'email': 'cliente5@empresa.co', 'nombre': 'Diana Ospina'},
        ]

        newsletters_creados = 0
        for newsletter_data in newsletters_data:
            # Generar fecha aleatoria en los últimos 3 meses
            fecha_base = datetime.now() - timedelta(days=90)
            fecha_random = fecha_base + timedelta(days=random.randint(0, 90))
            
            newsletter, created = Newsletter.objects.get_or_create(
                email=newsletter_data['email'],
                defaults={
                    'nombre': newsletter_data['nombre'],
                    'activo': True,
                    'fecha_suscripcion': fecha_random,
                }
            )
            
            if created:
                newsletters_creados += 1
                status = "✅ Creado"
            else:
                status = "ℹ️ Ya existe"
            
            self.stdout.write(f"   {status}: {newsletter.email}")
        
        self.stdout.write(f"   📊 Total: {newsletters_creados} creados")

    def mostrar_resumen(self):
        self.stdout.write("\n" + "="*60)
        self.stdout.write(
            self.style.SUCCESS("🎉 ¡CARGA DE DATOS COMPLETADA EXITOSAMENTE!")
        )
        self.stdout.write("="*60)
        
        # Estadísticas actuales
        self.stdout.write(f"📂 Categorías: {Categoria.objects.count()}")
        self.stdout.write(f"🏷️ Marcas: {Marca.objects.count()}")
        self.stdout.write(f"🛏️ Productos: {Producto.objects.count()}")
        self.stdout.write(f"   • Destacados: {Producto.objects.filter(destacado=True).count()}")
        self.stdout.write(f"   • Con descuento: {Producto.objects.filter(precio_descuento__isnull=False).count()}")
        self.stdout.write(f"💬 Testimonios: {Testimonio.objects.count()}")
        self.stdout.write(f"📧 Contactos: {Contacto.objects.count()}")
        self.stdout.write(f"📰 Newsletter: {Newsletter.objects.count()}")

        self.stdout.write("\n🚀 PRÓXIMOS PASOS:")
        self.stdout.write("1. Ve al admin: http://127.0.0.1:8000/admin/")
        self.stdout.write("2. Revisa los productos creados")
        self.stdout.write("3. Prueba la tienda: http://127.0.0.1:8000/")
        self.stdout.write("4. Testa el widget de WhatsApp")

        self.stdout.write(
            self.style.SUCCESS("\n✅ TU TIENDA ESTÁ LISTA PARA USAR!")
        )