import select

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout


# Контроллеры - классы


class HomeNews(ListView):
    model = News  # Указание модели
    template_name = 'news/home_news_list.html'  # Путь к шаблону
    context_object_name = 'news'  # Заменить дефолтное название
    paginate_by = 2

    # extra_context = {'title': 'Главная'} # Передача доп данных (лучше только для статик файлов)

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['title'] = 'Главная страница'
        return contex

    def get_queryset(self):  # Указываем нужные получаемые обьекты (В данном случае, только все опубликованные)
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    model = News  # Указание модели
    template_name = 'news/home_news_list.html'  # Путь к шаблону
    context_object_name = 'news'  # Заменить дефолтное название
    allow_empty = False  # Разрешать / запрещать показы пустых списков
    paginate_by = 2

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return contex


class ViewNews(DetailView):
    model = News
    # pk_url_kwarg = 'news_id'
    # template_name = 'news/news_detail.html'  # Путь к шаблону
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'  # Путь к шаблону
    # success_url = reverse_lazy('home') # Изменение дефолтного пути редиректа
    # login_url = '/admin/'
    raise_exception = True


# Контроллеры - функции

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте правильность заполнения формы')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')




# def test(request): # Постраничная навигация (Пагинация)
#     objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6', 'george7']
#     paginator = Paginator(objects, 2)
#     page_num = request.GET.get('page', 1)
#     page_objects = paginator.get_page(page_num)
#     return render(request, 'news/test.html', {'page_obj': page_objects})


# def index(request):
#     news = News.objects.all()
#     context = {'news': news,
#                'title': 'Список новостей',
#                }
#     return render(request, template_name='news/index.html', context=context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {"news": news, 'category': category})


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {"news_item": news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # news = News.objects.create(**form.cleaned_data)
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
