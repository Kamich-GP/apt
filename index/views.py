from django.shortcuts import render, redirect
from .models import Category, Product
from .forms import RegForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views import View


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


# Поиск товара
def search_product(request):
    if request.method == "POST":
        get_product = request.POST.get('search_product')

        searched_products = Product.objects.filter(product_name__iregex=get_product)

        if searched_products:
            context = {'products': searched_products}

            return render(request, 'result.html', context)
        else:
            return redirect('/')


# Регистрация
class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {'form': RegForm}

        return render(request, self.template_name, context)


    def post(self, request):
        form = RegForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password2')

            user = User.objects.create_user(username=username,
                                     email=email,
                                     password=password)
            user.save()

            login(request, user)

            return redirect('/')



