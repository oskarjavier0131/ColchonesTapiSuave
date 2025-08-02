from .models import Categoria

def categorias_context(request):
    return {
        'categorias_menu': Categoria.objects.filter(activa=True)
    }