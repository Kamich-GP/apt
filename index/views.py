from django.shortcuts import render, redirect
from .models import Category, Product, Cart
from .forms import RegForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views import View
import telebot


# Создаем объект бота
bot = telebot.TeleBot('7805051129:AAG4As3B6rEmKfsfpJ5r7TTYrUIBho9A9jQ')


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


# Выход из аккаунта
def logout_view(request):
    logout(request)
    return redirect('/')


# Добавление товара в корзину
def to_cart(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        if 0 < int(request.POST.get('pr_count')) <= product.product_count:
            Cart.objects.create(user_id=request.user.id,
                                user_product=product,
                                user_pr_count=int(request.POST.get('pr_count'))).save()

            return redirect('/')
        return redirect(f'/products/{pk}')


# Удаление товара из корзины
def del_from_cart(request, pk):
    product_to_del = Product.objects.get(id=pk)
    Cart.objects.filter(user_product=product_to_del).delete()

    return redirect('/cart')


# Отображение корзины
def cart(request):
    user_cart = Cart.objects.filter(user_id=request.user.id)

    product_ids = [p.user_product.id for p in user_cart]
    product_counts = [p.user_product.product_count for p in user_cart]
    user_pr_counts = [p.user_pr_count for p in user_cart]

    totals = [round(t.user_pr_count * t.user_product.product_price, 2) for t in user_cart]
    text = (f'Новый заказ!\n\n'
            f'Клиент: {User.objects.get(id=request.user.id).email}\n\n')


    if request.method == 'POST':
        for i in range(len(product_ids)):
            product = Product.objects.get(id=product_ids[i])
            product.product_count = product_counts[i] - user_pr_counts[i]
            product.save(update_fields=['product_count'])

        for t in user_cart:
            text += (f'Товар: {t.user_product}\n'
                     f'Количество: {t.user_pr_count}\n\n')

        text += f'Итого: ${round(sum(totals, 2))}'
        bot.send_message(6775701667, text)
        user_cart.delete()
        return redirect('/')

    context = {'cart': user_cart, 'total': round(sum(totals, 2))}
    return render(request, 'cart.html', context)
