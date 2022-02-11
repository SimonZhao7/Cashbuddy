from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
            return redirect('account:home')
    return render(request, 'create_category.html', {'form': form})


@login_required
def delete_category(request, slug):
    try:
        category = Category.objects.get(id=Category.get_id(slug))
    except Category.DoesNotExist:
        return render(request, '404.html')
    
    category.delete()
    return redirect('account:home')
    