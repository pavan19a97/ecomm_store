from .models import Category, Product

def menu_categories(request):
    categories = Category.objects.all()

    return {'menu_categories': categories}

