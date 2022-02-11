from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CreateCategoryForm

# Create your views here.


@login_required
def create_category(request):
    form = CreateCategoryForm()
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
    return render(request, 'create_category.html', {'form': form})
    