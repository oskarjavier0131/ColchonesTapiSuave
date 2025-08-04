from tienda.models import Producto, Testimonio, Categoria, Newsletter
from tienda.forms import NewsletterForm

print("=== DEPURACIÓN DE DATOS ===")

# Verificar productos destacados
productos_destacados = Producto.objects.filter(destacado=True, activo=True)[:8]
print(f"Productos destacados encontrados: {productos_destacados.count()}")
for p in productos_destacados:
    print(f"  - {p.nombre} (destacado: {p.destacado}, activo: {p.activo})")

# Verificar testimonios
testimonios = Testimonio.objects.filter(activo=True)[:6]
print(f"\nTestimonios encontrados: {testimonios.count()}")
for t in testimonios:
    print(f"  - {t.nombre} (activo: {t.activo})")

# Verificar categorías
categorias = Categoria.objects.filter(activa=True)
print(f"\nCategorías encontradas: {categorias.count()}")
for c in categorias:
    print(f"  - {c.nombre} (activa: {c.activa})")

# Verificar formulario
try:
    form = NewsletterForm()
    print(f"\nFormulario NewsletterForm: OK")
except Exception as e:
    print(f"\nError en NewsletterForm: {e}")

print("\n=== FIN DEPURACIÓN ===")