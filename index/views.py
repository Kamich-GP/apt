from django.shortcuts import render
from .models import Category, Product


# Create your views here.
def home_page(request):
    # Достаем данные из БД
    categories = Category.objects.all()
    products = Product.objects.all()

    # Отправляем данные на фронт
    context = {'products': products, 'categories': categories}

    return render(request, 'home.html', context)
