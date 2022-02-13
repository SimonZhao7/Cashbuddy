from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import CreateCategoryForm
from .models import Category

# Create your views here.


@login_required
def create_category(request):
    form = CreateCategoryForm()
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('account:dashboard')
    return render(request, 'form.html', {'form': form, 'title': 'Create Category', 'btn_text': 'Create'})


@login_required
def delete_category(request, slug):
    try:
        category = Category.objects.get(id=Category.get_id(slug))
    except Category.DoesNotExist:
        return render(request, '404.html')
    
    request.user.budget += sum([transaction.amount for transaction in category.transaction_set.all()])
    request.user.save()
    category.delete()
    return redirect('categories:view')

@login_required
def view(request):
    categories = Category.objects.filter(user=request.user).order_by('name')
    paginator = Paginator(categories, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)
    return render(request, 'list_categories.html', {'page_obj': page_obj})


@login_required
def edit(request, slug):
    try: 
        category = Category.objects.get(id=Category.get_id(slug))
    except Category.DoesNotExist:
        return render(request, '404.html')
    
    form = CreateCategoryForm(initial={
        'name': category.name
    })
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            form.update(category)
            return redirect('categories:view')
    return render(request, 'form.html', {'form': form, 'title': 'Edit Category', 'btn_text': 'Edit'})