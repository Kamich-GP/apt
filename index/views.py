from django.shortcuts import render
from .models import Category, Product


# Create your views here.
# Главная страница
def home_page(request):
    # Достаем данные из БД
    categories = Category.objects.all()
    products = Product.objects.all()

    # Отправляем данные на фронт
    context = {'products': products, 'categories': categories}

    return render(request, 'home.html', context)


# Вывод информации о конкретном продукте
def product_page(request, pk):
    # Достаем данные из БД
    product = Product.objects.get(id=pk)

    # Отправляем данные на фронт
    context = {'product': product}

    return render(request, 'product.html', context)


# Вывод товаров по категории
def category_page(request, pk):
    # Достаем данные из БД
    category = Category.objects.get(id=pk)
    products = Product.objects.filter(product_category=category)

    # Передаем данные на фронт
    context = {'category': category, 'products': products}

    return render(request, 'category.html', context)
